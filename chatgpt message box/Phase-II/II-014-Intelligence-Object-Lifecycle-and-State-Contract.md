# II-014 — Intelligence Object Lifecycle & State Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Depends On:** II-001 through II-013  
**Scope:** Lifecycle, state transitions, validity, locking, invalidation, revision, archival, retirement, and dependency behavior of intelligence-layer objects

---

## 1. Purpose

II-014 defines the lifecycle of the major semantic objects that exist within the Campaign Intelligence Layer.

The system contains objects such as:

```text
KNOWLEDGE
CLAIM
AUTHORITY
INTENT
EVIDENCE REQUIREMENT
ASSET STRATEGY
NARRATIVE NODE
CHANNEL PROJECTION
ASSET SPECIFICATION
EVALUATION
FAILURE
RECOVERY PLAN
DECISION
```

These objects cannot be treated as static records.

They evolve through controlled states.

The lifecycle contract answers:

> **When is an intelligence object created, when can it be trusted, when is it valid for downstream consumption, when must it be locked, when does it become stale or invalid, how can it be revised, and when should it be archived or retired?**

---

# 2. Core Principle

> **An intelligence object is not defined only by its content; its lifecycle state determines whether and how that object may participate in downstream decisions.**

Therefore:

```text
OBJECT CONTENT
+
OBJECT STATE
+
AUTHORITY
+
VERSION
+
PROVENANCE
=
USABLE INTELLIGENCE OBJECT
```

A valid-looking object in the wrong lifecycle state must not automatically be consumed.

---

# 3. Canonical Object Lifecycle

The generalized lifecycle is:

```text
CREATED
   ↓
DRAFT
   ↓
VALIDATING
   ↓
VALID
   ↓
APPROVED
   ↓
LOCKED
   ↓
CONSUMED
   ↓
[REVISED / INVALIDATED / SUPERSEDED]
   ↓
ARCHIVED
   ↓
RETIRED
```

Not every object must pass through every state.

The allowed lifecycle depends on object type and authority.

---

# 4. Lifecycle State Definitions

## 4.1 CREATED

The object has been instantiated but has not yet completed basic structural validation.

```text
CREATED
```

does not imply semantic validity.

---

## 4.2 DRAFT

The object is actively being developed.

A draft may be:

```text
incomplete
uncertain
under discussion
```

Draft objects should not normally serve as authoritative downstream inputs.

---

## 4.3 VALIDATING

The object is undergoing required validation.

Examples:

```text
claim validation
authority validation
constraint validation
evidence validation
schema validation
```

---

## 4.4 VALID

The object satisfies the minimum semantic requirements for its type.

Validity does not necessarily imply approval.

```text
VALID
≠
APPROVED
```

---

## 4.5 APPROVED

An authorized decision-maker or governance mechanism has accepted the object for use within a defined scope.

Approval must preserve:

```text
authority
timestamp
scope
version
```

---

## 4.6 LOCKED

A locked object cannot be silently mutated.

Locks may exist because:

```text
campaign decision is finalized
user approved it
downstream dependencies rely on it
hard invariant depends on it
production execution has begun
```

Unlocking requires explicit authority.

---

## 4.7 CONSUMED

An object has been used by one or more downstream processes.

Consumption does not invalidate the object.

It creates additional lineage:

```text
OBJECT
 ↓
CONSUMED BY
 ↓
DOWNSTREAM OBJECT
```

---

## 4.8 SUPERSEDED

A newer valid version replaces the object for future use.

The old version remains historically auditable.

```text
v1
 ↓ superseded by
v2
```

---

## 4.9 INVALIDATED

The object is no longer valid for its intended scope.

Reasons may include:

```text
source invalidation
authority change
knowledge correction
constraint change
upstream dependency failure
evaluation failure
policy change
product change
```

Invalidated objects must not silently continue as authoritative inputs.

---

## 4.10 ARCHIVED

The object is retained for historical and audit purposes but is no longer active.

---

## 4.11 RETIRED

The object is permanently removed from active semantic participation while remaining subject to applicable retention and audit policies.

Implementation-specific deletion semantics remain deferred.

---

# 5. State Is Not Authority

An object can be:

```text
APPROVED
```

without being universally authoritative.

Likewise:

```text
LOCKED
```

does not mean:

```text
TRUE IN ALL CONTEXTS
```

State and authority remain separate dimensions.

---

# 6. State Is Not Confidence

An object may have:

```text
HIGH CONFIDENCE
```

while remaining:

```text
DRAFT
```

or:

```text
UNVALIDATED
```

Confidence cannot bypass lifecycle requirements.

---

# 7. State Is Not Truth

A system should never interpret:

```text
APPROVED
```

as:

```text
OBJECTIVE TRUTH
```

Approval means:

> Authorized for use within the defined scope.

---

# 8. Object-Type Lifecycle Profiles

Different objects may require different state transitions.

Example:

### Knowledge Claim

```text
CREATED
→ VALIDATING
→ VALID
→ APPROVED
→ SUPERSEDED / INVALIDATED
→ ARCHIVED
```

### Campaign Intent

```text
CREATED
→ DRAFT
→ VALIDATING
→ APPROVED
→ LOCKED
→ REVISED / SUPERSEDED
→ ARCHIVED
```

### Generated Asset

```text
CREATED
→ GENERATED
→ EVALUATING
→ ACCEPTED / REJECTED
→ SELECTED
→ ARCHIVED
```

The final object-specific state machine must be defined per object type.

---

# 9. Lifecycle Transition

A state transition must have:

```text
object_id
from_state
to_state
trigger
authority
actor
timestamp
reason
evidence
version
```

No consequential state transition should exist without a traceable trigger.

---

# 10. Valid State Transitions

The architecture should define allowed transitions rather than permitting arbitrary state mutation.

Conceptually:

```text
DRAFT
 ├── VALIDATING
 └── ABANDONED

VALIDATING
 ├── VALID
 ├── INVALIDATED
 └── REQUIRES_REVIEW

VALID
 ├── APPROVED
 ├── REVISED
 └── INVALIDATED

APPROVED
 ├── LOCKED
 ├── REVISED
 └── INVALIDATED

LOCKED
 ├── CONSUMED
 ├── UNLOCKED → REVISED
 └── SUPERSEDED
```

Exact transition matrices remain object-specific.

---

# 11. Invalid Transitions

The system must reject transitions such as:

```text
RETIRED → ACTIVE
```

without an explicit restoration policy.

Likewise:

```text
LOCKED → MUTATED
```

must not occur silently.

---

# 12. State Transition Authority

Different transitions may require different authority.

Example:

```text
Draft → Valid
→ validation mechanism

Valid → Approved
→ approval authority

Approved → Locked
→ governance / campaign authority

Locked → Unlocked
→ explicit unlock authority

Valid → Invalidated
→ authorized invalidation mechanism
```

Authority must be scoped.

---

# 13. Lifecycle Guards

Before allowing a transition, the system should verify:

```text
authority
required evidence
required dependencies
current version
current state
lock status
conflicts
validation requirements
```

Conceptually:

```text
TRANSITION REQUEST
       ↓
LIFECYCLE GUARDS
       ↓
ALLOW / REJECT / ESCALATE
```

---

# 14. Dependency Validity

An object is not fully valid if a mandatory upstream dependency has become invalid.

Example:

```text
Intent v2
   ↓
Evidence v4
```

If:

```text
Intent v2
```

is invalidated, downstream evidence may require re-evaluation.

The system should detect dependency invalidation.

---

# 15. Cascading Invalidation

Upstream invalidation may propagate.

Example:

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
CHANNEL PROJECTION
```

If the knowledge is materially invalidated:

```text
DOWNSTREAM IMPACT ANALYSIS
```

must determine which descendants require:

```text
REVALIDATION
REVISION
INVALIDATION
```

Not every descendant must automatically be deleted.

---

# 16. Cascading Revision

An upstream revision may require downstream revision without invalidating everything.

Example:

```text
Evidence v3
→ Evidence v4

Asset Strategy v5
→ still valid

Narrative v6
→ requires revision
```

The system should evaluate impact rather than assume total invalidation.

---

# 17. Dependency Status

Each dependency should conceptually have a state:

```text
VALID
STALE
INVALID
MISSING
UNVERIFIED
```

This allows downstream objects to detect whether they remain consumable.

---

# 18. Stale Object

An object is stale when:

> A newer relevant upstream version exists and the object has not been evaluated against that change.

Stale does not automatically mean invalid.

```text
STALE
→ REVALIDATE
```

is generally preferred over:

```text
STALE
→ DELETE
```

---

# 19. Invalid Object

An object becomes invalid when its governing assumptions or requirements no longer hold.

Examples:

```text
product changed
source retracted
authority revoked
hard constraint changed
critical dependency invalidated
```

Invalid objects must not be used as active authoritative inputs.

---

# 20. Lock Semantics

A lock protects semantic integrity.

It should specify:

```text
lock_id
object
version
scope
authority
reason
created_at
unlock_conditions
```

---

# 21. Partial Locks

Some objects may have partially locked fields.

Example:

```text
Campaign Intent:
objective → LOCKED
tone → FLEXIBLE
CTA → OPEN
```

Partial locking may be useful but must be explicit.

A field-level lock cannot be inferred from object-level lock unless the schema defines that behavior.

---

# 22. Lock Propagation

A lock on an upstream object does not automatically lock every descendant.

Example:

```text
LOCKED INTENT
```

does not necessarily mean:

```text
LOCKED ASSET STRATEGY
```

However, downstream agents must respect the locked dependency.

---

# 23. Unlocking

Unlocking must record:

```text
unlock authority
reason
trigger
previous state
new state
impact
```

Possible unlock triggers:

```text
user instruction
critical failure
new authoritative evidence
policy change
product change
approved recovery
```

---

# 24. Revision

Revision means creating a new semantic version.

```text
v1
 ↓
revision
 ↓
v2
```

The original remains immutable for audit.

---

# 25. Revision Requirements

A revision should preserve:

```text
reason
trigger
changed fields
authority
supporting evidence
impact
previous version
new version
```

---

# 26. Revision vs Mutation

Mutation:

```text
v1 silently changed
```

is prohibited for consequential semantic objects.

Revision:

```text
v1
 ↓
v2
```

is the required pattern.

---

# 27. Supersession

When a new version replaces an old version:

```text
v1 → SUPERSEDED
v2 → ACTIVE
```

The system must preserve the relation:

```text
SUPERSEDED_BY
```

---

# 28. Archival

An object should be archived when it is no longer active but remains relevant to:

```text
audit
research
reproducibility
regression testing
historical reconstruction
```

Archived objects should not normally enter new decisions unless explicitly requested.

---

# 29. Retirement

Retirement removes an object from normal semantic participation.

A retired object may remain available for:

```text
audit
legal retention
historical analysis
security review
```

depending on system policy.

---

# 30. Restoration

If restoration is supported, it must create an explicit transition.

```text
ARCHIVED
 ↓
RESTORED
 ↓
REVALIDATING
```

Restoration must not simply reactivate an old object without checking current dependencies.

---

# 31. Object Consumption

When an object is consumed, the system should record:

```text
consumer
consumer_version
purpose
timestamp
input_version
```

This enables downstream impact analysis.

---

# 32. Multiple Consumers

One object may be consumed by multiple downstream objects.

```text
Evidence v3
   ├── Asset Strategy v4
   ├── Narrative v5
   └── Evaluation v2
```

The lifecycle system must preserve all dependencies.

---

# 33. Consumption Does Not Transfer Ownership

A consumer does not gain authority over the consumed object.

```text
READ
≠
OWN
≠
MODIFY
```

This follows II-013.

---

# 34. Lifecycle and Governance

Lifecycle transitions must respect agent authority.

Example:

```text
Agent:
REQUEST LOCK

Governance:
VERIFY AUTHORITY

Lifecycle:
LOCK
```

An agent should not be able to lock an object merely because it wants to prevent another agent from changing it.

---

# 35. Lifecycle and Evaluation

Evaluation can trigger state transitions.

Example:

```text
GENERATED
 ↓
EVALUATING
 ↓
PASS
 ↓
ACCEPTED
```

or:

```text
EVALUATING
 ↓
FAIL
 ↓
REQUIRES_RECOVERY
```

Evaluation results must remain separate from lifecycle state.

---

# 36. Lifecycle and Replanning

A failed evaluation may trigger:

```text
ACTIVE
 ↓
REQUIRES_REPLAN
```

The Recovery Engine then determines the appropriate action.

The lifecycle engine should not decide strategy by itself.

---

# 37. Lifecycle and Provenance

Every state transition must become part of the object's lineage.

```text
OBJECT
 ↓
STATE TRANSITION
 ↓
AUDIT EVENT
```

This enables:

> Why is this object currently in this state?

to be answered.

---

# 38. Lifecycle and Authority

An object may only enter an authoritative state if the required authority exists.

Example:

```text
VALID
 ↓
APPROVED
```

requires an approving authority.

The system must reject:

```text
APPROVED
```

records with no valid approval provenance.

---

# 39. Lifecycle and Knowledge Updates

When new knowledge arrives:

```text
NEW KNOWLEDGE
 ↓
IMPACT ANALYSIS
 ↓
DEPENDENT OBJECTS
 ↓
REVALIDATE
```

The system should avoid global invalidation unless evidence requires it.

---

# 40. Lifecycle and Law / Policy Updates

When a governing law, policy, glossary, or system rule changes:

```text
LAW / POLICY v1
        ↓
v2
        ↓
DEPENDENCY SEARCH
        ↓
AFFECTED OBJECTS
        ↓
REVALIDATION
```

This makes the intelligence layer maintainable over time.

---

# 41. Lifecycle and Model Updates

A model update should not automatically invalidate semantic objects.

However, outputs whose validity depends materially on model behavior may require regression evaluation.

The system should distinguish:

```text
MODEL CHANGE
```

from:

```text
KNOWLEDGE CHANGE
```

and:

```text
SEMANTIC REQUIREMENT CHANGE
```

---

# 42. Lifecycle and Prompt Compiler

A prompt compiler change may affect generated outputs without invalidating upstream campaign intelligence.

Example:

```text
Prompt Compiler v4
 ↓
Generation changes
```

The architecture should evaluate:

```text
output regression
```

rather than unnecessarily rewriting:

```text
intent
evidence
asset strategy
```

---

# 43. Object State Queries

The lifecycle system should eventually support queries such as:

```text
What is the current valid version?

Is this object approved?

Is it locked?

Who owns it?

Which dependencies are stale?

Which downstream objects depend on it?

Why was it invalidated?

What superseded it?

Can it be consumed?
```

These are architectural requirements.

---

# 44. Consumability

A downstream agent should not consume an object merely because it exists.

Conceptually:

```text
OBJECT
 ↓
CAN_CONSUME?
 ↓
STATE
AUTHORITY
VERSION
DEPENDENCIES
LOCKS
VALIDITY
 ↓
YES / NO / ESCALATE
```

---

# 45. Consumability Rules

An object should generally be consumable when:

```text
state permits consumption
authority is valid
required dependencies are valid
version is current enough
no blocking conflict exists
provenance is sufficient
```

Exact rules are object-specific.

---

# 46. Orphan Objects

An orphan object is one whose required parent or authority reference is missing.

Examples:

```text
Asset Strategy
→ no intent reference

Decision
→ no authority

Evaluation
→ no target
```

Orphans should be detected as lifecycle integrity failures.

---

# 47. Zombie Objects

A zombie object is one that has been:

```text
INVALIDATED
SUPERSEDED
RETIRED
```

but continues to influence active decisions.

This is a critical lifecycle failure.

The system should detect:

```text
ZOMBIE DEPENDENCY
```

---

# 48. State Drift

State drift occurs when the stored lifecycle state no longer reflects the object's actual semantic condition.

Example:

```text
Object:
APPROVED

But:
approval authority was revoked.
```

The lifecycle system must support periodic or event-triggered state integrity checks.

---

# 49. Lifecycle Reconciliation

A reconciliation process should compare:

```text
OBJECT STATE
+
DEPENDENCY STATE
+
AUTHORITY STATE
+
PROVENANCE
+
EVALUATION
```

and identify inconsistencies.

Possible outcomes:

```text
CONSISTENT
STALE
INVALID
REQUIRES_REVIEW
CORRUPTED
```

---

# 50. Self-Critique Requirements

The Self-Critique Agent should inspect lifecycle behavior for:

- unauthorized transitions,
- stale active objects,
- zombie dependencies,
- hidden mutation,
- missing approval,
- invalid locks,
- premature archival,
- unjustified invalidation,
- state drift,
- and incorrect lifecycle recovery.

The critic should produce findings rather than silently rewriting lifecycle state.

---

# 51. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to:

1. Mutate locked objects.
2. Skip validation states.
3. Promote drafts to approved status without authority.
4. Consume invalid objects.
5. Hide stale dependencies.
6. Create zombie dependencies.
7. Delete superseded versions.
8. Forge approval provenance.
9. Restore invalid objects without revalidation.
10. Trigger cascading invalidation unnecessarily.
11. Prevent required cascading invalidation.
12. Create orphan objects.
13. Create impossible state transitions.
14. Exploit partial locks.
15. Use archived objects as active truth.
16. Bypass lifecycle guards.
17. Make state appear valid while authority is invalid.
18. Create lifecycle loops with no terminal state.

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

# 52. Validation Invariants

### Invariant 1

Every consequential object has an explicit lifecycle state.

### Invariant 2

State does not imply authority.

### Invariant 3

State does not imply truth.

### Invariant 4

Confidence cannot bypass lifecycle requirements.

### Invariant 5

Consequential state transitions preserve provenance.

### Invariant 6

Invalid transitions are rejected.

### Invariant 7

Locked semantic objects cannot be silently mutated.

### Invariant 8

Semantic changes create new versions.

### Invariant 9

Superseded versions remain auditable.

### Invariant 10

Invalidated objects cannot silently participate in new authoritative decisions.

### Invariant 11

Stale dependencies are detectable.

### Invariant 12

Zombie dependencies are detectable.

### Invariant 13

Object consumers do not inherit ownership.

### Invariant 14

Approval requires valid authority.

### Invariant 15

Restoration requires revalidation where dependencies may have changed.

### Invariant 16

Lifecycle state remains consistent with authority and dependency state.

### Invariant 17

Orphan objects are detectable.

### Invariant 18

Lifecycle transitions cannot create unbounded state loops.

### Invariant 19

Archived objects cannot silently re-enter active decision paths.

### Invariant 20

Self-Critique and Adversarial Verification findings remain auditable.

---

# 53. Falsifiable Architectural Hypotheses

## Hypothesis A — Explicit lifecycle states reduce invalid object consumption

**Experiment:**

Inject objects that are:

```text
DRAFT
INVALIDATED
STALE
ARCHIVED
```

Compare:

```text
state-aware consumption
vs
existence-based consumption
```

Measure invalid consumption rate.

---

## Hypothesis B — Dependency-aware invalidation reduces both stale decisions and unnecessary recomputation

**Experiment:**

Change upstream objects selectively.

Compare:

```text
global invalidation
vs
dependency-aware revalidation
```

Measure:

```text
stale decision rate
unnecessary recomputation
recovery cost
```

---

## Hypothesis C — Immutable semantic versions improve audit reconstruction

**Experiment:**

Compare mutable records with versioned records.

Measure:

```text
decision reconstruction accuracy
change attribution accuracy
```

---

## Hypothesis D — Lifecycle guards prevent unauthorized state escalation

**Experiment:**

Attempt:

```text
DRAFT → APPROVED
LOCKED → MUTATED
INVALIDATED → CONSUMED
```

without proper authority.

Expected:

```text
BLOCK
```

---

## Hypothesis E — Lifecycle reconciliation detects hidden state drift

**Experiment:**

Create inconsistencies between:

```text
object state
authority state
dependency state
```

Measure detection rate.

---

## Hypothesis F — Zombie detection prevents invalid knowledge propagation

**Experiment:**

Invalidate an upstream object after downstream objects have consumed it.

Measure whether active downstream decisions are correctly identified for revalidation.

---

# 54. Lifecycle Evaluation

The lifecycle system should eventually expose:

```text
INVALID TRANSITION RATE
STALE OBJECT RATE
ZOMBIE DEPENDENCY RATE
ORPHAN OBJECT RATE
UNAUTHORIZED STATE CHANGE RATE
STATE DRIFT RATE
VERSION INTEGRITY
DEPENDENCY REVALIDATION ACCURACY
```

These should remain diagnostic metrics.

---

# 55. Lifecycle Test Corpus

The architecture should maintain cases covering:

```text
NORMAL CREATION
VALIDATION FAILURE
APPROVAL
LOCKING
UNLOCKING
REVISION
SUPERSESSION
INVALIDATION
ARCHIVAL
RESTORATION
STALE DEPENDENCY
ZOMBIE DEPENDENCY
ORPHAN OBJECT
STATE DRIFT
UNAUTHORIZED TRANSITION
PARTIAL LOCK
CASCADE CHANGE
MODEL UPDATE
KNOWLEDGE UPDATE
LAW / POLICY UPDATE
```

Each case should define:

```text
initial state
trigger
expected transition
expected authority
expected downstream impact
terminal state
```

---

# 56. Architecture Proof Through Lifecycle

Lifecycle behavior provides another falsifiable surface for the architecture.

The system should eventually demonstrate that it can:

```text
prevent unauthorized transitions
preserve historical versions
detect stale dependencies
prevent zombie consumption
revalidate affected descendants
preserve authority boundaries
recover from upstream change
```

These are measurable system properties.

---

# 57. Core Contract

> **The Intelligence Object Lifecycle Layer shall govern the creation, validation, approval, locking, consumption, revision, invalidation, supersession, archival, restoration, and retirement of consequential intelligence objects through explicit, authority-scoped, provenance-preserving state transitions. It shall prevent invalid, stale, zombie, orphaned, or unauthorized objects from silently participating in active decisions; detect dependency and state drift; preserve semantic versions; coordinate with evaluation, governance, recovery, and audit systems; and expose lifecycle behavior to self-critique and adversarial verification.**

---

# 58. Deferred Decisions

II-014 does not freeze:

- exact state-machine implementation,
- database representation,
- event-sourcing architecture,
- lifecycle orchestration,
- object-specific transition matrices,
- retention policy,
- archival storage,
- restoration policy,
- field-level locking syntax,
- dependency propagation algorithm,
- garbage collection strategy.

These remain engineering decisions.

---

# 59. Exit Criteria

II-014 is semantically complete when:

- [x] Object lifecycle defined
- [x] Lifecycle states defined
- [x] State / authority distinction established
- [x] State / truth distinction established
- [x] State / confidence distinction established
- [x] Object-specific lifecycle principle established
- [x] Transition provenance established
- [x] Valid transition principle established
- [x] Invalid transition principle established
- [x] Lifecycle guards established
- [x] Dependency validity established
- [x] Cascading invalidation established
- [x] Cascading revision established
- [x] Stale object semantics established
- [x] Invalid object semantics established
- [x] Lock semantics established
- [x] Partial locks established
- [x] Unlocking established
- [x] Revision / mutation distinction established
- [x] Supersession established
- [x] Archival established
- [x] Retirement established
- [x] Restoration established
- [x] Consumption lineage established
- [x] Consumability established
- [x] Orphan object detection established
- [x] Zombie object detection established
- [x] State drift established
- [x] Lifecycle reconciliation established
- [x] Governance integration established
- [x] Evaluation integration established
- [x] Replanning integration established
- [x] Provenance integration established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Lifecycle evaluation established
- [x] Lifecycle test corpus established
- [x] Architecture-proof role established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-015 — Intelligence Runtime & Execution Contract**

This specification will define how the ratified semantic contracts become an executable runtime: orchestration boundaries, execution order, dependency scheduling, state access, retries, concurrency, deterministic controls, observability, and the boundary between the intelligence runtime and the generation runtime.
