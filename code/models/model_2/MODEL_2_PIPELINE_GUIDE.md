# Panduan Pipeline Model 2 NusaQC (Surface Contamination & Defect Detector)

Dokumen ini berisi panduan teknis untuk penyiapan dataset, strategi anotasi, serta eksekusi pelatihan model **YOLOv8s ONNX** untuk **Model 2 NusaQC**.

---

## 📂 Prioritasi Dataset Model 2

### 1. Dataset Utama (Active Scope MVP)
- **Roboflow Fish Disease**: Dataset ber-bounding box YOLO mentah (7 kelas: BDA, BGD, BRD, FDS, HF, PD, WTD). 457 gambar.
- **panda992/fish_disease_datasets (HuggingFace)**: Dataset klasifikasi 7 kelas penyakit ikan (2.450 gambar, train: 2.082 + test: 368). Public, tidak perlu token. Sumber: [`panda992/fish_disease_datasets`](https://huggingface.co/datasets/panda992/fish_disease_datasets).
- **Alaa Mahmoud Fish Disease Dataset (Kaggle)**: Dataset klasifikasi infeksi & cacat kulit ikan (305 gambar).

### 2. Dataset Pengembangan Lanjutan (Future Expansion Scope)
- **SalmonScan Dataset**: Dataset infeksi fisik Salmonidae (1.208 gambar) ditangguhkan untuk tahap pengembangan selanjutnya pasca-MVP.

---

## 🛠️ Strategi Anotasi & Pseudo-Labeling Data Klasifikasi (Disepakati)

Dataset panda992 Fish Disease dan Alaa Mahmoud merupakan dataset klasifikasi (*image-level label*) yang belum memiliki *bounding box*. Strategi yang disepakati dan diaktifkan:

### Pipeline Pseudo-Labeling (Seed Model YOLOv8s):
1. **Training Seed Model**: Melatih model Seed YOLOv8s awal pada 457 citra Roboflow Fish Disease yang sudah ber-bounding box (`03_model2_kaggle_pipeline.py`).
2. **Generasi Pseudo-BBox Otomatis**: Menjalankan inferensi Seed Model pada dataset panda992 (2.450 gambar) & Alaa Mahmoud (305 gambar) untuk menghasilkan file anotasi YOLO (`.txt`) (`04_model2_kaggle_pseudolabeling.py`).
3. **Human-in-the-Loop Verification**: Verifikasi dan refinement acak pada 10-15% sampel via Label Studio menggunakan template `02_label_studio_config.xml`.

---

## ⚡ Langkah Eksekusi Pipeline Kaggle

### Tahap 1: Training Seed Model (Notebook 03)
Jalankan `03_model2_kaggle_pipeline.py` di Kaggle GPU:
- **Input**: Roboflow Fish Disease dataset
- **Output**: `best.pt` (seed model), `model2_defect_detector.onnx`

### Tahap 2: Pseudo-Labeling (Notebook 04)
Jalankan `04_model2_kaggle_pseudolabeling.py` di Kaggle GPU:
- **Input 1**: Roboflow Fish Disease dataset
- **Input 2**: Output notebook 03 (`best.pt` seed model)
- **Input 3** (opsional): Alaa Mahmoud Fish Disease dataset
- **Auto-download**: panda992/fish_disease_datasets dari HuggingFace (public)
- **Output**: `nusaqc_extended_pseudo_dataset.zip` (dataset gabungan siap training)

### Tahap 3: Retrain Final (Notebook 03 ulang)
Jalankan `03_model2_kaggle_pipeline.py` lagi dengan dataset extended:
- Ubah `DATASET_ROOT` ke path dataset extended
- **Output**: Model final `best.pt` + `model2_defect_detector.onnx`

### Eksekusi Lokal & Verifikasi
```bash
python models/model_2/01_prepare_model2_dataset.py --setup-dirs
python models/model_2/03_model2_kaggle_pipeline.py
```

Model ONNX final (`nusaqc_model2_defect_detector.onnx`) akan otomatis tersimpan dan siap diintegrasikan ke engine NusaQC.
