# Phase 12 — Operational Resource Governance Review

## Executive Governance Summary

This review details the operational resource governance policies, lease mechanics, capacity bounds, and starvation defense implemented in Phase 12 (`src/coordination/`).

---

## 1. Resource Catalog & Granular Scope Control

Phase 12 governs five primary resource categories across multiple concurrent missions:

| Resource ID Category | Resource Type | Default Capacity | Governance Mechanism |
|---|---|---|---|
| `staff:designer` | Human Staff | 2 concurrent tasks | Atomic reservation, max task limit |
| `staff:strategist` | Human Staff | 2 concurrent tasks | Atomic reservation, max task limit |
| `staff:trend_analyst` | Human Staff | 2 concurrent tasks | Atomic reservation, max task limit |
| `quota:model_tokens` | Model Tokens | 1,000,000 tokens/hr | Token bucket & budget hierarchy |
| `account:nocap_social` | Social Account | 1 publisher at a time | Single-lease exclusive lock |
| `calendar:nocap_september` | Content Calendar | 1 editor at a time | Exclusive window lock |
| `slot:execution` | Execution Slot | 10 concurrent slots | Global capacity counter |

---

## 2. Cryptographic Lease Management (`LeaseManager`)

All allocated resources are bound to a cryptographically signed `ResourceLease`:

- **HMAC Signature Generation:** `HMAC-SHA256(secret_key, lease_id + mission_id + resource_id + expires_at)`
- **Short-Lived TTLs:** Default lease TTL is set between 60 to 300 seconds.
- **Auto-Revocation & Purge:** `ResourceManager.purge_expired_leases()` identifies expired leases, frees underlying resources, and logs an expiration audit record.
- **Replay & Tamper Defense:** Any attempt to present a lease with an altered `expires_at`, `mission_id`, or signature throws `LeaseValidationError`.

---

## 3. Hierarchical Capacity Evaluation (`CapacityTracker`)

Resource allocation strictly enforces a three-tier hierarchical limit:

$$\text{Available Capacity} = \min(\text{Mission Budget}, \text{Global Budget}, \text{Rate Limit Bucket})$$

- **Tier 1 (Mission Budget):** Individual mission allocated token and step limits.
- **Tier 2 (Global Budget):** System-wide ceiling ($1,000,000$ tokens/hr, $10$ execution slots).
- **Tier 3 (Rate Limit Buckets):** Sliding window limit of $100$ requests per minute across external APIs.

If any tier is exhausted, arbitration rejects or pauses the requesting mission.

---

## 4. Conflict Engine & Mutation Collision Defense (`ConflictEngine`)

When two missions request resources:
1. **Direct Collision:** Re-reserving an already exclusively leased resource (e.g. `account:nocap_social`).
2. **Mutation Collision:** Concurrent planned mutations targeting overlapping scopes (e.g. Mission $A$ updating Instagram grid while Mission $B$ deletes posts on `account:nocap_social`).

**Resolution Matrix:**
- Higher priority mission acquires lease.
- Lower priority mission is set to `PAUSED` and an `EscalationTicket` is recorded.
- Equal priority: First-come, first-served based on monotonic request timestamp.

---

## 5. Deadlock Detection & Preemption (`DeadlockDetector` & `PreemptionEngine`)

- **Wait-For Graph (WFG):** Maintained dynamically as missions wait for reserved resources.
- **Cycle Detection:** Tarjan's Strongly Connected Components algorithm scans the WFG on every block event.
- **Victim Selection:** When a cycle $C$ is detected, the detector selects the victim mission $V \in C$ with the lowest priority rank and fewest acquired leases.
- **Preemption Execution:** `PreemptionEngine` revokes $V$'s leases, transitions $V$ to `PREEMPTED`, issues an `EscalationTicket`, and allows the remaining missions to proceed without deadlock.

---

## 6. Fairness Engine & Starvation Aging (`FairnessEngine`)

To prevent high-priority missions from indefinitely starving lower-priority missions (e.g. LOW or BACKGROUND):
- **Aging Formula:**
  $$\text{Effective Priority} = \text{Base Priority Score} + \left\lfloor \frac{\text{Wait Time (seconds)}}{30} \right\rfloor$$
- Every 30 seconds of waiting increases a mission's effective priority index, ensuring that prolonged waiting missions eventually preempt or out-arbitrate newly arrived higher-priority requests.
