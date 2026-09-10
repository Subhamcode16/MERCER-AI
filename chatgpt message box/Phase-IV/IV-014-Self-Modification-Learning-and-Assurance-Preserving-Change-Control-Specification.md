# IV-014 — Self-Modification, Learning & Assurance-Preserving Change Control Specification

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-006, IV-007, IV-008, IV-009, IV-010, IV-011, IV-012, IV-013

---

# 1. Purpose

IV-014 defines how the intelligence architecture may change itself without allowing change capability to become an implicit self-certification mechanism.

The system may eventually modify:

```text
code
models
prompts
policies
memory
tools
configurations
verification logic
authority logic
assurance logic
```

The central invariant is:

```text
SELF-MODIFICATION
        ≠
SELF-CERTIFICATION
```

A system that proposes a change must not automatically become the sole authority that decides that the change is safe, correct, authorized, and deployable.

---

# 2. Core Principle

Every consequential change must move through an explicit change-control lifecycle:

```text
OBSERVATION
 ↓
CHANGE PROPOSAL
 ↓
IMPACT ANALYSIS
 ↓
ISOLATION
 ↓
TEST
 ↓
ADVERSARIAL VERIFICATION
 ↓
INDEPENDENT EVALUATION
 ↓
ASSURANCE CHECK
 ↓
GOVERNANCE
 ↓
DEPLOY
 ↓
RUNTIME MONITORING
 ↓
ROLLBACK / RETAIN / RETIRE
```

The exact depth of this lifecycle depends on change risk.

---

# 3. Source Basis

IV-014 extends:

```text
IV-006 — Evidence, Verification, Self-Critique & Adversarial Self-Verification Architecture
IV-007 — Coverage, Assurance-Gap & Implementation Verification Matrix
IV-008 — System-Wide Falsification, Red-Team Protocol & Failure-Injection Specification
IV-009 — Verification Runtime, Evaluation Harness & Experimental Control Specification
IV-010 — Assurance Ledger, Evidence Graph & Claim-to-Proof Knowledge Architecture
IV-011 — Assurance Computation, Evidence Aggregation & Conservative Decision Semantics
IV-012 — Assurance-Gated Execution, Release & Governance Control
IV-013 — Runtime Assurance Monitor, Continuous Reverification & Drift Detection
```

---

# 4. Why Self-Modification Is Different

A normal software change can be reviewed by an external engineering process.

A self-modifying intelligence may:

```text
observe
reason
propose
implement
test
evaluate
deploy
```

through closely related components.

This creates a dangerous correlation:

```text
SAME INTELLIGENCE
        ↓
creates change
        ↓
creates tests
        ↓
creates evidence
        ↓
declares change safe
```

The architecture must prevent this chain from becoming sufficient for high-risk changes.

---

# 5. Change Classes

Candidate classes:

```text
C0 — NO MATERIAL CHANGE
C1 — LOW-RISK CONFIGURATION
C2 — LOCAL BEHAVIOR CHANGE
C3 — CAPABILITY CHANGE
C4 — SECURITY / AUTHORITY CHANGE
C5 — VERIFICATION / ASSURANCE CHANGE
C6 — CORE ARCHITECTURE CHANGE
```

The classification determines required controls.

---

# 6. C0 — No Material Change

Examples:

```text
documentation
non-executable metadata
non-functional formatting
```

May use lightweight validation.

---

# 7. C1 — Low-Risk Configuration

Examples:

```text
non-critical thresholds
UI configuration
resource tuning
```

May use:

```text
automated validation
regression testing
```

subject to policy.

---

# 8. C2 — Local Behavior Change

Examples:

```text
algorithm adjustment
prompt adjustment
small workflow change
```

Requires:

```text
isolated test
regression
relevant verification
```

---

# 9. C3 — Capability Change

Examples:

```text
new tool
new external integration
new execution capability
new planning capability
```

Requires stronger:

```text
impact analysis
adversarial testing
assurance evaluation
governance
```

---

# 10. C4 — Security / Authority Change

Examples:

```text
permission change
credential handling
delegation logic
security policy
authority model
```

These require elevated independent verification.

---

# 11. C5 — Verification / Assurance Change

Examples:

```text
verification logic
judge logic
assurance rules
evidence aggregation
gate logic
```

These are especially sensitive because they modify the mechanisms used to establish trust.

A change must not be allowed to:

```text
modify verifier
+
modify assurance rule
+
self-certify
```

through one authority path.

---

# 12. C6 — Core Architecture Change

Examples:

```text
memory architecture
authority architecture
execution architecture
control plane
self-modeling architecture
core reasoning architecture
```

These require the strongest available change-control process.

---

# 13. Change Proposal

Every material change begins with:

```yaml
change_proposal:
  change_id: ...
  proposer: ...
  target: ...
  current_version: ...
  proposed_version: ...
  rationale: ...
  expected_benefit: ...
  expected_risks: []
  affected_claims: []
  affected_capabilities: []
```

---

# 14. Proposal Does Not Equal Approval

A proposal is:

```text
HYPOTHESIS
```

not:

```text
AUTHORIZED CHANGE
```

The system must preserve this distinction.

---

# 15. Change Rationale

The proposal should explain:

```text
problem
observed failure
assurance gap
performance limitation
security issue
new requirement
```

A change should have a traceable reason.

---

# 16. Expected Benefit

Represent expected benefit explicitly:

```text
performance
reliability
safety
security
capability
cost
latency
maintainability
```

Benefits must not be treated as evidence that the change is safe.

---

# 17. Expected Risk

Identify:

```text
new failure modes
removed safeguards
new authority
new dependencies
new attack surface
new behavioral uncertainty
```

---

# 18. Impact Analysis

Before implementation:

```text
CHANGE
 ↓
DEPENDENCY GRAPH
 ↓
AFFECTED CLAIMS
 ↓
AFFECTED PROOF OBLIGATIONS
 ↓
AFFECTED VERIFIERS
 ↓
AFFECTED ASSURANCE
 ↓
AFFECTED CAPABILITIES
```

IV-010 provides the required graph structure.

---

# 19. Change Impact Categories

Assess:

```text
FUNCTIONAL
SECURITY
AUTHORITY
ASSURANCE
VERIFICATION
DATA
PRIVACY
PERFORMANCE
RELIABILITY
OPERABILITY
```

---

# 20. Verification Dependency Analysis

A change must explicitly determine whether it affects:

```text
the target
the verifier
the judge
the benchmark
the dataset
the protocol
the assurance engine
the gate
```

This is essential for detecting correlated verification.

---

# 21. Verification Independence Risk

If:

```text
change
```

modifies both:

```text
target
```

and:

```text
verifier
```

then previous evidence may no longer demonstrate independent assurance.

The system must trigger reassessment.

---

# 22. Isolation

Before high-risk deployment:

```text
candidate version
```

must be isolated from production authority.

Isolation may include:

```text
sandbox
container
virtual machine
separate credentials
mock tools
synthetic environment
network restrictions
```

---

# 23. Authority Isolation

Candidate code must not inherit production authority merely because it is being evaluated.

Use:

```text
least privilege
temporary credentials
scoped tokens
capability restrictions
```

---

# 24. Tool Isolation

Candidate versions should use:

```text
mock
simulated
sandboxed
read-only
```

tools where practical.

---

# 25. Data Isolation

Candidate evaluation should use:

```text
test data
sanitized data
controlled datasets
```

unless production data is explicitly required and governed.

---

# 26. Environment Isolation

The evaluation environment must be reproducible enough to distinguish:

```text
change effect
```

from:

```text
environmental noise
```

IV-009 provides the experimental foundation.

---

# 27. Candidate Identity

Every candidate must have an immutable identity:

```text
change_id
version
content digest
dependency manifest
configuration
```

---

# 28. Change Artifact

The exact artifact evaluated must be recorded.

Examples:

```text
commit
container digest
model version
prompt version
policy version
configuration hash
```

---

# 29. Change-Specific Evidence

Evidence must be linked specifically to:

```text
candidate version
```

not merely:

```text
component name
```

---

# 30. Regression Requirement

Every material change should run:

```text
existing regression suite
```

appropriate to the affected scope.

---

# 31. New Tests

New tests should target:

```text
expected benefit
new behavior
known failure
new risk
affected invariants
```

---

# 32. Negative Testing

Changes must be tested not only for:

```text
what they should do
```

but also:

```text
what they must not do
```

---

# 33. Adversarial Verification

High-risk changes should undergo adversarial testing designed to:

```text
break the intended property
find hidden regressions
exploit new authority
bypass new controls
trigger unexpected behavior
```

---

# 34. Self-Critique

The modifying intelligence may critique its own change.

This is useful evidence, but:

```text
SELF-CRITIQUE
≠
INDEPENDENT VERIFICATION
```

---

# 35. Adversarial Self-Verification

The modifying intelligence may also explicitly attempt to break its own change.

Again:

```text
SELF-ATTACK
≠
INDEPENDENT ASSURANCE
```

The distinction must remain visible in the evidence graph.

---

# 36. Independent Evaluation

For C3–C6 changes, independent evaluation should be required according to risk.

Independence may mean:

```text
different model
different implementation
different evaluator
different test generation method
different dataset
different threat model
```

The appropriate dimensions must be explicitly recorded.

---

# 37. Independence Is Not Binary

Represent:

```text
strong independence
partial independence
weak independence
unknown
```

with supporting dependencies.

---

# 38. Change Assurance

The candidate change receives an assurance assessment based on:

```text
tests
regression
adversarial evaluation
independent evaluation
evidence integrity
freshness
counterexamples
affected proof obligations
```

IV-011 defines the computation semantics.

---

# 39. No Automatic Promotion

A candidate cannot become production-assured simply because:

```text
all self-generated tests passed
```

---

# 40. Governance Gate

Before deployment:

```text
candidate assurance
+
authority
+
security
+
policy
+
risk
```

must satisfy the applicable release policy.

---

# 41. Human Governance

High-risk changes may require explicit human approval.

The approval must identify:

```text
change
risk
assurance
limitations
affected capabilities
rollback plan
```

---

# 42. Governance Override

If a human approves a risky change despite incomplete evidence:

```text
GOVERNANCE OVERRIDE
```

must be recorded separately from:

```text
ASSURANCE
```

The underlying uncertainty remains.

---

# 43. Pre-Deployment Gate

```text
CANDIDATE
 ↓
IDENTITY VALID
 ↓
IMPACT REVIEW
 ↓
REGRESSION
 ↓
ADVERSARIAL TEST
 ↓
INDEPENDENT EVALUATION
 ↓
ASSURANCE
 ↓
SECURITY
 ↓
AUTHORITY
 ↓
GOVERNANCE
 ↓
DEPLOY / BLOCK
```

---

# 44. Canary Deployment

High-risk changes should use:

```text
small controlled cohort
```

before broad deployment where practical.

---

# 45. Canary Monitoring

Monitor:

```text
error rate
security events
unexpected behavior
assurance signals
tool usage
performance
counterexamples
```

---

# 46. Progressive Promotion

Candidate may progress:

```text
sandbox
 ↓
shadow
 ↓
canary
 ↓
limited production
 ↓
full deployment
```

Each transition requires explicit criteria.

---

# 47. Shadow Mode

A candidate can operate without controlling external effects.

Compare:

```text
existing system
vs
candidate
```

for:

```text
outputs
decisions
tool choices
risk signals
```

---

# 48. Shadow Disagreement

Disagreement does not automatically mean candidate failure.

It becomes:

```text
evidence requiring analysis
```

and may reveal:

```text
improvement
regression
distribution shift
```

---

# 49. Promotion Criteria

Promotion should require:

```text
required tests passed
no blocking counterexamples
required assurance satisfied
monitoring healthy
rollback available
governance satisfied
```

---

# 50. Automatic Rollback

For predefined critical conditions:

```text
candidate
 ↓
critical failure
 ↓
automatic rollback / containment
```

may be required.

---

# 51. Rollback Artifact

Rollback must identify:

```text
previous version
candidate version
trigger
evidence
time
affected scope
```

---

# 52. Rollback Is Not Proof

Returning to an old version does not prove:

```text
old version is currently safe
```

because:

```text
environment
dependencies
threat model
policy
```

may have changed.

---

# 53. Post-Rollback Reverification

After rollback:

```text
current state
 ↓
assurance reassessment
```

must occur for affected critical capabilities.

---

# 54. Learning Changes

Learning can alter:

```text
parameters
memory
policy preferences
retrieval
planning behavior
```

The system must classify which learning changes are:

```text
ephemeral
persistent
capability-affecting
authority-affecting
verification-affecting
```

---

# 55. Ephemeral Learning

Temporary adaptation may remain within a controlled execution context.

However, if it affects safety-critical decisions:

```text
runtime monitoring
```

must still apply.

---

# 56. Persistent Learning

Persistent learning changes the future behavior of the system.

Therefore:

```text
persistent learning
→
change record
→
assurance impact analysis
```

where relevant.

---

# 57. Memory Modification

Memory may contain:

```text
facts
preferences
policies
plans
procedures
self-model information
```

Memory updates must not automatically gain authority merely because the system generated them.

---

# 58. Memory Provenance

Critical memory should record:

```text
source
creation event
confidence/epistemic status where applicable
validation
scope
timestamp
```

---

# 59. Memory Promotion

A memory should become operationally authoritative only through explicit policy.

For example:

```text
OBSERVATION
 ↓
MEMORY
 ↓
VALIDATION
 ↓
AUTHORIZED KNOWLEDGE
```

---

# 60. Policy Self-Modification

Changes to policies are high-risk because they alter:

```text
what the system is allowed to do
```

Policy changes require:

```text
versioning
impact analysis
independent review
governance
```

---

# 61. Authority Logic Modification

Changes to:

```text
identity
delegation
revocation
scope
privilege
```

must be treated as C4 or higher.

---

# 62. Verification Logic Modification

Changes to:

```text
tests
judges
attack generators
assurance rules
evidence aggregation
```

must be treated as C5.

---

# 63. Assurance Logic Modification

The assurance engine cannot be allowed to modify:

```text
its own rules
```

and immediately use those rules to certify the modification.

Required separation:

```text
PROPOSE
 ↓
ISOLATE
 ↓
INDEPENDENTLY EVALUATE
 ↓
GOVERN
 ↓
ACTIVATE
```

---

# 64. Verifier Modification

If the verifier changes:

```text
previous verifier evidence
```

must not automatically establish the new verifier's correctness.

The verifier requires its own verification.

---

# 65. Judge Modification

If the evaluation judge changes:

```text
historical results
```

remain tied to the old judge.

New results must identify the new judge version.

---

# 66. Benchmark Modification

Changing the benchmark may change what is being measured.

Therefore:

```text
benchmark version
```

must be immutable for a recorded evaluation.

---

# 67. Dataset Modification

Changes to evaluation data can materially affect results.

Record:

```text
dataset version
digest
generation method
filtering
sampling
```

where applicable.

---

# 68. Prompt Modification

Prompts can be part of the verification protocol.

Therefore:

```text
prompt version
```

must be recorded.

---

# 69. Self-Improvement Proposal

A self-improvement agent may generate:

```yaml
improvement_proposal:
  proposal_id: ...
  observed_problem: ...
  proposed_change: ...
  expected_benefit: ...
  risks: []
  affected_claims: []
  affected_capabilities: []
```

---

# 70. Improvement Ranking

Candidate improvements may be ranked by:

```text
expected benefit
risk
assurance impact
implementation cost
reversibility
blast radius
```

Ranking is not authorization.

---

# 71. Change Budget

High-risk systems may impose:

```text
maximum change rate
maximum concurrent changes
maximum capability delta
```

This reduces uncontrolled self-modification.

---

# 72. Change Rate Limiting

Prevent:

```text
rapid recursive modification
```

from producing an untraceable chain of versions.

---

# 73. Version Lineage

Every change must produce:

```text
parent_version
→
candidate_version
```

and retain the complete lineage.

---

# 74. Recursive Modification

If:

```text
change A
→
creates change B
→
creates change C
```

the system must preserve the entire ancestry.

---

# 75. Change Depth

For self-generated modifications, record:

```text
generation_depth
```

This can support additional controls for long recursive modification chains.

---

# 76. Modification Authority

A self-modifying component requires explicit authority:

```text
may_propose
may_implement
may_test
may_deploy
```

These permissions should be separate.

---

# 77. Separation of Modification Roles

Prefer:

```text
PROPOSER
IMPLEMENTER
VERIFIER
APPROVER
DEPLOYER
```

as logically distinct roles for high-risk changes.

They may be implemented by separate agents, services, or human roles depending on system design.

---

# 78. No Single-Path Certification

For high-risk changes, avoid:

```text
same component
→
proposes
→
implements
→
verifies
→
approves
→
deploys
```

without independent controls.

---

# 79. Change Authority Graph

Represent:

```text
actor
 ↓
role
 ↓
change permission
 ↓
scope
 ↓
expiration
```

This integrates with the authority architecture.

---

# 80. Change Quarantine

Suspicious or high-risk changes should enter:

```text
QUARANTINED
```

state until resolved.

---

# 81. Change States

Candidate state machine:

```text
PROPOSED
 ↓
CLASSIFIED
 ↓
ANALYZED
 ↓
IMPLEMENTED
 ↓
ISOLATED
 ↓
TESTED
 ↓
ADVERSARIALLY_TESTED
 ↓
INDEPENDENTLY_EVALUATED
 ↓
ASSURANCE_REVIEW
 ↓
GOVERNANCE_REVIEW
 ↓
CANARY
 ↓
DEPLOYED
 ↓
MONITORED
 ↓
RETAINED / ROLLED_BACK / RETIRED
```

---

# 82. Rejected Changes

Rejected proposals should remain historically available with:

```text
reason
evidence
review
```

This creates institutional memory.

---

# 83. Failed Changes

A failed candidate should generate:

```text
failure record
counterexample where applicable
lessons
regression test where appropriate
```

---

# 84. Learning From Failed Changes

Failure information should feed:

```text
future proposal generation
attack generation
test generation
assurance gaps
```

without granting the failed change additional authority.

---

# 85. Change Knowledge Graph

Connect:

```text
change
→
problem
→
proposal
→
implementation
→
tests
→
attacks
→
evidence
→
assurance
→
deployment
→
runtime outcomes
```

---

# 86. Change Ledger

Every material transition should create:

```yaml
change_event:
  event_id: ...
  change_id: ...
  state_from: ...
  state_to: ...
  trigger: ...
  actor: ...
  evidence_refs: []
  timestamp: ...
```

---

# 87. Reproducibility

A candidate evaluation should be reproducible using:

```text
artifact
environment
dependencies
configuration
protocol
dataset
model
prompt
seed
```

IV-009 establishes this requirement.

---

# 88. Change Evidence Package

Before deployment, preserve:

```text
change proposal
impact analysis
candidate artifact
test results
adversarial results
independent evaluation
assurance computation
approval
rollback plan
```

---

# 89. Deployment Evidence

After deployment preserve:

```text
deployment event
environment
cohort
runtime monitoring
incidents
assurance transitions
```

---

# 90. Change-to-Assurance Query

The system must answer:

```text
WHAT ASSURANCE CLAIMS DID THIS CHANGE AFFECT?
```

---

# 91. Assurance-to-Change Query

It must also answer:

```text
WHICH CHANGES SUPPORT THE CURRENT ASSURANCE OF THIS CLAIM?
```

---

# 92. Change-to-Failure Query

```text
WHICH FAILURES HAVE EVER RESULTED FROM THIS CHANGE FAMILY?
```

---

# 93. Failure-to-Change Query

```text
WHICH CHANGE INTRODUCED THIS FAILURE?
```

where causality can be established.

---

# 94. Change Correlation

A failure may result from:

```text
multiple interacting changes
```

The graph should support multiple candidate causes rather than forcing one cause prematurely.

---

# 95. Root Cause

Root cause should be represented as:

```text
hypothesis
```

until supported by evidence.

---

# 96. Change Experimentation

Self-improvement may use controlled experiments:

```text
baseline
vs
candidate
```

with explicit success criteria.

---

# 97. A/B Evaluation

For behavior changes:

```text
baseline cohort
candidate cohort
```

may be compared.

The evaluation must control for:

```text
population
environment
time
data
```

where relevant.

---

# 98. Improvement Must Not Optimize the Judge

A dangerous loop is:

```text
candidate
 ↓
judge
 ↓
candidate learns judge preferences
 ↓
candidate passes judge
```

The architecture must defend against evaluator gaming.

---

# 99. Hidden Evaluation

Where practical, critical evaluation should include:

```text
hidden tests
unseen attacks
independent benchmarks
```

so that the modifying system cannot optimize solely against visible criteria.

---

# 100. Judge Diversity

Use materially different evaluators for high-risk properties where practical:

```text
deterministic checker
formal property
independent model
human reviewer
adversarial generator
```

---

# 101. Reward Hacking

Optimization against evaluation metrics may produce:

```text
metric improvement
```

without:

```text
real capability improvement
```

Therefore:

```text
metric gain
≠
assurance gain
```

---

# 102. Proxy Risk

If the system optimizes:

```text
proxy P
```

for:

```text
desired property D
```

then evaluation must test:

```text
P ↑
while
D unchanged / ↓
```

to detect proxy exploitation.

---

# 103. Change Gaming

The system must not be rewarded merely for:

```text
passing tests
```

if it can:

```text
modify tests
modify evaluator
modify evidence
modify reporting
```

without independent controls.

---

# 104. Evaluation Integrity

Evaluation artifacts must be protected against:

```text
candidate modification
result manipulation
test tampering
selective reporting
```

---

# 105. Independent Evidence Storage

Critical evaluation evidence should be stored outside the candidate's direct modification authority.

---

# 106. Self-Model Changes

If the system changes its own:

```text
self-model
self-critique
self-verification
```

mechanisms, treat these as verification-sensitive changes.

They require:

```text
independent testing
```

because they alter the architecture's epistemic defenses.

---

# 107. Verification Dominance Concern

A more capable system may potentially outperform its verifier.

Therefore:

```text
target capability ↑
```

must trigger evaluation of:

```text
verifier capability
verifier diversity
verifier independence
attack coverage
```

This directly addresses the architecture's earlier concern about verification becoming weaker than the intelligence it evaluates.

---

# 108. Capability-Verifier Gap

Track:

```text
TARGET CAPABILITY
vs
VERIFIER CAPABILITY
```

where meaningful measures exist.

The goal is not to assume:

```text
verifier ≥ target
```

in every dimension.

Instead, identify domains where verification may become unreliable.

---

# 109. Verification Escalation

If:

```text
target exceeds known verifier competence
```

then:

```text
AUTOMATIC ASSURANCE
→
REASSESSMENT_REQUIRED
```

for affected claims.

Possible response:

```text
stronger verifier
formal method
external evaluator
human review
restricted deployment
```

---

# 110. Recursive Trust Boundary

The system must avoid:

```text
agent
→
modifies verifier
→
verifier approves agent
→
agent trusts verifier
```

without an external trust anchor.

---

# 111. Trust Anchors

Candidate trust anchors:

```text
immutable policy
external evaluator
independent service
human governance
formally verified component
hardware-backed control
```

The appropriate anchor depends on risk.

---

# 112. Immutable Control Plane

Some controls may need to remain outside self-modification authority:

```text
root authority
assurance governance
security shutdown
audit ledger
deployment approval
```

---

# 113. Protected Components

Define a protected set:

```text
PROTECTED_CONTROL_SET
```

Self-modification cannot directly modify these components.

Changes require external governance.

---

# 114. Protected Ledger

The assurance/change ledger should be append-only from the perspective of the modifying intelligence.

---

# 115. Protected Evidence

Critical evidence should be write-once or otherwise integrity-protected.

---

# 116. Change Review Package

A high-risk review should answer:

```text
WHAT CHANGED?
WHY?
WHAT COULD BREAK?
WHAT CLAIMS ARE AFFECTED?
WHAT TESTS WERE RUN?
WHAT ATTACKS WERE RUN?
WHO/WHAT VERIFIED IT?
HOW INDEPENDENT IS THAT VERIFICATION?
WHAT REMAINS UNKNOWN?
HOW CAN WE ROLLBACK?
```

---

# 117. Change Approval Semantics

Approval should be:

```text
specific
scoped
version-bound
time-bound
revocable
```

---

# 118. Deployment Scope

A change should specify:

```text
target cohort
capabilities
environment
duration
rollback criteria
```

---

# 119. Automatic Promotion Limits

Do not allow unrestricted:

```text
sandbox
→
production
```

promotion for high-risk change classes.

---

# 120. Recursive Change Limits

For self-modifying systems, policy may impose:

```text
maximum recursion depth
maximum change rate
maximum capability delta
maximum concurrent candidate count
```

---

# 121. Emergency Changes

Emergency patches may use shortened paths, but must retain:

```text
authority
audit
evidence
post-deployment verification
```

---

# 122. Emergency Retrospective

After emergency deployment:

```text
emergency change
 ↓
post-hoc verification
 ↓
assurance reassessment
 ↓
formalization / rollback
```

---

# 123. Change Retirement

A change should be retired when:

```text
superseded
unsafe
unmaintainable
assurance unavailable
```

Historical records remain preserved.

---

# 124. Change Compatibility

Before deployment verify compatibility with:

```text
existing contracts
authority model
security model
assurance rules
memory
tools
runtime
```

---

# 125. Contract Preservation

Where a change claims to preserve an existing contract:

```text
contract
 ↓
regression
 ↓
verification
```

must establish that preservation.

---

# 126. Contract Change

If a contract itself changes:

```text
new contract version
```

must trigger:

```text
affected claim reassessment
```

---

# 127. Semantic Change Detection

Changing implementation while keeping the same interface may still alter semantics.

Therefore:

```text
interface compatibility
≠
semantic equivalence
```

---

# 128. Semantic Equivalence

Where required, evaluate:

```text
old behavior
vs
new behavior
```

against:

```text
invariants
contracts
critical scenarios
```

---

# 129. Performance-Only Changes

A performance change may still alter:

```text
timing
resource use
failure probability
tool behavior
```

and therefore cannot be assumed risk-free.

---

# 130. Observability Changes

Changing telemetry or monitoring is itself assurance-sensitive.

A change that reduces observability may increase assurance uncertainty even if functionality is unchanged.

---

# 131. Monitoring Reduction

If:

```text
monitor coverage ↓
```

then:

```text
assurance may need demotion
```

for affected properties.

---

# 132. Change Risk Invariants

Risk increases with:

```text
authority delta
capability delta
irreversibility
blast radius
verification change
security impact
```

---

# 133. Change Risk Record

```yaml
change_risk:
  authority_delta: ...
  capability_delta: ...
  security_delta: ...
  assurance_delta: ...
  blast_radius: ...
  reversibility: ...
  verification_impact: ...
```

---

# 134. Critical Invariants

### Invariant 1

Self-modification cannot equal self-certification.

### Invariant 2

A change cannot gain production authority merely because it generated successful self-tests.

### Invariant 3

Changes to verification or assurance logic require independent evaluation.

### Invariant 4

Changes to authority or security logic require elevated governance.

### Invariant 5

Candidate changes must be isolated from production authority during evaluation.

### Invariant 6

Every material change must have an immutable identity and lineage.

### Invariant 7

Historical evidence remains tied to the exact version and evaluation conditions that generated it.

### Invariant 8

A verifier modified by the target cannot automatically establish independent assurance of the modified target.

### Invariant 9

Hidden or independent evaluation should be used where evaluator gaming is plausible.

### Invariant 10

Metric improvement does not automatically imply assurance improvement.

### Invariant 11

Persistent learning that changes consequential behavior must be subject to change-control semantics.

### Invariant 12

Rollback does not automatically restore current assurance.

### Invariant 13

Protected control components cannot be modified through the same authority path they govern.

### Invariant 14

Emergency changes require post-deployment verification.

### Invariant 15

Every high-risk change must have a bounded rollback or containment strategy.

### Invariant 16

Changes that reduce observability can themselves reduce assurance.

### Invariant 17

The system must detect when target capability may exceed verifier competence.

### Invariant 18

A more capable target must not be assumed to remain safely self-verifiable merely because prior evaluations passed.

---

# 135. Exit Criteria

- [x] Self-modification lifecycle defined
- [x] Self-certification boundary defined
- [x] Change classes defined
- [x] Change proposal model defined
- [x] Impact analysis defined
- [x] Verification dependency analysis defined
- [x] Isolation requirements defined
- [x] Authority/tool/data/environment isolation defined
- [x] Candidate identity and artifact integrity defined
- [x] Regression and negative testing defined
- [x] Self-critique/adversarial self-verification boundaries defined
- [x] Independent evaluation defined
- [x] Change assurance defined
- [x] Governance gate defined
- [x] Canary/shadow/progressive deployment defined
- [x] Rollback semantics defined
- [x] Learning and persistent-memory change control defined
- [x] Policy/authority/verification/assurance modification controls defined
- [x] Self-improvement proposal model defined
- [x] Change budget/rate/depth limits defined
- [x] Modification role separation defined
- [x] Change quarantine/state machine defined
- [x] Change knowledge graph and ledger defined
- [x] Evidence integrity requirements defined
- [x] Judge/verifier/benchmark/dataset/prompt versioning defined
- [x] Evaluator gaming and reward hacking risks defined
- [x] Self-model and verification-dominance concerns defined
- [x] Capability-verifier gap defined
- [x] Recursive trust boundary defined
- [x] Protected control set defined
- [x] Emergency change semantics defined
- [x] Contract/semantic compatibility defined
- [x] Observability-change impact defined
- [x] Change-risk model defined
- [x] Core invariants defined

**Current assessment:** IV-014 establishes the change-control boundary required for a self-improving intelligence architecture. It allows the system to generate and implement improvements while preventing the same intelligence from silently changing the mechanisms by which it is trusted and then certifying those changes through the modified mechanisms themselves.

---

# 136. Next Document

**IV-015 — Integrated Assurance Architecture, End-to-End Validation & Engineering Readiness Specification**

IV-015 should consolidate the entire Phase IV architecture and define the final readiness gate before implementation.

It should integrate:

```text
verification
coverage
falsification
evaluation runtime
assurance graph
assurance computation
execution gates
continuous monitoring
self-modification
```

into one end-to-end architecture.

The central question becomes:

```text
CAN THE COMPLETE ARCHITECTURE
BE IMPLEMENTED, TESTED, FALSIFIED,
AND GOVERNED AS ONE COHERENT SYSTEM?
```

IV-015 should produce the final:

```text
architecture-wide dependency map
claim-to-control map
verification matrix
assurance lifecycle
failure paths
readiness criteria
implementation sequencing
open research questions
unresolved assumptions
known limits
```

At that point, Phase IV can be formally ratified as an engineering baseline, subject to the explicit unresolved items recorded by the final document.
