import os
import io
import json
import time
from datetime import datetime
from typing import Optional
from PIL import Image
from sqlalchemy.orm import Session

from app.config import settings
from app.ai import get_ai_engine
from app.hardware import get_hardware_controller
from app.services.decision_engine import DecisionEngine
from app.models.inspection_record import InspectionRecord
from app.models.system_setting import SystemSetting
from app.schemas.inspection import InspectionResultSchema, DefectSchema
from app.core.websocket import ws_manager  # <--- Imported WebSocket Manager


class InspectionService:
    @staticmethod
    def generate_lot_id(db: Session) -> str:
        today_str = datetime.utcnow().strftime("%Y%m%d")
        prefix = f"LOT-{today_str}-"
        today_count = db.query(InspectionRecord).filter(
            InspectionRecord.lot_id.like(f"{prefix}%")
        ).count()
        return f"{prefix}{(today_count + 1):03d}"

    @classmethod
    async def process_inspection(
        cls,
        image_bytes: bytes,
        filename: str,
        fish_family: str,
        db: Session,
        custom_lot_id: Optional[str] = None
    ) -> InspectionResultSchema:
        start_time = time.time()

        # 1. Determine Lot ID
        lot_id = custom_lot_id if custom_lot_id else cls.generate_lot_id(db)

        # 2. Save image locally
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        timestamp_slug = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        saved_filename = f"{lot_id}_{timestamp_slug}.jpg"
        file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)
        pil_image.save(file_path, format="JPEG", quality=90)
        image_url = f"/uploads/{saved_filename}"

        # 3. AI Inference
        ai_engine = get_ai_engine()
        freshness_result = ai_engine.predict_freshness(pil_image)
        grade = freshness_result["grade"]
        grade_confidence = freshness_result["confidence"]

        # Fetch configured confidence threshold from settings
        setting = db.query(SystemSetting).filter(SystemSetting.key == "global_config").first()
        threshold = float(setting.confidence_threshold) if setting and setting.confidence_threshold is not None else 0.75

        raw_defects = ai_engine.predict_defects(pil_image)
        # Filter defects by confidence threshold
        defects_schemas = [
            DefectSchema(label=d["label"], bbox=d["bbox"], confidence=d["confidence"])
            for d in raw_defects
            if d.get("confidence", 1.0) >= threshold
        ]

        # 4. Decision Engine
        decision, hardware_signal, reason = DecisionEngine.evaluate(
            grade=grade,
            grade_confidence=grade_confidence,
            defects=[d.dict() for d in defects_schemas],
            confidence_threshold=threshold
        )

        # 5. Hardware Actuation
        hardware_controller = get_hardware_controller()
        hardware_controller.trigger_signal(hardware_signal)

        processing_time_ms = int((time.time() - start_time) * 1000)
        timestamp_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # 6. Persist to SQLite
        db_record = InspectionRecord(
            lot_id=lot_id,
            timestamp=datetime.utcnow(),
            fish_family=fish_family,
            grade=grade,
            grade_confidence=grade_confidence,
            defects_count=len(defects_schemas),
            defects_json=json.dumps([d.dict() for d in defects_schemas]),
            decision=decision,
            hardware_signal=hardware_signal,
            processing_time_ms=processing_time_ms,
            image_path=image_url,
            reason_summary=reason
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        result_payload = InspectionResultSchema(
            lot_id=lot_id,
            timestamp=timestamp_iso,
            fish_family=fish_family,
            grade=grade,
            grade_confidence=grade_confidence,
            defects=defects_schemas,
            decision=decision,
            hardware_signal=hardware_signal,
            processing_time_ms=processing_time_ms,
            image_url=image_url
        )


        # 7. Real-Time Broadcast via WebSocket
        try:
            await ws_manager.broadcast_json({
                "event": "NEW_INSPECTION",
                "data": result_payload.dict()
            })
        except Exception:
            pass

        return result_payload