"""Two-view (dorsal + ventral) conveyor capture: inference, fish pairing and persistence."""

import asyncio
import hashlib
import io
import json
import os
import shutil
import time
from datetime import datetime, timedelta

from PIL import Image
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai import get_ai_engine
from app.config import settings
from app.models.delivery_trace import (
    FishInspection,
    InferenceMode,
    InspectionStatus,
    InspectionView,
    ReceivingDelivery,
    utcnow,
)
from app.services.errors import (
    CaptureBackpressureError,
    DeliveryStateError,
    InsufficientStorageError,
    InvalidImageError,
    NotFoundError,
    QuantityValidationError,
)

PAIRING_TIMEOUT_SECONDS = 3.0
SUPPORTED_FAMILIES = {"Scombridae", "Cichlidae", "Salmonidae"}
MAX_PENDING = 8
_INFER_SEM = asyncio.Semaphore(4)
_WRITE_LOCK = asyncio.Lock()
_pending = 0

MISSING_DORSAL = "missing_dorsal_view"
MISSING_VENTRAL = "missing_ventral_view"


def ensure_capture_capacity() -> None:
    """Create the upload dir and refuse to start capture when free disk space is too low."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    free = shutil.disk_usage(settings.UPLOAD_DIR).free
    required = settings.CAPTURE_MIN_FREE_BYTES
    if free < required:
        raise InsufficientStorageError(
            f"Free disk {free / 1024**3:.1f} GiB is below the required {required / 1024**3:.1f} GiB"
        )


def _load_reasons(fish: FishInspection) -> list[str]:
    return json.loads(fish.flag_reasons_json or "[]")


def _merge_reasons(existing: list[str], new: list[str]) -> list[str]:
    """Append new reasons in encounter order, skipping duplicates."""
    merged = list(existing)
    for reason in new:
        if reason not in merged:
            merged.append(reason)
    return merged


def _has_view(fish: FishInspection, view_side: str) -> bool:
    return any(v.view_side == view_side for v in fish.views)


def _next_sequence(db: Session, delivery_id: str) -> int:
    current = db.scalar(
        select(func.max(FishInspection.sequence_in_delivery)).where(
            FishInspection.delivery_id == delivery_id
        )
    )
    return (current or 0) + 1


def reap_timed_out_captures(
    db: Session,
    delivery_id: str | None = None,
    timeout_seconds: float = PAIRING_TIMEOUT_SECONDS,
    now: datetime | None = None,
) -> int:
    """Flag dorsal-only fish whose ventral view never arrived within the pairing window."""
    now = now or utcnow()
    stmt = select(FishInspection).where(
        FishInspection.status == InspectionStatus.PARTIAL_DORSAL_ONLY.value,
        FishInspection.created_at < now - timedelta(seconds=timeout_seconds),
    )
    if delivery_id is not None:
        stmt = stmt.where(FishInspection.delivery_id == delivery_id)

    changed = 0
    for fish in db.scalars(stmt).all():
        reasons = _load_reasons(fish)
        if MISSING_VENTRAL in reasons:
            continue
        fish.flagged_for_review = True
        fish.flag_reasons_json = json.dumps(_merge_reasons(reasons, [MISSING_VENTRAL]))
        changed += 1
    if changed:
        db.commit()
    return changed


def _write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as fh:
        fh.write(data)


def _run_inference(pil: Image.Image, fish_family: str) -> dict:
    start = time.perf_counter()
    if fish_family not in SUPPORTED_FAMILIES:
        grade, confidence, defects = "UNSUPPORTED", 0.0, []
        mode = InferenceMode.SKIPPED_UNSUPPORTED.value
    else:
        engine = get_ai_engine()
        freshness = engine.predict_freshness(pil)
        grade, confidence = freshness["grade"], freshness["confidence"]
        defects = engine.predict_defects(pil)
        is_real = engine.freshness_session is not None and engine.defect_session is not None
        mode = (InferenceMode.REAL_ONNX if is_real else InferenceMode.SIMULATED_MOCK).value
    return {
        "grade": grade,
        "confidence": confidence,
        "defects": defects,
        "mode": mode,
        "latency_ms": int((time.perf_counter() - start) * 1000),
    }


def _resolve_fish(
    db: Session,
    delivery_id: str,
    view_side: str,
    sequence_in_delivery: int | None,
    now: datetime,
) -> FishInspection:
    """Return the fish this view belongs to, creating or pairing as needed."""
    if view_side == "dorsal":
        if sequence_in_delivery is not None:
            raise QuantityValidationError("sequence_in_delivery applies only to ventral captures")
        fish = FishInspection(
            delivery_id=delivery_id,
            sequence_in_delivery=_next_sequence(db, delivery_id),
            status=InspectionStatus.PARTIAL_DORSAL_ONLY.value,
            flagged_for_review=False,
            flag_reasons_json="[]",
            created_at=now,
        )
        db.add(fish)
        db.flush()
        return fish

    if sequence_in_delivery is not None:
        fish = db.scalar(
            select(FishInspection).where(
                FishInspection.delivery_id == delivery_id,
                FishInspection.sequence_in_delivery == sequence_in_delivery,
            )
        )
        if fish is None:
            raise NotFoundError(f"Fish {sequence_in_delivery} not found in delivery {delivery_id}")
        if _has_view(fish, "ventral") or fish.status != InspectionStatus.PARTIAL_DORSAL_ONLY.value:
            raise QuantityValidationError(f"Fish {sequence_in_delivery} cannot take a ventral view")
        fish.status = InspectionStatus.COMPLETE.value
        # Operator-confirmed pairing resolves an earlier timeout flag.
        fish.flag_reasons_json = json.dumps([r for r in _load_reasons(fish) if r != MISSING_VENTRAL])
        return fish

    window_start = now - timedelta(seconds=PAIRING_TIMEOUT_SECONDS)
    candidates = db.scalars(
        select(FishInspection)
        .where(
            FishInspection.delivery_id == delivery_id,
            FishInspection.status == InspectionStatus.PARTIAL_DORSAL_ONLY.value,
            FishInspection.created_at >= window_start,
        )
        .order_by(FishInspection.sequence_in_delivery)
    ).all()
    fish = next((c for c in candidates if not _has_view(c, "ventral")), None)
    if fish is not None:
        fish.status = InspectionStatus.COMPLETE.value
        return fish

    fish = FishInspection(
        delivery_id=delivery_id,
        sequence_in_delivery=_next_sequence(db, delivery_id),
        status=InspectionStatus.PARTIAL_VENTRAL_ONLY.value,
        flagged_for_review=True,
        flag_reasons_json=json.dumps([MISSING_DORSAL]),
        created_at=now,
    )
    db.add(fish)
    db.flush()
    return fish


async def handle_view_capture(
    db: Session,
    delivery_id: str,
    view_side: str,
    image_bytes: bytes,
    sequence_in_delivery: int | None = None,
    now: datetime | None = None,
) -> FishInspection:
    """Run inference on one view, pair it with its fish, and persist the image and results."""
    global _pending

    delivery = db.get(ReceivingDelivery, delivery_id)
    if delivery is None:
        raise NotFoundError(f"Delivery {delivery_id} not found")
    if delivery.status != "active_receiving":
        raise DeliveryStateError(f"Delivery {delivery_id} is not accepting captures")
    if view_side not in ("dorsal", "ventral"):
        raise QuantityValidationError("view_side must be 'dorsal' or 'ventral'")

    try:
        raw = Image.open(io.BytesIO(image_bytes))
        fmt = (raw.format or "JPEG").lower()
        pil = raw.convert("RGB")
    except Exception as exc:
        raise InvalidImageError("Capture is not a decodable image") from exc
    ext = "jpg" if fmt in ("jpeg", "jpg") else fmt

    if _pending >= MAX_PENDING + 4:
        raise CaptureBackpressureError("Too many captures are queued for inference")
    _pending += 1
    try:
        async with _INFER_SEM:
            result = await asyncio.to_thread(_run_inference, pil, delivery.fish_family)
    finally:
        _pending -= 1

    async with _WRITE_LOCK:
        now = now or utcnow()
        reap_timed_out_captures(db, delivery_id, now=now)
        fish = _resolve_fish(db, delivery_id, view_side, sequence_in_delivery, now)

        directory = os.path.join(settings.UPLOAD_DIR, "captures", delivery_id)
        os.makedirs(directory, exist_ok=True)
        filename = f"{fish.sequence_in_delivery:05d}_{view_side}.{ext}"
        await asyncio.to_thread(_write_bytes, os.path.join(directory, filename), image_bytes)

        db.add(
            InspectionView(
                fish_inspection_id=fish.id,
                view_side=view_side,
                image_path=f"/uploads/captures/{delivery_id}/{filename}",
                sha256=hashlib.sha256(image_bytes).hexdigest(),
                freshness_grade=result["grade"],
                freshness_confidence=result["confidence"],
                defects_detected_json=json.dumps(result["defects"]),
                inference_mode=result["mode"],
                inference_latency_ms=result["latency_ms"],
                created_at=now,
            )
        )

        new_reasons = (["grade_C"] if result["grade"] == "C" else []) + [
            d["label"] for d in result["defects"]
        ]
        reasons = _merge_reasons(_load_reasons(fish), new_reasons)
        fish.flag_reasons_json = json.dumps(reasons)
        fish.flagged_for_review = bool(reasons)

        db.commit()
        db.refresh(fish)
        return fish
