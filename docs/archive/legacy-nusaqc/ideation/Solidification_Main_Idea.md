---
date_created: 2026-07-26T15:23
date_modified: 2026-07-26T23:15
---

# Outline Obsidian

```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
include: 
exclude: 
includeLinks: true # Make headings clickable
hideWhenEmpty: false # Hide TOC if no headings are found
debugInConsole: false # Print debug info in Obsidian console
```

---

# A. Permasalahan Utama

Berikut adalah beberapa berita dan publikasi studi kasus yang sangat relevan dengan topik permasalahan utama NusaQC (**penolakan ekspor perikanan Indonesia akibat kelemahan _Quality Control_, kontaminasi fisik/_filthy_, serta penurunan kesegaran di Unit Pengolahan Ikan**):

## 📰 Berita & Publikasi Relevan

### 1. Penolakan Ekspor Udang Beku RI oleh US FDA & Risiko Hambatan Pasar Ekspor

- **Poin Utama Berita:** Kasus penolakan dan penarikan (_recall_) kontainer produk perikanan (seperti udang beku) asal Indonesia oleh Badan Pengawas Obat dan Makanan Amerika Serikat (US FDA).
- **Dampak & Urgensi:** Pasar ekspor udang Indonesia ke AS bernilai sangat besar (mencapai USD 1,4–2 miliar per tahun). Penolakan kontainer secara beruntun memicu kekhawatiran besar di kalangan eksportir dan asosiasi industri (seperti APINDO) karena berisiko memicu ancaman larangan impor (_import ban_) serta pembekuan nomor registrasi ekspor UPI.
- **Relevansi dengan NusaQC:** Kasus ini menyoroti betapa ketatnya pengawasan standar keamanan pangan di negara tujuan ekspor. Kegagalan _Quality Control_ di lini pengolahan dapat berakibat fatal pada pengembalian kontainer secara masif.

### 2. Riset Historis: _Filthy_ (Kontaminasi Fisik) dan _Decomposition_ Menyumbang Mayoritas Kasus Penolakan

- **Poin Utama Riset (_Journal Analysis / Root Cause Analysis_):** Berdasarkan analisis data historis _FDA Import Refusal Logs_ dan studi _Root Cause Analysis_ ekspor perikanan Indonesia:
    - **Di Pasar Amerika Serikat (FDA):** _Filthy_ (kontaminasi fisik visual seperti sisik sisa, lendir abnormal, benda asing, dan kotoran) serta _Decomposition_ (pembusukan/penurunan kesegaran) secara konsisten menyumbang **porsi terbesar (~80%) dari total penolakan produk perikanan**.
    - **Di Pasar Uni Eropa (EU RASFF):** Penolakan didominasi oleh isu **Histamin** (akibat penurunan kesegaran/pembusukan ikan scrombidae seperti tuna dan cakalang) serta pencemaran mutu.
- **Relevansi dengan NusaQC:** Data empiris ini memvalidasi _grounding problem_ NusaQC bahwa akar masalah utama penolakan ekspor di pelabuhan tujuan berawal dari kecacatan fisik-organoleptik visual yang lolos saat inspeksi di meja sortasi pabrik.

### 3. Pengetatan Audit Mutu UPI oleh Otoritas Impor Internasional (GACC China & EU)

- **Poin Utama Berita (Badan Pengendalian Mutu KKP):** Otoritas luar negeri seperti GACC China dan Komisi Uni Eropa secara rutin membekukan (_suspend_) maupun mencabut izin ekspor Unit Pengolahan Ikan (UPI) di Indonesia jika ditemukan kegagalan penjaminan mutu pada sampel hasil pengolahan.
- **Relevansi dengan NusaQC:** Permasalahan ini mempertegas kebutuhan UPI akan pencatatan rekam jejak digital (_digital traceability_) yang terverifikasi dan siap diaudit secara transparan, menggantikan sistem pencatatan manual berbasis kertas (_paper-based logbook_) yang selama ini tidak transparan dan mudah dimanipulasi.

### 4. Tantangan _Highly Perishable_ & Kelelahan Operator Manual di Lini Pengolahan

- **Poin Utama Liputan Akademis (FPIK IPB & UGM):** Komoditas perikanan bersifat _highly perishable_ (sangat cepat membusuk). Kecepatan dan ketelitian pemeriksaan mutu di lini pascapanen menjadi kunci utama daya saing ekspor perikanan nasional.
- **Relevansi dengan NusaQC:** Mengingat tingginya kecepatan konveyor dan banyaknya jumlah ekor ikan yang diproses per shift, metode pengawasan manual dengan mata manusia terbukti mengalami _human visual fatigue_ dan menciptakan penumpukan (_throughput bottleneck_).

## 💡 Ringkasan Hubungan Kasus Berita dengan NusaQC

```
[ Temuan Berita Nyata ]                         [ Solusi Inovasi NusaQC ]
├─ Rejection FDA akibat Filthy & Cacat Visual ──> AI Surface Defect Detector (YOLOv8n)
├─ Pembusukan & Histamin Tuna di Pasar EU ─────> AI Freshness Classifier (SNI 2729:2013)
├─ Pencabutan Izin UPI / Ketatnya Audit GACC ──> SHA-256 Hash Cryptographic QR Certificate
└─ Bottleneck & Visual Fatigue Operator ────────> Real-time Offline Edge AI (<500ms Latency)
```

Data dan kasus penolakan nyata dari FDA maupun RASFF ini dapat dijadikan sebagai **argumen latar belakang (_urgency statement_) yang sangat kuat** pada proposal maupun _pitch deck_ lomba untuk membuktikan bahwa masalah yang diangkat NusaQC adalah masalah riil berskala industri bernilai triliunan rupiah.

---

# B. Data Faktual Permasalahan

Berikut adalah data faktual dari berita, laporan pemerintah, serta jurnal ilmiah yang membuktikan bahwa permasalahan yang diangkat oleh NusaQC adalah **masalah riil dan kritis di dunia industri perikanan nasional**:

## 1. Data Faktual Penolakan Ekspor (US FDA & EU RASFF)

- **Riset Universitas Gadjah Mada (UGM) tentang Penolakan Ekspor (2010–2020):**
    
    Studi analisis data historis ekspor perikanan Indonesia menunjukkan bahwa dalam periode 2010–2020 terdapat **2.318 kasus penolakan di Amerika Serikat (FDA)** dan **79 kasus di Uni Eropa (RASFF)**.
    
    - **Kategori Utama Penolakan:** Analisis Pareto dalam jurnal ilmiah ini membuktikan bahwa faktor **_filthy_** (kontaminasi fisik visual seperti kotoran, sisa sisik, lendir abnormal, parasit, dan benda asing) serta **_decomposition_** (pembusukan/penurunan kesegaran) menyumbang **porsi terbesar (~80–83%) dari total kasus penolakan ekspor di pasar Amerika Serikat**.
    - **Pasar Uni Eropa (EU RASFF):** Penolakan didominasi oleh isu **Histamin** (senyawa racun yang terbentuk akibat kegagalan penanganan kesegaran pada ikan scombroid seperti tuna/cakalang) serta _poor temperature control_.
- **Kasus Penolakan Lonjakan FDA (2024–2025):**
    
    Data analisis perdagangan laut mencatat kasus penolakan produk udang dan hasil laut Indonesia oleh US FDA mengalami lonjakan signifikan. Salah satu pemicunya adalah **kegagalan kontrol mutu fisik dan kontaminasi di tingkat _supplier_/Unit Pengolahan Ikan (UPI)** saat pemilahan bahan baku. Penolakan kontainer secara massal ini memicu pengembalian (_recall_), kerugian puluhan miliar rupiah, hingga ancaman pembekuan izin registrasi ekspor UPI.

## 2. Keterbatasan Inspeksi QC Manual di Lini Pabrik (UPI)

- **Kelelahan Visual Operator (_Human Visual Fatigue_):**
    
    Riset pengujian mutu organoleptik perikanan di Indonesia membuktikan bahwa uji organoleptik visual konvensional di meja sortasi sangat bergantung pada persepsi indra manusia. Operator pabrik yang memilah ribuan ekor ikan secara terus-menerus mengalami penurunan akurasi drastis setelah **2–3 jam kerja kontinu**, yang memicu tingginya angka _False Negative_ (ikan cacat/berlendir abnormal lolos ke kotak kemas ekspor).
    
- **Hambatan Kecepatan Produksi (_Throughput Bottleneck_):**
    
    Studi operasional lini pengolahan menunjukkan inspeksi manual secara teliti memerlukan waktu **5–15 detik per ekor**. Di lini konveyor yang bergerak cepat, kecepatan ini menjadi titik hambat (_bottleneck_) utama yang menurunkan efisiensi produksi pabrik.
    
- **Kendala Glare pada Permukaan Ikan Basah:**
    
    Di lingkungan basah UPI, pantulan cahaya (_glare/specular highlight_) pada permukaan kulit dan lendir ikan basah sering menyulitkan pengamatan mata telanjang maupun kamera standar, sehingga memerlukan metode khusus (_cross-polarization_) untuk menangkap tekstur cacat permukaan secara akurat.

## 3. Tuntutan Regulasi & Ketidakmampuan _Paper-Based Logbook_

- **Regulasi Ketat FDA SIMP & EU Traceability:**
    
    Otoritas pengawas impor internasional seperti US FDA (melalui _Seafood Import Monitoring Program_ / SIMP) dan Uni Eropa mewajibkan seluruh produk hasil laut memiliki rekam jejak digital (_digital traceability_) yang transparan dan dapat diverifikasi dari pintu masuk pabrik hingga pengiriman.
    
- **Resiko Pencatatan Manual (_Zero Traceability_):**
    
    Laporan evaluasi sanitasi dan mutu KKP menunjukkan bahwa mayoritas UPI skala menengah masih menggunakan **pencatatan borang kertas (_paper logbook_)**. Sistem berbasis kertas ini rentan hilang, mudah dimanipulasi, serta **tidak memiliki bukti digital terenkripsi** yang dapat diaudit oleh pembeli B2B internasional atau badan pengawas (BPOM/KKP).

## 💡 Kesimpulan Relevansi Dunia Kerja

Data-data faktual di atas menegaskan bahwa permasalahan yang diselesaikan oleh NusaQC adalah **krisis riil industri manufaktur perikanan nasional**:

```
[ Problem Industri Nyata ]                        [ Solusi Terbukti NusaQC ]
├─ 80% Penolakan FDA akibat Filthy & Cacat ─────> AI Surface Defect Detector (YOLOv8n)
├─ Pembusukan & Histamin di Pasar EU/US ─────────> AI Freshness Classifier SNI 2729:2013
├─ Human Visual Fatigue & Throughput Bottleneck ─> Automated Edge AI Snapshot (<500ms)
└─ Audit Penolakan akibat Paper Logbook ─────────> Cryptographic SHA-256 PDF Certificate
```

---

# C. UPI Surabaya

Berikut adalah rekomendasi **Unit Pengolahan Ikan (UPI) skala ekspor terdekat dari Surabaya/ITS** yang sangat ideal untuk kebutuhan observasi, riset, maupun wawancara proyek NusaQC.

Pabrik-pabrik ini berlokasi di tiga zona industri utama perikanan Jawa Timur (**Surabaya, Sidoarjo, dan Gresik**) yang mudah dijangkau dari kampus ITS.

## 🏭 Top Rekomendasi UPI & Industri Perikanan Target

### 1. PT Bumi Menara Internusa (BMI) – Surabaya Unit

- **Lokasi:** Jl. Margomulyo No. 4E, Tandes, Surabaya (~30–45 menit dari ITS).
- **Komoditas Utama:** Udang, Ikan Beku, dan Kepiting (_Seafood Exporter_ utama ke AS, Uni Eropa, & Jepang).
- **Mengapa Sangat Direkomendasikan?**
    - BMI adalah **salah satu eksportir produk laut terbesar di Indonesia**.
    - Standar _Quality Control_ (QC) mereka sangat ketat (HACCP, BRCGS, US FDA Compliant).
    - Lini produksi mereka menggunakan sistem konveyor berkecepatan tinggi dengan proses sortasi yang ideal untuk mengamati fenomena _human visual fatigue_ dan kendala pencatatan log.

### 2. PT Kelola Mina Laut (KML Food) – Gresik

- **Lokasi:** Kawasan Industri Gresik (KIG), Jl. KIG Raya Selatan, Gresik (~45–60 menit via Tol Dupak/Gresik).
- **Komoditas Utama:** Ikan Segar & Beku (_Snapper_, _Grouper_, _Mackerel_, Tuna), _Cephalopods_ (Cumi/Gurita), dan _Surimi_.
- **Mengapa Sangat Direkomendasikan?**
    - KML Food fokus pada **komoditas ikan utuh dan fillet**, sangat relevan dengan pengujian klasifikasi kesegaran (_Freshness Grading_) berbasis **SNI 2729:2013** pada NusaQC.
    - Mereka sangat terbuka terhadap kolaborasi akademis dan sering menerima mahasiswa riset/magang dari kampus-kampus di Jawa Timur.

### 3. PT Sekar Bumi Tbk – Sidoarjo

- **Lokasi:** Jl. Jenggolo No. 51, Waru / Buduran, Sidoarjo (~35–45 menit dari ITS via Tol Waru).
- **Komoditas Utama:** Udang Beku dan _Value-Added Seafood_ (merek FINNA).
- **Mengapa Sangat Direkomendasikan?**
    - Perusahaan _go-public_ (Tbk) dengan manajemen _supply chain_ dan QC berbasis standar internasional.
    - Memiliki lini pengolahan berskala besar dengan meja sortasi konvensional yang cocok dijadikan _benchmark_ otomatisasi _Smart Manufacturing_.

### 4. PT Alter Trade Indonesia (ATINA) – Sidoarjo

- **Lokasi:** Buduran, Sidoarjo (~35 menit dari ITS).
- **Komoditas Utama:** Udang Windu Organik (_Eco-Shrimp_) untuk pasar ekspor Jepang dan Eropa.
- **Mengapa Sangat Direkomendasikan?**
    - Menekankan pada **keterusutan rantai pasok (_traceability_) tingkat tinggi** dari tambak hingga kemasan ekspor.
    - Sangat cocok untuk melakukan wawancara terkait kebutuhan sertifikat digital terenkripsi (QR Code/Hash) yang menjadi salah satu fitur utama NusaQC.

## 🏛️ Alternatif Instansi Pemerintah (Akses Mudah & Cepat)

Jika mengurus surat izin masuk ke pabrik swasta membutuhkan waktu beberapa hari, Anda bisa mendatangi **instansi pengawas mutu perikanan resmi** berikut terlebih dahulu untuk wawancara ahli (_expert interview_):

### UPT Laboratorium Pengujian dan Penerapan Mutu Hasil Perikanan (LPPMHP) Surabaya

- **Lokasi:** Jl. Gayung Kebonsari No. 50, Gayungan, Surabaya (~30 menit dari ITS).
- **Instansi:** Dinas Kelautan dan Perikanan (DKP) Provinsi Jawa Timur.
- **Keunggulan untuk Wawancara:**
    - Tempat di mana para **inspektur mutu perikanan dan penguji organoleptik resmi** bekerja.
    - Anda bisa mendapatkan data riil mengenai kriteria penolakan ekspor, standar pengujian organoleptik SNI 2729:2013, serta masukan teknis mengenai parameter cacat visual ikan tanpa perlu menunggu izin masuk pabrik.

## 💡 Taktik Pendekatan (_Outreach Strategy_) Mahasiswa

1. **Gunakan "Almamater Pass":** Pengajuan riset dengan nama **ITS (Institut Teknologi Sepuluh Nopember)** memiliki tingkat keberterimaan (_acceptance rate_) yang sangat tinggi di kawasan industri Jatim.
2. **Jalur Person In Charge (PIC):**
    
    - Kirimkan surat pengantar resmi dari Departemen ke divisi **HRD / Manager QA (Quality Assurance) / Manager Plant**.
    - Opsi yang sering berhasil: Hubungi alumni ITS yang bekerja di perusahaan target via LinkedIn (cari dengan kata kunci: _"QA Manager PT Bumi Menara Internusa ITS"_ atau _"Quality Control PT KML Food ITS"_).
        
3. **Poin Penawaran (_Value Proposition_):** Tekankan bahwa Anda tidak sedang mengevaluasi kerahasiaan resep/proses bisnis mereka, melainkan **melakukan observasi akademis mengenai digitalisasi QC dan ergonomi meja sortasi**.

Apakah Anda ingin saya bantu buatkan draf **surat/pesan pengantar resmi (surat permohonan observasi)** yang singkat dan profesional untuk dikirimkan ke pihak manajemen UPI?

---

# D. Design Thinking

Berikut adalah dokumen **Design Thinking NusaQC Versi Terbaru** yang telah disesuaikan 100% dengan aturan dan batasan ruang lingkup penyisihan **Rulebook COMPFEST 18 AI Innovation Challenge (AIC)**.

Penyesuaian ini memisahkan secara tegas antara **Scope MVP Penyisihan** (_Single-Page UI_, Pemrosesan Sinkron, _Core AI_, _GPIO Actuation_, dan _Mock Data Mode_) dengan **Roadmap Babak Final** (_Database Logging_, _PDF Certificate_, dan _Cloud Sync_) agar repositori timmu bebas dari risiko penalti nilai _overbuilt_ pada kriteria **Kesiapan MVP (Bobot 15%)**.

## 🎨 Design Thinking NusaQC (Versi Strict Guidebook COMPFEST 18 AIC)

### 👥 1. FASE 1: EMPATHIZE (Memahami Pengguna di Dunia Nyata)

Fase empati tetap mengeksplorasi kondisi nyata di meja sortasi Unit Pengolahan Ikan (UPI) untuk membangun fondasi masalah yang kuat pada Proposal PDF (memenuhi kriteria **Orisinalitas & Dampak Sosial - 20%**).

#### A. Persona 1: Operator Meja Sortasi (Budi, 28 Tahun)

- **Lingkungan Kerja:** Memilah ribuan ekor ikan per _shift_ di atas konveyor bergerak, area basah, dingin, dan bising.
- **Says:** _"Mata saya perih kalau memilah ikan dari pagi sampai sore. Tangan saya basah pakai sarung tebal, susah kalau harus pencet keyboard atau layar."_
- **Thinks:** _"Takut salah membedakan cacat luka dengan kilauan air basah di bawah lampu. Jangan sampai ada ikan busuk yang lolos."_
- **Does:** Memilah ikan 5–15 detik/ekor. Mengalami penurunan akurasi visual (_visual fatigue_) setelah 2–3 jam kerja kontinu.
- **Feels:** Lelah mata, cemas, dan tertekan oleh kecepatan konveyor.

#### B. Persona 2: Quality Assurance (QA) Manager (Pak Hendra, 42 Tahun)

- **Lingkungan Kerja:** Kantor administrasi mutu dan area audit ekspor UPI.
- **Says:** _"Kalau 1 kontainer ditolak FDA/RASFF gara-gara filthy atau busuk, rugi ratusan juta dan izin ekspor pabrik bisa dibekukan!"_
- **Thinks:** _"Bagaimana cara membuktikan ke buyer dan auditor bahwa inspeksi di meja sortasi kami konsisten dan objektif?"_
- **Does:** Memeriksa lembar logbook kertas manual. Tertekan oleh risiko _import refusal_.
- **Feels:** Khawatir akan manipulasi data manual dan penolakan kargo ekspor.

### 🎯 2. FASE 2: DEFINE (Rumusan Masalah & Need Statements)

#### Point of View (POV) Statements

- **Operator Meja Sortasi:** "Operator meja sortasi **membutuhkan** sistem penandaan ikan cacat yang berjalan otomatis tanpa sentuhan tangan (_zero-touch_) dan tanpa memaksa mereka terus menatap layar monitor, **karena** mata mereka mengalami kelelahan visual (_visual fatigue_) dan tangan mereka basah/bersarung tebal."
- **QA Manager:** "QA Manager **membutuhkan** standar inspeksi visual AI yang presisi dengan _recall_ tinggi, **karena** metode manual terbukti subjektif dan berisiko meloloskan ikan cacat ke kargo ekspor."

#### Pernyataan _How Might We_ (HMW) & Solusi

1. **HMW** memberi tahu operator ada ikan cacat tanpa mereka harus menatap layar monitor? $\rightarrow$ **Solusi:** _Closed-Loop GPIO Actuator Integration_ (Sinyal alarm _Siren & LED_ otomatis aktif via GPIO saat _REJECT_).
2. **HMW** menghilangkan kesalahan deteksi AI akibat kilau (_glare_) air pada kulit ikan basah? $\rightarrow$ **Solusi:** _Cross-Polarization Lens Filter Hardware Spec_.
3. **HMW** memastikan panitia/juri lomba dapat menguji sistem secara utuh tanpa memiliki perangkat keras fisik? $\rightarrow$ **Solusi:** **Mock Data Mode Toggle Switch** pada antarmuka tunggal.

### 💡 3. FASE 3: IDEATE (Curah Ide & Pemisahan Ruang Lingkup)

Pada tahap ini, ide solusi dipisahkan secara tegas mengikuti aturan **Rulebook COMPFEST 18 AIC (Hal. 15 & 18)**:

```
┌─────────────────────────────────────────────────────────────────┐
│ A. SCOPE MVP BABAK PENYISIHAN (Strict Rules Compliant)          │
│    • Single-Page Core UI (Input Gambar/Snapshot → Output AI)   │
│    • Synchronous FastAPI Backend (`/predict` endpoint)          │
│    • Static Dual ONNX Model (MobileNetV3 INT8 + YOLOv8n Float32)│
│    • Mock Data Mode Switch (Testing tanpa hardware kamera/IR)   │
│    • Closed-Loop GPIO Relay Signal (Output Siren & LED Alarm)   │
│    • Docker Compose Deployment & README.md Setup Guide          │
└────────────────────────────────────┬────────────────────────────┘
                                     │
                                     ▼ (Disimpan untuk Final)
┌─────────────────────────────────────────────────────────────────┐
│ B. ROADMAP BABAK FINAL (Hackathon 10 Jam di Fasilkom UI)        │
│    ❌ SQLite Local Audit Database & Automated Data Logging      │
│    ❌ Automated PDF Quality Certificate Generator (SHA-256 QR)   │
│    ❌ End-of-Shift Cloud Batch Synchronization                   │
│    ❌ Dashboard Analitik & History Log Page                     │
└─────────────────────────────────────────────────────────────────┘
```

### 🛠️ 4. FASE 4: PROTOTYPE (Perancangan Prototipe Penyisihan)

Prototipe babak penyisihan dibangun dengan arsitektur **Interaksi Sinkron Tunggal (_Synchronous Single-Interaction_)**:

```
[ INPUT LAYER ]                     [ SYNCHRONOUS BACKEND LAYER ]             [ OUTPUT LAYER ]
 (Single Image)                      (FastAPI + ONNX Runtime)                 (Single-Page UI)
┌──────────────────────────────┐    ┌───────────────────────────────────┐    ┌──────────────────────────────┐
│ • Upload Foto (.jpg/.png)    │    │ 1. Pre-processing (ROI Crop)      │    │ • Visual Bounding Box Overlay│
│ • IR Sensor Camera Snapshot  │───>│ 2. Freshness Classifier (INT8)    │───>│ • SNI Grade & Confidence Score│
│ • [TOGGLE] MOCK DATA MODE    │    │ 3. Defect Detector (Float32)      │    │ • Large PASS/REJECT Banner   │
└──────────────────────────────┘    │ 4. GPIO Signal Output Trigger     │    │ • Audio Siren / LED Signal   │
                                    └───────────────────────────────────┘    └──────────────────────────────┘
```

#### Komponen Detail Prototipe Penyisihan:

1. **Frontend (Single-Page App):**
    
    - Berfokus hanya pada 1 halaman interaksi.
    - Menyediakan area unggah foto / tombol _snapshot_ dan sakelar **Mock Data Mode Switch**.
    - Menampilkan hasil prediksi AI secara instan berupa _overlay bounding box_, label kesegaran SNI 2729:2013, serta _banner_ status **PASS** (hijau) / **REJECT** (merah)[cite: 1, 3].
        
2. **Backend (FastAPI Synchronous Endpoint):**
    
    - Endpoint `/predict` menerima request citra masukan $\rightarrow$ memproses _Core AI_ secara sinkron $\rightarrow$ mengembalikan respons JSON & pemicuan sinyal GPIO dalam 1 siklus _request-response_.
    - **TIDAK ADA** _background jobs_, _automated database logging_, atau _cloud sync pipeline_ (100% _clean synchronous backend_).
        
3. **Core AI Models (Static Parameter):**
    
    - _Freshness Classifier:_ MobileNetV3-Small INT8 terkalibrasi baku mutu **SNI 2729:2013**[cite: 1, 2, 3].
    - _Surface Defect Detector:_ YOLOv8n Float32 untuk deteksi cacat fisik permukaan[cite: 1, 2, 3].
        
4. **Mock Data Mode (Mandatory Rulebook Hal. 18):**
    
    - Saat sakelar _Mock Data_ diaktifkan, backend mengambil sampel gambar lokal dari direktori `/mock_samples` untuk mengeksekusi inferensi penuh tanpa memerlukan ketersediaan fisik kamera/sensor IR.
        
5. **Infrastructure Deployment:**
    
    - Seluruh aplikasi dibungkus dalam **Docker Compose** dan dapat dijalankan di _localhost_ panitia via perintah `docker compose up` berdasarkan petunjuk di file `README.md`.

### 🧪 5. FASE 5: TEST (Pengujian & Validasi Metrik Penyisihan)

Pengujian prototipe penyisihan difokuskan pada keandalan _core inference_ AI, kecepatan latensi sinkron, serta kestabilan _Mock Data Mode_[cite: 2, 3]:

|**Parameter Pengujian**|**Target Metrik**|**Metode Pengujian**|**Status Compliance Rulebook**|
|---|---|---|---|
|**Defect Recall (YOLOv8n)**|$\ge 85\%$|Evaluasi matrik konfusi pada _test set_ terpisah ($N \ge 200$).|✅ Memenuhi Kriteria Teknologi (25%).|
|**Freshness F1-Score (MobileNetV3)**|$\ge 85\%$|Uji _weighted F1-Score_ terhadap _ground truth_ SNI 2729:2013.|✅ Memenuhi Kriteria Teknologi (25%).|
|**Synchronous Latency**|$< 500\text{ ms/ekor}$|Pengukuran waktu _request-response_ sinkron API lokal[cite: 2, 3].|✅ Memenuhi Kriteria Kesiapan MVP (15%).|
|**Mock Data Mode Reliability**|$100\%$ Functional|Pengujian eksekusi aplikasi tanpa perangkat keras terpasang.|✅ **Mandatory Rulebook (Hal. 18)**.|
|**Docker Compose Execution**|Zero Error|Pengujian perintah `docker compose up` pada lingkungan bersih.|✅ **Mandatory Rulebook (Hal. 15)**.|

## 📌 Kesimpulan Penyelarasan Tim

1. **Pada Proposal PDF:** Paparkan narasi _Design Thinking_ secara utuh (termasuk latar belakang masalah penolakan FDA, kelelahan mata operator, hingga rencana _roadmap_ sertifikasi digital PDF) untuk memaksimalkan poin **Orisinalitas & Dampak Sosial (20%)** serta **Relevansi Tema (10%)**.
2. **Pada Repositori Kode GitHub:** Batasi kode **HANYA** pada _Single-Page UI_, _Synchronous Backend_, _Static Dual ONNX AI_, _Closed-Loop GPIO Relay_, dan **Mock Data Mode Switch** yang berjalan via _Docker Compose_. Hal ini menjamin nilai sempurna pada kriteria **Kesiapan MVP (15%)** tanpa terkena penalti _overbuilt_.

---

# E. Jobs to be Done

Berikut adalah analisis **Jobs To Be Done (JTBD)** NusaQC yang telah disesuaikan 100% dengan aturan dan batasan **Rulebook COMPFEST 18 AI Innovation Challenge (AIC)**.

Analisis ini membedakan secara tegas antara **kebutuhan nyata pengguna di dunia kerja (yang dituangkan dalam Proposal PDF untuk poin _Dampak Sosial - 20%_)** dengan **pembagian eksekusi fitur (_Phasing Execution_) pada Babak Penyisihan vs. Babak Final** agar repositori kode timmu aman dari penalti _overbuilt_ (Rulebook Halaman 15 & 18).

## 🎯 Core Job Statement (Tugas Utama Sistem)

> **"Ketika** memproses komoditas perikanan pasca-pemanenan di lini konveyor Unit Pengolahan Ikan (UPI) ekspor, **kami ingin** menginspeksi mutu fisik-organoleptik ikan secara otomatis, cepat, dan terukur secara lokal, **agar kami dapat** meminimalisasi _False Negative_ (ikan cacat/busuk lolos ke kemasan ekspor) yang berisiko memicu penolakan kontainer oleh otoritas impor global (US FDA / EU RASFF)."

## 👥 Analisis JTBD per Persona & Pembagian Eksekusi (Phasing)

### 1. Primary User: Operator Meja Sortasi (Budi, 28 Tahun)

- **Peran:** Lini operasional pemilahan ikan di area basah, dingin, dan bising.

#### A. Main JTBD Statement

> _"**When** sorting thousands of wet, slippery fish on a fast-moving conveyor under harsh factory lighting, **I want to** receive instant, zero-touch audio-visual alerts whenever a defective or rotten fish passes by, **so I can** separate reject fish immediately without straining my eyes, staring at screens, or touching electronic devices with my wet/gloved hands."_

#### B. Tiga Dimensi Jobs

- **Functional Job:** Memilah ikan cacat (_filthy_, luka, lendir abnormal, Grade C) dalam latensi sinkron $< 500\text{ ms}$ per ekor tanpa harus menyentuh layar/keyboard.
- **Emotional Job:** Bebas dari kelelahan mata (_human visual fatigue_) dan rasa cemas akan ikan busuk yang tidak sengaja terlewat.
- **Social Job:** Dianggap sebagai operator lini yang tangkas, presisi, dan berkinerja tinggi oleh supervisor pabrik.

#### C. Status Eksekusi dalam Kompetisi:

- ✅ **100% TERPENUHI DI BABAK PENYISIHAN:**
    - Dijawab dengan: _Single-Page UI_ + _Synchronous FastAPI Backend_ + _Static Dual ONNX AI_ + _Closed-Loop GPIO Relay Siren/LED Alarm_.

### 2. Secondary User: Quality Assurance (QA) Manager (Pak Hendra, 42 Tahun)

- **Peran:** Lini manajerial penanggung jawab kepatuhan standar mutu dan audit ekspor UPI.

#### A. Main JTBD Statement

> _"**When** managing quality compliance for export batches, **I want** an objective AI-powered visual inspection standard on the sorting table, **so I can** ensure zero defective products enter export containers and protect the factory's export registration status."_

#### B. Tiga Dimensi Jobs

- **Functional Job:** Mengeliminasi subjektivitas penilaian kesegaran manual dan memastikan standar kesegaran SNI 2729:2013 serta deteksi cacat fisik berjalan konsisten dengan _Recall_ $\ge 85\%$.
- **Emotional Job:** Merasa tenang dan percaya diri bahwa mutu produk di meja sortasi terinspeksi secara objektif.
- **Social Job:** Dikenal sebagai Manajer QA visioner yang berhasil mentransformasi lini pabrik menjadi _Smart Manufacturing_.

#### C. Status Eksekusi dalam Kompetisi (DIBAGI MENJADI 2 FASE):

- 🟡 **Fase 1 (Babak Penyisihan):** Dijawab dengan _Real-time Visual Overlay (Bounding Box & Grade SNI)_ dan _Status Banner PASS/REJECT_ berukuran besar pada antarmuka tunggal.
- 🔵 **Fase 2 (Babak Final / Hackathon 10 Jam):** Dijawab dengan modul _Automated Local Audit Logging (SQLite)_ dan _PDF Certificate Generator (SHA-256 QR Code)_.

### 3. Tertiary Stakeholder: Juri / Panitia COMPFEST 18 AIC (Evaluator Lomba)

- **Peran:** Penilai teknis reprodusibilitas dan kelayakan produk.

#### A. Main JTBD Statement

> _"**When** evaluating and testing the submission repository locally, **I want to** run the application seamlessly on localhost without hardware dependencies using a mock testing mode, **so I can** verify the working status of the core AI inference and architecture easily."_

#### B. Status Eksekusi dalam Kompetisi:

- ✅ **MANDATORY DI BABAK PENYISIHAN (Rulebook Hal. 18):**
    - Dijawab dengan: **Mock Data Mode Toggle Switch** di antarmuka tunggal + _Docker Compose Deployment_ + Panduan _Setup_ di `README.md`.

## 🔄 Matriks Four Forces Framework (Dinamika Psikologis JTBD)

Dinamika dorongan pengguna dialokasikan dengan menambahkan _force_ khusus terkait aturan perlombaan:

```
                       DORONGAN KEMAJUAN (PROGRES)
                                    ▲
                                    │
    [ 1. PUSH OF THE PRESENT ]      │      [ 2. PULL OF THE NEW SOLUTION ]
    • Kelelahan visual operator     │      • Closed-loop alarm siren/LED
    • Kerugian penolakan FDA/RASFF  │      • Single-page instant visual overlay
    • Pencatatan manual tidak valid │      • Static Dual ONNX (<500ms latency)
                                    │
 ───────────────────────────────────┼───────────────────────────────────
                                    │
    [ 3. ANXIETY OF NEW SOLUTION ]  │      [ 4. HABIT OF THE PRESENT ]
    • "Apakah alat rusak kena air?" │      • Kebiasaan nulis di papan jepit
    • "Apakah AI butuh internet?"   │      • Enggan pakai touchscreen rumit
    • NEW: "Apakah juri bisa meng- │
      uji tanpa hardware fisik?"   │
                                    │
                                    ▼
                      HAMBATAN KEMAJUAN (RETENTION)
```

### Penanganan Four Forces dalam NusaQC:

1. **Push:** Diangkat dalam Proposal PDF sebagai urgensi masalah penolakan ekspor FDA akibat _filthy_ dan kelelahan mata operator.
2. **Pull:** Dijawab dengan solusi _Closed-Loop GPIO Actuator_ dan _Core AI Inference_ berbasis baku mutu SNI 2729:2013.
3. **Anxiety:**
    
    - _Kecemasan Pabrik (Air & Internet):_ Dijawab dengan spesifikasi _enclosure_ IP69K dan operasi _100% Offline-First_.
    - _Kecemasan Juri (Hardware-less Testing):_ Dijawab dengan ketersediaan **Mock Data Mode Switch** pada antarmuka tunggal.
        
4. **Habit:** Dijawab dengan prinsip **Zero-Touch**: Operator tidak perlu mengetik atau menyentuh layar saat proses sortasi berlangsung.

## 📊 Matriks Pemetaan JTBD vs. Penyelarasan Rulebook

| **User Need (JTBD)**                     | **Solusi Fitur NusaQC**                        | **Alokasi Scope Penyisihan (MVP)** | **Alokasi Scope Final / Roadmap** | **Rulebook Compliance (Rulebook Hal. 15 & 18)**                              |
| ---------------------------------------- | ---------------------------------------------- | ---------------------------------- | --------------------------------- | ---------------------------------------------------------------------------- |
| **Pemilahan Cacat Tanpa Menatap Layar**  | Closed-Loop GPIO Relay Alarm Siren & LED       | ✅ **Termasuk di Penyisihan**       | -                                 | **Compliant:** Sinyal keluaran sinkron langsung dari AI.                     |
| **Inspeksi Kesegaran SNI & Cacat Fisik** | Static Dual ONNX Model (MobileNetV3 + YOLOv8n) | ✅ **Termasuk di Penyisihan**       | -                                 | **Compliant:** _Core inference_ dengan parameter statis.                     |
| **Pengujian Aplikasi Tanpa Hardware**    | Mock Data Mode Switch                          | ✅ **Termasuk di Penyisihan**       | -                                 | **Mandatory:** Wajib ada untuk pengujian panitia (Hal. 18).                  |
| **Kemudahan Deployment Lokal**           | Docker Compose & README Setup Guide            | ✅ **Termasuk di Penyisihan**       | -                                 | **Mandatory:** Syarat wajib repositori GitHub (Hal. 15 & 20).                |
| **Bukti Audit & Sertifikat Digital**     | Local SQLite Log DB & SHA-256 PDF Certificate  | ❌ **Dikeluarkan dari Penyisihan**  | ✅ **Dikerjakan di Final**         | **Compliant:** Dilarang ada _automated data logging pipeline_ di penyisihan. |
| **Analisis Tren Mutu Pabrik**            | Dashboard Analitik & History Log Page          | ❌ **Dikeluarkan dari Penyisihan**  | ✅ **Future Roadmap**              | **Compliant:** Dilarang ada _history page_ / _analytics_ di penyisihan.      |

---

# F. Functional Requirements 

Berikut adalah **Spesifikasi Kebutuhan Fungsional (_Functional Requirements_) NusaQC Versi Penyisihan COMPFEST 18 AIC** yang disesuaikan secara ketat terhadap batasan _Rulebook_ (Halaman 15 & 18) dan disusun menggunakan standar **ISO/IEC/IEEE 29148:2018**.

Seluruh fitur yang tergolong _overbuilt_ (seperti _dashboard_ analitik, halaman riwayat log, _database logging pipeline_, _background jobs_, dan _cloud sync_) telah **dihapus**, serta digantikan dengan fungsionalitas **Interaksi Sinkron Tunggal** dan **Mock Data Mode**.

## 📑 Tabel Spesifikasi Kebutuhan Fungsional (FR) — Strictly Rulebook Compliant

|**ID Kebutuhan**|**Modul / Kategori**|**Pernyataan Kebutuhan Fungsional (ISO/IEC/IEEE 29148)**|**Kriteria Lolos / Metode Pengujian**|
|---|---|---|---|
|**FR-INP-01**|Akuisisi Input|Sistem harus menerima masukan tunggal dari pengguna berupa unggahan berkas citra lokal atau pemicuan _snapshot_ citra dari kamera _overhead_.|Pengguna dapat mengunggah 1 foto atau mengambil 1 _snapshot_ gambar secara langsung.|
|**FR-INP-02**|Akuisisi Input _(Mock Mode)_|Sistem harus menyediakan **Mock Data Mode** yang memungkinkan aplikasi berjalan menggunakan sampel data/gambar lokal tanpa ketergantungan pada perangkat keras fisik.|Sistem dapat mengeksekusi inferensi penuh menggunakan citra _mock_ lokal saat perangkat keras tidak terhubung.|
|**FR-AI-01**|Core AI Inference|Sistem harus melakukan pemotongan area fokus (_ROI extraction_) pada bagian mata dan insang dari citra input secara otomatis sebelum klasifikasi kesegaran.|Pemotongan ROI mata dan insang berhasil dilakukan pada citra masukan.|
|**FR-AI-02**|Core AI Inference|Sistem harus mengklasifikasikan kesegaran ikan ke dalam **Grade A**, **Grade B**, atau **Grade C** menggunakan model terkalibrasi **SNI 2729:2013** (MobileNetV3-Small INT8)[cite: 1, 2, 3].|Parameter model bersifat statis dan menghasilkan nilai _grade_ serta _confidence score_[cite: 1, 2, 3].|
|**FR-AI-03**|Core AI Inference|Sistem harus memindai dan mendeteksi cacat/luka permukaan serta menghasilkan koordinat _bounding box_ ternormalisasi ($0.0\text{–}1.0$) menggunakan model YOLOv8n (Float32)[cite: 1, 2, 3].|_Bounding box_ dan label kelas cacat fisik berhasil dihasilkan[cite: 1, 2, 3].|
|**FR-AI-04**|Core AI Inference|Sistem harus menghitung logika keputusan mutu secara langsung: **"REJECT"** jika cacat $> 0$ ATAU kesegaran **"Grade C"**; serta **"PASS"** jika ikan segar (Grade A/B) dan bebas cacat.|Keputusan _PASS/REJECT_ dihasilkan secara konsisten sesuai aturan logika.|
|**FR-OUT-01**|Pemrosesan Sinkron|Sistem harus mengembalikan seluruh hasil inferensi (overlay _bounding box_, label _grade_, _confidence score_, dan status keputusan mutu) dalam 1 respons API sinkron.|Respons JSON/API diterima oleh antarmuka dalam 1 siklus _request-response_ sinkron.|
|**FR-OUT-02**|Pemrosesan Sinkron|Sistem harus mengarahkan sinyal keluaran status (**PASS** / **REJECT**) secara sinkron ke antarmuka visual dan/atau indikator aktuator[cite: 1, 3].|Indikator keluaran berubah status secara instan mengikuti hasil keputusan mutu[cite: 1, 3].|
|**FR-UI-01**|Single-Page UI|Antarmuka pengguna harus berfokus **HANYA** pada halaman tunggal yang menerima input dari pengguna dan menampilkan output dari AI.|Antarmuka tidak memiliki bilah navigasi ke halaman riwayat, _analytics_, atau fitur otentikasi kompleks.|
|**FR-UI-02**|Single-Page UI|Antarmuka pengguna harus menampilkan _visual overlay_ berupa kotak pembatas (_bounding box_) cacat permukaan dan label kesegaran SNI tepat di atas citra masukan[cite: 1, 3].|_Overlay_ visual ter-render tepat di atas objek citra yang diinspeksi[cite: 1, 3].|
|**FR-UI-03**|Single-Page UI|Antarmuka pengguna harus menampilkan banner indikator keputusan mutu berukuran besar dengan warna kontras (**PASS** berwarna hijau / **REJECT** berwarna merah)[cite: 1, 3].|Banner status berubah warna secara kontras sesuai hasil keputusan AI[cite: 1, 3].|
|**FR-UI-04**|Single-Page UI|Antarmuka pengguna harus menyediakan sakelar tombol (_toggle switch_) untuk mengaktifkan atau mematikan **Mock Data Mode** dengan mudah saat demonstrasi.|Pengguna dapat berpindah antara _Live/Hardware Mode_ dan _Mock Data Mode_ melalui 1 tombol.|

## 📌 Catatan Penyelarasan Teknis:

1. **Penyederhanaan Arsitektur:** Tidak ada modul _Database_, _Background Workers_, atau _Certificate PDF Generator_ dalam tabel ini untuk menjamin repositori tahap penyisihan **100% mematuhi batasan Rulebook COMPFEST 18 AIC (Hal. 15)**.
2. **Setup Execution:** Seluruh FR di atas wajib dapat dieksekusi secara lokal di server panitia menggunakan perintah `docker compose up` berdasarkan petunjuk di file `README.md`.

---

# G. Non-Functional Requirements

Berikut adalah **Spesifikasi Kebutuhan Fungsional (_Functional Requirements_) NusaQC Versi Penyisihan COMPFEST 18 AIC** yang disesuaikan secara ketat terhadap batasan _Rulebook_ (Halaman 15 & 18) dan disusun menggunakan standar **ISO/IEC/IEEE 29148:2018**.

Seluruh fitur yang tergolong _overbuilt_ (seperti _dashboard_ analitik, halaman riwayat log, _database logging pipeline_, _background jobs_, dan _cloud sync_) telah **dihapus**, serta digantikan dengan fungsionalitas **Interaksi Sinkron Tunggal** dan **Mock Data Mode**.

## 📑 Tabel Spesifikasi Kebutuhan Fungsional (FR) — Strictly Rulebook Compliant

|**ID Kebutuhan**|**Modul / Kategori**|**Pernyataan Kebutuhan Fungsional (ISO/IEC/IEEE 29148)**|**Kriteria Lolos / Metode Pengujian**|
|---|---|---|---|
|**FR-INP-01**|Akuisisi Input|Sistem harus menerima masukan tunggal dari pengguna berupa unggahan berkas citra lokal atau pemicuan _snapshot_ citra dari kamera _overhead_.|Pengguna dapat mengunggah 1 foto atau mengambil 1 _snapshot_ gambar secara langsung.|
|**FR-INP-02**|Akuisisi Input _(Mock Mode)_|Sistem harus menyediakan **Mock Data Mode** yang memungkinkan aplikasi berjalan menggunakan sampel data/gambar lokal tanpa ketergantungan pada perangkat keras fisik.|Sistem dapat mengeksekusi inferensi penuh menggunakan citra _mock_ lokal saat perangkat keras tidak terhubung.|
|**FR-AI-01**|Core AI Inference|Sistem harus melakukan pemotongan area fokus (_ROI extraction_) pada bagian mata dan insang dari citra input secara otomatis sebelum klasifikasi kesegaran.|Pemotongan ROI mata dan insang berhasil dilakukan pada citra masukan.|
|**FR-AI-02**|Core AI Inference|Sistem harus mengklasifikasikan kesegaran ikan ke dalam **Grade A**, **Grade B**, atau **Grade C** menggunakan model terkalibrasi **SNI 2729:2013** (MobileNetV3-Small INT8)[cite: 1, 2, 3].|Parameter model bersifat statis dan menghasilkan nilai _grade_ serta _confidence score_[cite: 1, 2, 3].|
|**FR-AI-03**|Core AI Inference|Sistem harus memindai dan mendeteksi cacat/luka permukaan serta menghasilkan koordinat _bounding box_ ternormalisasi ($0.0\text{–}1.0$) menggunakan model YOLOv8n (Float32)[cite: 1, 2, 3].|_Bounding box_ dan label kelas cacat fisik berhasil dihasilkan[cite: 1, 2, 3].|
|**FR-AI-04**|Core AI Inference|Sistem harus menghitung logika keputusan mutu secara langsung: **"REJECT"** jika cacat $> 0$ ATAU kesegaran **"Grade C"**; serta **"PASS"** jika ikan segar (Grade A/B) dan bebas cacat.|Keputusan _PASS/REJECT_ dihasilkan secara konsisten sesuai aturan logika.|
|**FR-OUT-01**|Pemrosesan Sinkron|Sistem harus mengembalikan seluruh hasil inferensi (overlay _bounding box_, label _grade_, _confidence score_, dan status keputusan mutu) dalam 1 respons API sinkron.|Respons JSON/API diterima oleh antarmuka dalam 1 siklus _request-response_ sinkron.|
|**FR-OUT-02**|Pemrosesan Sinkron|Sistem harus mengarahkan sinyal keluaran status (**PASS** / **REJECT**) secara sinkron ke antarmuka visual dan/atau indikator aktuator[cite: 1, 3].|Indikator keluaran berubah status secara instan mengikuti hasil keputusan mutu[cite: 1, 3].|
|**FR-UI-01**|Single-Page UI|Antarmuka pengguna harus berfokus **HANYA** pada halaman tunggal yang menerima input dari pengguna dan menampilkan output dari AI.|Antarmuka tidak memiliki bilah navigasi ke halaman riwayat, _analytics_, atau fitur otentikasi kompleks.|
|**FR-UI-02**|Single-Page UI|Antarmuka pengguna harus menampilkan _visual overlay_ berupa kotak pembatas (_bounding box_) cacat permukaan dan label kesegaran SNI tepat di atas citra masukan[cite: 1, 3].|_Overlay_ visual ter-render tepat di atas objek citra yang diinspeksi[cite: 1, 3].|
|**FR-UI-03**|Single-Page UI|Antarmuka pengguna harus menampilkan banner indikator keputusan mutu berukuran besar dengan warna kontras (**PASS** berwarna hijau / **REJECT** berwarna merah)[cite: 1, 3].|Banner status berubah warna secara kontras sesuai hasil keputusan AI[cite: 1, 3].|
|**FR-UI-04**|Single-Page UI|Antarmuka pengguna harus menyediakan sakelar tombol (_toggle switch_) untuk mengaktifkan atau mematikan **Mock Data Mode** dengan mudah saat demonstrasi.|Pengguna dapat berpindah antara _Live/Hardware Mode_ dan _Mock Data Mode_ melalui 1 tombol.|

## 📌 Catatan Penyelarasan Teknis:

1. **Penyederhanaan Arsitektur:** Tidak ada modul _Database_, _Background Workers_, atau _Certificate PDF Generator_ dalam tabel ini untuk menjamin repositori tahap penyisihan **100% mematuhi batasan Rulebook COMPFEST 18 AIC (Hal. 15)**.
2. **Setup Execution:** Seluruh FR di atas wajib dapat dieksekusi secara lokal di server panitia menggunakan perintah `docker compose up` berdasarkan petunjuk di file `README.md`.

---

# H. Rencana Strategis Pengumpulan Data

Rencana strategis akuisisi data ini dirancang khusus untuk memenuhi **3 kebutuhan utama sekaligus**:

1. **Kepatuhan Aturan Rulebook COMPFEST 18 AIC (Hal. 16–17)**: Menggunakan kombinasi dataset publik, data sintetik, dan data primer lokal yang diproses _full_ selama periode lomba (17 Juni – 25 Agustus 2026).
2. **Kebutuhan Fitur Core AI NusaQC**: Menyuplai data yang tepat untuk _Model 1 Freshness Classifier_ (SNI 2729:2013), _Model 2 Surface Defect Detector_ (YOLOv8n), serta sampel lokal untuk **Mock Data Mode**.
3. **Keunggulan Geografis & Akademis ITS**: Memanfaatkan lokasi di Surabaya serta almamater ITS untuk mendapatkan data validasi lapangan di kawasan industri perikanan Jawa Timur.

## 🎯 1. Pemetaan Kebutuhan Data per Fitur Sistem

|**Fitur / Modul NusaQC**|**Jenis Model & Target Metrik**|**Kebutuhan Dataset & Karakteristik Visual**|**Sumber Data Utama**|
|---|---|---|---|
|**Model 1: Freshness Classifier**|MobileNetV3-Small (INT8)<br><br>  <br><br>• _Target:_ F1-Score $\ge 85\%$|• Citra serial pembusukan harian mata & insang ikan.<br><br>  <br><br>• Label ground-truth terpetakan ke **SNI 2729:2013** (Grade A, B, C).|**Dataset Publik Akademis:**<br><br>  <br><br>• DaFiF Dataset (~2.536 citra)<br><br>  <br><br>• Freshness of Fish Eyes / FFE (~4.390 citra)<br><br>  <br><br>• Mendeley SalmonScan (~1.208 citra)|
|**Model 2: Surface Defect Detector**|YOLOv8n (Float32)<br><br>  <br><br>• _Target:_ Defect Recall $\ge 85\%$|• Citra permukaan kulit/fillet dengan anotasi _bounding box_.<br><br>  <br><br>• Kelas cacat: luka (_lesion_), bintik merah (_red spot_), parasit, dan _filthy_ (kotoran fisik).|**Dataset Publik & Sintetik:**<br><br>  <br><br>• Roboflow BD Fish Disease (~2.082 citra teranotasi)<br><br>  <br><br>• _Defect Injection Synthetic Pipeline_|
|**Modul Anti-Glare Optik**|Preprocessing Domain Adaptation|• Citra ikan basah dengan variasi _specular highlight_ (kilau air) vs. hasil filter polarisasi.|**Data Augmentasi Domain:**<br><br>  <br><br>• Injeksi _brightness/contrast_ & _Gaussian blur_|
|**Mock Data Mode Switch** _(Syarat Hal. 18)_|File Lokal `/mock_samples`|• 15–20 sampel citra terkurasi (Grade A/B/C dan Cacat/Bersih) untuk _dry-run demo_ tanpa hardware.|**Pengumpulan Mandiri / Sampel Terkurasi**|

## 📋 2. Strategi 3-Jalur Akuisisi Data (3-Track Data Acquisition)

```
[ JALUR 1: PUBLIC FAST-TRACK ] ──┐
 (DaFiF, FFE, Roboflow BD)        │
                                  ├─► [ DATA PREPROCESSING & PIPELINE ] ──► [ TRAIN / VAL / MOCK DATA ]
[ JALUR 2: LOCAL ITS AUDIT ] ────┤    (Augmentation, Split 80/10/10,        (ONNX Core Models +
 (LPPMHP Surabaya / UPI Jatim)    │     INT8 Quantization, Mock Setup)         /mock_samples directory)
                                  │
[ JALUR 3: SYNTHESIS & GLARE ] ──┘
 (Specular Highlight Injection)
```

### 🟢 Jalur 1: Public Academic Fast-Track (Bobot Data: 70%)

- **Tujuan:** Menyediakan _baseline dataset_ berukuran besar untuk _fine-tuning_ awal model AI.
- **Eksekusi:**
    - **Dataset DaFiF (Prasetyo et al., 2024 - Mendeley Data):** Digunakan sebagai dataset utama Model 1. Data ini berisi deret waktu (_time-series_) pembusukan harian ikan yang memiliki korelasi langsung dengan skor organoleptik SNI 2729:2013 (Grade A = Uji Hari 1–2, Grade B = Uji Hari 3–4, Grade C = Uji Hari 5+).
    - **Roboflow BD Fish Disease Dataset:** Digunakan sebagai dataset utama Model 2. Sudah dilengkapi anotasi koordinat _bounding box_ untuk 7 kelas penyakit/luka fisik permukaan tubuh ikan.

### 🟡 Jalur 2: Local Field Validation — "ITS Academic Cover" (Bobot Data: 15%)

- **Tujuan:** Mendapatkan dataset validasi lapangan (_Field Test Set_) untuk membuktikan bahwa model AI bekerja pada kondisi nyata meja sortasi UPI di Jawa Timur.
- **Taktik Akses Mahasiswa ITS:**
    
    1. **Kunjungan ke UPT LPPMHP Surabaya (Gayungan):** Menggunakan Surat Pengantar Riset dari Departemen ITS untuk mewawancarai penguji mutu organoleptik resmi DKP Jatim sekaligus mendokumentasikan 30–50 foto sampel ikan uji segar vs. reject.
    2. **Kunjungan Lapangan UPI (Sidoarjo/Gresik):** Pengambilan sampel citra kondisi meja sortasi basah sebagai data _ground-truth_ pengujian lokal.

### 🔵 Jalur 3: Synthetic Data & Glare Augmentation (Bobot Data: 15%)

- **Tujuan:** Menutup _domain gap_ antara foto laboratorium/kamera biasa dengan kondisi meja sortasi basah yang penuh kilauan air (_glare_).
- **Pipelines Augmentasi Sintetik (Python `albumentations`):**
    - **Specular Highlight Injection:** Menambahkan _patch_ piksel putih intensitas tinggi secara acak untuk mensimulasikan kilau lampu pabrik pada kulit ikan basah.
    - **Mucus Blur Simulation:** Mengaplikasikan _Gaussian blur_ lokal untuk mensimulasikan lapisan lendir tebal pada ikan Grade C.
    - **HSV Color Jitter:** Mengubah variasi warna kulit untuk mensimulasikan perbedaan spesies ikan (tuna, bandeng, udang).

## 🛠️ 3. Pipeline Pengolahan Data untuk Babak Penyisihan

Rangkaian alur pengolahan data ini wajib dituliskan secara rinci dalam **Sub-Bab Metodologi Proposal PDF (Maksimal 20 Halaman)** untuk memenuhi kriteria penilaian **Kualitas Proposal & Proses Pengembangan (15%)**:

```
 1. DATA COLLECTION      2. PREPROCESSING & ANNOTATION      3. FINE-TUNING & QUANTIZATION      4. MOCK DATA CURATION
┌──────────────────┐    ┌──────────────────────────────┐   ┌──────────────────────────────┐   ┌──────────────────────────────┐
│ • DaFiF + FFE    │    │ • ROI Crop (Mata/Insang)     │   │ • Fine-tune MobileNetV3      │   │ • Terpilih 15 Gambar sampel  │
│ • Roboflow BD    │───>│ • Bounding Box Normalization │──>│ • Fine-tune YOLOv8n          │──>│ • Disimpan di /mock_samples  │
│ • Local Field    │    │ • Split 80% Train / 10% Val /│   │ • Export ONNX INT8/Float32   │   │ • Siap dieksekusi via Toggle │
│ • Synthetic Glare│    │   10% Test                   │   │   (Parameter Statis Demo)    │   │   Switch di Single-Page UI   │
└──────────────────┘    └──────────────────────────────┘   └──────────────────────────────┘   └──────────────────────────────┘
```

### Rincian Tahapan Pipeline:

1. **Preprocessing & Standardization:**
    
    - Resizing gambar Model 1 ke $224 \times 224\text{ px}$ (RGB) dan Model 2 ke $640 \times 640\text{ px}$ (RGB).
    - Normalisasi koordinat _bounding box_ ($0.0 \text{–} 1.0$) pada format YOLO.
        
2. **Train / Val / Test Partition:**
    
    - Pembagian dataset secara ketat: **80% Training Set**, **10% Validation Set**, dan **10% Unseen Test Set**.
        
3. **Model Fine-Tuning & Quantization:**
    
    - Pelatihan model menggunakan PyTorch/Ultralytics selama periode kompetisi (Juni–Agustus 2026).
    - Kuantisasi _weights_ MobileNetV3 menjadi **INT8 ONNX** (ukuran file $< 5\text{ MB}$) untuk latensi cepat di CPU lokal.
        
4. **Mock Data Preparation (Syarat Rulebook Hal. 18):**
    
    - Mengurasi 15 sampel citra mewakili seluruh variasi hasil (Grade A, Grade B, Grade C, dan Cacat Fisik).
    - Memasukkan citra ke folder repositori `/mock_samples` sehingga panitia dapat menguji fungsionalitas AI secara penuh tanpa butuh _hardware_ terpasang.

## 📋 4. Checklist Kepatuhan Aturan Data (Rulebook Compliance)

|**Ketentuan Rulebook COMPFEST 18 AIC**|**Tindakan Strategis Tim NusaQC**|**Status Compliance**|
|---|---|---|
|**Sumber Dataset (Hal. 16)**|Mengombinasikan dataset publik terakreditasi (DaFiF/Mendeley) dan data sintetik.|✅ **100% Compliant**|
|**Periode Pengerjaan Model (Hal. 16)**|Seluruh alur _preprocessing_, _fine-tuning_, dan kuantisasi dikerjakan sepenuhnya dalam rentang 17 Juni – 25 Agustus 2026.|✅ **100% Compliant**|
|**Syarat Bab Metodologi Proposal (Hal. 17)**|Proposal PDF memuat bab khusus: Alur Memperoleh Dataset, Alur Pengembangan Model, dan Alur Integrasi Code Environment.|✅ **100% Compliant**|
|**Persyaratan Mock Data Mode (Hal. 18)**|Repositori GitHub menyediakan dataset sampel lokal dalam folder `/mock_samples` yang dipanggil via sakelar UI.|✅ **100% Compliant**|

---

# I. Rencana Strategis Pelatihan Model

Berikut adalah **Rencana Strategis Pelatihan Model AI (_Model Training Strategy_)** untuk sistem **NusaQC**. Plan ini dirancang secara sistematis agar menghasilkan performa _inference_ yang presisi di meja sortasi basah, sekaligus **100% patuh pada aturan Rulebook COMPFEST 18 AI Innovation Challenge (AIC)** (khususnya batasan waktu pengerjaan 17 Juni – 25 Agustus 2026, penggunaan _fine-tuning pre-trained model_, _static parameter demo_, dan _export ONNX_ untuk _Docker Compose_).

## 📊 1. Matriks Strategi Arsitektur & Target Metrik AI Engine

Sesuai kebutuhan sistem NusaQC, pemrosesan AI dibagi menjadi **2 model independen** yang dieksekusi secara berurutan (_sequential synchronous pipeline_):

|**Parameter Strategi**|**Model 1: Freshness Classifier**|**Model 2: Surface Defect Detector**|
|---|---|---|
|**Fokus Tugas**|Mengklasifikasikan tingkat kesegaran organoleptik.|Mendeteksi titik luka, parasit, bintik merah, dan _filthy_.|
|**Standar Acuan**|**SNI 2729:2013** (Grade A, Grade B, Grade C).|Prioritas _High Recall_ (mencegah _False Negative_).|
|**Arsitektur Backbone**|**MobileNetV3-Small** (Lightweight CNN).|**YOLOv8n** (Nano Anchor-Free Object Detector).|
|**Input Dimensions**|$224 \times 224 \times 3$ RGB (ROI Crop Mata/Insang).|$640 \times 640 \times 3$ RGB (Full Conveyor Shot).|
|**Loss Function**|Weighted Categorical Cross-Entropy Loss.|Task-Aligned Loss (TAL: BCE Cls Loss + CIoU Box Loss).|
|**Target Metrik**|Weighted $F_1\text{-Score} \ge 85\%$.|Defect $\text{Recall} \ge 85\%$, $\text{Precision} \ge 80\%$.|
|**Format Export**|**ONNX Quantized INT8** (Ukuran File $< 2.5\text{ MB}$).|**ONNX Float32 Engine** (Ukuran File $\approx 6\text{ MB}$).|
|**Target Latensi**|$< 50\text{ ms}$ di CPU Lokal.|$< 250\text{ ms}$ di CPU Lokal.|

## 🛠️ 2. FASE 1: Setup Environment & Infrastruktur Pelatihan

Untuk menjamin kelancaran _workflow_ pengerjaan tim selama periode kompetisi:

- **Paket & Dependency Manager:** Menggunakan **`uv`** (Python package manager berbasis Rust) untuk menjamin isolasi lingkungan virtual yang cepat, stabil, dan reproduosibel di OS Linux/WSL2.
- **Framework Pelatihan:** PyTorch 2.x, Ultralytics (YOLOv8), Albumentations (Augmentasi Optik), dan ONNX Runtime Tools.
- **Infrastruktur Komputasi:**
    - _Local Development:_ GPU NVIDIA (Local CUDA).
    - _Cloud Acceleration:_ Memanfaatkan **Free GPU/VPS Credits** resmi dari panitia COMPFEST 18 AIC atau Google Colab Pro / Kaggle GPU untuk proses _training & fine-tuning_ skala besar.

## 🐟 3. FASE 2: Strategi Pelatihan Model 1 — Freshness Classifier (MobileNetV3-Small)

### Langkah 1: Two-Stage ROI Preprocessing Pipeline

Input foto dari konveyor berisi seluruh tubuh ikan. Untuk meningkatkan akurasi klasifikasi kesegaran organoleptik:

1. **Fish Bounding Crop:** Menggunakan _bounding box_ ikan dari YOLOv8n untuk memotong (_crop_) citra ikan utuh.
2. **ROI Auto-Extraction:** Memotong area spesifik **Mata** ($\approx 15\%$ dari _bounding box_ atas) dan **Insang** ($\approx 10\%$ area lateral) menggunakan estimasi rasio terstandar.
3. Resizing citra hasil _crop_ menjadi $224 \times 224\text{ px}$.

```
[ Conveyor Shot 640x640 ] ──> [ Fish BBox Detection ] ──> [ Crop ROI Mata/Insang 224x224 ] ──> [ MobileNetV3 INT8 ]
```

### Langkah 2: Fine-Tuning & Penanganan Class Imbalance

- **Pre-trained Backbone:** Menginisialisasi _weights_ MobileNetV3-Small yang telah dilatih pada ImageNet.
- **Penanganan Imbalance Data:** Mengingat sampel ikan busuk (Grade C) biasanya lebih sedikit di dataset publik, gunakan **Weighted Cross-Entropy Loss**:

    $$\text{Loss} = -\sum_{c=1}^{C} w_c \cdot y_c \log(\hat{y}_c)$$

    Di mana bobot kelas $w_c$ dihitung secara otomatis berbalik nilai dengan frekuensi kemunculan jumlah sampel kelas.
    
- **Hyperparameter Config:**
    - _Optimizer:_ AdamW ($\text{lr} = 10^{-3}$, $\text{weight\_decay} = 10^{-4}$).
    - _Scheduler:_ CosineAnnealingLR (Warmup 5 epoch, total 50 epoch).
    - _Batch Size:_ 32 atau 64.

### Langkah 3: Post-Training Quantization (INT8 Conversion)

Setelah model PyTorch mencapai $F_1\text{-Score} \ge 85\%$:

1. Export model PyTorch ke format ONNX (`opset_version=13`).
2. Terapkan **INT8 Quantization** menggunakan `onnxruntime.quantization`:
    
    - Mengubah presisi bobot dari Float32 ke INT8 (integer 8-bit).
    - Menekan ukuran berkas dari $\approx 10\text{ MB}$ menjadi **$\approx 2.5\text{ MB}$**.
    - Mempercepat inferensi di CPU lokal hingga $3\times$ lebih cepat dengan penurunan akurasi $< 0.8\%$.

## 🔍 4. FASE 3: Strategi Pelatihan Model 2 — Surface Defect Detector (YOLOv8n)

### Langkah 1: Domain-Specific Data Augmentation Pipeline

Kunci utama keberhasilan deteksi cacat di meja sortasi basah adalah membuat model kebal terhadap kilauan air (_glare_) dan variasi pencahayaan pabrik.

Gunakan alur augmentasi khusus via `Albumentations` & `YOLO Native Augmentation`:

- **Specular Highlight / Glare Injection ($p=0.4$):** Menambahkan _patch_ piksel putih intensitas tinggi ($240\text{--}255$) untuk mensimulasikan pantulan lampu pada permukaan basah.
- **Mucus / Moisture Blur ($p=0.3$):** _Gaussian Blur_ lokal untuk mensimulasikan lendir tebal.
- **HSV Color Jitter:** `hsv_h=0.015`, `hsv_s=0.7`, `hsv_v=0.4` untuk mensimulasikan perbedaan spesies dan tingkat pencahayaan.
- **Mosaic Augmentation ($1.0$) & MixUp ($0.15$):** Menggabungkan 4 citra sampel sekaligus untuk meningkatkan kemampuan deteksi objek cacat berukuran kecil.

### Langkah 2: Tuning Hyperparameter untuk Priority High Recall ($\ge 85\%$)

Dalam dunia industri ekspor pangan, biaya akibat _False Negative_ (ikan cacat lolos ke kontainer ekspor) jauh lebih fatal daripada _False Positive_ (ikan meragukan diperiksa ulang).

- **Confidence Threshold Tuning:** Turunkan _confidence threshold_ saat inferensi dari standar $0.25$ menjadi **$\text{conf} = 0.15\text{--}0.20$** untuk memaksimalkan _Recall_.
- **NMS IoU Threshold:** Tetapkan IoU threshold $\text{iou} = 0.45$ untuk eliminasi _overlapping bounding box_.

### Langkah 3: Float32 ONNX Export

1. Train YOLOv8n selama 100 epoch menggunakan dataset gabungan Roboflow BD Fish Disease & Data Primer.
2. Export model terbaik (`best.pt`) ke ONNX Engine:
    
    Bash

    ```
    yolo export model=best.pt format=onnx dynamic=False imgsz=640 opset=13
    ```

## ⚡ 5. FASE 4: Integrasi Synchronous Inference & Benchmarking

Setelah kedua model ONNX berhasil dikompilasi, integrasikan ke dalam **FastAPI Backend Execution Loop** yang 100% mematuhi syarat _synchronous processing_ babak penyisihan:

Python

```
# Synchronous Pipeline Execution (Conceptual Flow)
@app.post("/predict")
def predict_synchronous(image_bytes: bytes, mock_mode: bool = False):
    # 1. Load image / Mock image
    img = load_image(image_bytes, mock_mode)
    
    # 2. Exec Model 2: YOLOv8n Defect & Localization (640x640 Float32 ONNX)
    bbox_list, defects_found = run_yolov8_onnx(img)
    
    # 3. Pre-process ROI Crop for Freshness
    roi_crop = extract_eye_gill_roi(img, bbox_list)
    
    # 4. Exec Model 1: MobileNetV3 Freshness (224x224 INT8 ONNX)
    freshness_grade, sni_score, conf = run_mobilenet_onnx(roi_crop)
    
    # 5. Execute Decision Logic
    decision = "REJECT" if (defects_found > 0 or freshness_grade == "Grade C") else "PASS"
    
    # 6. Trigger GPIO Actuator Signal (Synchronous)
    trigger_gpio_signal(decision)
    
    return {
        "freshness": {"grade": freshness_grade, "sni_score": sni_score, "confidence": conf},
        "defects": bbox_list,
        "decision": decision
    }
```

### Benchmarking Target di CPU Lokal (Docker Environment)

:

- **YOLOv8n ONNX Latency:** $\approx 180\text{ ms}$
- **MobileNetV3 INT8 Latency:** $\approx 35\text{ ms}$
- **Preprocessing & GPIO Overhead:** $\approx 45\text{ ms}$
- **Total Latency:** **$\approx 260\text{ ms}$** ($\ll 500\text{ ms}$ limit, mampu melayani $2\text{ ekor/detik}$ di konveyor).

## 📑 6. FASE 5: Penulisan Metodologi untuk Proposal PDF (Maks. 20 Halaman)

Seluruh strategi pelatihan di atas harus ditransformasikan ke dalam dokumen **Proposal PDF** pada bagian **Sub-Bab Metodologi** (syarat Rulebook Halaman 17):

1. **Alur Memperoleh Dataset:** Jelaskan rasionalisasi penggunaan DaFiF (Mendeley), Roboflow BD, serta teknik augmentasi _Specular Highlight Injection_[cite: 1, 2, 3].
2. **Alur Pengembangan Model:** Tuliskan grafik/diagram tahapan pelatihan, rumus _Loss Function_, penanganan _class imbalance_, serta teknik kuantisasi INT8[cite: 1, 2, 3].
3. **Alur Integrasi Model ke Environment Kode:** Paparkan diagram _Synchronous ONNX Runtime execution_ di dalam kontainer Docker Compose dan penggunaan _Mock Data Mode_[cite: 1, 3].
4. **Decision Making Berbasis Data:** Cantumkan tabel matriks perbandingan performa sebelum vs sesudah kuantisasi INT8 untuk membuktikan alasan teknis pemilihan arsitektur[cite: 2, 3].

---

# I. Rencana Strategis Integrasi

Apakah benar AI dapat diintegrasikan secara nyata ke dalam sistem Unit Pengolahan Ikan (UPI) dan memberikan manfaat langsung di dunia kerja? Jawabannya adalah **SANGAT MEMUNGKINKAN DAN SANGAT REALISTIS**.

Keraguan ini sangat wajar karena lini pengolahan ikan terkenal sebagai **lingkungan industri basah (_wet processing environment_)** yang dingin, penuh cipratan air garam, dan berkecepatan tinggi.

AI **tidak perlu membongkar atau mengganti mesin konveyor mahal** yang sudah dimiliki oleh UPI. Solusi NusaQC menerapkan metode Non-Invasive Retrofitting (Plug-and-Play), yaitu menambahkan modul pengawasan AI di atas lini konveyor eksisting tanpa merusak alur kerja pabrik.

## 🏭 1. Anatomi QC Eksisting di UPI: Bagaimana QC Nyata Bekerja Saat Ini?

Berdasarkan praktik standar industri pengolahan ikan (seperti di UPI skala ekspor Jawa Timur), berikut adalah gambaran fakta lapangan mengenai teknologi dan alur kerja QC konvensional:

### Teknologi & Alat yang Sudah Ada di UPI Saat Ini:

- **Lini Konveyor Makanan (_Food-Grade Conveyor Belt_):** Menggunakan sabuk berbahan PVC/Modular Plastic atau meja _Stainless Steel_ (AISI 304/316) tempat ikan meluncur dari area pencucian ke area penimbangan/pengemasan.
- **Pencahayaan Overhead:** Lampu TL atau LED industri di atas meja sortasi.
- **Timbangan Digital (_Checkweigher_):** Digunakan untuk mengelompokkan ukuran berat ikan setelah sortasi visual.
- **Alat Pencatatan:** Papan jepit dengan kertas penulisan (_clipboard paper logbook_).

### Alur Kerja QC Manual di Lapangan:

```
[ Washing Tank ] ──> [ Conveyor Line ] ──> [ Manual QC Operator ] ──> [ Checkweighing ] ──> [ Packing ]
                                                  │
                                                  ▼ (Diperiksa Mata Manual 5-15 Detik/Ekor)
                                           [ Paper Logbook ]
```

1. **Pemeriksaan Visual Organoleptik:** Operator berdiri/duduk di pinggir konveyor, melihat satu per satu ikan yang lewat.
2. **Pemilahan Kategori Mutu:** Operator memeriksa kejernihan mata, warna insang, tekstur kulit, serta mencari luka/cacat fisik. Ikan dipisahkan secara manual ke keranjang Grade A, B, atau C.
3. **Pencatatan Manual:** Di akhir _shift_, supervisor menghitung lembar kertas pencatatan untuk dibuat laporan mutunya.

## ⚠️ 2. Di Mana AI Masuk & Bagaimana AI Membantu QC secara Nyata?

AI NusaQC **tidak menggantikan konveyor atau pekerja**, melainkan **diintegrasikan di atas stasiun kerja sortasi (_Sorting Station_)** sebagai "mata otomatis dan asisten telinga".

```
                 ┌────────────────────────────────────────┐
                 │  NusaQC Overhead Enclosure (IP69K)     │
                 │  • Kamera + Filter Polarisasi Anti-Glare│
                 │  • Trigger Proximity Sensor            │
                 └───────────────────┬────────────────────┘
                                     │
[ Washing Tank ] ──> [ Conveyor Line ] ──> [ Closed-Loop Actuator ] ──> [ Checkweighing ]
                                                  │ (Buzzer/Strobe Alarm)
                                                  ▼
                                       [ Operator Hanya Memisah ]
                                       [   Ikan Saat Alarm Aktif  ]
```

### Transformasi Nyata Pekerjaan QC di Lapangan:

|**Aspek Pekerjaan**|**QC Manual Konvensional**|**QC Terintegrasi AI NusaQC**|**Manfaat Nyata di Dunia Kerja**|
|---|---|---|---|
|**Metode Inspeksi**|Operator menatap ikan satu per satu secara kontinu di bawah lampu pabrik.|Kamera _overhead_ mengambil foto snapshot otomatis saat ikan lewat sensor.|**Menghilangkan Kelelahan Visual:** Operator tidak perlu menatap tajam ribuan ikan selama 8 jam.|
|**Kecepatan Periksa**|**5–15 detik per ekor** (menciptakan penumpukan/ _bottleneck_).|**$< 500\text{ ms}$ per ekor** (tereksekusi sinkron di _edge CPU_).|**Menghilangkan _Throughput Bottleneck_:** Alur konveyor berjalan maksimal tanpa tertahan.|
|**Tindakan Pemilahan**|Operator harus melihat layar monitor/menilai sendiri sebelum menyisihkan ikan.|**Closed-Loop Actuation:** Siren/LED Alarm menyala **HANYA** saat AI menemukan ikan _REJECT_.|**Zero-Touch Operation:** Operator bekerja dengan tangan basah tanpa perlu menyentuh alat sama sekali.|
|**Penanganan Glare**|Pantulan lampu pada kulit ikan basah menyulitkan mata manusia.|**Cross-Polarization Filter:** Menghilangkan pantulan air basah $\ge 80\%$ pada citra.|**Mencegah False Positive:** Deteksi cacat fisik menjadi presisi dan objektif.|

## 📊 3. Bukti Factual: Mengapa UPI Memiliki Infrastruktur yang Cocok untuk NusaQC?

Berikut adalah data faktual mengenai teknologi eksisting UPI yang membuktikan bahwa integrasi NusaQC dapat dilakukan **tanpa hambatan teknis (_frictionless_)**:

### 1. Bukti Faktual 1: Struktur Fisik Frame Konveyor (_Mounting Overhead_)

- **Fakta Lapangan:** Meja sortasi dan konveyor UPI terbuat dari kerangka _Stainless Steel_ AISI 304/316.
- **Kesesuaian Integrasi:** Modul _enclosure_ NusaQC dirancang menggunakan _clamp bracket_ industri yang dapat dijepitkan (_clamped_) langsung pada kerangka besi konveyor tanpa memerlukan pengelasan atau pemotongan struktur konveyor.

### 2. Bukti Faktual 2: Kecepatan Konveyor Standar vs. Latensi AI

- **Fakta Lapangan:** Kecepatan konveyor sortasi UPI berada pada kisaran $0.5\text{ hingga }1.0\text{ m/s}$ dengan jarak antar ikan $\approx 0.3\text{--}0.5\text{ meter}$ ($\approx 1\text{--}2\text{ ekor/detik}$).
- **Kesesuaian Integrasi:** Latensi inferensi AI NusaQC berbasis pemicu sensor (_trigger-based capture_) adalah **$\approx 260\text{--}450\text{ ms}$ per ekor**. Karena waktu proses AI ($< 0.5\text{ detik}$) lebih cepat daripada jarak antar ikan ($1.0\text{ detik}$), AI dipastikan mampu memproses setiap ikan secara _real-time_ tanpa ada yang terlewat.

### 3. Bukti Faktual 3: Ketersediaan Daya Listrik Industri (AC 220V)

- **Fakta Lapangan:** Setiap stasiun konveyor UPI selalu dilengkapi suplai listrik industri untuk menggerakkan motor konveyor dan sistem pencahayaan.
- **Kesesuaian Integrasi:** NusaQC hanya membutuhkan daya komputasi _Edge CPU_ (seperti Mini PC / Raspberry Pi) dan _LED Ring Light_ berdaya rendah ($\approx 15\text{--}30\text{ Watt}$) yang dapat dicolokkan langsung ke stopkontak eksisting stasiun kerja.

### 4. Bukti Faktual 4: Standar Sanitasi Semprot Air Tekanan Tinggi (_High-Pressure Washdown_)

- **Fakta Lapangan:** Sesuai prosedur HACCP/SSOP, seluruh area meja sortasi UPI disemprot air bertekanan tinggi setiap akhir _shift_ untuk sanitasi harian.
- **Kesesuaian Integrasi:** _Enclosure_ NusaQC menggunakan material _Stainless Steel AISI 316L_ berstandar proteksi **IP66/IP69K**. Perangkat aman dari korosi air garam dan tahan semprotan air sanitasi tekanan tinggi hingga 100 bar tanpa perlu dicopot saat pabrik dibersihkan.

## 🚀 4. Rencana Strategis Tahapan Integrasi Nyata di Pabrik (Implementation Roadmap)

Untuk menerapkan NusaQC di UPI secara nyata, berikut adalah rencana strategis 3 fase integrasi tanpa mengganggu jalannya produksi (_Zero Downtime_):

```
[ FASE 1: RETROFITTING ] ──> [ FASE 2: OPTICAL CALIBRATION ] ──> [ FASE 3: CLOSED-LOOP ACTIVATION ]
 Pasang Bracket Overhead      Atur Polarisasi Anti-Glare         Hubungkan Sinyal Alarm Siren
 (Tanpa Hentikan Konveyor)    & Pengujian Trigger Sensor        (Sistem AI Beroperasional Penuh)
```

1. **Fase 1 — Non-Invasive Mechanical Retrofitting (1 Hari):**
    
    - Pemasangan _bracket mounting overhead_ NusaQC pada kerangka meja konveyor eksisting.
    - Pemasangan jepitan sensor _infrared/proximity_ pada tepi rel konveyor untuk mendeteksi posisi ikan.
        
2. **Fase 2 — Optical Calibration & Mock Validation (1 Hari):**
    
    - Penyesuaian filter polarisasi silang (_cross-polarization_) pada lensa kamera untuk menyerap kilauan air basah.
    - Pengujian pengambilan citra snapshot berbasis pemicu sensor (_trigger-based capture_).
        
3. **Fase 3 — Closed-Loop Alarm Integration (1 Hari):**
    
    - Menghubungkan modul _relay_ GPIO dari _Edge CPU_ ke perangkat _Audio Siren Buzzer & Strobe LED Light_ di atas meja kerja.
    - **Hasil:** Saat AI mendeteksi ikan _REJECT_ (cacat/Grade C), siren langsung berbunyi dan operator menyisihkan ikan tersebut secara instan.

## 💡 Kesimpulan Soliditas Integrasi

Integrasi AI NusaQC pada UPI **sangat memungkinkan secara teknis dan operasional**:

1. **Tidak Membutuhkan Mesin Baru:** Memanfaatkan konveyor dan aliran kerja eksisting UPI via metode _overhead retrofitting_.
2. **Menjawab Ketakutan Lingkungan Basah:** Dilindungi cangkang _IP69K SS316L_ dan filter optik _cross-polarization_.
3. **Membantu Pekerjaan QC Secara Konkret:** Mengubah inspeksi manual yang melelahkan ($5\text{--}15\text{ detik/ekor}$) menjadi pemindaian AI otomatis ($< 0.5\text{ detik}$) dengan pemicuan alarm _zero-touch_.

---

# J. Rencana Penambahan Framework

Dalam pengembangan perangkat lunak yang mengintegrasikan kecerdasan buatan (AI/ML), terdapat tantangan mendasar: **perangkat lunak konvensional bersifat deterministik** (berbasis logika kode yang pasti), sedangkan **model AI bersifat probabilistik/non-deterministik** (berbasis pola data yang dinamis).

Untuk menjembatani kolaborasi antara alur riset AI dan alur rekayasa perangkat lunak (_Software Engineering_), para peneliti dan praktisi industri mengembangkan berbagai **framework & metodologi standar**.

Berikut adalah daftar framework utama yang didukung penelitian akademis dan praktik industri, beserta penjelasan, manfaat, dan perbedaannya.

## 📚 Daftar Framework Penggabungan AI & Rekayasa Perangkat Lunak

### 1. CRISP-ML(Q) (_Cross-Industry Standard Process for Machine Learning with Quality Assurance_)

- **Penjelasan:** CRISP-ML(Q) adalah evolusi dari standar metodologi data mining klasik (CRISP-DM) yang diperbarui secara ilmiah untuk menangani siklus hidup model Machine Learning modern. Framework ini menambahkan lapisan _Quality Assurance_ (QA) dan pemeliharaan perangkat lunak pada 6 fasenya: _Business Understanding, Data Understanding/Prep, Model Building, Evaluation, Deployment,_ serta _Monitoring & Maintenance_.
- **Manfaat:**
    - **Jaminan Kualitas Sistem:** Memastikan kriteria kualitas (_accuracy_, _robustness_, _explainability_) ditetapkan sejak awal bersama standar rekayasa perangkat lunak.
    - **Mitigasi _Data Drift_:** Memiliki fase khusus untuk memantau penurunan performa model AI setelah diintegrasikan ke dalam sistem produksi.

### 2. MLOps & CD4ML (_Continuous Delivery for Machine Learning_)

- **Penjelasan:** MLOps merupakan adaptasi dari kultur **DevOps** dalam rekayasa perangkat lunak yang digabungkan dengan alur _Machine Learning Engineering_. Salah satu implementasi konkretnya dirumuskan oleh ThoughtWorks melalui **CD4ML** (_Continuous Delivery for Machine Learning_). CD4ML memperlakukan kode _backend/frontend_, data, dan bobot model AI sebagai satu kesatuan _pipeline_ otomatisasi (**CI/CD/CT** — _Continuous Integration, Continuous Delivery, Continuous Training_).
- **Manfaat:**
    - **Otomasi Otomatisasi Terintegrasi:** Setiap pembaruan kode aplikasi _backend_ maupun retraining model AI dapat diuji dan dideploy secara otomatis tanpa merusak sistem.
    - **Reproduosibilitas Tinggi:** Menjamin _versioning_ gabungan antara kode aplikasi, dataset, dan parameter model.

### 3. Microsoft TDSP (_Team Data Science Process_)

- **Penjelasan:** Metodologi pengembangan berbasis _Agile_ yang dirancang oleh Microsoft khusus untuk proyek AI/Data Science yang dikerjakan oleh tim rekayasa perangkat lunak multidisiplin. TDSP menstrukturkan alur kerja ke dalam 4 tahap utama (_Business Understanding, Data Acquisition & Understanding, Modeling, Deployment_) dengan _checkpoint_ dokumen dan struktur direktori terstandar.
- **Manfaat:**
    - **Sangat Ramah _Agile/Scrum_:** Siklus eksperimen AI dibagi ke dalam _sprint_ kerja yang mudah dipahami oleh pengembang _software_ (_frontend/backend/DBA_).
    - **Kolaborasi Tim Terstruktur:** Menetapkan peran yang jelas antara _Data Scientist_, _ML Engineer_, dan _Software Developer_.

### 4. SEI AI Engineering Framework (CMU SEI)

- **Penjelasan:** Dirumuskan oleh _Software Engineering Institute_ (SEI) di Carnegie Mellon University, framework ini tidak hanya berfokus pada alur pembuatan model, melainkan pada **arsitektur rekayasa sistem secara holistik**. Framework ini bertumpu pada 3 pilar utama:
    
    1. **Scalable AI:** Keterhubungan infrastruktur data dan perangkat lunak.
    2. **Robust & Secure AI:** Keandalan software dan keamanan AI dari serangan (_adversarial attacks_).
    3. **Human-Centered AI:** Antarmuka pengguna (UX), etika, dan pengawasan manusia (_Human-in-the-Loop_).
        
- **Manfaat:**
    - **Kematangan Arsitektur Sistem:** Memastikan AI tidak hanya bagus di lingkungan riset, tetapi tangguh saat diintegrasikan dengan _software architecture_, antarmuka pengguna, dan _hardware_.
    - **Fokus Keamanan & Etika:** Menangani risiko kegagalan sistem dan kemudahan pengawasan oleh pengguna manusia di lapangan.

### 5. Metodologi Hibrida: _Scrum-CRISP Hybrid_

- **Penjelasan:** Metodologi gabungan yang memadukan sifat eksploratif dari pengembangan AI (_CRISP-DM/ML_) dengan ketepatan waktu serta pengiriman fitur berulang dari rekayasa perangkat lunak (_Scrum_). Eksperimen AI dimasukkan ke dalam _Backlog_ sebagai _Research Spikes_, sementara integrasi aplikasi tetap berjalan dalam siklus _Sprint_ 1–2 mingguan.
- **Manfaat:**
    - **Menyeimbangkan Ketidakpastian AI:** Eksperimen AI yang bersifat tidak pasti (_trial-and-error_) tidak menghentikan jadwal rilis komponen _software_ (UI, API, Database).
    - **Iteratif dan Reflektif:** Evaluasi berkala memastikan keselarasan antara performa model dan kebutuhan fitur aplikasi.

## 📊 Matriks Perbedaan Utama Framework

|**Nama Framework**|**Fokus Utama**|**Pendekatan Integrasi SE & AI**|**Keunggulan Utama**|**Skenario Penggunaan Terbaik**|
|---|---|---|---|---|
|**CRISP-ML(Q)**|Kualitas & Siklus Hidup Model ML|Menambahkan standar _Quality Assurance_ rekayasa ke alur riset ML.|Menjamin keandalan model AI sebelum dan sesudah rilis.|Proyek AI yang membutuhkan akurasi tinggi dan kepatuhan standar mutu (misal: QC Industri, Medis).|
|**MLOps / CD4ML**|Otomasi Operasional (_Pipeline & DevOps_)|Menggabungkan _continuous integration_ kode aplikasi dengan _continuous training_ model AI.|Otomasi _deployment_, pemantauan sistem, dan _versioning_ terpadu.|Aplikasi berbasis AI yang rilis ke sistem produksi dan memerlukan _retraining_ berkala.|
|**Microsoft TDSP**|Manajemen Proses & Kolaborasi Tim|Menyesuaikan eksperimen data ke dalam manajemen proyek _Agile/Scrum_.|Struktur proyek rapi, dokumentasi jelas, mudah dipahami _software engineer_.|Tim gabungan (Software Engineer + Data Scientist) yang bekerja dengan metodologi _Agile_.|
|**SEI AI Engineering**|Arsitektur Sistem & Keandalan Industri|Memandag AI sebagai salah satu modul dalam sistem rekayasa perangkat lunak skala besar.|Keamanan sistem (_robustness_), skalabilitas _hardware_, dan desai UX/Human-in-the-Loop.|Sistem industri kompleks, _cyber-physical systems_, dan AI kritis (_safety-critical systems_).|
|**Scrum-CRISP Hybrid**|Manajemen Siklus _Sprint_ & Fitur|Memisahkan alur _exploratory research_ AI dan _feature delivery_ aplikasi.|Fleksibilitas tinggi, menghindari _delay_ pengembangan aplikasi akibat riset AI.|Pengembangan produk MVP atau kompetisi/hackathon dengan batas waktu pengerjaan yang ketat.|

## 💡 Penerapan Ringkas pada Pengembangan Sistem (Seperti NusaQC)

Jika diterapkan pada sistem seperti **NusaQC** (_Edge Computer Vision & Digital Traceability_):

- **Manajemen Tim & Proses:** Gunakan **Scrum-CRISP Hybrid** / **Microsoft TDSP** agar pembuatan antarmuka _Web Dashboard_ (Next.js/FastAPI) dapat berjalan paralel dengan _fine-tuning_ model AI (MobileNetV3 & YOLOv8).
- **Standar Mutu AI Engine:** Gunakan **CRISP-ML(Q)** untuk memastikan penetapan kriteria _Recall_ $\ge 85\%$ dan sinkronisasi label kesegaran dengan baku mutu SNI 2729:2013 terdefinisi secara terukur.
- **Arsitektur Perangkat:** Gunakan pilar **SEI AI Engineering** untuk merancang sistem _Closed-Loop Actuator_ (sinyal AI memicu Buzzer/LED via GPIO) dan penanganan _domain gap_ (kilau air pada permukaan ikan menggunakan filter polarisasi).
