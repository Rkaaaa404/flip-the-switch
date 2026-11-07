#### **RINGKASAN EKSEKUTIF** 

NusaQC adalah sistem inspeksi mutu dan pemilah otomatis berbasis Computer Vision yang dirancang untuk menggantikan proses Quality Control (QC) manual di lini sortasi Unit Pengolahan Ikan (UPI) ekspor Indonesia. 

**Visi Utama Produk (Production Vision):** NusaQC dirancang sebagai Sistem Pemilah Otomatis Kontinyu di Atas Conveyor Belt. Kamera industri memindai setiap ikan secara terus-menerus seiring conveyor bergerak, tanpa interupsi alur produksi. 

**Strategi MVP Babak Penyisihan COMPFEST 18:** NusaQC menggunakan _Synchronous Snapshot Inspection (Capture on Tiggier)_ , yaitu mengambil satu ikan saat melewati titik inspeksi berdasarkan pemicu sensor. Pendekatan ini disesuaikan dengan batasan MVP pada rulebook, sementara arsitektur modularnya dipersiapkan untuk dikembangkan menjadi _continuous inspection_ pada Babak Final. 

Setiap ikan diproses oleh dua model AI secara berurutan: **Model Kesegaran** mengklasifikasikan kondisi visual ikan ke dalam grade A/B/C berdasarkan indikator mata dan insang, sedangkan **Model Deteksi Defek** mengidentifikasi cacat dan kontaminasi visual seperti sisik sisa, perubahan warna abnormal, _foreign object_ , dan lendir berlebih menggunakan _bounding box_ . Hasil inspeksi diteruskan ke dashboard operator, _Stack Light_ & _Buzzer_ , kendali _conveyor_ , serta _SQLite Database_ untuk pencatatan hasil QC dan _digital traceability_ . 

**Nilai Bisnis (Business Value)** 

|**Dimensi**|**Kondisi Saat Ini**|**Dengan NusaQC**|**Delta**|
|---|---|---|---|
|Kecepatan<br>inspeksi per ikan|5–10 detik (manual)|≤ 1,5 detik (AI + trigger)|~5x lebih cepat|
|Konsistensi<br>penilaian|Subjektif, bergantung<br>kondisi fisik operator|Objektif, parameter tetap|Error rate turun<br>signifikan|
|Dokumentasi QC|_Paper-based_, sulit<br>diaudit|Log digital SQLite<br>dengan timestamp & lot<br>ID|Audit-ready|
|Harga sistem<br>(CAPEX)|QC visual manual: Rp 0<br>CAPEX, tapi biaya<br>tenaga tinggi|RPi 5 + kamera +<br>actuator: ≈ Rp 3–4 juta<br>per titik inspeksi|Terjangkau untuk UPI<br>menengah|
|Potensi<br>penghematan per<br>UPI|Risiko penolakan<br>ekspor: kerugian USD<br>5.000–50.000+ per<br>kontainer|Estimasi reduksi reject<br>rate ≥15%|ROI < 6 bulan|



### **Target Penerima Manfaat dan Potensi Pasar** 

NusaQC menargetkan **UPI skala menengah–besar yang berorientasi ekspor** , khususnya yang telah menerapkan HACCP dan memiliki lini sortasi berbasis conveyor. Fokus awal mencakup komoditas **Tuna/Cakalang, Tilapia, dan Salmon** . 

Berdasarkan data aktivitas ekspor menunjukkan **522 UPI aktif mengekspor ke Tiongkok pada 2024** . Dengan penyaringan berdasarkan skala usaha, orientasi ekspor, dan kesiapan lini 

produksi, NusaQC memperkirakan **400–600 UPI** sebagai _addressable market_ awal, dengan potensi **±400–1.800 titik inspeksi** berdasarkan asumsi 1–3 titik per UPI. 

**Catatan:** _angka 400–600 UPI merupakan_ **_estimasi pasar awal_** _, bukan jumlah resmi UPI yang telah tervalidasi memenuhi seluruh kriteria NusaQC._ 

#### **BAB 1 — PENDAHULUAN** 

#### **1.1 Latar Belakang** 

Indonesia memiliki sektor perikanan berorientasi ekspor dengan nilai perdagangan yang signifikan. Data 2022 menunjukkan nilai ekspor perikanan Januari–November 2022 mencapai USD 5,71 miliar (volume 1,11 juta ton), tumbuh 10,66% dari periode yang sama 2021 (Sumber: BPS/KKP, Januari 2023). Namun target 2022 sebesar USD 7,13 miliar tidak tercapai terdapat selisih USD 1,42 miliar yang gagal terealisasi. Komoditas utama adalah udang (28,1%), tuna-cakalang-tongkol (12,4%), dan cumi-sotong-gurita (10,1%), dengan negara tujuan utama Amerika Serikat (47,5%), Tiongkok, Jepang, ASEAN, dan Uni Eropa (Sumber: KKP, 2022). Industri sebesar ini sangat rentan terhadap satu masalah struktural yaitu kegagalan kontrol mutu di level Unit Pengolahan Ikan (UPI). 

Penelitian _peer-reviewed_ dari Jurnal Industria (Desember 2022), yang menganalisis data FDAOASIS dan RASFF periode 2010–2020, menemukan bahwa dalam periode yang diamati terdapat 2.318 kasus penolakan di Amerika Serikat dan 79 di Eropa. Berdasarkan analisis Pareto, faktor utama yang menyumbang lebih dari 80% penolakan di AS adalah _filthy_ (kontaminasi fisik) dan Salmonella (Nurkhasanah et al., 2022 Industria: Jurnal Teknologi dan Manajemen Agroindustri, Vol. 11, No. 2, hlm. 165–176). 

|Pasar Tujuan|Faktor Penolakan<br>Utama|Kebutuhan Validasi|Status Cakupan<br>NusaQC|
|---|---|---|---|
|Amerika Serikat|Filthy (Kontaminasi<br>Fisik)|Inspeksi Visual|Dalam Scope|
|(>80% Pareto)|Salmonella(Bakteri)|Uji Mikrobiologi|Di luar scope|
|Uni Eropa|Merkuri / Kadmium|Uji Laboratorium<br>(Logam Berat)|Di luar scope|
||Kontrol Temperatur<br>Buruk|Sensor Suhu IoT|Di luar scope MVP|
||Histamin / Salmonella|Uji Kimia / Klinis|Di luar scope|



NusaQC secara sengaja memfokuskan MVP pada faktor mutu yang dapat diidentifikasi secara visual, khususnya kontaminasi fisik ( _filthy_ ), sementara bahaya mikrobiologis, kimia, dan parameter temperatur tetap memerlukan metode pengujian khusus di luar cakupan sistem. 

FDA menerapkan _Detention Without Physical Examination (DWPE)_ terhadap udang dari beberapa produsen Indonesia terkait temuan _filthy_ dan Salmonella (FDA OASIS Import Alert 16-18; Southern Shrimp Alliance, 2023). Dalam konteks NusaQC, _filthy_ yang dapat diamati secara visual menjadi _domain Computer Vision_ , sedangkan Salmonella memerlukan pengujian mikrobiologis dan berada di luar cakupan sistem. Dengan demikian, NusaQC difokuskan pada kontaminasi fisik dan indikator mutu yang dapat diidentifikasi secara visual. 



<!-- Start of picture text -->
Manusia Mesin & Alat<br>* QC manual subjektif + Tanpa Deteksi<br>* Kelelahan operator Otomatis<br>* Kurang koordinasi * CahayaKonsistenTidak<br>Akibat<br>Produk Ikan<br>ditolak FDA<br>karena ‘Filthy’<br>* InspeksiTak Standar * Kondisi basahdan licin<br>* Pencatatan Kertas * Tekanan waktu<br>* Tanpa Mekanisme (Throughput)<br>Reject Otomatis<br>Metode Lingkungan<br><!-- End of picture text -->





(Gambar 1.2 Closed-Loop Control Architecture Nusa QC) 

**NusaQC** tidak berhenti pada fungsi inspeksi visual. Melalui _closed-loop control_ , hasil inferensi AI diteruskan menjadi keputusan yang memengaruhi operasi _conveyor_ , sehingga sistem mengintegrasikan persepsi, pengambilan keputusan, dan aktuasi dalam satu alur produksi. Pendekatan ini menempatkan **NusaQC** sebagai solusi _Smart Manufacturing_ , sesuai fokus tema pada penerapan AI dalam proses pengolahan dan operasi pabrik. 

**Mapping Komponen NusaQC ke Kriteria Smart Manufacturing** 

|**Komponen Smart**<br>**Manufacturing**|**Implementasi di NusaQC**|**Status**|
|---|---|---|
|Sensor otomatis|Proximity sensor + kamera industri|Ada|
|AI inference real-time|ONNX Runtime CPU, Snapshot per<br>Trigger (MVP)|Ada|
|Aktuasi otomatis|Relay -> motor conveyor STOP/SLOW|Ada|
|Human-Machine Interface|React.js Dashboard + Tower Light +<br>Buzzer|Ada|
|Data logging digital|SQLite (lot ID, timestamp, grade,<br>gambar)|Ada|
|Roadmap Continuous Mode|Fase 2: async inference queue di Final<br>Hackathon|Direncanakan|



#### **1.3 Tujuan dan Manfaat Pengembangan** 

Tabel 1.4 Peta Perjalanan Transformasi QC (Current State vs MVP vs Target State) 

|Aspek Operasional|Current State|NusaQC MVP -<br>Penyisihan|Production Vision -<br>Pabrik|
|---|---|---|---|
|Metode|Inspeksi visual|Snapshot per trigger|Continuous Automated<br>Conveyor Inspection.|
|Kecepatan|5-10 detik/ikan|<= 1.500 ms  per ikan|Mengikuti laju<br>conveyor.|



|Penilaian|Bergantung pada<br>operator|Parameter/model<br>terstandar|Otomatis dan<br>terintegrasi|
|---|---|---|---|
|Dokumentasi|Pencatatan manual|SQLite: lot ID,<br>timestamp, grade,<br>defect|Data terintegrasi untuk<br>analitik|
|Feedback|Reject dilakukan<br>operator|Relay →<br>STOP/SLOW +<br>indikator|Aktuasi otomatis<br>kontinu|
|Traceability|Terbatas|Digital dan dapat<br>diekspor|Terintegrasi skala<br>industri|
|Biaya (SDM vs<br>CAPEX)|Biaya SDM: 2-3<br>operator/lini X Rp 3,5-<br>4 jt/bulan = ~Rp 7-12<br>jt/lini/bulan.|±Rp3–4 juta/titik<br>inspeksi.|Disesuaikan skala<br>deployment|



Peta jalan menuju continuous automated inspection dirancang bertahap dalam tiga fase: 

Fase 1 — **MVP Penyisihan** : Snapshot per Trigger 

Fase 2 — **Final** : Continuous Capture + Async Inference 

Fase 3 — **Production** : Multi-camera & scalable deployment 

### **Tujuan Pengembangan** 

Berangkat dari permasalahan di atas, pengembangan NusaQC ditujukan untuk menjembatani empat kesenjangan utama (gap) dalam proses QC di UPI: 

#### **Gap 1: Subjektivitas → Standardisasi.** 

Mengubah inspeksi visual berbasis persepsi operator menjadi penilaian berbasis parameter dan model AI yang konsisten. 

#### **Gap 2: Human-in-the-Loop → Closed-Loop Automation.** 

Menghubungkan hasil inferensi AI dengan aktuator _conveyor_ melalui _relay_ sehingga keputusan _reject_ dapat diteruskan langsung ke proses produksi. 

#### **Gap 3: Paper-based → Digital Traceability.** 

Mencatat setiap hasil inspeksi berdasarkan _lot ID_ , waktu, _grade, defect, confidence_ , dan citra sehingga data QC terdokumentasi dan dapat ditelusuri. 

#### **Gap 4: Reaktif → Analitik Preventif** 

Mengubah data historis inspeksi menjadi informasi pola mutu antar-lot untuk mendukung evaluasi proses, pemasok, dan tindakan preventif. 

#### **Manfaat & Indikator Keberhasilan (KPI)** 

|**KPI**<br>**Baseline**<br>**Target MVP**<br>**Target Production**|
|---|



|Throughput inspeksi|40 ikan/menit atau<br>**2.400 ikan/jam**<br>pada sistem<br>computer vision<br>conveyor terdahulu|≥ 2.400 ikan/jam<br>(snapshot)|Mengikuti kecepatan<br>conveyor industri|
|---|---|---|---|
|False Negative Rate<br>(ikan cacat lolos)|**≤ 10%**sebagai<br>batas turunan dari<br>studi freshness<br>berbasis computer<br>vision dengan<br>akurasi prediksi<br>90%|≤ 8%|≤ 5%|
|Waktu per inspeksi|Inspeksi manual<br>memerlukan<br>proses<br>pemeriksaan<br>individual;<br>penelitian<br>automated fish<br>vision<br>menunjukkan<br>kelayakan inspeksi<br>pada conveyor|≤ 1,5 detik|Real-time (parallel<br>queue)|
|Lot terdokumentasi<br>digital|Manual / belum<br>terintegrasi|100%|100%|
|Recall per lot tersedia<br>dalam 5 menit|Tidak<br>memungkinkan|Ya (SQLite query)|Ya|
|Mode operasi|Manual|Snapshot per trigger|Continuous stream|



Dasar Penetapan KPI. Target NusaQC ditetapkan berdasarkan capaian penelitian _computer vision_ pada inspeksi kualitas ikan. Banwari et al. (2022) menunjukkan bahwa analisis citra mata ikan dapat mencapai 96,67% akurasi, sedangkan penelitian RT-GalaDet (2026) untuk deteksi abnormalitas permukaan ikan mencapai 89,7% recall dengan 51,98 FPS. Hasil tersebut menjadi acuan dalam menetapkan target MVP NusaQC sebesar recall ≥90% (FNR ≤10%) dan target produksi recall ≥95% (FNR ≤5%), dengan target throughput dan waktu inspeksi disesuaikan dengan kebutuhan sistem yang dirancang. 

#### **BAB 2 — METODOLOGI DAN PERANCANGAN SISTEM** 

#### **2.1 Kerangka Kerja Rekayasa & Solusi Optik** 

NusaQC dirancang dengan arsitektur **modular dan terintegrasi** , yang memisahkan proses akuisisi, _AI inference_ , pengambilan keputusan, aktuasi, dan antarmuka pengguna. Pendekatan ini 

memungkinkan setiap komponen diuji secara independen serta dikembangkan bertahap dari _MVP Snapshot Inspection_ menuju _Continuous Automated Conveyor Inspection._ 

#### **Tumpukan Teknologi (Tech Stack)** 

|**Komponen**|**Teknologi**|**Alasan Pemilihan**|
|---|---|---|
|Backend API|FastAPI (Python 3.11)|Async-capable, performant, mudah<br>di-deploy via Docker; siap di-<br>upgrade ke async mode di Final|
|Inference Engine|ONNX Runtime (CPU)|Platform-agnostic, tidak butuh GPU,<br>mendukung Raspberry Pi 5|
|Database|SQLite|Zero-config, lokal, audit-ready,<br>tidak perlu server DB|
|Frontend|React.js + Vite|Ringan, komponen WebSocket<br>native|
|Hardware GPIO|RPi.GPIO (Python)|Direct GPIO control untuk relay &<br>actuator|
|Container|Docker + docker-compose|Memudahkan reproduksi dan<br>deployment sistem|
|Mock Mode|Environment variable<br>ENABLE_MOCK_HARDWARE=true|Memungkinkan demonstrasi tanpa<br>perangkat fisik|



**Bill of Materials (BOM) Perangkat Keras** 

|**Komponen**|**Spesifikasi**|**Estimasi Harga**|**Fungsi**|
|---|---|---|---|
|Single<br>Board<br>Computer|Raspberry<br>Pi<br>5<br>(8GB<br>RAM)|≈ Rp 1.200.000|Inference + GPIO<br>control|
|Kamera Industri|USB Webcam ≥5MP +<br>lensa fixed|≈ Rp 300.000–<br>500.000|Capture frame per<br>trigger|
|LED Ring Light|5500K (Cool White), 15–<br>20 cm diameter|≈ Rp 150.000|Pencahayaan merata|
|Polarizing Filter|Linear<br>Polarizer<br>55mm/52mm|≈ Rp 80.000|Mengurangi<br>glare/refleksi<br>permukaan<br>ikan<br>basah|
|Proximity Sensor|IR Photoelectric Sensor<br>(NPN)|≈ Rp 50.000|Deteksi<br>ikan<br>melewati titik|



TANPA POLARIZER DENGAN POLARIZER LED Light LED Light L J Ikan Basah Ikan Basah t L GLARE [Polarizer] L J Kamera Kamera L L Citra terganggu Citra lebih jelas 





<!-- Start of picture text -->
>>><br>>> ><br><!-- End of picture text -->

(Gambar 2.3 Gambar 2.3. Alur Inferensi Dua Model AI NusaQC) 

#### **B. Dasar Pemilihan Model** 

MobileNetV3-Small dipilih karena memiliki arsitektur yang ringan dan sesuai untuk kebutuhan klasifikasi pada perangkat dengan sumber daya terbatas. Pada penelitian klasifikasi kesegaran ikan berdasarkan citra mata, MobileNetV3-Small telah digunakan dan menghasilkan F1-score sebesar 68% pada 24 kelas kesegaran dan jenis ikan (Rakhmat & Haekal, 2023). 

YOLOv8n dipilih karena memberikan kompromi antara kemampuan deteksi dan waktu inferensi pada perangkat edge. Pada pengujian _industrial visual inspection_ menggunakan Raspberry Pi 500, YOLOv8n mencapai mAP@0.5 sebesar 0,938, F1-score 0,914, dan waktu inferensi sekitar 470 ms, sedangkan YOLOv8s membutuhkan sekitar 1.315 ms (Okano et al., 2025). 

Kedua model ditargetkan untuk diekspor ke ONNX agar dapat digunakan pada lingkungan CPU tanpa ketergantungan terhadap GPU. Dengan demikian, F1 ≥85% dan latency 150–300 ms pada MobileNetV3-Small merupakan target pengembangan NusaQC, sedangkan mAP50 ≥0,70 dan latency ±470 ms pada YOLOv8n digunakan sebagai target engineering yang mengacu pada benchmark perangkat edge. 

|Model|Target|Latency|
|---|---|---|
|MobileNetV3-Small|F1 ≥ 85%|±150–300 ms|
|YOLOv8n|mAP50 ≥ 0,70|±470 ms|



#### **C. Grading dan Decision Logic** 

|**Grade**|**Kondisi Mata**|**Kondisi Insang**|**Kondisi Kulit**|
|---|---|---|---|
|A|Jernih, cembung, kornea<br>transparan|Merah cerah/merah tua, bersih|Bersih, berkilap, lendir<br>transparan|
|B|Sedikit cekung, kornea mulai<br>keruh|Merah pudar/merah jambu|Lendir mulai keruh, sedikit<br>bau|
|C|Sangat cekung, mata<br>keruh/kering|Coklat/abu-abu, berbau|Lendir keruh/hijau, bau<br>menyengat|



#### **D. Training & Evaluation Pipeline** 

### **Training Pipeline** 

TRAINING PIPELINE =================== STEP 1: Data Collection +-- Primary: Ambil foto ikan di UPI lokal (dengan izin) |   +-- Scombridae: Tuna, Cakalang (dominan ekspor) 

|   +-- Cichlidae: Tilapia/Nila |   +-- Salmonidae: Salmon +-- Augmentation: Albumentations (flip, rotate, color jitter, blur) STEP 2: Annotation +-- Model 1: Label kelas (A/B/C) per gambar -> CSV format +-- Model 2: Bounding box annotation via Roboflow/CVAT 





<!-- Start of picture text -->
PHYSICAL LAYER PROCESSING / APPLICATION LAYER OUTPUT / CONTROL LAYER<br>- input image / |»! Pre-processing+  |» Norrallaion Tower Light @<br>pe > ms | —— | Fah! bo Buzzer @<br>Conveyor Single Frame | —[ image Resize ) | Localization Motor Control<br> Belt — 4 ConveyorPASS<br>| MobileNetV3-Smal _) (Freshnss Classification ) — Green LightRi<br>|\ pcavis, ) ‘Head / Eye-Gillx  RO! Grade A/B/Ct FAIL +YellowRed Light Light+ Buzzer<br>! J Grade A/B/C Confidence Score Bsc hi<br>Camera >5MP —— ——) vsenmeice<br>os | |(_YoLoven> Crarimaliols1 ‘SurfaceFull Defect Fish FrameDetection Inspection. Result<br>TRIGER ||| Defeect| Lanbe "a BoundingDefectLabel}: Box ) |, BoundingcadeBox VisualizationMBE<br>i |—| ,lCorfidence Score ConfidenceConfidence ScoreScore io<br>cape sae (DECISION’ ENGINE =| DATA LOGGING<br>|<br>yeLED Ring Light Grade, A + No©:Defect + PASS ‘Seprect.jonieacerden‘SQhitteDefectGrade DatabaseResuitsfacadeDatabase<br>Linear Polarizing Grade B + No Defect -» CONDITIONAL Confidence<br>Fatter u Detect Rests,<br>Grade C OR Defect Detected + FAIL Tonfence<br>Closed-Loop Qualty Inspection 0RETTerese<br><!-- End of picture text -->



<!-- Start of picture text -->
HASIL INSPEKSI Al<br>KEPUTUSAN<br>tutusGradeA=TidakSTAMeu= convevon crass)Hyau NORMALAda Defek «GradeKONDISIONALStxsaeuSI PEMERIKSAAN Bs Tidak Adakunine TAMBAHANDefek Kritis GradeGAGaLa>mevameartamuCONVEYOR©(ran)AYAU nienant DefekBERHENTI/> BUZZERTerdetekst<br>DATABASE sqLite<br>KEPUTUSAN 2=2 DorenWaktuVaaatl InapakalInspekst<br>2 Wo toes Trecesbltty<br>DETEKS! —* KLASIFIKASI —* KEPUTUSAN —* AKTUATOR ~—* PENCATATAN<br><!-- End of picture text -->

kapasitas tinggi. Perbandingan ini digunakan untuk melihat fungsi, kapasitas, pendekatan teknologi, serta kebutuhan investasi sebelum menentukan posisi komersial NusaQC. 

|Penelitian/Solusi|Kontribusi|Keterbatasan|
|---|---|---|
|Computer Vision untuk<br>Freshness Estimation<br>Prasetyo et al.(2022)|Estimasi<br>kesegaran<br>ikan<br>berdasarkan citra mata dengan<br>akurasi 96,67%.|Berfokus<br>pada<br>estimasi<br>kesegaran<br>dan<br>belum<br>mengintegrasikan deteksi defek<br>serta kendali conveyor.|
|MobileNetV3-Small untuk<br>Klasifikasi Kesegaran —<br>Rakhmat et al.|Klasifikasi kesegaran ikan<br>menggunakan MobileNetV3-<br>Small dengan F1-score 68%<br>pada 24 kelas.|Belum diarahkan pada sistem<br>inspeksi terintegrasi di lini<br>produksi.|
|YOLO-based Fish Surface<br>Detection — Yin et al. (2025)|Deteksi abnormalitas<br>permukaan ikan dengan<br>mAP@0.5 hingga 93% dan<br>kecepatan50,2 FPS.|Belum mengintegrasikan<br>grading kesegaran dan_closed-_<br>_loop control_.|
|BAADER 1870 Whole Fish<br>Grader|Sistem grading otomatis<br>dengan kapasitas hingga 160<br>ikan/menit dan_single-fish_<br>_tracking_.|Berorientasi pada grading<br>industri dan membutuhkan<br>perangkat khusus; harga tidak<br>dipublikasikan.|
|Commercial Fish Grader<br>Market|Beberapa_fish grader_komersial<br>ditawarkan sekitar US$6.000–<br>7.000 hingga US$8.800–<br>12.000/unit.|Umumnya berfokus pada<br>_weight/size grading_, bukan<br>freshness dan defect detection<br>berbasisAI.|
|NusaQC|Mengintegrasikan freshness<br>classification, defect detection,<br>decision engine, closed-loop<br>actuator, dan digital<br>traceability dalam satu sistem<br>edge-AI.|MVP masih menggunakan<br>_synchronous snapshot_<br>_inspection_dan memerlukan<br>validasi pada operasi kontinu.|



Benchmark tersebut menunjukkan bahwa solusi komersial yang tersedia umumnya membutuhkan investasi perangkat di awal dan berfokus pada fungsi _grading_ tertentu. Sebaliknya, NusaQC menggunakan pendekatan _hardware-enabled SaaS_ untuk menyediakan fungsi inspeksi AI secara modular dengan biaya operasional bulanan. Dengan demikian, struktur harga NusaQC ditujukan untuk menurunkan kebutuhan CAPEX awal UPI, sekaligus mempertahankan akses terhadap perangkat keras, perangkat lunak, dan pembaruan model selama masa berlangganan. 

**Skema Komersial NusaQC** 

|Layanan|Harga|Target|
|---|---|---|
|Tier 1 – Starter|Rp1.500.000/bulan/unit|UPI skala menengah, 1–2 titik<br>inspeksi|
|Tier 2 – Business|Rp3.500.000/bulan/UPI|UPI skala besar, hingga 5 titik<br>inspeksi|



Dengan begitu, harga NusaQC tidak perlu dibandingkan langsung secara nominal dengan BAADER, karena produk dan scope-nya berbeda. Yang dibandingkan adalah kelas solusi dan kebutuhan investasi awal. Itu jauh lebih aman secara akademik. 

#### **Struktur Ekonomi Unit (** **_Unit Economics_ ) & Potensi Pasar** 

Secara finansial, arsitektur sistem NusaQC yang efisien menghasilkan profil marjin yang menarik. Estimasi biaya manufaktur perangkat keras ( _CAPEX hardware_ ) sebesar Rp3.000.000/unit, dengan _monthly OPEX_ sekitar Rp200.000/unit. Dengan pendapatan Tier 1 sebesar Rp1.500.000/bulan, model bisnis NusaQC diarahkan untuk mengubah investasi perangkat menjadi biaya operasional yang lebih terukur bagi UPI. 

Potensi pasar NusaQC dihitung berdasarkan jumlah UPI yang tersedia dan bukan menggunakan estimasi jumlah UPI ekspor yang tidak terverifikasi. KKP mencatat 3.365 UPI bersertifikat SKP pada 2024, dengan 1.816 UPI berada pada skala menengah-besar, yang menjadi kelompok pasar paling relevan untuk solusi otomasi inspeksi. 

|Indikator|Dasar Data|Perhitungan|Nilai|
|---|---|---|---|
|Potential Market Base|UPI menengah-besar<br>bersertifikat SKP|1.816 UPI|1.816 UPI|
|Asumsi titik inspeksi|Asumsi bisnis<br>NusaQC|3 titik/UPI|5.448 titik|
|TAM Monthly|5.448 × Rp1,5 juta|—|Rp8,172 Miliar/bulan|
|Target penetrasi awal|Asumsi konservatif<br>5%|1.816 × 5% ≈ 91 UPI|±91 UPI|
|SAM Monthly|91 × Rp4,5 juta|—|±Rp409,5 Juta/bulan|



Basis pasar NusaQC menggunakan data KKP, yang mencatat 1.816 UPI skala menengah-besar bersertifikat SKP pada 2024 dari total 3.365 UPI bersertifikat. Dengan asumsi bisnis NusaQC sebesar tiga titik inspeksi per UPI dan tarif Tier 1 Rp1,5 juta per titik per bulan, diperoleh _potential market_ sekitar Rp8,17 miliar/bulan. Target penetrasi awal sebesar 5% menghasilkan sekitar 91 UPI atau potensi pendapatan sekitar Rp409,5 juta/bulan. Asumsi jumlah titik inspeksi dan penetrasi digunakan sebagai skenario konservatif untuk perencanaan bisnis, sedangkan jumlah UPI sebagai basis pasar mengacu pada data resmi KKP. 

#### **Simulasi Kalkulator ROI & Valuasi Dampak Finansial Klien** 

Simulasi ROI NusaQC menggunakan pendekatan _scenario-based_ , dengan memisahkan data eksternal dan asumsi bisnis. Relevansi pasar tuna untuk ekspor AS didukung oleh data KKP: pada 2024, nilai ekspor tuna-cakalang-tongkol Indonesia mencapai USD1,03 miliar, sementara AS menjadi salah satu pasar utama dengan nilai ekspor TCT sebesar USD254,82 juta menurut data UN Comtrade yang dihimpun KKP. 

|Komponen|Nilai|Dasar Penetapan|
|---|---|---|
|Nilai ekspor TCT Indonesia<br>2024|USD 1,03 Miliar|Data KKP 2024|
|Ekspor TCT Indonesia → AS|USD 254,82 Juta|UN Comtrade via KKP|
|Biaya NusaQC Tier 1|Rp1.500.000/bulan|Harga layanan NusaQC|
|CAPEX Hardware|Rp3.000.000|Estimasi BOM NusaQC|
|Biaya yang dapat dihindari|Asumsi skenario|Harus divalidasi melalui<br>wawancara UPI|



|Pengurangan kerugian|Skenario 10–50%|Sensitivity analysis, bukan<br>klaimempiris|
|---|---|---|
|Net Benefit|Bergantungskenario|Penghematan|



|Skenario|Biaya/Kerugian<br>yang Dapat<br>Dioptimalkan|Efisiensi<br>NusaQC|Benefit/Bulan|Subscription|Net Benefit|
|---|---|---|---|---|---|
|Konservatif|Rp130 jt|10%|Rp13 jt|Rp1,5 jt|Rp11,5 jt|
|Moderat|Rp130 jt|25%|Rp32,5 jt|Rp1,5 jt|Rp31 jt|
|Optimistis|Rp130 jt|50%|Rp65 jt|Rp1,5 jt|Rp63,5 jt|



Nilai manfaat NusaQC tidak diasumsikan langsung sebesar 50%, tetapi diuji melalui beberapa skenario efisiensi. Pendekatan ini digunakan karena studi pengendalian mutu tuna di Indonesia menunjukkan bahwa proses produksi melibatkan pemeriksaan kualitas dari bahan baku hingga produk akhir dan masih terdapat karakteristik _critical-to-quality_ yang perlu dikendalikan. Besaran penghematan aktual selanjutnya perlu divalidasi melalui data operasional UPI, sehingga angka ROI pada tahap proposal diposisikan sebagai simulasi sensitivitas, bukan klaim penghematan yang telah terbukti. 

#### **3.2 Tata Kelola AI & Manajemen Risiko** 

#### **AI Governance & Etika** 

Pengimplementasian kecerdasan buatan pada rantai pasok industri perikanan menuntut keandalan, transparansi, serta perlindungan data yang ketat. NusaQC mengadopsi prinsip _Responsible AI_ untuk memastikan bahwa model yang dikembangkan bertindak sebagai alat bantu keputusan ( _decisionsupport system_ ) yang etis, aman, dan dapat dipertanggungjawabkan tanpa menggantikan peran mutlak pengawasan manusia. 

Tabel berikut merangkum dimensi tata kelola AI, potensi risiko etis-teknis yang diidentifikasi, serta strategi mitigasi yang diterapkan 

|**Dimensi**|**Risiko**|**Mitigasi**|
|---|---|---|
|Bias Dataset|Model dilatih mayoritas dari 3<br>familia ikan; ikan jenis lain bisa<br>false negative|Dokumentasikan scope dengan jelas;<br>label "Unsupported Species" jika ikan<br>tidak dikenal|
|False Negative<br>Risk|Ikan cacat lolos karena confidence<br>di bawah threshold|Threshold dapat dikonfigurasi per<br>UPI; default konservatif (lebih<br>sensitif)|
|Data Privacy|Foto ikan yang diambil di UPI<br>bisa berisi informasi produksi<br>sensitif|Foto tidak dikirim ke cloud; disimpan<br>lokal di SQLite + dapat dihapus per lot|
|Operator Over-<br>trust|Operator terlalu bergantung pada<br>AI, mengabaikan judgment<br>manual|UI selalu menampilkan peringatan "AI<br>is an assistant, not a replacement for<br>human QC"|



|Model<br>Transparency|Juri / UPI tidak memahami dasar<br>keputusan AI|Confidence score + bounding box<br>selalu ditampilkan; tidak ada black-<br>box decision|
|---|---|---|



#### **Risk Register & Mitigasi** 

Untuk menjamin keberhasilan eksekusi proyek—baik pada tahap penilaian proposal, demonstrasi sistem, hingga penerapan di lapangan—dilakukan pemetaan risiko ( _Risk Register_ ) secara komprehensif. Matriks ini mencakup evaluasi probabilitas, dampak, serta rencana kontingensi teknis dan teknologis yang terukur: 

|**No**|**Risiko**|**Prob.**|**Dampak**|**Mitigasi**|
|---|---|---|---|---|
|R01|Hardware inference<br>terlalu lambat di RPi5|Sedang|Tinggi|Benchmark awal di hardware<br>target; fallback ke laptop CPU<br>untuk demo|
|R02|Variasi pencahayaan<br>& kilau air pada kulit<br>ikan basah|Sedang|Tinggi|Pemasangan Linear Polarizing<br>Filter pada kamera optis +<br>augmentasi Albumentations<br>(glare injection)|
|R03|Variasi spesies<br>regional di luar dataset<br>publik|Sedang|Sedang|Arsitektur AI modular dengan<br>transfer learning cepat (DaFiF +<br>FFE) untuk fine-tuning spesies<br>baru|
|R04|Polarizing filter tidak<br>efektif di kondisi<br>tertentu|Rendah|Sedang|Tes dengan sampel ikan basah;<br>backup: preprocessing contrast<br>enhancement di software|
|R05|Mock Mode tidak<br>merepresentasikan<br>hardware asli|Rendah|Rendah|Mock Mode log didesain verbose<br>dan representatif; juri memahami<br>ini adalah simulasi|
|R06|Blind judging<br>violation (logo<br>universitas)|Rendah|Sangat<br>Tinggi|Checklist sebelum submit: scan<br>semua file untuk mention nama<br>kampus|
|R07|Deadline terlewat|Rendah|Fatal|Set alarm 3 hari sebelum deadline<br>(22 Agustus) untuk final review|
|R08|Framing MVP<br>disalahpahami sebagai<br>kelemahan produk|Rendah|Sedang|Narasi eksplisit di proposal &<br>video bahwa Snapshot adalah<br>trade-off rulebook, bukan batas<br>visi|



#### **BAB 4 — KESIMPULAN** 

NusaQC menjawab masalah struktural yang nyata dan berbasis data: kegagalan kontrol mutu manual di lini sortasi Unit Pengolahan Ikan (UPI) ekspor Indonesia, yang berkontribusi terhadap kasus penolakan ekspor akibat kontaminasi fisik (filthy) di pasar Amerika Serikat dan Eropa. Solusi yang diajukan secara ketat membatasi klaimnya pada domain yang valid secara ilmiah — deteksi visual berbasis Computer Vision dan secara eksplisit tidak mengklaim kemampuan mendeteksi kontaminasi mikrobiologis seperti Salmonella. 

Dari sisi teknis, NusaQC dirancang dengan dua model AI yang saling melengkapi (MobileNetV3-Small untuk klasifikasi kesegaran, YOLOv8n untuk deteksi defek permukaan), didukung oleh konsolidasi enam dataset akademis dan data lapangan, serta setiap keputusan arsitektur didokumentasikan melalui Engineering Decision Record yang eksplisit. Arsitektur closed-loop — dari inferensi AI hingga aktuasi fisik pada motor conveyor — memastikan sistem ini benar-benar memenuhi definisi Smart Manufacturing, bukan sekadar Smart Inspection. 

Untuk Babak Penyisihan COMPFEST 18, tim secara sadar memilih skema Synchronous Snapshot Inspection sebagai strategi kepatuhan rulebook, bukan sebagai batas kemampuan produk. Seluruh komponen sistem — dari pemilihan FastAPI yang async-ready hingga struktur folder modular — dirancang agar transisi menuju Continuous Automated Conveyor Inspection pada Babak Final Hackathon dapat dilakukan tanpa perombakan arsitektur total. 

Dari sisi bisnis, model B2B SaaS dengan skema berlangganan per titik inspeksi menunjukkan potensi payback period yang sangat cepat bagi UPI, dengan estimasi penghematan potensial jauh melampaui biaya operasional bulanan sistem. Tata kelola AI dan manajemen risiko turut disusun secara eksplisit mencakup mitigasi bias dataset, transparansi model, privasi data, dan pencegahan ketergantungan berlebihan operator terhadap output AI. 

# **LAMPIRAN** 

## **Lampiran A — Matriks Kepatuhan Rulebook COMPFEST 18 (MVP Compliance Matrix)** 

### **A.1 Ketentuan Produk** 

|**No**|**Ketentuan Rulebook**|**Status**|**Implementasi**|
|---|---|---|---|
|1|Proyek merupakan inovasi di bidang<br>AI for Backbone Economy|Terpenuhi|Smart Manufacturing: CV-based QC<br>di lini produksi UPI|
|2|Proyek merupakan karya orisinal tim|Terpenuhi|Tidak menggunakan project lama;<br>dibuat periode 17 Juni–25 Agustus<br>2026|
|3|Proyek hanya dikerjakan selama<br>perlombaan berlangsung|Terpenuhi|Repository dibuat fresh, commit<br>history dari mulai lomba|



|4|Proyek penyisihan wajib dilanjutkan<br>ke Final|Terpenuhi|Arsitektur modular dirancang<br>eksplisit untuk iterasi di hackathon<br>final — upgrade snapshot →<br>continuous mode|
|---|---|---|---|



### **A.2 Batasan MVP (Scope Compliance)** 

|**Batasan**|**Ketentuan**|**Status**|
|---|---|---|
|Frontend|UI wajib hanya berfokus pada alur interaksi inti|Terpenuhi — Hanya: upload foto →<br>tampil hasil. Tidak ada advanced<br>dashboard|
|Frontend|Tidak perlu dashboard analitik tingkat lanjut|Terpenuhi — Tidak ada time-series<br>analytics di MVP|
|Frontend|Tidak perlu sistem otentikasi kompleks|Terpenuhi — Tidak ada multi-role auth|
|Backend|Arsitektur wajib hanya sampai pemrosesan<br>sinkron|Terpenuhi — FastAPI sync endpoint,<br>Snapshot per Trigger|
|Backend|Tidak perlu background jobs / auto data logging|Terpenuhi — Logging hanya saat<br>request masuk (per trigger)|
|Backend|Tidak perlu infrastruktur database terdistribusi|Terpenuhi — SQLite lokal murni|
|Backend|Fokus agar API/sistem lokal dapat dijalankan<br>via docker-compose|Terpenuhi — docker-compose up<br>langsung running|
|AI Model|Implementasi AI wajib hanya berfokus pada<br>core inference|Terpenuhi — ONNX inference dengan<br>frozen weights|
|AI Model|Tidak perlu sistem auto-tuning|Terpenuhi — Tidak ada online learning|
|AI Model|Tidak perlu bulk testing scripts|Terpenuhi — Test dilakukan manual<br>via UI|
|AI Model|Tidak perlu mekanisme loop umpan balik<br>otomatis ke model|Terpenuhi — Feedback loop ke<br>hardware (relay/aktuator), bukan ke<br>model|



### **A.3 Ketentuan Deliverables** 

|**Deliverable**|**Ketentuan**|**Status**|**Detail**|
|---|---|---|---|
|GitHub Repo|Public, setup guide di<br>README.md, docker-compose|Terpenuhi|README menjelaskan:<br>prerequisites → clone →<br>docker-compose up → akses<br>localhost|
|GitHub Repo|Conventional commits<br>(feat/fix/refactor)|Terpenuhi|Git hook pre-commit<br>menggunakan commitlint|
|GitHub Repo|Batas commit: 25 Agustus 2026<br>23:55 WIB|Perlu perhatian|Wajib diingat tim, set alarm|



|Video PoW|Maks 7 menit, YouTube<br>UNLISTED|Terpenuhi|Durasi rencana: 5 menit|
|---|---|---|---|
|Video PoW|Format: COMPFEST 18 AIC:<br>PROOF OF WORK - [Tim] -<br>NusaQC|Terpenuhi|Template nama sudah disiapkan|
|Video PoW|Double screen (terminal +<br>aplikasi), tanpa cut|Terpenuhi|OBS Studio: split screen<br>recording|
|Video PoW|Semua fitur di video promosi<br>harus ada di PoW|Terpenuhi|Feature parity check sebelum<br>upload|
|Video Promosi|Maks 5 menit, YouTube PUBLIC,<br>MP4 ≥720p|Terpenuhi|Durasi rencana: 4 menit|
|Video Promosi|Format: COMPFEST 18 AIC:<br>[Tim] - NusaQC|Terpenuhi|—|
|Proposal PDF|Maks 20 halaman (exclude cover,<br>pustaka, lampiran)|Perlu<br>penyesuaian<br>akhir|Dokumen ini disusun lengkap<br>sesuai arahan; kompresi ke<br>batas halaman dilakukan pada<br>tahap finalisasi PDF|
|Proposal PDF|Mencakup: Latar Belakang,<br>Tujuan, Metodologi, Kesimpulan|Terpenuhi|Semua bagian ada|
|Blind Judging|Tidak boleh ada nama/logo<br>universitas|Terpenuhi|Semua asset diperiksa sebelum<br>submit|



### **A.4 Proyeksi Skor Berdasarkan Kriteria Resmi (referensi lengkap)** 

Rincian proyeksi skor per kriteria resmi disajikan secara utuh pada Bab 4 (Kesimpulan). Estimasi total skor berada pada kisaran 80–88%, dengan variabel utama berupa kualitas eksekusi video dan performa model saat validasi. 

## **Lampiran B — Deliverables Checklist Submisi** 

Final check sebelum tenggat 25 Agustus 2026 pukul 23:55 WIB: 

#### **GitHub Repository** 

- Repository public, URL dapat diakses 

- README.md berisi: prerequisites → clone → docker-compose up → akses browser 

- Tidak ada nama/logo universitas di seluruh kode, komentar, atau docs 

- Commit history menggunakan Conventional Commits (feat/fix/refactor) 

- .env.example ada dan terdokumentasi 

- Model ONNX dapat didownload (via README link atau include di repo) 

- docker-compose up berhasil dijalankan di mesin clean (validasi sendiri) 

#### **Video Proof of Work (YouTube UNLISTED)** 

- Durasi ≤ 7 menit 

- Format nama: COMPFEST 18 AIC: PROOF OF WORK - [Nama Tim] - NusaQC 

- Menampilkan double screen: terminal + aplikasi 

- Timestamp visible di terminal 

- Tidak ada cut atau edit memotong — hanya fast-forward bagian loading 

- Semua fitur di video ini ada juga di video promosi 

- Jujur tentang fitur yang belum beres (dengan penjelasan) 

#### **Video Promosi (YouTube PUBLIC)** 

- Durasi ≤ 5 menit, resolusi ≥720p, format MP4 

- Format nama: COMPFEST 18 AIC: [Nama Tim] - NusaQC 

- Menjelaskan: problem → solution → impact (dengan angka konkret) 

- Menunjukkan alur inspeksi ikan di dashboard 

- Tidak ada nama/logo universitas 

- Narasi jelas membedakan visi produk (continuous) vs scope MVP penyisihan (snapshot) 

#### **Proposal PDF** 

- Maksimal 20 halaman (tidak termasuk cover, daftar pustaka, lampiran) 

- Berisi: Nama Kelompok, Latar Belakang, Tujuan, Metodologi, Kesimpulan 

- Metodologi mencakup: alur dataset, alur training, alur integrasi model ke kode 

- Setiap keputusan teknis ada Engineering Decision Record-nya 

- Tidak ada klaim ilmiah yang salah (khususnya: tidak ada klaim deteksi Salmonella) 

- Tidak ada nama/logo universitas 

- Framing MVP vs Production Vision dijelaskan dengan jelas 

