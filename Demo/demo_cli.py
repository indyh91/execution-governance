#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from policy import Policy, authorize_then_execute


def utc_ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_json(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")


def get_git_head() -> str:
    # Best-effort: we don't want demo to fail if git isn't present.
    try:
        import subprocess
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return "UNKNOWN"


def policy_hash(policy: Policy) -> str:
    # Hash the policy description deterministically (not the whole code).
    return sha256_json(policy.describe())


def make_run_id(git_head: str) -> str:
    # Unique enough for demo: time + short commit
    short = git_head[:8] if git_head != "UNKNOWN" else "nogit"
    return f"demo-{short}-{int(time.time())}"


def load_scenario(scenarios: dict, scenario_id: str) -> dict:
    if scenario_id not in scenarios:
        raise ValueError(f"Unknown scenario_id: {scenario_id}. Available: {list(scenarios.keys())}")
    return scenarios[scenario_id]


def main() -> int:
    parser = argparse.ArgumentParser(description="Execution Governance Black-Box Demo (VETO/ALLOW).")
    parser.add_argument("--scenario", required=True, help="Scenario id (e.g., S1 or S2)")
    parser.add_argument("--out", default="demo/out", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out)
    decision_log = out_dir / "decision_log.jsonl"
    executed_actions = out_dir / "executed_actions.jsonl"
    counters_path = out_dir / "counters.json"

    scenarios_path = Path(__file__).resolve().parent / "scenarios.json"
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))

    scenario = load_scenario(scenarios, args.scenario)

    # Build policy and run metadata
    git_head = get_git_head()
    run_id = make_run_id(git_head)
    pol = Policy()
    pol_hash = policy_hash(pol)

    # Load / init counters
    counters = read_json(counters_path, {
        "proposed": 0,
        "vetoed": 0,
        "allowed": 0,
        "executed_committed": 0
    })

    # Create a proposed action (note: payload is hashed; we don't store payload in logs)
    action = {
        "action_id": scenario["action_id"],
        "action_type": scenario["action_type"],
        "payload_hash": sha256_bytes(scenario["payload"].encode("utf-8")),
        "context": {
            "env": "demo",
            "scenario": args.scenario,
            "authority_token_present": bool(scenario.get("authority_token_present", False)),
            "action_class": scenario.get("action_class", "GENERIC"),
        }
    }
    inputs_hash = sha256_json(action)

    # Counters: proposed increments always
    counters["proposed"] += 1

    # Execute through the ONLY boundary
    decision_record, executed = authorize_then_execute(
        action=action,
        run_id=run_id,
        policy=pol,
        policy_hash=pol_hash,
        inputs_hash=inputs_hash,
        executed_actions_path=executed_actions,
        now_ts=utc_ts(),
    )

    # Counters depend on decision
    if decision_record["decision"] == "ALLOW":
        counters["allowed"] += 1
    else:
        counters["vetoed"] += 1

    if decision_record["execution_committed"]:
        counters["executed_committed"] += 1

    # Persist decision + counters
    append_jsonl(decision_log, decision_record)
    write_json(counters_path, counters)

    # Print a crisp summary line for the video
    reasons = decision_record["reason_codes"]
    print(f"GIT_HEAD={git_head}")
    print(f"RUN_ID={run_id} POLICY_HASH={pol_hash}")
    print(f"SCENARIO={args.scenario} ACTION_ID={action['action_id']} TYPE={action['action_type']}")
    print(f"DECISION={decision_record['decision']} REASONS={reasons} EXECUTED={'YES' if executed else 'NO'}")
    print(f"COUNTERS proposed={counters['proposed']} vetoed={counters['vetoed']} allowed={counters['allowed']} executed={counters['executed_committed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
