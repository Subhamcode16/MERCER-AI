# IV-007 — Coverage, Assurance-Gap & Implementation Verification Matrix

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-002, IV-003, IV-004, IV-005, IV-006, III-004, III-009, III-010, III-012, III-013, III-015

---

# 1. Purpose

IV-007 converts the preceding architectural analysis into an implementation-oriented verification matrix.

The central question is no longer:

```text
WHAT SHOULD THE ARCHITECTURE DO?
```

It is:

```text
WHAT HAVE WE ACTUALLY IMPLEMENTED,
HOW DO WE TEST IT,
HOW DO WE VERIFY THE TEST,
AND WHAT EVIDENCE SUPPORTS THE CLAIM?
```

The architecture therefore requires a traceability chain:

```text
ARCHITECTURAL CLAIM
        ↓
SPECIFICATION
        ↓
OBJECT / CONTRACT
        ↓
IMPLEMENTATION COMPONENT
        ↓
DETERMINISTIC TEST
        ↓
SELF-CRITIQUE
        ↓
ADVERSARIAL TEST
        ↓
INDEPENDENT EVALUATION
        ↓
EVIDENCE
        ↓
ASSURANCE STATUS
```

This document is intended to expose gaps rather than conceal them.

---

# 2. Core Principle

A documented feature is not automatically an implemented feature.

An implemented feature is not automatically a verified feature.

A verified component is not automatically system-level assurance.

Therefore:

```text
DESIGN
≠
IMPLEMENTATION
≠
TEST
≠
VERIFICATION
≠
ASSURANCE
```

---

# 3. Traceability Model

Every consequential architectural claim should eventually map to:

```text
claim_id
 ↓
requirement_id
 ↓
contract_id
 ↓
implementation_ref
 ↓
test_refs
 ↓
verification_refs
 ↓
evidence_refs
 ↓
assurance_record
```

If any required relationship is missing, the claim has an assurance gap.

---

# 4. Coverage Dimensions

Coverage should be measured across at least:

```text
SPECIFICATION COVERAGE
IMPLEMENTATION COVERAGE
TEST COVERAGE
DETERMINISTIC VERIFICATION COVERAGE
ADVERSARIAL COVERAGE
INDEPENDENT EVALUATION COVERAGE
EVIDENCE COVERAGE
ASSURANCE COVERAGE
```

A single percentage must not hide these dimensions.

---

# 5. Specification Coverage

A claim has specification coverage when:

```text
the intended behavior
is explicitly defined
by an approved contract/specification.
```

Example:

```text
authority containment
```

must have a defined:

```text
scope
actor
resource
constraints
failure behavior
```

before implementation coverage can be meaningfully evaluated.

---

# 6. Implementation Coverage

A claim has implementation coverage when:

```text
a concrete implementation component
enforces or realizes the specified behavior.
```

The implementation reference should identify:

```text
module
service
function
policy
state machine
runtime boundary
configuration
```

where applicable.

---

# 7. Test Coverage

A claim has test coverage when:

```text
at least one reproducible test
evaluates the specified behavior.
```

Tests should include both:

```text
positive cases
negative cases
```

where applicable.

---

# 8. Verification Coverage

A claim has verification coverage when:

```text
test results are themselves assessed
against the claim and acceptance criteria.
```

Running tests is not identical to interpreting what the results establish.

---

# 9. Adversarial Coverage

A claim has adversarial coverage when:

```text
the architecture has been actively attacked
for ways to violate the claim.
```

For consequential claims, adversarial coverage should attempt:

```text
normal misuse
boundary conditions
malicious inputs
state races
authority escalation
dependency manipulation
version confusion
evidence poisoning
```

as relevant.

---

# 10. Independent Evaluation Coverage

Independent coverage exists when the claim is evaluated by a mechanism with sufficiently reduced shared failure modes.

Independence must be described across:

```text
model
prompt
data
implementation
evidence
runtime
threat model
evaluator
```

Complete independence may be impossible.

In that case, the limitation must be recorded.

---

# 11. Evidence Coverage

Evidence coverage asks:

```text
DO WE HAVE RECONSTRUCTABLE EVIDENCE
FOR THE VERIFICATION RESULT?
```

The evidence should preserve:

```text
target
version
protocol
inputs
outputs
evaluator
timestamp
provenance
limitations
```

---

# 12. Assurance Coverage

Assurance coverage asks:

```text
HAS THE EVIDENCE BEEN CONNECTED
TO A BOUNDED CLAIM?
```

Evidence without a claim is an observation.

A claim without evidence is an assertion.

Assurance requires the relationship.

---

# 13. Gap Taxonomy

Candidate assurance-gap classes:

```text
G0 — NO CLAIM DEFINITION
G1 — NO SPECIFICATION
G2 — NO IMPLEMENTATION
G3 — NO TEST
G4 — NO DETERMINISTIC CHECK
G5 — NO ADVERSARIAL TEST
G6 — NO INDEPENDENT EVALUATION
G7 — INSUFFICIENT EVIDENCE
G8 — EVIDENCE NOT TRACEABLE
G9 — VERIFIER CORRELATION TOO HIGH
G10 — ASSURANCE NOT DERIVED
G11 — ASSURANCE STALE
G12 — ASSURANCE REVOKED
G13 — UNKNOWN FAILURE MODE
G14 — UNSPECIFIED DEPENDENCY
G15 — IMPLEMENTATION / SPECIFICATION DRIFT
```

These are candidate engineering classifications.

---

# 14. Gap Severity

Candidate severity:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Critical gaps should include missing assurance for:

```text
authority containment
security boundaries
execution authorization
human-governance precedence
self-modification controls
irreversible actions
```

---

# 15. Master Traceability Record

Conceptually:

```yaml
assurance_trace:
  claim_id: ...
  requirement_ref: ...
  contract_ref: ...
  implementation_refs: []
  test_refs: []
  deterministic_verification_refs: []
  self_critique_refs: []
  adversarial_refs: []
  independent_evaluation_refs: []
  evidence_refs: []
  assurance_ref: ...
  gaps: []
  status: ...
```

---

# 16. Status Vocabulary

Candidate status:

```text
UNDEFINED
SPECIFIED
IMPLEMENTED
TESTED
VERIFIED
ADVERSARIALLY_TESTED
INDEPENDENTLY_EVALUATED
ASSURED
REASSESSMENT_REQUIRED
BLOCKED
REFUTED
```

The highest status reached must be evidence-backed.

---

# 17. Claim Promotion

A claim should move through:

```text
UNDEFINED
 ↓
SPECIFIED
 ↓
IMPLEMENTED
 ↓
TESTED
 ↓
VERIFIED
 ↓
ADVERSARIALLY_TESTED
 ↓
INDEPENDENTLY_EVALUATED
 ↓
ASSURED
```

Transitions may be skipped only when the assurance argument explicitly justifies the omission.

---

# 18. Demotion

A previously assured claim can be demoted by:

```text
new counterexample
implementation change
dependency invalidation
evidence invalidation
security change
policy change
target version change
verification protocol change
```

Possible result:

```text
REASSESSMENT_REQUIRED
```

or:

```text
REFUTED
```

---

# 19. Architecture-Level Coverage Matrix

| Claim | Specification | Implementation | Tests | Deterministic | Adversarial | Independent | Evidence | Assurance |
|---|---|---|---|---|---|---|---|---|
| Object identity integrity | Required | Required | Required | Required | Recommended | Recommended | Required | Required |
| Authority containment | Required | Required | Required | Required | Required | Required | Required | Required |
| Delegation containment | Required | Required | Required | Required | Required | Required | Required | Required |
| Constraint enforcement | Required | Required | Required | Required | Required | Recommended | Required | Required |
| Security non-bypass | Required | Required | Required | Required | Required | Required | Required | Required |
| Execution-intent containment | Required | Required | Required | Required | Required | Required | Required | Required |
| Provenance preservation | Required | Required | Required | Required | Recommended | Recommended | Required | Required |
| Lifecycle consistency | Required | Required | Required | Required | Required | Recommended | Required | Required |
| Revocation propagation | Required | Required | Required | Required | Required | Required | Required | Required |
| Approval binding | Required | Required | Required | Required | Required | Required | Required | Required |
| Self-critique effectiveness | Required | Required | Required | Partial | Required | Required | Required | Required |
| Adversarial verification effectiveness | Required | Required | Required | Partial | Required | Required | Required | Required |
| Verification independence | Required | Required | Required | Partial | Required | Required | Required | Required |
| Self-modification governance | Required | Required | Required | Required | Required | Required | Required | Required |
| Assurance invalidation | Required | Required | Required | Required | Required | Required | Required | Required |
| Recovery authorization | Required | Required | Required | Required | Required | Required | Required | Required |
| Evidence integrity | Required | Required | Required | Required | Required | Recommended | Required | Required |
| Decision reconstruction | Required | Required | Required | Partial | Recommended | Required | Required | Required |

`Required` means the architecture should not consider the claim fully assured without the corresponding evidence.

---

# 20. Authority Coverage Matrix

Authority claims deserve their own matrix.

| Property | Required artifact | Verification | Attack | Evidence |
|---|---|---|---|---|
| Identity | identity record | deterministic | spoofing | required |
| Issuer authority | authority chain | deterministic/relational | forged issuer | required |
| Scope | scope definition | deterministic | escalation | required |
| Expiration | temporal bound | deterministic | stale use | required |
| Revocation | revocation state | deterministic | post-revocation use | required |
| Delegation | delegation record | graph validation | transitive escalation | required |
| Constraints | constraint set | policy evaluation | bypass | required |
| Version | version binding | deterministic | version confusion | required |
| Execution binding | intent/action relation | relational | substitution | required |
| Provenance | lineage | provenance checker | poisoning | required |

---

# 21. Lifecycle Coverage Matrix

| Lifecycle property | Test |
|---|---|
| Legal state transition | positive + negative transition tests |
| Illegal transition rejection | seeded invalid transitions |
| Supersession | stale-object tests |
| Revocation | post-revocation execution tests |
| Expiration | boundary-time tests |
| Renewal | version-binding tests |
| Invalidation | dependency propagation tests |
| Rollback | authority and audit tests |
| Recovery | recovery authorization tests |
| Terminal-state protection | terminal mutation tests |
| Concurrent updates | race-condition tests |
| Version consistency | cross-version tests |
| Dependency cycles | graph validation tests |

---

# 22. Verification-Stack Coverage

For each high-impact claim:

```text
DETERMINISTIC CHECK
        +
SELF-CRITIQUE
        +
ADVERSARIAL VERIFICATION
        +
INDEPENDENT EVALUATION
```

should be considered as a combined stack where appropriate.

The architecture must not assume that every claim requires every layer.

The verification strategy must be claim-specific.

---

# 23. Verification Strategy Selection

A verification strategy should depend on:

```text
claim type
risk
determinism
impact
reversibility
authority
security sensitivity
available evidence
```

For example:

```text
expiration
→ deterministic check

semantic consistency
→ semantic evaluator

authority escalation
→ deterministic + adversarial + independent

self-critique usefulness
→ empirical benchmark + independent evaluation
```

---

# 24. Test Design Requirements

Every consequential test should identify:

```text
test_id
claim_ref
target_version
preconditions
input
expected behavior
observed behavior
pass/fail condition
evidence_ref
```

---

# 25. Negative Testing Requirement

For protected properties, negative testing is mandatory.

Examples:

```text
unauthorized action
expired authorization
revoked delegation
wrong version
wrong scope
invalid provenance
blocked security state
invalid lifecycle transition
```

The system must demonstrate rejection, not only successful operation.

---

# 26. Adversarial Test Requirements

Adversarial tests should document:

```text
attack objective
attacker capability
attack strategy
target
expected failure
observed result
counterexample
severity
reproduction
```

---

# 27. Hidden Evaluation Requirement

At least some consequential adversarial evaluations should use:

```text
held-out attack cases
```

to reduce benchmark overfitting.

---

# 28. Independent Evaluation Requirement

Independence should be strongest where:

```text
impact is high
failure is hard to detect
execution is irreversible
authority is broad
security boundaries are involved
```

---

# 29. Evidence Completeness

A verification result is incomplete when:

```text
PASS
```

exists without:

```text
target version
test protocol
inputs
expected behavior
observed behavior
provenance
```

The system should reject assurance records that cannot reconstruct how the result was obtained.

---

# 30. Evidence Freshness

Evidence should be checked against:

```text
target version
dependency versions
policy version
security state
evaluation protocol
```

Stale evidence must trigger:

```text
REASSESSMENT_REQUIRED
```

where the relevant contract requires it.

---

# 31. Implementation / Specification Drift

Drift exists when:

```text
IMPLEMENTATION
≠
CURRENT SPECIFICATION
```

Drift may occur because:

```text
implementation changed
contract changed
policy changed
dependency changed
assumptions changed
```

The traceability matrix must identify these mismatches.

---

# 32. Orphan Detection

An orphan implementation is:

```text
implementation
without a current specification / contract reference.
```

An orphan claim is:

```text
claim
without implementation or verification evidence.
```

Both should be reported.

---

# 33. Duplicate Assurance

Two assurance records may appear independent while both derive from the same evidence.

Therefore detect:

```text
duplicate evidence lineage
shared evaluator
shared test set
shared model
shared prompt
```

before counting them as independent evidence.

---

# 34. Correlation Risk Matrix

| Shared dependency | Risk |
|---|---|
| Same model | High correlated reasoning failure |
| Same prompt | Shared framing failure |
| Same evidence | Shared evidence error |
| Same test set | Shared blind spot |
| Same implementation | Shared implementation defect |
| Same runtime | Shared infrastructure failure |
| Same threat model | Shared attack-space omission |

This matrix is diagnostic, not a mathematical independence proof.

---

# 35. Coverage Does Not Equal Quality

A system can have:

```text
100% test coverage
```

and still have:

```text
weak tests
wrong expected behavior
poor threat model
correlated verification
unmeasured failure modes
```

Therefore coverage must always be accompanied by evidence quality.

---

# 36. Evidence Quality Dimensions

Candidate dimensions:

```text
RELEVANCE
VALIDITY
COMPLETENESS
INDEPENDENCE
REPRODUCIBILITY
FRESHNESS
INTEGRITY
TRACEABILITY
```

---

# 37. Assurance-Gap Report

The system should be able to produce:

```text
CLAIMS
SUPPORTED
CLAIMS
PARTIALLY SUPPORTED
CLAIMS
UNSUPPORTED
CLAIMS
REFUTED
CLAIMS
STALE
CLAIMS
REQUIRING INDEPENDENT REVIEW
```

This report is itself evidence of architectural maturity.

---

# 38. Gap Prioritization

Prioritize gaps by:

```text
impact
likelihood
uncertainty
attackability
irreversibility
dependency centrality
authority scope
```

A missing test for a cosmetic output is not equivalent to missing verification of execution authorization.

---

# 39. Centrality Risk

A component with many downstream dependencies has greater assurance importance.

Conceptually:

```text
dependency centrality
        ↑
assurance priority
        ↑
verification depth
```

A failure in a central authority or policy component can invalidate many downstream claims.

---

# 40. Critical Path Verification

The following path deserves maximum scrutiny:

```text
IDENTITY
 ↓
AUTHORITY
 ↓
POLICY
 ↓
CONSTRAINT
 ↓
DECISION
 ↓
APPROVAL
 ↓
EXECUTION INTENT
 ↓
SECURITY GATE
 ↓
EXECUTION
```

Each transition must be independently reconstructable.

---

# 41. Proof-Carrying Execution

For high-impact execution, the runtime should ideally be able to produce:

```text
execution_id
decision_ref
approval_ref
authority_ref
constraint_refs
security_state_ref
verification_refs
assurance_ref
```

This creates an execution evidence chain.

---

# 42. Pre-Execution Verification

Before consequential execution:

```text
CURRENT STATE
 ↓
AUTHORITY VALID
 ↓
DECISION CURRENT
 ↓
APPROVAL CURRENT
 ↓
CONSTRAINTS SATISFIED
 ↓
SECURITY ALLOWS
 ↓
VERIFICATION REQUIREMENTS SATISFIED
 ↓
EXECUTE
```

This complements the lifecycle and precedence work from IV-004 and IV-005.

---

# 43. Post-Execution Evidence

After execution:

```text
ACTION
 ↓
OBSERVED OUTCOME
 ↓
EVIDENCE
 ↓
EVALUATION
 ↓
ASSURANCE UPDATE
```

The system should preserve both intended and observed outcomes.

---

# 44. Failure-to-Claim Feedback

A discovered failure should update:

```text
implementation
test suite
adversarial suite
proof obligation
assurance status
documentation
```

where applicable.

This creates a learning loop for the engineering process.

---

# 45. Counterexample Promotion

A confirmed counterexample should normally become:

```text
counterexample record
+
regression test
+
assurance impact assessment
```

For systemic failures, it should also produce:

```text
new proof obligation
```

if the existing claim was underspecified.

---

# 46. Self-Critique Coverage

The self-critique subsystem should itself have a coverage matrix:

| Capability | Seeded errors | Hidden errors | Independent evaluator | Status |
|---|---|---|---|---|
| contradiction detection | Required | Required | Required | OPEN |
| unsupported-claim detection | Required | Required | Required | OPEN |
| constraint checking | Required | Required | Required | OPEN |
| assumption detection | Required | Required | Required | OPEN |
| uncertainty detection | Required | Required | Required | OPEN |
| correction quality | Required | Required | Required | OPEN |

---

# 47. Adversarial-Verifier Coverage

| Attack class | Seeded | Variant | Hidden | Independent judge | Status |
|---|---|---|---|---|---|
| authority escalation | Required | Required | Required | Required | OPEN |
| scope confusion | Required | Required | Required | Required | OPEN |
| stale approval | Required | Required | Required | Required | OPEN |
| provenance poisoning | Required | Required | Required | Required | OPEN |
| security race | Required | Required | Required | Required | OPEN |
| prompt injection | Required | Required | Required | Required | OPEN |
| tool manipulation | Required | Required | Required | Required | OPEN |
| self-modification bypass | Required | Required | Required | Required | OPEN |

---

# 48. Verifier Capability Matrix

Measure the verifier against increasingly capable producers.

| Producer difficulty | Detection rate | False reassurance | Coverage |
|---|---:|---:|---:|
| Low | TBD | TBD | TBD |
| Moderate | TBD | TBD | TBD |
| High | TBD | TBD | TBD |
| Expert / adversarial | TBD | TBD | TBD |

This is one of the most important empirical experiments in the architecture.

---

# 49. Assurance Maturity

Candidate maturity stages:

```text
M0 — DESIGN ONLY
M1 — IMPLEMENTED
M2 — TESTED
M3 — VERIFIED
M4 — ADVERSARIALLY TESTED
M5 — INDEPENDENTLY EVALUATED
M6 — ASSURANCE-TRACKED
M7 — CONTINUOUSLY ASSURED
```

These are proposed engineering maturity labels.

---

# 50. Minimum Evidence for Maturity

### M0

Specification exists.

### M1

Implementation exists.

### M2

Reproducible tests exist.

### M3

Verification criteria and results exist.

### M4

Adversarial testing exists.

### M5

Independent evaluation exists.

### M6

Evidence and assurance are versioned and traceable.

### M7

Assurance is continuously reassessed after relevant change.

---

# 51. Current Architectural Reality

At this stage, we should not label the entire architecture:

```text
PROVEN
```

The correct status is closer to:

```text
SPECIFICATION-RICH
+
PARTIALLY IMPLEMENTED
+
VERIFICATION PLAN DEFINED
+
EMPIRICAL ASSURANCE PENDING
```

This distinction must remain explicit.

---

# 52. Current Highest-Priority Gaps

The next engineering effort should prioritize evidence for:

```text
G2 — implementation completeness
G3 — reproducible test coverage
G5 — adversarial coverage
G6 — independent evaluation
G7 — evidence sufficiency
G9 — verification independence
G10 — assurance derivation
```

The exact gap status must be updated against the actual implementation repository and current test results before being treated as final.

---

# 53. Engineering Build Order

Recommended order:

```text
1. Freeze contracts
2. Build traceability registry
3. Implement deterministic invariants
4. Implement lifecycle checks
5. Implement authority enforcement
6. Build evidence ledger
7. Build self-critique agent
8. Build adversarial verifier
9. Build hidden failure suite
10. Build independent evaluation path
11. Build assurance engine
12. Build assurance dashboard
13. Run system-wide falsification
14. Update assurance records
```

This order is designed to avoid building sophisticated AI verification around weak underlying invariants.

---

# 54. Do Not Start With the LLM Verifier

A critical engineering rule:

```text
DO NOT BUILD THE SELF-CRITIQUE
AND ADVERSARIAL AGENTS FIRST.
```

First implement:

```text
schemas
identities
authority
constraints
state transitions
provenance
deterministic invariants
```

Otherwise the verifier may merely produce plausible language around an unstable substrate.

---

# 55. Verification Stack Dependency

The dependency should be:

```text
FOUNDATIONAL INVARIANTS
        ↓
DETERMINISTIC VERIFICATION
        ↓
SEMANTIC VERIFICATION
        ↓
ADVERSARIAL VERIFICATION
        ↓
INDEPENDENT EVALUATION
        ↓
ASSURANCE
```

Not:

```text
LLM
 ↓
LLM critic
 ↓
LLM adversary
 ↓
"trusted"
```

---

# 56. Engineering Acceptance Rule

A critical architectural claim cannot be marked:

```text
ASSURED
```

merely because:

```text
the implementation exists
+
tests pass
```

The assurance record must demonstrate that the verification depth is appropriate to the claim's risk.

---

# 57. Auditability Requirement

Every assurance status must answer:

```text
WHY IS THIS CLAIM CURRENTLY MARKED THIS WAY?
```

The answer must be reconstructable from:

```text
specification
implementation
tests
verification
adversarial results
independence
evidence
assurance history
```

---

# 58. Architecture-Wide Matrix

The eventual master registry should resemble:

```text
CLAIM
│
├── CONTRACT
│
├── IMPLEMENTATION
│
├── TESTS
│
├── DETERMINISTIC CHECKS
│
├── SELF-CRITIQUE
│
├── ADVERSARIAL VERIFICATION
│
├── INDEPENDENT EVALUATION
│
├── EVIDENCE
│
├── COUNTEREXAMPLES
│
├── LIMITATIONS
│
└── ASSURANCE STATUS
```

This registry becomes the architectural equivalent of a verification ledger.

---

# 59. Key Invariants

### Invariant 1

No claim may be considered assured without a traceable evidence chain.

### Invariant 2

Implementation existence does not establish verification.

### Invariant 3

Test success does not establish universal correctness.

### Invariant 4

Self-critique does not establish independence.

### Invariant 5

Multiple correlated verifiers do not constitute independent verification.

### Invariant 6

No counterexample found does not prove impossibility.

### Invariant 7

High-impact authority claims require negative and adversarial testing.

### Invariant 8

Stale evidence must not silently preserve current assurance.

### Invariant 9

Material counterexamples must affect assurance status.

### Invariant 10

Assurance must be version- and dependency-aware.

### Invariant 11

A critical verification gap must prevent unconditional assurance.

### Invariant 12

The verification stack itself must be evaluated.

---

# 60. Exit Criteria

- [x] Traceability model defined
- [x] Coverage dimensions defined
- [x] Specification coverage defined
- [x] Implementation coverage defined
- [x] Test coverage defined
- [x] Verification coverage defined
- [x] Adversarial coverage defined
- [x] Independent evaluation coverage defined
- [x] Evidence coverage defined
- [x] Assurance coverage defined
- [x] Assurance-gap taxonomy defined
- [x] Gap severity defined
- [x] Master traceability record defined
- [x] Claim promotion/demotion defined
- [x] Architecture coverage matrix defined
- [x] Authority coverage matrix defined
- [x] Lifecycle coverage matrix defined
- [x] Verification strategy selection defined
- [x] Negative testing requirement defined
- [x] Hidden evaluation requirement defined
- [x] Evidence completeness/freshness defined
- [x] Specification drift defined
- [x] Correlation risk defined
- [x] Critical execution path defined
- [x] Proof-carrying execution defined
- [x] Self-critique coverage defined
- [x] Adversarial-verifier coverage defined
- [x] Verifier capability matrix defined
- [x] Assurance maturity defined
- [x] Current architectural status distinguished from proof
- [x] Engineering build order defined
- [x] Verification stack dependency defined
- [x] Architecture-wide invariants defined

**Current assessment:** IV-007 establishes the traceability and gap-analysis layer required to prevent the project from confusing architectural documentation with demonstrated capability. The next engineering phase should use this matrix against the actual implementation and test repository to convert every `OPEN` item into an evidence-backed status.

---

# 61. Next Document

**IV-008 — System-Wide Falsification, Red-Team Protocol & Failure-Injection Specification**

IV-008 should turn the verification philosophy into an executable adversarial campaign:

```text
ARCHITECTURAL CLAIM
        ↓
ATTACK MODEL
        ↓
FAILURE INJECTION
        ↓
OBSERVATION
        ↓
COUNTEREXAMPLE
        ↓
CONTAINMENT
        ↓
REPAIR
        ↓
REGRESSION
        ↓
REVERIFICATION
```

It should define how we deliberately try to break:

```text
authority
delegation
constraints
policy
lifecycle
provenance
decision integrity
approval binding
security boundaries
self-critique
adversarial verification
self-modification
recovery
assurance itself
```

The objective is to make **failure discovery a designed capability of the product**, rather than something we perform only after deployment.
