> [!WARNING]
> **README INI BERSIFAT SEMENTARA — KHUSUS UNTUK TIM INTERNAL (Backend & AI)**
> Dokumen ini dibuat untuk membantu tim bekerja secara paralel sebelum MVP selesai.
> README ini **belum dioptimasi untuk juri**. Revisi final akan dilakukan setelah seluruh fitur MVP (frontend + backend + AI) selesai diintegrasikan.

---

# NusaQC — Frontend

**AI-Powered Visual Quality Control System for Fish Processing Units**

Frontend ini dibangun menggunakan **Next.js 16** dengan React 19 dan Tailwind CSS v4.
Berjalan sebagai bagian dari arsitektur **monorepo** `nusaqc/`.

---

## Prasyarat

Pastikan sudah terinstall di komputermu:
- **Node.js** >= 20
- **pnpm** >= 10

---

## Setup & Menjalankan Lokal

```bash
# 1. Masuk ke folder frontend
cd frontend

# 2. Copy file environment
cp .env.example .env.local

# 3. Install dependencies
pnpm install

# 4. Jalankan development server
pnpm dev
```

Frontend berjalan di: **http://localhost:3000**
Backend (FastAPI) harus berjalan di: **http://localhost:8000**

> Pastikan backend sudah berjalan sebelum membuka halaman yang membutuhkan data dari API.

---

## Konfigurasi Environment (`.env.local`)

Setelah meng-copy `.env.example` ke `.env.local`, pastikan isinya sesuai:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

Ubah URL jika backend berjalan di port yang berbeda.

---

## Peta Halaman (Routing)

| URL | Halaman | Deskripsi |
|---|---|---|
| `/` | Dashboard | Ringkasan statistik harian & riwayat inspeksi terbaru |
| `/inspection` | Inspection | Panel kamera + trigger AI + hasil grade real-time |
| `/history` | Lot History | Tabel seluruh riwayat inspeksi dengan filter & search |
| `/history/[lotId]` | Detail Lot | Detail lengkap satu sesi inspeksi (untuk audit) |
| `/settings` | Settings | Konfigurasi hardware, model AI, dan ekspor data |

---

## Struktur Folder

```
frontend/
├── app/                         # Routing (Next.js App Router)
│   ├── layout.tsx               # Shell global: Sidebar + Topbar
│   ├── page.tsx                 # URL: "/" → Dashboard
│   ├── inspection/page.tsx      # URL: "/inspection"
│   ├── history/page.tsx         # URL: "/history"
│   ├── history/[lotId]/page.tsx # URL: "/history/:lotId" (Dynamic Route)
│   └── settings/page.tsx        # URL: "/settings"
│
├── components/
│   ├── ui/                      # Komponen primitive (Button, Input, Switch)
│   ├── common/                  # Komponen reusable bisnis (StatusBadge, LoadingSpinner)
│   ├── layout/                  # Sidebar, Topbar
│   └── sections/                # Section UI per halaman
│       ├── dashboard-page/
│       ├── inspection-page/
│       ├── lot-history-page/
│       └── settings-page/
│
├── hooks/                       # Custom React hooks (untuk koneksi API)
├── types/                       # TypeScript type definitions (kontrak data)
│   └── index.ts                 # Semua types di satu tempat
└── lib/
    └── utils.ts                 # Helper function (cn, dll.)
```

---

## Kontrak API

Seluruh endpoint API yang diharapkan dari backend didokumentasikan di:
👉 `docs/COLLABORATION.md` *(di root monorepo)*

Pastikan backend mengembalikan response JSON dengan nama field yang **identik** dengan yang ada di `types/index.ts`.

---

## Tech Stack

| Teknologi | Versi | Kegunaan |
|---|---|---|
| Next.js | 16.3.0 | Framework utama |
| React | 19 | UI rendering |
| Tailwind CSS | v4 | Styling |
| Radix UI | 1.6.7 | Komponen headless |
| Lucide React | latest | Icon library |
| TanStack React Query | 5.x | Data fetching & caching |
| Axios | 1.x | HTTP client |
| TypeScript | 5 | Type safety |

---

## Conventional Commits

Semua commit **wajib** mengikuti format berikut (sesuai ketentuan rulebook COMPFEST 18):

```
feat: <deskripsi>     → penambahan fitur atau fungsionalitas baru
fix: <deskripsi>      → perbaikan bug atau kesalahan pada sistem
refactor: <deskripsi> → perubahan struktur kode yang tidak mengubah fungsionalitas
docs: <deskripsi>     → perubahan dokumentasi saja
chore: <deskripsi>    → perubahan konfigurasi, setup, dependencies
```

Referensi: https://www.conventionalcommits.org
