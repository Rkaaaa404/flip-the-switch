---
date_created: 2026-08-02T22:42
date_modified: 2026-08-03T20:29
---

# Outline Obisidian

```table-of-contents
title: 
style: nestedList # TOC style (nestedList|nestedOrderedList|inlineFirstLevel)
minLevel: 0 # Include headings from the specified level
maxLevel: 0 # Include headings up to the specified level
include: 
exclude: /outline/i
includeLinks: true # Make headings clickable
hideWhenEmpty: false # Hide TOC if no headings are found
debugInConsole: false # Print debug info in Obsidian console
```

---

# Outline GitHub

- [Referensi Proposal](#referensi-proposal)
- [Ringkasan Singkat Struktur Proposal](#ringkasan-singkat-struktur-proposal)
- [Ringkasan Eksekutif](#ringkasan-eksekutif)
- [Bab 1 – Pendahuluan](#bab-1--pendahuluan)
	- [1.1 Latar Belakang](#11-latar-belakang)
	- [1.2 Relevansi Tema: Smart Manufacturing](#12-relevansi-tema-smart-manufacturing)
	- [1.3 Tujuan](#13-tujuan)
- [Bab 2 – Metodologi \& Perancangan Sistem](#bab-2--metodologi--perancangan-sistem)
	- [2.1 Kerangka Kerja Rekayasa \& Solusi Optik](#21-kerangka-kerja-rekayasa--solusi-optik)
	- [2.2. Alur Akuisisi \& Konsolidasi Multi-Dataset AI](#22-alur-akuisisi--konsolidasi-multi-dataset-ai)
	- [2.3 Alur Pengembangan Model AI \& Endgineering Decision Records](#23-alur-pengembangan-model-ai--endgineering-decision-records)
	- [2.4 Arsitektur Sistem, Integrasi Kode, \& Closed-Loop Hardware](#24-arsitektur-sistem-integrasi-kode--closed-loop-hardware)
	- [2.5 Digital Traceability \& Pengembangan Sistem](#25-digital-traceability--pengembangan-sistem)
- [Bab 3 – Analisis Bisnis, Tata Kelola AI, dan Resiko](#bab-3--analisis-bisnis-tata-kelola-ai-dan-resiko)
	- [3.1 Analisis Kelayakan Bisnis \& Kalkulator ROI UPI](#31-analisis-kelayakan-bisnis--kalkulator-roi-upi)
	- [3.2 Tata Kelola AI \& Manajemen Risiko](#32-tata-kelola-ai--manajemen-risiko)
- [Bab 4 – Kesimpulan](#bab-4--kesimpulan)

---

# Referensi Proposal

1. [Lomba Ellen – Proposal UISP](https://drive.google.com/file/d/1x6DdGyZQ-n9NqcOZUJBvfGjYMnqkaEXv/view?usp=drive_link) → Kreativitas dan Visual Proposal menarik + Pencantuman Lampiran 
2. [Lomba Ellen – BCC WOW Case Competiiton](https://drive.google.com/file/d/1-enK5Bs4RrdB5idlqctKtH6JjBXFRG72/view?usp=sharing) → Struktur Propoosal Sederhana + Ringkasan Eksekutif
3. [Lomba Ellen – Proposal Eureca](https://drive.google.com/drive/folders/1VEuVNpm1LWz8T5ByZSTxSUWSCoVyq0mE) → Kepadatan Implementasi (Rekomendasi Strategi + Implementasi + Kesimpulan) + Full makeover tiap halaman proposal + layouting kreatif

---

# Ringkasan Singkat Struktur Proposal

1. Cover
2. Daftar Isi
3. Ringkasan Eksekutif (opsional; 1 halaman)
4. Bab 1 – Pendahuluan (max 2–3 halaman)
	- 1.1 Latar Belakang
	- 1.2 Relevansi Tema: Smart Manufacturing
	- 1.3 Tujuan dan Manfaat Pengembangan
5. Bab 2 – Metodologi dan Perancangan Sistem (max 8–10 halaman)
	- 2.1 Kerangka Kerja Rekayasa & Solusi Optik
	- 2.2 Alur Akuisisi & Konsolidasi Multi-Dataset AI
	- 2.3 Alur Pengembangan Model AI & Engineering Decision Records
	- 2.4 Arsitektur Sistem, Integrasi Kode, & Closed-Loop Hardware
	- 2.5 Digital Traceability & Pengembangan Sistem
6. Bab 3 – Analisis Bisnis, Tata Kelola AI, dan Resiko (max 3–4 halaman)
	- 3.1 Analisis Kelayakan Bisnis & Kalkulator ROI UPI
	- 3.2 Tata Kelola AI & Manajemen Risiko
7. Bab 4 – Kesimpulan (max 1–2 halaman)
8. Lampiran 

---

> [!important] Important Note
> Semua yang di bawah, jika terdapat deskripsi terlalu mendetail seperti dalam visual harus ada apa saja, itu adalah sebuah **contoh saja**. Riilnya masih **dapat diubah-ubah dan bersifat cukup fleksibel** dalam penerapan maupun interpretasi penyampaian yang dieksekusi dalam proposal.

---

# Ringkasan Eksekutif

1. Framing Masalah Kritis & urgensi ekonomi Indonesia
	- Kontribusi ekspor perikanan Indonesia, tetapi ditolak ekspor di negara tujuan terkait regulasi FDA/RASFF
	- Data dari FDA-OASIS & RASFF mengenai penolakan yang terjadi diakibatkan kontaminasi fisik (kotor/tidak segar)
	- Framing akar masalah yang berada di UPI karena QC masih berbasis **pencatatan manual (kertas)** dengan **inspeksi mata manusia** yang **lambat**, **subjektif**, memicu **kelelahan operator**, dan **tidak memenuhi standar audit digital**
2. Penyataan solusi NusaQC & Relevansi Smart Manufacturing
	- NusaQC sebagai _AI-Powered Visual Wuality Control System_ berbasis Computer Vision (CV) dan Internet of Things (IoT)
	- Keunggulan **Closed-Loop Control** dari NusaQC → **bukan** sekadar menampilakn hasil di layar (**Smart Inspection**) → **Sistem Smart Manufactring** yang **memicu tindakan fisik secara otomatis** (menghentikan/memperlambat lini sortasi + nyalain lampu & buzzer) saat mendeteksi ikan cacat/busuk
	- Visi produk sebagai Continuous Automated Conveyor Inspector — kamera industri memindai setiap ikan secara terus-menerus seiring conveyor bergerak, tanpa interupsi alur produksi (untuk final)
3. Inti Teknologi & Inovasi Rekayasa
	- Dual-Engine AI Pipeline: 
		1. Model 1 (Freshness Classifier): MobileNetV3-Small ONNX untuk klasifikasi mutu fisik (Grade A / B / C) berdasarkan SNI 2729:2013.
		2. Model 2 (Defect Detector): YOLOv8n ONNX untuk lokalisasi kontaminasi fisik visual (_bounding box_).
	- Solusi optik → Linear-Polarizing Filter → hilangkan masalah pantulan cahaya
	- Digital traceability → catat log otomatis & Sertifikat berbasis QR Code
4. (opsional) Nilai bisnis dan dampak kuantitatif
	- Target pasar
	- Dampak yang terukut dengan data kuantitatif (e.g., peningkatan kecepatan inspeksi, reduksi penolakan ekspor, CAPEX terjangkau, estimasi ROI)

---

# Bab 1 – Pendahuluan

## 1.1 Latar Belakang

- Urgensi & nilai ekonomi sektor → kontribusi ekspor perikanan Indonesia + potensi kerugian akibat gagal memenuhi target (framing produk perikanan sebagai _highly perishable_)
- Data empiris penolakan ekspor (FDA & RSAFF)
- Akar permasalahan di UPI yang melakukan QC dengan secara **manual** dengan **kertas** sehingga **tidak memenuhi standar audit digital** dan inspeksi berdasarkan **mata manusia** yang menyebabkan proses **lambat**, **subjektif**, dan **kelelahan operator**
- Penegasan solusi NusaQC berfokus pada **indikator visual kesegaran** dan **kontaminasi fisik** dengan Computer Vision (**CV**)
- Bisa menambahkan diagram Pareto untuk penolakan ekspor FDA
- Bisa menambahkan diagram Fishbone sebagai Root Cause analysis

## 1.2 Relevansi Tema: Smart Manufacturing

- Konsolidasi penerapan AI NUsaQC sesuai dengan tema Smart Manufacturing (proses pengolahan dan operasi pabrik/UPI)
- Diferensiasi antara smart inspection dengan (True) Smart Manufacturing dimana NusaQC hadir sebagai sistem Smart Manufacturing yagn berperan aktif dengan Closed-Loop Control dengan melibatkan AI untuk menghentikan/memperlabmbat motor conveyor secara real-time ketika dibutuhkan
- Integrasi Ekosistem Otomasi → Kombinasi sensor fisik (proximity sensor), inferensi AI edge device, aktuator fisik (relay, tower light, buzzer), dan pencatatan log digital SQLite.
- Bisa menambahkan diagram perbandingan Open-Loop vs. Closed-Loop Control

## 1.3 Tujuan 

- Sesuaiin dengan permasalahan: permasalahan → solusi → tujuan → manfaat → visi

----

# Bab 2 – Metodologi & Perancangan Sistem

## 2.1 Kerangka Kerja Rekayasa & Solusi Optik

- Pendekatan hibrid **Scrum-CRISP** → Agile Scrum for Software Development + CRISP-DM/ML for siklus iterasi eksperimen AI
- Penerapan **SEI AI Engineering** → implementasi kontrak API, explicit hardware x computing ability limitations and requirements (CUDA Version, memory limti, compute availability u/backend tidak crash dengan banyaknya payload in inference time), loosely coupled design & modular architecutre (abstract inference engine & isolasi driver logic), multi-tiered checkpoints & resilience (circuit breaker ketika inference model hardware terlalu panas, atau memory leak, atau latency degradation; atau Recovery Checkpoint seperti explicit state fallbacks dan ada graceful route request untuk hardware yang lebih lambat seperti dari GPU ke CPU sebagai backup), resource-adaptive edge and backend layers (e.g., dynamic batchning and throttling, gracefule degradation), building integrated testing and monitoring (MLOps) e.g., Telemetry data integration and or automated regression pipelines

> [!NOTE]
> SEI AI Engineering terdiri dari 3 pillar prinsip dalam pembuatan AI, dan di atas merupakan contoh-contoh penerapannya, tetapi masih **belum pasti** diimplementasikan pada AI dalam kompetisi

- Pemasangan Linear Polarizing Filter pada lensa kamera optis 
- Bisa menambahkan flow diagram Hybrid Development Lifecycle (Scrum + CRIPS-ML)
- Bisa menambahkan Ray Optics Diagram (Prinsip kerja linear/cross polarizing filter) atau menambahkan contoh before and after ikan yang terkena pantulan cahaya (glare) dan sesudah dikurangi melalui linear polarization filter

## 2.2. Alur Akuisisi & Konsolidasi Multi-Dataset AI

- Penerapan Strategi Multi-Dataset Akademis → 6 dataset akademis terverifikasi u/mencegah keterbatasan data tunggal & mencegah overfitting
	1. DaFiF Dataset (Prasetyo et al., 2024): 2.536 gambar + sensor gas E-nose sebagai acuan kesegaran SNI 2729:2013.
	2. Freshness of Fish Eyes / FFE (Prasetyo et al., 2022): 4.390 gambar mata ikan untuk eye-clarity sub-engine.
	3. SalmonScan (Ahmed et al., 2024): 1.208 gambar klasifikasi infeksi fisik.
	4. Roboflow Fish Disease: 457 gambar beranotasi YOLO bounding box untuk lesi/luka.
	5. Alaa Mahmoud & BD Fish Disease: Data benchmark penyakit kulit/sisik.
- Mengambil data penunjang riset lapangan & domain adapatation → mengambil sampel foto lapangan di UPI/pasar lokal → dataset adaptasi domain real
- (opsional) Pipeline Augmentasi Albumentation → menyimulasikan kondisi riil conveyor & membuat data sintetis berdasarkan data publik dan lapangan disesuaikan dengan augmentasi albumentation → simulasi sisa kilau bash (specular highlight injection),  gerakan conveyor (motion blur), brightness/contrast jittering
- (opsional) bisa menambahkan diagram pohon sebagai pemetaanaliran 6 dataset publik + data lapangan → proses pembersihan/harmonisasi label → pipeline augmentasi albumentations → output dataset final untuk model 1 & model 2
- Matriks dataset AI NusaQC dalam bentuk tabel ringkas berisikan Nama Dataset, Sumber, Jumlah Sampel, Format Anotasi, Peran Spesifik dalam Sistem (e.g., DaFIF→ Backbone Freshness, Roboflow → YOLO Bounding Box)

## 2.3 Alur Pengembangan Model AI & Endgineering Decision Records

- Spesifikasi & Alur Kerja Dual Engine AI Pipeline: 
	- **Model 1 — Freshness Classifier (2-Tahap):**
	    - _Tahap 1 (ROI Localization):_ YOLOv8n mendeteksi dan melakukan _crop_ otomatis pada area kepala ikan (mata dan insang) dari _full frame_.
	    - _Tahap 2 (Classification):_ MobileNetV3-Small INT8 ONNX mengklasifikasikan ROI kepala menjadi Grade A, B, atau C sesuai parameter SNI 2729:2013.
	- **Model 2 — Surface Contamination & Defect Detector:**
	    - YOLOv8n ONNX Float32 mendeteksi kontaminasi visual (_sisik_sisa_, _warna_abnormal_, _luka_robekan_, _foreign_object_, _lendir_berlebih_) dengan _bounding box_.
- Logika pengambilan keputusan AI (Decision Engine)
	- Penggabungan output Model 1 & 2: Grade A + No Defect $\rightarrow$ **PASS (HIJAU)**; Grade B + Minor Defect $\rightarrow$ **CONDITIONAL (KUNING)**; Grade C ATAU Major Defect $\rightarrow$ **FAIL (MERAH)**.
- **Engineering Decision Records (EDR) berbasis Data Benchmark:**
	- _EDR-001 (Pemilihan Model Deteksi):_ Memilih YOLOv8n dibanding YOLOv8s berdasarkan data benchmark Raspberry Pi 5 (~470ms vs ~1315ms) demi menjaga latensi inferensi $\le 1,5$ detik.
	- _EDR-002 (Pemilihan Backbone Klasifikasi):_ Memilih MobileNetV3-Small ONNX dibanding ResNet/EfficientNet karena rasio akurasi-ke-latensi CPU terbaik untuk _edge device_.
- Bisa menambahkan flowchart visual dual engine AI pipeline & decision Engine:
	- Diagram alir pemrosesan citra: Input Foto Full Frame $\rightarrow$ YOLO Head Crop ROI $\rightarrow$ MobileNetV3 Freshness (Grade A/B/C) $\parallel$ YOLO Defect Bbox $\rightarrow$ Decision Matrix $\rightarrow$ Sinyal Output (PASS / CONDITIONAL / FAIL).
- Bisa menambahkan tabel Benchmark EDR (YOLOv8n vs YOLOv8s vs ResNet) → tabel komparasi kuantitatif antara model, menampilkan ukurang model (MB), latensi CPU RPi5 (ms), mAP50/F1-score, daya komputasi, etc. → pembuktian secara matematis sebagai alasan pemilihan model adalah keputusan rekayasa terbaik

## 2.4 Arsitektur Sistem, Integrasi Kode, & Closed-Loop Hardware

- Arsitektur Sistem End-to-End (3 layer)
	- _Physical Layer:_ Sensor Proximity, Kamera Industri, LED Ring Light + Polarization Filter, Relay Controller, Motor Conveyor, Stack Light, dan Buzzer.
	- _Backend & Inference Layer:_ FastAPI (Python 3.11), ONNX Runtime (CPU execution provider), dan SQLite Database.
	- _UI Layer:_ React.js + Vite Dashboard via WebSocket komunikasi _real-time_
- Alur Integrasi REST APi & Closed-Loop GPIO Control
	- Alur panggilan endpoint `POST /api/v1/inspect`: Eksekusi ONNX $\rightarrow$ Evaluasi Decision Engine $\rightarrow$ Eksekusi sinyal GPIO ke Relay Conveyor (STOP/SLOW) & Tower Light.
- (opsional banget) Mock Hardware Mode (`ENABLE_MOCK_HARDWARE=true`):
	- Skema komputasi simulasi saat variabel lingkungan aktif: Sinyal GPIO dialihkan ke _verbose terminal logs_ dan visualisasi animasi UI.
	- Menjamin juri dapat menguji seluruh alur sistem secara lokal hanya dengan perintah `docker-compose up` tanpa memerlukan fisik _hardware_.
- Bisa menambahkan diagram arsitektur sistem end-to-end: Diagram arsitektur modular yang memisahkan Hardware/Physical Layer, FastAPI/ONNX Backend Layer, dan React UI/SQLite Layer lengkap dengan garis komunikasi (GPIO, HTTP REST, WebSocket).
- Bisa menambahkan Sequence Diagram Alur Trigger hinga aktuasi Physical: Sequence diagram UML yang menggambarkan urutan waktu interaksi: Proximity Sensor $\rightarrow$ Trigger Camera Capture $\rightarrow$ POST Request ke FastAPI $\rightarrow$ Dual ONNX Session $\rightarrow$ Write SQLite $\rightarrow$ Trigger GPIO Relay $\rightarrow$ Push WebSocket ke Dashboard UI.

## 2.5 Digital Traceability & Pengembangan Sistem

- Penerapan sistem pencatatan digital traceability dengan skema database SQLite lokal setiap peristiwa inspeksi per lot produksi (`lot_id`, `timestamp`, `fish_family`, `grade`, `defects`, `confidence_score`, `image_path`).
- Penerapan keamanan cryptographic SHA-256 Hash pada tiap log
- Penerapan generasi otomatis sertifikat QC digital dengan QR code yang langsung siap didownload/diekspor untuk keperluan audit HACCP/FDA
- Bisa menambahkan diagram ERD & Mockup Sertifikat QC Digital 
- Bisa menambahkan diagram perbedaan arsitektur dari Snapshot ke Continuours Mode

---

# Bab 3 – Analisis Bisnis, Tata Kelola AI, dan Resiko 

## 3.1 Analisis Kelayakan Bisnis & Kalkulator ROI UPI

- Segementasi target pasar (right-sized market), contoh:
	- Target Pasar Primer: 400–600 Unit Pengolahan Ikan (UPI) skala menengah-besar di Indonesia yang aktif mengekspor komoditas utama (Tuna/Cakalang, Tilapia, Salmon) dan telah tersertifikasi HACCP.
	- Total Addressable Market (TAM), Serviceable Addressable Market (SAM), dan target penetrasi awal pada lini sortasi berpenggerak conveyor.
- Model Bisnsis B2B SaaS (Software & Hardware as a Service), contoh adanya tier starter dan tier business
- Unit economics & Struktur biaya → estimasi CAPEX Hardware per unit & Gross Margin bisnis dengan estimasi waktu ROI
- Simulasi ROI u/UPI → simulasi studi kasus UPI, potensi kerugian akibat penolakan ekspor, proyeksi pengematan dengan NusaQC, dan hasil dari perhitungan
- Bisa menambahkan tabel skema harga & fitur matrix B2B SaaS
- (opsional) Bisa menambahkan diagram garis/batang proyeksi/simulasi cash flow dari studi kasus

## 3.2 Tata Kelola AI & Manajemen Risiko

- Prinsip tata kelola & Etika AI (Responsible AI):
	- Penjelasan pembatasan cakupan model pada 3 familia utama (Scombridae, Cichlidae, Salmonidae) dan penanganan spesies di luar dataset dengan _label alert_ "Unsupported Species".
	- penanganan risiko false negative dengan pelatihan threshold sensitivitas tinggi pada kontaminasi fisik → kepastian tidak ada ikan cacat/busuk dalam ekspor
	- Penjelasan transparansi model dalam keputusannya dengan confidence score yang ditampilkan tiap jawaban
	- Privasi data produksi sehingga seluruh data foto dan log inspeksi disimpan secara lokasl di SQLite internal UPI 
- Matriks manajemen risiko & mitgasi opersional (Risk Register):
	- Risiko Teknis: Latensi inferensi CPU di RPi5, pantulan sinar (glare) ekstrem pada permukaan basah, serta variasi spesies regional di luar dataset.
	- Rencana Mitigasi Konkret: Pemasangan Cross-Polarization Filter, fallback skrip ke laptop CPU, penyediaan verbose log pada Mock Mode, dan checklist verifikasi blind judging sebelum submisi.
- Bisa menambahkan tabel ringkas akan risiko & strategi mitigasi (risk register table) → Kode Risiko, Deskripsi Risiko, Level Severity, Tindakan Mitigasi Terencana

---

# Bab 4 – Kesimpulan

- Berhasil menjawab penyelesaian masalah utama dengan NusaQC → penolakan ekspor perikanan Indonesia akibat kontaminasi fisik visual dan penurunan kesegaran di UPI → pengubahan proses QC menjadi sistem Smart Manufacturing yang otomatis, objektif, dan closed-loop
- Keunggulan dari Teknis dan Rekayasa Arsitektur NusaQC →Penggunaan dual-engine AI + solusi fisika optik Linear Polarization Filter + Integrasi closed-loop hardware + digital traceability + sertifikat QR code
- Dampak bisnis secara kuantitatif → peningkatan kecepatan inspeksi, reduksi reject rate, biaya hardware terjangkau, estimasi ROI 
- (ospional) Rencanan komitmen ketika masuk final → rencana detail per jam akan melakukan pengembangan apa saja ketika final dengan 10 jam Luring
- (opsional) bisa menambahkan diagram Gantt chart Garis Waktu (10-Hour Action Plan Diagram)