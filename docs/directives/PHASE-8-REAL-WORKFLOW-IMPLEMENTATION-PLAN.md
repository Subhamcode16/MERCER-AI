# Implementation Plan: Phase 8 — Real Visual Intelligence Workflow Integration & Validation Boundary

**Document Status:** PROPOSED — AWAITING USER APPROVAL  
**Phase:** 8  
**Purpose:** First controlled end-to-end testing of the actual Visual Intelligence workflow against the completed Phases 1–7 security substrate  
**Prerequisites:** Phases 1–7 COMPLETE & RATIFIED — 159/159 Pytests PASSED  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`

---

# 1. Why Phase 8 Exists

Phases 1–7 established the security substrate as isolated, testable boundaries:

```text
Phase 1 → State / Assurance / Execution Gate
Phase 2 → Ephemeral Verification
Phase 3 → Recovery Boundary
Phase 4 → FROST Research Prototype
Phase 5 → Evidence Orchestration
Phase 6 → Decision & Attestation
Phase 7 → Audit & Integrity
```

Those phases have demonstrated component-level and cross-phase correctness.

**Phase 8 is the transition from security-substrate validation to actual application-workflow validation.**

The objective is to answer:

> **Can the real Visual Intelligence workflow operate through the security substrate end-to-end while all previously established security and governance boundaries remain intact?**

This phase must therefore test a **realistic Visual Intelligence workflow**, using representative visual assets and actual application workflow components where they already exist.

It must not merely create another abstract security wrapper.

---

# 2. Core Architectural Principle

The governing invariant remains:

$$
\mathbf{Evidence \neq Truth \neq Decision \neq Authorization \neq Execution\ Authority}
$$

Phase 8 adds:

$$
\mathbf{Workflow\ Result \neq Security\ Authorization}
$$

and:

$$
\mathbf{End\!-\!to\!-\!End\ Success \neq Automatic\ Permission\ to\ Execute}
$$

The workflow may produce analytical results.

The security substrate may evaluate evidence.

The decision layer may produce a security decision.

The audit layer may record the event.

**None of those facts independently grant execution authority.**

---

# 3. Scope

Phase 8 covers controlled end-to-end validation of the actual Visual Intelligence application pipeline.

The engineer must first inspect the repository and identify the real workflow already implemented outside the security substrate.

Do **not** invent a hypothetical workflow if an existing application workflow is present.

The implementation must map the real pipeline into the following conceptual stages:

```text
REAL VISUAL INPUT
       ↓
APPLICATION INGESTION
       ↓
ASSET IDENTIFICATION / NORMALIZATION
       ↓
VISUAL ANALYSIS / EXTRACTION
       ↓
APPLICATION-GENERATED EVIDENCE
       ↓
PHASE 2 VERIFICATION
       ↓
PHASE 5 EVIDENCE ORCHESTRATION
       ↓
PHASE 6 SECURITY DECISION / ATTESTATION
       ↓
PHASE 7 AUDIT / INTEGRITY
       ↓
END-TO-END WORKFLOW RESULT
```

If the current application does not yet contain one or more stages, the engineer must document the gap rather than fabricate production functionality.

---

# 4. Non-Negotiable Boundary

Phase 8 is an **integration and validation phase**, not a production authorization phase.

It MUST NOT:

- unlock `ExecutionGate`;
- automatically transition `EpistemicState` to `VERIFIED`;
- introduce production FROST;
- introduce real YubiKey/PIV/TPM/HSM integration;
- introduce production key provisioning;
- convert Phase 4 research results into authorization;
- bypass Phase 2 verification;
- bypass Phase 5 evidence orchestration;
- bypass Phase 6 decision policy;
- bypass Phase 7 audit integrity;
- silently suppress failed or conflicting evidence;
- treat successful workflow completion as authorization;
- introduce autonomous remediation;
- introduce distributed consensus, ZKP, TEE, or BFT infrastructure.

---

# 5. Required Repository Reconnaissance

Before writing implementation code, the engineer MUST inspect the repository to determine:

1. The actual Visual Intelligence application entry points.
2. Existing asset ingestion modules.
3. Existing visual-analysis/extraction modules.
4. Existing data models.
5. Existing API routes or service boundaries.
6. Existing workflow orchestration.
7. Existing test fixtures and representative assets.
8. Existing configuration/environment requirements.
9. Existing integration-test infrastructure.
10. How the Phase 1–7 security substrate can be called without violating its boundaries.

The engineer must produce a short architecture mapping showing:

```text
Existing Application Component
        ↓
Phase 8 Integration Adapter
        ↓
Security Substrate Boundary
```

If a required component does not exist, report it as an architectural gap.

---

# 6. Proposed Phase 8 Components

The exact implementation should be determined after repository reconnaissance.

Where appropriate, introduce a narrowly scoped integration layer under:

```text
Visual-Intelligence/product/backend/src/
```

Possible modules include:

## [NEW] `workflow_integration/`

Only create this package if the repository architecture warrants it.

Potential modules:

### `visual_workflow_runner.py`

Responsible for controlled execution of the real application workflow in a test/integration context.

It must:

- accept a representative visual input;
- invoke existing application components;
- collect application outputs;
- pass security-relevant outputs into the Phase 2–7 substrate;
- return a structured end-to-end workflow result;
- avoid direct execution-authority manipulation.

### `security_integration_adapter.py`

Responsible for translating real application outputs into the already-defined Phase 2–7 contracts.

It must not duplicate security policy already implemented in Phases 1–7.

### `workflow_models.py`

Define only the minimum integration-level models required to represent:

- workflow run identity;
- input asset reference;
- application output reference;
- evidence references;
- decision/attestation references;
- audit reference;
- workflow outcome;
- failure stage.

No raw asset bytes should be persisted in security records.

---

# 7. Real Asset Testing

Phase 8 must use **representative real visual assets** appropriate to the existing Visual Intelligence workflow.

The engineer must distinguish:

### A. Integration fixtures

Safe local test assets used to exercise the actual workflow.

### B. Sensitive production assets

Assets that must not be copied into tests, logs, audit records, or source control.

### C. Synthetic adversarial assets

Controlled fixtures intentionally modified to test failure behavior.

The test suite must never commit confidential or production visual assets.

If no appropriate real-world fixture is available in the repository, the engineer must state that limitation and use clearly labeled representative fixtures rather than claiming production validation.

---

# 8. End-to-End Test Scenarios

At minimum, Phase 8 must test the following workflows.

## T01 — Successful End-to-End Workflow

```text
Asset
 → ingestion
 → visual analysis
 → evidence
 → verification
 → orchestration
 → decision
 → attestation
 → audit
 → result
```

Expected:

- workflow completes;
- evidence is traceable;
- decision is traceable;
- attestation is verifiable;
- audit record is present;
- no security boundary is bypassed.

---

## T02 — Invalid / Corrupted Asset

Modify or corrupt the input.

Expected:

- verification failure;
- no false positive security decision;
- audit trail records the failure where applicable;
- execution remains locked.

---

## T03 — Stale Evidence

Provide stale security evidence.

Expected:

- stale condition is surfaced;
- no silent acceptance;
- workflow result reflects the security limitation;
- execution authority is unchanged.

---

## T04 — Evidence Mutation

Alter evidence after generation.

Expected:

- commitment/signature/integrity verification detects mutation;
- decision cannot treat mutated evidence as valid;
- audit result remains integrity-consistent.

---

## T05 — Research Evidence Injection

Inject a Phase 4 `FROSTSignature`.

Expected:

```text
RESEARCH_CRYPTOGRAPHIC_EVIDENCE
+
TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION
```

must remain intact.

The workflow must never convert it into authorization.

---

## T06 — Recovery During Workflow

Trigger the Phase 3 recovery path.

Expected:

```text
RECOVERY
   ↓
UNKNOWN
   ↓
fresh verification required
```

Execution remains locked until independently authorized through the already-existing production security path.

---

## T07 — Conflicting Evidence

Supply internally inconsistent evidence.

Expected:

- conflict is explicitly surfaced;
- no optimistic resolution;
- no authorization implication;
- auditability preserved.

---

## T08 — Replay

Replay a previously consumed workflow/evidence event.

Expected:

- replay defense activates;
- duplicate event rejected or quarantined according to the existing policy;
- no state escalation.

---

## T09 — Concurrent Workflow Runs

Run multiple workflows concurrently.

Expected:

- no cross-run identity contamination;
- no nonce/evidence replay;
- deterministic security records;
- no race-induced authorization;
- audit sequencing remains valid.

---

## T10 — Mid-Workflow Failure

Force a failure after one or more security stages.

Expected:

- failure is explicit;
- partial results are not misrepresented as successful completion;
- no sensitive material leaks;
- audit/integrity behavior remains valid.

---

# 9. Cross-Phase Traceability

Every Phase 8 integration test should be capable of tracing:

```text
workflow_run_id
      ↓
asset_reference
      ↓
evidence_id(s)
      ↓
decision_id
      ↓
attestation_id
      ↓
audit_record_id
```

The trace must be reference-based.

Do not duplicate raw visual assets or secret material into security records.

---

# 10. Security Invariants

Phase 8 must prove:

### I-8.1 — Workflow Does Not Become Authority

```text
Workflow Success ≠ Authorization
```

### I-8.2 — Evidence Boundary

```text
Application Output ≠ Automatically Trusted Evidence
```

### I-8.3 — Research Isolation

```text
Phase 4 Research Result ≠ Production Authorization
```

### I-8.4 — Recovery Isolation

```text
Recovery ≠ Verification
```

### I-8.5 — Audit Integrity

```text
Workflow Audit Record ≠ Execution Permission
```

### I-8.6 — Failure Visibility

```text
Failure / Conflict / Stale / Quarantine
    ≠
Successful Security State
```

### I-8.7 — ExecutionGate Isolation

Phase 8 itself cannot unlock the gate.

### I-8.8 — Epistemic State Isolation

Phase 8 itself cannot mutate epistemic state.

---

# 11. Observability Requirements

The integration layer should expose sufficient metadata to diagnose a workflow without exposing secrets.

Permitted examples:

- workflow run ID;
- stage name;
- timestamps;
- status;
- evidence IDs;
- decision IDs;
- attestation IDs;
- audit IDs;
- reason codes;
- failure category.

Forbidden:

- raw visual bytes in logs;
- private keys;
- HMAC keys;
- secret nonces;
- salts;
- raw sensitive payloads;
- credentials.

---

# 12. Test Architecture

Create an integration test package appropriate to the repository, for example:

```text
tests/integration/
```

or an existing repository integration-test location if one already exists.

Potential test modules:

- `test_real_workflow_success.py`
- `test_real_workflow_failures.py`
- `test_real_workflow_security_boundaries.py`
- `test_real_workflow_replay.py`
- `test_real_workflow_concurrency.py`
- `test_real_workflow_traceability.py`
- `test_phase8_regression.py`

Do not create duplicate unit tests for functionality already adequately covered by Phases 1–7.

Phase 8 tests should primarily prove **composition and real workflow behavior**.

---

# 13. Regression Requirement

The complete existing suite must remain green:

```bash
python -m pytest tests/security_substrate tests/frost_prototype -v
```

Baseline:

```text
Phase 1–7:
159 PASSED
0 FAILED
0 SKIPPED
```

Then run the Phase 8 integration suite.

Final report must clearly distinguish:

```text
Phase 1–7 regression: 159 PASSED
Phase 8 integration:  [N] PASSED
Total:                159 + N PASSED
Failures:             0
Skipped:              0
```

If a repository/environment limitation prevents a full real-workflow test, the engineer must report it explicitly rather than claiming success.

---

# 14. Security Review Requirements

The engineer must review:

1. Input handling.
2. Asset lifecycle.
3. Evidence creation.
4. Evidence verification.
5. Cross-phase data flow.
6. Research evidence isolation.
7. Recovery behavior.
8. Replay behavior.
9. Concurrent workflow behavior.
10. Failure behavior.
11. Logging/secret leakage.
12. ExecutionGate isolation.
13. Epistemic-state isolation.
14. Audit traceability.
15. Configuration/environment boundaries.

---

# 15. Documentation Deliverables

Create:

- `PHASE-8-ARCHITECTURE.md`
- `PHASE-8-SECURITY-REVIEW.md`
- `PHASE-8-THREAT-MODEL.md`
- `PHASE-8-TEST-REPORT.md`
- `PHASE-8-GOVERNANCE-GATE.md`

The architecture document must include an explicit diagram of the **real workflow** discovered during repository reconnaissance.

The test report must identify:

- exact test assets/fixtures used;
- exact workflow entry point;
- exact components exercised;
- exact security-substrate boundaries crossed;
- exact failures tested;
- exact test counts;
- complete pytest output.

---

# 16. Threat Model

## T1 — Untrusted Application Output

Application-generated output is incorrectly treated as security evidence.

**Mitigation:** Explicit integration boundary and Phase 2–5 validation.

## T2 — Asset Substitution

One asset is associated with another workflow's evidence.

**Mitigation:** Asset/workflow identity binding and commitment verification.

## T3 — Evidence Mutation

Evidence is changed after generation.

**Mitigation:** Phase 2/5/6 integrity mechanisms.

## T4 — Research Escalation

FROST research output enters the production workflow as authorization.

**Mitigation:** Permanent research classification and isolation tests.

## T5 — Recovery Escalation

Recovery is interpreted as verification.

**Mitigation:** Recovery remains `UNKNOWN`; fresh verification required.

## T6 — Replay

Old workflow/evidence artifacts are submitted again.

**Mitigation:** Existing nonce/evidence replay defenses.

## T7 — Concurrency Contamination

Parallel workflows share identifiers or security state.

**Mitigation:** Per-run identity, atomic caches, concurrency tests.

## T8 — Secret Leakage

Workflow instrumentation exposes sensitive material.

**Mitigation:** Logging/exception audit.

## T9 — Partial-Failure Confusion

A partially completed workflow is represented as successful.

**Mitigation:** Explicit stage/failure state.

## T10 — Workflow-to-Authority Escalation

A successful end-to-end workflow is interpreted as permission to execute.

**Mitigation:** No authority methods and runtime `ExecutionGate` isolation test.

---

# 17. Governance Gate

Phase 8 cannot be ratified merely because tests pass.

The governance review must establish:

- the actual workflow was exercised;
- the workflow-to-security-substrate mapping is documented;
- Phase 1–7 semantics remain unchanged;
- no new authority path exists;
- research boundaries remain intact;
- failures are represented honestly;
- limitations are explicitly documented.

Minimum acceptable verdict:

```text
PASS WITH LIMITATIONS
```

A stronger verdict requires explicit evidence and governance justification.

---

# 18. Explicit Deferred Capabilities

Phase 8 does NOT authorize:

- production execution;
- autonomous actions;
- production FROST;
- hardware-backed authorization;
- real YubiKey/PIV/TPM/HSM;
- production key provisioning;
- distributed consensus;
- ZKP/TEE deployment;
- autonomous remediation;
- automatic escalation from workflow success to `VERIFIED`;
- automatic escalation from consistency to authorization.

---

# 19. Acceptance Criteria

Phase 8 is complete only when:

- [ ] The real Visual Intelligence workflow has been identified.
- [ ] The real workflow entry point is documented.
- [ ] Representative visual assets are used.
- [ ] The actual application components are exercised.
- [ ] Application output is correctly separated from security evidence.
- [ ] Phase 2 verification is exercised in the workflow.
- [ ] Phase 5 evidence orchestration is exercised.
- [ ] Phase 6 decision/attestation is exercised.
- [ ] Phase 7 audit/integrity is exercised.
- [ ] End-to-end traceability is demonstrated.
- [ ] Corrupted input behavior is tested.
- [ ] Stale evidence behavior is tested.
- [ ] Evidence mutation is tested.
- [ ] Research evidence isolation is tested.
- [ ] Recovery behavior is tested.
- [ ] Replay behavior is tested.
- [ ] Conflict behavior is tested.
- [ ] Concurrent workflows are tested.
- [ ] Mid-workflow failure is tested.
- [ ] No sensitive data leaks.
- [ ] `ExecutionGate` remains protected.
- [ ] `EpistemicState` remains protected.
- [ ] Phase 4 remains research-only.
- [ ] All 159 Phase 1–7 tests pass.
- [ ] All Phase 8 tests pass.
- [ ] Security review is complete.
- [ ] Threat model is complete.
- [ ] Test report is complete.
- [ ] Governance gate is complete.

---

# 20. Engineer Instruction

## STOP — DO NOT IMPLEMENT YET

This document is an **architectural implementation proposal**.

The engineer must first receive explicit project-owner approval.

Before coding, perform repository reconnaissance and report:

1. Actual Visual Intelligence workflow.
2. Actual workflow entry point.
3. Existing components that can be integrated.
4. Existing test fixtures/assets.
5. Any architectural gaps.
6. Proposed exact Phase 8 integration files.
7. Confirmation that the implementation can preserve all Phase 1–7 boundaries.

**Do not begin implementation until the project owner gives the green signal.**

Required approval phrase:

> `GREEN SIGNAL — PROCEED WITH PHASE 8 REAL WORKFLOW INTEGRATION`

After approval:

- implement only the approved scope;
- preserve all Phase 1–7 invariants;
- do not weaken existing tests;
- do not invent missing production functionality;
- do not claim real-workflow validation if the repository does not contain the required workflow;
- report every limitation;
- provide exact changed files;
- provide exact test counts;
- provide complete pytest output;
- provide security findings;
- provide governance verdict.

If an architectural conflict appears, **STOP and report it instead of improvising a new authority path.**

---

# Final Position

Phases 1–7 established the security machinery.

**Phase 8 is where we finally put that machinery around the actual Visual Intelligence workflow and test the composition under realistic conditions.**

The goal is not:

> "Can our security classes pass tests?"

The goal is:

> **"Can the actual Visual Intelligence system run its real workflow while the security substrate correctly observes, validates, records, and constrains that workflow without becoming an unauthorized source of execution authority?"**

That is the purpose of this phase.
