"""Receiving delivery sessions, two-view fish pairing, flags, operator pairing and disposition immutability."""

import asyncio
import hashlib
import json
import os
import re
from datetime import datetime, timedelta

import pytest
from sqlalchemy import select

from app.config import settings
from app.models.delivery_trace import (
    FishInspection,
    HumanDisposition,
    InspectionStatus,
    InspectionView,
)
from app.services import two_view_inspection_service
from app.services.errors import (
    CaptureBackpressureError,
    NotFoundError,
    QuantityValidationError,
)
from app.services.two_view_inspection_service import (
    MAX_PENDING,
    MISSING_DORSAL,
    MISSING_VENTRAL,
    handle_view_capture,
    reap_timed_out_captures,
)

T0 = datetime(2026, 1, 15, 9, 0, 0)
DELIVERIES = "/api/v1/deliveries"


def _api_payload(**overrides):
    payload = {
        "supplier_name": "Supplier A",
        "species": "Oreochromis niloticus",
        "fish_family": "Cichlidae",
        "stated_quantity": 500,
        "quantity_unit": "kg",
        "truck_identifier": "B 1234 XY",
        "created_by": "qc.tester",
    }
    payload.update(overrides)
    return payload


def _disposition_json(disposition, lot, quantity, **extra):
    body = {
        "disposition": disposition,
        "affected_quantity": quantity,
        "quantity_unit": "kg",
        "decision_reason": "QC review",
        "authorized_by": "qc.lead",
    }
    if lot is not None:
        body["output_lot_id"] = lot
    body.update(extra)
    return body


def _capture_api(client, delivery_id, side, image, sequence=None):
    data = {"view_side": side}
    if sequence is not None:
        data["sequence_in_delivery"] = str(sequence)
    return client.post(
        f"{DELIVERIES}/{delivery_id}/capture-view",
        files={"image": ("fish.jpg", image, "image/jpeg")},
        data=data,
    )


def _capture(db, delivery_id, side, image, now, sequence=None):
    return asyncio.run(
        handle_view_capture(db, delivery_id, side, image, sequence_in_delivery=sequence, now=now)
    )


def _rows(db, table):
    return [tuple(row) for row in db.execute(select(table)).all()]


def test_delivery_session_lifecycle(client, jpeg_bytes):
    created = client.post(DELIVERIES, json=_api_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "active_receiving"
    assert re.fullmatch(r"DEL-\d{8}-\d{3}", body["id"])
    delivery_id = body["id"]

    inspected = client.patch(f"{DELIVERIES}/{delivery_id}/status", json={"status": "inspection_complete"})
    assert inspected.status_code == 200
    assert inspected.json()["status"] == "inspection_complete"

    disposition = client.post(
        f"{DELIVERIES}/{delivery_id}/dispositions",
        json=_disposition_json("ACCEPT", "LOT-A", 500),
    )
    assert disposition.status_code == 201
    detail = client.get(f"{DELIVERIES}/{delivery_id}").json()
    assert detail["delivery"]["status"] == "disposition_recorded"

    closed = client.patch(f"{DELIVERIES}/{delivery_id}/status", json={"status": "closed"})
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"

    late_capture = _capture_api(client, delivery_id, "dorsal", jpeg_bytes)
    assert late_capture.status_code == 409

    repeat_close = client.patch(f"{DELIVERIES}/{delivery_id}/status", json={"status": "closed"})
    assert repeat_close.status_code == 409


def test_two_view_normal_pairing(db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    dorsal = _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
    ventral = _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=1))

    assert ventral.id == dorsal.id
    assert ventral.status == InspectionStatus.COMPLETE.value
    assert ventral.flagged_for_review is False
    assert sorted(v.view_side for v in ventral.views) == ["dorsal", "ventral"]

    expected_sha = hashlib.sha256(jpeg_bytes).hexdigest()
    for view in ventral.views:
        assert len(view.sha256) == 64
        assert view.sha256 == expected_sha
        filename = f"{ventral.sequence_in_delivery:05d}_{view.view_side}.jpg"
        assert view.image_path == f"/uploads/captures/{delivery.id}/{filename}"
        on_disk = os.path.join(settings.UPLOAD_DIR, "captures", delivery.id, filename)
        assert os.path.isfile(on_disk)


def test_two_view_timeout_partial_fallback(db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    dorsal = _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)

    assert reap_timed_out_captures(db, delivery.id, now=T0 + timedelta(seconds=4)) == 1
    db.refresh(dorsal)
    assert dorsal.status == InspectionStatus.PARTIAL_DORSAL_ONLY.value
    assert dorsal.flagged_for_review is True
    assert MISSING_VENTRAL in dorsal.flag_reasons_json

    assert reap_timed_out_captures(db, delivery.id, now=T0 + timedelta(seconds=4)) == 0
    assert reap_timed_out_captures(db, now=T0 + timedelta(seconds=4)) == 0

    # A ventral arriving after the window must not attach to the timed-out dorsal fish.
    late_ventral = _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=5))
    assert late_ventral.id != dorsal.id
    assert late_ventral.sequence_in_delivery == 2
    assert late_ventral.status == InspectionStatus.PARTIAL_VENTRAL_ONLY.value
    assert late_ventral.flagged_for_review is True
    assert late_ventral.flag_reasons_json == f'["{MISSING_DORSAL}"]'
    assert [v.view_side for v in late_ventral.views] == ["ventral"]

    db.refresh(dorsal)
    assert dorsal.status == InspectionStatus.PARTIAL_DORSAL_ONLY.value
    assert [v.view_side for v in dorsal.views] == ["dorsal"]


@pytest.mark.parametrize(
    ("dorsal_grade", "dorsal_defects", "ventral_grade", "ventral_defects", "expected_reasons"),
    [
        ("C", [], "A", [], ["grade_C"]),
        ("A", [], "A", [{"label": "luka_robekan", "bbox": [1, 1, 9, 9], "confidence": 0.8}], ["luka_robekan"]),
        ("A", [], "A", [], []),
    ],
    ids=["grade_c_dorsal", "defect_on_ventral", "both_clean"],
)
def test_flagged_inspection_criteria(
    db, make_delivery, jpeg_bytes, fake_engine,
    dorsal_grade, dorsal_defects, ventral_grade, ventral_defects, expected_reasons,
):
    delivery = make_delivery(db, now=T0)
    fake_engine.grades = [dorsal_grade, ventral_grade]
    fake_engine.defects = [dorsal_defects, ventral_defects]

    _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
    fish = _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=1))

    assert fish.status == InspectionStatus.COMPLETE.value
    assert json.loads(fish.flag_reasons_json) == expected_reasons
    assert fish.flagged_for_review is bool(expected_reasons)


def test_human_disposition_immutability(client, db, make_delivery, jpeg_bytes, fake_engine):
    delivery = make_delivery(db, now=T0)
    fake_engine.grades = ["C", "A"]
    _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
    _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=1))

    inspected = client.patch(f"{DELIVERIES}/{delivery.id}/status", json={"status": "inspection_complete"})
    assert inspected.status_code == 200

    original = client.post(
        f"{DELIVERIES}/{delivery.id}/dispositions",
        json=_disposition_json("ACCEPT", "LOT-A", 500),
    )
    assert original.status_code == 201
    original_id = original.json()["id"]

    fish_before = _rows(db, FishInspection.__table__)
    views_before = _rows(db, InspectionView.__table__)
    dispositions_before = _rows(db, HumanDisposition.__table__)

    correction = client.post(
        f"{DELIVERIES}/{delivery.id}/dispositions",
        json=_disposition_json("REPROCESS", "LOT-R", 500, supersedes_id=original_id),
    )
    assert correction.status_code == 201
    correction_id = correction.json()["id"]

    assert _rows(db, FishInspection.__table__) == fish_before
    assert _rows(db, InspectionView.__table__) == views_before
    dispositions_after = _rows(db, HumanDisposition.__table__)
    assert len(dispositions_after) == len(dispositions_before) + 1
    assert dispositions_after[: len(dispositions_before)] == dispositions_before

    detail = client.get(f"{DELIVERIES}/{delivery.id}").json()
    superseded = {d["id"]: d["superseded"] for d in detail["dispositions"]}
    assert superseded == {original_id: True, correction_id: False}

    again = client.post(
        f"{DELIVERIES}/{delivery.id}/dispositions",
        json=_disposition_json("REJECT", None, 500, supersedes_id=original_id),
    )
    assert again.status_code == 422

    unknown = client.post(
        f"{DELIVERIES}/{delivery.id}/dispositions",
        json=_disposition_json("REJECT", None, 500, supersedes_id=9999),
    )
    assert unknown.status_code == 404


def test_operator_assisted_pairing(db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    dorsal = _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)

    assert reap_timed_out_captures(db, delivery.id, now=T0 + timedelta(seconds=10)) == 1
    db.refresh(dorsal)
    assert dorsal.flagged_for_review is True

    with pytest.raises(QuantityValidationError):
        _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0 + timedelta(seconds=11), sequence=1)
    with pytest.raises(NotFoundError):
        _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=11), sequence=99)

    paired = _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=11), sequence=1)
    assert paired.id == dorsal.id
    assert paired.status == InspectionStatus.COMPLETE.value
    assert paired.flagged_for_review is False
    assert paired.flag_reasons_json == "[]"
    assert sorted(v.view_side for v in paired.views) == ["dorsal", "ventral"]


def test_explicit_sequence_cannot_pair_a_completed_fish(db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
    _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=1))

    with pytest.raises(QuantityValidationError, match="cannot take a ventral view"):
        _capture(db, delivery.id, "ventral", jpeg_bytes, now=T0 + timedelta(seconds=2), sequence=1)


def test_unsupported_family_skips_inference(db, make_delivery, jpeg_bytes, fake_engine):
    delivery = make_delivery(db, now=T0, fish_family="Pangasiidae")
    fish = _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)

    (view,) = fish.views
    assert view.freshness_grade == "UNSUPPORTED"
    assert view.inference_mode == "skipped_unsupported"
    assert view.freshness_confidence == 0.0
    assert fake_engine.freshness_calls == 0
    assert fake_engine.defect_calls == 0


def test_real_onnx_mode_when_both_sessions_loaded(db, make_delivery, jpeg_bytes, fake_engine):
    fake_engine.freshness_session = object()
    fake_engine.defect_session = object()
    delivery = make_delivery(db, now=T0)
    fish = _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
    assert fish.views[0].inference_mode == "real_onnx"


def test_png_capture_keeps_source_extension(db, make_delivery, png_bytes):
    delivery = make_delivery(db, now=T0)
    fish = _capture(db, delivery.id, "dorsal", png_bytes, now=T0)
    (view,) = fish.views
    assert view.image_path.endswith("00001_dorsal.png")
    assert os.path.isfile(os.path.join(settings.UPLOAD_DIR, "captures", delivery.id, "00001_dorsal.png"))


def test_invalid_view_side_rejected_by_service(db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    with pytest.raises(QuantityValidationError, match="view_side"):
        _capture(db, delivery.id, "side", jpeg_bytes, now=T0)


def test_capture_rejects_invalid_image_and_state(client, jpeg_bytes):
    created = client.post(DELIVERIES, json=_api_payload()).json()

    bad = _capture_api(client, created["id"], "dorsal", b"definitely not an image")
    assert bad.status_code == 422

    missing = _capture_api(client, "DEL-20990101-001", "dorsal", jpeg_bytes)
    assert missing.status_code == 404


def test_api_single_capture_uses_wall_clock(client, jpeg_bytes):
    created = client.post(DELIVERIES, json=_api_payload()).json()
    resp = _capture_api(client, created["id"], "dorsal", jpeg_bytes)
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == InspectionStatus.PARTIAL_DORSAL_ONLY.value
    assert body["sequence_in_delivery"] == 1


def test_create_delivery_insufficient_storage(client, monkeypatch):
    monkeypatch.setattr(settings, "CAPTURE_MIN_FREE_BYTES", 10**18)
    resp = client.post(DELIVERIES, json=_api_payload())
    assert resp.status_code == 507

    listing = client.get(DELIVERIES).json()
    assert listing["total"] == 0


@pytest.mark.parametrize(
    ("pending", "expect_error"),
    [(MAX_PENDING + 3, False), (MAX_PENDING + 4, True)],
    ids=["below_limit", "at_limit"],
)
def test_backpressure(db, make_delivery, jpeg_bytes, monkeypatch, pending, expect_error):
    delivery = make_delivery(db, now=T0)
    monkeypatch.setattr(two_view_inspection_service, "_pending", pending)

    if expect_error:
        with pytest.raises(CaptureBackpressureError):
            _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
        assert two_view_inspection_service._pending == pending
    else:
        fish = _capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0)
        assert fish.status == InspectionStatus.PARTIAL_DORSAL_ONLY.value
        assert two_view_inspection_service._pending == pending
