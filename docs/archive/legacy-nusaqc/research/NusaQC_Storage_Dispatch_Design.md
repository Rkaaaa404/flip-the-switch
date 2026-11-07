# 🆕 NusaQC — Feature Design: Storage Map & Dispatch
## Ide Konten + MVP Scope + Stitch UI Prompts Lengkap
> Dua tab baru: `Lot Storage` dan `Export Dispatch`

---

## 🧠 BAGIAN 1 — MENGAPA DUA FITUR INI MASUK AKAL UNTUK NUSAQC

### Alur Nilai yang Lengkap

Tanpa dua fitur ini, NusaQC hanya menjawab **"apakah ikan ini layak?"** — tapi tidak menjawab **"setelah layak, ikan itu pergi ke mana?"**

```
[Conveyor]                [Storage]              [Export]
Ikan masuk
    ↓
[NusaQC Inspection]  →→  [Lot Storage Map]  →→  [Export Dispatch]
Grade A/B/C                Slot mana?             Dikirim ke buyer mana?
PASS / FAIL                Cold/Frozen?           Container berapa?
    ↓                          ↓                       ↓
Dashboard ✅           [FITUR BARU #1]         [FITUR BARU #2]
Lot History ✅
```

Ini **memperkuat narasi Smart Manufacturing** di proposal:
- Sekarang: Inspect → Log
- Dengan fitur baru: Inspect → **Store → Dispatch** (full traceability chain)

Dari proposal NusaQC sendiri, Gap 3 yang ingin diselesaikan adalah:
> *"Paper-based → Digital Traceability: mencatat setiap hasil inspeksi berdasarkan lot ID, waktu, grade, defect, confidence, dan citra sehingga data QC terdokumentasi dan dapat ditelusuri."*

Storage + Dispatch adalah **perwujudan konkret dari digital traceability** ini — dari inspeksi hingga sampai ke tangan buyer.

---

## 📦 BAGIAN 2 — FITUR #1: LOT STORAGE MAP

### 2.1 Apa Isinya?

**Konteks di UPI Ikan:**
Setelah ikan melewati QC dan mendapat status PASS, ikan tersebut dimasukkan ke area penyimpanan sebelum diproses lebih lanjut atau dikirim. Di UPI ekspor, terdapat beberapa zona penyimpanan:

| Zona | Suhu | Untuk |
|------|------|-------|
| Cold Zone | 0–4°C | Ikan segar Grade A/B, menunggu packing |
| Frozen Zone | ≤ -18°C | Ikan yang akan di-IQF atau deep-frozen |
| Ambient Zone | Suhu ruang | Produk ikan olahan kering/kemasan |

**Core concept:** Setelah lot dinyatakan PASS di Inspection screen, lot tersebut muncul di daftar "Pending Storage." Operator kemudian meng-assign lot tersebut ke slot penyimpanan yang sesuai di grid map.

---

### 2.2 Batasan MVP (Sesuai Rulebook)

**Yang ADA di MVP:**
```
✅ Grid slot penyimpanan statis (misal 5×6 = 30 slot total)
✅ Dua zona: Cold Zone dan Frozen Zone
✅ "Pending Storage" list — diambil dari SQLite:
   lot dengan decision=PASS yang belum punya storage_slot
✅ Klik slot → assign lot ke slot (simpan ke SQLite)
✅ Slot menampilkan: Lot ID, Grade, Fish Family, stored since
✅ Status per slot: Available / Occupied
✅ Unassign slot (jika lot sudah dipindah/dispatch)
```

**Yang TIDAK ADA di MVP (sesuai rulebook — hindari over-engineer):**
```
❌ IoT temperature sensor per slot (hardware tambahan)
❌ Background monitoring / auto-alert temperature
❌ Expiry countdown / real-time freshness degradation
❌ Multi-warehouse / multi-lokasi
❌ Barcode/QR scanner integration
```

---

### 2.3 Rencana Pengembangan di Final Hackathon (Realistis)

**Feasible dalam 10 jam hackathon:**
```
🔧 Cold-Chain Monitor:
   - Tambah endpoint GET /api/v1/storage/temperature
   - Baca dari sensor suhu (DS18B20 via RPi GPIO)
   - Tampilkan suhu per zona di panel kanan
   - Alert visual jika suhu melebihi threshold

🔧 Auto-assign suggestion:
   - Jika Grade A → suggest Cold Zone
   - Jika Frozen product → suggest Frozen Zone
   - Operator tetap bisa override
```

---

### 2.4 Data Model (SQLite — Tambahan)

```sql
-- Tabel baru yang perlu ditambahkan:
TABLE: storage_slots
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
slot_id       TEXT PRIMARY KEY   -- contoh: "C-01", "F-03", "A-12"
zone          TEXT               -- "cold" | "frozen" | "ambient"
lot_id        TEXT               -- FK ke inspection_logs.lot_id (nullable)
assigned_at   DATETIME           -- kapan lot di-assign ke slot ini
assigned_by   TEXT               -- "QC Supervisor" (dari config)

-- Update tabel inspection_logs (tambah kolom):
ALTER TABLE inspection_logs ADD COLUMN storage_slot TEXT;
ALTER TABLE inspection_logs ADD COLUMN storage_zone TEXT;
ALTER TABLE inspection_logs ADD COLUMN stored_at    DATETIME;
```

---

### 2.5 API Endpoints Baru (Backend)

```
GET  /api/v1/storage/slots           → Semua slot + status + lot assigned
GET  /api/v1/storage/pending         → Lot PASS yang belum punya slot
POST /api/v1/storage/assign          → Assign lot ke slot
     body: { slot_id, lot_id }
DELETE /api/v1/storage/slots/{slot_id} → Kosongkan slot (unassign)
```

---

## 🚢 BAGIAN 3 — FITUR #2: EXPORT DISPATCH

### 3.1 Apa Isinya?

**Konteks di UPI Ikan:**
Setelah lot disimpan dan siap dikirim, UPI perlu membuat catatan pengiriman ekspor. Ini mencakup: lot mana yang dikirim, ke buyer mana, tanggal keberangkatan, dan nomor kontainer.

Tanpa fitur ini, proses NusaQC berhenti di storage — tapi tidak ada bukti digital bahwa lot yang sudah ter-QC benar-benar sampai ke tangan pembeli. Dispatch adalah **dokumen traceability akhir** yang menjawab: "ikan dengan Grade A yang diinspeksi pada tanggal X, sekarang ada di kontainer Y, dikirim ke buyer Z."

**Core concept:** Operator membuat record dispatch baru dengan memilih lot-lot dari storage, mengisi informasi pembeli dan tujuan, lalu menyimpannya. Lot yang sudah di-dispatch ditandai sebagai "Dispatched" di Storage Map.

---

### 3.2 Batasan MVP (Sesuai Rulebook)

**Yang ADA di MVP:**
```
✅ Tabel dispatch records (Lot ID, Buyer, Destination, Date, Status)
✅ "+ New Dispatch" form:
   - Pilih lot dari storage (multi-select dari daftar stored lots)
   - Nama buyer/perusahaan
   - Negara tujuan (dropdown: USA, Japan, China, EU, dll)
   - Tanggal & estimasi keberangkatan
   - Nomor container (text input)
   - Catatan tambahan (optional)
✅ Status badge: Pending / Dispatched
✅ Dispatch mengubah status lot menjadi "dispatched" di SQLite
✅ Filter dispatch records by date / destination / status
```

**Yang TIDAK ADA di MVP:**
```
❌ Export ke PDF manifest (untuk Final)
❌ Integrasi dengan sistem BKIPM/KKP elektronik
❌ Tracking pengiriman real-time (Shipper API)
❌ QR code generation per container
❌ Auto-calculate QC summary per dispatch
```

---

### 3.3 Rencana Pengembangan di Final Hackathon (Realistis)

**Feasible dalam 10 jam hackathon:**
```
🔧 QC Summary per Dispatch:
   - Saat dispatch dibuat, hitung:
     * % PASS dari semua lot di dispatch ini
     * Avg freshness confidence
     * Jumlah defect terdeteksi total
   - Tampilkan sebagai "Quality Certificate Preview"
   - Ini bisa dijadikan argumen: "NusaQC generates exportable
     QC evidence untuk auditor FDA/BKIPM"

🔧 Export Dispatch Summary:
   - Generate teks summary yang bisa di-copy:
     "Dispatch #DISP-001: 5 lots, Avg Grade A, 
      0 defects detected, Destination: USA"
   - Copy to clipboard button
```

---

### 3.4 Data Model (SQLite — Tambahan)

```sql
TABLE: dispatches
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
dispatch_id      TEXT PRIMARY KEY  -- "DISP-2026-0825-001"
buyer_name       TEXT NOT NULL
destination      TEXT NOT NULL     -- "USA", "Japan", "China", dll
container_no     TEXT              -- "CONT-ABC123" (optional)
dispatch_date    DATETIME
estimated_arrival DATETIME
status           TEXT              -- "pending" | "dispatched"
notes            TEXT
created_at       DATETIME

TABLE: dispatch_lots  (many-to-many)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
id               INTEGER PRIMARY KEY AUTOINCREMENT
dispatch_id      TEXT    -- FK ke dispatches
lot_id           TEXT    -- FK ke inspection_logs

-- Update inspection_logs:
ALTER TABLE inspection_logs ADD COLUMN dispatch_id   TEXT;
ALTER TABLE inspection_logs ADD COLUMN dispatched_at DATETIME;
```

---

### 3.5 API Endpoints Baru (Backend)

```
GET  /api/v1/dispatch               → Semua dispatch records
GET  /api/v1/dispatch/{dispatch_id} → Detail satu dispatch + lot list
POST /api/v1/dispatch               → Buat dispatch baru
     body: { buyer_name, destination, container_no,
             dispatch_date, lot_ids[], notes }
PATCH /api/v1/dispatch/{dispatch_id}/status → Update status ke "dispatched"
GET  /api/v1/dispatch/available-lots → Stored lots yang belum di-dispatch
```

---

## 🎨 BAGIAN 4 — STITCH UI PROMPTS: LOT STORAGE MAP

> **Catatan:** Jalankan prompt secara berurutan. Satu prompt per giliran.
> Pastikan sidebar NusaQC sudah ada (dari sesi sebelumnya) sebelum mulai.

---

### UPDATE SIDEBAR DULU (Jalankan ini sebelum buat screen baru)

```
On the left sidebar, add two new navigation items between "Lot History" 
and "Settings":

1. "Lot Storage" with a warehouse/box icon
2. "Dispatch" with a truck/shipping icon

The sidebar order should now be:
- Dashboard
- Inspection
- Lot History
- Lot Storage    ← BARU
- Dispatch       ← BARU
- Settings

Keep all existing sidebar styling unchanged (dark background #0F172A,
same icon and text style as existing items).
```

---

### STORAGE SCREEN — Prompt S1: Foundation Layout

```
Create the Lot Storage screen (when user clicks "Lot Storage" in sidebar).

Page title: "Lot Storage Map"
Subtitle: "Assign inspected lots to cold storage slots"

Layout: Two columns.
Left column (65% width): Storage grid map
Right column (35% width): Pending Storage panel

Left column contains:
- A section header "Cold Zone" with a snowflake icon and a blue-tinted 
  badge showing "18 available  |  6 occupied"
- A 5×5 grid of storage slot buttons below it

Right column contains:
- A panel title "Pending Storage" with a clock icon and a badge 
  showing "3" (pending count)
- Below: a vertical list of 3 lot cards waiting to be assigned

Use the same design language as the rest of NusaQC: white cards, 
slate-50 background, Inter font, sky-blue (#0EA5E9) accent.
```

---

### STORAGE SCREEN — Prompt S2: Storage Grid Slots

```
On the Lot Storage screen, update the 5×5 grid in the left column.

Each slot is a square button (roughly 90×90px) with rounded corners.

Show these states across the grid:

AVAILABLE slots (most of them): 
- White background, light gray border
- Slot label in center: "C-01", "C-02" etc. in small gray text
- No other content

OCCUPIED slots (6 of them, scattered):
- Light blue background (#EFF6FF)
- Sky blue border
- Slot label "C-06" at top-left in small text (10px)
- Lot ID "LOT-2026-0730-003" in bold sky-blue monospace text (11px)
- Fish family below: "Scombridae" in gray text (10px)
- Grade badge at bottom-right: green "A" circle badge

Show a second section below the Cold Zone grid titled "Frozen Zone"
with an ice/snowflake icon, showing a 2×5 grid of slots labeled 
"F-01" through "F-10". All slots in frozen zone should be available 
(white/empty) for now.

Do not change the right column.
```

---

### STORAGE SCREEN — Prompt S3: Pending Storage Panel

```
On the Lot Storage screen, update the right column "Pending Storage" panel.

Show 3 lot cards in a vertical list. Each card has:
- Light yellow-amber background (#FFFBEB) with amber left border (3px)
- Lot ID in monospace sky-blue bold text: "LOT-2026-0730-008"
- Fish family below: "Cichlidae"
- Grade badge: green "A" circle
- Confidence: "88.3%"
- A small label: "Waiting for slot assignment"
- At the bottom of each card: two small buttons side by side:
  * "Assign to Cold" button (sky-blue, small, pill-shaped)
  * "Assign to Frozen" button (outline, small, pill-shaped)

The three cards should show different lots:
Card 1: LOT-2026-0730-008 | Cichlidae | Grade A | 88.3%
Card 2: LOT-2026-0730-007 | Scombridae | Grade B | 74.1%
Card 3: LOT-2026-0730-006 | Scombridae | Grade A | 91.7%

Below the 3 cards, add a "View All in Lot History" text link.
```

---

### STORAGE SCREEN — Prompt S4: Slot Assignment Interaction

```
On the Lot Storage screen, show the state when a user hovers over 
an available slot (for example slot "C-09").

Show slot C-09 with:
- Green-tinted background (#F0FDF4)
- Green dashed border
- A "+" icon in center
- A tooltip above the slot showing:
  "C-09 — Cold Zone (Compatible)
   Click to assign: LOT-2026-0730-008 (Grade A, Cichlidae)"

Also show a blue banner/notification bar at the top of the left column:
"Placing: LOT-2026-0730-008 (Cichlidae, Grade A) — 
Click a green highlighted slot to place the lot"
With a small × button to cancel the placement.

Highlight ALL available Cold Zone slots with the green-tinted style 
to show they are compatible with this Grade A lot.

Do not highlight Frozen Zone slots during this interaction 
(they are shown grayed out with 40% opacity to indicate incompatibility).
```

---

### STORAGE SCREEN — Prompt S5: Summary Statistics Bar

```
On the Lot Storage screen, add a horizontal statistics bar at the very top 
of the main content area, above both columns.

The bar shows 4 statistics in a single row:
- Total Slots: 35
- Occupied: 6 (sky-blue colored number)
- Available: 29 (green colored number)
- Pending Assignment: 3 (amber colored number)

Style: white background, thin bottom border, 12px height padding,
statistics separated by a vertical divider line.

Below the statistics bar, add a small filter row:
"Show zone:" followed by three pill toggle buttons:
[All Zones ✓] [Cold Zone] [Frozen Zone]

The "All Zones" button should be active (sky-blue background, white text).
The others should be inactive (white background, gray text).

Do not change anything in the two-column layout below.
```

---

### STORAGE SCREEN — Prompt S6: Occupied Slot Detail Panel

```
On the Lot Storage screen, show the state when a user clicks on 
an occupied slot (for example slot "C-06").

Show a compact detail panel sliding in from the right side, overlapping 
the Pending Storage panel (like a side drawer, 280px wide).

The detail panel contains:
- Header: "Slot C-06" with an × close button
- Zone badge: blue "Cold Zone" pill

Detail rows with label and value:
- Lot ID: LOT-2026-0730-003 (monospace sky-blue)
- Fish Family: Scombridae
- Grade: A (green circle badge)
- Confidence: 92.1%
- Defects Found: 0
- Stored Since: 2026-07-30 10:31:05
- Duration: 2 hours 14 minutes

Two action buttons at the bottom:
- "View Inspection Detail" button (outline, sky-blue, with external link icon)
- "Clear Slot" button (outline, red, with trash icon)

Below buttons: small warning text in gray:
"Clearing a slot does not delete the inspection record."
```

---

## 🚢 BAGIAN 5 — STITCH UI PROMPTS: EXPORT DISPATCH

---

### DISPATCH SCREEN — Prompt D1: Foundation Layout

```
Create the Dispatch screen (when user clicks "Dispatch" in the left sidebar).

Page title: "Export Dispatch"
Subtitle: "Manage export shipments and lot assignments"

Layout: Full-width content area (no sidebar split needed).

Show two sections stacked vertically:

Section 1 (top): A statistics bar with 3 cards in a row:
- "Total Dispatches": 8
- "Pending": 2 (amber number)
- "Dispatched": 6 (green number)

Section 2 (below): 
- Row header: "Dispatch Records" on the left
- On the right: "+ New Dispatch" button (sky-blue, solid, with plus icon)
- Below header: a filter row with search input + status dropdown
- Below filter: a data table

The table should be empty for now (just the header row).
Table columns: Dispatch ID | Buyer | Destination | Lots | Date | Status | Actions

Use the same visual language as the rest of NusaQC.
```

---

### DISPATCH SCREEN — Prompt D2: Dispatch Records Table

```
On the Dispatch screen, populate the dispatch records table with 8 rows.

Table columns: Dispatch ID | Buyer | Destination | Lots | Dispatch Date | Status | Actions

Sample data:
Row 1: DISP-2026-0730-008 | PT Rahayu Seafood | 🇺🇸 USA | 5 lots | 2026-07-30 14:00 | Dispatched (green badge) | [View]
Row 2: DISP-2026-0730-007 | Seatrade Japan Co. | 🇯🇵 Japan | 3 lots | 2026-07-30 11:30 | Dispatched (green badge) | [View]
Row 3: DISP-2026-0730-006 | PT Mina Bahari | 🇨🇳 China | 8 lots | 2026-07-29 09:00 | Dispatched (green badge) | [View]
Row 4: DISP-2026-0730-005 | Ocean Fresh EU | 🇪🇺 EU | 4 lots | 2026-07-29 08:00 | Dispatched (green badge) | [View]
Row 5: DISP-2026-0730-004 | PT Mina Bahari | 🇨🇳 China | 6 lots | 2026-07-28 14:00 | Dispatched (green badge) | [View]
Row 6: DISP-2026-0730-003 | PT Rahayu Seafood | 🇺🇸 USA | 3 lots | 2026-07-28 10:00 | Dispatched (green badge) | [View]
Row 7: DISP-2026-0730-002 | Seatrade Japan Co. | 🇯🇵 Japan | 7 lots | 2026-08-01 06:00 | Pending (amber badge) | [View] [Edit]
Row 8: DISP-2026-0730-001 | PT Nusantara Fish | 🇺🇸 USA | 4 lots | 2026-08-02 08:00 | Pending (amber badge) | [View] [Edit]

Status badges:
- "Dispatched": green background (#DCFCE7), green text
- "Pending": amber background (#FEF3C7), amber text

Pending rows have both [View] and [Edit] action buttons.
Dispatched rows have only [View] action button.
```

---

### DISPATCH SCREEN — Prompt D3: New Dispatch Modal

```
On the Dispatch screen, show the state when user clicks "+ New Dispatch".

Display a centered modal overlay (white, 620px wide, rounded corners, shadow).

Modal header: "Create New Dispatch" with × close button.

The modal form has these fields in order:

Section 1 — Shipment Info (two columns):
Left: "Buyer / Company Name" text input — placeholder "PT Rahayu Seafood"
Right: "Destination Country" dropdown — options: USA, Japan, China, EU, South Korea, Others

Left: "Container Number" text input — placeholder "CONT-2026-001 (optional)"
Right: "Dispatch Date" date-time picker

"Inspector Notes" textarea — placeholder "Optional notes about this shipment"

Section 2 — Select Lots (below, full width):
Title: "Select Lots from Storage" with a small info icon
Subtitle: "Only stored lots that haven't been dispatched are shown"

Show a compact table/list of 5 available lots:
Each row has: checkbox | Lot ID (monospace) | Fish Family | Grade badge | Confidence | Stored Since
Row 1: ☑ LOT-2026-0730-008 | Cichlidae | A | 88.3% | 2 hrs ago
Row 2: ☑ LOT-2026-0730-007 | Scombridae | B | 74.1% | 3 hrs ago
Row 3: ☐ LOT-2026-0730-006 | Scombridae | A | 91.7% | 4 hrs ago
Row 4: ☐ LOT-2026-0729-105 | Cichlidae | A | 86.2% | 1 day ago
Row 5: ☐ LOT-2026-0729-104 | Scombridae | B | 71.8% | 1 day ago

At the bottom: "2 lots selected"

Modal footer (two buttons right-aligned):
- "Cancel" button (outline, gray)
- "Create Dispatch" button (sky-blue, solid)
```

---

### DISPATCH SCREEN — Prompt D4: Dispatch Detail View

```
On the Dispatch screen, show the Dispatch Detail screen when user clicks 
[View] on a dispatch record.

Show a back button: "← Back to Dispatch"
Page title: "DISP-2026-0730-007" in monospace font
Subtitle: "Seatrade Japan Co. — 🇯🇵 Japan"

Layout: Two columns.

Left column (60%): Lot Details Table
Title: "Lots in This Shipment (3 lots)"
A table with columns: Lot ID | Fish Family | Grade | Defects | Confidence | Inspection Date
Row 1: LOT-2026-0730-005 | Scombridae | A (green) | 0 defects | 92.1% | 2026-07-30 10:38
Row 2: LOT-2026-0730-004 | Scombridae | A (green) | 0 defects | 94.8% | 2026-07-30 10:31
Row 3: LOT-2026-0730-003 | Cichlidae | B (amber) | 1 defect | 87.4% | 2026-07-30 10:24

Below table: "All 3 lots passed QC inspection" in green text with checkmark.

Right column (40%): Shipment Summary card
Title: "Shipment Summary"
Rows:
- Dispatch ID: DISP-2026-0730-007 (monospace)
- Status: Dispatched (green badge)
- Buyer: Seatrade Japan Co.
- Destination: Japan 🇯🇵
- Container: CONT-2026-007
- Dispatch Date: 2026-07-30 11:30

Divider line, then QC Summary:
- Total Lots: 3
- All Grade A/B: ✓ Yes (green)
- Avg Confidence: 91.4%
- Defects Found: 1 (amber)

Two action buttons:
- "Mark as Dispatched" (sky-blue, solid) — if status is Pending
- "Export Summary" (outline, gray, download icon) — disabled with tooltip 
  "Available in Final version"
```

---

### DISPATCH SCREEN — Prompt D5: Filter & Search

```
On the Dispatch screen, update the filter row above the table.

Show these filter controls in a single row:
- Search input (30% width): placeholder "Search by Dispatch ID or Buyer..."
- Dropdown: "All Destinations" (USA, Japan, China, EU, South Korea)
- Dropdown: "All Status" (Pending, Dispatched)
- Date range: "From" and "To" date inputs

Far right:
- "Export CSV" button with download icon (outline, sky-blue)
- "Clear Filters" text link (gray)

Below the filter row, add a summary line:
"Showing 8 dispatches — 5 lots dispatched to USA | 
 3 lots to Japan | 8 lots to China"

Style: small text, slate-500 color, thin bottom border.
Do not change the table.
```

---

## 🔧 BAGIAN 6 — INTEGRASI KE BACKEND (Ringkasan untuk T2)

### Endpoint Summary Kedua Fitur

```python
# routes/storage.py
GET  /api/v1/storage/slots           → list semua slot
GET  /api/v1/storage/pending         → lot PASS tanpa slot
POST /api/v1/storage/assign          → assign lot ke slot
     body: { "slot_id": "C-09", "lot_id": "LOT-2026-0730-008" }
DELETE /api/v1/storage/slots/{slot_id} → kosongkan slot

# routes/dispatch.py
GET  /api/v1/dispatch                → list semua dispatch
GET  /api/v1/dispatch/{id}           → detail + lot list
GET  /api/v1/dispatch/available-lots → stored lots belum dispatch
POST /api/v1/dispatch                → buat dispatch baru
     body: { buyer_name, destination, container_no,
             dispatch_date, lot_ids: [], notes }
PATCH /api/v1/dispatch/{id}/status  → update status
```

### Mock Data untuk Mock Mode

Karena kedua fitur ini bergantung pada data dari Inspection + Storage,
mock mode harus menyediakan seed data:

```python
# scripts/seed_mock_data.py
MOCK_SLOTS = [
    {"slot_id": "C-01", "zone": "cold", "lot_id": "LOT-2026-0730-001", ...},
    {"slot_id": "C-02", "zone": "cold", "lot_id": None, ...},
    # ... dst 30 slots total
]

MOCK_DISPATCHES = [
    {"dispatch_id": "DISP-2026-0730-007", "buyer_name": "Seatrade Japan", ...},
    # ... 8 dispatches
]
```

---

## ✅ BAGIAN 7 — CHECKLIST SEBELUM IMPLEMENTASI

### Validasi Scope vs Rulebook

| Feature | Ketentuan Rulebook | Status |
|---------|-------------------|--------|
| Storage grid | FE: UI hanya untuk alur interaksi inti | ✅ Assign lot = core workflow |
| Storage: IoT sensors | BE: tidak perlu background jobs | ✅ Tidak ada di MVP |
| Dispatch form | FE: tidak perlu fitur kompleks | ✅ Form sederhana |
| Dispatch: PDF export | AI: tidak perlu bulk processing | ✅ Disabled di MVP, planned Final |
| Storage SQLite | BE: tidak perlu distributed DB | ✅ SQLite lokal |
| Dispatch CSV export | BE: sync endpoint | ✅ Sync query ke SQLite |
| Mock mode | Must work without hardware | ✅ Seed data tersedia |

### Navbar Update Checklist
```
□ Tambah "Lot Storage" menu item di sidebar
□ Tambah "Dispatch" menu item di sidebar
□ Route React: /storage dan /dispatch
□ Update docker-compose jika ada volume baru
□ Update README.md: tambah deskripsi 2 fitur baru
□ Update API_CONTRACT.md: tambah endpoint baru
□ Seed script tersedia untuk mock data
```

---

## 💡 BAGIAN 8 — NILAI TAMBAH DI PROPOSAL

Tambahkan 2 kalimat ini di Bab 1.3 (Tujuan dan Manfaat) proposal:

> *"NusaQC tidak hanya menginspeksi ikan, tetapi menyediakan digital traceability chain yang lengkap: dari inspeksi mutu (Inspection), penempatan di cold storage (Lot Storage Map), hingga pencatatan pengiriman ekspor (Export Dispatch). Setiap lot ikan terlacak secara digital mulai dari conveyor belt hingga kontainer ekspor — sebuah kemampuan yang secara langsung mendukung kebutuhan audit BKIPM dan buyer internasional."*

Dan tambahkan di Mapping Smart Manufacturing table (Bab 1.2):

| Komponen | Implementasi di NusaQC | Status |
|----------|----------------------|--------|
| Traceability chain | Storage Map + Dispatch Record | **Ada (baru)** |
| Digital lot tracking | SQLite: inspect → store → dispatch | **Ada (baru)** |

---

*Dokumen ini adalah panduan implementasi fitur Storage dan Dispatch untuk NusaQC MVP*
*Dibuat: Agustus 2026 | Untuk: AIC COMPFEST 18 2026*
