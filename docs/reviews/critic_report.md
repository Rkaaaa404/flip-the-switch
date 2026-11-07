# Critic Review Report (Stage 7)

**Target Document**: `docs/designs/nusaqc_delivery_traceability.md`  
**Target Range**: FeatureRange (Lines 1–287)  
**Standard**: `resources/document_standards/feature-spec-standard.md`  
**Reviewers**: `egm-design`, `egm-structural`, `egm-style`  
**Goldfish Context**: `nusaqc-pitchdeck.pdf`, `nusaqc-proposal.pdf`, extracted evaluation tables.  

---

# Part 1: Design Critic Review (`egm-design`)

# Review7Design (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/design_critic.md and C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/feature-spec-standard.md first. Review FeatureRange (lines 1–287) of docs/designs/nusaqc_delivery_traceability.md against the feature spec standard and GoldfishContext. DetailedRange (lines 288–436) may be read for context, but all findings must target the FeatureRange contract. Assign IDs S7D-01 onward. Evaluate failure modes, race conditions, edge cases, scalability, hardware/operational boundary risks, and contract completeness. Include exact reading manifest.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/design_critic.md) ⇒ ok · 64 lines

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/feature-spec-standard.md) ⇒ ok · 40 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-150) ⇒ ok · 165 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:150-287) ⇒ ok · 157 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:288-436) ⇒ ok · 160 lines

## assistant

→ read(nusaqc-proposal.pdf) ⇒ ok · 393 lines

## assistant

→ read(nusaqc-proposal.pdf:195-312) ⇒ ok · 125 lines

## assistant

→ read(nusaqc-proposal.pdf:507-600) ⇒ ok · 58 lines

## assistant

→ read(nusaqc-pitchdeck.pdf) ⇒ ok · 440 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-12-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-13-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-13-X16.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-14-X15.png) ⇒ ok · 3 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-14-X16.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-15-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-16-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-17-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-18-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-20-X15.png) ⇒ ok · 2 lines

## assistant

# Critic Review Report: NusaQC Delivery Traceability Design

* **Reviewer**: Design Critic Goldfish (`Review7Design`)
* **Review Mode**: REVIEW (Document Audit)
* **Target Document**: `docs/designs/nusaqc_delivery_traceability.md`
* **Target Scope**: FeatureRange (Lines 1–287) *(DetailedRange lines 288–436 referenced for context)*
* **Target Standard**: Feature Specification Standard (`feature-spec-standard.md`) & Design Critic Mandate (`design_critic.md`)

---

## Reading Manifest & Review Limitations

### Document & Artifact Reading Manifest
1. **Target Feature Specification**:
   * `docs/designs/nusaqc_delivery_traceability.md`:
     * Primary Audit Target: FeatureRange lines 1–287 (Overview, Problem, Goals, Non-Goals, Open Questions, CUJs, Architecture, Data Model, Pipeline, API, Non-Functional Requirements, Alternatives Considered).
     * Contextual Verification: DetailedRange lines 288–436 (Implementation Sequence, File Declarations, Verification Plan).
2. **Evaluation Standards**:
   * `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/design_critic.md` (Design Critic Mandates).
   * `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/feature-spec-standard.md` (Feature Specification Standard).
3. **Approved Goldfish Context**:
   * `nusaqc-proposal.pdf`: Full document text, Table of Contents, Problem Analysis, System Architecture, Table 1.4.1 (Smart Manufacturing Mapping), Table 3.1 & 3.2.1 (KPIs & Baselines), Section 4.5 (Grading & Decision Logic), Section 5.2 (Two-Model Architecture), Section 6.1 (BOM), Section 7.2 (UI Walkthrough), Section 8.4 (Responsible AI Risk Matrix), Section 8.5 (Risk Register).
   * `nusaqc-pitchdeck.pdf`: Executive Summary, Gap Analysis, Solution Architecture, Unit Economics, Appendix 1–6.
   * **Extracted Empirical Pitchdeck Tables & Figures (Images)**:
     * `pitch-page-12-X15.png`: Test Scenarios & Dataset Matrix.
     * `pitch-page-13-X15.png` & `pitch-page-13-X16.png`: Appendix 2 Initial Benchmark & Failure Mode Stress-Testing.
     * `pitch-page-14-X15.png` & `pitch-page-14-X16.png`: Defect Latency Bottlenecks & Quantization Benchmarks.
     * `pitch-page-15-X6.png`: Appendix 4 Metrics Optimization Before vs. After (Recall, FNR, Latency, Glare, VLM).
     * `pitch-page-16-X6.png`: Comparison Table 1 (AI Model & Edge Engineering Performance, INT8 footprint, CPU latency).
     * `pitch-page-17-X6.png`: Comparison Table 2 (System Architecture & Product Track: Snapshot vs Continuous, RBAC, Golden Samples).
     * `pitch-page-18-X15.png`: Environmental Robustness & Edge Case Table (Low-light, Motion blur, Physical occlusion).
     * `pitch-page-20-X15.png`: Unresolved Technical Edge Cases Matrix (Photon starvation, Partial occlusion, Motion blur, Micro-defects, Cloud VLM latency, Class imbalance).

### Audit Limitations
* **Strict Read-Only Execution**: No implementation code exists in the repository workspace; no source code was compiled, executed, or modified.
* **Empirical Measurements vs. Projections**: Review findings strictly distinguish reported empirical measurements in the approved context (e.g., Raspberry Pi 4 FP32 inference latency of 1,315 ms, baseline defect FNR of 46.39%, low-light Macro F1 collapse to 41.58% under <50 lux, 50% physical occlusion recall drop to 28.00%) from forward-looking design projections and goals (e.g., target 2,400 fish/hour throughput, <1.5s total edge cycle time, <5-minute audit retrieval).

---

## Executive Summary of Findings

| ID | Severity | Category | Target Lines | Summary Description |
| :--- | :---: | :--- | :--- | :--- |
| **S7D-01** | **Blocker** | Concurrency / Physical Reliability | Lines 201–222 | Lack of physical sensor correlation / distance tracking creates fatal FIFO desynchronization. |
| **S7D-02** | **Blocker** | Standard Compliance Gap | Lines 1–287 | Total omission of mandatory `## Risks & Mitigations` section required by Feature Spec Standard. |
| **S7D-03** | **Blocker** | Data Model / Audit Integrity | Lines 152–160, 174–184 | Disconnection between aggregate `human_dispositions` and individual flagged `fish_inspections`. |
| **S7D-04** | **Major** | Performance & Scalability | Lines 204–217, 240–244 | Unbounded thread spawning during sequential inference causes CPU saturation and thermal throttling. |
| **S7D-05** | **Major** | Concurrency / Database | Lines 136–200, 246–248 | Unprotected SQLite write concurrency under concurrent hardware triggers and user mutations. |
| **S7D-06** | **Major** | Security & Compliance | Lines 223–232, 235–239 | Complete absence of authentication, RBAC, and token verification in API contracts. |
| **S7D-07** | **Major** | Infrastructure Economics | Lines 242–243, 237–238 | Edge storage calculation ignores production velocity and lacks automated archival/retention policies. |
| **S7D-08** | **Major** | Data Model Completeness | Lines 185–200, 81–85 | Single `quantity_unit` column prevents cross-unit transformations (`count` to `kg`). |
| **S7D-09** | **Major** | Hardware / CV Failure Mode | Lines 101–103, 210–217 | Passive flipper jams and failure modes lead to uninspected fish falsely certified as `COMPLETE`. |
| **S7D-10** | **Major** | Standard Compliance Gap | Lines 250–287 | Violation of Alternatives Rule: Personal author attributions and omission of core engineering trade-offs. |
| **S7D-11** | **Major** | Operational Robustness | Lines 161–173, 201–222 | Lack of frame quality validation gates against known low-light, blur, and occlusion failure modes. |
| **S7D-12** | **Nit** | Relational Lineage | Lines 185–200 | Strict single-delivery foreign key prevents modeling multi-delivery lot blending/co-mingling. |
| **S7D-13** | **Nit** | Operational State Machine | Lines 149, 225–230 | Undefined lifecycle transition guards and multi-delivery station concurrency rules. |

---

## Detailed Audit Findings

### S7D-01: Lack of Physical Sensor Correlation and Bounded FIFO Tracking Creates Cascade Desynchronization
* **Severity**: **Blocker**
* **Affected Scope**: Lines 201–222 (`### Two-View Conveyor Ingestion Pipeline`)
* **Finding & Technical Description**:
  The two-view pipeline relies on an unverified temporal assumption between two independent proximity sensors: Sensor 1 (dorsal) triggers, allocates sequence $N$, and starts a 3.0-second timer; Sensor 2 (ventral) pulses and simply "cancels timeout timer for sequence $N$" (Line 212). 
  At the target conveyor throughput of 2,400 fish/hour (1 fish every 1.5 seconds) or during physical surge loading, multiple fish simultaneously occupy the physical belt section between Sensor 1, the passive flipper, and Sensor 2. The specification provides **no physical correlation mechanism** (e.g., belt distance encoder / tachometer ticks, spatial tracking, or indexed FIFO queue).
* **Evidence**:
  * Line 209: "Sets pairing timeout timer (3.0s)."
  * Line 212: "Cancels timeout timer for sequence N."
  * Open Question Q1 (Line 52) explicitly notes that passive flipper failure rates and jams are uncharacterized.
  * Pitchdeck Appendix 6 (`pitch-page-20-X15.png`) stresses that fish overlap and travel delays are prominent physical failure modes.
* **Consequence**:
  If a single fish jams in the passive guide block, slips on wet conveyor slats, or falls off the line:
  1. Sensor 2 triggers for Fish $N+1$, but the backend pairs it with sequence $N$.
  2. The dorsal view of Fish $N$ is irrevocably paired with the ventral view of Fish $N+1$.
  3. Every subsequent fish on the conveyor suffers an off-by-one pairing cascade, permanently corrupting the inspection evidence chain for the entire delivery.
* **Recommendation**:
  Do not rely on a naive timestamp timeout. Specify a physical correlation contract:
  1. Integrate a rotary conveyor pulse encoder to measure physical belt displacement between Sensor 1 and Sensor 2.
  2. Maintain an explicit bounded in-flight FIFO queue with positional tracking.
  3. Mandate an immediate conveyor halt signal via relay and alert operator when an unexpected sensor pulse sequence or position anomaly is detected.
* **Tradeoff**:
  Requires an additional hardware sensor input (rotary encoder or dual-beam gate) and state machine logic, slightly increasing hardware integration complexity.

---

### S7D-02: Total Omission of Mandatory `## Risks & Mitigations` Section Mandated by Standard
* **Severity**: **Blocker**
* **Affected Scope**: Lines 1–287 (`docs/designs/nusaqc_delivery_traceability.md`)
* **Finding & Technical Description**:
  The Feature Specification Standard explicitly establishes:
  > *"Risks & Limits: The specification must explicitly call out its own constraints. It must identify potential failure modes, security implications, scalability limits, and how they will be mitigated."*
  > *"Requirements: ... Risks & Mitigations: Identified security, scalability, or complexity risks."*
  
  FeatureRange (lines 1–287) contains `## Open Questions` (Lines 50–59) and brief `### Non-Functional Requirements` (Lines 233–249), but **completely omits a dedicated `## Risks & Mitigations` section**. Known critical risks documented in the project's background—such as photon starvation in low light, partial body occlusion, conveyor motion blur, Raspberry Pi thermal throttling, and sensor desynchronization—are absent from the architectural risk analysis.
* **Evidence**:
  * `feature-spec-standard.md`, Lines 23–27 & 38–39.
  * `docs/designs/nusaqc_delivery_traceability.md`, Lines 1–287 table of contents and headings.
  * `nusaqc-pitchdeck.pdf`, Appendix 6 (`pitch-page-20-X15.png`), which contains a detailed matrix of 6 major technical failure modes.
* **Consequence**:
  The specification violates the governing quality standard. Engineering implementation will proceed without binding architectural mitigations for known physical, hardware, and operational failure modes.
* **Recommendation**:
  Insert a formal `## Risks & Mitigations` section into FeatureRange directly preceding `## Alternatives Considered`. Detail each operational, security, scalability, and algorithmic risk alongside concrete architectural safeguards.
* **Tradeoff**:
  Expands the length of the specification document, but ensures structural compliance and risk visibility.

---

### S7D-03: Disconnection Between Aggregate Human Dispositions and Individual Flagged Fish Inspections
* **Severity**: **Blocker**
* **Affected Scope**: Lines 152–160 (`fish_inspections`), Lines 174–184 (`human_dispositions`), Line 229 (`API Endpoints`)
* **Finding & Technical Description**:
  A core goal of NusaQC is creating an unbroken evidence chain where human decisions do not overwrite AI findings (Goal 3, Line 32; CUJ 2, Lines 68–73). However, the relational data model breaks this link:
  * `fish_inspections` flags individual fish (`flagged_for_review = TRUE`, `flag_reasons_json`).
  * `human_dispositions` links *only* to `delivery_id` (`VARCHAR(64)` NOT NULL FK -> `receiving_deliveries.id`) and records an aggregate quantity (`affected_quantity: FLOAT`, `disposition: ACCEPT|REJECT|REPROCESS|DOWNGRADE`).
  
  There is **no foreign key, association table, or array linking `human_dispositions` to specific `fish_inspections.id` records**.
* **Evidence**:
  * Lines 152–160: `fish_inspections` schema lacks any `disposition_id` or resolution state.
  * Lines 174–184: `human_dispositions` schema contains `delivery_id`, but zero reference to individual fish inspection IDs.
  * Line 229: `POST /api/v1/deliveries/{id}/dispositions` payload contains only `{output_lot_id, disposition, affected_quantity, quantity_unit, decision_reason, authorized_by}`.
* **Consequence**:
  If a delivery has 20 flagged fish with visible ulcer lesions or decay, and the supervisor logs a disposition of `REJECT 15 kg`, the system cannot determine *which* of the flagged fish were rejected, accepted, or reprocessed. When an export auditor or buyer inspects a specific flagged fish photograph, the platform cannot prove its ultimate fate, invalidating the core traceability value proposition.
* **Recommendation**:
  Establish an explicit relational link between human dispositions and fish inspections:
  1. Add an association table `disposition_inspection_items (disposition_id INT FK, fish_inspection_id INT FK, resolution VARCHAR(32))`, or
  2. Add `disposition_id INT NULL FK -> human_dispositions.id` and `resolution_status VARCHAR(32)` directly to `fish_inspections`.
* **Tradeoff**:
  Requires the QC dashboard to submit itemized or batch-selected fish IDs upon recording dispositions, rather than entering a single bulk number.

---

### S7D-04: Unbounded Background Thread Ingestion Causes CPU Saturation and Thermal Throttling
* **Severity**: **Major**
* **Affected Scope**: Lines 204–217 (`Two-View Conveyor Ingestion Pipeline`), Lines 240–244 (`Performance & Capacity Envelope`)
* **Finding & Technical Description**:
  Lines 204 and 211 specify that upon each sensor pulse, a "Background thread" computes SHA-256, writes the image to disk, and executes MobileNetV3 + YOLOv8s sequentially (~650–800 ms CPU time per frame, ~1.5s total execution per fish).
  At production rates of 2,400 fish/hour (1 fish every 1.5 seconds) or when fish arrive in quick succession (e.g., 0.8s apart), spawning unthrottled background threads on a quad-core ARM CPU (Raspberry Pi 5) will cause severe CPU core contention, thermal throttling, and thread explosion. If 4 fish pass in 3 seconds, 8 heavy ONNX vision processes will compete for 4 CPU cores, increasing per-frame inference latency far beyond 1.5s.
* **Evidence**:
  * Line 204: "Sensor 1 pulses on fish arrival... Background thread: Computes SHA-256... Executes MobileNetV3... and YOLOv8s..."
  * Line 241: "Sequential MobileNetV3 (150–300 ms) + YOLOv8s (470 ms) yields ~650–800 ms total CPU execution per frame... Total two-view inference execution is ~1.5 s per fish."
  * Pitchdeck Appendix 2 & 3 (`pitch-page-14-X16.png`, `pitch-page-15-X6.png`): Unoptimized CPU execution suffered from 1,315 ms to 2,739 ms latency bottlenecks.
* **Consequence**:
  CPU starvation causes the background execution of Sensor 1 to stall. Consequently, Sensor 2's 3.0-second timeout timer (Line 218) will prematurely fire and mark healthy fish as `PARTIAL_DORSAL_ONLY`, flooding the review dashboard with false anomalies and degrading factory throughput.
* **Recommendation**:
  Replace ad-hoc background thread creation with an explicit, bounded worker architecture:
  1. Decouple high-priority I/O (capturing frame, SHA-256, and saving raw image) from CPU-intensive inference.
  2. Direct captured image references into a bounded FIFO inference queue (`asyncio.Queue` or worker pool with max 2 concurrent ONNX inference workers).
  3. Anchor timeout evaluations to physical conveyor travel rather than wall-clock inference completion.
* **Tradeoff**:
  Inference results may lag real-time display by 1–2 seconds during surge arrivals, but system stability, thermal safety, and deterministic pairing are guaranteed.

---

### S7D-05: Unprotected SQLite Write Concurrency Under Multi-Source Operational Mutations
* **Severity**: **Major**
* **Affected Scope**: Lines 136–200 (`Data Model & Relational Schema`), Lines 246–248 (`Rollout & Backward Compatibility`)
* **Finding & Technical Description**:
  The architecture designates SQLite as the sole operational datastore while introducing multiple concurrent asynchronous write paths:
  1. Sensor 1 background thread inserting `fish_inspections` and `inspection_views`.
  2. Sensor 2 background thread updating `fish_inspections` and inserting `inspection_views`.
  3. Async timeout reaper updating timed-out records.
  4. Dock intake operator creating and updating `receiving_deliveries`.
  5. QC supervisor posting `human_dispositions`.
  6. Line operators submitting `material_movements`.
  
  Under SQLite's default rollback journal mode (`DELETE`), any write transaction locks the entire database file exclusively. The specification fails to define database concurrency controls, transaction isolation, or busy handler configurations.
* **Evidence**:
  * Lines 136–200: Schema definition mentions SQLite with zero pragma configurations.
  * Lines 223–232: Seven concurrent read/write REST endpoints.
* **Consequence**:
  Under active conveyor operation, rapid database writes from camera trigger threads will collide with supervisor form submissions, triggering unhandled `sqlite3.OperationalError: database is locked` exceptions and 500 API responses.
* **Recommendation**:
  Mandate SQLite industrial concurrency settings in Section 240:
  1. Enforce Write-Ahead Logging: `PRAGMA journal_mode = WAL;`.
  2. Set a busy timeout handler: `PRAGMA busy_timeout = 5000;` (5 seconds).
  3. Enforce `PRAGMA synchronous = NORMAL;` to maintain write throughput without compromising file durability.
  4. Specify an explicit transactional retry decorator with exponential backoff on all API database sessions.
* **Tradeoff**:
  WAL mode generates `-wal` and `-shm` auxiliary files requiring proper filesystem permissions and regular checkpointing.

---

### S7D-06: Complete Absence of Authentication, RBAC, and Token Verification in API Contracts
* **Severity**: **Major**
* **Affected Scope**: Lines 223–232 (`API Endpoints`), Lines 235–239 (`Security & Attributability`)
* **Finding & Technical Description**:
  Non-functional requirement 1 states: *"Every disposition and material movement record requires an authenticated `authorized_by` or `operator_id`"* (Line 236).
  However, the API endpoint specifications in lines 225–230 define:
  * `POST /api/v1/deliveries/{id}/dispositions` accepting `{..., authorized_by}` as a plaintext JSON payload attribute.
  * `POST /api/v1/deliveries/{id}/movements` accepting `{..., operator_id}` as a plaintext JSON payload attribute.
  * `POST /api/v1/deliveries/{id}/capture-view` accepting raw trigger uploads with zero token or hardware signature.
  
  There is no specification of HTTP `Authorization: Bearer <token>` headers, JWT/session validation, badge PIN verification, or Role-Based Access Control (RBAC).
* **Evidence**:
  * Lines 228–230: Request payloads allow client-controlled identity strings.
  * Pitchdeck Comparison Table 2 (`pitch-page-17-X6.png`, Pillar 6) explicitly highlights a requirement for: *"Role-Based Access Control (4 Roles: Admin, Supervisor, PPIC, Staff)"*.
* **Consequence**:
  Any station tablet, browser client, or device on the plant LAN can forge supervisor credentials, falsify dispositions, or alter transformation yields without cryptographic proof or non-repudiation. This violates export audit standards (FDA 21 CFR Part 11).
* **Recommendation**:
  1. Remove `authorized_by` and `operator_id` from request JSON bodies; derive user identity securely from verified JWT claims via FastAPI dependencies (`Depends(get_current_user)`).
  2. Define the 4 RBAC roles (Admin, Supervisor, PPIC, Staff) and bind them to endpoint operations (e.g., only `Supervisor` may write dispositions; only `Staff`/`PPIC` may record movements).
  3. Secure internal hardware trigger endpoints (`/capture-view`) with a preshared station secret or mutual TLS.
* **Tradeoff**:
  Requires implementing an authentication provider/session service and user login state in the frontend.

---

### S7D-07: Edge Storage Budget Ignores Production Velocity and Lacks Retention / Archival Policy
* **Severity**: **Major**
* **Affected Scope**: Lines 242–243 (`Storage Budget`), Lines 237–238 (`Security & Attributability`), Line 58 (`Open Question Q7`)
* **Finding & Technical Description**:
  Line 242 calculates an image footprint of ~600 MB per 1,000 fish (300 KB $\times$ 2 views) and mandates a pre-capture check requiring at least 10 GB of free disk space.
  However, at the project's target throughput of 2,400 fish/hour (Proposal Table 3.2.1), an 8-hour production shift processes 19,200 fish, generating **11.52 GB of raw JPEG images per day**. On a standard 32 GB or 64 GB Raspberry Pi MicroSD card, local disk space will be completely exhausted within 2 to 4 days of operation.
  Furthermore, Line 237 dictates that image deletion is disabled while referenced by open records, and Open Question Q7 (Line 58) admits retention and backup ownership are unresolved.
* **Evidence**:
  * Line 242: "Storage volume must enforce a pre-capture check requiring at least 10 GB free disk space before initiating an active delivery session."
  * Line 237: "Image artifacts are append-only. Deletion of historical inspection images is disabled while referenced by an open delivery, disposition, or dispatch record."
  * Proposal Table 3.2.1: Throughput target $\ge 2,400\text{ fish/hour}$.
* **Consequence**:
  Within days of deployment, the Raspberry Pi will hit the 10 GB safety limit, causing `POST /api/v1/deliveries` to reject all incoming deliveries and shutting down the receiving dock.
* **Recommendation**:
  Formulate a concrete storage lifecycle policy in the specification:
  1. Local storage on the edge device must function as a circular buffer retaining raw images for a fixed window (e.g., 72 hours).
  2. Implement an automated background archival worker that syncs completed delivery bundles (images + checksums) to an external factory NAS, on-premise server, or object storage (MinIO/S3).
  3. Allow local pruning of verified, synced images while preserving checksums and metadata in SQLite.
* **Tradeoff**:
  Requires an active network uplink to local factory storage or a high-capacity external SSD mounted to the Raspberry Pi.

---

### S7D-08: Single `quantity_unit` in `material_movements` Prevents Cross-Unit Processing Transformations
* **Severity**: **Major**
* **Affected Scope**: Lines 185–200 (`material_movements`), Lines 81–85 (`CUJ 4`)
* **Finding & Technical Description**:
  Table `material_movements` defines a single unit column: `quantity_unit VARCHAR(16) NOT NULL` (`kg` or `count`). This single unit governs `quantity_in`, `quantity_out`, `normal_yield_loss`, `qc_reject_loss`, and `unexplained_variance`.
  However, in fish processing plants (and explicitly acknowledged in CUJ 4, Line 84: *"Fish count and weight are recorded in agreed units; they are not automatically converted"*), materials frequently enter a stage measured in whole fish **`count`** (e.g., 500 whole tilapia from receiving) and exit filleting or WGGS processing measured in **`kg`** (e.g., 320 kg fillets).
* **Evidence**:
  * Line 193: `quantity_unit` (`VARCHAR(16)` NOT NULL): Unit of measure (`kg` or `count`).
  * Lines 191–196: Single unit applied across both inputs and outputs.
  * Line 84 (CUJ 4): "Fish count and weight are recorded in agreed units; they are not automatically converted."
* **Consequence**:
  Because inputs and outputs cannot have differing units in a single movement record, the mass/count balance equation ($\text{in} = \text{out} + \text{losses} + \text{variance}$) cannot be computed when converting count to mass. Operators will be forced to falsify records or calculate external ad-hoc conversion estimates.
* **Recommendation**:
  Update `material_movements` schema to support unit transitions:
  1. Define explicit `unit_in` and `unit_out` columns, or
  2. Provide dual columns: `count_in`, `weight_kg_in`, `count_out`, and `weight_kg_out`, with explicit declaration of nominal conversion factors where biological transformations cross unit boundaries.
* **Tradeoff**:
  Adds minor schema width, but eliminates balance accounting errors.

---

### S7D-09: Passive Inversion Jamming and Slippage Cause Falsified Ventral Classifications
* **Severity**: **Major**
* **Affected Scope**: Lines 101–103 (`ConveyorHardware`), Lines 210–217 (`Passive Inversion & Ventral Trigger`), Line 52 (`Open Question Q1`)
* **Finding & Technical Description**:
  The physical conveyor design assumes a 100% mechanical inversion rate through a passive guide block (Line 210). When Sensor 2 pulses, the pipeline unconditionally records the captured image as `view_side = ventral` (Line 215) and marks the inspection as `COMPLETE` (Line 217).
  However, real-world wet fish with varying slime layers, stiff fins, or curved spines frequently fail to flip 180 degrees—sliding through on their dorsal side, rotating 90 degrees, or jamming. If a fish fails to flip, Camera 2 captures a second dorsal frame. The system blindly labels it `ventral`, marks the fish `COMPLETE`, and certifies two-view inspection compliance even though the ventral side was never photographed.
* **Evidence**:
  * Line 210: "3. Passive Inversion: Fish moves through the Japanese passive guide block, flipping 180 degrees onto its ventral side."
  * Line 215: "Writes inspection_views row for view_side = ventral."
  * Line 217: "Sets fish_inspections.status = COMPLETE."
  * Open Question Q1 (Line 52): "What is the failure rate, and how are misflipped or jammed fish handled without blocking the line?"
* **Consequence**:
  Ventral defects (such as belly burst, visceral discoloration, or ventral parasite lesions) will bypass inspection completely, while the platform produces an audit report falsely asserting that full two-view verification occurred.
* **Recommendation**:
  1. Implement a lightweight anatomical orientation check in the vision pipeline to verify that ventral anatomical landmarks (vent, pelvic fins, belly contour) are visible before accepting the frame as `ventral`.
  2. If orientation is ambiguous or dorsal features recur, classify the record as `PARTIAL_DORSAL_ONLY` with flag `INVERSION_FAILED`, routing the fish to a manual inspection or recirculation lane.
* **Tradeoff**:
  Requires an additional pose/feature verification step in the edge vision pipeline.

---

### S7D-10: Violation of Alternatives Rule and Omission of Core Engineering Trade-offs
* **Severity**: **Major**
* **Affected Scope**: Lines 250–287 (`## Alternatives Considered`)
* **Finding & Technical Description**:
  The Feature Specification Standard strictly mandates:
  > *"The specification must include a mandatory evaluation of alternatives. It fails this standard if it proposes a single path without proving that other viable designs were considered and rejected for specific, documented reasons... Rejection rationales must state concrete technical or scope trade-offs and must not attribute a rejection to a maintainer without linking their issue, discussion, or PR."*
  
  The current specification fails this rule in two critical ways:
  1. Every single rejection rationale (Lines 256, 262, 268, 274, 280) attributes the decision to personal author fiat (*"Rejected by author"*, *"Deferred by author"*) without linking issues, RFCs, or PRs.
  2. The alternatives analyzed (Automated Direct Loss, RFID Fish Tagging, Full ERP Replacement, Handheld Gun, Recall Room, Paper Tally Sheets) are macro-level product scope boundaries rather than **system engineering alternatives** for the feature being specified. Key engineering alternatives—such as (a) Simultaneous dual cameras with optical mirrors vs. passive mechanical flipper, (b) Local SQLite vs. embedded DuckDB vs. client-server PostgreSQL, (c) Polling triggers vs. message queues (e.g. MQTT/Redis Streams), and (d) Filesystem storage vs. SQLite BLOBs—are completely omitted.
* **Evidence**:
  * `feature-spec-standard.md`, Lines 13–22.
  * `docs/designs/nusaqc_delivery_traceability.md`, Lines 250–287.
* **Consequence**:
  The document fails the Feature Specification Standard and lacks documented justification for its primary hardware, database, and queuing architecture decisions.
* **Recommendation**:
  Rewrite Section 250:
  1. Remove all personal *"by author"* phrases and replace them with objective technical and economic trade-offs.
  2. Replace conceptual strawmen with real engineering alternatives (e.g., Optical mirror single-camera chute vs. dual-camera mechanical flipper; SQLite vs. DuckDB/PostgreSQL for transformation lineage trees).
* **Tradeoff**:
  Requires drafting substantive technical trade-off comparisons for core subsystem choices.

---

### S7D-11: Lack of Frame Quality Validation Gates Against Known Low-Light, Blur, and Occlusion Failure Modes
* **Severity**: **Major**
* **Affected Scope**: Lines 161–173 (`inspection_views`), Lines 201–222 (`Ingestion Pipeline`)
* **Finding & Technical Description**:
  Empirical stress-testing of NusaQC on real fish lines (Pitchdeck Appendix 6, `pitch-page-18-X15.png` and `pitch-page-20-X15.png`) revealed acute environmental degradation:
  * Low-light (<50 lux) caused freshness classification Macro F1 to collapse from 96.07% to 41.58% due to chromatic contrast loss.
  * Conveyor motion blur (>15 cm/s) dropped defect recall to 40.00%.
  * Physical occlusion (>50% stacked fish) dropped defect recall to 28.00%.
  * Micro-defects (<15 px) experienced 0% detection due to NMS post-processing filtering.
  
  Despite these documented failure modes, the ingestion pipeline (Lines 201–222) contains **zero pre-inference image validation gates**. If a factory lamp burns out, water splashes on the lens, or fish overlap on the belt, the pipeline blindly executes MobileNetV3 and YOLOv8s, generating high-confidence false passes.
* **Evidence**:
  * Lines 161–173: `inspection_views` records grades and defects, but has no field for image quality, lux, or sharpness score.
  * Pitchdeck Appendix 6 (`pitch-page-18-X15.png`, `pitch-page-20-X15.png`).
* **Consequence**:
  Severe defect escapes (high FNR) during routine plant disturbances (e.g., conveyor speed shifts, dim lighting, lens misting) while falsely recording Grade A compliance.
* **Recommendation**:
  Introduce a deterministic pre-inference image quality filter in the ingestion pipeline:
  1. Calculate mean luminance ($Y$ channel in YUV/LAB) and blur score (Laplacian variance).
  2. If luminance < 50 lux or blur exceeds threshold, reject the frame immediately: set status to `FAILED_CAPTURE` with flag `UNREADABLE_IMAGE_QUALITY`.
  3. Emit an operator warning and route the uninspected fish to manual QC without running inference or logging misleading grades.
* **Tradeoff**:
  Adds ~10 ms of CPU image processing per frame, but prevents corrupted inferences from entering export audit logs.

---

### S7D-12: Strict Single-Delivery Foreign Key Prevents Multi-Delivery Lot Co-Mingling
* **Severity**: **Nit**
* **Affected Scope**: Lines 185–200 (`material_movements`)
* **Finding & Technical Description**:
  In `material_movements`, `delivery_id` is defined as `VARCHAR(64) NOT NULL FK -> receiving_deliveries.id`.
  In fish processing plants, raw materials from multiple small supplier deliveries (e.g., DEL-01 and DEL-02) are regularly co-mingled into a single processing batch (e.g., 2,000 kg filleting run) or consolidated into a shared cold storage lot. Constraining each movement row to a single non-nullable `delivery_id` makes it impossible to model many-to-one or many-to-many lineage relationships.
* **Evidence**:
  * Line 187: `delivery_id` (`VARCHAR(64)` NOT NULL FK -> `receiving_deliveries.id`).
* **Consequence**:
  Processing runs combining multiple deliveries cannot be cleanly recorded in the journal, forcing operators to invent artificial lot divisions.
* **Recommendation**:
  Allow `delivery_id` to be nullable on downstream movements, or introduce a junction table `movement_input_deliveries (movement_id INT FK, delivery_id VARCHAR(64) FK, contributed_quantity FLOAT)`.
* **Tradeoff**:
  Slightly complicates lineage tree traversal queries.

---

### S7D-13: Undefined State Machine Lifecycle and Station Concurrency Rules
* **Severity**: **Nit**
* **Affected Scope**: Line 149 (`receiving_deliveries.status`), Lines 225–230 (`API Endpoints`)
* **Finding & Technical Description**:
  Line 149 lists delivery statuses: `active_receiving`, `inspection_complete`, `disposition_recorded`, `closed`. However, the specification lacks:
  1. A formal state transition diagram detailing which API endpoints trigger each transition.
  2. Rules on whether states are terminal or reversible (e.g., can inspections continue after `inspection_complete`?).
  3. Station concurrency rules: Can an inspection station support two concurrent open deliveries (e.g. alternating species on two shifts), or is the station strictly single-tenant? (Line 203 refers to setting "station context in memory").
* **Evidence**:
  * Line 149, Line 203, Lines 225–230.
* **Consequence**:
  Risk of race conditions and illegal workflow sequencing, such as logging material movements before dispositions are finalized.
* **Recommendation**:
  Define a formal state transition table with explicit pre-conditions and post-conditions for all delivery status transitions.
* **Tradeoff**:
  Requires enforcing strict validation logic in the delivery service state machine.

---

## Conclusion & Next Steps for Main Agent

The FeatureRange of `docs/designs/nusaqc_delivery_traceability.md` lays a clear functional foundation for separating AI visual observations from human quality decisions. However, it currently contains **three Blocker-level architectural flaws**:
1. It relies on a fragile timer-based sensor pairing mechanism that guarantees cascade desynchronization upon physical jams (**S7D-01**).
2. It completely omits the mandatory `## Risks & Mitigations` section required by the Feature Specification Standard (**S7D-02**).
3. It fails to relationally connect human dispositions to individual flagged fish, compromising audit traceability (**S7D-03**).

These issues, along with the edge CPU starvation (**S7D-04**), SQLite lock contention (**S7D-05**), and API security vulnerabilities (**S7D-06**), must be remediated in the feature contract before implementation commences.

---

# Part 2: Structural Review (`egm-structural`)

# Review7Structure (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/structural.md and C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/feature-spec-standard.md first. Review FeatureRange (lines 1–287) of docs/designs/nusaqc_delivery_traceability.md. Check section presence, ordering, heading hierarchy, template compliance, and structural consistency. Avoid personal stylistic preferences unsupported by the feature-spec standard. Assign IDs S7R-01 onward. Include exact reading manifest.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/structural.md) ⇒ ok · 66 lines

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/feature-spec-standard.md) ⇒ ok · 40 lines

## assistant

→ glob(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/*) ⇒ ok · 6 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-150) ⇒ ok · 165 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:150-290) ⇒ ok · 160 lines

## assistant

→ read(nusaqc-proposal.pdf) ⇒ ok · 393 lines

## assistant

→ read(nusaqc-proposal.pdf:190-315) ⇒ ok · 133 lines

## assistant

→ read(nusaqc-proposal.pdf:500-507) ⇒ ok · 15 lines

## assistant

→ read(nusaqc-proposal.pdf:508-562) ⇒ ok · 57 lines

## assistant

→ read(nusaqc-pitchdeck.pdf) ⇒ ok · 440 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-12-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-13-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-13-X16.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-14-X15.png) ⇒ ok · 3 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-14-X16.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-15-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-16-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-17-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-18-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-20-X15.png) ⇒ ok · 2 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-70) ⇒ ok · 80 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:74-150) ⇒ ok · 98 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:200-288) ⇒ ok · 110 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:288-436) ⇒ ok · 160 lines

## assistant

→ grep(\| @ docs/designs/nusaqc_delivery_traceability.md:1-287) ⇒ ok · 33 lines

## assistant

→ grep(``` @ docs/designs/nusaqc_delivery_traceability.md:1-287) ⇒ ok · 12 lines

## assistant

→ grep(http @ docs/designs/nusaqc_delivery_traceability.md:1-287) ⇒ ok · 1 line

## assistant

→ grep(\]\( @ docs/designs/nusaqc_delivery_traceability.md:1-287) ⇒ ok · 1 line

## assistant

### Reading Manifest & Audit Limitations

#### 1. Documents & Standards Read
*   **Structural Agent Specification**: `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/structural.md` (lines 1–65).
*   **Target Standard**: `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/feature-spec-standard.md` (lines 1–39).
*   **Target Review Scope**: `docs/designs/nusaqc_delivery_traceability.md` (FeatureRange: lines 1–287 audited in detail; lines 288–436 read for structural boundary context).
*   **Approved Context PDF 1**: `D:/main/Documents/explore/compe/hackhathon/flip-the-switch/nusaqc-proposal.pdf` (all 27 pages read in full; lines 1–562).
*   **Approved Context PDF 2**: `D:/main/Documents/explore/compe/hackhathon/flip-the-switch/nusaqc-pitchdeck.pdf` (all 23 pages read in full; lines 1–439).
*   **Extracted Image-Only Tables from Pitch Deck**:
    *   `pitch-page-12-X15.png`: Appendix 2 — Initial Test Suite & Baseline Metrics.
    *   `pitch-page-13-X15.png`: Appendix 2 — Module Performance Benchmark Summary.
    *   `pitch-page-13-X16.png`: Appendix 2 — Technical Root Cause Deconstruction.
    *   `pitch-page-14-X15.png`: Appendix 2 — Class Precision & Latency Bottleneck Table.
    *   `pitch-page-14-X16.png`: Appendix 2 — Quantization Optimization Summary.
    *   `pitch-page-15-X6.png`: Appendix 4 — Metrics Optimization: Before vs After.
    *   `pitch-page-16-X6.png`: Comparison Table 1 — AI Model & Edge Engineering Performance.
    *   `pitch-page-17-X6.png`: Comparison Table 2 — System Architecture & Product Track.
    *   `pitch-page-18-X15.png`: Environmental Robustness & Edge Case Table.
    *   `pitch-page-20-X15.png`: Unresolved Technical Edge Cases Matrix.

#### 2. Audit Scope & Operational Limitations
*   **Read-Only Boundary**: No modifications, compilations, test executions, or external repository accesses were conducted.
*   **Grounding**: All findings evaluate document layout, heading hierarchy, template compliance, and structural symmetry against `feature-spec-standard.md`. No empirical or measured code execution behavior is claimed or implied.

---

### Heading Hierarchy Map (FeatureRange: Lines 1–287)

```text
# NusaQC — Incoming Inspection and Traceable Factory Records (H1, Line 1)
├── [Metadata Block: Author, Status, Date] (Lines 3–5)
├── ## Overview (H2, Line 9)
├── ## The Problem (H2, Line 15)
├── ## Goals (H2, Line 28)
├── ## Non-Goals (H2, Line 38)
├── ## Open Questions (H2, Line 50)
├── ## Critical User Journeys (CUJs) (H2, Line 60)
│   ├── ### CUJ 1: Register an incoming delivery and begin inspection (H3, Line 62)
│   ├── ### CUJ 2: Review AI findings and record a human disposition (H3, Line 68)
│   ├── ### CUJ 3: Trace a delivery through storage and dispatch (H3, Line 74)
│   └── ### CUJ 4: Record a processing handoff and quantity outcome (H3, Line 80)
├── ## Technical Plan (Architecture) (H2, Line 86)
│   ├── ### System Architecture & Boundaries (H3, Line 88)
│   ├── ### Data Model & Relational Schema (H3, Line 136)
│   ├── ### Two-View Conveyor Ingestion Pipeline (H3, Line 201)
│   ├── ### API Endpoints (FastAPI Backend) (H3, Line 223)
│   └── ### Non-Functional Requirements (H3, Line 233)
│       ├── #### 1. Security & Attributability (H4, Line 235)
│       ├── #### 2. Performance & Capacity Envelope (H4, Line 240)
│       └── #### 3. Rollout, Backward Compatibility & Rollback (H4, Line 245)
└── ## Alternatives Considered (H2, Line 250)
    ├── ### Alternative A: Automated Direct Loss (...) (H3, Line 252)
    ├── ### Alternative B: Individual Fish Tagging (...) (H3, Line 258)
    ├── ### Alternative C: Full Factory ERP & Inventory Management Replacement (H3, Line 264)
    ├── ### Alternative D: Handheld Optical Inspection Gun (...) (H3, Line 270)
    ├── ### Alternative E: Proceeding Directly to Incident Response Workflow (...) (H3, Line 276)
    └── ### Alternative F: Paper Tally Sheets and Manual Photo Folders (H3, Line 282)
[Line 288 initiates Detailed Implementation Plan]
```

---

### Structural Review Findings

#### S7R-01: Missing Mandatory Section — "Risks & Mitigations" (or "Risks & Limits")
*   **Severity**: Major
*   **Affected Scope**: Lines 1–287 (Global Feature Spec Structure; omission at Section Boundary before line 288)
*   **Discrepancy Description & Rationale**:
    `feature-spec-standard.md` explicitly mandates a dedicated evaluation of risks and constraints:
    > *"## Risks & Limits: The specification must explicitly call out its own constraints. It must identify potential failure modes, security implications, scalability limits, and how they will be mitigated."*
    > *"## Requirements (Non-Exhaustive Examples): ... Risks & Mitigations: Identified security, scalability, or complexity risks."*
    In `docs/designs/nusaqc_delivery_traceability.md`, FeatureRange (lines 1–287) completely lacks a top-level `## Risks & Mitigations` or `## Risks & Limits` section. While lines 233–249 detail select non-functional requirements (security, inference overhead, storage budget, rollout), critical operational and physical failure modes documented in the proposal and pitchdeck (e.g., passive guide mechanical jams, conveyor belt speed motion blur, optical low-light collapse under $<50$ lux, 50% partial body occlusion blind spots, disk fill-up mid-session, and SQLite concurrent write lock contention) are never addressed or mitigated in a dedicated risks section.
*   **Evidence**: Inspection of all H2 sections between lines 1 and 287 reveals `Overview`, `The Problem`, `Goals`, `Non-Goals`, `Open Questions`, `Critical User Journeys`, `Technical Plan (Architecture)`, and `Alternatives Considered`, but no section for `Risks & Mitigations`.
*   **Consequence**: The specification omits a core required section from the standard, leaving engineering implementers without a consolidated reference for anticipated system failure modes and mitigation mechanisms.
*   **Recommendation**: Add a dedicated top-level section `## Risks & Mitigations` immediately following `## Alternatives Considered` (or expand Section 233 into `## Risks, Limits & Mitigations`), formalizing the physical edge cases (guide jamming, optical occlusion, low-light), data storage thresholds, and operational mitigations.
*   **Tradeoff**: Increases document length by ~30–40 lines, but ensures full compliance with the feature-spec standard.

---

#### S7R-02: Structural Ordering Contradiction and Stale Inquiries in "Open Questions"
*   **Severity**: Major
*   **Affected Scope**: Lines 50–59 (`## Open Questions`) vs Lines 84, 138, 147, 193, 247 (`### Data Model & Relational Schema` and `### Non-Functional Requirements`)
*   **Discrepancy Description & Rationale**:
    `## Open Questions` is placed at lines 50–59, ahead of `Critical User Journeys` and the `Technical Plan (Architecture)`. This creates forward dependencies on concepts not yet defined. More critically, the text contains direct internal contradictions:
    1. Line 56 poses **Q5**: *"Can the original nusaqc.db inspection records be retained as historical observations without being promoted to receiving-linked, quantity-bearing records? Or must they be migrated?"* However, line 138 already settles this: *"The SQLite schema is expanded with five purpose-built tables that leave legacy inspection rows intact as historical observations"*, and line 247 confirms: *"Historical Data Isolation: Existing rows in inspections retain their historical values. They are marked as legacy_observation records and not synthesized into artificial delivery sessions."*
    2. Line 55 poses **Q4**: *"Does the factory measure receiving quantities in fish count, weight, or both?"* However, lines 84, 147, and 193 have already formalized the schema: `quantity_unit: VARCHAR(16) NOT NULL: kg or count`, explicitly stating fish count and weight are recorded in agreed units without automatic conversion.
*   **Evidence**: Compare line 56 with line 138/line 247, and line 55 with line 84/line 147/line 193.
*   **Consequence**: Posing questions as "open" when the architecture has already resolved and codified them creates confusion over whether the data model is settled or speculative.
*   **Recommendation**:
    1. Move `## Open Questions` after the Technical Plan (or incorporate unresolved items into `Risks & Mitigations`).
    2. Remove answered questions Q4 and Q5, and re-scope the remaining questions (Q1, Q2, Q3, Q6, Q7) around genuine factory integration variables.
*   **Tradeoff**: Requires pruning resolved queries and shifting section position, but eliminates internal contradictions.

---

#### S7R-03: Template Contradiction in Alternative F and Subjective Rejection Prefixes
*   **Severity**: Major
*   **Affected Scope**: Lines 250–287 (`## Alternatives Considered`, specifically lines 256, 262, 268, 274, 280, 286)
*   **Discrepancy Description & Rationale**:
    The section violates the structural template and the Alternatives Rule defined in `feature-spec-standard.md`:
    1. **Structural Contradiction in Alternative F (lines 282–286)**: The subsection is titled `### Alternative F: Paper Tally Sheets and Manual Photo Folders`. However, line 286 states: `* **Reason for Rejection**: Retained as the baseline comparison case (not outright rejected).` Categorizing an operational baseline that is explicitly *retained* under a list of *rejected alternatives*, while using a label called *Reason for Rejection* that claims it is *not* rejected, is an oxymoronic structural contradiction.
    2. **Subjective Maintainer Attribution (lines 256, 262, 268, 274, 280)**: Every rejection rationale begins with `Rejected by author:` or `Deferred by author:`, attributing the technical decision to subjective author fiat rather than stating objective technical, economic, or physical constraints directly. The standard explicitly states: *"Rejection rationales must state concrete technical or scope trade-offs and must not attribute a rejection to a maintainer without linking their issue, discussion, or PR."* Additionally, line 256 cites *"real-world factory interviews"* without linking or referencing the specific discovery interview notes (e.g., PT Dimas Reiza Perwira interview documentation in Appendix 6).
*   **Evidence**: Lines 256, 262, 268, 274, 280, 286.
*   **Consequence**: Weakens the objective rigor of the alternatives analysis, violates the explicit wording of the Alternatives Rule, and conflates comparison baselines with rejected technical architectures.
*   **Recommendation**:
    1. In Alternative F, explicitly declare the rejection for production records (e.g., *"Rejected as an acceptable operational mechanism for export-grade compliance due to 5-minute retrieval failure and data loss risks, but maintained as an offline comparison baseline for pilot benchmarking"*).
    2. Remove `Rejected by author:` and `Deferred by author:` prefixes. Phrase rationales strictly around technical, physical, and operational trade-offs, citing interview findings directly.
*   **Tradeoff**: Minor textual refactoring with zero change to design conclusions.

---

#### S7R-04: Inconsistent Unordered List Markdown Syntax
*   **Severity**: Nit
*   **Affected Scope**: Lines 30–36, 40–48, 52–58, 64–84, 254–286 vs Lines 225–231, 236–248
*   **Discrepancy Description & Rationale**:
    The document alternates unpredictably between two list bullet indentation conventions:
    *   **Three-space indent (`*   `)**: Used in lines 3–5 (metadata), lines 30–36 (Goals), lines 40–48 (Non-Goals), lines 52–58 (Open Questions), lines 64–84 (CUJ Given/When/Then), and lines 254–286 (Alternatives Pros/Cons/Rejection).
    *   **Single-space indent (`* `)**: Used in lines 225–231 (API Endpoints), lines 236–238 (Security), lines 241–243 (Performance), and lines 246–248 (Rollout).
*   **Evidence**: Visual and raw text inspection across FeatureRange.
*   **Consequence**: Inconsistent markdown formatting syntax across sibling sections.
*   **Recommendation**: Standardize all top-level unordered lists across the entire document to a uniform convention (e.g., `* ` with single space).
*   **Tradeoff**: None; strictly improves syntactic consistency.

---

#### S7R-05: Formatting Asymmetry in Non-Functional Requirements Subsections
*   **Severity**: Nit
*   **Affected Scope**: Lines 235–248 (`### Non-Functional Requirements`)
*   **Discrepancy Description & Rationale**:
    Within `### Non-Functional Requirements`, sibling H4 subsections exhibit inconsistent item labeling:
    *   `#### 1. Security & Attributability` (lines 235–239) uses unadorned prose bullets without bold lead-in tags:
        *   `* Every disposition...`
        *   `* Image artifacts...`
        *   `* SHA-256 checksums...`
    *   `#### 2. Performance & Capacity Envelope` (lines 240–244) and `#### 3. Rollout, Backward Compatibility & Rollback` (lines 245–249) use structured, bold categorical lead-in tags:
        *   `* **Inference Overhead**: ...`
        *   `* **Storage Budget**: ...`
        *   `* **Zero Token Budget**: ...`
        *   `* **Additive Migration**: ...`
        *   `* **Historical Data Isolation**: ...`
        *   `* **Operational Recovery**: ...`
*   **Evidence**: Lines 235–248.
*   **Consequence**: Creates visual and structural asymmetry when scanning sibling subsections.
*   **Recommendation**: Prepend bold descriptor tags to the items in `#### 1. Security & Attributability` (e.g., `* **Attributable Identity**: ...`, `* **Append-Only Immutability**: ...`, `* **Filesystem Integrity**: ...`).
*   **Tradeoff**: None; establishes typographic symmetry.

---

#### S7R-06: Asymmetrical Specification Structure in API Endpoints Section
*   **Severity**: Nit
*   **Affected Scope**: Lines 223–232 (`### API Endpoints (FastAPI Backend)`)
*   **Discrepancy Description & Rationale**:
    The API specification list lacks uniform structural completeness across endpoints:
    *   Lines 225, 229, and 230 explicitly define inline pseudo-JSON request bodies (`Request body: {...}`).
    *   Line 228 (`POST /api/v1/deliveries/{id}/capture-view`) omits request payload parameters entirely, offering only an informal descriptive clause.
    *   Lines 226, 227, and 231 (GET endpoints) omit expected response status codes and return payload structures.
*   **Evidence**: Lines 225–231.
*   **Consequence**: Incomplete and uneven API contract representation at the architectural level.
*   **Recommendation**: Reformat the API section into a structured Markdown table or symmetrical sub-blocks detailing Method, Path, Request Schema, and Response Schema.
*   **Tradeoff**: Slightly increases vertical line count; significantly enhances technical precision.

---

#### S7R-07: Section Header Naming Deviation from Standard Taxonomy
*   **Severity**: Nit
*   **Affected Scope**: Line 15 (`## The Problem`)
*   **Discrepancy Description & Rationale**:
    Line 15 uses the heading `## The Problem`. `feature-spec-standard.md` (line 33) specifies the canonical section title as `Problem Statement`.
*   **Evidence**: Line 15 vs `feature-spec-standard.md` line 33.
*   **Consequence**: Minor terminological divergence from the standard's blueprint.
*   **Recommendation**: Rename `## The Problem` to `## Problem Statement`.
*   **Tradeoff**: None.

---

### Verification Summary for Main Agent
The structural audit of FeatureRange (lines 1–287) of `docs/designs/nusaqc_delivery_traceability.md` is complete. Seven findings were identified: **3 Major** (S7R-01, S7R-02, S7R-03) and **4 Nit** (S7R-04, S7R-05, S7R-06, S7R-07). Addressing these will bring the specification into full structural alignment with `feature-spec-standard.md`.

---

# Part 3: Style Review (`egm-style`)

# Review7Style (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/style.md first. Review FeatureRange (lines 1–287) of docs/designs/nusaqc_delivery_traceability.md. Check for banned marketing adjectives, buzzwords, ungrounded certainty, ambiguous verbs, and passive voice that obscures agency. Prioritize materially misleading or ungrounded claims over cosmetic edits. Assign IDs S7S-01 onward. Include exact reading manifest.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/style.md) ⇒ ok · 68 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-120) ⇒ ok · 134 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:124-287) ⇒ ok · 182 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:288-436) ⇒ ok · 160 lines

## assistant

→ read(nusaqc-proposal.pdf) ⇒ ok · 393 lines

## assistant

→ read(nusaqc-proposal.pdf:194-312) ⇒ ok · 126 lines

## assistant

→ read(nusaqc-pitchdeck.pdf) ⇒ ok · 440 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-15-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-16-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-17-X6.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-18-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-20-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-12-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-13-X15.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-13-X16.png) ⇒ ok · 2 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-14-X15.png) ⇒ ok · 3 lines

## assistant

→ read(C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/pitch-page-14-X16.png) ⇒ ok · 2 lines

## assistant

→ grep((Jepang|Japanese) @ nusaqc-proposal.pdf) ⇒ ok · 1 line

## assistant

→ grep(Japanese @ docs/designs/nusaqc_delivery_traceability.md) ⇒ ok · 6 lines

## assistant

→ read(docs/designs/nusaqc_delivery_traceability.md:1-85) ⇒ ok · 97 lines

## assistant

# Style Audit Report: NusaQC Delivery Traceability Design

## 1. Reading Manifest & Limitations

### 1.1 Documents and Artifacts Read
*   **Style Agent Persona Standard**: `~/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/style.md` (lines 1–67).
*   **Target Document**: `docs/designs/nusaqc_delivery_traceability.md`
    *   *FeatureRange (Audited Scope)*: Lines 1–287 (Overview, Problem, Goals, Non-Goals, Open Questions, CUJs, Architecture, Data Model, Conveyor Pipeline, API Endpoints, Non-Functional Requirements, Alternatives Considered).
    *   *DetailedRange (Context Scope)*: Lines 288–436 (Implementation Sequence, Target Files, Verification Plan).
*   **Approved Context Documentation**:
    *   `nusaqc-proposal.pdf` (lines 1–507, including Background, State of the Art, System Design, AI & Model Implementation, Hardware & Optics, and Business Model).
    *   `nusaqc-pitchdeck.pdf` (lines 1–439, including Gap Analysis, Solution Architecture, Appendices 1–6).
*   **Extracted Pitch Deck Image Artifacts**:
    *   `pitch-page-12-X15.png`: Table 1.2 Test Scenarios & Dataset Matrix (TC-1.1 to TC-5.2).
    *   `pitch-page-13-X15.png`: Table 2.1 Baseline Metrics & Status Breakdown.
    *   `pitch-page-13-X16.png`: Table 2.2 Root-Cause Deconstruction of Failure Modes.
    *   `pitch-page-14-X15.png`: Table 2.3 Freshness Classifier Confusion Matrix (TC-1.1).
    *   `pitch-page-14-X16.png`: Defect Detector Class Breakdown & Overall Baseline Metrics.
    *   `pitch-page-15-X6.png`: Table 4.1 Metrics Optimization: Before vs. After.
    *   `pitch-page-16-X6.png`: Optimization Performance Breakdown (Part 1).
    *   `pitch-page-17-X6.png`: Optimization Performance Breakdown (Part 2).
    *   `pitch-page-18-X15.png`: Optimization Summary Table.
    *   `pitch-page-20-X15.png`: Appendix 6 Current System Boundary & Stress Test Failures.

### 1.2 Operational Limitations & Ground Truth
*   **Workspace Source Code**: No approved implementation source code exists in this repository. All evaluations of code behavior are assessed strictly against the design specification, the proposal, and the pitch deck. No live runtime or external repositories are assumed.
*   **Measurements vs. Projections**: Metrics cited from external literature (e.g., Banwari et al., 2022; Okano et al., 2025) and internal development targets (e.g., MobileNetV3 F1 $\ge 85\%$, latency 150–300 ms) are distinguished from actual tested baseline values (e.g., Raspberry Pi 4 FP32 1,315 ms latency, YOLOv8s baseline 2,739.4 ms total frame latency).
*   **Protocol**: Read-only audit; no files modified, no background agents spawned, no code executed.

---

## 2. Audit Findings (FeatureRange: Lines 1–287)

### S7S-01: Ungrounded Mechanical Certainty and Hallucinated Sourcing for Turning Mechanism
*   **Severity**: Blocker
*   **Affected Scope**: Lines 210, 101, 109 (Section: "Two-View Conveyor Ingestion Pipeline" & "System Architecture & Boundaries")
*   **Style Vector**: Ungrounded Certainty / Unverified Sourcing
*   **Evidence**:
    *   Line 210 states: *"Fish moves through the Japanese passive guide block, flipping 180 degrees onto its ventral side."*
    *   Neither `nusaqc-proposal.pdf` nor `nusaqc-pitchdeck.pdf` contains any reference to a "Japanese" passive guide block.
    *   The document itself directly identifies this mechanism as an unresolved physical unknown in Open Questions Q1 (line 52): *"Is a suitable passive flipping device commercially available for wet fish at the target conveyor speed and size range? What is the failure rate, and how are misflipped or jammed fish handled without blocking the line?"*
*   **Consequence**: Stating that the fish flips 180 degrees through an imported "Japanese passive guide block" asserts physical certainty over an unverified mechanical component, directly contradicting Q1 and misleading engineering teams into treating an open mechanical risk as a solved commercial procurement item.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Remove the ungrounded descriptor "Japanese". Reframe Step 3 as an intended operational inversion stage subject to the physical qualification and jam-handling requirements flagged in Q1.
    *   *Draft Revision*: *"3. **Passive Inversion Stage**: Fish passes through a passive physical inverter guide intended to orient the fish onto its ventral side. (Subject to mechanical validation under Open Question Q1; anomalous orientations or jams fall back to Step 5)."*
*   **Tradeoff**: Removes the impression of an off-the-shelf turnkey mechanical solution, but accurately portrays the prototype status of the conveyor flipping mechanism.

---

### S7S-02: Projected Engineering Target Stated as Measured CPU Execution Yield
*   **Severity**: Major
*   **Affected Scope**: Line 241 (Section: "Performance & Capacity Envelope")
*   **Style Vector**: Ungrounded Certainty / Claim Calibration
*   **Evidence**:
    *   Line 241 asserts: *"Sequential MobileNetV3 (150–300 ms) + YOLOv8s (470 ms) yields ~650–800 ms total CPU execution per frame on target hardware (Raspberry Pi 5 / x86 CPU). Total two-view inference execution is ~1.5 s per fish."*
    *   Proposal Section 5.2.2 (p. 15, lines 330–340) defines 150–300 ms as an internal target (*"target pengembangan"*) and 470 ms as an external benchmark from literature (Okano et al., 2025 on Raspberry Pi 500) used as an engineering benchmark target (*"target engineering yang mengacu pada benchmark"*).
    *   Pitch deck test suite benchmarks (slide 13-X16, slide 14-X16) show measured baseline YOLOv8s latency on edge hardware was 1,315 ms (FP32) / 380 ms (INT8) on a Raspberry Pi 4, with average sample latency reaching 2,739.4 ms.
    *   No sequential two-model pipeline has been measured on a physical Raspberry Pi 5 within this workspace.
*   **Consequence**: Stating that the pipeline "yields ~650–800 ms total CPU execution per frame" misleads plant operators and software engineers into treating a theoretical mathematical sum of heterogeneous external benchmarks as an empirically verified runtime throughput.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Replace the indicative verb "yields" with calibrated target terminology.
    *   *Draft Revision*: *"**Inference Latency Budget**: Targets a combined execution budget of ~650–800 ms per frame on target CPU hardware (Raspberry Pi 5 / x86), projected from single-model edge benchmarks (Okano et al., 2025 for YOLOv8s; internal MobileNetV3 targets). Total targeted two-view inference execution is $\le 1.5$ s per fish, subject to empirical validation on the dual-camera rig."*
*   **Tradeoff**: Concedes that multi-model edge latency is an unvalidated projection rather than a proven benchmark, maintaining technical credibility.

---

### S7S-03: Generative AI Buzzwords Applied to Deterministic CV Timeout Handling
*   **Severity**: Major
*   **Affected Scope**: Line 221 (Section: "Two-View Conveyor Ingestion Pipeline", Step 5)
*   **Style Vector**: Buzzwords & Jargon / Hyperbole
*   **Evidence**:
    *   Line 221 states: *"The station does not crash or halt conveyor motor; anomaly is recorded with zero inference hallucination."*
    *   The inspection pipeline consists of deterministic computer vision models (MobileNetV3 and YOLOv8s) and relational SQLite tables. Computer vision object detection does not "hallucinate" in the generative large language model sense.
    *   A sensor timeout simply represents missing optical data. Describing this failure mode as "zero inference hallucination" applies irrelevant LLM terminology to a conveyor sensor timeout.
*   **Consequence**: Introduces marketing jargon that obscures the relational database behavior when a sensor times out, degrading the technical precision of the specification.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Strip "with zero inference hallucination" and state the concrete data behavior.
    *   *Draft Revision*: *"The station does not crash or halt the conveyor motor; the system records the anomaly with status `PARTIAL_DORSAL_ONLY` without inserting synthetic view records or defect predictions."*
*   **Tradeoff**: Eliminates trendy generative AI phrasing in favor of direct relational database semantics.

---

### S7S-04: Unsubstantiated Assertion of Existing Codebase Flaws Without Workspace Implementation
*   **Severity**: Major
*   **Affected Scope**: Lines 22, 90 (Section: "The Problem", Item 2 & "System Architecture & Boundaries")
*   **Style Vector**: Ungrounded Certainty / Subjective Evaluation of Non-Existent Code
*   **Evidence**:
    *   Line 22 asserts: *"2. **AI observation and human decision are conflated.** The current system writes the final decision (PASS/FAIL/CONDITIONAL) back onto the inspection record, overwriting the original model output when a supervisor overrides it."*
    *   Line 90 asserts: *"NusaQC extends the existing FastAPI and SQLite architecture to enforce strict boundaries..."*
    *   No approved implementation source code exists in the workspace. While the proposal mentions a UI mockup override action (p. 16, line 406), nowhere is it verified that an existing codebase actively executes destructive database overwrites.
*   **Consequence**: Fabricates a concrete implementation defect in a non-existent local codebase rather than framing the issue as an architectural requirement for the proposed design.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Frame the observation as an architectural vulnerability that the proposed relational schema prevents, rather than asserting empirical facts about an unseen codebase.
    *   *Draft Revision (Line 22)*: *"2. **Risk of conflating AI observation with human decision.** If supervisor overrides write directly to the primary inspection table, original model outputs are destroyed. NusaQC prevents this by storing model observations and supervisor dispositions in distinct, immutable relational tables."*
    *   *Draft Revision (Line 90)*: *"The proposed NusaQC design specifies a FastAPI backend and SQLite database structured to enforce strict boundaries between automated optical inspection, human quality disposition, and material transformation accounting."*
*   **Tradeoff**: Grounds the design justification in sound architectural principles rather than unprovable claims about legacy code.

---

### S7S-05: Contradictory and Ambiguous Unit Conversion Semantics
*   **Severity**: Major
*   **Affected Scope**: Line 180 (Section: "Data Model & Relational Schema", `human_dispositions`)
*   **Style Vector**: Ambiguous Verbs / Internal Contradiction
*   **Evidence**:
    *   Line 180 specifies: `quantity_unit`: *"Unit matching or converted from delivery."*
    *   Line 84 (CUJ 4) explicitly states: *"Fish count and weight are recorded in agreed units; they are not automatically converted."*
    *   Line 55 (Open Question Q4) asks: *"Does the factory measure receiving quantities in fish count, weight, or both? What unit governs supplier agreements and loss calculations?"*
    *   The phrase "or converted from delivery" introduces an ambiguous verb phrase without specifying who performs the conversion, by what formula, or whether automated conversion is permitted.
*   **Consequence**: Leaves the unit conversion agency undefined. If downstream accounting stages (lines 191–196) compare mismatched units (e.g., input in count vs. output in kg), the material balance equation ($Q_{in} = Q_{out} + L_{yield} + L_{reject} + V_{unexplained}$) produces invalid calculations.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Disallow ambiguous automated conversion in the schema definition, aligning line 180 with line 84 and line 55.
    *   *Draft Revision*: `quantity_unit` (`VARCHAR(16)` NOT NULL): *"Unit of measure matching `receiving_deliveries.quantity_unit` (`kg` or `count`). Automated unit conversion is not performed; any unit change must be logged as an explicit manual reconciliation."*
*   **Tradeoff**: Restricts schema flexibility by prohibiting implicit unit conversion, but protects data integrity across downstream transformation balances.

---

### S7S-06: Systematic Passive Voice Obscuring Agency in System Safeguards
*   **Severity**: Major
*   **Affected Scope**: Lines 218–221, 237–238, 242, 248 (Sections: "Two-View Conveyor Ingestion Pipeline" & "Non-Functional Requirements")
*   **Style Vector**: Passive Voice Obscuring Agency
*   **Evidence**:
    *   Line 219–220: *"Sequence N status is set to `PARTIAL_DORSAL_ONLY`. The inspection is flagged for manual supervisor inspection."* (Who or what sets and flags?)
    *   Line 237: *"Deletion of historical inspection images is disabled while referenced by an open delivery, disposition, or dispatch record."* (Enforced by filesystem permissions, database triggers, or API application logic?)
    *   Line 238: *"SHA-256 checksums are verified on image read to detect filesystem corruption."* (Verified by what service, and what error is returned on failure?)
    *   Line 242: *"Storage volume must enforce a pre-capture check requiring at least 10 GB free disk space..."* (A passive storage volume/disk cannot enforce an application check; the API endpoint or daemon must perform the check.)
    *   Line 248: *"Manual paper tally sheets during outages are ingested as a single reconciliation movement record with explicit `manual_outage_reconciliation` tag."* (How are they ingested? Automated OCR or manual operator form entry?)
*   **Consequence**: Omits the operational actor and system boundary for critical safeguards, leaving implementers uncertain whether logic belongs in backend routes, background workers, or manual operator workflows.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Rewrite in active voice, naming the specific software component or operator role responsible for each safeguard.
    *   *Draft Revisions*:
        *   Lines 219–220: *"The background pairing task updates Sequence N status to `PARTIAL_DORSAL_ONLY` and sets `flagged_for_review = TRUE`."*
        *   Line 237: *"The FastAPI storage service rejects HTTP DELETE requests for image artifacts that are referenced by active delivery, disposition, or dispatch records."*
        *   Line 238: *"The backend image-retrieval handler recomputes and verifies the SHA-256 checksum against `inspection_views.sha256` before streaming the file, raising an HTTP 500 integrity error if corrupted."*
        *   Line 242: *"The `POST /api/v1/deliveries` endpoint queries available disk space and rejects session creation with HTTP 507 if free storage is under 10 GB."*
        *   Line 248: *"During recovery from an outage, the QC supervisor manually enters paper tally totals via `POST /api/v1/deliveries/{id}/movements` with the tag `manual_outage_reconciliation`."*
*   **Tradeoff**: Adds specific implementation detail to the technical plan, removing architectural vagueness.

---

### S7S-07: Promotional Buzzwords and Inapposite Terminology
*   **Severity**: Nit
*   **Affected Scope**: Lines 138, 243 (Sections: "Data Model & Relational Schema" & "Non-Functional Requirements")
*   **Style Vector**: Jargon & Buzzwords / Tone
*   **Evidence**:
    *   Line 138: *"The SQLite schema is expanded with five purpose-built tables..."* ("purpose-built" is promotional filler).
    *   Line 243: Section heading *"Zero Token Budget"*. While technically true that no cloud LLM is called, "token budget" is LLM billing jargon inappropriately imported into an edge computer vision specification.
*   **Consequence**: Dilutes the dry, objective tone of an engineering document with marketing buzzwords.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Replace promotional adjectives and mismatched terminology with factual technical phrasing.
    *   *Draft Revisions*:
        *   Line 138: *"The SQLite schema is expanded with five relational tables..."*
        *   Line 243: Rename heading to *"On-Premises Local Compute (Zero External API Dependencies)"*.
*   **Tradeoff**: None.

---

### S7S-08: Subjective Authorial Voice in Alternatives Rejection
*   **Severity**: Nit
*   **Affected Scope**: Lines 256, 262, 268, 274, 280, 286 (Section: "Alternatives Considered")
*   **Style Vector**: Subjective Quality Judgments / Tone
*   **Evidence**:
    *   Repeated phrasing across all alternatives: *"Rejected by author: ..."*, *"Deferred by author: ..."*
*   **Consequence**: Shifts the decision-making framework from objective engineering constraints, operational interviews, and physical trade-offs to subjective personal decree.
*   **Style Rationale & Recommendation**: `CALIBRATE`. Adopt standard RFC/architecture decision record (ADR) status conventions.
    *   *Draft Revision*: Replace *"Rejected by author: real-world factory interviews..."* with *"Status: Rejected — factory interviews confirmed..."* and *"Deferred by author: ..."* with *"Status: Deferred — ..."*
*   **Tradeoff**: None.

---

## 3. Style Audit Summary Table

| Finding ID | Severity | FeatureRange Lines | Audit Vector | Editorial Action | Recommended Edit Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S7S-01** | **Blocker** | 210 (cf. 101, 109) | Ungrounded Certainty / Sourcing | `CALIBRATE` | Strip unverified "Japanese" sourcing; reframe turning guide as prototype concept linked to Open Question Q1. |
| **S7S-02** | **Major** | 241 | Ungrounded Performance Certainty | `CALIBRATE` | Frame 650–800 ms as an engineering latency budget projected from external benchmarks, not an empirical yield. |
| **S7S-03** | **Major** | 221 | Jargon & Buzzwords | `CALIBRATE` | Remove "zero inference hallucination"; describe deterministic fallback to `PARTIAL_DORSAL_ONLY` without synthetic data. |
| **S7S-04** | **Major** | 22, 90 | Ungrounded Claims on Unseen Code | `CALIBRATE` | Reframe from an empirical assertion about legacy code into an architectural requirement for immutable record separation. |
| **S7S-05** | **Major** | 180 (cf. 55, 84) | Ambiguous Verbs / Contradiction | `CALIBRATE` | Disallow ambiguous conversion in `quantity_unit`; mandate exact unit matching or explicit manual reconciliation. |
| **S7S-06** | **Major** | 218–221, 237–238, 242, 248 | Passive Voice Obscuring Agency | `CALIBRATE` | Rewrite safeguards in active voice, explicitly assigning agency to background tasks, API route handlers, or supervisors. |
| **S7S-07** | **Nit** | 138, 243 | Jargon & Buzzwords | `CALIBRATE` | Replace "purpose-built" with "relational" and "Zero Token Budget" with "On-Premises Local Compute". |
| **S7S-08** | **Nit** | 256, 262, 268, 274, 280, 286 | Subjective Authorial Tone | `CALIBRATE` | Replace "Rejected by author" with standard ADR status labels ("Status: Rejected — ..."). |
