# Necessity Argument #1 — TOCTOU + Runtime Enforceability

This document isolates a minimal necessity argument for execution governance.

Goal: eliminate the common escape hatch:
> “We can validate earlier (approvals, pre-checks, confidence thresholds), then execute later.”

That structure is a TOCTOU gap, and it cannot support a deterministic prevention claim in non-idempotent environments.

---

## Setup

We consider a system that produces an action stream:

a₀, a₁, a₂, ...

Some actions cross an irreversible boundary (external side effects).  
Define:

- sᵢ = environment state immediately before action aᵢ
- Valid(sᵢ, aᵢ) = deterministic predicate deciding whether aᵢ is allowed in sᵢ

The prevention claim is a safety requirement:

> For every i, if aᵢ is executed at the irreversible boundary, then Valid(sᵢ, aᵢ) was true at the moment of execution.

Equivalently:
> “No invalid irreversible action ever executes.”

This is a **safety property** (a “nothing bad happens” property).

---

## Lemma 1 — Off-path checks create a TOCTOU gap

If Valid(s, a) is evaluated at time t_check but the action executes at t_use > t_check, then there exists an interval (t_check, t_use) during which s may change.

Therefore, a pre-check establishes at most:

> Valid(s_at_check, a) is true

It does *not* establish:

> Valid(s_at_use, a) is true

Unless the system can prove that state cannot change between check and use, the pre-check cannot justify deterministic prevention.

This is the TOCTOU structure:

- check condition
- later use result
- state changes in between

If your governance mechanism is not colocated with execution (or does not make check+use atomic), it is structurally a TOCTOU risk.

---

## Lemma 2 — Prevention requires runtime enforcement for safety properties

A safety requirement over an action stream can be enforced only if some mechanism can:

1) observe each attempted security-relevant action, and  
2) stop or suppress actions that would violate the requirement.

This is the class of mechanisms studied as **execution monitors** / **runtime enforcement**.

Key point:
- Monitoring alone (observe but cannot block) yields detection.
- Post-hoc rollback yields remediation attempts.
- Neither yields prevention at an irreversible boundary.

---

## Theorem — Deterministic prevention at irreversible boundaries implies in-path suppression

Assume:

A1. Environment state can change between planning and execution (distributed / concurrent world).  
A2. Some actions are irreversible (external side effects).  
A3. The requirement is “no invalid irreversible action executes” (a safety property).

Then any architecture that claims deterministic prevention must include a component that:

- is invoked for every boundary-crossing action (complete mediation),
- evaluates validity against current state (at use time, not only at check time),
- and can suppress the action when invalid.

If any one of these is missing, the architecture does not implement prevention; it implements a weaker property (detection, delay, or best-effort remediation).

This is why an in-path execution governance layer with veto authority is not an “implementation choice”; it is the minimal mechanism class consistent with the prevention claim.

---

## “What if we…” (common escape hatches) — and why they fail as prevention

1) “We do approvals.”  
Approvals are pre-checks unless revalidated at execution time.

2) “We monitor.”  
Monitoring is observation after (or during) execution, not suppression before the boundary.

3) “We rollback.”  
Rollback is not equivalent to prevention in non-idempotent environments with external side effects.

4) “We use model confidence thresholds.”  
Confidence is not a validity predicate over state transitions, and it is not checked at the boundary by default.

All of these can be valuable for other goals; none are logically sufficient substitutes for in-path enforcement.

---

## Minimal escape clause (intellectual honesty)

The necessity argument fails only if you can falsify at least one assumption:

- If actions are not irreversible (the world is fully compensatable), then prevention may be unnecessary.
- If you can make check+use atomic with respect to the relevant state (transaction/lock/commit at the same boundary), you have effectively implemented in-path governance by another name.
- If the requirement is not safety (“something good eventually happens”), runtime suppression alone is insufficient.

---

## References (for lineage, not authority)

- MITRE CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition.
- Schneider, F. B. (2000). Enforceable Security Policies. ACM TISSEC.
- Ligatti, J., Bauer, L., & Walker, D. (2005). Edit Automata: Enforcement Mechanisms for Run-time Security Policies. International Journal of Information Security.
