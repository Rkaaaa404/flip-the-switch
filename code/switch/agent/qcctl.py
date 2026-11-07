#!/usr/bin/env python3
"""qcctl: qc-agent's only door into NusaQC. Prints JSON. Standard library only.

It can read deliveries and traces and draft proposals. It cannot record anything: dispositions and
movements are applied only when an authorized person types `@qc-gate approve|confirm <id>` in the room.

Config (environment or a `.env` next to this file): QC_API_URL (default http://localhost:8000), QC_AGENT_TOKEN.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_env() -> None:
    path = os.path.join(HERE, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ.setdefault(key, value.strip().strip('"'))


_load_env()
API = os.environ.get("QC_API_URL", "http://localhost:8000").rstrip("/") + "/api/v1"
TOKEN = os.environ.get("QC_AGENT_TOKEN", "")


def call(method: str, path: str, body: dict | None = None, raw: bool = False):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("X-Api-Token", TOKEN)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read()
            return payload if raw else json.loads(payload or b"null")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        try:
            detail = json.loads(detail).get("detail", detail)
        except ValueError:
            pass
        out({"error": exc.code, "detail": detail})
        sys.exit(1)
    except urllib.error.URLError as exc:
        out({"error": "unreachable", "detail": f"NusaQC API at {API} is not reachable: {exc.reason}"})
        sys.exit(1)


def out(obj) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(obj, indent=1, ensure_ascii=False, default=str))


def q(s: str) -> str:
    return urllib.parse.quote(s, safe="")


# ------------------------------------------------------------------ commands


def cmd_deliveries(a):
    params = f"?status={a.status}" if a.status else ""
    res = call("GET", f"/deliveries{params}")
    out([{k: d[k] for k in ("id", "supplier_name", "species", "status", "stated_quantity", "quantity_unit",
                            "total_inspected", "flagged_count", "partial_count")} for d in res["items"]])


def cmd_show(a):
    d = call("GET", f"/deliveries/{q(a.delivery)}?limit=200")
    fish = []
    for f in d["inspections"]:
        views = {v["view_side"]: v for v in f["views"]}
        fish.append({
            "seq": f["sequence_in_delivery"], "status": f["status"], "flagged": f["flagged_for_review"],
            "flag_reasons": f["flag_reasons"],
            "views": {side: {"view_id": v["id"], "grade": v["freshness_grade"], "mode": v["inference_mode"],
                             "defects": [f"{x['label']} {x['confidence']:.2f}" for x in v["defects"]]}
                      for side, v in views.items()},
        })
    out({"delivery": d["delivery"], "fish": fish,
         "dispositions": d["dispositions"], "movements": d["movements"]})


def cmd_trace(a):
    out(call("GET", f"/deliveries/{q(a.delivery)}/trace"))


def cmd_provenance(a):
    out(call("GET", f"/deliveries/lots/{q(a.lot)}/provenance"))


def cmd_flagged(a):
    """Save annotated photos of every flagged fish so they can be posted with send_attachment."""
    d = call("GET", f"/deliveries/{q(a.delivery)}?limit=200")
    os.makedirs(a.out, exist_ok=True)
    saved = []
    for f in d["inspections"]:
        if not f["flagged_for_review"]:
            continue
        for v in f["views"]:
            img = call("GET", f"/switchroom/views/{v['id']}/annotated.jpg", raw=True)
            path = os.path.abspath(os.path.join(a.out, f"{a.delivery}_seq{f['sequence_in_delivery']:03d}_{v['view_side']}.jpg"))
            with open(path, "wb") as fh:
                fh.write(img)
            saved.append({"seq": f["sequence_in_delivery"], "side": v["view_side"], "path": path,
                          "defects": [f"{x['label']} {x['confidence']:.2f}" for x in v["defects"]],
                          "grade": v["freshness_grade"]})
        if not f["views"]:
            saved.append({"seq": f["sequence_in_delivery"], "side": None, "path": None, "note": f["status"]})
    out({"delivery": a.delivery, "saved": saved})


def cmd_propose_disposition(a):
    payload = {"disposition": a.disposition.upper(), "affected_quantity": a.qty, "quantity_unit": a.unit,
               "output_lot_id": a.lot, "decision_reason": a.reason}
    if a.supersedes:
        payload["supersedes_id"] = a.supersedes
    out(call("POST", "/switchroom/proposals", {"kind": "disposition", "delivery_id": a.delivery,
                                               "payload": payload, "source_message_id": a.message_id}))


def cmd_propose_movement(a):
    payload = {"stage": a.stage, "input_ref": a.input_ref, "output_lot_id": a.out_lot,
               "quantity_in": a.qty_in, "quantity_out": a.qty_out, "quantity_unit": a.unit,
               "normal_yield_loss": a.yield_loss, "qc_reject_loss": a.reject_loss,
               "unexplained_variance": a.variance, "notes": a.notes}
    out(call("POST", "/switchroom/proposals", {"kind": "movement", "delivery_id": a.delivery,
                                               "payload": payload, "source_message_id": a.message_id}))


def cmd_proposal(a):
    out(call("GET", f"/switchroom/proposals/{q(a.id)}"))


def cmd_proposals(a):
    params = urllib.parse.urlencode({k: v for k, v in (("delivery_id", a.delivery), ("status", a.status)) if v})
    out(call("GET", f"/switchroom/proposals{'?' + params if params else ''}"))


def main() -> None:
    p = argparse.ArgumentParser(prog="qcctl", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("deliveries", help="list deliveries"); s.add_argument("--status"); s.set_defaults(fn=cmd_deliveries)
    s = sub.add_parser("show", help="one delivery: fish, flags, dispositions, movements"); s.add_argument("delivery"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("trace", help="lineage, balance and missing links"); s.add_argument("delivery"); s.set_defaults(fn=cmd_trace)
    s = sub.add_parser("provenance", help="walk a lot back to its delivery"); s.add_argument("lot"); s.set_defaults(fn=cmd_provenance)
    s = sub.add_parser("flagged", help="save annotated photos of flagged fish"); s.add_argument("delivery")
    s.add_argument("--out", default=os.path.join(os.getcwd(), "flagged")); s.set_defaults(fn=cmd_flagged)

    s = sub.add_parser("propose-disposition", help="draft a disposition (a person must approve it)")
    s.add_argument("delivery"); s.add_argument("--disposition", required=True, choices=["ACCEPT", "REJECT", "REPROCESS", "DOWNGRADE", "accept", "reject", "reprocess", "downgrade"])
    s.add_argument("--qty", type=float, required=True); s.add_argument("--unit", default="kg", choices=["kg", "count"])
    s.add_argument("--lot", help="output lot id (required unless REJECT)"); s.add_argument("--reason", required=True)
    s.add_argument("--supersedes", type=int, help="disposition id this corrects"); s.add_argument("--message-id")
    s.set_defaults(fn=cmd_propose_disposition)

    s = sub.add_parser("propose-movement", help="draft a material movement (an operator must confirm it)")
    s.add_argument("delivery"); s.add_argument("--stage", required=True, choices=[
        "receiving_to_storage", "receiving_to_processing", "processing_wggs", "processing_fillet",
        "storage_to_processing", "processing_to_dispatch"])
    s.add_argument("--input-ref", required=True, help="delivery id for receiving_* stages, else the input lot id")
    s.add_argument("--out-lot", required=True); s.add_argument("--qty-in", type=float, required=True)
    s.add_argument("--qty-out", type=float, required=True); s.add_argument("--unit", default="kg", choices=["kg", "count"])
    s.add_argument("--yield-loss", type=float, default=0.0, help="normal removal: gills/guts/scales, head/bones/skin")
    s.add_argument("--reject-loss", type=float, default=0.0); s.add_argument("--variance", type=float, default=0.0)
    s.add_argument("--notes"); s.add_argument("--message-id"); s.set_defaults(fn=cmd_propose_movement)

    s = sub.add_parser("proposal", help="show one proposal (DP-n / MV-n)"); s.add_argument("id"); s.set_defaults(fn=cmd_proposal)
    s = sub.add_parser("proposals", help="list proposals"); s.add_argument("--delivery"); s.add_argument("--status"); s.set_defaults(fn=cmd_proposals)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
