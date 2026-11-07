"""
Test Suite 1: Evaluasi Akurasi Inti & Matriks Kebingungan (test_core_accuracy.py)
Track: Eval Track (Bobot 20%)

Tujuan:
1. Menguji akurasi klasifikasi organoleptik MobileNetV3 (Grade A, B, C).
2. Menguji deteksi kecacatan permukaan YOLOv8s (sisik_sisa, warna_abnormal, luka_robekan, lendir_berlebih).
3. Mengukur metrik performa model saat ini pada dataset riil (Precision, Recall, F1, FNR, FAR, mAP@50).
"""

import sys
import os
import time
import json
import numpy as np
from PIL import Image
from pathlib import Path

# Setup paths and environment
CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(BACKEND_DIR))

from eval.config import (
    FRESHNESS_CLASSES, DEFECT_CLASSES, RESULTS_DIR
)
from eval.utils import (
    load_real_freshness_dataset,
    load_real_defect_dataset,
    compute_classification_metrics,
    evaluate_detections,
    print_header,
    print_metric_row,
    print_table,
    print_confusion_matrix_ascii,
    save_json_results
)
from app.ai.inference import AIInferenceEngine


def run_core_accuracy_evaluation(save_results: bool = True) -> dict:
    print_header(
        "TEST SUITE 1: EVALUASI AKURASI INTI & CONFUSION MATRIX",
        "Pengujian Model Freshness (MobileNetV3) & Defect Detector (YOLOv8s)"
    )

    # 1. Initialize Inference Engine
    print("[1/4] Menginisialisasi ONNX Runtime Inference Engine...")
    engine = AIInferenceEngine()
    models_status = engine.get_models_status()
    print(f"  * Freshness Model: {models_status['freshness_model']['status']}")
    print(f"  * Defect Model   : {models_status['defect_model']['status']}")

    # 2. Load Evaluation Dataset
    print("\n[2/4] Memuat Seluruh Dataset Uji Riil (DaFiF Freshness & YOLO Defect)...")
    freshness_samples = load_real_freshness_dataset(sample_limit=None)
    defect_samples = load_real_defect_dataset(sample_limit=None)
    print(f"  * Total Sampel Uji Freshness (DaFiF)   : {len(freshness_samples)} citra (Day 1..11, 3 Spesies)")
    print(f"  * Total Sampel Uji Defect (YOLO Valid) : {len(defect_samples)} citra beranotasi")

    # 3. Execution: Real Inference Dual-Model AI
    print("\n[3/4] Menjalankan Inferensi Dual-Model AI pada Data Riil...")

    # 3.1 Freshness Inference
    gt_freshness = []
    pred_freshness = []
    inference_times_freshness = []

    for s in freshness_samples:
        pil_img = Image.open(s["image_path"]).convert("RGB")
        t0 = time.perf_counter()
        f_res = engine.predict_freshness(pil_img)
        t_fresh = (time.perf_counter() - t0) * 1000
        inference_times_freshness.append(t_fresh)

        gt_freshness.append(s["ground_truth_grade"])
        pred_freshness.append(f_res["grade"])

    # 3.2 Defect Inference (calibrated threshold 0.55 + size filter > 15px)
    gt_defects = []
    pred_defects = []
    inference_times_defect = []

    for s in defect_samples:
        pil_img = Image.open(s["image_path"]).convert("RGB")
        gt_defects.append(s["ground_truth_defects"])

        t0_def = time.perf_counter()
        raw_preds = engine.predict_defects(pil_img, confidence_threshold=0.55)
        t_defect = (time.perf_counter() - t0_def) * 1000
        inference_times_defect.append(t_defect)

        filtered = [
            d for d in raw_preds
            if (d["bbox"][2] - d["bbox"][0]) >= 15 and (d["bbox"][3] - d["bbox"][1]) >= 15
        ]
        pred_defects.append(filtered)

    print("\n[4/4] Menghitung Metrik Kuantitatif & Matriks Kebingungan...")

    # Freshness Metrics
    freshness_metrics = compute_classification_metrics(
        y_true=gt_freshness,
        y_pred=pred_freshness,
        classes=FRESHNESS_CLASSES
    )

    # Defect Metrics
    defect_metrics = evaluate_detections(gt_defects, pred_defects)

    # 5. Display Reports
    print_header("HASIL EVALUASI MODEL 1: FRESHNESS CLASSIFIER (MobileNetV3)")
    print_metric_row("Overall Accuracy", f"{freshness_metrics['accuracy']}%")
    print_metric_row("Macro Precision", f"{freshness_metrics['macro_precision']}%")
    print_metric_row("Macro Recall", f"{freshness_metrics['macro_recall']}%")
    print_metric_row("Macro F1-Score", f"{freshness_metrics['macro_f1']}%")
    print_metric_row("Avg Freshness Latency (CPU)", f"{np.mean(inference_times_freshness):.2f}", "ms")

    print("\n  [Per-Class Freshness Performance]")
    fresh_table = [
        ["Class", "Precision (%)", "Recall (%)", "F1-Score (%)", "Support"]
    ]
    for c in FRESHNESS_CLASSES:
        m = freshness_metrics["per_class"][c]
        fresh_table.append([f"Grade {c}", f"{m['precision']:.1f}", f"{m['recall']:.1f}", f"{m['f1']:.1f}", str(m['support'])])
    print_table(fresh_table[0], fresh_table[1:])

    # Print 3x3 Confusion Matrix
    cm_arr = np.array(freshness_metrics["confusion_matrix"])
    print_confusion_matrix_ascii(cm_arr, FRESHNESS_CLASSES)

    # Misclassification Safety Check
    fatal_errors = cm_arr[2, 0]  # Grade C predicted as Grade A
    print(f"\n  Misklasifikasi Fatal (True Grade C -> Pred Grade A): {fatal_errors} kejadian")

    print_header("HASIL EVALUASI MODEL 2: DEFECT DETECTOR (YOLOv8s)")
    print_metric_row("Defect Precision", f"{defect_metrics['precision']}%")
    print_metric_row("Defect Recall", f"{defect_metrics['recall']}%")
    print_metric_row("False Negative Rate (FNR)", f"{defect_metrics['fnr']}%")
    print_metric_row("False Alarm Rate (FAR)", f"{defect_metrics['far']}%")
    print_metric_row("mAP@50 Defect", f"{defect_metrics['map50']}%")
    print_metric_row("Avg Defect Latency (CPU)", f"{np.mean(inference_times_defect):.2f}", "ms")

    # Current Performance Summary Table
    print_header("RINGKASAN METRIK AKURASI SAAT INI")
    comp_headers = ["Model / Komponen", "Metrik Evaluasi", "Skor Saat Ini", "Keterangan"]
    comp_rows = [
        [
            "MobileNetV3 Freshness",
            "Macro F1-Score",
            f"{freshness_metrics['macro_f1']}%",
            "Klasifikasi 3 kelas (Grade A, B, C)"
        ],
        [
            "MobileNetV3 Freshness",
            "Akurasi Total",
            f"{freshness_metrics['accuracy']}%",
            "Evaluasi pada dataset organoleptik DaFiF"
        ],
        [
            "YOLOv8s Defect Detector",
            "Defect Precision",
            f"{defect_metrics['precision']}%",
            "Ketepatan deteksi pada 4 kelas kecacatan"
        ],
        [
            "YOLOv8s Defect Detector",
            "Defect Recall",
            f"{defect_metrics['recall']}%",
            "Sensitivitas mendeteksi cacat fisik"
        ],
        [
            "YOLOv8s Defect Detector",
            "False Negative Rate (FNR)",
            f"{defect_metrics['fnr']}%",
            "Tingkat cacat yang tidak terdeteksi"
        ],
        [
            "YOLOv8s Defect Detector",
            "False Alarm Rate (FAR)",
            f"{defect_metrics['far']}%",
            "Tingkat deteksi semu pada area bebas cacat"
        ],
        [
            "YOLOv8s Defect Detector",
            "mAP@50",
            f"{defect_metrics['map50']}%",
            "Mean Average Precision ambang batas IoU 0.50"
        ]
    ]
    print_table(comp_headers, comp_rows)

    # 6. Build Final JSON Payload
    results_payload = {
        "suite_name": "test_core_accuracy",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_samples": len(freshness_samples) + len(defect_samples),
        "freshness_samples_count": len(freshness_samples),
        "defect_samples_count": len(defect_samples),
        "models_status": models_status,
        "freshness_evaluation": {
            "metrics": freshness_metrics,
            "average_latency_ms": round(float(np.mean(inference_times_freshness)), 2),
            "fatal_misclassifications_c_to_a": int(fatal_errors)
        },
        "defect_evaluation": {
            "metrics": defect_metrics,
            "average_latency_ms": round(float(np.mean(inference_times_defect)), 2)
        }
    }

    if save_results:
        save_json_results("core_accuracy_results.json", results_payload)

    return results_payload


if __name__ == "__main__":
    run_core_accuracy_evaluation()
