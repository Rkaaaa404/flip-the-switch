# Drift Report — 2026-11-07

Scope: `docs/designs/` (1 document). Source paths below are relative to `code/webdev/` unless noted.
Branch inspected: `feat/delivery-traceability` @ `59e38f2`.

## nusaqc_delivery_traceability.md

**Missing features**

- **Operator guide missing.** The guide in target file 17, `docs/DELIVERY_TRACEABILITY_GUIDE.md`, does not exist. Nothing covers delivery creation, manual outage tally reconciliation, or image retention and backup procedures.
- **No background timeout task or per-fish timer.** The design says to start a 3.0 s timer per sequence N, cancel it when Sensor 2 fires, and run `reap_timed_out_captures` as a background asyncio task. The code has no timer, and nothing is scheduled in `backend/app/main.py`'s lifespan. The reaper only runs when something triggers it: the next capture (`two_view_inspection_service.py:250`), `GET /{id}`, `GET /{id}/trace`, or `PATCH /{id}/status` (`deliveries.py:183,235,295`). A dorsal-only fish stays unflagged until one of those happens.
- **`FAILED_CAPTURE` is never assigned.** It is declared in the enum (`models/delivery_trace.py:35`), the schema `Literal`, and the UI labels, but no code path sets it.
- **No authentication.** NFR 1 and Risk 5 require an authenticated `authorized_by` / `operator_id`. The backend has no auth layer. Both fields are free-text request strings (`schemas/delivery_trace.py:71,93`), so anyone can type any badge string. Risk 5 names exactly this.
- **Checksums are never verified on read.** The SHA-256 is computed and stored when the image is written (`two_view_inspection_service.py:263`). Images are then served raw through `StaticFiles` at `/uploads` (`main.py:46`) with no check.
- **Images are not protected from deletion.** Nothing enforces the "append-only" rule or "deletion disabled while referenced". The old `DELETE /api/v1/lots/{lot_id}` (`api/v1/lots.py:358-394`) still deletes the image file and its `DispatchLot` rows without checking whether a dispatch references them.
- **Old rows are not marked `legacy_observation`.** The rollout section says existing `inspections` rows get this marker. No column, flag or label exists anywhere in the code.
- **No `manual_outage_reconciliation` tag.** `ProcessingStage` (`models/delivery_trace.py:45-51`) and `StageT` only allow the six normal stages, and there is no tag field. A paper-tally reconciliation movement cannot be recorded as the design specifies.
- **`CaptureViewInbound` schema missing.** `POST /{id}/capture-view` takes multipart `image`, `view_side` and an optional `sequence_in_delivery` (`deliveries.py:247-258`), with no hardware trigger timestamp. Server receive time is used as the trigger time (`two_view_inspection_service.py:222`).
- **No in-memory station context.** The design says `POST /deliveries` sets station context in memory. Instead, every capture carries the delivery ID in its URL.
- **No eye/gill crop before freshness inference.** MobileNetV3 is meant to run on an eye/gill region. It actually runs on the whole frame resized to 224×224 (`app/ai/preprocessor.py:14-19`).
- **Trace response leaves out the inspections.** CUJ 3 and the `DeliveryTraceTreeResponse` spec include the linked dual-view inspections. The response returns only `inspection_summary` counts (`schemas/delivery_trace.py:258-291`), so the trace page cannot show the inspections or their images.
- **`/trace` cannot find lots missing their upstream link.** `get_delivery_lineage` only loads movements with `delivery_id == id` (`material_lineage_service.py:253`). A storage slot or dispatch lot with no upstream movement never shows up. That check exists only in the undocumented `GET /deliveries/lots/{lot_id}/provenance`. Test case 7 (`test_audit_trace_with_missing_links`) never covers this case. The no-upstream case is tested only through the provenance endpoint (`test_provenance_legacy_lot_no_upstream`, `tests/test_material_lineage.py:265`).
- **CUJ 3 search is missing.** No UI or API lets staff search by delivery ID or by supplier name and date. `GET /deliveries` only filters by `status` (`deliveries.py:140-146`), and `frontend/app/deliveries/page.tsx` has no search field.
- **Hardware controller doesn't match its spec.** Target file 8 says it extends `gpio_controller.py` / `mock_controller.py`, drives both proximity sensors and controls the conveyor motor. `DualConveyorController` (`hardware/dual_conveyor_controller.py:26`) is a standalone, mock-only class. It does not subclass `BaseHardwareController`, and it has no GPIO and no motor control.
- **Smoke test step 3 can't be run as written.** It asks the mock controller for "1 ulcer-flagged fish". The simulator can only drop ventral views (`SimulateRequest.drop_ventral_every`); it cannot inject a defect. It feeds whatever `*.jpg` files sit at the top of `UPLOAD_DIR` (`dual_conveyor_controller.py:84-93`). A defect fish has to be uploaded by hand through `POST /{id}/capture-view`, or a defect image copied into `UPLOAD_DIR`. Even then, the deployed model labels the candidate ulcer images `warna_abnormal`, not ulcer (see **Defect labels** below).
- **85% branch coverage is not enforced.** `pytest-cov` was added, but `backend/pyproject.toml` has no `--cov-branch` or `fail_under` settings.
- **The verification plan's `ruff` command will fail.** `uv run ruff check backend/app` needs `ruff`, which is not in `pyproject.toml` or `uv.lock`.
- **Trace page tree is not interactive.** The design calls for an "interactive provenance tree". `trace/page.tsx` renders a static nested list with no expand or collapse.
- **Intake dock can't stop a session.** `frontend/app/deliveries/page.tsx` can only create deliveries. Ending a session (→ `inspection_complete`) is only possible from the detail page header (`deliveries/[id]/page.tsx:173`).

**Incomplete or extra model fields**

- **`human_dispositions.supersedes_id` isn't in the design's schema.** The column exists (`models/delivery_trace.py:135`, nullable, unique FK) and is accepted in `HumanDispositionCreate`. The design's Data Model section and its disposition request body leave it out; only Risk 5 mentions it.
- **`receiving_deliveries.created_at`** (`models/delivery_trace.py:73`) is not in the design's schema.
- **Undocumented unique constraints.** These are `uq_fish_delivery_sequence`, `uq_view_fish_side`, and a unique `material_movements.output_lot_id` (`models/delivery_trace.py:87,105,144`). The last one means only one movement can ever produce a given lot, so two paths can't feed into the same lot.
- **`InferenceMode` has an extra value, `skipped_unsupported`** (`models/delivery_trace.py:57`). The design only allows `real_onnx` and `simulated_mock`.
- **`DeliveryCreate` differs from the documented body.** It requires `created_by` and accepts `received_at` (`schemas/delivery_trace.py:55-56`); the design's request body has neither.
- **`flag_reasons_json` holds more than defect classes.** The design says it is an array of detected defect classes. The code also writes `grade_C`, `missing_ventral_view` and `missing_dorsal_view` (`two_view_inspection_service.py:44-45,273`).
- **Wrong ID types in the frontend.** `InspectionView.id` and `FishInspection.id` are typed as `string` (`frontend/types/delivery.ts:82,95`), but the backend returns integers.

**Defect labels** (reference: `code/models/model_2/ANNOTATION_GUIDE_MODEL2.md`)

- **The design's label names don't exist in the model.** The design uses English names: `["ulcer", "scale_loss"]` in the `flag_reasons_json` example, and "ulcer-flagged fish" in smoke test step 3. The deployed detector only emits the four classes from the annotation guide, as mapped in `backend/app/ai/inference.py:19-24`:

  | ID | Model class | Closest English term |
  |:--:|---|---|
  | 0 | `sisik_sisa` | parasites, scale loss |
  | 1 | `warna_abnormal` | red lesions, hemorrhage, Aeromoniasis |
  | 2 | `luka_robekan` | ulcer, fin or tail rot, Saprolegniasis fungus |
  | 3 | `lendir_berlebih` | excess mucus, White Tail Disease |

  So the design's `ulcer` is `luka_robekan` and `scale_loss` is `sisik_sisa`. Neither English string can ever appear in `flag_reasons_json`.
- **Open Question Q6 is already answered.** It asks for the deployed model's exact defect labels; the annotation guide and `ALL_DEFECT_CLASSES` give them. The design still lists it as open.
- **The bounding-box key is `bbox`, not `bounding_box`.** The design gives `defects_detected_json` entries as `{label, confidence, bounding_box: [x1, y1, x2, y2]}`. The code stores `{label, bbox, confidence}` (`backend/app/schemas/inspection.py:15-18`, `inference.py:187-191`).
- **Model labels disagree with the guide on open ulcers.** I ran the deployed `nusaqc_model2_defect_detector.onnx` at the default 0.50 threshold on two candidate ulcer images:
  - `code/models/datasets/model-2/nusaqc_extended_pseudo_dataset/train/images/hf_00811.jpg` shows a clear open ulcer with exposed tissue. The model returns one `warna_abnormal` box (confidence 0.864). Its training label is class 1 (`warna_abnormal`, in `train/labels/hf_00811.txt`) too. That breaks the guide's Overlap rule 2: damaged or perforated tissue should be `luka_robekan`, class 2.
  - `code/models/datasets/yolo8s/train/images/Untitled.jpg` is a tuna with six round red lesions. It has no label file in `yolo8s/train/labels/`. The model returns only 2 of the 6 lesions, both as `warna_abnormal` (0.68 and 0.518). At 0.25 it finds 5, all `warna_abnormal`.

  Any detected defect flags the fish, so both images work as "flagged fish" for the smoke test. Neither can test ulcer (`luka_robekan`) detection with the current weights. If pseudo-labels like `hf_00811` taught the model to call ulcers `warna_abnormal`, they may need relabelling before retraining.

**Hardcoded values (logic shortcuts)**

- **Supported fish families are a hardcoded list:** `SUPPORTED_FAMILIES = {"Scombridae", "Cichlidae", "Salmonidae"}` (`two_view_inspection_service.py:38`). Other families skip inference and get grade `UNSUPPORTED`. The design never mentions this, and Salmonidae isn't one of its example families.
- **Unsupported views pass silently.** The review flag only checks for grade C or detected defects (`two_view_inspection_service.py:273-278`). An unsupported fish with both views ends up `COMPLETE` and not flagged. This conflicts with the Goal that incomplete evidence must not be "silently treated as a pass".
- **Backpressure starts at 12, not 8.** The design caps the queue at 8 frames and then applies backpressure. The code accepts up to `MAX_PENDING + 4` = 12 pending frames, then rejects with HTTP 503 (`two_view_inspection_service.py:39,240`).
- **The semaphore guards the wrong step.** In the design, `asyncio.Semaphore(4)` limits view persistence and a separate worker semaphore limits inference. In the code, `Semaphore(4)` limits inference, and persistence is serialized by a single `asyncio.Lock` (`two_view_inspection_service.py:40-41,244,249`).
- **Different capture directory.** The design uses `/data/captures/{delivery_id}/`. The code uses `{UPLOAD_DIR}/captures/{delivery_id}/`, which defaults to `./uploads` (`deliveries.py:130`, `two_view_inspection_service.py:253`).
- **Transit time is a hardcoded constant:** `EXPECTED_TRANSIT_SECONDS = 1.15` (`two_view_inspection_service.py:37`). The design doesn't mention it, and it can't be configured.

**Architectural divergence**

- **Different pairing algorithm.** The design pairs with a per-sequence timer. The code waits for each ventral capture, then picks the unpaired dorsal within the 3 s window whose age is closest to 1.15 s (`two_view_inspection_service.py:178-197`). A ventral with no match creates a new fish under a new sequence number with status `PARTIAL_VENTRAL_ONLY` (`:199-209`). The design never describes how `PARTIAL_VENTRAL_ONLY` arises.
- **Partial status is set up front.** Each new dorsal fish gets `PARTIAL_DORSAL_ONLY` immediately (`two_view_inspection_service.py:153`), not when the timeout fires. On timeout, the reaper only adds the flag and the `missing_ventral_view` reason.
- **Different overdraw check.** The design specifies one atomic SQLite check: Σ`quantity_in` ≤ `stated_quantity`. The code checks per `input_ref` instead. Receiving stages are capped by `stated_quantity`, and downstream stages by the source lot's `quantity_out` (`material_lineage_service.py:191-219`). It relies on a process-wide `threading.Lock` (`:44`) rather than an SQLite transaction.
- **Movements are not tied to accepted quantity.** The design sends only accepted lots to the handoff. In the code, receiving stages can draw the full `stated_quantity`, including rejected quantity, and any disposition `output_lot_id` can be skipped. The link is only reported afterward as a `DISPOSITION_LOT_NOT_HANDED_OFF` gap.
- **Only one unit per delivery.** Dispositions and movements must use the delivery's unit (`material_lineage_service.py:137-140,186-189`). The design allows a disposition unit that is "matching or converted from delivery". CUJ 4 records both fish count and weight, which the code can't do.
- **Lineage service names and signatures differ.** `get_delivery_audit_trail` is implemented as `get_delivery_lineage` (`material_lineage_service.py:242`). `record_transformation_stage` takes an extra `delivery_id`. `handle_view_capture` is `async` and takes extra `sequence_in_delivery` and `now` parameters.
- **No recursive SQL traversal.** The design specifies recursive SQLite queries that return a hierarchical tree. The backend returns a flat movement list (`DeliveryTraceTreeResponse.movements`), and the tree is built in the browser (`frontend/app/deliveries/[id]/trace/page.tsx:56`). Lot provenance is an iterative Python loop (`material_lineage_service.py:353-373`).

**Undocumented logic**

- **Three extra endpoints and a filter.** These are `PATCH /{id}/status`, `POST /{id}/simulate`, `GET /lots/{lot_id}/provenance`, and a `status` query filter on `GET /` (`deliveries.py:143,165,226,316`). Their schemas (`DeliveryStatusUpdate`, `SimulateRequest`, `LotProvenanceResponse`) and client methods (`updateDeliveryStatus`, `captureView`, `simulateConveyor`, `getLotProvenance`) are also undocumented.
- **Undocumented status machine.** The design lists statuses but no transitions. The code allows only these (`material_lineage_service.py:46-50,135,184`):
  - `active_receiving` → `inspection_complete`: manual only.
  - `inspection_complete` → `disposition_recorded`: automatic on the first disposition.
  - `disposition_recorded` → `closed`.

  Dispositions are allowed only in `inspection_complete` or `disposition_recorded`. Movements are allowed only in `disposition_recorded`. Captures are refused once a delivery leaves `active_receiving`. As a result, a closed delivery can never record a later handoff, such as the storage-to-dispatch step in CUJ 3.
- **Undocumented disposition rules.**
  - `output_lot_id` is required unless the outcome is `REJECT` (`schemas/delivery_trace.py:74-78`).
  - Active dispositions may not add up to more than `stated_quantity` (`material_lineage_service.py:152-157`).
  - A correction must point to a disposition that is still active.
- **Undocumented movement rules.**
  - `output_lot_id` must differ from `input_ref`.
  - Receiving stages must use the delivery ID as `input_ref`.
  - Downstream stages need an existing output lot from the same delivery.
  - `unexplained_variance` can be negative, while every other loss field must be ≥ 0 (`schemas/delivery_trace.py:87-107`, `material_lineage_service.py:191-207`).
- **Trace response has undocumented parts.** It adds a `QuantityBalance` block (`schemas/delivery_trace.py:267-272`) and a fixed list of seven `missing_links` kinds (`MissingLinkKindT`, `:33-41`). The design only describes "an array of `missing_links`".

**Documentation links**

- **Target paths don't match the repo layout.** The design writes paths as `backend/...` and `frontend/...`, but they actually live under `code/webdev/`. Prefixing them (for example `code/webdev/backend/app/services/two_view_inspection_service.py`) would make future drift checks cheaper.
