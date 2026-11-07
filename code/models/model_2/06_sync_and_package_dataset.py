import os
import sys
import json
import shutil
import zipfile
import yaml
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# NusaQC Model 2 Class Taxonomy
CLASS_MAP = {
    0: "sisik_sisa",
    1: "warna_abnormal",
    2: "luka_robekan",
    3: "lendir_berlebih"
}
NAME_TO_CLASS = {v: k for k, v in CLASS_MAP.items()}

def compute_iou(box1, box2):
    """
    Hitung Intersection over Union (IoU) antara dua bounding box format YOLO: [xc, yc, w, h] (0-1)
    """
    xc1, yc1, w1, h1 = box1
    xc2, yc2, w2, h2 = box2

    x1_min, x1_max = xc1 - w1 / 2.0, xc1 + w1 / 2.0
    y1_min, y1_max = yc1 - h1 / 2.0, yc1 + h1 / 2.0

    x2_min, x2_max = xc2 - w2 / 2.0, xc2 + w2 / 2.0
    y2_min, y2_max = yc2 - h2 / 2.0, yc2 + h2 / 2.0

    inter_xmin = max(x1_min, x2_min)
    inter_ymin = max(y1_min, y2_min)
    inter_xmax = min(x1_max, x2_max)
    inter_ymax = min(y1_max, y2_max)

    inter_w = max(0.0, inter_xmax - inter_xmin)
    inter_h = max(0.0, inter_ymax - inter_ymin)
    inter_area = inter_w * inter_h

    area1 = w1 * h1
    area2 = w2 * h2

    union_area = area1 + area2 - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area

def filter_overlapping_bboxes(lines, iou_threshold=0.85):
    """
    Filter dan hapus bounding box yang overlap parah (> iou_threshold / 85-90%) pada citra yang sama.
    """
    parsed_boxes = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        try:
            cls_id = int(parts[0])
            xc, yc, w, h = map(float, parts[1:5])
            parsed_boxes.append((cls_id, [xc, yc, w, h], line))
        except ValueError:
            continue

    if not parsed_boxes:
        return [], 0

    keep = []
    removed_count = 0
    
    # Sort berdasarkan area terbesar agar memprioritaskan box yang lebih informatif/mencakup area
    parsed_boxes.sort(key=lambda item: item[1][2] * item[1][3], reverse=True)

    for i, (cls1, box1, raw_line1) in enumerate(parsed_boxes):
        should_keep = True
        for (cls2, box2, _) in keep:
            iou = compute_iou(box1, box2)
            # Jika overlap > threshold (85-90%), anggap duplikat & hapus
            if iou >= iou_threshold:
                should_keep = False
                removed_count += 1
                break
        if should_keep:
            keep.append((cls1, box1, raw_line1))

    cleaned_lines = [item[2] for item in keep]
    return cleaned_lines, removed_count

def process_label_studio_export(ls_export_json, output_dir, iou_threshold=0.85):
    """
    Konversi ekspor JSON dari Label Studio ke file .txt YOLO + filter NMS/Overlap.
    """
    export_path = Path(ls_export_json)
    if not export_path.exists():
        print(f"⚠️ File ekspor Label Studio tidak ditemukan: {export_path}")
        return False

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(export_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    converted_count = 0
    total_raw_bboxes = 0
    total_removed_bboxes = 0

    for task in data:
        file_name = task.get("data", {}).get("file_name")
        if not file_name:
            img_url = task.get("data", {}).get("image", "")
            file_name = Path(img_url).name.split("?")[0]

        stem = Path(file_name).stem
        label_file = out_dir / f"{stem}.txt"

        annotations = task.get("annotations", [])
        if not annotations:
            annotations = task.get("predictions", [])

        yolo_lines = []

        for ann in annotations:
            results = ann.get("result", [])
            for res in results:
                if res.get("type") != "rectanglelabels":
                    continue

                val = res.get("value", {})
                labels = val.get("rectanglelabels", [])
                if not labels:
                    continue

                label_name = labels[0]
                if label_name not in NAME_TO_CLASS:
                    continue

                cls_id = NAME_TO_CLASS[label_name]

                x_pct = val.get("x", 0.0)
                y_pct = val.get("y", 0.0)
                w_pct = val.get("width", 0.0)
                h_pct = val.get("height", 0.0)

                w = max(0.001, min(1.0, w_pct / 100.0))
                h = max(0.001, min(1.0, h_pct / 100.0))
                x_center = max(0.0, min(1.0, (x_pct / 100.0) + (w / 2.0)))
                y_center = max(0.0, min(1.0, (y_pct / 100.0) + (h / 2.0)))

                yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
                total_raw_bboxes += 1

        # Apply Overlap Filter (IoU >= iou_threshold)
        clean_lines, removed_count = filter_overlapping_bboxes(yolo_lines, iou_threshold=iou_threshold)
        total_removed_bboxes += removed_count

        with open(label_file, "w", encoding="utf-8") as lf:
            lf.writelines(clean_lines)
        converted_count += 1

    print(f"✅ Ekspor Label Studio Berhasil Disinkronkan!")
    print(f"   • Total file diperbarui : {converted_count}")
    print(f"   • Total BBox Awal       : {total_raw_bboxes}")
    print(f"   • BBox Overlap Di-filter: {total_removed_bboxes} (IoU >= {iou_threshold*100:.0f}%)")
    print(f"   • BBox Bersih Akhir     : {total_raw_bboxes - total_removed_bboxes}")
    return True

def apply_nms_filter_on_dataset_dir(dataset_dir, iou_threshold=0.85):
    """
    Jalankan pembersihan NMS/Overlap pada seluruh folder labels dataset yang sudah ada.
    """
    d_path = Path(dataset_dir)
    total_removed = 0
    total_processed = 0

    for split in ["train", "valid", "test"]:
        lbl_dir = d_path / split / "labels"
        if not lbl_dir.exists():
            continue
        for lbl_file in lbl_dir.glob("*.txt"):
            lines = lbl_file.read_text(encoding="utf-8").splitlines(keepends=True)
            if not lines:
                continue
            clean_lines, removed = filter_overlapping_bboxes(lines, iou_threshold=iou_threshold)
            if removed > 0:
                lbl_file.write_text("".join(clean_lines), encoding="utf-8")
                total_removed += removed
            total_processed += 1

    print(f"🧹 Pembersihan Overlap Dataset Selesai:")
    print(f"   • Processed {total_processed} label files.")
    print(f"   • Removed {total_removed} overlapping bboxes (IoU >= {iou_threshold*100:.0f}%).")

def package_final_dataset(dataset_dir, output_zip_path):
    """
    ZIP dataset final terverifikasi dan siap di-upload ke Kaggle.
    """
    d_path = Path(dataset_dir)
    out_zip = Path(output_zip_path)
    out_zip.parent.mkdir(parents=True, exist_ok=True)

    print(f"📦 Mengompres dataset final ke: {out_zip}")
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in d_path.rglob('*'):
            if f.is_file():
                zf.write(f, f.relative_to(d_path))

    size_mb = out_zip.stat().st_size / (1024 * 1024)
    print(f"✅ Dataset Siap Upload Kaggle: {out_zip.resolve()} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    LS_EXPORT_JSON = BASE_DIR / "project_export.json"
    VERIFIED_LABELS_DIR = BASE_DIR / "verified_labels"
    DATASET_DIR = BASE_DIR.parent / "datasets" / "model-2" / "nusaqc_extended_pseudo_dataset"
    FINAL_ZIP = BASE_DIR / "nusaqc_verified_final_dataset.zip"

    print("🚀 === OTOMASI SINKRONISASI DATASET & FILTER OVERLAP === 🚀\n")

    # 1. Jika ada file ekspor Label Studio, proses dulu
    if LS_EXPORT_JSON.exists():
        print(f"1️⃣ Memproses ekspor Label Studio ({LS_EXPORT_JSON.name})...")
        process_label_studio_export(LS_EXPORT_JSON, VERIFIED_LABELS_DIR, iou_threshold=0.85)
        
        # Copy verified labels to dataset dir
        print("2️⃣ Memperbarui file label di dataset...")
        for split in ["train", "valid"]:
            lbl_dir = DATASET_DIR / split / "labels"
            if lbl_dir.exists():
                for v_file in VERIFIED_LABELS_DIR.glob("*.txt"):
                    target_file = lbl_dir / v_file.name
                    if target_file.exists():
                        shutil.copy(v_file, target_file)
    else:
        print("ℹ️ File project_export.json dari Label Studio belum ada/ditemukan.")
        print("1️⃣ Menjalankan Filter NMS / Overlap (>85% IoU) langsung pada dataset saat ini...")

    # 2. Filter overlap pada seluruh dataset dir
    apply_nms_filter_on_dataset_dir(DATASET_DIR, iou_threshold=0.85)

    # 3. Re-package ZIP untuk Kaggle
    package_final_dataset(DATASET_DIR, FINAL_ZIP)

    print("\n✨ SELESAI! Langkah berikutnya:")
    print("1. File 'nusaqc_verified_final_dataset.zip' sudah dibuat di folder models/model_2/.")
    print("2. Upload ZIP tersebut sebagai Kaggle Dataset (misal: 'nusaqc-verified-dataset').")
    print("3. Jalankan notebook '03_model2_kaggle_pipeline.ipynb' di Kaggle GPU.")
