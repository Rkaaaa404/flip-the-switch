# NusaQC Web App: Backend and Dashboard

The NusaQC application behind the Receiving QC Room: a FastAPI backend that runs both vision models and keeps the QC records, and a Next.js dashboard. For the Switch room itself, setup and the demo, start with the [main README](../../README.md).

NusaQC was built before the hackathon as a visual QC and sorting system for Indonesian export fish processing plants. It grades freshness against SNI 2729:2013, detects visible surface defects, drives the conveyor's lights and relay, and records each lot from inspection to export manifest. During the hackathon we added **delivery traceability** (two-view conveyor capture, dispositions, movements, mass balance and lineage) and the **Switch room** write path.

## Architecture

```text
conveyor ── sensor trigger ── camera (dorsal + ventral views)
                                   │
┌──────────────────────────────────┼───────────────────────────────────┐
│ FastAPI backend                  ▼                                   │
│   Model 1: freshness (MobileNetV3-Small, ONNX) ──> grade A / B / C   │
│   Model 2: defects (YOLOv8s, ONNX)             ──> boxes + classes   │
│                     │                                                │
│        decision engine (grade + defects + threshold)                 │
│          │                    │                    │                 │
│   hardware controller   SQLite records       Switch room API         │
│   GREEN / YELLOW / RED  lots, deliveries,    proposals (agent token) │
│   (GPIO or mock)        dispositions,        gate commands           │
│                         movements, lineage   (gate token only)       │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                     Next.js dashboard (read-only for decisions)
```

### Models

| | Model 1: freshness | Model 2: surface defects |
|---|---|---|
| Architecture | MobileNetV3-Small | YOLOv8s |
| Input | 224 × 224 | 640 × 640, letterboxed |
| Output | Grade A (prime), B (fresh), C (reject) | Boxes for `sisik_sisa`, `warna_abnormal`, `luka_robekan`, `lendir_berlebih` (shown as scale damage, red lesion, open wound, excess mucus) |
| Host CPU latency (measured) | 5.39 ms | 255 ms FP32 |
| Details | [`code/models/model_1`](../models/model_1/README.md) | [`code/models/model_2`](../models/model_2/README.md) |

Measured accuracy and the known weaknesses are in [`eval/BASELINE_EVALUATION_REPORT.md`](eval/BASELINE_EVALUATION_REPORT.md).

### Decision engine (single-snapshot inspection)

`backend/app/services/decision_engine.py`:

| Decision | Signal | When | Action |
|---|---|---|---|
| **PASS** | GREEN | Grade A, or Grade B at or above the confidence threshold, with no defect at or above the threshold | Belt runs, lot queues for storage |
| **CONDITIONAL** | YELLOW | Grade B below the threshold, no defect | Operator checks visually |
| **FAIL** | RED | Grade C, or at least one defect at or above the threshold | Relay stops the belt, alarm on, lot marked reject |

### Delivery traceability (built during the hackathon)

- **Two-view capture.** Each fish is photographed from above (dorsal) and below (ventral). Views are paired by expected transit time. A fish with one view is kept and flagged `missing_ventral_view` or `missing_dorsal_view`, never silently dropped.
- **Dispositions.** Accept, reject, reprocess or downgrade a quantity of a delivery into a lot. The quantity rules stop a delivery from being over-dispositioned.
- **Movements.** Receiving to processing, WGGS and other steps, each with a mass balance: in = out + normal yield loss + QC rejects, and any unexplained variance is recorded, not hidden.
- **Lineage and trace.** Any lot walks back to its delivery and truck, and every gap is listed.
- **Switch write path.** Dispositions and movements are only recorded through `/switchroom/gate/commands`, called by `qc-gate` with the sender id Switch verified. The old write routes return 403 to anything except the gate token. See the main README.

Design: [`docs/designs/nusaqc_delivery_traceability.md`](../../docs/designs/nusaqc_delivery_traceability.md).

### Hardware: real or mock

`backend/app/hardware/` drives the conveyor.

- `ENABLE_MOCK_HARDWARE=false`: Raspberry Pi 5 with `RPi.GPIO`, a 24 V DC conveyor relay, a three-color stack light and a buzzer.
- `ENABLE_MOCK_HARDWARE=true` (the default): runs on any laptop and logs each signal instead.

  ```text
  [MOCK HARDWARE] [SIGNAL: GREEN] Conveyor Normal Speed | Tower: GREEN | Buzzer: OFF
  [MOCK HARDWARE] [SIGNAL: RED] RELAY CUT-OFF -> Conveyor STOPPED | Tower: RED | Siren: ACTIVE
  ```

## Run it

**With Docker** (backend and dashboard only, mock hardware):

```bash
cd code/webdev
docker compose up --build
```

The dashboard is at http://localhost:3000, the API docs at http://localhost:8000/docs and the health check at http://localhost:8000/health. Compose doesn't set `QC_AGENT_TOKEN` or `QC_GATE_TOKEN`, so the Switch routes stay locked; use the manual setup below for the full room.

**Manually:**

```bash
# backend
cd code/webdev/backend
cp .env.example .env          # set QC_AGENT_TOKEN and QC_GATE_TOKEN for the Switch room
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000

# demo data: 5 fish through the real two-view pipeline and models
uv run python scripts/seed_demo.py --bridge <Switch bridge id>

# tests
uv run pytest

# dashboard (new terminal)
cd code/webdev/frontend
pnpm install && pnpm dev
```

## API

All routes are under `/api/v1` and documented live at http://localhost:8000/docs.

**Deliveries and traceability** (`deliveries.py`)

| Method | Path | What |
|---|---|---|
| `POST` / `GET` | `/deliveries` | Create or list deliveries |
| `GET` | `/deliveries/{id}` | Delivery detail: views, fish, dispositions, movements, balance |
| `PATCH` | `/deliveries/{id}/status` | Update the delivery status |
| `POST` | `/deliveries/{id}/capture-view` | Upload one dorsal or ventral view; runs both models |
| `POST` | `/deliveries/{id}/dispositions`, `/movements` | Write routes, **gate token only** |
| `GET` | `/deliveries/{id}/trace` | Trace tree from the delivery to its lots |
| `GET` | `/deliveries/lots/{lot_id}/provenance` | Walk a lot back upstream |
| `POST` | `/deliveries/{id}/simulate` | Mock conveyor run |

**Switch room** (`switchroom.py`)

| Method | Path | Token | What |
|---|---|---|---|
| `POST` | `/switchroom/proposals` | agent | qc-agent drafts a disposition or movement (`DP-n`, `MV-n`), validated but not recorded |
| `GET` | `/switchroom/proposals`, `/proposals/{id}` | none | Read drafts and their status |
| `POST` | `/switchroom/gate/commands` | gate | Apply `approve`, `reject`, `confirm` or `status` from a Switch-verified sender, return the receipt |
| `PUT` | `/switchroom/identities` | gate | Map a Switch sender id to a plant role (setup) |
| `GET` | `/switchroom/views/{view_id}/annotated.jpg` | none | The inspection photo with the model's boxes drawn on |

**Earlier NusaQC routes**

| Area | Routes |
|---|---|
| Inspections | `POST /inspections/run` (multipart `image`, `family`) |
| Lots | `GET /lots`, `/lots/recent`, `/lots/{lot_id}`, `/lots/export/csv`; `PATCH /lots/{lot_id}/note`, `/lots/{lot_id}/override`; `DELETE /lots/{lot_id}` |
| Storage | `GET /storage/slots`, `/storage/pending`; `POST /storage/assign`; `DELETE /storage/slots/{slot_id}` |
| Dispatch | `GET /dispatch`, `/dispatch/available-lots`, `/dispatch/{id}`, `/dispatch/{id}/export`; `POST /dispatch`; `PATCH /dispatch/{id}/status` |
| Dashboard, hardware, settings | `GET /dashboard/stats`, `GET /hardware/status`, `POST /hardware/test-connection`, `GET /settings/models/status`, `GET` / `PUT /settings` |
| Events | WebSocket `/ws/events` |

## Layout

```text
code/webdev/
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── ai/            # ONNX inference and preprocessing
│   │   ├── api/v1/        # routers (above); api/auth.py checks the agent and gate tokens
│   │   ├── core/          # SQLite and WebSocket manager
│   │   ├── hardware/      # GPIO, dual-conveyor and mock controllers
│   │   ├── models/        # SQLAlchemy tables: inspections, storage, dispatch, delivery_trace, switchroom
│   │   ├── schemas/       # Pydantic request and response models
│   │   └── services/      # decision engine, two-view inspection, lineage, switchroom
│   ├── models_weights/    # ONNX weights
│   ├── scripts/seed_demo.py
│   └── tests/             # traceability, lineage and Switch room tests
├── frontend/              # Next.js dashboard, see frontend/README.md
└── eval/                  # model evaluation suite and baseline report
```

## Team

Team 4 IT Goes International:

- Rayka Dharma Pranandita
- Naufal Ardhana
- Evan Christian Nainggolan
- Rayhan Agnan Kusuma
