import io
import csv
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_db
from app.models.dispatch import Dispatch, DispatchLot
from app.models.inspection_record import InspectionRecord
from app.models.storage_slot import StorageSlot

router = APIRouter()

class CreateDispatchPayload(BaseModel):
    buyer_name: str
    destination: str
    container_no: Optional[str] = None
    dispatch_date: Optional[str] = None
    lot_ids: List[str]
    notes: Optional[str] = None

class UpdateStatusPayload(BaseModel):
    status: str # "pending" | "in_transit" | "delivered"

def generate_dispatch_id(db: Session) -> str:
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"DISP-{today_str}-"
    today_count = db.query(Dispatch).filter(
        Dispatch.dispatch_id.like(f"{prefix}%")
    ).count()
    return f"{prefix}{(today_count + 1):03d}"

@router.get(
    "",
    summary="List All Export Dispatch Records",
    description="Returns all dispatches with aggregate metrics and lot counts."
)
def get_dispatches(db: Session = Depends(get_db)):
    dispatches = db.query(Dispatch).order_by(desc(Dispatch.created_at)).all()
    total_count = len(dispatches)
    pending_count = sum(1 for d in dispatches if d.status == "pending")
    in_transit_count = sum(1 for d in dispatches if d.status in ["in_transit", "dispatched"])
    delivered_count = sum(1 for d in dispatches if d.status == "delivered")

    items = []
    for d in dispatches:
        lot_links = db.query(DispatchLot).filter(DispatchLot.dispatch_id == d.dispatch_id).all()
        # Normalize status
        normalized_status = "in_transit" if d.status == "dispatched" else d.status

        items.append({
            "dispatch_id": d.dispatch_id,
            "dispatchId": d.dispatch_id,
            "buyer_name": d.buyer_name,
            "buyerName": d.buyer_name,
            "destination": d.destination,
            "container_no": d.container_no,
            "containerNo": d.container_no,
            "dispatch_date": d.dispatch_date.strftime("%Y-%m-%d %H:%M") if d.dispatch_date else None,
            "dispatchDate": d.dispatch_date.strftime("%Y-%m-%d %H:%M") if d.dispatch_date else None,
            "status": normalized_status,
            "notes": d.notes,
            "lots_count": len(lot_links),
            "lotsCount": len(lot_links),
            "created_at": d.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    return {
        "total_dispatches": total_count,
        "totalDispatches": total_count,
        "pending": pending_count,
        "in_transit": in_transit_count,
        "inTransit": in_transit_count,
        "dispatched": in_transit_count, # Alias for backwards compatibility
        "delivered": delivered_count,
        "items": items
    }

@router.get(
    "/available-lots",
    summary="Get Lots Available for Dispatch",
    description="Returns lots currently stored in slots that have not yet been assigned to any dispatch."
)
def get_available_lots_for_dispatch(db: Session = Depends(get_db)):
    # Lots that are passed, actively assigned to a storage slot, and not yet dispatched
    records = db.query(InspectionRecord).filter(
        InspectionRecord.decision == "PASS",
        InspectionRecord.storage_slot != None,
        InspectionRecord.dispatch_id == None
    ).order_by(desc(InspectionRecord.stored_at)).all()

    return [
        {
            "id": r.id,
            "lot_id": r.lot_id,
            "lotId": r.lot_id,
            "timestamp": r.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fish_family": r.fish_family,
            "fishFamily": r.fish_family,
            "grade": r.grade,
            "grade_confidence": r.grade_confidence,
            "confidence": r.grade_confidence,
            "defects_count": r.defects_count,
            "defectsCount": r.defects_count,
            "decision": r.decision,
            "hardware_signal": r.hardware_signal,
            "storage_slot": r.storage_slot,
            "storageSlot": r.storage_slot,
            "storage_zone": r.storage_zone,
            "stored_at": r.stored_at.strftime("%Y-%m-%d %H:%M") if r.stored_at else r.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        for r in records
    ]

@router.get(
    "/{dispatch_id}",
    summary="Get Single Dispatch Record Details with QC Summary",
    description="Returns shipment metadata, associated lots list, and aggregated QC statistics."
)
def get_dispatch_detail(dispatch_id: str, db: Session = Depends(get_db)):
    disp = db.query(Dispatch).filter(Dispatch.dispatch_id == dispatch_id).first()
    if not disp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispatch '{dispatch_id}' not found"
        )

    links = db.query(DispatchLot).filter(DispatchLot.dispatch_id == dispatch_id).all()
    lot_ids = [link.lot_id for link in links]

    lots = db.query(InspectionRecord).filter(InspectionRecord.lot_id.in_(lot_ids)).all() if lot_ids else []

    total_lots = len(lots)
    all_passed = all(l.decision == "PASS" for l in lots) if lots else True
    avg_conf = (sum(l.grade_confidence for l in lots) / total_lots) if total_lots > 0 else 0.92
    total_defects = sum(l.defects_count for l in lots)

    lots_data = [
        {
            "id": l.id,
            "lot_id": l.lot_id,
            "lotId": l.lot_id,
            "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M"),
            "fish_family": l.fish_family,
            "fishFamily": l.fish_family,
            "grade": l.grade,
            "grade_confidence": l.grade_confidence,
            "confidence": l.grade_confidence,
            "defects_count": l.defects_count,
            "defectsCount": l.defects_count,
            "decision": l.decision,
            "hardware_signal": l.hardware_signal,
            "image_path": l.image_path,
            "imageUrl": l.image_path,
        }
        for l in lots
    ]

    normalized_status = "in_transit" if disp.status == "dispatched" else disp.status

    return {
        "dispatch_id": disp.dispatch_id,
        "dispatchId": disp.dispatch_id,
        "buyer_name": disp.buyer_name,
        "buyerName": disp.buyer_name,
        "destination": disp.destination,
        "container_no": disp.container_no,
        "containerNo": disp.container_no,
        "dispatch_date": disp.dispatch_date.strftime("%Y-%m-%d %H:%M") if disp.dispatch_date else None,
        "dispatchDate": disp.dispatch_date.strftime("%Y-%m-%d %H:%M") if disp.dispatch_date else None,
        "status": normalized_status,
        "notes": disp.notes,
        "created_at": disp.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lots": lots_data,
        "qc_summary": {
            "total_lots": total_lots,
            "all_passed": all_passed,
            "avg_confidence": round(avg_conf * 100, 1) if avg_conf <= 1.0 else round(avg_conf, 1),
            "total_defects": total_defects
        }
    }

@router.post(
    "",
    summary="Create New Export Dispatch Record",
    description="Registers a new shipment with selected lots and assigns them to buyer & destination."
)
def create_dispatch(payload: CreateDispatchPayload, db: Session = Depends(get_db)):
    if not payload.lot_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one lot must be selected for dispatch"
        )

    dispatch_id = generate_dispatch_id(db)

    # Parse dispatch date or default to now
    disp_date = datetime.utcnow()
    if payload.dispatch_date:
        try:
            disp_date = datetime.fromisoformat(payload.dispatch_date.replace("Z", ""))
        except Exception:
            disp_date = datetime.utcnow()

    new_dispatch = Dispatch(
        dispatch_id=dispatch_id,
        buyer_name=payload.buyer_name,
        destination=payload.destination,
        container_no=payload.container_no or f"CONT-{datetime.utcnow().strftime('%Y%m%d')}-001",
        dispatch_date=disp_date,
        status="pending",
        notes=payload.notes,
        created_at=datetime.utcnow()
    )
    db.add(new_dispatch)

    # Associate lots
    for lid in payload.lot_ids:
        link = DispatchLot(dispatch_id=dispatch_id, lot_id=lid)
        db.add(link)

        # Update inspection record
        rec = db.query(InspectionRecord).filter(InspectionRecord.lot_id == lid).first()
        if rec:
            rec.dispatch_id = dispatch_id
            rec.dispatched_at = disp_date

    db.commit()
    db.refresh(new_dispatch)

    return {
        "status": "success",
        "message": f"Dispatch {dispatch_id} created successfully with {len(payload.lot_ids)} lots",
        "dispatch_id": dispatch_id,
        "dispatchId": dispatch_id
    }

@router.patch(
    "/{dispatch_id}/status",
    summary="Update Dispatch Status",
    description="Updates dispatch status to pending, in_transit, or delivered."
)
def update_dispatch_status(
    dispatch_id: str,
    payload: UpdateStatusPayload,
    db: Session = Depends(get_db)
):
    disp = db.query(Dispatch).filter(Dispatch.dispatch_id == dispatch_id).first()
    if not disp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispatch '{dispatch_id}' not found"
        )

    new_status = "in_transit" if payload.status == "dispatched" else payload.status
    disp.status = new_status

    if new_status in ["in_transit", "delivered"]:
        # Free up storage slots for lots that are now shipped/delivered
        lot_links = db.query(DispatchLot).filter(DispatchLot.dispatch_id == dispatch_id).all()
        for link in lot_links:
            slot = db.query(StorageSlot).filter(StorageSlot.lot_id == link.lot_id).first()
            if slot:
                slot.lot_id = None
                slot.assigned_at = None
            rec = db.query(InspectionRecord).filter(InspectionRecord.lot_id == link.lot_id).first()
            if rec:
                rec.storage_slot = None
                rec.storage_zone = None

    db.commit()

    return {
        "status": "success",
        "message": f"Dispatch {dispatch_id} status updated to {new_status}",
        "dispatch_id": dispatch_id,
        "new_status": new_status,
        "status": new_status
    }

@router.get(
    "/{dispatch_id}/export",
    summary="Export Dispatch Manifest Summary CSV",
    description="Downloads a CSV QC certificate manifest for the specified dispatch shipment."
)
def export_dispatch_csv(dispatch_id: str, db: Session = Depends(get_db)):
    disp = db.query(Dispatch).filter(Dispatch.dispatch_id == dispatch_id).first()
    if not disp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispatch '{dispatch_id}' not found"
        )

    links = db.query(DispatchLot).filter(DispatchLot.dispatch_id == dispatch_id).all()
    lot_ids = [link.lot_id for link in links]
    lots = db.query(InspectionRecord).filter(InspectionRecord.lot_id.in_(lot_ids)).all() if lot_ids else []

    output = io.StringIO()
    writer = csv.writer(output)

    # Manifest Header Information
    writer.writerow(["NusaQC Export Dispatch Certificate & Traceability Manifest"])
    writer.writerow(["Dispatch ID", disp.dispatch_id])
    writer.writerow(["Buyer / Company", disp.buyer_name])
    writer.writerow(["Destination Country", disp.destination])
    writer.writerow(["Container Number", disp.container_no or "-"])
    writer.writerow(["Dispatch Date", disp.dispatch_date.strftime("%Y-%m-%d %H:%M") if disp.dispatch_date else "-"])
    writer.writerow(["Shipment Status", disp.status.upper()])
    writer.writerow([])

    # Table Header
    writer.writerow(["Lot ID", "Fish Family", "Freshness Grade", "Confidence Score", "Defects Count", "Decision", "Inspection Date"])

    for l in lots:
        conf_str = f"{(l.grade_confidence * 100):.1f}%" if l.grade_confidence <= 1.0 else f"{l.grade_confidence:.1f}%"
        writer.writerow([
            l.lot_id,
            l.fish_family,
            f"Grade {l.grade}",
            conf_str,
            l.defects_count,
            l.decision,
            l.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])

    output.seek(0)
    filename = f"NusaQC_Manifest_{dispatch_id}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
