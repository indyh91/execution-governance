# ADVERSARIAL_LIMITS

## Purpose

This document enumerates **explicit assumptions, limits, and adversarial considerations** of the execution governance approach defined in this repository.

It exists to:
- prevent overclaiming
- preempt hostile or careless misinterpretation
- distinguish what is proven from what is not
- clarify where responsibility remains with system designers

This document intentionally constrains the scope of the claim.

---

## What This Work Does NOT Claim

This repository does **not** claim to solve:

- decision optimality
- alignment of intent
- prediction accuracy
- elimination of all system failure
- absolute safety under all conditions
- immunity to adversarial agents
- correctness of long-term planning

The claim is strictly limited to **execution-time correctness enforcement** at the irreversible action boundary.

---

## Core Assumptions

The correctness guarantees described in this work rely on the following assumptions.

If any assumption is violated, the guarantees do not hold.

---

### A1. Complete Mediation of Irreversible Actions

**Assumption:**  
All irreversible or high-impact actions are routed through a single, non-bypassable execution interface.

**Adversarial Risk:**  
If an agent can trigger irreversible effects through an unmediated side channel (e.g., undocumented APIs, covert signaling, hardware-level access), execution governance cannot intercept the action.

**Mitigation:**  
Execution governance must be placed at the lowest viable execution layer, below agent logic and above the environment.

---

### A2. Non-Bypassability of the Governance Layer

**Assumption:**  
The execution governance layer cannot be disabled, overridden, or circumvented by the decision system.

**Adversarial Risk:**  
A sufficiently privileged or self-modifying agent could attempt to disable governance checks.

**Mitigation:**  
Governance must be implemented as part of the trusted computing base or enforced by external infrastructure not controlled by the agent.

---

### A3. Deterministic Veto Semantics

**Assumption:**  
The governance layer produces deterministic authorization outcomes for identical execution contexts.

**Adversarial Risk:**  
If governance behavior is probabilistic, adaptive, or state-corruptible, correctness guarantees degrade into likelihood estimates.

**Mitigation:**  
Governance logic must be deterministic and side-effect-free with respect to authorization decisions.

---

### A4. Suppression Is an Acceptable Outcome

**Assumption:**  
System designers accept that suppression (inaction) is a valid and correct terminal outcome.

**Adversarial Risk:**  
Operational pressure may incentivize bypassing governance to maintain throughput or availability.

**Mitigation:**  
Systems must be explicitly designed to treat non-execution as success under uncertainty, not failure.

---

### A5. Timely Execution-Time Evaluation

**Assumption:**  
Authorization is evaluated immediately prior to execution, using live context.

**Adversarial Risk:**  
If authorization is evaluated too early, assumptions may become stale and unsafe.

**Mitigation:**  
Governance must be positioned as close as possible to the execution boundary.

---

## Known Limitations

These limitations are **fundamental**, not implementation defects.

---

### L1. Cumulative and Long-Horizon Effects

Execution governance evaluates individual actions or bounded contexts.

It does not inherently detect:
- long-term drift
- cumulative harm from individually safe actions
- delayed irreversibility

Example:
A sequence of small, permitted actions may collectively lead to an unsafe state.

This is an open problem.

---

### L2. Domain-Specific Policy Definition

Governance correctness depends on policy quality.

Incorrect, incomplete, or naive policies can:
- over-block safe actions
- under-block unsafe ones

Policy design requires domain expertise and cannot be fully automated.

---

### L3. Latency-Sensitive Domains

In ultra-low-latency environments:
- governance checks may introduce unacceptable delay
- suppression may itself cause harm

This approach is best suited to systems where:
- irreversible harm outweighs momentary hesitation
- safety dominates throughput

---

### L4. Adversarial or Malicious Agents

This work assumes cooperative agents.

An agent intentionally attempting to:
- disable governance
- exploit policy loopholes
- manipulate authorization inputs

falls outside the scope of this claim.

Execution governance is not a substitute for adversarial security.

---

### L5. Human Override Risk

If humans are included as authorization authorities:
- alert fatigue
- rubber-stamping
- delayed response

can reintroduce risk.

This work does not claim to solve human reliability.

---

## Failure Modes That Remain Possible

Even with execution governance, the following remain possible:

- indefinite suppression (system stalls)
- safe but suboptimal outcomes
- inability to act in novel conditions
- operational frustration
- false positives

These are **preferred** to irreversible failure.

---

## Why These Limits Do Not Weaken the Claim

The claim does not assert total safety.

It asserts **deterministic prevention of unauthorized irreversible execution** under stated conditions.

The limits above:
- bound applicability
- clarify responsibility
- prevent misinterpretation

They do not invalidate the core result.

---

## Adversarial Summary

Execution governance fails only when:

- irreversibility is unobservable
- execution is unmediated
- veto authority is bypassed
- suppression is treated as failure
- governance itself is compromised

These are **architectural violations**, not logical flaws.

---

## Conclusion

This work intentionally trades:
- completeness for correctness
- throughput for safety
- optimism for determinism

Within its stated scope, the guarantees are structural and enforceable.

Outside that scope, no guarantees are claimed.

This document completes the adversarial boundary of the system.
