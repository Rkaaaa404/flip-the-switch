# NusaQC — Incoming Inspection and Traceable Factory Records

* **Author:** Rkaaaa404
* **Date:** 2026-11-07
* **Status:** Author aligned on the refined product direction after independent review and clarification. Finalized for concept handoff; not an implementation specification or factory-approved procedure. Operational details and proposed staging remain to be validated.

## Overview

NusaQC helps a fish processor record the condition of incoming fish before processing and retrieve their subsequent history. Staff connect inspection photographs and observations to identifiable incoming stock, record a human decision about its disposition, and preserve links as material moves through processing, storage and shipment.

The core product is traceability, not automatic disposal. AI assists with supported visible findings; it does not establish food safety, supplier liability, or suitability for a particular market. A disposition is a person's decision about what should happen to the material. Recording that decision is separate from confirming the physical action occurred.

The intended benefit is evidence that staff can find and interpret when investigating quality or accounting for material. Reduced losses and improved supplier trust remain hypotheses to measure, not demonstrated results.

### What supports this direction

- **Interview recollections:** The processor receives fish from a first supplier, wants inspection history and tracking, and handles different problems through tolerance, reprocessing, downgrade or rejection. Exact procedures and financial responsibility remain unconfirmed.
- **Current capability reported by the author:** The defect model detects limited visible disease-related signs. Size inspection is unsupported. Exact deployed labels remain unverified; do not infer a disease diagnosis from a visual label.
- **Earlier proposal:** [nusaqc-proposal.pdf](nusaqc-proposal.pdf), §§3–5 and 7, describes freshness and defect models, inspection history, storage and dispatch. These descriptions are not proof of running features.
- **Financial evidence:** PDF §8.3 explicitly presents assumed savings scenarios. Its Rp130 million loss basis and 10–50% reductions are not measured NusaQC savings.

## Analysis

### 1. The main prerequisite is physical identity

All seven reviewers identified the same gap: attaching a batch number to a photo does not prove that the record follows the stock being moved.

Before claiming traceability, establish what staff can identify physically: a delivery, container, separated portion or individual fish. Confirm how that identifier remains attached during inspection and handoff. Existing markings may be sufficient; new hardware is not yet justified.

**Clarification after review:** The author reports that suppliers arrive in separate trucks at different times and are handled one at a time. This supports using each arrival as a receiving-delivery boundary; species or region is not a unique identifier.

**Author-proposed workflow, not verified factory practice:** For direct processing, staff select the current supplier/batch in the system. For storage first, staff tag stock with the supplier and storage location.

**Refinement recommended:** Give each receiving delivery its own ID and display the supplier beside it. A supplier name alone cannot distinguish repeat deliveries, and a storage location is not a permanent stock identity. Direct processing should select the delivery ID explicitly; stored portions should carry that ID on their physical labels, with their current location recorded separately. If a delivery is split, distinguish its portions while retaining the common source. Starting a new delivery must not relabel stock left from the previous one. How labels persist through partial withdrawal or mixing remains unconfirmed.

Each inspection must distinguish an individual observation, a selected sample and complete inspection of a defined unit. Record the inspected quantity and unit; keep it separate from delivery quantity. A sample does not establish the condition of every fish. Unknown identity or coverage must stay visible.

**Inspection coverage clarified after review:** The author recalls that the factory currently samples fish, but proposes inspecting every fish individually on a conveyor. A turning mechanism would expose another side for a second capture. This is intended behavior, not verified hardware performance; the precise views, camera arrangement and turning reliability remain unspecified. Two views do not establish complete surface coverage or food safety.

**Recommended capture contract:** Both views belong to one fish inspection, linked to the receiving delivery. Two photographs must not count as two inspected fish. Preserve view-specific findings and distinguish complete, missing, unreadable and ambiguously paired captures. An incomplete inspection must not silently become a pass. Verify that the system can maintain fish identity through turning and any downstream separation, and measure throughput across the entire two-view cycle. A fixed sample of two fish is not an established sampling procedure.

**Hardware status clarified:** The turning mechanism is proposed, not built or demonstrated for NusaQC. The author recalls a passive flipping block used in a Japanese can factory, but no specific source or device has been identified. That recollection does not establish suitability for wet fish with variable sizes and shapes. Treat successful turning, image pairing, product damage, jams and cleanability as validation questions before relying on two-view completion. Keep the evidence model capable of multiple views without claiming that the mechanical capture process is solved.

**Tradeoff:** Container-level tracking reduces handling effort but cannot promise individual-fish identity after processing. Without a maintained physical link, the product is an inspection archive rather than stock traceability.

### 2. Keep observations, decisions and material movements separate

| Record | What it establishes | What it does not establish |
|---|---|---|
| Inspection observation | What was photographed or assessed, when, and with which model/configuration | A final human decision or whole-batch safety |
| Human disposition | Who decided what should happen, to which quantity, and why | That the action occurred or that the supplier owes money |
| Physical movement or transformation | What material actually moved, split, combined or changed through processing | A new inspection or financial settlement |
| Commercial outcome | Confirmed credits, recoveries or costs borne by a party | That physical waste was prevented |

A reinspection adds evidence, not stock. When material splits, preserve links from its original identity to the resulting portions. If mixing occurs, record all contributing sources or explicitly mark the downstream history incomplete. Do not infer missing links from nearby timestamps.

Record quantities in agreed units. Distinguish useful outputs, normal processing removal, rework, final loss and unexplained differences. Scaling-related weight reduction is not automatically avoidable waste; fish count cannot silently become weight.

QC, production planning and inventory control (PPIC), warehousing and logistics may participate. Their actual decision authority needs factory confirmation. Do not invent a four-department approval chain.

### 3. Reuse NusaQC without preserving misleading meanings

[recall-room.md §7](recall-room.md#7-nusaqc-baseline-verified-facts) records a previous source-only baseline review: inspection observations have nonunique lot IDs; storage captures current location; receiving-source relationships are absent. These are not sufficient for quantity tracking through transformations.

The simplicity reviewer also inspected selected baseline source files and found that the existing override changes the inspection decision and related fields. Relabeling that action would not create a separate, attributable human disposition. This was a static source observation, not a runtime check.

**Recommendation:** Extend existing inspection/history, storage and dispatch components rather than build another application. Use existing factory records where they can supply reliable handoff references. Add only the relationships needed for the actual physical workflow; avoid a general rules engine or full inventory replacement.

Preserve historical observations and identifiers. Old PASS/FAIL results must not become retrospective human approvals or disposal records. Missing historical sources remain unknown. Any operational change must migrate all affected write paths consistently; a shadow-recording trial must not claim to enforce decisions.

### 4. Audit evidence requires more than searchable rows

Preserve original observations and attributable corrections. Human decisions need a responsible user, time, reason, scope and quantity. Model records need available model/configuration identity and a clear real-versus-simulated distinction.

Agree evidence retention, access and deletion rules with the factory; no legal retention duration is established here. Back up records and images together. Show failed or incomplete saves rather than a successful inspection. Define who reconciles manual records after an interruption, avoiding duplicates.

Restoring an old database does not reverse physical stock movements. Recovery must retain or reconcile events that occurred afterward.

For a single local installation, correlated operation logs, visible failures and a documented recovery process may suffice. A distributed monitoring platform, new message broker or cloud synchronization service is not justified by the supplied evidence.

### 5. Capacity and savings need measurement

The PDF's 1.5-second sequential inspection target implies a theoretical ceiling of 2,400 inspections/hour before capture, storage, retries and human handling. It is not a verified factory throughput figure. Measure the complete operation and peak arrivals before selecting capacity.

Estimate image storage from captures per day × stored bytes per capture × retention days, adding backup copies. Include staff review, support and recovery costs. This base concept requires no language-model agent or token spending; the existing vision models are a separate workload.

Proposed trial measures:

- Completeness of physical links and inspection evidence.
- Time staff spend capturing, reviewing and reconciling records.
- Time to retrieve and explain a delivery history, including its gaps.
- Final quantities, normal processing removal, recoveries and losses.
- Net financial effect after added labor and operating costs, only where credible cost data exist.

Evaluate AI separately from digitization. Review a defined sample of unflagged as well as flagged inputs; alert review alone cannot reveal missed findings. Confidence scores and pass rates are not safety or savings measures.

### 6. Resolve the effort-versus-traceability tension

The inventive review proposed three practical patterns:

- **Establish context before capture:** Select the physical delivery/unit once and reuse it for observations. Explicit context changes prevent many photos being assigned to the wrong delivery.
- **Separate responsibilities:** Keep observations useful even when inference is unavailable, and keep human decisions distinct. This preserves the record workflow but still requires human QC effort.
- **Record physical boundaries:** Capture a record when material changes identity or custody, linking existing modules through a small transactional register if needed. This avoids building production scheduling or accounting, but every supported stock-changing path must preserve those links.

**Ideal result:** Staff record each real handoff once; the same evidence supports daily work, later investigation and quantity reconciliation without duplicate departmental entry. Physical discipline and human judgment cannot be eliminated by software.

### Strongest argument against building

A labelled receiving register with linked photographs may deliver most of the value. If missing records do not change decisions, or staff cannot maintain physical identity, custom AI integration could add work while making incomplete records appear authoritative. Compare against that simpler workflow before claiming incremental benefit.

## Goals vs. Non-Goals

### In-Scope Goals

- Incoming inspection before processing, linked to supplier and identifiable stock.
- Honest representation of inspection coverage and supported model findings.
- Separate human dispositions, reasons and completed physical actions.
- Traceable relationships through supported processing, storage and shipment handoffs.
- Retrievable evidence, visible gaps, accountable corrections and quantity outcomes.
- Measured documentation value and an explicit method for evaluating financial benefit.

### Out-of-Scope Non-Goals

- Recall Room or Switch workflow design during this refinement.
- Size measurement, new model training or handheld hardware deployment.
- Automatic disposal, definitive disease diagnosis or food-safety certification.
- Automatic A/B/C-to-market or cold/frozen-storage rules.
- Supplier settlement rules not grounded in actual agreements.
- Replacing production planning, purchasing and accounting systems.
- Promising savings percentages or reconstructing undocumented history.

## Alternatives Weighed

| Alternative | Review assessment and reason |
|---|---|
| Labelled receiving register with photographs | Keep as the comparison case; may solve the immediate problem with less effort. Not rejected. |
| Extend existing NusaQC records | Recommended direction, conditional on physical identity and workflow validation. Reuses existing surfaces without requiring another application. |
| Every AI finding automatically becomes rejection and loss | Review recommends against: conflates observation, disposition, physical action and financial responsibility. No validated policy supports it. |
| Track every individual fish through all processing | Not justified yet; introduces handling burden without evidence that this precision is necessary or physically maintainable. |
| Full factory inventory/ERP replacement | Review recommends against: expands scope before demonstrating the traceability benefit. |
| Handheld supplier-side inspection first | Deferred in the review scope; different capture conditions and handling require validation. Remains a possible later direction. |
| Proceed directly to Recall Room | Deferred by the author until the underlying NusaQC concept is refined. |

Except for the stated deferral, these are review recommendations, not author-approved rejections.

## Key Decisions & Staging for Next Steps

### Established context

- Inspection starts at receiving, before processing.
- Individual size deviation is distinct from the proportion of defective fish; current models do not measure it.
- Traceability and digital factory records are the core purpose.
- The author authorized independent review of this concept, with Recall Room held aside.
- Suppliers reportedly arrive in separate trucks and are handled one at a time. The author proposes selecting the current batch for direct processing or tagging stored stock by supplier and location; these proposed controls have not been observed in factory use.

### Recommended staging — awaiting approval

1. Document one real receiving-to-processing journey: physical identifiers, inspection coverage, separation, quantities, handoffs and actual decision owner.
2. Trial that journey against current recordkeeping, retaining downstream references needed to explain its outcomes. This is proposed sequencing, not an approved reduction of the broader traceability goal.
3. Resolve any identity breaks before extending coverage. If the path includes mixing, handle it explicitly rather than omitting it.
4. Verify deployed labels and baseline behavior before implementation design. Keep documentary claims separate from runtime evidence.
5. Extend through additional storage/shipment paths only after the evidence and entry effort are understood. Revisit Recall Room using the resulting record meanings.

**Author-aligned direction:** Traceable receiving and factory records are the core product, supported by automated every-fish, two-view inspection as the intended production design. The turning mechanism remains an unvalidated hardware dependency, not a demonstrated current capability. Digital records must report actual capture coverage even when the intended sequence is incomplete. This alignment does not confirm factory procedures, detailed architecture or a reduced implementation scope.

### Review record and limits

Seven fresh-context reviewers completed in parallel: design, codebase details, simplicity, comprehension, implementation readiness, structural/maintenance and inventive catalyst. Each reported reading its bundled persona, the anchored concept, PDF §§3–5 and 7–8, and Recall Room §7. All supplied reading manifests; the simplicity reviewer additionally inspected selected baseline source files.

This is a conceptual review, not a factory validation or operational test. PDF diagrams were not visually inspected. No application was run, model performance measured, factory loss verified or implementation changed. The original PDF and recall-room.md remain unchanged. The author approved the refined direction after post-review clarifications; those clarifications were not subjected to a second independent review.
