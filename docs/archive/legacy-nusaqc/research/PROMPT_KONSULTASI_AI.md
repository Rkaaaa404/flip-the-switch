# Template Prompt Konsultasi AI (Second Opinion / Reviewer)
### Project: NusaQC — COMPFEST 18 AI Innovation Challenge (AIC)

Dokumen ini berisi panduan dan template prompt siap pakai jika kamu ingin berkonsultasi atau meminta *second opinion* dari LLM/AI lain (seperti ChatGPT, Claude, Gemini, atau Perplexity).

---

## 1. Daftar Dokumen Konteks yang Perlu Diunggah / Dilampirkan

Saat berkonsultasi dengan AI lain, attach/upload berkas-berkas berikut sebagai konteks utama:

| Nama Berkas | Fungsi Sebagai Konteks |
| :--- | :--- |
| **`guidebook.md`** | Aturan main lomba, kriteria penilaian, dan batasan MVP babak penyisihan COMPFEST 18. |
| **`FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md`** | Draft proposal utama produk NusaQC (problem landscape, arsitektur, closed-loop hardware, bisnis). |
| **`spesifikasi_dataset_dan_scope_ai.md`** | Rincian arsitektur dual-engine AI, pemetaan multi-dataset, dan penanganan anotasi. |
| **`Deep feature optimization for enhanced fish freshness assessment.md`** | Jurnal ilmiah rujukan (Elsevier 2026) untuk benchmark metode kesegaran mata ikan. |
| **`past_winners_analysis.md`** | Analisis pola pemenang terdahulu COMPFEST (Setorin, Mechaminds, Tunarasa). |
| **`REKAP_DISKSI_DAN_REKAYASA_AI_MODEL1.md`** | Catatan eksperimen & keputusan rekayasa AI Model 1 (DaFiF, MobileNetV3-Small INT8 ONNX). |

---

## 2. Template Prompt Utama (Siap Copy-Paste)

Gunakan prompt di bawah ini saat memulai percakapan baru dengan AI lain:

```text
Bertindaklah sebagai Senior AI Engineer & Juri Hackathon AI berpengalaman. Saya sedang mengikuti kompetisi AI Innovation Challenge (AIC) COMPFEST 18 dengan tema "AI for the Backbone of the Economy" (Fokus: Smart Manufacturing).

Saya telah melampirkan beberapa berkas konteks utama:
1. `guidebook.md` (Rulebook & Kriteria Penilaian Lomba)
2. `FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md` (Draft Proposal Produk NusaQC)
3. `spesifikasi_dataset_dan_scope_ai.md` (Spesifikasi Dual-Engine AI & Multi-Dataset)
4. `Deep feature optimization for enhanced fish freshness assessment.md` (Jurnal Rujukan Elsevier 2026)
5. `past_winners_analysis.md` (Analisis Pola Pemenang Terdahulu)
6. `REKAP_DISKSI_DAN_REKAYASA_AI_MODEL1.md` (Rekapitulasi Eksperimen AI Model 1)

---

### RINGKASAN PROYEK NUSAQC:
- **Produk:** NusaQC — AI-Powered Visual Quality Control System & Conveyor Inspector untuk Unit Pengolahan Ikan (UPI) ekspor.
- **Dual-Engine AI:**
  1. Model 1 (Freshness Engine): MobileNetV3-Small INT8 ONNX untuk klasifikasi mutu fisik (Grade A/B/C) berdasarkan SNI 2729:2013 menggunakan dataset DaFiF (2.536 foto). Hasil eksperimen test set: Accuracy 99.48%, Macro F1 0.9939.
  2. Model 2 (Defect Detector): YOLOv8n ONNX untuk deteksi cacat fisik visual (5 kelas: sisik_sisa, warna_abnormal, luka_robekan, foreign_object, lendir_berlebih).
- **Closed-Loop Hardware:** AI terhubung langsung ke relay conveyor (STOP/SLOW) + Tower Light + Buzzer saat ikan afkir terdeteksi.
- **Kepatuhan Rulebook MVP:** Mode Synchronous Snapshot (Capture on Trigger), Runnable via `docker compose`, CPU-only inference, SQLite digital traceability.

---

### PERTANYAAN / AREA REVIEW YANG SAYA BUTUHKAN:
1. **Review Kekuatan & Celah Proposal:** Apakah proposal NusaQC v3 sudah memenuhi seluruh kriteria penilaian COMPFEST 18 (bobot Arsitektur 25%, Orisinalitas 20%, MVP 15%, Proposal 15%) dan pola pemenang terdahulu?
2. **Review Rekayasa AI Model 1:** Model 1 kami mencapai F1-Score 0.9939 pada DaFiF dataset 3-class. Bagaimana cara terbaik menyajikan hasil ini di proposal agar tidak terkesan overfit atau terlalu mudah di mata juri? Apakah perlu memasukkan skenario "Freshness Day Estimator (Regresi Hari)" sebagai wacana iterasi?
3. **Saran Peningkatan Teknis & Pitching:** Apakah ada celah teknis/bisnis pada NusaQC yang berpotensi dikritisasi oleh juri, dan bagaimana cara memitigasinya?

Berikan masukan yang objektif, kritis, langsung ke poin, dan solutif berbasis berkas konteks yang saya berikan.
```

---

## 3. Opsi Pertanyaan Spesifik Lanjutan

Jika ingin menanyakan topik spesifik tertentu ke AI lain, kamu bisa menggunakan variasi prompt berikut:

### Opsi A: Review Khusus Alur & Arsitektur AI
> *"Berdasarkan `spesifikasi_dataset_dan_scope_ai.md` dan jurnal Elsevier 2026, berikan tinjauan kritis terhadap arsitektur Dual-Engine AI NusaQC (MobileNetV3-Small INT8 + YOLOv8n ONNX). Apakah pilihan model dan metode pseudo-labeling SAM 2 kami sudah efisien untuk di-deploy di edge device Raspberry Pi 5 CPU?"*

### Opsi B: Review Khusus Dampak Bisnis & Relevansi Tema
> *"Berdasarkan `FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md` dan `guidebook.md`, evaluasi apakah penajaman target pasar ke 400–600 UPI ekspor tersertifikasi HACCP dan analisis ROI yang kami buat sudah cukup realistis untuk mendapatkan nilai maksimal pada kriteria Orisinalitas & Business Value (+3.5%)?"*
