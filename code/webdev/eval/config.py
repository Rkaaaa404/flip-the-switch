"""
NusaQC Evaluation Suite Configuration
Single Source of Truth for Evaluation Track & Product Track Metrics.
Aligned with Rulebook Babak Final AIC COMPFEST 18 & TEST_SUITE_PLANNING.md.
"""

import os
from pathlib import Path

# Paths Resolution
EVAL_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVAL_DIR.parent  # webdev/
PROJECT_ROOT = EVAL_DIR.parent.parent if EVAL_DIR.parent.name == "webdev" else EVAL_DIR.parent
BACKEND_DIR = REPO_ROOT / "backend"
MODEL_DIR = BACKEND_DIR / "models_weights"
UPLOAD_DIR = BACKEND_DIR / "uploads"
DATABASE_PATH = BACKEND_DIR / "nusaqc.db"
RESULTS_DIR = EVAL_DIR / "results"

# Real Model Weights Paths (strictly verified, no simulation fallback)
FRESHNESS_MODEL_PATH = MODEL_DIR / "mobilenetv3_freshness.onnx"
DEFECT_MODEL_PATH = MODEL_DIR / "nusaqc_model2_defect_detector.onnx"

# Real Dataset Paths (from project datasets repository)
DATASET_FRESHNESS_DIR = Path(r"d:\main\Documents\explore\compe\hackhathon\AIC\models\datasets\mobilenet")
if not DATASET_FRESHNESS_DIR.exists():
    DATASET_FRESHNESS_DIR = PROJECT_ROOT / "models" / "datasets" / "mobilenet"

DATASET_DEFECT_DIR = Path(r"d:\main\Documents\explore\compe\hackhathon\AIC\models\datasets\yolo8s")
if not DATASET_DEFECT_DIR.exists():
    DATASET_DEFECT_DIR = PROJECT_ROOT / "models" / "datasets" / "yolo8s"

DATASET_DEFECT_VALID_IMAGES = DATASET_DEFECT_DIR / "valid" / "images"
DATASET_DEFECT_VALID_LABELS = DATASET_DEFECT_DIR / "valid" / "labels"
# Ensure environment variables and application settings point to absolute paths
os.environ["MODEL_DIR"] = str(MODEL_DIR)
os.environ["UPLOAD_DIR"] = str(UPLOAD_DIR)
os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH}"

try:
    from app.config import settings
    settings.MODEL_DIR = str(MODEL_DIR)
    settings.UPLOAD_DIR = str(UPLOAD_DIR)
    settings.DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
except Exception:
    pass
# Strict validation: Fail fast with clear error if real files are missing
if not FRESHNESS_MODEL_PATH.exists():
    raise FileNotFoundError(f"CRITICAL: Real Freshness model missing at {FRESHNESS_MODEL_PATH}")
if not DEFECT_MODEL_PATH.exists():
    raise FileNotFoundError(f"CRITICAL: Real Defect model missing at {DEFECT_MODEL_PATH}")
if not DATASET_FRESHNESS_DIR.exists():
    raise FileNotFoundError(f"CRITICAL: Real Freshness dataset missing at {DATASET_FRESHNESS_DIR}")
if not DATASET_DEFECT_VALID_IMAGES.exists():
    raise FileNotFoundError(f"CRITICAL: Real Defect dataset images missing at {DATASET_DEFECT_VALID_IMAGES}")
if not DATASET_DEFECT_VALID_LABELS.exists():
    raise FileNotFoundError(f"CRITICAL: Real Defect dataset labels missing at {DATASET_DEFECT_VALID_LABELS}")

# Model Classes
FRESHNESS_CLASSES = ["A", "B", "C"]
DEFECT_CLASSES = ["sisik_sisa", "warna_abnormal", "luka_robekan", "lendir_berlebih"]
DEFECT_CLASS_NAMES_MAP = {0: "sisik_sisa", 1: "warna_abnormal", 2: "luka_robekan", 3: "lendir_berlebih"}
TARGET_FISH_FAMILIES = ["Scombridae", "Cichlidae", "Salmonidae"]

# Model Weight Filenames
FRESHNESS_MODEL_NAME = "mobilenetv3_freshness.onnx"
DEFECT_MODEL_NAME = "nusaqc_model2_defect_detector.onnx"
# Operational Inference Thresholds
DEFECT_CONF_THRESHOLD = 0.55
DEFECT_IOU_THRESHOLD = 0.45
MIN_BBOX_SIZE = 15
