# 🏷️ Panduan Anotasi & Taksonomi Kelas NusaQC Model 2 (Fish Defect Detector)

Dokumen ini adalah panduan acuan visual untuk melakukan anotasi & verifikasi *Bounding Box* pada **Model 2 NusaQC** (Surface Contamination & Defect Detector).

---

## 📌 Ringkasan 4 Kelas Standar NusaQC

| ID | Nama Kelas | Hotkey | Warna Label | Definisi Singkat |
|:--:|:---|:---:|:---:|:---|
| **0** | `sisik_sisa` | `1` | 🟠 Oranye | Parasit menempel, bintik parasit, sisa sisik mengelupas/kasar |
| **1** | `warna_abnormal` | `2` | 🔴 Merah | Lesi merah, pendarahan kulit, bercak Aeromoniasis, peradangan insang |
| **2** | `luka_robekan` | `3` | 🟡 Kuning | Ulserasi (luka terbuka), sirip/ekor robek (fin rot), jamur Saprolegniasis |
| **3** | `lendir_berlebih` | `4` | 🟣 Ungu | Lendir tebal keruh, White Tail Disease (WTD), mukus putih berlebih |

---

## 🔍 Detail Kriteria Visual per Kelas

### 1. `sisik_sisa` (Class ID 0) — 🟠 Oranye
* **Deskripsi Visual**: 
  - Adanya parasit menempel pada permukaan badan/bersisik ikan (misal: *Argulus* / kutu ikan, *Anchor worm* / cacing jangkar).
  - Sisik yang terlepas sebagian, mencuat, atau tekstur sisik rusak kasar berantakan.
  - Bintik-bintik putih/hitam kecil terlokalisasi akibat serangga/parasit akuakultur.
* **Termasuk dalam kelas ini**:
  - `Parasitic diseases` (PD) dari Roboflow & HF.
  - Cacing/kutu fisik yang terlihat di permukaan tubuh ikan.
* **Aturan Bounding Box**:
  - Buat bbox ketat mengelilingi area parasit atau kelompok sisik yang mencuat.

---

### 2. `warna_abnormal` (Class ID 1) — 🔴 Merah
* **Deskripsi Visual**:
  - Ruam kemerahan, bintik merah (*red spot*), pendarahan di bawah kulit/sisik (*hemorrhage*).
  - Pembengkakan merah akibat infeksi bakteri *Aeromonas* (Aeromoniasis).
  - Perubahan warna insang atau kulit tidak wajar (pudar/lebam/kehitaman lokal).
* **Termasuk dalam kelas ini**:
  - `Bacterial Red disease` (BRD)
  - `Aeromoniasis` (BDA)
  - `Bacterial gill disease` (BGD)
  - Discoloration / kemerahan pada area perut/punggung.
* **Aturan Bounding Box**:
  - Buat bbox melingkupi seluruh area bercak kemerahan/peradangan warna kulit.

---

### 3. `luka_robekan` (Class ID 2) — 🟡 Kuning
* **Deskripsi Visual**:
  - **Luka Terbuka (Ulcer)**: Daging ikan terlihat robek, berlubang, atau terkelupas sampai lapisan dalam.
  - **Cacat Sirip/Ekor (Fin Rot / Tail Rot)**: Sirip dada, punggung, atau ekor gerabah, robek, atau putus.
  - **Infeksi Jamur (Saprolegniasis)**: Serabut benang putih/abu-abu seperti benang kapas yang tumbuh melingkupi luka robekan.
* **Termasuk dalam kelas ini**:
  - `Fungal diseases Saprolegniasis` (FDS)
  - `Skin Ulcer` / `Tail Rot` / `Fin Rot`
  - Robekan akibat benturan fisik / jaringan terputus.
* **Aturan Bounding Box**:
  - Melingkupi area jaringan yang robek/berlubang dan benang jamur di sekitarnya.

---

### 4. `lendir_berlebih` (Class ID 3) — 🟣 Ungu
* **Deskripsi Visual**:
  - Lapisan mukus/lendir yang sangat tebal, keruh, atau memutih di permukaan badan/ekor ikan.
  - **White Tail Disease (WTD)**: Ekor atau tubuh bagian belakang menjadi pucat/putih keruh karena penumpukan lendir pekat akibat infeksi virus/bakteri.
  - Bercak putih menyebar (bukan serabut benang jamur) berupa selaput lendir.
* **Termasuk dalam kelas ini**:
  - `White tail disease` (WTD)
  - `Excess mucus` / lapisan lendir abnormal.
* **Aturan Bounding Box**:
  - Melingkupi area selaput lendir keruh/putih yang menutupi bagian tubuh ikan.

---

## 🛑 Aturan Khusus (Edge Cases & Boundary Rules)

1. **Ikan Sehat (`Healthy Fish`)**:
   - Jika citra adalah ikan sehat tanpa cacat/penyakit, **JANGAN buat Bounding Box sama sekali** (biarkan label kosong/empty background).

2. **Tumpang Tindih Defek (Overlap)**:
   - Jika ada daerah luka robek yang *sekaligus* ada pendarahan merah disekitarnya, prioritaskan **`luka_robekan`** jika jaringan daging rusak/berlubang.
   - Jika hanya berupa ruam/merah tanpa luka terbuka, tandai sebagai **`warna_abnormal`**.

3. **Perbedaan Jamur vs Lendir**:
   - **Jamur (`luka_robekan`)**: Berbentuk serabut seperti **kapas/benang timbul** yang menancap pada luka.
   - **Lendir (`lendir_berlebih`)**: Berbentuk **lapisan selaput licin/keruh memutih** yang merata di permukaan kulit/ekor.
