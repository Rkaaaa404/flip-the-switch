# Stage 5 — Initial zoom-out review

Target: `docs/designs/nusaqc_delivery_traceability.md`, lines 1–436. Both independent reviewers completed. Supporting PDFs are claims, not verified implementation. Design unchanged.

# Simplicity review

## Readiness verdict

**Not ready for implementation approval.** The objective is understandable and well focused: preserve delivery-linked evidence without allowing AI to become the final quality authority. Retaining SQLite/FastAPI, separating observations from dispositions, and rejecting ERP replacement are sensible choices.

However, the plan specifies implementation details before resolving physical identity, material ownership, audit corrections, and integration with the existing application. Its evidence does not establish deployed capabilities or measured performance.

### S5Z-01 — Major: The integration plan assumes an unverified application baseline

**Target lines:** 22, 90, 138, 245–248, 293–300, 312–314, 330, 352–358.

**Evidence:** The document asserts current overwrite behavior, existing tables/controllers, and automatic table registration through `init_db()`. It then names precise files to modify. Searches of the supplied workspace found no Python, TypeScript, or TSX implementation files, including ignored files; targeted searches found no implementation matches for the proposed services or claimed integration points. The proposal describes similar components, but that is documentation, not code verification.

**Consequence:** The plan cannot establish whether new services duplicate existing behavior, whether downstream lot identifiers are compatible, or whether leaving legacy routes active preserves the very overwrite behavior being removed.

**Recommendation:** Gate the file-level implementation plan on an approved source snapshot. Inspect the existing inspection, inference, identity, storage, dispatch, and database-initialization boundaries; then explicitly identify reused components and superseded write paths. Until then, label those integration details as assumptions.

**Tradeoff:** This delays precise implementation assignments, but avoids creating a parallel application model around imagined interfaces. No existing-code reuse recommendation can honestly be confirmed from this workspace.

### S5Z-02 — Major: Traceability delivery is unnecessarily coupled to an unresolved conveyor redesign

**Target lines:** 52, 64–66, 98–110, 201–221, 295, 298, 356–358.

**Evidence:** Q1 leaves the turning mechanism and its failure behavior unresolved. Nevertheless, the architecture commits to two cameras, two sensors, passive inversion, background processing, and a fixed three-second pairing window. It describes cancelling the timer for sequence `N`, but does not establish how a second-camera event identifies that same fish when triggers are missed or several fish are between sensors.

The proposal describes synchronous single-snapshot operation as its initial approach (proposal lines 207–217, 343–345). The pitch also describes manual uploads/batch inspection as an available workflow (pitch lines 182–186); neither establishes an implemented reusable capability.

**Consequence:** A records feature becomes dependent on mechanical feasibility and a new correlation mechanism. Incorrect pairing would create apparently complete—but false—evidence, which is worse than an explicit missing view.

**Recommendation:** Separate the evidence-recording contract from the physical acquisition mechanism. Retain the required two-view evidence model, but make trustworthy same-fish identification an explicit acquisition acceptance gate. Evaluate operator-confirmed sequential two-view capture as the simpler pilot alternative while validating automated inversion separately. Ambiguous pairs must remain incomplete rather than being assigned by convenient ordering.

**Tradeoff:** Manual pairing sacrifices throughput and requires agreement on the pilot workflow; it does not require abandoning two-view coverage or building speculative tracking hardware.

### S5Z-03 — Blocker: The model does not yet establish trustworthy material identity through splits and reuse

**Target lines:** 11–13, 53, 74–84, 174–198, 230–231, 323–338.

**Evidence:** The design promises tracking through shipment or confirmed disposal and explicitly includes split storage/processing paths. Yet downstream identity is represented by nullable or unconstrained lot strings and a polymorphic `input_ref` pointing to a delivery or movement. The only stated accounting validation balances each movement independently. There is no defined rule preventing multiple movements from consuming the same available quantity, nor a defined terminal disposal record. Q2 leaves the physical continuity of the delivery identifier unanswered.

**Consequence:** Individually balanced records can collectively allocate more fish than were received. A rejected quantity can be mistaken for confirmed disposal, and a provenance tree can look complete while container identity has been lost. These are failures of the core evidence chain, not optional inventory features.

**Recommendation:** Define one authoritative lot/container identity and its relationship to delivery, disposition, movement, storage, and dispatch. Specify how operators preserve that identity at physical splits, how available quantities are consumed, and how disposal is confirmed. Reuse an existing lot model if the approved baseline supports it. Keep this to identity and quantity invariants rather than introducing a general inventory engine.

**Tradeoff:** Requires stronger operational discipline and transaction rules, but avoids a much larger reconciliation layer later. This does not require speculative mixed-source processing support.

### S5Z-04 — Major: “Auditable” is asserted without a complete human-record lifecycle

**Target lines:** 13, 71–72, 174–183, 197, 229–237, 322, 337, 419.

**Evidence:** The overview promises that every correction and handoff is attributable. The API bodies accept `authorized_by` and `operator_id`, while the security section only says they must be authenticated. It does not define whether identity is derived from the authenticated session or supplied by the caller. More importantly, there is no correction/supersession workflow for incorrect quantities or dispositions. The immutability test only establishes that recording a disposition leaves model outputs unchanged.

**Consequence:** An operator cannot correct a mistaken decision without either silently mutating history or appending a contradictory decision whose effect is undefined. Attribution may also be mistaken for validating a supplied badge string.

**Recommendation:** State a minimal audit contract: derive actor identity from the authenticated principal, authorize the operation, preserve the previous record, and explicitly link corrections to the record they replace. Define which decision and quantity allocation remain effective. Reuse the application's authentication and audit conventions once verified; a bespoke event-sourcing platform is unnecessary.

**Tradeoff:** Adds a small correction workflow and requires resolving decision authority, but directly supports the promised product rather than expanding it.

### S5Z-05 — Major: The acceptance plan measures implementation activity more than the proposed operational benefit

**Target lines:** 24, 35–36, 240–242, 282–286, 396–432.

**Evidence:** The design correctly calls five-minute lookup a target and retains paper records as the pilot comparison. Its verification plan, however, concentrates on code checks, coverage, simulated captures, and a five-fish demonstration with a sub-second trace-page target. It does not define the bounded pilot, documentation-completeness denominator, retrieval task, or acceptable operator effort.

Line 241 also states model execution times as a capacity envelope. The proposal explicitly labels the corresponding numbers as development/engineering targets (proposal lines 330–339). The pitch reports other baseline latency and failure figures (pitch lines 334–385), not validation of this two-view configuration.

**Consequence:** The implementation can satisfy its automated checks while failing to improve real trace retrieval or maintain accurate records during routine work. Hardware and storage choices could be made against targets presented as established capacity.

**Recommendation:** Separate assumed budgets from measurements. Add a small operational acceptance protocol using representative deliveries, actual split handoffs, missing evidence, and corrections. Measure completeness, end-to-end lookup time, recording effort, and acquisition performance against the manual baseline. Avoid importing the proposal’s numerical targets as observed facts.

**Tradeoff:** Requires factory participation, but tests whether the additional software and hardware justify their complexity.

### S5Z-06 — Nit: High-level sections freeze low-level choices before their governing decisions

**Target lines:** 136–221, 240–248; related detailed section 288–390.

**Evidence:** Before the detailed implementation section, the architecture specifies SQL widths, ID formatting, JSON layouts, capture paths, background-thread steps, exact timeout values, and a fixed disk threshold. Meanwhile, units, hardware behavior, retention, and decision authority remain open.

**Consequence:** Apparent precision can anchor implementation to arbitrary choices and obscure unresolved architectural contracts.

**Recommendation:** Keep the feature section focused on ownership, relationships, invariants, data flow, and failure semantics. Move necessary field-level details into the detailed plan and identify provisional values there. The detailed section itself is an appropriate place for implementation detail; it should not be rejected merely for being detailed.

**Tradeoff:** Slightly less immediate coding convenience, substantially clearer review and decision-making.

## Strongest simpler alternative

Deliver a **delivery-centred evidence workflow using the verified existing application**, with explicit physical lot identity, preserved AI observations, human dispositions and corrections, quantity-conserving handoffs, and a straightforward searchable trace report.

Treat automated two-view conveyor acquisition as a separately gated integration—not a prerequisite for proving the records workflow. Consider operator-confirmed two-view capture for the pilot, subject to explicit approval of that operating mode. Reuse existing inspection/upload, storage, dispatch, and authentication components only after examining their actual code.

## Exact reading manifest and limitations

Fully read:

- `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/zoom_out.md`: lines **1–74**; requested range 1–220.
- `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/zoom-out-standard.md`: lines **1–60**; requested range 1–260.
- `docs/designs/nusaqc_delivery_traceability.md`: **1–150, 151–287, 288–436**.
- `nusaqc-pitchdeck.pdf`, extracted text: **1–180, 181–330, 331–439**.
- `nusaqc-proposal.pdf`, extracted text: **1–200, 201–380, 381–562**.

Reuse discovery searched local Python/TypeScript/TSX paths with and without ignore filtering, plus implementation symbols for capture, lineage, storage, dispatch, GPIO, and initialization. No source implementation was found. No external repository paths were guessed.

PDF extracted text is **not visual proof**: some figures/tables have missing or garbled extraction. Reported benchmarks, interviews, capabilities, and targets remain document claims, not independently verified observations. No code execution, modification, tests, builds, or deployments were performed.


## Supplemental review after reading embedded PDF tables

**Verdict unchanged: not ready for implementation approval.** The additional evidence strengthens S5Z-01, S5Z-02, and S5Z-05; it does not establish a verified code baseline or deployed two-view capability. S5Z-03, S5Z-04, and S5Z-06 remain unchanged.

### S5Z-01 — Major — Additional reuse evidence

**Target lines:** 90, 293–300, 330, 352–358.

Pitch page 17 describes a final-round continuous inspection pipeline, camera proxy endpoint, four-role access control, storage automation, and traceability output. These are **documented capability claims**, not inspected implementations.

**Consequence:** Building new ingestion, authorization, storage integration, or reporting paths without checking that baseline risks duplicating components and leaving competing operational behavior active.

**Recommendation:** Inspect the approved implementation behind those specific claims before committing to new services. Verify whether the existing capture pipeline can accept delivery context and preserve separate observations, and whether its authentication supplies trustworthy actor identity. Reuse compatible components rather than assuming either their presence or their absence.

**Tradeoff:** Baseline inspection adds a prerequisite, but avoids speculative rebuilding. Local source searches still provide no implementation evidence.

### S5Z-02 — Major — Physical acquisition assumptions remain especially consequential

**Target lines:** 52, 64–66, 98–110, 201–221, 356–358.

Pitch page 18 reports residual limitations: **41.58% freshness F1 under low light**, **65% motion-blur recall retention**, and **28% defect recall under heavy occlusion**. Page 20 separately lists unresolved optical, physical, motion, latency, and detection issues, with planned mitigations and target metrics.

These reported results do not validate automatic inversion, same-fish pairing, or the new two-view arrangement.

**Consequence:** Two successfully stored pictures do not establish correct pairing, useful visibility, or supported inference coverage. The proposed pipeline’s `COMPLETE` status risks being interpreted more broadly than its capture-only definition warrants.

**Recommendation:** Preserve the distinction between capture completeness and usable evidence. Gate automated acquisition on demonstrated physical identity and visibility, not merely two sensor events within a timeout. Keep operator-confirmed sequential two-view capture as the simpler pilot alternative, subject to approval of that operating mode.

**Tradeoff:** Reduced throughput during validation, but fewer falsely complete evidence chains. No speculative conveyor-tracking subsystem is needed merely to evaluate the records workflow.

### S5Z-05 — Major — Explicit correction to the performance evidence

**Target lines:** 240–242, 396–432.

The newly visible tables require a sharper distinction than the extracted text allowed:

- Page 15 presents **380 ms / 2.63 FPS** as an after-optimization edge result.
- Page 16 explicitly labels the corresponding Raspberry Pi 4 figure **“Projected Edge Latency.”**
- Page 16 separately reports host CPU execution times of **3.14 ms** for the freshness model and **72.64 ms** for the defect detector.
- Page 14 reports **2,739.4 ms** average latency for a separate 25-sample detector run.
- Pages 12–14 describe test scenarios and reported baseline measurements; they are not this review’s independently reproduced results.

**Consequence:** These different environments and measurement categories cannot substantiate the target design’s approximately 1.5-second two-view execution envelope.

**Recommendation:** Mark line 241 as an estimate pending measurement on the selected hardware and actual two-view workload. Record the model artifact, device, capture configuration, and measurement boundary when validating it. Separate host measurements, edge projections, and operational throughput.

**Tradeoff:** This removes premature certainty without requiring a new optimization architecture.

## Strongest simpler alternative

Unchanged: a delivery-centred records workflow reusing verified capture, authentication, storage, and dispatch components; explicit lot identity and quantity accounting; preserved observations and correctable human decisions; straightforward trace retrieval. Validate automated dual-view acquisition separately rather than making an unproven mechanism the prerequisite for proving traceability value.

## Additional reading manifest

Fully viewed all ten supplied original embedded images under:

`C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/`

- `pitch-page-12-X15.png`
- `pitch-page-13-X15.png`
- `pitch-page-13-X16.png`
- `pitch-page-14-X15.png`
- `pitch-page-14-X16.png`
- `pitch-page-15-X6.png`
- `pitch-page-16-X6.png`
- `pitch-page-17-X6.png`
- `pitch-page-18-X15.png`
- `pitch-page-20-X15.png`

These images supplement the previous complete text-reading manifest. They establish what the PDF tables display—not measurement reproducibility, implementation existence, or field readiness. No edits, execution, tests, or external repository inspection occurred.

# Inventive review

1. **S5I-01 — Major: Separate evidence capture from inference to avoid trading conveyor continuity for trustworthy inspection records.**

   **Affected scope and exact target lines:** “Two-View Conveyor Ingestion Pipeline,” **203–221**; “Performance & Capacity Envelope,” **241–242**; “Operational Recovery,” **248**; ingestion-service implementation, **320–331**.

   **Evidence:** The dorsal path performs both model inferences before starting its pairing timeout (**207–209**). The ventral path cancels the timeout for sequence `N`, then performs inference before marking the inspection complete (**211–217**). The service likewise combines image persistence, inference, and sequence matching in one operation (**330**). Despite this coupling, anomalies must not halt the conveyor (**218–221**). The stated capacity envelope gives inference execution time but no admitted arrival rate or bounded backlog policy (**241–242**). Restart recovery resumes sequence numbering, without specifying recovery of captured-but-unprocessed evidence or unresolved pairs (**248**).

   **False compromise:** The design implicitly makes timely, reliable physical-event accounting depend on expensive model execution, while treating continued conveyor operation as the fallback. Evidence capture and inference completion do not need to share that timing dependency. The target’s own separation of AI observations from human decisions makes deferred inference possible without abandoning its core function.

   **Consequences — [INFERENCE]:** Model latency variation or overlapping fish arrivals could distort pairing deadlines, accumulate unresolved work, or leave persisted images without completed observations. A missing ventral trigger also needs an explicit correlation rule so that a subsequent fish’s ventral image is not assigned to the wrong dorsal record. Merely logging a partial inspection and continuing does not establish trustworthy identity. These outcomes are architectural risks, not observed failures.

   **Proposed resolution — Segmentation, with bounded Beforehand Cushioning:** Establish a small capture-and-correlation stage that records the delivery/session identity, trigger identity and timestamp, image reference, and pairing state independently of inference. Base pairing deadlines on physical capture events rather than inference completion. Run inference against those persisted captures through a bounded local work queue; a database-backed pending-work state can serve this purpose without introducing a message broker. Restart reconciliation should resolve unfinished capture/pairing/inference states rather than only advancing the counter.

   Define the supported physical ordering/spacing assumptions and what happens when correlation becomes ambiguous. Preserve uncertain captures as uncertain instead of guessing a match. Specify an operator-visible admission/backpressure policy for capacity exhaustion.

   **Secondary operational trade-offs:** Additional persistence operations, pending-work storage, restart reconciliation, and separate capture-versus-analysis status in the UI. Results may arrive after the fish has moved downstream. Queue limits require an operational choice—slower intake, stopping admission, or explicitly documented inspection gaps. **Finite compute and storage cannot guarantee unlimited uninterrupted intake with complete evidence; a queue absorbs bursts, not sustained overload.** Software correlation also cannot reconstruct physical identity when the available signals are insufficient.

### Assessment boundaries

The separation of AI observations, human dispositions, and material transformations is a sound architectural choice; no false compromise was detected in those foundational boundaries. Rejecting individual-fish tagging throughout processing does not itself justify a more elaborate tracking architecture.

The supplied proposal explicitly labels the cited model latencies as development/engineering **targets** (`nusaqc-proposal.pdf`, **330–339**). Its throughput and five-minute retrieval figures are also targets (**186–199**). The pitch deck reports baseline performance and stress-test failures (**334–385**), but those statements are not independently verified measurements here. None establishes that the proposed two-view ingestion path meets its operating envelope.

### Exact reading manifest

All paths below are the supplied files; no implementation repository or unrelated documents were inspected.

- `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/inventive_catalyst.md`: requested **1–250**, covering the complete **1–101** file.
- `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/resources/document_standards/zoom-out-standard.md`: requested **1–300**, covering the complete **1–60** file.
- `D:/main/Documents/explore/compe/hackhathon/flip-the-switch/docs/designs/nusaqc_delivery_traceability.md`: **1–150**, **151–287**, **288–436**; complete target.
- `D:/main/Documents/explore/compe/hackhathon/flip-the-switch/nusaqc-pitchdeck.pdf`: extracted-text ranges **1–180**, **181–440**, covering all **439** extracted lines.
- `D:/main/Documents/explore/compe/hackhathon/flip-the-switch/nusaqc-proposal.pdf`: extracted-text ranges **1–180**, **181–360**, **361–562**, covering all **562** extracted lines.

**Limitations:** PDF extracted text is not visual proof. Several figures and appendix pages expose little or no substantive text, and some tables are garbled. No approved current code baseline was supplied; implementation behavior, existing reusable components, hardware performance, and empirical outcomes remain unverified. No edits, builds, tests, formatters, or deployments were performed.

### Supplemental review: S5I-01 retained, with a reuse qualification

The image-only evaluation tables do **not** establish that the target’s two-view pairing, timeout, and recovery design is reliable. They do, however, report an existing asynchronous ingestion capability. **S5I-01 should recommend reusing or extending that capability if the approved implementation baseline confirms it, rather than introducing a second queue.**

**Additional evidence:**
- **Page 12, X15:** The stated asynchronous ingestion tests comprise a 40-frame burst and three endurance cycles totaling 9.09 seconds.
- **Page 13, X15:** Reports asynchronous throughput of **4.40 FPS**, **0% frame drops**, and **2.59 MB/min memory growth**. These are reported results, not independently verified measurements, and do not demonstrate two-camera identity correlation or crash recovery.
- **Page 16, X6:** Explicitly labels Raspberry Pi 4 latency as **“Projected Edge Latency”**—1,315 ms before and 380 ms after. Host CPU execution figures appear separately. The less-qualified edge-performance wording on page 15 therefore must not be treated as proof of measured target-hardware performance.
- **Page 17, X6:** Describes continuous streaming, IoT proxying, and a three-second network timeout. That timeout is not evidence for the target document’s three-second physical fish-pairing deadline.
- **Pages 18 and 20:** Describe persistent occlusion and motion limitations. They reinforce the need to state physical correlation assumptions; a software queue cannot recover unseen physical identity.

**Refined recommendation for S5I-01:** Preserve the proposed separation of capture/correlation from inference, bounded pending work, explicit overload behavior, and restart reconciliation. Before selecting implementation components, inspect the approved baseline for the reported asynchronous pipeline and extend it where appropriate. No supplied source demonstrates that its existing semantics already meet these requirements.

**Secondary liabilities remain:** More persistent lifecycle state, delayed inference results, reconciliation logic, and explicit operator handling of backlog or ambiguity. Reuse also requires checking whether the existing pipeline’s frame-oriented identity and failure semantics support paired inspections; reported throughput alone is insufficient.

**No additional false-compromise finding is warranted from these images.** Optical visibility limits are physical constraints, not contradictions that software architecture can eliminate.

### Supplemental exact reading manifest

Read all ten supplied image files under:

`C:/Users/Rayka/AppData/Local/Temp/nusaqc-review-pdf-dw1ronnn/`

1. `pitch-page-12-X15.png`
2. `pitch-page-13-X15.png`
3. `pitch-page-13-X16.png`
4. `pitch-page-14-X15.png`
5. `pitch-page-14-X16.png`
6. `pitch-page-15-X6.png`
7. `pitch-page-16-X6.png`
8. `pitch-page-17-X6.png`
9. `pitch-page-18-X15.png`
10. `pitch-page-20-X15.png`

This supplements the previous complete text-reading manifest. These images provide visual evidence of what the embedded tables state, **not empirical verification of their claims**, full-page visual coverage, or evidence of the current implementation. No code inspection, edits, or execution occurred.