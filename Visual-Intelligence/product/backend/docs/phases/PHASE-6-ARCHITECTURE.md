# Phase 6 — Security Decision & Attestation Boundary Architecture

**Phase:** 6  
**Status:** IMPLEMENTED & RATIFIED — 136/136 Pytests PASSED  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`

---

## 1. Overview & Core Epistemic Invariant

Phase 6 implements the **Security Decision & Attestation Boundary** above the Phase 5 `EvidenceOrchestrator`.

The fundamental architectural invariant enforced by Phase 6 is:

$$\text{Observation} \longrightarrow \text{Evidence} \longrightarrow \text{Evidence Validation} \longrightarrow \text{Orchestration} \longrightarrow \text{Security Evaluation} \longrightarrow \text{Decision / Attestation} \stackrel{\mathbf{X}}{\centernot\longrightarrow} \text{Execution Authority}$$

$$\mathbf{Evidence \neq Truth \neq Authorization \neq Execution\ Authority}$$

Phase 6 provides a deterministic, thread-safe mechanism to evaluate normalized evidence records and produce cryptographically committed attestation records. It carries **zero** execution or state-mutation authority.

---

## 2. Core Components

1. **`decision_models.py`**:
   - Defines `DecisionClassification` (`INSUFFICIENT_EVIDENCE`, `EVIDENCE_CONFLICT`, `EVIDENCE_EXPIRED`, `EVIDENCE_QUARANTINED`, `RESEARCH_ONLY`, `EVALUATION_PASS`, `EVALUATION_FAIL`). Prohibits `AUTHORIZED` to prevent authority confusion.
   - Defines `SecurityDecision`, `AttestationRecord`, `DecisionContext`, and `DecisionEvidenceReference` with strict runtime schema validation.

2. **`decision_policy.py`**:
   - `DecisionPolicy`: Evaluates normalized evidence records against required classifications, freshness limits ($\le 900\text{s}$), conflict detection, quarantine checks, policy version matching, and research-only boundaries.

3. **`attestation.py`**:
   - Canonicalizes decision objects into deterministic JSON representations and computes SHA-256 decision commitments.
   - Verifies attestation records against decisions using constant-time comparison (`hmac.compare_digest`).

4. **`decision_replay.py`**:
   - `DecisionReplayCache`: Provides thread-safe (`threading.RLock()`) atomic replay prevention for decision IDs and attestation nonces.

5. **`decision_engine.py`**:
   - `SecurityDecisionEngine`: Evaluates evidence sets through `DecisionPolicy`, emits committed `AttestationRecord` artifacts, and registers nonces in `DecisionReplayCache`. Possesses **zero** execution or gating methods.

---

## 3. Strict Boundary Isolation

- **No ExecutionGate Coupling:** Neither `SecurityDecisionEngine` nor `DecisionPolicy` imports or invokes `ExecutionGate`.
- **No Epistemic State Mutation:** Evaluating evidence does not mutate `EpistemicState` or trigger `EpistemicStateStore` transitions.
- **Phase 4 Research Isolation:** Phase 4 FROST research payloads remain classified as `RESEARCH_ONLY` with trust marker `"TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION"`.
