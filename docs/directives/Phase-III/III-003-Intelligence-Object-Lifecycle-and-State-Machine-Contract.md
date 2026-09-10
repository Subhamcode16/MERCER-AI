# III-003 — Intelligence Object Lifecycle & State Machine Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** II-001 through II-017, II-RAT-001 through II-RAT-003, III-001, III-002  
**Purpose:** Compile the ratified Intelligence Object lifecycle semantics into an explicit machine-readable state machine with governed transitions, preconditions, postconditions, invalid-transition handling, locking, invalidation, supersession, archival, restoration, recovery, and provenance.

---

# 1. Purpose

III-003 translates the frozen lifecycle semantics into an executable state-machine contract.

The central boundary is:

```text
OBJECT STATE
    ≠
AUTHORITY
    ≠
RUNTIME STATE
```

The lifecycle system answers:

```text
WHAT STATE IS THIS OBJECT IN?
WHAT TRANSITIONS ARE LEGAL?
WHAT CONDITIONS MUST HOLD?
WHAT AUTHORITY IS REQUIRED?
WHAT MUST BE RECORDED?
```

It does not independently answer:

```text
WHO IS AUTHORIZED?
```

That remains the responsibility of III-002.

---

# 2. Lifecycle as a State Machine

Every governed Intelligence Object participates in a lifecycle state machine.

Conceptually:

```text
DRAFT
  ↓
VALIDATING
  ↓
VALID
  ↓
APPROVED
  ↓
LOCKED
```

with controlled branches such as:

```text
INVALIDATED
SUPERSEDED
ARCHIVED
RETIRED
RESTORED
```

The exact transition graph must be derived from the ratified lifecycle semantics and must not be expanded merely for implementation convenience.

---

# 3. Lifecycle State Identity

Every lifecycle state must have a canonical identifier.

Recommended conceptual form:

```text
LCS-<NAME>
```

Examples:

```text
LCS-DRAFT
LCS-VALIDATING
LCS-VALID
LCS-APPROVED
LCS-LOCKED
```

The identifier should be stable and non-ambiguous.

---

# 4. State Semantics

A lifecycle state describes the semantic status of an object.

It must not be used to represent:

```text
process execution
agent availability
runtime queue position
worker health
network state
```

Those belong to runtime state.

---

# 5. Canonical Lifecycle States

The architecture recognizes the following conceptual states:

```text
DRAFT
VALIDATING
VALID
APPROVED
LOCKED
INVALIDATED
SUPERSEDED
ARCHIVED
RETIRED
```

A restoration path may return an eligible historical object to an explicitly permitted active state.

The implementation must not invent additional semantic states without an explicit change proposal.

---

# 6. DRAFT

`DRAFT` represents an object that is still being constructed or prepared.

Typical properties:

```text
not yet fully validated
may still undergo controlled revision
not automatically eligible for consequential consumption
```

DRAFT does not mean:

```text
incorrect
untrusted
unauthorized
```

It means the lifecycle has not yet established the conditions required for a more mature state.

---

# 7. VALIDATING

`VALIDATING` indicates that the object is undergoing a defined validation process.

It does not mean:

```text
VALID
```

and does not mean:

```text
APPROVED
```

A validation process may result in:

```text
VALID
INVALIDATED
ESCALATED
```

according to the applicable evaluation contract.

---

# 8. VALID

`VALID` indicates that the object has satisfied the applicable validation requirements.

It does not automatically imply:

```text
approved for every use
authorized for every agent
locked
universally correct
```

Validity remains contextual to the applicable contract.

---

# 9. APPROVED

`APPROVED` indicates that the object has received the required approval decision under the applicable authority contract.

Therefore:

```text
VALID
+
REQUIRED AUTHORITY
+
APPROVAL DECISION
=
APPROVED
```

Approval must never be inferred solely from:

```text
model confidence
validation score
successful execution
```

---

# 10. LOCKED

`LOCKED` represents a lifecycle state in which mutation is restricted or prohibited according to the applicable contract.

A locked object should be treated as immutable for ordinary operations.

Unlocking must not be implemented as an arbitrary boolean toggle.

Any permitted transition out of LOCKED must itself be governed and recorded.

---

# 11. INVALIDATED

`INVALIDATED` indicates that an object previously considered usable or valid can no longer be treated as valid under the applicable contract.

Invalidation may result from:

```text
contradictory evidence
failed validation
authority failure
constraint violation
superseding information
adversarial discovery
runtime integrity failure
```

The exact cause must be recorded.

---

# 12. SUPERSEDED

`SUPERSEDED` indicates that another object version or object has replaced the object for the applicable purpose.

Supersession preserves historical traceability.

The system must retain:

```text
superseded_object
superseding_object
reason
timestamp
authority / process
provenance
```

---

# 13. ARCHIVED

`ARCHIVED` indicates that an object is retained for historical, audit, provenance, reconstruction, or research purposes but is not automatically eligible for active decision-making.

Archive status must not imply deletion.

---

# 14. RETIRED

`RETIRED` indicates that the object is no longer intended for active operational use.

Historical records remain traceable according to the persistence and provenance contracts.

---

# 15. Restoration

Restoration is not a generic:

```text
UNARCHIVE = ACTIVE
```

operation.

Restoration must resolve:

```text
object version
reason
authority
current evidence
current constraints
current dependencies
target state
```

A historical object may require revalidation before returning to an active state.

---

# 16. State Transition Record

Every consequential lifecycle transition should produce a structured record.

Conceptually:

```yaml
transition:
  transition_id: LCT-...
  object_id: IO-...
  object_version: ...
  from_state: ...
  to_state: ...
  requested_by: ...
  authorized_by: ...
  reason: ...
  preconditions: []
  postconditions: []
  timestamp: ...
  provenance_ref: ...
```

---

# 17. Transition Identity

Every lifecycle transition should receive a unique identifier:

```text
LCT-<ULID>
```

The transition identifier is immutable.

---

# 18. Transition Authority

A state transition requires applicable authority.

The lifecycle engine must query the authority contract rather than embed independent authority semantics.

Conceptually:

```text
TRANSITION REQUEST
        ↓
III-002 AUTHORITY CHECK
        ↓
III-003 STATE CHECK
        ↓
TRANSITION
```

---

# 19. Preconditions

Every defined transition should specify preconditions.

Examples:

```text
object exists
current state matches expected state
required evidence exists
required validation completed
authority is valid
dependencies are satisfied
object version is current
```

A failed precondition must prevent the transition.

---

# 20. Postconditions

Every transition should define expected postconditions.

Examples:

```text
state updated
transition recorded
provenance updated
audit event emitted
new state consumability recalculated
dependent runtime tasks notified where required
```

---

# 21. Atomicity

A lifecycle transition should be atomic from the perspective of consumers.

The system must not expose a state where:

```text
state says APPROVED
```

but:

```text
approval record missing
provenance missing
required authority record missing
```

If a transition cannot be completed consistently, it must fail or enter an explicitly defined recovery condition.

---

# 22. Idempotency

Repeated submission of the same transition request should not create uncontrolled duplicate transitions.

The implementation should support:

```text
transition_id
request_id
idempotency key
```

where appropriate.

Exact mechanism remains an implementation decision.

---

# 23. Valid Transition Graph

The canonical graph should be encoded explicitly.

Conceptually:

```text
DRAFT
  │
  ├──→ VALIDATING
  │
  └──→ INVALIDATED

VALIDATING
  │
  ├──→ VALID
  ├──→ INVALIDATED
  └──→ ESCALATION / controlled recovery

VALID
  │
  ├──→ APPROVED
  ├──→ INVALIDATED
  └──→ SUPERSEDED

APPROVED
  │
  ├──→ LOCKED
  ├──→ INVALIDATED
  └──→ SUPERSEDED

LOCKED
  │
  ├──→ INVALIDATED
  ├──→ SUPERSEDED
  └──→ explicitly authorized restoration path

INVALIDATED
  │
  ├──→ SUPERSEDED
  └──→ explicitly authorized restoration / revalidation path

SUPERSEDED
  │
  └──→ ARCHIVED

ARCHIVED
  │
  └──→ explicitly authorized restoration path

RETIRED
  └──→ terminal unless explicit architecture change permits restoration
```

The diagram is a conceptual compilation target. The final machine-readable transition matrix is authoritative.

---

# 24. Invalid Transitions

The lifecycle engine must reject transitions not present in the canonical transition matrix.

Examples:

```text
DRAFT → LOCKED
DRAFT → APPROVED
ARCHIVED → APPROVED
INVALIDATED → LOCKED
RETIRED → APPROVED
```

unless an explicit contract defines the transition.

---

# 25. No Implicit State Promotion

The system must not infer:

```text
successful generation
→ VALID
```

or:

```text
VALID
→ APPROVED
```

or:

```text
APPROVED
→ LOCKED
```

without their respective conditions and authority.

---

# 26. Evaluation vs Lifecycle Transition

An evaluator may produce:

```text
PASS
```

but the lifecycle engine must still determine whether that result is sufficient for a transition.

Therefore:

```text
EVALUATION RESULT
        ↓
TRANSITION PRECONDITIONS
        ↓
AUTHORITY CHECK
        ↓
LIFECYCLE TRANSITION
```

This prevents evaluator output from becoming hidden lifecycle authority.

---

# 27. Invalidation

Invalidation should be explicit and reasoned.

Conceptually:

```yaml
invalidation:
  invalidation_id: ...
  object_id: ...
  reason_code: ...
  evidence_refs: []
  detected_by: ...
  authorized_by: ...
  timestamp: ...
```

An invalidation event must preserve the evidence that caused it where available.

---

# 28. Invalidating Evidence

Potential invalidating evidence includes:

```text
contradictory authoritative evidence
critical constraint violation
provenance failure
authority revocation
adversarially demonstrated failure
schema incompatibility
runtime integrity violation
```

The implementation must not treat every low-confidence signal as automatic invalidation.

The exact severity policy remains domain-dependent.

---

# 29. Supersession

Supersession must be explicit.

Conceptually:

```text
OBJECT A
   ↓
SUPERSEDED BY
   ↓
OBJECT B
```

The relationship must preserve:

```text
A version
B version
reason
authority
timestamp
```

---

# 30. Version and Lifecycle Interaction

A new object version does not automatically imply:

```text
APPROVED
```

A new version normally re-enters the lifecycle at a state determined by the semantic contract.

For example:

```text
APPROVED v1
   ↓
revision
   ↓
DRAFT v2
```

rather than:

```text
APPROVED v2
```

without revalidation.

---

# 31. Locking and Versioning

A locked version should remain immutable.

A new revision should normally be represented as:

```text
new version
```

with its own lifecycle state.

The implementation must not modify the locked version in place.

---

# 32. Lifecycle and Authority Separation

The lifecycle engine determines:

```text
is this transition structurally valid?
```

The authority system determines:

```text
is this actor permitted to request / perform it?
```

Neither engine should silently duplicate the other's semantics.

---

# 33. Lifecycle and Runtime Separation

Runtime state may indicate:

```text
RUNNING
```

while the object remains:

```text
APPROVED
```

Likewise:

```text
runtime FAILED
```

does not automatically mean:

```text
object INVALIDATED
```

unless the applicable semantic rule explicitly defines that consequence.

---

# 34. Runtime Event vs Lifecycle Transition

An execution event such as:

```text
TASK_COMPLETED
```

is not itself a lifecycle transition.

It may provide evidence that enables a transition.

Therefore:

```text
RUNTIME EVENT
→ EVIDENCE
→ TRANSITION EVALUATION
→ LIFECYCLE CHANGE
```

where applicable.

---

# 35. Dependency Interaction

Before a transition that requires dependencies, the lifecycle engine must resolve:

```text
dependency identity
dependency version
dependency lifecycle state
dependency validity
dependency authority constraints
```

A dependency merely existing does not make it valid.

---

# 36. Stale Dependency Protection

A transition must not silently consume a stale dependency when a current version is required.

Example:

```text
Object A v1
Object B expects A v2
```

must not resolve to:

```text
A v1
```

without an explicit compatibility rule.

---

# 37. State Transition Concurrency

Concurrent transition requests must be serialized or otherwise conflict-controlled.

Example:

```text
Request A: VALID → APPROVED
Request B: VALID → INVALIDATED
```

The implementation must not produce an impossible merged state.

The winning transition and rejected transition must remain auditable.

---

# 38. Optimistic Concurrency

A version or revision token may be used to prevent stale writes.

Conceptually:

```text
READ v3
 ↓
REQUEST TRANSITION based on v3
 ↓
CURRENT = v4
 ↓
REJECT STALE TRANSITION
```

The exact mechanism remains an implementation decision.

---

# 39. State Machine Determinism

For the same:

```text
object state
+
transition request
+
authority context
+
preconditions
+
relevant evidence
```

the lifecycle engine should produce a deterministic transition decision.

Where external adjudication is required, the decision must explicitly record that dependency.

---

# 40. Recovery

Lifecycle recovery must not silently restore a previous state.

A recovery action must specify:

```text
failure
reason
target object
recovery strategy
authority
target state
postconditions
```

Recovery may require:

```text
revalidation
re-authorization
reconstruction
```

---

# 41. Recovery and Strategic Drift

Recovery must not change the object's intended strategic purpose merely because the previous implementation failed.

If recovery changes semantics:

```text
NEW DECISION / NEW VERSION
```

must be created.

---

# 42. Terminal States

The implementation must define terminal behavior explicitly.

Potential terminal or effectively terminal states include:

```text
RETIRED
```

and potentially:

```text
ARCHIVED
```

depending on restoration policy.

No state should become terminal merely because no outgoing transition was implemented.

---

# 43. State Transition Provenance

Every consequential transition must preserve:

```text
who requested it
who authorized it
why it occurred
what evidence supported it
what object version was involved
when it occurred
what previous state existed
what new state resulted
```

---

# 44. Audit Reconstruction

Given an object, the system should be able to reconstruct:

```text
CURRENT STATE
        ↓
PREVIOUS STATE
        ↓
TRANSITIONS
        ↓
AUTHORITY
        ↓
EVIDENCE
        ↓
PROVENANCE
```

Historical state must not depend solely on current mutable fields.

---

# 45. Lifecycle Falsification

The lifecycle implementation must be attacked with:

```text
unauthorized transition
invalid transition
stale transition
concurrent transition
duplicate transition
state spoofing
approval without validation
lock bypass
invalidated-object consumption
supersession bypass
archive bypass
retirement bypass
recovery escalation
```

---

# 46. Lifecycle Invariants

### Invariant 1

Every governed object has an explicit lifecycle state.

### Invariant 2

Lifecycle state is distinct from authority.

### Invariant 3

Lifecycle state is distinct from runtime state.

### Invariant 4

Only defined transitions are permitted.

### Invariant 5

Every consequential transition requires applicable authority.

### Invariant 6

Transition preconditions must be satisfied.

### Invariant 7

Transition postconditions must be satisfied.

### Invariant 8

Invalid transitions are rejected or explicitly escalated.

### Invariant 9

Evaluation results do not automatically perform lifecycle transitions.

### Invariant 10

Successful execution does not automatically establish semantic validity.

### Invariant 11

Invalidation is explicit and reasoned.

### Invariant 12

Supersession preserves historical lineage.

### Invariant 13

Locked objects are not mutated in place.

### Invariant 14

New semantic revisions receive explicit version treatment.

### Invariant 15

Stale transition requests cannot silently overwrite current state.

### Invariant 16

Concurrent state changes remain auditable.

### Invariant 17

Recovery is governed.

### Invariant 18

Recovery cannot silently introduce strategic drift.

### Invariant 19

Runtime failure does not automatically imply semantic invalidation without an explicit rule.

### Invariant 20

Historical state remains reconstructable.

### Invariant 21

Implementation must not invent lifecycle semantics.

---

# 47. Machine-Readable State Concept

Conceptually:

```yaml
lifecycle_state:
  state_id: LCS-APPROVED
  name: APPROVED
  terminal: false

  permitted_transitions:
    - LOCKED
    - INVALIDATED
    - SUPERSEDED

  consumption_policy:
    active: true

  mutation_policy:
    mutable: false
```

This is conceptual and must be compiled into the final schema.

---

# 48. Machine-Readable Transition Concept

```yaml
transition:
  transition_id: LCT-...
  from_state: VALID
  to_state: APPROVED

  required_authority:
    decision_type: APPROVE

  preconditions:
    - validation_complete
    - required_evidence_present
    - dependencies_satisfied

  postconditions:
    - approval_record_exists
    - provenance_record_exists

  failure_policy:
    mode: DENY_OR_ESCALATE
```

---

# 49. State Registry

Phase III should establish:

```text
STATE
→ STATE ID
→ DESCRIPTION
→ PERMITTED TRANSITIONS
→ CONSUMPTION POLICY
→ MUTATION POLICY
→ REQUIRED AUTHORITY
→ PRECONDITIONS
→ POSTCONDITIONS
```

This becomes the canonical lifecycle registry.

---

# 50. Transition Registry

Likewise:

```text
TRANSITION
→ SOURCE STATE
→ TARGET STATE
→ AUTHORITY REQUIREMENT
→ PRECONDITIONS
→ POSTCONDITIONS
→ FAILURE POLICY
→ PROVENANCE REQUIREMENT
```

The runtime must consume this registry rather than embedding transition logic across unrelated code paths.

---

# 51. Single Source of Lifecycle Truth

Lifecycle transition definitions must have one canonical source.

Avoid:

```text
API transition rules
+
database transition rules
+
agent transition rules
+
runtime transition rules
```

that can diverge.

Prefer:

```text
CANONICAL LIFECYCLE CONTRACT
        ↓
VALIDATED RUNTIME ENFORCEMENT
```

---

# 52. API Boundary

An API request such as:

```text
POST /approve
```

must not directly mutate lifecycle state.

The request must enter the lifecycle contract:

```text
REQUEST
 ↓
AUTHORITY
 ↓
PRECONDITIONS
 ↓
STATE MACHINE
 ↓
TRANSITION RECORD
 ↓
COMMIT
```

---

# 53. Agent Boundary

Agents must request lifecycle transitions through the same contract.

An agent must not bypass the lifecycle engine by directly writing:

```text
lifecycle_state = APPROVED
```

---

# 54. Database Boundary

Persistence must not become an alternative state machine.

Database constraints may enforce:

```text
integrity
uniqueness
referential consistency
```

but semantic transitions remain governed by the lifecycle contract.

---

# 55. Event Boundary

Lifecycle events should be emitted after a successful transition.

Example:

```text
VALID → APPROVED
        ↓
LIFECYCLE_TRANSITION_COMMITTED
        ↓
EVENT
```

Events must not be interpreted as transitions unless the event contract explicitly defines that behavior.

---

# 56. Observability

The lifecycle engine should expose metrics such as:

```text
transition_attempts
transition_success
transition_denials
transition_escalations
stale_transition_rejections
concurrent_conflicts
invalid_transition_attempts
recovery_attempts
invalidation_events
supersession_events
```

Metrics are operational evidence, not semantic truth.

---

# 57. Required Tests

The reference implementation must test:

```text
valid transitions
invalid transitions
missing authority
wrong authority scope
wrong decision type
missing evidence
failed precondition
failed postcondition
stale transition
concurrent transition
duplicate transition
lock bypass
invalidation
supersession
archival
restoration
retirement
recovery
runtime-state confusion
```

---

# 58. Required Falsification Cases

Deliberately attempt:

```text
write APPROVED directly
approve without validation
approve with expired authority
approve with wrong scope
unlock without authority
mutate LOCKED object
consume INVALIDATED object
consume SUPERSEDED version
restore ARCHIVED object without revalidation
reuse stale transition request
race APPROVE vs INVALIDATE
```

---

# 59. Deferred Decisions

III-003 intentionally does not freeze:

- exact persistence technology;
- exact state-machine library;
- exact concurrency mechanism;
- exact event-bus technology;
- final restoration policy for every state;
- exact terminal-state semantics where domain-specific;
- retry strategy;
- database transaction implementation;
- exact transition API;
- final lifecycle registry syntax.

These remain engineering decisions unless they alter semantic meaning.

---

# 60. Exit Criteria

- [x] Lifecycle state machine defined
- [x] Canonical states defined
- [x] State semantics defined
- [x] Transition identity defined
- [x] Transition authority boundary defined
- [x] Preconditions defined
- [x] Postconditions defined
- [x] Atomicity defined
- [x] Idempotency boundary defined
- [x] Invalid transitions defined
- [x] Evaluation/lifecycle separation defined
- [x] Invalidation defined
- [x] Supersession defined
- [x] Locking defined
- [x] Archival defined
- [x] Restoration defined
- [x] Retirement defined
- [x] Version interaction defined
- [x] Runtime-state separation defined
- [x] Stale dependency protection defined
- [x] Concurrency boundary defined
- [x] Recovery defined
- [x] Strategic-drift protection defined
- [x] Provenance requirements defined
- [x] Falsification cases defined
- [x] Lifecycle invariants defined
- [x] Required tests defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 61. Next Contract

**III-004 — Provenance, Lineage & Evidence Trace Contract**

III-004 will compile the provenance semantics into a machine-readable contract covering:

```text
source identity
object lineage
transformation lineage
decision lineage
execution lineage
evidence lineage
evaluation lineage
critique lineage
attack lineage
authority lineage
version reconstruction
audit reconstruction
tamper detection
```

The central requirement remains:

```text
IF A CONSEQUENTIAL DECISION OCCURRED,
THE SYSTEM MUST BE ABLE TO RECONSTRUCT
HOW IT CAME TO EXIST.
```
