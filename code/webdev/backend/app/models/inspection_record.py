from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from app.core.database import Base
from datetime import datetime

class InspectionRecord(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lot_id = Column(String(64), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    fish_family = Column(String(32), nullable=False)                        # Scombridae, Cichlidae, Salmonidae
    grade = Column(String(8), nullable=False)                               # A, B, C
    grade_confidence = Column(Float, nullable=False)                        # 0.0 to 1.0 (or 0-100)
    defects_count = Column(Integer, default=0, nullable=False)
    defects_json = Column(Text, default="[]", nullable=False)               # JSON array of {label, bbox, confidence}
    decision = Column(String(16), nullable=False)                           # PASS, FAIL, CONDITIONAL
    hardware_signal = Column(String(16), nullable=False)                    # GREEN, YELLOW, RED
    processing_time_ms = Column(Integer, default=0, nullable=False)
    image_path = Column(String(255), nullable=True)
    inspector_note = Column(Text, nullable=True)
    reason_summary = Column(Text, nullable=True)

    # Storage and Dispatch Tracking
    storage_slot = Column(String(20), nullable=True, index=True)
    storage_zone = Column(String(20), nullable=True)                         # cold, frozen
    stored_at = Column(DateTime, nullable=True)
    dispatch_id = Column(String(50), nullable=True, index=True)
    dispatched_at = Column(DateTime, nullable=True)


    # lot_id: string;
    # timestamp: string; // ISO 8601
    # fish_family: "Scombridae" | "Cichlidae" | "Salmonidae";
    # grade: Grade;
    # grade_confidence: number;
    # defects: Defect[];
    # decision: Decision;
    # hardware_signal: HardwareSignal;
    # processing_time_ms: number;
