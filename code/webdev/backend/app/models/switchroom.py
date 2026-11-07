"""Tables for the Switch room workflow: verified identities, agent proposals and gate commands."""

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base
from app.models.delivery_trace import utcnow

ROLES = ("qc_supervisor", "floor_operator", "auditor")


class SwitchIdentity(Base):
    """Maps a Switch-issued sender id to a person and their plant role."""

    __tablename__ = "switch_identities"

    participant_id = Column(String(255), primary_key=True)
    username = Column(String(64), nullable=False)
    role = Column(String(32), nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)


class RecordProposal(Base):
    """A disposition or movement drafted by qc-agent, applied only by an authorized gate command."""

    __tablename__ = "record_proposals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kind = Column(String(16), nullable=False)  # disposition | movement
    delivery_id = Column(String(64), nullable=False, index=True)
    payload_json = Column(Text, nullable=False)
    status = Column(String(16), nullable=False, default="pending")  # pending | applied | rejected
    source_message_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    decided_by = Column(String(64), nullable=True)
    decided_at = Column(DateTime, nullable=True)
    decision_note = Column(Text, nullable=True)
    applied_record_id = Column(Integer, nullable=True)

    @property
    def public_id(self) -> str:
        return f"{'DP' if self.kind == 'disposition' else 'MV'}-{self.id}"


class GateCommand(Base):
    """Every command the gate relayed, keyed by Switch message id so a replay changes nothing."""

    __tablename__ = "gate_commands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    switch_message_id = Column(String(64), nullable=False, unique=True)
    sender = Column(String(255), nullable=False)
    sender_name = Column(String(255), nullable=True)
    room_id = Column(String(64), nullable=True)
    text = Column(Text, nullable=False)
    ok = Column(Integer, nullable=False, default=0)
    receipt = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)
