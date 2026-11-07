#!/usr/bin/env python3
"""
NusaQC Model 2 - Dataset Preparation & Label Harmonization Script
===================================================================
Script ini berfungsi untuk:
1. Menyiapkan struktur folder dataset Model 2 (raw & processed).
2. Memetakan label heterogen (Roboflow, BD Fish, Kaggle Bite Marks) ke 5 Kelas Standar NusaQC.
3. Melakukan split dataset (70% Train / 15% Val / 15% Test).
4. Menghasilkan statistik rekapitulasi data.

Penggunaan:
    python models/model_2/01_prepare_model2_dataset.py --setup-dirs
    python models/model_2/01_prepare_model2_dataset.py --verify-split
"""

import os
import sys
import shutil
import json
import glob
import argparse
from pathlib import Path

# Force stdout UTF-8 encoding for Windows console compatibility
sys.stdout.reconfigure(encoding='utf-8')

# Path Konfigurasi Utama
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_DIR = BASE_DIR / "models" / "datasets" / "model2_defect"
RAW_DIR = DATASET_DIR / "raw"
PROCESSED_DIR = DATASET_DIR / "processed"

# 5 Kelas Standar NusaQC
NUSAQC_CLASSES = {
    0: "sisik_sisa",
    1: "warna_abnormal",
    2: "luka_robekan",  # Termasuk Winter Ulcer Disease (lesi ulseratif parah/daging cekung-kroak), luka robek mekanis, & skin ulcer
    3: "foreign_object",
    4: "lendir_berlebih"
}

# Mapping Label Sumber External ke Class ID NusaQC
ROBOFLOW_LABEL_MAP = {
    # Class 0: sisik_sisa
    "scale_loss": 0, "missing_scales": 0, "descaling": 0, "parasite": 0,
    
    # Class 1: warna_abnormal
    "brd": 1, "bacterial_red_disease": 1, "red_spot": 1, "bda": 1, 
    "aeromoniasis": 1, "bgd": 1, "bacterial_gill_disease": 1, "black_gill": 1, "discoloration": 1,
    
    # Class 2: luka_robekan (Ulcer, Winter Ulcer Disease, & luka robek mekanis)
    "skin_ulcer": 2, "ulcer": 2, "winter_ulcer": 2, "winter_ulcer_disease": 2, "saprolegniasis_wound": 2, "tearing": 2, "cut": 2, 
    "bite_mark": 2, "bites": 2, "damaged_flesh": 2, "kroak": 2, "gouged": 2,
    
    # Class 3: foreign_object
    "debris": 3, "plastic": 3, "foreign_matter": 3,
    
    # Class 4: lendir_berlebih
    "excess_mucus": 4, "white_mucus": 4, "gill_mucus": 4
}


def setup_directory_structure():
    """Membuat hirarki folder yang dibutuhkan untuk Model 2."""
    print("📁 Menyiapkan hirarki folder dataset Model 2...")
    
    folders = [
        RAW_DIR / "roboflow",
        RAW_DIR / "bd_fish",
        RAW_DIR / "salmonscan",
        RAW_DIR / "alaa_mahmoud",
        RAW_DIR / "kaggle_bites",
        RAW_DIR / "label_studio_export",
        PROCESSED_DIR / "train" / "images",
        PROCESSED_DIR / "train" / "labels",
        PROCESSED_DIR / "val" / "images",
        PROCESSED_DIR / "val" / "labels",
        PROCESSED_DIR / "test" / "images",
        PROCESSED_DIR / "test" / "labels",
    ]
    
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {folder.relative_to(BASE_DIR)}")
        
    print("\n✅ Struktur folder berhasil dibuat!")


def verify_dataset_integrity():
    """Memeriksa jumlah file gambar & label dalam train/val/test split."""
    print("\n🔍 Memeriksa Integritas & Statistik Dataset Model 2...")
    
    splits = ["train", "val", "test"]
    stats = {}
    
    for split in splits:
        img_dir = PROCESSED_DIR / split / "images"
        lbl_dir = PROCESSED_DIR / split / "labels"
        
        images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
        labels = list(lbl_dir.glob("*.txt"))
        
        stats[split] = {
            "images": len(images),
            "labels": len(labels)
        }
        
        print(f"  • Split [{split.upper()}]: {len(images)} gambar, {len(labels)} label annotation file")
        
    total_imgs = sum(s["images"] for s in stats.values())
    total_lbls = sum(s["labels"] for s in stats.values())
    print(f"\n📊 Total Dataset: {total_imgs} gambar, {total_lbls} file label.")
    
    if total_imgs == 0:
        print("💡 Catatan: Folder dataset processed masih kosong. Silakan jalankan ekspor dari Label Studio!")
    return stats


def parse_label_studio_yolo_export(export_dir):
    """
    Mengonversi hasil ekspor YOLO dari Label Studio ke struktur processed NusaQC.
    """
    export_path = Path(export_dir)
    if not export_path.exists():
        print(f"❌ Folder ekspor tidak ditemukan: {export_path}")
        return

    images = list(export_path.glob("*.jpg")) + list(export_path.glob("*.png"))
    print(f"🔄 Memproses {len(images)} gambar hasil ekspor Label Studio...")

    # Logik pembagian 70% Train, 15% Val, 15% Test
    import random
    random.seed(42)
    random.shuffle(images)
    
    n_train = int(0.7 * len(images))
    n_val = int(0.15 * len(images))
    
    train_imgs = images[:n_train]
    val_imgs = images[n_train:n_train + n_val]
    test_imgs = images[n_train + n_val:]
    
    def copy_files(img_list, split_name):
        for img_p in img_list:
            lbl_p = img_p.with_suffix(".txt")
            
            dest_img = PROCESSED_DIR / split_name / "images" / img_p.name
            dest_lbl = PROCESSED_DIR / split_name / "labels" / lbl_p.name
            
            shutil.copy(img_p, dest_img)
            if lbl_p.exists():
                shutil.copy(lbl_p, dest_lbl)
                
    copy_files(train_imgs, "train")
    copy_files(val_imgs, "val")
    copy_files(test_imgs, "test")
    
    print(f"✅ Berhasil membagi dataset: {len(train_imgs)} Train, {len(val_imgs)} Val, {len(test_imgs)} Test")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NusaQC Model 2 Dataset Preparation Utility")
    parser.add_argument("--setup-dirs", action="store_true", help="Buat struktur folder dataset raw dan processed")
    parser.add_argument("--verify-split", action="store_true", help="Periksa statistik dataset split")
    parser.add_argument("--process-export", type=str, help="Path folder ekspor Label Studio untuk diproses")
    
    args = parser.parse_args()
    
    if args.setup_dirs:
        setup_directory_structure()
    elif args.verify_split:
        verify_dataset_integrity()
    elif args.process_export:
        parse_label_studio_yolo_export(args.process_export)
    else:
        # Default: Setup dirs & verify
        setup_directory_structure()
        verify_dataset_integrity()
