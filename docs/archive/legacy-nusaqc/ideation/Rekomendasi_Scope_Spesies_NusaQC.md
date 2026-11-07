# Rekomendasi Scope Spesies & Strategi AI Quality Control (NusaQC - COMPFEST 18 AIC)

---

## 🎯 1. Ringkasan Rekomendasi Scope Tim

> **Formulasi Scope Utama (Core MVP Scope):** **4 Spesies Utama** yang berasal dari **Dataset 3 (DaFiF)** (*Mackerel* / Kembung, *Tilapia* / Nila, *Tuna* / Tongkol) dan **Dataset 2 (SalmonScan)** (*Salmon*).
> 
> **Scope Tambahan / Kondisional (Conditional Expansion):** **8 Spesies Mata Ikan dari Dataset 4 (FFE)** serta **Dataset Penyakit/Objek Deteksi (Dataset 1, 5, & 6)** yang digunakan sebagai *benchmark cross-domain* dan validasi generalisasi model jika waktu/resource memungkinkan.

### Mengapa Formulasi Ini Sangat Ideal & Realistis?
1. **Fokus & Eksekusi MVP Matang (Kesepakatan Tim):**
   * **3 Spesies DaFiF (Dataset 3)** memberikan pondasi **Multimodal (Visual + E-Nose Sensor MQ-135/TGS-2602 + Organoleptik SNI 2729:2013)** untuk komoditas utama Indonesia: Kembung (*Mackerel*), Nila/Mujair (*Tilapia*), dan Tongkol (*Tuna*).
   * **1 Spesies SalmonScan (Dataset 2)** memberikan kapabilitas **Deteksi Infeksi/Kesehatan Surface** (*Fresh vs Infected Salmon*).
2. **Kesesuaian dengan Bobot Penilaian (Kesiapan MVP 15% & Arsitektur AI 25%):**
   Fokus pada 4 spesies utama memastikan demo di *localhost* berjalan *smooth*, tanpa beban komputasi berlebih, namun tetap memiliki analisis multimodal yang sangat kuat.
3. **Ekspansi Kondisional yang Fleksibel:**
   Spesies pendukung dari **Dataset 4 (FFE)** (*Bandeng, Kurau, Biji Nangka, Croaker, dll.*) serta dataset penyakit lainnya dapat ditarik secara kondisional untuk membuktikan *Taxonomy-Aware Transfer Learning* saat penulisan proposal atau demo tahap lanjut.

---

## 📊 2. Matriks Pemetaan Scope Komoditas & Dataset (Sinkron dengan `datasets.md`)

Berikut adalah pemetaan komprehensif yang telah dicocokkan secara presisi dengan penomoran dan nama dataset pada [datasets.md](file:///D:/main/Documents/explore/compe/hackhathon/AIC/datasets.md):

### 🌟 Tier 1: Scope Utama / Core MVP (Sepakat Tim)

| Kelompok / Spesies Utama | Spesies & Nama Latin | Sumber Dataset di `datasets.md` | Karakteristik Data & Peran Industri |
| :--- | :--- | :--- | :--- |
| **1. Pelagis Kecil (Kembung)** | • *Mackerel* (*Rastrelliger sp.*) | **Dataset 3: DaFiF**<br>*(859 JPG + 21 .xlsx)* | **Multimodal Kesegaran (Visual + E-Nose + SNI):** Ikan pelagis kecil konsumsi lokal & ekspor. Pengujian degradasi mioglobin & gas pembusukan. |
| **2. Air Tawar / Budidaya (Nila)** | • *Tilapia* (*Oreochromis sp.*) | **Dataset 3: DaFiF**<br>*(840 JPG + 21 .xlsx)* | **Multimodal Kesegaran (Visual + E-Nose + SNI):** Komoditas utama akuakultur budidaya Indonesia. |
| **3. Pelagis Besar (Tongkol/Tuna)** | • *Tuna / Tongkol* (*Euthynnus affinis*) | **Dataset 3: DaFiF**<br>*(837 JPG + 21 .xlsx)* | **Multimodal Kesegaran (Visual + E-Nose + SNI):** Komoditas ekspor maritim utama. Risiko pembentukan histamin tinggi. |
| **4. Salmon (Kesehatan & Infeksi)** | • *Salmon* (*Salmo salar*) | **Dataset 2: SalmonScan**<br>*(1,208 JPG)* | **Visual Disease / Infection Detection:** Klasifikasi biner kondisi fisik luar (*Fresh Salmon* vs *Infected Salmon*). |

---

### 🔄 Tier 2: Scope Kondisional / Pengujian Generalisasi (Optional / Secondary)

| Kelompok / Fungsi Dataset | Spesies yang Dicakup | Sumber Dataset di `datasets.md` | Peran & Penggunaan Kondisional |
| :--- | :--- | :--- | :--- |
| **Freshness of Fish Eyes (FFE)** | • *Chanos chanos* (Bandeng)<br>• *Eleutheronema tetradactylum* (Kurau)<br>• *Johnius trachycephalus* (Gelama)<br>• *Nibea albiflora* (Croaker)<br>• *Upeneus moluccensis* (Biji Nangka)<br>• *Oreochromis spp.* & *Rastrelliger sp.* | **Dataset 4: FFE**<br>*(4,390 JPG Mata, 24 Kelas)* | **Validasi Generalisasi Mata Ikan:** Digunakan secara kondisional jika tim ingin memperluas fitur inspeksi visual kesegaran mata ke 8 spesies regional. |
| **Fish & Shrimp Disease Benchmark** | • Berbagai Ikan & Udang (Bakteri, Jamur, Parasit, Virus WSSV, Black Gill) | **Dataset 1: BD Fish & Shrimp Disease**<br>*(5,887 Gambar, 11 Kelas)* | **Validasi Penyakit Spesifik:** Pengujian deteksi lesi/penyakit akuakultur spesifik udang & ikan tawar. |
| **Binary Fresh/Infected Baseline** | • Ikan Umum (*FreshFish* vs *InfectedFish*) | **Dataset 5: Alaa Mahmoud**<br>*(305 Gambar)* | **Baseline Testing:** Pengujian awal klasifikasi biner sederhana. |
| **Object Detection & Bounding Box** | • Berbagai Ikan (Gejala BDA, BGD, BRD, dll.) | **Dataset 6: Roboflow Fish Disease**<br>*(457 Gambar Beranotasi YOLO)* | **Object Detection Model:** Digunakan jika MVP membutuhkan *bounding box* lokasi luka/lesi spesifik pada tubuh ikan. |

---

## 🚀 3. Strategi "Selling Points" untuk Juri COMPFEST 18

Gunakan 3 argumen strategis berikut di dalam dokumen proposal dan video promosi:

1. **Pondasi Multimodal yang Solid (Visual + E-Nose Sensor + Organoleptik SNI):**
   > *"NusaQC tidak hanya mengandalkan aspek visual mata/kulit, tetapi mengintegrasikan data sensor penciuman e-nose (MQ-135 & TGS 2602) dan skor standar SNI 2729:2013 dari Dataset DaFiF untuk 3 komoditas strategis Indonesia (Kembung, Nila, Tongkol), ditambah deteksi patologi visual dari SalmonScan."*

2. **Arsitektur Modular yang Scalable (Core 4 Spesies + Flexible Expansion):**
   > *"Dengan arsitektur modular, NusaQC terbukti tangguh pada 4 spesies core MVP dan dapat langsung diekspansi ke 8 spesies mata ikan (Dataset FFE) serta deteksi penyakit udang/ikan (Dataset 1 & 6) secara plug-and-play tanpa merombak total pipeline."*

3. **Solusi Langsung Standar Mutu Ekspor & SNI 2729:2013:**
   > *"Seluruh hasil prediksi diharmonisasikan secara ketat ke dalam 3 tier mutu: Grade A (Skor 8–9, Export Grade), Grade B (Skor 7–7.9, Domestic Grade), dan Grade C (Skor < 7, Reject Grade)."*

---

## 🛠️ 4. Batasan Execution Scope pada Hackathon (MVP 10 Jam)

Agar produk tidak dinilai **Overbuilt** atau **Underbuilt** oleh Juri (Kriteria MVP 15%):

* **Tampilan Frontend (UI Dashboard):**
  Sediakan **Dropdown Select Preset Komoditas**:
  * `[Core Preset 1: Kembung / Mackerel (Multimodal DaFiF)]`
  * `[Core Preset 2: Nila / Tilapia (Multimodal DaFiF)]`
  * `[Core Preset 3: Tongkol / Tuna (Multimodal DaFiF)]`
  * `[Core Preset 4: Salmon Disease Inspection (SalmonScan)]`
  * `[Optional Preset: Regional Eye Freshness (FFE 8 Species)]`
* **Inference Backend:**
  Satu *pipeline* sinkron OpenCV + ONNX Runtime yang menjalankan:
  * **MobileNetV3-Small / Lightweight CNN** -> Output Grade Kesegaran A/B/C + Prediksi E-Nose
  * **YOLOv8n (Float32)** -> Output Bounding Box Cacat/Luka/Penyakit (dari Dataset 2 / Dataset 6)

---

## 📝 5. Draf Teks Tambahan untuk Proposal (`Proposal_Inovasi_NusaQC_COMPFEST18.md`)

Potongan paragraf berikut dapat disisipkan ke **Bab III (3.2 Konsolidasi Dataset)**:

```markdown
### 3.2 Strategi Multi-Commodity & Scope Konsolidasi Dataset

Guna menjamin efisiensi pengembangan MVP dan keberterimaan industri, NusaQC menetapkan **4 Spesies Core MVP** yang mencakup 3 komoditas utama Indonesia dari **Dataset 3 (DaFiF: Mackerel, Tilapia, Tuna)** dan 1 model benchmark penyakit dari **Dataset 2 (SalmonScan: Salmo salar)**. 

Dataset DaFiF memberikan keunggulan multimodal (integrasi citra digital + 9.401 sampel sensor e-nose MQ-135/TGS-2602 + evaluasi organoleptik SNI 2729:2013), sementara SalmonScan memperkuat aspek visual disease classification. Selain itu, NusaQC menyiapkan skema ekspansi kondisional berbasis **Dataset 4 (FFE)** untuk 8 spesies mata ikan regional serta **Dataset 1 & 6** untuk deteksi lesi objek ber-bounding box.
```
