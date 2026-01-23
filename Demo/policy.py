import json
from typing import Dict, List, Tuple
from pathlib import Path


class InvariantResult:
    def __init__(self, ok: bool, code: str):
        self.ok = ok
        self.code = code

    def to_dict(self) -> Dict:
        return {"ok": self.ok, "code": self.code}


class Policy:
    """
    Policy is a set of invariants evaluated at the irreversible action boundary.
    This is intentionally generic and non-domain-specific.
    """

    def __init__(self):
        # In a real system, these could be config-driven. For demo: fixed.
        self._invariants = [
            self._inv_action_type_recognized,
            self._inv_authority_token_required_for_restricted,
        ]

    def describe(self) -> Dict:
        # A stable description that can be hashed for policy_hash.
        return {
            "policy_name": "execution-governance-demo-policy",
            "version": 1,
            "invariants": [
                {"code": "INV-01", "name": "ACTION_TYPE_RECOGNIZED"},
                {"code": "INV-02", "name": "AUTHORITY_TOKEN_FOR_RESTRICTED_ACTIONS"},
            ],
            "fail_closed": True,
        }

    def evaluate(self, action: Dict) -> Tuple[bool, List[str]]:
        """
        Returns (allow, reason_codes). Fail-closed: any error => VETO.
        """
        reasons: List[str] = []
        try:
            for inv in self._invariants:
                r = inv(action)
                if not r.ok:
                    reasons.append(r.code)
            allow = (len(reasons) == 0)
            return allow, reasons
        except Exception:
            # Fail-closed: treat evaluation error as veto
            return False, ["INV-00"]  # INV-00 = evaluation failed / unknown

    # --- invariants ---

    def _inv_action_type_recognized(self, action: Dict) -> InvariantResult:
        # INV-01: ensure action type is among allowed enum
        action_type = action.get("action_type")
        allowed = {"EXTERNAL_CALL", "WRITE_ONCE", "STATE_TRANSITION"}
        ok = action_type in allowed
        return InvariantResult(ok=ok, code="INV-01")

    def _inv_authority_token_required_for_restricted(self, action: Dict) -> InvariantResult:
        # INV-02: if action_class is RESTRICTED, require authority token.
        ctx = action.get("context", {})
        action_class = ctx.get("action_class", "GENERIC")
        token_present = bool(ctx.get("authority_token_present", False))
        if action_class == "RESTRICTED":
            ok = token_present
        else:
            ok = True
        return InvariantResult(ok=ok, code="INV-02")


def _append_jsonl(path: Path, obj: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")


def authorize_then_execute(
    action: Dict,
    run_id: str,
    policy: Policy,
    policy_hash: str,
    inputs_hash: str,
    executed_actions_path: Path,
    now_ts: str,
) -> Tuple[Dict, bool]:
    """
    The non-bypassable irreversible boundary.

    - Always emits a DecisionRecord to logs (handled by caller).
    - Only commits execution to the irreversible sink on ALLOW.
    """
    allow, reason_codes = policy.evaluate(action)

    decision = "ALLOW" if allow else "VETO"
    execution_committed = False

    if allow:
        # Irreversible sink: append an executed action record
        exec_record = {
            "ts": now_ts,
            "run_id": run_id,
            "action_id": action["action_id"],
            "action_type": action["action_type"],
            "payload_hash": action["payload_hash"],
        }
        _append_jsonl(executed_actions_path, exec_record)
        execution_committed = True

    decision_record = {
        "ts": now_ts,
        "run_id": run_id,
        "policy_hash": policy_hash,
        "action_id": action["action_id"],
        "decision": decision,
        "reason_codes": reason_codes,
        "inputs_hash": inputs_hash,
        "execution_committed": execution_committed,
    }

    return decision_record, execution_committed
