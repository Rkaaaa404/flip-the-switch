"""Reset the Receiving QC Room demo to the same starting point every time.

Wipes delivery, inspection, lineage and Switch-room records, then runs five fish through the real
two-view capture pipeline with the real models:

    seq 1  clean dorsal + clean ventral
    seq 2  hf_00811 (open lesion) dorsal + clean ventral  -> flagged (warna_abnormal on current weights)
    seq 3  clean dorsal, ventral never arrives             -> PARTIAL_DORSAL_ONLY, flagged
    seq 4  clean dorsal + clean ventral
    seq 5  clean dorsal + clean ventral

It then marks inspection complete and maps the three demo chat accounts to plant roles.

    uv run python scripts/seed_demo.py --bridge <mattermost bridge id>

The bridge id is the Mattermost bridge in your Switch (Console > Messaging apps, or the
`sender` of any gate event: `@switch-mattermost-<bridge>-<username>:localhost`).
"""

import argparse
import asyncio
import os
import shutil
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.models  # noqa: E402,F401
from app.config import settings  # noqa: E402
from app.core.database import SessionLocal, init_db  # noqa: E402
from app.models.delivery_trace import (  # noqa: E402
    FishInspection, HumanDisposition, InspectionView, MaterialMovement, ReceivingDelivery, utcnow,
)
from app.models.switchroom import GateCommand, RecordProposal, SwitchIdentity  # noqa: E402
from app.schemas.delivery_trace import DeliveryCreate  # noqa: E402
from app.services import material_lineage_service as lineage  # noqa: E402
from app.services.two_view_inspection_service import handle_view_capture, reap_timed_out_captures  # noqa: E402

IMAGES = Path(__file__).resolve().parents[3] / "switch" / "demo" / "images"
FISH = [
    ("clean_02451_aug_0_1086.png", "clean_02506_aug_0_4100.png"),
    ("flagged_hf_00811.jpg", "clean_02535_aug_0_5576.png"),
    ("clean_02584_aug_0_8302.png", None),
    ("clean_02729_aug_0_818.png", "clean_02608_aug_0_9762.png"),
    ("clean_02477_aug_0_2294.png", "clean_02560_aug_0_6817.png"),
]
PEOPLE = [("qc.supervisor", "qc_supervisor"), ("floor.operator", "floor_operator"), ("auditor", "auditor")]


def participant_id(bridge: str, username: str) -> str:
    return f"@switch-mattermost-{bridge}-{username.replace('.', '-')}:localhost"


async def main(bridge: str) -> None:
    init_db()
    db = SessionLocal()
    for model in (GateCommand, RecordProposal, MaterialMovement, HumanDisposition, InspectionView,
                  FishInspection, ReceivingDelivery, SwitchIdentity):
        db.query(model).delete()
    db.commit()
    shutil.rmtree(os.path.join(settings.UPLOAD_DIR, "captures"), ignore_errors=True)

    start = utcnow() - timedelta(minutes=20)
    delivery = lineage.create_delivery(db, DeliveryCreate(
        supplier_name="PT Samudra Bitung (synthetic)", species="Tilapia", fish_family="Cichlidae",
        stated_quantity=500, quantity_unit="kg", truck_identifier="DB 8812 KT", created_by="floor.operator",
        received_at=start,
    ), now=start)

    t = start + timedelta(minutes=2)
    for dorsal, ventral in FISH:
        await handle_view_capture(db, delivery.id, "dorsal", (IMAGES / dorsal).read_bytes(), now=t)
        if ventral:
            await handle_view_capture(db, delivery.id, "ventral", (IMAGES / ventral).read_bytes(),
                                      now=t + timedelta(seconds=1.15))
        t += timedelta(seconds=6)
    reap_timed_out_captures(db, delivery.id, now=t + timedelta(seconds=10))
    lineage.transition_status(db, delivery.id, "inspection_complete")

    for username, role in PEOPLE:
        db.add(SwitchIdentity(participant_id=participant_id(bridge, username), username=username, role=role))
    db.commit()

    fish = db.query(FishInspection).filter_by(delivery_id=delivery.id).order_by(FishInspection.sequence_in_delivery).all()
    print(f"Seeded {delivery.id} (inspection_complete):")
    for f in fish:
        print(f"  seq {f.sequence_in_delivery}: {f.status:<20} flagged={f.flagged_for_review} {f.flag_reasons_json}")
    print("Linked identities:", ", ".join(f"{u} -> {r}" for u, r in PEOPLE))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--bridge", required=True, help="Mattermost bridge id in your Switch")
    asyncio.run(main(parser.parse_args().bridge))
