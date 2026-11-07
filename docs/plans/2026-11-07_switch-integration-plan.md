# Receiving QC Room: plan to make NusaQC a Switch hackathon entry

| | |
|---|---|
| **Written** | 2026-11-07, 05:40 UTC (12:40 WIB) |
| **Deadline** | 2026-11-07 23:59 IST = **18:29 UTC** (01:29 WIB on 8 Nov). About 12h 45m left at time of writing |
| **Branch** | `feat/delivery-traceability` @ `59e38f2` |
| **Target Switch** | Switch Console 0.40.1 (switch-core 0.31.0). API facts below are reused from `docs/ideation/recall-room.md` §15.0. They come from reading the source at that tag and were never run live, so Phase 0 verifies them |

## 1. Verdict: not submittable yet

The software works: 32/32 backend tests pass, and the delivery → inspection → disposition → movement → trace chain exists end to end. But measured against the brief in `docs/ideation/competition-ideation.md`, it fails the one hard requirement.

| Criterion | Weight | Today | Why |
|---|:-:|:-:|---|
| Use of Switch | 30% | **0/10** | No Switch code, room, template or agent anywhere in the repo. The design doc lists "Switch workflow design" as a **non-goal**. The brief requires that "the workflow must not function without it". As it stands, the entry would likely fail screening. |
| Technical execution | 25% | 6/10 | Runs and is tested, and the weights are committed. But the repo is **private**, the README has no Switch setup, there is no demo seed, and the drift report found gaps (no auth, lazy timeout). |
| Creativity and impact | 25% | 7/10 | A real, specific problem (fish exporters' QC evidence chain), but on its own it is a CRUD dashboard, not a person-plus-agent workflow. |
| Presentation | 20% | 2/10 | No demo video, and the README describes the workspace rather than the problem or the Switch workflow. |
| **Weighted** | | **≈3.6** | |

## 2. The idea: let Switch do what the code can't do alone

The drift report's most serious finding is that `authorized_by` and `operator_id` are free-text strings, so anyone can sign a disposition as anyone. The design requires authenticated identities and has no way to provide them.

**Switch supplies exactly that.** Every message event it delivers to a custom agent carries a `sender` participant id issued by Switch, not typed by a user. If the only way to record a disposition is through a deterministic gate that trusts that id, three things follow:

1. The design's attributability requirement is met for real.
2. Removing Switch breaks the workflow: without verified senders, the API accepts no dispositions at all.
3. The human decision (CUJ 2) happens in a shared room where the supervisor sees the flagged-fish photos the agent posts. It no longer happens in a form anyone can fill in.

> **Idea definition** (brief template): For **fish-processing QC teams**, the **end of a delivery's inspection run** starts a Switch room where **`qc-agent` (Claude Code)** summarizes the run, posts the flagged fish's photos and defect boxes, and drafts disposition and movement records from staff instructions. **The QC supervisor** decides accept, reject, reprocess or downgrade, and **floor operators** report processing yields. The result is **an attributable disposition and lineage record**, with every write signed by a Switch-verified person and a trace with explicit gaps. Switch is indispensable because **it is the only source of verified human identity for those writes, and the only place where photos, agent analysis and people from different jobs meet on the same delivery.**

### 2.1 Participants

| Participant | Type | Does | Cannot |
|---|---|---|---|
| QC supervisor | Person (Mattermost account) | Reviews flagged fish, decides dispositions, approves via `@gate` | — |
| Floor operator | Person | Reports WGGS and fillet yields, confirms movements via `@gate` | Approve dispositions |
| Dispatch / audit staff | Person | Asks "which delivery is in DISP-…?" | Write anything |
| `qc-agent` | Claude Code through Switch Console | Runs `qcctl`; summarizes, posts photos, drafts proposals, answers trace questions | Record any disposition or movement. Its token is read-and-propose only, and the API enforces this |
| `qc-gate` | Deterministic Python client, no LLM | Turns `@gate approve DP-3` from a verified sender into an API call and posts the receipt | Act on anything outside its fixed command grammar |

### 2.2 Demo script (target length 3 minutes)

1. **Trigger.** The operator finishes a mock conveyor run on `DEL-20261107-001`, which contains the real `hf_00811.jpg` ulcer image and one dropped ventral view. In the room: `@qc DEL-20261107-001 inspection done`.
2. **Agent summary.** `qc-agent` runs `qcctl delivery show` and `qcctl trace`, then posts: "5 fish, 1 partial (seq 3, no ventral view), 1 flagged: `warna_abnormal` 0.86. 500 kg undispositioned." It sends the flagged fish's dorsal photo with its box drawn on (Console's `send_attachment`).
3. **Human decision.** Supervisor: "Accept 450 kg as LOT-A. Reprocess 50 kg for trimming; the lesion is local."
4. **Agent drafts.** It drafts `DP-1` (ACCEPT 450 LOT-A) and `DP-2` (REPROCESS 50 LOT-R), and posts: `@gate approve DP-1` / `@gate approve DP-2`.
5. **Two refusals, then a real approval.** The floor operator types `@gate approve DP-1` → ⛔ "role floor_operator cannot approve dispositions". The agent tries to address the gate → refused by Switch's addressing policy. The supervisor approves → ✅ receipt: "DP-1 recorded as disposition #1, authorized_by = qc.supervisor (Switch participant p_…), message m_…".
6. **Floor.** Operator: "@qc LOT-A WGGS in 450, out 400, gills/guts 45, reject 5." The agent drafts `MV-1`, and the operator confirms with `@gate confirm MV-1`. The balance check runs; an unbalanced variant is refused with the API's 422 message.
7. **Audit question.** Auditor: "@qc where did LOT-W come from?" The agent runs `qcctl provenance LOT-W` and answers with the chain and its explicit gaps. The trace page in the UI shows the same chain, with each record badged "Signed via Switch".

## 3. Build plan, time-boxed

Times are UTC. **Feature freeze at 15:30.** After that, only the README, video and submission.

### Phase 0: Switch smoke test and go/no-go (05:45–07:00) ⚠️ biggest risk

- [ ] Start Switch Console 0.40.1 and the local server with Mattermost. The Windows build is early access, so check this first.
- [ ] Create one room with a Claude Code agent, and confirm it replies to `@` messages and that `send_attachment` posts an image.
- [ ] Create three Mattermost accounts (`qc.supervisor`, `floor.operator`, `auditor`) and link each to a Switch user (identity claim).
- [ ] Register a custom agent with `POST /agents/register-known`. From a 20-line Python script, receive one `message` event over `/agents/{id}/connection/ws?filter=addressed` (or long-poll `GET /agents/{id}/events`). Print `sender`, `sender_role`, `room_id`, `message_id`, then reply with `POST /agents/{id}/message`.
- **Go/no-go at 07:00.** If the custom-agent event stream cannot be made to work, switch to the **fallback** in §5.

### Phase 1: backend auth, proposals and gate endpoint (07:00–09:00)

New module `code/webdev/backend/app/switchroom/`, plus small changes to the existing routes.

- [ ] **Tokens.** `QC_AGENT_TOKEN` and `QC_GATE_TOKEN` in `.env`, checked through an `X-Api-Token` dependency. `POST /deliveries/{id}/dispositions` and `/movements` now **require the gate token**; the old open routes return 403. All `GET`s and `/simulate` stay open for the UI.
- [ ] **Models.**
  - `switch_identities`: `participant_id` PK, `username`, `role` (one of `qc_supervisor`, `floor_operator`, `auditor`).
  - `record_proposals`: `id` (`DP-n` / `MV-n`), `kind`, `delivery_id`, `payload_json`, `status` (`pending`, `applied`, `rejected`, `superseded`), `proposed_by` = agent, `source_message_id`.
  - `gate_commands`: `switch_message_id` UNIQUE for idempotency, `sender`, `room_id`, `command`, `result`, `receipt`.
  - Add `authorized_via` / `switch_message_id` columns to `human_dispositions` and `material_movements`. They're additive, and `init_db` creates them.
- [ ] **Agent endpoints** (agent token): `POST /switchroom/proposals` validates the payload with the existing `HumanDispositionCreate` / `MaterialMovementCreate` and dry-runs the quantity checks, so the agent finds out at draft time. `GET /switchroom/proposals/{id}`.
- [ ] **Gate endpoint** (gate token): `POST /switchroom/gate/commands` with `{sender, sender_name, room_id, message_id, command, subject}`. In one transaction:
  1. Idempotency on `message_id`.
  2. The sender maps to `switch_identities` → else refuse.
  3. The role allows the command: approve DP needs `qc_supervisor`; confirm MV needs `floor_operator` or `qc_supervisor`.
  4. The proposal is pending.
  5. Apply through the **existing** `record_disposition` / `record_transformation_stage`, with `authorized_by` / `operator_id` = the mapped username, plus the message id.
  6. Return a receipt.
- [ ] **Tests** in `tests/test_switchroom.py`: wrong token → 403; unknown sender → refused; floor operator approving a DP → refused; replayed message id → same receipt with no second row; over-quantity proposal → refused at draft and again at apply.
- [ ] **Cheap fixes from the drift report** (≤20 min): flag `UNSUPPORTED` views for review; add `scripts/` reaper-on-startup if time allows.

### Phase 2: agent tooling and Switch template (09:00–10:30)

- [ ] `code/switch/agent/qcctl.py`: a thin client that prints JSON. Commands: `delivery list|show`, `trace <id>`, `provenance <lot>`, `flagged <id> --save-images <dir>` (downloads flagged views and draws the bboxes with PIL, for `send_attachment`), `propose disposition …`, `propose movement …`, `proposal show <id>`.
- [ ] `code/switch/agent/CLAUDE.md`: commands, output templates, the "never claim recorded until the gate receipt appears" rule, the four defect labels and what they mean (from `ANNOTATION_GUIDE_MODEL2.md`), and "visual screening is not a food-safety verdict".
- [ ] `code/switch/receiving-qc.template.yaml`: one agent (`qc-agent`), one room `receiving-qc` with users and aliases (`qc`, `gate`), room instructions, and a kickoff. Base it on `recall-room.md` §15.1. **Build one room first**; split into `qc-review` and `processing-floor` only if Phase 5 finishes early.

### Phase 3: `qc-gate` client (10:30–12:00)

- [ ] `code/switch/gate/register.py`: one-time `register-known`, which writes `gate/.env`.
- [ ] `code/switch/gate/main.py`:
  - Open the WebSocket (answer `ping` with `{"type":"pong","cursor":n}`), with long poll as the fallback.
  - Parse the fixed grammar: `approve DP-n`, `reject DP-n <reason>`, `confirm MV-n`, `reject MV-n <reason>`, `status DEL-…`. Anything else gets a one-line help reply.
  - Call the gate endpoint, then post the receipt verbatim.
- [ ] Addressing policy on `qc-gate`: named users only, **no agents**, so Switch itself refuses `qc-agent`.
- [ ] `code/switch/link_identities.py`: maps the three participant ids to roles in `switch_identities`.

### Phase 4: demo seed and full rehearsal (12:00–13:30)

- [ ] `code/webdev/backend/scripts/seed_demo.py`: a deterministic reset. It creates `DEL-20261107-001` (PT Samudra Bitung, Tilapia/Cichlidae, 500 kg) and feeds 5 fish through `handle_view_capture` with the real model: `hf_00811.jpg` as the flagged fish, 3 clean images, and one dorsal with no ventral. Then it moves the delivery to `inspection_complete`.
- [ ] Run the §2.2 script end to end twice. Fix whatever breaks. Record the timings.

### Phase 5: UI evidence of Switch (13:30–15:00)

- [ ] On the delivery and trace pages, add a "Signed via Switch · @qc.supervisor · message m_…" badge on dispositions and movements, and a pending-proposals panel (`DP-n awaiting @gate approve`).
- [ ] Remove or disable the UI's direct disposition and movement forms, since they now get 403. Replace them with a one-line "Record decisions in the `receiving-qc` room" hint. This keeps the Switch-is-essential story honest.
- [ ] **15:30: feature freeze.**

### Phase 6: submission package (15:30–18:00, 30 min buffer)

- [ ] **README rewrite**, structured for the rubric:
  - Problem.
  - The workflow in one diagram (Mermaid: Mattermost ↔ Switch ↔ `qc-agent` / `qc-gate` ↔ FastAPI ↔ SQLite).
  - The removal test table.
  - Prerequisites.
  - Numbered setup: clone, `.env.example`, seed, `docker compose up`, Console, accounts, register the gate, import the template, link identities, start the gate.
  - The demo script.
  - What is pre-existing (NusaQC baseline, models) and what was built during the hackathon (everything from 7 Nov, per the git log).
  - Limits: visual screening only; the ulcer and `warna_abnormal` confusion noted in Q6.
- [ ] Add a root `.env.example` (tokens and Switch URL) and `code/switch/gate/.env.example`.
- [ ] **Update the design doc:** move "Switch workflow design" out of Non-Goals, add the gate-signed write path to NFR 1, and link this plan.
- [ ] **Demo video** (≤3 min unless organizers say otherwise): problem (20 s) → trigger and agent summary with photo → refusals → approval receipt → floor movement → trace page with "Signed via Switch" → removal test slide.
- [ ] **Make the repo public, or invite the judges** (confirm which on Discord). Check that no secrets are committed (`gate/.env` must be gitignored). Submit with time to spare.

## 4. What to leave out

Out of scope today. List these in the README as next steps:

- The remaining drift-report items: background timeout task, checksum verification on image read, `legacy_observation`, `manual_outage_reconciliation`, search UI.
- Recall Room containment (holds, dispatch blocks).
- A multi-room split, unless Phase 5 ends early.
- Retraining the detector or relabelling `hf_00811`.

## 5. Risks and fallbacks

| Risk | Sign | Fallback |
|---|---|---|
| Switch Console misbehaves on Windows (early access) | Phase 0 can't get a room working by about 06:45 | Run Switch in WSL2 or on a teammate's macOS machine. Decide by 07:00 |
| Custom-agent WebSocket or registration doesn't work as source-read | No event received by 07:00 | Use the long poll on `GET /agents/{id}/events`. If that fails too, **degrade**: `qc-agent` submits gate commands itself, using the sender display name and role from Console's `[Switch] <name> (workspace <role>)` line, and the README states the identity is not cryptographically verified. Switch stays central (room, photos, agent), but the Switch score drops from about 9 to about 7 |
| Real model labels the ulcer `warna_abnormal` | Already confirmed | Say so in the demo: "the model screens; the human decides". This shows the human's job isn't a rubber stamp |
| Running out of time | Phase 3 not done by 12:30 | Cut the Phase 5 UI work to just the badge, then cut movements from the demo (dispositions alone prove the point) |
| Mattermost accounts not linked to Switch users | `sender_role` is null | The gate refuses (correct). Fix the identity claims before recording |

## 6. Expected score after the plan

| Criterion | Weight | After | Main reason |
|---|:-:|:-:|---|
| Use of Switch | 30% | 8–9 | Verified-sender gate is the only write path; shared room with photos; removal test is concrete |
| Technical execution | 25% | 7–8 | Tested gate and API, deterministic seed, turnkey README. Switch setup is still manual |
| Creativity and impact | 25% | 8 | Real industrial QC with the evidence chain signed by named people; AI screens, people decide |
| Presentation | 20% | 7–8 | Refusal and approval receipts are easy to film; real fish photos |
| **Weighted** | | **≈7.6–8.3** | vs ≈3.6 today |
