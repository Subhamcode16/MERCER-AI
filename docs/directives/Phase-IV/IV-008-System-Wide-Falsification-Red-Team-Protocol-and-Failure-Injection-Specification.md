# IV-008 — System-Wide Falsification, Red-Team Protocol & Failure-Injection Specification

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-003, IV-004, IV-005, IV-006, IV-007, III-004, III-009, III-010, III-012, III-013, III-015

---

# 1. Purpose

IV-008 defines the architecture's systematic method for trying to break its own claims.

The objective is not:

```text
DEMONSTRATE THAT THE SYSTEM WORKS
```

but:

```text
MAXIMIZE THE CHANCE OF DISCOVERING
WHERE THE SYSTEM DOES NOT WORK.
```

The central loop is:

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

This document converts the adversarial-verification principles of IV-006 into an executable engineering protocol.

---

# 2. Core Principle

A system should not be considered robust because:

```text
normal tests pass
```

It should be subjected to:

```text
expected failures
unexpected failures
adversarial failures
composed failures
temporal failures
dependency failures
verification failures
```

The red-team system exists to search for cases where:

```text
SYSTEM CLAIM
≠
SYSTEM BEHAVIOR
```

---

# 3. Source Basis

IV-008 builds directly on:

```text
IV-003 — Dependency, Invalidation & Propagation Semantics
IV-004 — Authority, Constraint, Security & Human-Governance Precedence
IV-005 — State, Lifecycle & Transition Consistency
IV-006 — Evidence, Verification, Self-Critique & Adversarial Self-Verification
IV-007 — Coverage, Assurance-Gap & Implementation Verification Matrix
```

III-009 provides the architectural basis for adversarial verification and counterexample discovery.

III-012 provides the security and adversarial runtime boundary.

III-013 provides governed adaptation and self-modification concerns.

III-015 provides system-wide assurance and proof distinctions.

The existing engineering system also demonstrates a useful failure-response pattern in which violations are classified and handled through correction, regeneration, rebase, escalation, or related bounded responses rather than being silently ignored. fileciteturn16file2L164-L174

---

# 4. Falsification vs Testing

Ordinary testing asks:

```text
DOES THE SYSTEM WORK ON EXPECTED CASES?
```

Falsification asks:

```text
CAN WE FIND A CASE THAT BREAKS THE CLAIM?
```

Both are necessary.

The second is particularly important for claims involving:

```text
security
authority
safety
alignment
self-modification
governance
```

---

# 5. Falsification Target

Every red-team campaign must identify a target claim:

```yaml
falsification_target:
  claim_id: ...
  target_ref: ...
  target_version: ...
  property: ...
  scope: ...
  assumptions: []
```

The red team must know what proposition it is trying to disprove.

---

# 6. Attack Objective

Each attack should have a concrete objective.

Examples:

```text
execute without authority
execute after revocation
execute outside scope
bypass constraint
use stale approval
use superseded decision
forge provenance
confuse versions
bypass security gate
poison evidence
mislead self-critique
blind adversarial verifier
cause unauthorized self-modification
recover without authorization
```

---

# 7. Threat Model

Every adversarial campaign should specify:

```text
attacker identity
attacker capability
attacker knowledge
available tools
available evidence
network/runtime access
time/resources
protected assets
success condition
```

The absence of a threat model makes attack results difficult to interpret.

---

# 8. Attack Classes

The system should support at least:

```text
A1 — INPUT MANIPULATION
A2 — AUTHORITY ESCALATION
A3 — DELEGATION ABUSE
A4 — CONSTRAINT BYPASS
A5 — POLICY CONFLICT
A6 — LIFECYCLE ABUSE
A7 — VERSION CONFUSION
A8 — PROVENANCE POISONING
A9 — EVIDENCE MANIPULATION
A10 — SECURITY BYPASS
A11 — TOOL / ENVIRONMENT MANIPULATION
A12 — SELF-CRITIQUE EVASION
A13 — ADVERSARIAL-VERIFIER EVASION
A14 — SELF-MODIFICATION ABUSE
A15 — RECOVERY / ROLLBACK ABUSE
A16 — ASSURANCE MANIPULATION
A17 — CONCURRENCY / RACE ATTACK
A18 — COMPOSITION ATTACK
```

---

# 9. Attack Surface

Candidate surfaces:

```text
input parser
identity
authority registry
delegation
policy engine
constraint engine
decision engine
approval system
execution intent
security gate
memory
retrieval
provenance
tools
external integrations
self-critique
adversarial verifier
learning/adaptation
self-modification
recovery
assurance ledger
```

---

# 10. Failure-Injection Principle

Failure injection deliberately introduces a known defect or abnormal condition to verify:

```text
detection
containment
classification
recovery
assurance impact
```

The objective is not merely to crash the system.

It is to verify that the architecture responds correctly to failure.

---

# 11. Failure-Injection Classes

Candidate classes:

```text
INVALID INPUT
INVALID STATE
MISSING DEPENDENCY
STALE DEPENDENCY
REVOKED AUTHORITY
EXPIRED AUTHORITY
SUPERSEDED DECISION
INVALID EVIDENCE
MISSING PROVENANCE
POLICY CONFLICT
CONSTRAINT CONFLICT
SECURITY BLOCK
TOOL FAILURE
NETWORK FAILURE
MODEL FAILURE
VERIFIER FAILURE
DATA CORRUPTION
VERSION MISMATCH
CONCURRENT UPDATE
PARTIAL EXECUTION
RECOVERY FAILURE
```

---

# 12. Controlled Failure Injection

Failure injection must be:

```text
authorized
isolated
reproducible
observable
reversible
auditable
```

Never perform uncontrolled failure injection against production execution paths.

---

# 13. Failure-Injection Record

Conceptually:

```yaml
failure_injection:
  injection_id: ...
  target_ref: ...
  target_version: ...
  failure_class: ...
  injection_method: ...
  preconditions: ...
  expected_response: ...
  observed_response: ...
  evidence_refs: []
  cleanup: ...
  severity: ...
```

---

# 14. Red-Team Campaign Record

```yaml
red_team_campaign:
  campaign_id: ...
  target_claim: ...
  threat_model_ref: ...
  attack_refs: []
  findings: []
  coverage: ...
  unresolved_risks: []
  assurance_impact: ...
  provenance_ref: ...
```

---

# 15. Expected Failure

A controlled failure should have a predicted result:

```text
INJECTION
 ↓
EXPECTED DETECTION
 ↓
EXPECTED CONTAINMENT
 ↓
EXPECTED STATE
```

If the system behaves differently, that difference is evidence.

---

# 16. Unexpected Failure

An unexpected failure is often more valuable.

Example:

```text
attack intended to test authority
        ↓
causes provenance corruption
```

This reveals:

```text
cross-domain coupling
```

The unexpected effect must therefore be preserved rather than discarded as irrelevant.

---

# 17. Failure Severity

Candidate severity:

```text
F0 — INFORMATIONAL
F1 — LOW
F2 — MODERATE
F3 — HIGH
F4 — CRITICAL
F5 — CATASTROPHIC
```

Severity should consider:

```text
impact
scope
exploitability
detectability
reversibility
authority involved
```

---

# 18. Severity vs Detection

A dangerous failure that is immediately detected may be less severe operationally than:

```text
low-frequency
high-impact
undetected
```

Therefore track separately:

```text
impact
likelihood
detectability
```

---

# 19. Authority Escalation Campaign

Attempt:

```text
A has authority S
        ↓
attempt action outside S
```

Variants:

```text
direct escalation
transitive escalation
identifier confusion
scope wildcard
version confusion
delegation chaining
tool-mediated escalation
human-mediated escalation
```

Expected outcome:

```text
DENY / ESCALATE / REQUIRE NEW AUTHORIZATION
```

depending on contract.

---

# 20. Revocation Campaign

Scenario:

```text
AUTHORITY ACTIVE
        ↓
REVOCATION
        ↓
EXECUTION ATTEMPT
```

Expected:

```text
EXECUTION BLOCKED
```

Test:

```text
immediate revocation
delayed revocation
cached authorization
distributed state
concurrent execution
```

---

# 21. Expiration Campaign

Test:

```text
before expiry
at expiry boundary
after expiry
clock skew
stale cache
delayed execution
```

The architecture must not silently interpret expired authority as current authority.

---

# 22. Delegation Campaign

Attempt:

```text
delegator
 ↓
delegatee
 ↓
sub-delegatee
 ↓
action outside original scope
```

Verify:

```text
scope containment
delegation depth
expiration
revocation
transitive authority
```

---

# 23. Constraint Bypass Campaign

Attempt to satisfy an action by:

```text
changing representation
splitting action
delegating sub-actions
using alternative tool
using indirect execution
changing sequence
```

The purpose is to detect semantic rather than purely syntactic constraint bypass.

---

# 24. Policy Conflict Campaign

Inject:

```text
policy A
policy B
```

with contradictory requirements.

Verify:

```text
precedence
conflict detection
escalation
non-silent resolution
```

The system must not manufacture a winner when the contract requires escalation.

---

# 25. Lifecycle Attack Campaign

Attempt:

```text
DRAFT → ACTIVE
REVOKED → ACTIVE
SUPERSEDED → CURRENT
EXPIRED → ACTIVE
INVALIDATED → EXECUTABLE
COMPLETED → ACTIVE
```

Expected behavior:

```text
REJECT
```

unless a specific restoration contract exists.

---

# 26. Version-Confusion Campaign

Create:

```text
D1_v1
D1_v2
```

Then attempt:

```text
Approval(v1)
→ Execution(v2)
```

Expected:

```text
reject / revalidate
```

depending on materiality.

---

# 27. Provenance-Poisoning Campaign

Attempt to:

```text
modify source identity
replace provenance
alter timestamp
forge evaluator
remove lineage
substitute evidence
```

Expected:

```text
integrity failure
```

or:

```text
assurance invalidation
```

---

# 28. Evidence-Poisoning Campaign

Introduce:

```text
false evidence
stale evidence
contradictory evidence
misattributed evidence
tampered evidence
irrelevant evidence
```

Verify that the assurance system detects:

```text
invalid evidence
insufficient evidence
conflicting evidence
```

---

# 29. Security-Gate Campaign

Attempt execution while:

```text
security state = BLOCKED
```

Variants:

```text
race condition
cached decision
tool bypass
alternate execution path
recovery path
emergency path
```

Expected:

```text
NO UNAUTHORIZED EXECUTION
```

---

# 30. Tool Manipulation Campaign

Test:

```text
malicious tool output
malformed tool output
unexpected tool side effect
tool identity confusion
tool authorization confusion
tool result injection
```

The architecture should distinguish:

```text
tool output
```

from:

```text
trusted fact
```

unless independently verified.

---

# 31. Memory / Retrieval Campaign

Attempt:

```text
stale memory retrieval
wrong-version retrieval
provenance mismatch
poisoned memory
context collision
retrieval substitution
```

Verify that retrieved content does not silently become authoritative without required validation.

---

# 32. Self-Critique Evasion Campaign

Produce outputs designed to fool the self-critic:

```text
subtle contradiction
buried constraint violation
plausible false premise
misleading confidence
long-context distraction
semantic ambiguity
```

Measure:

```text
detection
false reassurance
error localization
```

---

# 33. Adversarial-Verifier Evasion Campaign

Attempt to fool the adversarial verifier with:

```text
attack camouflage
rare edge cases
distribution shifts
novel compositions
deceptive formatting
counterexample obfuscation
```

The objective is to measure:

```text
false-negative rate
```

rather than only attack success.

---

# 34. Producer–Verifier Capability Campaign

Increase producer capability:

```text
basic
advanced
expert
adversarial
```

and measure verifier detection.

Record:

```text
difficulty
detection
false negatives
attack class
severity
```

This directly tests the capability-asymmetry hypothesis from IV-006.

---

# 35. Self-Modification Campaign

Attempt:

```text
model proposes change
 ↓
change modifies verification
 ↓
change weakens its own constraints
 ↓
system approves itself
```

Expected:

```text
governance boundary blocks self-certifying modification.
```

---

# 36. Assurance Manipulation Campaign

Attempt to manipulate:

```text
assurance level
verification status
evidence references
timestamps
evaluator identity
counterexample status
```

Expected:

```text
integrity violation
```

or:

```text
assurance invalidation
```

---

# 37. Recovery Campaign

Inject:

```text
partial failure
state corruption
dependency loss
tool failure
execution interruption
verification failure
```

Then evaluate:

```text
recovery authorization
state reconstruction
rollback correctness
audit completeness
assurance impact
```

---

# 38. Rollback Abuse Campaign

Attempt:

```text
rollback without authority
rollback past security changes
rollback to revoked authority
rollback to superseded policy
rollback without audit
```

Expected:

```text
REJECT
```

or:

```text
CONTROLLED RECOVERY
```

according to contract.

---

# 39. Concurrency Campaign

Create simultaneous events:

```text
approval
revocation
policy change
security block
execution request
```

The objective is to detect:

```text
TOCTOU
race conditions
lost updates
stale authorization
non-deterministic resolution
```

---

# 40. Composition Attacks

A critical category is:

```text
A safe alone
+
B safe alone
+
C safe alone
=
unsafe combination
```

Examples:

```text
valid delegation
+
valid tool
+
valid execution intent
=
authority escalation
```

or:

```text
valid approval
+
valid policy
+
stale security state
=
unsafe execution
```

The red team must therefore test combinations, not only individual components.

---

# 41. Dependency-Cascade Campaign

Change an upstream dependency:

```text
evidence
policy
authority
goal
security state
context
```

Then observe downstream:

```text
decision
approval
execution intent
assurance
```

Verify that propagation matches IV-003 and IV-005.

---

# 42. Blast-Radius Measurement

For each injected failure record:

```text
directly affected objects
indirectly affected objects
unaffected objects
unexpectedly affected objects
```

Unexpected blast radius is a significant finding.

---

# 43. Local-vs-Global Failure Campaign

Inject:

```text
one local artifact failure
```

Expected:

```text
local containment
```

Then inject:

```text
shared dependency failure
```

Expected:

```text
broader invalidation / rebase / escalation
```

The system must not confuse the two.

---

# 44. Failure Containment

Every critical failure should have an intended containment boundary:

```text
component
agent
decision
authority
execution
campaign
system
```

A failure that escapes its intended boundary is a containment failure.

---

# 45. Detection Latency

Record:

```text
failure_time
detection_time
containment_time
recovery_time
```

Derived metrics:

```text
time_to_detect
time_to_contain
time_to_recover
```

---

# 46. Silent Failure

A silent failure is:

```text
system violates a required property
without producing the expected signal.
```

Silent failures are particularly severe because they can produce:

```text
false assurance.
```

---

# 47. False Reassurance Campaign

Deliberately create materially flawed cases and measure whether the system reports:

```text
SUPPORTED
```

or equivalent acceptance.

The principal metric is:

```text
FALSE_REASSURANCE_RATE
```

This should be treated as a first-class system metric.

---

# 48. False Alarm Campaign

Also measure:

```text
false positive
```

because an adversarial verifier that rejects everything is not useful.

The goal is:

```text
high detection
+
acceptable precision
```

not maximum rejection.

---

# 49. Attack Coverage

Coverage should include:

```text
attack-class coverage
state coverage
authority coverage
dependency coverage
tool coverage
model-behavior coverage
failure-severity coverage
composition coverage
```

---

# 50. Attack Novelty

A mature red-team process should distinguish:

```text
known attack
variant attack
novel attack
```

Novel attacks are particularly valuable because they test generalization.

---

# 51. Attack Generation

Attack generation can combine:

```text
manual red-team design
property-based generation
mutation testing
LLM adversarial generation
randomized testing
state-machine exploration
dependency graph exploration
```

LLM-generated attacks must themselves be evaluated for usefulness.

---

# 52. Mutation Testing

Take a valid implementation and deliberately introduce mutations:

```text
remove authority check
invert condition
skip revocation
accept expired state
ignore version
bypass constraint
alter precedence
```

Then verify that the test and assurance stack catches the mutation.

This provides strong evidence about test sensitivity.

---

# 53. Property-Based Fuzzing

Generate inputs satisfying broad categories:

```text
valid
near-valid
invalid
adversarial
ambiguous
boundary
```

The objective is to search state/input spaces rather than only manually selected examples.

---

# 54. State-Machine Fuzzing

Generate transition sequences such as:

```text
DRAFT → VALIDATED → APPROVED → ACTIVE
```

and adversarial sequences such as:

```text
DRAFT → ACTIVE
REVOKED → ACTIVE
EXPIRED → EXECUTE
SUPERSEDED → APPROVE
```

Verify the state machine rejects invalid paths.

---

# 55. Dependency-Graph Fuzzing

Generate:

```text
chains
branches
shared dependencies
cycles
deep delegation
```

and measure:

```text
invalidation propagation
blast radius
cycle detection
recovery
```

---

# 56. Evidence Mutation

Mutate:

```text
source
timestamp
version
content
lineage
evaluator
integrity metadata
```

The evidence and assurance systems should detect relevant mutations.

---

# 57. Verifier Mutation

Deliberately weaken the verifier:

```text
remove one check
reduce attack space
alter threshold
remove independence
use stale evidence
```

Then verify whether the broader assurance system detects that the verifier itself has degraded.

---

# 58. Red-Team / Blue-Team Separation

Where feasible:

```text
BLUE TEAM
implements and defends

RED TEAM
attacks claims

JUDGE
evaluates whether failures are real
```

The red team should not control final pass/fail interpretation.

---

# 59. Human Red Team

Human adversaries should be used for high-impact claims where automated attacks may miss:

```text
semantic loopholes
organizational loopholes
policy ambiguity
unexpected compositions
social-engineering-like pathways
```

---

# 60. Red-Team Safety Boundary

The red-team framework must have:

```text
scope restrictions
execution sandbox
rollback
kill switch
credential isolation
data isolation
audit logging
```

No adversarial experiment should create uncontrolled real-world side effects.

---

# 61. Finding Record

Every finding should contain:

```yaml
finding:
  finding_id: ...
  campaign_ref: ...
  target_ref: ...
  claim_ref: ...
  attack_ref: ...
  severity: ...
  exploitability: ...
  observed_behavior: ...
  expected_behavior: ...
  evidence_refs: []
  reproduction: ...
  containment_status: ...
  remediation_status: ...
  assurance_impact: ...
```

---

# 62. Finding Lifecycle

```text
DISCOVERED
 ↓
TRIAGED
 ↓
REPRODUCED
 ↓
CONFIRMED
 ↓
CONTAINED
 ↓
FIXED
 ↓
REGRESSION TESTED
 ↓
REVERIFIED
 ↓
CLOSED
```

A finding must not be marked closed merely because the original symptom disappeared.

---

# 63. Unresolved Finding

A finding remains open when:

```text
not reproducible
but plausible and high-impact
```

unless the evidence demonstrates that the concern is invalid.

High-impact uncertainty must not be silently discarded.

---

# 64. Assurance Impact

Each confirmed finding must evaluate:

```text
which claims are affected?
which evidence is invalidated?
which assurance records become stale?
which downstream objects require reassessment?
```

---

# 65. Counterexample-to-Claim Mapping

A counterexample should map to:

```text
claim
proof obligation
implementation
test
verification layer
assurance record
```

This allows systemic learning.

---

# 66. Regression Rule

A confirmed counterexample should become:

```text
permanent regression test
```

unless a documented reason exists not to.

This prevents the system from repeatedly rediscovering the same failure.

---

# 67. Regression Failure

If a previously fixed counterexample returns:

```text
REGRESSION
```

The affected assurance claims should be reassessed automatically or through the appropriate governance path.

---

# 68. Assurance Revocation Trigger

A confirmed critical failure should be capable of triggering:

```text
ASSURANCE REASSESSMENT
```

and where required:

```text
ASSURANCE REVOCATION
```

---

# 69. Red-Team Metrics

At minimum:

```text
attack attempts
unique attack classes
novel attacks
counterexamples
confirmed failures
false positives
false negatives
severity-weighted findings
detection latency
containment latency
recovery latency
regression recurrence
false reassurance rate
```

---

# 70. Coverage Metrics

Track:

```text
attack-surface coverage
state-space coverage
authority-path coverage
dependency-path coverage
failure-class coverage
tool-path coverage
verification-layer coverage
```

Coverage numbers must be accompanied by methodology.

---

# 71. Campaign Exit Criteria

A campaign should not end merely because:

```text
no failures were found.
```

It should end when:

```text
attack objectives were exhausted
OR
defined coverage thresholds were reached
OR
risk budget was exhausted
OR
campaign was superseded
```

The chosen termination reason must be recorded.

---

# 72. Red-Team Failure of the Red Team

The red-team mechanism itself may fail through:

```text
narrow attack model
test-set overfitting
shared assumptions
weak attack generation
limited tool access
insufficient capability
```

Therefore red-team effectiveness must itself be evaluated.

---

# 73. Red-Team Benchmark

Construct seeded vulnerabilities:

```text
V1 authority bypass
V2 stale approval
V3 provenance poisoning
V4 lifecycle violation
V5 security race
V6 self-critique evasion
V7 adversarial-verifier evasion
V8 self-modification bypass
```

Measure discovery.

Then introduce hidden vulnerabilities.

Measure generalization.

---

# 74. Red-Team Capability Asymmetry

Test:

```text
attack-generator capability
        vs
system defensive capability
```

If the attack generator is weaker than the target, successful attack absence may mean little.

Therefore use:

```text
multiple attack generators
manual experts
mutation testing
property-based generation
```

where appropriate.

---

# 75. Composed Attack Campaign

The highest-value attacks may combine:

```text
authority
+
version confusion
+
tool manipulation
+
security race
```

because real failures may emerge only through composition.

---

# 76. Multi-Agent Attack

Test whether multiple agents can accidentally create an authority escalation:

```text
Agent A
 ↓
delegates
Agent B
 ↓
tool
 ↓
Agent C
 ↓
execution
```

Each local step may appear valid while the complete chain violates global authority.

---

# 77. Human-in-the-Loop Attack

Test:

```text
ambiguous approval
approval fatigue
context mismatch
approval substitution
stale approval presentation
```

The objective is not to attack humans personally.

It is to test whether governance semantics remain intact when human decisions interact with system state.

---

# 78. Emergency-Mode Attack

Emergency pathways often create exceptions.

Test:

```text
normal security boundary
 ↓
emergency mode
 ↓
attempt unrelated privileged action
```

Verify that emergency authority is:

```text
scoped
time-bounded
audited
revocable
```

---

# 79. Recovery-Mode Attack

Attempt to use recovery mechanisms to bypass ordinary authorization:

```text
failure
 ↓
recovery
 ↓
privileged operation
```

Recovery must not become an implicit escalation channel.

---

# 80. Assurance-Mode Attack

Attempt to manipulate the assurance layer itself:

```text
fake PASS
change assurance level
hide counterexample
remove evidence
alter evaluator
```

A system whose assurance ledger can be manipulated is not assured.

---

# 81. Red-Team Evidence Requirements

A red-team result is evidence only when:

```text
attack reproducible
target version known
expected behavior known
observed behavior recorded
environment known
```

Otherwise classify as:

```text
UNCONFIRMED FINDING
```

rather than confirmed failure.

---

# 82. Reproduction Requirement

High-severity findings should have:

```text
minimal reproduction
```

where possible.

This improves:

```text
repair
regression
independent verification
```

---

# 83. Failure Injection and Real-World Safety

Failure injection should occur in:

```text
sandbox
test environment
isolated staging
simulation
```

unless a production-safe protocol explicitly authorizes a narrowly scoped test.

---

# 84. Falsification of Core Claims

The campaign should ultimately target:

```text
C1 — Authority cannot be escalated
C2 — Constraints cannot be bypassed
C3 — Security boundary cannot be bypassed
C4 — Lifecycle invalidation propagates correctly
C5 — Provenance remains trustworthy
C6 — Decisions remain bound to their dependencies
C7 — Approvals remain bound to decisions
C8 — Self-critique detects measurable classes of errors
C9 — Adversarial verification discovers measurable classes of failures
C10 — Independent verification reduces false reassurance
C11 — Self-modification remains governed
C12 — Assurance is invalidated when its basis becomes invalid
```

These become the primary red-team campaign targets.

---

# 85. Campaign Matrix

| Claim | Attack classes | Failure injection | Independent judge | Status |
|---|---|---|---|---|
| Authority containment | A2,A3,A7,A18 | revoke/expire/scope mutation | Required | OPEN |
| Constraint enforcement | A4,A5,A18 | constraint mutation | Required | OPEN |
| Security non-bypass | A10,A11,A17 | security block/race | Required | OPEN |
| Lifecycle consistency | A6,A7,A17 | invalid transitions | Recommended | OPEN |
| Provenance integrity | A8,A9 | metadata mutation | Recommended | OPEN |
| Decision dependency integrity | A6,A7,A18 | stale dependency | Required | OPEN |
| Approval binding | A2,A6,A7 | version substitution | Required | OPEN |
| Self-critique | A12 | seeded hidden errors | Required | OPEN |
| Adversarial verifier | A13 | verifier evasion | Required | OPEN |
| Self-modification governance | A14 | verification bypass | Required | OPEN |
| Assurance integrity | A16 | ledger manipulation | Required | OPEN |
| Recovery safety | A15,A17 | partial failure | Required | OPEN |

---

# 86. System-Wide Falsification Campaign

Eventually run a composed campaign:

```text
PHASE 1 — COMPONENT ATTACKS
        ↓
PHASE 2 — CROSS-COMPONENT ATTACKS
        ↓
PHASE 3 — STATE / TEMPORAL ATTACKS
        ↓
PHASE 4 — MULTI-AGENT ATTACKS
        ↓
PHASE 5 — VERIFIER ATTACKS
        ↓
PHASE 6 — ASSURANCE ATTACKS
        ↓
PHASE 7 — UNKNOWN / NOVEL ATTACK SEARCH
```

The final phase is explicitly intended to search beyond known failure categories.

---

# 87. Unknown Failure Search

Methods may include:

```text
property-based exploration
LLM attack generation
mutation testing
randomized state exploration
dependency graph search
novel composition generation
human red teaming
```

The objective is not to guarantee discovery of unknown failures.

It is to increase the probability of discovering them.

---

# 88. Falsification Budget

A campaign should record resources:

```text
time
compute
attack attempts
human hours
test cases
models
tools
```

A statement such as:

```text
"no failures found"
```

is meaningless without knowing how aggressively the system was searched.

---

# 89. Negative Result Interpretation

A negative red-team result means:

```text
NO FAILURE FOUND
UNDER THE EXECUTED CAMPAIGN.
```

It does not mean:

```text
NO FAILURE EXISTS.
```

The campaign scope must always accompany the result.

---

# 90. Red-Team Report

Each campaign should produce:

```text
scope
threat model
attack surface
attack classes
coverage
findings
counterexamples
false positives
unresolved risks
assurance impact
limitations
recommendations
```

---

# 91. Integration with Assurance

The final relationship is:

```text
RED-TEAM FINDING
 ↓
COUNTEREXAMPLE
 ↓
ASSURANCE IMPACT
 ↓
CLAIM DEMOTION
 ↓
REPAIR
 ↓
REGRESSION
 ↓
REVERIFICATION
 ↓
ASSURANCE PROMOTION
```

This creates a closed engineering loop.

---

# 92. Critical Invariants

### Invariant 1

Every high-impact architectural claim must have a defined falsification strategy.

### Invariant 2

Failure injection must be controlled and auditable.

### Invariant 3

Adversarial tests must include negative and boundary cases.

### Invariant 4

A successful attack is permanent evidence until explicitly superseded by a verified repair.

### Invariant 5

A confirmed counterexample must affect the relevant assurance status.

### Invariant 6

No-failure results must retain campaign scope and limitations.

### Invariant 7

The red-team mechanism itself must be evaluated.

### Invariant 8

Composed attacks must be tested.

### Invariant 9

Recovery mechanisms must not become authority-escalation channels.

### Invariant 10

Assurance records must be attackable and integrity-protected.

### Invariant 11

Critical findings require reproducible evidence where feasible.

### Invariant 12

Failure discovery should generate regression coverage.

---

# 93. Exit Criteria

- [x] Falsification objective defined
- [x] Falsification target defined
- [x] Threat model requirements defined
- [x] Attack classes defined
- [x] Attack surfaces defined
- [x] Failure-injection principle defined
- [x] Failure-injection classes defined
- [x] Controlled injection requirements defined
- [x] Red-team campaign record defined
- [x] Failure severity defined
- [x] Authority escalation campaign defined
- [x] Revocation campaign defined
- [x] Expiration campaign defined
- [x] Delegation campaign defined
- [x] Constraint bypass campaign defined
- [x] Policy conflict campaign defined
- [x] Lifecycle attack campaign defined
- [x] Version-confusion campaign defined
- [x] Provenance/evidence poisoning defined
- [x] Security-gate attacks defined
- [x] Tool manipulation defined
- [x] Memory/retrieval attacks defined
- [x] Self-critique evasion defined
- [x] Adversarial-verifier evasion defined
- [x] Producer/verifier capability testing defined
- [x] Self-modification attacks defined
- [x] Assurance manipulation attacks defined
- [x] Recovery/rollback attacks defined
- [x] Concurrency attacks defined
- [x] Composition attacks defined
- [x] Dependency-cascade testing defined
- [x] Blast-radius measurement defined
- [x] Detection/containment/recovery latency defined
- [x] False-reassurance campaign defined
- [x] Mutation testing defined
- [x] State-machine fuzzing defined
- [x] Evidence mutation defined
- [x] Verifier mutation defined
- [x] Finding lifecycle defined
- [x] Assurance impact defined
- [x] Regression requirements defined
- [x] Red-team metrics defined
- [x] Campaign exit criteria defined
- [x] System-wide campaign defined
- [x] Unknown-failure search defined
- [x] Falsification budget defined
- [x] Negative-result interpretation defined
- [x] Core claim campaign matrix defined

**Current assessment:** IV-008 establishes failure discovery as a first-class engineering capability. The architecture now has a defined path from claim → attack → counterexample → repair → regression → reverification → assurance update. The next stage should formalize how these campaigns are scheduled, isolated, executed, and reported across the entire system.

---

# 94. Next Document

**IV-009 — Verification Runtime, Evaluation Harness & Experimental Control Specification**

IV-009 will define the actual infrastructure required to execute IV-006 through IV-008 reproducibly:

```text
TEST CASE
 ↓
CONTROLLED ENVIRONMENT
 ↓
TARGET VERSION
 ↓
ATTACK / EVALUATION
 ↓
OBSERVATION
 ↓
EVIDENCE CAPTURE
 ↓
JUDGE
 ↓
RESULT
 ↓
REGRESSION / ASSURANCE UPDATE
```

It should cover:

```text
sandboxing
experiment isolation
dataset/version control
seed management
reproducibility
evaluation harnesses
model/version pinning
tool isolation
telemetry
evidence capture
judge separation
benchmark management
failure replay
experiment provenance
```

This will be the infrastructure layer required before we can claim that our verification results are experimentally trustworthy.
