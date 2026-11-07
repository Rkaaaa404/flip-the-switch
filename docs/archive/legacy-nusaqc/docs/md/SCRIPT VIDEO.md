# Panduan & Script Video Proof of Work (PoW) - NusaQC MVP

  

Dokumen ini berisi panduan lengkap dan *script voice over* (VO) untuk mendemonstrasikan sistem NusaQC pada video Proof of Work (PoW) babak penyisihan AIC COMPFEST 18.

  

---

  

## 1. Koherensi MVP, Proposal, & Guidebook

  

Sebelum masuk ke script video, penting untuk memahami *positioning* aplikasi saat ini agar narasi video sejalan dengan proposal (`FIX_NusaQC_Proposal_AIC_COMPFEST18_2026_v3.md`) dan desain fitur (`NusaQC_Storage_Dispatch_Design.md`).

  

### **Apa yang Sudah Dibangun (Scope MVP Saat Ini):**

Aplikasi saat ini telah mewujudkan **Digital Traceability Chain** (Rantai Keterlacakan Digital) end-to-end yang menjadi *core value* smart manufacturing NusaQC:

1. **Inspection & Sorting**: Menggunakan AI Vision (Snapshot mode) untuk klasifikasi Grade (A/B/C) dan deteksi Defek Fisik (*Filthy*), memicu sinyal hardware (Conveyor Reject).

2. **Lot History & Human-in-the-loop**: Log inspeksi permanen di SQLite dengan kemampuan Supervisor untuk melakukan *Override Decision* (AI Governance).

3. **Lot Storage Map**: Menempatkan ikan yang lulus QC (PASS) ke dalam slot penyimpanan (Cold/Frozen Zone).

4. **Export Dispatch**: Memilih lot dari *storage* untuk dimuat ke dalam kontainer ekspor berdasarkan pesanan *buyer*.

  

### **Mengapa ini Relevan dengan Proposal & Guidebook?**

Sistem ini menjawab *Gap 3* di proposal: transisi dari QC manual (paper-based) ke **Digital Traceability**. NusaQC tidak hanya menjawab *"apakah ikan ini layak?"*, tetapi memastikan *"ikan yang layak, kini ada di mana dan dikirim ke siapa?"*. Hal ini menyelesaikan *root cause* penolakan ekspor (*filthy*) oleh FDA/RASFF dengan bukti audit digital.

  

### **Apa Scope untuk Final Hackathon (Jangan Didemokan Sekarang, Tapi Di-Mention):**

Untuk mematuhi batasan MVP rulebook COMPFEST, beberapa fitur sengaja ditahan untuk babak final 10 jam:

- Transisi dari **Snapshot Inspection** (foto manual per klik) menjadi **Continuous Video Streaming** di atas conveyor.

- **Export to PDF** Manifest / Sertifikat QC (saat ini hanya aktif Export CSV).

- **IoT Temperature Monitoring** untuk memantau suhu Storage secara *real-time*.

  

---

  

## 2. Script Voice Over (VO) Video per Halaman

  

*Tips: Perekam layar (screen record) harus mengikuti aksi yang disebutkan di kolom Visual.*

  

### **A. Pengantar (0:00 - 0:15)**

- **Visual:** Tampilkan halaman `Dashboard`, sorot kursor ke arah statistik harian.

- **Voice Over (VO):** "Halo, ini adalah Proof of Work dari NusaQC, sistem *Quality Control* dan *Traceability* ikan otomatis untuk Unit Pengolahan Ikan skala ekspor. Di Dashboard ini, manajer pabrik dapat memantau tingkat kelulusan QC secara *real-time*."

  

### **B. Halaman Inspection (0:15 - 0:45)**

- **Visual:** Pindah ke tab `Inspection`. Klik "Upload or Capture Image", pilih foto ikan, klik "Run AI Inspection". Tunjukkan hasil Grade, Bounding box cacat, dan simulasi sinyal Conveyor Actuator (hijau/merah).

- **VO:** "Sistem ini menggunakan Computer Vision. Saat ikan melewati kamera, sistem memindainya secara instan. Terdapat dua model yang bekerja: klasifikasi kesegaran standar SNI, dan deteksi defek fisik seperti sisa sisik atau luka. Jika terdeteksi cacat di bawah standar, sistem otomatis mengirimkan sinyal *REJECT* berwarna merah ke aktuator conveyor."

  

### **C. Halaman Lot History & Detail (0:45 - 1:15)**

- **Visual:** Pindah ke `Lot History`. Tunjukkan tabel, lalu klik tombol **View** pada salah satu ikan yang *FAIL* atau *CONDITIONAL*.

- **Visual di Detail:** Sorot Bounding box di foto, scroll ke bagian *Inspector Note*, ketikkan catatan lalu *Save*. Klik tombol *Override Decision*, pilih *PASS*, ketik alasan, dan submit.

- **VO:** "Seluruh hasil QC dicatat permanen dalam basis data lokal untuk *traceability*. Di halaman Detail Lot, kita bisa melihat bukti visual defek. Sesuai prinsip *AI Governance* di proposal kami, NusaQC menyediakan kontrol *Human-in-the-Loop*. Supervisor dapat menambahkan catatan manual, atau membatalkan keputusan AI jika diperlukan melalui fitur *Override*."

  

### **D. Halaman Lot Storage (1:15 - 1:40)**

- **Visual:** Pindah ke `Lot Storage`. Tunjukkan panel *Pending Storage* di kanan. Klik salah satu slot kosong (warna putih) di bagian *Cold Zone* untuk memindahkan ikan dari status *Pending* ke slot tersebut. Klik slot yang sudah terisi (biru) untuk melihat detailnya.

- **VO:** "NusaQC bukan hanya alat deteksi, tapi rantai keterlacakan utuh. Ikan yang lolos QC (PASS) akan masuk ke antrean *Storage*. Operator dapat mengalokasikan ikan-ikan tersebut ke slot penyimpanan spesifik di *Cold Zone* atau *Frozen Zone*, sehingga lokasi fisik setiap lot ikan di pabrik selalu terlacak."

  

### **E. Halaman Export Dispatch (1:40 - 2:05)**

- **Visual:** Pindah ke `Dispatch`. Klik "+ New Dispatch". Isi nama Buyer, pilih destinasi, lalu centang 2 atau 3 ikan dari daftar *storage* di bawahnya. Klik Create.

- **VO:** "Ketika ikan siap diekspor, operator membuat rekaman *Dispatch*. Mereka memilih *buyer*, negara tujuan, dan memilih lot ikan dari *storage* untuk dimasukkan ke kontainer. Ini menciptakan bukti *Digital Traceability* akhir bahwa produk yang diekspor telah 100% melewati proses QC NusaQC."

  

### **F. Halaman Settings & Penutup (2:05 - 2:30)**

- **Visual:** Pindah ke `Settings`. Ubah slider *AI Confidence Threshold* (misal dari 75% ke 90%). Sorot tombol *Save*.

- **VO:** "Sebagai fleksibilitas standar mutu pabrik, *Confidence Threshold* AI dapat diatur secara dinamis, yang akan langsung memengaruhi sensitivitas deteksi defek dan kelulusan Grade B. Untuk MVP ini, fitur ekspor PDF dan pemrosesan video streaming kontinyu belum kami aktifkan, dan telah kami rencanakan secara khusus untuk diimplementasikan pada sesi *Hackathon Final* 10 jam. Terima kasih."

  

---

  

## 3. Checklist Penting Sebelum Rekaman

  

1. **Siapkan Data Dummy/Mock**: Pastikan database sudah terisi beberapa data (bisa manfaatkan tombol auto-inspect beberapa kali di halaman inspection).

2. **Siapkan Gambar Ikan**: Siapkan 2-3 gambar ikan (segar dan cacat) di folder lokal PC untuk di-upload saat demo halaman *Inspection*.

3. **Uji Coba Flow**: Lakukan *dry-run* (latihan klik) sesuai urutan A sampai F di atas tanpa direkam terlebih dahulu.

4. **Bersihkan UI**: Pastikan tidak ada pesan *error console* atau tampilan *glitch* sebelum mulai merekam layar.