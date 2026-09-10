# II-016 — Validation, Benchmarking & Architectural Evidence Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Depends On:** II-001 through II-015  
**Scope:** Empirical validation of the Intelligence Architecture, benchmark design, evidence collection, falsification, calibration, regression testing, object-authority validation, evaluator validation, and architecture-level proof

---

## 1. Purpose

II-016 defines how the Intelligence Architecture will be empirically evaluated.

The purpose is not to demonstrate that the system can produce impressive outputs.

The purpose is to determine:

> **Which architectural claims are supported by evidence, which are unsupported, which fail under controlled testing, and under what conditions the architecture remains reliable.**

This specification establishes the validation boundary between:

```text
ARCHITECTURAL DESIGN
        ↓
IMPLEMENTATION
        ↓
EMPIRICAL TEST
        ↓
MEASURED EVIDENCE
        ↓
ARCHITECTURAL CLAIM
```

---

# 2. Core Principle

> **An architectural claim is not evidence of architectural correctness.**

Therefore:

```text
DESIGNED
≠
IMPLEMENTED
≠
WORKS
≠
PROVEN
```

The architecture must produce measurable evidence against explicit hypotheses.

---

# 3. What "Proof" Means in This Architecture

The system should not claim mathematical proof of general intelligence correctness.

Instead, architectural validity should be established through:

```text
EXPLICIT CLAIM
        ↓
FALSIFIABLE HYPOTHESIS
        ↓
CONTROLLED TEST
        ↓
BASELINE
        ↓
MEASUREMENT
        ↓
REPLICATION
        ↓
FAILURE ANALYSIS
        ↓
EVIDENCE
```

The resulting evidence supports a bounded claim:

> The architecture performs better, more reliably, or more safely than the specified baseline under the tested conditions.

---

# 4. Validation Scope

II-016 evaluates at least:

```text
OBJECT AUTHORITY
KNOWLEDGE QUALITY
EVIDENCE SUFFICIENCY
DECISION QUALITY
CONSTRAINT PRESERVATION
NARRATIVE COHERENCE
CHANNEL PROJECTION
PROMPT COMPILATION
EVALUATOR RELIABILITY
SELF-CRITIQUE
ADVERSARIAL VERIFICATION
REPLANNING
PROVENANCE
LIFECYCLE INTEGRITY
MULTI-AGENT GOVERNANCE
RUNTIME CORRECTNESS
STRATEGIC DRIFT
```

Not every property requires the same evaluation method.

---

# 5. Evaluation Layers

Validation should occur at multiple levels.

```text
LEVEL 0 — UNIT
LEVEL 1 — OBJECT
LEVEL 2 — AGENT
LEVEL 3 — SUBSYSTEM
LEVEL 4 — PIPELINE
LEVEL 5 — CAMPAIGN
LEVEL 6 — ARCHITECTURE
```

A system should not claim architecture-level validity from unit-level tests alone.

---

# 6. Level 0 — Unit Validation

Tests deterministic mechanisms such as:

```text
schema validation
state transitions
authority checks
constraint checks
version checks
dependency checks
prompt compilation
```

These tests establish implementation correctness for individual mechanisms.

---

# 7. Level 1 — Object Validation

Tests whether semantic objects satisfy their contracts.

Examples:

```text
knowledge object
authority object
intent object
evidence requirement
asset strategy
narrative node
channel projection
evaluation record
recovery plan
```

---

# 8. Level 2 — Agent Validation

Tests an individual agent against its defined authority and responsibilities.

Questions include:

```text
Does it perform its assigned task?
Does it stay within scope?
Does it preserve provenance?
Does it abstain when evidence is insufficient?
Does it produce the required output type?
```

---

# 9. Level 3 — Subsystem Validation

Tests coordinated components.

Examples:

```text
retrieval + authority validation
evaluation + self-critique
replanning + lifecycle
governance + runtime
provenance + audit
```

---

# 10. Level 4 — Pipeline Validation

Tests end-to-end information flow:

```text
KNOWLEDGE
 ↓
INTENT
 ↓
EVIDENCE
 ↓
ASSET STRATEGY
 ↓
NARRATIVE
 ↓
CHANNEL
 ↓
PROMPT
 ↓
GENERATION
 ↓
EVALUATION
 ↓
RECOVERY
```

---

# 11. Level 5 — Campaign Validation

Tests whether the system produces a coherent campaign across multiple assets and channels while preserving:

```text
intent
product truth
authority
evidence
brand constraints
narrative coherence
```

---

# 12. Level 6 — Architecture Validation

Tests the architectural claims themselves.

Examples:

```text
Does explicit authority reduce unauthorized decisions?

Does structured evidence reduce unsupported claims?

Does adversarial verification discover failures missed by normal evaluation?

Does provenance improve decision reconstruction?

Does dependency-aware recovery reduce strategic drift?
```

These are the highest-level validation questions.

---

# 13. Baseline Principle

Every performance claim should have a meaningful baseline where feasible.

Possible baselines:

```text
RAW GENERATION
SINGLE-AGENT GENERATION
UNSTRUCTURED PROMPTING
NO RETRIEVAL
NO AUTHORITY LAYER
NO EVALUATOR
NO ADVERSARIAL VERIFICATION
NO PROVENANCE
FULL REGENERATION
```

The baseline must represent the capability the proposed architecture claims to improve upon.

---

# 14. Baseline Fairness

The architecture and baseline should receive comparable:

```text
input information
model capability
generation budget
time budget
evaluation opportunity
```

unless the experiment specifically tests resource differences.

A stronger baseline should not be deliberately weakened.

---

# 15. Hypothesis Structure

Each architectural hypothesis should specify:

```text
HYPOTHESIS_ID
CLAIM
NULL / ALTERNATIVE
TEST
BASELINE
INPUTS
METRICS
SUCCESS CRITERIA
FAILURE CRITERIA
CONFOUNDERS
REPLICATION PLAN
```

Exact statistical implementation remains deferred.

---

# 16. Falsifiability

A hypothesis is valid only if there exists a possible result that would count against it.

Bad:

```text
"The architecture produces better intelligence."
```

Better:

```text
"Under controlled benchmark conditions, the governed
architecture reduces false PASS decisions compared
with the defined baseline."
```

The second can be falsified.

---

# 17. Null Hypothesis

Where appropriate, experiments should define a null hypothesis.

Example:

```text
H1:
Adversarial verification improves critical-failure detection.

H0:
Adversarial verification does not improve critical-failure detection
relative to the baseline.
```

---

# 18. Metrics

Metrics should correspond directly to the claim being tested.

Potential metrics include:

```text
FALSE PASS RATE
FALSE FAIL RATE
CRITICAL FAILURE DETECTION
REQUIREMENT COVERAGE
EVIDENCE SUFFICIENCY
AUTHORITY PRECISION
AUTHORITY RECALL
UNAUTHORIZED MUTATION RATE
STALE DECISION RATE
STRATEGIC DRIFT
RECOVERY SUCCESS
RECOVERY REGRESSION
PROVENANCE COMPLETENESS
AUDIT RECONSTRUCTION ACCURACY
EVALUATOR CALIBRATION
ADVERSARIAL FAILURE DISCOVERY
```

Metrics should not be selected merely because they are easy to measure.

---

# 19. Composite Scores

Composite scores should be used cautiously.

A single score can hide:

```text
critical failures
disagreement
abstention
authority violations
```

Therefore the architecture should preserve component metrics.

---

# 20. Critical Failure Rule

A high aggregate score must not conceal a critical invariant violation.

Example:

```text
Overall score = 94%

Authority violation = CRITICAL
```

The system cannot declare the architecture successful without addressing the critical failure.

---

# 21. Ground Truth

Ground truth must be classified.

Possible categories:

```text
OBJECTIVE
MEASURED
EXPERT-LABELED
USER-AUTHORITATIVE
CONSENSUS
PROXY
UNKNOWN
```

The architecture must not silently treat a proxy as objective truth.

---

# 22. Human Ground Truth

For subjective domains such as:

```text
aesthetic quality
brand coherence
cultural interpretation
emotional response
creative effectiveness
```

human expert evaluation may be necessary.

Human labels should preserve:

```text
criteria
role
rationale
confidence
disagreement
```

---

# 23. Gold Set

A controlled benchmark should eventually contain a gold set of cases with:

```text
known requirements
known authoritative inputs
expected constraints
validated evidence
expected decisions
known failure modes
```

The gold set should be versioned.

---

# 24. Negative Set

The benchmark must also contain intentionally invalid cases.

Examples:

```text
unsupported claim
wrong authority
stale knowledge
missing evidence
conflicting constraints
invalid asset strategy
narrative contradiction
channel violation
prompt slop
```

The system must demonstrate that it can reject or challenge these cases.

---

# 25. Adversarial Set

A separate adversarial corpus should attempt to exploit the architecture.

Examples:

```text
authority spoofing
citation spoofing
stale-version injection
prompt injection
circular evidence
false corroboration
hidden constraint conflict
strategic drift
evaluation manipulation
recovery loop
```

---

# 26. Regression Set

Every previously discovered important failure should become a regression test.

```text
FAILURE
 ↓
ROOT CAUSE
 ↓
FIX
 ↓
REGRESSION CASE
```

The architecture must demonstrate that fixes do not silently reintroduce known failures.

---

# 27. Object Authority Evaluation

Object authority should be evaluated independently.

For each authority claim:

```text
CLAIMED AUTHORITY
        ↓
SCOPE
        ↓
SOURCE
        ↓
PROVENANCE
        ↓
CONFLICT SEARCH
        ↓
INDEPENDENT VALIDATION
        ↓
ADVERSARIAL CHALLENGE
        ↓
AUTHORITY RESULT
```

---

# 28. Authority Evaluation Outcomes

Potential states:

```text
SUPPORTED
PARTIALLY_SUPPORTED
CONTESTED
UNSUPPORTED
UNKNOWN
INVALID
```

Authority should not be represented only as a scalar confidence score.

---

# 29. Authority Benchmark

Create cases where:

```text
high-confidence source is not authoritative
low-confidence source is authoritative
two authorities conflict
authority is scoped narrowly
authority has expired
authority has been revoked
source claims authority without evidence
```

The system must distinguish these cases.

---

# 30. Authority Precision

Measure:

```text
Correct authority assignments
/
All authority assignments
```

This estimates authority precision.

---

# 31. Authority Recall

Measure:

```text
Correctly identified authoritative objects
/
All authoritative objects in benchmark
```

This estimates authority recall.

---

# 32. Authority Scope Accuracy

A system may identify the correct source but assign it excessive scope.

Therefore test:

```text
OBJECT CORRECT?
SCOPE CORRECT?
DOMAIN CORRECT?
TIME CORRECT?
DECISION TYPE CORRECT?
```

Scope errors must be measured separately.

---

# 33. Evidence Sufficiency Evaluation

Test whether the system correctly distinguishes:

```text
SUPPORTED
vs
INSUFFICIENT
vs
UNCERTAIN
```

The benchmark should contain cases where evidence is:

```text
strong
weak
contradictory
indirect
missing
misleading
```

---

# 34. False PASS

One of the most important evaluation metrics is:

```text
FALSE PASS RATE
```

A false PASS occurs when:

```text
system = PASS
ground truth / expert assessment = FAIL
```

Critical false PASS cases should be weighted heavily.

---

# 35. False FAIL

Also measure:

```text
FALSE FAIL RATE
```

because excessive rejection can make the system unusable.

The architecture should optimize for calibrated decisions rather than maximum rejection.

---

# 36. Abstention

The system must be allowed to say:

```text
UNCERTAIN
NOT_EVALUABLE
```

when evidence is insufficient.

Evaluate whether abstention improves calibration.

---

# 37. Calibration

Confidence should correspond to empirical correctness.

For example:

```text
90% confidence
```

should approximately correspond to:

```text
~90% correctness
```

within the applicable evaluation setting.

Exact calibration metrics remain deferred.

---

# 38. Evaluator Validation

The evaluator itself must be tested.

Questions:

```text
Does it detect known failures?
Does it recognize known passes?
Does it abstain appropriately?
Does it over-trust generated assertions?
Does it reproduce generator errors?
```

---

# 39. Critic Validation

The Self-Critique Agent should be tested against known weaknesses.

Measure:

```text
weakness discovery
false criticism
missed critical failures
actionability
```

---

# 40. Adversarial Verifier Validation

The adversarial verifier should be tested against seeded vulnerabilities.

Measure:

```text
attack success
failure discovery
false alarms
coverage
novel failure discovery
```

A verifier that only finds obvious failures is insufficient.

---

# 41. Independent Verification

Where possible, validation should use mechanisms that are meaningfully independent from the system being tested.

Potential independence:

```text
different model
different prompt
different evidence
different evaluator
rule-based check
human expert
external benchmark
```

But:

```text
different model
≠
automatic independence
```

Correlated assumptions must be considered.

---

# 42. Ablation Testing

Ablation tests remove architectural components to measure their contribution.

Examples:

```text
FULL SYSTEM
vs
NO AUTHORITY LAYER

FULL SYSTEM
vs
NO RETRIEVAL

FULL SYSTEM
vs
NO SELF-CRITIQUE

FULL SYSTEM
vs
NO ADVERSARIAL VERIFICATION

FULL SYSTEM
vs
NO PROVENANCE

FULL SYSTEM
vs
NO REPLANNING
```

This is essential for determining whether each subsystem provides measurable value.

---

# 43. Component Contribution

A component should not be considered necessary merely because the architecture contains it.

Evidence should show:

```text
COMPONENT
→ measurable contribution
```

or:

```text
COMPONENT
→ no demonstrated contribution
```

Both outcomes are valuable.

---

# 44. Counterfactual Testing

Where possible, evaluate:

```text
What would have happened
without this intelligence decision?
```

Example:

```text
WITH evidence requirement
vs
WITHOUT evidence requirement
```

Measure downstream differences.

---

# 45. Perturbation Testing

Inputs should be intentionally perturbed.

Examples:

```text
slightly incorrect knowledge
conflicting source
missing source
changed product attribute
changed channel constraint
altered user objective
```

Observe whether the architecture:

```text
detects
adapts
rejects
or
fails silently
```

---

# 46. Robustness

Robustness asks:

> Does the architecture remain valid when inputs vary within expected conditions?

Measure:

```text
decision stability
authority stability
evidence stability
narrative stability
```

---

# 47. Sensitivity

Sensitivity asks:

> Which input changes cause meaningful decision changes?

A good architecture should be:

```text
sensitive to consequential changes
```

and:

```text
insensitive to irrelevant noise
```

---

# 48. Distribution Shift

Evaluation should eventually include cases outside the development distribution.

Examples:

```text
new product category
new visual style
new channel
new knowledge source
new campaign objective
new cultural context
```

This tests whether the architecture generalizes or merely memorizes benchmark patterns.

---

# 49. Cross-Domain Evaluation

The architecture must be tested where multiple domains interact.

Example:

```text
Apparel
+
Footwear
+
Jewelry
```

with competing:

```text
material requirements
lighting requirements
composition requirements
evidence requirements
```

Measure whether governance and constraint resolution remain stable.

---

# 50. Strategic Drift Measurement

Strategic drift should be explicitly measured.

Potential representation:

```text
ORIGINAL LOCKED INTENT
        ↓
FINAL OUTPUT STRATEGY
        ↓
SEMANTIC DIFFERENCE
```

Drift should be evaluated against approved intent rather than visual similarity alone.

---

# 51. Recovery Evaluation

Measure:

```text
RECOVERY SUCCESS RATE
RECOVERY COST
RECOVERY TIME
REGRESSION RATE
STRATEGIC DRIFT
REPEATED FAILURE RATE
```

A recovery that succeeds only by changing the campaign objective is not necessarily a successful recovery.

---

# 52. Provenance Evaluation

Test whether a reviewer can reconstruct:

```text
output
→ prompt
→ specification
→ narrative
→ asset strategy
→ evidence
→ intent
→ knowledge
→ source
```

Measure:

```text
TRACE COMPLETENESS
TRACE CORRECTNESS
RECONSTRUCTION ACCURACY
```

---

# 53. Lifecycle Evaluation

Test:

```text
invalid transition
stale object
zombie dependency
orphan object
lock violation
unauthorized approval
incorrect invalidation
```

The runtime should detect these before they become downstream intelligence.

---

# 54. Governance Evaluation

Test:

```text
unauthorized override
authority overreach
false delegation
stale agent output
suppressed dissent
false consensus
cross-domain authority violation
```

---

# 55. Runtime Evaluation

Test:

```text
dependency scheduling
concurrency
stale writes
retry behavior
timeouts
cancellation
resource exhaustion
execution provenance
```

---

# 56. End-to-End Evaluation

The full architecture should eventually be tested:

```text
INPUT
 ↓
KNOWLEDGE
 ↓
INTENT
 ↓
EVIDENCE
 ↓
ASSET STRATEGY
 ↓
NARRATIVE
 ↓
CHANNEL
 ↓
GENERATION
 ↓
EVALUATION
 ↓
ADVERSARIAL VERIFICATION
 ↓
RECOVERY
 ↓
FINAL OUTPUT
```

The test should measure both:

```text
OUTPUT QUALITY
```

and:

```text
PROCESS INTEGRITY
```

---

# 57. Process Integrity

An output should not be considered a success if it violates architectural invariants while accidentally producing a good result.

Example:

```text
Unauthorized agent override
+
beautiful final campaign
```

Result:

```text
OUTPUT QUALITY = PASS
ARCHITECTURAL INTEGRITY = FAIL
```

Both must be reported.

---

# 58. Benchmark Versioning

Every benchmark should preserve:

```text
benchmark_id
version
cases
ground truth
criteria
evaluation method
date
source
```

Changing the benchmark invalidates direct comparison unless version differences are accounted for.

---

# 59. Dataset Contamination

The system should consider whether benchmark cases have leaked into:

```text
prompts
training data
retrieval corpus
agent memory
evaluation examples
```

Contaminated benchmarks can produce misleadingly strong results.

---

# 60. Test Isolation

Evaluation should prevent the system under test from knowing:

```text
expected answer
ground truth label
adversarial condition
```

unless the experiment explicitly tests behavior under known conditions.

---

# 61. Statistical Validity

The exact statistical methodology remains deferred, but experiments should consider:

```text
sample size
variance
confidence intervals
effect size
repeated trials
paired comparisons
multiple comparisons
```

The system should avoid declaring meaningful improvement from anecdotal examples.

---

# 62. Replication

Important architectural claims should be replicated.

Replication may involve:

```text
new cases
new random seeds
new campaign
new evaluator
new model version
new domain
```

The appropriate replication strategy depends on the claim.

---

# 63. Failure Analysis

A failed experiment is not merely a negative result.

The architecture should record:

```text
hypothesis
test
observed failure
root cause
scope
conditions
severity
implication
```

Failure analysis becomes part of the evidence base.

---

# 64. Evidence Ledger

The architecture should maintain an evidence ledger for architectural claims.

Conceptually:

```text
CLAIM
 ↓
HYPOTHESIS
 ↓
EXPERIMENT
 ↓
RESULT
 ↓
REPLICATION
 ↓
CURRENT EVIDENCE STATUS
```

Potential statuses:

```text
UNTESTED
WEAKLY_SUPPORTED
SUPPORTED
STRONGLY_SUPPORTED
CONTESTED
FALSIFIED
INCONCLUSIVE
```

---

# 65. Claim Status

A claim should never be marked:

```text
PROVEN
```

simply because one experiment succeeded.

The evidence status should reflect:

```text
scope
replication
quality
limitations
contradictory results
```

---

# 66. Architectural Claim Registry

The architecture should maintain a registry containing:

```text
claim_id
claim
scope
hypothesis
tests
baselines
results
replications
failures
limitations
current_status
version
```

---

# 67. Evidence Independence

Evidence supporting an architectural claim should be evaluated for correlation.

Example:

```text
Five evaluators
all using the same model
same prompt
same benchmark
```

do not necessarily represent five independent pieces of evidence.

---

# 68. Evidence Weight

Evidence weight may depend on:

```text
independence
quality
replication
ground-truth reliability
sample size
effect magnitude
adversarial robustness
```

The exact formula remains deferred.

---

# 69. Claim Falsification

If strong evidence contradicts an architectural claim:

```text
CLAIM
 ↓
FALSIFIED / CONTESTED
```

The system should not reinterpret the experiment merely to preserve the claim.

Possible responses:

```text
REVISE ARCHITECTURE
NARROW CLAIM
CHANGE CONDITIONS
ABANDON CLAIM
```

---

# 70. No Goodharting

Metrics must not become the target in a way that destroys the underlying objective.

Example:

```text
Optimize PASS rate
→ evaluator manipulation
→ apparent improvement
→ real reliability decreases
```

The architecture should use:

```text
multiple measures
adversarial testing
held-out cases
human review
```

where appropriate.

---

# 71. Hidden Test Set

A held-out evaluation set should eventually be maintained.

The system under development should not have unrestricted access to the labels or exact cases.

This reduces benchmark overfitting.

---

# 72. Challenge Set

The challenge set should contain cases designed specifically to expose:

```text
authority confusion
evidence hallucination
strategic drift
cross-domain conflict
evaluation gaming
recovery failure
provenance gaps
```

---

# 73. Architecture Acceptance Criteria

The architecture should not be accepted solely on average performance.

Acceptance should require:

```text
CRITICAL INVARIANTS PASS
+
NO UNRESOLVED CRITICAL GOVERNANCE FAILURE
+
NO UNRESOLVED CRITICAL PROVENANCE FAILURE
+
EVALUATOR RELIABILITY WITHIN REQUIRED BOUNDS
+
ADVERSARIAL TESTING COMPLETED
+
REGRESSION SUITE PASSING
+
KNOWN LIMITATIONS DOCUMENTED
```

Exact thresholds remain deferred.

---

# 74. Human Review Gate

Certain high-consequence architectural conclusions may require human review.

Examples:

```text
claim of authority validity
major architecture change
critical benchmark interpretation
falsification decision
release acceptance
```

The human review must itself be recorded.

---

# 75. Evaluation Security

Evaluation infrastructure must be protected against:

```text
benchmark manipulation
ground-truth leakage
result tampering
selective reporting
hidden failed runs
post-hoc metric changes
```

The exact security architecture remains deferred.

---

# 76. Reporting

Evaluation reports should distinguish:

```text
OBSERVED
MEASURED
INFERRED
INTERPRETED
UNKNOWN
```

A report should not convert interpretation into observation.

---

# 77. Reproducibility Package

Important experiments should preserve sufficient artifacts to reproduce the evaluation conditions:

```text
code version
model version
prompt/policy version
knowledge version
benchmark version
configuration
input data
evaluation criteria
results
```

Sensitive data handling remains implementation-specific.

---

# 78. External Validation

Where practical, important claims should eventually be tested outside the immediate development environment.

Possible forms:

```text
independent reviewer
independent evaluator
external benchmark
new campaign
new domain
new model
```

This helps detect internal confirmation bias.

---

# 79. Architecture-Level Evidence Matrix

The final validation program should map:

| Architectural Claim | Test | Baseline | Metric | Current Evidence |
|---|---|---|---|---|
| Authority improves decision validity | Authority benchmark | Unscoped baseline | Authority precision/recall | TBD |
| Evidence requirements reduce unsupported decisions | Evidence benchmark | No evidence layer | False PASS | TBD |
| Self-critique finds weaknesses | Seeded critique set | No critic | Failure discovery | TBD |
| Adversarial verification finds hidden failures | Adversarial set | Normal evaluation | Critical discovery | TBD |
| Replanning reduces drift | Recovery benchmark | Full regeneration | Strategic drift | TBD |
| Provenance improves reconstruction | Audit benchmark | Final output only | Reconstruction accuracy | TBD |
| Lifecycle guards prevent invalid consumption | State benchmark | Ungoverned state | Invalid consumption | TBD |
| Governance prevents unauthorized override | Multi-agent benchmark | Implicit authority | Violation rate | TBD |
| Runtime enforces contracts | Runtime benchmark | Unenforced runtime | Contract violation rate | TBD |

This matrix becomes a living research artifact.

---

# 80. Proof Boundary

The architecture should distinguish:

```text
PROVED IMPLEMENTATION PROPERTY
```

from:

```text
EMPIRICALLY SUPPORTED BEHAVIOR
```

and:

```text
UNTESTED ASSUMPTION
```

For example:

```text
"Runtime rejects an invalid state transition"
→ implementation property verified by tests.

"Authority layer improves campaign reliability"
→ empirical claim requiring experiments.

"Architecture will generalize to all creative domains"
→ unsupported unless separately demonstrated.
```

---

# 81. Current Evidence State

At the beginning of implementation:

```text
ARCHITECTURAL DESIGN
        ↓
HYPOTHESES DEFINED
        ↓
EMPIRICAL EVIDENCE
        ↓
NOT YET ESTABLISHED
```

This is the correct state.

The architecture must not claim validation before the tests are run.

---

# 82. Self-Critique Requirements

The Self-Critique Agent should inspect validation for:

- unsupported conclusions,
- weak baselines,
- benchmark leakage,
- metric gaming,
- overgeneralization,
- insufficient sample size,
- hidden confounders,
- selective reporting,
- evaluator dependence,
- ignored failures,
- and unjustified architectural claims.

---

# 83. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to:

1. Manufacture a false PASS.
2. Select a weak baseline.
3. Leak benchmark answers.
4. Manipulate evaluation criteria.
5. Hide failed experiments.
6. Cherry-pick successful cases.
7. Overfit to the benchmark.
8. Create correlated evaluators and call them independent.
9. Convert proxy metrics into proof.
10. Suppress contradictory evidence.
11. Inflate confidence.
12. Redefine the claim after seeing the result.
13. Ignore critical failures because aggregate performance is high.
14. Produce a benchmark that the system can trivially memorize.
15. Treat one successful experiment as universal proof.
16. Remove difficult cases after failure.
17. Alter the ground truth after observing outputs.
18. Claim architectural improvement without an appropriate baseline.

Expected behavior:

```text
ATTACK
    ↓
DETECT
    ↓
BLOCK / CHALLENGE
    ↓
RECORD
```

---

# 84. Validation Invariants

### Invariant 1

Architectural claims must be falsifiable.

### Invariant 2

Design is not evidence.

### Invariant 3

Implementation correctness is not architectural proof.

### Invariant 4

Every major empirical claim has an explicit test.

### Invariant 5

Important claims have meaningful baselines.

### Invariant 6

Critical failures cannot be hidden by aggregate metrics.

### Invariant 7

Ground truth type is explicit.

### Invariant 8

Abstention is permitted where appropriate.

### Invariant 9

Benchmark contamination is considered.

### Invariant 10

Regression cases preserve previously discovered failures.

### Invariant 11

Evidence independence is explicitly considered.

### Invariant 12

Contradictory evidence remains visible.

### Invariant 13

A successful experiment does not automatically establish universal validity.

### Invariant 14

Claims remain scoped to tested conditions.

### Invariant 15

Evaluation criteria cannot be changed after observing results without recording the change.

### Invariant 16

Self-Critique cannot silently alter experimental results.

### Invariant 17

Adversarial verification findings remain part of the evidence record.

### Invariant 18

Architecture acceptance requires critical invariants to pass.

### Invariant 19

The evidence ledger preserves both positive and negative evidence.

### Invariant 20

The architecture may be revised when evidence falsifies an architectural claim.

---

# 85. Falsifiable Architectural Hypotheses

II-016 consolidates the major hypotheses introduced throughout Phase II.

## H-001 — Authority improves decision validity

**Claim:**

Explicitly scoped authority reduces incorrect or unauthorized semantic decisions compared with unscoped authority.

**Primary metric:**

```text
AUTHORITY VIOLATION RATE
+
DECISION VALIDITY
```

---

## H-002 — Evidence requirements reduce unsupported decisions

**Claim:**

Explicit evidence requirements reduce false PASS and unsupported strategic decisions.

**Primary metric:**

```text
FALSE PASS RATE
```

---

## H-003 — Structured evaluation improves calibration

**Claim:**

Requirement-grounded evaluation produces better-calibrated decisions than holistic quality judgment.

---

## H-004 — Self-critique increases weakness discovery

**Claim:**

Adding a dedicated self-critique mechanism increases detection of meaningful weaknesses.

---

## H-005 — Adversarial verification discovers additional failures

**Claim:**

A dedicated adversarial verifier discovers critical failures missed by ordinary evaluation.

---

## H-006 — Replanning reduces strategic drift

**Claim:**

Dependency-aware minimal recovery produces less unintended strategic change than full regeneration.

---

## H-007 — Provenance improves decision reconstruction

**Claim:**

Structured provenance and lineage improve the ability to reconstruct why a decision occurred.

---

## H-008 — Lifecycle controls reduce invalid object consumption

**Claim:**

Explicit lifecycle states and guards reduce stale, invalid, zombie, and unauthorized object consumption.

---

## H-009 — Governance reduces unauthorized agent behavior

**Claim:**

Explicit multi-agent authority boundaries reduce unauthorized cross-domain decisions.

---

## H-010 — Runtime enforcement preserves semantic contracts

**Claim:**

Runtime-enforced authority, version, dependency, and lifecycle checks reduce contract violations compared with agent self-restraint alone.

---

# 86. Minimum Evidence Standard

Before a major architectural claim is treated as supported, the validation program should ideally establish:

```text
DEFINED HYPOTHESIS
+
APPROPRIATE BASELINE
+
CONTROLLED TEST
+
MEANINGFUL METRIC
+
RELEVANT SAMPLE
+
FAILURE ANALYSIS
+
AT LEAST ONE REPLICATION / HELD-OUT TEST
```

Exact statistical thresholds remain deferred.

---

# 87. Strong Evidence Standard

For high-consequence claims, stronger evidence should include:

```text
MULTIPLE TEST SETS
+
INDEPENDENT EVALUATION
+
ADVERSARIAL TESTING
+
HELD-OUT CASES
+
REGRESSION TESTING
+
CROSS-DOMAIN VALIDATION
+
CONTRADICTORY-EVIDENCE ANALYSIS
```

---

# 88. Architecture Release Gate

Before declaring a production architecture validated:

```text
UNIT TESTS
        ↓
OBJECT TESTS
        ↓
AGENT TESTS
        ↓
SUBSYSTEM TESTS
        ↓
PIPELINE TESTS
        ↓
ADVERSARIAL TESTS
        ↓
REGRESSION TESTS
        ↓
CROSS-DOMAIN TESTS
        ↓
ARCHITECTURE EVIDENCE REVIEW
```

A failure at a critical layer blocks the release until resolved or explicitly accepted by the appropriate authority.

---

# 89. Core Contract

> **The Validation, Benchmarking & Architectural Evidence Layer shall provide a falsifiable, versioned, and auditable empirical framework for determining whether the Intelligence Architecture performs the functions it claims to perform. It shall distinguish design from evidence, implementation correctness from architectural validity, quality from sufficiency, and empirical support from universal proof. It shall use controlled baselines, explicit hypotheses, ground-truth-aware benchmarks, adversarial and regression testing, ablation, perturbation, cross-domain evaluation, provenance-aware evidence, and preserved contradictory results to support, narrow, or falsify architectural claims.**

---

# 90. Deferred Decisions

II-016 does not freeze:

- exact benchmark size,
- statistical framework,
- confidence thresholds,
- significance thresholds,
- evaluator model selection,
- human panel size,
- exact metric formulas,
- dataset storage,
- benchmark execution platform,
- experiment orchestration,
- external validation partners,
- release thresholds.

These remain research and engineering decisions.

---

# 91. Exit Criteria

II-016 is semantically complete when:

- [x] Proof boundary established
- [x] Validation scope established
- [x] Multi-level validation established
- [x] Baseline principle established
- [x] Baseline fairness established
- [x] Hypothesis structure established
- [x] Falsifiability established
- [x] Ground-truth taxonomy established
- [x] Gold set established
- [x] Negative set established
- [x] Adversarial set established
- [x] Regression set established
- [x] Object authority evaluation established
- [x] Authority benchmark established
- [x] Authority precision / recall established
- [x] Authority scope evaluation established
- [x] Evidence sufficiency evaluation established
- [x] False PASS / False FAIL established
- [x] Abstention established
- [x] Calibration established
- [x] Evaluator validation established
- [x] Self-critique validation established
- [x] Adversarial verifier validation established
- [x] Independent verification established
- [x] Ablation established
- [x] Counterfactual testing established
- [x] Perturbation testing established
- [x] Robustness established
- [x] Sensitivity established
- [x] Distribution shift established
- [x] Cross-domain evaluation established
- [x] Strategic drift measurement established
- [x] Recovery evaluation established
- [x] Provenance evaluation established
- [x] Lifecycle evaluation established
- [x] Governance evaluation established
- [x] Runtime evaluation established
- [x] End-to-end evaluation established
- [x] Process integrity established
- [x] Benchmark versioning established
- [x] Dataset contamination established
- [x] Test isolation established
- [x] Statistical validity boundary established
- [x] Replication established
- [x] Failure analysis established
- [x] Evidence ledger established
- [x] Architectural claim registry established
- [x] Claim falsification established
- [x] Anti-Goodharting principle established
- [x] Hidden test set established
- [x] Challenge set established
- [x] Architecture acceptance criteria established
- [x] Human review gate established
- [x] Reporting distinction established
- [x] Reproducibility package established
- [x] External validation established
- [x] Architecture evidence matrix established
- [x] Proof boundary established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Consolidated architectural hypotheses established
- [x] Minimum evidence standard established
- [x] Strong evidence standard established
- [x] Architecture release gate established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-017 — Self-Critique, Adversarial Verification & Meta-Validation Contract**

This specification will define the two independent challenge mechanisms discussed throughout Phase II:

1. **Self-Critique** — systematically searches the system's own decisions and outputs for weaknesses, unsupported assumptions, omissions, and internal inconsistencies.

2. **Adversarial Self-Verification** — explicitly attempts to break the implementation, exploit authority boundaries, manufacture false success, evade evaluation, corrupt provenance, trigger recovery loops, and demonstrate that the architecture's claims are false.

II-017 will also define how these mechanisms themselves are validated so that the architecture does not create a "critic" that merely agrees with the system it is supposed to challenge.
