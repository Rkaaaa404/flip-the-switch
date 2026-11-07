# NusaQC Master Context & Lembar Kerja Revisi Tim (AIC COMPFEST 18)
### Dokumen Utama Acuan Eksekusi AI Engineer, Frontend/Backend, & Team Lead

---

> 📌 **Tujuan Dokumen Ini:**
> Dokumen ini menyatukan seluruh konteks produk NusaQC, aturan lomba COMPFEST 18, analisis jurnal rujukan, serta **daftar revisi kritis 7-poin** yang wajib dieskusi bersama sebelum submisi babak penyisihan (25 Agustus 2026).

---

## DAFTAR ISI
1. [Ringkasan Eksekutif & Positioning Produk](#1-ringkasan-eksekutif--positioning-produk)
2. [Checklist Revisi Kritis Proposal & Sistem (7 Celah Kunci)](#2-checklist-revisi-kritis-proposal--sistem-7-celah-kunci)
3. [Arsitektur & Action Plan Model 1 (Freshness Engine)](#3-arsitektur--action-plan-model-1-freshness-engine)
4. [Arsitektur & Action Plan Model 2 (Defect Detector - YOLOv8n)](#4-arsitektur--action-plan-model-2-defect-detector---yolov8n)
5. [Closed-Loop Hardware & Rulebook MVP Compliance](#5-closed-loop-hardware--rulebook-mvp-compliance)
6. [Multi-Stakeholder Framing & Kalkulasi Bisnis Kredibel](#6-multi-stakeholder-framing--kalkulasi-bisnis-kredibel)

---

## 1. Ringkasan Eksekutif & Positioning Produk

* **Nama Produk:** **NusaQC** — AI-Powered Visual Quality Control System
* **Tema Lomba:** *AI for the Backbone of the Economy* (Fokus: Smart Manufacturing / Unit Pengolahan Ikan - UPI Ekspor)
* **Problem Framing:** Kerugian ekspor perikanan Indonesia akibat penolakan pasar global (FDA AS & RASFF EU) pada kategori **filthy** (kontaminasi fisik visual) dan **penurunan kesegaran**. QC manual saat ini berbasis kertas, subjektif, lambat (5–10 detik/ikan), dan kelelahan operator.
* **Solusi NusaQC:** Sistem pemilah otomatis berbasis Computer Vision & Closed-Loop Control. Sinyal AI (PASS / CONDITIONAL / FAIL) langsung mengendalikan aktuator fisik (Relay Conveyor STOP/SLOW + Tower Light + Buzzer) dan mencatat log digital ke SQLite.

---

## 2. Checklist Revisi Kritis Proposal & Sistem (7 Celah Kunci)

Berdasarkan hasil cross-check mendalam antara proposal, spesifikasi AI, dan rulebook COMPFEST 18, berikut 7 hal yang **WAJIB DIREVISI** oleh tim:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    7 REVISI KRITIS SUBMISI NUSAQC                       │
├────┬─────────────────────────────┬──────────────────────────────────────┤
│ No │ Temuan & Celah              │ Tindakan Eksekusi (Action Plan)      │
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 1  │ Pelanggaran Rulebook FE     │ Hapus halaman/komponen "History"     │
│    │ (`LotHistory.jsx` di FE)    │ (`LotHistory.jsx`) agar patuh rule   │
│    │                             │ "Dilarang Halaman Riwayat".          │
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 2  │ Inkonsistensi Kapabilitas   │ Ubah Salmon di Proposal dari Tier 1  │
│    │ Spesies (Salmon)            │ ke Tier 2 (Target Ekspansi via       │
│    │                             │ Transfer Learning Model 2).          │
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 3  │ Kalkulasi Payback Period    │ Ubah Payback dari "0,05 bulan" ke    │
│    │ Tidak Kredibel              │ **3–6 Bulan** (CAPEX Rp 3-4 jt/unit) │
│    │                             │ dengan sensitivitas biaya realistis. │
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 4  │ Asimetri Kematangan Model   │ Jalankan baseline Model 2 (YOLOv8n)  │
│    │ (Model 1 vs Model 2)        │ & cantumkan angka mAP50 awal di proposal│
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 5  │ Kepatuhan Blind Judging     │ Bersihkan "Catatan Internal",        │
│    │ & Anonimitas Berkas         │ "Kritisasi Rayka", dan username      │
│    │                             │ Kaggle sebelum ekspor PDF.           │
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 6  │ Risiko Halaman PDF          │ Susun ulang layouting diagram ASCII  │
│    │ Melebihi Batas (Maks 20 hlm)│ agar pas dalam format PDF ≤20 hlm.   │
├────┼─────────────────────────────┼──────────────────────────────────────┤
│ 7  │ Ekosistem Masih 1-Aktor     │ Angkat narasi Multi-Stakeholder:     │
│    │ (Hanya UPI)                 │ **Pemasok/Nelayan ↔ UPI ↔ Buyer**    │
│    │                             │ via Digital Quality Traceability.    │
└────┴─────────────────────────────┴──────────────────────────────────────┘
```

---

## 3. Arsitektur & Action Plan Model 1 (Freshness Engine)

### A. Simplifikasi Arsitektur MVP (Kepatuhan Rulebook "Dilarang Overbuilt")
* **Rekonsiliasi Pipeline:** Untuk MVP Penyisihan, arsitektur Model 1 disederhanakan dan disamakan di seluruh dokumen:
  * **Input:** Preprocessing non-ML (Fixed-region crop / Full-frame resize $224 \times 224$ + normalization).
  * **Backbone:** **MobileNetV3-Small INT8 ONNX** langsung mengklasifikasikan ke `Grade_A`, `Grade_B`, `Grade_C` berdasarkan acuan organoleptik **SNI 2729:2013**.
  * **Roadmap Hackathon Final:** "Two-Stage YOLO Head Localizer" dan "Freshness Day Estimator" ditulis secara eksplisit sebagai *Roadmap Hackathon Final / Production Vision*, bukan diklaim sudah selesai di MVP Penyisihan.

### B. Peran Dataset & Metodologi Evaluation
* **DaFiF (2.536 gambar):** Dataset Utama untuk Training & Testing Model 1 MVP.
* **FFE (2.199 / 4.390 gambar):** Didokumentasikan sebagai **Secondary Validation Set / Cross-Species Generalization Check** (bukan digabung mentah-mentah agar alur cerita konsisten).
* **Metodologi Split & Laporan Metrik:**
  * Laporkan dua angka di proposal: *Random Split Accuracy* (**99.48%**) dan *Grouped Split by Day/Session* (untuk membuktikan ketahanan terhadap temporal data leakage).
  * Laporkan secara eksplisit **Recall Grade C = 1.0000 (0% False Negative)** sebagai metrik keamanan pangan (*safety critical*).

---

## 4. Arsitektur & Action Plan Model 2 (Defect Detector — YOLOv8n)

### A. Baseline Benchmark & Kalibrasi Target mAP50
* **Seed Dataset:** Dataset 6 (Roboflow Fish Disease, 457 gambar ber-bounding box, 7 kelas).
  * Benchmark Pretrained Roboflow awal: mAP50 **62.7%**, Precision 76%, Recall 53%.
  * *Catatan Kelas:* Kelas `HF` (Healthy Fish) adalah sampel negatif (bebas defek).
* **Pipeline Pseudo-Labeling:** Mengonversi 7.400+ gambar dari Dataset 1 (BD Fish), Dataset 2 (SalmonScan), dan Dataset 5 (Alaa Mahmoud) menggunakan seed YOLOv8n & SAM 2.
* **Target mAP50 Proposal:** Cantumkan target mAP50 sebagai **rentang realistis (0.65 – 0.75)**. Jika training sudah selesai, cantumkan angka aktual apa adanya.

### B. Taxonomy Harmonization Matrix (Penyelarasan 5 Kelas NusaQC)

| Kelas Asli Roboflow / BD Fish / SalmonScan | Pemetaan Kelas Standar NusaQC |
| :--- | :--- |
| `Scale Loss`, `Missing Scales`, `Parasite Attach` | **`0: sisik_sisa`** |
| `BRD`, `Red Spot`, `Aeromoniasis`, `Black Gill`, `Skin Discoloration`, **`WTD` (White Tail)** | **`1: warna_abnormal`** |
| `BDA`, `Skin Ulcer`, `Tearing`, `Cut`, **`FDS` (Fungal Saprolegniasis)** | **`2: luka_robekan`** |
| `Foreign Object`, `Debris`, `Plastic Particle` | **`3: foreign_object`** |
| `Excess Mucus`, `Clotted White Mucus` | **`4: lendir_berlebih`** |

### C. Alokasi Anotasi Manual Terbatas (Quality Control)
* Alokasikan anotasi manual **hanya** untuk:
  1. **QC Verification (15% sample check)** pada stage pseudo-labeling.
  2. **Field Validation Set kecil (50–100 foto)** dari sampel observasi lapangan (UPT LPPMHP Surabaya / LPPMHP Jatim).

---

## 5. Closed-Loop Hardware & Rulebook MVP Compliance

### Matrix Kepatuhan Rulebook COMPFEST 18 (Penyisihan):

| Komponen Rulebook | Batasan Wajib | Implementasi NusaQC |
| :--- | :--- | :--- |
| **Frontend (FE)** | Input tunggal & output AI | Dashboard monitoring real-time (Hapus halaman History). |
| **Backend (BE)** | Pemrosesan sinkron, `docker compose` | FastAPI + ONNX Runtime CPU, synchronous HTTP request. |
| **Model AI** | Inference core, parameter static | MobileNetV3-Small INT8 ONNX + YOLOv8n Float32 ONNX. |
| **Mock Hardware Mode** | Wajib untuk pengujian juri | Variable `ENABLE_MOCK_HARDWARE=true` di FastAPI. |

---

## 6. Multi-Stakeholder Framing & Kalkulasi Bisnis Kredibel

### A. Diagram Framing Ekosistem 3-Pihak
Untuk memenuhi kriteria nilai tertinggi Orisinalitas & Dampak Sosial (20%), posisikan NusaQC sebagai penghubung ekosistem:

```
┌─────────────────┐        Digital Quality Traceability        ┌─────────────────┐
│ PEMASOK/NELAYAN ├───────────────────────────────────────────►│ IMPORTER/BUYER  │
└────────┬────────┘                                            └────────▲────────┘
         │ Transparansi Lot                                             │ Sertifikat QC
         ▼                                                              │ Digital QR
┌───────────────────────────────────────────────────────────────────────┴─┐
│                         UPI (NUSAQC SYSTEM)                             │
│  • Closed-Loop Inspection  • Digital Audit Log  • Continuous Sorting    │
└─────────────────────────────────────────────────────────────────────────┘
```

### B. Kalkulasi ROI & Unit Economics Realistis
* **CAPEX Hardware per Titik Inspeksi:** Rp 3.000.000 – Rp 4.000.000 (Raspberry Pi 5, Lensa Polarizer, LED Light, Relay Module, Proximity Sensor, Tower Light).
* **Target Pasar (TAM/SAM):** 400–600 UPI ekspor tersertifikasi HACCP di Indonesia.
* **Proyeksi Payback Period:** **3–6 Bulan** (Berdasarkan estimasi reduksi *reject rate* 15% pada kontainer ekspor bernilai USD 5.000–50.000).

---

*Dokumen Master Context ini menjadi acuan tunggal seluruh tim NusaQC dalam menyelaraskan proposal, repository code, dan video demo.*
