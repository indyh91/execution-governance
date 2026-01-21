# Theory Anchor #1 — Reference Monitor for Actions

This document is a *theoretical anchor*.  
It does not introduce new requirements beyond what `/docs/execution-governance.md` already implies.  
Its purpose is to eliminate ambiguity by mapping execution governance to an established concept in computer security: the **reference monitor**.

---

## Why this anchor exists

Execution governance claims deterministic prevention of invalid irreversible actions via an in-path veto layer.

A common objection is that this is “just policy,” “just a workflow,” or “just approvals.”  
This objection survives only when the enforcement mechanism is not named precisely.

In security theory, the structure “untrusted actor + protected operation + non-bypassable mediator with veto” has a name:

> **Reference Monitor**: a mechanism that mediates every security-relevant operation and enforces a policy that the subject cannot bypass.

If execution governance is not a reference monitor (or equivalent), then it cannot claim deterministic prevention — only detection.

---

## Reference monitor trust conditions (non-negotiable)

A reference monitor is trustworthy only if it satisfies all of the following:

1. **Complete mediation**  
   Every security-relevant operation is checked. Not “most,” not “usually,” not “when convenient.”

2. **Tamperproofness**  
   The subject being governed cannot modify, disable, or influence the monitor’s enforcement logic.

3. **Verifiability (analyzable correctness)**  
   The monitor is small/simple enough — and isolated enough — that its enforcement behavior can be meaningfully analyzed, tested, or proven.

If any of these are false, the mechanism is not a reference monitor in the sense required to claim prevention.

---

## Mapping: reference monitor → execution governance

| Security theory term | Execution governance term |
|---|---|
| Subject (untrusted principal) | Autonomous agent / controller / planner |
| Security-relevant operation | Outbound action at an irreversible boundary (API call, capital movement, infra mutation) |
| Protected object | Environment state + invariants defining what transitions are valid |
| Policy | Non-probabilistic execution invariants / risk gates |
| Reference monitor | In-path execution governance layer |
| “Decision procedure” | Deterministic veto logic based on real-time state validity |
| Trusted computing base (TCB) | Governance layer + its state authority + its enforcement perimeter |

This mapping matters because it pins down what must be true for “prevention” to be a coherent claim.

---

## What “alternatives” must prove to be logically equivalent

A proposed substitute (approvals, monitoring, rollback, confidence thresholds, dashboards) is only equivalent if it can demonstrate the same three trust conditions.

### Test 1 — Complete mediation
Show *where* the mechanism interposes on every outbound action.

If the check happens only:
- at planning time,
- at “approval time,”
- after execution (monitoring),
- or on a subset of actions (sampling),

then complete mediation is false.

### Test 2 — Tamperproofness
Show that the governed system cannot:
- disable the gate,
- swap the policy,
- downgrade enforcement,
- route around the mediator,
- or execute actions through an ungoverned channel.

If bypass exists “for emergencies,” then the mechanism is not a reference monitor; it is advisory governance.

### Test 3 — Verifiability
Show that the enforcement mechanism is bounded enough to be audited as a unit.

If the enforcement logic is:
- distributed across unbounded code paths,
- implemented as a probabilistic classifier,
- or dependent on the subject’s own claims,

then verifiability is false.

---

## Why this tightens the execution governance claim

Once execution governance is named as a reference monitor for actions, the debate is no longer “do you like governance?”

The debate becomes:

> **How do you achieve complete mediation, tamperproofness, and analyzable correctness at the irreversible action boundary?**

Any alternative that cannot answer this is not competing on prevention; it is competing on process.

---

## References (for lineage, not authority)

- Saltzer, J. H., & Schroeder, M. D. (1975). *The Protection of Information in Computer Systems*. Proceedings of the IEEE.
- Schneider, F. B. (2000). *Enforceable Security Policies*. ACM Transactions on Information and System Security.
- Jaeger, T. (reference monitor notes / lecture material), for concise statement of the three reference monitor requirements.
