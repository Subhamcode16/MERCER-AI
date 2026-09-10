# IV-006 — Evidence, Verification, Self-Critique & Adversarial Self-Verification Architecture

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-002, IV-003, IV-004, IV-005, III-004, III-009, III-010, III-012, III-013, III-015

---

## 1. Purpose

IV-006 defines how the architecture moves from:

```text
CLAIM
 ↓
PROOF OBLIGATION
 ↓
TEST / OBSERVATION
 ↓
EVIDENCE
 ↓
VERIFICATION
 ↓
ADVERSARIAL ATTACK
 ↓
INDEPENDENCE ANALYSIS
 ↓
ASSURANCE
```

The central rule is:

```text
SELF-CRITIQUE
≠
PROOF

NO COUNTEREXAMPLE FOUND
≠
UNIVERSAL CORRECTNESS

MODEL CONFIDENCE
≠
ASSURANCE
```

The purpose of verification is to reduce uncertainty about a **bounded claim**, not to manufacture certainty by assertion.

---

# 2. Source Basis

This document builds on the Phase III contracts and the completed IV-002 through IV-005 analysis.

Relevant contracts include:

```text
III-004 — Provenance, Lineage & Evidence Trace
III-009 — Evaluation, Self-Critique & Adversarial Verification
III-010 — Provenance-Aware Memory, Evidence & Retrieval Integrity
III-012 — Security, Isolation & Adversarial Runtime
III-013 — Learning, Adaptation, Self-Modification & Behavioral Stability
III-015 — System-Wide Intelligence Assurance, Evaluation & Proof
```

III-015 establishes the distinction:

```text
DESIGNED
≠
IMPLEMENTED
≠
TESTED
≠
VERIFIED
≠
VALIDATED
≠
PROVEN
```

The engineering implementation also already preserves structured conflict, provenance, evaluator identity, evidence references, and escalation information. These are implementation evidence, not substitutes for the normative contracts. fileciteturn16file0L19-L45

---

# 3. Claim Taxonomy

Every important assurance claim should identify its type.

Candidate types:

```text
STRUCTURAL
BEHAVIORAL
SECURITY
AUTHORITY
PROVENANCE
PERFORMANCE
ROBUSTNESS
SAFETY
ALIGNMENT
LIFECYCLE
RECOVERY
ASSURANCE
```

A claim without a scope is not sufficiently specified.

For example:

```text
"the verifier is reliable"
```

is inadequate.

A bounded claim is:

```text
"under threat model T, protocol P, and failure set F,
the verifier detected X% of seeded failures."
```

---

# 4. Proof Obligation

Every critical claim should generate a proof obligation:

```yaml
proof_obligation:
  obligation_id: ...
  claim_ref: ...
  property: ...
  acceptance_condition: ...
  evidence_required: []
  falsification_conditions: []
```

The obligation answers:

```text
WHAT WOULD COUNT AS EVIDENCE?
WHAT WOULD FALSIFY THE CLAIM?
```

---

# 5. What "Proof" Means

Three categories must remain separate:

```text
FORMAL PROOF
EMPIRICAL EVIDENCE
ASSURANCE ARGUMENT
```

### Formal proof

A property follows from an explicit formal system.

### Empirical evidence

A property is supported by controlled testing, measurement, observation, or experimentation.

### Assurance argument

Multiple bounded evidence sources collectively support a claim.

A successful empirical test must not be relabeled as formal proof.

---

# 6. Bounded Assurance

Many system properties cannot legitimately be claimed universally.

Therefore use claims such as:

```text
VERIFIED UNDER PROTOCOL P
FOR VERSION V
WITHIN ENVIRONMENT E
UNDER THREAT MODEL T
```

rather than unsupported claims such as:

```text
UNIVERSALLY SAFE
ALWAYS CORRECT
IMPOSSIBLE TO BREAK
```

---

# 7. Evidence Taxonomy

Candidate evidence classes:

```text
SOURCE EVIDENCE
RUNTIME EVIDENCE
TEST EVIDENCE
EVALUATION EVIDENCE
SECURITY EVIDENCE
PROVENANCE EVIDENCE
COUNTEREXAMPLE EVIDENCE
HUMAN REVIEW
FORMAL PROOF
STATISTICAL EVIDENCE
REGRESSION EVIDENCE
RECOVERY EVIDENCE
```

Evidence must preserve source, version, protocol, timestamp, producer/evaluator, and provenance where applicable.

---

# 8. Evidence Is Not Truth

A core invariant is:

```text
EVIDENCE
≠
TRUTH
```

Evidence must itself be evaluated for:

```text
integrity
relevance
validity
sufficiency
independence
freshness
provenance
```

Perfect provenance does not make a false claim true.

---

# 9. Verification vs Validation

Verification asks:

```text
DID WE IMPLEMENT THE SPECIFICATION CORRECTLY?
```

Validation asks:

```text
DOES THE RESULT ACTUALLY SERVE
THE INTENDED PURPOSE?
```

These remain separate.

A system can be correctly implemented and still fail its intended purpose.

---

# 10. Self-Critique

Self-critique evaluates a system's own:

```text
output
plan
decision
reasoning
assumptions
constraints
```

Conceptually:

```text
PRODUCER
 ↓
SELF-CRITIC
 ↓
CRITIQUE ARTIFACT
 ↓
REVISION / ESCALATION
```

The critic should produce a governed artifact rather than silently mutate the original result.

---

# 11. Self-Critique Limitation

The central limitation is:

```text
THE SYSTEM THAT PRODUCED AN ERROR
MAY ALSO PRODUCE A CRITIQUE THAT
FAILS TO DETECT THAT ERROR.
```

Potential correlated failures include:

```text
shared model failure
shared representation
shared data
shared prompt
shared evidence
shared assumptions
confirmation bias
reward hacking
blind spots
```

Therefore self-critique is evidence, not proof.

---

# 12. Self-Critique Contract

Conceptually:

```yaml
self_critique:
  critique_id: ...
  target_ref: ...
  target_version: ...
  critic_ref: ...
  criteria_refs: []
  detected_issues: []
  evidence_refs: []
  confidence: ...
  recommendation: ...
  provenance_ref: ...
```

The original target must remain reconstructable.

---

# 13. Self-Critique Metrics

Measure:

```text
error detection rate
false-negative rate
false-positive rate
error localization
correction success
regression rate
false reassurance
```

Seed known errors and evaluate detection performance.

---

# 14. Adversarial Self-Verification

The adversarial verifier has a different objective:

```text
SELF-CRITIQUE:
"What might be wrong?"

ADVERSARIAL VERIFICATION:
"How can I break this?"
```

Conceptually:

```text
CLAIM
 ↓
ATTACK GENERATION
 ↓
COUNTEREXAMPLE SEARCH
 ↓
FAILURE / NO FAILURE
```

The verifier should optimize for finding counterexamples, not confirming the producer.

---

# 15. Adversarial Verifier Contract

Conceptually:

```yaml
adversarial_verification:
  verification_id: ...
  target_ref: ...
  target_version: ...
  threat_model_ref: ...
  attack_strategy_refs: []
  attempts: []
  counterexamples: []
  uncovered_regions: []
  conclusion: ...
  provenance_ref: ...
```

All attempted attacks should remain auditable.

---

# 16. No Counterexample Is Not Proof

A verifier reporting:

```text
NO COUNTEREXAMPLE FOUND
```

means only:

```text
NO COUNTEREXAMPLE WAS FOUND
WITHIN THE TESTED SEARCH SPACE.
```

It does not establish:

```text
COUNTEREXAMPLES DO NOT EXIST.
```

---

# 17. Counterexamples as First-Class Evidence

A counterexample should preserve:

```text
target
version
initial state
input
attack strategy
expected behavior
observed behavior
failure condition
reproduction
severity
provenance
```

Material counterexamples should become regression tests.

---

# 18. Adversarial Loop

The preferred loop is:

```text
CLAIM
 ↓
ATTACK
 ↓
COUNTEREXAMPLE?
 ├─ YES → RECORD → CONTAIN → FIX → REGRESSION → REVERIFY
 └─ NO  → EXPAND ATTACK SPACE → REPEAT
```

The loop should not terminate merely because one attack passed.

---

# 19. Threat-Model Binding

Adversarial verification must identify:

```text
attacker capability
attacker knowledge
attacker resources
attack surface
protected assets
failure objective
assumptions
```

Without a threat model:

```text
"we adversarially tested it"
```

is incomplete.

---

# 20. Verification Independence

Independence is multidimensional:

```text
MODEL
PROMPT
DATA
IMPLEMENTATION
EVALUATOR
RUNTIME
THREAT MODEL
EVIDENCE
```

Therefore independence should not be represented only as:

```text
independent = true
```

A verification record should preserve the relevant independence dimensions.

---

# 21. Correlated Verification Failure

This configuration:

```text
PRODUCER = MODEL A
CRITIC = MODEL A
ADVERSARY = MODEL A
```

with:

```text
same context
same evidence
same prompt structure
same failure distribution
```

may produce:

```text
3 agreeing outputs
```

that actually represent:

```text
1 correlated failure mode.
```

Therefore:

```text
3 agents
≠
3 independent verifiers
```

---

# 22. Capability Asymmetry

A critical research concern is:

```text
PRODUCER CAPABILITY
>
VERIFIER CAPABILITY
```

If the producer can generate failures the verifier cannot detect, a verifier pass may provide weak assurance.

Therefore measure:

```text
producer failure-generation capability
verifier failure-detection capability
false-negative rate
attack coverage
```

Do not assume the verifier is stronger.

---

# 23. Capability-Matched Verification

Where appropriate, combine:

```text
stronger model
diverse model
deterministic checker
formal checker
independent evaluator
human reviewer
```

The objective is not model count.

The objective is reduction of correlated failure.

---

# 24. Deterministic Verification

Properties that can be checked deterministically should preferentially use deterministic mechanisms.

Examples:

```text
schema validity
authority scope
expiration
revocation
version binding
required fields
state-transition legality
cryptographic integrity
resource limits
policy predicates
```

LLMs should not be the only verifier for deterministic properties.

---

# 25. Semantic Verification

LLM-based or human verification is more appropriate for:

```text
semantic consistency
ambiguous language
missing assumptions
reasoning quality
goal consistency
qualitative critique
adversarial interpretation
```

These remain probabilistic and require empirical evaluation.

---

# 26. Hybrid Verification Architecture

Preferred architecture:

```text
                 PRODUCER
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
   DETERMINISTIC          SEMANTIC
     CHECKERS             VERIFIERS
          ↓                   ↓
          └─────────┬─────────┘
                    ↓
           ADVERSARIAL TESTING
                    ↓
          INDEPENDENT EVALUATION
                    ↓
             ASSURANCE ENGINE
```

No single component certifies the entire system.

---

# 27. Authority Verification

IV-006 must turn object authority from a design assertion into a measurable property.

For every authority-bearing object evaluate:

```text
identity
issuer
subject
scope
target
constraints
expiration
revocation
provenance
version
execution effect
```

---

# 28. Authority Proof Obligation

Example claim:

```text
A delegatee cannot execute outside its delegated scope.
```

Proof obligations:

```text
P1 — delegation scope is represented
P2 — target action scope is represented
P3 — scope comparison is enforceable
P4 — enforcement occurs before execution
P5 — revocation propagates
P6 — expiration propagates
P7 — adversarial escalation fails
P8 — evidence is reconstructable
```

---

# 29. Authority Falsification

Attempt:

```text
scope expansion
scope confusion
identifier collision
version confusion
expired delegation
revoked delegation
transitive escalation
tool-mediated escalation
cross-agent escalation
human-mediated escalation
```

A successful bypass is a direct assurance failure.

---

# 30. Object Authority Evidence Chain

For a consequential authority object, reconstruct:

```text
WHO CREATED IT?
 ↓
UNDER WHICH AUTHORITY?
 ↓
FOR WHAT SCOPE?
 ↓
UNDER WHICH POLICY?
 ↓
WITH WHICH CONSTRAINTS?
 ↓
FOR HOW LONG?
 ↓
WAS IT REVOKED?
 ↓
WHAT DID IT AUTHORIZE?
 ↓
WHAT EXECUTION RESULTED?
```

This connects identity, authority, provenance, delegation, security, execution, and assurance.

---

# 31. Authority Verification Matrix

| Property | Preferred verification |
|---|---|
| identity | deterministic |
| issuer | authority/provenance check |
| scope | deterministic predicate |
| expiration | deterministic |
| revocation | deterministic state |
| delegation containment | graph check |
| policy applicability | policy engine |
| execution binding | relational validation |
| provenance | lineage verification |
| abuse resistance | adversarial testing |
| semantic intent | semantic evaluation |
| emergency use | specialized governance test |

---

# 32. Verification Layers

Candidate layers:

```text
L0 — TYPE / SCHEMA
L1 — DETERMINISTIC INVARIANTS
L2 — RELATIONAL CONSISTENCY
L3 — SECURITY ENFORCEMENT
L4 — SELF-CRITIQUE
L5 — ADVERSARIAL VERIFICATION
L6 — INDEPENDENT EVALUATION
L7 — HUMAN REVIEW
L8 — SYSTEM-WIDE ASSURANCE
```

Critical claims may require multiple layers.

---

# 33. Candidate Assurance Levels

A candidate vocabulary:

```text
A0 — UNASSESSED
A1 — OBSERVED
A2 — TESTED
A3 — VERIFIED
A4 — ADVERSARIALLY VERIFIED
A5 — INDEPENDENTLY EVALUATED
A6 — ASSURANCE ARGUMENT COMPLETE
A7 — FORMALLY PROVEN
```

These labels are proposed, not yet normative.

Passing more tests does not automatically promote a claim to a higher assurance level.

---

# 34. Self-Critique Benchmark

Construct seeded errors and measure:

```text
precision
recall
false negatives
false positives
error localization
correction success
regression
false reassurance
```

Compare against:

```text
no critique baseline
```

to determine whether self-critique provides measurable benefit.

---

# 35. Adversarial Verification Benchmark

Seed failures across:

```text
authority bypass
constraint bypass
provenance break
state-machine violation
stale evidence
approval mismatch
delegation escalation
security race
self-modification bypass
prompt injection
tool-output manipulation
```

Measure:

```text
attack coverage
counterexample discovery
time to detection
severity-weighted recall
false-negative rate
```

---

# 36. Hidden Failure Set

Use:

```text
development failure set
+
held-out failure set
```

Do not expose all failures to the verifier.

This helps distinguish genuine generalization from memorization.

---

# 37. Adaptive Adversarial Testing

When a verifier learns to catch an attack:

```text
ATTACK A
```

generate variants:

```text
A1
A2
A3
A4
```

to test whether it learned:

```text
the vulnerability class
```

rather than:

```text
the exact example.
```

---

# 38. Metamorphic Verification

Use transformations where expected relationships are known.

Example:

```text
change irrelevant metadata
→ authorization should remain unchanged
```

while:

```text
change authority scope
→ authorization should change
```

This provides testable invariants without requiring a known output for every possible input.

---

# 39. Differential Verification

Run multiple mechanisms:

```text
Verifier A
Verifier B
Deterministic checker
Independent evaluator
```

Disagreement must trigger analysis.

Do not use simple majority voting as proof.

---

# 40. Disagreement as Evidence

Preferred flow:

```text
VERIFIER DISAGREEMENT
 ↓
CLASSIFY
 ↓
ANALYZE
 ↓
REVALIDATE / ESCALATE
```

not:

```text
3 votes vs 1 vote
→ truth
```

The existing engineering pattern already escalates unresolved mandatory conflicts rather than silently selecting a winner. fileciteturn16file0L19-L45

---

# 41. Common-Mode Failure

Track common dependencies:

```text
model lineage
data lineage
prompt lineage
evidence lineage
tool lineage
runtime lineage
policy lineage
```

High agreement with high commonality should not be interpreted as strong independence.

---

# 42. Evidence Independence

Evidence itself can be correlated.

For example:

```text
Verifier A
Verifier B
Verifier C
```

all using the same retrieved source do not provide three independent evidence bases.

Therefore preserve:

```text
evidence lineage
evidence overlap
source identity
transformation lineage
```

---

# 43. Human Verification

Human review is also not automatically independent.

Record:

```text
reviewer
criteria
evidence set
scope
decision
limitations
```

Reviewers may share the same evidence and assumptions.

---

# 44. Assurance Separation

The assurance engine should receive:

```text
claim
proof obligation
evidence
verification results
adversarial results
independence metadata
known failures
limitations
```

It should not receive only:

```text
producer_confidence
```

---

# 45. Confidence Is Not Assurance

A model output such as:

```text
confidence = 0.99
```

does not establish:

```text
assurance = 0.99
```

Confidence may be an input signal, but the assurance decision requires evidence.

---

# 46. Self-Reported Verification

A statement:

```text
"I verified this."
```

is not sufficient verification evidence.

A verification artifact should preserve:

```text
protocol
checks
results
evidence
limitations
provenance
```

---

# 47. Proof-Carrying Decision

For consequential decisions, target:

```text
DECISION
+
EVIDENCE / ASSURANCE PACKAGE
```

The package should answer:

```text
what was decided
why
under which authority
using which evidence
under which constraints
which checks passed
which attacks were attempted
what failed
what remains uncertain
```

---

# 48. Assurance Package

Conceptually:

```yaml
assurance_package:
  claim_ref: ...
  subject_ref: ...
  target_version: ...
  evidence_refs: []
  verification_refs: []
  adversarial_refs: []
  independence_assessment: ...
  known_failures: []
  assumptions: []
  limitations: []
  assurance_level: ...
  decision: ...
  provenance_ref: ...
```

---

# 49. Assurance Outcomes

Candidate outcomes:

```text
SUPPORTED
PARTIALLY_SUPPORTED
UNSUPPORTED
REFUTED
INCONCLUSIVE
REQUIRES_REVIEW
REQUIRES_REASSESSMENT
```

`INCONCLUSIVE` must remain a valid result.

The system must be allowed to say:

```text
WE DO NOT KNOW
```

---

# 50. Falsification Priority

Verification should prioritize tests capable of disproving the claim.

Conceptually:

```text
CLAIM
 ↓
MOST DANGEROUS COUNTEREXAMPLE
 ↓
ATTACK
```

This is more valuable than producing large quantities of low-risk tests.

---

# 51. Risk-Weighted Verification

Verification strength should consider:

```text
impact
likelihood
uncertainty
attackability
irreversibility
authority scope
```

High-impact authority and execution claims require stronger evidence.

---

# 52. Verification of the Verifier

The verifier itself is a system component.

Therefore:

```text
TARGET
 ↓
VERIFIER
```

must be complemented by:

```text
VERIFIER
 ↓
VERIFIER EVALUATION
```

Ask:

```text
What failures does it miss?
What false alarms does it generate?
Can it be manipulated?
Does it overfit?
Does it share producer blind spots?
```

---

# 53. Adversarial Testing of the Verifier

Attack the verifier with:

```text
deceptive outputs
adversarial formatting
hidden constraints
ambiguous evidence
prompt injection
confidence manipulation
evidence poisoning
counterexample camouflage
long-context dilution
tool-output manipulation
```

The verifier's own failure modes must enter the assurance record.

---

# 54. Bounded Verification Recursion

Do not create infinite:

```text
verify verifier
verify verifier of verifier
...
```

Instead define a bounded assurance architecture:

```text
verifier benchmark
+
held-out failures
+
independent evaluation
+
deterministic checks
```

and declare the resulting assurance boundary explicitly.

---

# 55. Self-Verification Cannot Establish Universal Correctness

The architecture must explicitly reject:

```text
SELF-VERIFICATION
→
UNIVERSAL CORRECTNESS
```

A system can generate evidence about itself.

It cannot establish that the evidence-generating mechanism is universally reliable merely because it generated the evidence.

---

# 56. Capability-Dominance Experiment

Construct increasingly difficult failures:

```text
producer difficulty ↑
```

and measure:

```text
verifier detection rate
```

The important curve is:

```text
producer capability
        vs
verifier detection capability
```

If detection collapses as producer capability rises, the verification mechanism cannot be treated as strong assurance without additional independent mechanisms.

---

# 57. Red-Team / Blue-Team Model

Candidate operational pattern:

```text
BLUE TEAM
producer + normal verification

RED TEAM
adversarial generator

JUDGE
independent evaluator / deterministic checks
```

The red team attempts to break the claim.

The judge determines whether the discovered failure is real.

---

# 58. Regression Assurance

Every material counterexample should be classified:

```text
NEW FAILURE
KNOWN FAILURE
REGRESSION
NON-REPRODUCIBLE
FALSE POSITIVE
```

Fixed failures should become regression tests where appropriate.

---

# 59. Assurance History

Assurance must be versioned.

Preserve:

```text
target version
evidence set
verification protocol
verification result
adversarial results
known failures
limitations
assurance decision
```

Thus:

```text
ASSURANCE AT T1
```

can be distinguished from:

```text
ASSURANCE AT T2
```

after system change.

---

# 60. Assurance Revocation

If supporting evidence becomes invalid:

```text
EVIDENCE INVALIDATED
 ↓
ASSURANCE DEPENDENCY CHECK
 ↓
REVOKE / REASSESS
```

This inherits the dependency and lifecycle model of IV-003 and IV-005.

---

# 61. Self-Modification

Before deploying a material self-modification:

```text
CHANGE
 ↓
AUTHORIZATION
 ↓
VERIFICATION
 ↓
ADVERSARIAL ATTACK
 ↓
INDEPENDENT EVALUATION
 ↓
ASSURANCE UPDATE
 ↓
DEPLOYMENT
```

A protected self-modification must not be able to:

```text
produce
+
solely approve
+
solely verify
+
deploy
```

itself.

---

# 62. Separation of Duties

For high-impact claims:

```text
PRODUCER
≠
SOLE CRITIC
≠
SOLE ADVERSARY
≠
SOLE ASSURANCE DECIDER
```

Where reuse is unavoidable, correlation must be recorded as an assurance limitation.

---

# 63. Failure Handling

When verification discovers a failure:

```text
DETECT
 ↓
RECORD
 ↓
CLASSIFY
 ↓
CONTAIN
 ↓
REPRODUCE
 ↓
REPAIR
 ↓
REGRESSION TEST
 ↓
REVERIFY
 ↓
REASSESS ASSURANCE
```

The original failure remains evidence.

---

# 64. Assurance State Machine

Conceptually:

```text
UNASSESSED
    ↓
EVIDENCE_COLLECTED
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

Any material:

```text
new failure
evidence invalidation
target change
protocol change
security change
```

can produce:

```text
REASSESSMENT_REQUIRED
```

---

# 65. False Reassurance

A critical metric is:

```text
FALSE_REASSURANCE_RATE
```

Defined as:

```text
fraction of materially flawed cases
incorrectly accepted by the verification stack.
```

For this architecture, reducing false reassurance is generally more important than maximizing the number of critiques.

---

# 66. Required Metrics

At minimum:

```text
error detection rate
false-negative rate
false-positive rate
counterexample discovery rate
correction success
regression rate
verification latency
evidence coverage
claim coverage
independence indicators
correlated failure rate
authority bypass rate
security bypass rate
assurance revocation rate
false reassurance rate
```

---

# 67. Statistical Claims

Probabilistic claims should preserve:

```text
sample size
test population
sampling method
failure count
protocol
confidence interval where appropriate
```

A percentage without methodology is insufficient.

---

# 68. Distribution Shift

Evidence collected under:

```text
D1
```

does not automatically establish behavior under:

```text
D2
```

Verification should therefore include, where relevant:

```text
edge cases
novel inputs
distribution shifts
compositional cases
out-of-distribution cases
```

---

# 69. Evaluation Leakage

Protect against:

```text
test-set leakage
attack-set memorization
benchmark-specific optimization
verifier exposure to hidden answers
```

Otherwise measured assurance may be inflated.

---

# 70. Benchmark Gaming

Test for:

```text
metric gaming
reward hacking
evaluation overfitting
proxy optimization
```

This is especially important for adaptive systems.

---

# 71. Architecture-Level Proof Obligations

Candidate obligations:

```text
PO-001 — Object identity integrity
PO-002 — Authority containment
PO-003 — Delegation containment
PO-004 — Constraint enforcement
PO-005 — Security boundary non-bypass
PO-006 — Execution-intent containment
PO-007 — Provenance preservation
PO-008 — Lifecycle consistency
PO-009 — Revocation propagation
PO-010 — Approval binding
PO-011 — Self-critique effectiveness
PO-012 — Adversarial verification effectiveness
PO-013 — Verification independence
PO-014 — Self-modification governance
PO-015 — Assurance invalidation
PO-016 — Recovery authorization
PO-017 — Evidence integrity
PO-018 — Decision reconstruction
```

These must eventually map to implementation tests and evidence.

---

# 72. Proof Coverage Matrix

| Claim | Proof obligation | Evidence | Verification | Adversarial | Independent | Status |
|---|---|---|---|---|---|---|
| Authority containment | bounded delegation | required | deterministic | required | required | OPEN |
| Execution boundary | no bypass | required | runtime | required | required | OPEN |
| Provenance integrity | lineage preserved | required | deterministic | required | optional | OPEN |
| Self-critique usefulness | seeded-error detection | benchmark | empirical | required | required | OPEN |
| Adversarial verifier usefulness | hidden-failure discovery | benchmark | empirical | required | required | OPEN |
| Assurance applicability | version/evidence binding | ledger | relational | required | required | OPEN |

`OPEN` means the property is specified but not yet empirically demonstrated.

---

# 73. Strong vs Weak Evidence

### Stronger evidence

```text
formal invariant
+
deterministic enforcement
+
positive tests
+
negative tests
+
adversarial tests
+
independent evaluation
+
regression history
```

### Weaker evidence

```text
single demo
model confidence
self-reported correctness
single benchmark
manual inspection
absence of observed failures
```

Weak evidence may contribute to an assurance argument but should not carry critical claims alone.

---

# 74. What We Can Legitimately Claim

After implementation and evidence collection, bounded claims may include:

```text
"Delegation scope is enforced for the tested authority classes."

"The runtime rejects execution after revocation for the tested paths."

"The adversarial verifier detected X% of seeded failures under protocol P."

"The verification stack detected failures missed by self-critique."

"The assurance package is invalidated when specified supporting evidence is revoked."
```

These are scoped, measurable claims.

---

# 75. What We Must Not Claim Without Stronger Basis

Do not claim:

```text
universally safe
universally correct
self-critique proves correctness
adversarial verification cannot be fooled
agent agreement proves truth
no counterexample proves correctness
benchmark success proves general safety
confidence proves correctness
```

unless a stronger formal and empirical basis genuinely exists.

---

# 76. Assurance Language Standard

Preferred:

```text
SUPPORTED WITHIN SCOPE
EVIDENCE INDICATES
VERIFIED UNDER PROTOCOL P
NO COUNTEREXAMPLE FOUND UNDER TEST SET T
INDEPENDENT EVALUATION SUPPORTS
ASSURANCE REQUIRES REASSESSMENT AFTER CHANGE
```

Avoid unsupported absolute language.

---

# 77. Evidence Ledger

Conceptual structure:

```yaml
evidence_record:
  evidence_id: ...
  type: ...
  source_ref: ...
  target_ref: ...
  target_version: ...
  protocol_ref: ...
  produced_at: ...
  integrity_ref: ...
  provenance_ref: ...
  evaluator_ref: ...
  limitations: []
```

---

# 78. Verification Ledger

```yaml
verification_record:
  verification_id: ...
  target_ref: ...
  target_version: ...
  claim_ref: ...
  verifier_ref: ...
  protocol_ref: ...
  evidence_refs: []
  result: ...
  counterexamples: []
  independence_metadata: ...
  limitations: []
  provenance_ref: ...
```

---

# 79. Counterexample Ledger

```yaml
counterexample:
  counterexample_id: ...
  target_ref: ...
  target_version: ...
  attack_ref: ...
  observed_failure: ...
  expected_behavior: ...
  reproduction: ...
  severity: ...
  evidence_refs: []
  regression_status: ...
```

---

# 80. Assurance Ledger

```yaml
assurance_record:
  assurance_id: ...
  claim_ref: ...
  target_ref: ...
  target_version: ...
  evidence_refs: []
  verification_refs: []
  adversarial_refs: []
  independence_assessment: ...
  assurance_level: ...
  limitations: []
  decision: ...
  created_at: ...
```

---

# 81. End-to-End Assurance Loop

The target architecture is:

```text
CLAIM
 ↓
PROOF OBLIGATION
 ↓
TEST DESIGN
 ↓
EVIDENCE
 ↓
DETERMINISTIC VERIFICATION
 ↓
SELF-CRITIQUE
 ↓
ADVERSARIAL VERIFICATION
 ↓
INDEPENDENT EVALUATION
 ↓
ASSURANCE ARGUMENT
 ↓
ASSURANCE DECISION
 ↓
MONITORING
 ↓
NEW EVIDENCE
 ↓
REASSESSMENT
```

This makes assurance continuous rather than one-time.

---

# 82. Falsification of the Assurance System

The assurance mechanism itself must be attacked.

Attempt:

```text
producer stronger than verifier
correlated verifier failures
evidence poisoning
hidden counterexamples
target-version confusion
evaluation-protocol changes
supporting-evidence invalidation
confidence manipulation
evaluator disagreement
self-critique false reassurance
adversarial-verifier blind spots
independent-review bypass
```

A verification system that cannot survive attacks against itself must not be treated as strong assurance.

---

# 83. Research Hypotheses

The implementation should test:

### H1
Self-critique improves error detection relative to no critique.

### H2
Self-critique does not detect all producer failures.

### H3
Adversarial generation discovers failures missed by self-critique.

### H4
Independent verification reduces correlated false reassurance.

### H5
Deterministic checks outperform LLM evaluation for deterministic properties.

### H6
Verification effectiveness decreases when producer capability substantially exceeds verifier capability.

### H7
Diverse verification mechanisms reduce common-mode failure.

### H8
Counterexample-driven regression improves assurance over static benchmarking.

These are hypotheses, not established facts.

---

# 84. Experimental Design

For each hypothesis:

```text
BASELINE
 ↓
CONTROL
 ↓
INTERVENTION
 ↓
HELD-OUT TEST
 ↓
ANALYSIS
 ↓
REPLICATION
```

A single successful experiment does not establish a universal property.

---

# 85. Critical Architectural Principle

The strongest conclusion of IV-006 is:

```text
THE PURPOSE OF VERIFICATION
IS NOT TO CONFIRM THE SYSTEM.

THE PURPOSE OF VERIFICATION
IS TO REDUCE UNCERTAINTY ABOUT
A BOUNDED CLAIM.
```

And:

```text
THE PURPOSE OF ADVERSARIAL VERIFICATION
IS TO INCREASE THE CHANCE THAT
A FALSE CLAIM IS EXPOSED.
```

This makes falsification a first-class architectural capability.

---

# 86. Exit Criteria

- [x] Claim taxonomy defined
- [x] Proof obligations defined
- [x] Formal proof distinguished from empirical evidence
- [x] Bounded assurance defined
- [x] Evidence taxonomy defined
- [x] Evidence traceability defined
- [x] Evidence distinguished from truth
- [x] Verification distinguished from validation
- [x] Self-critique defined
- [x] Self-critique limitations defined
- [x] Self-critique metrics defined
- [x] Adversarial verification defined
- [x] Counterexample model defined
- [x] Threat-model binding defined
- [x] Verification independence analyzed
- [x] Correlated failure analyzed
- [x] Capability asymmetry analyzed
- [x] Deterministic verification defined
- [x] Hybrid verification defined
- [x] Object-authority verification defined
- [x] Authority proof obligations defined
- [x] Assurance layers defined
- [x] Candidate assurance levels defined
- [x] Self-critique benchmark defined
- [x] Adversarial benchmark defined
- [x] Hidden failure set defined
- [x] Adaptive testing defined
- [x] Metamorphic verification defined
- [x] Differential verification defined
- [x] Disagreement handling defined
- [x] Verifier evaluation defined
- [x] Assurance history defined
- [x] Assurance revocation defined
- [x] Self-modification verification defined
- [x] Required metrics defined
- [x] False-reassurance metric defined
- [x] Proof obligations mapped
- [x] Permissible assurance language defined
- [x] Falsification of the assurance system defined

**Current assessment:** The architecture now has a concrete path from claims to evidence, deterministic verification, self-critique, adversarial falsification, independent evaluation, and bounded assurance. Self-critique and adversarial self-verification are explicitly treated as measurable verification mechanisms rather than proof-generating oracles.

---

# 87. Next Document

**IV-007 — Coverage, Assurance-Gap & Implementation Verification Matrix**

IV-007 will compile the preceding architecture into an implementation-oriented matrix:

```text
ARCHITECTURAL CLAIM
 ↓
SPECIFICATION
 ↓
IMPLEMENTATION COMPONENT
 ↓
TEST
 ↓
DETERMINISTIC CHECK
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

The purpose is to identify every case where:

```text
DESIGN EXISTS
BUT IMPLEMENTATION DOES NOT

IMPLEMENTATION EXISTS
BUT TEST DOES NOT

TEST EXISTS
BUT INDEPENDENT VERIFICATION DOES NOT

EVIDENCE EXISTS
BUT ASSURANCE ARGUMENT DOES NOT

CLAIM EXISTS
BUT ADEQUATE PROOF OBLIGATION DOES NOT
```

This is the bridge from the specification/validation phase into concrete engineering execution.
