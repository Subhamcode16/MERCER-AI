# IV-012 — Assurance-Gated Execution, Release & Governance Control Specification

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-006, IV-007, IV-008, IV-009, IV-010, IV-011

---

# 1. Purpose

IV-012 defines how assurance becomes an operational control.

The preceding documents established:

```text
IV-006 → verification architecture
IV-007 → coverage and assurance gaps
IV-008 → falsification and red-team testing
IV-009 → controlled experimental execution
IV-010 → assurance evidence graph and ledger
IV-011 → conservative assurance computation
```

IV-012 answers:

```text
GIVEN THE CURRENT ASSURANCE STATE,
WHAT IS THE SYSTEM ACTUALLY ALLOWED TO DO?
```

The governing principle is:

```text
ASSURANCE
→
INFORMS / GATES DECISIONS

ASSURANCE
≠
AUTHORITY
```

---

# 2. Core Principle

A system must not infer permission from confidence.

The operational chain is:

```text
REQUEST
 ↓
IDENTITY
 ↓
AUTHORITY
 ↓
CONSTRAINTS
 ↓
ASSURANCE REQUIREMENT
 ↓
ASSURANCE STATE
 ↓
SECURITY POLICY
 ↓
DECISION
 ↓
EXECUTION
```

Assurance is one control input among several.

---

# 3. Separation of Concerns

The architecture must preserve:

```text
AUTHORITY
=
may this actor perform this action?

ASSURANCE
=
how well supported is the knowledge relevant to this action?

POLICY
=
under what conditions is this action permitted?

SECURITY
=
is execution currently safe?

DECISION
=
what should happen now?
```

These must not be collapsed.

---

# 4. Execution Gate Model

A high-impact action should pass through:

```text
ACTION REQUEST
        ↓
AUTHENTICATION
        ↓
AUTHORIZATION
        ↓
CONSTRAINT VALIDATION
        ↓
ASSURANCE GATE
        ↓
SECURITY GATE
        ↓
EXECUTION POLICY
        ↓
EXECUTE / BLOCK / ESCALATE
```

---

# 5. Gate Types

Candidate gates:

```text
IDENTITY_GATE
AUTHORITY_GATE
CONSTRAINT_GATE
ASSURANCE_GATE
SECURITY_GATE
RESOURCE_GATE
HUMAN_APPROVAL_GATE
RATE_GATE
ENVIRONMENT_GATE
```

Each gate should have explicit semantics.

---

# 6. Gate Independence

A failed gate must not be silently bypassed because another gate succeeded.

Example:

```text
ASSURANCE = HIGH
AUTHORITY = INVALID
```

must remain:

```text
BLOCKED
```

---

# 7. Assurance Gate

An assurance gate evaluates:

```text
required assurance level
current assurance level
scope compatibility
freshness
open counterexamples
limitations
```

It should return:

```text
PASS
BLOCK
ESCALATE
DEGRADED
```

---

# 8. Required Assurance

Each action class may define:

```yaml
assurance_requirement:
  action_class: ...
  minimum_status: ...
  required_obligations: []
  freshness_requirement: ...
  independence_requirement: ...
  counterexample_policy: ...
```

---

# 9. Risk-Based Assurance Requirements

Higher-impact actions should require stronger evidence.

Conceptually:

```text
LOW IMPACT
→
basic assurance

MEDIUM IMPACT
→
verified assurance

HIGH IMPACT
→
adversarial + independent assurance

IRREVERSIBLE / CRITICAL
→
maximum applicable assurance
+
additional governance controls
```

Exact thresholds belong to policy.

---

# 10. Authority Remains Separate

Even when:

```text
assurance requirement = satisfied
```

the system must still verify:

```text
actor authority
action scope
delegation
expiration
revocation
constraints
```

---

# 11. No Assurance Escalation

A critical invariant:

```text
ASSURANCE LEVEL
        ↓
must never
        ↓
CREATE AUTHORITY
```

A well-verified proposition does not give the agent permission to act.

---

# 12. Decision Record

Every gated decision should produce a structured record:

```yaml
decision:
  decision_id: ...
  request_id: ...
  authority_result: ...
  constraint_result: ...
  assurance_result: ...
  security_result: ...
  policy_result: ...
  outcome: ...
  reason: ...
  evidence_refs: []
```

---

# 13. Decision Outcomes

Candidate outcomes:

```text
ALLOW
DENY
BLOCK
ESCALATE
REQUIRE_HUMAN_APPROVAL
DEGRADE
RETRY_VERIFICATION
```

---

# 14. Allow

`ALLOW` means all mandatory gates have satisfied their requirements under the applicable policy.

It does not mean:

```text
action is guaranteed to succeed
```

or:

```text
action is universally safe
```

---

# 15. Deny

`DENY` means the action is not permitted under current authority or policy.

Examples:

```text
invalid authority
prohibited action
scope violation
```

---

# 16. Block

`BLOCK` means execution is prevented because a required safety, assurance, security, or operational condition is not satisfied.

---

# 17. Escalate

`ESCALATE` means the system cannot safely resolve the decision within its current authority or evidence state.

Escalation may route to:

```text
human
higher-trust agent
security controller
governance service
```

---

# 18. Human Approval

Human approval should be explicit where required.

The approval record should contain:

```text
request
scope
risk
assurance state
limitations
proposed action
approver
timestamp
expiration
```

---

# 19. Human Approval Is Not Proof

A human approval does not transform insufficient evidence into verified knowledge.

It changes the governance decision.

Therefore:

```text
HUMAN APPROVAL
≠
ASSURANCE
```

---

# 20. Approval Scope

Approvals must be:

```text
specific
bounded
time-limited
revocable
auditable
```

Avoid:

```text
"approved for everything"
```

---

# 21. Assurance Failure

If required assurance is missing:

```text
ACTION
 ↓
ASSURANCE GATE
 ↓
FAIL
```

default behavior should be:

```text
BLOCK
```

unless policy explicitly defines:

```text
ESCALATE
DEGRADE
```

---

# 22. Assurance Uncertainty

If assurance is:

```text
UNKNOWN
```

the system must not interpret that as:

```text
SAFE
```

or:

```text
UNSAFE
```

It should use the action policy to determine whether:

```text
block
escalate
request additional verification
```

is appropriate.

---

# 23. Stale Assurance

If assurance is stale:

```text
CURRENT ACTION
 ↓
STALE ASSURANCE
 ↓
REASSESSMENT
```

unless the policy explicitly allows bounded use of stale evidence.

---

# 24. Counterexample Gate

For critical actions:

```text
OPEN CRITICAL COUNTEREXAMPLE
```

should normally result in:

```text
BLOCK
```

or:

```text
ESCALATE
```

---

# 25. Resolved Counterexamples

A counterexample is not considered resolved merely because:

```text
a developer changed code
```

Resolution requires:

```text
repair
+
reproduction
+
regression
+
reverification
```

as established by IV-008 and IV-009.

---

# 26. Security Gate

The security gate independently evaluates:

```text
current security state
credentials
network
device
threat state
policy
runtime integrity
```

Assurance cannot override a security block.

---

# 27. Constraint Gate

Validate:

```text
preconditions
resource limits
scope
time bounds
location/environment bounds
dependency requirements
```

---

# 28. Resource Gate

Before execution verify:

```text
CPU
memory
storage
network
API quotas
tool availability
external resources
```

where relevant.

---

# 29. Environment Gate

Some actions may only be allowed in:

```text
simulation
staging
sandbox
production
```

The gate verifies environment compatibility.

---

# 30. Tool Execution Gate

Before a tool call:

```text
tool authorized?
 ↓
action authorized?
 ↓
assurance sufficient?
 ↓
constraints valid?
 ↓
security valid?
 ↓
execute
```

---

# 31. External Side-Effect Gate

Actions producing external effects should require elevated controls.

Examples:

```text
send message
write database
publish content
execute financial action
modify infrastructure
change security policy
```

---

# 32. Irreversibility

Classify actions by reversibility:

```text
READ-ONLY
REVERSIBLE
PARTIALLY REVERSIBLE
IRREVERSIBLE
```

Irreversible actions should require stronger controls.

---

# 33. Blast Radius

Every consequential action should estimate:

```text
scope
affected resources
affected users
duration
reversibility
dependency impact
```

Higher blast radius should increase gate requirements.

---

# 34. Transaction Boundary

Where possible:

```text
PREPARE
 ↓
VALIDATE
 ↓
APPROVE
 ↓
EXECUTE
 ↓
VERIFY RESULT
```

Avoid partially authorized execution.

---

# 35. Pre-Execution Verification

Immediately before execution, revalidate:

```text
authority
constraints
assurance freshness
security
environment
resource limits
```

This prevents stale approval.

---

# 36. TOCTOU Protection

The system should guard against:

```text
CHECK
 ↓
state changes
 ↓
USE
```

where the state relevant to the decision changes between verification and execution.

---

# 37. Decision Binding

Where appropriate, bind the authorization decision to:

```text
request
target
action
scope
version
constraints
assurance snapshot
expiration
```

---

# 38. Decision Expiration

High-risk decisions should expire after:

```text
time interval
state change
policy change
assurance change
authority change
```

---

# 39. Re-Authorization

If a decision expires:

```text
old decision
→
invalid
```

and the action requires:

```text
new authorization
new gate evaluation
```

---

# 40. Post-Execution Verification

After execution:

```text
EXPECTED RESULT
vs
OBSERVED RESULT
```

should be evaluated.

This can produce:

```text
SUCCESS
FAILURE
PARTIAL_SUCCESS
UNEXPECTED_SIDE_EFFECT
```

---

# 41. Post-Execution Evidence

Record:

```text
action
inputs
authorization
assurance snapshot
execution trace
result
side effects
errors
```

This can feed IV-010.

---

# 42. Unexpected Side Effects

If the system produces an unapproved side effect:

```text
EXECUTION
 ↓
UNEXPECTED EFFECT
 ↓
SECURITY / ASSURANCE EVENT
 ↓
REVIEW
```

Severity determines whether execution is halted.

---

# 43. Release Gate

A release may require:

```text
critical claims assured
critical counterexamples resolved
verification coverage sufficient
security tests passed
regression suite passed
evidence current
```

---

# 44. Release Policy

Release requirements should be declarative:

```yaml
release_policy:
  release_class: ...
  required_claims: []
  minimum_assurance: ...
  blocking_counterexamples: ...
  required_tests: []
  required_approvals: []
```

---

# 45. Release Decision

Conceptually:

```text
CANDIDATE BUILD
 ↓
DEPENDENCY CHECK
 ↓
REGRESSION
 ↓
SECURITY
 ↓
ASSURANCE
 ↓
GOVERNANCE
 ↓
RELEASE / BLOCK
```

---

# 46. No Single-Test Release

Critical release decisions must not depend on one test or one verifier.

They should reference the assurance graph.

---

# 47. Release Evidence Package

Every release should have:

```text
version
claims
assurance snapshot
verification results
counterexample status
security results
dependency manifest
known limitations
approval records
```

---

# 48. Release Rollback

If post-release evidence invalidates a critical assurance claim:

```text
NEW EVIDENCE
 ↓
ASSURANCE DEMOTION
 ↓
RELEASE IMPACT ANALYSIS
 ↓
ROLLBACK / PATCH / RESTRICT
```

---

# 49. Rollback Authority

Rollback should itself be governed.

The system must define:

```text
who may rollback
under which conditions
which components
what evidence is required
```

---

# 50. Emergency Path

Emergency controls may bypass normal throughput but should not silently bypass:

```text
audit
authority
security
post-event review
```

---

# 51. Emergency Shutdown

A critical failure may trigger:

```text
HALT EXECUTION
 ↓
REVOKE TEMPORARY AUTHORITY
 ↓
ISOLATE SYSTEM
 ↓
PRESERVE EVIDENCE
 ↓
ESCALATE
```

---

# 52. Fail-Closed vs Fail-Safe

Different controls may require different failure semantics.

Example:

```text
security boundary
→ fail closed
```

while:

```text
non-critical informational service
→ degraded mode
```

The policy must specify the correct behavior.

---

# 53. Degraded Mode

A degraded system may reduce capability:

```text
external writes disabled
tool access restricted
read-only mode
human approval required
local execution only
```

---

# 54. Degraded Assurance

If assurance decreases but the system remains usable:

```text
ASSURANCE DEMOTION
 ↓
CAPABILITY REDUCTION
```

rather than necessarily:

```text
TOTAL SHUTDOWN
```

This should be policy-driven.

---

# 55. Capability Matrix

Maintain:

```text
capability
required assurance
required authority
security conditions
human approval
environment
```

Example:

```yaml
capability:
  name: external_write
  assurance: A5
  authority: elevated
  security: strict
  approval: required
```

---

# 56. Capability Downgrade

When assurance falls:

```text
A5
 ↓
A3
```

the capability set may change:

```text
write
 ↓
read-only
```

This creates graceful degradation.

---

# 57. Assurance-Aware Planner

Planning components may use assurance to select among:

```text
high-risk plan
low-risk plan
simulation
human escalation
```

But planning must still obey authority and policy.

---

# 58. Verification Before Action

For uncertain plans:

```text
PLAN
 ↓
VERIFY
 ↓
EXECUTE
```

rather than:

```text
PLAN
 ↓
EXECUTE
 ↓
discover uncertainty
```

where practical.

---

# 59. Action Preconditions

An action should have:

```yaml
action_preconditions:
  authority: ...
  assurance: ...
  security: ...
  environment: ...
  resources: ...
  human_approval: ...
```

---

# 60. Action Postconditions

After execution verify:

```yaml
action_postconditions:
  expected_state: ...
  expected_effect: ...
  prohibited_effects: []
  evidence_required: []
```

---

# 61. Governance Escalation

Escalate when:

```text
assurance conflict
authority ambiguity
policy conflict
security uncertainty
high-impact action
unresolved counterexample
```

---

# 62. Escalation Package

Provide the reviewer:

```text
request
proposed action
authority
assurance state
evidence
limitations
counterexamples
risk
alternatives
```

The reviewer should not need to reconstruct the entire graph manually.

---

# 63. Human Review UX Principle

The system should expose:

```text
WHAT DO WE KNOW?
WHAT DON'T WE KNOW?
WHAT COULD GO WRONG?
WHAT AUTHORITY EXISTS?
WHAT ACTION IS PROPOSED?
WHY IS IT BLOCKED / ALLOWED?
```

rather than merely:

```text
PASS / FAIL
```

---

# 64. Governance Audit Trail

Every override should create:

```text
override event
reason
actor
scope
expiration
evidence
```

---

# 65. Override Semantics

An override should be:

```text
bounded
explicit
auditable
revocable
```

An override must not silently modify the underlying assurance state.

---

# 66. Assurance Override

Avoid allowing:

```text
human says "I trust it"
```

to mutate:

```text
ASSURANCE = VERIFIED
```

Instead:

```text
GOVERNANCE OVERRIDE = TRUE
ASSURANCE = unchanged
```

---

# 67. Governance vs Epistemology

The system must preserve:

```text
EPISTEMIC STATE
```

and:

```text
GOVERNANCE DECISION
```

as separate records.

Example:

```text
Assurance = UNKNOWN
Governance = HUMAN_APPROVED_WITH_RISK
```

Both may be simultaneously true.

---

# 68. Policy Conflict

If:

```text
policy A = allow
policy B = deny
```

the system should not silently choose one.

It should invoke:

```text
policy precedence
conflict resolution
or escalation
```

---

# 69. Security Conflict

If:

```text
assurance = high
security = block
```

result:

```text
BLOCK
```

unless an explicitly authorized emergency policy applies.

---

# 70. Authority Conflict

If:

```text
actor A = authorized
delegation = expired
```

result:

```text
BLOCK
```

Assurance is irrelevant to the authority failure.

---

# 71. Assurance Conflict

If:

```text
verification = pass
counterexample = confirmed
```

result:

```text
REASSESSMENT_REQUIRED
```

and the action gate follows the resulting policy.

---

# 72. Release vs Runtime Gates

Separate:

```text
RELEASE ASSURANCE
```

from:

```text
RUNTIME ASSURANCE
```

A release may be sufficiently assured while a specific runtime action remains disallowed.

---

# 73. Continuous Runtime Revalidation

For long-running tasks, re-evaluate:

```text
authority
security
assurance
constraints
```

when material state changes.

---

# 74. Long-Running Action

A long-running operation should have:

```text
start authorization
mid-operation checks
completion verification
```

where risk warrants it.

---

# 75. Cancellation

Cancellation should be available when:

```text
assurance invalidated
authority revoked
security state worsens
constraint violated
unexpected side effect detected
```

---

# 76. Recovery

Recovery should follow:

```text
DETECT
 ↓
CONTAIN
 ↓
REVOKE
 ↓
RESTORE SAFE STATE
 ↓
VERIFY
 ↓
REASSESS
 ↓
RESUME / RETIRE
```

---

# 77. Recovery Assurance

Do not assume that:

```text
recovery succeeded
```

without verification.

Recovery itself requires:

```text
post-recovery evidence
```

---

# 78. Safe State

Every high-impact subsystem should define:

```text
SAFE STATE
```

and:

```text
HOW TO REACH IT
```

This becomes a recovery invariant.

---

# 79. Rollforward vs Rollback

Recovery may choose:

```text
rollback
```

or:

```text
rollforward
```

depending on the failure and governance policy.

---

# 80. Assurance During Recovery

During recovery:

```text
NORMAL ASSURANCE
```

may be temporarily unavailable.

The system should enter:

```text
DEGRADED
RECOVERY
or
LOCKDOWN
```

rather than pretending normal assurance remains valid.

---

# 81. Post-Incident Reassessment

After a critical incident:

```text
incident
 ↓
evidence capture
 ↓
counterexample
 ↓
assurance impact
 ↓
reverification
 ↓
release decision
```

---

# 82. Governance Metrics

Track:

```text
blocked actions
escalations
assurance failures
overrides
security blocks
release blocks
rollback events
unexpected side effects
```

---

# 83. Gate Effectiveness

Measure:

```text
true prevention
false blocks
missed unsafe actions
override frequency
```

A gate that blocks everything is not necessarily a good gate.

---

# 84. Assurance-Gate Testing

Test:

```text
valid assurance
invalid assurance
stale assurance
unknown assurance
counterexample
authority failure
security failure
policy conflict
human approval
expiration
```

---

# 85. Gate Compositionality

The system must test interactions such as:

```text
authority valid
+
assurance valid
+
security invalid
```

and:

```text
authority valid
+
assurance unknown
+
low-risk action
```

to ensure policy composition behaves as intended.

---

# 86. Gate Bypass Testing

IV-008 should include attempts to bypass:

```text
assurance gate
authority gate
security gate
human approval gate
release gate
```

through:

```text
alternate tools
delegation
race conditions
direct API calls
state manipulation
self-modification
```

---

# 87. Self-Modification Boundary

A self-modifying agent must not be able to:

```text
modify assurance rules
+
modify gate policy
+
certify the modification
```

through one authority path.

---

# 88. Independent Verification of Gate Changes

Changes to:

```text
assurance engine
gate logic
security policy
authority model
release policy
```

require independent verification according to risk.

---

# 89. Policy Version Binding

Decisions must identify:

```text
policy version
assurance rule version
authority policy version
security policy version
```

---

# 90. Decision Replay

Every important decision should be replayable:

```text
original request
+
policy versions
+
assurance snapshot
+
authority state
+
security state
        ↓
reconstructed decision
```

---

# 91. Decision Provenance

Decision records should link to:

```text
request
identity
authority
policy
assurance
evidence
execution
outcome
```

This integrates with IV-010.

---

# 92. Product Auditability

The product should eventually support:

```text
WHY WAS THIS ACTION ALLOWED?
```

and:

```text
WHY WAS THIS ACTION BLOCKED?
```

with an inspectable evidence trail.

---

# 93. User-Facing Explanation

Explanations must not expose sensitive internal information unnecessarily.

Use bounded disclosure:

```text
decision
reason category
required condition
safe next step
```

while preserving restricted evidence internally.

---

# 94. Fail-Safe Disclosure

Security-sensitive details should not be revealed merely because a user requests the reason for a block.

The explanation layer should respect information-access policy.

---

# 95. Critical Invariants

### Invariant 1

Assurance never creates authority.

### Invariant 2

A failed mandatory gate cannot be bypassed by success in another gate.

### Invariant 3

High assurance cannot override a security prohibition.

### Invariant 4

Human approval does not convert uncertainty into assurance.

### Invariant 5

Critical counterexamples cannot be ignored by the execution gate.

### Invariant 6

Expired decisions cannot authorize execution.

### Invariant 7

Material state changes require revalidation where policy requires it.

### Invariant 8

Irreversible actions require stronger controls than low-risk reversible actions.

### Invariant 9

Every high-impact decision must be auditable.

### Invariant 10

Every governance override must preserve the underlying epistemic state.

### Invariant 11

Release assurance and runtime assurance remain distinct.

### Invariant 12

Recovery must itself be verified.

### Invariant 13

Gate logic and assurance rules must be version-bound.

### Invariant 14

Self-modification cannot silently modify and certify its own control boundaries.

### Invariant 15

A blocked action must not be executable through an ungoverned alternate path.

---

# 96. Exit Criteria

- [x] Assurance-to-execution model defined
- [x] Separation of authority, assurance, policy, security, and decision defined
- [x] Gate architecture defined
- [x] Assurance gate defined
- [x] Risk-based assurance requirements defined
- [x] Authority separation defined
- [x] Decision record defined
- [x] Decision outcomes defined
- [x] Human approval semantics defined
- [x] Assurance failure/uncertainty semantics defined
- [x] Counterexample gate defined
- [x] Security/constraint/resource/environment gates defined
- [x] External side-effect gate defined
- [x] Irreversibility and blast radius defined
- [x] Transaction boundaries defined
- [x] Pre-execution and post-execution verification defined
- [x] TOCTOU protection defined
- [x] Decision binding and expiration defined
- [x] Release gate defined
- [x] Release evidence package defined
- [x] Rollback and emergency paths defined
- [x] Fail-closed/fail-safe distinction defined
- [x] Degraded mode defined
- [x] Capability matrix defined
- [x] Capability downgrade defined
- [x] Assurance-aware planning defined
- [x] Governance escalation defined
- [x] Override semantics defined
- [x] Governance/epistemology separation defined
- [x] Continuous runtime revalidation defined
- [x] Recovery semantics defined
- [x] Post-incident reassessment defined
- [x] Gate effectiveness metrics defined
- [x] Gate compositionality and bypass testing defined
- [x] Self-modification boundary defined
- [x] Policy/version binding defined
- [x] Decision replay/provenance defined
- [x] Product auditability defined
- [x] Core invariants defined

**Current assessment:** IV-012 connects the epistemic assurance architecture to operational behavior without allowing assurance to become an implicit authority mechanism. It establishes assurance gates, release gates, execution controls, escalation, degradation, rollback, recovery, and governance boundaries. This is the control-plane contract that determines how the system behaves when its knowledge is strong, weak, contradictory, stale, or unavailable.

---

# 97. Next Document

**IV-013 — Runtime Assurance Monitor, Continuous Reverification & Drift Detection Specification**

IV-013 should define how the system maintains assurance after deployment rather than assuming that a previously verified state remains valid forever.

It should cover:

```text
continuous monitoring
assurance freshness
implementation drift
model drift
policy drift
environment drift
behavioral drift
dependency drift
new counterexamples
runtime anomalies
continuous reverification
assurance invalidation
automatic capability downgrade
incident triggers
```

The central question becomes:

```text
HOW DO WE KNOW THAT AN ASSURED SYSTEM
IS STILL ASSURED AFTER IT HAS BEEN RUNNING IN THE REAL WORLD?
```
