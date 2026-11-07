"""Request and response schemas for the Switch room workflow."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ProposalCreate(BaseModel):
    """Drafted by qc-agent. ``payload`` is a disposition or movement body without the signer field."""

    kind: Literal["disposition", "movement"]
    delivery_id: str = Field(min_length=1, max_length=64)
    payload: dict[str, Any]
    source_message_id: str | None = Field(default=None, max_length=64)


class ProposalRead(BaseModel):
    id: str
    kind: str
    delivery_id: str
    payload: dict[str, Any]
    status: str
    source_message_id: str | None
    created_at: datetime
    decided_by: str | None
    decided_at: datetime | None
    decision_note: str | None
    applied_record_id: int | None
    approve_command: str


class GateCommandIn(BaseModel):
    """Relayed verbatim by qc-gate. ``sender`` is the participant id Switch put on the event."""

    sender: str = Field(min_length=1, max_length=255)
    sender_name: str | None = Field(default=None, max_length=255)
    room_id: str | None = Field(default=None, max_length=64)
    message_id: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1, max_length=2000)


class GateReceipt(BaseModel):
    ok: bool
    receipt: str
    replayed: bool = False


class IdentityUpsert(BaseModel):
    participant_id: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=64)
    role: Literal["qc_supervisor", "floor_operator", "auditor"]
