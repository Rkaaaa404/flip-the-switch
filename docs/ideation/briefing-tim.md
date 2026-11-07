# Briefing Tim: Hackathon "Flip the Switch"

> Dokumen pengantar untuk teman satu tim. Tujuannya: setelah membaca ini, kamu paham kompetisinya, paham apa itu Switch, paham lima kandidat ide yang sedang kita bandingkan, dan bisa ikut memutuskan.

| | |
|---|---|
| **Ditulis** | 6 November 2026 |
| **Status ide** | **Belum ada ide yang dipilih.** Kita masih membandingkan lima kandidat. |
| **Deadline submit** | **7 November 2026, 23:59 IST** = **8 November 2026, 01:29 WIB** (18:29 UTC) |
| **Versi Switch yang kita pakai** | Switch Console **0.40.1** (di dalamnya switch-core 0.31.0) |
| **Sumber detail** | `competition-ideation.md` (aturan lomba), `recall-room.md`, `buzzerdefuse-room.md`, `accessfix-room.md`, `brandecho-room.md`, `deadline-rescue.md` (spesifikasi tiap ide), `idea-ranking.md` (peringkat lengkap) |

---

## Daftar isi

1. [Ringkasan 1 menit](#1-ringkasan-1-menit)
2. [Kompetisinya tentang apa](#2-kompetisinya-tentang-apa)
3. [Waktu, aturan, dan track](#3-waktu-aturan-dan-track)
4. [Cara penjurian dan cara membacanya](#4-cara-penjurian-dan-cara-membacanya)
5. [Mengenal Switch](#5-mengenal-switch)
6. [Fakta teknis Switch 0.40.1 yang mengubah desain](#6-fakta-teknis-switch-0401-yang-mengubah-desain)
7. [Tiga prinsip desain yang kita pegang](#7-tiga-prinsip-desain-yang-kita-pegang)
8. [Lima kandidat ide](#8-lima-kandidat-ide)
9. [Perbandingan dan skor](#9-perbandingan-dan-skor)
10. [Risiko dan hal yang belum pasti](#10-risiko-dan-hal-yang-belum-pasti)
11. [Yang perlu kita putuskan bersama](#11-yang-perlu-kita-putuskan-bersama)
12. [Glosarium](#12-glosarium)

---

## 1. Ringkasan 1 menit

- **Lombanya:** bikin *workflow* di mana **manusia dan AI agent menyelesaikan pekerjaan nyata bersama di dalam chat tim**, dengan **Switch** sebagai penghubungnya. Switch wajib dan harus jadi pusat, bukan tempelan.
- **Penjurian:** Use of Switch **30%**, Technical execution **25%**, Creativity & impact **25%**, Presentation **20%**.
- **Kandidat ide (urut peringkat):**
  1. **Recall Room (NusaQC):** keluhan kualitas ikan → telusuri asal-usul lot → tahan stok dan blokir pengiriman yang terdampak, setelah disetujui orang yang berwenang.
  2. **BuzzerDefuse Room:** serangan hoaks terkoordinasi (*buzzer*) ke sebuah merek → agent memisahkan aktivitas terkoordinasi dari keluhan pelanggan asli dan menyusun pernyataan → PR dan Legal sama-sama menyetujui revisi yang sama → pernyataan baru terbit.
  3. **AccessFix Room:** laporan hambatan aksesibilitas → agent mereproduksi dan memperbaiki kode → agent lain me-review → manusia menerima hasilnya.
  4. **BrandEcho Room:** konsep iklan dan banner dicek terhadap aturan merek → agent mengadaptasi per kanal → Brand Director mensertifikasi revisi yang tepat → hanya aset tersertifikasi yang masuk antrean publikasi.
  5. **Deadline Rescue Room (Compe-In):** deadline berubah → agent menyusun ulang jadwal tim → ketua tim menyetujui → jadwal di aplikasi benar-benar berubah.
- **Skor (bobot resmi, tanpa faktor waktu):** Recall **8,85**, BuzzerDefuse **8,05**, AccessFix **8,00**, BrandEcho **7,70**, Deadline Rescue **6,70**.
- **Jika sisa waktu ikut dihitung,** tiga teratas hampir seri (Recall 8,10, BuzzerDefuse 8,05, AccessFix 8,00). **Rekomendasi:** BuzzerDefuse, karena paling seimbang antara skor dan beban pengerjaan. Ini rekomendasi, bukan keputusan.
- **Temuan teknis terpenting:** agent berbasis LLM di Switch **tidak bisa memastikan siapa pengirim pesan**. Jadi persetujuan ("approve") tidak boleh diputuskan oleh LLM. Persetujuan harus dicek oleh kode yang deterministik.

---

## 2. Kompetisinya tentang apa

Kalimat tantangan resminya:

> *Build a workflow where an AI agent and the people in a team chat get a real task done together.*

Artinya, syarat minimal:

- Ada **minimal satu manusia dan satu AI agent**, terhubung lewat **Switch**.
- **Switch harus sentral.** Juri secara eksplisit bertanya: *"Apakah proyek ini berhenti berfungsi kalau Switch dicabut?"* Kalau jawabannya "tidak, cuma kehilangan notifikasi", nilainya jelek.
- **Hasilnya harus nyata:** sesuatu di-*ship*, diperbaiki, di-*review*, atau tugas lain benar-benar selesai. Jawaban AI di chat saja **tidak cukup**.

Yang **boleh**:

- Memakai agent, library, dan template yang sudah ada. Kita tidak wajib membuat agent baru.
- Memakai aplikasi yang sudah kita punya sebelumnya (misalnya NusaQC atau Compe-In) sebagai sistem dasar.
- Memakai AI coding tools, asalkan kita paham dan bisa menjelaskan submisi kita.

Yang **wajib dibangun selama hackathon**:

- **Setup Switch-nya** (room, agent, konfigurasi).
- **Workflow yang dijalankan agent-agent tersebut.**

Jadi kalau kita pakai NusaQC, kita harus jujur memisahkan mana yang sudah ada sebelum lomba dan mana yang baru. Rencananya: tandai kondisi awal dengan git tag `baseline-nusaqc`, lalu jelaskan pemisahannya di README.

---

## 3. Waktu, aturan, dan track

### Waktu

| Item | Waktu |
|---|---|
| Event berjalan | 4 Nov 2026 00:01 IST s/d 7 Nov 2026 23:59 IST |
| Deadline submit | **8 Nov 2026 01:29 WIB** |
| Peserta | Online, gratis, solo atau tim maksimal 4 orang |
| Biaya | Switch open source dan gratis di-*self-host*; kita bawa langganan atau API key sendiri untuk agent-nya (misalnya Claude Code) |

### Track

| Track | Isi | Hadiah |
|---|---|---|
| **Best Business Workflow** | Workflow praktis untuk tim kerja | $2.000 |
| Best Personal or Creative Workflow | Workflow untuk keperluan pribadi atau kreatif | $2.000 |
| Best Core Contribution | Pull request ke repo Switch sendiri | $100 per PR terbaik |
| Code with Wispr (side track) | Membangun dengan suara pakai Wispr Flow | $500 |
| Best Blog (side track) | Tulisan tentang cara membangun dengan Switch | AirPods |

Kelima kandidat ide kita masuk **Best Business Workflow** (BrandEcho juga bisa masuk Creative Workflow). Boleh ikut beberapa track sekaligus, jadi **Blog** bisa jadi tambahan murah karena kita toh harus menulis README.

---

## 4. Cara penjurian dan cara membacanya

### Bobot resmi

| Kriteria | Bobot | Pertanyaan juri |
|---|---|---|
| **Use of Switch** | **30%** | Apakah Switch sentral? Apakah proyek mati tanpa Switch? |
| **Technical execution** | **25%** | Apakah jalan? Bisakah orang lain *clone* repo lalu menjalankannya? |
| **Creativity & impact** | **25%** | Ide segar yang menyelesaikan masalah nyata sebuah tim? |
| **Presentation** | **20%** | Apakah video demo dan README menjelaskan cara Switch dipakai? |

### Cara membacanya

- **Satu poin di "Use of Switch" bernilai 1,2× poin technical atau creativity, dan 1,5× poin presentation.** Jadi ide yang membuat Switch benar-benar tak tergantikan punya keuntungan struktural.
- **Technical execution menuntut reproducibility.** Juri harus bisa *clone* dan menjalankan. Ketergantungan pada akun cloud pribadi, OAuth, atau data rahasia mengurangi nilai.
- **Presentation hanya 20%,** tetapi video dan README adalah satu-satunya cara juri *melihat* tiga kriteria lainnya. Jadi tetap penting.

### Alur penjurian

1. WeMakeDevs me-review semua submisi.
2. WeMakeDevs membuat *shortlist*.
3. Finalis dinilai oleh Switch, DevTools Academy, dan WeMakeDevs.

Artinya, kita harus lolos saringan pertama dulu. README dan video yang langsung jelas di menit pertama sangat menentukan.

---

## 5. Mengenal Switch

### Gambaran besar

Switch adalah "jembatan" yang menghubungkan **AI agent** (misalnya Claude Code, Codex, OpenCode) ke **chat tim** (Slack, Teams, Discord, Telegram, Mattermost). Di dalam chat, agent tampil seperti anggota tim: punya nama dan avatar sendiri, bisa di-*mention*, dan bisa membalas.

Switch **tidak menyediakan model AI**. Kita bawa agent sendiri.

```
  Manusia di chat  <──>  Switch server  <──>  AI agent
  (Mattermost, dsb.)     (room, aturan,        (Claude Code, Codex,
                          identitas)            atau client custom)
```

### Komponen yang perlu kamu tahu

| Komponen | Penjelasan |
|---|---|
| **Switch Console** | Aplikasi desktop. Menjalankan agent, menyalakan Switch server lokal di Docker, dan menghubungkan chat. Ini yang kita install (versi 0.40.1). |
| **Mattermost lokal** | Chat bawaan Switch lokal. Kita tidak butuh workspace Slack perusahaan. Ini bagus untuk reproducibility. |
| **Room** | Satu channel chat yang punya konteks bersama: pesan, instruksi, peran, dokumen referensi. Semua manusia dan agent di room melihat konteks yang sama. |
| **Agent** | Peserta AI di room. Bisa agent bawaan Console (Claude Code dll.) atau **agent custom** yang kita tulis sendiri dan terhubung lewat protokol agent Switch. |
| **Template** | File YAML yang mendefinisikan room, agent, instruksi, dan hubungan antar-room. Dengan template, setup bisa diulang orang lain. |
| **Addressing policy** | Aturan siapa yang boleh memanggil agent tertentu: hanya owner, owner dan agent milik owner, atau siapa saja. |
| **Identity claim** | Menghubungkan akun chat dengan pengguna Switch. Akun chat yang belum di-*claim* tidak dikenali oleh aturan addressing. |

### Dua jenis agent, dan kenapa bedanya penting

1. **Agent LLM lewat Console** (misalnya Claude Code). Pintar, bisa membaca kode, menjalankan tools, menulis jawaban. Tetapi ia hanya melihat pesan dalam bentuk teks seperti:
   `[Switch] Budi (workspace member) addressed you in room ...`
   Ia **tidak** melihat ID peserta yang unik.
2. **Client custom deterministik.** Program biasa (misalnya Python) yang terhubung langsung ke protokol Switch. Ia menerima *event* lengkap, termasuk ID pengirim (`sender`) dan perannya (`sender_role`). Tidak pintar, tetapi **bisa dipercaya untuk memeriksa identitas**.

Kombinasi keduanya adalah inti desain kita (lihat bagian 7).

---

## 6. Fakta teknis Switch 0.40.1 yang mengubah desain

Semua ini dicek langsung ke kode Switch di tag `switch-console-v0.40.1`, bukan hanya dari dokumentasi.

| Fakta | Dampak ke desain |
|---|---|
| **Transport live agent adalah WebSocket** (`/agents/{id}/connection/ws`). Dokumentasi di tag itu masih menyebut SSE, tetapi kodenya sudah WebSocket. SSE tinggal jalur lama. | Client custom harus memakai WebSocket. **Pelajaran: kalau dokumentasi dan kode berbeda, percayai kode.** |
| Agent LLM lewat Console **tidak melihat ID peserta**, hanya nama tampilan dan peran. | **Persetujuan tidak bisa diautentikasi oleh LLM.** Siapa pun bisa mengganti nama tampilan atau menulis teks yang meniru format. Perlu client deterministik atau pengecekan di luar chat. |
| Event pesan untuk client custom memuat `sender`, `sender_role` (owner/admin/member, null jika belum di-*claim*), `message_id`, `room_id`. | Client custom bisa mencocokkan pengirim dengan daftar orang yang berwenang, dan memakai `message_id` agar satu persetujuan tidak diproses dua kali. |
| Kirim pesan tanpa koneksi live: `POST /agents/{id}/message`. | Aplikasi kita bisa memposting "tanda terima" resmi ke room setelah perubahan diterapkan. |
| Lampiran masuk ke agent: PNG, JPEG, WebP, PDF, teks, Markdown, CSV, JSON. Maksimal 8 file per pesan, 10 MB per file. **Tidak ada video.** | Bukti dari manusia harus berupa gambar atau dokumen. Agent sendiri bisa mengirim file apa pun (termasuk video) lewat tool `send_attachment`. |
| Provider di template hanya **claude, codex, opencode**. | Agent lain (misalnya Gemini) tidak bisa didefinisikan di template versi ini. |
| Template room punya field: name, description, instructions, agents, users, roles, references, docs, aliases, dan lain-lain. Ada `connections` untuk GitHub. Room bisa dikelompokkan dan saling ditautkan. | Kita bisa membuat beberapa room yang saling terhubung dalam satu template yang bisa diulang. |
| Fitur *task* di Switch: "ada tetapi belum siap dipakai". | Jangan bergantung pada task Switch. Serah-terima antar-agent pakai @mention. |
| Build Windows dan Linux masih *early access*. | Kita di Windows. Harus dites live sedini mungkin. |
| Port server lokal **dipilih acak** oleh Console saat pertama jalan (gateway, API agent, Mattermost, Postgres), lalu disimpan. | Jangan *hard-code* `localhost:3000`. Pakai `SWITCH_API_ENDPOINT` yang ditampilkan Console di `.env`. |
| Pesan dari *incoming webhook* Mattermost dianggap dikirim oleh pembuat webhook, dan dibuang kalau pembuatnya admin Mattermost. | Alert otomatis (misalnya di BuzzerDefuse) harus dikirim lewat client custom yang terdaftar di Switch, bukan webhook. |
| Role `admin` di Switch adalah **bypass global** untuk semua izin. | Jangan jadikan orang yang berwenang menyetujui sebagai admin Switch. Simpan peran di tabel aplikasi kita, dipetakan dari ID pengirim. |
| Kalau aturan *addressing* menolak pengirim, **Switch sendiri** yang membalas penolakan, dan client gate tidak pernah menerima pesannya. | Di demo, biarkan orang berperan rendah lolos ke gate secara sengaja, supaya yang tampil adalah penolakan dari aplikasi kita. |
| Dokumen room di template berupa teks *inline* (nama, deskripsi, instruksi, isi), bukan path file. Agent hanya bisa mengedit dokumen buatannya sendiri. | Aturan yang dibaca kode (misalnya palet warna) disimpan di repo; dokumen room berisi versi yang dibaca manusia dan agent. |

---

## 7. Tiga prinsip desain yang kita pegang

### Prinsip 1: Tes pencabutan Switch

Untuk setiap ide, tanyakan: *"Kalau Switch dicabut, apa yang rusak?"* Jawaban yang baik: informasinya tersebar di beberapa orang dengan pekerjaan berbeda; orang-orang itu hanya bisa dijangkau dan dikoordinasikan di room; dan persetujuan hanya sah kalau datang dari pengirim yang diverifikasi Switch.

### Prinsip 2: Hasil nyata, bukan obrolan

Setiap ide harus berakhir dengan **perubahan keadaan yang bisa dibuktikan**: baris database berubah, pengiriman diblokir, kode di-*merge*, jadwal diperbarui. Disertai *receipt* atau catatan yang bisa diekspor.

### Prinsip 3: LLM mengusulkan, kode deterministik memutuskan

- **LLM** mengerjakan interpretasi, penelusuran, penjelasan, dan menyusun proposal.
- **Kode deterministik** mengerjakan: siapa yang boleh menyetujui, apakah proposal masih sama dengan yang disetujui, apakah data berubah sejak proposal dibuat, dan menerapkan perubahan secara atomik.
- **Instruksi room bukan batas keamanan.** Menulis "jangan lakukan X tanpa persetujuan" di prompt tidak menjamin apa pun.

Contoh pola persetujuan yang kita rancang (dari Recall Room):

```
@gate approve CP-0001 r2
```

Client `gate` (bukan LLM) lalu memeriksa dalam satu transaksi database:

1. `message_id` belum pernah diproses.
2. Pengirim punya peran dan ID-nya terdaftar sebagai orang berwenang.
3. Perintah dikirim dari room yang benar.
4. Peran pengirim memang boleh menjalankan perintah ini.
5. Revisi `r2` adalah revisi terbaru yang menunggu persetujuan.
6. Data belum berubah sejak proposal dibuat.
7. Penelusuran ulang menghasilkan aksi yang sama persis.
8. Terapkan perubahan.
9. Kirim *receipt* berdasarkan data yang benar-benar tersimpan.

---

## 8. Lima kandidat ide

Semua ide sudah dicek terhadap Switch 0.40.1. Urutan di bagian ini bukan peringkat; peringkatnya ada di bagian 9.

### 8.1 Recall Room (berbasis NusaQC)

**Satu kalimat:** ketika ada keluhan kualitas ikan dari pembeli, telusuri ke belakang sampai sumbernya dan ke depan sampai semua lot yang terdampak, isi celah data bersama orang yang tahu, lalu terapkan tindakan penahanan yang disetujui orang berwenang, semuanya di dalam room Switch.

**Latar belakang:** NusaQC adalah aplikasi inspeksi kualitas ikan yang kita bangun untuk COMPFEST 18 (AIC). Isinya inspeksi, grading, slot penyimpanan, dan dispatch. Recall Room adalah workflow baru di atasnya.

**Masalah nyata:** keracunan histamin pada ikan tuna dan sejenisnya (Scombridae). Regulasi keamanan pangan menuntut penelusuran *one-step-back / one-step-forward*: dari mana bahan datang, ke mana produk pergi. Kenyataannya, catatan sering bolong dan informasinya tersebar di beberapa orang.

**Pemeran:**

| Peran | Tugas |
|---|---|
| QA manager | Menentukan cakupan investigasi dan memberi persetujuan akhir |
| Receiving lead | Melengkapi bukti asal bahan yang hilang |
| Dispatch coordinator | Mengetahui status pengiriman |
| Ops lead | Melaksanakan penahanan di lantai produksi |
| `recall-trace` (Claude Code) | Menjalankan penelusuran deterministik, menyusun proposal |
| `recall-gate` (client custom, bukan LLM) | Memverifikasi pengirim dan menerapkan persetujuan |

**Tiga room yang saling terhubung:** `recall-intake` (keluhan masuk), `recall-floor` (koordinasi lapangan), `recall-decision` (persetujuan).

**Alur demo:**

1. Pembeli di Jepang mengeluhkan histamin pada pengiriman `DISP-20261104-001`.
2. Agent menelusuri ke belakang sampai batch penerimaan `RB-20261102-A` (tuna sirip kuning dari KM Bahari Jaya), lalu ke depan ke lot-lot lain dari batch yang sama.
3. Agent menemukan `LOT-007` tidak punya data asal. Ia bertanya di room. Receiving lead mengonfirmasi tautan lewat `@gate confirm LC-0001`.
4. Agent menyusun proposal `CP-0001`: tahan lot yang masih di gudang, blokir pengiriman ke EU yang belum berangkat, tandai pengiriman ke USA yang sedang di jalan.
5. QA manager menyetujui: `@gate approve CP-0001 r2`.
6. Gate memeriksa dan menerapkan. Aplikasi benar-benar menolak pengiriman lot yang ditahan (HTTP 409).
7. Catatan investigasi lengkap diekspor.

**Kekuatan:** Switch paling sentral di antara kelima ide (banyak orang, banyak room, persetujuan terverifikasi). Masalahnya serius dan spesifik. Hasilnya berupa perubahan keadaan yang kuat.

**Kelemahan:** paling banyak yang harus dibangun (tabel baru, mesin penelusuran, client gate custom, perbaikan beberapa celah di NusaQC). Domainnya perlu dijelaskan ke juri yang bukan orang industri pangan.

**Celah NusaQC yang harus ditambal** (sudah dicek di kode): `create_dispatch` menerima lot apa saja tanpa validasi; status dispatch bisa diisi string apa saja; tidak ada autentikasi; ada 89 `lot_id` yang duplikat dari 550 inspeksi.

### 8.2 AccessFix Room

**Satu kalimat:** seseorang melaporkan hambatan aksesibilitas; agent mereproduksi dan memperbaikinya; agent lain me-review secara independen; manusia memverifikasi pengalaman yang sudah diperbaiki.

**Alur:** laporan hambatan → klarifikasi → reproduksi → perbaikan → review independen → penerimaan manusia.

**Demo:** aplikasi booking dengan dialog bermasalah. Fokus keyboard tertinggal di belakang dialog, Tab bisa ke kontrol di belakang, dan saat dialog ditutup fokus tidak kembali.

1. Reporter: *"@accessfix saya tidak bisa booking tanpa mouse."*
2. Agent developer (Claude) membuka browser sungguhan dengan Playwright, mereproduksi, menemukan komponennya, dan memperbaiki di branch terpisah.
3. Agent reviewer (Codex, provider berbeda supaya benar-benar independen) memeriksa fokus, navigasi, label aksesibel, dan alur booking.
4. Reporter mencoba versi baru. Maintainer menerima revisi yang sudah di-review lewat *gate* (`@gate accept <revisi>`), client deterministik yang memverifikasi pengirim seperti di Recall Room.

**Desain untuk 0.40.1:** template custom dengan blok `agents:`; serah-terima lewat @mention; penerimaan manusia lewat gate di room, dan `main` tetap dilindungi branch protection GitHub sehingga tidak ada merge otomatis.

**Kekuatan:** demo sangat visual (sebelum dan sesudah di browser). Mudah dipahami juri developer. Hasil berupa PR yang nyata.

**Kelemahan:** idenya lebih "umum" di kalangan developer tools. Gate menambah pekerjaan dibanding hanya memakai GitHub.

### 8.3 Deadline Rescue Room (berbasis Compe-In)

**Satu kalimat:** asisten perencanaan di Switch yang membantu tim lomba mengubah perubahan deadline atau kemunduran pekerjaan menjadi jadwal baru yang disepakati dan benar-benar diterapkan.

**Latar belakang:** Compe-In adalah aplikasi manajemen lomba kita (Supabase, Google OAuth, ada chatbot Gemini).

**Alur:**

1. Seseorang melaporkan perubahan deadline atau hambatan di room.
2. Agent membaca task, tanggal, dependensi, dan tahap lomba dari Compe-In.
3. Agent menemukan konflik dan menanyakan info yang kurang (misalnya ketersediaan anggota).
4. Agent menyusun revisi jadwal beserta *tradeoff*-nya.
5. Tim berdiskusi.
6. Ketua tim menyetujui revisi yang spesifik.
7. Kode aplikasi memvalidasi dan menerapkan secara atomik.
8. Agent memposting hasil dan tautan ke timeline baru.

**Desain untuk 0.40.1:**

- Persetujuan lewat client approver deterministik di room, dengan perintah `@approver approve P-003 r2`. Akun chat dihubungkan ke akun Compe-In lewat kode sekali pakai.
- Agent perencana adalah agent Console (Claude), bukan chatbot Gemini yang sudah ada. Ia butuh API, CLI, dan user Supabase dengan hak minimal.

**Kekuatan:** masalahnya relatable bagi juri (semua peserta hackathon mengalaminya). Ironi yang bagus untuk presentasi.

**Kelemahan:** masalahnya terasa lebih ringan dibanding keamanan pangan. Switch tidak terlalu wajib karena orang bisa langsung mengedit jadwal di aplikasi. Reproducibility lebih sulit karena memakai Supabase hosted dan Google OAuth (solusinya Supabase lokal).

### 8.4 BuzzerDefuse Room

**Satu kalimat:** ketika serangan hoaks terkoordinasi menyerang sebuah merek, agent forensik dan agent penyusun bekerja bersama PR dan Legal di satu room Switch, dan pernyataan publik baru terbit setelah PR dan Legal sama-sama menyetujui revisi yang persis sama.

**Masalah nyata:** merek di Indonesia sering diserang akun-akun *buzzer* yang menyebar klaim palsu dalam hitungan jam. Responsnya harus cepat, tetapi juga benar secara hukum, dan tidak boleh menganggap pelanggan yang benar-benar mengeluh sebagai bot.

**Pemeran:**

| Peran | Tugas |
|---|---|
| PR crisis lead | Menentukan cakupan dan nada; kunci persetujuan pertama (`release`) |
| Legal officer | Mengoreksi klaim yang berisiko hukum; kunci persetujuan kedua (`cosign`) |
| Social media analyst (opsional) | Menilai akun yang ambigu |
| `social-listener` (client custom, bukan LLM) | Mengirim alert dan file data postingan ke room |
| `buzzer-forensic` (Claude Code) | Menjalankan pengelompokan (*clustering*) deterministik dan menjelaskan hasilnya |
| `counter-narrative` (Claude Code atau Codex) | Menyusun pernyataan dan FAQ sebagai revisi bernomor |
| `defuse-gate` (client custom, bukan LLM) | Memverifikasi pengirim dan menerapkan dua kunci |

**Alur demo (data sintetis, merek fiktif "Tirta Sejati"):**

1. `social-listener` memposting lonjakan 60 postingan dalam 10 menit di `#TercemarBakteriTirta`.
2. Agent forensik menemukan klaster 42 akun dengan indikator koordinasi, 11 postingan yang tampak keluhan asli, dan 7 yang ambigu. Agent menanyakan cakupan respons ke PR.
3. PR memutuskan: pernyataan publik untuk klaim palsu, dan customer care menghubungi 11 pelanggan asli.
4. `counter-narrative` menyusun `DEBUNK-001 r1` dari sertifikat lab yang dilampirkan.
5. Legal mengoreksi ("jangan bilang semua batch aman", tambahkan nomor sertifikat), lalu agent membuat `r2`.
6. Analyst mencoba `release` dan ditolak. PR memberi kunci 1. PR mencoba `cosign` sendiri dan ditolak karena harus orang lain. Legal memberi kunci 2.
7. Pernyataan terbit di layanan *newsroom* lokal. Menerbitkan langsung revisi yang belum disetujui ditolak (HTTP 409).

**Desain untuk 0.40.1:** gate memakai WebSocket dan memverifikasi ID pengirim dari Switch (bukan tanda tangan digital). Alert datang dari client custom, bukan webhook Mattermost. Peran disimpan di aplikasi, bukan sebagai admin Switch.

**Pengaman wajib:** keluaran publik tidak pernah menyebut atau mengutip akun individu. Keluhan asli dikirim ke customer care, tidak pernah ke laporan platform. Tanpa pengaman ini, ide ini bisa terbaca sebagai alat untuk membungkam kritik.

**Kekuatan:** dua kunci dari dua orang berbeda yang diverifikasi Switch adalah jawaban paling jelas untuk tes pencabutan Switch. Momen "Key 1/2, menunggu Legal" sangat mudah divideokan. Dibangun dari nol, jadi tidak perlu menambal aplikasi lama.

**Kelemahan:** hanya satu room. Data sintetis yang sengaja dibuat mudah dikelompokkan bisa terlihat seperti rekayasa (diatasi dengan kelompok keluhan asli sebagai kontrol). Topiknya sensitif.

### 8.5 BrandEcho Room

**Satu kalimat:** gerbang *pre-flight* untuk aset kampanye: agent mengecek teks dan banner terhadap aturan merek dan mengadaptasi konsep per kanal; Brand Director mensertifikasi revisi yang tepat di room; hanya aset tersertifikasi yang masuk antrean publikasi.

**Masalah nyata:** saat kampanye berjalan di banyak kanal, aset mudah melenceng (warna hampir benar, logo terlalu mepet tepi, slogan bertentangan dengan positioning). Review biasanya manual, dan tidak ada bukti versi mana yang disetujui.

**Pemeran:**

| Peran | Tugas |
|---|---|
| Copywriter | Mengirim konsep dan banner, menerapkan perbaikan |
| Brand Director | Memberi arahan kreatif; satu-satunya yang boleh mensertifikasi |
| `brand-guard` (Claude Code) | Menjalankan pengecekan aturan, membaca gambar banner, memberi review nada sebagai saran |
| `channel-adapter` (Codex atau Claude Code) | Menulis varian teks per kanal sebagai revisi baru |
| `brand-gate` (client custom, bukan LLM) | Memverifikasi pengirim dan menerapkan sertifikasi |

**Alur demo (merek fiktif "Kartu Teduh"):**

1. Copywriter mengirim konsep "Swipe like a degen!" beserta banner.
2. Pengecekan kode menemukan 3 pelanggaran: warna di luar palet, logo 8 px dari tepi (minimal 24 px), dan kata terlarang.
3. Brand Director memberi arahan. Copywriter mengunggah banner v2, dan semua cek lolos.
4. `channel-adapter` membuat varian TikTok, Instagram, dan LinkedIn (`r3`); setiap varian dicek ulang.
5. Copywriter mencoba mensertifikasi sendiri dan ditolak. Director mencoba revisi lama dan ditolak. Director mensertifikasi `r3`.
6. Aset masuk antrean publikasi lokal. Mendorong banner lama langsung ke antrean ditolak (HTTP 409).

**Desain:** lolos atau gagal hanya ditentukan oleh cek kode (warna dengan Pillow, margin logo dengan OpenCV, kata terlarang, tagline), bukan skor dari AI. Review nada dari AI hanya saran. Pengirim aset tidak pernah boleh mensertifikasi. Gate memverifikasi ID pengirim dari Switch.

**Kekuatan:** demo paling visual (banner sebelum dan sesudah, galeri pratinjau feed). Workflow bisnis untuk tim non-developer.

**Kelemahan:** peran manusia cukup tipis (satu arahan, satu sertifikasi). Alat desain sudah punya fitur approval, dan kategori alat *brand compliance* sudah ramai.

---

## 9. Perbandingan dan skor

Detail lengkap (termasuk checklist validasi per ide) ada di `idea-ranking.md`.

### Skor dengan bobot resmi (fokus potensi, tanpa faktor waktu)

| Peringkat | Ide | Switch (30%) | Technical (25%) | Creativity (25%) | Presentation (20%) | **Total (dari 10)** |
|---|---|---|---|---|---|---|
| 1 | Recall Room | 10 | 8 | 9 | 8 | **8,85** |
| 2 | BuzzerDefuse | 9 | 7 | 8 | 8 | **8,05** |
| 3 | AccessFix | 9 | 7 | 7 | 9 | **8,00** |
| 4 | BrandEcho | 8 | 7 | 7 | 9 | **7,70** |
| 5 | Deadline Rescue | 7 | 6 | 6 | 8 | **6,70** |

Alasan skor:

- **Recall Room:** Switch 10 karena tiga room terhubung, celah data ditutup oleh orang dengan pekerjaan berbeda, dan persetujuan hanya sah dari pengirim terverifikasi. Technical 8. Creativity 9 karena masalah keamanan pangan yang serius. Presentation 8 karena domainnya perlu dijelaskan ke juri.
- **BuzzerDefuse:** Switch 9 karena dua kunci dari dua orang berbeda yang diverifikasi Switch, tetapi hanya satu room. Technical 7 karena dibangun dari nol dan datanya sintetis. Creativity 8 dengan syarat pengaman tetap ada; tanpa pengaman turun ke sekitar 6. Presentation 8.
- **AccessFix:** Switch 9 karena reporter, dua agent, dan maintainer bertemu di satu room, dan penerimaan lewat gate terverifikasi. Technical 7 karena gate menambah pekerjaan. Creativity 7 karena idenya umum di developer tools. Presentation 9 karena sebelum dan sesudah di browser sangat visual.
- **BrandEcho:** Switch 8 karena gate terverifikasi dan gambar mengalir dua arah, tetapi peran manusia tipis. Technical 7. Creativity 7 karena kategori ini sudah ramai. Presentation 9 karena paling visual.
- **Deadline Rescue:** Switch 7 karena tim tetap bisa mengedit jadwal langsung di aplikasi. Technical 6 karena Supabase hosted dan OAuth sulit direproduksi juri. Creativity 6 karena taruhannya rendah. Presentation 8.

**Jika client gate custom gagal di tes live,** semua ide turun sekitar 1 poin di Switch (sekitar −0,3 total). AccessFix punya cadangan paling aman: penerimaan bisa ditegakkan lewat branch protection GitHub tanpa gate.

### Jika sisa waktu ikut dihitung

Di sini nilai Technical dibaca ulang sebagai "kemungkinan berjalan andal dan bisa direproduksi sebelum 7 Nov 23:59 IST". Tiga kriteria lain tetap.

| Ide | Technical (disesuaikan) | **Total** | Risiko utama |
|---|---|---|---|
| Recall Room | 5 | **8,10** | Tambalan NusaQC + mesin penelusuran + gate + 3 room + badge UI |
| BuzzerDefuse | 7 | **8,05** | Gate + clustering + newsroom, semuanya baru |
| AccessFix | 7 | **8,00** | Playwright di Windows; `connections` GitHub di server lokal belum pasti |
| BrandEcho | 6 | **7,45** | Cek gambar + gate + antrean, semuanya baru |
| Deadline Rescue | 5 | **6,45** | Supabase hosted, OAuth, dan penautan identitas |

Tiga teratas hanya berselisih 0,1. Rubrik saja tidak lagi membedakan mereka; yang membedakan adalah sisa waktu.

### Ringkasan posisi

- **Recall Room:** potensi tertinggi, risiko pengerjaan tertinggi.
- **BuzzerDefuse:** **rekomendasi untuk deadline ini.** Mempertahankan sebagian besar keunggulan Switch milik Recall, momen demo paling jelas, dan tidak perlu menambal aplikasi lama.
- **AccessFix:** paling kecil dan visual, tetapi masalahnya lebih lemah.
- **BrandEcho:** kalah atau seri di semua kriteria dibanding AccessFix.
- **Deadline Rescue:** kalah atau seri di semua kriteria dibanding BuzzerDefuse.

---

## 10. Risiko dan hal yang belum pasti

### Soal kompetisi

- **Jumlah pemenang Core Contribution tidak konsisten:** bagian hadiah menyebut 20 PR, bagian penjurian menyebut 10 PR. Tidak memengaruhi track kita.
- **Detail registrasi dan formulir submit** belum terbaca lengkap dari halaman lomba. Harus dicek langsung sebelum deadline. Bantuan tersedia di [Discord WeMakeDevs](https://discord.gg/E2rWw2Yhsm).
- Durasi video demo dan syarat visibilitas repo belum diketahui.

### Soal teknis Switch (perlu tes live)

- Apakah agent custom (client gate) bisa dimasukkan ke room yang dibuat dari template?
- Apakah *alias* dan *roles* dari template benar-benar diterapkan?
- Apakah ID pengirim dari chat yang di-*bridge* (Mattermost) stabil?
- Apakah addressing per-room bisa diatur dari UI?
- Seberapa stabil Switch Console di Windows (masih early access)?
- Untuk AccessFix: apakah `connections` GitHub berjalan di server lokal?
- Untuk BuzzerDefuse: apakah @mention dari client `social-listener` (lewat `POST /message`) membangunkan agent Console dengan aturan `owner-agents`?
- Untuk BrandEcho: apakah gambar yang diunggah orang sampai ke agent tanpa dikompres ulang (yang akan mengubah hash dan warna)?

**Prioritas tertinggi, apa pun ide yang dipilih:** jalankan Switch Console 0.40.1 di mesin kita, hubungkan satu agent ke satu room Mattermost, dan pastikan pesan bolak-balik berjalan. Setelah itu, uji client custom yang terhubung via WebSocket. Kelima ide membutuhkan client gate yang sama; yang berbeda hanya tata bahasa perintah dan pengecekan di aplikasi.

---

## 11. Yang perlu kita putuskan bersama

1. **Pilih ide.** Pilihan nyatanya: BuzzerDefuse (rekomendasi untuk deadline ini), Recall Room (potensi tertinggi, paling ambisius), atau AccessFix (paling kecil dan paling aman). BrandEcho dan Deadline Rescue menurut analisis ini kalah di semua kriteria dibanding salah satu ide di atas.
2. **Bagi peran.** Contoh untuk BuzzerDefuse: satu orang mengerjakan client gate, `social-listener`, dan setup Switch; satu orang API kasus, clustering, dan newsroom lokal; satu orang data sintetis, README, dan video. Untuk Recall: satu orang backend NusaQC dan mesin penelusuran, satu orang client gate dan setup Switch, satu orang README, video, dan data demo.
3. **Tentukan batas minimum yang harus jalan** (versi paling kecil yang tetap lolos tes pencabutan Switch), lalu tambahkan fitur di atasnya kalau waktu masih ada.
4. **Putuskan apakah ikut Blog side track.** Biayanya rendah karena bahannya sama dengan README.

Spesifikasi lengkap tiap ide ada di file masing-masing. `recall-room.md` adalah yang paling detail (model data, perintah gate, rencana tes, urutan pembangunan, rencana video). Peringkat lengkap ada di `idea-ranking.md`.

---

## 12. Glosarium

| Istilah | Arti |
|---|---|
| **Switch** | Platform open source yang menghubungkan AI agent ke chat tim |
| **Switch Console** | Aplikasi desktop untuk menjalankan Switch dan agent secara lokal |
| **Room** | Channel chat dengan konteks bersama untuk manusia dan agent |
| **Template** | File YAML yang mendefinisikan room, agent, dan instruksi agar setup bisa diulang |
| **Addressing policy** | Aturan siapa yang boleh memanggil sebuah agent |
| **Identity claim** | Menautkan akun chat dengan pengguna Switch |
| **WebSocket** | Koneksi dua arah yang dipakai agent custom untuk menerima event dari Switch |
| **Client deterministik / gate** | Program non-LLM yang memeriksa identitas dan aturan secara pasti sebelum menerapkan perubahan |
| **Idempotensi** | Satu perintah yang diproses dua kali tetap hanya berefek sekali (dicek lewat `message_id`) |
| **Receipt** | Pesan konfirmasi yang dibuat dari data yang benar-benar tersimpan, bukan dari klaim agent |
| **One-step-back / one-step-forward** | Prinsip ketertelusuran pangan: tahu asal bahan dan tujuan produk |
| **Histamin / Scombridae** | Racun yang terbentuk pada ikan keluarga tuna jika suhu tidak terjaga, penyebab umum recall ikan |
| **Lot / batch / dispatch** | Satuan produk / satuan penerimaan bahan baku / satuan pengiriman |
| **Branch protection** | Aturan GitHub yang mewajibkan review sebelum kode bisa di-*merge* |
| **Buzzer** | Akun-akun media sosial (sering dibayar) yang bergerak terkoordinasi untuk menggiring opini |
| **Two-key / dua kunci** | Aksi baru dijalankan setelah dua orang berbeda dengan peran berbeda menyetujui revisi yang sama |
| **Separation of duties** | Orang yang membuat sesuatu tidak boleh menjadi orang yang menyetujuinya |
| **Pre-flight gate** | Pemeriksaan wajib sebelum aset boleh diterbitkan |
| **Reproducibility** | Kemampuan orang lain menjalankan proyek dari *clone* repo, salah satu syarat penjurian |
