"""REST endpoints for receiving deliveries, two-view captures, dispositions and material lineage."""

import asyncio
import logging
import math
import os
from collections.abc import Iterator
from contextlib import contextmanager

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, selectinload

from app.api.auth import require_gate_token
from app.api.deps import get_db
from app.config import settings
from app.core.database import SessionLocal
from app.hardware.dual_conveyor_controller import (
    DualConveyorController,
    sample_image_source,
)
from app.models.delivery_trace import (
    DeliveryStatus,
    FishInspection,
    HumanDisposition,
    InspectionStatus,
    MaterialMovement,
    ReceivingDelivery,
)
from app.schemas.delivery_trace import (
    DeliveryCreate,
    DeliveryDetailResponse,
    DeliveryListResponse,
    DeliveryRead,
    DeliveryStatusT,
    DeliveryStatusUpdate,
    DeliverySummary,
    DeliveryTraceTreeResponse,
    FishInspectionRead,
    HumanDispositionCreate,
    HumanDispositionRead,
    LotProvenanceResponse,
    MaterialMovementCreate,
    MaterialMovementRead,
    SimulateRequest,
    ViewSideT,
)
from app.services import material_lineage_service, two_view_inspection_service
from app.services.errors import (
    CaptureBackpressureError,
    DeliveryServiceError,
    DeliveryStateError,
    InsufficientStorageError,
    InvalidImageError,
    NotFoundError,
    QuantityValidationError,
)

router = APIRouter()
logger = logging.getLogger(__name__)
_tasks: set[asyncio.Task] = set()

_STATUS_BY_ERROR: dict[type[DeliveryServiceError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    DeliveryStateError: status.HTTP_409_CONFLICT,
    QuantityValidationError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    InvalidImageError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    CaptureBackpressureError: status.HTTP_503_SERVICE_UNAVAILABLE,
    InsufficientStorageError: status.HTTP_507_INSUFFICIENT_STORAGE,
}


@contextmanager
def _service_errors() -> Iterator[None]:
    """Translate delivery service errors into HTTP responses."""
    try:
        yield
    except DeliveryServiceError as exc:
        raise HTTPException(status_code=_STATUS_BY_ERROR[type(exc)], detail=str(exc)) from exc


def _require_delivery(db: Session, delivery_id: str) -> ReceivingDelivery:
    delivery = db.get(ReceivingDelivery, delivery_id)
    if delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"delivery {delivery_id} not found")
    return delivery


def _counts_by_delivery(db: Session, delivery_ids: list[str]) -> dict[str, dict[str, int]]:
    """Return inspected, flagged and partial fish counts for each delivery in one grouped query."""
    rows = db.execute(
        select(
            FishInspection.delivery_id,
            func.count(),
            func.sum(case((FishInspection.flagged_for_review.is_(True), 1), else_=0)),
            func.sum(case((FishInspection.status != InspectionStatus.COMPLETE.value, 1), else_=0)),
        )
        .where(FishInspection.delivery_id.in_(delivery_ids))
        .group_by(FishInspection.delivery_id)
    )
    return {
        delivery_id: {"total_inspected": total, "flagged_count": flagged, "partial_count": partial}
        for delivery_id, total, flagged, partial in rows
    }


def _summary(delivery: ReceivingDelivery, counts: dict[str, dict[str, int]]) -> DeliverySummary:
    return DeliverySummary.model_validate(delivery).model_copy(update=counts.get(delivery.id, {}))


@router.post(
    "",
    response_model=DeliveryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create Receiving Delivery",
    description="Opens a delivery in active_receiving status and prepares its capture directory.",
)
def create_delivery(payload: DeliveryCreate, db: Session = Depends(get_db)):
    with _service_errors():
        two_view_inspection_service.ensure_capture_capacity()
        delivery = material_lineage_service.create_delivery(db, payload)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "captures", delivery.id), exist_ok=True)
    return DeliveryRead.model_validate(delivery)


@router.get(
    "",
    response_model=DeliveryListResponse,
    summary="List Receiving Deliveries",
    description="Returns deliveries newest first, with inspection counts, optionally filtered by status.",
)
def list_deliveries(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: DeliveryStatusT | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    conditions = [ReceivingDelivery.status == status_filter] if status_filter else []
    total = db.scalar(select(func.count()).select_from(ReceivingDelivery).where(*conditions))
    deliveries = db.scalars(
        select(ReceivingDelivery)
        .where(*conditions)
        .order_by(ReceivingDelivery.received_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    ).all()
    counts = _counts_by_delivery(db, [d.id for d in deliveries])
    return DeliveryListResponse(
        items=[_summary(d, counts) for d in deliveries],
        total=total,
        page=page,
        limit=limit,
        total_pages=math.ceil(total / limit),
    )


@router.get("/lots/{lot_id}/provenance", response_model=LotProvenanceResponse, summary="Get Lot Provenance")
def get_lot_provenance(lot_id: str, db: Session = Depends(get_db)):
    """Walk upstream from a lot to its receiving delivery and report broken links."""
    return material_lineage_service.get_lot_provenance(db, lot_id)


@router.get(
    "/{delivery_id}",
    response_model=DeliveryDetailResponse,
    summary="Get Delivery Detail",
    description="Returns one delivery with a page of its fish inspections, dispositions and movements.",
)
def get_delivery(
    delivery_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    two_view_inspection_service.reap_timed_out_captures(db, delivery_id)
    delivery = _require_delivery(db, delivery_id)

    inspections = db.scalars(
        select(FishInspection)
        .where(FishInspection.delivery_id == delivery_id)
        .options(selectinload(FishInspection.views))
        .order_by(FishInspection.sequence_in_delivery)
        .offset((page - 1) * limit)
        .limit(limit)
    ).all()
    inspections_total = db.scalar(
        select(func.count()).select_from(FishInspection).where(FishInspection.delivery_id == delivery_id)
    )

    dispositions = list(
        db.scalars(
            select(HumanDisposition)
            .where(HumanDisposition.delivery_id == delivery_id)
            .order_by(HumanDisposition.id)
        )
    )
    active_ids = {d.id for d in material_lineage_service.active_dispositions(dispositions)}
    movements = db.scalars(
        select(MaterialMovement)
        .where(MaterialMovement.delivery_id == delivery_id)
        .order_by(MaterialMovement.id)
    ).all()

    return DeliveryDetailResponse(
        delivery=_summary(delivery, _counts_by_delivery(db, [delivery_id])),
        inspections=[FishInspectionRead.model_validate(f) for f in inspections],
        inspections_total=inspections_total,
        page=page,
        limit=limit,
        dispositions=[
            HumanDispositionRead.model_validate(d).model_copy(update={"superseded": d.id not in active_ids})
            for d in dispositions
        ],
        movements=[MaterialMovementRead.model_validate(m) for m in movements],
    )


@router.patch(
    "/{delivery_id}/status",
    response_model=DeliveryRead,
    summary="Update Delivery Status",
    description="Moves a delivery along its allowed status transitions.",
)
def update_delivery_status(delivery_id: str, payload: DeliveryStatusUpdate, db: Session = Depends(get_db)):
    with _service_errors():
        if payload.status == DeliveryStatus.INSPECTION_COMPLETE.value:
            two_view_inspection_service.reap_timed_out_captures(db, delivery_id)
        delivery = material_lineage_service.transition_status(db, delivery_id, payload.status)
    return DeliveryRead.model_validate(delivery)


@router.post(
    "/{delivery_id}/capture-view",
    response_model=FishInspectionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Capture One Fish View",
    description="Runs inference on a dorsal or ventral image and pairs it with its fish.",
)
async def capture_view(
    delivery_id: str,
    image: UploadFile = File(...),
    view_side: ViewSideT = Form(...),
    sequence_in_delivery: int | None = Form(None),
    db: Session = Depends(get_db),
):
    image_bytes = await image.read()
    with _service_errors():
        fish = await two_view_inspection_service.handle_view_capture(
            db, delivery_id, view_side, image_bytes, sequence_in_delivery
        )
    return FishInspectionRead.model_validate(fish)


@router.post(
    "/{delivery_id}/dispositions",
    response_model=HumanDispositionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record Human Disposition",
    description="Records an accept, reject, reprocess or downgrade decision. Gate token only: people sign "
    "dispositions in the Switch room through qc-gate.",
    dependencies=[Depends(require_gate_token)],
)
def record_disposition(delivery_id: str, payload: HumanDispositionCreate, db: Session = Depends(get_db)):
    with _service_errors():
        disposition = material_lineage_service.record_disposition(db, delivery_id, payload)
    return HumanDispositionRead.model_validate(disposition)


@router.post(
    "/{delivery_id}/movements",
    response_model=MaterialMovementRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record Material Movement",
    description="Records one transformation or handoff stage. Gate token only: operators confirm "
    "movements in the Switch room through qc-gate.",
    dependencies=[Depends(require_gate_token)],
)
def record_movement(delivery_id: str, payload: MaterialMovementCreate, db: Session = Depends(get_db)):
    with _service_errors():
        movement = material_lineage_service.record_transformation_stage(db, delivery_id, payload)
    return MaterialMovementRead.model_validate(movement)


@router.get(
    "/{delivery_id}/trace",
    response_model=DeliveryTraceTreeResponse,
    summary="Get Delivery Trace Tree",
    description="Returns inspections, dispositions, movements, quantity balance and missing links.",
)
def get_delivery_trace(delivery_id: str, db: Session = Depends(get_db)):
    two_view_inspection_service.reap_timed_out_captures(db, delivery_id)
    with _service_errors():
        return material_lineage_service.get_delivery_lineage(db, delivery_id)


async def _run_simulation(delivery_id: str, payload: SimulateRequest) -> None:
    """Feed mock fish passes through the dual conveyor into the capture pipeline."""
    controller = DualConveyorController()
    source = sample_image_source(settings.UPLOAD_DIR)

    async def emit(side: str, data: bytes) -> None:
        session = SessionLocal()
        try:
            await two_view_inspection_service.handle_view_capture(session, delivery_id, side, data)
        finally:
            session.close()

    summary = await controller.run_mock_batch(payload.count, emit, source, payload.drop_ventral_every)
    logger.info("Mock simulation for delivery %s finished: %s", delivery_id, summary)


@router.post(
    "/{delivery_id}/simulate",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start Mock Conveyor Simulation",
    description="Runs simulated fish passes in the background for an active delivery (mock hardware only).",
)
async def simulate_deliveries(
    delivery_id: str,
    payload: SimulateRequest | None = None,
    db: Session = Depends(get_db),
):
    payload = payload or SimulateRequest()
    if not settings.ENABLE_MOCK_HARDWARE:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="mock hardware disabled")
    delivery = _require_delivery(db, delivery_id)
    if delivery.status != DeliveryStatus.ACTIVE_RECEIVING.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"delivery {delivery_id} is {delivery.status}, not active_receiving",
        )

    task = asyncio.create_task(_run_simulation(delivery_id, payload))
    _tasks.add(task)
    task.add_done_callback(_tasks.discard)
    return {"status": "started", "delivery_id": delivery_id, "count": payload.count}
