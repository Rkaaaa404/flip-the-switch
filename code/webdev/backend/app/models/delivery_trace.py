import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class DeliveryStatus(str, enum.Enum):
    ACTIVE_RECEIVING = "active_receiving"
    INSPECTION_COMPLETE = "inspection_complete"
    DISPOSITION_RECORDED = "disposition_recorded"
    CLOSED = "closed"


class QuantityUnit(str, enum.Enum):
    KG = "kg"
    COUNT = "count"


class ViewSide(str, enum.Enum):
    DORSAL = "dorsal"
    VENTRAL = "ventral"


class InspectionStatus(str, enum.Enum):
    COMPLETE = "COMPLETE"
    PARTIAL_DORSAL_ONLY = "PARTIAL_DORSAL_ONLY"
    PARTIAL_VENTRAL_ONLY = "PARTIAL_VENTRAL_ONLY"
    FAILED_CAPTURE = "FAILED_CAPTURE"


class DispositionOutcome(str, enum.Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    REPROCESS = "REPROCESS"
    DOWNGRADE = "DOWNGRADE"


class ProcessingStage(str, enum.Enum):
    RECEIVING_TO_STORAGE = "receiving_to_storage"
    RECEIVING_TO_PROCESSING = "receiving_to_processing"
    PROCESSING_WGGS = "processing_wggs"
    PROCESSING_FILLET = "processing_fillet"
    STORAGE_TO_PROCESSING = "storage_to_processing"
    PROCESSING_TO_DISPATCH = "processing_to_dispatch"


class InferenceMode(str, enum.Enum):
    REAL_ONNX = "real_onnx"
    SIMULATED_MOCK = "simulated_mock"
    SKIPPED_UNSUPPORTED = "skipped_unsupported"


class ReceivingDelivery(Base):
    __tablename__ = "receiving_deliveries"

    id = Column(String(64), primary_key=True)
    supplier_name = Column(String(255), nullable=False)
    species = Column(String(128), nullable=False)
    fish_family = Column(String(64), nullable=False)
    received_at = Column(DateTime, nullable=False, default=utcnow)
    stated_quantity = Column(Float, nullable=False)
    quantity_unit = Column(String(16), nullable=False)
    truck_identifier = Column(String(64), nullable=True)
    status = Column(String(32), nullable=False, default=DeliveryStatus.ACTIVE_RECEIVING.value)
    created_by = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow, index=True)

    inspections = relationship(
        "FishInspection",
        back_populates="delivery",
        order_by="FishInspection.sequence_in_delivery",
    )
    dispositions = relationship("HumanDisposition", order_by="HumanDisposition.id")
    movements = relationship("MaterialMovement", order_by="MaterialMovement.id")


class FishInspection(Base):
    __tablename__ = "fish_inspections"
    __table_args__ = (
        UniqueConstraint("delivery_id", "sequence_in_delivery", name="uq_fish_delivery_sequence"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_id = Column(String(64), ForeignKey("receiving_deliveries.id"), nullable=False, index=True)
    sequence_in_delivery = Column(Integer, nullable=False)
    status = Column(String(32), nullable=False)
    flagged_for_review = Column(Boolean, nullable=False, default=False)
    flag_reasons_json = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow, index=True)

    delivery = relationship("ReceivingDelivery", back_populates="inspections")
    views = relationship("InspectionView", back_populates="fish_inspection", order_by="InspectionView.id")


class InspectionView(Base):
    __tablename__ = "inspection_views"
    __table_args__ = (
        UniqueConstraint("fish_inspection_id", "view_side", name="uq_view_fish_side"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    fish_inspection_id = Column(Integer, ForeignKey("fish_inspections.id"), nullable=False, index=True)
    view_side = Column(String(16), nullable=False)
    image_path = Column(String(512), nullable=False)
    sha256 = Column(String(64), nullable=False)
    freshness_grade = Column(String(16), nullable=False)
    freshness_confidence = Column(Float, nullable=False)
    defects_detected_json = Column(Text, nullable=False, default="[]")
    inference_mode = Column(String(32), nullable=False)
    inference_latency_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow, index=True)

    fish_inspection = relationship("FishInspection", back_populates="views")


class HumanDisposition(Base):
    __tablename__ = "human_dispositions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_id = Column(String(64), ForeignKey("receiving_deliveries.id"), nullable=False, index=True)
    output_lot_id = Column(String(64), nullable=True, index=True)
    disposition = Column(String(32), nullable=False)
    affected_quantity = Column(Float, nullable=False)
    quantity_unit = Column(String(16), nullable=False)
    decision_reason = Column(Text, nullable=False)
    authorized_by = Column(String(64), nullable=False)
    decided_at = Column(DateTime, nullable=False, default=utcnow, index=True)
    supersedes_id = Column(Integer, ForeignKey("human_dispositions.id"), nullable=True, unique=True)
    authorized_via = Column(String(32), nullable=True)  # "switch_gate" when signed in a Switch room
    switch_message_id = Column(String(64), nullable=True, index=True)


class MaterialMovement(Base):
    __tablename__ = "material_movements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_id = Column(String(64), ForeignKey("receiving_deliveries.id"), nullable=False, index=True)
    input_ref = Column(String(64), nullable=False, index=True)
    output_lot_id = Column(String(64), nullable=False, unique=True, index=True)
    stage = Column(String(64), nullable=False)
    quantity_in = Column(Float, nullable=False)
    quantity_out = Column(Float, nullable=False)
    quantity_unit = Column(String(16), nullable=False)
    normal_yield_loss = Column(Float, nullable=False, default=0.0)
    qc_reject_loss = Column(Float, nullable=False, default=0.0)
    unexplained_variance = Column(Float, nullable=False, default=0.0)
    operator_id = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=utcnow, index=True)
    notes = Column(Text, nullable=True)
    authorized_via = Column(String(32), nullable=True)
    switch_message_id = Column(String(64), nullable=True, index=True)
