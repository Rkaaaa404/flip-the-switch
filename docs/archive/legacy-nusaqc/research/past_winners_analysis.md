# Analisis Pemenang Terdahulu (Past Winners Analysis) - AI Innovation Challenge (AIC)

Dokumen ini berisi hasil ekstraksi ringkasan dari 3 proyek pemenang terdahulu AIC (`ADA SPARTANS`, `Mechaminds`, dan `Tunarasa`) serta **Analisis Pola Pemenang (Winning Patterns)** untuk membantu penyusunan ideasi dan arsitektur pada AIC 2026 (*Theme: AI for the Backbone of the Economy*).

---

## 1. Ekstraksi Proyek Pemenang Terdahulu

### A. ADA SPARTANS — Project "Setorin"
* **Domain / Topik:** Pengelolaan & Daur Ulang Sampah Plastik (Circular Economy & Smart Waste Management).
* **Problem Framing:** Indonesia menghasilkan 60+ juta ton sampah/tahun, <10% botol plastik didaur ulang, menimbulkan kerugian ekonomi triliunan rupiah & beban lingkungan TPA.
* **Solusi & Fitur Utama:**
  * **`Temuin`**: Peta/fitur lokasi pencarian *Smart Bin* terdekat.
  * **`Duitin`**: Scan QR botol plastik via kamera smartphone $\rightarrow$ deteksi otomatis merek, ukuran, dan volume botol $\rightarrow$ mengonversi sampah menjadi reward/poin nilai ekonomi bagi warga.
  * **`Setorin` (Core Supply Chain Hub)**: Menghubungkan supply sampah terisolasi dari warga langsung ke pabrik daur ulang, memberikan kepastian pasokan bahan baku bersih & terprediksi.
* **Multi-Stakeholder Impact:**
  * **Warga (Sumber Material):** Insentif ekonomi dari sampah.
  * **Pabrik / Industri Daur Ulang:** Pasokan bahan baku bersih terukur & terprediksi.
  * **Pemerintah:** Menurunkan akumulasi TPA & biaya pengelolaan sampah daerah.
* **Alur Transformasi Nilai:** `Sampah → Data → Logistik → Nilai Ekonomi`.

---

### B. Mechaminds — Project "Skill Quest"
* **Domain / Topik:** EdTech & Pengembangan Talenta Digital Pemrograman (Python Course AI).
* **Problem Framing:** Ketimpangan kualitas lulusan IT di Indonesia (97% lulusan IT gagal seleksi awal perusahaan tech; data Kominfo & VP Engineering Bukalapak).
* **Solusi & Fitur Utama:**
  * **`Tanya Silva`**: Asisten Virtual / AI Tutor interaktif pendamping belajar coding (Python).
  * **`Code Playground`**: IDE / Sandbox interaktif real-time di browser untuk menulis, menguji, dan debug kode.
  * **`Forum Diskusi`**: Wadah kolaborasi, tanya-jawab, dan interaksi antar komunitas pengguna.
* **AI Pipeline & Metrik Eksperimen:**
  * **Dataset & Fine-Tuning:** Data publik + synthetic dataset dari API Gemini / OpenAI.
  * **Iterasi Eksperimen:** 129x trial running, 155x deployment running.
  * **Metrik Evaluasi Khusus:** Menggunakan **FBD (Feature-Based Distance / Semantic Similarity)** sebagai metrik utama menggantikan F1-Score tradisional agar dapat menilai kesamaan makna kode/jawaban meski sintaks berbeda.
* **Tech Stack System:**
  * **Frontend:** Laravel (Blade), Tailwind CSS, Flowbite UI (Responsive Mobile/Desktop).
  * **Backend:** Laravel (MVC), MySQL, Midtrans (Payment Gateway), WebSockets (Real-time update status bayar & balasan forum).

---

### C. Tunarasa — Project "Tuna Rasa"
* **Domain / Topik:** Inklusivitas Pelayanan Publik bagi Disabilitas Pendengaran (Smart City, SDGs 10 & 16).
* **Problem Framing:** 0,4% penduduk Indonesia mengalami disabilitas pendengaran, namun hanya 4,1% yang memakai alat bantu dengar $\rightarrow$ memicu kesenjangan komunikasi di ruang publik.
* **Solusi & Fitur Utama:**
  * **Computer Vision Gesture Translator:** Penerjemah bahasa isyarat (SIBI) real-time dari kamera.
  * **LLM Sentence Corrector & Chatbot:** Memperbaiki teks hasil CV menjadi kalimat natural dan berfungsi sebagai chatbot pelayanan publik.
  * **RAG Knowledge Base Upload:** Super Admin dapat mengunggah PDF regulasi/layanan baru ke Vector DB untuk memperbarui pengetahuan AI.
  * **Auto Summary & PDF QR Code:** Rangkaian percakapan di-summary otomatis dan dikonversi menjadi file PDF via QR Code.
  * **Content-Based Recommendation System:** Rekomendasi topik/pertanyaan populer berbasis clustering.
* **AI Pipeline & Metrik Kuantitatif:**
  * **CV Model:** TensorFlow & MediaPipe (Akurasi awal CV: 78%).
  * **Hybrid CV + LLM Synergy:** Gabungan CV + LLM correction menaikkan akurasi terjemahan akhir hingga **98%**.
  * **LLM Evaluation Metrics:** Quality Score 80%, Pass Rate 86.5%, Question Answering Accuracy 82%.
  * **RAG Architecture:** LangChain, Ollama/LLaMA, Pinecone Vector DB.
  * **Recommendation Evaluation:** K-Means Clustering dengan Silhouette Score 0.6.
* **Tech Stack & System Observability:**
  * **Frontend & DB:** Supabase (Auth + PostgreSQL database).
  * **Backend:** FastAPI (Python).
  * **System Monitoring / Observability:** Grafana, Prometheus, Zipkin (Dipal).

---

## 2. Analisis Pola Pemenang (Winning Patterns Analysis)

Meskipun tema lomba berganti setiap tahun (misal: *Smart City*, *EdTech*, *Sustainability* $\rightarrow$ tahun ini: ***AI for the Backbone of the Economy***), terdapat pola universal yang selalu dibawa oleh tim pemenang:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        WINNING FORMULA MATRIX                          │
├───────────────────────────────────────┬────────────────────────────────┤
│ 1. Multi-Stakeholder Ecosystem        │ Menghubungkan 2-3 Pihak Real   │
│ 2. Hybrid AI & Synergy Pipeline       │ Multi-model (CV + LLM / Fine)  │
│ 3. Rigorous Empirical AI Metrics      │ Metrik Spesifik (Silhou, FBD)  │
│ 4. Production-Ready System Integrity │ WebSocket, RAG, Monitoring DB  │
│ 5. Data-Driven Problem Pitching       │ Fakta Kuantitatif Indonesia    │
└───────────────────────────────────────┴────────────────────────────────┘
```

### 1. Ecosystem / Multi-Stakeholder Focus (Bukan Cuma 1 User)
* **Pola:** Solusi pemenang **tidak pernah hanya menjadi aplikasi 1-arah** untuk konsumen akhir. Mereka selalu menghubungkan ekosistem bisnis (misal: *Warga $\leftrightarrow$ Industri Daur Ulang*, *User Disabilitas $\leftrightarrow$ Admin Layanan Publik*, *Siswa $\leftrightarrow$ Industri Tech*).
* **Implikasi untuk AIC 2026 (Backbone Economy):** Solusi wajib menghubungkan setidaknya **2 aktor utama** dalam rantai nilai pasca-produksi (contoh: *Petani/Nelayan/IKM $\leftrightarrow$ Pabrik Pengolahan $\leftrightarrow$ Offtaker/Distributor*).

### 2. Sinergi Hybrid AI (Multimodal / Multi-Stage Pipeline)
* **Pola:** Pemenang menggabungkan minimal 2 komponen AI yang saling melengkapi (*Synergy*).
  * *Tunarasa:* Computer Vision (78%) + LLM Refinement $\rightarrow$ Akurasi naik ke 98%.
  * *Setorin:* Vision / OCR Scan + Supply Chain Predictive Analytics.
* **Implikasi untuk AIC 2026:** Penggunaan AI tidak boleh terasa "tempelan". Menggabungkan misal *Visual Quality Control (CV)* dengan *Demand Forecasting / LLM Assistant (Tabular / NLP)* akan memberikan nilai teknis yang sangat tinggi.

### 3. Metrik Evaluasi Model yang Spesifik & Ilmiah
* **Pola:** Tim pemenang tidak sekadar bilang "Model kami akurat", tetapi menyajikan metrik spesifik:
  * Metrik non-standar yang disesuaikan (*Feature-Based Distance* untuk kode di Mechaminds).
  * Metrik clustering (*Silhouette Score 0.6* di Tunarasa).
  * Metrik evaluasi RAG / LLM (*Quality Score 80%*, *Pass Rate 86.5%*).
  * Jumlah eksperimen (*129 trial runs, 155 deployment runs*).
* **Implikasi untuk AIC 2026:** Pada proposal dan video proof of work, sertakan grafik/tabel evaluasi kuantitatif (mAP50, Precision/Recall, Latensi ONNX, atau Pass Rate).

### 4. Kematangan Arsitektur Hardware/Software & Observability
* **Pola:** Pemenang menyajikan sistem yang utuh (*dockerized*, *clean architecture*, real-time communication via WebSockets, bahkan monitoring via Grafana/Prometheus).
* **Implikasi untuk AIC 2026:** Sesuai batasan MVP penyisihan (`docker compose` lokal, sinkron), arsitektur modular yang bersih antara FE, BE, dan Inference Server akan dinilai tinggi (Bobot Arsitektur = 25%).

### 5. Storytelling & Problem Framing Berbasis Data Indonesia
* **Pola:** Membuka pitch video dengan fakta kuantitatif spesifik situasi di Indonesia (misal: 60 juta ton sampah, 97% lulusan IT gagal, 0.4% disabilitas).
* **Implikasi untuk AIC 2026:** Tarik masalah dari data nyata rantai nilai pasca-produksi primer Indonesia (misal: kerugian *food loss* 30-40% pada komoditas perikanan/pertanian akibat pembusukan dan rantai dingin yang buruk).
