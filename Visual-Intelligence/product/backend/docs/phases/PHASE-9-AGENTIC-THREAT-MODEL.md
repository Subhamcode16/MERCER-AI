# Phase 9 Agentic Threat Model & Risk Matrix

**Document Status:** RATIFIED THREAT MODEL  
**Phase:** 9 (Persistent Learning, Knowledge & Workflow Optimization Boundary)  
**Threat Vector Range:** T9-1 through T9-12

---

## Threat Matrix & Mitigation Verification

| Threat ID | Threat Description | Attack Vector | Mitigation Architecture | Verification Test | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T9-1** | Learning Poisoning | Adversary inputs single biased feedback item to warp strategy | Threshold-based aggregation requires $N \ge 3$ consistent feedback signals before pattern formation | `test_t9_1_learning_poisoning_mitigation` | **PASSED** |
| **T9-2** | Trend Poisoning | Malicious external visual trend claims to be trusted truth | Store forcibly sets status to `UNTRUSTED_EXTERNAL_OBSERVATION` | `test_t9_2_trend_poisoning_mitigation` | **PASSED** |
| **T9-3** | Self-Escalation | Candidate strategy attempts to set `execution_gate_permitted = True` | `validate_allowlist()` raises `SecurityBoundaryViolation` on forbidden fields | `test_t9_3_self_escalation_rejection` | **PASSED** |
| **T9-4** | Regression Amplification | Strategy optimization degrades visual or critique quality | 5-Category Benchmark Suite evaluates candidate performance; rejects degradation | `test_phase9_benchmark_suite.py` | **PASSED** |
| **T9-5** | Memory Contamination | Storage of raw API keys or secrets in memory records | `WorkflowMemoryStore` inspects keys and raises `SecretStorageForbiddenError` | `test_t9_5_memory_contamination_secret_rejection` | **PASSED** |
| **T9-6** | Artifact Lineage Forgery | Forged lineage records or altered provenance | SHA-256 payload and lineage hash verification; raises `LineageTamperError` | `test_t9_6_artifact_lineage_forgery_detection` | **PASSED** |
| **T9-7** | Feedback Replay | Re-submitting identical feedback ID to bypass N=3 threshold | `PersistentFeedbackEngine` tracks recorded IDs; raises `DuplicateFeedbackError` | `test_t9_7_feedback_replay_defense` | **PASSED** |
| **T9-8** | Knowledge Staleness | Obsolete trend observations bias current design direction | Temporal confidence weighting and classification filtering | `test_phase9_persistent_knowledge.py` | **PASSED** |
| **T9-9** | Benchmark Gaming | Optimizer proposes degraded strategy that fails benchmark | `PersistentImprovementEngine` scores candidates against baseline; raises `DegradationRejectedError` | `test_t9_9_benchmark_degradation_rejection` | **PASSED** |
| **T9-10** | Autonomous Policy Mutation | Strategy adaptation targets security policy or gate lock | Hardcoded `FORBIDDEN_SECURITY_FIELDS` and runtime `ExecutionGate.is_permitted() == False` check | `test_t9_10_execution_gate_remains_locked` | **PASSED** |
| **T9-11** | Prompt Injection via Knowledge | External trend details contain executable system instructions | Sanitizer strips prompt tags (`<SYSTEM_MESSAGE>`), treating text as pure data | `test_t9_11_prompt_injection_in_knowledge` | **PASSED** |
| **T9-12** | Cross-Workflow Contamination | Context or memory leaks between distinct workflow IDs | Memory records and lineage are strictly scoped by `workflow_id` | `test_phase9_memory_store.py` | **PASSED** |
