"""Pydantic schemas for delivery traceability: requests, reads and trace responses."""

import json
from datetime import datetime
from typing import Literal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.schemas.inspection import DefectSchema

QuantityUnitT = Literal["kg", "count"]
DeliveryStatusT = Literal["active_receiving", "inspection_complete", "disposition_recorded", "closed"]
InspectionStatusT = Literal["COMPLETE", "PARTIAL_DORSAL_ONLY", "PARTIAL_VENTRAL_ONLY", "FAILED_CAPTURE"]
ViewSideT = Literal["dorsal", "ventral"]
FreshnessGradeT = Literal["A", "B", "C", "UNSUPPORTED"]
InferenceModeT = Literal["real_onnx", "simulated_mock", "skipped_unsupported"]
DispositionT = Literal["ACCEPT", "REJECT", "REPROCESS", "DOWNGRADE"]
StageT = Literal[
    "receiving_to_storage",
    "receiving_to_processing",
    "processing_wggs",
    "processing_fillet",
    "storage_to_processing",
    "processing_to_dispatch",
]
MissingLinkKindT = Literal[
    "PARTIAL_INSPECTION",
    "FLAGGED_WITHOUT_DISPOSITION",
    "UNDISPOSITIONED_QUANTITY",
    "DISPOSITION_LOT_NOT_HANDED_OFF",
    "LOT_LOCATION_UNKNOWN",
    "NO_UPSTREAM_MOVEMENT",
    "DELIVERY_NOT_FOUND",
]

_STRIPPED = ConfigDict(str_strip_whitespace=True)


class DeliveryCreate(BaseModel):
    model_config = _STRIPPED

    supplier_name: str = Field(min_length=1, max_length=255)
    species: str = Field(min_length=1, max_length=128)
    fish_family: str = Field(min_length=1, max_length=64)
    stated_quantity: float = Field(gt=0)
    quantity_unit: QuantityUnitT
    truck_identifier: str | None = Field(default=None, max_length=64)
    created_by: str = Field(min_length=1, max_length=64)
    received_at: datetime | None = None


class DeliveryStatusUpdate(BaseModel):
    status: Literal["inspection_complete", "closed"]


class HumanDispositionCreate(BaseModel):
    model_config = _STRIPPED

    output_lot_id: str | None = Field(default=None, max_length=64)
    disposition: DispositionT
    affected_quantity: float = Field(gt=0)
    quantity_unit: QuantityUnitT
    decision_reason: str = Field(min_length=1)
    authorized_by: str = Field(min_length=1, max_length=64)
    supersedes_id: int | None = None

    @model_validator(mode="after")
    def _lot_required_unless_reject(self) -> "HumanDispositionCreate":
        if self.disposition != "REJECT" and not self.output_lot_id:
            raise ValueError("output_lot_id is required unless disposition is REJECT")
        return self


class MaterialMovementCreate(BaseModel):
    model_config = _STRIPPED

    input_ref: str = Field(min_length=1, max_length=64)
    output_lot_id: str = Field(min_length=1, max_length=64)
    stage: StageT
    quantity_in: float = Field(gt=0)
    quantity_out: float = Field(ge=0)
    quantity_unit: QuantityUnitT
    normal_yield_loss: float = Field(default=0.0, ge=0)
    qc_reject_loss: float = Field(default=0.0, ge=0)
    unexplained_variance: float = 0.0
    operator_id: str = Field(min_length=1, max_length=64)
    notes: str | None = None

    @model_validator(mode="after")
    def _check_balance(self) -> "MaterialMovementCreate":
        if self.output_lot_id == self.input_ref:
            raise ValueError("output_lot_id must differ from input_ref")
        accounted = (
            self.quantity_out + self.normal_yield_loss + self.qc_reject_loss + self.unexplained_variance
        )
        if abs(self.quantity_in - accounted) > 1e-6 * max(1.0, self.quantity_in):
            raise ValueError(
                f"quantity_in ({self.quantity_in}) does not balance with accounted quantity ({accounted})"
            )
        return self


class SimulateRequest(BaseModel):
    count: int = Field(default=5, ge=1, le=50)
    drop_ventral_every: int | None = Field(default=None, ge=2)


class DeliveryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    supplier_name: str
    species: str
    fish_family: str
    received_at: datetime
    stated_quantity: float
    quantity_unit: QuantityUnitT
    truck_identifier: str | None
    status: DeliveryStatusT
    created_by: str
    created_at: datetime


class DeliverySummary(DeliveryRead):
    total_inspected: int = 0
    flagged_count: int = 0
    partial_count: int = 0


class DeliveryListResponse(BaseModel):
    items: list[DeliverySummary]
    total: int
    page: int
    limit: int
    total_pages: int


class InspectionViewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    view_side: ViewSideT
    image_path: str
    sha256: str
    freshness_grade: FreshnessGradeT
    freshness_confidence: float
    defects: list[DefectSchema] = Field(
        default_factory=list, validation_alias=AliasChoices("defects", "defects_detected_json")
    )
    inference_mode: InferenceModeT
    inference_latency_ms: int
    created_at: datetime

    @field_validator("defects", mode="before")
    @classmethod
    def _decode_json(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return json.loads(value)
        return value


class FishInspectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sequence_in_delivery: int
    status: InspectionStatusT
    flagged_for_review: bool
    flag_reasons: list[str] = Field(
        default_factory=list, validation_alias=AliasChoices("flag_reasons", "flag_reasons_json")
    )
    created_at: datetime
    views: list[InspectionViewRead] = []

    @field_validator("flag_reasons", mode="before")
    @classmethod
    def _decode_json(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return json.loads(value)
        return value


class HumanDispositionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    delivery_id: str
    output_lot_id: str | None
    disposition: DispositionT
    affected_quantity: float
    quantity_unit: QuantityUnitT
    decision_reason: str
    authorized_by: str
    decided_at: datetime
    supersedes_id: int | None
    superseded: bool = False
    authorized_via: str | None = None
    switch_message_id: str | None = None


class MaterialMovementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    delivery_id: str
    input_ref: str
    output_lot_id: str
    stage: StageT
    quantity_in: float
    quantity_out: float
    quantity_unit: QuantityUnitT
    normal_yield_loss: float
    qc_reject_loss: float
    unexplained_variance: float
    operator_id: str
    timestamp: datetime
    notes: str | None
    authorized_via: str | None = None
    switch_message_id: str | None = None


class StorageSlotRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slot_id: str
    zone: str
    assigned_at: datetime | None = None


class DispatchRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dispatch_id: str
    buyer_name: str
    destination: str
    status: str
    dispatch_date: datetime


class MovementNode(MaterialMovementRead):
    storage_slots: list[StorageSlotRef] = []
    dispatches: list[DispatchRef] = []


class MissingLink(BaseModel):
    kind: MissingLinkKindT
    ref: str
    detail: str


class InspectionSummary(BaseModel):
    total: int = 0
    complete: int = 0
    partial_dorsal_only: int = 0
    partial_ventral_only: int = 0
    failed_capture: int = 0
    flagged: int = 0


class QuantityBalance(BaseModel):
    stated_quantity: float
    quantity_unit: QuantityUnitT
    dispositioned_quantity: float
    allocated_from_intake: float
    unallocated_quantity: float


class DeliveryDetailResponse(BaseModel):
    delivery: DeliverySummary
    inspections: list[FishInspectionRead]
    inspections_total: int
    page: int
    limit: int
    dispositions: list[HumanDispositionRead]
    movements: list[MaterialMovementRead]


class DeliveryTraceTreeResponse(BaseModel):
    delivery: DeliveryRead
    inspection_summary: InspectionSummary
    dispositions: list[HumanDispositionRead]
    movements: list[MovementNode]
    balance: QuantityBalance
    missing_links: list[MissingLink]


class LotProvenanceResponse(BaseModel):
    lot_id: str
    delivery: DeliveryRead | None = None
    chain: list[MaterialMovementRead]
    missing_links: list[MissingLink]
