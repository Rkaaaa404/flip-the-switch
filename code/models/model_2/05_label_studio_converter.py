import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image

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

def yolo_to_label_studio(dataset_dir: str, output_json: str, local_prefix: str = ""):
    """
    Konversi dataset YOLO (images & labels) menjadi file JSON import Label Studio
    dengan pre-filled predictions (bounding box hasil pseudo-labeling).
    """
    dataset_path = Path(dataset_dir)
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    # Cari citra secara rekursif (mendukung folder train/valid/test dan struktur rata)
    image_files = [f for f in dataset_path.rglob("*") if f.suffix.lower() in image_extensions]

    tasks = []
    print(f"📦 Ditemukan {len(image_files)} citra di {dataset_path}")

    for img_path in sorted(image_files):
        # Ambil dimensi gambar
        try:
            with Image.open(img_path) as img:
                img_width, img_height = img.size
        except Exception as e:
            print(f"⚠️ Gagal membaca gambar {img_path.name}: {e}")
            continue

        # Cari lokasi label_path yang mungkin
        label_candidates = [
            img_path.parent.parent / "labels" / f"{img_path.stem}.txt",
            img_path.parent / "labels" / f"{img_path.stem}.txt",
            img_path.parent / f"{img_path.stem}.txt",
            dataset_path / "labels" / f"{img_path.stem}.txt",
        ]
        label_path = None
        for cand in label_candidates:
            if cand.exists():
                label_path = cand
                break

        results = []

        if label_path and label_path.exists():
            with open(label_path, "r", encoding="utf-8") as lf:
                lines = lf.readlines()

            for idx, line in enumerate(lines):
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                
                cls_id = int(parts[0])
                if cls_id not in CLASS_MAP:
                    continue

                x_center = float(parts[1])
                y_center = float(parts[2])
                w = float(parts[3])
                h = float(parts[4])

                # Hitung persentase untuk Label Studio (0-100)
                x_pct = (x_center - w / 2.0) * 100.0
                y_pct = (y_center - h / 2.0) * 100.0
                w_pct = w * 100.0
                h_pct = h * 100.0

                label_name = CLASS_MAP[cls_id]

                results.append({
                    "original_width": img_width,
                    "original_height": img_height,
                    "image_rotation": 0,
                    "value": {
                        "x": max(0.0, min(100.0, x_pct)),
                        "y": max(0.0, min(100.0, y_pct)),
                        "width": max(0.0, min(100.0, w_pct)),
                        "height": max(0.0, min(100.0, h_pct)),
                        "rectanglelabels": [label_name]
                    },
                    "id": f"bbox_{idx}",
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels"
                })

        # URL / Path gambar di Label Studio
        if local_prefix:
            try:
                rel_path = img_path.relative_to(dataset_path).as_posix()
            except ValueError:
                rel_path = img_path.name
            img_url = f"{local_prefix.rstrip('/')}/{rel_path}"
        else:
            img_url = f"/data/local-files/?d={img_path.resolve().as_posix()}"

        task = {
            "data": {
                "image": img_url,
                "file_name": img_path.name
            },
            "predictions": [
                {
                    "model_version": "seed_model_v1_pseudo",
                    "result": results
                }
            ]
        }
        tasks.append(task)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

    print(f"✅ Berhasil mengonversi {len(tasks)} tugas ke {output_json}")

def label_studio_to_yolo(export_json: str, output_labels_dir: str):
    """
    Konversi hasil ekspor JSON Label Studio kembali menjadi file label YOLO (.txt).
    """
    out_dir = Path(output_labels_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(export_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    converted_count = 0
    bbox_count = 0

    for task in data:
        file_name = task.get("data", {}).get("file_name")
        if not file_name:
            # Ambil dari URL jika file_name tidak ada
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

                # Konversi persentase ke relatif (0-1)
                w = w_pct / 100.0
                h = h_pct / 100.0
                x_center = (x_pct / 100.0) + (w / 2.0)
                y_center = (y_pct / 100.0) + (h / 2.0)

                # Clamp 0-1
                x_center = max(0.0, min(1.0, x_center))
                y_center = max(0.0, min(1.0, y_center))
                w = max(0.0, min(1.0, w))
                h = max(0.0, min(1.0, h))

                yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
                bbox_count += 1

        with open(label_file, "w", encoding="utf-8") as lf:
            lf.writelines(yolo_lines)
        converted_count += 1

    print(f"✅ Ekspor selesai: {converted_count} file label diperbarui ({bbox_count} bounding box) di {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Label Studio <-> YOLO Annotation Converter for NusaQC Model 2")
    parser.add_argument("--export-to-ls", action="store_true", help="Konversi dataset YOLO -> Label Studio JSON Import")
    parser.add_argument("--import-from-ls", action="store_true", help="Konversi Label Studio JSON Export -> YOLO Labels (.txt)")
    parser.add_argument("--dataset-dir", type=str, default="models/model_2/runs_model2_workspace/nusaqc_extended_dataset", help="Direktori dataset YOLO")
    parser.add_argument("--output-json", type=str, default="models/model_2/label_studio_tasks.json", help="Path output JSON untuk Label Studio")
    parser.add_argument("--ls-export-json", type=str, default="models/model_2/project_export.json", help="Path JSON hasil ekspor Label Studio")
    parser.add_argument("--output-labels-dir", type=str, default="models/model_2/verified_labels", help="Direktori output file .txt YOLO terverifikasi")
    parser.add_argument("--local-prefix", type=str, default="", help="Prefix URL gambar jika menggunakan Local Storage Sync")

    args = parser.parse_args()

    if args.export_to_ls:
        yolo_to_label_studio(args.dataset_dir, args.output_json, args.local_prefix)
    elif args.import_from_ls:
        label_studio_to_yolo(args.ls_export_json, args.output_labels_dir)
    else:
        parser.print_help()
