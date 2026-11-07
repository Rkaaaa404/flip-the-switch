from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db
from app.schemas.inspection import InspectionResultSchema
from app.services.inspection_service import InspectionService

router = APIRouter()

@router.post(
    "/run",
    # response_model=InspectionResultSchema,
    status_code=status.HTTP_200_OK,
    summary="Run Fish Quality Inspection Snapshot",
    description="Processes a single snapshot image, computes freshness & defects, sets hardware signal, and stores QC log."
)
async def run_inspection(
    image: UploadFile = File(..., description="Snapshot image file of the fish on conveyor"),
    fish_family: Optional[str] = Form(None, description="Fish type (e.g. Tuna, Mackarel, Nila)"),
    family: Optional[str] = Form(None, description="Frontend alias for fish_family"),
    lot_id: Optional[str] = Form(None, description="Optional custom lot identifier"),
    db: Session = Depends(get_db)
):

    selected_family = family or fish_family or "Tuna"  # Default to Tuna if not provided

    # Validate image file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a valid image (JPEG, PNG, WEBP)."
        )

    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image file is empty."
        )

    # Execute inspection pipeline
    result = await InspectionService.process_inspection(
        image_bytes=image_bytes,
        filename=image.filename or "snapshot.jpg",
        fish_family=selected_family,
        db=db,
        custom_lot_id=lot_id
    )

    # Return dual-compatible payload (snake_case + camelCase)
    res_dict = result.model_dump() if hasattr(result, "model_dump") else result.dict()
    res_dict.update({
        "lotId": result.lot_id,
        "confidence": round(result.grade_confidence * 100, 1) if result.grade_confidence <= 1.0 else result.grade_confidence,
        "conveyorSignal": result.hardware_signal,
        "freshnessNote": f"Grade {result.grade} ({int(result.grade_confidence * 100) if result.grade_confidence <= 1.0 else int(result.grade_confidence)}% confidence)",
        "processingTimeMs": result.processing_time_ms,
        "imageUrl": result.image_url,
    })
    return res_dict

# Endpoint Alias for compatibility with Section 8.3 of Proposal V3
@router.post(
    "/inspect",
    # response_model=InspectionResultSchema,
    include_in_schema=False
)
async def inspect_fish_alias(
    image: UploadFile = File(...),
    fish_family: Optional[str] = Form(None),
    family: Optional[str] = Form(None),
    lot_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    return await run_inspection(
        image=image,
        fish_family=fish_family,
        family=family,
        lot_id=lot_id,
        db=db
    )