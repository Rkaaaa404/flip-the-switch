"""Material lineage: balanced movements, overdraw and unit rules, stage input rules, provenance and trace gaps."""

import asyncio
from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.models.delivery_trace import MaterialMovement, ReceivingDelivery
from app.models.dispatch import Dispatch, DispatchLot
from app.models.storage_slot import StorageSlot
from app.schemas.delivery_trace import HumanDispositionCreate, MaterialMovementCreate
from app.services import material_lineage_service
from app.services.errors import QuantityValidationError
from app.services.two_view_inspection_service import (
    handle_view_capture,
    reap_timed_out_captures,
)

T0 = datetime(2026, 1, 15, 9, 0, 0)
DELIVERIES = "/api/v1/deliveries"


def _disposition(lot, outcome, quantity, unit="kg"):
    return HumanDispositionCreate(
        output_lot_id=lot,
        disposition=outcome,
        affected_quantity=quantity,
        quantity_unit=unit,
        decision_reason="QC decision",
        authorized_by="qc.lead",
    )


def _movement(input_ref, output, stage, qty_in, qty_out, *, unit="kg", nyl=0.0, qrl=0.0, uv=0.0):
    return MaterialMovementCreate(
        input_ref=input_ref,
        output_lot_id=output,
        stage=stage,
        quantity_in=qty_in,
        quantity_out=qty_out,
        quantity_unit=unit,
        normal_yield_loss=nyl,
        qc_reject_loss=qrl,
        unexplained_variance=uv,
        operator_id="op.line1",
    )


def _ready(db, make_delivery, qty=500.0):
    """Delivery in inspection_complete with no dispositions yet."""
    delivery = make_delivery(db, now=T0, stated_quantity=qty)
    material_lineage_service.transition_status(db, delivery.id, "inspection_complete")
    return delivery


def _dispositioned(db, make_delivery, *dispositions, qty=500.0):
    """Delivery in disposition_recorded; defaults to ACCEPT 500 kg into LOT-A."""
    delivery = _ready(db, make_delivery, qty=qty)
    for item in dispositions or [_disposition("LOT-A", "ACCEPT", qty)]:
        material_lineage_service.record_disposition(db, delivery.id, item, now=T0)
    return delivery


def _links(body):
    return [(link["kind"], link["ref"]) for link in body["missing_links"]]


def test_wggs_and_fillet_lineage_accounting(db, make_delivery):
    delivery = _ready(db, make_delivery)
    material_lineage_service.record_disposition(db, delivery.id, _disposition("LOT-A", "ACCEPT", 450), now=T0)
    material_lineage_service.record_disposition(db, delivery.id, _disposition("LOT-R", "REPROCESS", 50), now=T0)

    stages = [
        _movement(delivery.id, "LOT-A", "receiving_to_processing", 450, 450),
        _movement("LOT-A", "LOT-W", "processing_wggs", 450, 400, nyl=45, qrl=5),
        _movement("LOT-W", "LOT-F", "processing_fillet", 400, 180, nyl=210, uv=10),
    ]
    for stage in stages:
        material_lineage_service.record_transformation_stage(db, delivery.id, stage, now=T0)

    stored = list(
        db.scalars(select(MaterialMovement).where(MaterialMovement.delivery_id == delivery.id).order_by(MaterialMovement.id))
    )
    assert [(m.input_ref, m.output_lot_id, m.quantity_in, m.quantity_out) for m in stored] == [
        (delivery.id, "LOT-A", 450, 450),
        ("LOT-A", "LOT-W", 450, 400),
        ("LOT-W", "LOT-F", 400, 180),
    ]
    for m in stored:
        accounted = m.quantity_out + m.normal_yield_loss + m.qc_reject_loss + m.unexplained_variance
        assert m.quantity_in == pytest.approx(accounted)

    provenance = material_lineage_service.get_lot_provenance(db, "LOT-F")
    assert [m.output_lot_id for m in provenance.chain] == ["LOT-A", "LOT-W", "LOT-F"]
    assert provenance.delivery is not None
    assert provenance.delivery.id == delivery.id
    assert provenance.missing_links == []

    balance = material_lineage_service.get_delivery_lineage(db, delivery.id).balance
    assert balance.allocated_from_intake == pytest.approx(450)
    assert balance.dispositioned_quantity == pytest.approx(500)
    assert balance.unallocated_quantity == pytest.approx(50)


def test_movement_rejects_unbalanced(client, db, make_delivery):
    with pytest.raises(ValidationError):
        _movement("DEL-X", "LOT-A", "receiving_to_processing", 450, 400)

    delivery = _dispositioned(db, make_delivery)
    resp = client.post(
        f"{DELIVERIES}/{delivery.id}/movements",
        json={
            "input_ref": delivery.id,
            "output_lot_id": "LOT-A",
            "stage": "receiving_to_processing",
            "quantity_in": 450,
            "quantity_out": 400,
            "quantity_unit": "kg",
            "operator_id": "op.line1",
        },
    )
    assert resp.status_code == 422


def test_overdraw_rejected(client, db, make_delivery):
    delivery = _dispositioned(db, make_delivery)
    first = client.post(
        f"{DELIVERIES}/{delivery.id}/movements",
        json=_movement(delivery.id, "LOT-A", "receiving_to_processing", 300, 300).model_dump(mode="json"),
    )
    assert first.status_code == 201

    second = client.post(
        f"{DELIVERIES}/{delivery.id}/movements",
        json=_movement(delivery.id, "LOT-B", "receiving_to_processing", 250, 250).model_dump(mode="json"),
    )
    assert second.status_code == 422
    assert "overdraw" in second.json()["detail"]


def test_upstream_lot_overdraw_rejected(db, make_delivery):
    delivery = _dispositioned(db, make_delivery)
    material_lineage_service.record_transformation_stage(
        db, delivery.id, _movement(delivery.id, "LOT-A", "receiving_to_processing", 300, 300), now=T0
    )
    with pytest.raises(QuantityValidationError, match="overdraw"):
        material_lineage_service.record_transformation_stage(
            db, delivery.id, _movement("LOT-A", "LOT-W", "processing_wggs", 350, 350), now=T0
        )


def test_unit_mismatch_rejected(db, make_delivery):
    delivery = _ready(db, make_delivery)
    with pytest.raises(QuantityValidationError, match="does not match"):
        material_lineage_service.record_disposition(
            db, delivery.id, _disposition("LOT-A", "ACCEPT", 100, unit="count"), now=T0
        )

    dispositioned = _dispositioned(db, make_delivery)
    with pytest.raises(QuantityValidationError, match="does not match"):
        material_lineage_service.record_transformation_stage(
            db,
            dispositioned.id,
            _movement(dispositioned.id, "LOT-A", "receiving_to_processing", 100, 100, unit="count"),
            now=T0,
        )


def test_stage_input_rules(db, make_delivery):
    delivery = _dispositioned(db, make_delivery)

    with pytest.raises(QuantityValidationError, match="receiving stages must take input_ref"):
        material_lineage_service.record_transformation_stage(
            db, delivery.id, _movement("DEL-OTHER", "LOT-A", "receiving_to_processing", 100, 100), now=T0
        )

    with pytest.raises(QuantityValidationError, match="unknown input_ref"):
        material_lineage_service.record_transformation_stage(
            db, delivery.id, _movement("LOT-NOPE", "LOT-W", "processing_wggs", 100, 100), now=T0
        )

    material_lineage_service.record_transformation_stage(
        db, delivery.id, _movement(delivery.id, "LOT-A", "receiving_to_processing", 100, 100), now=T0
    )
    with pytest.raises(QuantityValidationError, match="already exists"):
        material_lineage_service.record_transformation_stage(
            db, delivery.id, _movement(delivery.id, "LOT-A", "receiving_to_processing", 100, 100), now=T0
        )


def test_stage_requires_disposition_recorded(client, db, make_delivery):
    delivery = _ready(db, make_delivery)
    resp = client.post(
        f"{DELIVERIES}/{delivery.id}/movements",
        json=_movement(delivery.id, "LOT-A", "receiving_to_processing", 100, 100).model_dump(mode="json"),
    )
    assert resp.status_code == 409


def test_audit_trace_with_missing_links(client, db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    asyncio.run(handle_view_capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0))
    assert reap_timed_out_captures(db, delivery.id, now=T0 + timedelta(seconds=10)) == 1
    material_lineage_service.transition_status(db, delivery.id, "inspection_complete")
    material_lineage_service.record_disposition(db, delivery.id, _disposition("LOT-A", "ACCEPT", 400), now=T0)
    material_lineage_service.record_disposition(db, delivery.id, _disposition("LOT-R", "REPROCESS", 50), now=T0)
    material_lineage_service.record_transformation_stage(
        db, delivery.id, _movement(delivery.id, "LOT-S", "receiving_to_storage", 400, 400), now=T0
    )

    base_links = [
        ("PARTIAL_INSPECTION", "seq-1"),
        ("UNDISPOSITIONED_QUANTITY", delivery.id),
        ("DISPOSITION_LOT_NOT_HANDED_OFF", "LOT-A"),
        ("DISPOSITION_LOT_NOT_HANDED_OFF", "LOT-R"),
    ]

    body = client.get(f"{DELIVERIES}/{delivery.id}/trace").json()
    assert _links(body) == base_links + [("LOT_LOCATION_UNKNOWN", "LOT-S")]
    (node,) = body["movements"]
    assert node["storage_slots"] == []
    assert node["dispatches"] == []

    db.add(StorageSlot(slot_id="F-01", zone="frozen", lot_id="LOT-S"))
    db.commit()
    body = client.get(f"{DELIVERIES}/{delivery.id}/trace").json()
    assert _links(body) == base_links
    (node,) = body["movements"]
    assert [slot["slot_id"] for slot in node["storage_slots"]] == ["F-01"]

    material_lineage_service.record_transformation_stage(
        db, delivery.id, _movement("LOT-S", "LOT-D", "processing_to_dispatch", 400, 400), now=T0
    )
    db.add(Dispatch(dispatch_id="DISP-1", buyer_name="B", destination="Japan", dispatch_date=T0))
    db.add(DispatchLot(dispatch_id="DISP-1", lot_id="LOT-D"))
    db.commit()

    body = client.get(f"{DELIVERIES}/{delivery.id}/trace").json()
    assert _links(body) == base_links
    nodes = {node["output_lot_id"]: node for node in body["movements"]}
    assert [slot["slot_id"] for slot in nodes["LOT-S"]["storage_slots"]] == ["F-01"]
    (dispatch,) = nodes["LOT-D"]["dispatches"]
    assert dispatch["dispatch_id"] == "DISP-1"
    assert dispatch["buyer_name"] == "B"
    assert dispatch["destination"] == "Japan"
    assert dispatch["status"] == "pending"


def test_trace_flagged_without_disposition(client, db, make_delivery, jpeg_bytes):
    delivery = make_delivery(db, now=T0)
    asyncio.run(handle_view_capture(db, delivery.id, "dorsal", jpeg_bytes, now=T0))
    assert reap_timed_out_captures(db, delivery.id, now=T0 + timedelta(seconds=10)) == 1

    body = client.get(f"{DELIVERIES}/{delivery.id}/trace").json()
    assert body["inspection_summary"]["flagged"] == 1
    assert _links(body) == [
        ("PARTIAL_INSPECTION", "seq-1"),
        ("FLAGGED_WITHOUT_DISPOSITION", delivery.id),
        ("UNDISPOSITIONED_QUANTITY", delivery.id),
    ]


def test_provenance_legacy_lot_no_upstream(client, db):
    db.add(StorageSlot(slot_id="F-02", zone="frozen", lot_id="LOT-20260821-001"))
    db.commit()

    body = client.get(f"{DELIVERIES}/lots/LOT-20260821-001/provenance").json()
    assert body["chain"] == []
    assert body["delivery"] is None
    assert len(body["missing_links"]) == 1
    assert body["missing_links"][0]["kind"] == "NO_UPSTREAM_MOVEMENT"


def test_disposition_state_and_quantity_rules(client, db):
    created = client.post(
        DELIVERIES,
        json={
            "supplier_name": "Supplier A",
            "species": "Oreochromis niloticus",
            "fish_family": "Cichlidae",
            "stated_quantity": 500,
            "quantity_unit": "kg",
            "created_by": "qc.tester",
        },
    ).json()
    delivery_id = created["id"]

    early = client.post(
        f"{DELIVERIES}/{delivery_id}/dispositions",
        json={"output_lot_id": "LOT-A", "disposition": "ACCEPT", "affected_quantity": 100,
              "quantity_unit": "kg", "decision_reason": "x", "authorized_by": "qc"},
    )
    assert early.status_code == 409

    assert client.patch(f"{DELIVERIES}/{delivery_id}/status", json={"status": "inspection_complete"}).status_code == 200

    early_move = client.post(
        f"{DELIVERIES}/{delivery_id}/movements",
        json=_movement(delivery_id, "LOT-A", "receiving_to_processing", 100, 100).model_dump(mode="json"),
    )
    assert early_move.status_code == 409

    over = client.post(
        f"{DELIVERIES}/{delivery_id}/dispositions",
        json={"output_lot_id": "LOT-A", "disposition": "ACCEPT", "affected_quantity": 600,
              "quantity_unit": "kg", "decision_reason": "x", "authorized_by": "qc"},
    )
    assert over.status_code == 422

    reject = client.post(
        f"{DELIVERIES}/{delivery_id}/dispositions",
        json={"disposition": "REJECT", "affected_quantity": 100, "quantity_unit": "kg",
              "decision_reason": "Spoiled", "authorized_by": "qc"},
    )
    assert reject.status_code == 201
    assert reject.json()["output_lot_id"] is None

    accept_without_lot = client.post(
        f"{DELIVERIES}/{delivery_id}/dispositions",
        json={"disposition": "ACCEPT", "affected_quantity": 50, "quantity_unit": "kg",
              "decision_reason": "x", "authorized_by": "qc"},
    )
    assert accept_without_lot.status_code == 422

    unknown = client.post(
        "/api/v1/deliveries/DEL-20990101-001/dispositions",
        json={"disposition": "REJECT", "affected_quantity": 1, "quantity_unit": "kg",
              "decision_reason": "x", "authorized_by": "qc"},
    )
    assert unknown.status_code == 404

    # Rejected quantity counts as dispositioned; the rest is still undispositioned and no lot is expected.
    body = client.get(f"{DELIVERIES}/{delivery_id}/trace").json()
    assert _links(body) == [("UNDISPOSITIONED_QUANTITY", delivery_id)]
    assert body["balance"]["dispositioned_quantity"] == pytest.approx(100)

    with pytest.raises(ValidationError):
        HumanDispositionCreate(
            disposition="ACCEPT", affected_quantity=1, quantity_unit="kg",
            decision_reason="x", authorized_by="qc",
        )


def test_delivery_id_sequence(db, make_delivery):
    day = datetime(2026, 3, 4, 8, 0, 0)
    first = make_delivery(db, now=day)
    second = make_delivery(db, now=day)
    assert first.id == "DEL-20260304-001"
    assert second.id == "DEL-20260304-002"

    next_day = make_delivery(db, now=datetime(2026, 3, 5, 8, 0, 0))
    assert next_day.id == "DEL-20260305-001"

    db.add(
        ReceivingDelivery(
            id="DEL-20260304-ABC",
            supplier_name="Legacy",
            species="Unknown",
            fish_family="Cichlidae",
            stated_quantity=1.0,
            quantity_unit="kg",
            created_by="legacy",
        )
    )
    db.commit()
    assert material_lineage_service.generate_delivery_id(db, now=day) == "DEL-20260304-003"
