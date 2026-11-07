from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from datetime import datetime

class StorageSlot(Base):
    __tablename__ = "storage_slots"

    slot_id = Column(String(20), primary_key=True, index=True) # e.g. "A01".."E05", "F-01".."F-10"
    zone = Column(String(20), nullable=False)                    # "cold" | "frozen"
    lot_id = Column(String(64), nullable=True, index=True)      # Assigned Lot ID
    assigned_at = Column(DateTime, nullable=True)
    assigned_by = Column(String(64), default="QC Supervisor", nullable=True)
