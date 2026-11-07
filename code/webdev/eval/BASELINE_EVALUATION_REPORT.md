# NusaQC — Laporan Evaluasi Baseline & Analisis Kelemahan Sistem AI
**Dokumen:** Rekapitulasi Komprehensif Hasil Automated Test Suite (Fase 1 Baseline)  
**Tanggal Pengujian:** 26 September 2026  
**Infrastruktur Evaluasi:** `webdev/eval/` (ONNX Runtime CPU, Standar SNI 2729:2013)  
**Dataset Evaluasi Penuh:**
- **Model 1 (Freshness):** `models/datasets/mobilenet/val` (380 citra validasi riil: Grade A, B, C lintas 11 hari penyimpanan es)
- **Model 2 (Defect Detector):** `models/datasets/yolo8s/valid` (642 citra validasi riil beranotasi: 720 bounding box cacat fisik)

---

## 1. Executive Summary

Pengujian baseline komprehensif telah dieksekusi menggunakan seluruh data uji validasi riil tanpa sampling artifisial. Pengujian mencakup 6 suite pengujian (*Core Accuracy*, *Optical Robustness*, *Edge Cases*, *Agentic Adjudication*, *Async Stream*, dan *Quantization Profile*).

Hasil pengujian menunjukkan bahwa **Model 1 (MobileNetV3)** memiliki akurasi nominal sempurna pada kondisi ideal, namun sangat rentan terhadap degradasi lingkungan. Sebaliknya, **Model 2 (YOLOv8s FP32)** menunjukkan **tingkat ketidakterdeteksian cacat (False Negative Rate) yang sangat tinggi (46.39%)** dan **latensi inferensi yang terlalu lambat untuk chip Edge (ARM Cortex-A72)**. Temuan-temuan empiris ini menjadi baseline resmi dan justifikasi teknis untuk pengembangan perbaikan di **Fase 2 (Iteration)**.

---

## 2. Tabel Rekapitulasi Skor Baseline (Master Scorecard)

| No | Skrip Test Suite | Dimensi Evaluasi | Metrik Kunci Baseline | Status / Catatan Lapangan |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `test_core_accuracy.py` | Akurasi Freshness (MobileNetV3) & Deteksi Cacat (YOLOv8s) | **Freshness F1: 100.0%**<br>**Defect Recall: 53.61%**<br>**Defect FNR: 46.39%**<br>**Defect Precision: 89.56%**<br>**Defect mAP@50: 50.41%** | 380 citra kesegaran terklasifikasi sempurna.<br>**Kelemahan Kritis:** 334 dari 720 cacat fisik lolos deteksi pada YOLO awal. |
| **2** | `test_optical_robustness.py` | Ketahanan Optik (Wet Glare, Low-Light <50 lux, Blur >15 cm/s) | **Wet Glare FAR: 0.00%**<br>**Low-Light F1: 41.58%**<br>**Blur Recall Retain: 40.00%** | Sangat tahan refleksi kilau lendir/air.<br>**Kelemahan Kritis:** Akurasi anjlok drastis pada cahaya redup dan konveyor cepat. |
| **3** | `test_edge_cases.py` | Kasus Batas (Empty Belt, OOD Anomaly, Oklusi Fisik) | **Phantom Defect: 0.00%**<br>**OOD Conf Drop: 34.92%**<br>**Oklusi >50% Recall: 28.00%** | Sabuk kosong 100% bersih tanpa deteksi palsu.<br>**Kelemahan Kritis:** Oklusi fisik >50% menjadi *blind spot* kamera tunggal. |
| **4** | `test_agentic_adjudication.py` | Resolusi Kasus CONDITIONAL (VLM Review & Fallback) | **Resolusi: 100.0%**<br>**Akurasi vs Pakar: 86.00%**<br>**Fallback Success: 100.0%**<br>**Latensi VLM: 1.19 s** | Kasus ambigu terselesaikan otomatis tanpa stop line; fallback graceful ke operator 100% aman. Terdapat 14% selisih opini dengan pakar QC. |
| **5** | `test_async_stream.py` | Beban Aliran Streaming & Stabilitas RAM | **Throughput: 4.40 FPS**<br>**RAM Growth: 2.59 MB/min**<br>**Frame Drop: 0.00%** | Pipeline asinkronus stabil tanpa *memory leak*, namun throughput CPU host masih di bawah target konveyor (10 FPS). |
| **6** | `test_quantization_performance.py` | Profiling Model FP32 Baseline & Kesiapan Edge | **Ukuran Model: 42.68 MB**<br>**Host CPU Latency: 226.83 ms**<br>**Edge Projection: 1.315 ms (0.76 FPS)**<br>**Status INT8: PENDING FASE 2** | Model FP32 terlalu berat untuk Raspberry Pi 4.<br>**Kelemahan Kritis:** Bottleneck latensi mewajibkan kuantisasi INT8 di Fase 2. |

---

## 3. Rincian Metrik Evaluasi Kuantitatif

### A. Model 1: Freshness Classifier (MobileNetV3-Small FP32)
- **Total Sampel Validasi:** 380 citra
- **Overall Accuracy:** 100.0% | **Macro Precision:** 100.0% | **Macro Recall:** 100.0% | **Macro F1:** 100.0%
- **Rata-rata Latensi Host CPU:** 5.39 ms/frame
- **Breakdown per Grade SNI 2729:2013:**
  - `Grade_A` (Day 1–2): Precision 100.0%, Recall 100.0%, F1 100.0% (Support: 60 citra)
  - `Grade_B` (Day 3–6): Precision 100.0%, Recall 100.0%, F1 100.0% (Support: 141 citra)
  - `Grade_C` (Day 7–11): Precision 100.0%, Recall 100.0%, F1 100.0% (Support: 179 citra)
- **Safety Critical Metric:**
  - Fatal Misclassification (`True Grade C` diprediksi sebagai `Grade A`): **0 kejadian** (*Critical Escape Rate = 0.00%*).

### B. Model 2: Defect Detector (YOLOv8s FP32 Native)
- **Total Citra Validasi:** 642 citra (720 anotasi ground-truth bounding box)
- **Overall Precision:** 89.56%
- **Overall Recall:** 53.61%
- **False Negative Rate (FNR):** **46.39%**
- **False Alarm Rate (FAR):** 10.44%
- **mAP@50 Defect:** 50.41%
- **Rata-rata Latensi Host CPU:** 255.34 ms/frame (~3.9 FPS)
- **Breakdown Deteksi per Kelas Cacat:**
  | Kelas Cacat | True Positives (TP) | False Positives (FP) | False Negatives (FN) | Precision | Catatan Pola Kegagalan |
  | :--- | :---: | :---: | :---: | :---: | :--- |
  | `sisik_sisa` | 51 | 9 | - | 85.0% | Sering terlewat jika sisik tipis/transparan |
  | `warna_abnormal` | 229 | 8 | - | 96.6% | Deteksi stabil pada memar/bercak kemerahan luas |
  | `luka_robekan` | 45 | 8 | - | 84.9% | Terlewat pada robekan sempit (<15 px) |
  | `lendir_berlebih` | 61 | 20 | - | 75.3% | Terbanyak menghasilkan False Alarm akibat pantulan air |

---

## 4. Daftar 6 Kelemahan AI yang Ditemukan (Baseline Failure Modes)

Berdasarkan hasil pengujian empiris di atas, berikut adalah 6 kelemahan utama sistem AI NusaQC saat ini:

### 🔴 Kelemahan 1: Tingginya False Negative Rate Defek (FNR 46.39% / Recall 53.61%)
- **Fakta Evaluasi:** Dari 720 kecacatan fisik nyata pada 642 citra validasi, **334 cacat fisik gagal dideteksi (lolos)** oleh model YOLOv8s.
- **Akar Masalah:**
  1. Model dilatih dengan Loss Cross-Entropy standar tanpa pembobotan kelas minoritas (*class imbalance*).
  2. Bounding box cacat mikro (<20 piksel) kehilangan resolusi fitur spasial pada pooling layer backbone CSPDarknet.
- **Dampak Industri:** Ikan dengan luka robekan atau sisik sisa berisiko lolos ke kontainer ekspor, memicu penalti *quality rejection* di UPI/pasar tujuan.

### 🔴 Kelemahan 2: Bottleneck Latensi & Ukuran Model FP32 pada Edge CPU (0.76 FPS)
- **Fakta Evaluasi:** Bobot YOLOv8s FP32 berukuran **42.68 MB**. Latensi eksekusi di Host CPU mencapai **226.83 ms – 255.34 ms** (~4 FPS), dan pada prosesor Edge ARM Cortex-A72 (Raspberry Pi 4) diproyeksikan mencapai **1.315 ms (0.76 FPS)**.
- **Akar Masalah:** Format FP32 melakukan kalkulasi floating-point 32-bit penuh yang membebani ALU CPU tanpa akselerator NPU/GPU terpisah.
- **Dampak Industri:** Pada kecepatan konveyor standar (15 cm/s), kamera menangkap 10 frame/detik. Throughput 0.76 FPS akan menyebabkan antrean frame *overflow* dan sistem tertinggal hingga 5–10 detik.

### 🔴 Kelemahan 3: Kolaps Akurasi Kesegaran pada Pencahayaan Redup (<50 Lux)
- **Fakta Evaluasi:** Pada skenario redup / tertutup bayangan operator, skor **Macro F1 MobileNetV3 anjlok dari 100.0% menjadi 41.58%** (penurunan performa -58.42%).
- **Akar Masalah:** Distribusi histogram piksel menyempit ke area gelap. Model mengandalkan fitur visual warna insang dan kornea mata yang kehilangan kontras kromatik saat kekurangan lux pencahayaan.
- **Dampak Industri:** Fluktuasi pencahayaan di area sortasi pabrik dapat menyebabkan ikan segar Grade A salah dinilai sebagai Grade B atau C.

### 🟡 Kelemahan 4: Penurunan Drastis Retensi Deteksi Akibat Motion Blur (>15 cm/s)
- **Fakta Evaluasi:** Ketika konveyor bergerak cepat (>15 cm/s) sehingga menimbulkan motion blur linier, *Recall Retain Rate* defek merosot ke **40.00%**, dan Freshness Macro F1 turun ke **67.29%**.
- **Akar Masalah:** Blur linier mengaburkan gradien tepi (*edge boundaries*) luka robekan dan sisik sisa, menyebabkan skor confidence deteksi jatuh di bawah ambang batas operasional (0.55).

### 🟡 Kelemahan 5: Blind Spot Fisik Akibat Oklusi Berat (>50% Tumpukan Ikan)
- **Fakta Evaluasi:** Ketika ikan berada dalam posisi bertumpuk dengan luas permukaan tertutup >50%, *Defect Recall* anjlok menjadi **28.00%** (kehilangan -52.0% sensitivitas).
- **Akar Masalah:** Keterbatasan fisik perspektif kamera tunggal 2D (*single top-down viewpoint*) yang tidak dapat melihat sisi bawah atau area yang tertindih fisik oleh ikan lain.

### 🟡 Kelemahan 6: False Alarm pada Lendir Berlebih & Deviasi Opini AI Agent (14%)
- **Fakta Evaluasi:**
  - Deteksi `lendir_berlebih` menyumbang False Positive tertinggi (20 FP dari 81 prediksi, precision 75.3%) karena pantulan air/es basah terkadang disalahartikan sebagai lendir abnormal.
  - Pada kasus ambigu/borderline yang diserahkan ke VLM Agent (`test_agentic_adjudication.py`), terdapat **14.0% ketidaksesuaian keputusan** antara AI Agent dengan pakar QC manusia.

---

## 5. Rencana Aksi Pengembangan & Iterasi (Fase 2 Roadmap)

Berdasarkan 6 kelemahan empiris di atas, berikut adalah agenda perbaikan terarah untuk Fase 2:

```text
               ┌────────────────────────────────────────────────────────┐
               │         TEMUAN EVALUASI BASELINE (FASE 1)              │
               │  - Defect FNR: 46.39%        - Edge Latency: 1.315 ms  │
               │  - Low-Light F1: 41.58%      - Blur Retain: 40.00%     │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     [ PERBAIKAN MODEL 1 (FRESHNESS) ]             [ PERBAIKAN MODEL 2 (DEFECT) ]
     1. Preprocessing CLAHE Adaptive               1. Retraining dengan Weighted / Focal Loss
        (Kompensasi redup <50 lux)                    (Target Recall >= 75%, FNR <= 25%)
     2. Motion-Blur Training Augmentation          2. Multi-Scale Augmentation (Mosaic + Copy-Paste)
        (Kompensasi blur konveyor cepat)              (Deteksi cacat mikro <20 px)
                  │                                               │
                  └───────────────────────┬───────────────────────┘
                                          │
                                          ▼
                         [ OPTIMASI EDGE INFERENCE ]
                         1. Dynamic INT8 Quantization (quantize_dynamic)
                            - Target Ukuran: 42.7 MB -> ~10.8 MB (-74%)
                            - Target Throughput Edge RPi 4: 0.76 FPS -> > 2.5 FPS
                         2. Adaptive Threshold Calibration
                            - IoU 0.45 & Confidence 0.50 tuning (tekan FAR lendir)
```

| Prioritas | Program Pengembangan | Target Metrik Pasca-Iterasi | Metode Implementasi |
| :-: | :--- | :--- | :--- |
| **P1** | **Retraining YOLOv8s dengan Focal Loss & Weighted BBox** | Defect Recall: **$\ge 75\%$**<br>Defect FNR: **$\le 25\%$** (turun dari 46.39%) | Terapkan loss berbobot pada kelas luka robekan dan sisik sisa; tambahkan augmentasi *Copy-Paste* cacat mikro. |
| **P2** | **Kuantisasi Dinamis INT8 Model Defect** | Ukuran: **$\sim 10.8\text{ MB}$**<br>Host Latency: **$<80\text{ ms}$**<br>Edge Throughput: **$>2.5\text{ FPS}$** | Gunakan `onnxruntime.quantization.quantize_dynamic` dengan tipe `QuantType.QUInt8`. |
| **P3** | **Adaptive CLAHE Preprocessing Pipeline** | Low-Light Macro F1: **$\ge 70\%$** (naik dari 41.58%) | Sisipkan *Contrast Limited Adaptive Histogram Equalization* pada kanal Luminansi (Y) sebelum inferensi MobileNetV3. |
| **P4** | **Synthetic Motion Blur & Glare Augmentation** | Blur Recall Retain: **$\ge 65\%$** (naik dari 40.00%) | Latih ulang model dengan injeksi filter kernel blur linier konveyor (15–20 cm/s). |
| **P5** | **Mitigasi Oklusi Fisik & Integrasi Hardware Diverter** | Penanganan Kasus Oklusi: **100% dialihkan** | Tandai citra dengan oklusi >50% sebagai `CONDITIONAL` dan picu sinyal GPIO actuator untuk memisahkan ikan ke jalur re-orientasi. |
