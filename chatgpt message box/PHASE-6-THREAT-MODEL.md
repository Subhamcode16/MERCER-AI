# Phase 6 — Threat Model & Security Assurance Matrix

**Phase:** 6  
**Status:** RATIFIED — Threat Vectors T1–T12 Addressed & Verified

---

## Threat Matrix

| Threat ID | Threat Description | Severity | Control & Mitigation Strategy | Test Verification |
|---|---|---|---|---|
| **T1** | Evidence Insufficiency | HIGH | Policy checks required classifications; yields `INSUFFICIENT_EVIDENCE`. | `test_decision_policy_insufficient_evidence` |
| **T2** | Evidence Conflict | HIGH | Detects contradictory payload commitments for same correlation ID; yields `EVIDENCE_CONFLICT`. | `test_decision_policy_conflict_evidence` |
| **T3** | Evidence Expiry | MEDIUM | Enforces max freshness window ($\le 900\text{s}$); yields `EVIDENCE_EXPIRED`. | `test_decision_policy_expired_evidence` |
| **T4** | Quarantined Promotion | HIGH | Hard rejection on `QUARANTINED`/`REJECTED` status; yields `EVIDENCE_QUARANTINED`. | `test_decision_policy_quarantined_evidence` |
| **T5** | Research-to-Production Escalation | CRITICAL | Permanent research classification; yields `RESEARCH_ONLY` with trust marker. | `test_decision_policy_research_evidence`, `test_runtime_isolation_research_evidence...` |
| **T6** | Decision-to-Execution Escalation | CRITICAL | Engine possesses zero execution methods; `ExecutionGate` remains locked. | `test_decision_engine_has_no_execution_gate_methods`, `test_runtime_isolation...` |
| **T7** | Attestation Mutation | HIGH | SHA-256 canonical commitments verified via constant-time `hmac.compare_digest`. | `test_attestation_verification_failure_on_commitment_tamper` |
| **T8** | Attestation Replay | HIGH | Atomic `DecisionReplayCache` under `threading.RLock()`. | `test_decision_replay_concurrent_duplicate_race` |
| **T9** | Policy Downgrade | MEDIUM | Policy version checked during evaluation and bound in commitment. | `test_decision_policy_version_mismatch` |
| **T10** | Timestamp Manipulation | MEDIUM | Rejects future timestamps ($> \text{now} + 5.0\text{s}$) and negative values. | `test_decision_context_future_timestamp` |
| **T11** | Secret Leakage | HIGH | Data models store only commitments, references, and nonces. Zero raw asset bytes or keys. | `test_decision_models.py`, logging audit |
| **T12** | Dependency Contamination | HIGH | AST static audit enforces zero imports of `frost_prototype` or gate methods in Phase 6. | `test_ast_audit_no_frost_research_imports_in_substrate` |
