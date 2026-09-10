# II-010 — Evaluation & Sufficiency Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Evaluation of intelligence-layer outputs, evidence sufficiency, decision quality, and architectural validity

---

## 1. Purpose

II-010 defines how the system evaluates whether outputs produced by the Campaign Intelligence Layer are actually **sufficient, supported, coherent, and valid**.

The central problem is:

> **A system that can generate plausible outputs is not necessarily a system that has generated correct or sufficient outputs.**

Therefore, evaluation must be treated as an independent architectural function rather than as a side effect of generation.

The Evaluation Layer exists to answer:

```text
Did the system produce something plausible?
        ↓
Did it satisfy the requirement?
        ↓
Did it preserve the relevant invariants?
        ↓
Is the supporting evidence sufficient?
        ↓
Can the result survive challenge?
```

---

# 2. Core Principle

> **Generation produces candidate decisions. Evaluation determines whether those decisions satisfy independently defined requirements.**

Therefore:

```text
GENERATION
≠
EVALUATION
```

and:

```text
HIGH GENERATION QUALITY
≠
ARCHITECTURAL CORRECTNESS
```

The evaluator must not simply ask another model:

```text
"Is this good?"
```

without reference to explicit requirements, evidence, and validation criteria.

---

# 3. Evaluation Boundary

The Evaluation Layer evaluates outputs from:

```text
Intent Derivation
Evidence Derivation
Asset Strategy
Narrative Construction
Channel Projection
Prompt Compilation
Generation
```

against:

```text
Authoritative Inputs
Requirements
Constraints
Evidence
Invariants
Evaluation Criteria
```

Canonical structure:

```text
AUTHORITATIVE REQUIREMENTS
        ↓
CANDIDATE OUTPUT
        ↓
EVALUATION
        ↓
PASS / PARTIAL / FAIL / UNCERTAIN
```

---

# 4. Evaluation vs Generation

Generation asks:

> What should we produce?

Evaluation asks:

> Did what we produced satisfy the intended requirement?

The evaluator must not silently modify the candidate output.

Instead:

```text
OUTPUT
    ↓
EVALUATION
    ↓
FINDINGS
    ↓
DECISION
```

If correction is necessary:

```text
EVALUATION
    ↓
FAILURE / CHALLENGE
    ↓
REPLANNING
    ↓
NEW CANDIDATE
```

---

# 5. Evaluation vs Self-Critique

Self-Critique and Evaluation are related but distinct.

## Evaluation

Determines whether a defined requirement is satisfied.

## Self-Critique

Attempts to identify weaknesses, assumptions, omissions, and reasoning failures.

Therefore:

```text
EVALUATION
→ requirement satisfaction

SELF-CRITIQUE
→ weakness discovery
```

A system may pass an evaluation while still receiving a critique.

---

# 6. Evaluation vs Adversarial Verification

Adversarial Verification is intentionally hostile.

```text
Evaluation:
"Does this satisfy the requirement?"

Adversarial Verification:
"How can I demonstrate that this system's
claim of satisfaction is wrong?"
```

Both are required.

---

# 7. Evaluation Object

Conceptually:

```text
evaluation_id
target_id
target_type
requirement_ids
criteria
observations
evidence
result
confidence
authority
evaluator
evaluation_method
failure_modes
timestamp
version
provenance
```

The exact runtime schema remains deferred.

---

# 8. Evaluation Result States

The evaluator should distinguish:

```text
PASS
PARTIAL
FAIL
UNCERTAIN
NOT_EVALUABLE
```

### PASS

The available evidence supports sufficient satisfaction.

### PARTIAL

Some requirements are satisfied, but one or more remain insufficient.

### FAIL

A required condition is clearly violated.

### UNCERTAIN

Available evidence cannot confidently establish pass or fail.

### NOT_EVALUABLE

The requirement cannot currently be evaluated because necessary information or instrumentation is unavailable.

These states must not be collapsed into a binary score.

---

# 9. Sufficiency

Sufficiency means:

> **The available evidence is strong enough, under the defined evaluation criteria, to support the required conclusion.**

Sufficiency is contextual.

```text
Requirement
+
Threshold
+
Evidence
+
Evaluation Method
=
Sufficiency Decision
```

There is no universal visual or semantic sufficiency threshold.

---

# 10. Sufficiency vs Quality

A high-quality artifact can still fail a requirement.

Example:

```text
Beautiful image
+
excellent lighting
+
excellent composition

BUT

required craftsmanship detail is not observable.
```

Result:

```text
VISUAL QUALITY = HIGH
EVIDENCE SUFFICIENCY = FAIL
```

Therefore:

```text
QUALITY ≠ SUFFICIENCY
```

---

# 11. Sufficiency vs Confidence

Confidence represents evaluator certainty.

Sufficiency represents requirement satisfaction.

Example:

```text
Requirement:
Material texture must be visible.

Observation:
Texture appears visible.

Evaluator confidence:
0.62

Sufficiency:
UNCERTAIN
```

High confidence in an incorrect conclusion must not become sufficient evidence.

Therefore:

```text
CONFIDENCE ≠ SUFFICIENCY
```

---

# 12. Evaluation Criteria

Every consequential evaluation should reference explicit criteria.

Criteria may include:

```text
requirement satisfaction
evidence observability
constraint compliance
intent preservation
product truth
brand compliance
narrative coherence
channel compatibility
authenticity
technical validity
```

The exact criteria depend on the evaluated object.

---

# 13. Requirement-to-Evaluation Mapping

Every evaluated result should preserve:

```text
OUTPUT
    ↓
REQUIREMENT
    ↓
CRITERION
    ↓
OBSERVATION
    ↓
RESULT
```

This prevents vague evaluations such as:

```text
"Looks good."
```

without knowing:

```text
good according to what?
```

---

# 14. Observation vs Interpretation

Evaluation should distinguish what was actually observed from what was inferred.

Example:

```text
OBSERVATION:
Visible folds appear present near the elbow.

INTERPRETATION:
The fabric may be exhibiting believable drape behavior.

CONFIDENCE:
Medium.
```

The evaluator must not represent interpretation as direct observation.

---

# 15. Evaluation Evidence

Evaluation evidence may include:

```text
visual observation
structured metadata
source-backed fact
constraint result
model measurement
human assessment
comparison result
simulation result
test output
```

Each evidence item should preserve provenance.

---

# 16. Evaluation Evidence Quality

Evidence used to evaluate an output should itself be assessed.

Potential states:

```text
DIRECT
INDIRECT
WEAK
CONTRADICTORY
MISSING
```

The evaluator should avoid circular validation.

Example:

```text
Generator says:
"Texture is authentic."

Evaluator:
"The generator says texture is authentic."

```

This is not independent evidence.

---

# 17. Independent Evaluation

Whenever possible, evaluation should use information or mechanisms that are meaningfully independent from the generation process.

Independence may exist at different levels:

```text
MODEL INDEPENDENCE
PROMPT INDEPENDENCE
DATA INDEPENDENCE
MEASUREMENT INDEPENDENCE
HUMAN INDEPENDENCE
PROCEDURAL INDEPENDENCE
```

The architecture should not assume that using a second model automatically creates independence.

---

# 18. Evaluator Independence

A critic using the same:

```text
model
prompt
knowledge
assumptions
```

as the generator may reproduce the same failure.

Therefore:

```text
SECOND MODEL
≠
INDEPENDENT VERIFIER
```

Independence must be evaluated structurally.

---

# 19. Multi-Evaluator Evidence

For consequential evaluations, the system may use multiple evaluators:

```text
Evaluator A
+
Evaluator B
+
Human
+
Rule-based check
```

The architecture should preserve each result independently before aggregation.

Do not immediately collapse them into one score.

---

# 20. Evaluation Agreement

If multiple evaluators disagree:

```text
A → PASS
B → FAIL
```

the system should preserve:

```text
DISAGREEMENT
```

rather than automatically averaging it away.

Possible outcomes:

```text
REVIEW
ADDITIONAL EVIDENCE
ADVERSARIAL TEST
HUMAN ESCALATION
```

---

# 21. Evaluation Aggregation

Aggregation may eventually produce:

```text
FINAL EVALUATION STATE
```

but the underlying evidence must remain recoverable.

Conceptually:

```text
EVALUATOR RESULTS
        ↓
AGREEMENT / DISAGREEMENT
        ↓
AGGREGATION
        ↓
FINAL STATE
```

The aggregation function must not erase disagreement.

---

# 22. Hard Constraint Evaluation

Hard constraints should be evaluated deterministically wherever possible.

Example:

```text
Requirement:
No visible brand competitor.

Detection:
Competitor detected.

Result:
FAIL
```

A soft preference should not produce the same failure semantics.

---

# 23. Soft Constraint Evaluation

Soft constraints should be evaluated separately.

Example:

```text
Preferred:
Warm editorial lighting.

Observed:
Neutral lighting.

Result:
SOFT DEVIATION
```

This should not automatically invalidate the entire output.

---

# 24. Requirement Criticality

Requirements may be classified:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

Failure of a critical requirement may invalidate an otherwise strong output.

The evaluator must preserve requirement-level results before calculating any overall state.

---

# 25. Evaluation Coverage

The system should determine whether all relevant requirements were actually evaluated.

Conceptually:

```text
TOTAL REQUIREMENTS
        ↓
EVALUATED
        ↓
NOT EVALUATED
        ↓
PARTIALLY EVALUATED
```

A system must not claim:

```text
PASS
```

for an artifact when critical requirements were never evaluated.

---

# 26. Evaluation Completeness

Evaluation completeness is distinct from output quality.

Example:

```text
Output:
Excellent.

Evaluation:
Only 4 of 10 requirements assessed.
```

Result:

```text
EVALUATION INCOMPLETE
```

not:

```text
PASS
```

---

# 27. Evaluation Blind Spots

The evaluator should explicitly track what it cannot observe.

Examples:

```text
material composition cannot be visually verified
historical claim cannot be validated from image
cultural interpretation cannot be objectively measured
physical durability cannot be inferred from a generated image
```

These should become:

```text
NOT_EVALUABLE
```

rather than fabricated conclusions.

---

# 28. Evaluation Confidence

Confidence should reflect:

```text
evidence quality
observation clarity
method reliability
evaluator agreement
measurement uncertainty
```

Confidence should not be manually inflated to make the system pass.

---

# 29. Evaluation Calibration

Evaluators should eventually be calibrated against known examples.

Conceptually:

```text
KNOWN CASES
        ↓
EVALUATOR PREDICTION
        ↓
GROUND TRUTH / EXPERT LABEL
        ↓
CALIBRATION
```

Calibration should be tracked separately from campaign outputs.

---

# 30. Ground Truth

The architecture must distinguish several forms of ground truth:

```text
OBJECTIVE FACT
EXPERT-ESTABLISHED FACT
USER-AUTHORITATIVE FACT
HUMAN-LABELED JUDGMENT
MEASURED RESULT
PROXY
```

Not every evaluation target has objective ground truth.

The system must not pretend subjective judgments are objective facts.

---

# 31. Human Evaluation

Human evaluation may be required when:

```text
semantic interpretation
aesthetic judgment
cultural nuance
brand coherence
emotional response
creative originality
```

cannot be reliably evaluated automatically.

Human evaluation should preserve:

```text
evaluator identity / role where appropriate
criteria
observations
judgment
confidence
rationale
timestamp
```

Privacy requirements are deferred.

---

# 32. Human Evaluation Aggregation

Multiple human evaluations should preserve disagreement.

Example:

```text
Evaluator A:
Authentic = YES

Evaluator B:
Authentic = UNCERTAIN

Evaluator C:
Authentic = NO
```

The result should expose:

```text
DISAGREEMENT
```

rather than silently selecting a majority without context.

---

# 33. Evaluation Feedback

Evaluation results may trigger:

```text
PASS
        ↓
CONTINUE

PARTIAL
        ↓
REVISE / REPLAN

FAIL
        ↓
REGENERATE / REPLAN

UNCERTAIN
        ↓
GATHER EVIDENCE / ESCALATE

NOT_EVALUABLE
        ↓
INSTRUMENTATION / KNOWLEDGE GAP
```

The evaluator should not directly mutate upstream intelligence.

---

# 34. Evaluation Loop

The architecture should support:

```text
PLAN
 ↓
GENERATE
 ↓
EVALUATE
 ↓
CRITIQUE
 ↓
ADVERSARIAL VERIFY
 ↓
REPLAN
 ↓
GENERATE AGAIN
```

The loop must have bounded iteration controls.

Otherwise:

```text
self-improvement
→ infinite revision
```

becomes possible.

---

# 35. Evaluation Budget

Each evaluation cycle should have limits on:

```text
time
model calls
human reviews
retrieval calls
generation retries
computation
```

Budget policy belongs to runtime engineering.

The semantic contract requires only that evaluation be bounded and observable.

---

# 36. Evaluation Stopping Criteria

A campaign output may be accepted when:

```text
CRITICAL REQUIREMENTS = SUFFICIENT
AND
NO HARD CONSTRAINT VIOLATION
AND
EVALUATION COVERAGE ≥ REQUIRED LEVEL
AND
NO UNRESOLVED CRITICAL ADVERSARIAL FINDING
```

Exact thresholds remain deferred.

---

# 37. Evaluation Escalation

Escalation should occur when:

```text
critical disagreement
+
insufficient evidence
+
high consequence
```

exists.

Possible escalation:

```text
MORE EVIDENCE
SECOND EVALUATOR
EXPERT REVIEW
HUMAN REVIEW
RESEARCH
REPLANNING
```

---

# 38. Evaluation Decision Record

Each final evaluation should preserve:

```text
evaluation_id
target
requirements
criteria
observations
evidence
evaluator_results
disagreements
final_state
confidence
limitations
failure_modes
recommended_action
provenance
version
```

This makes evaluation auditable.

---

# 39. Self-Critique Requirements

The Self-Critique Agent should inspect the evaluation process itself for:

- unsupported conclusions,
- circular evidence,
- missed requirements,
- evaluator overconfidence,
- conflation of quality and sufficiency,
- ignored disagreement,
- hidden assumptions,
- invalid aggregation,
- incomplete evaluation coverage,
- and unjustified PASS decisions.

The critic evaluates the evaluator.

---

# 40. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break the evaluation system by:

1. Creating outputs that appear visually excellent but fail core evidence requirements.
2. Injecting unsupported PASS decisions.
3. Exploiting vague evaluation criteria.
4. Supplying circular evidence.
5. Creating evaluator agreement through shared assumptions.
6. Hiding unevaluated requirements.
7. Converting UNCERTAIN into PASS.
8. Treating subjective judgments as objective ground truth.
9. Exploiting aggregation to hide disagreement.
10. Removing critical requirements from the evaluation set.
11. Producing false confidence.
12. Creating infinite evaluation/revision loops.
13. Exploiting proxy metrics as if they were direct measurements.
14. Manipulating evaluator prompts to produce desired outcomes.
15. Declaring success because the artifact looks plausible rather than because requirements are satisfied.

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

# 41. Validation Invariants

### Invariant 1

Evaluation must reference explicit requirements or criteria.

### Invariant 2

Generation and evaluation remain separate operations.

### Invariant 3

Evaluation evidence must preserve provenance.

### Invariant 4

Circular evidence cannot establish independent validation.

### Invariant 5

Confidence cannot substitute for evidence.

### Invariant 6

Visual quality cannot substitute for requirement satisfaction.

### Invariant 7

Critical requirements must be evaluated before final PASS.

### Invariant 8

Unevaluated critical requirements prevent a complete PASS.

### Invariant 9

Evaluator disagreement remains visible.

### Invariant 10

NOT_EVALUABLE is distinct from PASS, FAIL, and UNCERTAIN.

### Invariant 11

Hard constraint failures cannot be hidden by aggregate quality.

### Invariant 12

Soft preference deviations cannot automatically be treated as hard failures.

### Invariant 13

Self-Critique cannot silently rewrite evaluation results.

### Invariant 14

Adversarial findings cannot silently disappear.

### Invariant 15

Every accepted result preserves an auditable decision record.

### Invariant 16

Evaluation loops must be bounded.

---

# 42. Falsifiable Architectural Hypotheses

## Hypothesis A — Requirement-grounded evaluation reduces false PASS decisions

**Claim:**

Evaluation tied to explicit requirements produces fewer false positive approvals than holistic quality judgment.

**Experiment:**

Compare:

```text
System A:
"Is this image good?"

System B:
Requirement-by-requirement evaluation
```

Measure:

- false PASS rate,
- missed critical failures,
- evaluator agreement.

---

## Hypothesis B — Independent evaluation reduces correlated failure

**Claim:**

Evaluation mechanisms with meaningful independence identify failures missed by the generator.

**Experiment:**

Compare:

```text
same-model self-evaluation
vs
independent evaluator
vs
rule + model + human evaluation
```

Measure:

- failure discovery rate,
- false PASS rate,
- correlated errors.

---

## Hypothesis C — Explicit NOT_EVALUABLE reduces fabricated certainty

**Claim:**

Allowing the evaluator to abstain produces better calibration than forcing binary judgments.

**Experiment:**

Provide cases where required properties cannot actually be observed.

Measure:

```text
fabricated PASS
vs
appropriate abstention
```

---

## Hypothesis D — Requirement coverage prevents incomplete evaluation

**Claim:**

Explicit evaluation coverage tracking reduces cases where systems declare success after evaluating only easy requirements.

**Experiment:**

Create campaigns with hidden critical requirements.

Measure whether the system identifies incomplete evaluation.

---

## Hypothesis E — Adversarial evaluation reveals evaluator blind spots

**Claim:**

A dedicated adversarial verifier identifies failure modes that ordinary evaluation misses.

**Experiment:**

Run:

```text
normal evaluation
vs
normal + adversarial verification
```

Measure newly discovered critical failures.

---

## Hypothesis F — Independent evaluator diversity improves calibration

**Claim:**

Combining meaningfully different evaluation mechanisms improves reliability more than simply adding additional instances of the same evaluator.

**Experiment:**

Compare:

```text
3 identical model evaluators
vs
rule-based + model + human
```

Measure agreement, calibration, and failure discovery.

---

# 43. Architecture Validation

The Evaluation Layer is itself an object of evaluation.

The system must eventually be able to ask:

```text
Is our evaluator reliable?
```

Therefore evaluation infrastructure should be tested against:

```text
KNOWN FAILURES
KNOWN PASSES
AMBIGUOUS CASES
ADVERSARIAL CASES
DISTRIBUTION SHIFTS
```

This is necessary before evaluator outputs are treated as evidence for architectural correctness.

---

# 44. Proving the Intelligence Architecture

II-010 establishes the first formal bridge toward proving the architecture.

The architecture should not be considered validated because:

```text
outputs look good
```

or:

```text
agents agree
```

Instead, evidence should accumulate across:

```text
ARCHITECTURAL HYPOTHESES
        ↓
DEFINED TESTS
        ↓
KNOWN TEST CASES
        ↓
MEASURED RESULTS
        ↓
REPLICATION
        ↓
FAILURE ANALYSIS
        ↓
CALIBRATION
```

The resulting evidence should support or falsify specific claims.

---

# 45. Object Authority Evaluation

Object authority should eventually be evaluated through:

```text
AUTHORITY CLAIM
        ↓
DEFINED SCOPE
        ↓
SOURCE / PROVENANCE
        ↓
INDEPENDENT SUPPORT
        ↓
CONFLICT TEST
        ↓
ADVERSARIAL CHALLENGE
        ↓
AUTHORITY STATUS
```

The system must not prove authority merely because:

```text
the object says it is authoritative
```

or:

```text
the LLM assigns high confidence.
```

---

# 46. Architecture-Level Metrics

Potential architecture-level metrics include:

```text
FALSE PASS RATE
FALSE FAIL RATE
ABSTENTION RATE
CRITICAL FAILURE DETECTION RATE
REQUIREMENT COVERAGE
PROVENANCE COMPLETENESS
AUTHORITY CALIBRATION
STRATEGIC DRIFT RATE
ADVERSARIAL FAILURE RATE
EVALUATOR AGREEMENT
REPLANNING SUCCESS RATE
```

These are candidate metrics, not yet frozen.

---

# 47. Evaluation Dataset

The architecture should eventually maintain a controlled evaluation corpus containing:

```text
KNOWN_GOOD CASES
KNOWN_BAD CASES
EDGE CASES
CONFLICT CASES
AMBIGUOUS CASES
ADVERSARIAL CASES
REGRESSION CASES
```

Each test case should preserve:

```text
input
requirements
expected properties
known failure modes
evaluation criteria
ground-truth type
expected outcome
```

---

# 48. Regression Evaluation

Every significant intelligence-layer change should be evaluated against prior cases.

Conceptually:

```text
VERSION N
    ↓
TEST CORPUS
    ↓
VERSION N+1
    ↓
COMPARISON
```

A new version should not be considered improved merely because it performs better on new examples.

It must also avoid regressions on established cases.

---

# 49. Evaluation Provenance

The system should preserve:

```text
MODEL VERSION
PROMPT / POLICY VERSION
KNOWLEDGE VERSION
EVALUATION RULE VERSION
INPUT VERSION
OUTPUT VERSION
TIMESTAMP
```

This makes results reproducible.

---

# 50. Evaluation Reproducibility

Where deterministic reproduction is impossible because of stochastic generation, the system should preserve enough information to reproduce the **evaluation conditions** and compare distributions or repeated trials.

The architecture must not falsely claim exact reproducibility when stochastic components prevent it.

---

# 51. Evaluation vs Benchmarking

Benchmarking compares systems or versions.

Evaluation determines whether a specific requirement is satisfied.

Therefore:

```text
EVALUATION
→ requirement satisfaction

BENCHMARK
→ comparative performance
```

Both may be used later.

---

# 52. Evaluation vs User Preference

User preference is valuable evidence but must remain distinct from objective requirement satisfaction.

Example:

```text
User prefers:
Image A.

Requirement evaluation:
Image B better satisfies material evidence.
```

The system should preserve both:

```text
OBJECTIVE / REQUIREMENT RESULT
USER PREFERENCE
```

rather than silently treating preference as proof.

---

# 53. Core Contract

> **The Evaluation Engine shall independently determine whether generated intelligence, assets, narratives, projections, and related outputs satisfy their explicit requirements and constraints using traceable evidence, observable criteria, calibrated confidence, and bounded evaluation procedures. It shall distinguish sufficiency from quality, confidence from correctness, evaluation from self-critique, and ordinary evaluation from adversarial verification; preserve disagreement and abstention; prevent circular validation; evaluate its own reliability; and generate measurable evidence that can support or falsify claims about the intelligence architecture itself.**

---

# 54. Deferred Decisions

II-010 does not freeze:

- exact evaluator models,
- scoring equations,
- calibration methods,
- benchmark dataset size,
- human-review protocol,
- statistical significance thresholds,
- aggregation algorithms,
- evaluator independence architecture,
- automated visual measurement stack,
- experiment orchestration infrastructure.

These remain subjects for later specifications.

---

# 55. Exit Criteria

II-010 is semantically complete when:

- [x] Evaluation boundary established
- [x] Generation / evaluation separation established
- [x] Evaluation / self-critique separation established
- [x] Evaluation / adversarial verification separation established
- [x] PASS / PARTIAL / FAIL / UNCERTAIN / NOT_EVALUABLE states established
- [x] Sufficiency model established
- [x] Quality / sufficiency distinction established
- [x] Confidence / sufficiency distinction established
- [x] Requirement-to-evaluation mapping established
- [x] Observation / interpretation distinction established
- [x] Evidence provenance established
- [x] Independent evaluation principle established
- [x] Multi-evaluator disagreement handling established
- [x] Hard / soft constraint evaluation established
- [x] Evaluation coverage established
- [x] Evaluation completeness established
- [x] Blind-spot handling established
- [x] Ground-truth taxonomy established provisionally
- [x] Human evaluation boundary established
- [x] Evaluation loop established
- [x] Evaluation budget / stopping principles established
- [x] Escalation established
- [x] Decision record established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Architecture-level validation established
- [x] Object-authority evaluation established
- [x] Evaluation dataset principles established
- [x] Regression evaluation established
- [x] Reproducibility principles established
- [x] Benchmarking boundary established
- [x] User-preference boundary established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-011 — Replanning & Decision Recovery Contract**

This specification will define what the system does when evaluation, self-critique, adversarial verification, knowledge gaps, or constraint conflicts show that the current plan is insufficient or invalid.
