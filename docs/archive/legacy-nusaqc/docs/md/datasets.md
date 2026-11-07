# Daftar Dataset Akuakultur & Kesehatan Ikan (Fish & Shrimp Datasets)

Dokumen ini berisi daftar dataset yang digunakan untuk klasifikasi penyakit, kesegaran, serta deteksi objek pada ikan dan udang.

---

## 📊 Ringkasan Dataset (Dataset Overview)

| No | Dataset | Tugas Utama (Task) | Jumlah Sampel | Jumlah Kelas | Sumber |
|:--:|:--- |:--- |:--- |:--- |:--- |
| 1 | **Fish Disease Dataset (panda992)** | `Image Classification` | 2,450 Gambar | 7 Kelas (Ikan) | [Hugging Face](https://huggingface.co/datasets/panda992/fish_disease_datasets) |
| 2 | **SalmonScan** | `Image Classification` | 1,208 Gambar | 2 Kelas | [Mendeley Data](https://data.mendeley.com/datasets/x3fz2nfm4w/1) |
| 3 | **Dataset for Fish’s Freshness Problems** | `Multimodal (Image + Sensor)` | 2,536 Gambar & 9,401 Sensor | 3 Spesies | [Mendeley Data](https://data.mendeley.com/datasets/vx4ptwk3pb/1) |
| 4 | **The Freshness of the Fish Eyes Dataset (FFE)** | `Image Classification` | 4,392 Gambar Mata | 24 Kelas (8 Spesies × 3 Tingkat Kesegaran) | [Mendeley Data](https://data.mendeley.com/datasets/xzyx7pbr3w/1) |
| 5 | **Alaa Mahmoud - Fish Disease** | `Image Classification` | 305 Gambar | 2 Kelas | [Kaggle](https://www.kaggle.com/datasets/alaamahmoud2010/fish-disease) |
| 6 | **Roboflow - Fish Disease Object Detection** | `Object Detection` | 457 Gambar | Annotations Bounding Box (BDA, BGD, BRD, dll) | [Roboflow Universe](https://universe.roboflow.com/yolo-eq1f5/fish-disease-qvxvl) |

---

## 1. Fish Disease Dataset (panda992)

* **Tugas (Task)**: `Image Classification`
* **Sumber**: [HuggingFace - panda992/fish_disease_datasets](https://huggingface.co/datasets/panda992/fish_disease_datasets) (public, no token needed)
* **Provenance**: Sumber asli data ikan dari BD Fish & Shrimp Disease Dataset (Saon110). Dataset panda992 berisi subset ikan saja tanpa data udang.
* **Domain**: Akuakultur, Patologi Ikan

### Deskripsi
Dataset gambar untuk klasifikasi penyakit ikan yang berisi 2.450 gambar berkualitas tinggi terbagi dalam 7 kategori penyakit ikan. Dataset ini merupakan subset ikan dari koleksi asli BD Fish & Shrimp Disease (Saon110), tanpa data udang.

### Spesifikasi Dataset
* **Total Gambar**: 2.450 gambar (Format JPG/PNG)
* **Resolusi**: Variasi (tangkapan asli)
* **Pembagian Dataset (Split)**:
  * **Train**: 2.082 gambar
  * **Test**: 368 gambar

### Kategori Penyakit & Distribusi Kelas

#### 🐟 Penyakit Ikan (7 Kelas - Total 2.450 Gambar)
1. **Bacterial Red disease** (label 0): Infeksi bakteri yang menyebabkan lesi merah pada tubuh ikan.
2. **Bacterial diseases - Aeromoniasis** (label 1): Disebabkan oleh bakteri *Aeromonas*, umum pada ikan air tawar.
3. **Bacterial gill disease** (label 2): Infeksi pada jaringan insang yang menyebabkan gangguan pernapasan.
4. **Fungal diseases Saprolegniasis** (label 3): Infeksi jamur berupa pertumbuhan menyerupai kapas.
5. **Healthy Fish** (label 4): Ikan sehat tanpa penyakit sebagai pembanding.
6. **Parasitic diseases** (label 5): Berbagai infeksi parasit umum pada akuakultur.
7. **Viral diseases White tail disease** (label 6): Infeksi virus yang ditandai dengan pemutihan daerah ekor.

> **Catatan**: Dataset asli Saon110 juga memiliki 4 kelas udang (3.808 gambar), namun tidak digunakan dalam NusaQC. Dataset panda992 sudah hanya berisi data ikan.

<details>
<summary><b>📌 Rincian Distribusi Jumlah Gambar per Split Set</b></summary>

| Nama Kelas | Train Set | Validation Set | Test Set | Total |
| :--- | :---: | :---: | :---: | :---: |
| `Fish_Bacterial Red disease` | 207 | 59 | 31 | 297 |
| `Fish_Bacterial diseases - Aeromoniasis` | 207 | 59 | 30 | 296 |
| `Fish_Bacterial gill disease` | 203 | 58 | 29 | 290 |
| `Fish_Fungal diseases Saprolegniasis` | 205 | 58 | 30 | 293 |
| `Fish_Healthy Fish` | 210 | 60 | 30 | 300 |
| `Fish_Parasitic diseases` | 212 | 60 | 31 | 303 |
| `Fish_Viral diseases White tail disease` | 212 | 60 | 31 | 303 |
| `Shrimp_Black_Gill` | 388 | 111 | 56 | 555 |
| `Shrimp_Healthy` | 1484 | 424 | 212 | 2120 |
| `Shrimp_White_Spot_Syndrome_Virus` | 381 | 109 | 55 | 545 |
| `Shrimp_White_Spot_Syndrome_Virus_and_Black_Gill` | 409 | 117 | 59 | 585 |
| **Total** | **4,118** | **1,175** | **594** | **5,887** |

</details>

---

## 2. SalmonScan: Fish Disease Detection in Salmon Aquaculture

* **Tugas (Task)**: `Image Classification`
* **Sumber**: [Mendeley Data](https://data.mendeley.com/datasets/x3fz2nfm4w/1)
* **DOI**: `10.17632/x3fz2nfm4w.1` (Publikasi: 27 Februari 2024, Version 1)
* **Kontributor**: Md Shoaib Ahmed

### Deskripsi
Dataset *SalmonScan* merupakan koleksi gambar ikan salmon yang ditujukan untuk deteksi/klasifikasi kesehatan dan penyakit pada sistem budidaya salmon. Gambar diambil dari berbagai perspektif, skala, dan kondisi pencahayaan.

### Spesifikasi Dataset
* **Total Gambar**: 1.208 gambar
* **Pembagian Kelas**:
  1. 🐟 **Fresh salmon** (Ikan sehat tanpa tanda penyakit): **456 gambar**
  2. 🐠 **Infected Salmon** (Ikan terinfeksi penyakit): **752 gambar**

### Data Preprocessing & Augmentasi
1. **Resizing**: Seluruh gambar diubah ukurannya menjadi **600 × 250 piksel**.
2. **Augmentasi Gambar**:
   * *Horizontal Flip* ↩️ & *Vertical Flip* ⬆️
   * *Rotation* 🔄 & *Random Cropping* 🪓
   * *Gaussian Noise* 🌌 & *Shearing* 🌆
   * *Contrast Adjustment*: Penyesuaian kontras menggunakan Gamma Correction ⚖️ dan Fungsi Sigmoid ⚖️.

---

## 3. Dataset for Fish’s Freshness Problems

* **Tugas (Task)**: `Multimodal (Image Classification + Sensor Analysis + Organoleptic)`
* **Sumber**: [Mendeley Data](https://data.mendeley.com/datasets/vx4ptwk3pb/1)
* **DOI**: `10.17632/vx4ptwk3pb.1` (Publikasi: 19 Maret 2024, Version 1)
* **Kontributor**: Eko Prasetyo, Nanik Suciati, Ni Putu Sutramiani, Adi Ananda, Ayu Putu Wiweka Krisna Dewi

### Deskripsi
Dataset multimodal untuk mengevaluasi tingkat kesegaran ikan. Menggabungkan data sensor penciuman elektronik (e-nose), gambar digital berbentuk persegi, serta hasil pengujian organoleptik berdasarkan **Standard Nasional Indonesia (SNI) 2729:2013**.

### Spesifikasi Dataset
* **Spesies Ikan**: 3 Spesies (*Mackerel* / Kembung, *Tilapia* / Nila, *Tuna*)
* **Data Sensor**: **9.401 sampel** data sensor dari **MQ-135** dan **TGS 2602** untuk masing-masing dari ketiga spesies.
* **Data Gambar**:
  * **Mackerel**: 859 gambar JPG
  * **Tilapia**: 840 gambar JPG
  * **Tuna**: 837 gambar JPG
  * **Total Gambar**: **2.536 gambar JPG**
* **File Spreadsheet (Sensor/Organoleptik)**: **63 file Excel (`.xlsx`)** rekapitulasi data (21 sesi × 3 spesies).

### 📁 Konteks Struktur Direktori (Berdasarkan `treeDaFiF.txt`)
Data dikumpulkan dalam hierarki bertingkat berdasarkan **Hari Eksperimen (Day)**, **Sesi Perekaman (Session)**, dan **Spesies Ikan (Species)**:
$$\text{Day [1..11]} \longrightarrow \text{Session [1..2]} \longrightarrow \text{[Mackerel | Tilapia | Tuna]}$$

* **Eksperimen 11 Hari**: Berlangsung dari `Day 1` hingga `Day 11`.
* **21 Sesi Perekaman**: `Day 1` memiliki 1 sesi (`Session 2`), sedangkan `Day 2` hingga `Day 11` masing-masing memiliki 2 sesi (`Session 1` & `Session 2`).
* **Format File per Folder Spesies**:
  * Berisi **~40 gambar JPG** per sesi.
  * Berisi **1 file Excel (`.xlsx`)** yang merekap data sensor e-nose dan skor organoleptik untuk sesi tersebut (contoh: `19-01-2024(Makarel).xlsx`, `Rekap Tongkol 28 Sesi 1.xlsx`, dll).

<details>
<summary><b>📌 Rincian Struktur Direktori & Distribusi File per Hari (DaFiF)</b></summary>

| Hari | Sesi Perekaman | Mackerel (JPG + Excel) | Tilapia (JPG + Excel) | Tuna (JPG + Excel) | Total Gambar Sesi |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Day 1** | Session 2 | 60 JPG + 1 .xlsx | 40 JPG + 1 .xlsx | 60 JPG + 1 .xlsx | 160 JPG |
| **Day 2** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 3** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>20 JPG + 1 .xlsx | 120 JPG<br>100 JPG |
| **Day 4** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 5** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 6** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 7** | Session 1<br>Session 2 | 39 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 41 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 8** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 9** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Day 10** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 36 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 116 JPG<br>120 JPG |
| **Day 11** | Session 1<br>Session 2 | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 40 JPG + 1 .xlsx<br>40 JPG + 1 .xlsx | 120 JPG<br>120 JPG |
| **Total** | **21 Sesi** | **859 JPG + 21 .xlsx** | **840 JPG + 21 .xlsx** | **837 JPG + 21 .xlsx** | **2.536 JPG + 63 .xlsx** |

</details>

---

## 4. The Freshness of the Fish Eyes Dataset (FFE)

* **Tugas (Task)**: `Image Classification`
* **Sumber**: [Mendeley Data](https://data.mendeley.com/datasets/xzyx7pbr3w/1)
* **DOI**: `10.17632/xzyx7pbr3w.1` (Publikasi: 1 Februari 2022, Version 1)
* **Kontributor**: Eko Prasetyo, Raden Dimas Adityo, Nanik Suciati, Chastine Fatichah

### Deskripsi
Dataset *Freshness of the Fish Eyes* (FFE) dirancang khusus untuk mengklasifikasikan tingkat kesegaran ikan berdasarkan analisis visual gambar mata ikan. Dataset terdiri dari 8 spesies ikan di mana masing-masing spesies dibagi ke dalam 3 tingkat kesegaran:
* **Highly Fresh**: Hari ke-1 & 2
* **Fresh**: Hari ke-3 & 4
* **Not Fresh**: Hari ke-5 & 6

### Spesifikasi Dataset
* **Total Gambar**: 4.390 gambar mata ikan (berdasarkan direktori `treeFFE.txt`; publikasi mencantumkan 4.392 gambar)
* **Total Kelas**: **24 kelas** (8 Spesies × 3 Tingkat Kesegaran)

### 📁 Konteks Struktur Direktori (Berdasarkan `treeFFE.txt`)
Dataset ini diorganisir secara flat langsung di direktori utama menjadi **24 folder kelas**, dengan format penamaan folder:
$$\text{[Nama Spesies]} - \text{[Tingkat Kesegaran]}$$

Setiap folder berisi gambar mata ikan (`.jpg`) sesuai kelas spesifiknya.

<details>
<summary><b>📌 Rincian Distribusi Gambar per Folder Kelas (FFE Tree)</b></summary>

| Nama Spesies | Highly Fresh (H1-2) | Fresh (H3-4) | Not Fresh (H5-6) | Total Gambar (Tree) |
| :--- | :---: | :---: | :---: | :---: |
| *Chanos Chanos* (Bandeng) | 168 | 162 | 170 | 500 |
| *Eleutheronema Tetradactylum* (Kurau) | 80 | 80 | 80 | 240 |
| *Johnius Trachycephalus* | 80 | 80 | 80 | 240 |
| *Nibea Albiflora* | 173 | 125 | 121 | 419 |
| *Oreochromis Mossambicus* (Mujair) | 289 | 174 | 162 | 625 |
| *Oreochromis Niloticus* (Nila) | 328 | 231 | 246 | 805 |
| *Rastrelliger Faughni* (Kembung) | 336 | 216 | 217 | 769 |
| *Upeneus Moluccensis* (Biji Nangka) | 310 | 252 | 230 | 792 |
| **Total** | **1.764** | **1.320** | **1.306** | **4.390** |

</details>

---

## 5. Alaa Mahmoud - Fish Disease Dataset

* **Tugas (Task)**: `Image Classification`
* **Sumber**: [Kaggle - Fish Disease](https://www.kaggle.com/datasets/alaamahmoud2010/fish-disease)
* **Lisensi**: Open Dataset

### Deskripsi
Dataset klasifikasi biner sederhana untuk membedakan antara kondisi ikan yang segar/sehat (*Fresh Fish*) dan ikan yang terinfeksi/sakit (*Infected Fish*).

### Spesifikasi Dataset
* **Total Gambar**: 305 gambar
* **Kategori Kelas**:
  1. `FreshFish`: 163 gambar
  2. `InfectedFish`: 142 gambar

---

## 6. Roboflow - Fish Disease Object Detection Dataset

* **Tugas (Task)**: `Object Detection` *(YOLO Format)*
* **Sumber**: [Roboflow Universe - yolo-eq1f5/fish-disease-qvxvl](https://universe.roboflow.com/yolo-eq1f5/fish-disease-qvxvl)
* **Lisensi**: Open Source (Roboflow Universe)

### Deskripsi
Dataset khusus untuk tugas **Object Detection** (Deteksi Objek) guna mendeteksi lokasi spesifik penyakit/lesi pada tubuh ikan menggunakan *bounding boxes*. Sangat cocok digunakan untuk melatih model arsitektur YOLO (misal: YOLOv8, YOLOv9, YOLOv10, YOLO11).

### Spesifikasi Dataset
* **Total Gambar**: ~457 gambar beranotasi
* **Format Anotasi**: Bounding Box (YOLO, Pascal VOC, COCO JSON, dll.)
* **Label / Tag Bounding Box**: Berbagai jenis gejala penyakit ikan (termasuk kode penyakit seperti `BDA`, `BGD`, `BRD`, dll.)