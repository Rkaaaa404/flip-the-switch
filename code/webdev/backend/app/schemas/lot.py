from pydantic import BaseModel
from typing import List, Optional
from app.schemas.inspection import DecisionType, GradeType, FishFamilyType, DefectSchema

class LotRecordSchema(BaseModel):
    id: int
    lot_id: str
    timestamp: str
    fish_family: FishFamilyType
    grade: GradeType
    grade_confidence: float
    defects_count: int
    decision: DecisionType
    hardware_signal: str
    processing_time_ms: int
    image_path: Optional[str] = None

    class Config:
        from_attributes = True

class LotDetailSchema(LotRecordSchema):
    defects: List[DefectSchema] = []

class LotListResponseSchema(BaseModel):
    items: List[LotRecordSchema]
    total: int
    page: int
    limit: int
    total_pages: int
#   lot_id: string;
#   fish_family: string;
#   grade: Grade;
#   decision: Decision;
#   confidence: number;
#   timestamp: string;
