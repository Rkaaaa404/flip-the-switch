#!/usr/bin/env python3
"""Wire a local Switch to NusaQC's Receiving QC Room. Safe to re-run. Standard library only.

What it does, in order:
  1. Mattermost: create the demo accounts qc.supervisor, floor.operator and auditor (Docker mmctl).
  2. Switch: create matching Switch users and claim each Mattermost identity for them, so Switch
     puts a stable, verified sender id on everything they type.
  3. Add the three people to the `receiving-qc` room.
  4. Register `qc-gate` (a custom agent with no LLM), add it to the room, and set its addressing
     policy: plant users in this room may address it, and no agent may. Writes code/switch/gate/.env.
  5. Install qc-agent's tool and instructions into its Switch working folder, with its API token.

Before running it:
  - Switch Console is running, with a Mattermost messaging app connected.
  - You created the `receiving-qc` room and the `qc-agent` Claude Code agent in Console.
  - code/webdev/backend/.env has QC_AGENT_TOKEN and QC_GATE_TOKEN set.

    python code/switch/setup/setup_switch.py --password '<demo password>'

Then seed the demo data, which also maps the three Switch sender ids to plant roles:

    cd code/webdev/backend && uv run python scripts/seed_demo.py --bridge <bridge id printed here>
"""

import argparse
import http.cookiejar
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SWITCH_DIR = REPO / "code" / "switch"
BACKEND_ENV = REPO / "code" / "webdev" / "backend" / ".env"
DEFAULT_SWITCH_ENV = Path.home() / "AppData/Roaming/switchdash/local-switch-server/native/run/switch-core.env"
DEFAULT_AGENT_DIR = Path.home() / ".switch/agents/localhost-57078/qc-agent"
PEOPLE = {"qc.supervisor": "QC Supervisor", "floor.operator": "Floor Operator", "auditor": "Auditor"}
ROOM_DESCRIPTION = "Receiving QC for incoming fish deliveries"
ROOM_INSTRUCTIONS = (
    "Receiving QC for incoming fish deliveries. qc-agent summarizes inspection runs, posts flagged photos and "
    "drafts records. Only people sign, with `@qc-gate approve DP-n`, `@qc-gate reject DP-n <reason>`, "
    "`@qc-gate confirm MV-n` or `@qc-gate status DEL-...`."
)


def read_env(path: Path) -> dict[str, str]:
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip('"')
    return env


class Client:
    """JSON over HTTP with a cookie jar (the Switch gateway logs in with a cookie)."""

    def __init__(self, base: str, headers: dict | None = None):
        self.base = base.rstrip("/")
        self.headers = headers or {}
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(self, method: str, path: str, body=None, ok=(200, 201, 204)):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method, headers=dict(self.headers))
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with self.opener.open(req, timeout=30) as resp:
                raw = resp.read()
                return resp.status, (json.loads(raw) if raw else None), resp.headers
        except urllib.error.HTTPError as exc:
            text = exc.read().decode(errors="replace")
            if exc.code in ok:
                return exc.code, None, exc.headers
            raise SystemExit(f"{method} {path} -> {exc.code}: {text[:300]}") from None


def items(data, *keys):
    if isinstance(data, list):
        return data
    for key in keys:
        if isinstance(data, dict) and isinstance(data.get(key), list):
            return data[key]
    return []


def step(msg: str) -> None:
    print(f"\n== {msg}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--password", required=True, help="password for the three demo chat accounts")
    p.add_argument("--switch-url", default="http://localhost:57078")
    p.add_argument("--mattermost-url", default="http://127.0.0.1:57079")
    p.add_argument("--mattermost-container", default="switchdash-local-mattermost-mattermost-1")
    p.add_argument("--mattermost-team", default="switch")
    p.add_argument("--switch-env", type=Path, default=DEFAULT_SWITCH_ENV, help="holds GATEWAY_ADMIN_EMAIL/PASSWORD")
    p.add_argument("--room", default="receiving-qc")
    p.add_argument("--fresh-room", action="store_true",
                   help="archive the existing room of that name (reversible) and create a new, empty one")
    p.add_argument("--agent-dir", type=Path, default=DEFAULT_AGENT_DIR, help="qc-agent's Switch working folder")
    p.add_argument("--api-url", default="http://localhost:8000", help="NusaQC backend")
    a = p.parse_args()

    tokens = read_env(BACKEND_ENV)
    for key in ("QC_AGENT_TOKEN", "QC_GATE_TOKEN"):
        if not tokens.get(key):
            raise SystemExit(f"{key} is empty in {BACKEND_ENV}. Generate one: python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
    admin = read_env(a.switch_env)

    step("Mattermost accounts")
    for username in PEOPLE:
        create = subprocess.run(
            ["docker", "exec", a.mattermost_container, "mmctl", "--local", "user", "create",
             "--email", f"{username}@nusaqc.local", "--username", username, "--password", a.password],
            capture_output=True, text=True)
        exists = "already exists" in (create.stdout + create.stderr).lower() or "exists" in create.stderr.lower()
        print(f"  {username}: {'created' if create.returncode == 0 else 'exists' if exists else create.stderr.strip()[:120]}")
        subprocess.run(["docker", "exec", a.mattermost_container, "mmctl", "--local", "team", "users", "add",
                        a.mattermost_team, username], capture_output=True, text=True)
    mm_ids = {}
    for username in PEOPLE:
        mm = Client(a.mattermost_url + "/api/v4")
        _, me, _ = mm.call("POST", "/users/login", {"login_id": username, "password": a.password})
        mm_ids[username] = me["id"]

    sw = Client(a.switch_url)
    sw.call("POST", "/gateway/auth/login", {"email": admin["GATEWAY_ADMIN_EMAIL"], "password": admin["GATEWAY_ADMIN_PASSWORD"]})

    step("Mattermost bridge")
    _, bridges, _ = sw.call("GET", "/gateway/collaborations")
    bridges = items(bridges, "bridges", "items", "collaborations")
    mm_bridges = [b for b in bridges if b.get("bridge_type") == "mattermost" and b.get("status") == "active"]
    if len(mm_bridges) != 1:
        raise SystemExit(f"expected one active Mattermost bridge in Switch, found {len(mm_bridges)}")
    bridge = mm_bridges[0]["bridge_id"]
    print(f"  bridge {bridge}")

    step("Switch users and identity claims")
    _, users, _ = sw.call("GET", "/gateway/users")
    by_email = {u["email"]: u for u in items(users, "users", "items")}
    for username in PEOPLE:
        user = by_email.get(f"{username}@nusaqc.local")
        if user is None:
            _, user, _ = sw.call("POST", "/gateway/users", {"name": username, "email": f"{username}@nusaqc.local",
                                                            "password": a.password, "role": "user"})
        sw.call("POST", f"/gateway/collaborations/{bridge}/identities",
                {"external_user_id": mm_ids[username], "username": username, "user_id": user["id"]})
        print(f"  {username}: Switch user {user['id']} claims Mattermost {mm_ids[username]}")

    step(f"Room {a.room}")
    _, rooms, _ = sw.call("GET", "/gateway/rooms")
    room = next((r for r in items(rooms, "rooms", "items") if r.get("name") == a.room and not r.get("archived")), None)
    if room is not None and a.fresh_room:
        sw.call("POST", f"/gateway/rooms/{room['id']}/archive")
        print(f"  archived old room {room['id']} (unarchive: POST /gateway/rooms/{room['id']}/unarchive)")
        room = None
    if room is None:
        _, agents, _ = sw.call("GET", "/gateway/agents")
        if not any(x.get("name") == "qc-agent" for x in items(agents, "agents", "items")):
            raise SystemExit("create the qc-agent Claude Code agent in Switch Console first")
        _, room, _ = sw.call("POST", "/gateway/rooms", {
            "name": a.room, "description": ROOM_DESCRIPTION, "instructions": ROOM_INSTRUCTIONS,
            "agent_names": ["qc-agent"], "user_names": list(PEOPLE), "bridge_id": bridge,
            "channel_type": "channel_public"})
        print(f"  created room {room['id']} with qc-agent")
    sw.call("POST", f"/gateway/rooms/{room['id']}/users", {"user_names": list(PEOPLE)}, ok=(200, 201, 204, 409))
    print(f"  room {room['id']}: added {', '.join(PEOPLE)}")

    step("qc-gate")
    gate_env = SWITCH_DIR / "gate" / ".env"
    _, agents, _ = sw.call("GET", "/gateway/agents")
    gate = next((x for x in items(agents, "agents", "items") if x.get("name") == "qc-gate"), None)
    if gate is None:
        _, reg, _ = sw.call("POST", "/gateway/agents/register-other", {
            "name": "qc-gate", "display_name": "QC Gate",
            "description": "Signs NusaQC records from verified chat commands. No LLM."})
        gate_id = reg["id"]
        gate_env.write_text(
            f"SWITCH_URL={a.switch_url}\nQC_GATE_AGENT_ID={gate_id}\nQC_GATE_API_KEY={reg['api_key']}\n"
            f"QC_ROOM_ID={room['id']}\nQC_API_URL={a.api_url}\nQC_GATE_TOKEN={tokens['QC_GATE_TOKEN']}\n",
            encoding="utf-8")
        print(f"  registered {gate_id}; key saved to {gate_env}")
    else:
        gate_id = gate["id"]
        if not gate_env.exists():
            raise SystemExit(f"qc-gate {gate_id} exists but {gate_env} is missing; its API key is shown only once. "
                             "Delete the agent in Console and re-run.")
        print(f"  already registered: {gate_id}")
        lines = [ln for ln in gate_env.read_text(encoding="utf-8").splitlines() if not ln.startswith("QC_ROOM_ID=")]
        gate_env.write_text("\n".join(lines + [f"QC_ROOM_ID={room['id']}"]) + "\n", encoding="utf-8")
        print(f"  QC_ROOM_ID={room['id']} written to {gate_env} (restart the relay to pick it up)")
    sw.call("POST", f"/gateway/rooms/{room['id']}/agents", {"agent_ids": [gate_id]}, ok=(200, 201, 204, 409))
    # Layer 1: in this room any plant user may address the gate, and no agent may (qc-agent included).
    sw.call("PUT", f"/gateway/agents/{gate_id}/addressing-policy",
            {"policy": {"rules": [{"rooms": [room["id"]], "users": "*", "agents": []}]}})
    print("  in room, policy: users=* agents=[]")

    step("qc-agent files")
    a.agent_dir.mkdir(parents=True, exist_ok=True)
    for name in ("qcctl.py", "CLAUDE.md"):
        shutil.copy2(SWITCH_DIR / "agent" / name, a.agent_dir / name)
    (a.agent_dir / ".env").write_text(f"QC_API_URL={a.api_url}\nQC_AGENT_TOKEN={tokens['QC_AGENT_TOKEN']}\n", encoding="utf-8")
    print(f"  installed into {a.agent_dir}")

    print(f"\nDone. Next:\n  cd code/webdev/backend && uv run python scripts/seed_demo.py --bridge {bridge}\n"
          "  python code/switch/gate/main.py")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
