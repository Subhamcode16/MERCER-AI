# III-009 — Evaluation, Self-Critique & Adversarial Verification Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001 through III-008 and the ratified Phase II semantic architecture  
**Purpose:** Define the machine-readable evaluation and verification contract, including evaluation identity, targets, protocols, criteria, metrics, evidence, self-critique, independent critique, adversarial attack, verification independence, failure discovery, regression testing, uncertainty, decision outcomes, evaluator authority, and evaluation provenance.

---

# 1. Purpose

III-009 defines verification as an explicit architectural process rather than an informal second opinion.

The central requirement is:

```text
A SYSTEM MUST NOT CLAIM
THAT IT HAS VERIFIED ITSELF
MERELY BECAUSE IT GENERATED
A SECOND ANSWER ABOUT ITS FIRST ANSWER.
```

Evaluation must therefore specify:

```text
WHAT IS BEING EVALUATED?
WHAT CLAIM IS BEING TESTED?
WHAT PROTOCOL IS USED?
WHAT COUNTS AS PASS?
WHAT COUNTS AS FAILURE?
WHO / WHAT EVALUATES IT?
HOW INDEPENDENT IS THE EVALUATOR?
WHAT EVIDENCE SUPPORTS THE RESULT?
CAN THE RESULT BE REPRODUCED?
```

---

# 2. Evaluation Is a Governed Process

An evaluation is not merely:

```text
score = model_output
```

It is a structured process:

```text
TARGET
 ↓
CLAIM / QUESTION
 ↓
PROTOCOL
 ↓
TEST / EVIDENCE
 ↓
EVALUATOR
 ↓
RESULT
 ↓
INTERPRETATION
 ↓
PROVENANCE
```

---

# 3. Evaluation Identity

Every consequential evaluation should have a unique identifier.

Recommended conceptual form:

```text
EVAL-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

---

# 4. Evaluation Version

The evaluation protocol itself must be versioned.

Therefore:

```text
EVALUATION ID
≠
EVALUATION PROTOCOL VERSION
≠
TARGET VERSION
```

A changed evaluation protocol must not silently rewrite the meaning of historical results.

---

# 5. Evaluation Target

Every evaluation must identify the exact target.

Possible targets:

```text
object
agent
model
decision
plan
execution
knowledge state
memory
constraint
policy
architecture
claim
verification mechanism
```

Target identity and version must be preserved where applicable.

---

# 6. Evaluation Question

Every evaluation should specify what it is attempting to establish.

Examples:

```text
Does the object satisfy schema requirements?
Does the agent obey authority boundaries?
Can the verifier detect known failures?
Does the architecture preserve provenance?
Can the decision survive adversarial perturbation?
```

A vague:

```text
"Is this good?"
```

is insufficient for consequential evaluation.

---

# 7. Evaluation Claim

Where an evaluation supports an architectural claim, the evaluation must reference the corresponding claim.

Conceptually:

```text
CLAIM
 ↓
EVALUATION
 ↓
RESULT
 ↓
EVIDENCE STATUS
```

This connects III-009 to the claim framework introduced earlier.

---

# 8. Evaluation Protocol

A protocol defines:

```text
inputs
procedure
criteria
metrics
thresholds
failure conditions
termination conditions
```

The protocol must be versioned.

---

# 9. Evaluation Dataset / Test Set

Where evaluation uses data or test cases, preserve:

```text
dataset identity
dataset version
test-set identity
test-set version
selection criteria
```

A changing test set must not silently produce an incomparable benchmark.

---

# 10. Test Case Identity

Individual consequential test cases should have stable identifiers.

Recommended conceptual form:

```text
TST-<ULID>
```

A test case should specify:

```text
setup
input
expected property
attack / perturbation where applicable
pass condition
failure condition
```

---

# 11. Evaluation Criteria

Criteria define what constitutes acceptable behavior.

Examples:

```text
correctness
constraint compliance
authority compliance
schema compliance
provenance completeness
robustness
safety
reproducibility
```

Criteria must be explicit rather than inferred from the evaluator's preference.

---

# 12. Metrics

Metrics quantify observed behavior.

Examples:

```text
accuracy
precision
recall
failure discovery rate
false positive rate
false negative rate
coverage
reconstruction success
```

A metric must specify its denominator and measurement scope where necessary.

---

# 13. Metric vs Criterion

A criterion describes:

```text
WHAT MUST BE SATISFIED
```

A metric describes:

```text
HOW PERFORMANCE IS MEASURED
```

Therefore:

```text
METRIC
≠
CRITERION
```

A high metric does not automatically satisfy a criterion unless the protocol explicitly defines the relationship.

---

# 14. Threshold

Where a metric has a required threshold:

```yaml
threshold:
  metric: ...
  operator: >=
  value: ...
```

The threshold must be part of the protocol version.

Changing the threshold changes the evaluation semantics.

---

# 15. Evaluation Result

Conceptually:

```yaml
evaluation_result:
  evaluation_id: EVAL-...
  target_ref: ...
  protocol_ref: ...
  result: PASS
  metrics: []
  evidence_refs: []
  evaluator_ref: ...
  timestamp: ...
```

Possible high-level outcomes:

```text
PASS
FAIL
INCONCLUSIVE
NOT_TESTED
BLOCKED
```

---

# 16. PASS

`PASS` means the target satisfied the defined protocol and criteria for the evaluated scope.

It does not mean:

```text
universally correct
universally safe
free of undiscovered failures
```

---

# 17. FAIL

`FAIL` means the target violated one or more defined evaluation requirements.

A failure should identify:

```text
criterion
test case
observed behavior
expected behavior
evidence
```

---

# 18. INCONCLUSIVE

`INCONCLUSIVE` means the evaluation protocol did not establish either pass or failure.

Examples:

```text
insufficient evidence
unstable environment
incomplete test
ambiguous result
insufficient evaluator independence
```

Inconclusive must not be silently converted into pass.

---

# 19. NOT TESTED

`NOT_TESTED` explicitly indicates that a property was not evaluated.

Absence of a failure does not imply success.

Therefore:

```text
NOT_TESTED
≠
PASS
```

---

# 20. BLOCKED

`BLOCKED` means evaluation could not proceed because a required prerequisite was unavailable.

Examples:

```text
missing dependency
missing authority
missing target
missing dataset
missing tool
```

---

# 21. Evaluation Evidence

Every consequential result should reference the evidence supporting it.

Evidence may include:

```text
test outputs
execution traces
observations
artifacts
counterexamples
human review
independent evaluator results
```

Evidence must preserve provenance.

---

# 22. Evaluation Provenance

Every evaluation should preserve:

```text
target
target version
protocol version
test-set version
evaluator
model / implementation version
configuration
inputs
outputs
evidence
result
timestamp
```

This connects directly to III-004.

---

# 23. Evaluator Identity

Every evaluation must identify the evaluator.

Possible evaluator types:

```text
human
agent
model
programmatic checker
formal verifier
external system
hybrid evaluator
```

Evaluator identity must be explicit.

---

# 24. Evaluator Authority

Evaluation authority must be distinguished from evaluator capability.

Therefore:

```text
CAN_EVALUATE
≠
AUTHORIZED_EVALUATION
```

A system component may technically calculate a metric without being authorized to issue a consequential approval decision.

---

# 25. Self-Critique

Self-critique is an evaluation performed by the producing system or a closely coupled critic against its own output.

Conceptually:

```text
PRODUCER
 ↓
OUTPUT
 ↓
SELF-CRITIC
 ↓
CRITIQUE
```

Self-critique is useful for defect discovery but must not automatically establish independent verification.

---

# 26. Self-Critique Target

A self-critique may target:

```text
reasoning
output
plan
decision
assumptions
evidence usage
constraint compliance
provenance completeness
```

The target version must be fixed.

---

# 27. Self-Critique Output

A critique should preserve:

```yaml
critique:
  critique_id: CRIT-...
  target_ref: ...
  findings: []
  severity: ...
  recommendations: []
  evidence_refs: []
```

Critique is an evidence-producing object, not an automatic state transition.

---

# 28. Self-Critique Limitations

Self-critique may share the producer's:

```text
model
context
training biases
prompt assumptions
knowledge errors
blind spots
```

Therefore it can reproduce the same failure.

This limitation must be treated as a testable hypothesis.

---

# 29. Independent Critique

Independent critique introduces separation between producer and evaluator.

Possible separation dimensions:

```text
different model
different prompt
different context
different implementation
different evaluator
different data
different reasoning path
```

Independence is multidimensional.

---

# 30. Independence Is Not a Binary Label

The system should not simply record:

```text
independent = true
```

without defining the basis.

Instead preserve:

```yaml
independence:
  dimensions:
    model: ...
    prompt: ...
    implementation: ...
    context: ...
    evaluator: ...
    data: ...
  assessment: ...
```

---

# 31. Shared Failure Modes

Two evaluators may appear independent while sharing the same failure mode.

Examples:

```text
same corrupted evidence
same flawed benchmark
same hidden assumption
same model family behavior
same implementation bug
```

Evaluation should therefore test shared failure modes where the claim requires independence.

---

# 32. Adversarial Verification

Adversarial verification explicitly attempts to cause the target to fail.

Conceptually:

```text
TARGET
 ↓
ATTACK GENERATOR
 ↓
ATTACK
 ↓
TARGET RESPONSE
 ↓
VERIFICATION RESULT
```

The objective is:

```text
FIND A COUNTEREXAMPLE
```

rather than merely:

```text
CONFIRM THE EXPECTED RESULT
```

---

# 33. Attack Identity

Every adversarial attack should receive an identifier.

Recommended conceptual form:

```text
ATK-<ULID>
```

The attack record should preserve:

```text
target
target version
attack type
attack parameters
attacker
expected failure
observed result
```

---

# 34. Attack Classes

The initial conceptual attack taxonomy includes:

```text
INPUT PERTURBATION
CONSTRAINT BYPASS
AUTHORITY BYPASS
STALE DATA
CONTEXT POISONING
MEMORY POISONING
PROMPT INJECTION
TOOL INJECTION
VERSION CONFUSION
PROVENANCE TAMPERING
DECISION DRIFT
POLICY CONFLICT
DEPENDENCY FAILURE
RESOURCE EXHAUSTION
ADVERSARIAL EXAMPLE
COUNTERFACTUAL ATTACK
```

The definitive taxonomy remains extensible.

---

# 35. Attack Success

An attack succeeds when it demonstrates a defined failure property.

Examples:

```text
unauthorized action executed
invalid output accepted
constraint bypassed
false claim accepted
provenance lost
stale object consumed
verification incorrectly passes
```

An attack that produces an unexpected output is not automatically a successful attack unless the failure property is established.

---

# 36. Counterexample

A counterexample is a concrete case demonstrating violation of the evaluated property.

Counterexamples should preserve:

```text
input
target version
execution context
expected property
observed failure
```

Counterexamples are high-value evidence for architecture refinement.

---

# 37. Attack Reproducibility

A successful attack should be reproducible where practical.

Preserve:

```text
attack configuration
input
environment
target version
protocol
result
```

This allows regression testing.

---

# 38. Regression Test

A discovered failure should be convertible into a regression test.

Conceptually:

```text
ATTACK
 ↓
FAILURE
 ↓
REGRESSION TEST
 ↓
REPAIR
 ↓
RE-RUN
```

The original failure must remain traceable.

---

# 39. Repair Verification

After a repair:

```text
ORIGINAL FAILURE
+
REGRESSION SUITE
+
NEW ATTACKS
```

must be evaluated.

Passing only the triggering test is insufficient.

---

# 40. Verification Independence

When an architecture claim depends on independent verification, the verification protocol must specify:

```text
what is independent
why it is independent
what shared failure modes remain
how independence is measured
```

Different agent names are not sufficient evidence.

---

# 41. Evaluator Diversity

Where feasible, evaluation should vary:

```text
model
implementation
prompt
data
reasoning strategy
test generator
```

Diversity is a mechanism for reducing correlated evaluator failure.

It is not automatically proof of independence.

---

# 42. Verification Hierarchy

A useful conceptual hierarchy is:

```text
SELF-CHECK
 ↓
SELF-CRITIQUE
 ↓
INDEPENDENT CRITIQUE
 ↓
ADVERSARIAL VERIFICATION
 ↓
INDEPENDENT EVALUATION
 ↓
EXTERNAL / FORMAL VERIFICATION
```

Not every claim requires every level.

The protocol must specify the required verification strength.

---

# 43. Verification Strength

Verification strength should be proportional to claim importance.

Conceptually:

```text
LOW-IMPACT CLAIM
→ basic evaluation

HIGH-IMPACT CLAIM
→ stronger independent / adversarial verification
```

The exact risk-to-verification mapping remains domain-specific.

---

# 44. Verification Coverage

Coverage should measure what has actually been tested.

Possible dimensions:

```text
input space
constraint space
authority space
state space
failure modes
attack classes
decision branches
```

Coverage is evidence of tested scope, not proof outside that scope.

---

# 45. Coverage vs Correctness

A system can have:

```text
HIGH COVERAGE
```

and still be:

```text
INCORRECT
```

Coverage must therefore remain distinct from correctness.

---

# 46. False Pass

A false pass occurs when:

```text
evaluation result = PASS
```

but the target violates the evaluated property.

False passes are especially important for verification systems.

They should be explicitly measured.

---

# 47. False Fail

A false fail occurs when:

```text
evaluation result = FAIL
```

while the target actually satisfies the evaluated property.

False fails affect operational usefulness and should also be measured.

---

# 48. Verification Calibration

Where evaluators produce confidence, calibration should be tested.

For example:

```text
predicted confidence
vs
observed correctness
```

Confidence remains diagnostic and does not establish authority.

---

# 49. Uncertainty

Evaluation results may contain uncertainty.

Preserve:

```text
uncertainty sources
confidence
sample limitations
measurement limitations
environmental limitations
```

Do not force every uncertain result into:

```text
PASS
```

or:

```text
FAIL
```

---

# 50. Statistical Significance

Where statistical evaluation is appropriate, preserve:

```text
sample size
sampling procedure
uncertainty interval
test assumptions
statistical method
```

A statistically significant result does not automatically establish architectural significance.

---

# 51. Benchmark Integrity

Benchmarks themselves must be evaluated.

Potential benchmark failures include:

```text
data leakage
contamination
unrepresentative cases
hidden test overlap
incorrect labels
insufficient adversarial cases
```

A benchmark result is only as meaningful as the benchmark protocol.

---

# 52. Benchmark Versioning

Benchmark datasets and protocols must be versioned.

Historical results should preserve the exact versions used.

---

# 53. Evaluation Leakage

The system must detect or control situations where the target has access to:

```text
test answers
attack cases
evaluation criteria
hidden labels
future benchmark data
```

where such access invalidates the evaluation.

---

# 54. Evaluator Leakage

An evaluator must not accidentally receive information that makes the evaluation invalid.

Examples:

```text
expected answer
target's hidden state
attack label
post-hoc outcome
```

unless the protocol explicitly requires it.

---

# 55. Evaluation Order Effects

Repeated evaluation may change:

```text
memory
agent state
model state
tool state
environment
```

Where this affects validity, the protocol must control or record the order.

---

# 56. Evaluation Reproducibility

A consequential evaluation should be reproducible from:

```text
target version
protocol version
test-set version
configuration
inputs
environment
```

where technically feasible.

---

# 57. Evaluation Determinism

If the evaluator is nondeterministic, the protocol must specify:

```text
number of runs
aggregation
variance treatment
stopping rule
```

A single stochastic run should not automatically be treated as definitive evidence.

---

# 58. Human Evaluation

Human evaluation should preserve:

```text
evaluator identity
evaluation rubric
instructions
decision
timestamp
```

Where anonymity is required, a stable pseudonymous evaluator reference may be used.

---

# 59. Human / Machine Disagreement

If human and machine evaluations disagree:

```text
DO NOT SILENTLY SELECT ONE
```

Represent the disagreement explicitly and apply the applicable adjudication process.

---

# 60. Adjudication

Adjudication resolves disputed evaluation results.

It must preserve:

```text
original results
disagreement
adjudicator
authority
evidence
final determination
```

Adjudication does not erase the original evaluations.

---

# 61. Evaluation Status and Lifecycle

Evaluation results may inform lifecycle transitions but must not silently perform them.

Conceptually:

```text
EVALUATION
 ↓
LIFECYCLE PRECONDITION
 ↓
AUTHORITY
 ↓
TRANSITION
```

This preserves III-003's separation.

---

# 62. Evaluation vs Approval

Evaluation answers:

```text
DID THE TARGET SATISFY THE TEST?
```

Approval answers:

```text
IS THE TARGET AUTHORIZED FOR THE RELEVANT USE?
```

Therefore:

```text
EVALUATION PASS
≠
APPROVAL
```

---

# 63. Evaluation vs Truth

An evaluation establishes only what its protocol supports.

Therefore:

```text
EVALUATION PASS
≠
UNIVERSAL TRUTH
```

The claim scope must be explicit.

---

# 64. Evaluation of Verification Mechanisms

The verification system itself must be evaluated.

Examples:

```text
Can the critic detect known defects?
Can the adversary discover seeded vulnerabilities?
Does the verifier miss correlated failures?
Does repair introduce regressions?
Can the system detect evaluator failure?
```

This creates a recursive but bounded evaluation requirement.

---

# 65. Seeded Failure Testing

To evaluate verifier sensitivity, known failures may be deliberately inserted.

Conceptually:

```text
KNOWN DEFECT
 ↓
VERIFIER
 ↓
DETECTED / MISSED
```

The defect must be labeled in the benchmark so that detection performance is measurable.

---

# 66. Novel Failure Discovery

Known-failure detection is insufficient.

Adversarial verification should also measure:

```text
NOVEL FAILURE DISCOVERY
```

where the verifier finds failures not explicitly seeded into the test set.

---

# 67. Critic Effectiveness

Self-critique should be evaluated on:

```text
critical defect recall
false criticism rate
useful correction rate
severity calibration
agreement with independent evaluation
```

---

# 68. Adversarial Verifier Effectiveness

Adversarial verification should be evaluated on:

```text
attack coverage
failure discovery rate
false attack rate
novel failure discovery
reproducibility
regression detection
```

---

# 69. Verification Blind Spots

The architecture should maintain a record of known blind spots.

Conceptually:

```yaml
blind_spot:
  blind_spot_id: ...
  evaluator_ref: ...
  failure_class: ...
  evidence_refs: []
  mitigation: ...
```

Known blind spots must not be hidden behind aggregate scores.

---

# 70. Verification Debt

Unverified critical claims create verification debt.

Conceptually:

```text
CLAIM
 ↓
REQUIRED VERIFICATION
 ↓
MISSING TEST
 ↓
VERIFICATION DEBT
```

This enables prioritization of future testing.

---

# 71. Evaluation Queue

High-impact claims should be prioritized for stronger evaluation according to:

```text
impact
uncertainty
novelty
failure cost
historical failure rate
verification debt
```

The exact prioritization formula remains implementation-specific.

---

# 72. Evaluation Record Concept

```yaml
evaluation:
  evaluation_id: EVAL-...
  protocol_ref: EVPROT-...
  target:
    object_id: ...
    version: ...

  question: ...

  evaluator:
    evaluator_id: ...
    type: ...

  criteria:
    - ...

  tests:
    - TST-...

  result: PASS

  metrics: []

  evidence_refs: []

  independence:
    dimensions: {}
    assessment: ...

  provenance_ref: PROV-...
```

This is conceptual, not final JSON Schema.

---

# 73. Attack Record Concept

```yaml
attack:
  attack_id: ATK-...
  target_ref: ...
  target_version: ...
  attacker_ref: ...
  attack_type: ...
  parameters: ...
  observed_result: ...
  success: true
  evidence_refs: []
  regression_ref: ...
  provenance_ref: PROV-...
```

---

# 74. Verification Pipeline

The canonical verification path is:

```text
CLAIM / PROPERTY
 ↓
TARGET VERSION
 ↓
EVALUATION PROTOCOL
 ↓
TEST SET
 ↓
SELF-CRITIQUE / INDEPENDENT CRITIQUE
 ↓
ADVERSARIAL ATTACKS
 ↓
OBSERVATION
 ↓
RESULT
 ↓
EVIDENCE
 ↓
INTERPRETATION
 ↓
PROVENANCE
 ↓
LIFECYCLE / DECISION CONSEQUENCE
```

The exact sequence may vary by protocol, but required semantic checks cannot be skipped.

---

# 75. Verification Invariants

### Invariant 1

Every consequential evaluation has an explicit target.

### Invariant 2

Every consequential evaluation uses an identifiable protocol version.

### Invariant 3

Evaluation results are scoped to what the protocol actually tests.

### Invariant 4

PASS does not mean universal correctness.

### Invariant 5

NOT_TESTED does not mean PASS.

### Invariant 6

INCONCLUSIVE does not mean PASS.

### Invariant 7

Evaluator identity is explicit.

### Invariant 8

Evaluator capability is distinct from evaluator authority.

### Invariant 9

Evaluation evidence is provenance-traceable.

### Invariant 10

Self-critique is distinct from independent verification.

### Invariant 11

Adversarial verification actively seeks counterexamples.

### Invariant 12

Verification independence must have explicit dimensions.

### Invariant 13

Different agent names do not establish independence.

### Invariant 14

False passes must be measurable.

### Invariant 15

False fails must be measurable.

### Invariant 16

Coverage is distinct from correctness.

### Invariant 17

Benchmark integrity must be evaluated.

### Invariant 18

Evaluation leakage must be controlled.

### Invariant 19

Historical evaluation results remain reconstructable.

### Invariant 20

Corrections do not silently erase prior evaluations.

### Invariant 21

Evaluation pass does not automatically equal approval.

### Invariant 22

Evaluation does not automatically mutate lifecycle state.

### Invariant 23

Known verifier blind spots remain visible.

### Invariant 24

Known failures should become regression tests where appropriate.

### Invariant 25

Novel failure discovery should be measured.

### Invariant 26

Verification mechanisms themselves are evaluable.

### Invariant 27

Verification debt is explicitly representable.

### Invariant 28

Implementation must not invent evaluation semantics.

---

# 76. Required Tests

The reference implementation must test:

```text
evaluation identity
protocol versioning
target versioning
criteria evaluation
metric calculation
threshold enforcement
PASS
FAIL
INCONCLUSIVE
NOT_TESTED
BLOCKED
evidence capture
evaluator identity
evaluator authority
self-critique
independent critique
adversarial attack
attack reproducibility
known-failure detection
novel-failure discovery
false-pass detection
false-fail detection
verification independence
benchmark leakage
evaluation leakage
stochastic evaluator behavior
human/machine disagreement
adjudication
verification regression
verification blind spots
verification debt
```

---

# 77. Falsification Cases

Deliberately attempt:

```text
mark untested target as PASS
change protocol after evaluation
evaluate wrong target version
hide failed test cases
reuse stale benchmark
leak expected answers
allow evaluator to inspect hidden labels
claim independence from shared model
seed a failure that the verifier misses
introduce correlated evaluator failure
erase a failed evaluation
turn INCONCLUSIVE into PASS
turn evaluation PASS into automatic approval
repair only the triggering case
hide novel attack failures
inflate coverage without testing new cases
```

---

# 78. Core Verification Benchmarks

The architecture should maintain at least four benchmark classes:

```text
1. CORRECTNESS BENCHMARK
2. ROBUSTNESS BENCHMARK
3. ADVERSARIAL FAILURE-DISCOVERY BENCHMARK
4. VERIFICATION-MECHANISM BENCHMARK
```

The fourth benchmark is especially important.

We must evaluate not only:

```text
IS THE SYSTEM GOOD?
```

but also:

```text
IS OUR METHOD OF CHECKING THE SYSTEM GOOD?
```

---

# 79. Meta-Verification

Meta-verification evaluates the verifier itself.

Conceptually:

```text
TARGET
 ↓
VERIFIER
 ↓
VERIFICATION RESULT
 ↓
META-VERIFIER
 ↓
VERIFIER QUALITY ASSESSMENT
```

This does not create infinite recursion.

The architecture should define bounded verification layers appropriate to the claim.

---

# 80. Verification Independence Experiment

A key research benchmark should compare:

```text
SELF-CRITIQUE
vs
INDEPENDENT CRITIQUE
vs
ADVERSARIAL VERIFIER
vs
EXTERNAL EVALUATOR
```

using the same seeded and naturally occurring failures.

Measure:

```text
failure detection
overlap
unique discoveries
false passes
false fails
correlated misses
```

This produces evidence about whether additional verification layers actually add independent information.

---

# 81. Verification Dominance Test

A stronger verifier should not be assumed to be better merely because it is:

```text
larger
more capable
more expensive
more verbose
```

Compare actual failure-detection behavior.

A verifier that is more capable than the target may still reproduce the target's failure mode.

This must remain an empirical question.

---

# 82. Verification Failure as Evidence

A verification failure should be treated as evidence about:

```text
target
verifier
protocol
benchmark
architecture
```

It must not automatically be interpreted as proof that only the target is wrong.

The failure analysis should determine the source.

---

# 83. Evaluator Error Model

Where possible, model:

```text
TARGET ERROR
VERIFIER ERROR
BENCHMARK ERROR
PROTOCOL ERROR
INTERPRETATION ERROR
```

as distinct failure classes.

This is critical for proving the architecture rather than merely generating confidence.

---

# 84. Deferred Decisions

III-009 intentionally does not freeze:

- exact evaluation framework;
- benchmark infrastructure;
- evaluator model selection;
- attack-generation model;
- statistical library;
- confidence aggregation;
- independence scoring formula;
- exact verification hierarchy;
- meta-verification depth;
- formal-method integration;
- human review workflow;
- exact evaluation schema syntax.

These remain engineering decisions unless they change semantic meaning.

---

# 85. Exit Criteria

- [x] Evaluation identity defined
- [x] Evaluation version defined
- [x] Target identity defined
- [x] Evaluation question defined
- [x] Claim linkage defined
- [x] Protocol defined
- [x] Dataset / test-set versioning defined
- [x] Test-case identity defined
- [x] Criteria defined
- [x] Metrics defined
- [x] Thresholds defined
- [x] Result states defined
- [x] Evidence defined
- [x] Evaluation provenance defined
- [x] Evaluator identity defined
- [x] Evaluator authority boundary defined
- [x] Self-critique defined
- [x] Independent critique defined
- [x] Independence dimensions defined
- [x] Shared failure modes defined
- [x] Adversarial verification defined
- [x] Attack identity defined
- [x] Attack taxonomy defined
- [x] Counterexamples defined
- [x] Attack reproducibility defined
- [x] Regression testing defined
- [x] Verification independence defined
- [x] Coverage defined
- [x] False pass / false fail defined
- [x] Benchmark integrity defined
- [x] Evaluation leakage defined
- [x] Human evaluation defined
- [x] Adjudication defined
- [x] Verification mechanism evaluation defined
- [x] Seeded failure testing defined
- [x] Novel failure discovery defined
- [x] Verification blind spots defined
- [x] Verification debt defined
- [x] Meta-verification defined
- [x] Core benchmarks defined
- [x] Verification invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 86. Next Contract

**III-010 — Provenance-Aware Memory, Evidence & Retrieval Integrity Contract**

III-010 will deepen the information-integrity layer by formalizing:

```text
evidence identity
source hierarchy
retrieval integrity
citation binding
evidence snapshots
source mutation
retrieval reproducibility
evidence conflict
evidence freshness
evidence contamination
retrieval poisoning
knowledge graph lineage
vector retrieval lineage
evidence-to-claim binding
```

The central requirement will be:

```text
IF INFORMATION SUPPORTS A CONSEQUENTIAL CLAIM,
THE SYSTEM MUST BE ABLE TO ESTABLISH
WHICH INFORMATION WAS ACTUALLY USED,
WHICH VERSION IT HAD,
AND WHETHER THAT INFORMATION
REMAINS TRUSTWORTHY FOR THE CLAIM.
```
