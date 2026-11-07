# NusaQC — AI-Powered Visual Quality Control & Digital Traceability System

[![COMPFEST 18](https://img.shields.io/badge/AIC-COMPFEST%2018%20(2026)-0284c7?style=flat-square)](https://compfest.id)
[![Track](https://img.shields.io/badge/Track-Smart%20Manufacturing-16a34a?style=flat-square)](https://compfest.id)
[![Architecture](https://img.shields.io/badge/Architecture-Dual--Model%20ONNX%20Edge%20Inference-8b5cf6?style=flat-square)](https://onnxruntime.ai/)
[![Docker](https://img.shields.io/badge/Container-Docker%20Compose-2563eb?style=flat-square)](https://docker.com)
[![Status](https://img.shields.io/badge/MVP%20Status-Ready%20for%20Evaluation-emerald?style=flat-square)](#)

> **NusaQC** adalah sistem kendali mutu visual (*Quality Control*) dan rantai keterlacakan digital (*Digital Traceability Chain*) berbasis *Computer Vision* dan *Edge AI* yang dirancang untuk lini sortasi Unit Pengolahan Ikan (UPI) ekspor Indonesia. Sistem ini mengotomatisasi inspeksi kesegaran berstandar SNI 2729:2013, mendeteksi kontaminasi/cacat fisik (*filthy*), mengontrol aktuator konveyor secara tertutup (*closed-loop*), serta mencatat jejak audit dari inspeksi hingga manifes pengiriman ekspor.

---

## 📑 Daftar Isi

1. [Latar Belakang & Masalah](#latar-belakang--masalah)
2. [Arsitektur Sistem & Alur Kerja](#arsitektur-sistem--alur-kerja)
3. [Pipeline AI & Decision Engine](#pipeline-ai--decision-engine)
4. [Ekosistem Keterlacakan Digital (Traceability Chain)](#ekosistem-keterlacakan-digital-traceability-chain)
5. [Integrasi Hardware Closed-Loop & Mock Mode](#integrasi-hardware-closed-loop--mock-mode)
6. [Struktur Repositori](#struktur-repositori)
7. [Panduan Pengaturan & Instalasi (Setup Guide)](#panduan-pengaturan--instalasi-setup-guide)
8. [Spesifikasi Kontrak REST API & WebSocket](#spesifikasi-kontrak-rest-api--websocket)
9. [Panduan Verifikasi & Simulasi Pengujian Juri](#panduan-verifikasi--simulasi-pengujian-juri)
10. [Kepatuhan terhadap Rulebook AIC COMPFEST 18](#kepatuhan-terhadap-rulebook-aic-compfest-18)
11. [Tim Pengembang](#tim-pengembang)

---

<a id="latar-belakang--masalah"></a>
## 🎯 Latar Belakang & Masalah

Berdasarkan data penelitian peer-reviewed (*Nurkhasanah et al., 2022*) terhadap penolakan ekspor perikanan Indonesia oleh US-FDA dan EU-RASFF, **lebih dari 80% kasus penolakan disebabkan oleh faktor *filthy* (kontaminasi fisik visual)** seperti sisa sisik, luka robekan, lendir abnormal, dan benda asing.

Tiga kelemahan struktural metode QC konvensional:
1. **Subjektivitas & Kelelahan Operator:** Pemeriksaan organoleptik manual rentan terhadap inkonsistensi penilaian antar operator dan penurunan akurasi pada shift malam.
2. **Pencatatan Berbasis Kertas (*Paper-Based*):** Data hasil QC tidak terhubung langsung dengan denah cold storage maupun dokumen pengiriman, menyulitkan audit kepatuhan karantina (BKIPM/FDA).
3. **Ketiadaan Intervensi Real-Time:** Ikan berkualitas rendah sering kali lolos ke tahap pembekuan (*IQF*) sebelum terdeteksi, meningkatkan risiko kerugian penolakan ekspor bernilai ribuan USD per kontainer.

**Solusi NusaQC:** Menghadirkan sistem pemilah berbasis *dual-model inference* dengan latensi sub-detik (≤ 500 ms), aktuasi konveyor otomatis, serta rantai data digital utuh dari inspeksi, penempatan di *cold storage*, hingga pembuatan manifes pengiriman ekspor.

---

<a id="arsitektur-sistem--alur-kerja"></a>
## 🏗️ Arsitektur Sistem & Alur Kerja

```
[Conveyor Inflow] ──> [Optical Trigger Sensor]
                             │ (Trigger Signal)
                             ▼
               [Industrial Camera (5MP/Polarized)]
                             │ (Snapshot Image)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Engine                   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │               Dual-Model AI Inference               │   │
│   │                                                     │   │
│   │  Model 1: Freshness (MobileNetV3) ──> Grade A/B/C   │   │
│   │  Model 2: Defect Detection (YOLOv8s) ──> BBoxes     │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│                              ▼                              │
│               [Rule-Based Decision Engine]                  │
│       Evaluates Grade + Defect Filter + Threshold           │
│                              │                              │
│            ┌─────────────────┴─────────────────┐            │
│            ▼                                   ▼            │
│   [Hardware Controller]              [Data Persistence]     │
│   • GREEN: Conveyor Normal           • SQLite QC Audit Logs │
│   • YELLOW: Warning / Verify         • WebSocket Event Bus  │
│   • RED: Conveyor STOP / Eject       • Storage Map & Slot   │
└────────────────────────────────────────────────┬────────────┘
                                                 │
                                                 ▼
                              [Next.js 16 Operator Dashboard]
                              • Live Inspection Monitoring
                              • Lot History & Human Override
                              • Cold/Frozen Storage Map Grid
                              • Export Dispatch Manifest Builder
```

### Alur Kerja Operasional (Step-by-Step Execution):

1. **Deteksi Objek (Proximity Sensor):** Sensor *photoelectric* mendeteksi ikan melintas di konveyor dan mengirim sinyal pemicu (*trigger*) ke backend.
2. **Akuisisi Citra (Kamera Industri):** Kamera mengambil 1 frame snapshot beresolusi tinggi dengan pencahayaan terkontrol dan filter polarisasi untuk meredam pantulan kilau air (*specular glare*).
3. **Pra-Pemrosesan (FastAPI):** Frame dinormalisasi; area kepala/mata diekstrak sebagai ROI untuk Model 1, sedangkan frame utuh diproses dengan *letterbox padding* untuk Model 2.
4. **Inferensi Ganda AI (ONNX Runtime CPU):**
    - **Model 1 (MobileNetV3-Small):** Mengklasifikasikan tingkat kesegaran organoleptik sesuai baku mutu SNI 2729:2013 (Grade A, B, C).
    - **Model 2 (YOLOv8s):** Memindai 5 kelas defek permukaan (`sisik_sisa`, `warna_abnormal`, `luka_robekan`, `foreign_object`, `lendir_berlebih`) pasca-*Non-Maximum Suppression* (NMS).
5. **Penetapan Keputusan (Decision Engine):** Menggabungkan luaran kedua model dengan memperhitungkan *Confidence Threshold* dinamis dari konfigurasi sistem.
6. **Aktuasi Fisik Konveyor (GPIO Relay / Mock Hardware):**
    - **PASS:** Konveyor melaju normal, lampu hijau aktif.
    - **CONDITIONAL:** Konveyor melambat, lampu kuning berkedip untuk verifikasi manual.
    - **FAIL:** Relai memutus arus motor (**STOP**), lampu merah dan sirine aktif seketika.
7. **Pencatatan Audit (SQLite Logging):** Data inspeksi lengkap (Lot ID, timestamp UTC, famili ikan, grade, defek, skor keyakinan, bounding box, dan citra) disimpan ke SQLite lokal.
8. **Alokasi Penyimpanan (Lot Storage Map):** Lot berstatus PASS masuk ke antrean *Pending Storage* untuk dialokasikan operator ke slot fisik *Cold Zone* (0–4°C) atau *Frozen Zone* (≤ -18°C).
9. **Manifes Pengiriman (Export Dispatch):** Lot yang tersimpan dikonsolidasikan ke dalam dokumen kontainer ekspor digital yang siap diekspor ke format CSV untuk audit kepatuhan karantina.

---

<a id="pipeline-ai--decision-engine"></a>
## 🧠 Pipeline AI & Decision Engine

### Spesifikasi Model AI

| Atribut | Model 1: Freshness Classifier | Model 2: Surface Defect Detector |
|---|---|---|
| **Arsitektur Dasar** | **MobileNetV3-Small** | **YOLOv8s** |
| **Format Deployment** | ONNX Runtime (CPU-optimized) | ONNX Runtime (CPU-optimized) |
| **Dimensi Input** | 224 × 224 × 3 (ROI Kepala/Mata) | 640 × 640 × 3 (Full Frame) |
| **Luaran Model** | Grade A (Prima), Grade B (Layak), Grade C (Afkir) | Bounding Boxes, Class Labels, Confidence Scores |
| **Target Rekayasa** | F1-Score ≥ 85% | mAP@50 ≥ 0.70 |
| **Latensi CPU Rata-Rata** | 150 - 250 ms | 200 - 300 ms |

### Matriks Logika Keputusan Mutu (*Decision Engine*)

Keputusan akhir dievaluasi secara deterministik berdasarkan rumus:
`Decision = f(Grade, Grade Confidence, Filtered Defects, Threshold)`

| Keputusan | Sinyal Hardware | Kondisi Evaluasi | Aksi Sistem |
|---|---|---|---|
| **PASS** | `GREEN` | Grade A (semua confidence) **ATAU** Grade B dengan `confidence` ≥ threshold, dan **tanpa** defek nyata ≥ threshold. | Konveyor berjalan normal, lampu hijau menyala, lot masuk antrean *Lot Storage Map*. |
| **CONDITIONAL** | `YELLOW` | Grade B dengan `confidence` < threshold yang disetel pada Settings, dan tanpa defek kritis. | Konveyor melambat/peringatan visual, operator diarahkan melakukan verifikasi visual. |
| **FAIL / REJECT** | `RED` | Grade C (Afkir) **ATAU** terdeteksi ≥ 1 defek fisik dengan confidence ≥ threshold. | Relai memutus arus motor (**Konveyor STOP**), alarm menyala, lot ditandai *Reject*. |

---

<a id="ekosistem-keterlacakan-digital-traceability-chain"></a>
## 🔗 Ekosistem Keterlacakan Digital (Traceability Chain)

NusaQC menghubungkan seluruh simpul operasional pabrik pengolahan ikan:

```
[Conveyor Inspection] ───> [Lot Storage Map] ───> [Export Dispatch] ───> [Audit BKIPM / Buyer]
 • Keputusan QC            • Cold Zone (0-4°C)     • No. Kontainer         • Digital Manifest
 • Bounding Box Defek      • Frozen (≤ -18°C)      • Buyer & Destinasi     • CSV Audit Trail
 • Human Override Option   • Slot C-01 s.d. F-10   • 1-Click Assignment    • Compliance Ready
```

### 1. Lot Storage Map Module (Penyimpanan Dingin Terzonasi)
- **Interactive Grid Layout:** Memvisualisasikan denah *Cold Zone* (grid 5×5, label C-01 s.d. C-25) dan *Frozen Zone* (grid 2×5, label F-01 s.d. F-10).
- **Slot Assignment:** Lot PASS dialokasikan ke slot fisik secara digital, mencegah pencampuran grade dan kontaminasi silang.
- **Side Drawer Detail:** Menampilkan metadata lot, famili ikan, grade, waktu masuk (*stored since*), serta aksi pengosongan (*clear slot*).

### 2. Export Dispatch Module (Manajemen Manifes Ekspor)
- **Shipment Manifest Builder:** Menggabungkan lot-lot yang tersimpan di storage ke dalam satu dokumen pengiriman terpadu.
- **Compliance Summary:** Menjawab pertanyaan audit regulasi: *"Lot Grade A pada tanggal X berada di kontainer mana dan dikirim ke buyer siapa?"*
- **1-Click CSV Export:** Menghasilkan rekapitulasi data lot dan QC summary yang siap dilampirkan pada dokumen kepatuhan karantina.

---

<a id="integrasi-hardware-closed-loop--mock-mode"></a>
## 🔌 Integrasi Hardware Closed-Loop & Mock Mode

Aplikasi dilengkapi modul abstraksi perangkat keras (`backend/app/hardware/`):

1. **Mode Perangkat Keras Fisik (`ENABLE_MOCK_HARDWARE=false`):**
    - Berjalan di Raspberry Pi 5 menggunakan `RPi.GPIO` untuk mengontrol modul relai konveyor 24V DC, Stack Light 3-warna, dan Buzzer 85dB.
2. **Mode Simulasi / Mock Hardware (`ENABLE_MOCK_HARDWARE=true`):**
    - **Wajib untuk Evaluasi Juri:** Mengizinkan seluruh sistem berjalan 100% di komputer/laptop penguji tanpa perangkat fisik.
    - Mencetak log terminal terstruktur dengan visualisasi warna ASCII saat aktuator terpicu:
        ```text
        [MOCK HARDWARE] [SIGNAL: GREEN] Conveyor Normal Speed | Tower: GREEN | Buzzer: OFF
        [MOCK HARDWARE] [SIGNAL: RED] RELAY CUT-OFF -> Conveyor STOPPED | Tower: RED | Siren: ACTIVE
        ```

---

<a id="struktur-repositori"></a>
## 📁 Struktur Repositori

```text
nusaqc/
├── docker-compose.yml              # Orkestrasi multi-container Docker (Backend + Frontend)
├── README.md                       # Dokumentasi teknis & panduan pengaturan
├── LICENSE                         # Lisensi proyek open source
│
├── backend/                        # Layanan Backend FastAPI
│   ├── Dockerfile                  # Container definition backend
│   ├── pyproject.toml              # Definisi dependensi & metadata package manager
│   ├── .env.example                # Template variabel lingkungan
│   ├── models_weights/             # Bobot model AI ONNX teroptimasi CPU
│   │   ├── mobilenetv3_freshness.onnx
│   │   └── nusaqc_model2_defect_detector.onnx
│   ├── uploads/                    # Penyimpanan lokal foto inspeksi sampel
│   └── app/
│       ├── main.py                 # Entrypoint FastAPI & WebSocket lifecycle
│       ├── config.py               # Pydantic BaseSettings
│       ├── ai/                     # Runtime AI ONNX & Preprocessing
│       │   ├── inference.py        # Engine inferensi ganda (Freshness + Defects)
│       │   └── preprocessor.py     # Letterbox padding & ROI extractor
│       ├── api/                    # Endpoint API versi 1
│       │   ├── deps.py             # Dependency injection session database
│       │   └── v1/                 # Router modular (inspections, lots, storage, dispatch, dll)
│       ├── core/                   # Koneksi SQLite & WebSocket Connection Manager
│       ├── hardware/               # Abstraksi GPIO & Logger Mock Controller
│       ├── models/                 # Model tabel SQLAlchemy (inspections, storage, dispatch)
│       ├── schemas/                # Skema validasi request/response Pydantic
│       └── services/               # Logika bisnis & Decision Engine
│
└── frontend/                       # Web Dashboard Next.js 16
    ├── Dockerfile                  # Multi-stage production container definition
    ├── package.json                # Dependensi React 19, Lucide, Tailwind CSS
    ├── app/                        # Next.js App Router
    │   ├── layout.tsx              # Shell layout utama (Sidebar + Topbar)
    │   ├── page.tsx                # Dashboard operasional utama
    │   ├── inspection/page.tsx     # Alur inspeksi kamera & live inference
    │   ├── history/page.tsx        # Tabel audit riwayat lot & filter
    │   ├── history/[lotId]/page.tsx# Detail inspeksi, BBoxes, catatan & human override
    │   ├── storage/page.tsx        # Lot Storage Map (Grid Cold & Frozen Zone)
    │   ├── dispatch/page.tsx       # Export Dispatch Management
    │   ├── dispatch/[dispatchId]/page.tsx # Detail manifes shipment & QC summary
    │   └── settings/page.tsx       # Konfigurasi Ambang Batas AI & Mode Mock
    ├── components/                 # Komponen modular UI (Atomic Design)
    ├── lib/                        # Client API Fetcher & WebSocket helper
    └── types/                      # Kontrak tipe TypeScript terpusat
```

---

<a id="panduan-pengaturan--instalasi-setup-guide"></a>
## 🚀 Panduan Pengaturan & Instalasi (Setup Guide)

### 📋 Prasyarat Lingkungan

- [Docker & Docker Compose](https://www.docker.com/) *(Sangat Disarankan)*
- [Git](https://git-scm.com/)
- *(Opsional untuk pengujian manual tanpa Docker)*: Python 3.11+ / [`uv`](https://github.com/astral-sh/uv), Node.js 20+ / [`pnpm`](https://pnpm.io/)

---

### METODE 1: Menjalankan via Docker Compose (Rekomendasi Utama Penilaian Juri) 🐳

Metode ini memungkinkan dewan juri menjalankan keseluruhan sistem (Backend FastAPI + Frontend Next.js 16 + SQLite DB + Mock Hardware) dalam **satu perintah** pada lingkungan terisolasi.

1. **Clone Repositori:**
```bash
git clone https://github.com/EvanCN10/nusaqc.git
cd nusaqc
```

2. **Jalankan Aplikasi dengan Docker Compose:**
```bash
docker compose up --build
```
*Docker Compose akan secara otomatis mem-build image backend dan frontend, memasang dependensi, memuat model ONNX, dan mengaktifkan Mock Hardware Mode.*

3. **Akses Layanan Aplikasi:**
- 🖥️ **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
- 📖 **Interactive API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- 🩺 **Backend Healthcheck:** [http://localhost:8000/health](http://localhost:8000/health)

4. **Menghentikan Aplikasi:**
```bash
docker compose down
```

---

### METODE 2: Menjalankan Secara Manual (Local Development)

#### A. Setup Backend (FastAPI + `uv` / `pip`)

1. Masuk ke direktori backend:
```bash
cd backend
```

2. Buat file konfigurasi `.env` dari template:
```bash
cp .env.example .env
```

3. Sinkronisasi dependensi dan jalankan server:
```bash
# Opsi 1: Menggunakan uv (cepat)
uv sync
uv run fastapi dev app/main.py --port 8000

# Opsi 2: Menggunakan pip standar & venv
python -m venv .venv
# Linux/macOS: source .venv/bin/activate | Windows: .venv\Scriptsctivate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
*Backend aktif di `http://localhost:8000`.*

#### B. Setup Frontend (Next.js 16 + `pnpm` / `npm`)

1. Buka terminal baru dan masuk ke direktori frontend:
```bash
cd frontend
```

2. Instal dependensi dan jalankan development server:
```bash
pnpm install
pnpm dev
# Atau jika menggunakan npm: npm install && npm run dev
```
*Frontend aktif di `http://localhost:3000`.*

---

<a id="spesifikasi-kontrak-rest-api--websocket"></a>
## 📡 Spesifikasi Kontrak REST API & WebSocket

Semua endpoint backend terdokumentasi interaktif di Swagger UI (`http://localhost:8000/docs`).

| HTTP Method | Endpoint Path | Deskripsi Fungsional | Parameter / Payload Utama |
|---|---|---|---|
| `POST` | `/api/v1/inspections/run` | Menjalankan inferensi AI snapshot pada citra ikan | Multipart: `image` (File), `family` (string) |
| `GET` | `/api/v1/lots` | Mengambil tabel riwayat inspeksi lot (filter & paginasi) | Query: `page`, `limit`, `grade`, `decision`, `family` |
| `GET` | `/api/v1/lots/recent` | Mengambil 5 lot inspeksi terkini untuk Dashboard | Query: `limit` (default: 5) |
| `GET` | `/api/v1/lots/{lot_id}` | Mengambil detail inspeksi lengkap (BBoxes, catatan, log) | Path: `lot_id` |
| `PATCH` | `/api/v1/lots/{lot_id}/note` | Menyimpan catatan audit manual Supervisor QC | JSON: `{ "note": "..." }` |
| `PATCH` | `/api/v1/lots/{lot_id}/override` | Override keputusan AI (Human-in-the-Loop) | JSON: `{ "decision": "PASS", "reason": "..." }` |
| `DELETE` | `/api/v1/lots/{lot_id}` | Menghapus rekaman lot & mengosongkan slot terkait | Path: `lot_id` |
| `GET` | `/api/v1/lots/export/csv` | Mengunduh rekapitulasi audit data QC ke format CSV | Query: `from`, `to`, `family` |
| `GET` | `/api/v1/storage/slots` | Mengambil seluruh slot penyimpanan (*Cold & Frozen*) | - |
| `GET` | `/api/v1/storage/pending` | Mengambil daftar lot PASS yang belum punya slot | - |
| `POST` | `/api/v1/storage/assign` | Mengalokasikan lot PASS ke slot penyimpanan fisik | JSON: `{ "slot_id": "C-01", "lot_id": "..." }` |
| `DELETE` | `/api/v1/storage/slots/{slot_id}` | Mengosongkan slot penyimpanan (*clear slot*) | Path: `slot_id` |
| `GET` | `/api/v1/dispatch` | Mengambil daftar riwayat dokumen pengiriman ekspor | - |
| `GET` | `/api/v1/dispatch/available-lots` | Mengambil daftar lot tersimpan yang siap diekspor | - |
| `GET` | `/api/v1/dispatch/{dispatch_id}` | Mengambil detail manifes pengiriman & QC summary | Path: `dispatch_id` |
| `POST` | `/api/v1/dispatch` | Membuat manifes pengiriman baru dari lot tersimpan | JSON: `{ "buyer_name", "destination", "lot_ids": [] }` |
| `PATCH` | `/api/v1/dispatch/{dispatch_id}/status` | Memperbarui status manifes (Pending / Dispatched) | JSON: `{ "status": "dispatched" }` |
| `GET` | `/api/v1/dispatch/{dispatch_id}/export` | Mengunduh ringkasan manifes dispatch ke CSV | Path: `dispatch_id` |
| `GET` | `/api/v1/dashboard/stats` | Menghitung statistik & metrik KPI lini QC harian | - |
| `GET` | `/api/v1/hardware/status` | Memeriksa status konektivitas perangkat & mode mock | - |
| `POST` | `/api/v1/hardware/test-connection` | Menguji latensi ping perangkat keras / kamera IP | JSON: `{ "ipAddress": "..." }` |
| `GET` | `/api/v1/settings/models/status` | Mengambil metadata & input shape model AI aktif | - |
| `GET` | `/api/v1/settings` | Mengambil konfigurasi global ambang batas & mock mode | - |
| `PUT` | `/api/v1/settings` | Menyimpan konfigurasi ambang batas keyakinan sistem | JSON: `{ "confidence_threshold": 0.85, ... }` |
| `WS` | `/ws/events` | Saluran WebSocket event siaran inspeksi real-time | Stream JSON Payload |

---

<a id="panduan-verifikasi--simulasi-pengujian-juri"></a>
## 🧪 Panduan Verifikasi & Simulasi Pengujian Juri

Dewan juri dapat memverifikasi seluruh fitur sistem secara langsung melalui antarmuka web:

1. **Uji Kasus 1: Inspeksi Ikan Segar (PASS)**
   - Buka menu **Inspection** di [http://localhost:3000/inspection](http://localhost:3000/inspection).
   - Pilih jenis ikan (misal: *Tuna*) dan unggah citra sampel ikan segar atau klik auto-inspect.
   - **Hasil Diharapkan:** Tampil lencana **PASS** (Hijau), Grade A/B, tanpa bounding box defek kritis. Pada terminal backend tercetak log: `[MOCK HARDWARE] [SIGNAL: GREEN] Conveyor Normal Speed`.
   - Buka menu **Lot Storage Map**; lot tersebut otomatis muncul di panel *Pending Storage* dan siap di-*assign* ke grid slot *Cold Zone*.

2. **Uji Kasus 2: Inspeksi Ikan Cacat / Terkontaminasi (FAIL)**
   - Unggah citra sampel ikan yang memiliki anomali visual (misal: luka robekan atau sisik sisa).
   - **Hasil Diharapkan:** Tampil lencana **FAIL** (Merah), overlay *bounding box* presisi di area cacat dengan skor keyakinan. Pada terminal backend tercetak log: `[MOCK HARDWARE] [SIGNAL: RED] RELAY CUT-OFF -> Conveyor Motor STOPPED | Siren: ACTIVE`.

3. **Uji Kasus 3: Human-in-the-Loop & Audit Override**
   - Buka menu **Lot History** di [http://localhost:3000/history](http://localhost:3000/history) dan klik tombol **View** pada salah satu lot.
   - Tambahkan catatan supervisor pada kolom **Inspector Note** dan klik **Save**.
   - Klik tombol **Override Decision**, ubah status menjadi PASS dengan alasan audit supervisor, dan verifikasi keputusan berhasil diperbarui di database.

4. **Uji Kasus 4: Rantai Keterlacakan Ekspor (Export Dispatch)**
   - Buka menu **Export Dispatch** di [http://localhost:3000/dispatch](http://localhost:3000/dispatch).
   - Klik tombol **"+ New Dispatch"**, masukkan nama buyer (misal: *Seatrade Japan Co.*), pilih negara tujuan, dan centang lot yang telah dialokasikan di storage.
   - Klik **"Create Dispatch"** dan verifikasi data pengiriman berhasil dibuat serta dapat diunduh via tombol **"Export CSV"**.

---

<a id="kepatuhan-terhadap-rulebook-aic-compfest-18"></a>
## 🛡️ Kepatuhan terhadap Rulebook AIC COMPFEST 18

Sistem NusaQC dirancang dengan mematuhi secara ketat seluruh batasan teknis **Babak Penyisihan**:

1. **Batasan Pemrosesan Sinkron (*Synchronous Snapshot*):** Inferensi AI dijalankan per pemicu snapshot citra tunggal, tanpa antrean background streaming yang melanggar batasan MVP penyisihan.
2. **Kemandirian Database Lokal:** Menggunakan SQLite zero-config yang tertanam di dalam container tanpa membutuhkan kluster basis data terdistribusi eksternal.
3. **Optimasi CPU & Portabilitas:** Seluruh model AI dieksekusi via ONNX Runtime CPU dengan bobot statis (*frozen weights*), memastikan sistem dapat berjalan lancar di berbagai mesin penguji tanpa GPU khusus.
4. **Kepatuhan Aturan Penilaian Anonim (*Blind Judging*):** Seluruh kode program, skema data, antarmuka pengguna, dan berkas dokumentasi telah dibersihkan dari logo, nama, maupun identitas perguruan tinggi.
5. **Integritas Ilmiah:** Memfokuskan cakupan deteksi mutu murni pada parameter fisik visual (*filthy*) dan organoleptik mata/insang sesuai batasan teknologi Computer Vision.

---

<a id="tim-pengembang"></a>
## 👥 Tim Pengembang

- **Praditya Haekal Islami A.H**
- **Evan Christian N.**
- **Jonathan Zelig Sutopo**
- **Rayka Dharma P.**
- **Rayhan Agnan Kusuma**

---
