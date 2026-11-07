# 📜 Rekap Rekayasa, Eksperimen & Kemajuan AI Model 2 (Fish Defect Detector)

Dokumen ini mencatat secara sistematis seluruh keputusan arsitektural, diagnosa performa, optimasi hyperparameter, pivot dataset, dan hasil pipeline **Model 2 NusaQC** (*Surface Contamination & Defect Detector*).

---

## 📌 Ringkasan Status & Pencapaian Utama

- **Tipe Model**: YOLOv8s (*Object Detection & Classification*)
- **Skop Kelas Active**: 4 Kelas NusaQC (`sisik_sisa`, `warna_abnormal`, `luka_robekan`, `lendir_berlebih`)
- **Hasil Performa Seed Model**:
  - **Run 1** (Hyperparameter awal): mAP@50 = **0.188**, Recall = **0.133** (Val Loss meledak ke ~80.000).
  - **Run 2** (Tuned Hyperparameter): mAP@50 = **0.409 (+117%)**, Recall = **0.356 (+167%)**, Test mAP@50 = **0.287 (+53%)**.
- **Pencapaian Pseudo-Labeling Pipeline**:
  - Berhasil mengkonsolidasi 3 dataset (Roboflow + HuggingFace panda992 + Alaa Mahmoud).
  - Total citra berkembang dari **457 citra ➔ 3.212 citra (+602% / 7x lipat)**.
  - Total anotasi bounding box: **3.509 bbox**.

---

## 🧪 Chronological Log & Rekayasa Teknikal

### 1. Diagnosa & Tuning Hyperparameter Seed Model (Eksperimen Run 1 vs Run 2)
- **Problem**: Pada Run 1 (60 epoch), Val Classification Loss melonjak tak terkendali ke ~80.000 di epoch awal dan Recall hanya 0.133.
- **Root Cause**:
  1. `lr0: 0.003` terlalu tinggi tanpa warmup yang cukup.
  2. Weight `cls: 0.7` terlalu rendah, sehingga model tidak memprioritaskan akurasi klasifikasi.
  3. Augmentasi `mosaic: 0.2` kurang agresif untuk dataset berukuran kecil (457 citra).
- **Solusi & Hyperparameter Final**:
  ```python
  HPARAMS = {
      'epochs': 100, 'batch': 16, 'imgsz': 640,
      'optimizer': 'AdamW', 'lr0': 0.001, 'lrf': 0.01,
      'momentum': 0.937, 'weight_decay': 0.001, 'warmup_epochs': 5.0,
      'mosaic': 1.0, 'close_mosaic': 15, 'mixup': 0.15, 'copy_paste': 0.2,
      'hsv_h': 0.015, 'hsv_s': 0.7, 'hsv_v': 0.4,
      'scale': 0.5, 'fliplr': 0.5, 'flipud': 0.1,
      'translate': 0.2, 'degrees': 10.0,
      'box': 7.5, 'cls': 1.5, 'dfl': 1.5, 'patience': 30
  }
  ```
- **Hasil**: Val mAP@50 melonjak dari 0.188 ➔ 0.409. Loss kurva stabil dan konvergen.

---

### 2. Pivot Dataset HuggingFace (Gated ➔ Public)
- **Problem**: Dataset `Saon110/bd-fish-disease-dataset` membutuhkan authentikasi token (Gated dataset) sehingga melempar `DatasetNotFoundError` di Kaggle.
- **Solusi**: Pivot ke dataset publik [`panda992/fish_disease_datasets`](https://huggingface.co/datasets/panda992/fish_disease_datasets).
- **Validasi Provenance**: Dataset `panda992` merupakan sumber publik asli dari data ikan BD Fish (2.450 gambar, 7 kelas) tanpa menyertakan data udang yang irrelevant.
- **Dampak**: Pipeline pseudo-labeling dapat berjalan otomatis 100% tanpa hambatan autentikasi token.

---

### 3. Arsitektur Hybrid Class-Locking pada Pseudo-Labeling
Untuk mencegah pembiasan (*class drift/hallucination*) oleh Seed Model pada dataset eksternal, dikembangkan strategi **Hybrid Class-Locking**:

```text
               ┌────────────────────────────────────────────────────────┐
               │         INPUT DATASET PSEUDO-LABELING                  │
               └──────────────────────────┬─────────────────────────────┘
                                          │
        ┌─────────────────────────────────┼────────────────────────────────┐
        ▼                                 ▼                                ▼
┌───────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
│   Roboflow Dataset    │   │   HF panda992 Dataset     │   │   Alaa Mahmoud Dataset    │
│    (457 BBox Raw)     │   │  (2.450 Specific GT)      │   │   (305 Binary Infected)   │
└───────────┬───────────┘   └─────────────┬─────────────┘   └─────────────┬─────────────┘
            │                             │                               │
            ▼                             ▼                               ▼
┌───────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
│ 100% Direct Mapping   │   │  Ground-Truth Class Lock  │   │  Dynamic AI Classification│
│ (7 ➔ 4 kelas NusaQC)  │   │   (`lock_class = True`)   │   │  (`lock_class = False`)   │
│                       │   │  YOLO hanya cari (x,y,w,h)│   │  YOLO cari (x,y,w,h) & cls│
└───────────┬───────────┘   └─────────────┬─────────────┘   └─────────────┬─────────────┘
            │                             │                               │
            └─────────────────────────────┼───────────────────────────────┘
                                          ▼
                        ┌──────────────────────────────────┐
                        │ Extended Dataset (3.212 Gambar)  │
                        │ 3.509 BBox | 4 Kelas NusaQC      │
                        └──────────────────────────────────┘
```

---

### 4. Hasil Distribusi Final Extended Dataset (3.212 Gambar)

| ID | Kelas NusaQC | Jumlah BBox (Train Set) | Persentase |
|:--:|:---|:---:|:---:|
| **0** | `sisik_sisa` | 434 | 12.4% |
| **1** | `warna_abnormal` | 1.511 | 43.1% |
| **2** | `luka_robekan` | 726 | 20.7% |
| **3** | `lendir_berlebih` | 489 | 13.9% |
| **—** | `background/empty` | 549 | 15.6% |
| **TOTAL** | **4 Kelas + Background** | **3.509 BBox / 3.212 Gambar** | **100%** |

---

## 🔗 Sinergi dengan Dokumen Proyek Lainnya

1. **[MODEL_2_PIPELINE_GUIDE.md](file:///d:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/MODEL_2_PIPELINE_GUIDE.md)**: Telah diperbarui mencakup alur 3-tahap eksekusi Kaggle (Seed Model ➔ Pseudo-labeling ➔ Retrain Final).
2. **[ANNOTATION_GUIDE_MODEL2.md](file:///d:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/ANNOTATION_GUIDE_MODEL2.md)**: Telah diselaraskan dengan kriteria visual 4 kelas dan dikonfirmasi 1-to-1 dengan template XML Label Studio [`02_label_studio_config.xml`](file:///d:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/02_label_studio_config.xml).
3. **[docs/md/datasets.md](file:///d:/main/Documents/explore/compe/hackhathon/AIC/docs/md/datasets.md)**: Spesifikasi dataset 1 telah diperbarui dari Saon110 ke `panda992/fish_disease_datasets` (2.450 citra).
