# NusaQC Frontend

The NusaQC operator dashboard: Next.js 16, React 19 and Tailwind CSS v4. For decisions it is **read-only**. Dispositions and movements are signed in the Switch room, and this UI shows the pending drafts with their sign command and badges every record **Signed in Switch**.

## Run it

Needs Node.js 20+ and pnpm 10+, and the backend running on `http://localhost:8000`.

```bash
cd code/webdev/frontend
cp .env.example .env.local   # NEXT_PUBLIC_API_URL and NEXT_PUBLIC_WS_URL
pnpm install
pnpm dev                     # http://localhost:3000
```

## Pages

| URL | Page | What it shows |
|---|---|---|
| `/deliveries` | Deliveries | Incoming deliveries and their inspection status |
| `/deliveries/[id]` | Delivery workspace | Two-view inspection results, flagged fish, mass balance, pending Switch drafts with their `@qc-gate` command, signed dispositions and movements |
| `/deliveries/[id]/trace` | Trace | Lineage from the delivery to every lot, with the signer of each step and any gaps |
| `/` | Dashboard | Daily stats and recent inspections |
| `/inspection` | Inspection | Single-snapshot inspection with live model output and boxes |
| `/history`, `/history/[lotId]` | Lot history | Past inspections, filters, CSV export, per-lot detail |
| `/storage` | Storage map | Cold and frozen zone slots |
| `/dispatch`, `/dispatch/[dispatchId]` | Export dispatch | Shipment manifests built from stored lots |
| `/settings` | Settings | Thresholds, hardware and model status |

The delivery pages were built during the hackathon. The others come from the earlier NusaQC app.

## Layout

```text
frontend/
├── app/            # App Router pages (above)
├── components/
│   ├── ui/         # primitives (button, input, switch)
│   ├── common/     # shared business components (status badges, spinners)
│   ├── layout/     # sidebar, top bar
│   └── sections/   # per-page sections
├── lib/            # API client, WebSocket helper, utils
└── types/index.ts  # data contracts; field names match the backend's JSON
```

## Stack

Next.js 16.3, React 19.2, Tailwind CSS 4, Radix UI, Lucide icons, TanStack Query 5, Axios, TypeScript 5.

`AGENTS.md` and `CLAUDE.md` in this folder are written by `next dev` for coding agents.
