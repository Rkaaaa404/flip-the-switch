# Idea ranking: all five candidates

> Scoring of every candidate in the project root against the rubric in `competition-ideation.md`. **No idea is selected**; this is input for the team's decision.

| | |
|---|---|
| **Written** | 2026-11-06 |
| **Candidates** | `recall-room.md`, `buzzerdefuse-room.md`, `accessfix-room.md`, `brandecho-room.md`, `deadline-rescue.md` |
| **Basis** | Every spec is checked against Switch Console 0.40.1 (switch-core 0.31.0). AccessFix is scored with an approval gate for human acceptance |
| **Deadline** | 7 Nov 2026, 23:59 IST = 8 Nov, 01:29 WIB |

## 1. Validation checklist (`competition-ideation.md` §5)

✅ = clearly met · ⚠️ = met with a caveat

| Dimension | Recall | BuzzerDefuse | AccessFix | BrandEcho | Deadline Rescue |
|---|---|---|---|---|---|
| User & problem | ✅ Fish exporters, histamine recall | ✅ Brand PR/Legal under a coordinated smear | ✅ Users blocked by inaccessible UI | ⚠️ Real but familiar; design tools already review assets | ⚠️ Relatable, low stakes |
| Workflow trigger | ✅ Buyer complaint + lab report | ✅ Alert from a listener client | ✅ Barrier report | ✅ Concept + banner submission | ✅ Deadline change report |
| Human contribution | ✅ Scope, missing evidence, approval (4 roles) | ✅ Scope, legal amendment, two keys | ✅ Clarification, acceptance | ⚠️ One steer + certification | ✅ Constraints, approval |
| Agent execution | ✅ Trace engine, proposals, export | ✅ Clustering, drafting, export | ✅ Browser repro, code fix, review | ✅ Rule checks, image reading, variants | ✅ Schedule proposals |
| Switch dependency | ✅ 3 linked rooms, verified gate | ✅ War room, two-key gate | ✅ Verified gate for acceptance | ✅ Verified gate, attachments both ways | ⚠️ Team could edit the app directly |
| Verifiable outcome | ✅ Holds; shipping refused with 409 | ✅ Statement published only after both keys | ✅ Real PR | ✅ Queue accepts certified assets only | ✅ Timeline changed |
| Feasibility by deadline | ⚠️ Largest build (baseline patches, engine, 3 rooms) | ✅ Medium, greenfield | ✅ Smallest | ✅ Medium, greenfield | ⚠️ Supabase/OAuth reproducibility |

## 2. Weighted rubric (potential, deadline ignored)

1–10 per criterion. Weights: Switch 30%, Technical 25%, Creativity 25%, Presentation 20%.

| Rank | Idea | Switch | Technical | Creativity | Presentation | **Weighted** |
|---|---|---|---|---|---|---|
| 1 | Recall Room | 10 | 8 | 9 | 8 | **8.85** |
| 2 | BuzzerDefuse | 9 | 7 | 8 | 8 | **8.05** |
| 3 | AccessFix | 9 | 7 | 7 | 9 | **8.00** |
| 4 | BrandEcho | 8 | 7 | 7 | 9 | **7.70** |
| 5 | Deadline Rescue | 7 | 6 | 6 | 8 | **6.70** |

**Recall Room**
- **Switch 10:** three linked rooms, gaps closed by people in different jobs, and approvals that count only from Switch-verified senders.
- **Technical 8:** deterministic tracing, holds enforced on every dispatch path.
- **Creativity 9:** a serious, specific food-safety problem.
- **Presentation 8:** the domain needs explaining to judges outside the food industry.

**BuzzerDefuse**
- **Switch 9:** the two-key release needs two *different* Switch-verified people. It's one room, and the gap-filling across jobs is thinner than Recall's.
- **Technical 7:** clustering on synthetic data, a gate and a small newsroom service are achievable. It's greenfield, and a dataset built to be clustered can look staged; the genuine-complaint control group mitigates that.
- **Creativity 8:** timely and unusual for chat-ops, with a strong local angle. This depends on the safeguards (real complaints go to customer care, no account is ever named); without them it drops to about 6.
- **Presentation 8:** the "Key 1/2 … waiting for Legal" moment and the same-person cosign refusal are easy to film.

**AccessFix**
- **Switch 9:** reporter, developer agent, reviewer agent and maintainer meet in one room, and acceptance goes through a verified gate.
- **Technical 7:** Playwright reproduction plus a gate; the gate adds work.
- **Creativity 7:** a real problem, but a familiar developer-tools idea.
- **Presentation 9:** before/after in a real browser is very visual.

**BrandEcho**
- **Switch 8:** a verified gate plus images flowing both ways, but the human loop is short and design tools already have approvals.
- **Technical 7:** palette and margin checks in Python are reliable; logo template matching needs tuning.
- **Creativity 7:** a solid non-developer business workflow in a crowded category.
- **Presentation 9:** before/after banners and the feed gallery are the most visual demo of the five.

**Deadline Rescue**
- **Switch 7:** approval through a deterministic approver client in the room, but the team could edit the schedule in the app directly.
- **Technical 6:** hosted Supabase, Google OAuth and identity linking make it hard for judges to reproduce.
- **Creativity 6:** relatable to judges, but lower stakes.
- **Presentation 8:** a clear before/after timeline.

## 3. Deadline-adjusted view

Here the Technical score is re-read as "likely to run reliably and reproducibly by 7 Nov, 23:59 IST". The other three criteria are unchanged.

| Idea | Technical (adjusted) | **Weighted** | Main build risk |
|---|---|---|---|
| Recall Room | 5 | **8.10** | Baseline patches + trace engine + gate + 3 rooms + UI badges |
| BuzzerDefuse | 7 | **8.05** | Gate + clustering + newsroom, all new |
| AccessFix | 7 | **8.00** | Playwright on Windows; GitHub connections on a local server unverified |
| BrandEcho | 6 | **7.45** | Image checks + gate + queue, all new |
| Deadline Rescue | 5 | **6.45** | Compe-In on hosted Supabase/OAuth; identity linking |

The top three end up within 0.1 of each other. The rubric alone no longer separates them; the time left does.

## 4. Recommendation

**BuzzerDefuse gives the best score for the effort under this deadline.** It keeps most of Recall's Switch advantage (a verified multi-person gate), it has the most filmable Switch moment, and it doesn't depend on patching an existing app.

- **Pick Recall instead** if the team is confident it can build the full engine and the baseline patches in about a day. Its ceiling is clearly the highest.
- **Pick AccessFix** if the team wants the smallest, most visual build and accepts a weaker problem.
- **BrandEcho and Deadline Rescue** are dominated: a higher-ranked idea matches or beats each of them on every criterion (AccessFix for BrandEcho, BuzzerDefuse for Deadline Rescue).

## 5. Common to every option

These come before any product code, whichever idea is picked:

1. **Live smoke test:** Console 0.40.1 on Windows, the local server, Mattermost, and one person talking to one Console agent.
2. **A custom client over WebSocket** (`register-known`, `/connection/ws`, `POST /message`, media upload). Every idea needs the same gate client. Only the command grammar and the app checks differ.
3. **Two Mattermost accounts with identity claims**, to confirm that `sender` ids are stable and addressing rules match them.
4. **Note the agent API URL from Console.** Ports are random per machine, so `.env.example` takes `SWITCH_API_ENDPOINT`.

If step 2 fails, every idea loses about 1 point on Switch. AccessFix then has the safest fallback: GitHub branch protection can enforce acceptance without a gate.
