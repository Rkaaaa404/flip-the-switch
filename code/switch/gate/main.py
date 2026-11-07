#!/usr/bin/env python3
"""qc-gate: relays `@qc-gate ...` chat commands, with the sender id Switch issued, to NusaQC.

No LLM and no business logic. It long-polls its Switch agent events and, for every room message
that starts with `@qc-gate`, forwards {sender, sender_name, room_id, message_id, text} to
`POST /api/v1/switchroom/gate/commands`. Then it posts the API's receipt back into the room verbatim.
Who may do what is decided by the API, never here.

Config: `.env` next to this file (written by register.py, plus QC_API_URL and QC_GATE_TOKEN).
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
for line in open(os.path.join(HERE, ".env"), encoding="utf-8"):
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.strip().split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"'))

SWITCH = os.environ["SWITCH_URL"].rstrip("/")
AGENT_ID = os.environ["QC_GATE_AGENT_ID"]
SWITCH_KEY = os.environ["QC_GATE_API_KEY"]
API = os.environ.get("QC_API_URL", "http://localhost:8000").rstrip("/") + "/api/v1"
GATE_TOKEN = os.environ["QC_GATE_TOKEN"]
ADDRESSED = re.compile(r"^\s*@qc-gate\b", re.IGNORECASE)


def http(method: str, url: str, headers: dict, body: dict | None = None, timeout: float = 40):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        return resp.status, (json.loads(raw) if raw else None)


def log(*parts) -> None:
    print(time.strftime("%H:%M:%S"), *parts, flush=True)


def post_to_room(room_id: str, content: str) -> None:
    http("POST", f"{SWITCH}/agents/{AGENT_ID}/message", {"Authorization": f"Bearer {SWITCH_KEY}"},
         {"room_id": room_id, "content": content})


def handle(event: dict) -> None:
    envelope = event.get("data") or event
    if envelope.get("type") != "message":
        return
    payload = envelope.get("payload", envelope)
    body = payload.get("body") or ""
    # Layer 1 is Switch's own addressing policy on qc-gate (plant users only, no agents). A message it
    # refused arrives with addressed=false (Switch has already told the sender), so it is ignored here.
    if not payload.get("addressed") or not ADDRESSED.match(body):
        return
    room_id = envelope.get("room_id")
    command = {
        "sender": payload.get("sender") or "",
        "sender_name": payload.get("sender_name"),
        "room_id": room_id,
        "message_id": payload.get("message_id") or "",
        "text": body,
    }
    log(f"<- {command['sender_name']} ({command['sender']}): {body!r}")
    try:
        _, receipt = http("POST", f"{API}/switchroom/gate/commands", {"X-Api-Token": GATE_TOKEN}, command)
    except urllib.error.HTTPError as exc:
        receipt = {"ok": False, "receipt": f"⛔ Not applied. NusaQC refused the command ({exc.code}).", "replayed": False}
    except urllib.error.URLError as exc:
        receipt = {"ok": False, "receipt": f"⛔ Not applied. NusaQC API is unreachable ({exc.reason}).", "replayed": False}
    if receipt.get("replayed"):
        log("   replay of an already-handled message; not re-posting")
        return
    log(f"-> {receipt['receipt']}")
    if room_id:
        post_to_room(room_id, receipt["receipt"])


def main() -> None:
    log(f"qc-gate {AGENT_ID} polling {SWITCH}; NusaQC API {API}")
    headers = {"Authorization": f"Bearer {SWITCH_KEY}"}
    backoff = 1
    while True:
        try:
            status, data = http("GET", f"{SWITCH}/agents/{AGENT_ID}/events?timeout=25", headers, timeout=40)
            backoff = 1
            if status == 200 and data:
                for event in data.get("events", []):
                    try:
                        handle(event)
                    except Exception as exc:  # one bad event must not stop the gate
                        log("!! event failed:", repr(exc))
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as exc:
            log(f"!! poll failed ({exc!r}); retrying in {backoff}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)


if __name__ == "__main__":
    main()
