# Phase 8 Architecture Specification: Security State Reconciliation & Consistency Boundary

**Document Status:** RATIFIED ARCHITECTURE SPECIFICATION  
**Phase:** 8 (Security State Reconciliation & Consistency Boundary)  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`  
**Prerequisite Baselines:** Phase 1 (Epistemic State & Execution Gate), Phase 2 (Verification Harness), Phase 3 (Recovery Parser), Phase 4 (FROST Prototype), Phase 5 (Evidence Orchestrator), Phase 6 (Decision Engine), Phase 7 (Audit Boundary).

---

## 1. Executive Summary & Epistemic Boundary

Phase 8 introduces the `SecurityReconciler` boundary operating above the Phase 7 `SecurityAuditBoundary`.

Its purpose is to construct deterministic, read-oriented consistency views across pre-fetched security records produced across Phases 1–7.

### Fundamental Non-Negotiable Invariants

$$
\mathbf{Evidence \neq Truth \neq Decision \neq Authorization \neq Execution\ Authority}
$$

$$
\mathbf{Reconciliation\ Result \neq Authorization} \quad \text{and} \quad \mathbf{Conflict \neq Permission\ to\ Override}
$$

1. `SecurityReconciler` is strictly non-authoritative.
2. It possesses ZERO methods named `authorize()`, `verify_for_execution()`, `unlock()`, `grant()`, or `execute()`.
3. It cannot transition `EpistemicState` nor unlock `ExecutionGate`.
4. `CONSISTENT` status means only that pre-fetched security records are mutually coherent and intact; it does NOT imply `VERIFIED` or `AUTHORIZED`.
5. Historical audit records remain append-only; Phase 8 reconciliation cannot delete, modify, or repair audit chain entries.

---

## 2. Core Component Design

### 2.1 `reconciliation_models.py`

Defines immutable data models:
- `ReconciliationStatus`: `CONSISTENT`, `INCONSISTENT`, `CONFLICT`, `INCOMPLETE`, `QUARANTINED`.
- `ReconciliationReasonCode`: Diagnostic finding identifiers (`ALL_RECORDS_CONSISTENT`, `EVIDENCE_MISSING`, `DECISION_MISSING`, `ATTESTATION_MISSING`, `AUDIT_INTEGRITY_FAILURE`, `CLASSIFICATION_CONFLICT`, `PROVENANCE_MISMATCH`, `EXPIRED_RECORD`, `QUARANTINED_RECORD`, `REFERENCE_MISMATCH`, `RESEARCH_BOUND_ONLY`, `SCHEMA_VALIDATION_ERROR`).
- `ReconciliationSource`: Subsystem identifier (`ASSURANCE_LOOP`, `VERIFICATION_HARNESS`, `RECOVERY_MANAGER`, `FROST_PROTOTYPE`, `EVIDENCE_ORCHESTRATOR`, `DECISION_ENGINE`, `AUDIT_BOUNDARY`).
- `ReconciliationFinding`: Dataclass containing finding details, affected record IDs, and metadata.
- `ReconciliationSnapshot`: Immutable collection of pre-fetched records across Phases 1–7.
- `ReconciliationResult`: Immutable result carrying snapshot digest, result commitment, `is_authoritative = False`, and `trust_marker = "NON_AUTHORITATIVE_RECONCILIATION_VIEW"`.

### 2.2 `reconciliation_policy.py`

Evaluates a `ReconciliationSnapshot` against deterministic rules:
1. **Identity & Provenance Binding:** Rejects `system_id` or `correlation_id` mismatches across records (`PROVENANCE_MISMATCH`, `REFERENCE_MISMATCH`).
2. **Quarantine Inspection:** Surfaces quarantined evidence explicitly (`QUARANTINED_RECORD`).
3. **Classification Conflict Inspection:** Detects conflicting decision classifications or state mismatches between evidence and decisions (`CLASSIFICATION_CONFLICT`).
4. **Audit Chain Integrity:** Surfacing hash chain breaks or discontinuity flags (`AUDIT_INTEGRITY_FAILURE`).
5. **Missing Records:** Identifies missing evidence, decision, or attestation sets (`INCOMPLETE`).
6. **Research Artifact Boundaries:** Preserves Phase 4 research evidence tags (`RESEARCH_BOUND_ONLY`) with `TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION` trust markers.
7. **Stale/Expired Records:** Evaluates timestamp freshness against maximum window ($900\text{s}$).

### 2.3 `reconciliation_integrity.py`

Provides canonical JSON serialization (`sort_keys=True`, compact separators) and computes SHA-256 digests for snapshots and results. Commitment verification is performed using `hmac.compare_digest`.

### 2.4 `security_reconciler.py`

Thread-safe reconciler (`threading.RLock()`) exposing:
- `reconcile(snapshot: ReconciliationSnapshot) -> ReconciliationResult`
- `get_result(result_id: str) -> Optional[ReconciliationResult]`
- `query_results(system_id, correlation_id, status) -> List[ReconciliationResult]`

---

## 3. Data Flow Diagram

```text
Phase 2 Verification Evidence ─┐
Phase 1 Assurance Records ─────┤
Phase 3 Recovery Results ───────┤
Phase 4 Research Evidence ──────┤
Phase 5 Normalized Evidence ────┤
Phase 6 Decisions/Attestations ─┤
Phase 7 Audit Records ──────────┘
                │
                ▼
      ┌─────────────────────────┐
      │ SecurityReconciler      │
      │ - snapshot construction │
      │ - consistency policy    │
      │ - conflict detection    │
      │ - SHA-256 digest        │
      └────────────┬────────────┘
                   │
                   ▼
         ReconciliationResult
        (is_authoritative=False)
                   │
       READ-ONLY DIAGNOSTIC REPORT
```

---

---

## 5. Real Workflow Integration Architecture (`src/workflow_integration`)

To validate that real visual application pipelines operate strictly under non-authoritative security boundaries, Phase 8 introduces the `src/workflow_integration/` package bridging `app/adapters/vision_adapter.py` and `app/services/orra_loop.py` with the Phase 1–8 security substrate.

### 5.1 Package Architecture & Component Map

```text
Visual Application Pipeline (app/adapters/vision_adapter.py)
                  │ (Visual DNA / Garment Claims)
                  ▼
   src/workflow_integration/
   ├── workflow_models.py (WorkflowRunContext, WorkflowRunResult, WorkflowStatus)
   ├── security_integration_adapter.py (Pipes claims: Phase 2 -> 5 -> 6 -> 7 -> 8)
   └── visual_workflow_runner.py (Orchestrates OBSERVE -> RECONCILE stages)
                  │
                  ▼
Security Substrate (Phases 1–8) ───► ExecutionGate.is_permitted() MUST be False
```

### 5.2 End-to-End Workflow Stages

1. **OBSERVE Stage:** `VisionAdapter` analyzes garment/textile assets, producing physical constraints, creative direction, and raw knowledge claims.
2. **VERIFY Stage:** `OptionHVerificationHarness` evaluates salted hash commitments in transient RAM, wiping buffers post-computation.
3. **ORCHESTRATE Stage:** `EvidenceOrchestrator` ingests normalized evidence records with multi-layer replay defense.
4. **DECIDE Stage:** `SecurityDecisionEngine` evaluates policy and issues cryptographically bound `AttestationRecord` artifacts (`classification != AUTHORIZED`).
5. **AUDIT Stage:** `SecurityAuditBoundary` records attestations in the append-only hash-chained ledger.
6. **RECONCILE Stage:** `SecurityReconciler` computes non-authoritative snapshot digests and consistency findings.

### 5.3 Invariant Enforcement

Throughout all stages, `ExecutionGate.is_permitted()` remains `False`. The workflow runner contains zero authorization authority.

