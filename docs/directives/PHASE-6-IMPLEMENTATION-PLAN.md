# Implementation Plan: Phase 6 — Security Decision & Attestation Boundary

**Document Status:** PROPOSED — AWAITING USER APPROVAL  
**Phase:** 6  
**Scope:** Security Evidence Decisioning, Attestation Readiness, and Explicit Authorization Boundary  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`  
**Prerequisites:** Phases 1–5 COMPLETE & VERIFIED — 103/103 Pytests PASSED

> [!IMPORTANT]
> **Phase 6 must NOT turn evidence into execution authority.**
>
> The implementation must preserve:
>
> `Evidence ≠ Truth ≠ Authorization ≠ Execution Authority`
>
> Phase 6 may evaluate and aggregate already-normalized evidence into a deterministic security decision/attestation result, but it must not directly unlock `ExecutionGate`, bypass `AssuranceLoopController`, mutate `EpistemicState`, or promote Phase 4 research cryptography into production authorization.

---

## 1. Objective

Phase 6 establishes a **Security Decision & Attestation Boundary** above the Phase 5 `EvidenceOrchestrator`.

Its purpose is to provide a controlled, deterministic mechanism for:

1. evaluating normalized evidence;
2. checking whether required evidence classes and provenance are present;
3. detecting conflicting, expired, quarantined, rejected, or replayed evidence;
4. producing a signed/committed **decision artifact** describing the evaluated security posture;
5. explicitly distinguishing a decision/attestation result from execution authorization;
6. preserving complete isolation from the Phase 4 FROST research prototype;
7. preparing a future architectural seam for authorization without implementing production authorization in this phase.

Phase 6 is therefore an **evaluation and attestation boundary**, not an execution-control mechanism.

---

## 2. Non-Negotiable Architectural Invariants

### Invariant A — Evidence Is Not Truth

The system must never represent the presence of evidence as proof of semantic or metaphysical truth.

`Evidence → Evaluation → Decision` is permitted.

`Evidence → Truth` is prohibited.

### Invariant B — Decision Is Not Execution Authority

A Phase 6 decision artifact must not itself unlock execution.

`SecurityDecision != ExecutionAuthorization != ExecutionGate`

`ExecutionGate` remains controlled exclusively by the already-established production security substrate.

### Invariant C — Research Evidence Is Never Production Authorization

Any Phase 4-derived evidence remains permanently classified as:

`RESEARCH_CRYPTOGRAPHIC_EVIDENCE`

with:

`TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION`

Phase 6 must not provide a conversion path from that classification into production authorization.

### Invariant D — Recovery Is Not Verification

Phase 3 recovery evidence remains informational.

Recovery success must continue to result in:

`EpistemicState.UNKNOWN`

A fresh verification/assurance cycle is required before `VERIFIED`.

### Invariant E — Fail Closed

Any ambiguity, malformed evidence, provenance violation, conflicting evidence, invalid attestation, replay condition, or policy evaluation error must produce a non-authorizing outcome.

### Invariant F — No Implicit Trust

Phase 6 must not introduce a generic `trusted=True`, `authorized=True`, or equivalent boolean that can silently become execution authority.

Decisions must carry explicit classification and reason codes.

### Invariant G — Deterministic Evaluation

Given the same normalized evidence set, policy version, and evaluation context, the decision engine must produce the same decision classification and deterministic reason set.

---

## 3. Proposed Architecture

```text
Phase 1 Assurance Records ───────┐
Phase 2 Verification Evidence ──┤
Phase 3 Recovery Evidence ──────┤
Phase 4 Research Evidence ──────┤
                                 ▼
                     ┌──────────────────────┐
                     │ EvidenceOrchestrator │
                     │      Phase 5         │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ SecurityDecision     │
                     │ Engine / Policy      │
                     │       Phase 6        │
                     └──────────┬───────────┘
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
       Decision / Attestation          Non-authorizing outcome
          Artifact                         / Quarantine
                 │
                 ▼
       Future Authorization Seam
        (NOT IMPLEMENTED HERE)
                 │
                 X
          ExecutionGate
       remains independently
             controlled
```

Phase 6 must not introduce a direct call path from `SecurityDecisionEngine` to `ExecutionGate`.

---

## 4. Proposed File Manifest

### Security Substrate

#### [NEW] `decision_models.py`

Define:

- `DecisionClassification`
- `DecisionStatus`
- `DecisionReasonCode`
- `SecurityDecision`
- `DecisionContext`
- `DecisionEvidenceReference`
- `AttestationRecord`

Models must:

- use strict runtime type validation;
- reject boolean type confusion where inappropriate;
- reject empty/whitespace-only identifiers;
- reject negative timestamps/windows;
- reject impossible temporal relationships;
- contain references/commitments rather than raw asset bytes;
- contain no private keys, HMAC keys, secret nonces, or raw cryptographic secrets.

Suggested classifications:

- `INSUFFICIENT_EVIDENCE`
- `EVIDENCE_CONFLICT`
- `EVIDENCE_EXPIRED`
- `EVIDENCE_QUARANTINED`
- `RESEARCH_ONLY`
- `EVALUATION_PASS`
- `EVALUATION_FAIL`

**Do NOT create a classification named `AUTHORIZED` in Phase 6.**

---

#### [NEW] `decision_policy.py`

Define `DecisionPolicy`.

Responsibilities:

- validate required evidence classes;
- validate evidence provenance;
- reject expired/quarantined/rejected evidence;
- detect conflicting evidence;
- enforce freshness requirements;
- enforce policy-version compatibility;
- enforce research-only boundaries;
- produce deterministic reason codes;
- fail closed on malformed or ambiguous input.

The policy must not mutate `EpistemicState` or call `ExecutionGate`.

---

#### [NEW] `decision_engine.py`

Define `SecurityDecisionEngine`.

Responsibilities:

- accept only `NormalizedEvidenceRecord` / Phase 5 outputs;
- invoke `DecisionPolicy`;
- evaluate evidence deterministically;
- produce `SecurityDecision`;
- generate an `AttestationRecord` containing the decision commitment and relevant evidence references;
- maintain no execution authority;
- expose no `unlock()`, `authorize()`, `execute()`, or equivalent methods.

The engine should be thread-safe where shared state is required.

---

#### [NEW] `attestation.py`

Define an application-level attestation/commitment mechanism.

Responsibilities:

- canonicalize decision data;
- compute a cryptographic commitment over the canonical decision artifact;
- bind the commitment to policy version, evaluation timestamp, evidence references, and decision classification;
- prevent mutation without commitment mismatch;
- avoid claiming that the commitment proves truth.

Use existing cryptographic utilities where appropriate.

Do NOT introduce production key provisioning or real hardware-backed signing.

---

#### [NEW] `decision_replay.py`

Define a replay-defense mechanism for decision/attestation artifacts.

Responsibilities:

- track unique decision IDs;
- track evaluation nonces where applicable;
- atomically reject duplicate decision artifacts;
- support bounded in-memory retention;
- fail closed under concurrent replay.

Do not weaken or replace Phase 5 evidence replay controls.

---

#### [MODIFY] `__init__.py`

Export only approved Phase 6 public symbols.

No Phase 4 research symbols should be re-exported into the production security substrate.

---

## 5. Test Suite Manifest

### [NEW] `test_decision_models.py`

Cover:

- valid decision construction;
- mandatory-field validation;
- empty identifier rejection;
- boolean type confusion;
- invalid temporal relationships;
- forbidden `AUTHORIZED`-style classifications;
- secret/raw-data containment checks.

### [NEW] `test_decision_policy.py`

Cover:

- sufficient evidence evaluation;
- insufficient evidence;
- expired evidence;
- quarantined evidence;
- rejected evidence;
- conflicting evidence;
- provenance mismatch;
- research-only evidence;
- policy version mismatch;
- malformed input;
- fail-closed behavior.

### [NEW] `test_decision_engine.py`

Cover:

- deterministic evaluation;
- stable reason-code ordering;
- decision artifact generation;
- evidence-reference binding;
- concurrent evaluation;
- repeated evaluation consistency;
- mutation detection.

### [NEW] `test_attestation.py`

Cover:

- canonicalization;
- commitment generation;
- commitment verification;
- modified decision rejection;
- modified evidence-reference rejection;
- modified policy-version rejection;
- timestamp/nonce binding;
- no raw secret inclusion.

### [NEW] `test_decision_replay.py`

Cover:

- first-use acceptance;
- duplicate decision rejection;
- duplicate nonce rejection;
- concurrent replay race;
- bounded retention behavior;
- fail-closed handling.

### [NEW] `test_phase6_isolation.py`

AST/runtime audit proving:

- zero imports of `research.frost_prototype` into Phase 6 production code;
- zero imports of Phase 6 production code into `research.frost_prototype`;
- zero `ExecutionGate` calls from Phase 6;
- zero `EpistemicState` mutation from Phase 6;
- zero `RecoveryManager` mutation from Phase 6;
- no `authorize`, `unlock`, or `execute` methods on the Phase 6 decision engine;
- Phase 4 research evidence remains research-only.

### [NEW] `test_phase6_regression.py`

Ensure all Phase 1–5 tests continue to pass without modification.

---

## 6. Threat Model — T1 to T12

### T1 — Evidence Insufficiency

Incomplete evidence must never accidentally produce a positive decision.

**Control:** explicit `INSUFFICIENT_EVIDENCE`.

### T2 — Evidence Conflict

Contradictory evidence must not be resolved through implicit trust ordering.

**Control:** explicit `EVIDENCE_CONFLICT` result.

### T3 — Evidence Expiry

Expired evidence cannot satisfy current policy requirements.

**Control:** freshness validation and `EVIDENCE_EXPIRED`.

### T4 — Quarantined Evidence Promotion

Quarantined evidence must never satisfy a positive evaluation.

**Control:** hard policy rejection.

### T5 — Research-to-Production Escalation

Phase 4 FROST evidence must never become production authorization.

**Control:** permanent research classification and isolation tests.

### T6 — Decision-to-Execution Escalation

A positive evaluation must not unlock execution.

**Control:** AST audit, reflection audit, runtime gate test.

### T7 — Attestation Mutation

Changing any decision-bearing field after commitment must invalidate verification.

**Control:** canonical commitment verification.

### T8 — Attestation Replay

Previously consumed decision artifacts must not be accepted repeatedly where replay semantics apply.

**Control:** atomic replay cache.

### T9 — Policy Downgrade

An artifact evaluated under an incompatible or older policy must not silently satisfy a newer policy.

**Control:** policy-version binding.

### T10 — Timestamp Manipulation

Future, expired, or internally inconsistent timestamps must fail validation.

**Control:** strict temporal validation.

### T11 — Secret Leakage

Decision and attestation records must not expose raw assets, private keys, salts, secret nonces, or HMAC keys.

**Control:** structural model constraints, logging audit, exception-path tests.

### T12 — Dependency Contamination

Phase 6 must not create unauthorized coupling with research cryptography or execution control.

**Control:** AST dependency audit and runtime isolation tests.

---

## 7. Security Boundary Rules

The engineer MUST preserve:

```text
Phase 1 ─┐
Phase 2 ─┤
Phase 3 ─┤
Phase 4 ─┤→ Phase 5 Evidence Boundary → Phase 6 Decision Boundary
         │                                      │
         └──────────────────────────────────────┘
                                                │
                                                X
                                         ExecutionGate
```

The `X` is intentional.

Phase 6 may **describe** a security decision.

Phase 6 may **commit** an attestation.

Phase 6 may **evaluate** evidence.

Phase 6 may **not execute** the decision.

---

## 8. Cryptographic Requirements

Use cryptography only for integrity, binding, replay defense, and research-safe attestation commitments.

Allowed:

- SHA-256 commitments;
- existing HMAC verification infrastructure where already appropriate;
- cryptographically secure random nonces;
- canonical serialization;
- constant-time comparison;
- deterministic commitment verification.

Prohibited:

- production private-key provisioning;
- real hardware signing;
- YubiKey/PIV/TPM/HSM integration;
- production FROST authorization;
- threshold authorization;
- ZKP/TEE/BFT deployment;
- execution-gate signing authority;
- production identity issuance.

The engineer must not interpret a valid cryptographic commitment as semantic truth.

---

## 9. Concurrency Requirements

All mutable replay or decision-consumption state must use appropriate atomic synchronization.

At minimum test:

- 10+ concurrent decision evaluations;
- concurrent duplicate attestation submission;
- concurrent replay attempts;
- deterministic output under parallel evaluation;
- no race-induced acceptance of the same artifact more than once.

---

## 10. Observability & Leakage Requirements

Audit:

- `print()` calls;
- logger calls;
- exception messages;
- assertions;
- tracebacks.

Verify that no output exposes:

- raw asset bytes;
- private keys;
- HMAC secrets;
- secret nonces;
- salts;
- complete sensitive evidence payloads.

Reason codes should be safe for diagnostic exposure.

---

## 11. Documentation Deliverables

Create:

- `PHASE-6-ARCHITECTURE.md`
- `PHASE-6-SECURITY-REVIEW.md`
- `PHASE-6-THREAT-MODEL.md`
- `PHASE-6-TEST-REPORT.md`
- `PHASE-6-GOVERNANCE-GATE.md`

Documentation must explicitly distinguish:

1. evidence;
2. evaluation;
3. decision;
4. attestation;
5. authorization;
6. execution authority.

---

## 12. Verification Plan

Run the complete regression suite:

```bash
python -m pytest tests/security_substrate tests/frost_prototype -v
```

Then run the Phase 6-specific suite:

```bash
python -m pytest tests/security_substrate/test_decision_models.py tests/security_substrate/test_decision_policy.py tests/security_substrate/test_decision_engine.py tests/security_substrate/test_attestation.py tests/security_substrate/test_decision_replay.py tests/security_substrate/test_phase6_isolation.py tests/security_substrate/test_phase6_regression.py -v
```

Expected baseline:

- Existing Phase 1–5 tests: **103/103 PASSED**.
- All new Phase 6 tests: **0 failures**.
- No skipped security tests.
- No existing tests modified merely to accommodate Phase 6.
- No production security boundary weakened.

The final walkthrough must report:

- exact total test count;
- exact Phase 6 test count;
- exact runtime;
- exact files created/modified;
- security-review result;
- governance-gate result;
- any limitations discovered.

---

## 13. Governance Gate Requirements

Phase 6 is not considered complete merely because tests pass.

The engineer must provide a final governance gate demonstrating:

- [ ] Phase 1–5 behavior remains unchanged.
- [ ] Evidence remains distinct from truth.
- [ ] Decision remains distinct from authorization.
- [ ] Authorization remains distinct from execution authority.
- [ ] Phase 4 research evidence remains permanently research-only.
- [ ] No execution gate coupling exists.
- [ ] No epistemic state mutation exists.
- [ ] No production cryptographic provisioning exists.
- [ ] No real hardware integration exists.
- [ ] No production FROST authorization exists.
- [ ] Attestation commitments detect mutation.
- [ ] Replay defenses are concurrency-safe.
- [ ] No secret material is leaked.
- [ ] Threat model T1–T12 is addressed.
- [ ] All tests pass.
- [ ] Documentation accurately reflects implemented capability and limitations.

Final verdict must be one of:

- `PASS`
- `PASS WITH LIMITATIONS`
- `FAIL`

Do not declare `PASS` if a mandatory invariant is violated.

---

## 14. Explicitly Deferred Capabilities

The following remain prohibited and deferred:

- Production authorization engine
- Production execution authorization
- FROST-backed authorization
- Native YubiKey/PIV/TPM/HSM integration
- Hardware-backed production signing
- Production key provisioning
- Decentralized trust-anchor infrastructure
- BFT consensus
- ZKP infrastructure
- TEE enclave deployment
- Identity issuance
- Direct Phase 6 control of `ExecutionGate`
- Direct Phase 6 mutation of `EpistemicState`

These capabilities require a future explicit governance directive.

---

## 15. Engineer Operating Instructions

1. **Do not begin implementation until the user gives the green signal.**
2. Before modifying code, inspect the existing Phase 1–5 implementation and tests.
3. Preserve existing public APIs unless a compatibility-safe extension is explicitly required.
4. Do not rewrite earlier phases simply to make Phase 6 easier.
5. Prefer additive implementation.
6. Keep Phase 6 inside `security_substrate/`.
7. Keep all Phase 4 research code inside `research/frost_prototype/`.
8. Do not import research modules into production security-substrate modules.
9. Do not add production cryptographic credentials or hardware dependencies.
10. Do not create an `AUTHORIZED` decision state as a hidden substitute for authorization.
11. Do not add methods named `authorize()`, `unlock()`, `execute()`, or equivalent to `SecurityDecisionEngine`.
12. Do not allow a positive decision artifact to mutate `ExecutionGate` or `EpistemicState`.
13. If an architectural requirement is ambiguous, **stop and report the ambiguity rather than inventing authority semantics**.
14. If an implementation choice could weaken an existing security invariant, stop and report it before proceeding.
15. Run focused Phase 6 tests first, then the complete regression suite.
16. Perform a static/AST audit after implementation.
17. Perform a runtime isolation audit after implementation.
18. Produce all five Phase 6 documentation artifacts.
19. Do not claim production readiness.
20. Final completion must include a machine-verifiable test result and governance assessment.

---

## 16. Approval Gate

**Current status: PROPOSED — NOT YET AUTHORIZED FOR IMPLEMENTATION.**

The engineer must wait for explicit user approval before making Phase 6 code changes.

Required approval:

> **GREEN SIGNAL — PROCEED WITH PHASE 6**

Only after that approval should implementation begin.

---

## 17. Final Phase Boundary Statement

Phase 6 establishes a **decision and attestation boundary**, not an authorization or execution boundary.

The intended progression remains:

```text
Observation
    ↓
Evidence
    ↓
Evidence Validation
    ↓
Evidence Orchestration
    ↓
Security Evaluation
    ↓
Decision / Attestation
    ↓
[Future Explicit Authorization Boundary]
    ↓
[Future Explicit Execution Authority]
```

No arrow may bypass the governance boundary.

**End of Phase 6 Implementation Plan**
