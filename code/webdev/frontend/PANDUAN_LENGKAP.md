# PANDUAN LENGKAP — NusaQC Frontend: Dari Kondisi Sekarang ke GitHub Push

> Dibuat: 2026-08-07  
> Tujuan: Panduan bertahap untuk menyelesaikan setup frontend agar bisa di-push ke GitHub dan backend bisa langsung bekerja paralel.

---

## Daftar Isi

1. [Kondisi Saat Ini (Audit)](#1-kondisi-saat-ini-audit)
2. [Fase 1 — Perbaiki `app/layout.tsx` (Global Shell)](#2-fase-1--perbaiki-applayout-tsx-global-shell)
3. [Fase 2 — Buat Struktur Routing (Folder & File `page.tsx`)](#3-fase-2--buat-struktur-routing-folder--file-pagetsx)
4. [Fase 3 — Bersihkan `app/page.tsx` (Dashboard)](#4-fase-3--bersihkan-apppagetsx-dashboard)
5. [Fase 4 — Buat Page Skeleton untuk Setiap Halaman](#5-fase-4--buat-page-skeleton-untuk-setiap-halaman)
6. [Fase 5 — Setup Environment & Koneksi API](#6-fase-5--setup-environment--koneksi-api)
7. [Fase 6 — Siapkan `.gitignore` & File Dokumentasi](#7-fase-6--siapkan-gitignore--file-dokumentasi)
8. [Fase 7 — Push ke GitHub](#8-fase-7--push-ke-github)
9. [Wawasan Industri: Mengapa Urutan Ini Penting?](#9-wawasan-industri-mengapa-urutan-ini-penting)

---

## 1. Kondisi Saat Ini (Audit)

### ✅ Yang Sudah Ada & Baik
| File/Folder | Status |
|---|---|
| `components/ui/Button.tsx` | ✅ Selesai |
| `components/ui/Switch.tsx` | ✅ Selesai |
| `components/ui/Input.tsx` | ⚠️ Ada tapi kosong |
| `components/common/StatusBadge.tsx` | ✅ Ada (belum pakai props) |
| `components/common/LoadingSpinner.tsx` | ✅ Selesai |
| `components/common/EmptyState.tsx` | ⚠️ Ada tapi kosong |
| `components/layout/Sidebar.tsx` | ✅ Selesai |
| `components/layout/Topbar.tsx` | ⚠️ Ada tapi kosong |
| `components/sections/dashboard-page/` | ⚠️ Ada 2 file, belum berisi kode |
| `components/sections/inspection-page/` | ⚠️ Ada 2 file, belum berisi kode |
| `components/sections/lot-history-page/` | ⚠️ Ada 2 file, belum berisi kode |
| `components/sections/settings-page/` | ⚠️ Ada 4 file, belum berisi kode |
| `lib/utils.ts` | ✅ Selesai |
| `app/layout.tsx` | ❌ Perlu diperbaiki (Sidebar belum di sini) |
| `app/page.tsx` | ❌ Perlu dibersihkan (isi testing sementara) |

### ❌ Yang Belum Ada (Perlu Dibuat)
| File/Folder | Prioritas |
|---|---|
| `app/inspection/page.tsx` | TINGGI |
| `app/history/page.tsx` | TINGGI |
| `app/history/[lotId]/page.tsx` | TINGGI |
| `app/settings/page.tsx` | TINGGI |
| `.env.local` | TINGGI |
| `.env.example` | TINGGI |
| `hooks/` folder | SEDANG |
| `types/index.ts` | SEDANG |

---

## 2. Fase 1 — Perbaiki `app/layout.tsx` (Global Shell)

**Mengapa ini paling pertama?**

`app/layout.tsx` adalah *shell* (cangkang) yang membungkus **semua** halaman. Apapun yang ditaruh di sini akan muncul di setiap halaman tanpa harus copy-paste ke setiap `page.tsx`. Sidebar harus dipindahkan ke sini.

> **Konsep:** Di Next.js App Router, `layout.tsx` bersifat *nested*. `app/layout.tsx` menyelubungi SEMUA halaman. Ini berbeda dari `page.tsx` yang hanya berlaku untuk satu URL spesifik.

**Ubah `app/layout.tsx` menjadi:**

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "NusaQC — Fish Quality Control AI",
  description: "AI-powered visual quality control system for fish processing units.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" className={`${inter.variable} h-full antialiased`}>
      <body className="min-h-screen flex flex-row bg-zinc-50">
        {/* Sidebar muncul di SEMUA halaman */}
        <Sidebar />

        {/* Area konten utama */}
        <main className="flex-1 flex flex-col overflow-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
```

> **Kenapa ganti `Geist` ke `Inter`?**  
> `Inter` adalah font standar industri yang juga dipakai Vercel, Linear, dan Shadcn. Kamu sudah menulis `font-['Inter']` di Sidebar, jadi ini menyambungkan font ke seluruh aplikasi secara konsisten.

---

## 3. Fase 2 — Buat Struktur Routing (Folder & File `page.tsx`)

**Aturan dasar Next.js App Router:**
- Folder = URL segment
- File `page.tsx` di dalam folder = Halaman yang bisa dikunjungi
- Folder tanpa `page.tsx` = Folder biasa (tidak bisa diakses via URL)

**Buat folder dan file berikut:**

```
app/
├── inspection/
│   └── page.tsx
├── history/
│   ├── page.tsx
│   └── [lotId]/          ← NAMA FOLDER HARUS PAKAI KURUNG SIKU (sintaks Next.js)
│       └── page.tsx
└── settings/
    └── page.tsx
```

**Isi sementara untuk setiap `page.tsx` baru:**

```tsx
// app/inspection/page.tsx
export default function InspectionPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Inspection</h1>
      <p className="text-gray-500 mt-2">Halaman ini sedang dalam pengerjaan.</p>
    </div>
  );
}
```

Gunakan pola yang sama untuk `history/page.tsx`, `history/[lotId]/page.tsx`, dan `settings/page.tsx`.

> **Mengapa buat placeholder dulu?** Pendekatan ini disebut **"route-first development"**. Kamu mendefinisikan semua URL terlebih dahulu sehingga: navigasi di Sidebar bisa langsung diuji, backend tahu URL apa yang ada, dan tim bisa kerja paralel tanpa saling menunggu.

---

## 4. Fase 3 — Bersihkan `app/page.tsx` (Dashboard)

Hapus semua import komponen testing dan ganti dengan struktur yang rapi:

```tsx
// app/page.tsx
import { HeadSection } from "@/components/sections/dashboard-page/HeadSection";
import { BodySection } from "@/components/sections/dashboard-page/BodySection";

export default function DashboardPage() {
  return (
    <div className="flex flex-col flex-1 p-8 gap-6">
      <HeadSection />
      <BodySection />
    </div>
  );
}
```

> **Prinsip:** File `page.tsx` tidak boleh berisi kode UI yang kompleks. Tugasnya hanya **mengumpulkan dan mengatur posisi** komponen section. Kode UI sesungguhnya ada di dalam file section masing-masing. Ini disebut prinsip **Single Responsibility**.

---

## 5. Fase 4 — Buat Page Skeleton untuk Setiap Halaman

Setiap `page.tsx` hanya mengimpor section. Contoh untuk `/inspection`:

```tsx
// app/inspection/page.tsx
import { FishInspection } from "@/components/sections/inspection-page/FishInspection";
import { ResultSection } from "@/components/sections/inspection-page/ResultSection";

export default function InspectionPage() {
  return (
    <div className="flex flex-row flex-1 gap-6 p-8">
      <FishInspection />
      <ResultSection />
    </div>
  );
}
```

Lakukan hal yang sama untuk `/history`, `/history/[lotId]`, dan `/settings`.

> **Tentang `/history/[lotId]/page.tsx`:** Next.js akan otomatis mengekstrak nilai dari URL. Jika user mengunjungi `/history/LOT-2026-0807-003`, maka nilai `LOT-2026-0807-003` bisa dibaca menggunakan props `params`:

```tsx
// app/history/[lotId]/page.tsx
type PageProps = {
  params: Promise<{ lotId: string }>;
};

export default async function LotDetailPage({ params }: PageProps) {
  const { lotId } = await params;
  // lotId = "LOT-2026-0807-003" (diambil otomatis dari URL)

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Detail Lot: {lotId}</h1>
    </div>
  );
}
```

---

## 6. Fase 5 — Setup Environment & Koneksi API

### 6.1 Buat `.env.local` (JANGAN di-commit ke Git)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 6.2 Buat `.env.example` (HARUS di-commit ke Git sebagai template)

```env
# URL Backend API (FastAPI)
NEXT_PUBLIC_API_URL=http://localhost:8000

# URL WebSocket Backend
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

> **Aturan penamaan di Next.js:**  
> `NEXT_PUBLIC_` = bisa dibaca di browser (client-side).  
> Tanpa prefix = hanya bisa dibaca di server (untuk API keys/secrets yang rahasia).  
> Karena URL backend tidak rahasia, kita pakai `NEXT_PUBLIC_`.

### 6.3 Install Dependencies Koneksi API

```bash
pnpm add @tanstack/react-query axios
```

### 6.4 Buat Folder `types/` dengan file `types/index.ts`

```typescript
// types/index.ts

export type Decision = "PASS" | "FAIL" | "CONDITIONAL";
export type HardwareSignal = "GREEN" | "YELLOW" | "RED";
export type Grade = "A" | "B" | "C";

export type Defect = {
  label: "sisik_sisa" | "warna_abnormal" | "luka_robekan" | "foreign_object" | "lendir_berlebih";
  bbox: [number, number, number, number]; // [x1, y1, x2, y2]
  confidence: number;
};

export type InspectionResult = {
  lot_id: string;
  timestamp: string; // ISO 8601
  fish_family: "Scombridae" | "Cichlidae" | "Salmonidae";
  grade: Grade;
  grade_confidence: number;
  defects: Defect[];
  decision: Decision;
  hardware_signal: HardwareSignal;
  processing_time_ms: number;
};

export type LotSummary = {
  lot_id: string;
  fish_family: string;
  grade: Grade;
  decision: Decision;
  confidence: number;
  timestamp: string;
};

export type DashboardStats = {
  total_inspected_today: number;
  current_lot_id: string;
  pass_rate: number;
  pass_rate_delta: number;
  fail_rate: number;
  fail_rate_delta: number;
  avg_confidence_score: number;
};

export type HardwareStatus = {
  camera: "ONLINE" | "OFFLINE";
  conveyor_relay: "ACTIVE" | "INACTIVE";
  tower_light: "GREEN" | "YELLOW" | "RED";
  mock_mode_enabled: boolean;
};
```

> **Mengapa types dipisah ke folder sendiri?**  
> Types ini dipakai di BANYAK tempat: komponen, hooks, dan API calls. Jika nama field berubah di masa depan, kamu hanya perlu ubah di satu tempat (`types/index.ts`) dan TypeScript akan otomatis menandai semua tempat lain yang perlu diupdate. Ini disebut prinsip **Single Source of Truth**.

---

## 7. Fase 6 — Siapkan `.gitignore` & File Dokumentasi

### 7.1 Pastikan `.gitignore` Sudah Benar

Buka `frontend/.gitignore` dan pastikan baris berikut ada:

```gitignore
# Jangan pernah commit file ini
.env.local
.env.development.local
.env.test.local
.env.production.local

node_modules/
.next/
```

### 7.2 Buat `frontend/README.md`

```markdown
# NusaQC — Frontend

## Prasyarat
- Node.js >= 20
- pnpm >= 10

## Setup

1. Copy file environment:
   cp .env.example .env.local

2. Install dependencies:
   pnpm install

3. Jalankan development server:
   pnpm dev

Frontend berjalan di: http://localhost:3000
Backend harus berjalan di: http://localhost:8000

## Struktur Folder
| Folder | Isi |
|---|---|
| `app/` | Routing pages (Next.js App Router) |
| `components/ui/` | Komponen primitive (Button, Input, Switch) |
| `components/common/` | Komponen reusable dengan konteks bisnis |
| `components/layout/` | Komponen kerangka (Sidebar, Topbar) |
| `components/sections/` | Komponen section per halaman |
| `hooks/` | Custom React hooks |
| `types/` | TypeScript type definitions |
| `lib/` | Utility functions |
```

---

## 8. Fase 7 — Push ke GitHub

```bash
# 1. Pastikan kamu di root monorepo (nusaqc/), bukan di dalam frontend/
cd ..

# 2. Cek status — pastikan .env.local TIDAK muncul di daftar ini
git status

# 3. Tambahkan semua perubahan
git add .

# 4. Commit dengan conventional commit message
git commit -m "feat(frontend): setup routing structure, layout, and component foundation"

# 5. Push
git push origin main
```

> **Wajib diingat — Conventional Commits:**
> Format: `type(scope): pesan`
> - `feat` = Fitur baru
> - `fix` = Perbaikan bug
> - `refactor` = Ubah kode tanpa tambah fitur/fix bug
> - `docs` = Perubahan dokumentasi
> - `chore` = Setup, konfigurasi, package

---

## 9. Wawasan Industri: Mengapa Urutan Ini Penting?

Di tim profesional, urutan pengerjaan ini disebut **"Outside-in Development"** (pengembangan dari luar ke dalam):

```
Level 1: Shell & Layout      → app/layout.tsx
Level 2: Routing             → app/*/page.tsx (skeleton)
Level 3: Page Assembly       → import sections di setiap page.tsx
Level 4: Section UI          → isi komponen section
Level 5: Primitive UI        → ui/Button, ui/Input
Level 6: Logic & API calls   → hooks, react-query
```

**Keuntungan konkret:**

1. **Bisa diuji lebih awal.** Navigasi antar halaman bisa diuji jauh sebelum semua komponen selesai.
2. **Kerja paralel lebih mudah.** Dua orang bisa mengerjakan level berbeda tanpa konflik file.
3. **Perubahan desain lebih murah.** Layout berubah? Hanya ubah `layout.tsx` satu file, bukan setiap halaman.
4. **Backend bisa mulai lebih awal.** Routing sudah terdefinisi, backend tahu URL dan data apa yang diperlukan.

---

## Ringkasan Cepat: Urutan Kerja

| # | Yang Dikerjakan | File Terkait |
|---|---|---|
| 1 | Perbaiki global layout | `app/layout.tsx` |
| 2 | Buat routing skeleton | `app/inspection/`, `app/history/`, `app/history/[lotId]/`, `app/settings/` |
| 3 | Bersihkan page.tsx | `app/page.tsx` |
| 4 | Buat file types | `types/index.ts` |
| 5 | Buat file environment | `.env.local`, `.env.example` |
| 6 | Install deps API | `react-query`, `axios` |
| 7 | Perbaiki .gitignore | `.gitignore` |
| 8 | Tulis README.md | `frontend/README.md` |
| 9 | Push ke GitHub | `git push` |
