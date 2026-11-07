from sqlalchemy import Column, String, Integer, DateTime, Text
from app.core.database import Base
from datetime import datetime

class Dispatch(Base):
    __tablename__ = "dispatches"

    dispatch_id = Column(String(64), primary_key=True, index=True) # e.g. "DISP-2026-0730-008"
    buyer_name = Column(String(128), nullable=False)
    destination = Column(String(64), nullable=False)               # "USA", "Japan", "China", "EU", etc.
    container_no = Column(String(64), nullable=True)               # e.g. "CONT-2026-001"
    dispatch_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending", nullable=False) # "pending" | "dispatched"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class DispatchLot(Base):
    __tablename__ = "dispatch_lots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispatch_id = Column(String(64), nullable=False, index=True)
    lot_id = Column(String(64), nullable=False, index=True)
