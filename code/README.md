# 🐟 NusaQC — Quality Control & Delivery Traceability System
> **Flip the Switch Hackathon**

NusaQC adalah sistem inspeksi mutu dan pemilah otomatis berbasis Computer Vision yang dirancang untuk mengoptimalkan proses Quality Control (QC) dan rantai keterlacakan digital (*traceability*) di lini sortasi Unit Pengolahan Ikan (UPI) ekspor Indonesia.

Sistem ini memadukan **dua arsitektur AI modular**:
1. **Model 1 (Kesegaran Ikan / Freshness Assessment)**: Deep Feature Extractor (ResNet50 / MobileNetV3) + Classifier untuk klasifikasi grade kesegaran (Grade A / B / C) berdasarkan indikator visual organoleptik SNI 2729:2013.
2. **Model 2 (Deteksi Defek & Kontaminasi / Defect Detection)**: Fine-tuned YOLOv8 Object Detection dengan pseudo-labeling otomatis (3.200+ citra) untuk mendeteksi cacat fisik visual & kontaminasi permukaan.
---

## 🗂️ Struktur Direktori Project

```text
code/
├── 📄 AI_CONTEXT.md              # 🧠 Context Map & Rujukan Navigasi Proyek
├── 📄 README.md                  # 📘 Dokumentasi Repositori
├── 📄 requirements.txt           # Dependensi Python
├── 📄 default_yolo.yaml          # Konfigurasi YOLO default
├── 📄 test_hardware.py           # Script pengujian hardware lokal
├── 📄 test_rpi_remote.py         # Script pengujian Raspberry Pi jarak jauh (SSH)
│
├── 📂 webdev/                    # 🌐 Aplikasi Web & AI Serving
│   ├── 📂 backend/               # FastAPI + ONNX Runtime + SQLite + WebSockets
│   │   ├── 📂 app/               # Logic backend, hardware controller & endpoints
│   │   └── 📂 models_weights/    # Bobot model ONNX riil
│   ├── 📂 frontend/              # Next.js 16 + React 19 + Tailwind CSS
│   └── 📂 eval/                  # Test suite & metrik evaluasi
│
├── 📂 edge/                      # ⚡ Edge runtime & IoT conveyor actuation
│   ├── main.py                   # Entrypoint edge controller
│   ├── inference.py              # Edge inference engine
│   ├── camera.py                 # Industrial camera handler
│   ├── gpio.py                   # GPIO pin controller & relay trigger
│   ├── decision.py               # Sorting decision logic
│   └── telemetry.py              # Telemetry & status reporting
│
├── 📂 models/                    # 🤖 Pipeline Machine Learning & Datasets
│   ├── 📂 model_1/               # Freshness Classification (MobileNetV3)
│   ├── 📂 model_2/               # Surface Defect Detection (YOLOv8)
│   └── 📂 datasets/              # 🚫 Git Ignored (Folder penyimpanan lokal dataset)
│
└── 📂 AI/                        # 🧠 Artefak & pipeline eksperimen AI
    ├── 📂 model-1/               # Eksperimen model kesegaran
    └── 📂 model-2/               # Eksperimen model defek
```

---

## 🤖 Menggunakan Context dengan AI

Untuk memfasilitasi integrasi dengan AI assistant, gunakan file [`AI_CONTEXT.md`](AI_CONTEXT.md) di direktori utama.

File tersebut memuat pemetaan tautan langsung ke setiap file penting sesuai dengan tugas yang ingin dikerjakan.
