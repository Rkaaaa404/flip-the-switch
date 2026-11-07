# NusaQC — AI-Powered Visual Quality Control System
## Dokumen Spesifikasi & Proposal Inovasi
### AIC COMPFEST 18 · 2026 · Smart Manufacturing

---

> **Catatan Internal:** Dokumen ini mengintegrasikan koreksi dari kritisasi individu (Rayka) dengan data riset terbaru. Setiap klaim didukung sumber yang dapat diverifikasi. Angka-angka dari sumber KKP/BPS/FDA digunakan sesuai ketentuan: data paling lama tahun 2022.

---

## DAFTAR ISI

1. [Executive Summary & Business Value](#1-executive-summary--business-value)
2. [Problem Landscape: Data & Root Cause Analysis](#2-problem-landscape-data--root-cause-analysis)
3. [Gap Analysis & Tujuan Utama Solusi](#3-gap-analysis--tujuan-utama-solusi)
4. [Relevansi Tema: Smart Manufacturing (Alignment AIC)](#4-relevansi-tema-smart-manufacturing-alignment-aic)
5. [System Architecture: End-to-End Flow](#5-system-architecture-end-to-end-flow)
6. [Hardware & IoT Conveyor Control Logic](#6-hardware--iot-conveyor-control-logic)
7. [AI Model Specification & Dataset Strategy](#7-ai-model-specification--dataset-strategy)
8. [Metodologi Perancangan Perangkat Lunak](#8-metodologi-perancangan-perangkat-lunak)
9. [COMPFEST 18 MVP Compliance Matrix](#9-compfest-18-mvp-compliance-matrix)
10. [Business Model & Governance](#10-business-model--governance)
11. [Risk Register & Mitigasi](#11-risk-register--mitigasi)
12. [Deliverables Checklist Submisi](#12-deliverables-checklist-submisi)

---

## 1. Executive Summary & Business Value

### 1.1 Ringkasan Solusi

**NusaQC** adalah sistem inspeksi mutu dan pemilah otomatis berbasis Computer Vision yang dirancang untuk menggantikan proses Quality Control (QC) manual di lini sortasi Unit Pengolahan Ikan (UPI) ekspor Indonesia.

**Visi Utama Produk (Production Vision):**
NusaQC dirancang sebagai **Sistem Pemilah Otomatis Kontinyu di Atas Conveyor Belt** (*Continuous Automated Conveyor Inspection*) — kamera industri memindai setiap ikan secara terus-menerus seiring conveyor bergerak, tanpa interupsi alur produksi.

**Strategi MVP Babak Penyisihan COMPFEST 18:**
Pada fase penyisihan ini, sistem diimplementasikan dengan skema **Synchronous Snapshot Inspection** (*Capture on Trigger*) — memproses satu foto per ikan per trigger sensor — sebagai *trade-off* strategis untuk memenuhi batasan rulebook COMPFEST 18 (sistem sinkron, tanpa background streaming, dapat dijalankan via `docker-compose up` di CPU biasa). Transisi dari mode snapshot ke mode continuous adalah target eksplisit **Babak Final Hackathon 10 Jam**.

Sistem berjalan dengan menangkap satu frame foto ikan saat melewati titik inspeksi (*Capture on Trigger*), lalu menjalankan dua model AI secara berurutan:

1. **Model Kesegaran:** Mengklasifikasikan kondisi fisik ikan ke dalam tiga grade (A / B / C) berdasarkan indikator visual mata dan insang.
2. **Model Deteksi Defek:** Mendeteksi kontaminasi dan cacat fisik visual (sisik sisa, perubahan warna abnormal, foreign object, lendir berlebih) dengan bounding box.

Hasil inspeksi dikirimkan secara real-time ke:
- **Frontend Dashboard** (React.js) untuk monitoring operator
- **Stack Light & Buzzer** sebagai sinyal visual/audio peringatan
- **Relay ke Motor Conveyor** untuk menghentikan/memperlambat lini saat ikan cacat terdeteksi
- **SQLite Database** untuk pencatatan digital lot QC (*digital traceability*)

### 1.2 Positioning Statement

> *"NusaQC adalah sistem inspeksi mutu dan pemilah otomatis berbasis Computer Vision yang visinya menjadi Continuous Automated Conveyor Inspector di lini sortasi UPI — mendeteksi kesegaran dan kontaminasi fisik ikan secara objektif, konsisten, dan terdokumentasi digital sesuai standar ekspor internasional (FDA/RASFF/EU). Untuk Babak Penyisihan COMPFEST 18, sistem dihadirkan dalam mode MVP sinkron (Snapshot per Trigger) yang sepenuhnya mematuhi rulebook, dengan arsitektur modular yang siap ditingkatkan ke mode continuous pada Babak Final Hackathon."*

### 1.3 Nilai Bisnis (Business Value)

| Dimensi | Kondisi Saat Ini | Dengan NusaQC | Delta |
|---------|-----------------|---------------|-------|
| **Kecepatan inspeksi per ikan** | 5–10 detik (manual) | ≤ 1.5 detik (AI + trigger) | **~5x lebih cepat** |
| **Konsistensi penilaian** | Subjektif, bergantung kondisi fisik operator | Objektif, parameter tetap | **Error rate turun signifikan** |
| **Dokumentasi QC** | Paper-based, sulit diaudit | Log digital SQLite dengan timestamp & lot ID | **Audit-ready** |
| **Harga sistem (CAPEX)** | QC visual manual: Rp 0 CAPEX, tapi biaya tenaga tinggi | RPi 5 + kamera + actuator: ≈ Rp 3–4 juta per titik inspeksi | **Terjangkau untuk UPI menengah** |
| **Potensi penghematan per UPI** | Risiko penolakan ekspor: kerugian USD 5.000–50.000+ per kontainer | Estimasi reduksi reject rate ≥15% | **ROI < 6 bulan** |

### 1.4 Target Penerima Manfaat (Dipersempit dari Kritisasi)

Berdasarkan kritisasi, scope penerima manfaat **WAJIB dipersempit**. Target primer bukan seluruh 3.365 UPI nasional, melainkan:

**Target Utama:**
- **UPI berskala menengah-besar** yang sudah memiliki sertifikasi HACCP dan memasok pasar ekspor (AS, Jepang, EU)
- **Fokus komoditas:** Tuna/Cakalang (*Scombridae*), Tilapia (*Cichlidae*), Salmon (*Salmonidae*)

**Jumlah Target Terverifikasi:**
- Per November 2022, BKIPM KKP mencatat **2.406 UPI telah memiliki sertifikat HACCP** *(Sumber: KKP, Desember 2022)*
- Dari 127.787 frekuensi ekspor pada 2022, terdapat **8 kasus penolakan resmi (0,006%)** — namun angka ini mencakup penolakan di titik masuk negara tujuan, bukan cacat yang dibuang saat pra-ekspor *(Sumber: BKIPM KKP, 2022)*
- UPI yang aktif mengekspor ke China saja berjumlah **386 UPI (2023)** dan **522 UPI (2024)** *(Sumber: ANTARA/KKP, 2025)*

**Estimasi TAM yang Realistis:**
- UPI menengah-besar aktif ekspor: **400–600 UPI** (sebagai baseline konservatif dari data di atas)
- Setiap UPI memiliki 1–3 lini sortasi
- Potensi deployment awal: **1.000–1.800 titik inspeksi**

> ⚠️ **Koreksi Kritis:** Angka "3.365 UPI tersertifikasi" dalam dokumen lama tidak tepat dijadikan TAM karena mayoritas adalah UPI UMKM skala kecil yang tidak memiliki conveyor belt industrial. Klaim ini harus diperbaiki dalam proposal final.

---

## 2. Problem Landscape: Data & Root Cause Analysis

### 2.1 Skala Masalah Ekonomi: Ekspor Perikanan Indonesia

Indonesia adalah kekuatan ekspor perikanan global. Data 2022 menunjukkan:

- **Nilai ekspor perikanan Jan–Nov 2022:** USD 5,71 miliar (volume 1,11 juta ton), tumbuh **10,66%** dari periode yang sama 2021 *(Sumber: BPS/KKP, Jan 2023)*
- **Target 2022 yang tidak tercapai:** USD 7,13 miliar — artinya ada selisih USD 1,42 miliar yang gagal terealisasi
- **Komoditas utama:** Udang (28,1%), Tuna-Cakalang-Tongkol (12,4%), Cumi-Sotong-Gurita (10,1%) *(Sumber: KKP, 2022)*
- **Negara tujuan utama:** Amerika Serikat (47,5%), Tiongkok, Jepang, ASEAN, Uni Eropa

Industri sebesar ini sangat rentan terhadap satu masalah struktural: **kegagalan kontrol mutu di level UPI.**

### 2.2 Data Penolakan Ekspor: FDA, RASFF, dan KKP

#### Temuan Studi Akademis (Sumber Primer)

Penelitian peer-reviewed dari Jurnal *Industria* (Desember 2022), yang menganalisis data FDA-OASIS dan RASFF periode 2010–2020, menemukan:

> *"Dalam periode yang diamati, terdapat 2.318 kasus penolakan di Amerika Serikat dan 79 di Eropa. Berdasarkan analisis Pareto, faktor utama yang menyumbang lebih dari 80% penolakan di AS adalah **filthy** (kontaminasi fisik) dan **Salmonella**."*
> *(Nurkhasanah et al., 2022 — Industria: Jurnal Teknologi dan Manajemen Agroindustri, Vol. 11, No. 2, pp. 165-176)*

**Breakdown Faktor Penolakan di Pasar AS (2010–2020):**

```
Faktor Utama (>80% Pareto):
├── Filthy (Kontaminasi Fisik)    ─── DAPAT DIDETEKSI OLEH COMPUTER VISION ✅
│    └── Sisik sisa, kotoran, parasit luar, benda asing
└── Salmonella (Bakteri)          ─── TIDAK DAPAT DIDETEKSI VISUAL ❌
     └── [TELAH DIHAPUS DARI SCOPE NUSAQC]

Faktor Pasar EU:
├── Merkuri (Logam Berat)         ─── Butuh uji laboratorium ❌
├── Kontrol Temperatur Buruk      ─── Sensor suhu IoT, di luar scope MVP ⚠️
├── Salmonella                    ─── Tidak bisa CV ❌
├── Histamin                      ─── Butuh uji kimia ❌
└── Kadmium                       ─── Butuh uji laboratorium ❌
```

#### Kasus FDA Import Alert 16-18 (Data Aktual)

FDA memberlakukan *Detention Without Physical Examination (DWPE)* untuk udang Indonesia dari beberapa produsen karena ditemukan:
- **Filthy** (kontaminasi fisik yang terlihat)
- **Salmonella** (hasil uji laboratorium)

*(Sumber: FDA OASIS Import Alert 16-18; Southern Shrimp Alliance, 2023)*

**Interpretasi untuk NusaQC:**
- Komponen *filthy* (kontaminasi fisik) adalah **domain valid untuk Computer Vision**
- Komponen *Salmonella* adalah kontaminasi mikrobiologis yang **wajib diuji laboratorium** — bukan domain CV
- NusaQC secara eksplisit mengatasi **komponen filthy** dan **indikator visual penurunan kualitas**

### 2.3 Root Cause Analysis: Mengapa Masalah Filthy Persisten?

Berdasarkan *fishbone diagram* dari Nurkhasanah et al. (2022), faktor penyebab utama kasus penolakan *filthy* adalah:

```
AKIBAT: Produk Ikan Indonesia Ditolak FDA/RASFF karena "Filthy"
│
├─[MANUSIA]
│   ├── QC manual subjektif → hasil berbeda antar operator
│   ├── Kelelahan operator di shift siang/malam → error rate naik
│   └── Kurangnya koordinasi antara pemasok bahan baku & UPI
│
├─[METODE]
│   ├── Inspeksi visual berbasis pengalaman (tidak terstandar)
│   ├── Pencatatan paper-based → tidak ada historical QC data
│   └── Tidak ada mekanisme reject otomatis di lini sortasi
│
├─[MESIN/ALAT]
│   ├── Tidak ada sistem deteksi defek otomatis di conveyor
│   └── Pencahayaan lini sortasi tidak konsisten
│
└─[LINGKUNGAN]
    ├── Kondisi basah/licin di lini pengolahan
    └── Tekanan throughput tinggi → terburu-buru inspeksi
```

**NusaQC menyasar langsung 3 dari 4 kategori root cause di atas.**

### 2.4 Validasi Teknis: Apa yang Bisa dan Tidak Bisa Dideteksi CV

> ⚠️ **KOREKSI KRITIS (Dari Kritisasi Rayka):** Klaim sebelumnya bahwa sistem bisa "mendeteksi Salmonella" adalah **kesalahan ilmiah fatal**. Salmonella adalah bakteri berukuran 0,7–1,5 mikrometer. Tidak ada kamera optis biasa yang mampu memvisualisasikannya. Klaim ini **harus dihapus sepenuhnya** dan **tidak boleh muncul dalam bentuk apapun** di proposal, video, maupun demo.

| Indikator | Dapat Dideteksi CV? | Metode | Masuk Scope NusaQC? |
|-----------|---------------------|--------|---------------------|
| Sisik sisa / kulit copot | ✅ Ya | Object Detection | ✅ Ya |
| Perubahan warna abnormal (kemerahan, kehijauan) | ✅ Ya | Color Feature + CNN | ✅ Ya |
| Lendir berlebih (tekstur permukaan) | ✅ Ya (terbatas) | Texture Analysis | ✅ Ya |
| Luka / robekan daging | ✅ Ya | Object Detection | ✅ Ya |
| Parasit luar (kutu ikan) | ✅ Ya | Object Detection | ✅ Ya |
| Foreign object (plastik, tulang, dll.) | ✅ Ya | Object Detection | ✅ Ya |
| Kondisi mata (jernih/segar vs. cekung/keruh) | ✅ Ya | ROI Classification | ✅ Ya |
| Kondisi insang (merah cerah vs. coklat/abu) | ✅ Ya | ROI Classification | ✅ Ya |
| **Salmonella / bakteri** | ❌ Tidak bisa CV | Perlu PCR/kultur lab | ❌ **HAPUS** |
| Histamin (keracunan scombroid) | ❌ Tidak bisa CV | Perlu uji kimia | ❌ Di luar scope |
| Merkuri / logam berat | ❌ Tidak bisa CV | Perlu uji laboratorium | ❌ Di luar scope |

---

## 3. Gap Analysis & Tujuan Utama Solusi

### 3.1 Current State vs. Target State

```
CURRENT STATE (Kondisi QC Manual Saat Ini)
──────────────────────────────────────────
• Metode    : Inspeksi visual oleh 2-3 orang operator per lini
• Kecepatan : ~5–10 detik/ikan (bergantung volume & kondisi operator)
• Akurasi   : Tidak konsisten — "segar menurut siapa?" berbeda antar orang
• Dokumentasi: Kertas (tally sheet manual), tidak ada timestamp digital
• Feedback  : Ikan reject dibuang secara manual SETELAH terlihat oleh operator
• Traceability: Tidak ada → hambatan audit ekspor FDA/RASFF
• Biaya SDM : 2–3 operator/lini × Rp 3,5–4 jt/bulan = ~Rp 7–12 jt/lini/bulan

INTERMEDIATE STATE (NusaQC MVP — Babak Penyisihan COMPFEST 18)
───────────────────────────────────────────────────────────────
• Metode    : Synchronous Snapshot Inspection (1 foto per trigger)
              → Kepatuhan rulebook: sinkron, tanpa background streaming
• Kecepatan : ≤ 1.500 ms end-to-end per ikan per trigger
• Akurasi   : Parameter tetap, tidak bergantung kondisi manusia
• Dokumentasi: SQLite log digital (lot ID, timestamp, grade, defect label, gambar)
• Feedback  : Relay signal → Conveyor STOP/SLOW otomatis + Tower Light + Buzzer
• Traceability: Digital, exportable, audit-ready
• Biaya CAPEX: ~Rp 3–4 juta per titik inspeksi (hardware)

TARGET STATE (NusaQC Production Vision — Pabrik Nyata)
───────────────────────────────────────────────────────
• Metode    : Continuous Automated Conveyor Inspection
              → Kamera memindai ikan terus-menerus seiring conveyor berjalan
              → Frame rate disesuaikan dengan kecepatan conveyor industri
• Kecepatan : Inspeksi paralel — throughput mengikuti laju conveyor (target ≥ 100 ikan/menit)
• Integrasi : Stream video masuk → queue inference → hasil real-time ke aktuator
• Roadmap   : Dicapai pada Babak Final Hackathon (26 September 2026, 10 jam luring)
              melalui implementasi async inference + pipeline buffering
```

**Peta Jalan Menuju Continuous Automated Inspection:**

```
FASE 1 (Penyisihan — Snapshot MVP)
   Capture on Trigger (1 foto/ikan/trigger)
   └── Sinkron, lokal, CPU biasa, docker-compose up
         │
         │  [Babak Final Hackathon — 10 Jam Luring, Fasilkom UI]
         ▼
FASE 2 (Final — Continuous Mode)
   Continuous Frame Capture + Async Inference Queue
   └── Frame rate → Queue → Parallel ONNX inference workers
   └── Throughput: mengikuti kecepatan conveyor industri
         │
         ▼
FASE 3 (Production — Enterprise Scale)
   Multi-camera, distributed inference, cloud dashboard
   └── Deployment di UPI ekspor aktif
```

### 3.2 Gap yang Dijembatani NusaQC

**Gap 1: Subjektivitas → Objektivitas**
Inspeksi berbasis persepsi manusia diganti dengan parameter fixed (model weights frozen).

**Gap 2: Human-in-the-Loop → Closed-Loop Automation**
Kritisasi Rayka menyebutkan bahwa jika output AI hanya tampil di layar, operator tetap bisa mengabaikannya. NusaQC menjembatani gap ini dengan **aktuasi langsung**: sinyal elektronik ke relay → motor conveyor berhenti. Ini menghilangkan ketergantungan pada perhatian operator untuk tindakan reject.

**Gap 3: Paper-based → Digital Traceability**
Setiap lot inspeksi dilog ke SQLite dengan struktur: `lot_id`, `timestamp`, `fish_family`, `grade`, `defect_labels`, `confidence_score`, `image_path`. Data ini exportable ke CSV/PDF untuk keperluan audit sertifikasi ekspor.

**Gap 4: Reaktif → Preventif**
Dengan adanya historical QC data per lot, supervisor UPI dapat mengidentifikasi pola: misalnya batch bahan baku dari pemasok tertentu secara konsisten menghasilkan Grade C. Ini memungkinkan tindakan preventif ke upstream supply chain.

### 3.3 KPI & Metrik Keberhasilan

| KPI | Baseline (Manual) | Target MVP Penyisihan | Target Production Vision |
|-----|------------------|-----------------------|--------------------------|
| Throughput inspeksi | ~360–720 ikan/jam | ≥ 2.400 ikan/jam (snapshot) | Mengikuti kecepatan conveyor industri |
| False Negative Rate (ikan cacat lolos) | ~15–25% (estimasi industri) | ≤ 8% | ≤ 5% |
| Waktu per inspeksi | 5–10 detik | ≤ 1,5 detik | Real-time (parallel queue) |
| Lot terdokumentasi digital | 0% | 100% | 100% |
| Recall per lot tersedia dalam 5 menit | Tidak memungkinkan | Ya (SQLite query) | Ya |
| Mode operasi | Manual | Snapshot per trigger | Continuous stream |

---

## 4. Relevansi Tema: Smart Manufacturing (Alignment AIC)

### 4.1 Mengapa NusaQC adalah Smart Manufacturing, Bukan Sekadar "Smart Inspection"

**Kritisasi Rayka** menyebutkan bahwa sistem sebelumnya hanya bersifat "Smart Inspection" karena output AI tidak memberikan umpan balik ke mesin produksi. Ini adalah kelemahan yang **telah diperbaiki** dalam versi revisi.

**Definisi Smart Manufacturing (sesuai tema AIC COMPFEST 18):**
> *"Penerapan AI di proses pengolahan dan operasi pabrik"* — termasuk kendali lini produksi secara otomatis berdasarkan data sensor/AI.

**Closed-Loop Control Architecture NusaQC:**

```
[KAMERA INDUSTRI]
      │ Trigger dari Proximity Sensor
      ▼
[INFERENCE ENGINE: FastAPI + ONNX]
      │ Keputusan: PASS / FAIL
      ├─────────────────────────────────────┐
      │                                     │
      ▼                                     ▼
[DASHBOARD UI]                    [GPIO / RELAY CONTROLLER]
(Monitoring operator)              │
                                   ├── Tower Light MERAH → STOP
                                   ├── Buzzer PERINGATAN
                                   └── Relay → Motor Conveyor STOP/SLOW
```

Dengan adanya **Closed-Loop Control** (AI output → sinyal fisik ke mesin), NusaQC memenuhi definisi Smart Manufacturing yang sesungguhnya: sistem AI tidak hanya memantau, tetapi **mengendalikan** operasi pabrik secara otomatis.

### 4.2 Mapping Komponen NusaQC ke Kriteria Smart Manufacturing

| Komponen Smart Manufacturing | Implementasi di NusaQC | Status |
|------------------------------|----------------------|--------|
| Sensor otomatis | Proximity sensor + kamera industri | ✅ Ada |
| AI inference real-time | ONNX Runtime CPU, Snapshot per Trigger (MVP) | ✅ Ada |
| Aktuasi otomatis | Relay → motor conveyor STOP/SLOW | ✅ Ada |
| Human-Machine Interface | React.js Dashboard + Tower Light + Buzzer | ✅ Ada |
| Data logging digital | SQLite (lot ID, timestamp, grade, gambar) | ✅ Ada |
| Mock Hardware Mode | `ENABLE_MOCK_HARDWARE=true` di FastAPI | ✅ Ada |
| **Roadmap Continuous Mode** | **Fase 2: async inference queue di Final Hackathon** | 🗺️ Planned |

---

## 5. System Architecture: End-to-End Flow

### 5.1 Diagram Arsitektur Sistem

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    NUSAQC SYSTEM ARCHITECTURE                         ║
║              (MVP Mode: Synchronous Snapshot Inspection)              ║
╚═══════════════════════════════════════════════════════════════════════╝

  LAYER FISIK (Hardware)              LAYER APLIKASI              LAYER UI
  ─────────────────────               ──────────────              ────────
  
  [ CONVEYOR BELT ]
        │
        │ Ikan melewati titik
        │ inspeksi
        ▼
  [ PROXIMITY SENSOR ]  ──trigger──▶  [ FastAPI Backend ]
        │                             │ (Python 3.11+)
        │                             │
  [ KAMERA ≥5MP ]  ──single frame──▶  │  ┌─ PRE-PROCESSING ─────────┐
        │              (JPEG/PNG)     │  │ Resize → 640×640          │
        │                             │  │ Normalize (0–1)           │
  [ LED RING LIGHT ]                  │  │ Fish ROI Localization     │
  (pencahayaan merata)                │  └──────────────────────────┘
  [ POLARIZING FILTER ]                         │
  (anti-glare ikan basah)                       ▼
                                      │  ┌─ MODEL 1: FRESHNESS ──────┐
                                      │  │ MobileNetV3-Small.onnx    │
                                      │  │ Input: ROI mata/insang    │
                                      │  │ 224×224 px               │
                                      │  │ Output: Grade A/B/C      │
                                      │  │         + Confidence Score│
                                      │  └──────────────────────────┘
                                      │         │
                                      │         ▼
                                      │  ┌─ MODEL 2: DEFECT ─────────┐
                                      │  │ YOLOv8n.onnx             │
                                      │  │ Input: Full frame 640×640 │
                                      │  │ Output: Bounding Box +    │
                                      │  │         Label + Conf      │
                                      │  │         PASS / FAIL       │
                                      │  └──────────────────────────┘
                                      │         │
                                      │         ▼
                                      │  ┌─ DECISION ENGINE ─────────┐
                                      │  │ Grade A + PASS → GREEN    │
                                      │  │ Grade B + PASS → YELLOW   │
                                      │  │ Grade C OR FAIL → RED     │
                                      │  └──────────────────────────┘
                                      │         │
                          ┌───────────┼─────────┤
                          │           │         │
                          ▼           ▼         ▼
                  [ SQLite DB ]  [ GPIO / ]  [ WebSocket ]
                  Lot logging    [ RELAY  ]  Event Push
                  Traceability        │            │
                                      │            ▼
                          ┌───────────┘    [ React.js Dashboard ]
                          │                ─────────────────────
                          ├──▶ Tower Light MERAH/HIJAU    • Live feed
                          ├──▶ Buzzer ON/OFF              • Grade display
                          └──▶ Motor Conveyor STOP/SLOW   • Lot history
                                                          • Export CSV
```

### 5.2 Strategi Eksekusi MVP Babak Penyisihan & Kepatuhan Rulebook COMPFEST

> **Catatan Penting untuk Juri:** Sub-bab ini menjelaskan *mengapa* sistem MVP menggunakan skema Snapshot, bukan karena keterbatasan visi produk, melainkan sebagai keputusan arsitektur yang disengaja untuk mematuhi rulebook penyisihan COMPFEST 18.

#### Kontras: Production Vision vs. COMPFEST 18 MVP Scope

```
┌─────────────────────────────────────────────────────────────────────┐
│              PRODUCTION VISION (Pabrik Nyata)                        │
│         Continuous Automated Conveyor Inspection                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [ CONVEYOR BERGERAK ] ──────────────────────────────────────────▶  │
│       🐟  🐟  🐟  🐟  🐟  🐟  (ikan bergerak kontinu)               │
│                                                                       │
│  Kamera merekam video stream secara terus-menerus                    │
│  Frame dikirim ke inference queue (async/non-blocking)               │
│  Multiple inference workers berjalan paralel                          │
│  Output real-time → aktuator tanpa interrupt conveyor                │
│  Throughput: mengikuti kecepatan conveyor industri                   │
│                                                                       │
│  Tech: Async FastAPI + inference worker pool + message queue         │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              ║
                              ║  [Alasan Tidak Diimplementasikan
                              ║   di Babak Penyisihan]
                              ║  • Rulebook melarang background jobs
                              ║  • Sistem wajib bersifat sinkron
                              ║  • Harus bisa dijalankan di CPU biasa
                              ║    via docker-compose up
                              ║  • Juri perlu mereproduksi lokal
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│         COMPFEST 18 MVP SCOPE (Babak Penyisihan)                     │
│         Synchronous Snapshot Inspection (Capture on Trigger)         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. Proximity sensor deteksi ikan → trigger sinyal                   │
│  2. Kamera ambil 1 foto (single frame JPEG, ~100ms)                  │
│  3. Foto dikirim ke FastAPI (synchronous request)                    │
│  4. Inference Model 1 + Model 2 berjalan berurutan                   │
│  5. Hasil dikirim ke relay, dashboard, SQLite (<50ms post-inference) │
│  6. Sistem siap untuk ikan berikutnya                                │
│                                                                       │
│  Kepatuhan Rulebook:                                                  │
│  ✅ Sinkron (tidak ada async background streaming)                   │
│  ✅ Tidak ada background jobs atau automated data logging pipeline    │
│  ✅ Berjalan di CPU biasa (ONNX Runtime, tanpa GPU)                  │
│  ✅ docker-compose up → langsung bisa didemonstrasikan               │
│  ✅ Reproducible oleh juri secara lokal                              │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              ║
                              ║  [Babak Final Hackathon — 10 Jam Luring]
                              ║  26 September 2026, Fasilkom UI
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│              TARGET UPGRADE DI FINAL HACKATHON                       │
│         Snapshot MVP → Continuous Automated Mode                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Implementasi yang akan dikerjakan dalam 10 jam:                     │
│  • Async FastAPI endpoint untuk menerima video stream               │
│  • Inference worker pool (thread/process pool)                       │
│  • Frame buffer queue untuk decoupling capture & inference           │
│  • Dynamic throughput tuning sesuai kecepatan conveyor               │
│                                                                       │
│  Arsitektur MVP saat ini dirancang modular agar upgrade ini          │
│  tidak memerlukan perombakan total — hanya penambahan layer          │
│  async di atas inference engine yang sudah ada.                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Alur Snapshot Inspection (Detail):**

```
Alur Capture on Trigger (MVP Penyisihan):
──────────────────────────────────────────
1. Proximity sensor mendeteksi ikan melewati titik inspeksi
2. Sinyal trigger dikirim ke kamera (GPIO HIGH → Camera Trigger)
3. Kamera mengambil 1 foto (single frame JPEG, ~100ms)
4. Foto dikirim ke FastAPI via lokal API call (synchronous)
5. Inference Model 1 + Model 2 berjalan sekuensial
6. Hasil dikirim ke relay, dashboard, SQLite (<50ms setelah inference)
7. Sistem siap untuk ikan berikutnya
```

**Keuntungan Arsitektur Snapshot untuk MVP:**
- CPU tidak terbebani frame yang tidak perlu
- Throughput terkontrol oleh jarak antar ikan di conveyor
- **Adjustable conveyor gap** menjadi parameter konfigurasi sistem
- Mudah direproduksi juri tanpa hardware khusus

### 5.3 Tech Stack

| Komponen | Teknologi | Alasan Pemilihan |
|----------|-----------|------------------|
| Backend API | FastAPI (Python 3.11) | Async-capable, performant, mudah di-deploy via Docker; siap di-upgrade ke async mode di Final |
| Inference Engine | ONNX Runtime (CPU) | Platform-agnostic, tidak butuh GPU, mendukung RPi5 |
| Database | SQLite | Zero-config, lokal, audit-ready, tidak perlu server DB |
| Frontend | React.js + Vite | Ringan, komponen WebSocket native |
| Hardware GPIO | RPi.GPIO (Python) | Direct GPIO control untuk relay & actuator |
| Container | Docker + docker-compose | Reproducible setup sesuai rulebook COMPFEST |
| Mock Mode | Environment variable `ENABLE_MOCK_HARDWARE=true` | Jury demo tanpa hardware fisik |

---

## 6. Hardware & IoT Conveyor Control Logic

### 6.1 Bill of Materials (BOM)

| Komponen | Spesifikasi | Estimasi Harga | Fungsi |
|----------|-------------|---------------|--------|
| Single Board Computer | Raspberry Pi 5 (8GB RAM) | ~Rp 1.200.000 | Inference + GPIO control |
| Kamera Industri | USB Webcam ≥5MP + lensa fixed | ~Rp 300.000–500.000 | Capture frame per trigger |
| LED Ring Light | 5500K (Cool White), 15–20cm diameter | ~Rp 150.000 | Pencahayaan merata |
| **Polarizing Filter** | Linear Polarizer 55mm/52mm | ~Rp 80.000 | **Mengurangi glare/refleksi permukaan ikan basah** *(solusi koreksi dari kritisasi)* |
| Proximity Sensor | IR Photoelectric Sensor (NPN) | ~Rp 50.000 | Deteksi ikan melewati titik |
| Stack/Tower Light | 3 warna (merah/kuning/hijau), 24V DC | ~Rp 200.000 | Indikator visual status inspeksi |
| Buzzer Industri | 85dB, 12V DC | ~Rp 50.000 | Peringatan audio saat reject |
| Relay Module | 4-channel 5V relay, 10A | ~Rp 50.000 | Switch motor conveyor |
| Conveyor Motor Controller | Variable Speed Drive (VSD) 220V | ~Rp 300.000–500.000 | Kontrol kecepatan/stop motor |
| **Total Estimasi** | | **~Rp 2.4–3.0 juta** | |

### 6.2 Solusi Masalah Glare pada Ikan Basah

**Kritisasi Rayka** menyebutkan bahwa ikan basah sangat reflektif. LED Ring Light dapat memantulkan cahaya ke kamera dan menghasilkan *False Positive* (kilau sisik dideteksi sebagai "perubahan warna abnormal").

**Solusi yang diimplementasikan:**

```
Tanpa Filter:          Dengan Polarizing Filter:
┌─────────────┐        ┌─────────────┐
│  LED LIGHT  │        │  LED LIGHT  │
│      ↓      │        │      ↓      │
│  [GLARE] ←→ │        │  [FILTER] ↓ │
│  Ikan basah │        │  Cahaya ↓   │
│      ↓      │        │  Ikan basah │
│  Kamera     │        │      ↓      │
│  [Glare!]   │        │  Kamera     │
└─────────────┘        │  [Bersih]   │
                       └─────────────┘
```

Linear Polarizing Filter dipasang di depan lensa kamera. Cahaya pantul (terpolarisasi) dari permukaan ikan basah diblokir, menghasilkan gambar dengan kontras yang lebih natural.

### 6.3 Logika Kontrol Conveyor

```python
# Pseudocode Conveyor Control Logic (FastAPI Backend)
# File: app/hardware/conveyor_controller.py

DECISION_THRESHOLD = {
    "GRADE_A_PASS": "GREEN",     # Tower Light Hijau, Buzzer OFF, Conveyor NORMAL
    "GRADE_B_PASS": "YELLOW",    # Tower Light Kuning, Buzzer SHORT_BEEP, Conveyor NORMAL
    "GRADE_C_OR_FAIL": "RED",    # Tower Light Merah, Buzzer CONTINUOUS, Conveyor STOP
}

def execute_hardware_action(decision: str, mock_mode: bool):
    if mock_mode:
        # MOCK MODE: Hanya print ke log, tidak akses GPIO
        logger.info(f"[MOCK HARDWARE] Signal: {decision}")
        logger.info(f"[MOCK HARDWARE] Tower Light → {DECISION_THRESHOLD[decision]}")
        logger.info(f"[MOCK HARDWARE] Conveyor → {'STOP' if 'RED' in decision else 'NORMAL'}")
        return {"mock": True, "signal": decision}
    else:
        # REAL HARDWARE MODE: Akses GPIO
        if decision == "GRADE_C_OR_FAIL":
            GPIO.output(RELAY_CONVEYOR_PIN, GPIO.HIGH)    # Matikan motor
            GPIO.output(TOWER_LIGHT_RED_PIN, GPIO.HIGH)   # Nyalakan merah
            GPIO.output(BUZZER_PIN, GPIO.HIGH)             # Aktifkan buzzer
        elif decision == "GRADE_B_PASS":
            GPIO.output(TOWER_LIGHT_YELLOW_PIN, GPIO.HIGH)
            buzzer_short_beep()
        else:
            GPIO.output(TOWER_LIGHT_GREEN_PIN, GPIO.HIGH) # Grade A — aman
```

### 6.4 Mock Hardware Mode untuk Demonstrasi Juri

Sesuai Rulebook COMPFEST 18, juri harus bisa menjalankan sistem secara lokal via `docker-compose up` **tanpa hardware fisik**. Implementasi Mock Mode:

```yaml
# docker-compose.yml
version: "3.8"
services:
  nusaqc-backend:
    build: ./backend
    environment:
      - ENABLE_MOCK_HARDWARE=true    # ← Aktifkan Mock Mode
      - MODEL_PATH=/app/models/
      - DATABASE_URL=sqlite:///./nusaqc_qc_log.db
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./data:/app/data

  nusaqc-frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - nusaqc-backend
```

**Dalam Mock Mode:**
- Sinyal GPIO diganti dengan **log terminal yang verbose** (format JSON)
- Dashboard UI tetap berfungsi penuh termasuk animasi Tower Light (simulasi visual di browser)
- Gambar ikan untuk demo dapat di-upload manual via UI (simulasi trigger sensor)
- Semua fitur logging, classification, bounding box visualisasi tetap berjalan normal

---

## 7. AI Model Specification & Dataset Strategy

### 7.1 Model 1: Fish Freshness Classifier

**Arsitektur & Konfigurasi:**

| Parameter | Nilai |
|-----------|-------|
| Backbone | MobileNetV3-Small |
| Export Format | ONNX Float32 (opset 18, 0.28 MB) |
| Input Shape | `(1, 3, 224, 224)` — RGB, normalized |
| Output | 3 kelas: Grade A / Grade B / Grade C + confidence score |
| Empirical Performance | **75.75% Acc** (Grouped Split) / **84.64% Recall Grade C** (Safety Critical) |
| Benchmark Latency (ONNX CPU) | **2.46 ms/frame (406.8 FPS)** |

**Pre-Processing Pipeline (Solusi Koreksi dari Kritisasi Rayka):**

> ⚠️ **Kritisasi:** Dokumen sebelumnya tidak menjelaskan bagaimana sistem memotret "mata dan insang" secara spesifik di conveyor. Ini adalah gap arsitektur yang fatal.

**Pipeline yang benar (2 tahap):**

```
Tahap 1: Fish ROI Localization
──────────────────────────────
Input: Full frame foto ikan (dari kamera, ~1280×720px)
      │
      ▼
YOLOv8s (digunakan juga sebagai localizer)
Deteksi bounding box kepala ikan → Crop area kepala
      │
      ▼
Cropped Region (kepala ikan, ~300×300px)
      │
      ▼ Resize ke 224×224 + Normalize

Tahap 2: Freshness Classification
──────────────────────────────────
Input: 224×224 ROI kepala ikan
      │
      ▼
MobileNetV3-Small.onnx
      │
      ▼
Output: Grade A (segar) / Grade B (menurun) / Grade C (tidak layak ekspor)
         + Confidence Score (0.0 – 1.0)
```

**Alasan Pemilihan MobileNetV3-Small:**
- Parameter ringan (~3.2M parameters) → cocok untuk inferensi CPU di edge device
- Sudah terbukti untuk task kesegaran ikan: penelitian MobileNetV1 + Attention (ICIIP 2022) mencapai akurasi tinggi pada dataset kesegaran ikan
- Export ke ONNX mudah dan well-documented via `torch.onnx.export`

**Grading Rubric (Berdasarkan Standar CODEX & SNI):**

| Grade | Kondisi Mata | Kondisi Insang | Kondisi Kulit |
|-------|-------------|---------------|---------------|
| **A** | Jernih, cembung, kornea transparan | Merah cerah/merah tua, bersih | Bersih, berkilap, lendir transparan |
| **B** | Sedikit cekung, kornea mulai keruh | Merah pudar/merah jambu | Lendir mulai keruh, sedikit bau |
| **C** | Sangat cekung, mata keruh/kering | Coklat/abu-abu, berbau | Lendir keruh/hijau, bau menyengat |

### 7.2 Model 2: Surface Contamination & Defect Detector

**Arsitektur & Konfigurasi:**

| Parameter | Nilai |
|-----------|-------|
| Backbone | YOLOv8s (Small) |
| Export Format | ONNX Float32 (opset 20, 42.7 MB) |
| Input Shape | `(1, 3, 640, 640)` |
| Output | Bounding box + Label + Confidence + PASS/FAIL decision |
| Empirical Performance | **mAP50 = 0.7310** (TTA: **0.7326**) / **mAP50-95 = 0.4984** |
| Benchmark Latency (ONNX CPU) | **152.07 ms/frame (6.6 FPS)** |
| Classes | `sisik_sisa`, `warna_abnormal`, `luka_robekan`, `lendir_berlebih` |

**Decision Logic:**

```
FAIL Condition (Trigger STOP):
   ├── Terdapat ≥1 bounding box dengan label apapun (confidence > threshold)
   └── Grade dari Model 1 adalah Grade C

CONDITIONAL Condition:
   └── Grade B → Flag untuk pemeriksaan manual tambahan (tidak langsung reject)

PASS Condition:
   ├── Tidak ada bounding box terdeteksi
   └── Grade A atau Grade B (tanpa defek fisik)
```

### 7.3 Strategi Konsolidasi Multi-Dataset Akademis & Training Engine

> 💡 **Pendekatan Dataset NusaQC:** Guna menjamin ketangguhan inferensi di lini produksi tanpa tergantung pada satu sumber data, NusaQC mengondolidasikan 6 dataset akademis terverifikasi (DaFiF, FFE, SalmonScan, Roboflow YOLO, Alaa Mahmoud, dan BD Fish & Shrimp Disease) yang diperkaya dengan **Data Penunjang Riset Lapangan** (foto sampel observasi pasar/UPI Jatim & augmentasi Albumentations).

**Matriks Konsolidasi Dataset AI NusaQC:**

```
DATASET STRATEGY & MODEL MAPPING
──────────────────────────────────────────────────────────────────────────

1. DUAL-ENGINE FRESHNESS MODULE (SNI 2729:2013 Grade A/B/C)
├── Dataset 3: DaFiF Dataset (Prasetyo et al., 2024 - Mendeley Data)
│   ├── 2.536 Gambar JPG (Mackerel: 859, Tilapia: 840, Tuna: 837)
│   ├── 63 File Excel (.xlsx) Rekap Sensor E-Nose (MQ-135 & TGS-2602) & SNI 2729:2013
│   └── Peran: Backbone Utama Multimodal Kesegaran (Citra + Sensor Gas E-Nose)
└── Dataset 4: Freshness of Fish Eyes / FFE (Prasetyo et al., 2022)
    ├── 4.390 Gambar JPG Mata Ikan (8 Spesies x 3 Tier Kesegaran)
    └── Peran: Eye-Clarity Sub-Engine (Inspeksi Visual Spesifik Kornea & Pupil Mata)

2. SURFACE DEFECT & DISEASE MODULE (YOLOv8n / YOLO11n + Binary Classifier)
├── Dataset 6: Roboflow Fish Disease Object Detection (YOLO Format)
│   ├── 457 Gambar Beranotasi YOLO Bounding Box (BDA, BGD, BRD, dll.)
│   └── Peran: Core Training Engine YOLOv8n untuk Bounding Box Lokasi Lesi/Luka
├── Dataset 2: SalmonScan (Ahmed et al., 2024 - Mendeley Data)
│   ├── 1.208 Gambar (Fresh vs Infected Salmon)
│   └── Peran: Surface Disease Classifier (Validasi Biner Infeksi Fisik Salmon)
├── Dataset 5: Alaa Mahmoud Fish Disease (Kaggle)
│   ├── 305 Gambar (FreshFish vs InfectedFish)
│   └── Peran: Baseline Classifier Augmentation
└── Dataset 1: BD Fish & Shrimp Disease Dataset (Saon110, Kaggle)
    ├── 5.887 Gambar (11 Kelas Penyakit Ikan & Udang: WSSV, Black Gill, dll.)
    └── Peran: Cross-Domain Disease Benchmark

3. DATA PENUNJANG & DOMAIN ADAPTATION (Field Validation Set)
└── Data Penunjang Riset Lapangan & Synthetic Augmentation
    ├── Foto sampel observasi lapangan (UPT LPPMHP Surabaya & UPI Jatim)
    └── Albumentations Pipeline: Specular Highlight/Glare Injection (ikan basah),
        Motion Blur (gerakan conveyor), dan Brightness/Contrast Jittering
```

**Engineering Decision Record (EDR) — Model Selection:**

```
EDR-001: Mengapa YOLOv8n dan bukan YOLOv8s/m?
──────────────────────────────────────────────
Keputusan: Gunakan YOLOv8n (Nano) untuk MVP penyisihan
Alasan:
  1. Benchmark (Okano et al., Algorithms 2025, Raspberry Pi 500):
     - YOLOv8n: ~470ms per inference, precision 0.932, mAP50 0.938
     - YOLOv8s: ~1315ms per inference, precision 0.951, mAP50 0.941
  2. Delta akurasi YOLOv8n vs YOLOv8s hanya 0.003 mAP50
  3. Namun delta latency 2.8x lebih lambat untuk YOLOv8s
  4. Dengan Snapshot per Trigger (bukan streaming), YOLOv8n ONNX
     dapat menyelesaikan inferensi <500ms per ikan
  5. Upgrade ke YOLOv8s/m dimungkinkan di Babak Final jika
     hasil validasi menunjukkan mAP kurang memuaskan

EDR-002: Mengapa MobileNetV3-Small dan bukan ResNet/EfficientNet?
─────────────────────────────────────────────────────────────────
Keputusan: Gunakan MobileNetV3-Small
Alasan:
  1. Dirancang untuk mobile/edge inference
  2. Latency CPU sangat baik (<300ms pada RPi5 ONNX)
  3. Cocok untuk 3-class classification (Grade A/B/C)
  4. Transfer learning dari ImageNet weights tersedia dan stabil
  5. Divalidasi dalam literatur kesegaran ikan (ICIIP 2022)

Alternatif yang Dipertimbangkan:
  - ResNet50: 25x lebih banyak parameter, terlalu berat
  - EfficientNet-B0: Comparable accuracy tapi lebih berat dari V3-Small
  - ViT: Tidak cocok untuk edge inference CPU-only
```

### 7.4 Training Pipeline

```
TRAINING PIPELINE
─────────────────
STEP 1: Data Collection
├── Primary: Ambil foto ikan di UPI lokal (dengan izin)
│   ├── Scombridae: Tuna, Cakalang (dominan ekspor)
│   ├── Cichlidae: Tilapia/Nila
│   └── Salmonidae: Salmon
└── Augmentation: Albumentations (flip, rotate, color jitter, blur)

STEP 2: Annotation
├── Model 1: Label kelas (A/B/C) per gambar → CSV format
└── Model 2: Bounding box annotation via Roboflow/CVAT
    └── Classes: sisik_sisa, warna_abnormal, luka_robekan,
                 foreign_object, lendir_berlebih

STEP 3: Training Environment
├── Platform: Google Colab Pro / GPU workstation
├── Framework: PyTorch 2.0 + Ultralytics (untuk YOLOv8n)
├── Train/Val/Test Split: 70% / 15% / 15%
└── Epochs: 100 (Model 1) / 150 (Model 2)

STEP 4: Evaluation
├── Model 1: F1-Score per kelas, Confusion Matrix
└── Model 2: mAP50, Precision, Recall per defect class

STEP 5: Export & Optimization
└── Export ke ONNX (opset 17)
    └── Test latency di Raspberry Pi 5 / laptop CPU
        (wajib: total inference ≤ 1500ms per ikan di MVP Snapshot mode)
```

---

## 8. Metodologi Perancangan Perangkat Lunak

### 8.1 Scope MVP Penyisihan & Rencana Pengembangan Final

Sesuai ketentuan Rulebook COMPFEST 18 (Batasan Ketat MVP), scope NusaQC untuk fase penyisihan dirancang dengan dua pertimbangan utama: **kepatuhan penuh terhadap rulebook** dan **fleksibilitas arsitektur untuk Babak Final**.

**Yang ADA di MVP Penyisihan:**
- ✅ UI utama: upload/trigger foto → tampilkan hasil grade + bounding box
- ✅ Single frame inference / Snapshot per trigger (bukan live video)
- ✅ SQLite logging per lot inspeksi
- ✅ Mock Hardware Mode dengan log terminal verbose
- ✅ Dual-model inference (Model 1 + Model 2) secara sequential
- ✅ Export data CSV dari log inspeksi
- ✅ Dashboard monitoring real-time (WebSocket)

**Yang TIDAK ADA di MVP (sesuai batasan rulebook):**
- ❌ Continuous video streaming inference
- ❌ Advanced analytics dashboard (time-series grafik per minggu/bulan)
- ❌ Sistem autentikasi kompleks (login multi-role)
- ❌ Background jobs / auto-retraining pipeline
- ❌ Distributed database atau cloud sync
- ❌ Multi-camera support
- ❌ Auto-tuning model parameters

**Yang Direncanakan untuk Babak Final Hackathon (10 Jam Luring):**
- 🎯 **Continuous Automated Conveyor Mode** — upgrade dari Snapshot ke streaming async
- 🎯 Async inference worker pool (multi-threaded ONNX sessions)
- 🎯 Frame buffer queue untuk decoupling capture & inference
- 🎯 Dynamic throughput tuning

> **Catatan Arsitektur:** Pemilihan FastAPI sebagai backend bukan sekadar kebutuhan MVP — FastAPI mendukung async/await natively, sehingga upgrade ke continuous mode di Final Hackathon hanya membutuhkan penambahan layer async di atas inference engine yang sudah ada, **tanpa perombakan arsitektur total**.

### 8.2 Alur Pengembangan Model (Per Feature)

```
FEATURE DEVELOPMENT FLOW (Iteratif)
────────────────────────────────────

Sprint 1 (Minggu 1–2): Foundation
  ├── Setup repo GitHub (public visibility)
  ├── Struktur folder: /backend, /frontend, /models, /data, /docs
  ├── Docker + docker-compose dasar (backend FastAPI)
  └── Conventional commits setup

Sprint 2 (Minggu 2–3): AI Pipeline
  ├── Data collection (primary data + augmentation)
  ├── Model 1 training (MobileNetV3) → Export ONNX
  ├── Model 2 training (YOLOv8n) → Export ONNX
  └── Validation metrics: F1-Score, mAP50

Sprint 3 (Minggu 3–4): Backend Integration
  ├── FastAPI endpoint: POST /inspect (terima gambar → return JSON result)
  ├── SQLite schema + logging
  ├── Mock Hardware Controller
  └── WebSocket event emitter

Sprint 4 (Minggu 4–5): Frontend
  ├── React Dashboard: upload UI + hasil inspeksi
  ├── Bounding box overlay visualization
  ├── Real-time lot log table
  └── CSV export

Sprint 5 (Minggu 5–6): Integration & Testing
  ├── End-to-end test: gambar masuk → inference → result tampil
  ├── Mock Mode validation (semua path tanpa hardware)
  ├── README.md + setup guide (docker-compose up)
  └── Proof of Work video recording

Submisi: 25 Agustus 2026 pukul 23:55 WIB
```

### 8.3 Alur Integrasi Model ke Environment Kode

```
ALUR INTEGRASI MODEL → KODE (Backend)
──────────────────────────────────────

1. Training Output:
   models/
   ├── freshness_classifier.onnx    ← MobileNetV3-Small
   ├── defect_detector.onnx         ← YOLOv8n
   └── class_labels.json            ← Mapping index → label

2. FastAPI Startup (app/main.py):
   - Load model dengan onnxruntime.InferenceSession()
   - Session disimpan di app state (singleton, tidak reload per request)
   - Validasi model tersedia: jika tidak ada, raise startup error

3. Inference Request (POST /api/v1/inspect):
   Receive: multipart/form-data (image + lot_id + fish_family)
   Processing:
     a. Read image → PIL Image → numpy array
     b. Pre-process: resize, normalize, to tensor
     c. Run Model 1 (freshness): ort_session_freshness.run()
     d. Parse output: argmax → Grade + confidence
     e. Run Model 2 (defect): ort_session_defect.run()
     f. Parse output: NMS → bounding boxes + labels
     g. Decision Engine: combine Grade + defects → PASS/FAIL
     h. Hardware action: execute_hardware_action(decision, MOCK_MODE)
     i. Log to SQLite: INSERT INTO inspections (...)
     j. Return JSON response

4. Response Schema (JSON):
   {
     "lot_id": "LOT-2026-0825-001",
     "timestamp": "2026-08-25T10:30:00Z",
     "fish_family": "Scombridae",
     "grade": "B",
     "grade_confidence": 0.87,
     "defects": [
       {
         "label": "sisik_sisa",
         "bbox": [120, 45, 280, 190],
         "confidence": 0.91
       }
     ],
     "decision": "CONDITIONAL",
     "hardware_signal": "YELLOW",
     "processing_time_ms": 892
   }
```

### 8.4 Struktur Folder Repository (GitHub)

```
nusaqc/
├── README.md                    ← Setup guide (WAJIB, jelas untuk juri)
├── docker-compose.yml           ← docker-compose up langsung jalan
├── .env.example                 ← Contoh environment variables
├── .gitignore
│
├── backend/                     ← FastAPI Python
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── inspect.py   ← POST /inspect endpoint
│   │   │       └── lots.py      ← GET /lots (history)
│   │   ├── models/
│   │   │   ├── inference.py     ← ONNX Runtime wrapper
│   │   │   └── decision.py      ← Grade + defect → PASS/FAIL
│   │   ├── hardware/
│   │   │   └── controller.py    ← GPIO / Mock Mode logic
│   │   ├── database/
│   │   │   ├── schema.sql
│   │   │   └── crud.py
│   │   └── config.py            ← ENABLE_MOCK_HARDWARE, paths
│   └── models/                  ← ONNX files (gitignored jika >100MB)
│       ├── freshness_classifier.onnx
│       ├── defect_detector.onnx
│       └── class_labels.json
│
├── frontend/                    ← React.js
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── InspectPanel.jsx    ← Upload + trigger
│       │   ├── ResultCard.jsx      ← Grade + bbox overlay
│       │   ├── LotHistory.jsx      ← Tabel log inspeksi
│       │   └── StatusIndicator.jsx ← Simulasi Tower Light di UI
│       └── hooks/
│           └── useWebSocket.js     ← Real-time event subscription
│
└── docs/
    ├── architecture.md
    ├── hardware_setup.md
    └── training/
        ├── model1_training.ipynb
        └── model2_training.ipynb
```

---

## 9. COMPFEST 18 MVP Compliance Matrix

Berikut adalah bukti kepatuhan terhadap seluruh ketentuan Rulebook COMPFEST 18 (Teknis & Kriteria Penyisihan):

### 9.1 Ketentuan Produk

| No | Ketentuan Rulebook | Status NusaQC | Implementasi |
|----|-------------------|---------------|-------------|
| 1 | Proyek merupakan inovasi di bidang AI for Backbone Economy | ✅ | Smart Manufacturing: CV-based QC di lini produksi UPI |
| 2 | Proyek merupakan karya orisinal tim | ✅ | Tidak menggunakan project lama; dibuat periode 17 Juni–25 Agustus 2026 |
| 3 | Proyek hanya dikerjakan selama perlombaan berlangsung | ✅ | Repository dibuat fresh, commit history dari mulai lomba |
| 4 | Proyek penyisihan wajib dilanjutkan ke Final | ✅ | Arsitektur modular dirancang eksplisit untuk iterasi di hackathon final — upgrade snapshot → continuous mode |

### 9.2 Batasan MVP (Scope Compliance)

| Batasan | Ketentuan | Status |
|---------|-----------|--------|
| **Frontend** | UI wajib hanya berfokus pada alur interaksi inti | ✅ Hanya: upload foto → tampil hasil. Tidak ada advanced dashboard |
| **Frontend** | Tidak perlu dashboard analitik tingkat lanjut | ✅ Tidak ada time-series analytics di MVP |
| **Frontend** | Tidak perlu sistem otentikasi kompleks | ✅ Tidak ada multi-role auth |
| **Backend** | Arsitektur wajib hanya sampai pemrosesan sinkron | ✅ FastAPI sync endpoint — Snapshot per Trigger, tidak ada background streaming |
| **Backend** | Tidak perlu background jobs / auto data logging | ✅ Logging hanya saat request masuk (per trigger) |
| **Backend** | Tidak perlu infrastruktur database terdistribusi | ✅ SQLite lokal murni |
| **Backend** | Fokus agar API/sistem lokal dapat dijalankan via docker-compose | ✅ `docker-compose up` langsung running |
| **AI Model** | Implementasi AI wajib hanya berfokus pada core inference | ✅ ONNX inference dengan frozen weights |
| **AI Model** | Tidak perlu sistem auto-tuning | ✅ Tidak ada online learning |
| **AI Model** | Tidak perlu bulk testing scripts | ✅ Test dilakukan manual via UI |
| **AI Model** | Tidak perlu mekanisme loop umpan balik otomatis di repository | ✅ Feedback loop ke hardware (relay/aktuator), bukan ke model |

### 9.3 Ketentuan Deliverables

| Deliverable | Ketentuan | Status | Detail |
|-------------|-----------|--------|--------|
| **GitHub Repo** | Public, setup guide di README.md, docker-compose | ✅ | README menjelaskan: prerequisites → clone → `docker-compose up` → akses localhost |
| **GitHub Repo** | Conventional commits (feat/fix/refactor) | ✅ | Git hook pre-commit menggunakan commitlint |
| **GitHub Repo** | Batas commit: 25 Agustus 2026 23:55 WIB | ⚠️ | Wajib diingat tim, set alarm |
| **Video PoW** | Maks 7 menit, YouTube UNLISTED | ✅ | Durasi rencana: 5 menit |
| **Video PoW** | Format: `COMPFEST 18 AIC: PROOF OF WORK - [Tim] - NusaQC` | ✅ | Template nama sudah disiapkan |
| **Video PoW** | Double screen (terminal + aplikasi), TANPA CUT | ✅ | OBS Studio: split screen recording |
| **Video PoW** | Semua fitur di video promosi HARUS ada di PoW | ✅ | Feature parity check sebelum upload |
| **Video Promosi** | Maks 5 menit, YouTube PUBLIC, MP4 ≥720p | ✅ | Durasi rencana: 4 menit |
| **Video Promosi** | Format: `COMPFEST 18 AIC: [Tim] - NusaQC` | ✅ | |
| **Proposal PDF** | Maks 20 hal (exclude cover, pustaka, lampiran) | ✅ | Target: 18 halaman |
| **Proposal PDF** | Mencakup: Latar Belakang, Tujuan, Metodologi, Kesimpulan | ✅ | Semua bagian ada |
| **Blind Judging** | TIDAK BOLEH ada nama/logo universitas | ✅ | Semua asset diperiksa sebelum submit |

### 9.4 Potensi Final Hackathon: Snapshot MVP → Continuous Automated Mode

> **Ini adalah amunisi utama untuk Babak Final.**

Arsitektur NusaQC MVP dirancang dengan prinsip *upgrade-first*: setiap komponen dalam Snapshot Mode memiliki jalur upgrade yang jelas menuju Continuous Automated Mode. Hal ini menunjukkan kepada juri bahwa tim memahami perbedaan antara *batasan MVP yang disengaja* dan *keterbatasan visi produk*.

```
UPGRADE PATH: Snapshot MVP → Continuous Mode (Target Final Hackathon)
──────────────────────────────────────────────────────────────────────

Komponen       │ MVP Penyisihan (Snapshot)  │ Final Hackathon Target
───────────────┼────────────────────────────┼──────────────────────────────
Capture        │ Single frame per trigger   │ Continuous video stream
               │                            │ (kamera rekam terus)
               │                            │
Inference      │ Synchronous sequential     │ Async worker pool
               │ (blocking per request)     │ (non-blocking, paralel)
               │                            │
Queue          │ Tidak ada                  │ Frame buffer queue
               │                            │ (decouple capture & inference)
               │                            │
FastAPI        │ Sync endpoint              │ Async endpoint + BackgroundTasks
               │                            │ (native FastAPI support)
               │                            │
Throughput     │ ≤ 1 ikan/1,5 detik         │ Mengikuti kecepatan conveyor
               │                            │ industri (target: real-time)
               │                            │
Hardware       │ Trigger → capture → result │ Continuous scan → queue →
Control        │ → aktuasi (sekuensial)     │ result → aktuasi (paralel)
```

**Estimasi waktu upgrade di Hackathon 10 Jam:**
- Implementasi async endpoint FastAPI: ~2 jam
- Frame buffer queue (Python asyncio + threading): ~3 jam
- Integration testing + tuning: ~3 jam
- Demo preparation: ~2 jam

### 9.5 Skor Proyeksi Berdasarkan Kriteria Resmi

| Kriteria | Bobot | Proyeksi NusaQC | Justifikasi |
|----------|-------|-----------------|-------------|
| Orisinalitas & Dampak Sosial | 20% | **Tinggi** | Solusi CV untuk QC ikan UPI belum ada yang open-source lokal; impact ke industri ekspor USD 5,7 miliar |
| Implementasi Teknologi & Kematangan Arsitektur | 25% | **Tinggi** | Dual-model ONNX, Closed-Loop Hardware, Mock Mode, modular folder structure, upgrade path yang jelas |
| Kesiapan MVP | 15% | **Sedang–Tinggi** | Scope tepat (snapshot = trade-off rulebook, bukan kelemahan), core features functional, mudah diexpand di hackathon final |
| Video Promosi | 15% | **Sedang** | Bergantung pada kualitas produksi video tim |
| Kualitas Proposal & Proses Pengembangan | 15% | **Tinggi** | EDR per keputusan teknis, data-driven methodology, framing MVP vs Production Vision yang jelas |
| Relevansi dengan Tema | 10% | **Sangat Tinggi** | Smart Manufacturing dengan Closed-Loop Control = definisi literal tema |
| Business Value & Governance (BONUS) | 3.5% | **Sedang** | Business model B2B SaaS ada; AI ethics (bias analisis) perlu ditambahkan |
| AIC Talks (BONUS) | 1.5% | **Tinggi** | Wajib hadir 25 Juli 2026 |
| **ESTIMASI TOTAL** | **≤105%** | **~80–88%** | Bergantung eksekusi video & kualitas model |

---

## 10. Business Model & Governance

### 10.1 Model Bisnis B2B SaaS

```
REVENUE MODEL
─────────────
Tier 1 — Starter (per titik inspeksi)
  Harga   : Rp 1.500.000/bulan per unit NusaQC
  Target  : UPI menengah (1–2 lini sortasi)
  Include : Hardware kit (RPi5 + kamera + actuator) + Software license
            + Setup support + 1 tahun garansi hardware

Tier 2 — Business (per UPI)
  Harga   : Rp 3.500.000/bulan (up to 5 titik inspeksi)
  Target  : UPI besar (multiple lini sortasi)
  Include : Semua Tier 1 + Priority support + Model retraining quarterly

UNIT ECONOMICS (Proyeksi Konservatif)
───────────────────────────────────────
Hardware cost per unit : ~Rp 3.000.000 (CAPEX sekali)
Monthly opex per unit  : ~Rp 200.000 (listrik, support)
Monthly revenue Tier 1 : Rp 1.500.000
Gross margin           : ~85%
Customer payback       : ~3 bulan untuk UPI

MARKET POTENTIAL
────────────────
Total addressable UPI (export-certified) : ~400–600 UPI
Average spend per UPI (3 titik)          : Rp 4.500.000/bulan
TAM (monthly)                            : Rp 1,8–2,7 miliar/bulan
SAM (reachable, 5% penetrasi)            : Rp 90–135 juta/bulan
```

### 10.2 ROI Kalkulator untuk UPI

Berdasarkan estimasi konservatif:

```
Skenario: UPI Menengah, Ekspor Tuna ke AS
──────────────────────────────────────────
Volume proses per bulan  : 50 ton ikan
Rata-rata nilai ekspor   : USD 8/kg = Rp 130.000/kg (kurs Rp 16.200)
Total nilai produksi/bln : Rp 6,5 miliar

Risiko penolakan ekspor saat ini (estimasi 2% lot):
  2% × Rp 6,5 miliar = Rp 130 juta/bulan potensi kerugian

Dengan NusaQC (estimasi reduksi penolakan 50%):
  Penghematan potensial : Rp 65 juta/bulan
  Biaya NusaQC Tier 1  : Rp 1,5 juta/bulan (1 titik)
  NET BENEFIT/bulan    : Rp 63,5 juta
  Payback hardware     : 3.000.000 / 63.500.000 = 0,05 bulan ≈ SEGERA
```

### 10.3 AI Governance & Etika

| Dimensi | Risiko | Mitigasi |
|---------|--------|----------|
| **Bias Dataset** | Model dilatih mayoritas dari 3 familia ikan; ikan jenis lain bisa false negative | Dokumentasikan scope dengan jelas; label "Unsupported Species" jika ikan tidak dikenal |
| **False Negative Risk** | Ikan cacat lolos karena confidence di bawah threshold | Threshold dapat dikonfigurasi per UPI; default konservatif (lebih sensitif) |
| **Data Privacy** | Foto ikan yang diambil di UPI bisa berisi informasi produksi sensitif | Foto tidak dikirim ke cloud; disimpan lokal di SQLite + dapat dihapus per lot |
| **Operator Over-trust** | Operator terlalu bergantung pada AI, mengabaikan judgment manual | UI selalu menampilkan peringatan "AI is an assistant, not a replacement for human QC" |
| **Model Transparency** | Juri / UPI tidak memahami dasar keputusan AI | Confidence score + bounding box selalu ditampilkan; tidak ada black-box decision |

---

## 11. Risk Register & Mitigasi

| No | Risiko | Probabilitas | Dampak | Mitigasi |
|----|--------|-------------|--------|----------|
| R01 | **Hardware inference terlalu lambat di RPi5** | Sedang | Tinggi | Benchmark awal di hardware target; fallback ke laptop CPU untuk demo |
| R02 | **Variasi pencahayaan & kilau air pada kulit ikan basah** | Sedang | Tinggi | Pemasangan Linear Polarizing Filter pada kamera optis + augmentasi Albumentations (glare injection) |
| R03 | **Variasi spesies regional di luar dataset publik** | Sedang | Sedang | Arsitektur AI modular dengan transfer learning cepat (DaFiF + FFE) untuk fine-tuning spesies baru |
| R04 | **Polarizing filter tidak efektif di kondisi tertentu** | Rendah | Sedang | Tes dengan sampel ikan basah; backup: preprocessing contrast enhancement di software |
| R05 | **Mock Mode tidak merepresentasikan hardware asli** | Rendah | Rendah | Mock Mode log didesain verbose dan representatif; juri memahami ini adalah simulasi |
| R06 | **Blind judging violation (logo universitas)** | Rendah | Sangat Tinggi | Checklist sebelum submit: scan semua file untuk mention nama kampus |
| R07 | **Deadline terlewat** | Rendah | Fatal | Set alarm 3 hari sebelum deadline (22 Agustus) untuk final review |
| R08 | **Framing MVP disalahpahami sebagai kelemahan produk** | Rendah | Sedang | Narasi eksplisit di proposal & video bahwa Snapshot adalah *trade-off rulebook*, bukan batas visi |

---

## 12. Deliverables Checklist Submisi

### Final Check sebelum 25 Agustus 2026 pukul 23:55 WIB

**GitHub Repository:**
- [ ] Repository public, URL dapat diakses
- [ ] README.md berisi: prerequisites → clone → `docker-compose up` → akses browser
- [ ] Tidak ada nama/logo universitas di seluruh kode, komentar, atau docs
- [ ] Commit history menggunakan Conventional Commits (feat/fix/refactor)
- [ ] `.env.example` ada dan terdokumentasi
- [ ] Model ONNX dapat didownload (via README link atau include di repo)
- [ ] `docker-compose up` berhasil dijalankan di mesin clean (validasi sendiri)

**Video Proof of Work (YouTube UNLISTED):**
- [ ] Durasi ≤ 7 menit
- [ ] Format nama: `COMPFEST 18 AIC: PROOF OF WORK - [Nama Tim] - NusaQC`
- [ ] Menampilkan double screen: terminal + aplikasi
- [ ] Timestamp visible di terminal
- [ ] Tidak ada CUT atau edit memotong — hanya fast-forward bagian loading
- [ ] Semua fitur di video ini ada juga di video promosi
- [ ] Jujur tentang fitur yang belum beres (dengan penjelasan)

**Video Promosi (YouTube PUBLIC):**
- [ ] Durasi ≤ 5 menit, resolusi ≥720p, format MP4
- [ ] Format nama: `COMPFEST 18 AIC: [Nama Tim] - NusaQC`
- [ ] Menjelaskan: problem → solution → impact (dengan angka konkret)
- [ ] Menunjukkan alur inspeksi ikan di dashboard
- [ ] Tidak ada nama/logo universitas
- [ ] Narasi jelas membedakan visi produk (continuous) vs scope MVP penyisihan (snapshot)

**Proposal PDF:**
- [ ] Maksimal 20 halaman (tidak termasuk cover, daftar pustaka, lampiran)
- [ ] Berisi: Nama Kelompok, Latar Belakang, Tujuan, Metodologi, Kesimpulan
- [ ] Metodologi mencakup: alur dataset, alur training, alur integrasi model ke kode
- [ ] Setiap keputusan teknis ada Engineering Decision Record-nya
- [ ] Tidak ada klaim ilmiah yang salah (khususnya: tidak ada klaim deteksi Salmonella)
- [ ] Tidak ada nama/logo universitas
- [ ] Framing MVP vs Production Vision dijelaskan dengan jelas

