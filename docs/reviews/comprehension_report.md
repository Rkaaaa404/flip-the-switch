# Stage 6 — Document Comprehension Audit

Target: `docs/designs/nusaqc_delivery_traceability.md`, lines 1–436.
Reviewer: `egm-comprehension`

# Review6Comprehension (idle)

## user

Complete assignment thoroughly:

Read C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/comprehension.md first. Read entire target in ranges. No document standard. Return COMPLETE result with headings exactly "What this proposes" and "How the existing system works, per this document" first, then findings with IDs S6C-01 etc, severity, exact lines, consequence and suggested clarification. Test self-containment, not demand code details in feature section. Include exact reading manifest. Do not write files.

## assistant

→ read(C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/comprehension.md:1-220) ⇒ ok · 70 lines

## assistant

→ read(D:/main/Documents/explore/compe/hackhathon/flip-the-switch/docs/designs/nusaqc_delivery_traceability.md:1-145) ⇒ ok · 160 lines

## assistant

→ read(D:/main/Documents/explore/compe/hackhathon/flip-the-switch/docs/designs/nusaqc_delivery_traceability.md:149-287) ⇒ ok · 158 lines

## assistant

→ read(D:/main/Documents/explore/compe/hackhathon/flip-the-switch/docs/designs/nusaqc_delivery_traceability.md:288-436) ⇒ ok · 160 lines

## assistant

## What this proposes

NusaQC would connect supplier arrivals to two-view fish inspections, preserve AI observations separately from human quantity-based decisions, and trace material through processing, storage, and dispatch. Five new tables would support these records alongside existing data, with APIs and operator dashboards for capture, decisions, movements, and audit retrieval. Missing evidence and lineage gaps would remain visible rather than being inferred away. The implementation plan also specifies mock hardware, automated tests, and a manual demonstration.

## How the existing system works, per this document

Factory records currently rely on paper, scattered documents, or staff memory, and inspection results are not reliably connected to incoming deliveries. An existing FastAPI/SQLite application stores inspections, storage records, and dispatch information, but supervisor overrides overwrite inspection decisions rather than preserving separate observations and dispositions. Existing inspection rows would remain historical observations rather than becoming artificial delivery records. The document mentions existing inference and hardware-controller components, but does not fully explain their current operational workflow.

## Findings

### S6C-01 — Major — Open questions and proposed commitments have unclear decision status

**Exact lines:** 52–57, 138, 182, 210, 246–247.

**Discrepancy:** Several questions presented as unresolved are subsequently treated as settled: whether legacy inspections remain historical observations, who may authorize dispositions, and whether a passive turning device is available. The later sections prescribe historical isolation, supervisor authorization, and a particular passive guide without distinguishing provisional assumptions from approved decisions.

**Consequence:** A new reader cannot tell which parts are implementable requirements and which depend on factory or hardware validation.

**Suggested clarification:** Mark the corresponding commitments as provisional, identify which open question gates them, or update the questions to record resolved decisions. Explain what may proceed before each remaining prerequisite is resolved.

### S6C-02 — Major — Same-fish view pairing depends on an unstated conveyor assumption

**Exact lines:** 66, 204–220, 328–331, 358.

**Discrepancy:** The document says the second trigger belongs to sequence `N`, but never explains how that association is established when multiple fish are in transit or a trigger is missing or late. “Matches with existing sequence or opens new sequence” does not define the observable pairing rule.

**Consequence:** Readers cannot determine why the two photographs represent the same fish, particularly after the first anomaly. This makes the central evidence relationship difficult to understand or evaluate.

**Suggested clarification:** Describe the physical ordering/spacing assumptions and the pairing policy in ordinary language, including what happens to a late or unmatched second capture. No implementation algorithm is necessary in the feature section.

### S6C-03 — Major — Capture completeness and usable model coverage are not connected

**Exact lines:** 31, 34, 66, 156–170, 216–220, 374.

**Discrepancy:** The journey promises that unreadable views are incomplete, but `COMPLETE` is defined as both views being captured. Separately, a view can have freshness `UNSUPPORTED`, yet the document does not explain whether this means an unsupported species, an unusable image, unavailable model coverage, or something else. The named flags cover defects, Grade C, and capture timeouts, but do not establish the reviewer-visible outcome for these other conditions.

**Consequence:** A reader cannot distinguish “two files exist” from “both sides have usable inspection evidence,” or understand how unsupported evidence avoids appearing satisfactory.

**Suggested clarification:** Define capture completeness versus assessment coverage, explain `UNSUPPORTED`, and state the display/review outcome for unreadable or unassessable views. Briefly define or link the project’s A/B/C freshness scale.

### S6C-04 — Major — Delivery session lifecycle lacks operational meaning

**Exact lines:** 65, 70, 149, 203, 225–231, 248, 370, 415.

**Discrepancy:** The document lists four delivery statuses and promises starting/stopping sessions, inspection completion, restart recovery, and eventual closure. It does not explain which operator action or event advances each state, whether stopping capture ends inspection, or how the station chooses the active delivery when another delivery starts or the backend restarts.

**Consequence:** A new operator or implementer cannot follow a delivery from intake to closure or understand how capture attribution remains correct across session changes.

**Suggested clarification:** Add a short lifecycle narrative or transition table covering start, stop, completion, disposition, closure, and resume. State whether the station can have more than one active delivery and how its capture context is selected.

### S6C-05 — Major — The downstream material identity chain is ambiguous

**Exact lines:** 53, 78, 83–84, 177, 185–190, 262, 323, 337–338.

**Discrepancy:** Different sections describe a processing input as a delivery/lot ID, a parent delivery or movement ID, and an “input lot” whose existence is validated. The relationship between a disposition’s optional output lot, a movement’s output lot, and a physical handling container is not explained. Consequently, it is unclear how a partially accepted delivery becomes separately identifiable storage and processing portions.

**Consequence:** Readers cannot consistently paraphrase which identifier follows material through a split and subsequent handoffs. Different interpretations could produce incompatible lineage records.

**Suggested clarification:** Define the relationship among delivery, lot, movement, and handling container, including which identifier a subsequent handoff references. Provide one small example of a delivery splitting into storage and processing paths, distinguishing the software contract from the physical-labeling question still open in Q2.

### S6C-06 — Major — Discovering a delivery’s missing upstream links is unexplained

**Exact lines:** 78, 187–189, 231, 324, 338, 421.

**Discrepancy:** The audit starts from a known delivery, yet promises to isolate lots with missing upstream receiving links. The document does not explain what remaining relationship associates such a lot with that delivery, or distinguish a broken edge in a reachable chain from a completely unassociated lot.

**Consequence:** “Complete evidence chain with explicit gaps” can be read as promising discovery of records the system has no stated way to associate with the requested delivery.

**Suggested clarification:** Define which gaps a delivery-scoped trace can identify and how they remain discoverable. Explain separately how wholly unassociated lots are surfaced, if they are in scope, and illustrate the missing-link test with a concrete broken relationship.

### S6C-07 — Major — Quantity conversion policy remains unclear across stages

**Exact lines:** 55, 84, 146–147, 179–180, 191–196, 323, 420.

**Discrepancy:** The journey says count and weight are recorded in agreed units without automatic conversion, while dispositions may use units “converted from delivery.” Each record exposes only one quantity unit, and the balance rules do not explain how successive records remain comparable when receiving uses count and processing uses kilograms.

**Consequence:** Readers cannot tell whether mixed-unit workflows are prohibited, manually measured, manually converted, or supported through an unstated rule. The meaning of a balanced transformation is therefore uncertain across stage boundaries.

**Suggested clarification:** State the supported unit policy, including whether both measurements can be retained and what happens when a downstream stage uses a different unit. Distinguish independently measured quantities from conversions and connect the provisional policy to Q4.

### S6C-08 — Major — Corrections and confirmed disposal have no explained workflow

**Exact lines:** 11–13, 71–72, 174–198, 229–230, 337, 419.

**Discrepancy:** The overview promises tracking through confirmed disposal and recording every correction under a named person. Later sections describe rejection decisions and discarded quantities, but never explain whether rejection itself confirms disposal or whether a separate physical event does. They also describe an immutable movement journal without explaining how an incorrect decision or movement is corrected and presented in subsequent traces.

**Consequence:** A reader cannot follow rejected material to the stated endpoint or understand how the evidence chain remains both auditable and operationally correct after a recording mistake.

**Suggested clarification:** Explain the distinction between rejecting material and confirming its disposal, and describe the correction relationship for erroneous records. State how corrected quantities and decisions appear in the current trace while preserving history.

### S6C-09 — Nit — The manual demonstration assumes knowledge of mock controls

**Exact lines:** 356–358, 426–432.

**Discrepancy:** “Trigger 5 mock fish inspections with Mock Controller” does not identify the control, command, endpoint, or configuration used to emit those events or select the partial and ulcer scenarios. The controller’s existence is explained, but its invocation is not.

**Consequence:** A fresh team member cannot execute the supplied smoke scenario from this document alone.

**Suggested clarification:** Name the mock-control entry point and the mechanism for selecting the two abnormal cases, or link to the relevant operational instructions.

## Exact reading manifest

Only the following files were read:

- `C:/Users/Rayka/.omp/plugins/cache/plugins/egm___egm___0.1.0/agents/comprehension.md`
  - Requested range: `1–220`.
  - Returned complete file: lines `1–69`.
- `D:/main/Documents/explore/compe/hackhathon/flip-the-switch/docs/designs/nusaqc_delivery_traceability.md`
  - Requested ranges, in order: `1–145`, `149–287`, `288–436`.
  - Tool context expansion supplied lines `146–148` with the first range.
  - Complete target coverage: lines `1–436`, including FeatureRange `1–287` and DetailedRange `288–436`.

No other documents, PDFs, prior reports, code, or conversation history were read. No files were written and no verification commands were executed.