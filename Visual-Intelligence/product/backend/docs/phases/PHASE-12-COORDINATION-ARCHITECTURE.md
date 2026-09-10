# Phase 12 — Multi-Mission Coordination & Operational Resource Governance Architecture

## Executive Architectural Summary

Phase 12 introduces a bounded **Multi-Mission Control Plane** above the Phase 1–11 baseline (`src/security_substrate/`, `src/agentic_work/`, `src/execution_control/`, `src/mission_control/`). It establishes deterministic coordination, resource arbitration, deadlock detection, fairness management, preemption, dynamic capacity tracking, and append-only hash-linked audit logging across concurrently running marketing, design, and strategic missions.

---

## Architectural Invariants

Phase 12 strictly enforces six core security and structural invariants:

$$\mathbf{Multiple\ Missions} \rightarrow \mathbf{One\ Bounded\ Coordination\ Plane}$$
$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$
$$\mathbf{Coordination \neq Authorization}$$

1. **`INV-12-001` — Strict Authorization Origin:**
   The coordination plane decides mission sequencing and resource allocation, but **CANNOT** originate execution authorization. All downstream actions require valid, externally issued `AuthorizationRecord` tokens from `HumanAuthorizationBoundary`.
2. **`INV-12-002` — Fixed Autonomy Tiers:**
   Coordination mechanisms cannot elevate mission or agent autonomy tiers. Autonomy constraints established in Phase 8–11 remain strictly immutable.
3. **`INV-12-003` — Deterministic Priority Arbitration:**
   Resource requests are resolved deterministically based on mission priority rank (`CRITICAL > HIGH > NORMAL > LOW > BACKGROUND`), request timestamp, and starvation aging factor.
4. **`INV-12-004` — Fail-Closed Conflict Resolution:**
   Resource or mutation collision between missions immediately triggers arbitration. Unresolvable or lower-priority collisions pause the affected mission and issue an `EscalationTicket`.
5. **`INV-12-005` — Cross-Mission Token Scope Isolation:**
   `AuthorizationRecord` tokens issued for Mission $A$ **CANNOT** be reused, inherited, or transferred to Mission $B$. Reusing tokens across missions raises `CrossMissionAuthorizationError`.
6. **`INV-12-006` — Immutable Coordination Security Policies:**
   Phase 9 persistent learning signals, recommendations, and execution metrics cannot modify, weaken, or bypass coordination security or resource limits.

---

## Control Plane Architecture

```
                                  +------------------------------------+
                                  |     HumanAuthorizationBoundary    |
                                  +-----------------+------------------+
                                                    | (Auth Tokens)
                                                    v
+-----------------------------------------------------------------------------------+
|                            MultiMissionCoordinator                                |
|                                                                                   |
|  +------------------------+   +-----------------------+   +--------------------+  |
|  |    MissionRegistry     |   |   ResourceRegistry    |   |    LeaseManager    |  |
|  |  (Cap: 20 Missions)    |   | (Staff, Tokens, Slots)|   | (HMAC-SHA256 TTLs) |  |
|  +-----------+------------+   +-----------+-----------+   +---------+----------+  |
|              |                            |                         |             |
|              v                            v                         v             |
|  +------------------------+   +-----------------------+   +--------------------+  |
|  |     ResourceManager    |   |    ArbitrationEngine  |   |   ConflictEngine   |  |
|  |  (Atomic Reservations) |   |  (Priority & Aging)   |   | (Mutation Overlap) |  |
|  +-----------+------------+   +-----------+-----------+   +---------+----------+  |
|              |                            |                         |             |
|              v                            v                         v             |
|  +------------------------+   +-----------------------+   +--------------------+  |
|  |    FairnessEngine      |   |   DeadlockDetector    |   |  PreemptionEngine  |  |
|  | (Starvation Defense)   |   |   (Tarjan Cycle SCCS) |   | (Victim Preemption)|  |
|  +-----------+------------+   +-----------+-----------+   +---------+----------+  |
|              |                            |                         |             |
|              +----------------------------+-------------------------+             |
|                                           |                                       |
|                                           v                                       |
|                               +-----------------------+                           |
|                               |    CapacityTracker    |                           |
|                               | (Global Rate Limits)  |                           |
|                               +-----------+-----------+                           |
|                                           |                                       |
|                                           v                                       |
|                               +-----------------------+                           |
|                               |   CoordinationLedger  |                           |
|                               | (SHA-256 Audit Trail) |                           |
|                               +-----------------------+                           |
+-----------------------------------------------------------------------------------+
                                            |
                                            v
                               +-------------------------+
                               | MissionCoordinator      | (Phase 11)
                               | ExecutionController     | (Phase 10)
                               +-------------------------+
```

---

## Core Components Overview

### 1. `MissionRegistry` (`src/coordination/mission_registry.py`)
Maintains active and archived missions in memory. Enforces a maximum concurrent active mission cap ($\le 20$). Rejects admission when the system capacity is exceeded.

### 2. `ResourceRegistry` (`src/coordination/resource_registry.py`)
Catalogs shared operational resources:
- `staff:designer`, `staff:strategist`, `staff:trend_analyst` (Human/Staff slots)
- `quota:model_tokens` (Model token budgets)
- `account:nocap_social` (Platform publishing accounts)
- `calendar:nocap_september` (Content calendar slots)
- `slot:execution` (Concurrent execution slots)

### 3. `LeaseManager` (`src/coordination/leases.py`)
Generates cryptographically signed `ResourceLease` tokens using SHA-256 HMAC. Handles TTL calculation, expiration verification, and signature tampering validation.

### 4. `ResourceManager` (`src/coordination/resource_manager.py`)
Performs thread-safe atomic reservations and releases. Rejects double reservations and auto-purges expired leases.

### 5. `ArbitrationEngine` (`src/coordination/arbitration.py`)
Evaluates competing resource requests using priority ranks and dynamic starvation aging factors. Issues deterministic arbitration decisions (`GRANTED`, `PAUSED`, `ESCALATED`).

### 6. `ConflictEngine` (`src/coordination/conflict.py`)
Analyzes incoming resource requests for resource ID overlaps, time window collisions, and planned mutation collisions (e.g. concurrent edits to the same social account or calendar slot).

### 7. `FairnessEngine` (`src/coordination/fairness.py`)
Calculates priority scores and applies aging boosts ($\Delta P = \lfloor \text{wait\_time} / 30 \rfloor$) to prevent low-priority mission starvation.

### 8. `DeadlockDetector` (`src/coordination/deadlock.py`)
Constructs a Wait-For Graph (WFG) of resource dependencies across missions. Uses Tarjan's Strongly Connected Components algorithm to find cyclic deadlocks and selects victim missions for preemption based on priority and lowest runtime cost.

### 9. `PreemptionEngine` (`src/coordination/preemption.py`)
Executes victim preemption by revoking active leases, releasing capacity, and transitioning affected missions to `PREEMPTED` state while logging escalation tickets.

### 10. `CapacityTracker` (`src/coordination/capacity.py`)
Tracks hierarchical global limits (`min(mission_budget, global_budget, rate_limit_bucket)`):
- Max active token usage ($1,000,000$ tokens/hr)
- Max concurrent staff tasks ($5$ active tasks)
- Max active execution slots ($10$ concurrent slots)
- API rate-limit buckets ($100$ reqs/min)

### 11. `CoordinationLedger` (`src/coordination/coordination_ledger.py`)
Provides an append-only, SHA-256 hash-linked immutable ledger stored in `data/phase12_ledger/coordination_ledger.jsonl`. Verifies ledger chain integrity against tampering.

### 12. `MultiMissionCoordinator` (`src/coordination/coordinator.py`)
The top-level orchestrator. Coordinates admission, resource requests, arbitration, preemption, execution via Phase 11 `MissionCoordinator` and Phase 10 `ExecutionController`, and audit logging.

---

## Multi-Mission Coordination Workflow

1. **Mission Admission:** Host registers missions with `MultiMissionCoordinator.admit_mission(...)`.
2. **Resource Request & Arbitration:** Missions submit resource requirements. `ArbitrationEngine` and `ConflictEngine` check capacity, lease validity, and mutation collisions.
3. **Lease Issuance:** On approval, `LeaseManager` generates a signed `ResourceLease`.
4. **Execution & Boundary Check:** Missions execute actions using Phase 10/11 control planes. `MultiMissionCoordinator` validates authorization token bindings (`INV-12-005`).
5. **Release & Purge:** On mission completion or preemption, resources are released and leases purged.
6. **Audit Trail:** Every state change, arbitration decision, lease issuance, and conflict resolution is appended to the SHA-256 hash-linked ledger.
