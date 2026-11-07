# %% [markdown]
# # NusaQC Model 2: Automated Pseudo-Labeling Pipeline (Kaggle GPU)
# Inferensi Seed Model YOLOv8 pada dataset eksternal (HuggingFace panda992 Fish Disease + Alaa Mahmoud + Roboflow),
# generate pseudo-bounding box YOLO `.txt`, split train/valid, ekspor dataset siap training.
#
# **Kaggle Inputs yang dibutuhkan:**
# 1. Roboflow Fish Disease dataset → `/kaggle/input/roboflow-fish-disease/`
# 2. Output notebook 03 (seed model) → `/kaggle/input/notebooks/raykapranandita/model-2-nusaqc/`
# 3. (Opsional) Alaa Mahmoud Fish Disease → `/kaggle/input/datasets/alaamahmoud2010/fish-disease/`
# 4. HuggingFace panda992/fish_disease_datasets → otomatis di-download (public, no token needed)

# %% [markdown]
# # 1. Setup Environment

# %%
import os, sys, shutil, zipfile, random, yaml
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import ultralytics
except ImportError:
    os.system('pip install -q ultralytics')

import torch
from ultralytics import YOLO

print(f"PyTorch {torch.__version__} | CUDA: {torch.cuda.is_available()} "
      f"({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

# --- Paths ---
WORKING_DIR = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("./runs_model2_workspace")
EXTENDED_DATASET_DIR = WORKING_DIR / "nusaqc_extended_dataset"
WORKING_DIR.mkdir(parents=True, exist_ok=True)

# HuggingFace panda992/fish_disease_datasets is public, no token needed

# --- Seed Model Discovery ---
def find_seed_model():
    """Cari best.pt dari output notebook 03 atau lokasi lain."""
    candidates = [
        Path("/kaggle/input/notebooks/raykapranandita/model-2-nusaqc/best.pt"),
        WORKING_DIR / "best.pt",
    ]
    for pt in candidates:
        if pt.exists():
            print(f"  Found: {pt}")
            return pt
    # Fallback: search recursively
    for d in [Path("/kaggle/input"), WORKING_DIR]:
        if d.exists():
            for pt in sorted(d.rglob("best.pt"), key=lambda p: len(str(p))):
                print(f"  Found: {pt}")
                return pt
    print("  ⚠️ Seed model tidak ditemukan, akan pakai pretrained yolov8s.pt")
    return Path("yolov8s.pt")

print("🔍 Searching for seed model...")
SEED_MODEL = find_seed_model()
print(f"🎯 Seed Model: {SEED_MODEL}")

# %% [markdown]
# # 2. Pemetaan Kelas Eksternal -> 4 Kelas NusaQC
# 0: sisik_sisa, 1: warna_abnormal, 2: luka_robekan, 3: lendir_berlebih

# %%
NUSAQC_CLASSES = {0: "sisik_sisa", 1: "warna_abnormal", 2: "luka_robekan", 3: "lendir_berlebih"}
NUSAQC_CLASS_NAMES = list(NUSAQC_CLASSES.values())

# Mapping Roboflow raw class ID (7-kelas) -> NusaQC class ID (4-kelas)
RAW_TO_NUSAQC = {
    0: 1,   # BDA -> warna_abnormal
    1: 1,   # BGD -> warna_abnormal
    2: 1,   # BRD -> warna_abnormal
    3: 2,   # FDS -> luka_robekan
    4: -1,  # HF  -> skip (healthy)
    5: 0,   # PD  -> sisik_sisa
    6: 3    # WTD -> lendir_berlebih
}

# Mapping nama kelas HF/folder -> NusaQC class ID
# -1 = healthy (empty label), -99 = exclude (shrimp)
DISEASE_MAP = {
    "parasitic": 0, "parasite": 0, "argulus": 0, "anchor_worm": 0,
    "fish_parasitic": 0,
    "aeromoniasis": 1, "bda": 1, "bgd": 1, "brd": 1,
    "red_spot": 1, "discoloration": 1, "bacterial red": 1,
    "bacterial gill": 1, "fish_bacterial": 1,
    "saprolegniasis": 2, "fds": 2, "fungal": 2,
    "skin_ulcer": 2, "ulcer": 2, "tail_rot": 2, "fin_rot": 2,
    "fish_fungal": 2,
    "white_tail": 3, "wtd": 3, "excess_mucus": 3,
    "fish_viral": 3,
    "healthy": -1, "fresh": -1,
    "shrimp": -99, "udang": -99, "prawn": -99,
}

def map_class_name(name: str) -> int:
    """Map a disease/class name string to NusaQC class ID."""
    name_lower = name.lower().replace(" ", "_")
    for key, val in DISEASE_MAP.items():
        if key in name_lower:
            return val
    return -1  # default: healthy / unknown

# %% [markdown]
# # 3. Pseudo-Labeling: Inferensi Seed Model + BBox Generation

# %%
def _write_label(lbl_path, lines):
    with open(lbl_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def _predict_and_label(model, source, expected_cls, conf, out_lbl_path, stats, lock_class=True):
    """Run YOLO inference, write YOLO label file.
    - lock_class=True  : Paksa kelas BBox = expected_cls (untuk dataset GT spesifik seperti HF).
    - lock_class=False : Izinkan Seed Model menentukan kelas spesifik (untuk dataset biner seperti Alaa Infected).
    """
    results = model.predict(source=source, conf=conf, verbose=False)
    bboxes = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            if lock_class:
                target = expected_cls
            else:
                target = cls_id if cls_id in NUSAQC_CLASSES else expected_cls
            xc, yc, w, h = box.xywhn[0].tolist()
            bboxes.append(f"{target} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
            stats["bboxes"] += 1

    if not bboxes:
        # Fallback: bbox centered, ukuran 50%x50%
        bboxes.append(f"{expected_cls} 0.500000 0.500000 0.500000 0.500000\n")
        stats["bboxes"] += 1
        stats["fallbacks"] += 1

    _write_label(out_lbl_path, bboxes)


def _harmonize_roboflow_label(raw_lbl_path):
    """Harmonisasi satu file label Roboflow (7-kelas) ke NusaQC (4-kelas)."""
    lines = []
    with open(raw_lbl_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            try:
                raw_cls = int(parts[0])
                nq = RAW_TO_NUSAQC.get(raw_cls, -1)
                if nq == -1:
                    continue  # skip healthy / unknown
                xc, yc, w, h = map(float, parts[1:5])
                xc, yc = max(0, min(1, xc)), max(0, min(1, yc))
                w, h = max(0.001, min(1, w)), max(0.001, min(1, h))
                if w * h <= 1e-6:
                    continue
                lines.append(f"{nq} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
            except ValueError:
                continue
    return lines


def generate_pseudo_labels(seed_model_path, output_dir, conf_thresh=0.15):
    if not Path(seed_model_path).exists():
        print(f"❌ Seed Model tidak ditemukan: {seed_model_path}")
        return

    model = YOLO(str(seed_model_path))
    print(f"🤖 Seed Model dimuat: {seed_model_path}")

    out_img = output_dir / "all_images"
    out_lbl = output_dir / "all_labels"
    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    stats = {"imgs": 0, "bboxes": 0, "fallbacks": 0,
             "src_hf": 0, "src_alaa": 0, "src_rb": 0, "skipped_healthy": 0}

    # =================================================================
    # SOURCE 1: HuggingFace panda992/fish_disease_datasets (PUBLIC)
    # 2,450 gambar (train: 2,082 + test: 368)
    # Label int: 0=Bacterial Red, 1=Aeromoniasis, 2=Bacterial Gill,
    #            3=Fungal Saprolegniasis, 4=Healthy, 5=Parasitic, 6=Viral WTD
    # =================================================================
    HF_CLASS_TO_NUSAQC = {
        0: 1,   # Bacterial Red disease -> warna_abnormal
        1: 1,   # Aeromoniasis -> warna_abnormal
        2: 1,   # Bacterial gill disease -> warna_abnormal
        3: 2,   # Fungal Saprolegniasis -> luka_robekan
        4: -1,  # Healthy Fish -> skip
        5: 0,   # Parasitic diseases -> sisik_sisa
        6: 3,   # Viral White tail disease -> lendir_berlebih
    }
    try:
        from datasets import load_dataset
        print("\n🔄 Loading HuggingFace panda992/fish_disease_datasets (public)...")
        ds = load_dataset("panda992/fish_disease_datasets")

        for split in ds:
            print(f"  • Split '{split}': {len(ds[split])} samples")
            for item in ds[split]:
                pil_img = item["image"].convert("RGB")
                label_int = item["label"]  # integer 0-6
                nusaqc_cls = HF_CLASS_TO_NUSAQC.get(label_int, -1)

                fname = f"hf_{stats['imgs']:05d}.jpg"
                img_path = out_img / fname
                pil_img.save(img_path)

                if nusaqc_cls == -1:  # healthy -> empty label
                    _write_label(out_lbl / f"{img_path.stem}.txt", [])
                    stats["skipped_healthy"] += 1
                else:
                    _predict_and_label(model, pil_img, nusaqc_cls, conf_thresh,
                                       out_lbl / f"{img_path.stem}.txt", stats)
                stats["imgs"] += 1
                stats["src_hf"] += 1

        print(f"  ✓ HF selesai: {stats['src_hf']} citra")
    except Exception as e:
        import traceback
        print(f"  ⚠️ HF Error: {e}")
        traceback.print_exc()

    # =================================================================
    # SOURCE 2: Alaa Mahmoud Fish Disease Dataset (Kaggle Input)
    # =================================================================
    alaa_candidates = [
        Path("/kaggle/input/datasets/alaamahmoud2010/fish-disease/Fish Disease Dataset"),
        Path("/kaggle/input/fish-disease/Fish Disease Dataset"),
    ]
    alaa_dir = None
    for p in alaa_candidates:
        if p.exists():
            alaa_dir = p
            break

    if alaa_dir:
        print(f"\n🔄 Scanning Alaa Mahmoud: {alaa_dir}")
        for img_path in sorted(alaa_dir.rglob("*.jpg")) + sorted(alaa_dir.rglob("*.png")):
            path_lower = str(img_path).lower()
            if "shrimp" in path_lower:
                continue

            parent = img_path.parent.name.lower()
            if "fresh" in parent:
                nusaqc_cls = -1
            elif "infected" in parent:
                nusaqc_cls = 2  # fallback: luka_robekan, Seed Model decides actual class
            else:
                nusaqc_cls = map_class_name(parent)

            if nusaqc_cls == -99:
                continue

            fname = f"alaa_{stats['imgs']:05d}_{img_path.name}"
            dest = out_img / fname
            shutil.copy(img_path, dest)

            if nusaqc_cls == -1:
                _write_label(out_lbl / f"{dest.stem}.txt", [])
                stats["skipped_healthy"] += 1
            else:
                # Untuk Alaa Mahmoud (InfectedFish biner): Seed Model mendeteksi lokasi DAN menentukan kelas spesifiknya (lock_class=False)
                _predict_and_label(model, str(img_path), nusaqc_cls, conf_thresh,
                                   out_lbl / f"{dest.stem}.txt", stats, lock_class=False)
            stats["imgs"] += 1
            stats["src_alaa"] += 1

        print(f"  ✓ Alaa Mahmoud selesai: {stats['src_alaa']} citra")
    else:
        print("\n⚠️ Alaa Mahmoud dataset tidak ditemukan (opsional, skipped)")

    # =================================================================
    # SOURCE 3: Roboflow Fish Disease (HARMONISASI label 7->4 kelas!)
    # =================================================================
    roboflow_candidates = [
        Path("/kaggle/input/roboflow-fish-disease"),
        Path("/kaggle/input/datasets/raykapranandita/roboflow-fish-disease"),
    ]
    roboflow_dir = None
    for p in roboflow_candidates:
        if p.exists():
            roboflow_dir = p
            break

    if roboflow_dir:
        print(f"\n🔄 Harmonizing & copying Roboflow dataset: {roboflow_dir}")
        rb_remapped, rb_skipped = 0, 0
        for split in ["train", "valid", "test"]:
            img_dir = roboflow_dir / split / "images"
            lbl_dir = roboflow_dir / split / "labels"
            if not img_dir.exists():
                continue
            for img_path in img_dir.glob("*.*"):
                dest_img = out_img / f"rb_{split}_{img_path.name}"
                shutil.copy(img_path, dest_img)

                lbl_src = lbl_dir / f"{img_path.stem}.txt"
                if lbl_src.exists():
                    # HARMONISASI: convert 7-kelas -> 4-kelas NusaQC
                    harmonized_lines = _harmonize_roboflow_label(lbl_src)
                    _write_label(out_lbl / f"{dest_img.stem}.txt", harmonized_lines)
                    rb_remapped += len(harmonized_lines)
                    if not harmonized_lines:
                        rb_skipped += 1  # semua bbox di file ini = HF (healthy)
                else:
                    _write_label(out_lbl / f"{dest_img.stem}.txt", [])
                stats["imgs"] += 1
                stats["src_rb"] += 1
        print(f"  ✓ Roboflow selesai: {stats['src_rb']} citra, {rb_remapped} bbox harmonized, {rb_skipped} empty (healthy)")
    else:
        print("\n⚠️ Roboflow dataset tidak ditemukan!")

    print(f"\n{'='*50}")
    print(f"✅ Pseudo-Labeling Selesai!")
    print(f"  • Total citra     : {stats['imgs']}")
    print(f"  • BBox dihasilkan : {stats['bboxes']}")
    print(f"  • Fallback bbox   : {stats['fallbacks']}")
    print(f"  • Healthy (empty) : {stats['skipped_healthy']}")
    print(f"  • Sumber: HF={stats['src_hf']} | Alaa={stats['src_alaa']} | Roboflow={stats['src_rb']}")

generate_pseudo_labels(SEED_MODEL, EXTENDED_DATASET_DIR)

# %% [markdown]
# # 4. Split Train/Valid (80/20) & Generate data.yaml

# %%
def split_and_finalize(dataset_dir, valid_ratio=0.2, seed=42):
    """Split all_images/all_labels into train/ dan valid/, generate data.yaml."""
    all_img = dataset_dir / "all_images"
    all_lbl = dataset_dir / "all_labels"

    if not all_img.exists():
        print("❌ all_images/ tidak ditemukan")
        return None

    # Collect semua image files
    img_files = sorted(list(all_img.glob("*.jpg")) + list(all_img.glob("*.png")) + list(all_img.glob("*.jpeg")))
    print(f"\n📂 Total images collected: {len(img_files)}")

    # Shuffle & split
    random.seed(seed)
    random.shuffle(img_files)
    n_valid = max(1, int(len(img_files) * valid_ratio))
    valid_files = img_files[:n_valid]
    train_files = img_files[n_valid:]

    print(f"  Train: {len(train_files)} | Valid: {len(valid_files)}")

    # Create directories
    for split, files in [("train", train_files), ("valid", valid_files)]:
        dst_img = dataset_dir / split / "images"
        dst_lbl = dataset_dir / split / "labels"
        dst_img.mkdir(parents=True, exist_ok=True)
        dst_lbl.mkdir(parents=True, exist_ok=True)

        for img_path in files:
            shutil.copy(img_path, dst_img / img_path.name)
            lbl_path = all_lbl / f"{img_path.stem}.txt"
            if lbl_path.exists():
                shutil.copy(lbl_path, dst_lbl / f"{img_path.stem}.txt")
            else:
                # Empty label for background images
                with open(dst_lbl / f"{img_path.stem}.txt", 'w') as f:
                    pass

    # Cleanup staging dirs
    shutil.rmtree(all_img, ignore_errors=True)
    shutil.rmtree(all_lbl, ignore_errors=True)

    # Generate data.yaml
    yaml_path = WORKING_DIR / "data_extended.yaml"
    cfg = {
        'path': dataset_dir.resolve().as_posix(),
        'train': (dataset_dir / "train" / "images").resolve().as_posix(),
        'val': (dataset_dir / "valid" / "images").resolve().as_posix(),
        'nc': len(NUSAQC_CLASS_NAMES),
        'names': NUSAQC_CLASS_NAMES
    }
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(cfg, f, default_flow_style=False)
    print(f"\n✅ data.yaml -> {yaml_path.resolve()}")

    # Print label distribution
    print("\n📊 Distribusi label (train):")
    cls_counts = {i: 0 for i in range(len(NUSAQC_CLASS_NAMES))}
    empty_count = 0
    for lbl in (dataset_dir / "train" / "labels").glob("*.txt"):
        content = lbl.read_text().strip()
        if not content:
            empty_count += 1
            continue
        for line in content.split('\n'):
            parts = line.strip().split()
            if parts:
                cls_id = int(parts[0])
                if cls_id in cls_counts:
                    cls_counts[cls_id] += 1
    for cls_id, name in NUSAQC_CLASSES.items():
        print(f"  [{cls_id}] {name:20s}: {cls_counts[cls_id]}")
    print(f"  [—] background/empty    : {empty_count}")

    return yaml_path

DATA_YAML = split_and_finalize(EXTENDED_DATASET_DIR)

# %% [markdown]
# # 5. ZIP Output Dataset

# %%
def package_dataset(dataset_dir, output_zip):
    if not dataset_dir.exists():
        print("Dataset dir tidak ditemukan.")
        return
    print(f"\n📦 Compressing -> {output_zip}...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in dataset_dir.rglob('*'):
            if f.is_file():
                zf.write(f, f.relative_to(dataset_dir))
    size_mb = output_zip.stat().st_size / (1024 * 1024)
    print(f"✅ Archive: {output_zip.resolve()} ({size_mb:.1f} MB)")

package_dataset(EXTENDED_DATASET_DIR, WORKING_DIR / "nusaqc_extended_pseudo_dataset.zip")

# data.yaml sudah dibuat di WORKING_DIR / "data_extended.yaml"
if DATA_YAML and DATA_YAML.exists() and DATA_YAML.resolve() != (WORKING_DIR / "data_extended.yaml").resolve():
    shutil.copy(DATA_YAML, WORKING_DIR / "data_extended.yaml")

print("\n" + "="*50)
print("💡 NEXT STEPS:")
print("1. Download 'nusaqc_extended_pseudo_dataset.zip' untuk review di Label Studio.")
print("2. ATAU: Buat notebook baru, add output notebook ini sebagai input,")
print("   lalu jalankan 03_model2_kaggle_pipeline.py dengan:")
print("   DATASET_ROOT = Path('/kaggle/input/<notebook-slug>/nusaqc_extended_dataset')")
