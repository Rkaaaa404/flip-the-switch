from pydantic import BaseModel

class DashboardStatsSchema(BaseModel):
    total_inspected_today: int
    current_lot_id: str
    pass_rate: float        # e.g., 94.2
    pass_rate_delta: float  # e.g., +2.4
    fail_rate: float        # e.g., 5.8
    avg_confidence: float   # e.g., 91.5

#   total_inspected_today: number;
#   current_lot_id: string;
#   pass_rate: number;
#   pass_rate_delta: number;
#   fail_rate: number;
#   fail_rate_delta: number;
#   avg_confidence_score: number;
