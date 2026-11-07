from datetime import datetime, time as dtime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.api.deps import get_db
from app.models.inspection_record import InspectionRecord

router = APIRouter()

@router.get(
    "/stats",
    # response_model=DashboardStatsSchema,
    summary="Get Real-Time Dashboard KPI Statistics",
    description="Aggregates today's inspection totals, pass/fail rates, and active lot for HeadSection.tsx."
)
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Start of today (00:00:00 UTC)
    today_start = datetime.combine(datetime.utcnow().date(), dtime.min)

    # Today's records
    today_query = db.query(InspectionRecord).filter(InspectionRecord.timestamp >= today_start)
    total_today = today_query.count()

    if total_today == 0:
        # Fallback defaults if no records yet today
        latest_record = db.query(InspectionRecord).order_by(desc(InspectionRecord.timestamp)).first()
        active_lot = latest_record.lot_id if latest_record else "LOT-READY"

        return {
            "total_inspected_today": 0,
            "totalInspectedToday": 0,
            "current_lot_id": active_lot,
            "currentLotId": active_lot,
            "pass_rate": 100.0,
            "passRate": 100.0,
            "pass_rate_delta": 0.0,
            "passRateDelta": 0.0,
            "fail_rate": 0.0,
            "failRate": 0.0,
            "avg_confidence": 95.0,
            "avgConfidence": 95.0,
            "avg_confidence_score": 95.0
        }

    # Calculate Passed vs Failed today
    passed_count = today_query.filter(InspectionRecord.decision == "PASS").count()
    failed_count = today_query.filter(InspectionRecord.decision == "FAIL").count()
    
    pass_rate = round((passed_count / total_today) * 100, 1)
    fail_rate = round((failed_count / total_today) * 100, 1)

    # Calculate Real Delta comparing Today vs Historical Baseline (Prior records)
    historical_query = db.query(InspectionRecord).filter(InspectionRecord.timestamp < today_start)
    hist_total = historical_query.count()
    if hist_total > 0:
        hist_passed = historical_query.filter(InspectionRecord.decision == "PASS").count()
        hist_failed = historical_query.filter(InspectionRecord.decision == "FAIL").count()
        hist_pass_rate = (hist_passed / hist_total) * 100
        hist_fail_rate = (hist_failed / hist_total) * 100
        pass_rate_delta = round(pass_rate - hist_pass_rate, 1)
        fail_rate_delta = round(fail_rate - hist_fail_rate, 1)
    else:
        pass_rate_delta = 0.0
        fail_rate_delta = 0.0

    # Average Confidence (strictly from Model 1 & 2 AI inference outputs)
    avg_conf = db.query(func.avg(InspectionRecord.grade_confidence)).filter(
        InspectionRecord.timestamp >= today_start
    ).scalar() or 0.90
    avg_confidence = round(float(avg_conf) * 100, 1) if avg_conf <= 1.0 else round(float(avg_conf), 1)

    # Current/Latest Lot ID
    latest_record = today_query.order_by(desc(InspectionRecord.timestamp)).first()
    current_lot_id = latest_record.lot_id if latest_record else "LOT-ACTIVE"

    return {
        "total_inspected_today": total_today,
        "totalInspectedToday": total_today,
        "current_lot_id": current_lot_id,
        "currentLotId": current_lot_id,
        "pass_rate": pass_rate,
        "passRate": pass_rate,
        "pass_rate_delta": pass_rate_delta,
        "passRateDelta": pass_rate_delta,
        "fail_rate": fail_rate,
        "failRate": fail_rate,
        "fail_rate_delta": fail_rate_delta,
        "failRateDelta": fail_rate_delta,
        "avg_confidence": avg_confidence,
        "avgConfidence": avg_confidence,
        "avg_confidence_score": avg_confidence
    }