# PHASE-11-THREAT-MODEL.md

# Phase 11 — Threat Model & Operational Security Matrix

**Document Status:** RATIFIED  
**Phase:** 11  
**Target Architecture:** `src/mission_control/` Control-Plane Layer

---

## Threat Matrix & Mitigations (T11-1 through T11-18)

| Threat ID | Threat Vector Description | Subsystem Impacted | Mitigation Mechanism | Verification Result |
|---|---|---|---|---|
| **T11-1** | **Self-Authorization:** Mission attempts to issue authorization tokens directly | `coordinator.py` | Hard separation: `MissionCoordinator` calls `HumanAuthorizationBoundary`, never creates tokens. | PASS |
| **T11-2** | **Authorization Expiry:** Token expires while work continues | `scheduler.py`, `resume.py` | `scheduler` & `resume` revalidate authorization `expires_at` prior to scheduling or executing. | PASS |
| **T11-3** | **Scope Expansion:** Task requests resource outside allowed boundaries | `autonomy_policy.py` | `autonomy_policy` rejects tasks requesting resources outside `MissionConstraints.allowed_resources`. | PASS |
| **T11-4** | **Capability Expansion:** Workflow requests capability outside mission scope | `coordinator.py` | Tasks requesting capabilities outside initial constraints trigger immediate `SecurityBoundaryViolation`. | PASS |
| **T11-5** | **Retry Amplification:** Repeated failure causes unlimited retries | `retry_policy.py` | `retry_policy` enforces strict `max_attempts` caps and classifies security errors as non-retryable. | PASS |
| **T11-6** | **Resume After Cancellation:** Cancelled mission is resumed | `mission_state.py` | `mission_state` transition matrix permanently locks `CANCELLED` missions against restart. | PASS |
| **T11-7** | **Resume After Revocation:** Authorization revoked while paused | `resume.py` | `resume.py` re-checks `HumanAuthorizationBoundary.is_revoked()` before any action execution. | PASS |
| **T11-8** | **Checkpoint Tampering:** Checkpoint modified on disk | `checkpoint.py` | `checkpoint.py` verifies SHA-256 HMAC digest on load; raises `CheckpointTamperedError` on mismatch. | PASS |
| **T11-9** | **Dependency Cycle:** Malformed task graph contains cycle | `mission_graph.py` | `mission_graph` runs Kahn's cycle detection on build; rejects cyclic DAGs. | PASS |
| **T11-10** | **Budget Exhaustion:** Mission exceeds token or execution limits | `budget.py` | `budget.py` traps runtime limits (`max_runtime`, `max_executions`, token caps) and halts work cleanly. | PASS |
| **T11-11** | **Learning Escalation:** Learned strategy requests privileged capability | `autonomy_policy.py` | Phase 9 strategy overrides are bounded by `MUTABLE_FIELD_ALLOWLIST` and cannot add capabilities. | PASS |
| **T11-12** | **Trend Injection:** External observation attempts to inject execution command | `autonomy_policy.py` | `UNTRUSTED_EXTERNAL_OBSERVATION` tags isolate trend data from privilege elevation. | PASS |
| **T11-13** | **Research Escalation:** FROST artifact presented as authorization | `autonomy_policy.py` | Phase 4 FROST artifacts rejected as execution tokens via explicit assertion check. | PASS |
| **T11-14** | **Concurrent Resume:** Two workers resume same mission | `coordinator.py` | Atomic state lock on mission transitions prevents duplicate workers from executing same state. | PASS |
| **T11-15** | **Duplicate Execution:** Same action submitted concurrently | `executor.py` | Phase 10 `IdempotencyGuard` checks action nonces to block redundant adapter side effects. | PASS |
| **T11-16** | **Partial Failure:** Multi-action mission fails after some actions complete | `coordinator.py` | `MissionCoordinator` catches action failure, updates `ExecutionLedger`, and halts remaining graph cleanly. | PASS |
| **T11-17** | **Security Policy Mutation:** Mission attempts to alter Phase 1–10 policies | Substrate Core | Security substrate policies (`ExecutionGate`, `DecisionEngine`) remain immutable to Phase 11. | PASS |
| **T11-18** | **Runaway Autonomous Loop:** Workflow recursively generates work | `mission_graph.py` | Graph depth limit ($\le 10$) and total task limit ($\le 50$) enforce structural execution bounds. | PASS |
