# Executive Summary & Ideation Guide: AI Innovation Challenge (AIC) COMPFEST 18

---

## 1. Tema & Core Focus Ideasi

* **Tema Utama:** AI for the Backbone of the Economy (Mentransformasi rantai nilai bisnis pasca-produksi primer di Indonesia).
* **3 Area Fokus Inovasi:**
  1. **Smart Manufacturing (Pabrik):** Pengolahan, efisiensi produksi, dan operasi pabrik.
  2. **Smart Logistics (Gudang & Distribusi):** Pergerakan barang, efisiensi rantai pasok, dan manajemen gudang.
  3. **Smart Commerce (Toko & Pasar):** Sisi konsumen, operasional sales, dan transaksi komersial.
* **Aturan Model AI:** 
  * Diperbolehkan menggunakan model API / Pre-trained model, **tetapi WAJIB dilakukan fine-tuning** sesuai dengan fitur/inovasi tim.
  * Dataset bisa dari data publik atau data sintetik; alur preprocessing dan pengembangan model wajib dijelaskan.

---

## 2. Ketentuan Khusus & Scope MVP (Critical Constraints)

Untuk menjaga reproduksibilitas lokal pada babak Penyisihan, ruang lingkup **Minimum Viable Product (MVP)** dibatasi secara ketat (**Dilarang Overbuilt**):

| Komponen | Batasan / Ruang Lingkup Wajib | Yang TIDAK Perlu Dibuat (Avoid) |
| :--- | :--- | :--- |
| **Frontend (FE)** | Berfokus **hanya** pada alur interaksi inti: menerima input tunggal pengguna & menampilkan output AI. | Dashboard analitik tingkat lanjut, sistem otentikasi kompleks, atau halaman riwayat. |
| **Backend (BE)** | Pemrosesan interaksi **sinkron**. Sistem lokal harus dapat dijalankan via `docker compose`. | Background jobs, automated data logging pipelines, atau database terdistribusi. |
| **Model AI** | Fungsionalitas **core inference** utama dengan parameter statis saat demo. | Auto-tuning, bulk testing scripts, atau loop umpan balik otomatis (automated feedback loop). |

> [!WARNING]
> **Catatan Penting Hardware:** Jika membuat proyek berbasis Hardware + Software, **WAJIB menyediakan Mock Data Mode** agar software dapat berjalan dan diuji panitia tanpa hardware fisik.

---

## 3. Bobot & Kriteria Penilaian Babak Penyisihan

| Kriteria Penilaian | Bobot | Detail Fokus Penilaian |
| :--- | :---: | :--- |
| **Implementasi Teknologi & Kematangan Arsitektur** | **25%** | Proporsionalitas stack/model AI, arsitektur modular (separasi FE/BE/AI bersih), kemudahan jalankan via Docker/README. |
| **Orisinalitas & Dampak Sosial** | **20%** | Keunikan, diferensiation dari solusi ada, relevansi masalah, urgensi, dan kecocokan dengan target user. |
| **Kesiapan MVP Babak Final** | **15%** | Kesesuaian batasan MVP (tidak overbuilt/underbuilt), kelayakan untuk dikembangkan pada babak 10 jam Hackathon. |
| **Video Promosi Inovasi** | **15%** | Storytelling, kejelasan penyampaian masalah & solusi AI, daya tarik investor/stakeholder. |
| **Kualitas Proposal & Proses Pengembangan** | **15%** | Rincian metodologi, data-driven decision making, alur dataset & integrasi model. |
| **Relevansi Tema** | **10%** | Kesesuaian dengan tema Backbone Economy dan integrasi AI yang alami (tidak dipaksakan). |
| **[BONUS] Business Value & Governance** | **+3.5%** | Model bisnis realistis, analisis adopsi industri, regulasi AI & etika/sistem AI bertanggung jawab. |
| **[BONUS] Kehadiran AIC Talks** | **+1.5%** | Menghadiri dan mengisi presensi sesi AIC Talks. |
| **TOTAL SKOR MAKSIMAL** | **105%** | |

---

## 4. Deliverables / Berkas Penyisihan (Deadline: 25 Agustus 2026, 23:55 WIB)

1. **Repository GitHub (Public):**
   * Berisi Source Code dengan panduan setup jelas di `README.md` dan `docker compose`.
   * Commit message **WAJIB** mengikuti standar Conventional Commits (contoh: `feat: ...`, `fix: ...`, `refactor: ...`).
2. **Video Proof of Work (Maks. 7 Menit, Unlisted YouTube):**
   * Menunjukkan jalannya MVP (working/buggy) dan alur program asli.
   * Tampilan double screen (terminal & aplikasi + timestamp).
   * Format Judul: `COMPFEST 18 AIC: PROOF OF WORK - [Nama Tim] - [Nama Proyek]`
   * ⛔ **DILARANG KERAS memotong (cut) video!** Hanya boleh fast-forward dan voice over.
3. **Video Promosi Inovasi (Maks. 5 Menit, Public YouTube):**
   * Menjelaskan latar belakang, alur perancangan, penyelesaian masalah, dan pitch antusiasme investor.
   * Format Judul: `COMPFEST 18 AIC: [Nama Tim] - [Nama Proyek]`
4. **Proposal Inovasi (PDF Maks. 20 Halaman):**
   * Struktur: Nama Tim & Judul → Latar Belakang → Tujuan & Manfaat → Metodologi (Alur Dataset, Alur Model per Feature, Alur Integrasi, Alasan Pemilihan Metode) → Kesimpulan.

---

## 5. Syarat Peserta & Tim

* **Anggota:** 3–5 orang per tim (boleh lintas institusi), maks. usia 25 tahun.
* **Mahasiswa:** Belum dinyatakan lulus hingga **6 Oktober 2026**.
* **Aturan Anonimitas:** Dilarang mencantumkan/menunjukkan nama institusi/universitas dalam bentuk apa pun pada seluruh berkas/video/karya.
* **Discord Constraint:** Ketua Wajib merubah nickname Server Discord menjadi: `[Nama Tim] [Nama]`

---

## 6. Timeline Krusial Lomba (2026)

```text
[17 Jun - 09 Jul]   Registrasi Batch 1 (FREE)
[10 Jul - 18 Jul]   Registrasi Batch 2 (Rp200.000/tim)
[18 Juli]          Technical Meeting Penyisihan (Zoom)
[25 Juli]          AIC Talks (Bonus Score 1.5%)
[25 Agustus]       DEADLINE SUBMISI PENYISIHAN (23:55 WIB)
[09 - 10 Sep]      Standby Discord (Klarifikasi / Live Demo jika dipanggil)
[11 September]     Pengumuman Top 8 Finalis
[20 September]     Sesi Mentoring Finalis (Daring)
[26 September]     BABAK FINAL: Hackathon 10 Jam (Luring Fasilkom UI)
[27 September]     Live Pitching & Awarding Night (Luring Fasilkom UI)
```

---

## 7. Alur Babak Final (Top 8 Tim)

1. **Mentoring (20 Sep):** Feedback langsung dari Expert AI & Product Management.
2. **Hackathon Luring 10 Jam (26 Sep @ Fasilkom UI):** Iterasi & penyempurnaan produk secara langsung dengan checkpoint push berkala ke GitHub.
3. **Live Pitching & Demo (27 Sep):** Presentasi & demonstrasi produk (dapat dijalankan di `localhost`) di depan para Juri.