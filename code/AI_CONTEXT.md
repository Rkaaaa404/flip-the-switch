# AI Context Map — Project NusaQC (COMPFEST 18 AIC)

File ini dibuat khusus sebagai acuan cepat (**Context Map**) untuk agen AI dan developer dalam menavigasi seluruh dokumen dan arsitektur proyek **NusaQC** (Quality Control & Freshness Assessment berbasis AI).

---

## 📌 Quick Summary Proyek
- **Nama Utama Proyek**: **NusaQC** (Quality Control & Visual Inspection System)
  - *Catatan Naming*: Dokumen awal/ideation kadang menyebut codename internal *NusaCatch*. Nama resmi submisi proposal dan sistem adalah **NusaQC**.
- **Kompetisi**: COMPFEST 18 - Artificial Intelligence Competition (AIC) · Smart Manufacturing Track
- **Fokus Utama**: Sistem inspeksi mutu dan pemilah otomatis berbasis Computer Vision & IoT Conveyor Control untuk rantai pasok industri perikanan ekspor Indonesia (UPI).
- **Arsitektur Dual AI Model (Universal Single-Model Engines)**:
  1. **Model 1 (Kesegaran / Freshness)**: MobileNetV3-Small Float32 ONNX (0.28 MB, 2.44 ms latency on CPU) -> Output Mutu Organoleptik SNI 2729:2013: **Grade A** (Prima), **Grade B** (Segar/Domestik), **Grade C** (Reject/Busuk).
  2. **Model 2 (Deteksi Defek Permukaan / Defect Detector)**: YOLOv8s Float32 ONNX (42.7 MB) -> Deteksi & lokalisasi bounding box untuk **4 Kelas Cacat Standar**:
     - `0: sisik_sisa` (Scale loss / Parasit Argulus, Anchor worm)
     - `1: warna_abnormal` (Bacterial Red Disease, Aeromoniasis, Hemorrhage)
     - `2: luka_robekan` (Skin ulcer, Fin rot, Jamur Saprolegniasis)
     - `3: lendir_berlebih` (White tail disease, Excess clotted mucus)
- **Metode Operasi**: **Synchronous Snapshot Mode** di conveyor sortasi (kamera overhead mengambil 1 snapshot per ikan, diproses instan <150 ms untuk memicu aktuator TowerLight & Conveyor Relay Ejector).

---

## 📂 Peta Struktur Direktori & Rujukan Konteks

### 1. 🌐 `webdev/` (Aplikasi Full-Stack Web & AI Serving)
- `backend/` (FastAPI + ONNX Runtime CPU + SQLite + WebSockets):
  - [`backend/app/ai/inference.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/backend/app/ai/inference.py): Production ONNX Runtime CPU inference engine untuk MobileNetV3 dan YOLOv8s.
  - [`backend/app/ai/preprocessor.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/backend/app/ai/preprocessor.py): Transformasi citra (letterboxing 640x640 dan ImageNet normalization 224x224).
  - [`backend/app/api/v1/inspections.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/backend/app/api/v1/inspections.py): Endpoint `POST /api/v1/inspections/run` pemrosesan snapshot gambar.
  - [`backend/app/api/v1/lots.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/backend/app/api/v1/lots.py): Endpoint riwayat QC, pagination, dan ekspor CSV.
  - [`backend/app/api/v1/dashboard.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/backend/app/api/v1/dashboard.py): Live statistics (Total inspected, pass rate, fail rate, confidence).
  - [`backend/models_weights/`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/backend/models_weights): Bobot model ONNX riil (`mobilenetv3_freshness.onnx` & `nusaqc_model2_defect_detector.onnx`).
- `frontend/` (Next.js 16 + React 19 + Tailwind CSS):
  - [`frontend/app/page.tsx`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/frontend/app/page.tsx): Live Monitoring Dashboard dengan integrasi WebSocket real-time.
  - [`frontend/app/inspection/page.tsx`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/frontend/app/inspection/page.tsx): Halaman Inspeksi dengan upload snapshot, demo generator, dan render dynamic bounding boxes.
  - [`frontend/app/history/page.tsx`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/frontend/app/history/page.tsx): Audit Log riwayat inspeksi, filter mutu, dan ekspor data CSV.
  - [`frontend/app/history/[lotId]/page.tsx`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/webdev/frontend/app/history/%5BlotId%5D/page.tsx): Halaman detail inspeksi per lot dengan visualisasi bounding box defek dan sinyal conveyor.

### 2. 🤖 `models/` (Kode Machine Learning, Pipeline & Dataset)
- `model_1/` (Freshness Engine):
  - [`01_model1_full_pipeline.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_1/01_model1_full_pipeline.py): Pipeline training, anti-leakage augmentasi, evaluasi DaFiF & FFE, serta ONNX export.
  - [`MODEL_1_PIPELINE_GUIDE.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_1/MODEL_1_PIPELINE_GUIDE.md): Panduan lengkap eksekusi dan arsitektur Model 1.
  - [`REKAP_DISKUSI_DAN_REKAYASA_AI_MODEL1.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_1/REKAP_DISKUSI_DAN_REKAYASA_AI_MODEL1.md): Rekap eksperimen dan mitigasi leakage latar belakang lab.
- `model_2/` (Defect Detector):
  - [`01_prepare_model2_dataset.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/01_prepare_model2_dataset.py): Inisialisasi folder, harmonisasi label, & dataset split.
  - [`03_model2_kaggle_pipeline.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/03_model2_kaggle_pipeline.py) & `.ipynb`: Pipeline training YOLOv8s pada Kaggle GPU & ONNX export.
  - [`04_model2_kaggle_pseudolabeling.py`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/04_model2_kaggle_pseudolabeling.py) & `.ipynb`: Pipeline pseudo-labeling otomatis (3.212 citra, 3.509 bounding box).
  - [`ANNOTATION_GUIDE_MODEL2.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/ANNOTATION_GUIDE_MODEL2.md): Panduan visual 4 kelas defek permukaan ikan.
  - [`MODEL_2_PIPELINE_GUIDE.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/MODEL_2_PIPELINE_GUIDE.md): Panduan eksekusi pipeline Model 2.
  - [`REKAP_DISKUSI_DAN_REKAYASA_AI_MODEL2.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/models/model_2/REKAP_DISKUSI_DAN_REKAYASA_AI_MODEL2.md): Rekap rekayasa teknis & eksperimen Model 2.

### 3. 📄 `proposal/` (Dokumen Proposal Hackathon)
- [`FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/proposal/FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md): Proposal Utama Active (v3) dengan data statistik KKP/BPS/FDA & rancangan sistem.
- [`Rencana_Struktur_Proposal.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/proposal/Rencana_Struktur_Proposal.md): Breakdown outline bab proposal.

### 4. 💡 `ideation/` & 📚 `docs/`
- [`docs/md/spesifikasi_dataset_dan_scope_ai.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/docs/md/spesifikasi_dataset_dan_scope_ai.md): Spesifikasi komprehensif dataset, taksonomi label, dan integrasi proposal.
- [`docs/md/dafif.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/docs/md/dafif.md): Ringkasan dataset DaFiF dan pemetaan organoleptik SNI.
- [`ideation/Solidification_Main_Idea.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/ideation/Solidification_Main_Idea.md): Pembekuan ide utama & arsitektur solusi.
