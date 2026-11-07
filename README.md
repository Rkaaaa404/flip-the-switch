# Flip the Switch — NusaQC Delivery Traceability

Welcome to the workspace for the **Flip the Switch** hackathon project, enhancing **NusaQC** with verifiable incoming delivery inspection, material transformation lineage, and immutable quality records.

---

## Workspace Navigation Map

```text
flip-the-switch/
├── README.md                      # This workspace roadmap
├── docs/
│   ├── designs/                   # Active technical design documents & specifications
│   │   └── nusaqc_delivery_traceability.md
│   ├── reviews/                   # Stage 5–9 EGM review reports & remediation roadmap
│   │   ├── consolidated_review_report.md     # Consolidated synthesis & verified remediation plan
│   │   ├── zoom_out_report.md                # Stage 5: Initial Zoom-Out & Inventive Catalyst
│   │   ├── comprehension_report.md           # Stage 6: Document Comprehension Audit
│   │   ├── critic_report.md                  # Stage 7: Feature Spec Critic Review (Design/Struct/Style)
│   │   ├── intermediate_zoom_out_report.md   # Stage 8: Intermediate Zoom-Out & De-bloat
│   │   └── implementation_readiness_report.md# Stage 9: Implementation Readiness & Codebase Audit
│   ├── ideation/                  # Hackathon problem context, candidate ideas & briefing
│   │   ├── briefing-tim.md                   # Team competition intro & timeline
│   │   ├── competition-ideation.md           # Hackathon rules & requirements
│   │   ├── idea-ranking.md                   # Multi-criteria idea comparison
│   │   ├── recall-room.md                    # Early incident response concept
│   │   ├── deadline-rescue.md                # Scope risk mitigation notes
│   │   ├── concepts_brief.md                 # Concept brief for incoming delivery QC
│   │   └── design_draft.md                   # Initial architectural draft
│   ├── references/                # Pitch deck and proposal context documents
│   │   ├── nusaqc-pitchdeck.pdf              # Verified system benchmark & pitch deck
│   │   └── nusaqc-proposal.pdf               # Original innovation proposal & BOM
│   └── archive/                   # Archived background & past competition artifacts
│       ├── legacy-nusaqc/                    # Historical proposals, plans, and research
│       ├── past-comp-idea/                   # Prior competition baseline documents
│       └── other-idea/                       # Candidate concepts evaluated during intake
└── code/
    ├── webdev/                    # Core web application repository (Git: Rkaaaa404/flip-the-switch)
    │   ├── backend/               # FastAPI backend, SQLite persistence, AI engine & controllers
    │   ├── frontend/              # Next.js React dashboard, QC review workspaces, Tailwind UI
    │   └── docker-compose.yml     # Container orchestration for backend & frontend
    ├── edge/                      # Raspberry Pi edge runtime, GPIO drivers & camera server
    └── models/                    # Vision model weights (ONNX), quantization & datasets
```

---

## Core Application Codebase (`code/webdev/`)

The primary software application is located in `code/webdev/` and tracked under GitHub repository [`Rkaaaa404/flip-the-switch`](https://github.com/Rkaaaa404/flip-the-switch) (private).

### Backend (`code/webdev/backend/`)
* **Framework**: FastAPI (Python 3.11+) with SQLAlchemy ORM and SQLite persistence (`nusaqc.db`).
* **AI Engine**: Local ONNX Runtime executing MobileNetV3 (eye/gill freshness) and YOLOv8s (surface defects).
* **Hardware Controller**: Dual-mode controller supporting physical Raspberry Pi GPIO relays and simulation mock mode (`ENABLE_MOCK_HARDWARE=true`).
* **Startup Auto-Migration**: `init_db()` in `app.core.database` dynamically inspects metadata and creates/migrates SQLite tables on startup.

### Frontend (`code/webdev/frontend/`)
* **Framework**: Next.js 15 (App Router, React 19) with Tailwind CSS, Lucide icons, and Shadcn UI components.
* **Key Workspaces**: Receiving dock intake, inspection sequences, lot history, cold storage slots, and export dispatch workflows.

---

## Quickstart

### Running Backend (Local Python / UV)
```bash
cd code/webdev/backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running Frontend (Local Node.js / PNPM)
```bash
cd code/webdev/frontend
pnpm install
pnpm run dev
```

### Running via Docker Compose
```bash
cd code/webdev
docker compose up --build
```
* Backend API: `http://localhost:8000` (Docs at `http://localhost:8000/docs`)
* Frontend Dashboard: `http://localhost:3000`
