from pydantic import BaseModel, Field
from typing import List, Literal

DecisionType = Literal["PASS", "FAIL", "CONDITIONAL"]
HardwareSignalType = Literal["GREEN", "YELLOW", "RED"]
GradeType = Literal["A", "B", "C"]

DefectLabelType = Literal[
    "sisik_sisa", 
    "warna_abnormal", 
    "luka_robekan", 
    "lendir_berlebih"
]

class DefectSchema(BaseModel):
    label: str
    bbox: List[float] = Field(..., description="[x1, y1, x2, y2] bounding box coordinates")
    confidence: float = Field(..., ge=0.0, le=1.0)

class InspectionResultSchema(BaseModel):
    lot_id: str
    timestamp: str  # ISO 8601 string
    fish_family: str
    grade: GradeType
    grade_confidence: float
    defects: List[DefectSchema]
    decision: DecisionType
    hardware_signal: HardwareSignalType
    processing_time_ms: int
    image_url: str = ""

    class Config:
        from_attributes = True

# export type InspectionResult = {
#   lot_id: string;
#   timestamp: string; // ISO 8601
#   fish_family: "Scombridae" | "Cichlidae" | "Salmonidae";
#   grade: Grade;
#   grade_confidence: number;
#   defects: Defect[];
#   decision: Decision;
#   hardware_signal: HardwareSignal;
#   processing_time_ms: number;
# };
