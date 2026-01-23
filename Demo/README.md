Black-Box Demo — Execution-Time Governance at the Irreversible Action Boundary
## Demo video
▶️ Black-box demo (VETO ⇒ no commit, ALLOW ⇒ commit): https://github.com/indyh91/execution-governance/releases/tag/demo-v1

This folder contains a minimal, non-domain-specific demo harness that proves one hard property:

**VETO ⇒ the irreversible commit record does not change**  
**ALLOW ⇒ the irreversible commit record changes**

The demo is intentionally generic. It does **not** expose MAS internals, trading logic, or proprietary system details. It demonstrates the **execution-time governance topology**:

> A proposed irreversible action is **blocked by default** and only **committed** when explicitly authorized by an invariant-based enforcement layer (fail-closed).

---

## What this proves

For each proposed action, the enforcement boundary `authorize_then_execute(...)` produces:

- a decision: `ALLOW` or `VETO`
- reason codes for veto decisions
- an auditable decision record
- an irreversible commit effect **only on ALLOW**

The key observable is the **execution commit record**:

- `out/executed_actions.jsonl`

If the decision is **VETO**, no executed action is appended.  
If the decision is **ALLOW**, an executed action is appended.

---

## Files

- `demo_cli.py` — CLI entrypoint (runs scenarios)
- `policy.py` — policy + invariants + non-bypassable boundary `authorize_then_execute(...)`
- `scenarios.json` — two scenarios:
  - `S1` → expected `VETO`
  - `S2` → expected `ALLOW`

Generated outputs (created at runtime, not committed):
- `out/decision_log.jsonl` — auditable decision records
- `out/executed_actions.jsonl` — irreversible commit record (changes only on ALLOW)
- `out/counters.json` — proposed/vetoed/allowed/executed counts

---

## Quickstart (PowerShell)

From inside this `Demo/` directory:

```powershell
# Clean previous outputs
if (Test-Path out) { Remove-Item -Recurse -Force out }

# Run VETO scenario (S1)
python .\demo_cli.py --scenario S1 --out out

# Prove no commit happened
if (Test-Path out\executed_actions.jsonl) { Get-Content out\executed_actions.jsonl } else { "No executed_actions.jsonl (expected after VETO)" }

# Run ALLOW scenario (S2)
python .\demo_cli.py --scenario S2 --out out

# Prove commit happened
Get-Content out\executed_actions.jsonl
Get-Content out\decision_log.jsonl -Tail 2
Get-Content out\counters.json

Output interpretation
S1 (VETO):

DECISION=VETO

EXECUTED=NO

out/executed_actions.jsonl remains empty / absent

S2 (ALLOW):

DECISION=ALLOW

EXECUTED=YES

out/executed_actions.jsonl contains a new executed action record

This demonstrates fail-closed, non-bypassable execution-time governance at the boundary.

Notes
This demo is a minimal proof of the boundary property, not a full system implementation.

Reason codes are intentionally generic (e.g., INV-02) to avoid leaking domain-specific logic.


All domain-specific implementation details remain outside this demo.
