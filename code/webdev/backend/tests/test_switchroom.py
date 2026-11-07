"""Switch room workflow: agent drafts, verified people sign through the gate, nobody else can write."""

from conftest import AGENT_TOKEN, GATE_TOKEN

from app.models.delivery_trace import HumanDisposition, MaterialMovement
from app.services import material_lineage_service

API = "/api/v1/switchroom"
SUP = "@switch-mattermost-b1-qc-supervisor:localhost"
OP = "@switch-mattermost-b1-floor-operator:localhost"
AUD = "@switch-mattermost-b1-auditor:localhost"
STRANGER = "@switch-mattermost-b1-user:localhost"
AGENT = {"X-Api-Token": AGENT_TOKEN}
GATE = {"X-Api-Token": GATE_TOKEN}

DISP = {"disposition": "ACCEPT", "affected_quantity": 450, "quantity_unit": "kg",
        "output_lot_id": "LOT-A", "decision_reason": "Lesion local; rest of delivery clean"}


def _setup(anon_client, db, make_delivery):
    for pid, user, role in ((SUP, "qc.supervisor", "qc_supervisor"), (OP, "floor.operator", "floor_operator"),
                            (AUD, "auditor", "auditor")):
        r = anon_client.put(f"{API}/identities", json={"participant_id": pid, "username": user, "role": role}, headers=GATE)
        assert r.status_code == 200
    delivery = make_delivery(db)
    material_lineage_service.transition_status(db, delivery.id, "inspection_complete")
    return delivery


def _propose(c, kind, delivery_id, payload):
    return c.post(f"{API}/proposals", json={"kind": kind, "delivery_id": delivery_id, "payload": payload}, headers=AGENT)


_n = 0


def _gate(c, sender, text, name=None, message_id=None):
    global _n
    _n += 1
    body = {"sender": sender, "sender_name": name, "room_id": "room-1", "message_id": message_id or f"m{_n}", "text": text}
    return c.post(f"{API}/gate/commands", json=body, headers=GATE).json()


def test_tokens_are_enforced(anon_client, db, make_delivery):
    delivery = make_delivery(db)
    no_token = anon_client.post(f"{API}/proposals", json={"kind": "disposition", "delivery_id": delivery.id, "payload": DISP})
    assert no_token.status_code == 403
    wrong = anon_client.post(f"{API}/proposals", headers={"X-Api-Token": GATE_TOKEN},
                             json={"kind": "disposition", "delivery_id": delivery.id, "payload": DISP})
    assert wrong.status_code == 403  # the gate token cannot draft
    gate_as_agent = anon_client.post(f"{API}/gate/commands", headers=AGENT,
                                     json={"sender": SUP, "message_id": "x", "text": "approve DP-1"})
    assert gate_as_agent.status_code == 403  # the agent token cannot sign
    direct = anon_client.post(f"/api/v1/deliveries/{delivery.id}/dispositions", headers=AGENT,
                              json={**DISP, "authorized_by": "anyone"})
    assert direct.status_code == 403  # the old open write route is closed to everyone but the gate


def test_draft_is_validated_like_the_real_write(anon_client, db, make_delivery):
    delivery = _setup(anon_client, db, make_delivery)
    too_much = _propose(anon_client, "disposition", delivery.id, {**DISP, "affected_quantity": 600})
    assert too_much.status_code == 422 and "exceeds" in too_much.json()["detail"]
    missing = _propose(anon_client, "disposition", delivery.id, {"disposition": "ACCEPT"})
    assert missing.status_code == 422
    ok = _propose(anon_client, "disposition", delivery.id, {**DISP, "authorized_by": "agent-tries-to-sign"})
    assert ok.status_code == 201
    body = ok.json()
    assert body["id"] == "DP-1" and body["status"] == "pending" and body["approve_command"] == "@qc-gate approve DP-1"
    assert "authorized_by" not in body["payload"]  # the agent can never pre-fill the signer


def test_only_supervisor_can_approve_and_signature_is_the_verified_sender(anon_client, db, make_delivery):
    delivery = _setup(anon_client, db, make_delivery)
    _propose(anon_client, "disposition", delivery.id, DISP)

    stranger = _gate(anon_client, STRANGER, "@qc-gate approve DP-1", name="user")
    assert not stranger["ok"] and "not a linked NusaQC identity" in stranger["receipt"]
    operator = _gate(anon_client, OP, "@qc-gate approve DP-1")
    assert not operator["ok"] and "floor_operator" in operator["receipt"]
    assert db.query(HumanDisposition).count() == 0

    approved = _gate(anon_client, SUP, "@qc-gate approve DP-1", message_id="sw_abc")
    assert approved["ok"] and "DP-1 recorded" in approved["receipt"] and "qc.supervisor" in approved["receipt"]
    row = db.query(HumanDisposition).one()
    assert (row.authorized_by, row.authorized_via, row.switch_message_id) == ("qc.supervisor", "switch_gate", "sw_abc")

    again = _gate(anon_client, SUP, "@qc-gate approve DP-1")
    assert not again["ok"] and "already applied" in again["receipt"]


def test_replayed_message_changes_nothing(anon_client, db, make_delivery):
    delivery = _setup(anon_client, db, make_delivery)
    _propose(anon_client, "disposition", delivery.id, DISP)
    first = _gate(anon_client, SUP, "approve DP-1", message_id="sw_same")
    second = _gate(anon_client, SUP, "approve DP-1", message_id="sw_same")
    assert first["ok"] and second["replayed"] and second["receipt"] == first["receipt"]
    assert db.query(HumanDisposition).count() == 1


def test_reject_needs_a_reason_and_keeps_record_untouched(anon_client, db, make_delivery):
    delivery = _setup(anon_client, db, make_delivery)
    _propose(anon_client, "disposition", delivery.id, DISP)
    no_reason = _gate(anon_client, SUP, "reject DP-1")
    assert not no_reason["ok"] and "understands only" in no_reason["receipt"]
    rejected = _gate(anon_client, SUP, "reject DP-1 quantity is wrong, re-weigh")
    assert rejected["ok"] and "re-weigh" in rejected["receipt"]
    assert db.query(HumanDisposition).count() == 0
    status = anon_client.get(f"{API}/proposals/DP-1").json()
    assert status["status"] == "rejected" and status["decided_by"] == "qc.supervisor"


def test_apply_time_check_refuses_when_data_changed_since_draft(anon_client, db, make_delivery):
    delivery = _setup(anon_client, db, make_delivery)
    _propose(anon_client, "disposition", delivery.id, {**DISP, "affected_quantity": 300})
    _propose(anon_client, "disposition", delivery.id, {**DISP, "affected_quantity": 300, "output_lot_id": "LOT-B"})
    assert _gate(anon_client, SUP, "approve DP-1")["ok"]
    late = _gate(anon_client, SUP, "approve DP-2")
    assert not late["ok"] and "exceeds" in late["receipt"]
    assert anon_client.get(f"{API}/proposals/DP-2").json()["status"] == "pending"


def test_operator_confirms_movement_and_status_is_readable(anon_client, db, make_delivery):
    delivery = _setup(anon_client, db, make_delivery)
    _propose(anon_client, "disposition", delivery.id, DISP)
    _gate(anon_client, SUP, "approve DP-1")
    mv = {"input_ref": delivery.id, "output_lot_id": "LOT-A", "stage": "receiving_to_processing",
          "quantity_in": 450, "quantity_out": 450, "quantity_unit": "kg"}
    unbalanced = _propose(anon_client, "movement", delivery.id, {**mv, "quantity_out": 400})
    assert unbalanced.status_code == 422
    assert _propose(anon_client, "movement", delivery.id, mv).json()["id"] == "MV-2"

    auditor = _gate(anon_client, AUD, "confirm MV-2")
    assert not auditor["ok"]
    confirmed = _gate(anon_client, OP, "@qc-gate confirm MV-2")
    assert confirmed["ok"]
    assert db.query(MaterialMovement).one().operator_id == "floor.operator"

    status = _gate(anon_client, AUD, f"status {delivery.id}")
    assert status["ok"] and "dispositioned 450/500" in status["receipt"]
    garbage = _gate(anon_client, SUP, "@qc-gate looks good, approve it")
    assert not garbage["ok"] and "understands only" in garbage["receipt"]
