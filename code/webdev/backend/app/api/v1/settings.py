import re
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.ai import get_ai_engine
from app.models.system_setting import SystemSetting
from app.config import settings

router = APIRouter()


@router.get(
    "/models/status",
    summary="Get AI Model Status & Metadata",
    description="Powers AIModel.tsx with model versions, providers, and input shapes."
)
def get_models_status():
    ai = get_ai_engine()
    raw = ai.get_models_status()

    fresh_dict = raw.get("freshness_model") or raw.get("freshnessModel") or {
        "name": "MobileNetV3-Small Freshness Classifier",
        "version": "v1.0-onnx",
        "status": "Loaded (ONNX Runtime CPU)",
        "input_shape": [1, 3, 224, 224]
    }

    defect_dict = raw.get("defect_model") or raw.get("defectModel") or {
        "name": "YOLOv8s Surface Defect Detector",
        "version": "8.4.121",
        "status": "Loaded (ONNX Runtime CPU)",
        "input_shape": [1, 3, 640, 640]
    }

    return {
        "freshness_model": fresh_dict,
        "freshnessModel": fresh_dict,
        "defect_model": defect_dict,
        "defectModel": defect_dict,
    }

@router.get(
    "",
    summary="Get Active System Settings",
    description="Loads saved configurations for the settings page."
)
def get_settings(db: Session = Depends(get_db)):
    record = db.query(SystemSetting).filter(SystemSetting.key == "global_config").first()
    
    # Fallback defaults if not yet customized in database
    threshold = float(record.confidence_threshold) if record and record.confidence_threshold is not None else 0.75
    auto_export = bool(record.auto_export_csv) if record and record.auto_export_csv is not None else False
    retention = int(record.log_retention_days) if record and record.log_retention_days is not None else 30
    
    # Corrected typo: active_species
    species = record.active_species.split(",") if (record and record.active_species) else ["Scombridae", "Cichlidae", "Salmonidae"]
    mock_mode = bool(record.mock_mode_enabled) if record and record.mock_mode_enabled is not None else settings.ENABLE_MOCK_HARDWARE

    # Return dual-compatible payload (snake_case + camelCase)
    return {
        # Confidence threshold
        "confidence_threshold": threshold,
        "confidenceThreshold": threshold,
        "confidenceThresholdPercent": int(threshold * 100) if threshold <= 1.0 else int(threshold),
        
        # CSV Export
        "auto_export_csv": auto_export,
        "autoExportCsv": auto_export,
        "autoExportCSV": auto_export,
        
        # Log retention
        "log_retention_days": retention,
        "logRetentionDays": retention,
        "logRetention": f"{retention} days",
        
        # Species & Hardware
        "active_species": species,
        "activeSpecies": species,
        "selectedSpecies": species,
        "mock_mode_enabled": mock_mode,
        "mockModeEnabled": mock_mode,
        "mockMode": mock_mode
    }

@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Save System Settings (POST)"
)
@router.put(
    "",
    status_code=status.HTTP_200_OK,
    summary="Save System Settings (PUT)"
)
async def save_settings(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    # 1. Parse Confidence Threshold (handles 0.75 or 75)
    raw_thresh = payload.get("confidence_threshold") or payload.get("confidenceThreshold") or 0.75
    try:
        thresh = float(raw_thresh)
        if thresh > 1.0:
            thresh = thresh / 100.0  # Convert 75 -> 0.75
    except (ValueError, TypeError):
        thresh = 0.75

    # 2. Parse Auto Export CSV
    auto_exp = payload.get("auto_export_csv")
    if auto_exp is None:
        auto_exp = payload.get("autoExportCsv")
    if auto_exp is None:
        auto_exp = payload.get("autoExportCSV", False)
    auto_exp = bool(auto_exp)

    # 3. Parse Log Retention Days (handles "30 days", "30", or 30)
    raw_retention = payload.get("log_retention_days") or payload.get("logRetentionDays") or payload.get("logRetention") or 30
    if isinstance(raw_retention, str):
        digits = re.findall(r"\d+", raw_retention)
        retention = int(digits[0]) if digits else 30
    else:
        retention = int(raw_retention)

    # 4. Parse Active Species Whitelist
    raw_species = payload.get("active_species") or payload.get("activeSpecies") or payload.get("selectedSpecies") or ["Scombridae", "Cichlidae", "Salmonidae"]
    if isinstance(raw_species, list):
        species_str = ",".join(raw_species)
    else:
        species_str = str(raw_species)

    # 5. Parse Mock Mode
    raw_mock = payload.get("mock_mode_enabled")
    if raw_mock is None:
        raw_mock = payload.get("mockModeEnabled")
    if raw_mock is None:
        raw_mock = payload.get("mockMode", True)
    mock_mode = bool(raw_mock)

    # Persist changes into SQLite
    record = db.query(SystemSetting).filter(SystemSetting.key == "global_config").first()
    if not record:
        record = SystemSetting(
            key="global_config",
            confidence_threshold=thresh,
            auto_export_csv=auto_exp,
            log_retention_days=retention,
            active_species=species_str,
            mock_mode_enabled=mock_mode
        )
        db.add(record)
    else:
        record.confidence_threshold = thresh
        record.auto_export_csv = auto_exp
        record.log_retention_days = retention
        record.active_species = species_str
        record.mock_mode_enabled = mock_mode

    db.commit()
    db.refresh(record)

    return {
        "status": "success",
        "message": "Settings saved successfully",
        "saved_config": {
            "confidence_threshold": record.confidence_threshold,
            "confidenceThreshold": record.confidence_threshold,
            "auto_export_csv": record.auto_export_csv,
            "autoExportCsv": record.auto_export_csv,
            "log_retention_days": record.log_retention_days,
            "logRetentionDays": record.log_retention_days,
            "active_species": record.active_species.split(",") if record.active_species else [],
            "activeSpecies": record.active_species.split(",") if record.active_species else [],
            "mock_mode_enabled": record.mock_mode_enabled,
            "mockModeEnabled": record.mock_mode_enabled
        }
    }