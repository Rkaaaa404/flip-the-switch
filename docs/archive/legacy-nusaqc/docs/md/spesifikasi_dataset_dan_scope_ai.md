# Spesifikasi Strategis Multi-Dataset & Scope Spesies NusaQC
## Integrasi Visi Proposal, Taksonomi Dataset, dan Teknik Handling Anotasi AI
### AIC COMPFEST 18 · 2026 · Smart Manufacturing

---

## 1. Executive Overview & Alignment Visi Proposal

Dokumen ini memetakan secara presisi integrasi antara **Visi Sistem NusaQC** (sebagaimana dirumuskan dalam [`FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md)), **Rencana Struktur Proposal** ([`Rencana Struktur Proposal.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/Rencana%20Struktur%20Proposal.md)), **Rekomendasi Scope Spesies** ([`ideation/Rekomendasi_Scope_Spesies_NusaQC.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/ideation/Rekomendasi_Scope_Spesies_NusaQC.md)), serta struktur fisik dataset aktual ([`treeDaFiF.txt`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/treeDaFiF.txt), [`treeFFE.txt`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/treeFFE.txt), [`docs/md/dafif.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/docs/md/dafif.md), dan [`datasets.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/datasets.md)).

### Core AI Architecture: Dual-Engine Pipeline
1. **Model 1 — Fish Freshness Classifier (MobileNetV3-Small ONNX Float32):** Mengklasifikasikan kesegaran fisik berdasarkan standar organoleptik **SNI 2729:2013** menjadi 3 grade (**Grade A** / **Grade B** / **Grade C**) dengan model ultra-kompak (0.28 MB) dan latensi 2.44 ms.
2. **Model 2 — Surface Contamination & Defect Detector (YOLOv8s ONNX):** Mendeteksi cacat fisik visual dan kontaminasi permukaan luar dengan *bounding box* untuk 4 kelas cacat utama NusaQC (`sisik_sisa`, `warna_abnormal`, `luka_robekan`, `lendir_berlebih`).

---

## 2. Formulasi Scope Spesies Komoditas Ekspor

Berdasarkan data BKIPM KKP & BPS (2022–2024), komoditas utama ekspor perikanan Indonesia terbagi menjadi Pelagis Besar, Pelagis Kecil, Akuakultur Air Tawar, dan Salmonidae (olahan re-ekspor/impor tinggi). Scope spesies NusaQC dibagi menjadi dua tier utama:

```
Scope Spesies NusaQC
├── Tier 1: Core MVP Scope (4 Spesies Strategis Utama)
│   ├── Pelagis Kecil : Mackerel / Kembung (Rastrelliger sp.)
│   ├── Air Tawar     : Tilapia / Nila / Mujair (Oreochromis sp.)
│   ├── Pelagis Besar : Tuna / Cakalang / Tongkol (Euthynnus affinis)
│   └── High-Value    : Salmon (Salmo salar)
│
└── Tier 2: Conditional Expansion & Benchmark Generalisasi
    ├── FFE Regional Eye Freshness (8 Spesies: Bandeng, Kurau, Gelama, Croaker, Biji Nangka, dll.)
    └── BD Fish & Shrimp Pathology (Penyakit spesifik udang WSSV & penyakit ikan akuakultur)
```

---

## 3. DATASET A: Engine Kesegaran Physical (Model 1 — MobileNetV3-Small)

Dataset A dirancang untuk melatih **Model 1 (Freshness Classifier)**. Memadukan dua dataset akademis utama: **DaFiF (Dataset 3)** dan **FFE (Dataset 4)**.

### 3.1 Detail Riil Struktur & Pelabelan DaFiF (Dataset 3)
*   **Struktur Direktori (`treeDaFiF.txt`):** Hierarki bertingkat:
    $$\text{Day [1..11]} \longrightarrow \text{Session [1..2]} \longrightarrow \text{[Mackerel | Tilapia | Tuna]}$$
*   **Isi Data:** Total 2.536 gambar JPG (Mackerel: 859, Tilapia: 840, Tuna: 837) + 63 file Excel (`.xlsx`) rekapitulasi organoleptik & sensor gas E-Nose.
*   **Metode Pelabelan DaFiF (Skor SNI 2729:2013):**
    Sebagaimana tercantum dalam [`docs/md/dafif.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/docs/md/dafif.md) (Tabel 2 & Tabel 3), setiap sesi pemeriksaan harian dinilai oleh ahli organoleptik pada 6 parameter dengan rentang skor 1–9:
    *   **E** (Eyes / Mata), **G** (Gills / Insang), **B** (Body Mucus / Lendir Surface), **M** (Meat / Daging), **S** (Smell / Bau), **T** (Body Textures / Tekstur).

#### Pemetaan Skor Organoleptik DaFiF ke Grade NusaQC:
$$S_{\text{avg}} = \frac{E + G + B + M + S + T}{6}$$

| Skor $S_{\text{avg}}$ (SNI 2729:2013) | Kategori Penyimpanan Es | Grade NusaQC | Keputusan Sistem |
|:---:|:---:|:---:|:---:|
| **8.0 – 9.0** | Hari ke 1–2 | **Grade A** | **PASS (Hijau)** |
| **6.0 – 7.9** | Hari ke 3–6 | **Grade B** | **CONDITIONAL (Kuning)** |
| **1.0 – 5.9** | Hari ke 7–11 | **Grade C** | **FAIL (Merah)** |

---

### 3.2 Detail Riil Struktur & Pelabelan FFE (Dataset 4 — Freshness of Fish Eyes)
*   **Struktur Direktori (`treeFFE.txt`):** 24 folder *flat* berformat `[Spesies] - [Tingkat Kesegaran]`:
    *   Contoh: `Chanos Chanos - Highly Fresh`, `Chanos Chanos - Fresh`, `Chanos Chanos - Not Fresh`, `Oreochromis Niloticus - Highly Fresh`, `Rastrelliger Faughni - Not Fresh`, dll.
*   **Isi Data:** 4.390 gambar cropped khusus area mata ikan dari 8 spesies.
*   **Pemetaan Folder FFE ke Grade NusaQC:**

| Label Folder FFE | Hari Penyimpanan | Grade NusaQC |
|:---|:---:|:---:|
| `[Spesies] - Highly Fresh` | Hari 1–2 | **Grade A** |
| `[Spesies] - Fresh` | Hari 3–4 | **Grade B** |
| `[Spesies] - Not Fresh` | Hari 5–6 | **Grade C** |

---

### 3.3 Merekonsiliasi & Menghubungkan DaFiF dan FFE
Bagaimana menghubungkan data DaFiF (full frame ikan/kepala + file Excel organoleptik) dengan FFE (cropped eye + folder label)?

```
                 GABUNGAN DATASET A (MODEL 1: FRESHNESS)
                 ─────────────────────────────────────────

  [ Full Frame Foto DaFiF ]                    [ Cropped Eyes FFE ]
 (Mackerel, Tilapia, Tuna)                    (8 Spesies Regional)
             │                                         │
             ▼ Tahap 1: Head Crop                      │
   YOLO Head/Eye Localizer                             │
             │                                         │
             ▼ Crop ROI (224×224)                      │
   ROI Kepala & Mata DaFiF                             │
             │                                         │
             └───────────────────┬─────────────────────┘
                                 │
                                 ▼ Label Harmonization
                   [ Harmonized Grade Dataset ]
                  • Grade A : 3.600+ Sampel
                  • Grade B : 2.100+ Sampel
                  • Grade C : 1.900+ Sampel
                                 │
                                 ▼ Training
                  MobileNetV3-Small INT8 ONNX Engine
```

1.  **Overlapping Taxa Alignment:** Spesies *Mackerel* (*Rastrelliger*) dan *Tilapia* (*Oreochromis*) hadir di kedua dataset. DaFiF menyediakan data ROI kepala utuh + acuan fisik SNI, sedangkan FFE memberikan variasi pupil/kornea mata resolusi tinggi.
2.  **Two-Stage Eye Clarity Sub-Engine:**
    *   *Stage 1 (Head Localizer):* Model YOLOv8n mengidentifikasi dan melakukan *crop* otomatis pada area kepala/mata dari foto full-frame DaFiF.
    *   *Stage 2 (Unified Classifier):* Hasil crop kepala DaFiF disatukan dengan citra mata FFE, yang semuanya telah di-label ulang ke skema baku **Grade A / B / C**.

---

## 4. DATASET B: Engine Deteksi Cacat Fisik & Kontaminasi (Model 2 — YOLOv8n)

Dataset B dirancang untuk melatih **Model 2 (Surface Contamination & Defect Detector)**. Mengombinasikan dataset patologi dan objek deteksi:

| No | Dataset | Jumlah Gambar | Format Asli Data | Status Scope | Peran Utama |
|:--:|:---|:---:|:---|:---|:---|
| **1** | **Roboflow Fish Disease** | 457 | Bounding Box YOLO (`.txt`) | **Active MVP** | *Seed Annotations* awal lokasi luka & lesi |
| **2** | **BD Fish & Shrimp Disease** | 5.887 | Classification 11 Kelas | **Active MVP** | Cross-domain penyakit akuakultur & lesi |
| **3** | **Alaa Mahmoud Fish Disease** | 305 | Binary Classification | **Active MVP** | Data augmentasi infeksi kulit fisik |
| **4** | **SalmonScan** | 1.208 | Classification (Fresh vs Infected) | *Future Scope* | Deteksi infeksi spesifik Salmonidae pasca-MVP |

---

## 5. Handling Label Heterogen & Missing Bounding Box Annotations

### ⚠️ Masalah Utama pada Dataset B:
1.  **Heterogenitas Nama Label:** Roboflow (Dataset 6) menggunakan kode internal seperti `BDA` (Bacterial Disease Aeromonas), `BGD` (Bacterial Gill Disease), `BRD` (Bacterial Red Disease), `Red Spot`, `Skin Ulcer`, dll.
2.  **Ketiadaan Bounding Box pada Dataset Classification (Dataset 1, 2, & 5):** Dataset 1 (BD Fish: 5.887 gambar), Dataset 2 (SalmonScan: 1.208 gambar), dan Dataset 5 (Alaa Mahmoud: 305 gambar) **hanya memiliki label kelas per gambar (image-level classification)** dan **TIDAK MEMILIKI anotasi bounding box ($x, y, w, h$)**.

---

### 🛡️ Solusi Engineering Handling Label Heterogen & Missing Annotations

#### Solusi 1: Taxonomy Harmonization Matrix (Penyelarasan Kelas)
Semua label heterogen dari seluruh dataset patologi diselaraskan ke dalam **4 Standard Bounding Box Classes NusaQC**:

```
                       TAXONOMY HARMONIZATION MATRIX
                       ──────────────────────────────
Roboflow / BD Fish / Alaa Mahmoud                       NusaQC Standard Classes
─────────────────────────────────                       ───────────────────────
• Scale Loss, Missing Scales, Parasite Attach   ──────►  [ 0: sisik_sisa ]
• BRD, Red Spot, Aeromoniasis, Black Gill,      ──────►  [ 1: warna_abnormal ]
  Hemorrhage, Skin Discoloration
• BDA, Skin Ulcer, Winter Ulcer Disease,        ──────►  [ 2: luka_robekan ]
  Fin Rot, Tail Rot, Saprolegniasis Fungus
• Excess Mucus, Clotted White Mucus, WTD        ──────►  [ 3: lendir_berlebih ]
```

---

#### Solusi 2: Semi-Automated Pseudo-Labeling & Auto-Annotation Pipeline
Untuk mengonversi 7.400+ gambar klasifikasi (dari Dataset 1, 2, & 5) yang **belum ber-bounding box** menjadi format anotasi YOLOv8n:

```
              AUTO-ANNOTATION & PSEUDO-LABELING PIPELINE
              ───────────────────────────────────────────

  [ Dataset 1, 2, & 5 (Image-Level Classification) ]
  (7.400+ Gambar Tanpa Bounding Box: SalmonScan, BD Fish, Alaa)
                              │
                              ▼
  [ Stage 1: Seed YOLO Training ]
  Latih Model YOLO Baseline menggunakan Dataset 6 (Roboflow: 457 gambar ber-bbox)
  + 200 Gambar Lapangan yang Dianotasi Manual via Label Studio / CVAT
                              │
                              ▼
  [ Stage 2: Segment Anything Model (SAM 2) / YOLO Auto-Annotator ]
  Jalankan Zero-Shot Feature Localization pada Regio Lesi/Infected Area
                              │
                              ▼
  [ Stage 3: Pseudo-BBox Generation ]
  Ekstraksi koordinat Saliency Map / CAM -> Hasilkan file `.txt` YOLO otomatis
  Format: <class_id> <x_center> <y_center> <width> <height>
                              │
                              ▼
  [ Stage 4: Human-in-the-Loop Verification ]
  Quality Check acak (15% sample) via Roboflow / CVAT untuk penyesuaian threshold
```

Dengan pipeline ini, dataset klasifikasi raksasa (seperti BD Fish & SalmonScan) dapat dikonversi menjadi dataset *object detection* ber-bounding box dalam waktu cepat tanpa perlu melakukan anotasi manual satu per satu dari nol.

---

## 6. Ringkasan Pembagian Dataset Final (Train / Validation / Test Split)

| Sub-Engine | Model Backbone | Dataset Sumber | Total Gambar Final | Split (70% Train / 15% Val / 15% Test) | Output Model |
|:---|:---|:---|:---:|:---:|:---|
| **Model 1 (Freshness)** | MobileNetV3-Small ONNX Float32 (0.28 MB) | DaFiF (Primary) + FFE (Secondary) | **2.536 (DaFiF)** | Grouped Split (by Session/Day) | Grade A / B / C + Confidence Score |
| **Model 2 (Defect Detector)** | YOLOv8s Float32 ONNX | NusaQC Cleaned Defect Dataset | **1.861 BBoxes** | 70% Train / 15% Val / 15% Test | Bounding Box + 4 Defect Labels + PASS/FAIL |

---

## 7. Panduan Integrasi ke Proposals & Repository Code

### A. Teks Tambahan untuk Proposal PDF (`FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md`)
Dapat disisipkan pada **Sub-bab 7.3 (Strategi Konsolidasi Multi-Dataset & Anotasi)**:

> *"NusaQC mengatasi keterbatasan dataset publik tunggal melalui konsolidasi 6 dataset akademis (DaFiF, FFE, SalmonScan, Roboflow, Alaa Mahmoud, dan BD Fish) yang diselaraskan secara ketat. Untuk mengatasi heterogenitas label dan ketiadaan bounding box pada dataset klasifikasi murni, NusaQC mengimplementasikan **Taxonomy Harmonization Matrix** yang menyatukan seluruh patologi ke dalam 5 kelas standar industri (`sisik_sisa`, `warna_abnormal`, `luka_robekan`, `foreign_object`, `lendir_berlebih`), serta menerapkan **Semi-Automated Pseudo-Labeling Pipeline** berbasis SAM 2 dan seed YOLOv8n untuk mengekstraksi koordinat bounding box secara presisi."*

### B. Struktur Folder Repository Data Pipeline
```
nusaqc/
├── data/
│   ├── raw/
│   │   ├── dafif/                  ← Tree: Day/Session/Species (.jpg + .xlsx)
│   │   ├── ffe/                    ← Tree: 24 Flat Class Folders
│   │   ├── roboflow_defect/        ← YOLO format (.jpg + .txt)
│   │   └── salmonscan/             ← Fresh vs Infected folders
│   ├── processed/
│   │   ├── model1_freshness/       ← Train/Val/Test split (Grade A/B/C)
│   │   └── model2_defect/          ← Train/Val/Test split (YOLO format)
│   └── scripts/
│       ├── parse_dafif_excel.py    ← Script ekstrak skor SNI .xlsx ke Grade A/B/C
│       ├── harmonize_labels.py     ← Map Roboflow/BD Fish labels ke 5 NusaQC classes
│       └── auto_annotate_sam.py    ← Pseudo-labeling generator untuk dataset 1 & 2
```
