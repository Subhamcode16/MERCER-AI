# III-002 — Authority Schema & Delegation Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** II-001 through II-017, II-RAT-001 through II-RAT-003, III-001  
**Purpose:** Compile the ratified authority model into a machine-readable contract for scoped authority, delegation, verification, revocation, conflicts, overrides, and human/agent authority.

---

## 1. Purpose

III-002 translates the frozen authority semantics into an explicit machine-readable contract.

The central rule remains:

```text
CAPABILITY
≠
AUTHORITY
```

An actor may possess technical capability without being authorized to exercise that capability in a particular context.

Authority therefore must be:

```text
explicit
scoped
verifiable
traceable
time-aware where applicable
revocable where applicable
```

---

## 2. Authority Is a First-Class Object

Authority must not be represented as an implicit property of:

```text
model
agent
role
API key
tool access
runtime process
confidence
```

Instead, authority is represented explicitly.

Conceptually:

```yaml
authority:
  authority_id: ...
  subject: ...
  scope: ...
  decision_types: ...
  constraints: ...
  issued_by: ...
  valid_from: ...
  valid_until: ...
  status: ...
  provenance_ref: ...
```

The exact serialized schema remains an implementation concern.

---

## 3. Authority Identity

Every authority record receives a globally unique identifier.

Recommended conceptual form:

```text
AUTH-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

Authority identity must not encode the authority's meaning.

Bad:

```text
ADMIN-PRODUCTION-APPAREL
```

Preferred:

```text
AUTH-01J...
```

---

## 4. Authority Subject

Every authority record must identify its subject.

A subject may be:

```text
human
agent
service
organization
system component
delegated principal
```

Conceptually:

```yaml
subject:
  subject_type: agent
  subject_id: agent-...
```

The subject's identity must be resolvable.

---

## 5. Authority Scope

Authority is never assumed to be universal.

Every authority record must define its scope.

Possible dimensions include:

```text
domain
object_type
object_scope
operation
campaign
environment
resource
decision_type
```

Example:

```yaml
scope:
  domain: apparel
  operations:
    - propose
    - evaluate
```

A subject authorized within one scope must not automatically receive authority outside that scope.

---

## 6. Scope Intersection

When multiple scopes apply:

```text
EFFECTIVE AUTHORITY
=
INTERSECTION OF APPLICABLE LIMITS
```

The implementation must not union scopes merely because multiple authority records exist.

If authority A allows:

```text
APPAREL
```

and authority B allows:

```text
PRODUCTION
```

the resulting authority must be derived through explicit policy, not by assuming:

```text
APPAREL + PRODUCTION = ALL
```

---

## 7. Decision Type

Authority must distinguish what an actor is permitted to decide or perform.

Possible decision types include:

```text
PROPOSE
READ
RETRIEVE
EVALUATE
APPROVE
REJECT
COMMIT
EXECUTE
DELEGATE
OVERRIDE
INVALIDATE
ARCHIVE
RESTORE
```

The definitive vocabulary must be compiled from the ratified architecture.

An actor authorized to:

```text
PROPOSE
```

is not automatically authorized to:

```text
APPROVE
```

---

## 8. Authority and Capability

The runtime must distinguish:

```text
CAN_EXECUTE
```

from:

```text
MAY_EXECUTE
```

Conceptually:

```text
capability check
+
authority check
+
state check
+
policy check
=
execution eligibility
```

Capability alone is insufficient.

---

## 9. Authority Status

Authority records should have an explicit status.

Conceptually:

```text
ACTIVE
SUSPENDED
REVOKED
EXPIRED
SUPERSEDED
```

An inactive authority must not be treated as active.

The definitive lifecycle semantics for authority records must remain compatible with II-014 and the dedicated authority implementation.

---

## 10. Validity Window

Where applicable, authority may have:

```text
valid_from
valid_until
```

The runtime must evaluate the authority against execution time.

An authority that was valid yesterday must not automatically be treated as valid today.

---

## 11. Revocation

Authority must support explicit revocation.

Conceptually:

```yaml
revocation:
  revoked_at: ...
  revoked_by: ...
  reason: ...
  provenance_ref: ...
```

Revocation must remain auditable.

A revoked authority cannot be silently reactivated by the subject.

---

## 12. Delegation

Authority may be delegated only where the source authority explicitly permits delegation.

Conceptually:

```text
SOURCE AUTHORITY
        ↓
DELEGATION
        ↓
DELEGATED AUTHORITY
```

Delegation does not automatically transfer all authority.

---

## 13. Delegation Contract

A delegation should preserve:

```text
delegation_id
source_authority_id
delegated_subject
scope
decision_types
constraints
issued_at
validity
revocation
provenance
```

The delegated scope must be bounded by the source authority.

---

## 14. No Scope Expansion Through Delegation

The fundamental invariant is:

```text
DELEGATED AUTHORITY
⊆
SOURCE AUTHORITY
```

A delegate must never gain authority greater than the authority that created the delegation.

If scope expansion is required, it must come from a separate authorized authority decision.

---

## 15. Delegation Depth

Delegation chains should be explicitly bounded.

Conceptually:

```text
A
 ↓
B
 ↓
C
```

must preserve the complete chain.

The implementation must define a maximum delegation depth or equivalent cycle-prevention mechanism.

Do not permit:

```text
A → B → C → A
```

---

## 16. Delegation Revocation

Revocation of a source authority must invalidate applicable delegated authority unless the authority contract explicitly defines another behavior.

The runtime must therefore resolve:

```text
source authority
→ delegation chain
→ effective authority
```

before acting.

---

## 17. Authority Verification

Before a consequential action, the runtime must resolve:

```text
subject identity
+
authority identity
+
scope
+
decision type
+
validity
+
revocation
+
delegation chain
+
object state
```

Only then can it determine whether the action is authorized.

---

## 18. Authority Resolution

Conceptually:

```text
REQUEST
 ↓
IDENTIFY SUBJECT
 ↓
LOAD AUTHORITY
 ↓
VERIFY STATUS
 ↓
VERIFY TIME
 ↓
VERIFY SCOPE
 ↓
VERIFY DECISION TYPE
 ↓
VERIFY DELEGATION
 ↓
VERIFY OBJECT STATE
 ↓
AUTHORIZE / DENY / ESCALATE
```

---

## 19. Authority Does Not Override Lifecycle Automatically

Even valid authority does not automatically permit an action forbidden by object lifecycle.

Therefore:

```text
AUTHORITY VALID
+
OBJECT STATE FORBIDS ACTION
=
DENY / ESCALATE
```

Authority and lifecycle are complementary constraints.

---

## 20. Authority Does Not Override Evidence Requirements

Likewise, an authorized actor cannot silently convert insufficient evidence into sufficient evidence.

Where a decision contract requires evidence:

```text
AUTHORITY
+
EVIDENCE REQUIREMENT
+
EVIDENCE SUFFICIENCY
=
DECISION ELIGIBILITY
```

---

## 21. Authority Does Not Override Critical Invariants

A valid authority record does not automatically permit violation of:

```text
critical architectural invariant
security boundary
mandatory provenance requirement
non-overridable lifecycle constraint
```

Where an explicit override exists, the override itself must be governed.

---

## 22. Human Authority

Human authority must be represented explicitly rather than inferred from:

```text
login session
account ownership
developer status
```

A human decision should preserve:

```text
human subject identity
authority context
decision
scope
timestamp
provenance
```

---

## 23. Agent Authority

Agent authority is also explicit.

An agent may have:

```text
read authority
proposal authority
evaluation authority
execution authority
```

but these permissions remain scoped.

An agent's model capability does not automatically expand its authority.

---

## 24. Cross-Domain Authority

Cross-domain actions require explicit authority.

For example:

```text
APPAREL
+
FOOTWEAR
+
JEWELRY
```

does not automatically create:

```text
CROSS-DOMAIN AUTHORITY
```

The runtime must identify which authority permits the reconciliation.

---

## 25. Conflict Resolution

When authority records conflict:

```text
AUTHORITY A → ALLOW
AUTHORITY B → DENY
```

the runtime must not arbitrarily choose one.

It should resolve through:

```text
scope
priority where explicitly defined
issuer authority
decision type
object state
governance policy
human escalation where required
```

The resolution must be recorded.

---

## 26. No Implicit Priority

The implementation must not invent:

```text
agent hierarchy
model strength hierarchy
creation-time priority
confidence priority
```

unless such priority is explicitly defined by the ratified governance contract.

---

## 27. Override

Overrides are exceptional authority operations.

An override must preserve:

```text
override_id
issuer
target authority / decision
scope
reason
timestamp
expiration where applicable
provenance
```

An override must itself be authorized.

---

## 28. Override Does Not Mean Unbounded Authority

An override must be:

```text
scoped
specific
traceable
time-bounded where appropriate
```

Avoid:

```text
override = true
```

as a universal bypass.

Prefer:

```text
override:
  target: ...
  permitted_operation: ...
  scope: ...
  expires_at: ...
```

---

## 29. Emergency Authority

If emergency authority exists, it must be explicitly modeled.

Emergency mode must not be implemented as:

```text
disable all checks
```

Instead, define:

```text
emergency scope
allowed operations
duration
issuer
audit requirements
post-event review
```

Exact emergency semantics remain deferred.

---

## 30. Authority Proof

The system should be able to answer:

```text
WHO
authorized
WHAT
to do
WHERE
WHEN
UNDER WHICH SCOPE
THROUGH WHICH DELEGATION
ON WHICH OBJECT
UNDER WHICH VERSION
```

This becomes an audit requirement.

---

## 31. Authority Decision Record

A consequential authorization decision should produce a structured record.

Conceptually:

```yaml
authorization_decision:
  decision_id: ...
  subject: ...
  requested_operation: ...
  object_ref: ...
  authority_refs: []
  lifecycle_state: ...
  decision: ALLOW
  reason: ...
  evaluated_at: ...
  provenance_ref: ...
```

The exact schema may be refined by the execution and provenance contracts.

---

## 32. Denial Is a First-Class Result

Authorization must support:

```text
ALLOW
DENY
ESCALATE
INSUFFICIENT_CONTEXT
```

The system must not collapse:

```text
DENY
```

into:

```text
ERROR
```

because denial may be the correct result.

---

## 33. Abstention

Where authority cannot be resolved reliably:

```text
DO NOT GUESS
```

The runtime should return:

```text
INSUFFICIENT_CONTEXT
```

or:

```text
ESCALATE
```

as applicable.

---

## 34. Authority Provenance

Every consequential authority decision must remain traceable to:

```text
authority record
issuer
delegation chain
object
requested action
runtime decision
```

This connects III-002 to III-004.

---

## 35. Authority References

Objects should reference authority records by:

```text
authority_id
```

and, where required, an explicit version.

Do not copy the entire authority record into every object unless required for immutable evidence snapshots.

---

## 36. Snapshotting

For historical audit, an authorization decision may preserve a snapshot of the authority context used at decision time.

This prevents later authority mutation from changing historical interpretation.

The snapshot should preserve:

```text
authority version
scope
decision types
status
validity
delegation chain
```

---

## 37. Authority Immutability

Committed authority records should be immutable.

Changes should create:

```text
new authority version
```

or an explicit lifecycle transition such as:

```text
revoked
expired
superseded
```

Historical authority must remain reconstructable.

---

## 38. Authority Equality

Distinguish:

```text
AUTHORITY IDENTITY
AUTHORITY VERSION
EFFECTIVE AUTHORITY
```

Two authority records may share a subject but have different:

```text
scope
decision type
validity
constraints
```

and therefore are not equivalent.

---

## 39. Authority Object Conceptual Schema

```yaml
authority:
  authority_id: AUTH-...
  version: 1.0.0

  subject:
    subject_type: ...
    subject_id: ...

  issuer:
    subject_type: ...
    subject_id: ...

  scope:
    domain: ...
    object_types: []
    object_ids: []
    operations: []
    environments: []

  decision_types: []

  constraints: []

  status: ACTIVE

  valid_from: ...
  valid_until: ...

  delegation:
    allowed: false
    parent_authority_id: null
    depth: 0

  provenance_ref: ...

  integrity:
    content_hash: ...
```

This is conceptual, not final JSON Schema.

---

## 40. Delegation Conceptual Schema

```yaml
delegation:
  delegation_id: DEL-...
  source_authority_id: AUTH-...
  source_authority_version: ...

  delegated_subject:
    subject_type: ...
    subject_id: ...

  scope: ...
  decision_types: []
  constraints: []

  issued_at: ...
  valid_until: ...

  status: ACTIVE

  provenance_ref: ...
```

---

## 41. Effective Authority

The runtime should derive an effective authorization context rather than blindly selecting one authority record.

Conceptually:

```text
SUBJECT
+
REQUEST
+
OBJECT
+
OBJECT STATE
+
AUTHORITY RECORDS
+
DELEGATION CHAIN
+
POLICY
=
EFFECTIVE AUTHORITY DECISION
```

---

## 42. Authority Composition

Multiple authority records must not automatically combine.

Composition requires an explicit policy.

For example:

```text
Authority A: may evaluate
Authority B: may execute
```

does not necessarily mean:

```text
Subject may evaluate + execute
```

unless the governance contract permits composition.

---

## 43. Least Authority

Where multiple valid authority interpretations exist, the runtime should prefer the least authority necessary to fulfill the requested operation.

This minimizes accidental privilege expansion.

The exact formal optimization rule remains deferred.

---

## 44. Authority Leakage

The runtime must prevent authority from leaking across:

```text
object
domain
campaign
environment
agent
delegation
```

An authority resolved for one request must not silently persist into unrelated requests.

---

## 45. Context Binding

Where applicable, authority should bind to:

```text
request_id
object_id
object_version
campaign_id
environment
```

This prevents replay of an authority decision in an unrelated context.

---

## 46. Replay Protection

A historical authorization decision must not automatically be reusable for a new request.

The runtime should verify:

```text
decision context
authority validity
object version
request context
```

before reuse.

---

## 47. Authority Attack Surface

III-002 must support adversarial tests for:

```text
authority spoofing
scope escalation
delegation escalation
delegation cycle
expired authority replay
revoked authority replay
cross-domain leakage
override abuse
issuer spoofing
conflicting authority
capability/authority confusion
```

---

## 48. Falsification Cases

The reference implementation should deliberately test:

```text
agent has capability but no authority
authority exists but wrong scope
authority correct but expired
authority correct but revoked
delegate exceeds source scope
delegate chain exceeds depth
conflicting allow/deny
invalid override
fake issuer
authority replay
cross-domain authority leakage
```

---

## 49. Security Invariants

### Invariant 1

Capability does not imply authority.

### Invariant 2

Authority must be explicit.

### Invariant 3

Authority is scoped.

### Invariant 4

Decision type is explicit.

### Invariant 5

Delegation cannot expand source authority.

### Invariant 6

Delegation chains are traceable.

### Invariant 7

Delegation cycles are prohibited.

### Invariant 8

Expired authority is not active authority.

### Invariant 9

Revoked authority is not active authority.

### Invariant 10

Authority does not automatically override lifecycle constraints.

### Invariant 11

Authority does not automatically override evidence requirements.

### Invariant 12

Authority does not automatically override critical invariants.

### Invariant 13

Overrides are governed.

### Invariant 14

Cross-domain authority is explicit.

### Invariant 15

Conflicts are resolved explicitly.

### Invariant 16

No implicit priority is invented.

### Invariant 17

Denial is a valid outcome.

### Invariant 18

Unresolvable authority produces abstention or escalation.

### Invariant 19

Authorization decisions are auditable.

### Invariant 20

Historical authority remains reconstructable.

### Invariant 21

Authority cannot silently leak across contexts.

### Invariant 22

Historical authorization decisions cannot be blindly replayed.

### Invariant 23

Implementation must not invent authority semantics.

---

## 50. Required Tests

Before the runtime consumes III-002:

```text
identity resolution
scope matching
decision-type matching
validity-window checking
revocation checking
delegation verification
delegation depth
delegation cycle
conflict resolution
override verification
human authority
agent authority
cross-domain authority
replay protection
authority leakage
abstention
```

---

## 51. Required Authorization Trace

For every consequential authorization decision, the system should be able to reconstruct:

```text
REQUEST
 ↓
SUBJECT
 ↓
CAPABILITY
 ↓
AUTHORITY RECORDS
 ↓
DELEGATION CHAIN
 ↓
SCOPE CHECK
 ↓
DECISION TYPE CHECK
 ↓
LIFECYCLE CHECK
 ↓
EVIDENCE CHECK
 ↓
POLICY / OVERRIDE CHECK
 ↓
ALLOW / DENY / ESCALATE
```

---

## 52. Deferred Decisions

III-002 intentionally does not freeze:

- exact authority storage;
- exact delegation-depth limit;
- final priority model where governance permits priority;
- exact emergency-authority semantics;
- cryptographic identity implementation;
- token/session integration;
- persistence mechanism;
- exact policy-engine implementation;
- final decision-type registry beyond ratified semantics.

These remain engineering decisions unless they change semantic meaning.

---

## 53. Exit Criteria

- [x] Authority identity defined
- [x] Authority subject defined
- [x] Authority scope defined
- [x] Decision type defined
- [x] Capability/authority boundary defined
- [x] Authority status defined
- [x] Validity window defined
- [x] Revocation defined
- [x] Delegation defined
- [x] Delegation containment defined
- [x] Delegation depth/cycle boundary defined
- [x] Authority verification defined
- [x] Lifecycle interaction defined
- [x] Evidence interaction defined
- [x] Human authority defined
- [x] Agent authority defined
- [x] Cross-domain authority defined
- [x] Conflict resolution defined
- [x] Override defined
- [x] Abstention defined
- [x] Provenance integration defined
- [x] Historical reconstruction defined
- [x] Replay protection defined
- [x] Attack surface defined
- [x] Falsification cases defined
- [x] Security invariants defined
- [x] Required tests defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

## 54. Next Contract

**III-003 — Intelligence Object Lifecycle & State Machine Contract**

III-003 will compile the ratified lifecycle model into an explicit machine-readable state machine covering:

```text
states
transitions
transition authority
preconditions
postconditions
invalid transitions
locking
invalidation
supersession
archival
restoration
recovery
runtime-state separation
transition provenance
```

The central boundary remains:

```text
OBJECT STATE
≠
AUTHORITY
≠
RUNTIME STATE
```
