# %% [markdown]
# # NusaQC Model 2: Fish Defect Detector (YOLOv8s Training Pipeline)
# Notebook ini melatih model YOLOv8s untuk deteksi 4 kelas cacat permukaan ikan NusaQC.
# Termasuk **Exploratory Data Analysis (EDA)** komprehensif, **Filtering Overlapping Bounding Boxes (NMS Clean-up)**, **Tuned Training**, **Evaluasi**, dan **Ekspor ONNX**.

# %% [markdown]
# # 1. Setup Environment & Configuration

# %%
import os, sys, shutil, yaml
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import ultralytics
except ImportError:
    os.system('pip install -q ultralytics')

import torch
torch_version = torch.__version__
has_cuda = torch.cuda.is_available()
gpu_name = torch.cuda.get_device_name(0) if has_cuda else 'CPU'
print(f"PyTorch {torch_version} | CUDA: {has_cuda} ({gpu_name})")

# --- Discovery Dataset Input ---
def find_dataset_root():
    candidates = [
        Path("/kaggle/input/nusaqc-verified-dataset"),
        Path("/kaggle/input/nusaqc-extended-pseudo-dataset"),
        Path("/kaggle/input/datasets/raykapranandita/nusaqc-extended-pseudo-dataset"),
        Path("/kaggle/input/roboflow-fish-disease"),
        Path("models/datasets/model-2/nusaqc_extended_pseudo_dataset"),
        Path("models/datasets/model-2/roboflow-fish-disease")
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fallback search
    for d in [Path("/kaggle/input"), Path("models/datasets")]:
        if d.exists():
            for p in d.rglob("train"):
                if p.is_dir():
                    return p.parent
    return Path("./dataset")

DATASET_ROOT = find_dataset_root()
WORKING_DIR = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("./runs_model2_workspace")
CLEAN_DATASET_DIR = WORKING_DIR / "nusaqc_clean_dataset"

WORKING_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DATASET_DIR.mkdir(parents=True, exist_ok=True)

print(f"🎯 Dataset Root Identified: {DATASET_ROOT.resolve()}")
print(f"📂 Working Directory      : {WORKING_DIR.resolve()}")

for split in ['train', 'valid', 'test']:
    imgs = len(list((DATASET_ROOT / split / 'images').glob('*.*'))) if (DATASET_ROOT / split / 'images').exists() else 0
    lbls = len(list((DATASET_ROOT / split / 'labels').glob('*.txt'))) if (DATASET_ROOT / split / 'labels').exists() else 0
    print(f"  [{split:<5}] Images: {imgs:<5} | Labels: {lbls:<5}")

# %% [markdown]
# # 2. Overlapping Bounding Box Clean-up (NMS Filter Rule > 85% IoU)

# %%
def compute_iou(box1, box2):
    """Hitung IoU antara dua box YOLO format [xc, yc, w, h]."""
    xc1, yc1, w1, h1 = box1
    xc2, yc2, w2, h2 = box2

    x1_min, x1_max = xc1 - w1 / 2.0, xc1 + w1 / 2.0
    y1_min, y1_max = yc1 - h1 / 2.0, yc1 + h1 / 2.0

    x2_min, x2_max = xc2 - w2 / 2.0, xc2 + w2 / 2.0
    y2_min, y2_max = yc2 - h2 / 2.0, yc2 + h2 / 2.0

    inter_w = max(0.0, min(x1_max, x2_max) - max(x1_min, x2_min))
    inter_h = max(0.0, min(y1_max, y2_max) - max(y1_min, y2_min))
    inter_area = inter_w * inter_h

    union_area = (w1 * h1) + (w2 * h2) - inter_area
    return inter_area / union_area if union_area > 0 else 0.0

def filter_overlapping_bboxes(lines, iou_thresh=0.85):
    boxes = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 5:
            try:
                cid = int(parts[0])
                xc, yc, w, h = map(float, parts[1:5])
                boxes.append((cid, [xc, yc, w, h], line))
            except ValueError:
                continue
    if not boxes:
        return [], 0
    
    boxes.sort(key=lambda item: item[1][2] * item[1][3], reverse=True)
    keep = []
    removed = 0
    for cid1, b1, line1 in boxes:
        overlap = False
        for cid2, b2, _ in keep:
            if compute_iou(b1, b2) >= iou_thresh:
                overlap = True
                removed += 1
                break
        if not overlap:
            keep.append((cid1, b1, line1))
    return [k[2] for k in keep], removed

# %% [markdown]
# # 3. EDA: Exploratory Data Analysis & Visualisasi Dataset

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2

NUSAQC_CLASSES = {0: "sisik_sisa", 1: "warna_abnormal", 2: "luka_robekan", 3: "lendir_berlebih"}
NUSAQC_CLASS_NAMES = list(NUSAQC_CLASSES.values())
COLOR_MAP = [(255, 153, 0), (255, 0, 0), (255, 204, 0), (153, 0, 255)] # Oranye, Merah, Kuning, Ungu

def run_dataset_eda(src_root):
    records = []
    image_bbox_counts = []
    
    for split in ['train', 'valid', 'test']:
        lbl_dir = src_root / split / "labels"
        if not lbl_dir.exists():
            continue
        for lbl_file in lbl_dir.glob("*.txt"):
            lines = lbl_file.read_text(encoding='utf-8').splitlines()
            cnt = len([l for l in lines if len(l.strip().split()) >= 5])
            image_bbox_counts.append({'split': split, 'file': lbl_file.name, 'count': cnt})
            
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    try:
                        cls_id = int(parts[0])
                        xc, yc, w, h = map(float, parts[1:5])
                        records.append({
                            'split': split,
                            'class_id': cls_id,
                            'class_name': NUSAQC_CLASSES.get(cls_id, f"C{cls_id}"),
                            'xc': xc, 'yc': yc, 'w': w, 'h': h,
                            'area': w * h, 'aspect_ratio': w / (h + 1e-6)
                        })
                    except ValueError:
                        continue
    df = pd.DataFrame(records)
    df_counts = pd.DataFrame(image_bbox_counts)
    print(f"📊 EDA Stats: Total BBoxes = {len(df)} | Total Images Analyzed = {len(df_counts)}")
    return df, df_counts

def plot_eda_charts(df, df_counts):
    if df.empty:
        print("⚠️ Dataframe EDA kosong.")
        return
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Distribusi Kelas
    sns.countplot(data=df, x='class_name', hue='split', ax=axes[0,0], palette='Set2', order=NUSAQC_CLASS_NAMES)
    axes[0,0].set_title("1. Frekuensi Bounding Box per Kelas NusaQC", fontsize=12, fontweight='bold')
    axes[0,0].tick_params(axis='x', rotation=15)
    for p in axes[0,0].patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            axes[0,0].annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='bottom', fontsize=8, xytext=(0, 2), textcoords='offset points')

    # 2. Distribusi Area Box
    sns.boxplot(data=df, x='class_name', y='area', hue='class_name', ax=axes[0,1], palette='flare', order=NUSAQC_CLASS_NAMES, legend=False)
    axes[0,1].set_title("2. Distribusi Ukuran Area BBox (Normalized 0-1)", fontsize=12, fontweight='bold')
    axes[0,1].tick_params(axis='x', rotation=15)

    # 3. Jumlah BBox per Gambar (Histogram)
    sns.histplot(data=df_counts, x='count', discrete=True, hue='split', multiple='stack', ax=axes[1,0], palette='crest')
    axes[1,0].set_title("3. Distribusi Jumlah BBox per Citra (Termasuk Background/0)", fontsize=12, fontweight='bold')
    axes[1,0].set_xlabel("Jumlah Bounding Box pada 1 Gambar")

    # 4. Total BBox per Kelas Summary
    counts = df['class_name'].value_counts().reindex(NUSAQC_CLASS_NAMES).fillna(0)
    bars = axes[1,1].bar(counts.index, counts.values, color=['#FF9900', '#FF0000', '#FFCC00', '#9900FF'])
    axes[1,1].set_title("4. Total BBox per Kelas NusaQC (Keseluruhan)", fontsize=12, fontweight='bold')
    axes[1,1].tick_params(axis='x', rotation=15)
    for b in bars:
        axes[1,1].text(b.get_x() + b.get_width()/2., b.get_height() + max(counts.values)*0.01,
                        f"{int(b.get_height())}", ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.show()

def visualize_sample_grid(src_root, n=6):
    img_dir = src_root / "train" / "images"
    lbl_dir = src_root / "train" / "labels"
    if not img_dir.exists():
        return
    img_files = list(img_dir.glob("*.*"))[:n]
    if not img_files:
        return
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    for ax, ip in zip(axes, img_files):
        img = cv2.imread(str(ip))
        if img is None:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ih, iw = img.shape[:2]
        lp = lbl_dir / f"{ip.stem}.txt"
        if lp.exists():
            for line in open(lp):
                p = line.strip().split()
                if len(p) >= 5:
                    cid = int(p[0]); xc, yc, bw, bh = map(float, p[1:5])
                    x1, y1 = int((xc - bw/2) * iw), int((yc - bh/2) * ih)
                    x2, y2 = int((xc + bw/2) * iw), int((yc + bh/2) * ih)
                    c_rgb = COLOR_MAP[cid] if cid < len(COLOR_MAP) else (0, 255, 0)
                    cv2.rectangle(img, (x1, y1), (x2, y2), c_rgb, 2)
                    c_name = NUSAQC_CLASSES.get(cid, str(cid))
                    cv2.putText(img, c_name, (x1, max(y1-5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, c_rgb, 2)
        ax.imshow(img)
        ax.set_title(ip.name[:20], fontsize=9)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

df_eda, df_counts = run_dataset_eda(DATASET_ROOT)
plot_eda_charts(df_eda, df_counts)
visualize_sample_grid(DATASET_ROOT)

# %% [markdown]
# # 4. Preparation & Copy Dataset (NMS Filter Auto-Applied)

# %%
def prepare_clean_dataset(src_root, dst_root):
    total_remapped = 0
    total_overlap_removed = 0
    
    for split in ['train', 'valid', 'test']:
        src_img = src_root / split / "images"
        src_lbl = src_root / split / "labels"
        dst_img = dst_root / split / "images"
        dst_lbl = dst_root / split / "labels"
        dst_img.mkdir(parents=True, exist_ok=True)
        dst_lbl.mkdir(parents=True, exist_ok=True)
        
        if not src_img.exists():
            continue
        for img_path in src_img.glob("*.*"):
            shutil.copy(img_path, dst_img / img_path.name)
            lbl_path = src_lbl / f"{img_path.stem}.txt"
            lines = []
            if lbl_path.exists():
                raw_lines = lbl_path.read_text(encoding='utf-8').splitlines(keepends=True)
                clean_lines, removed = filter_overlapping_bboxes(raw_lines, iou_thresh=0.85)
                total_overlap_removed += removed
                lines = clean_lines
                total_remapped += len(clean_lines)
            
            with open(dst_lbl / f"{img_path.stem}.txt", 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
    print(f"✅ Harmonisasi & Clean-up Selesai:")
    print(f"   • Total BBox Aktif         : {total_remapped}")
    print(f"   • Overlapping BBox Cleaned : {total_overlap_removed} (IoU >= 85%)")

def create_data_yaml(dst_root, output_dir):
    yaml_path = output_dir / "data.yaml"
    cfg = {
        'path': dst_root.resolve().as_posix(),
        'train': (dst_root / "train" / "images").resolve().as_posix(),
        'val': (dst_root / "valid" / "images").resolve().as_posix(),
        'nc': len(NUSAQC_CLASS_NAMES),
        'names': NUSAQC_CLASS_NAMES
    }
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(cfg, f, default_flow_style=False)
    print(f"✅ data.yaml -> {yaml_path.resolve()}")
    return yaml_path

prepare_clean_dataset(DATASET_ROOT, CLEAN_DATASET_DIR)
DATA_YAML = create_data_yaml(CLEAN_DATASET_DIR, WORKING_DIR)

# %% [markdown]
# # 5. Training YOLOv8s Final Model (Improved v2)
# Improvement dari baseline (mAP@50=0.72, Recall=0.68):
# - 200 epochs + cosine LR (model belum converge di 100 epoch)
# - imgsz 800 (deteksi defek kecil: sisik_sisa, lendir_berlebih)
# - cls_pw=1.0 inverse-frequency class weighting (warna_abnormal 3.25x sisik_sisa)
# - Augmentasi agresif (erasing, perspective, shear)
# - Loss weights rebalanced (cls 1.5→2.5, box 7.5→8.5, dfl 1.5→2.0)
# Deploy target: Raspberry Pi, <500ms latency, snapshot-based inspection

# %%
from ultralytics import YOLO

# --- Baseline HPARAMS (untuk referensi, JANGAN diubah) ---
BASELINE_METRICS = {
    'precision': 0.770, 'recall': 0.683,
    'mAP50': 0.721, 'mAP50-95': 0.477,
    'per_class_mAP50': {
        'sisik_sisa': 0.676, 'warna_abnormal': 0.836,
        'luka_robekan': 0.642, 'lendir_berlebih': 0.730
    }
}

HPARAMS = {
    # --- Core Training ---
    'epochs': 200,              # Konvergensi penuh dengan cosine LR
    'batch': 16,                # optimal untuk Kaggle T4 16GB VRAM
    'imgsz': 800,               # 800px: resolusi tinggi untuk mendeteksi defek mikro sisik & robekan
    'cos_lr': True,             # Cosine learning rate decay

    # --- Optimizer ---
    'optimizer': 'AdamW',
    'lr0': 0.001,
    'lrf': 0.01,
    'momentum': 0.937,
    'weight_decay': 0.0005,
    'warmup_epochs': 3.0,

    # --- Augmentation (Preservasi Tekstur Sisik Halus & Small Defects) ---
    'mosaic': 0.85,             # 1.0 -> 0.85: beri porsi citra tunggal utuh
    'close_mosaic': 25,         # matikan mosaic 25 epoch terakhir agar model adaptasi ke citra asli
    'mixup': 0.08,              # kurangi mixup agar tekstur sisik halus tidak blur
    'copy_paste': 0.25,         # paste defek proporsional untuk menyeimbangkan kelas minoritas
    'erasing': 0.10,            # kurangi occlusion berlebih pada defek mikro
    'hsv_h': 0.015,
    'hsv_s': 0.7,
    'hsv_v': 0.4,
    'scale': 0.30,              # 0.60 -> 0.30: cegah defek sisik menyusut hingga hilang
    'fliplr': 0.5,
    'flipud': 0.1,
    'translate': 0.10,
    'degrees': 10.0,
    'perspective': 0.0002,
    'shear': 2.0,

    # --- Loss Weights (Rebalanced) ---
    'box': 7.5,                 # bobot lokalisasi presisi tinggi
    'cls': 1.8,                 # perkuat klasifikasi fitur defek
    'dfl': 1.8,                 # focal loss presisi batas bounding box

    # --- Early Stopping ---
    'patience': 50,
}

print("⚙️ Hyperparameters Improved Training v2:")
print("─" * 50)
for k, v in HPARAMS.items():
    print(f"  {k:<20}: {v}")
print("─" * 50)
print(f"\n📋 Baseline Metrics (target improvement):")
print(f"   mAP@50={BASELINE_METRICS['mAP50']:.3f} → target ≥0.80")
print(f"   Recall={BASELINE_METRICS['recall']:.3f} → target ≥0.75")

model = YOLO("yolov8s.pt")
RUN_DIR = WORKING_DIR / "runs_model2" / "nusaqc_yolov8s_v2"

print("\n🚀 Starting YOLOv8s Improved Training v2...")
train_results = model.train(
    data=str(DATA_YAML),
    project=str(WORKING_DIR / "runs_model2"),
    name="nusaqc_yolov8s_v2",
    save=True, plots=True, exist_ok=True,
    **HPARAMS
)

# %% [markdown]
# # 6a. Visualisasi Training Curves

# %%
def plot_results(run_dir):
    csv = run_dir / "results.csv"
    if not csv.exists():
        print(f"results.csv tidak ditemukan di {run_dir}")
        return
    df = pd.read_csv(csv)
    df.columns = df.columns.str.strip()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("NusaQC Model 2 — Training Curves (Improved v2)", fontsize=14, fontweight='bold')
    if 'train/box_loss' in df.columns:
        for col, lbl in [('train/box_loss','Box'),('train/cls_loss','Cls'),('train/dfl_loss','DFL')]:
            axes[0,0].plot(df['epoch'], df[col], label=lbl)
        axes[0,0].set_title("Train Loss"); axes[0,0].legend(); axes[0,0].grid(True, ls='--', alpha=0.6)
    if 'val/box_loss' in df.columns:
        for col, lbl, c in [('val/box_loss','Box','red'),('val/cls_loss','Cls','orange'),('val/dfl_loss','DFL','purple')]:
            axes[0,1].plot(df['epoch'], df[col], label=lbl, color=c)
        axes[0,1].set_title("Val Loss"); axes[0,1].legend(); axes[0,1].grid(True, ls='--', alpha=0.6)
    if 'metrics/mAP50(B)' in df.columns:
        axes[1,0].plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP@50', color='green', lw=2)
        axes[1,0].plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP@50-95', color='blue', lw=2)
        axes[1,0].set_title("mAP Evaluation"); axes[1,0].legend(); axes[1,0].grid(True, ls='--', alpha=0.6)
    if 'metrics/precision(B)' in df.columns:
        axes[1,1].plot(df['epoch'], df['metrics/precision(B)'], label='Precision', color='teal')
        axes[1,1].plot(df['epoch'], df['metrics/recall(B)'], label='Recall', color='magenta')
        axes[1,1].set_title("Precision & Recall"); axes[1,1].legend(); axes[1,1].grid(True, ls='--', alpha=0.6)
    plt.tight_layout(); plt.show()

plot_results(RUN_DIR)

# %% [markdown]
# # 6b. Evaluasi Model + TTA (Test-Time Augmentation)

# %%
best_pt = RUN_DIR / "weights" / "best.pt"
eval_model = YOLO(str(best_pt)) if best_pt.exists() else model

# --- Standard Evaluation (imgsz=800 untuk konsistensi resolusi deteksi defek mikro) ---
print("\n📊 Evaluasi Model v2 pada Validation Split (imgsz=800)...")
metrics = eval_model.val(data=str(DATA_YAML), split='val', imgsz=800)

v2_metrics = {
    'precision': metrics.box.mp,
    'recall': metrics.box.mr,
    'mAP50': metrics.box.map50,
    'mAP50-95': metrics.box.map,
}

print(f"  • Precision : {v2_metrics['precision']:.4f}")
print(f"  • Recall    : {v2_metrics['recall']:.4f}")
print(f"  • mAP@50    : {v2_metrics['mAP50']:.4f}")
print(f"  • mAP@50-95 : {v2_metrics['mAP50-95']:.4f}")

# --- Test-Time Augmentation (TTA) Evaluation ---
print("\n📊 Evaluasi TTA (Test-Time Augmentation, imgsz=800)...")
metrics_tta = eval_model.val(data=str(DATA_YAML), split='val', imgsz=800, augment=True)
print(f"  [TTA] Precision : {metrics_tta.box.mp:.4f}")
print(f"  [TTA] Recall    : {metrics_tta.box.mr:.4f}")
print(f"  [TTA] mAP@50    : {metrics_tta.box.map50:.4f}")
print(f"  [TTA] mAP@50-95 : {metrics_tta.box.map:.4f}")

# %% [markdown]
# # 6c. Perbandingan v2 vs Baseline & Visualisasi

# %%
# --- Per-Class Detailed Report (Fixed mAP@50 Calculation) ---
print("\n" + "═" * 80)
print("📋 PER-CLASS PERFORMANCE REPORT (v2 vs Baseline)")
print("═" * 80)
if hasattr(metrics.box, 'maps') and len(metrics.box.maps) == len(NUSAQC_CLASS_NAMES):
    ap50_per_class = metrics.box.ap50 if (hasattr(metrics.box, 'ap50') and len(metrics.box.ap50) > 0) else (metrics.box.all_ap[:, 0] if hasattr(metrics.box, 'all_ap') else metrics.box.maps)
    print(f"{'Kelas':<18} {'v2 mAP50':>10} {'Base mAP50':>11} {'Δ mAP50':>10} {'v2 mAP50-95':>12} {'Status':>8}")
    print("─" * 80)
    for i, cls_name in enumerate(NUSAQC_CLASS_NAMES):
        v2_p50 = float(ap50_per_class[i])
        v2_p95 = float(metrics.box.maps[i])
        baseline_val = BASELINE_METRICS['per_class_mAP50'].get(cls_name, 0)
        delta = v2_p50 - baseline_val
        status = "✅ UP" if delta > 0 else ("⚠️ DOWN" if delta < 0 else "➡️ SAME")
        print(f"  {cls_name:<16} {v2_p50:>10.4f} {baseline_val:>11.4f} {delta:>+10.4f} {v2_p95:>12.4f} {status:>8}")
    print("─" * 80)

# --- Baseline Comparison Summary ---
print("\n" + "═" * 70)
print("📊 OVERALL COMPARISON: v2 vs Baseline")
print("═" * 70)
for metric_name in ['precision', 'recall', 'mAP50', 'mAP50-95']:
    v2_val = v2_metrics[metric_name]
    bl_val = BASELINE_METRICS[metric_name]
    delta = v2_val - bl_val
    pct = (delta / bl_val) * 100 if bl_val > 0 else 0
    status = "✅" if delta > 0 else "⚠️"
    print(f"  {status} {metric_name:<12}: {bl_val:.4f} → {v2_val:.4f} ({delta:+.4f}, {pct:+.1f}%)")
print("═" * 70)

# --- Target Achievement Check ---
TARGETS = {'mAP50': 0.80, 'recall': 0.75, 'mAP50-95': 0.55}
print("\n🎯 Target Achievement:")
all_met = True
for t_name, t_val in TARGETS.items():
    achieved = v2_metrics[t_name] >= t_val
    icon = "✅" if achieved else "❌"
    print(f"  {icon} {t_name}: {v2_metrics[t_name]:.4f} (target ≥ {t_val:.2f})")
    if not achieved:
        all_met = False
if all_met:
    print("\n🏆 SEMUA TARGET TERCAPAI!")
else:
    print("\n⚠️ Beberapa target belum tercapai — pertimbangkan iterasi lanjutan.")

# --- mAP@50 Per-Class Bar Chart (v2 vs Baseline) ---
if hasattr(metrics.box, 'maps') and len(metrics.box.maps) == len(NUSAQC_CLASS_NAMES):
    ap50_per_class = metrics.box.ap50 if (hasattr(metrics.box, 'ap50') and len(metrics.box.ap50) > 0) else (metrics.box.all_ap[:, 0] if hasattr(metrics.box, 'all_ap') else metrics.box.maps)
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(NUSAQC_CLASS_NAMES))
    width = 0.35
    baseline_vals = [BASELINE_METRICS['per_class_mAP50'][c] for c in NUSAQC_CLASS_NAMES]
    v2_vals = [float(ap50_per_class[i]) for i in range(len(NUSAQC_CLASS_NAMES))]

    bars1 = ax.bar(x - width/2, baseline_vals, width, label='Baseline v1', color='#CCCCCC', edgecolor='#999999')
    bars2 = ax.bar(x + width/2, v2_vals, width, label='Improved v2', color=['#FF9900', '#FF0000', '#FFCC00', '#9900FF'], edgecolor='#333333')

    ax.set_xlabel('Kelas Defek', fontsize=12)
    ax.set_ylabel('mAP@50', fontsize=12)
    ax.set_title('mAP@50 per Kelas: Baseline vs Improved v2', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(NUSAQC_CLASS_NAMES, fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=11)
    ax.grid(True, axis='y', ls='--', alpha=0.4)

    for b in bars1:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.02, f"{b.get_height():.3f}",
                ha='center', fontsize=9, color='#666666')
    for b in bars2:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.02, f"{b.get_height():.3f}",
                ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout(); plt.show()

# %% [markdown]
# # 6d. Ekspor ONNX, CPU Latency Benchmark & Copy Output

# %%
# --- Export ONNX Model (640px untuk deploy Raspi) ---
print("\n📦 Exporting ONNX (imgsz=640 untuk Raspberry Pi deploy)...")
onnx_path = eval_model.export(format="onnx", imgsz=640, simplify=True)
print(f"✅ ONNX exported: {onnx_path}")

# --- CPU Latency Benchmarking (Raspberry Pi 5 Simulation: Multi-threading 4 Cores) ---
print("\n" + "═" * 70)
print("⏱️ BENCHMARKING CPU INFERENCE LATENCY (MODEL 2 YOLOv8s)")
print("═" * 70)
try:
    import time
    import onnxruntime as ort
    
    sess_options = ort.SessionOptions()
    sess_options.intra_op_num_threads = 4
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    
    dummy_input = np.random.randn(1, 3, 640, 640).astype(np.float32)
    ort_session = ort.InferenceSession(str(onnx_path), sess_options, providers=["CPUExecutionProvider"])
    in_name = ort_session.get_inputs()[0].name
    
    # Warmup
    for _ in range(20):
        _ = ort_session.run(None, {in_name: dummy_input})
    
    # Timed runs
    t0 = time.time()
    n_runs = 50
    for _ in range(n_runs):
        _ = ort_session.run(None, {in_name: dummy_input})
    avg_ms = ((time.time() - t0) / n_runs) * 1000
    fps = 1000.0 / avg_ms
    print(f"  • ONNX CPU Latency (4 Cores, 640x640): {avg_ms:.2f} ms/frame ({fps:.1f} FPS)")
    print(f"  • Target Penyisihan COMPFEST (<150 ms): {'✅ TERCAPAI' if avg_ms < 150 else '⚠️ MELEBIHI'}")
except Exception as e:
    print(f"  Note: Benchmark latency skipped ({e})")

# Copy output ke lokasi utama
out_dir = WORKING_DIR / "MODEL_OUTPUTS"
out_dir.mkdir(parents=True, exist_ok=True)
if best_pt.exists():
    shutil.copy(best_pt, WORKING_DIR / "best.pt")
    shutil.copy(best_pt, out_dir / "nusaqc_model2_defect_detector.pt")
    print(f"  ✓ best.pt -> {WORKING_DIR / 'best.pt'}")
if onnx_path and Path(onnx_path).exists():
    shutil.copy(onnx_path, WORKING_DIR / "model2_defect_detector.onnx")
    shutil.copy(onnx_path, out_dir / "nusaqc_model2_defect_detector.onnx")
    print(f"  ✓ ONNX -> {WORKING_DIR / 'model2_defect_detector.onnx'}")
print(f"\n✨ Seluruh Output Siap di: {out_dir.resolve()}")

