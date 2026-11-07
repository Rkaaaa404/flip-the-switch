# LAPORAN EVALUASI KRITIS & STRESS-TEST IDE INNOVATION (DEVIL'S ADVOCATE REPORT)

**Proyek:** NusaQC — *AI-Powered Visual Quality Control & Digital Traceability System untuk Unit Pengolahan Ikan (UPI) Indonesia*  
**Kompetisi:** AI Innovation Challenge (AIC) COMPFEST 18  
**Peran Evaluator:** Super Critical AI Judge, Senior Tech Evaluator, & Lead Devil's Advocate  
**Target Dokumen:** `Laporan_Analisis_Bedah_Ide_NusaQC.md` (17 Poin Analisis)  

---

> [!IMPORTANT]
> **Tujuan Laporan Evaluasi:** Membedah celah logika, membedah asumsi naif/terlalu optimis, mendeteksi klaim tanpa dasar faktual, serta memberikan rekomendasi pengetatan teknis dan bisnis agar argumen NusaQC **kedap air (airtight)** di hadapan dewan juri AI Innovation Challenge COMPFEST 18.

---

## A. Ringkasan & Kesesuaian Lomba (Poin 1–2)

### 1. Ringkasan Ide Utama (Executive Summary)
1. **Devil's Advocate Critique:**
   * **Asumsi Naif Otomatisasi QC:** Mengklaim MobileNetV3 (Freshness) dan YOLOv8n (Contamination) dapat "menggantikan" QC manual secara utuh adalah klaim yang berbahaya. Model Computer Vision (CV) hanya membaca *surface/visual features*. CV **tidak bisa mendeteksi pembusukan kimiawi/biokimia internal** seperti *Total Volatile Basic-Nitrogen* (TVB-N), pembentukan *histamin*, atau kontaminasi bakteriologi (*Salmonella*, *E. coli*) yang terperangkap dalam jaringan daging tanpa gejala visual luar.
   * **Klaim Penyebab Penolakan:** Menyatakan NusaQC "langsung menargetkan akar masalah utama 80% penolakan ekspor FDA" adalah over-claim. Sebagian besar penolakan FDA berlabel *filthy* atau *Salmonella* berasal dari pengujian laboratorium mikro/kimia, bukan sekadar debu atau sisik sisa yang tampak oleh YOLOv8n.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Breakdown rincian data FDA Import Refusal: Berapa persen dari label *filthy* yang murni berupa **cacat makro visual** (dapat ditangkap kamera) vs **bakteriologik/mikroskopik/kimiawi** (wajib tes lab).
   * `[BUTUH DATA FAKTUAL]` Benchmarking kecepatan inferensi $<3$ detik per sampel: Wajib menyertakan spesifikasi hardware Edge nyata (misal: Intel N100 / Raspberry Pi 5 / CPU Laptop i5) beserta ukuran resolusi input image ($224\times224$ vs $640\times640$).
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Revisi Positioning:** Ubah narasi dari *"menggantikan proses QC manual"* menjadi **"Sistem Triase Awal (First-Line Visual Screening & AI Copilot)"**.
   * **Definisikan Batasan Visual:** Secara eksplisit bedakan antara *Visual Defect* (mata pudar, pendarahan, luka permukaan, sisa sisik/jeroan) yang ditangani NusaQC dengan *Chemical/Microbiological Test* yang tetap menjadi domain QC Laboratorium.

---

### 2. Keterkaitan Tema & Subtema AIC COMPFEST 18
1. **Devil's Advocate Critique:**
   * **Kerancuan Skop Supply Chain vs Manufacturing:** Proposal mengklaim 100% selaras dengan *Smart Manufacturing* di pabrik (UPI), tetapi mempromosikan *Digital Traceability*. Apabila sistem hanya mencatat data di meja inspeksi pabrik tanpa terkoneksi ke ID kapal/lokasi tangkap di hulu atau kontainer pendingin di hilir, maka ini **bukan True Traceability**, melainkan sekadar **In-Plant Inspection Logging System**. Juri supply chain akan dengan mudah mematahkan istilah ini.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Data komparatif kebocoran nilai (economic loss): Sertakan persentase kerugian mutu yang terjadi *di dalam lini pengolahan UPI* dibanding kerugian saat transportasi di laut/kapal.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Pertegas Istilah:** Gunakan istilah yang lebih akurat: **"In-Plant Batch Traceability"** atau **"Internal Lot Traceability"** untuk menghindari tuduhan *over-promising* rantai pasok end-to-end.
   * **Perkuat Argumentasi Smart Manufacturing:** Jelaskan bahwa efisiensi manufaktur terjadi karena pencegahan pemrosesan bahan baku *reject* lebih awal (*early defect removal*), sehingga menghemat energi pembekuan (*freezing cost*) dan jam kerja buruh sortasi.

---

## B. Validasi Masalah & Kebutuhan Pengguna (Poin 5, 7, 10)

### 3. Urgensi & Dampak Masalah (Poin 5)
1. **Devil's Advocate Critique:**
   * **BLUNDER KASUS CS-137 (2026):** Pencantuman kasus penolakan udang PT Bahari Makmur Sejati akibat radioaktif Cs-137 sebagai pembenaran NusaQC adalah **kesalahan fatal**. Kamera RGB dan model AI Vision **SAMA SEKALI TIDAK BISA mendeteksi zat radioaktif**. Memasukkan ini akan menghancurkan kredibilitas teknis tim di mata juri.
   * **Bias Korelasi Bitung:** Penurunan kapasitas tuna Bitung dari 70 ton ke 40 ton/hari & 14.000 PHK lebih didorong oleh kelangkaan pasokan bahan baku (*raw material supply shortage*) akibat regulasi moratorium kapal dan persaingan pasokan, bukan murni karena "inefisiensi QC manufaktur".
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Hapus/ganti kasus Cs-137 dengan data kasus penolakan FDA yang murni berakar dari *Visual Decomposition / Physical Contamination / Parasites*.
   * `[BUTUH DATA FAKTUAL]` Data empiris kerugian finansial akibat *re-work* (proses ulang sortasi) dan *downgrade price* (penurunan kelas mutu) langsung di tingkat pabrik UPI Indonesia.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Eliminasi Kasus Cs-137:** Ganti dengan kasus riil FDA Import Refusal report pada produk *frozen snapper/tuna/shrimp* yang ditolak akibat "Filthy - Contains Parasites / Foreign Matter" atau "Decomposed".
   * **Fokus pada Direct Cost of Poor Quality (COPQ):** Buat kalkulasi dampak finansial: berapa biaya pembekuan & kontainer yang terbuang percuma jika 1 lot (misal 20 ton) ditolak di pelabuhan tujuan.

---

### 4. Validasi Kebutuhan Pengguna (Poin 7)
1. **Devil's Advocate Critique:**
   * **Realita Lingkungan Pabrik Basah:** Pekerja QC di UPI menangani ratusan ikan per jam dalam lingkungan basah, dingin ($10-15^\circ\text{C}$), menggunakan sarung tangan tebal, dan bekerja sangat cepat. Jika NusaQC mengharuskan pekerja memegang mouse/keyboard atau menekan layar untuk meng-capture foto satu per satu ($<3$ detik/sampel), ini akan **memperlambat lini produksi (creating new bottleneck)**.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Standar *speed / throughput* inspeksi manual saat ini (ekor/menit) di lini sortasi UPI skala menengah-besar vs estimasi throughput NusaQC.
   * `[BUTUH DATA FAKTUAL]` Angka *human error rate* atau penurunan akurasi inspector akibat kelelahan mata (*eye fatigue*) setelah jam kerja ke-4 dan ke-8.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Mekanisme Sampling Kuantitatif:** Jelaskan bahwa NusaQC tidak memaksa inspeksi 100% sampel secara lambat, melainkan menerapkan **Statistical Quality Control / Lot Acceptance Sampling** (misal mengacu pada ISO 2859-1) atau *continuous conveyor belt capture*.
   * **Zero-Touch Hardware Interfacing:** Rancang skenario pengoperasian dengan pedal kaki (*foot switch*), sensor jarak (*infrared proximity sensor*), atau auto-capture interval agar pekerja tidak menyentuh perangkat.

---

### 5. Flow Masalah ke Solusi (Problem-to-Solution Flow) (Poin 10)
1. **Devil's Advocate Critique:**
   * **Lompatan Logika "Zero Export Rejection":** Flow diagram menggambarkan: *Dual-Model AI Inferencing* $\rightarrow$ *Zero Export Rejection*. Ini adalah asumsi yang terlalu menyepelekan konteks. AI hanya memberikan output data; jika tindakan mitigasi di lapangan tidak dieksekusi (misal: produk reject tetap dicampur oleh oknum pekerja), penolakan ekspor tetap terjadi.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Ganti klaim absolut "Zero Export Rejection" dengan metrik berbasis persentase riset: misal *"Estimasi penurunan risiko penolakan visual hingga X%"*.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Masukkan Closed-Loop Physical Action:** Pada flow diagram, tambahkan langkah *Physical Segregation / Actionable Alert* (misal: AI Detect Reject $\rightarrow$ Signal Warning Lamp / Interlock Gate / Auto-Stamp Flagged Lot).

---

## C. Analisis Inovasi, Relevansi Bisnis & Skalabilitas (Poin 3, 4, 6, 18, 19)

### 6. Inovasi & Diferensiasi (Poin 3)
1. **Devil's Advocate Critique:**
   * **Diferensiasi Dual-Model yang Standar:** Menjalankan MobileNetV3 + YOLOv8n secara bersamaan di REST API adalah standar pipeline CV industri, bukan terobosan ilmiah baru.
   * **Kelemahan Dataset Primer 800 Gambar:** Mengklaim 800 gambar dari Pasar Pabean Surabaya sebagai pilar diferensiasi utama "Domain Adaptation" adalah pernyataan yang riskan. Angka 800 gambar sangat kecil untuk pelatihan deep learning dan rentan *overfitting*.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Variasi dalam 800 data primer: Berapa jumlah spesies, berapa variasi sudut pencahayaan, dan berapa distribusi kelas (Grade A/B/C)?
   * `[BUTUH DATA FAKTUAL]` Metrik performa kuantitatif (mAP@50 untuk YOLO, F1-Score untuk MobileNet) sebelum dan sesudah digabungkan dengan dataset primer.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Perkuat Strategi Augmentasi & Transfer Learning:** Jelaskan penggunaan teknik *Albumentations, Synthetic Defect Generation (MixUp/CutMix), dan Mosaic Augmentation* untuk melipatgandakan data primer dari 800 menjadi $5.000+$ sampel efektif.
   * **Tekankan Inovasi Pipeline:** Ganti klaim "inovasi model AI" menjadi **"Inovasi Sistem: Low-Latency Multi-Task Edge Inference Architecture"** yang mengintegrasikan klasifikasi organ sensori dan deteksi cacat permukaan dalam 1 single-pass payload JSON.

---

### 7. Relevansi & Pertumbuhan Bisnis (Poin 4)
1. **Devil's Advocate Critique:**
   * **Logika Peningkatan Margin yang Cacat:** Proposal mengklaim NusaQC meningkatkan gross margin UPI 2-3x lipat dengan mengonversi bahan baku mentah menjadi produk olahan fillet Grade A. **AI QC tidak bisa mengubah kualitas fisik ikan yang memang sudah busuk dari nelayan!** Mutu bahan baku awal adalah pembatas (*Garbage In, Garbage Out*).
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Data selisih harga (price premium) antara ikan yang lolos sertifikasi mutu ekspor Grade A vs Grade B/C pasar domestik.
   * `[BUTUH DATA FAKTUAL]` Dasar kalkulasi klaim "efisiensi biaya operasional 60%".
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Revisi Kerangka Value Creation:** Posisikan NusaQC sebagai **"Margin Protection & Waste Elimination Engine"**. Efisiensi biaya diperoleh dari: (1) Menghentikan pemrosesan ikan reject sebelum masuk mesin fillet/freezer (hemat listrik & buruh), dan (2) Mencegah penalti/klaim retur dari buyer ekspor.

---

### 8. Eksekusi Global (Poin 18)
1. **Devil's Advocate Critique:**
   * **Klaim Adaptabilitas Compliance FDA SIMP:** FDA SIMP (*Seafood Import Monitoring Program*) mewajibkan pencatatan *Key Data Elements* (KDE) seperti *Vessel Flag, Harvest Area, Catch Document Number*, bukan sekadar skor kesegaran visual ikan. Menjanjikan compliance FDA SIMP hanya dengan skor AI visual adalah kesalahan pemahaman regulasi.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Daftar variabel wajib KDE FDA SIMP dan EU Regulation 178/2002.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Integrasi Schema Data Compliance:** Tunjukkan bahwa skema database NusaQC memetakan field standar FDA SIMP (Vessel ID, Harvest Date, Lot Weight) dan menggabungkannya dengan *AI Visual Certificate ID* menjadi satu payload QR Code audit.

---

### 9. Model Bisnis (Poin 19)
1. **Devil's Advocate Critique:**
   * **KONTRADIKSI LOGIKA UTAMA (Edge Offline vs SaaS Subskripsi):** Proposal menyatakan NusaQC beroperasi **"100% Offline Edge Inference Core"** demi mengatasi kendala internet di pabrik. Namun di saat bersamaan, proposal menjual **"B2B SaaS Subscription Rp 1.500.000 / bulan"**. Jika sistem berjalan 100% offline di CPU lokal pabrik, **mengapa pelanggan harus membayar subskripsi SaaS bulanan**? Mengapa mereka tidak memutus internet dan memakai software lokal selamanya tanpa bayar?
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Rincian CapEx (biaya hardware starter kit) vs OpEx per lini produksi di UPI.
   * `[BUTUH DATA FAKTUAL]` Benchmarking harga kompetitor / software ERP pabrik olahan pangan di Indonesia.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Selesaikan Kontradiksi dengan Arsitektur Hybrid:** Jelaskan bahwa *Inference Engine* berjalan Edge-Offline untuk *real-time execution*, tetapi membutuhkan **Cloud Synchronization Periodik** (misal setiap akhir shift) untuk: (1) Sync log audit ke cloud portal buyer/auditor, (2) Lisensi & health check, dan (3) Menerima *Model Weight Updates* hasil fine-tuning berkala.

---

### 10. Analisis Adopsi Industri (Poin 6)
1. **Devil's Advocate Critique:**
   * **Spesifikasi Enclosure Hardware yang Salah (IP65 vs IP69K):** Proposal menyebutkan hardware enclosure menggunakan standar **IP65**. Di lini pengolahan ikan (pabrik makanan basah), area selalu dibersihkan dengan semprotan air bertekanan tinggi dan bahan kimia sanitasi (*high-pressure washdown*). **IP65 pasti akan bocor/berembun**. Standar industri manufaktur makanan basah wajib **IP66 / IP69K / NEMA 4X**.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Standar regulasi *Food Grade Sanitation Enclosure* (ISO 14159 / EHEDG) untuk perangkat elektronik di area basah pengolahan hasil laut.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Koreksi Spesifikasi Hardware:** Naikkan spesifikasi enclosure menjadi **IP66/IP69K Stainless Steel 316 Casing** dengan *gasket food-grade silicone* dan pelindung lensa anti-fogging.

---

## D. Desain Produk, MVP & Iterasi Masa Depan (Poin 8, 13, 14, 15, 16)

### 11. Fitur Utama (MVP Babak Penyisihan) (Poin 8)
1. **Devil's Advocate Critique:**
   * **Resiko Persepsi "Over-Simplified":** Menyebutkan secara eksplisit bahwa Frontend "DILARANG/DIHINDARI: Dashboard analitik rumit, Auth kompleks" sudah sesuai batasan Guidebook. Namun jika penyampaian dalam proposal terlalu defensif, juri bisa menganggap aplikasi NusaQC terlalu dangkal atau sekadar *crud app* sederhana.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Pemetaan langsung kriteria penilaian babak penyisihan AIC COMPFEST 18 terhadap fitur MVP yang disajikan.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Kemudikan Narasi "Lean Perfection":** Bingkai pembatasan MVP sebagai **"Deterministic & Robust Core Engine Focus"**—menjamin *zero-crash*, inferensi cepat, dan 100% *reproducibility* saat dievaluasi oleh panitia.

---

### 12. Fleksibilitas & Ruang Pengembangan Babak Final (Poin 13)
1. **Devil's Advocate Critique:**
   * **OVER-PROMISING EXTREME PADA FINAL 10 JAM:** Proposal menjanjikan di babak final 10 jam akan membangun: (1) Real-time RTSP Video Stream, (2) Multi-Camera Batch Pipeline, dan (3) **RAG Compliance Chatbot (LangChain/Ollama)**.
   * Mengimplementasikan RAG Chatbot lokal + RTSP streaming dalam hackathon 10 jam adalah rencana yang sangat berisiko tinggi (*high probability of failure*). RAG Chatbot juga **tidak memberi nilai tambah langsung** pada inti masalah inspeksi visual manufaktur.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Estimasi resource GPU & latency eksekusi Ollama/LLM lokal pada environment hackathon 10 jam tanpa koneksi internet stabil.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Pangkas Skop Babak Final:** **COREK RAG CHATBOT!** Ganti dengan fitur final yang highly-impactful & realistis dibuat 10 jam: (1) **Live WebCam Stream Inference (Real-time Overlay)**, dan (2) **Automated PDF Export Certificate with Cryptographic QR Code**.

---

### 13. Metodologi Pengembangan Produk (Poin 14, 15, 16)
1. **Devil's Advocate Critique:**
   * **Timeline Tanpa Buffer Freeze Code:** Sprint 4 berlangsung hingga tanggal 25 Agustus (hari deadline submisi). Tidak ada alokasi *freeze code* atau *emergency buffer* jika terjadi bug tak terduga saat rendering video atau build Docker.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Jadwal rinci alokasi jam training GPU, kompilasi ONNX, rendering video POW (7 menit), dan final review proposal.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Geser Freeze Code ke H-3 (22 Agustus 2026):** Tetapkan tanggal 22 Agustus sebagai penghentian seluruh pengembangan kode. Tanggal 23–25 Agustus murni dialokasikan untuk pengetesan Docker Compose di clean OS, produksi video POW/Promo, dan audit dokumen proposal.

---

## E. Arsitektur Teknis, Sistem & AI (Poin 9, 11, 12, 20, 21, 22, 23)

### 14. Arsitektur Sistem & Tech Stack (Poin 9, 11)
1. **Devil's Advocate Critique:**
   * **Potensi Thread Blocking pada FastAPI CPU Inference:** FastAPI berjalan secara *asynchronous* (ASGI). Namun, pemanggilan ONNX Runtime pada CPU adalah operasi yang *CPU-bound* dan *synchronous*. Jika request dikirim bersamaan dari beberapa meja inspeksi ke endpoint `POST /predict`, ONNX Runtime akan **mengunci (block) event loop Uvicorn**, menyebabkan *request queueing* dan latency melonjak tinggi.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Benchmark throughput (RPS & p99 Latency) FastAPI + ONNX Runtime CPU under concurrent load (misal: 10-20 concurrent requests).
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Implementasi Async Threadpool Wrapper:** Gunakan `starlette.concurrency.run_in_threadpool` atau `asyncio.to_thread()` untuk memisahkan eksekusi inferensi ONNX dari main event loop Uvicorn:
     ```python
     @app.post("/predict/freshness")
     async def predict_freshness(file: UploadFile = File(...)):
         image_bytes = await file.read()
         result = await asyncio.to_thread(onnx_engine.run, image_bytes)
         return result
     ```

---

### 15. Modularitas Sistem (Clean Decoupled Architecture) (Poin 12)
1. **Devil's Advocate Critique:**
   * **Overhead Inter-Container Network Latency:** Memisah sistem menjadi 3 container Docker terpisah (`nusaqc-frontend`, `nusaqc-backend`, `nusaqc-ai-engine`) menambah kompleksitas konfigurasi jaringan Docker dan menyumbang *HTTP network overhead* (10–30 ms) antar container backend dan AI engine.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Latency perbandingan: Microservice Inter-container REST call vs Embedded ONNX Runtime inside Backend Process.
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Gunakan Embedded Micro-Architecture:** Untuk MVP Penyisihan, gabungkan `nusaqc-ai-engine` langsung ke dalam `nusaqc-backend` sebagai Python internal module. Ini memangkas latency jaringan inter-container menjadi $0\text{ ms}$ dan menyederhanakan `docker-compose.yml` menjadi 2 container saja (Frontend + Backend).

---

### 16. Fokus Core AI Inference (Parameter Input-Output) (Poin 20)
1. **Devil's Advocate Critique:**
   * **Kelemahan Parameter Input ROI:** Schema JSON Model 1 membutuhkan input `"roi_type": "eye_or_gill"`. Ini artinya **user/pekerja harus secara manual memilih** apakah foto yang diunggah adalah mata atau insang. Ini memperburuk UX di lapangan.
   * **Kelemahan Bounding Box Pixel Absolut:** Model 2 mengembalikan koordinat bboxes dalam pixel absolut `[120, 45, 210, 130]`. Jika resolusi gambar dari kamera berubah atau di-resize di Frontend, bounding box canvas overlay akan **meleset/dislokasi**.
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Standardisasi koordinat objek YOLO (Normalized Coordinates $0.0 - 1.0$).
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **Normalisasi Bounding Box:** Ubah output bounding box Model 2 menjadi nilai ternormalisasi $[x_{center}, y_{center}, width, height]$ berkisar $0.0 - 1.0$:
     ```json
     "bbox_normalized": [0.325, 0.187, 0.141, 0.095]
     ```
   * **Auto-Crop / Unified Model Input:** Hilangkan parameter manual `"roi_type"`. Biarkan model menerima gambar kepala/badan ikan secara utuh dan melakukan automatic ROI cropping atau multi-label classification.

---

### 17. Dataset & Model AI Spesifik (Poin 21, 22, 23)
1. **Devil's Advocate Critique:**
   * **KRITIK TEKNIS BESAR: PEMILIHAN DATASET MVTEC AD YANG SALAH DOMAIN:** Proposal mencantumkan dataset **D7 (MVTec Anomaly Detection)** untuk fine-tuning Model 2 (YOLOv8n deteksi cacat ikan). MVTec AD berisi gambar anomali komponen industri buatan manusia (*bottle, cable, hazelnut, metal nut, screw, tile, leather, wood*). **Tekstur permukaan komponen logam/plastik industri sangat berbeda radikal dengan tekstur daging/sisik/lendir biologis ikan.** Menggunakan MVTec AD untuk fine-tuning detektor cacat ikan adalah kelemahan logika transfer learning yang sangat fatal dan akan dibantai oleh juri pakar AI/CV!
2. **Flag Fact-Check (`[BUTUH DATA FAKTUAL]`):**
   * `[BUTUH DATA FAKTUAL]` Pertanyakan relevansi MVTec AD terhadap fitur visual *seafood defect*.
   * `[BUTUH DATA FAKTUAL]` Cari dan gantikan dengan dataset domain-specific (misal: Roboflow Fish Defect Datasets, DeepFish Dataset, atau Kaggle Fish Disease/Defect Datasets).
3. **Rekomendasi Pengetatan (Mitigasi):**
   * **REVISI KRITIS DATASET MODEL 2:** **Hapus MVTec AD dari daftar fine-tuning Model 2!** Gantikan matriks dataset Model 2 menjadi:
     * **Roboflow Seafood/Fish Surface Defect Dataset** (Data sekunder publik spesifik cacat ikan/fillet).
     * **Data Primer NusaQC (D6/D10)** (Pengumpulan mandiri sampel cacat nyata).
     * **Data Sintetis Defect (D11)** (Overlay gambar parasit/luka/sisik rusak di atas gambar ikan bersih via script Python PIL/OpenCV).
   * **Pertegas Justifikasi Metrik Evaluasi:** Pertahankan pertimbangan ilmiah mengapa **Recall ($\ge 85\%$) diprioritaskan di atas Precision ($\ge 80\%$)** pada deteksi kontaminasi: *False Negative* (kontaminasi lolos ekspor) berisiko denda triliunan dan penolakan kontainer FDA, sedangkan *False Positive* hanya memicu re-inspeksi manual internal.

---

## SUMMARY OF CRITICAL FIXES FOR THE TEAM

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SUMMARY ACTION PLAN: FIXING THE RED THREAD                      │
├───────────────────┬──────────────────────────────────┬─────────────────────────────────┤
│ Aspek             │ Masalah / Celah Teridentifikasi  │ Solusi Mitigasi Wajib           │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ **Logika Kasus**  │ Menyebut penolakan radiasi Cs-137│ Ganti dengan kasus FDA Import   │
│                   │ (kamera RGB tidak bisa deteksi)  │ Refusal murni visual filthy.    │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ **Model Bisnis**  │ Kontradiksi: 100% Offline Edge   │ Jelaskan Hybrid Edge-Cloud: Edge│
│                   │ vs Monthly SaaS Subskripsi       │ offline, Cloud sync log & update│
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ **Hardware Spec** │ Menulis Enclosure IP65           │ Naikkan ke IP66/IP69K Stainless │
│                   │ (pasti rusak di washdown UPI)    │ Steel 316 Food-Grade Casing.    │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ **Dataset AI**    │ Menggunakan MVTec AD             │ Hapus MVTec AD! Ganti dengan    │
│                   │ (salah domain: metal/screw)      │ Roboflow Fish Defect Dataset.   │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ **AI Inference**  │ Bounding Box Pixel Absolut &     │ Ubah Bounding Box ke Normalized │
│                   │ Manual Input ROI Type            │ (0-1) & hilangkan ROI dropdown. │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ **Final Hackathon│ Over-promising RAG Chatbot       │ Coret RAG Chatbot! Fokus pada   │
│ ** (10 Jam)**     │ lokal dalam 10 jam hackathon     │ Live WebCam Stream & PDF Export.│
└───────────────────┴──────────────────────────────────┴─────────────────────────────────┘
```
