# 🐟 NusaQC — AI-Powered Visual Quality Control System
> **COMPFEST 18 - Artificial Intelligence Competition (AIC)**

NusaQC adalah sistem inspeksi mutu dan pemilah otomatis berbasis Computer Vision yang dirancang untuk menggantikan proses Quality Control (QC) manual di lini sortasi Unit Pengolahan Ikan (UPI) ekspor Indonesia.

Sistem ini memadukan **dua arsitektur AI modular**:
1. **Model 1 (Kesegaran Ikan / Freshness Assessment)**: Deep Feature Extractor (ResNet50 / MobileNetV3) + Classifier untuk klasifikasi grade kesegaran (Grade A / B / C) berdasarkan indikator visual mata dan insang.
2. **Model 2 (Deteksi Defek & Kontaminasi / Defect Detection)**: Fine-tuned YOLOv8 Object Detection dengan pseudo-labeling otomatis (3.200+ citra) untuk mendeteksi cacat fisik visual & kontaminasi permukaan.

---

## 🗂️ Struktur Direktori Project

```text
AIC/
├── 📄 .gitignore                 # Rules pengabaian file Git (dataset & model weights)
├── 📄 AI_CONTEXT.md              # 🧠 Context Map & Rujukan Prompting AI Assistant
├── 📄 README.md                  # 📘 Dokumentasi Repositori
│
├── 📂 proposal/                  # 📝 Proposal resmi & draft kompetisi
│   ├── FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md   (⭐ Proposal Utama Active v3)
│   ├── Rencana_Struktur_Proposal.md                    (Outline & Breakdown Proposal)
│   ├── Draft_Proposal_Inovasi_v1.md                    (Draft Awal v1 - Historical)
│   └── Draft_Proposal_Inovasi_v1.pdf                    (Draft PDF v1 - Historical)
│
├── 📂 ideation/                  # 💡 Perancangan ide, spesifikasi teknis & jobdesk tim
│   ├── Solidification_Main_Idea.md                    (Pembekuan Ide Utama & Arsitektur Solusi)
│   ├── Laporan_Analisis_Bedah_Ide_NusaQC.md            (Bedah Problem Statement & Solusi)
│   ├── Laporan_Evaluasi_Kritis_NusaQC.md             (Kritisasi, Risks & Mitigations)
│   ├── NusaCatch_Specs.md                             (Spesifikasi Fitur System)
│   ├── MASTER_CONTEXT_DAN_REVISI_TIM_NUSAQC.md        (Catatan Revisi & Master Context Tim)
│   ├── Perbaikan_Ide_Rayka.md                         (Catatan Perbaikan Teknis)
│   ├── Rekomendasi_Scope_Spesies_NusaQC.md            (Penetapan Scope Spesies Target)
│   └── Pembagian_Jobdesk.md                           (Jobdesk Anggota Tim)
│
├── 📂 research/                  # 🔍 Benchmarking, guidebook & analisis kompetitor
│   ├── guidebook.md                                   (Guidebook Lomba COMPFEST 18)
│   ├── past_winners_analysis.md                       (Analisis Pemenang Tahun Lalu)
│   ├── Verifikasi_Sitasi_dan_Data_NusaQC.md           (Verifikasi Data & Sitasi)
│   ├── PROMPT_KONSULTASI_AI.md                        (Panduan Prompt Konsultasi)
│   └── 📂 past_winners/                               (Berkas karya pemenang terdahulu)
│
├── 📂 docs/                      # 📚 Paper ilmiah & rujukan teknis
│   ├── 📂 md/                    # Ringkasan paper & spesifikasi dataset
│   │   ├── Deep_feature_optimization_paper.md
│   │   ├── dafif.md
│   │   ├── datasets.md
│   │   └── spesifikasi_dataset_dan_scope_ai.md
│   └── 📂 pdf/                   # File asli paper penelitian (PDF)
│       ├── Deep_feature_optimization_paper.pdf
│       └── dafif.pdf
│
└── 📂 models/                    # 🤖 Pipeline Machine Learning & Datasets
    ├── 📂 model_1/               # Model 1: Freshness Assessment (Eye & Gill)
    │   ├── 01_model1_full_pipeline.py
    │   ├── MODEL_1_PIPELINE_GUIDE.md
    │   └── REKAP_DISKUSI_DAN_REKAYASA_AI_MODEL1.md
    ├── 📂 model_2/               # Model 2: Surface Defect Detection (YOLOv8)
    │   ├── 01_prepare_model2_dataset.py
    │   ├── 02_label_studio_config.xml
    │   ├── 03_model2_kaggle_pipeline.py (.ipynb)
    │   ├── 04_model2_kaggle_pseudolabeling.py (.ipynb)
    │   ├── 05_label_studio_converter.py
    │   ├── ANNOTATION_GUIDE_MODEL2.md
    │   ├── MODEL_2_PIPELINE_GUIDE.md
    │   ├── REKAP_DISKUSI_DAN_REKAYASA_AI_MODEL2.md
    │   ├── label_studio_tasks.json
    │   └── serve_images.py
    └── 📂 datasets/              # 🚫 Git Ignored (Tempat penyimpanan lokal dataset)
        ├── 📂 model-1/           # Local folder untuk dataset DaFiF & FFE
        └── 📂 model-2/           # Local folder untuk dataset defek & pseudo-labeling
```

---

## 🤖 Menggunakan Context dengan AI

Untuk memfasilitasi integrasi dengan AI assistant (seperti Antigravity, ChatGPT, Claude, dll), gunakan file [`AI_CONTEXT.md`](file:///D:/main/Documents/explore/compe/hackhathon/AIC/AI_CONTEXT.md) di direktori utama.

File tersebut memuat pemetaan tautan langsung ke setiap file penting sesuai dengan tugas yang ingin dikerjakan.
