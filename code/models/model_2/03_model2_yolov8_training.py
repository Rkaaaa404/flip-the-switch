#!/usr/bin/env python3
"""
NusaQC Model 2 - YOLOv8n Training & ONNX Export Pipeline
=========================================================
Script ini melatih model YOLOv8n (Surface Contamination & Defect Detector)
menggunakan 5 kelas standar NusaQC dan mengekspornya ke format ONNX INT8/Float32.

Penggunaan:
    python models/model_2/03_model2_yolov8_training.py --epochs 50 --batch 16
"""

import sys
import argparse
from pathlib import Path

# Force UTF-8 stdout encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_YAML = BASE_DIR / "models" / "datasets" / "model2_defect" / "dataset.yaml"
OUTPUT_DIR = BASE_DIR / "models" / "model_2" / "runs"


def train_yolov8_model(epochs=50, batch_size=16, img_size=640, device="auto"):
    """Melatih YOLOv8n dengan dataset NusaQC Model 2."""
    print("🚀 Memulai Pipeline Training YOLOv8n Model 2 NusaQC...")
    print(f"  • Config Dataset : {DATASET_YAML}")
    print(f"  • Epochs         : {epochs}")
    print(f"  • Batch Size     : {batch_size}")
    print(f"  • Image Size     : {img_size}")
    
    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n❌ Library 'ultralytics' belum terinstall!")
        print("💡 Silakan install dengan perintah: pip install ultralytics")
        return

    # 1. Load Pretrained YOLOv8n Weights
    model = YOLO("yolov8n.pt")
    
    # 2. Train Model
    results = model.train(
        data=str(DATASET_YAML),
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        project=str(OUTPUT_DIR),
        name="nusaqc_model2_defect_yolov8n",
        device=device,
        plots=True,
        save=True
    )
    
    print("\n✅ Training Selesai! Hasil disimpan di:", OUTPUT_DIR / "nusaqc_model2_defect_yolov8n")
    
    # 3. Export to ONNX Format
    print("\n📦 Mengekspor Model ke Format ONNX...")
    onnx_path = model.export(format="onnx", imgsz=img_size, dynamic=False)
    print(f"✅ Export ONNX Berhasil: {onnx_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NusaQC Model 2 YOLOv8 Training Script")
    parser.add_argument("--epochs", type=int, default=50, help="Jumlah epoch training (default: 50)")
    parser.add_argument("--batch", type=int, default=16, help="Batch size (default: 16)")
    parser.add_argument("--imgsz", type=int, default=640, help="Ukuran resolusi gambar (default: 640)")
    parser.add_argument("--device", type=str, default="cpu", help="Device: 'cpu', '0', atau 'auto'")
    
    args = parser.parse_args()
    
    train_yolov8_model(
        epochs=args.epochs,
        batch_size=args.batch,
        img_size=args.imgsz,
        device=args.device
    )
