# Consolidated Review & Remediation Report: NusaQC Incoming Inspection & Delivery Traceability

**Target Document**: `docs/designs/nusaqc_delivery_traceability.md`  
**Application Codebase**: `code/webdev/` (FastAPI backend + Next.js frontend)  
**Git Repository**: [`Rkaaaa404/flip-the-switch`](https://github.com/Rkaaaa404/flip-the-switch) (private)  
**Status**: **UPDATED WITH CODEBASE GROUND TRUTH — REMEDIATION ROADMAP APPROVED**  

---

## 1. Executive Summary & Codebase Ground Truth Reconciliation

Following the initial staged review (Stages 5–9), the full production application codebase was imported into `code/webdev/`. A pedantic re-audit was performed across the actual repository files.

### Critical Ground Truth Reconciliation
During Stage 9, several blocker and major findings (`S9C-01` through `S9C-06`, `S9I-01`, `S5Z-01`) flagged that the plan referenced "phantom files" and non-existent codebase components because no source tree was present in the initial workspace.

**Verification against `code/webdev/` confirms that all previously questioned base files, classes, and mechanisms exist verbatim in the repository:**
1. **Target Files to Modify**:
   * `backend/app/models/__init__.py`: **EXISTS**. Currently exports `InspectionRecord`, `SystemSetting`, `StorageSlot`, `Dispatch`, and `DispatchLot`.
   * `backend/app/api/v1/router.py`: **EXISTS**. Mounts `/inspections`, `/lots`, `/dashboard`, `/hardware`, `/storage`, `/dispatch`, and `/settings`.
   * `frontend/lib/api.ts`: **EXISTS**. Declares typed API client methods for lots, inspections, storage, and dispatch.
   * `frontend/components/layout/Sidebar.tsx`: **EXISTS**. Top-level navigation sidebar component.
2. **Existing Relational Schemas**:
   * `StorageSlot`: **EXISTS** in `backend/app/models/storage_slot.py` (table `storage_slots`, columns `slot_id`, `zone`, `lot_id`, `assigned_at`, `assigned_by`).
   * `Dispatch` & `DispatchLot`: **EXISTS** in `backend/app/models/dispatch.py` (tables `dispatches` and `dispatch_lots`).
   * `InspectionRecord`: **EXISTS** in `backend/app/models/inspection_record.py` (table `inspections`).
3. **Hardware Controllers & AI Engines**:
   * `MockHardwareController`: **EXISTS** in `backend/app/hardware/mock_controller.py`.
   * `GPIOHardwareController`: **EXISTS** in `backend/app/hardware/gpio_controller.py`.
   * `AIEngine`: **EXISTS** in `backend/app/ai/inference.py` (loads `mobilenetv3_freshness.onnx` and `nusaqc_model2_defect_detector.onnx`).
4. **Database Initialization & Auto-Migration**:
   * `init_db()`: **EXISTS** in `backend/app/core/database.py`. It inspects SQLAlchemy metadata and automatically issues `ALTER TABLE ... ADD COLUMN` statements for missing SQLite columns on startup.
5. **Project Manifests & Orchestration**:
   * `pyproject.toml`, `uv.lock`, `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`, and `frontend/package.json` are all present, configured, and operational.

---

## 2. Updated Blocker & Major Finding Status

| Priority | Finding ID | Original Finding Focus | Codebase Verification Status | Concrete Remediation Action |
|:---|:---|:---|:---:|:---|
| 🔴 **Blocker** | **BLK-01** | Missing base repository files & scaffolding (`S9C-01`, `S9I-01`) | **RESOLVED** | All target files marked `(Modify)` exist in `code/webdev/`. Edits will patch existing files directly. |
| 🔴 **Blocker** | **BLK-02** | Physical conveyor coupling & FIFO desynchronization (`S7D-01`, `S8Z-01`) | **ACTIVE** | Decouple software evidence schema from conveyor turning. Support operator-confirmed sequential mode in `dual_conveyor_controller.py` and record anomalies as explicit partial inspections without shifting sequence indexes. |
| 🔴 **Blocker** | **BLK-03** | Material allocation balance invariants across splits (`S5Z-03`, `S9I-03`) | **ACTIVE** | Implement consumption validation in `material_lineage_service.py`: `SUM(quantity_in) <= delivery.stated_quantity` across split storage and processing branches. |
| 🔴 **Blocker** | **BLK-04** | Trace gap directionality & undeclared schemas (`S6C-06`, `S9C-05`) | **REFACTORED** | Downstream schemas verified in `storage_slot.py` and `dispatch.py`. Split `/trace` into forward lineage (`/lineage`) and backward provenance (`/provenance`). |
| 🔴 **Blocker** | **BLK-05** | Omission of mandatory Risks & Mitigations section (`S7D-02`, `S7R-01`) | **ACTIVE** | Insert `## Risks & Mitigations` into `docs/designs/nusaqc_delivery_traceability.md`. |
| 🔴 **Blocker** | **BLK-06** | SQLite write concurrency & DDL execution (`S7D-05`, `S9C-04`) | **REFACTORED** | `init_db()` verified in `database.py`. Enable WAL mode (`PRAGMA journal_mode=WAL;`) and configure `timeout=30.0` in SQLAlchemy `create_engine` to handle concurrent writes. |
| 🟡 **Major** | **MAJ-01** | Attributable human decision lifecycle & supersession (`S5Z-04`, `S8Z-08`) | **ACTIVE** | Use authenticated session principals for `authorized_by`; add `supersedes_id` self-referential foreign key for corrections without event-sourcing bloat. |
| 🟡 **Major** | **MAJ-02** | Bounded capture pipeline vs CPU saturation (`S7D-04`, `S8Z-06`) | **ACTIVE** | Bound background thread execution using a worker semaphore in `two_view_inspection_service.py` to prevent thread explosions on edge hardware. |
| 🟡 **Major** | **MAJ-03** | Storage budget & configurable path (`S7D-07`, `S9C-07`) | **ACTIVE** | Use `settings.UPLOAD_DIR` rather than hardcoded `/data/captures/`; enforce pre-session disk space check. |
| 🟡 **Major** | **MAJ-04** | Dual-unit conversion policy (`S6C-07`, `S7S-05`) | **ACTIVE** | Allow explicit units (`kg` or `count`) per movement; reject automated ambiguous conversions. |
| 🟡 **Major** | **MAJ-05** | Pragmatic verification vs synthetic SLAs (`S5Z-05`, `S9S-02`) | **ACTIVE** | Calibrate test suite around functional correctness, gap detection, and balance invariants; replace arbitrary `< 1.0s` SLA assertions with deterministic assertions. |
| 🟡 **Major** | **MAJ-06** | Capture completeness vs usable model coverage (`S6C-03`, `S8Z-05`) | **ACTIVE** | Separate image persistence (`COMPLETE`) from visual model evaluation (`VALID_EVIDENCE` vs `UNSUPPORTED`). |
| 🟡 **Major** | **MAJ-07** | De-bloating and pruning speculative features (`S8Z-03`, `S8Z-04`) | **APPROVED** | Reject enterprise RBAC, station mTLS, message brokers, and M:N lot blending; keep architecture strictly local-first SQLite/FastAPI. |

---

## 3. Step-by-Step Implementation & Remediation Sequence

Execution will proceed in eight discrete phases within `code/webdev/`, committing each feature/adjustment separately:

### Phase 1: Persistence & Relational Models (`code/webdev/backend/`)
* **Create `app/models/delivery_trace.py`**:
  * `ReceivingDelivery`: table `receiving_deliveries` with primary key `DEL-YYYYMMDD-XXX`, supplier details, stated quantity, and status.
  * `FishInspection`: table `fish_inspections` with sequential counter, status (`COMPLETE`, `PARTIAL_DORSAL_ONLY`, `PARTIAL_VENTRAL_ONLY`, `FAILED_CAPTURE`), defect flags.
  * `InspectionView`: table `inspection_views` with view side (`dorsal`, `ventral`), image file path, SHA-256 checksum, freshness grade, confidence, and detected defects JSON.
  * `HumanDisposition`: table `human_dispositions` with authoritative supervisor outcome (`ACCEPT`, `REJECT`, `REPROCESS`, `DOWNGRADE`), affected quantity, rationale, and `supersedes_id` self-referential foreign key for corrections.
  * `MaterialMovement`: table `material_movements` tracking physical custody transformation stages (`receiving_to_storage`, `receiving_to_processing`, `processing_wggs`, `processing_fillet`, `storage_to_processing`, `processing_to_dispatch`) with mass/count balancing.
* **Modify `app/models/__init__.py`**:
  * Export `ReceivingDelivery`, `FishInspection`, `InspectionView`, `HumanDisposition`, and `MaterialMovement` so `init_db()` automatically registers metadata and initializes missing tables on startup.
* **Modify `app/core/database.py`**:
  * Configure `connect_args={"check_same_thread": False, "timeout": 30.0}` and enable WAL mode (`PRAGMA journal_mode=WAL;`) on connection to prevent lock contention.

### Phase 2: Input Validation & API Schemas (`code/webdev/backend/`)
* **Create `app/schemas/delivery_trace.py`**:
  * Define Pydantic models for delivery session inception, view capture ingestion, authoritative human disposition recording, transformation journal logging, and bidirectional lineage tree responses.

### Phase 3: Hardware Ingestion & Controller Extension (`code/webdev/backend/`)
* **Create `app/hardware/dual_conveyor_controller.py`**:
  * Inherit from `BaseHardwareController` (or extend `MockHardwareController`).
  * Support simulated Sensor 1 (dorsal) and Sensor 2 (ventral) pulses with realistic physical transit delays (0.8s–1.5s).
  * Provide an operator-assisted trigger mode allowing single-key manual view capture for validation pilot runs.

### Phase 4: Core Services (`code/webdev/backend/`)
* **Create `app/services/two_view_inspection_service.py`**:
  * Handle view capture, calculate SHA-256 integrity hash, persist image to `settings.UPLOAD_DIR`, execute MobileNetV3 and YOLOv8s sequentially, correlate ventral captures to existing dorsal sequences within 3.0s, and fallback to `PARTIAL_DORSAL_ONLY` on timeout.
  * Enforce bounded concurrency with an `asyncio.Semaphore(4)` to protect edge CPU resources.
* **Create `app/services/material_lineage_service.py`**:
  * Implement transformation logging with atomic balance verification (`quantity_in == quantity_out + normal_yield_loss + qc_reject_loss + unexplained_variance`).
  * Enforce non-overdraw rule: verify that total allocated `quantity_in` does not exceed available delivery or lot balance.
  * Implement forward lineage traversal (`get_delivery_lineage`) and backward provenance reconstruction (`get_lot_provenance`) querying `material_movements`, `storage_slots`, and `dispatch_lots`.

### Phase 5: REST API Endpoints (`code/webdev/backend/`)
* **Create `app/api/v1/deliveries.py`**:
  * `POST /api/v1/deliveries`: Start receiving delivery session.
  * `GET /api/v1/deliveries`: Paginated delivery list with summary metrics.
  * `GET /api/v1/deliveries/{id}`: Delivery detail with inspection sequences, flags, dispositions, and movements.
  * `POST /api/v1/deliveries/{id}/capture-view`: Camera trigger ingestion endpoint.
  * `POST /api/v1/deliveries/{id}/dispositions`: Record authoritative supervisor QC disposition.
  * `POST /api/v1/deliveries/{id}/movements`: Record material handoff and yield journal.
  * `GET /api/v1/deliveries/{id}/trace`: End-to-end lineage tree with explicit missing links array.
* **Modify `app/api/v1/router.py`**:
  * Include `deliveries.router` under prefix `/deliveries` with tag `Deliveries & Traceability`.

### Phase 6: Frontend Types & API Client (`code/webdev/frontend/`)
* **Create `types/delivery.ts`**: TypeScript definitions matching backend Pydantic schemas.
* **Modify `lib/api.ts`**: Export methods: `createDelivery()`, `getDeliveries()`, `getDeliveryById()`, `recordDisposition()`, `recordMovement()`, and `getDeliveryTrace()`.
* **Modify `components/layout/Sidebar.tsx`**: Add "Receiving & Trace" navigation link pointing to `/deliveries`.

### Phase 7: Frontend Workspaces (`code/webdev/frontend/`)
* **Create `app/deliveries/page.tsx`**: Receiving dock dashboard for truck registration, active session management, and live conveyor counts.
* **Create `app/deliveries/[id]/page.tsx`**: Inspection detail workspace displaying side-by-side dorsal/ventral images, bounding boxes, defect tags, supervisor disposition action modal, and WGGS/Fillet yield logging forms.
* **Create `app/deliveries/[id]/trace/page.tsx`**: Lineage visualization page rendering the interactive provenance graph from delivery through storage slots and export dispatches, badging unresolved gaps in red.

### Phase 8: Automated Regression Tests (`code/webdev/backend/`)
* **Create `tests/test_delivery_traceability.py`**: Unit & integration tests for delivery lifecycle, dual-view correlation, timeout partial fallback, defect flag triggers, and disposition immutability.
* **Create `tests/test_material_lineage.py`**: Balance invariant enforcement, multi-stage yield accounting, and missing upstream link detection.

---

## 4. Git Commit Hygiene & Delivery Rules

In accordance with user instructions, all changes to `code/webdev/` will be committed as **atomic, separate commits**:
1. Commit 1: `feat(db): add delivery and lineage models with SQLite WAL mode support`
2. Commit 2: `feat(api): add delivery trace validation schemas and API endpoints`
3. Commit 3: `feat(services): implement two-view conveyor ingestion and material lineage engine`
4. Commit 4: `feat(hardware): add dual conveyor controller with manual and mock triggers`
5. Commit 5: `feat(frontend): add delivery types, API client methods, and sidebar navigation`
6. Commit 6: `feat(frontend-ui): implement receiving dock dashboard, QC detail view, and lineage graph`
7. Commit 7: `test: add automated test suites for delivery traceability and mass balance invariants`
8. Commit 8: `docs: update delivery traceability guide and technical specification`
