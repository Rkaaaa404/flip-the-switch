"""Material lineage and disposition accounting for receiving deliveries."""

import threading
from collections import Counter, defaultdict
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.delivery_trace import (
    DeliveryStatus,
    DispositionOutcome,
    FishInspection,
    HumanDisposition,
    InspectionStatus,
    MaterialMovement,
    ReceivingDelivery,
    utcnow,
)
from app.models.dispatch import Dispatch, DispatchLot
from app.models.storage_slot import StorageSlot
from app.schemas.delivery_trace import (
    DeliveryCreate,
    DeliveryRead,
    DeliveryTraceTreeResponse,
    DispatchRef,
    HumanDispositionCreate,
    HumanDispositionRead,
    InspectionSummary,
    LotProvenanceResponse,
    MaterialMovementCreate,
    MaterialMovementRead,
    MissingLink,
    MovementNode,
    QuantityBalance,
    StorageSlotRef,
)
from app.services.errors import (
    DeliveryStateError,
    NotFoundError,
    QuantityValidationError,
)

_LOCK = threading.Lock()
_EPS = 1e-9
_DISPOSITION_OPEN = (DeliveryStatus.INSPECTION_COMPLETE.value, DeliveryStatus.DISPOSITION_RECORDED.value)
_TRANSITIONS = {
    (DeliveryStatus.ACTIVE_RECEIVING.value, DeliveryStatus.INSPECTION_COMPLETE.value),
    (DeliveryStatus.DISPOSITION_RECORDED.value, DeliveryStatus.CLOSED.value),
}


def _get_delivery(db: Session, delivery_id: str) -> ReceivingDelivery:
    delivery = db.get(ReceivingDelivery, delivery_id)
    if delivery is None:
        raise NotFoundError(f"delivery {delivery_id} not found")
    return delivery


def _dispositions_of(db: Session, delivery_id: str) -> list[HumanDisposition]:
    return list(
        db.scalars(
            select(HumanDisposition)
            .where(HumanDisposition.delivery_id == delivery_id)
            .order_by(HumanDisposition.id)
        )
    )


def _movements_of(db: Session, delivery_id: str) -> list[MaterialMovement]:
    return list(
        db.scalars(
            select(MaterialMovement)
            .where(MaterialMovement.delivery_id == delivery_id)
            .order_by(MaterialMovement.id)
        )
    )


def _producer(db: Session, lot_id: str) -> MaterialMovement | None:
    return db.scalar(select(MaterialMovement).where(MaterialMovement.output_lot_id == lot_id))


def generate_delivery_id(db: Session, now: datetime | None = None) -> str:
    """Return the next DEL-YYYYMMDD-NNN id for the given date."""
    prefix = f"DEL-{(now or utcnow()):%Y%m%d}-"
    highest = 0
    for delivery_id in db.scalars(select(ReceivingDelivery.id).where(ReceivingDelivery.id.like(f"{prefix}%"))):
        try:
            highest = max(highest, int(delivery_id.rsplit("-", 1)[-1]))
        except ValueError:
            continue
    return f"{prefix}{highest + 1:03d}"


def create_delivery(db: Session, payload: DeliveryCreate, now: datetime | None = None) -> ReceivingDelivery:
    """Create a delivery in active_receiving status."""
    with _LOCK:
        delivery = ReceivingDelivery(
            **payload.model_dump(exclude={"received_at"}),
            id=generate_delivery_id(db, now),
            received_at=payload.received_at or now or utcnow(),
            status=DeliveryStatus.ACTIVE_RECEIVING.value,
        )
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery


def transition_status(db: Session, delivery_id: str, target: str) -> ReceivingDelivery:
    """Move a delivery along its allowed status transitions."""
    with _LOCK:
        delivery = _get_delivery(db, delivery_id)
        if (delivery.status, target) not in _TRANSITIONS:
            raise DeliveryStateError(f"cannot move from {delivery.status} to {target}")
        delivery.status = target
        db.commit()
        db.refresh(delivery)
        return delivery


def active_dispositions(dispositions: list[HumanDisposition]) -> list[HumanDisposition]:
    """Return dispositions that no other disposition supersedes."""
    superseded_ids = {d.supersedes_id for d in dispositions if d.supersedes_id is not None}
    return [d for d in dispositions if d.id not in superseded_ids]


def record_disposition(
    db: Session, delivery_id: str, payload: HumanDispositionCreate, now: datetime | None = None
) -> HumanDisposition:
    """Record a human disposition, optionally superseding an earlier one, within the stated quantity."""
    with _LOCK:
        delivery = _get_delivery(db, delivery_id)
        if delivery.status not in _DISPOSITION_OPEN:
            raise DeliveryStateError(f"cannot record a disposition while delivery is {delivery.status}")
        if payload.quantity_unit != delivery.quantity_unit:
            raise QuantityValidationError(
                f"unit {payload.quantity_unit} does not match delivery unit {delivery.quantity_unit}"
            )

        existing = _dispositions_of(db, delivery_id)
        active = active_dispositions(existing)
        if payload.supersedes_id is not None:
            target = next((d for d in existing if d.id == payload.supersedes_id), None)
            if target is None:
                raise NotFoundError(f"disposition {payload.supersedes_id} not found on delivery {delivery_id}")
            if target.id not in {d.id for d in active}:
                raise QuantityValidationError(f"disposition {target.id} is already superseded")
            active = [d for d in active if d.id != target.id]

        active_total = sum(d.affected_quantity for d in active)
        if active_total + payload.affected_quantity > delivery.stated_quantity + _EPS:
            raise QuantityValidationError(
                f"affected quantity {payload.affected_quantity} exceeds remaining quantity: "
                f"stated {delivery.stated_quantity}, already dispositioned {active_total}"
            )

        disposition = HumanDisposition(
            delivery_id=delivery_id,
            output_lot_id=payload.output_lot_id,
            disposition=payload.disposition,
            affected_quantity=payload.affected_quantity,
            quantity_unit=payload.quantity_unit,
            decision_reason=payload.decision_reason,
            authorized_by=payload.authorized_by,
            decided_at=now or utcnow(),
            supersedes_id=payload.supersedes_id,
        )
        db.add(disposition)
        if delivery.status == DeliveryStatus.INSPECTION_COMPLETE.value:
            delivery.status = DeliveryStatus.DISPOSITION_RECORDED.value
        db.commit()
        db.refresh(disposition)
        return disposition


def record_transformation_stage(
    db: Session, delivery_id: str, payload: MaterialMovementCreate, now: datetime | None = None
) -> MaterialMovement:
    """Record one material movement, enforcing that no input is overdrawn."""
    with _LOCK:
        delivery = _get_delivery(db, delivery_id)
        if delivery.status != DeliveryStatus.DISPOSITION_RECORDED.value:
            raise DeliveryStateError(f"cannot record a stage while delivery is {delivery.status}")
        if payload.quantity_unit != delivery.quantity_unit:
            raise QuantityValidationError(
                f"unit {payload.quantity_unit} does not match delivery unit {delivery.quantity_unit}"
            )

        if payload.stage.startswith("receiving_"):
            if payload.input_ref != delivery_id:
                raise QuantityValidationError(f"receiving stages must take input_ref {delivery_id}")
            available = delivery.stated_quantity
        else:
            source = db.scalar(
                select(MaterialMovement).where(
                    MaterialMovement.delivery_id == delivery_id,
                    MaterialMovement.output_lot_id == payload.input_ref,
                )
            )
            if source is None:
                raise QuantityValidationError(f"unknown input_ref {payload.input_ref}")
            available = source.quantity_out

        if _producer(db, payload.output_lot_id) is not None:
            raise QuantityValidationError(f"output lot {payload.output_lot_id} already exists")

        consumed = db.scalar(
            select(func.coalesce(func.sum(MaterialMovement.quantity_in), 0.0)).where(
                MaterialMovement.delivery_id == delivery_id,
                MaterialMovement.input_ref == payload.input_ref,
            )
        )
        if consumed + payload.quantity_in > available + _EPS:
            raise QuantityValidationError(
                f"overdraw: {payload.input_ref} has {available} available, "
                f"{consumed} already consumed, {payload.quantity_in} requested"
            )

        movement = MaterialMovement(
            delivery_id=delivery_id,
            input_ref=payload.input_ref,
            output_lot_id=payload.output_lot_id,
            stage=payload.stage,
            quantity_in=payload.quantity_in,
            quantity_out=payload.quantity_out,
            quantity_unit=payload.quantity_unit,
            normal_yield_loss=payload.normal_yield_loss,
            qc_reject_loss=payload.qc_reject_loss,
            unexplained_variance=payload.unexplained_variance,
            operator_id=payload.operator_id,
            timestamp=now or utcnow(),
            notes=payload.notes,
        )
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement


def get_delivery_lineage(db: Session, delivery_id: str) -> DeliveryTraceTreeResponse:
    """Build the full trace tree for a delivery: inspections, dispositions, movements, balance and gaps."""
    delivery = _get_delivery(db, delivery_id)
    fish = list(
        db.scalars(
            select(FishInspection)
            .where(FishInspection.delivery_id == delivery_id)
            .order_by(FishInspection.sequence_in_delivery)
        )
    )
    dispositions = _dispositions_of(db, delivery_id)
    movements = _movements_of(db, delivery_id)
    active = active_dispositions(dispositions)
    active_ids = {d.id for d in active}

    status_counts = Counter(f.status for f in fish)
    flagged = sum(1 for f in fish if f.flagged_for_review)
    summary = InspectionSummary(
        total=len(fish),
        complete=status_counts[InspectionStatus.COMPLETE.value],
        partial_dorsal_only=status_counts[InspectionStatus.PARTIAL_DORSAL_ONLY.value],
        partial_ventral_only=status_counts[InspectionStatus.PARTIAL_VENTRAL_ONLY.value],
        failed_capture=status_counts[InspectionStatus.FAILED_CAPTURE.value],
        flagged=flagged,
    )

    lot_ids = list({m.output_lot_id for m in movements})
    slots_by_lot: dict[str, list[StorageSlotRef]] = defaultdict(list)
    for slot in db.scalars(select(StorageSlot).where(StorageSlot.lot_id.in_(lot_ids))):
        slots_by_lot[slot.lot_id].append(StorageSlotRef.model_validate(slot))
    dispatches_by_lot: dict[str, list[DispatchRef]] = defaultdict(list)
    dispatch_rows = db.execute(
        select(DispatchLot.lot_id, Dispatch)
        .join(Dispatch, Dispatch.dispatch_id == DispatchLot.dispatch_id)
        .where(DispatchLot.lot_id.in_(lot_ids))
    )
    for lot_id, dispatch in dispatch_rows:
        dispatches_by_lot[lot_id].append(DispatchRef.model_validate(dispatch))

    disposition_reads = [
        HumanDispositionRead.model_validate(d).model_copy(update={"superseded": d.id not in active_ids})
        for d in dispositions
    ]
    nodes = [
        MovementNode(
            **MaterialMovementRead.model_validate(m).model_dump(),
            storage_slots=slots_by_lot.get(m.output_lot_id, []),
            dispatches=dispatches_by_lot.get(m.output_lot_id, []),
        )
        for m in movements
    ]

    dispositioned = sum(d.affected_quantity for d in active)
    allocated = sum(m.quantity_in for m in movements if m.input_ref == delivery_id)
    balance = QuantityBalance(
        stated_quantity=delivery.stated_quantity,
        quantity_unit=delivery.quantity_unit,
        dispositioned_quantity=dispositioned,
        allocated_from_intake=allocated,
        unallocated_quantity=delivery.stated_quantity - allocated,
    )

    links: list[MissingLink] = []
    for f in fish:
        if f.status != InspectionStatus.COMPLETE.value:
            links.append(
                MissingLink(kind="PARTIAL_INSPECTION", ref=f"seq-{f.sequence_in_delivery}", detail=f.status)
            )
    if flagged > 0 and not active:
        links.append(
            MissingLink(
                kind="FLAGGED_WITHOUT_DISPOSITION",
                ref=delivery_id,
                detail=f"{flagged} flagged fish have no disposition",
            )
        )
    if dispositioned < delivery.stated_quantity - _EPS:
        remaining = delivery.stated_quantity - dispositioned
        links.append(
            MissingLink(
                kind="UNDISPOSITIONED_QUANTITY",
                ref=delivery_id,
                detail=f"{remaining:.2f} {delivery.quantity_unit} remain undispositioned",
            )
        )
    produced_lots = {m.output_lot_id for m in movements}
    consumed_refs = {m.input_ref for m in movements}
    for d in active:
        if d.disposition != DispositionOutcome.REJECT.value and d.output_lot_id not in produced_lots:
            links.append(
                MissingLink(
                    kind="DISPOSITION_LOT_NOT_HANDED_OFF",
                    ref=d.output_lot_id,
                    detail=f"{d.disposition} disposition {d.id} has no movement producing its lot",
                )
            )
    for m in movements:
        if m.output_lot_id in consumed_refs or slots_by_lot.get(m.output_lot_id) or dispatches_by_lot.get(m.output_lot_id):
            continue
        links.append(MissingLink(kind="LOT_LOCATION_UNKNOWN", ref=m.output_lot_id, detail=m.stage))

    return DeliveryTraceTreeResponse(
        delivery=DeliveryRead.model_validate(delivery),
        inspection_summary=summary,
        dispositions=disposition_reads,
        movements=nodes,
        balance=balance,
        missing_links=links,
    )


def get_lot_provenance(db: Session, lot_id: str) -> LotProvenanceResponse:
    """Walk upstream from a lot to its receiving root and report any broken links."""
    current = lot_id
    chain: list[MaterialMovement] = []
    visited: set[int] = set()
    links: list[MissingLink] = []
    while True:
        movement = _producer(db, current)
        if movement is None:
            if chain:
                links.append(
                    MissingLink(kind="NO_UPSTREAM_MOVEMENT", ref=current, detail="no recorded movement produced this lot")
                )
            break
        if movement.id in visited:
            break
        visited.add(movement.id)
        chain.append(movement)
        if movement.input_ref == movement.delivery_id:
            break
        current = movement.input_ref

    delivery = None
    if not chain:
        links.append(
            MissingLink(kind="NO_UPSTREAM_MOVEMENT", ref=lot_id, detail="no recorded movement produced this lot")
        )
    else:
        delivery = db.get(ReceivingDelivery, chain[-1].delivery_id)
        if delivery is None:
            links.append(
                MissingLink(
                    kind="DELIVERY_NOT_FOUND",
                    ref=chain[-1].delivery_id,
                    detail=f"delivery {chain[-1].delivery_id} not found",
                )
            )

    return LotProvenanceResponse(
        lot_id=lot_id,
        delivery=DeliveryRead.model_validate(delivery) if delivery is not None else None,
        chain=[MaterialMovementRead.model_validate(m) for m in reversed(chain)],
        missing_links=links,
    )
