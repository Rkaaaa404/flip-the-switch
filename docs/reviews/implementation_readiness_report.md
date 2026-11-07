# Implementation Readiness Audit Report (Stage 9)

**Target Document**: `docs/designs/nusaqc_delivery_traceability.md`  
**Target Scope**: Detailed Implementation Plan (Lines 288–436)  
**Standard**: `implementation-readiness-standard.md` (The Zero-Decision Rule)  
**Reviewers**: `egm-implementation-readiness`, `egm-codebase-details`, `egm-style`  
**Workspace Ground Truth**: Verified NO application source code in workspace (`backend/` and `frontend/` absent).  

---

# Part 1: Implementation Readiness & Zero-Decision Audit (`egm-implementation-readiness`)

# Review9Readiness (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/implementation_readiness.md and C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-standard.md first. Review DetailedRange (lines 288–436) of docs/designs/nusaqc_delivery_traceability.md against the Zero-Decision Rule. FeatureRange (lines 1–287) may be read for context. Identify any design, schema, algorithm, error handling, or hardware choices left to the implementer. Audit the execution sequence, target file declarations, verification test plan, and smoke scenario. Assign IDs S9I-01 onward. Include exact reading manifest.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/implementation_readiness.md) ⇒ ok · 63 lines

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-stand…) ⇒ ok · 38 lines

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-stand…) ⇒ ok · 1 line

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:280-360) ⇒ ok · 97 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:360-436) ⇒ ok · 88 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-120) ⇒ ok · 134 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:124-250) ⇒ ok · 145 lines

## assistant

→ glob(*) ⇒ ok · 144 lines

## assistant

→ glob(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/*) ⇒ ok · 11 lines

## assistant

# Stage 9: Implementation Readiness Audit Report

**Target Document**: `docs/designs/nusaqc_delivery_traceability.md`  
**Target Scope**: Detailed Implementation Plan (Lines 288–436)  
**Context Scope**: Feature & Architecture Overview (Lines 1–287)  
**Standard**: `implementation-readiness-standard.md` (The Zero-Decision Rule)  
**Auditor Persona**: Implementation Readiness Goldfish (Technical Lead & Implementing Software Engineer)

---

## 1. Reading Manifest & Limitations

### 1.1 Exact Reading Manifest
* `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/implementation_readiness.md` (lines 1–62)
* `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-standard.md` (lines 1–37)
* `docs/designs/nusaqc_delivery_traceability.md`:
  * DetailedRange (Lines 288–436): Execution sequence, 17 target file declarations, compilation commands, pytest suite, test coverage rules, and manual smoke scenario.
  * FeatureRange (Lines 1–287): Overview, Problem statement, Goals/Non-goals, Open Questions (Q1–Q7), CUJs 1–4, Architecture diagram, Relational schema, Ingestion pipeline, API endpoints, Non-functional requirements, and Alternatives.
* Workspace Filesystem Check (`glob`): Root directory, `.agents/`, `docs/`, `other-idea/`, and `past-comp-idea/`.
* Approved Reference Context: `C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/*` (extracted table/pitch assets).

### 1.2 Audit Limitations & Verified Ground Truth
* **Workspace Ground Truth**: Verified through repository inspection that **NO** backend or frontend implementation source code exists in this repository. Specifically, there is no `backend/` directory, no `frontend/` directory, no `pyproject.toml`, no `requirements.txt`, no `package.json`, and no `docker-compose.yml`.
* **Scope Restriction**: All findings strictly target lines 288–436 (DetailedRange). Upstream sections (1–287) were inspected solely as reference context to verify whether design gaps in lines 288–436 were resolved elsewhere in the specification.
* **Read-Only Compliance**: No files were created, edited, compiled, or executed during this audit.

---

## 2. Executive Summary & Zero-Decision Readiness Verdict

**Verdict**: **FAIL (Implementation Blocked)**

The Detailed Implementation Plan provides a coherent conceptual narrative and an organized 8-phase structure. However, it fails the **Zero-Decision Rule**:
> *"A plan passes if a competent engineer (or fresh AI session) who is unfamiliar with the codebase can execute the plan and produce the correct changes on the first attempt, without guessing, asking clarifying questions, or making independent design choices."*

An engineer tasked with executing this plan immediately faces three critical blockers:
1. **Ghost Codebase Assumptions**: The plan designates existing files to `(Modify)` (e.g. `backend/app/models/__init__.py`, `backend/app/api/v1/router.py`, `frontend/lib/api.ts`, `frontend/components/layout/Sidebar.tsx`) and references base classes (`gpio_controller.py`, `mock_controller.py`, `init_db()`), none of which exist in the workspace. It omits the initial project bootstrapping and configuration files (`pyproject.toml`, `package.json`, `docker-compose.yml`).
2. **Underspecified & Contradictory Two-View Ingestion**: The conveyor correlation algorithm (matching ventral to dorsal views), concurrency model, and timeout mechanisms contain architectural contradictions between per-sequence timer cancellations and batch database sweeper tasks.
3. **Ghost Downstream Tables & Paradoxical Trace Gap Logic**: The lineage engine references non-existent tables (`storage_slots`, `dispatch_lots`, `dispatches`) without declaring their schemas, and requires a forward trace endpoint (`/api/v1/deliveries/{id}/trace`) to detect lots with "missing upstream receiving links", which is mathematically impossible when traversing downstream from a known delivery root.

---

## 3. Detailed Audit Findings (S9I-01 through S9I-10)

### S9I-01: Ghost Base Repository Assumption & Omission of Project Scaffolding in Target Scope
* **Severity**: **Blocker**
* **Affected Scope**: Lines 292–300, 312–315, 352–355, 364–367, 380–383, 401–407, 427
* **Finding & Guidance**:
  * **Evidence**: The implementation sequence and target file list specify modifying pre-existing files:
    * Line 312: `backend/app/models/__init__.py (Modify)` to expose models for "FastAPI's `init_db()`".
    * Line 352: `backend/app/api/v1/router.py (Modify)` to mount alongside "legacy routes (`/inspections`, `/lots`, `/storage`, `/dispatch`, `/settings`)".
    * Line 358: `dual_conveyor_controller.py` states it "Extends existing `gpio_controller.py` and `mock_controller.py`".
    * Line 364 & 380: `frontend/lib/api.ts (Modify)` and `frontend/components/layout/Sidebar.tsx (Modify)`.
    * Lines 401–406 & 427: Verification commands assume pre-configured build chains (`uv run ruff check`, `pnpm run build`, `docker compose up --build`).
    * *Verified Workspace Fact*: There are no files or directories under `backend/` or `frontend/`, and no `pyproject.toml`, `package.json`, or `docker-compose.yml`.
  * **Consequence**: A developer or autonomous agent executing Phase 1 (`backend/app/models/__init__.py`) immediately encounters missing directories and base files. The developer is forced to make uncontrolled architectural design choices: selecting FastAPI application architecture, configuring SQLAlchemy `declarative_base()` and session lifecycle, creating a Next.js frontend project from scratch, and writing Docker Compose configurations without design guidance.
  * **Recommendation**: Update Section 302 ("Target Files to Create/Modify") to:
    1. Either declare the essential application scaffolding files as `(Create)`:
       * `pyproject.toml` (with Python 3.11+, FastAPI, SQLAlchemy, Pydantic, Ruff, Pytest dependencies).
       * `backend/app/main.py` and `backend/app/core/database.py` (Base declaration and engine factory).
       * `package.json` (Next.js 14+ app router, TypeScript, Tailwind CSS).
       * `docker-compose.yml` (backend and frontend container definitions).
    2. Or explicitly state in the preamble that the implementation is to be developed within a separate target repository, linking to its exact repository contract.
  * **Tradeoff**: Adding scaffold file manifests increases specification length, but is required for first-attempt execution in this workspace.

---

### S9I-02: Contradictory and Underspecified Dual-View Ingestion & Timeout Architecture
* **Severity**: **Blocker**
* **Affected Scope**: Lines 295, 326–332
* **Finding & Guidance**:
  * **Evidence**:
    * Line 330: `handle_view_capture(db: Session, delivery_id: str, view_side: str, image_bytes: bytes) -> FishInspection`: "...invokes inference sequentially via `app.ai.inference`, and matches with existing sequence or opens new sequence."
    * Line 331: `reap_timed_out_captures(db: Session, timeout_seconds: float = 3.0)`: "Background asyncio task that transitions orphan dorsal captures older than 3 seconds to `PARTIAL_DORSAL_ONLY` and sets `flagged_for_review = TRUE`."
    * Context Conflict: Upstream lines 209 and 212 specify: *"Sets pairing timeout timer (3.0s)... Cancels timeout timer for sequence N."*
  * **Hurdles & Missing Implementer Choices**:
    1. *Correlation Algorithm Left Open*: How does `handle_view_capture` match an incoming ventral capture to a dorsal capture? Is it a FIFO queue? What if two fish are in flight between Sensor 1 and Sensor 2? What if Sensor 2 fires for a fish whose Sensor 1 trigger failed?
    2. *Concurrency & State Hazards*: If correlation is tracked in-memory, what happens on server restarts or across multiple Uvicorn workers? If tracked in SQLite, table-level write locks under SQLite will stall ingestion.
    3. *Session Lifecycle Conflict*: Passing `db: Session` to a "Background asyncio task" violates SQLAlchemy session management. A synchronous session cannot be held across asynchronous sleep loops. Moreover, active timer cancellation (Line 212) contradicts a periodic polling reaper (Line 331).
    4. *Underspecified Inference Interface*: `app.ai.inference` has no defined signature, input tensor format, or mock return contract, leaving the developer to guess its API and ONNX model loading logic.
  * **Consequence**: The developer must independently design the conveyor queue state machine, resolve session concurrency bugs, and invent the AI inference interface.
  * **Recommendation**:
    1. Define the exact correlation query: when a `ventral` capture arrives, query `fish_inspections` for the earliest record where `delivery_id = :id AND status = 'PENDING_VENTRAL'` created within the last 3.0 seconds.
    2. Replace contradictory timer references with a deterministic database-backed reaper pattern: a background worker (`async def capture_timeout_worker()`) that spawns a transient `SessionLocal()` every 500 ms to transition expired pending inspections.
    3. Specify the inference function signature: `def run_vision_inference(image_bytes: bytes, view_side: str) -> tuple[str, float, list[dict]]`.
  * **Tradeoff**: Polling the database introduces slight polling overhead compared to in-memory timer handles, but is fully restart-safe, thread-safe, and deterministic.

---

### S9I-03: Underspecified Lineage Retrieval, Ghost Downstream Tables, and Paradoxical Gap Detection
* **Severity**: **Blocker**
* **Affected Scope**: Lines 296, 333–339, 350, 421
* **Finding & Guidance**:
  * **Evidence**:
    * Line 338: `get_delivery_audit_trail(db: Session, delivery_id: str) -> DeliveryTraceTreeResponse`: "...traces downstream `material_movements` into `storage_slots` and `dispatch_lots`, and isolates any lots with missing upstream receiving links."
    * Line 350: `GET /{id}/trace`: "End-to-end lineage retrieval with explicit data gaps array."
    * Line 421: `test_audit_trace_with_missing_links`: "Query `/api/v1/deliveries/{id}/trace` for lot with missing upstream receiving link; verify `missing_links` array isolates the gap explicitly without hallucinated connections."
  * **Hurdles & Missing Implementer Choices**:
    1. *Ghost Downstream Schemas*: The plan requires tracing into `storage_slots`, `dispatch_lots`, and `dispatches`, but never defines the ORM models, column names, or foreign keys for these tables.
    2. *Logical Contradiction in Gap Detection*: Tracing *downstream* from a specific `delivery_id` traverses child movements that inherently point to that delivery as root. A downstream node cannot have a "missing upstream receiving link" unless it was somehow linked to a delivery it does not point to. To detect lots with missing upstream links, an audit must trace *backward* from a lot or dispatch (e.g. `GET /api/v1/lots/{lot_id}/trace`), which is completely omitted from the API declarations!
    3. *Missing Graph Traversal Algorithm*: The recursive SQLite CTE query mentioned in Line 335 is not documented, leaving cyclic re-processing loops and recursion depth limits undefined.
  * **Consequence**: An implementer cannot write `material_lineage_service.py` or implement test case 7 (`test_audit_trace_with_missing_links`) without inventing table schemas and altering the API contract.
  * **Recommendation**:
    1. Provide explicit schema definitions or mocks for `storage_slots` and `dispatch_lots`.
    2. Define the exact graph traversal query/CTE in the plan.
    3. Clarify the gap detection rule: in a delivery trace (`GET /deliveries/{id}/trace`), a gap (`missing_link`) is defined as a `material_movement` whose `input_ref` cannot be resolved to an active delivery or prior movement, or an `output_lot_id` that has no downstream storage/dispatch record.
    4. If backward provenance is required, explicitly add `GET /api/v1/lots/{lot_id}/trace` to the API routes.
  * **Tradeoff**: Formalizing gap rules to unresolved parent references keeps the traversal bounded within the delivery tree without requiring external endpoints.

---

### S9I-04: Incomplete API Lifecycle Specifications (Missing Close Endpoint and Payload Contracts)
* **Severity**: **Major**
* **Affected Scope**: Lines 340–351, 415
* **Finding & Guidance**:
  * **Evidence**:
    * Line 415: `test_delivery_session_lifecycle` requires: *"Create delivery, verify status transitions from `active_receiving` to `closed`."*
    * Lines 344–350 list only 7 endpoints: `POST /`, `GET /`, `GET /{id}`, `POST /{id}/capture-view`, `POST /{id}/dispositions`, `POST /{id}/movements`, `GET /{id}/trace`.
    * There is NO endpoint defined to transition a delivery to `closed` or `inspection_complete`.
    * Line 347 declares `POST /{id}/capture-view` without specifying the HTTP transport contract (`multipart/form-data` vs JSON base64 vs octet-stream).
    * Line 345 declares `GET /` as a "Paginated list of deliveries with summary metrics" without naming the query parameters (`skip`/`limit` vs `page`/`size`) or defining the summary response fields.
  * **Consequence**: The implementer must invent an endpoint to close deliveries (e.g. `POST /{id}/close` or `PATCH /{id}`), guess how camera clients upload images, and guess the pagination query contract.
  * **Recommendation**:
    1. Add an explicit state transition endpoint: `POST /api/v1/deliveries/{id}/close` (returning status `closed`).
    2. Document `POST /{id}/capture-view` as consuming `multipart/form-data` with fields `view_side: str` and `file: UploadFile`.
    3. Define pagination on `GET /api/v1/deliveries` as `skip: int = 0, limit: int = 20`, returning `{ items: list[DeliverySummaryResponse], total: int, skip: int, limit: int }`.
  * **Tradeoff**: Standardizing on RESTful action sub-resources (`/{id}/close`) is clean and avoids ambiguous generic PATCH payloads.

---

### S9I-05: Unclear Mass/Count Balancing Validation Algorithm and Floating-Point Tolerances
* **Severity**: **Major**
* **Affected Scope**: Lines 323, 337, 349, 420
* **Finding & Guidance**:
  * **Evidence**:
    * Line 323 states `MaterialMovementCreate`: "requires that inputs equal outputs within declared variance."
    * Line 420 (`test_wggs_and_fillet_lineage_accounting`): "verify that input equals outputs + normal yield loss + reject loss + unexplained variance."
    * Line 230 includes `unexplained_variance` as a client-provided payload field in `POST /deliveries/{id}/movements`.
  * **Hurdles & Missing Implementer Choices**:
    1. *Trivialized Validation*: If `unexplained_variance` is supplied by the user, the equation `quantity_in = quantity_out + normal_yield_loss + qc_reject_loss + unexplained_variance` can always be satisfied by setting `unexplained_variance` to whatever remainder exists. Is `unexplained_variance` a calculated field, or is there an allowable threshold (e.g. $\le 5\%$)?
    2. *Float Inexactness*: Using exact equality (`==`) on floating-point mass numbers in Python (`0.1 + 0.2 != 0.3`) will cause false 400 validation rejections.
    3. *Cross-Unit Transformations*: Section 55 (Open Questions Q4) leaves quantity units open. If fish enter WGGS as `count` and exit as `kg`, how is mass/count balance validated without a defined average piece weight?
  * **Consequence**: An engineer will either implement fragile float equality that rejects valid records, or allow arbitrary unexplained variances that undermine audit reliability.
  * **Recommendation**:
    1. Specify that `unexplained_variance` is automatically computed by the backend service:
       $$\text{unexplained\_variance} = \text{round}(\text{quantity\_in} - (\text{quantity\_out} + \text{normal\_yield\_loss} + \text{qc\_reject\_loss}), 4)$$
    2. Apply a strict tolerance check: raise an HTTP 422 error if $\text{abs}(\text{unexplained\_variance}) > 0.05 \times \text{quantity\_in}$ unless accompanied by a mandatory `notes` justification.
    3. Enforce that `quantity_unit` must match across all balance fields for a given movement record.
  * **Tradeoff**: Auto-computing variance removes operator burden and eliminates client-side rounding disputes.

---

### S9I-06: Underspecified Hardware Simulation Interface and Execution Hook
* **Severity**: **Major**
* **Affected Scope**: Lines 356–359, 429
* **Finding & Guidance**:
  * **Evidence**:
    * Line 358 states `dual_conveyor_controller.py` "Extends existing `gpio_controller.py` and `mock_controller.py`". (Neither base file exists in the workspace).
    * Line 429 (Smoke Scenario step 3): "Trigger 5 mock fish inspections with Mock Controller (including 1 partial capture and 1 ulcer-flagged fish)."
  * **Hurdles & Missing Implementer Choices**:
    1. *Missing Execution Trigger*: Step 3 does not state *how* to trigger the mock controller during manual smoke testing. Is there an API endpoint, a CLI command, a script, or a frontend button?
    2. *Synthetic Image Provenance*: Where do the mock camera frames come from? Does the controller generate synthetic JPEGs with Pillow, load local fixtures, or send blank bytes?
  * **Consequence**: A tester or CI pipeline cannot execute the smoke scenario without inventing custom scripts or test-only hooks.
  * **Recommendation**:
    1. Define `MockConveyorController` as a standalone class with a direct method: `async def simulate_fish_passage(delivery_id: str, defect: str | None = None, drop_ventral: bool = False) -> FishInspection`.
    2. Expose a dedicated testing endpoint mounted only in test/development environments: `POST /api/v1/hardware/mock-passage`.
    3. Specify that synthetic test images are generated on-the-fly via Pillow with colored canvas and defect text.
  * **Tradeoff**: An explicit development/test endpoint allows both automated tests and browser smoke testers to easily trigger simulated hardware events.

---

### S9I-07: Unspecified Frontend Lineage Visualization Library and Node Model
* **Severity**: **Major**
* **Affected Scope**: Lines 376–379, 432
* **Finding & Guidance**:
  * **Evidence**:
    * Line 378: `frontend/app/deliveries/[id]/trace/page.tsx`: "Audit visualization page rendering the interactive provenance tree... prominently badging unresolved gaps in red."
    * Line 432: "verify the complete lineage tree loads in $< 1.0$ second, with all physical handoffs and yield losses clearly displayed."
  * **Hurdles & Missing Implementer Choices**:
    1. *Library Selection Left to Implementer*: The plan does not specify which visualization library to install (e.g. `@xyflow/react` / `reactflow`, `mermaid.js`, `d3`, or custom HTML/SVG).
    2. *Undefined Node Component Schema*: The plan does not define what visual cards represent a delivery, inspection batch, disposition, or movement.
    3. *Subjective Performance Benchmark*: "$< 1.0$ second" load time in a manual smoke test is undefined: does this measure API TTFB, DOM paint, or full image hydration?
  * **Consequence**: The frontend implementer must make independent technology choices that may introduce heavy client bundle overhead.
  * **Recommendation**: Specify a lightweight, dependency-free CSS/SVG hierarchical tree layout (or designate `@xyflow/react` specifically in `package.json`), document the 5 visual node types, and define the performance benchmark as API response latency $< 500$ ms plus client render $< 500$ ms.
  * **Tradeoff**: A native CSS/SVG hierarchy avoids third-party dependency bloat while easily meeting the sub-second render target.

---

### S9I-08: Hardcoded Non-Configurable Storage Path `/data/captures/{delivery_id}/`
* **Severity**: **Nit**
* **Affected Scope**: Line 330
* **Finding & Guidance**:
  * **Evidence**: Line 330 hardcodes: `handle_view_capture`: "writes image to `/data/captures/{delivery_id}/`".
  * **Consequence**: An absolute path starting with `/data` fails on Windows workstations (where `/data` does not exist or requires root permissions) and prevents custom container volume mounting.
  * **Recommendation**: Replace the hardcoded path with an environment-backed Pydantic setting: `CAPTURES_DIR: Path = Path("./data/captures")`.
  * **Tradeoff**: Zero negative tradeoff; guarantees local Windows and Docker compatibility.

---

### S9I-09: Missing Branch Coverage Enforcement in Pytest Execution Command
* **Severity**: **Nit**
* **Affected Scope**: Lines 412, 423–424
* **Finding & Guidance**:
  * **Evidence**: Line 424 specifies "Strict **85%+ branch coverage** across `backend/app/services/two_view_inspection_service.py` and `backend/app/services/material_lineage_service.py`", but the test execution command in Line 412 is:
    ```sh
    uv run pytest backend/tests/test_delivery_traceability.py backend/tests/test_material_lineage.py -v
    ```
    which contains no `--cov` or coverage gate flags.
  * **Consequence**: Developers running the command will see tests pass without knowing if the 85% branch coverage mandate was satisfied.
  * **Recommendation**: Update the command in Line 412 to:
    ```sh
    uv run pytest backend/tests/ --cov=backend/app/services --cov-branch --cov-fail-under=85 -v
    ```
  * **Tradeoff**: Requires adding `pytest-cov` to test dependencies.

---

### S9I-10: Missing Concrete Numerical Values in Smoke Scenario Steps 4 & 5
* **Severity**: **Nit**
* **Affected Scope**: Lines 430–431
* **Finding & Guidance**:
  * **Evidence**:
    * Line 430: "submit a human disposition (`ACCEPT` 450 kg, `REPROCESS` 50 kg for trimming)".
    * Line 431: "Record a `processing_wggs` movement and a `processing_fillet` movement, noting normal biological removal."
  * **Consequence**: Step 5 omits exact numerical values for `quantity_in`, `quantity_out`, and `normal_yield_loss`, forcing the tester to invent numbers that may violate the balance checks established in S9I-05.
  * **Recommendation**: Provide explicit test fixtures for Step 5:
    * WGGS: In 450 kg $\rightarrow$ Out 382.5 kg (WGGS Lot `W-001`), Yield Loss 67.5 kg (15%), QC Reject 0 kg, Variance 0 kg.
    * Fillet: In 382.5 kg $\rightarrow$ Out 153.0 kg (Fillet Lot `F-001`), Yield Loss 229.5 kg (60%), QC Reject 0 kg, Variance 0 kg.
  * **Tradeoff**: Zero negative tradeoff; provides a 100% deterministic, repeatable smoke walkthrough.

---

## 4. Summary Table of Audit Findings

| ID | Severity | Target Lines | Audit Vector | Description |
| :--- | :--- | :--- | :--- | :--- |
| **S9I-01** | **Blocker** | 292–300, 312–315, 352–383, 401–407, 427 | Scope & Boundary | Ghost base repository assumption; missing project bootstrapping files (`pyproject.toml`, `package.json`, `docker-compose.yml`). |
| **S9I-02** | **Blocker** | 295, 326–332 | Logic & Algorithm | Contradictory dual-view ingestion & timeout architecture; undefined correlation queue, session leaks, and missing AI inference contract. |
| **S9I-03** | **Blocker** | 296, 333–339, 350, 421 | Schema & Traversal | Underspecified lineage engine; ghost downstream tables (`storage_slots`, `dispatch_lots`), and paradoxical gap detection on delivery root. |
| **S9I-04** | **Major** | 340–351, 415 | API Contract | Missing delivery close endpoint, ambiguous multipart/form-data ingestion, and unspecified pagination query fields. |
| **S9I-05** | **Major** | 323, 337, 349, 420 | Data Validation | Trivialized variance equation, float comparison hazards, and unhandled cross-unit transformation balance checks. |
| **S9I-06** | **Major** | 356–359, 429 | Hardware Simulation | Missing base controllers (`gpio_controller.py`), undefined trigger API/hook, and unspecified synthetic image generation. |
| **S9I-07** | **Major** | 376–379, 432 | Frontend Design | Unspecified frontend graph rendering library, undefined visual node model, and subjective performance benchmark. |
| **S9I-08** | **Nit** | 330 | Portability | Hardcoded POSIX capture path `/data/captures/{delivery_id}/` breaks local Windows execution. |
| **S9I-09** | **Nit** | 412, 423–424 | Verification | Pytest execution command lacks `--cov-branch --cov-fail-under=85` flags required by coverage standard. |
| **S9I-10** | **Nit** | 430–431 | Smoke Scenario | Omission of concrete numerical mass balance figures in smoke scenario steps 4 & 5. |

---

## 5. Implementation Lead Handoff Notes

Prior to commencing Phase 1 coding, the technical design author must resolve the three blockers (`S9I-01`, `S9I-02`, and `S9I-03`):
1. **Scaffold Manifest**: Provide the minimal repository scaffold manifests so an engineer or AI worker can initialize the backend and frontend runtimes without guessing framework versions or project configurations.
2. **Ingestion Contract**: Provide the exact database schema transition logic for pairing dorsal and ventral views, replacing timer cancellation with a periodic database sweeper and declaring the vision inference function signature.
3. **Lineage Contract**: Specify the recursive SQL query and schema stubs for downstream storage/dispatch entities, or isolate the audit trail strictly to `material_movements` with clear parent-gap semantics.

---

# Part 2: Codebase Details & Integration Audit (`egm-codebase-details`)

# Review9Codebase (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/codebase_details.md and C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-standard.md first. Review DetailedRange (lines 288–436) of docs/designs/nusaqc_delivery_traceability.md. Verify whether target file paths, package imports, controllers (gpio_controller, mock_controller), and init_db() mechanisms assume an existing codebase that is absent in the workspace. Distinguish verified codebase facts from unverified assumptions. Note: Proposed files marked Create are not defects, but references asserting current existing code require verification. Assign IDs S9C-01 onward. Include exact reading manifest.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/codebase_details.md) ⇒ ok · 70 lines

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-stand…) ⇒ ok · 38 lines

## assistant

→ glob({"hidden":true}) ⇒ ok · 144 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:280-440) ⇒ ok · 166 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-100) ⇒ ok · 114 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:104-250) ⇒ ok · 165 lines

## assistant

→ glob(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/) ⇒ ok · 11 lines

## assistant

→ read(past-comp-idea/nusaqc.md:1-50) ⇒ ok · 63 lines

## assistant

→ glob(*{docker*,pyproject*,package*,requirements*}*) ⇒ ok · 1 line

## assistant

→ glob(**/{backend,frontend}/**) ⇒ ok · 1 line

## assistant

→ read(nusaqc-proposal.pdf:1-50) ⇒ ok · 56 lines

## assistant

→ read(nusaqc-proposal.pdf:230-310) ⇒ ok · 88 lines

## assistant

→ read(nusaqc-proposal.pdf:350-450) ⇒ ok · 108 lines

## assistant

# Codebase Details Audit Report: NusaQC Delivery Traceability

**Review Mode**: REVIEW  
**Audit Stage**: Stage 9 (Implementation Readiness Test)  
**Target Document**: `docs/designs/nusaqc_delivery_traceability.md`  
**Target Scope**: Detailed Implementation Plan (Lines 288–436)  
**Evaluator**: `Review9Codebase` (Codebase Details Goldfish)  

---

## 1. Reading Manifest & Verification Limitations

### Exact Reading Manifest
* `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/codebase_details.md` (Agent definition, mandates, audit vectors)
* `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/implementation-readiness-standard.md` (Implementation readiness bar, Zero-Decision Rule)
* `docs/designs/nusaqc_delivery_traceability.md`:
  * DetailedRange: lines 288–436 (Implementation sequence, 17 target files, compilation & test plans, smoke scenarios)
  * FeatureRange (context): lines 1–287 (Problem statement, goals, non-goals, architecture diagram, 5-table schema, 2-view pipeline, alternatives)
* `past-comp-idea/nusaqc.md` (Background context on prior competition proposal & repository structure)
* `nusaqc-proposal.pdf` (Pages 1–3, 10–22: BOM, system architecture, tech stack, page functionality)
* `C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/` (Extracted table image assets)
* Workspace Filesystem Scans (`glob`): Root directory, recursive search for `backend/`, `frontend/`, `docker-compose.yml`, `pyproject.toml`, `package.json`, and hardware controllers.

### Verification Ground Truth & Limitations
* **Workspace Ground Truth**: No application implementation source code exists in this workspace. There are zero files in `backend/` or `frontend/`, no `docker-compose.yml`, no `pyproject.toml`, and no `package.json`.
* **Standard Criteria Application**: In accordance with the *Implementation Readiness Standard* and *Codebase Details* guidelines:
  * Proposed files explicitly marked `(Create)` are **not** treated as defects.
  * References asserting **current existing code** (e.g., files marked `Modify`, extensions of "existing" classes, imports of "existing" internal modules, invocations of framework built-ins that do not exist, and legacy routes/tables) are strictly audited and verified against the workspace ground truth.

---

## 2. Summary of Findings

| ID | Severity | Target Scope (Lines) | Category | Core Issue |
| :--- | :--- | :--- | :--- | :--- |
| **S9C-01** | 🔴 Blocker | Lines 293, 297, 299, 312–315, 352–355, 364–367, 380–383 | Non-Existent References | 4 target files marked `(Modify)` do not exist in workspace |
| **S9C-02** | 🔴 Blocker | Lines 298, 356–359, 429 | Non-Existent References | Extends phantom controllers `gpio_controller.py` & `mock_controller.py` |
| **S9C-03** | 🔴 Blocker | Line 330 | Non-Existent References | Ingestion service imports phantom package `app.ai.inference` |
| **S9C-04** | 🟡 Major | Lines 293, 312–315 | Contradicts Code / Framework | Relies on non-existent `FastAPI's init_db()` table registration |
| **S9C-05** | 🟡 Major | Lines 338, 354 | Non-Existent References | Assumes legacy routes (`/inspections`, etc.) and models (`storage_slots`, `dispatch_lots`) |
| **S9C-06** | 🟡 Major | Lines 400–407, 411–413, 427 | Unstated Assumptions | Verification mandates `uv`, `pnpm`, `docker compose` with zero manifests |
| **S9C-07** | 🟢 Nit | Line 330 (cf. Line 203) | Unstated Assumptions | Hardcoded absolute storage root `/data/captures/` breaks non-container hosts |
| **S9C-08** | 🟢 Nit | Lines 300, 384–391, 411–422 | Test Infrastructure Neglect | Omission of shared test infrastructure (`conftest.py` / session fixtures) |

---

## 3. Detailed Audit Findings

### S9C-01: Non-Existent Base Files Marked as `(Modify)`
* **Severity**: 🔴 Blocker
* **Affected Scope**: Lines 293, 297, 299, 312–315, 352–355, 364–367, 380–383
* **Discrepancy Description & Rationale**:
  The plan specifies that execution proceeds by modifying four existing files:
  1. `backend/app/models/__init__.py (Modify)` (lines 293, 312)
  2. `backend/app/api/v1/router.py (Modify)` (lines 297, 352)
  3. `frontend/lib/api.ts (Modify)` (lines 299, 364)
  4. `frontend/components/layout/Sidebar.tsx (Modify)` (lines 299, 380)
  
  In the workspace ground truth, neither `backend/` nor `frontend/` directories exist. Marking these files as `(Modify)` asserts that an existing baseline codebase is present in the repository.
* **Evidence**:
  A workspace-wide glob search for `backend/**` and `frontend/**` returns zero matches.
* **Consequence**:
  An implementer or automated coding agent executing this plan will encounter immediate fatal `FileNotFoundError` / `ENOENT` errors when attempting to open and patch these files. Because there is no base router, no base API client, and no sidebar layout component to modify, execution halts immediately.
* **Recommendation**:
  1. If this workspace is a greenfield repository, change the operation tag for all four files from `(Modify)` to `(Create)` and supply their complete baseline content or scaffolding steps.
  2. If the plan assumes an external pre-existing NusaQC MVP repository, explicitly define Phase 0 with the mandatory repository prerequisite, submodule checkout, or branch setup instructions.
* **Tradeoff**:
  Providing greenfield creation specifications slightly increases the size of the plan, but guarantees that a fresh engineer or automated agent can execute the plan without ambiguity.

---

### S9C-02: Non-Existent Hardware Base Controllers (`gpio_controller.py`, `mock_controller.py`)
* **Severity**: 🔴 Blocker
* **Affected Scope**: Lines 298, 356–359, 429
* **Discrepancy Description & Rationale**:
  Line 358 states: *"Extends existing `gpio_controller.py` and `mock_controller.py` to drive both proximity sensors, control the conveyor motor, and emit mock Sensor 1 and Sensor 2 events..."*. Line 429 further directs the manual smoke test: *"Trigger 5 mock fish inspections with Mock Controller..."*.
  Neither `gpio_controller.py`, `mock_controller.py`, nor the directory `backend/app/hardware/` exists in the repository.
* **Evidence**:
  `glob` search confirms no files matching `*controller*` or any Python files under `backend/app/hardware/`.
* **Consequence**:
  `dual_conveyor_controller.py` cannot inherit from or wrap these base classes. The plan violates the Zero-Decision Rule because it leaves the hardware abstraction layer, GPIO pin assignments, motor relay signaling, and mock event scheduling completely undefined.
* **Recommendation**:
  Specify `backend/app/hardware/dual_conveyor_controller.py` as a standalone, self-contained controller class (defining its own abstract base or protocol, simulated timer loop, and direct mock trigger methods) rather than claiming to extend non-existent files. Add `gpio_controller.py` and `mock_controller.py` as `(Create)` if they are intended to remain distinct modules.
* **Tradeoff**:
  Self-containing the mock simulation and controller logic into `dual_conveyor_controller.py` eliminates phantom dependencies without adding unnecessary multi-file boilerplate.

---

### S9C-03: Non-Existent `app.ai.inference` AI Pipeline Module Reference
* **Severity**: 🔴 Blocker
* **Affected Scope**: Line 330
* **Discrepancy Description & Rationale**:
  Line 330 specifies the logic for `handle_view_capture`:
  `handle_view_capture(db: Session, delivery_id: str, view_side: str, image_bytes: bytes) -> FishInspection`: *"Computes SHA-256, writes image to `/data/captures/{delivery_id}/`, invokes inference sequentially via `app.ai.inference`, and matches with existing sequence or opens new sequence."*
  No Python package `app.ai` or module `app.ai.inference` exists in the repository.
* **Evidence**:
  No files match `app/ai/*` or `*inference*` across the workspace.
* **Consequence**:
  `two_view_inspection_service.py` cannot import `app.ai.inference`. The method signatures, payload formats, error handling (e.g., model execution failure, missing weights, corrupted image buffers), and mock inference hooks are undocumented, leaving the implementer unable to connect image capture with inspection output.
* **Recommendation**:
  Explicitly specify the signature of the inference interface (e.g. `run_view_inference(image_bytes: bytes, view_side: str) -> ViewInferenceResult`), and either:
  - Add `backend/app/ai/inference.py` to the target files list as `(Create)` with an ONNX/mock implementation; OR
  - Define an injectable `InferenceCallable` dependency in `two_view_inspection_service.py` that defaults to a deterministic heuristic/mock generator when ONNX runtime weights are unconfigured.
* **Tradeoff**:
  An injectable inference callable decouples application persistence and correlation logic from heavy ML runtimes (ONNX Runtime / PyTorch), facilitating fast unit testing.

---

### S9C-04: Non-Existent `FastAPI's init_db()` Mechanism and Missing Engine Setup
* **Severity**: 🟡 Major
* **Affected Scope**: Lines 293, 312–315
* **Discrepancy Description & Rationale**:
  Line 314 states: *"Exposes the new delivery and lineage models so FastAPI's `init_db()` automatically registers metadata and initializes missing tables on startup without requiring an external migration runner."*
  FastAPI does not have a native `init_db()` function or built-in ORM metadata registration mechanism. In standard SQLAlchemy applications, `init_db` is a custom function (invoking `Base.metadata.create_all(bind=engine)`). In this workspace, there is no database engine, declarative `Base`, session factory, or application startup lifespan anywhere.
* **Evidence**:
  Grep for `init_db` across the workspace yields zero occurrences in executable code.
* **Consequence**:
  Exporting models in `__init__.py` will not create any database tables on startup. The implementer is left without guidance on how the SQLite engine is created, where the DB file is located (`./nusaqc.db`), how SQLite WAL mode and foreign key enforcement (`PRAGMA foreign_keys = ON`) are configured, and where the FastAPI lifespan handler is wired.
* **Recommendation**:
  Add `backend/app/database.py` (Create) to the target files list. Explicitly define:
  1. The SQLAlchemy `engine` with `connect_args={"check_same_thread": False}` and a listener for `PRAGMA foreign_keys=ON`.
  2. The `Base = declarative_base()`.
  3. The `get_db()` dependency generator.
  4. The explicit `init_db()` function that calls `Base.metadata.create_all(bind=engine)`, wired to the FastAPI `lifespan` context manager.
* **Tradeoff**:
  Explicitly specifying `backend/app/database.py` adds one small module to the plan, but eliminates any ambiguity regarding database initialization.

---

### S9C-05: Non-Existent References to Legacy API Routers and Relational Tables
* **Severity**: 🟡 Major
* **Affected Scope**: Lines 338, 354
* **Discrepancy Description & Rationale**:
  - Line 354 states that `backend/app/api/v1/router.py` *"Registers `deliveries.router` under `/api/v1/deliveries` alongside legacy routes (`/inspections`, `/lots`, `/storage`, `/dispatch`, `/settings`)."*
  - Line 338 states that `get_delivery_audit_trail` *"...traces downstream `material_movements` into `storage_slots` and `dispatch_lots`..."*
  None of these legacy routes exist in the workspace, and no ORM models or SQLite tables exist for `storage_slots` or `dispatch_lots`.
* **Evidence**:
  No files or database schemas for `/inspections`, `/lots`, `/storage`, `/dispatch`, `storage_slots`, or `dispatch_lots` exist in the workspace.
* **Consequence**:
  If an implementer creates `backend/app/api/v1/router.py` attempting to import legacy routers, the imports will fail. If `material_lineage_service.py` executes SQL `JOIN`s against `storage_slots` or `dispatch_lots`, SQLite will raise `no such table: storage_slots`.
* **Recommendation**:
  1. Clarify that `backend/app/api/v1/router.py` mounts `deliveries.router` as the primary router, with legacy routers omitted or stubbed.
  2. In `material_lineage_service.py`, clarify that lineage graph traversal records `output_lot_id` strings and traces downstream stages through `material_movements`, treating `storage_slots` and `dispatch_lots` as optional external references (e.g. via left joins with fallback null handling) rather than mandatory relational foreign keys.
* **Tradeoff**:
  Decoupling the lineage engine from external legacy tables ensures that the incoming delivery traceability feature is completely self-contained and testable standalone.

---

### S9C-06: Non-Existent Project Tooling, Dependency Manifests, and Container Setup
* **Severity**: 🟡 Major
* **Affected Scope**: Lines 400–407, 411–413, 427
* **Discrepancy Description & Rationale**:
  The Verification Plan prescribes specific CLI invocations:
  - `uv run ruff check backend/app` (line 401)
  - `uv run python -m py_compile ...` (line 402)
  - `cd frontend && pnpm run build` (line 406)
  - `uv run pytest backend/tests/... -v` (line 412)
  - `docker compose up --build` (line 427)
  None of `pyproject.toml`, `requirements.txt`, `uv.lock`, `package.json`, `pnpm-workspace.yaml`, or `docker-compose.yml` exist in the workspace.
* **Evidence**:
  Workspace root contains no project manifest files.
* **Consequence**:
  An engineer attempting to execute the verification plan cannot run `uv run`, `pnpm run build`, `pytest`, or `docker compose`. The verification steps are currently unexecutable in this repository without first creating the project configuration from scratch.
* **Recommendation**:
  Add a prerequisite "Phase 0: Project Configuration & Manifest Scaffolding" to the implementation plan, specifying:
  - Minimal `pyproject.toml` containing dependencies: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pytest`, `httpx`, `ruff`.
  - Minimal `frontend/package.json` with Next.js, React, and TypeScript dependencies.
  - A clean `docker-compose.yml` defining the `backend` and `frontend` services and volume mounts.
* **Tradeoff**:
  Including manifest definitions expands the scope of Phase 0, but is essential for end-to-end verification and reproducible builds.

---

### S9C-07: Unstated Assumption on Storage Root and Hardcoded Absolute Path
* **Severity**: 🟢 Nit
* **Affected Scope**: Line 330 (cross-referenced with Line 203)
* **Discrepancy Description & Rationale**:
  Line 330 states that `handle_view_capture` *"writes image to `/data/captures/{delivery_id}/`"*.
  Hardcoding the absolute Unix path `/data/captures/` breaks compatibility on Windows workstations (where `/data` resolves to `D:\data` or root of drive, typically encountering `PermissionError`) and conflicts with line 165 where `image_path` is declared as a *"Relative path on local filesystem"*.
* **Evidence**:
  Line 330 specifies `/data/captures/{delivery_id}/`, while line 165 specifies relative path.
* **Consequence**:
  Local unit tests and services running outside a Docker Linux container will attempt to write to the drive root, causing test failures on developer machines.
* **Recommendation**:
  Parameterize the capture root directory via an environment variable (e.g. `NUSAQC_STORAGE_DIR`, defaulting to `./data/captures` or a temporary directory during automated tests).
* **Tradeoff**:
  Adding an environment variable configuration introduces minor plumbing in the settings module, but ensures cross-platform portability across Windows, Linux, and Docker.

---

### S9C-08: Test Infrastructure Neglect (Missing Shared Conftest & Fixtures)
* **Severity**: 🟢 Nit
* **Affected Scope**: Lines 300, 384–391, 411–422
* **Discrepancy Description & Rationale**:
  The plan lists two test files: `backend/tests/test_delivery_traceability.py` and `backend/tests/test_material_lineage.py`. However, it neglects test infrastructure (such as `backend/tests/conftest.py`). The test cases described (e.g., testing two-view pairing, timeout transitions, image capture, and API queries) require shared test setup: an isolated in-memory SQLite database, FastAPI `TestClient`, synthetic JPEG generation, and deterministic AI inference mocks.
* **Evidence**:
  No test helper or `conftest.py` is included in the list of target files (lines 302–395).
* **Consequence**:
  Test code will either duplicate session lifecycle and mocking boilerplate across both test files or fail to mock the external `app.ai.inference` dependency.
* **Recommendation**:
  Add `backend/tests/conftest.py` (Create) to the target files list, specifying shared fixtures:
  - `db_session`: Yields an isolated SQLite in-memory session.
  - `client`: Provides a configured `TestClient(app)`.
  - `mock_inference`: Patches the vision inference service to return deterministic mock bounding boxes and freshness grades without loading model weights.
  - `sample_image_bytes`: Returns valid minimal JPEG byte buffers for test uploads.
* **Tradeoff**:
  Formalizing `conftest.py` adds one test infrastructure file to the plan, but prevents duplicated setup code and flaky tests.

---

## 4. Conclusion & Next Steps for Main Agent

The implementation plan in lines 288–436 of `docs/designs/nusaqc_delivery_traceability.md` is technically coherent in its domain design (data modeling, schema contracts, and two-view logic), but currently assumes an existing codebase that is completely absent from the workspace. 

To achieve full **Implementation Readiness** (satisfying the Zero-Decision Rule):
1. **Resolve Blocker S9C-01**: Change `(Modify)` declarations to `(Create)` (or provide explicit repository checkout/prerequisite instructions).
2. **Resolve Blockers S9C-02 & S9C-03**: Self-contain the hardware controller mock logic and specify the inference interface contract rather than referencing phantom external files (`gpio_controller.py`, `mock_controller.py`, `app.ai.inference`).
3. **Resolve Major Findings S9C-04, S9C-05 & S9C-06**: Define database bootstrapping (`backend/app/database.py`), decouple lineage queries from unverified legacy tables, and add minimal project manifests (`pyproject.toml`, `package.json`, `docker-compose.yml`) in a preliminary setup phase.

---

# Part 3: Execution Instruction Precision & Style Audit (`egm-style`)

# Review9Style (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/style.md first. Review DetailedRange (lines 288–436) of docs/designs/nusaqc_delivery_traceability.md. Check execution instructions for vague action verbs, hand-waving requirements, passive voice obscuring responsible modules, ungrounded performance claims, or subjective language. Assign IDs S9S-01 onward. Include exact reading manifest.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/style.md) ⇒ ok · 68 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:280-440) ⇒ ok · 166 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-120) ⇒ ok · 134 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:124-287) ⇒ ok · 182 lines

## assistant

→ glob(*) ⇒ ok · 144 lines

## assistant

→ read(.agents/plugins/egm/resources/document_standards/implementation-readiness-standard.md) ⇒ ok · 38 lines

## assistant

→ read(past-comp-idea/nusaqc.md:1-50) ⇒ ok · 63 lines

## assistant

# Style Audit: Detailed Implementation Plan (Stage 9)

**Target Document**: `docs/designs/nusaqc_delivery_traceability.md`  
**Target Range**: DetailedRange (lines 288–436)  
**Context Evaluated**: FeatureRange (lines 1–287)  
**Auditor**: Style Goldfish (`Review9Style`)  
**Mode**: REVIEW (Stage 9 Implementation Readiness Test)

---

## Reading Manifest & Limitations

### Reading Manifest
1. `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/style.md`: Style Goldfish mandates, audit vectors, and editorial actions (`DROP | CALIBRATE | RELOCATE | KEEP`).
2. `.agents/plugins/egm/resources/document_standards/implementation-readiness-standard.md`: Implementation readiness criteria and the Zero-Decision Rule.
3. `docs/designs/nusaqc_delivery_traceability.md`:
   * Lines 1–287 (FeatureRange): Contextual grounding for architecture, data models, and non-goals.
   * Lines 288–436 (DetailedRange): Exact audit scope covering the implementation sequence, target file plans, and verification procedures.
4. `past-comp-idea/nusaqc.md`: Historical project structure and competition context.
5. Workspace File Tree: Verified ground truth that no backend (`backend/`) or frontend (`frontend/`) source files exist in the current workspace.

### Audit Limitations
* Strictly read-only evaluation. No files were written, modified, or compiled.
* All findings are restricted to execution instructions and file-level plans within DetailedRange (lines 288–436).
* Ground truth constraint applied: references to existing codebase controllers or routes are audited against the confirmed empty-codebase state of this repository.

---

## Executive Summary of Findings

The Detailed Implementation Plan is logically phased and covers the necessary components from ORM persistence to UI pages. However, several execution instructions suffer from hand-waving action verbs, ungrounded performance SLAs, uncalibrated assertions about non-existent codebase components, and anthropomorphic or subjective terminology. 

* **Blocker**: 0
* **Major**: 5
* **Nit**: 7

---

## Detailed Editorial Findings

### S9S-01: Hand-waving correlation logic using vague action verbs
* **Severity**: Major
* **Affected Scope**: Lines 329–330 (`backend/app/services/two_view_inspection_service.py`)
* **Vector**: Vague Action Verbs & Hand-Waving Requirements
* **Evidence**:
  ```markdown
  invokes inference sequentially via `app.ai.inference`, and matches with existing sequence or opens new sequence.
  ```
* **Style Rationale**: The phrase *"matches with existing sequence or opens new sequence"* relies on vague action verbs without defining the stateful matching criteria, key, or data structure. The method signature `handle_view_capture(db: Session, delivery_id: str, view_side: str, image_bytes: bytes)` does not receive a sequence counter, hardware trigger identifier, or parent inspection ID. Leaving the correlation mechanism to implementer intuition forces downstream architectural guessing.
* **Consequence**: An implementer must invent correlation mechanics and concurrency handling from scratch, violating the zero-decision rule.
* **Recommendation**: Replace the hand-waving clause with an exact correlation specification:
  > *"queries `fish_inspections` for an uncompleted record under `delivery_id` created within the last 3.0 seconds lacking a ventral view; if found, attaches the ventral `InspectionView` and updates status to `COMPLETE`; if not found, inserts a new `FishInspection` with `sequence_in_delivery = max(sequence_in_delivery) + 1` and `status = PARTIAL_DORSAL_ONLY`."*
* **Tradeoff**: Increases specification length, but removes all guessing regarding sequence correlation.

---

### S9S-02: Ungrounded UI latency SLA and subjective display criterion
* **Severity**: Major
* **Affected Scope**: Line 432 (Verification Plan / Manual Smoke Scenario, Step 6)
* **Vector**: Ungrounded Performance Claims & Subjective Language
* **Editorial Action**: `CALIBRATE`
* **Evidence**:
  ```markdown
  verify the complete lineage tree loads in < 1.0 second, with all physical handoffs and yield losses clearly displayed.
  ```
* **Style Rationale**: 
  1. The threshold `loads in < 1.0 second` is an ungrounded performance claim asserted without an execution harness, profiling data, hardware baseline, or query volume constraints.
  2. The phrase `"clearly displayed"` is subjective, unmeasurable aesthetic fluff.
* **Consequence**: The verification step is uncalibrated and unfalsifiable. A manual tester cannot objectively measure or assert whether information is "clearly displayed," and the `< 1.0s` requirement establishes an arbitrary SLA on unoptimized development environments.
* **Recommendation**: Calibrate the step to objective, verifiable criteria:
  > *"verify the response returns HTTP 200 with an array of material_movements containing all recorded stages, output lot IDs, and yield losses without unhandled UI errors or rendering timeouts."*
* **Tradeoff**: Removes the aspirational sub-second target, but provides an actionable and falsifiable acceptance criterion.

---

### S9S-03: Uncalibrated claim of existing hardware controllers and subjective delay modifier
* **Severity**: Major
* **Affected Scope**: Lines 356–358 (`backend/app/hardware/dual_conveyor_controller.py`)
* **Vector**: Uncalibrated Claim & Subjective Jargon
* **Editorial Action**: `CALIBRATE`
* **Evidence**:
  ```markdown
  Extends existing `gpio_controller.py` and `mock_controller.py` to drive both proximity sensors, control the conveyor motor, and emit mock Sensor 1 and Sensor 2 events with realistic physical transit delays (0.8s to 1.5s) through the passive inverter guide.
  ```
* **Style Rationale**:
  1. In workspace ground truth, no implementation source files exist in the repository (`gpio_controller.py` and `mock_controller.py` do not exist). Stating that the class *"Extends existing `gpio_controller.py` and `mock_controller.py`"* asserts an unverified codebase fact.
  2. Describing the synthetic 0.8s–1.5s delay as *"realistic"* is subjective puffery; physical transit through the passive inverter guide is an unverified open question (Q1).
* **Consequence**: An engineer executing the plan will search for non-existent base classes in the workspace. Calling unmeasured mock delays "realistic" asserts ungrounded physical fidelity.
* **Recommendation**: Calibrate to specify the creation of a standalone mock driver:
  > *"Implements standalone mock conveyor and sensor simulation routines in `backend/app/hardware/dual_conveyor_controller.py` that emit synthetic Sensor 1 and Sensor 2 events separated by a configurable transit delay (default 0.8s–1.5s)."*
* **Tradeoff**: Acknowledges the clean-slate workspace state instead of implying inheritance from pre-existing modules.

---

### S9S-04: Hand-waving verification instructions with ambiguous compound actions
* **Severity**: Major
* **Affected Scope**: Lines 430–431 (Verification Plan / Manual Smoke Scenario, Steps 4–5)
* **Vector**: Hand-Waving Requirements & Ambiguous Action Instructions
* **Evidence**:
  ```markdown
  4. In `http://localhost:3000/deliveries/DEL-20261107-001`, inspect the flagged fish, confirm two views are displayed side-by-side, and submit a human disposition (`ACCEPT` 450 kg, `REPROCESS` 50 kg for trimming).
  5. Record a `processing_wggs` movement and a `processing_fillet` movement, noting normal biological removal.
  ```
* **Style Rationale**: 
  1. In Step 4, *"submit a human disposition (`ACCEPT` 450 kg, `REPROCESS` 50 kg for trimming)"* describes two distinct disposition outcomes as a single action, contradicting the relational schema where each `human_dispositions` row takes a single outcome and affected quantity.
  2. In Step 5, *"noting normal biological removal"* hand-waves numerical accounting inputs. The data model requires explicit `quantity_in`, `quantity_out`, and `normal_yield_loss` values.
* **Consequence**: A tester cannot follow the scenario unambiguously without guessing whether the UI supports multi-disposition batching or what mass balance numbers to enter.
* **Recommendation**: Clarify each atomic action and provide explicit test figures:
  > *"4. In `http://localhost:3000/deliveries/DEL-20261107-001`, inspect the flagged fish and record two dispositions: first, record `ACCEPT` for 450 kg; second, record `REPROCESS` for 50 kg with reason 'trimming'.*  
  > *5. Record a `processing_wggs` movement (`quantity_in = 450.0`, `quantity_out = 360.0`, `normal_yield_loss = 90.0`); then record a `processing_fillet` movement (`quantity_in = 360.0`, `quantity_out = 180.0`, `normal_yield_loss = 180.0`)."*
* **Tradeoff**: Increases text length in the smoke test section, but guarantees deterministic reproducibility.

---

### S9S-05: Ambiguous validation condition in schema declaration
* **Severity**: Major
* **Affected Scope**: Line 323 (`backend/app/schemas/delivery_trace.py`)
* **Vector**: Hand-Waving Requirements & Vague Terminology
* **Evidence**:
  ```markdown
  requires that inputs equal outputs within declared variance.
  ```
* **Style Rationale**: The phrase *"within declared variance"* is ambiguous. It obscures whether the validator evaluates an exact arithmetic identity where `unexplained_variance` is a balancing term (`quantity_in == quantity_out + normal_yield_loss + qc_reject_loss + unexplained_variance`), or whether it allows a floating-point tolerance/delta between inputs and outputs.
* **Consequence**: Leaves the mathematical contract of Pydantic validation to the implementer's interpretation.
* **Recommendation**: Replace with the explicit arithmetic validation formula:
  > *"validates that `quantity_in == quantity_out + normal_yield_loss + qc_reject_loss + unexplained_variance` (enforcing zero unallocated mass/count discrepancy)."*
* **Tradeoff**: Precludes loose tolerance checks in favor of strict arithmetic balancing.

---

### S9S-06: Anthropomorphic AI buzzword applied to relational database queries
* **Severity**: Nit
* **Affected Scope**: Line 421 (Verification Plan / Automated Test Suite, Test Case 7)
* **Vector**: Jargon & Buzzwords
* **Editorial Action**: `CALIBRATE`
* **Evidence**:
  ```markdown
  verify `missing_links` array isolates the gap explicitly without hallucinated connections.
  ```
* **Style Rationale**: *"Hallucinated"* is an anthropomorphic AI buzzword inappropriately applied to deterministic SQL graph traversal. Relational databases do not hallucinate; they either produce spurious/inferred joins or correctly surface missing keys.
* **Consequence**: Diminishes technical precision and injects informal LLM jargon into backend relational test specifications.
* **Recommendation**: Replace with:
  > *"verify `missing_links` array isolates the gap explicitly without fabricated or inferred parent edges."*
* **Tradeoff**: Replaces marketing buzzwords with standard database engineering terminology.

---

### S9S-07: Framework misattribution and defensive caveat in model registration
* **Severity**: Nit
* **Affected Scope**: Line 314 (`backend/app/models/__init__.py`)
* **Vector**: Imprecise Jargon & Defensive Caveats
* **Editorial Action**: `DROP`
* **Evidence**:
  ```markdown
  Exposes the new delivery and lineage models so FastAPI's `init_db()` automatically registers metadata and initializes missing tables on startup without requiring an external migration runner.
  ```
* **Style Rationale**:
  1. *"FastAPI's `init_db()`"* misattributes application-level logic to the web framework. FastAPI has no native `init_db()` function; table initialization on startup is an application convention using SQLAlchemy's `Base.metadata.create_all()`.
  2. *"without requiring an external migration runner"* is a defensive caveat justifying the design choice rather than stating the operational fact.
* **Consequence**: Misleads readers regarding FastAPI's built-in capabilities and clutters the plan with defensive rationale.
* **Recommendation**: Edit to dry, accurate technical language:
  > *"Exposes the new delivery and lineage models so the application database initialization routine (`Base.metadata.create_all`) registers metadata and creates missing tables on startup."* Drop the clause *"without requiring an external migration runner"*.
* **Tradeoff**: Removes unnecessary defensive justification.

---

### S9S-08: Subjective modifier in API endpoint inventory
* **Severity**: Nit
* **Affected Scope**: Line 348 (`backend/app/api/v1/deliveries.py`)
* **Vector**: Subjective Modifier & Filler
* **Evidence**:
  ```markdown
  * `POST /{id}/dispositions`: Authoritative human QC disposition recording.
  ```
* **Style Rationale**: *"Authoritative"* is a promotional, subjective adjective in an API endpoint list. Technical specifications should state the functional action directly.
* **Consequence**: Injects editorial tone into a routing table.
* **Recommendation**: Rephrase to:
  > `* POST /{id}/dispositions: Record supervisor quality disposition for a specified quantity.`
* **Tradeoff**: Minor rewording for professional neutrality.

---

### S9S-09: Filler intensifiers and redundant modifiers
* **Severity**: Nit
* **Affected Scope**: Line 419 and Line 424 (Verification Plan)
* **Vector**: Filler Words & Wordiness
* **Evidence**:
  ```markdown
  419: verify original inspection records and model outputs remain completely unaltered.
  424: Strict **85%+ branch coverage** across `backend/app/services/two_view_inspection_service.py` and `backend/app/services/material_lineage_service.py`.
  ```
* **Style Rationale**:
  1. *"Completely"* in *"remain completely unaltered"* is a filler intensifier; "unaltered" is binary.
  2. *"Strict"* in *"Strict 85%+ branch coverage"* is rhetorical padding; the percentage target and threshold operator (`85%+`) define the constraint fully.
* **Consequence**: Adds noise without adding signal.
* **Recommendation**: Edit to:
  > Line 419: *"verify original inspection records and model outputs remain unaltered."*  
  > Line 424: *"Enforce 85%+ branch coverage across..."*
* **Tradeoff**: None.

---

### S9S-10: Uncalibrated reference to non-existent legacy routes
* **Severity**: Nit
* **Affected Scope**: Line 354 (`backend/app/api/v1/router.py`)
* **Vector**: Uncalibrated Claim
* **Editorial Action**: `CALIBRATE`
* **Evidence**:
  ```markdown
  Registers `deliveries.router` under `/api/v1/deliveries` alongside legacy routes (`/inspections`, `/lots`, `/storage`, `/dispatch`, `/settings`).
  ```
* **Style Rationale**: No router file or legacy route handlers currently exist in this repository workspace. Calling them *"legacy routes"* without qualifying that they represent proposed or mock domain routers treats documentation proposals as verified codebase facts.
* **Consequence**: An implementer will expect to find pre-existing router mounts in `backend/app/api/v1/router.py`.
* **Recommendation**: Calibrate the statement:
  > *"Registers `deliveries.router` under `/api/v1/deliveries` on the primary API router aggregator alongside existing or mock domain routers (`/inspections`, `/lots`, `/storage`, `/dispatch`, `/settings`)."*
* **Tradeoff**: Accurately reflects workspace ground truth.

---

### S9S-11: Subjective UI styling description
* **Severity**: Nit
* **Affected Scope**: Line 378 (`frontend/app/deliveries/[id]/trace/page.tsx`)
* **Vector**: Subjective / Hand-Waving UI Phrasing
* **Evidence**:
  ```markdown
  Audit visualization page rendering the interactive provenance tree from delivery through storage slots and export dispatches, prominently badging unresolved gaps in red.
  ```
* **Style Rationale**: *"Prominently badging unresolved gaps in red"* is informal presentation phrasing rather than a functional component specification.
* **Consequence**: Shifts focus from state/data contracts to arbitrary visual styling.
* **Recommendation**: Rephrase to:
  > *"Audit visualization page rendering the interactive provenance tree from delivery intake through storage slots and export dispatches, rendering nodes with unresolved upstream links in an explicit warning state."*
* **Tradeoff**: Focuses on data presentation state rather than hardcoded color choices.

---

### S9S-12: Puffery modifier in implementation phase summary
* **Severity**: Nit
* **Affected Scope**: Line 300 (`Implementation Sequence`, Phase 8)
* **Vector**: Filler Modifier / Wordiness
* **Evidence**:
  ```markdown
  8. **Test Automation**: Add full unit and end-to-end regression suites in `backend/tests/test_delivery_traceability.py` and `backend/tests/test_material_lineage.py`.
  ```
* **Style Rationale**: *"Full"* is an unmeasurable puffery modifier. The scope of testing is defined by the test cases and coverage targets in the Verification Plan, not by asserting a suite is "full".
* **Consequence**: Gives an ungrounded impression of exhaustive coverage.
* **Recommendation**: Rephrase to:
  > *"8. **Test Automation**: Implement unit and integration test suites in `backend/tests/test_delivery_traceability.py` and `backend/tests/test_material_lineage.py`."*
* **Tradeoff**: None.

---

## Next Steps for Main Agent
The identified findings require targeted text edits to lines 288–436 of `docs/designs/nusaqc_delivery_traceability.md`. No architectural redesign is necessary; refining the action verbs, removing defensive fluff, calibrating claims against the empty workspace, and supplying explicit numerical inputs for the verification scenarios will bring the Detailed Implementation Plan into full compliance with the Implementation Readiness Standard.
