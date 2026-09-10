# IV-009 — Verification Runtime, Evaluation Harness & Experimental Control Specification

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-006, IV-007, IV-008, III-004, III-009, III-010, III-012, III-013, III-015

---

# 1. Purpose

IV-009 defines the controlled experimental infrastructure required to execute verification, evaluation, adversarial testing, failure injection, and assurance experiments reproducibly.

The central problem is:

```text
"WE TESTED IT"
```

is not sufficient.

We must be able to answer:

```text
WHAT WAS TESTED?
WHICH VERSION?
UNDER WHICH ENVIRONMENT?
WITH WHICH MODEL?
WITH WHICH DATA?
WITH WHICH TOOLS?
WITH WHICH RANDOM SEED?
UNDER WHICH THREAT MODEL?
USING WHICH PROTOCOL?
WHO / WHAT JUDGED THE RESULT?
WHAT EVIDENCE WAS CAPTURED?
CAN THE RESULT BE REPLAYED?
```

The target execution chain is:

```text
EXPERIMENT SPECIFICATION
        ↓
EXACT TARGET VERSION
        ↓
CONTROLLED ENVIRONMENT
        ↓
PINNED DEPENDENCIES
        ↓
TEST / ATTACK / EVALUATION
        ↓
OBSERVATION
        ↓
EVIDENCE CAPTURE
        ↓
INDEPENDENT JUDGE
        ↓
RESULT
        ↓
REPLAY / REGRESSION
        ↓
ASSURANCE UPDATE
```

---

# 2. Core Principle

Experimental evidence is only useful to the extent that the experiment itself is reconstructable.

Therefore:

```text
RESULT
WITHOUT
EXPERIMENT PROVENANCE
=
WEAK EVIDENCE
```

The runtime must make experimental provenance a first-class object.

---

# 3. Source Basis

IV-009 operationalizes the verification and falsification architecture established in:

```text
IV-006 — Evidence, Verification, Self-Critique & Adversarial Self-Verification Architecture
IV-007 — Coverage, Assurance-Gap & Implementation Verification Matrix
IV-008 — System-Wide Falsification, Red-Team Protocol & Failure-Injection Specification
```

The document also inherits:

```text
provenance requirements
authority constraints
lifecycle semantics
security isolation
self-modification governance
assurance invalidation
```

from the preceding architectural contracts.

---

# 4. Experimental Control Model

Every controlled experiment should have:

```yaml
experiment:
  experiment_id: ...
  experiment_version: ...
  objective: ...
  claim_refs: []
  target_ref: ...
  target_version: ...
  environment_ref: ...
  dependency_lock_ref: ...
  dataset_refs: []
  model_refs: []
  tool_refs: []
  seed: ...
  protocol_ref: ...
  threat_model_ref: ...
  evaluator_ref: ...
  judge_ref: ...
  evidence_policy_ref: ...
```

---

# 5. Experiment Identity

Every experiment must have a unique identity.

Conceptually:

```text
EXPERIMENT_ID
+
EXPERIMENT_VERSION
+
TARGET_VERSION
```

must be sufficient to distinguish one run from another.

Experiment identity must never depend only on a human-readable name.

---

# 6. Target Version Pinning

A result must identify exactly what was evaluated.

Pin:

```text
application version
component versions
contract version
policy version
configuration version
model version
prompt version
tool version
dataset version
evaluation protocol version
```

where relevant.

---

# 7. Reproducibility Levels

Candidate reproducibility levels:

```text
R0 — NOT REPRODUCIBLE
R1 — PROCEDURALLY REPEATABLE
R2 — ENVIRONMENT REPRODUCIBLE
R3 — DETERMINISTIC REPLAYABLE
R4 — INDEPENDENTLY REPRODUCIBLE
```

These are proposed engineering labels.

A probabilistic experiment may not achieve deterministic replay while still being procedurally reproducible.

---

# 8. Determinism vs Reproducibility

These must remain separate.

```text
DETERMINISM
=
same inputs → same outputs
```

while:

```text
REPRODUCIBILITY
=
another authorized run can reconstruct
the relevant experiment conditions.
```

A stochastic system can therefore be reproducible without producing identical outputs.

---

# 9. Environment Isolation

Experiments should execute inside controlled environments where appropriate:

```text
sandbox
container
VM
isolated process
simulation
staging environment
```

The isolation level must correspond to experiment risk.

---

# 10. Production Safety

Adversarial and failure-injection experiments must default to:

```text
NON-PRODUCTION
```

Production testing requires explicit authorization and a narrowly bounded protocol.

The experimental runtime must prevent accidental crossing from:

```text
TEST ENVIRONMENT
```

into:

```text
REAL-WORLD EXECUTION
```

---

# 11. Resource Isolation

Experiments may require isolated:

```text
CPU
memory
GPU
filesystem
network
credentials
secrets
processes
ports
devices
```

The runtime should expose only the minimum resources required by the experiment.

---

# 12. Credential Isolation

Experimental credentials must be:

```text
scoped
temporary
revocable
auditable
environment-specific
```

A red-team experiment must not accidentally inherit unrestricted production credentials.

---

# 13. Network Isolation

Experiments should support:

```text
offline mode
allowlisted network
simulated network
restricted egress
restricted ingress
```

The default should be the narrowest network capability compatible with the experiment.

---

# 14. Tool Isolation

Tools should be represented as explicit experiment dependencies.

Conceptually:

```yaml
tool:
  tool_id: ...
  version: ...
  capability_scope: ...
  authorization_ref: ...
  environment_ref: ...
```

A tool must not be treated as an implicitly trusted extension of the model.

---

# 15. Tool Simulation

Where real execution is unnecessary, use:

```text
mock
stub
simulator
record/replay
deterministic fixture
```

This reduces:

```text
risk
cost
non-determinism
```

while preserving test intent.

---

# 16. Tool Record / Replay

For experiments involving external tools:

```text
REQUEST
 ↓
TOOL RESPONSE
 ↓
OBSERVED SIDE EFFECT
```

should be capturable.

Replay should allow the experiment to reuse a known tool interaction without requiring real-world side effects.

---

# 17. Model Pinning

Every model-based evaluation should preserve:

```text
provider
model identifier
model version / snapshot where available
system prompt
developer instructions
evaluation prompt
generation parameters
context configuration
tool configuration
```

where applicable.

---

# 18. Model Configuration

Record:

```text
temperature
top-p
max tokens
sampling configuration
reasoning configuration
tool choice configuration
structured-output constraints
```

where applicable.

A model result without configuration metadata may be difficult to reproduce.

---

# 19. Prompt Pinning

Prompts are experimental dependencies.

Record:

```text
prompt identity
prompt version
prompt hash
system instructions
evaluation instructions
attack instructions
```

Prompt changes may materially change evaluation results.

---

# 20. Dataset Pinning

Every evaluation dataset must identify:

```text
dataset_id
version
source
snapshot
preprocessing
filtering
sampling
split
```

where applicable.

---

# 21. Hidden Evaluation Data

Hidden evaluation data should remain inaccessible to the system under test when the purpose is to measure generalization.

The harness must prevent accidental leakage of:

```text
answers
expected labels
attack cases
hidden counterexamples
evaluation metadata
```

---

# 22. Seed Management

Where randomness exists, record:

```text
global seed
component seeds
data sampling seed
attack-generation seed
model sampling seed
fuzzing seed
```

where supported.

---

# 23. Seed Independence

Repeated experiments should distinguish:

```text
same seed
different seed
randomized seed
```

This helps identify:

```text
seed-sensitive behavior
```

rather than treating one successful run as representative.

---

# 24. Experiment Matrix

A serious evaluation should often run:

```text
target versions
×
models
×
datasets
×
seeds
×
attack strategies
```

The experiment matrix must be explicitly defined.

---

# 25. Evaluation Harness

The evaluation harness is responsible for:

```text
environment preparation
target initialization
input delivery
tool configuration
observation
oracle execution
evidence capture
cleanup
result generation
```

It should not silently alter the target under evaluation.

---

# 26. Harness Separation

Where possible:

```text
TARGET
≠
HARNESS
≠
JUDGE
```

The same component should not be solely responsible for:

```text
producing
testing
judging
certifying
```

a high-impact result.

---

# 27. Experiment Orchestrator

Conceptually:

```text
EXPERIMENT SPEC
        ↓
ORCHESTRATOR
        ├── environment
        ├── target
        ├── dataset
        ├── model
        ├── tools
        ├── attack
        └── judge
```

The orchestrator should produce a complete execution record.

---

# 28. Preflight Checks

Before execution verify:

```text
target version pinned
environment available
dependencies resolved
dataset version correct
model configuration correct
tools authorized
credentials scoped
seed recorded
protocol valid
safety boundary active
```

A failed preflight should prevent the experiment from being marked valid.

---

# 29. Experiment State Machine

Candidate states:

```text
DEFINED
 ↓
VALIDATED
 ↓
READY
 ↓
RUNNING
 ↓
OBSERVING
 ↓
JUDGING
 ↓
COMPLETED
```

Failure states:

```text
BLOCKED
ABORTED
INVALID
INCONCLUSIVE
REQUIRES_REPLAY
```

---

# 30. Invalid Experiment

An experiment should be marked invalid when a required precondition was violated.

Examples:

```text
wrong target version
wrong dataset
missing evidence
unauthorized tool
incorrect model configuration
broken isolation
missing seed where required
```

Invalid results must not be silently included in assurance calculations.

---

# 31. Observation Model

Capture both:

```text
EXPECTED OBSERVATION
OBSERVED OBSERVATION
```

where applicable.

The harness should avoid reducing the raw observation to a single pass/fail bit before evidence is preserved.

---

# 32. Raw Evidence

Preserve raw artifacts where appropriate:

```text
inputs
outputs
logs
tool calls
tool responses
state snapshots
metrics
traces
screenshots
structured records
counterexamples
```

Retention must follow security and privacy requirements.

---

# 33. Derived Evidence

Derived artifacts may include:

```text
classification
score
metric
coverage
failure label
severity
judge result
assurance status
```

Derived evidence should retain references to the raw evidence from which it was computed.

---

# 34. Evidence Hashing

Where integrity requires it, evidence artifacts should have integrity identifiers such as:

```text
content hash
artifact digest
immutable object identifier
```

The objective is to detect post-experiment modification.

---

# 35. Evidence Chain

The target chain is:

```text
EXPERIMENT
 ↓
RUN
 ↓
OBSERVATION
 ↓
RAW EVIDENCE
 ↓
DERIVED EVIDENCE
 ↓
JUDGMENT
 ↓
ASSURANCE
```

Each stage must remain traceable.

---

# 36. Experiment Provenance

Experiment provenance should preserve:

```text
who initiated
what was run
when it ran
where it ran
which versions
which dependencies
which data
which model
which tools
which configuration
which results
```

---

# 37. Initiator Identity

Record whether the experiment was initiated by:

```text
human
scheduled system
evaluation agent
red-team agent
regression pipeline
assurance pipeline
```

Initiator identity must not be confused with evaluator identity.

---

# 38. Evaluator Identity

Record:

```text
evaluator type
evaluator version
evaluation protocol
evaluation criteria
```

Examples:

```text
deterministic checker
LLM evaluator
human reviewer
hybrid judge
```

---

# 39. Judge Separation

For high-impact claims, the judge should be as independent as practical from the target.

Example:

```text
TARGET MODEL
        ↓
OUTPUT
        ↓
INDEPENDENT JUDGE
        ↓
RESULT
```

If the judge shares major failure modes with the target, record the limitation.

---

# 40. Deterministic Oracle

Use deterministic oracles whenever the expected property is deterministic.

Examples:

```text
schema validity
authority scope
expiration
revocation
state transition
cryptographic integrity
required field presence
```

---

# 41. Semantic Oracle

For properties that require interpretation:

```text
semantic consistency
reasoning quality
ambiguity
goal alignment
qualitative correctness
```

use:

```text
LLM evaluator
human evaluator
hybrid evaluator
```

with explicit limitations.

---

# 42. Oracle Independence

An oracle should not rely on the same uncertain mechanism it is supposed to evaluate unless the correlation is explicitly accepted.

For example:

```text
MODEL A produces answer
MODEL A evaluates answer
```

is not strong independent evaluation.

---

# 43. Multi-Judge Evaluation

For high-impact experiments, use:

```text
deterministic oracle
+
semantic judge
+
independent evaluator
```

where appropriate.

Disagreement should generate:

```text
INCONCLUSIVE
```

or:

```text
REVIEW_REQUIRED
```

rather than automatic majority-based truth.

---

# 44. Judge Calibration

Evaluators should be tested against:

```text
known correct cases
known incorrect cases
ambiguous cases
adversarial cases
```

to estimate:

```text
false positives
false negatives
consistency
```

---

# 45. Benchmark Registry

The system should maintain a registry of:

```yaml
benchmark:
  benchmark_id: ...
  version: ...
  purpose: ...
  claims: []
  datasets: []
  attack_classes: []
  expected_outputs: ...
  evaluation_protocol: ...
  known_limitations: []
```

---

# 46. Benchmark Immutability

Once used for a published or assurance-critical result, the benchmark version must remain identifiable.

Changing the benchmark silently creates:

```text
evaluation drift
```

---

# 47. Benchmark Evolution

New benchmark versions should be represented explicitly:

```text
Benchmark v1
Benchmark v2
Benchmark v3
```

Historical results must remain associated with their original benchmark version.

---

# 48. Regression Suite

Every confirmed material counterexample from IV-008 should be eligible for inclusion in:

```text
regression suite
```

The regression harness should preserve:

```text
original failure
expected fixed behavior
target version
reproduction
```

---

# 49. Failure Replay

The runtime should support:

```text
load original experiment
 ↓
load original target version
 ↓
load original environment
 ↓
load original inputs
 ↓
replay
 ↓
compare behavior
```

This is essential for verifying repairs.

---

# 50. Replay Fidelity

Replay should report:

```text
EXACT
APPROXIMATE
NON-REPRODUCIBLE
```

A replay should never be presented as exact when relevant dependencies changed.

---

# 51. Differential Replay

After a repair:

```text
OLD VERSION
      vs
NEW VERSION
```

run the same experiment.

Compare:

```text
behavior
failure
security state
authority state
evidence
```

---

# 52. Regression Acceptance

A repair is not complete merely because:

```text
original failure disappears.
```

Also verify:

```text
no new regression
no security weakening
no authority bypass
no unrelated behavior corruption
```

---

# 53. Experiment Scheduling

The evaluation runtime may support:

```text
on-demand
commit-triggered
release-triggered
nightly
periodic
risk-triggered
counterexample-triggered
```

Scheduling is an execution concern and must not alter assurance semantics.

---

# 54. Experiment Priority

Prioritize by:

```text
claim criticality
recent change
known failure
security risk
authority impact
uncertainty
dependency centrality
```

---

# 55. Continuous Evaluation

For continuously changing systems:

```text
CHANGE
 ↓
AFFECTED CLAIMS
 ↓
AFFECTED EXPERIMENTS
 ↓
RE-RUN
 ↓
COMPARE
 ↓
ASSURANCE UPDATE
```

This prevents stale evidence from being treated as current evidence.

---

# 56. Change Impact Analysis

A change should identify:

```text
affected components
affected contracts
affected datasets
affected models
affected tools
affected experiments
affected assurance records
```

Not every change requires the entire suite.

---

# 57. Experiment Dependency Graph

Experiments themselves have dependencies:

```text
benchmark
 ↓
dataset
 ↓
target
 ↓
environment
 ↓
tool
 ↓
judge
```

A dependency change may invalidate an experiment result.

---

# 58. Experiment Invalidation

An experiment should become stale when a material dependency changes.

Candidate triggers:

```text
target version change
model change
prompt change
policy change
dataset change
tool change
judge change
environment change
security configuration change
```

---

# 59. Experiment Evidence Lifecycle

```text
CREATED
 ↓
VALIDATED
 ↓
EXECUTED
 ↓
EVIDENCE SEALED
 ↓
EVALUATED
 ↓
REFERENCED BY ASSURANCE
 ↓
SUPERSEDED / INVALIDATED
```

Historical evidence should remain reconstructable.

---

# 60. Evidence Retention

Retention should consider:

```text
security
privacy
storage
regulatory requirements
research value
assurance lifetime
```

Sensitive raw artifacts may require restricted access while retaining sufficient metadata for audit.

---

# 61. Access Control

Experimental records should distinguish:

```text
creator
executor
evaluator
reviewer
assurance authority
administrator
```

No single role should silently gain all privileges in high-impact environments.

---

# 62. Audit Logging

Record:

```text
experiment creation
configuration changes
execution
abort
evidence access
judgment
assurance update
replay
deletion / retention events
```

---

# 63. Tamper Detection

Critical experiment metadata should be protected against:

```text
result alteration
timestamp manipulation
evaluator substitution
evidence deletion
configuration rewriting
```

---

# 64. Experiment Attestation

Where practical, the runtime should produce an attestation describing:

```text
target
environment
configuration
dependencies
execution status
evidence identifiers
```

This does not prove experiment correctness; it proves what the runtime reports having executed.

---

# 65. Environment Attestation

Record:

```text
OS
runtime
container image
libraries
hardware class
GPU configuration
network mode
filesystem configuration
```

where relevant to reproducibility.

---

# 66. Dependency Locking

Critical dependencies should be pinned.

Examples:

```text
package version
container digest
model version
tool version
benchmark version
dataset snapshot
```

Floating dependencies weaken reproducibility.

---

# 67. Floating Dependency Detection

The harness should warn or fail preflight when an assurance-critical experiment depends on:

```text
latest
unversioned
floating tag
unlocked package
unversioned model
```

unless explicitly permitted.

---

# 68. Experimental Configuration

Configurations should be version-controlled.

Avoid relying on:

```text
manual undocumented settings
local machine state
implicit environment variables
```

for assurance-critical experiments.

---

# 69. Configuration Hash

A configuration identity may be derived from:

```text
experiment parameters
model parameters
environment parameters
tool parameters
dataset references
```

to detect configuration drift.

---

# 70. Run Manifest

Every run should generate a manifest:

```yaml
run_manifest:
  run_id: ...
  experiment_id: ...
  started_at: ...
  completed_at: ...
  target: ...
  target_version: ...
  environment: ...
  dependencies: []
  models: []
  datasets: []
  tools: []
  seed: ...
  protocol: ...
  judge: ...
  evidence_refs: []
  result: ...
```

---

# 71. Experiment Result

Conceptually:

```yaml
experiment_result:
  run_id: ...
  status: ...
  outcome: ...
  observations: []
  evidence_refs: []
  failures: []
  metrics: {}
  judge_ref: ...
  reproducibility_level: ...
  limitations: []
```

---

# 72. Result States

Candidate result states:

```text
PASS
FAIL
INCONCLUSIVE
INVALID
ABORTED
ERROR
REQUIRES_REVIEW
```

`PASS` must not mean universal correctness.

It means:

```text
acceptance condition satisfied
under the specified experiment.
```

---

# 73. Statistical Experiments

For stochastic evaluations preserve:

```text
sample count
seed strategy
sampling method
aggregation method
variance
confidence intervals where appropriate
```

A single run should not be treated as a population estimate.

---

# 74. Repeated Runs

For stochastic claims, use:

```text
multiple independent seeds
```

where appropriate.

Report:

```text
mean
variance
distribution
failure frequency
```

rather than only:

```text
best run
```

---

# 75. Experimental Power

Where statistical claims matter, experiment design should consider:

```text
effect size
sample size
variance
desired confidence
```

The system must not imply strong statistical evidence from an underpowered experiment.

---

# 76. Benchmark Contamination

Monitor for:

```text
training contamination
evaluation leakage
prompt leakage
benchmark memorization
```

where relevant.

A benchmark result may overstate generalization if the target has effectively seen the evaluation material.

---

# 77. Attack-Set Contamination

The adversarial verifier must not be given the hidden attack set during normal evaluation.

Otherwise:

```text
attack success
```

may measure memorization rather than adversarial robustness.

---

# 78. Blind Evaluation

For high-value evaluations:

```text
target
```

should not receive unnecessary information about:

```text
test identity
expected answer
attack strategy
judge criteria
hidden failure class
```

---

# 79. Double-Blind Evaluation

Where practical:

```text
target team
≠
evaluator
```

and:

```text
evaluator
```

may be blinded to the expected outcome.

This reduces confirmation bias.

---

# 80. Evaluation Leakage Controls

The harness should explicitly control:

```text
prompt contents
tool metadata
benchmark labels
hidden test identifiers
filesystem access
environment variables
network endpoints
```

---

# 81. Failure Injection Safety

Failure injection should have:

```text
maximum blast radius
automatic timeout
automatic cleanup
kill mechanism
resource limit
credential revocation
```

---

# 82. Experiment Timeout

Every experiment should define:

```text
maximum runtime
maximum resource consumption
maximum tool calls
maximum attack attempts
```

to prevent runaway evaluation.

---

# 83. Kill Switch

Critical experimental environments should provide an emergency stop:

```text
STOP EXPERIMENT
 ↓
BLOCK EXECUTION
 ↓
REVOKE TEMPORARY AUTHORITY
 ↓
CAPTURE STATE
 ↓
PRESERVE EVIDENCE
```

---

# 84. Cleanup

After execution:

```text
temporary credentials revoked
temporary files removed
processes terminated
network permissions removed
sandbox reset
```

Evidence required for audit must be retained separately.

---

# 85. Experiment Snapshot

For important runs, capture:

```text
pre-run state
post-run state
failure state
```

where permitted.

This supports state-difference analysis.

---

# 86. State Diff

A run should support:

```text
BEFORE
vs
AFTER
```

comparison for:

```text
authority
policy
memory
provenance
security state
lifecycle state
configuration
```

---

# 87. Experimental Side Effects

Record:

```text
intended side effects
unexpected side effects
external calls
state mutations
resource changes
```

Unexpected side effects must be treated as findings when they violate experiment scope.

---

# 88. Judge Override

Human override may be required for ambiguous results.

If used, record:

```text
original result
override
reviewer
reason
evidence
```

Do not silently overwrite the original machine result.

---

# 89. Inconclusive Results

The harness must support:

```text
INCONCLUSIVE
```

when:

```text
judge disagreement
insufficient evidence
environment instability
non-reproducible observation
ambiguous expected behavior
```

Inconclusive is not equivalent to pass.

---

# 90. Experimental Failure vs System Failure

Distinguish:

```text
EXPERIMENT FAILED
```

from:

```text
SYSTEM FAILED
```

For example:

```text
environment crashed
```

may mean:

```text
experiment invalid
```

rather than:

```text
target violated the claim.
```

The judge must classify the distinction.

---

# 91. Harness Failure Testing

The harness itself must be tested.

Inject:

```text
missing evidence
wrong target
wrong dataset
wrong judge
corrupted configuration
broken isolation
incorrect seed
```

and verify that the harness detects the problem.

---

# 92. Evaluation Infrastructure as a Trusted Computing Base

The evaluation runtime becomes part of the assurance infrastructure.

Therefore its own properties matter:

```text
integrity
isolation
reproducibility
auditability
correctness
availability
```

The system should avoid treating the harness as an unquestioned oracle.

---

# 93. Harness Self-Verification

Use:

```text
known experiments
known failures
configuration mutation
evidence mutation
target substitution
judge substitution
```

to verify that the harness correctly identifies:

```text
what was run
what was observed
what was judged
```

---

# 94. Experiment Integrity Chain

Target:

```text
EXPERIMENT SPEC HASH
        ↓
ENVIRONMENT ID
        ↓
CONFIGURATION HASH
        ↓
RUN ID
        ↓
EVIDENCE HASHES
        ↓
JUDGE RESULT
        ↓
ASSURANCE RECORD
```

This makes the experimental chain auditable.

---

# 95. Reproducibility Package

For important results, preserve enough information to reconstruct:

```text
experiment definition
target version
environment
dependencies
data
model configuration
tool fixtures
seed strategy
protocol
judge
evidence
```

This is the minimum research artifact for serious claims.

---

# 96. Independent Reproduction

The strongest experimental evidence should ideally be reproducible by:

```text
different operator
different environment
independent evaluator
```

without requiring undocumented knowledge.

---

# 97. Reproduction Failure

If an independent reproduction fails, classify:

```text
TARGET DIFFERENCE
ENVIRONMENT DIFFERENCE
DATA DIFFERENCE
MODEL DIFFERENCE
TOOL DIFFERENCE
RANDOMNESS
HARNESS DEFECT
ORIGINAL RESULT DEFECT
```

The original result may require reassessment.

---

# 98. Evidence Confidence

Evidence quality should not be reduced to a single confidence score.

Instead preserve dimensions:

```text
reproducibility
independence
integrity
coverage
freshness
validity
```

---

# 99. Integration With Assurance

The evaluation runtime feeds IV-006 through:

```text
evidence
verification records
counterexamples
reproducibility metadata
independence metadata
```

IV-007 consumes these through:

```text
coverage
gap status
claim promotion/demotion
```

IV-008 consumes them through:

```text
attack replay
failure regression
campaign evidence
```

---

# 100. End-to-End Experimental Loop

```text
CLAIM
 ↓
PROOF OBLIGATION
 ↓
EXPERIMENT SPECIFICATION
 ↓
PRE-FLIGHT
 ↓
CONTROLLED EXECUTION
 ↓
RAW OBSERVATION
 ↓
EVIDENCE CAPTURE
 ↓
JUDGMENT
 ↓
REPRODUCTION
 ↓
ASSURANCE UPDATE
 ↓
REGRESSION / MONITORING
```

---

# 101. Minimum Viable Verification Runtime

The first implementation does not need every advanced feature.

Minimum viable capabilities:

```text
experiment registry
target version pinning
environment isolation
configuration capture
seed capture
model/config capture
dataset references
tool isolation
run manifest
raw evidence capture
deterministic judge
result classification
replay
regression linkage
```

---

# 102. Advanced Capabilities

Later additions:

```text
distributed experiment orchestration
automatic attack generation
adaptive fuzzing
multi-model evaluation
double-blind evaluation
automated independence analysis
formal environment attestation
large-scale benchmark scheduling
automatic assurance propagation
```

---

# 103. Build Order

Recommended engineering order:

```text
1. Experiment schema
2. Run registry
3. Version pinning
4. Environment isolation
5. Preflight validation
6. Evidence capture
7. Deterministic judge
8. Replay
9. Regression linkage
10. Model evaluation harness
11. Adversarial harness
12. Independent judge
13. Benchmark registry
14. Statistical experiment support
15. Assurance integration
```

---

# 104. Do Not Build Distributed Infrastructure First

The first runtime should prioritize:

```text
correctness
reproducibility
auditability
isolation
```

over:

```text
scale
throughput
complex orchestration
```

A fast experiment that cannot be trusted is less valuable than a slow experiment that can be reconstructed.

---

# 105. Minimum Trusted Core

The initial trusted experimental core should be as small as practical:

```text
experiment identity
target selection
environment setup
configuration capture
execution
evidence capture
judge
result
replay
```

Every additional automation should be evaluated for whether it introduces new failure modes.

---

# 106. Runtime Security Boundary

The verification runtime must itself enforce:

```text
experiment authorization
resource limits
credential isolation
network restrictions
target isolation
evidence integrity
auditability
```

The experiment cannot be allowed to redefine these controls from inside the experiment.

---

# 107. Verification Runtime vs Target Authority

The target under evaluation must not automatically inherit authority from the verification runtime.

Conceptually:

```text
VERIFICATION AUTHORITY
        ≠
TARGET EXECUTION AUTHORITY
```

This prevents evaluation infrastructure from becoming an accidental privilege-escalation channel.

---

# 108. Evidence Access Boundary

The target should not be able to modify its own:

```text
evaluation result
evidence ledger
judge result
assurance status
```

unless a separate authorized mechanism explicitly permits it.

---

# 109. Self-Modification Evaluation

A self-modifying target should be evaluated as:

```text
BASE VERSION
 ↓
PROPOSED CHANGE
 ↓
ISOLATED TEST
 ↓
VERIFICATION
 ↓
ADVERSARIAL TEST
 ↓
INDEPENDENT JUDGE
 ↓
RESULT
```

The proposed change must not silently alter the evaluation protocol itself.

---

# 110. Experiment Protocol Immutability

Once an assurance-critical experiment begins:

```text
protocol
target
judge
acceptance criteria
```

should not be modifiable by the target.

Any change should create:

```text
NEW EXPERIMENT VERSION
```

---

# 111. Experiment Forking

If a protocol changes:

```text
Experiment v1
        ↓
Experiment v2
```

not:

```text
Experiment v1
        ↓
silently modified
```

Historical results must remain intact.

---

# 112. Experiment Comparison

The runtime should support comparing:

```text
run A
vs
run B
```

across:

```text
target version
configuration
environment
model
data
metrics
failures
evidence
```

---

# 113. Evaluation Dashboard Requirements

A future dashboard should show:

```text
claim
experiment
target version
latest result
previous result
coverage
counterexamples
reproducibility
assurance status
```

The dashboard is a presentation layer, not the source of truth.

---

# 114. Source of Truth

The authoritative record should be the structured:

```text
experiment registry
evidence store
verification ledger
assurance ledger
```

The UI should derive from these.

---

# 115. Failure Replay as a Product Capability

A major differentiator can emerge from making every material failure:

```text
capturable
replayable
traceable
regression-testable
```

This creates a continuously growing institutional memory of how the system breaks.

---

# 116. Experimental Knowledge Accumulation

The verification system should accumulate:

```text
known failure classes
known counterexamples
known attack patterns
known verifier blind spots
known recovery failures
known assurance gaps
```

This becomes an engineering knowledge base.

---

# 117. Verification Memory

Verification memory must preserve:

```text
what was tested
what failed
what passed
under which conditions
what was fixed
what remains uncertain
```

It must not silently transform old observations into timeless truths.

---

# 118. Regression Knowledge

Each repair should answer:

```text
WHICH FAILURE DID THIS FIX?
WHICH CLAIM DID IT AFFECT?
WHICH TEST NOW PREVENTS REGRESSION?
WHAT NEW RISKS DID THE CHANGE INTRODUCE?
```

---

# 119. Experimental Governance

Experiments affecting:

```text
security
authority
real-world tools
self-modification
production systems
sensitive data
```

should require elevated authorization.

---

# 120. Experimental Audit

Periodic audits should inspect:

```text
invalid experiments
missing evidence
stale experiments
unreproduced results
judge conflicts
configuration drift
benchmark drift
assurance dependencies
```

---

# 121. Experimental Health Metrics

Track:

```text
experiment success rate
invalid-run rate
replay success rate
evidence completeness
judge disagreement rate
environment failure rate
reproducibility rate
stale-evidence rate
regression detection rate
```

---

# 122. Critical Invariants

### Invariant 1

Every assurance-critical experiment has a unique identity.

### Invariant 2

Every assurance-critical result identifies the exact target version.

### Invariant 3

Experimental environments must be isolated according to risk.

### Invariant 4

The target cannot redefine its own evaluation protocol.

### Invariant 5

The target cannot silently modify evidence or assurance records.

### Invariant 6

Deterministic properties should use deterministic oracles where practical.

### Invariant 7

Stochastic results must preserve seed and sampling metadata.

### Invariant 8

Invalid experiments cannot silently contribute to assurance.

### Invariant 9

Material counterexamples must be replayable where feasible.

### Invariant 10

A repair must be evaluated against the original failure and relevant regressions.

### Invariant 11

Experiment provenance must be preserved.

### Invariant 12

The evaluation harness itself must be testable.

### Invariant 13

Experiment authority and target authority remain distinct.

### Invariant 14

Protocol changes create new experiment versions.

### Invariant 15

No experimental result is stronger than the reproducibility and evidence chain supporting it.

---

# 123. Exit Criteria

- [x] Experimental control model defined
- [x] Experiment identity defined
- [x] Target version pinning defined
- [x] Reproducibility levels defined
- [x] Determinism distinguished from reproducibility
- [x] Environment isolation defined
- [x] Production safety boundary defined
- [x] Resource isolation defined
- [x] Credential isolation defined
- [x] Network isolation defined
- [x] Tool isolation defined
- [x] Tool simulation/replay defined
- [x] Model pinning defined
- [x] Prompt pinning defined
- [x] Dataset pinning defined
- [x] Hidden evaluation controls defined
- [x] Seed management defined
- [x] Experiment matrix defined
- [x] Evaluation harness defined
- [x] Harness/judge separation defined
- [x] Orchestration defined
- [x] Preflight validation defined
- [x] Experiment state machine defined
- [x] Invalid experiment semantics defined
- [x] Raw and derived evidence defined
- [x] Evidence integrity defined
- [x] Experiment provenance defined
- [x] Judge separation defined
- [x] Deterministic and semantic oracles defined
- [x] Benchmark registry defined
- [x] Regression suite defined
- [x] Failure replay defined
- [x] Differential replay defined
- [x] Continuous evaluation defined
- [x] Experiment invalidation defined
- [x] Auditability defined
- [x] Environment attestation defined
- [x] Dependency locking defined
- [x] Run manifest defined
- [x] Result states defined
- [x] Statistical experiment controls defined
- [x] Benchmark contamination controls defined
- [x] Blind evaluation defined
- [x] Harness self-verification defined
- [x] Experiment integrity chain defined
- [x] Reproducibility package defined
- [x] Minimum viable runtime defined
- [x] Build order defined
- [x] Runtime security boundary defined
- [x] Self-modification evaluation defined
- [x] Protocol immutability defined
- [x] Experiment forking defined
- [x] Failure replay as a product capability defined
- [x] Verification memory defined
- [x] Experimental governance defined
- [x] Experimental health metrics defined
- [x] Core invariants defined

**Current assessment:** IV-009 establishes the controlled experimental substrate required to make verification results reproducible, auditable, replayable, and appropriately bounded. It prevents the project from treating an untracked test run as strong evidence and establishes the minimum infrastructure required before large-scale empirical assurance claims are made.

---

# 124. Next Document

**IV-010 — Assurance Ledger, Evidence Graph & Claim-to-Proof Knowledge Architecture**

IV-010 will define how the evidence produced by the verification runtime becomes a persistent, queryable assurance structure:

```text
CLAIM
 ↓
PROOF OBLIGATION
 ↓
IMPLEMENTATION
 ↓
EXPERIMENT
 ↓
RUN
 ↓
OBSERVATION
 ↓
EVIDENCE
 ↓
COUNTEREXAMPLE
 ↓
VERIFICATION
 ↓
ASSURANCE
```

The document should define the graph/ledger structures required to answer questions such as:

```text
Which evidence supports this claim?

Which claims depend on this component?

Which assurance records became stale after this change?

Which failures have ever falsified this property?

Which verifier detected the failure?

How independent was that verifier?

Which implementation changes require re-verification?

What is the strongest evidence we currently possess?

Where are our largest unresolved assurance gaps?
```

This will become the information architecture connecting the entire verification and assurance system.
