"""Switch room workflow: qc-agent drafts proposals, and only verified people apply them through qc-gate.

The gate relays a chat command together with the sender id that Switch put on the event. Everything
that decides whether the command takes effect lives here, so it is tested without Switch running.
"""

import json
import re

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.delivery_trace import utcnow
from app.models.switchroom import GateCommand, RecordProposal, SwitchIdentity
from app.schemas.delivery_trace import HumanDispositionCreate, MaterialMovementCreate
from app.schemas.switchroom import GateCommandIn, GateReceipt, IdentityUpsert, ProposalCreate, ProposalRead
from app.services import material_lineage_service
from app.services.errors import DeliveryServiceError, NotFoundError, QuantityValidationError

PENDING_SIGNER = "pending-gate"
CAN = {
    "approve_dp": {"qc_supervisor"},
    "reject_dp": {"qc_supervisor"},
    "confirm_mv": {"floor_operator", "qc_supervisor"},
    "reject_mv": {"floor_operator", "qc_supervisor"},
    "status": {"qc_supervisor", "floor_operator", "auditor"},
}
HELP = (
    "qc-gate understands only: `approve DP-<n>` · `reject DP-<n> <reason>` · "
    "`confirm MV-<n>` · `reject MV-<n> <reason>` · `status DEL-<id>`"
)
_MENTION = re.compile(r"^\s*@?qc-gate\b[:,]?\s*", re.IGNORECASE)
_GRAMMAR = [
    ("approve_dp", re.compile(r"^approve\s+DP-(\d+)\s*$", re.IGNORECASE)),
    ("reject_dp", re.compile(r"^reject\s+DP-(\d+)\s+(.+)$", re.IGNORECASE | re.DOTALL)),
    ("confirm_mv", re.compile(r"^confirm\s+MV-(\d+)\s*$", re.IGNORECASE)),
    ("reject_mv", re.compile(r"^reject\s+MV-(\d+)\s+(.+)$", re.IGNORECASE | re.DOTALL)),
    ("status", re.compile(r"^status\s+(DEL-[\w-]+)\s*$", re.IGNORECASE)),
]


# ---------------------------------------------------------------- identities


def upsert_identity(db: Session, payload: IdentityUpsert) -> SwitchIdentity:
    row = db.get(SwitchIdentity, payload.participant_id)
    if row is None:
        row = SwitchIdentity(participant_id=payload.participant_id)
        db.add(row)
    row.username, row.role = payload.username, payload.role
    db.commit()
    db.refresh(row)
    return row


# ---------------------------------------------------------------- proposals


def _typed(kind: str, payload: dict, signer: str) -> HumanDispositionCreate | MaterialMovementCreate:
    body = dict(payload)
    if kind == "disposition":
        body["authorized_by"] = signer
        return HumanDispositionCreate(**body)
    body["operator_id"] = signer
    return MaterialMovementCreate(**body)


def _validate(db: Session, kind: str, delivery_id: str, typed) -> None:
    if kind == "disposition":
        material_lineage_service.validate_disposition(db, delivery_id, typed)
    else:
        material_lineage_service.validate_movement(db, delivery_id, typed)


def to_read(p: RecordProposal) -> ProposalRead:
    verb = "approve" if p.kind == "disposition" else "confirm"
    return ProposalRead(
        id=p.public_id,
        kind=p.kind,
        delivery_id=p.delivery_id,
        payload=json.loads(p.payload_json),
        status=p.status,
        source_message_id=p.source_message_id,
        created_at=p.created_at,
        decided_by=p.decided_by,
        decided_at=p.decided_at,
        decision_note=p.decision_note,
        applied_record_id=p.applied_record_id,
        approve_command=f"@qc-gate {verb} {p.public_id}",
    )


def create_proposal(db: Session, req: ProposalCreate) -> RecordProposal:
    """Validate a draft exactly as the real write would (minus the signer), then store it as pending."""
    payload = {k: v for k, v in req.payload.items() if k not in ("authorized_by", "operator_id")}
    try:
        typed = _typed(req.kind, payload, PENDING_SIGNER)
    except ValidationError as exc:
        raise QuantityValidationError("; ".join(e["msg"] for e in exc.errors())) from exc
    _validate(db, req.kind, req.delivery_id, typed)
    row = RecordProposal(
        kind=req.kind,
        delivery_id=req.delivery_id,
        payload_json=json.dumps(payload),
        status="pending",
        source_message_id=req.source_message_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def parse_public_id(public_id: str) -> tuple[str, int]:
    m = re.fullmatch(r"(DP|MV)-(\d+)", public_id.strip().upper())
    if not m:
        raise NotFoundError(f"proposal {public_id} not found")
    return ("disposition" if m.group(1) == "DP" else "movement"), int(m.group(2))


def get_proposal(db: Session, public_id: str) -> RecordProposal:
    kind, pk = parse_public_id(public_id)
    row = db.get(RecordProposal, pk)
    if row is None or row.kind != kind:
        raise NotFoundError(f"proposal {public_id} not found")
    return row


def list_proposals(db: Session, delivery_id: str | None = None, status: str | None = None) -> list[RecordProposal]:
    stmt = select(RecordProposal).order_by(RecordProposal.id)
    if delivery_id:
        stmt = stmt.where(RecordProposal.delivery_id == delivery_id)
    if status:
        stmt = stmt.where(RecordProposal.status == status)
    return list(db.scalars(stmt))


# ---------------------------------------------------------------- gate


def _parse(text: str) -> tuple[str, list[str]] | None:
    body = _MENTION.sub("", text.strip(), count=1).strip()
    for name, pattern in _GRAMMAR:
        m = pattern.match(body)
        if m:
            return name, [g.strip() for g in m.groups()]
    return None


def _describe(kind: str, payload: dict) -> str:
    if kind == "disposition":
        lot = f" → lot {payload['output_lot_id']}" if payload.get("output_lot_id") else ""
        return f"{payload['disposition']} {payload['affected_quantity']:g} {payload['quantity_unit']}{lot}"
    return (
        f"{payload['stage']} {payload['input_ref']} → {payload['output_lot_id']}, "
        f"in {payload['quantity_in']:g} / out {payload['quantity_out']:g} {payload['quantity_unit']}"
    )


def _status_text(db: Session, delivery_id: str) -> str:
    trace = material_lineage_service.get_delivery_lineage(db, delivery_id)
    s, b = trace.inspection_summary, trace.balance
    pending = [p.public_id for p in list_proposals(db, delivery_id, "pending")]
    return (
        f"📋 **{delivery_id}** ({trace.delivery.status}) · {s.total} fish, {s.flagged} flagged, "
        f"{s.total - s.complete} incomplete · dispositioned {b.dispositioned_quantity:g}/{b.stated_quantity:g} "
        f"{b.quantity_unit} · {len(trace.missing_links)} open gaps · pending: {', '.join(pending) or 'none'}"
    )


def _decide(db: Session, cmd: str, args: list[str], who: SwitchIdentity, req: GateCommandIn) -> tuple[bool, str]:
    if cmd == "status":
        return True, _status_text(db, args[0])

    kind = "disposition" if cmd.endswith("_dp") else "movement"
    prefix = "DP" if kind == "disposition" else "MV"
    public_id = f"{prefix}-{args[0]}"
    proposal = get_proposal(db, public_id)
    if proposal.status != "pending":
        return False, f"⛔ Not applied. {public_id} is already {proposal.status}."

    payload = json.loads(proposal.payload_json)
    if cmd.startswith("reject"):
        proposal.status, proposal.decision_note = "rejected", args[1]
        proposal.decided_by, proposal.decided_at = who.username, utcnow()
        db.commit()
        return True, f"🚫 {public_id} rejected by **{who.username}** ({who.role}): {args[1]}"

    extra = {"authorized_via": "switch_gate", "switch_message_id": req.message_id}
    typed = _typed(kind, payload, who.username)
    if kind == "disposition":
        record = material_lineage_service.record_disposition(db, proposal.delivery_id, typed, extra=extra)
        label = f"disposition #{record.id}"
    else:
        record = material_lineage_service.record_transformation_stage(db, proposal.delivery_id, typed, extra=extra)
        label = f"movement #{record.id}"
    proposal.status, proposal.applied_record_id = "applied", record.id
    proposal.decided_by, proposal.decided_at = who.username, utcnow()
    db.commit()
    return True, (
        f"✅ **{public_id} recorded** as {label}: {_describe(kind, payload)} on {proposal.delivery_id}. "
        f"Signed by **{who.username}** ({who.role}), Switch sender `{req.sender}`, message `{req.message_id}`."
    )


def handle_gate_command(db: Session, req: GateCommandIn) -> GateReceipt:
    """Apply one relayed chat command if, and only if, its verified sender is allowed to."""
    seen = db.scalar(select(GateCommand).where(GateCommand.switch_message_id == req.message_id))
    if seen is not None:
        return GateReceipt(ok=bool(seen.ok), receipt=seen.receipt, replayed=True)

    parsed = _parse(req.text)
    who = db.get(SwitchIdentity, req.sender)
    name = req.sender_name or req.sender
    if parsed is None:
        ok, receipt = False, HELP
    elif who is None:
        ok, receipt = False, f"⛔ Not applied. {name} is not a linked NusaQC identity, so I can't accept commands from them."
    elif who.role not in CAN[parsed[0]]:
        ok, receipt = False, (
            f"⛔ Not applied. **{who.username}** is `{who.role}`; "
            f"`{parsed[0].replace('_dp', ' DP').replace('_mv', ' MV')}` needs {' or '.join(sorted(CAN[parsed[0]]))}."
        )
    else:
        try:
            ok, receipt = _decide(db, parsed[0], parsed[1], who, req)
        except DeliveryServiceError as exc:
            db.rollback()
            ok, receipt = False, f"⛔ Not applied. {exc}"

    db.add(GateCommand(
        switch_message_id=req.message_id, sender=req.sender, sender_name=req.sender_name,
        room_id=req.room_id, text=req.text, ok=int(ok), receipt=receipt,
    ))
    try:
        db.commit()
    except IntegrityError:  # the same message raced in twice; the first one wins
        db.rollback()
        seen = db.scalar(select(GateCommand).where(GateCommand.switch_message_id == req.message_id))
        return GateReceipt(ok=bool(seen.ok), receipt=seen.receipt, replayed=True)
    return GateReceipt(ok=ok, receipt=receipt)
