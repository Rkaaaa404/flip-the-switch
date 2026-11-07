from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_db
from app.models.storage_slot import StorageSlot
from app.models.inspection_record import InspectionRecord

router = APIRouter()

class AssignSlotRequest(BaseModel):
    slot_id: str
    lot_id: str

def init_default_storage_slots(db: Session):
    """Seed 35 default storage slots (25 Cold Zone, 10 Frozen Zone) if not already created."""
    if db.query(StorageSlot).count() == 0:
        slots = []
        # 1. Cold Zone (5 rows x 5 cols = 25 slots)
        for row in ["A", "B", "C", "D", "E"]:
            for col in range(1, 6):
                slot_id = f"{row}{col:02d}"
                slots.append(StorageSlot(slot_id=slot_id, zone="cold", lot_id=None))

        # 2. Frozen Zone (10 slots F-01 to F-10)
        for col in range(1, 11):
            slot_id = f"F-{col:02d}"
            slots.append(StorageSlot(slot_id=slot_id, zone="frozen", lot_id=None))

        db.add_all(slots)
        db.commit()

        # Re-sync any lots that have storage_slot set in inspections table
        stored_records = db.query(InspectionRecord).filter(
            InspectionRecord.storage_slot != None,
            InspectionRecord.dispatch_id == None
        ).all()
        for rec in stored_records:
            slot = db.query(StorageSlot).filter(StorageSlot.slot_id == rec.storage_slot).first()
            if slot:
                slot.lot_id = rec.lot_id
                slot.assigned_at = rec.stored_at or datetime.utcnow()
        db.commit()

@router.get(
    "/slots",
    summary="Get All Storage Slots & Overview Stats",
    description="Returns full grid status for Cold Zone and Frozen Zone storage slots."
)
def get_storage_slots(db: Session = Depends(get_db)):
    init_default_storage_slots(db)

    slots = db.query(StorageSlot).all()
    occupied_count = sum(1 for s in slots if s.lot_id is not None)
    total_slots = len(slots)
    available_count = total_slots - occupied_count

    # Pending assignment count (PASS lots not yet stored in a slot and not dispatched)
    pending_count = db.query(InspectionRecord).filter(
        InspectionRecord.decision == "PASS",
        InspectionRecord.storage_slot == None,
        InspectionRecord.dispatch_id == None
    ).count()

    # Map lot details to occupied slots
    slot_list = []
    for s in slots:
        lot_data = None
        if s.lot_id:
            record = db.query(InspectionRecord).filter(InspectionRecord.lot_id == s.lot_id).first()
            if record:
                lot_data = {
                    "id": record.id,
                    "lot_id": record.lot_id,
                    "lotId": record.lot_id,
                    "timestamp": record.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fish_family": record.fish_family,
                    "fishFamily": record.fish_family,
                    "grade": record.grade,
                    "grade_confidence": record.grade_confidence,
                    "confidence": record.grade_confidence,
                    "defects_count": record.defects_count,
                    "defectsCount": record.defects_count,
                    "decision": record.decision,
                    "hardware_signal": record.hardware_signal,
                    "conveyorSignal": record.hardware_signal,
                    "image_path": record.image_path,
                    "imageUrl": record.image_path,
                    "stored_at": record.stored_at.strftime("%Y-%m-%dT%H:%M:%SZ") if record.stored_at else None,
                }

        slot_list.append({
            "slot_id": s.slot_id,
            "slotId": s.slot_id,
            "zone": s.zone,
            "lot_id": s.lot_id,
            "lotId": s.lot_id,
            "assigned_at": s.assigned_at.strftime("%Y-%m-%d %H:%M:%S") if s.assigned_at else None,
            "assignedAt": s.assigned_at.strftime("%Y-%m-%d %H:%M:%S") if s.assigned_at else None,
            "assigned_by": s.assigned_by,
            "assignedBy": s.assigned_by,
            "lot": lot_data
        })

    return {
        "total_slots": total_slots,
        "totalSlots": total_slots,
        "occupied": occupied_count,
        "available": available_count,
        "pending_assignment": pending_count,
        "pendingAssignment": pending_count,
        "slots": slot_list
    }

@router.get(
    "/pending",
    summary="Get Lots Pending Storage Assignment",
    description="Returns lots with decision PASS that are not yet assigned to any storage slot and not dispatched."
)
def get_pending_storage_lots(db: Session = Depends(get_db)):
    pending_records = db.query(InspectionRecord).filter(
        InspectionRecord.decision == "PASS",
        InspectionRecord.storage_slot == None,
        InspectionRecord.dispatch_id == None
    ).order_by(desc(InspectionRecord.timestamp)).all()

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
            "conveyorSignal": r.hardware_signal,
            "image_path": r.image_path,
            "imageUrl": r.image_path,
        }
        for r in pending_records
    ]

@router.post(
    "/assign",
    summary="Assign Inspected Lot to Storage Slot",
    description="Places a PASS lot into a specific Cold or Frozen storage slot."
)
def assign_slot(payload: AssignSlotRequest, db: Session = Depends(get_db)):
    init_default_storage_slots(db)

    slot = db.query(StorageSlot).filter(StorageSlot.slot_id == payload.slot_id).first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Storage slot '{payload.slot_id}' not found"
        )

    record = db.query(InspectionRecord).filter(InspectionRecord.lot_id == payload.lot_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lot '{payload.lot_id}' not found"
        )

    # If slot already had a lot, unassign the old one
    if slot.lot_id and slot.lot_id != payload.lot_id:
        old_record = db.query(InspectionRecord).filter(InspectionRecord.lot_id == slot.lot_id).first()
        if old_record:
            old_record.storage_slot = None
            old_record.storage_zone = None
            old_record.stored_at = None

    now = datetime.utcnow()
    slot.lot_id = payload.lot_id
    slot.assigned_at = now
    slot.assigned_by = "QC Supervisor"

    record.storage_slot = slot.slot_id
    record.storage_zone = slot.zone
    record.stored_at = now

    db.commit()

    return {
        "status": "success",
        "message": f"Lot {payload.lot_id} successfully placed into slot {slot.slot_id}",
        "slot_id": slot.slot_id,
        "lot_id": payload.lot_id,
        "zone": slot.zone,
        "stored_at": now.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.delete(
    "/slots/{slot_id}",
    summary="Clear / Unassign Storage Slot",
    description="Empties the storage slot without deleting the inspection record."
)
def clear_slot(slot_id: str, db: Session = Depends(get_db)):
    slot = db.query(StorageSlot).filter(StorageSlot.slot_id == slot_id).first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Storage slot '{slot_id}' not found"
        )

    if slot.lot_id:
        record = db.query(InspectionRecord).filter(InspectionRecord.lot_id == slot.lot_id).first()
        if record:
            record.storage_slot = None
            record.storage_zone = None
            record.stored_at = None

        slot.lot_id = None
        slot.assigned_at = None
        db.commit()

    return {
        "status": "success",
        "message": f"Slot {slot_id} cleared successfully",
        "slot_id": slot_id
    }
