"""Switch room endpoints: qc-agent drafts proposals, qc-gate relays verified commands."""

import io
import json
import os

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from PIL import Image, ImageDraw
from sqlalchemy.orm import Session

from app.config import settings
from app.models.delivery_trace import InspectionView

from app.api.auth import require_agent_token, require_gate_token
from app.api.deps import get_db
from app.schemas.switchroom import GateCommandIn, GateReceipt, IdentityUpsert, ProposalCreate, ProposalRead
from app.services import switchroom_service
from app.services.errors import DeliveryServiceError, DeliveryStateError, NotFoundError

router = APIRouter()
# Colours follow code/models/model_2/ANNOTATION_GUIDE_MODEL2.md.
_BOX_COLOURS = {
    "sisik_sisa": (255, 140, 0),
    "warna_abnormal": (230, 30, 30),
    "luka_robekan": (255, 215, 0),
    "lendir_berlebih": (150, 60, 220),
}


def _http(exc: DeliveryServiceError) -> HTTPException:
    code = {NotFoundError: 404, DeliveryStateError: 409}.get(type(exc), 422)
    return HTTPException(status_code=code, detail=str(exc))


@router.post(
    "/proposals",
    response_model=ProposalRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_agent_token)],
    summary="Draft a disposition or movement (qc-agent)",
)
def create_proposal(req: ProposalCreate, db: Session = Depends(get_db)):
    try:
        return switchroom_service.to_read(switchroom_service.create_proposal(db, req))
    except DeliveryServiceError as exc:
        raise _http(exc) from exc


@router.get("/proposals", response_model=list[ProposalRead], summary="List proposals")
def list_proposals(
    delivery_id: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    return [switchroom_service.to_read(p) for p in switchroom_service.list_proposals(db, delivery_id, status_filter)]


@router.get("/proposals/{public_id}", response_model=ProposalRead, summary="Get one proposal")
def get_proposal(public_id: str, db: Session = Depends(get_db)):
    try:
        return switchroom_service.to_read(switchroom_service.get_proposal(db, public_id))
    except DeliveryServiceError as exc:
        raise _http(exc) from exc


@router.post(
    "/gate/commands",
    response_model=GateReceipt,
    dependencies=[Depends(require_gate_token)],
    summary="Apply a chat command relayed by qc-gate with its Switch sender id",
)
def gate_command(req: GateCommandIn, db: Session = Depends(get_db)):
    return switchroom_service.handle_gate_command(db, req)


@router.put(
    "/identities",
    dependencies=[Depends(require_gate_token)],
    summary="Map a Switch sender id to a plant role (setup)",
)
def upsert_identity(req: IdentityUpsert, db: Session = Depends(get_db)):
    row = switchroom_service.upsert_identity(db, req)
    return {"participant_id": row.participant_id, "username": row.username, "role": row.role}


@router.get(
    "/views/{view_id}/annotated.jpg",
    summary="Inspection view photo with the model's defect boxes drawn on",
    response_class=Response,
)
def annotated_view(view_id: int, db: Session = Depends(get_db)):
    view = db.get(InspectionView, view_id)
    if view is None:
        raise HTTPException(status_code=404, detail=f"view {view_id} not found")
    path = os.path.join(settings.UPLOAD_DIR, view.image_path.removeprefix("/uploads/"))
    try:
        image = Image.open(path).convert("RGB")
    except OSError as exc:
        raise HTTPException(status_code=404, detail="image file missing") from exc
    draw = ImageDraw.Draw(image)
    width = max(2, image.width // 150)
    for defect in json.loads(view.defects_detected_json or "[]"):
        x1, y1, x2, y2 = defect["bbox"]
        colour = _BOX_COLOURS.get(defect["label"], (255, 255, 0))
        draw.rectangle([x1, y1, x2, y2], outline=colour, width=width)
        tag = f"{defect['label']} {defect['confidence']:.2f}"
        draw.rectangle([x1, max(0, y1 - 12), x1 + 7 * len(tag), max(12, y1)], fill=colour)
        draw.text((x1 + 2, max(0, y1 - 12)), tag, fill=(0, 0, 0))
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=90)
    return Response(content=buf.getvalue(), media_type="image/jpeg")
