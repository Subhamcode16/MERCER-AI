# IV-011 — Assurance Computation, Evidence Aggregation & Conservative Decision Semantics Specification

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-006, IV-007, IV-008, IV-009, IV-010, III-004, III-009, III-010, III-012, III-013, III-015

---

# 1. Purpose

IV-011 defines how the architecture derives an assurance state from the evidence and verification structure established in IV-006 through IV-010.

The central problem is:

```text
WE HAVE EVIDENCE
        ↓
WHAT ARE WE ACTUALLY ENTITLED TO CONCLUDE?
```

The system must not convert:

```text
many observations
```

into:

```text
unjustified certainty
```

The governing principle is:

```text
STRONGEST JUSTIFIABLE CLAIM
        ≤
AVAILABLE EVIDENCE
```

The assurance engine therefore performs bounded epistemic computation rather than generic confidence scoring.

---

# 2. Core Principle

Assurance is not:

```text
A SINGLE NUMBER
```

and it is not:

```text
MODEL CONFIDENCE
```

Instead, assurance is a structured conclusion bounded by:

```text
proof obligations
evidence
verification
independence
freshness
assumptions
counterexamples
scope
limitations
```

---

# 3. Source Basis

IV-011 builds on:

```text
IV-006 — Evidence, Verification, Self-Critique & Adversarial Self-Verification Architecture
IV-007 — Coverage, Assurance-Gap & Implementation Verification Matrix
IV-008 — System-Wide Falsification, Red-Team Protocol & Failure-Injection Specification
IV-009 — Verification Runtime, Evaluation Harness & Experimental Control Specification
IV-010 — Assurance Ledger, Evidence Graph & Claim-to-Proof Knowledge Architecture
```

The document preserves the distinction:

```text
OBSERVATION
≠
EVIDENCE
≠
VERIFICATION
≠
ASSURANCE
```

---

# 4. Assurance Computation Model

Conceptually:

```text
CLAIM
 ↓
PROOF OBLIGATIONS
 ↓
EVIDENCE
 ↓
VERIFICATION
 ↓
VALIDITY CHECK
 ↓
INDEPENDENCE CHECK
 ↓
COUNTEREXAMPLE CHECK
 ↓
SCOPE CHECK
 ↓
ASSURANCE DERIVATION
```

The engine should compute the strongest bounded status supported by these inputs.

---

# 5. No Unjustified Probability

The assurance engine must not produce:

```text
"93% assured"
```

unless a separately justified statistical model establishes what that number means.

Default representation should be:

```text
status
scope
basis
limitations
freshness
independence
unresolved obligations
```

---

# 6. Assurance State Space

Candidate states:

```text
UNKNOWN
UNASSESSED
PARTIALLY_SUPPORTED
SUPPORTED
VERIFIED
ADVERSARIALLY_VERIFIED
INDEPENDENTLY_EVALUATED
ASSURED
REASSESSMENT_REQUIRED
CONTRADICTED
REFUTED
RETIRED
```

These states describe epistemic and engineering status, not metaphysical truth.

---

# 7. State Ordering

A useful conceptual ordering is:

```text
UNKNOWN
  ↓
PARTIALLY_SUPPORTED
  ↓
SUPPORTED
  ↓
VERIFIED
  ↓
ADVERSARIALLY_VERIFIED
  ↓
INDEPENDENTLY_EVALUATED
  ↓
ASSURED
```

However, this is not a universal linear scale.

A claim may be:

```text
verified
```

while simultaneously:

```text
independence-limited
```

or:

```text
scope-limited
```

Therefore the engine should retain multidimensional metadata.

---

# 8. Orthogonal Assurance Dimensions

Represent separately:

```text
SPECIFICATION_STATUS
IMPLEMENTATION_STATUS
TEST_STATUS
VERIFICATION_STATUS
ADVERSARIAL_STATUS
INDEPENDENCE_STATUS
EVIDENCE_STATUS
FRESHNESS_STATUS
COUNTEREXAMPLE_STATUS
ASSUMPTION_STATUS
```

This avoids hiding weaknesses behind one aggregate label.

---

# 9. Proof-Obligation Satisfaction

Each proof obligation should resolve to:

```text
SATISFIED
PARTIALLY_SATISFIED
UNSATISFIED
UNKNOWN
NOT_APPLICABLE
```

The result must be evidence-backed.

---

# 10. Evidence Classification

Evidence should be classified as:

```text
DIRECT
INDIRECT
PARTIAL
CORROBORATING
CONTRADICTORY
IRRELEVANT
STALE
INVALID
```

Classification is separate from evidence integrity.

---

# 11. Evidence Validity

Evidence validity depends on:

```text
integrity
provenance
relevance
freshness
scope
method validity
```

An artifact may be authentic but still not support the claim.

---

# 12. Evidence Integrity

Integrity asks:

```text
WAS THE EVIDENCE ALTERED?
```

Possible states:

```text
VALID
COMPROMISED
UNKNOWN
```

---

# 13. Evidence Freshness

Freshness asks:

```text
DOES THE EVIDENCE STILL APPLY TO THE CURRENT TARGET?
```

Possible states:

```text
CURRENT
STALE
EXPIRED
UNKNOWN
```

---

# 14. Evidence Scope

Evidence should identify:

```text
target version
environment
dataset
model
protocol
threat model
```

A result outside the current scope must not silently become current assurance.

---

# 15. Evidence Relevance

For each proof obligation:

```text
does this evidence actually bear on the obligation?
```

Possible relation:

```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
CORROBORATION
CONTRADICTION
NO_SUPPORT
```

---

# 16. Evidence Independence

Evidence sources may share dependencies.

For example:

```text
E1 ← Model A
E2 ← Model A
E3 ← Model A
```

should not be treated as three fully independent confirmations.

The assurance engine should retain:

```text
shared_model
shared_dataset
shared_prompt
shared_implementation
shared_evaluator
shared_evidence
```

relationships.

---

# 17. Independence Profile

Represent independence as a structured profile:

```yaml
independence_profile:
  model_independence: ...
  evaluator_independence: ...
  data_independence: ...
  implementation_independence: ...
  evidence_independence: ...
  threat_model_independence: ...
```

Avoid collapsing this immediately into a single scalar.

---

# 18. Correlated Evidence

Correlated evidence can still be useful.

However:

```text
CORROBORATION
≠
INDEPENDENT CONFIRMATION
```

The assurance engine should preserve both facts.

---

# 19. Contradictory Evidence

When:

```text
E1 supports claim
E2 contradicts claim
```

the default result should not be:

```text
average(E1,E2)
```

Instead:

```text
CONFLICT
 ↓
INVESTIGATE
 ↓
REASSESS
```

The system must preserve the contradiction.

---

# 20. Evidence Conflict Record

```yaml
evidence_conflict:
  conflict_id: ...
  claim_id: ...
  supporting_refs: []
  contradicting_refs: []
  scope_comparison: ...
  severity: ...
  resolution_status: ...
```

---

# 21. Partial Evidence

Evidence may support only part of a claim.

Example:

```text
Claim:
authority cannot be escalated.

Evidence:
scope containment = verified
revocation = verified
delegation chaining = unknown
```

The claim should remain:

```text
PARTIALLY_SUPPORTED
```

unless its assurance argument explicitly establishes that the unresolved obligation is non-essential.

---

# 22. Required vs Optional Obligations

Proof obligations should be classified:

```text
REQUIRED
CONDITIONAL
SUPPORTING
OPTIONAL
```

A missing required obligation should prevent unconditional assurance.

---

# 23. Conditional Obligations

Some obligations apply only under conditions.

Example:

```text
IF external execution is enabled
THEN tool authorization proof is required.
```

The assurance engine must evaluate the condition before applying the obligation.

---

# 24. Assumption Validity

Assumptions are first-class inputs.

Each assumption should be:

```text
VALID
INVALID
UNKNOWN
```

An invalid critical assumption must invalidate or demote dependent assurance.

---

# 25. Assumption Scope

An assumption must identify:

```text
claim scope
environment
time
dependency
condition
```

A local assumption must not silently become global.

---

# 26. Counterexample Semantics

A confirmed counterexample is stronger than an additional weak positive test.

Candidate states:

```text
NONE_FOUND
SUSPECTED
CONFIRMED
RESOLVED
REGRESSION
```

---

# 27. Counterexample Severity

Severity should consider:

```text
impact
exploitability
reproducibility
scope
authority involved
reversibility
detection
```

---

# 28. Counterexample Effect

A confirmed counterexample may produce:

```text
ASSURANCE_DEMOTION
ASSURANCE_INVALIDATION
CLAIM_REFUTATION
REASSESSMENT_REQUIRED
```

depending on the claim and scope.

---

# 29. Counterexample Scope

A failure affecting:

```text
one edge case
```

does not automatically refute:

```text
all behavior
```

But it may refute a universal claim.

Therefore the engine must evaluate the semantic scope of the counterexample.

---

# 30. Universal Claim Caution

Claims using terms such as:

```text
always
never
cannot
all
guaranteed
```

require especially strong proof obligations.

A single valid counterexample may refute such a claim.

---

# 31. Bounded Claims

Prefer:

```text
"Under conditions X, the system enforces Y."
```

over:

```text
"The system can never violate Y."
```

Bounded claims are easier to verify honestly.

---

# 32. Assurance Scope

Every assurance result should specify:

```text
what is covered
what is not covered
which environment
which version
which assumptions
which threat model
```

---

# 33. Assurance Derivation

Conceptually:

```text
proof obligations
+
valid evidence
+
valid verification
+
acceptable independence
+
current scope
+
no unresolved disqualifying counterexample
        ↓
ASSURANCE STATE
```

The exact rule set must be explicit and versioned.

---

# 34. Conservative Aggregation

The default aggregation principle is:

```text
MISSING CRITICAL EVIDENCE
        ↓
DO NOT ASSUME SATISFACTION
```

and:

```text
UNKNOWN
        ≠
PASS
```

---

# 35. Unknown State

Unknown is a first-class result.

Examples:

```text
not tested
insufficient evidence
judge disagreement
unresolved dependency
unreliable evaluator
unexplored attack space
```

The engine must not convert these into:

```text
negative
```

or:

```text
positive
```

without justification.

---

# 36. Three-Valued Logic

Where useful, deterministic proof conditions may use:

```text
TRUE
FALSE
UNKNOWN
```

This is preferable to forcing uncertain observations into binary states.

---

# 37. Four-Valued Extension

For contradictory evidence, consider:

```text
SUPPORTED
CONTRADICTED
BOTH
NEITHER
```

This can be useful where evidence from multiple sources conflicts.

The implementation should select an explicit logical framework before production use.

---

# 38. Assurance Rule

A candidate rule:

```text
IF
all required proof obligations = SATISFIED
AND
evidence = CURRENT
AND
integrity = VALID
AND
no disqualifying counterexample
AND
verification requirements satisfied
THEN
claim may be ASSURED
```

This is a candidate rule, not yet a formal proof calculus.

---

# 39. Partial-Assurance Rule

If:

```text
some required obligations = SATISFIED
some = UNKNOWN
```

then:

```text
PARTIALLY_SUPPORTED
```

or:

```text
REASSESSMENT_REQUIRED
```

depending on risk.

---

# 40. Contradiction Rule

If:

```text
critical evidence = CONTRADICTORY
```

then:

```text
ASSURANCE
→
REASSESSMENT_REQUIRED
```

unless the conflict is resolved through a defined adjudication mechanism.

---

# 41. Refutation Rule

If a counterexample directly violates a universal or critical claim:

```text
CLAIM
→
REFUTED
```

The architecture must preserve the counterexample permanently in historical records.

---

# 42. Demotion Rule

If an assurance dependency becomes invalid:

```text
ASSURED
 ↓
REASSESSMENT_REQUIRED
```

rather than silently retaining the previous state.

---

# 43. Restoration Rule

Restoration requires:

```text
new evidence
+
new verification
+
updated assurance argument
```

It cannot be accomplished by manually restoring a previous status.

---

# 44. Assurance Thresholds

Thresholds should be used for:

```text
decision policies
risk controls
release gates
```

not as substitutes for epistemic reasoning.

Example:

```text
CRITICAL RELEASE
requires:
A5 assurance
+
zero open critical counterexamples
+
current evidence
```

---

# 45. Risk-Adjusted Requirements

Higher-risk claims require stronger evidence.

Conceptually:

```text
risk ↑
 ↓
verification depth ↑
 ↓
independence requirement ↑
 ↓
evidence requirement ↑
```

---

# 46. Reversibility

Irreversible actions should require stronger assurance than reversible actions.

Example:

```text
reversible simulation
<
production write
<
irreversible external action
```

The exact policy belongs in the governance layer.

---

# 47. Authority Sensitivity

Claims involving:

```text
privilege
security
self-modification
financial action
external execution
human governance
```

should receive elevated assurance requirements.

---

# 48. Decision Semantics

Assurance should inform decisions but not become the decision itself.

Conceptually:

```text
ASSURANCE
+
RISK
+
AUTHORITY
+
CONTEXT
+
POLICY
        ↓
DECISION
```

The assurance engine should expose bounded facts to the decision layer.

---

# 49. No Assurance-Based Authority Escalation

A critical invariant:

```text
HIGH ASSURANCE
≠
HIGHER AUTHORITY
```

Assurance may establish that a claim is well-supported.

It does not grant permission to act.

---

# 50. Decision Preconditions

A decision may require:

```text
minimum assurance level
current evidence
valid authority
valid constraints
security clearance
```

All must be evaluated separately.

---

# 51. Assurance as a Gate

For high-impact actions:

```text
ACTION REQUEST
 ↓
AUTHORITY VALID?
 ↓
CONSTRAINTS VALID?
 ↓
ASSURANCE REQUIREMENT SATISFIED?
 ↓
SECURITY ALLOWS?
 ↓
EXECUTE
```

A failed assurance requirement should produce:

```text
BLOCK
```

or:

```text
ESCALATE
```

according to policy.

---

# 52. Assurance vs Confidence

Confidence may be used inside a model or statistical evaluator.

But:

```text
MODEL CONFIDENCE
```

must remain distinct from:

```text
ARCHITECTURAL ASSURANCE
```

A model can be highly confident and still fail an assurance obligation.

---

# 53. Assurance vs Probability of Correctness

Unless a formally justified probabilistic argument exists:

```text
ASSURED
```

must not be interpreted as:

```text
P(correct) = X
```

The architecture should avoid that ambiguity.

---

# 54. Evidence Aggregation Strategies

Candidate strategies:

```text
CONJUNCTIVE
DISJUNCTIVE
THRESHOLD
CONDITIONAL
WEIGHTED
STRUCTURAL
```

The selected strategy must be defined by claim type.

---

# 55. Conjunctive Aggregation

Use when:

```text
all proof obligations are necessary.
```

Example:

```text
scope valid
AND
revocation valid
AND
expiration valid
```

---

# 56. Disjunctive Aggregation

Use when:

```text
multiple independent methods can establish the same property.
```

Example:

```text
formal proof
OR
independent deterministic test
```

only when the assurance rule explicitly permits either route.

---

# 57. Threshold Aggregation

Use when:

```text
N independent evaluators
```

are required to satisfy a policy.

This requires an explicit independence model.

---

# 58. Weighted Aggregation

Weighted scoring should be treated cautiously.

A weighted score may hide:

```text
critical missing evidence
```

Therefore weighted aggregation must not override hard safety/security requirements.

---

# 59. Structural Aggregation

Prefer structural reasoning where possible:

```text
claim
→ obligations
→ evidence
→ verification
```

rather than arbitrary numeric scores.

---

# 60. Evidence Redundancy

Multiple evidence sources can improve robustness when they have genuinely different failure modes.

Examples:

```text
formal invariant
+
deterministic runtime test
+
independent adversarial test
```

This is stronger than:

```text
three similar LLM judges
```

---

# 61. Independent Evidence Requirement

For the highest assurance levels, require evidence from materially different mechanisms.

Possible dimensions:

```text
implementation
model
method
data
evaluator
threat model
```

---

# 62. Judge Disagreement

If judges disagree:

```text
J1 = PASS
J2 = FAIL
```

default:

```text
INCONCLUSIVE
```

unless a predefined adjudication rule exists.

---

# 63. Adjudication

Adjudication should record:

```text
conflict
reviewer
evidence considered
reason
decision
limitations
```

The original disagreement remains preserved.

---

# 64. Evidence Weight vs Independence

An evidence source may be highly reliable but correlated.

Therefore track separately:

```text
reliability
independence
relevance
freshness
```

---

# 65. Staleness Penalty

Avoid arbitrary numerical decay unless justified.

Prefer categorical states:

```text
CURRENT
REASSESSMENT_REQUIRED
STALE
INVALID
```

with explicit invalidation rules.

---

# 66. Assurance Expiration

Some assurance may have an explicit validity interval:

```text
valid_until
```

Examples:

```text
security evaluation
dependency-specific verification
time-sensitive policy
temporary authority
```

---

# 67. Event-Triggered Reassessment

Even before expiration, trigger reassessment when:

```text
counterexample found
dependency changed
policy changed
model changed
implementation changed
security posture changed
```

---

# 68. Monotonicity

A useful desired property:

```text
ADDING VALID SUPPORT
```

should not unexpectedly reduce assurance.

But:

```text
ADDING CONTRADICTORY EVIDENCE
```

may reduce assurance.

The rules must explicitly define such behavior.

---

# 69. Non-Monotonic Assurance

Assurance is inherently non-monotonic because:

```text
new counterexample
```

can invalidate previous conclusions.

Therefore the architecture must support belief revision.

---

# 70. Belief Revision

Conceptually:

```text
CURRENT ASSURANCE
        ↓
NEW EVIDENCE
        ↓
RECALCULATION
        ↓
NEW ASSURANCE
```

Historical states remain preserved.

---

# 71. Assurance Stability

Repeated recalculation under unchanged inputs should produce the same result.

This gives:

```text
deterministic assurance computation
```

for deterministic assurance rules.

---

# 72. Assurance Rule Versioning

Record:

```text
rule_set_id
rule_set_version
```

with every derived assurance state.

A change in assurance logic is itself a material change.

---

# 73. Assurance Computation Record

```yaml
assurance_computation:
  computation_id: ...
  claim_id: ...
  rule_set_ref: ...
  input_refs: []
  previous_status: ...
  computed_status: ...
  unresolved_items: []
  limitations: []
  timestamp: ...
```

---

# 74. Explainability

The engine should answer:

```text
WHY DID THIS CLAIM RECEIVE THIS STATUS?
```

The answer should enumerate:

```text
satisfied obligations
unsatisfied obligations
evidence
counterexamples
assumptions
independence
freshness
rules
```

---

# 75. Counterfactual Explanation

The engine should also answer:

```text
WHAT WOULD HAVE TO CHANGE
FOR THIS CLAIM TO BECOME ASSURED?
```

Example:

```text
missing independent evaluation
+
stale evidence
```

This creates actionable engineering work.

---

# 76. Assurance Gap Generation

From the computation, generate:

```text
GAP
```

for:

```text
missing proof obligation
missing evidence
stale evidence
insufficient independence
unresolved contradiction
open counterexample
invalid assumption
```

These map back to IV-007.

---

# 77. Assurance Debt Integration

Each unresolved condition contributes to:

```text
assurance debt
```

according to:

```text
severity
criticality
dependency centrality
```

not arbitrary counts alone.

---

# 78. Release Decision

A release system may query:

```text
ARE ALL RELEASE-BLOCKING CLAIMS
AT REQUIRED ASSURANCE LEVEL?
```

The assurance engine supplies the answer.

It does not independently decide whether release is permitted unless governance explicitly assigns that authority.

---

# 79. Governance Boundary

The architecture must distinguish:

```text
ASSURANCE ENGINE
```

from:

```text
GOVERNANCE AUTHORITY
```

The first evaluates evidence.

The second determines policy consequences.

---

# 80. Safety Override

No assurance level should override:

```text
hard security constraint
explicit prohibition
human governance boundary
```

unless the governing contract explicitly allows such behavior.

---

# 81. Assurance Failure Modes

The assurance engine itself may fail through:

```text
incorrect aggregation
missing dependency
wrong rule version
evidence omission
counterexample omission
stale graph
correlated verifier misclassification
logic bug
```

Therefore the assurance engine must be tested and audited.

---

# 82. Assurance Engine Verification

Test:

```text
known pass
known fail
unknown
contradictory evidence
partial evidence
stale evidence
invalid evidence
counterexample
dependency change
rule change
```

---

# 83. Metamorphic Properties

Useful properties include:

```text
adding irrelevant evidence
→
should not change assurance.

removing required evidence
→
must not increase assurance.

introducing confirmed counterexample
→
must not increase assurance.

invalidating critical dependency
→
must not preserve unconditional assurance.
```

These become powerful deterministic tests.

---

# 84. Conservative Semantics

The engine should follow:

```text
UNCERTAINTY
→
PRESERVE UNCERTAINTY
```

rather than:

```text
UNCERTAINTY
→
ASSUME PASS
```

---

# 85. Strongest Defensible Statement

For each claim, the engine should produce:

```yaml
assurance_statement:
  claim: ...
  status: ...
  scope: ...
  evidence_basis: []
  verification_basis: []
  unresolved: []
  limitations: []
```

This is preferable to a naked confidence score.

---

# 86. Example

Claim:

```text
"The authority system prevents unauthorized delegation."
```

Evidence:

```text
scope test = PASS
revocation test = PASS
delegation chain test = PASS
adversarial escalation = PASS
independent evaluation = NOT RUN
```

Possible conclusion:

```text
ADVERSARIALLY_VERIFIED
```

with:

```text
independent evaluation = missing
```

It should not automatically become:

```text
INDEPENDENTLY_EVALUATED
```

---

# 87. Counterexample Example

If:

```text
delegation chain attack = SUCCESS
```

then:

```text
ASSURANCE
→
REASSESSMENT_REQUIRED
```

or:

```text
REFUTED
```

depending on whether the claim was universal and whether the counterexample directly violates it.

---

# 88. Unknown Example

If:

```text
no delegation chaining tests
```

then:

```text
delegation chaining = UNKNOWN
```

not:

```text
PASS
```

---

# 89. Contradiction Example

If:

```text
deterministic checker = PASS
independent red-team test = FAIL
```

then:

```text
CONFLICT
→
REVIEW_REQUIRED
```

The system should preserve both results.

---

# 90. Assurance Computation Pipeline

```text
LOAD CLAIM
 ↓
LOAD PROOF OBLIGATIONS
 ↓
LOAD CURRENT IMPLEMENTATION
 ↓
LOAD EVIDENCE
 ↓
VALIDATE EVIDENCE
 ↓
CHECK FRESHNESS
 ↓
CHECK ASSUMPTIONS
 ↓
CHECK COUNTEREXAMPLES
 ↓
CHECK INDEPENDENCE
 ↓
EVALUATE RULES
 ↓
DERIVE STATUS
 ↓
GENERATE LIMITATIONS
 ↓
GENERATE GAPS
 ↓
WRITE LEDGER EVENT
```

---

# 91. No Hidden Computation

Every derived assurance state must identify:

```text
inputs
rules
version
result
```

A black-box assurance score is unacceptable for critical claims.

---

# 92. Assurance Recalculation

Recalculate when:

```text
new evidence
counterexample
implementation change
dependency change
rule change
expiration
security change
```

---

# 93. Incremental Recalculation

The system should avoid recomputing unrelated claims.

Use the assurance graph to determine:

```text
affected subgraph
```

and recalculate only what is necessary.

---

# 94. Full Recalculation

A full recomputation must remain possible for:

```text
audit
migration
rule changes
graph repair
major releases
```

---

# 95. Computation Audit

The system should preserve:

```text
computation_id
rule_set
input hashes
output
```

so that an assurance result can be reproduced.

---

# 96. Critical Invariants

### Invariant 1

Unknown is never silently treated as pass.

### Invariant 2

Contradictory evidence is never silently averaged away.

### Invariant 3

A confirmed critical counterexample cannot increase assurance.

### Invariant 4

Invalid critical evidence cannot support assurance.

### Invariant 5

Stale evidence cannot silently establish current assurance.

### Invariant 6

Independence must be represented separately from evidence quantity.

### Invariant 7

Assurance computation rules must be versioned.

### Invariant 8

Assurance results must be explainable from explicit inputs and rules.

### Invariant 9

Assurance does not grant authority.

### Invariant 10

High-risk claims require stronger verification than low-risk claims.

### Invariant 11

Irreversible actions require stronger assurance than reversible actions where policy requires it.

### Invariant 12

Assurance computation must preserve historical states.

### Invariant 13

The strongest assurance statement cannot exceed the evidence supporting it.

### Invariant 14

Adding irrelevant evidence must not alter a claim's assurance.

### Invariant 15

Removing required evidence cannot increase assurance.

### Invariant 16

The assurance engine itself requires verification.

---

# 97. Exit Criteria

- [x] Assurance computation model defined
- [x] No-unjustified-probability principle defined
- [x] Assurance state space defined
- [x] Orthogonal assurance dimensions defined
- [x] Proof-obligation satisfaction states defined
- [x] Evidence classification defined
- [x] Evidence validity/integrity/freshness defined
- [x] Evidence scope and relevance defined
- [x] Independence profile defined
- [x] Correlated evidence semantics defined
- [x] Contradictory evidence semantics defined
- [x] Partial evidence defined
- [x] Required/conditional/supporting obligations defined
- [x] Assumption validity defined
- [x] Counterexample semantics defined
- [x] Universal-claim caution defined
- [x] Bounded claims defined
- [x] Assurance scope defined
- [x] Conservative aggregation defined
- [x] Unknown state defined
- [x] Three-valued logic defined
- [x] Contradictory-state extension considered
- [x] Candidate assurance rules defined
- [x] Promotion/demotion/restoration defined
- [x] Risk-adjusted requirements defined
- [x] Reversibility and authority sensitivity defined
- [x] Decision semantics defined
- [x] Assurance/authority separation defined
- [x] Aggregation strategies defined
- [x] Evidence redundancy defined
- [x] Judge disagreement/adjudication defined
- [x] Non-monotonic assurance defined
- [x] Belief revision defined
- [x] Assurance rule versioning defined
- [x] Computation record defined
- [x] Explainability and counterfactual explanation defined
- [x] Assurance-gap generation defined
- [x] Release/governance boundary defined
- [x] Assurance engine failure modes defined
- [x] Assurance engine verification defined
- [x] Metamorphic properties defined
- [x] Conservative semantics defined
- [x] Assurance computation pipeline defined
- [x] Incremental/full recalculation defined
- [x] Computation audit defined
- [x] Core invariants defined

**Current assessment:** IV-011 establishes the semantics for deriving bounded assurance from evidence without turning incomplete, correlated, stale, or contradictory evidence into unjustified certainty. The assurance engine is explicitly treated as a governed reasoning component whose own computation must be versioned, explainable, reproducible, and testable.

---

# 98. Next Document

**IV-012 — Assurance-Gated Execution, Release & Governance Control Specification**

IV-012 should connect assurance computation to actual system behavior.

It should define:

```text
assurance gates
execution gates
release gates
authority gates
security gates
human approval gates
emergency paths
degraded modes
assurance failure handling
rollback
recovery
release blocking
governance escalation
```

The central question will be:

```text
HOW DOES VERIFIED KNOWLEDGE
ACTUALLY CONSTRAIN WHAT THE SYSTEM IS ALLOWED TO DO?
```

The key distinction must remain:

```text
ASSURANCE
→
INFORMS / GATES DECISIONS

ASSURANCE
≠
AUTHORITY
```

This will connect the epistemic architecture to the operational control plane.
