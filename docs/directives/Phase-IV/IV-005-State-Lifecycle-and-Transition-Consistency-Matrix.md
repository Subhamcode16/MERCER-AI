# IV-005 — State, Lifecycle & Transition Consistency Matrix

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-002, IV-003, IV-004, III-005, III-006, III-008, III-011, III-012, III-014, III-015  
**Purpose:** Determine whether individually valid objects can form invalid combinations, and formalize lifecycle, transition, invalidation, supersession, revocation, rollback, recovery, and impossible-state requirements across the intelligence architecture.

---

# 1. Purpose

IV-005 addresses the next architectural question:

```text
CAN TWO OBJECTS EACH BE VALID
WHILE THEIR COMBINATION IS INVALID?
```

The answer is:

```text
YES.
```

This is a fundamental consequence of the dependency model established in IV-003.

Examples:

```text
valid approval
+
valid decision
+
decision superseded
=
invalid execution combination
```

or:

```text
valid delegation
+
valid authority
+
delegation revoked
=
invalid execution combination
```

or:

```text
valid assurance result
+
valid execution intent
+
security state changed
=
potentially invalid execution combination
```

Therefore object-level validity is insufficient.

The architecture requires:

```text
OBJECT VALIDITY
+
RELATIONAL VALIDITY
+
TEMPORAL VALIDITY
+
GOVERNANCE VALIDITY
=
EXECUTION ELIGIBILITY
```

---

# 2. Source Basis

This document builds on the cross-document analysis established in IV-003 and IV-004.

IV-003 established that object validity is dependency-sensitive and that upstream changes can invalidate downstream artifacts.

IV-004 established that governance is layered and that authority, capability, approval, security, constraints, decisions, and execution intent must remain distinct.

Existing engineering implementation also demonstrates explicit lifecycle responses such as:

```text
RETAIN
CORRECT
REGENERATE
REBASE
ESCALATE
```

for campaign-level failures, and distinguishes local failure from global failure. fileciteturn16file2L164-L174

The implementation also distinguishes hard drift from soft drift and maintains separate shot quality and campaign coherence dimensions. fileciteturn16file2L156-L168

These are engineering precedents, not complete lifecycle semantics for the entire intelligence architecture.

---

# 3. Core Thesis

A valid object is not necessarily valid **in relation to another object**.

Therefore:

```text
VALID(A)
+
VALID(B)
≠
VALID(A,B)
```

The architecture must explicitly evaluate relational consistency.

---

# 4. Four Validity Classes

Every consequential object should be evaluated across four conceptual dimensions.

## 4.1 Intrinsic Validity

Is the object internally well-formed?

```text
schema
required fields
type constraints
internal invariants
```

## 4.2 Relational Validity

Is the object compatible with its referenced objects?

```text
decision ↔ evidence
approval ↔ decision
execution ↔ authorization
delegation ↔ authority
assurance ↔ evaluated artifact
```

## 4.3 Temporal Validity

Is the object still valid at the current time/state?

```text
not expired
not revoked
not superseded
not invalidated
```

## 4.4 Governance Validity

Does the object remain valid under current:

```text
security
policy
constraints
authority
approval
```

---

# 5. Combined Validity Model

Conceptually:

```text
VALIDITY(object, context, time)
=
intrinsic
AND relational
AND temporal
AND governance
```

This is a conceptual model.

The final machine-readable implementation should be defined by the relevant runtime contracts.

---

# 6. Lifecycle State Is Not Validity

A common architectural error is:

```text
state = APPROVED
```

being interpreted as:

```text
currently executable
```

Instead:

```text
APPROVED
```

is one lifecycle fact.

Current execution eligibility is a derived property.

Therefore:

```text
state
≠
eligibility
```

---

# 7. Candidate Lifecycle States

The following states are useful analytical categories:

```text
DRAFT
PROPOSED
VALIDATED
AUTHORIZED
APPROVED
ACTIVE
SUSPENDED
REVOKED
EXPIRED
SUPERSEDED
INVALIDATED
COMPLETED
FAILED
ABORTED
ARCHIVED
```

Not every object should support every state.

Each contract must define its own permitted state machine.

---

# 8. State Categories

The states can be grouped into:

### Pre-activation

```text
DRAFT
PROPOSED
VALIDATED
```

### Governance

```text
AUTHORIZED
APPROVED
```

### Operational

```text
ACTIVE
SUSPENDED
```

### Terminal / Invalidating

```text
REVOKED
EXPIRED
SUPERSEDED
INVALIDATED
COMPLETED
FAILED
ABORTED
```

### Historical

```text
ARCHIVED
```

This grouping is analytical, not a universal state enum.

---

# 9. State Transition Principle

A transition must be:

```text
explicit
authorized
auditable
semantically valid
```

The system must not allow arbitrary transitions such as:

```text
DRAFT → ACTIVE
```

without satisfying the required intermediate governance conditions.

---

# 10. Transition as a First-Class Event

A lifecycle transition should conceptually contain:

```yaml
transition:
  object_ref: ...
  previous_state: ...
  next_state: ...
  actor_ref: ...
  authority_ref: ...
  reason: ...
  timestamp: ...
  evidence_refs: []
```

The exact schema is deferred.

The important architectural property is reconstructability.

---

# 11. State Transition Invariants

### Invariant 1

A transition must originate from the object's actual current state.

### Invariant 2

A transition must be permitted by the object's lifecycle contract.

### Invariant 3

A transition must not silently invalidate required downstream dependencies without propagation.

### Invariant 4

A revoked object must not silently return to active state.

### Invariant 5

A superseded object must not silently regain current authority.

### Invariant 6

An expired object must not be treated as current without explicit renewal/reissuance semantics.

### Invariant 7

A terminal object must not accept ordinary mutable transitions.

### Invariant 8

A state transition must preserve provenance.

---

# 12. Supersession

Supersession means:

```text
NEW OBJECT
    ↓
replaces
    ↓
OLD OBJECT
```

The old object may remain historically valid as an artifact while no longer being current.

Therefore:

```text
SUPERSEDED
≠
CORRUPTED
```

and:

```text
historically valid
≠
currently authoritative
```

---

# 13. Supersession Example

Consider:

```text
DECISION D1
```

followed by:

```text
DECISION D2
```

where D2 supersedes D1.

D1 may remain:

```text
intrinsically valid
```

but:

```text
current_decision = D2
```

Therefore an approval bound to D1 may no longer authorize execution based on D1.

---

# 14. Revocation

Revocation is an explicit withdrawal of current validity or authority.

Conceptually:

```text
ACTIVE
  ↓
REVOKED
```

Revocation should propagate to dependent objects where their validity depends on the revoked object.

---

# 15. Revocation Propagation

Example:

```text
Delegation D
    ↓
Agent Authority A
    ↓
Execution Intent E
```

If D is revoked:

```text
D = REVOKED
```

then A may become:

```text
INVALIDATED / INACTIVE
```

and E may become:

```text
NOT EXECUTABLE
```

The downstream objects do not necessarily need to be physically deleted.

They need to become semantically ineligible.

---

# 16. Expiration

Expiration is a time-driven invalidation.

```text
valid_until = T
current_time > T
```

implies:

```text
currently_valid = false
```

unless the object contract explicitly defines renewal semantics.

---

# 17. Renewal

Renewal should not automatically mutate the historical object.

Prefer:

```text
OLD AUTHORIZATION
      ↓
renewal
      ↓
NEW AUTHORIZATION
```

This preserves historical provenance.

Whether a renewal creates a new object or a new version depends on the relevant contract.

---

# 18. Invalidation

Invalidation means:

```text
an object that was previously acceptable
is no longer acceptable for its intended use.
```

Invalidation can result from:

```text
upstream change
revocation
expiration
supersession
policy change
constraint change
security change
evidence invalidation
decision change
scope change
```

---

# 19. Invalidation Is Not Deletion

An invalidated object should generally remain available for:

```text
audit
provenance
reconstruction
failure analysis
assurance
```

Therefore:

```text
INVALIDATED
≠
DELETED
```

---

# 20. Dependency Invalidation Graph

The architecture should represent dependency relationships explicitly:

```text
Evidence
   ↓
Knowledge
   ↓
Context
   ↓
Decision
   ↓
Approval
   ↓
Execution Intent
   ↓
Execution
   ↓
Outcome
   ↓
Evaluation
   ↓
Assurance
```

A change at an upstream node can affect downstream validity.

---

# 21. Invalidation Does Not Always Mean Destruction

If:

```text
Evidence E1
```

becomes invalid, it does not imply:

```text
Decision D1 = deleted
```

Instead:

```text
D1
status = DEPENDENCY_INVALIDATED
```

may be more appropriate.

The system can then decide:

```text
REVALIDATE
REPLAN
REVOKE
ESCALATE
ARCHIVE
```

depending on the object contract.

---

# 22. Dependency Severity

Not every upstream change has the same impact.

A dependency can be:

```text
CRITICAL
HIGH
MEDIUM
LOW
ADVISORY
```

These are analytical categories.

The actual severity vocabulary should be standardized in the relevant contracts.

---

# 23. Strong Dependency

A strong dependency means:

```text
if upstream validity fails,
downstream validity fails.
```

Example:

```text
approval
depends critically on
decision
```

If the approval is explicitly bound to a superseded decision, the approval should no longer authorize that decision.

---

# 24. Weak Dependency

A weak dependency means:

```text
upstream change may require reassessment
but does not automatically invalidate.
```

This is useful for:

```text
recommendations
context
non-critical evidence
optimization hints
```

The distinction prevents unnecessary global invalidation.

---

# 25. Dependency Policy

Each dependency should conceptually define:

```yaml
dependency:
  source_ref: ...
  target_ref: ...
  strength: ...
  invalidation_rule: ...
  revalidation_rule: ...
```

This provides a basis for deterministic propagation.

---

# 26. Relational Validity

The following combinations must be checked explicitly.

```text
Decision ↔ Evidence
Decision ↔ Goal
Decision ↔ Constraints
Decision ↔ Authority

Approval ↔ Decision
Approval ↔ Approver
Approval ↔ Scope
Approval ↔ Time

Delegation ↔ Delegator
Delegation ↔ Delegatee
Delegation ↔ Scope
Delegation ↔ Expiration

Execution Intent ↔ Decision
Execution Intent ↔ Authority
Execution Intent ↔ Security State
Execution Intent ↔ Policy

Evaluation ↔ Artifact
Evaluation ↔ Evaluation Contract
Assurance ↔ Evidence
Assurance ↔ Evaluation
```

---

# 27. The Invalid Pair Problem

The architecture must explicitly detect:

```text
VALID(A)
VALID(B)
BUT
INVALID(A,B)
```

Examples:

### Example A

```text
Decision D1 = valid
Approval A1 = valid

but A1 references D2
```

Result:

```text
A1 ↔ D1 = invalid
```

### Example B

```text
Delegation D = valid
Execution E = valid

but E occurs outside D's scope
```

Result:

```text
D ↔ E = invalid
```

### Example C

```text
Assurance A = valid
Artifact X = valid

but A evaluates an older version of X
```

Result:

```text
A ↔ X_current = invalid
```

---

# 28. Version Binding

References to mutable objects should preferably bind to:

```text
object_id
+
version_id
```

rather than:

```text
object_id only
```

This prevents an approval intended for version 1 from silently applying to version 2.

---

# 29. Content Binding

For high-integrity artifacts, version references may be insufficient.

The system may require:

```text
object_id
version_id
content_hash
```

This is a candidate integrity mechanism.

The exact use of hashes belongs to the security and artifact contracts.

---

# 30. Approval Binding

An approval should conceptually bind to:

```text
decision
decision version
scope
approver
authority
time
```

Therefore:

```text
approval(D1)
```

should not silently authorize:

```text
D2
```

when D2 materially changes the decision.

---

# 31. Material Change

Not every update invalidates all downstream objects.

The architecture therefore needs the concept:

```text
MATERIAL CHANGE
```

A material change is one that can alter the semantic assumptions on which a dependent object relies.

This concept must be explicitly defined before automated invalidation is implemented.

---

# 32. Change Classification

A change can be classified as:

```text
NON_MATERIAL
MATERIAL
GOVERNANCE_MATERIAL
SECURITY_MATERIAL
UNKNOWN
```

`UNKNOWN` should trigger reassessment for protected dependencies rather than optimistic continuation.

---

# 33. Revalidation

When a dependency changes but automatic invalidation is not justified:

```text
DEPENDENCY CHANGED
        ↓
REVALIDATE
        ↓
VALID / INVALID / ESCALATE
```

This allows the system to avoid both:

```text
unsafe continuation
```

and:

```text
unnecessary global invalidation
```

---

# 34. Revalidation vs Regeneration

These are distinct.

```text
REVALIDATE
```

asks:

```text
is the existing artifact still acceptable?
```

while:

```text
REGENERATE
```

asks:

```text
should a new artifact be produced?
```

Existing engineering already distinguishes correction, regeneration, rebase, and escalation strategies. fileciteturn16file2L164-L174

---

# 35. Rollback

Rollback is a transition from:

```text
CURRENT STATE
```

toward:

```text
PREVIOUS KNOWN STATE
```

Rollback must not be interpreted as erasing history.

The architecture should preserve:

```text
state_before
state_after
rollback_reason
actor
authority
timestamp
```

---

# 36. Rollback and Governance

A rollback can itself be a consequential action.

Therefore:

```text
ROLLBACK
```

requires the same governance analysis as other consequential actions where applicable.

A system must not allow rollback to bypass:

```text
security
authority
constraints
audit
```

---

# 37. Recovery

Recovery differs from rollback.

```text
ROLLBACK
=
return toward prior state
```

while:

```text
RECOVERY
=
restore safe operational capability
```

Recovery may involve:

```text
rebuild
reissue
revalidate
reconcile
repair
re-authorize
```

---

# 38. Terminal States

Terminal states require special treatment.

Examples:

```text
REVOKED
EXPIRED
SUPERSEDED
COMPLETED
FAILED
ABORTED
```

A terminal state should not automatically imply that all referenced objects are terminal.

Lifecycle semantics must remain object-specific.

---

# 39. Terminal State Re-entry

The system should not allow:

```text
REVOKED → ACTIVE
```

unless the object contract explicitly defines a controlled restoration mechanism.

Where restoration is allowed, it should preferably produce:

```text
NEW VERSION
```

or:

```text
NEW AUTHORIZATION
```

rather than silently rewriting history.

---

# 40. Impossible States

IV-005 must explicitly prevent combinations such as:

```text
REVOKED + ACTIVE
EXPIRED + CURRENTLY_AUTHORIZED
SUPERSEDED + CURRENT_PRIMARY
INVALIDATED + EXECUTION_ELIGIBLE
UNAUTHORIZED + EXECUTING
REJECTED + APPROVED
APPROVAL_FOR_D1 + EXECUTION_OF_D2
DELEGATION_REVOKED + ACTIVE_DELEGATE_SCOPE
SECURITY_BLOCKED + EXECUTING
```

The exact object-level state vocabulary may differ by contract.

---

# 41. Cross-Object Impossible States

Some impossible states only appear relationally.

Examples:

```text
Approval = ACTIVE
Decision = SUPERSEDED
Approval references Decision
```

or:

```text
ExecutionIntent = READY
Authorization = REVOKED
```

or:

```text
Evaluation = PASS
EvaluatedArtifact = obsolete version
```

These must be caught by relational validation.

---

# 42. State Compatibility Matrix

| Object A | Object B | Combination |
|---|---|---|
| Decision ACTIVE | Approval ACTIVE | Potentially valid |
| Decision SUPERSEDED | Approval bound to old decision | Invalid for current execution |
| Delegation ACTIVE | Execution within scope | Potentially valid |
| Delegation REVOKED | Execution requiring delegation | Invalid |
| Authorization EXPIRED | Execution pending | Requires reauthorization |
| Security BLOCKED | Execution intent READY | Not executable |
| Evaluation PASS | Current artifact | Potentially valid |
| Evaluation PASS | Superseded artifact | Not sufficient for current artifact |
| Policy ACTIVE | Exception ACTIVE | Valid only if exception is authorized and scoped |
| Exception REVOKED | Dependent execution | Invalid |

---

# 43. Lifecycle Propagation

When an object changes state, the runtime should determine:

```text
WHICH DEPENDENTS
ARE AFFECTED?
```

Then classify each dependent as:

```text
UNCHANGED
REVALIDATE
SUSPEND
INVALIDATE
REVOKE
REGENERATE
ESCALATE
```

This is preferable to a universal:

```text
invalidate_all_downstream
```

rule.

---

# 44. Local vs Global Propagation

Existing campaign engineering provides a useful precedent:

```text
single asset drift
→ local correction

multiple assets drift
→ global rebase
```

fileciteturn16file2L164-L174

The broader architecture should apply the same principle:

```text
LOCAL DEPENDENCY FAILURE
≠
GLOBAL SYSTEM FAILURE
```

unless the dependency graph demonstrates global impact.

---

# 45. Blast Radius

Every invalidation should ideally identify:

```text
source change
affected nodes
affected edges
affected governance
affected execution
```

Conceptually:

```yaml
blast_radius:
  source_ref: ...
  affected_objects: []
  affected_capabilities: []
  affected_authorizations: []
  affected_execution_intents: []
  severity: ...
```

---

# 46. Dependency Cycles

The dependency graph must be checked for cycles.

Potentially dangerous:

```text
A depends on B
B depends on C
C depends on A
```

Cycles can make invalidation and state propagation ambiguous.

The architecture should either:

```text
forbid cycles
```

or:

```text
define strongly connected component semantics
```

The preferred default is to forbid semantic dependency cycles unless explicitly justified.

---

# 47. State Machine Consistency

Each contract should define:

```text
states
transitions
transition guards
terminal states
recovery paths
invalidation semantics
```

A cross-contract checker should then test compatibility.

---

# 48. Transition Guard

A transition should conceptually be:

```text
ALLOW_TRANSITION(
    object,
    current_state,
    requested_state,
    actor,
    authority,
    context
)
```

The guard must evaluate:

```text
state validity
authority
policy
constraints
security
dependencies
```

where applicable.

---

# 49. State and Security

Security state must be treated as dynamic.

Therefore an execution intent that was valid at:

```text
T1
```

may become ineligible at:

```text
T2
```

because:

```text
security_state(T1)
≠
security_state(T2)
```

This reinforces the TOCTOU concern established in IV-004.

---

# 50. State and Approval

Approval is not timeless.

An approval can become invalid through:

```text
expiration
revocation
decision supersession
scope change
approver authority change
material context change
security change
```

The exact invalidation triggers must be specified by the approval contract.

---

# 51. State and Delegation

Delegation validity depends on:

```text
delegator authority
delegatee identity
delegated scope
time
revocation
policy
security
```

Therefore:

```text
delegation_valid
```

is not a static property.

---

# 52. State and Evidence

Evidence may transition through:

```text
CAPTURED
VALIDATED
SUPERSEDED
RETRACTED
INVALIDATED
ARCHIVED
```

These are candidate states.

A downstream decision may remain historically valid even if evidence is later invalidated, but its **current validity** may require reassessment.

This distinction is essential:

```text
HISTORICAL DECISION RECORD
≠
CURRENTLY TRUSTWORTHY DECISION
```

---

# 53. State and Evaluation

An evaluation result must be bound to the evaluated artifact/version.

Otherwise:

```text
PASS(X_v1)
```

could be incorrectly applied to:

```text
X_v2
```

This is an invalid relational state.

---

# 54. State and Assurance

Assurance should also be version-bound.

Conceptually:

```text
ASSURANCE(A, architecture_version, evidence_set_version)
```

must not automatically remain applicable after material architectural changes.

This does not mean every implementation change invalidates assurance; the assurance contract must define materiality.

---

# 55. State and Policy Changes

Policy changes can invalidate existing decisions or approvals.

However, automatic retroactive invalidation should not be assumed.

The system must distinguish:

```text
policy applies prospectively
```

from:

```text
policy applies to active obligations
```

This is a contract-level semantic decision.

---

# 56. State and Constraint Changes

Constraint changes can be more direct.

If a new binding constraint prohibits an action already scheduled for execution:

```text
execution eligibility
```

must be recomputed.

The action should not continue merely because it was previously approved.

---

# 57. State and Goal Changes

Goal changes can invalidate decisions without necessarily invalidating authority.

Example:

```text
Authority = ACTIVE
Decision = based on Goal G1
Current Goal = G2
```

The authority may remain valid while the decision becomes stale.

Therefore invalidation must propagate according to dependency semantics, not merely object type.

---

# 58. State and Context Changes

Context changes can have:

```text
no effect
```

or:

```text
material effect
```

depending on the decision's dependency model.

Therefore the system requires explicit dependency classification rather than assuming all context changes invalidate decisions.

---

# 59. Reconciliation

When independently valid states produce an inconsistent combined state, the system should enter:

```text
RECONCILIATION
```

rather than silently selecting one state.

Candidate reconciliation outcomes:

```text
REVALIDATE
REPLAN
REAUTHORIZE
REVOKE
SUSPEND
ESCALATE
ABORT
```

---

# 60. Concurrent Updates

Distributed components may update related objects concurrently.

Example:

```text
Human approval update
+
Policy update
+
Security state update
```

at approximately the same time.

The architecture therefore needs:

```text
versioning
ordering
conflict detection
atomicity boundaries
```

for governance-critical transitions.

Exact distributed consistency semantics remain deferred.

---

# 61. Race Condition Example

```text
T1: approval validated
T2: security state becomes blocked
T3: execution begins
```

The runtime must ensure that security enforcement at execution time prevents stale approval from authorizing execution.

---

# 62. Stale Object Detection

An object should be considered stale when:

```text
its assumptions no longer match
the current governing state.
```

Candidate metadata:

```yaml
freshness:
  evaluated_at: ...
  valid_until: ...
  dependency_versions: {}
  governance_snapshot_ref: ...
```

---

# 63. Freshness vs Validity

These are related but distinct.

```text
FRESH
```

means:

```text
recent/current enough for the defined purpose
```

while:

```text
VALID
```

means:

```text
satisfies the applicable contract.
```

A stale object may still be historically valid.

---

# 64. Historical Truth vs Current Truth

The architecture should preserve both.

```text
historical_truth
```

answers:

```text
what was valid then?
```

while:

```text
current_validity
```

answers:

```text
what is valid now?
```

This is essential for auditability.

---

# 65. Audit Requirement

Every material lifecycle transition should be reconstructable.

At minimum:

```text
who
what
when
from
to
why
under which authority
based on which evidence
```

The exact audit event schema is deferred.

---

# 66. Lifecycle Falsification Classes

The implementation must attempt to break lifecycle consistency through:

```text
stale approval
stale decision
revoked delegation
expired authority
superseded decision
invalidated evidence
changed security state
changed policy
changed constraint
material goal change
concurrent updates
duplicate transitions
out-of-order transitions
illegal state jumps
terminal-state mutation
rollback abuse
recovery without authorization
orphaned dependent object
cyclic dependency
version mismatch
content mismatch
```

---

# 67. Test Matrix

| Test | Scenario | Required result |
|---|---|---|
| LIFE-001 | D1 superseded after A1 approval | A1 cannot authorize D2 |
| LIFE-002 | Delegation revoked before execution | Execution blocked |
| LIFE-003 | Approval expires before execution | Reauthorization required |
| LIFE-004 | Security changes to BLOCKED | Execution denied |
| LIFE-005 | Constraint changes to prohibited | Revalidation required |
| LIFE-006 | Evidence invalidated | Dependent decision reassessed |
| LIFE-007 | Evaluation bound to v1, artifact is v2 | Evaluation not sufficient |
| LIFE-008 | Illegal DRAFT → ACTIVE transition | Reject |
| LIFE-009 | Revoked → ACTIVE without restoration path | Reject |
| LIFE-010 | Local dependency failure | Local response preferred |
| LIFE-011 | Global dependency failure | Global response / rebase / escalation |
| LIFE-012 | Concurrent approval + revocation | Deterministic final state |
| LIFE-013 | Duplicate transition | Idempotent or rejected |
| LIFE-014 | Out-of-order transition | Reject |
| LIFE-015 | Dependency cycle | Detect / reject |
| LIFE-016 | Rollback without authority | Reject |
| LIFE-017 | Recovery without authorization | Reject |
| LIFE-018 | Historical valid object used as current authority | Reject |
| LIFE-019 | Assurance for obsolete architecture version | Reassessment |
| LIFE-020 | Valid objects form invalid combination | Relational validation failure |

---

# 68. Candidate System-Level Invariants

### Invariant 1

Object validity does not imply relational validity.

### Invariant 2

Historical validity does not imply current validity.

### Invariant 3

A superseded object must not silently regain current authority.

### Invariant 4

A revoked authority must not remain executable.

### Invariant 5

An expired authorization must not silently authorize new execution.

### Invariant 6

Material upstream changes must trigger the contractually required downstream response.

### Invariant 7

Invalidation must not require deletion.

### Invariant 8

Execution eligibility must be derived from current governance state rather than historical approval alone.

### Invariant 9

Lifecycle transitions must be authorized and auditable.

### Invariant 10

Illegal state transitions must be rejected.

### Invariant 11

Cross-object incompatibilities must be detectable even when each object is individually valid.

### Invariant 12

Version-bound approvals and evaluations must not silently apply to different object versions.

### Invariant 13

Local dependency failures must not automatically produce global invalidation unless the dependency graph establishes global impact.

### Invariant 14

Recovery and rollback are governed actions.

### Invariant 15

Lifecycle history must remain reconstructable.

### Invariant 16

Unknown dependency impact must not be treated as harmless for consequential execution.

### Invariant 17

Dependency cycles must not produce ambiguous invalidation semantics.

### Invariant 18

Security-state changes must be capable of invalidating previously eligible execution.

---

# 69. Architectural Conclusion

IV-005 establishes a deeper principle:

```text
THE UNIT OF VALIDITY
IS NOT ALWAYS THE OBJECT.
```

For consequential intelligence systems, validity is often relational:

```text
VALID(
    object,
    referenced_objects,
    versions,
    time,
    governance_state
)
```

Therefore the architecture should not ask only:

```text
"Is this approval valid?"
```

It should ask:

```text
"Is this approval valid
for this decision,
for this version,
for this actor,
under this authority,
at this time,
under this security state,
under these constraints?"
```

Likewise:

```text
"Did the evaluator PASS?"
```

is insufficient.

The system must establish:

```text
PASS
+
correct artifact version
+
correct evaluation contract
+
current applicability
```

before using the result as assurance evidence.

---

# 70. Relationship to IV-003 and IV-004

The three documents now form a coherent validation sequence:

```text
IV-003
DEPENDENCY
"What becomes invalid when upstream state changes?"

        ↓

IV-004
PRECEDENCE
"Which governance layer controls when rules conflict?"

        ↓

IV-005
STATE CONSISTENCY
"Are the resulting object and cross-object states actually valid?"
```

Together:

```text
DEPENDENCY
+
PRECEDENCE
+
STATE CONSISTENCY
```

form the foundation for the next stage of runtime verification.

---

# 71. Exit Criteria

- [x] Intrinsic validity defined
- [x] Relational validity defined
- [x] Temporal validity defined
- [x] Governance validity defined
- [x] Object validity separated from execution eligibility
- [x] Candidate lifecycle states defined
- [x] Transition semantics defined
- [x] Supersession analyzed
- [x] Revocation analyzed
- [x] Expiration analyzed
- [x] Renewal analyzed
- [x] Invalidation analyzed
- [x] Dependency propagation analyzed
- [x] Strong and weak dependencies distinguished
- [x] Version binding analyzed
- [x] Content binding analyzed
- [x] Material change introduced
- [x] Revalidation distinguished from regeneration
- [x] Rollback distinguished from recovery
- [x] Terminal-state semantics analyzed
- [x] Impossible states identified
- [x] Relational invalid-state examples defined
- [x] Local vs global propagation analyzed
- [x] Blast radius introduced
- [x] Dependency cycles identified
- [x] State-machine consistency defined
- [x] Concurrent transition risks identified
- [x] TOCTOU implications incorporated
- [x] Historical vs current validity distinguished
- [x] Lifecycle audit requirements defined
- [x] Falsification classes defined
- [x] Test matrix defined
- [x] Candidate system-level invariants defined

**Current assessment:** The architecture now has a defensible conceptual basis for distinguishing object validity, relational validity, temporal validity, and current execution eligibility. The most important remaining specification gap is the exact cross-contract lifecycle/state vocabulary and the machine-readable dependency propagation semantics.

---

# 72. Next Document

**IV-006 — Evidence, Verification, Self-Critique & Adversarial Self-Verification Architecture**

This should directly address the concern previously raised about proving the designed intelligence architecture.

It will formalize:

```text
CLAIM
 ↓
EVIDENCE
 ↓
VERIFICATION
 ↓
SELF-CRITIQUE
 ↓
ADVERSARIAL SELF-VERIFICATION
 ↓
INDEPENDENT CHECK
 ↓
ASSURANCE
```

with explicit separation between:

```text
THE SYSTEM PRODUCED A RESULT
```

and:

```text
THE SYSTEM HAS EVIDENCE THAT THE RESULT
AND THE MECHANISM PRODUCING IT
SHOULD BE TRUSTED.
```

The document must also address the critical limitation:

```text
A MODEL CANNOT PROVE ITS OWN CORRECTNESS
MERELY BY CRITIQUING ITSELF.
```

Therefore self-critique and adversarial self-verification should be treated as **verification mechanisms with measurable failure modes**, not as automatic proof of alignment or correctness.
