# III-006 — Constraint, Policy & Invariant Enforcement Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001, III-002, III-003, III-004, III-005 and the ratified Phase II semantic architecture  
**Purpose:** Define the machine-readable contract for constraints, policies, invariants, enforcement, conflicts, exceptions, violations, escalation, and runtime compliance.

---

# 1. Purpose

III-006 translates the architecture's constraint semantics into an enforceable machine-readable contract.

The central distinction is:

```text
RECOMMENDATION
    ≠
CONSTRAINT
    ≠
NON-OVERRIDABLE INVARIANT
```

A recommendation may guide behavior.

A constraint restricts behavior.

A non-overridable invariant defines a condition that the architecture does not permit ordinary policy, authority, or agent discretion to violate.

---

# 2. Constraint as a First-Class Object

Every consequential constraint should have an explicit identity and scope.

Conceptually:

```yaml
constraint:
  constraint_id: CON-...
  version: ...
  type: ...
  scope: ...
  rule: ...
  severity: ...
  enforcement_mode: ...
  provenance_ref: ...
```

The exact serialization is deferred.

---

# 3. Constraint Identity

Every constraint receives a stable identifier.

Recommended conceptual form:

```text
CON-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

Constraint identity must not encode its priority or meaning.

---

# 4. Constraint Version

Constraints are versioned independently of:

```text
object version
agent version
policy-engine version
```

A change to constraint meaning must create a new constraint version.

Historical constraint versions remain reconstructable.

---

# 5. Constraint Type

The architecture should distinguish at minimum:

```text
PROHIBITION
REQUIREMENT
PRECONDITION
LIMIT
INVARIANT
RECOMMENDATION
```

The final registry must be compiled from the ratified semantics.

Do not use one generic boolean field to represent all of these.

---

# 6. Recommendation

A recommendation expresses preferred behavior.

Conceptually:

```text
SHOULD
```

A recommendation does not automatically block execution.

If a recommendation is violated, the system may record:

```text
deviation
```

without necessarily producing:

```text
constraint violation
```

---

# 7. Constraint

A binding constraint establishes a condition that must hold for a defined action or state.

Conceptually:

```text
MUST
```

Violation of a binding constraint should normally prevent the governed operation unless an explicitly authorized exception exists.

---

# 8. Prohibition

A prohibition defines an action or state that is not permitted.

Conceptually:

```text
MUST NOT
```

Examples:

```text
agent must not access object outside scope
agent must not mutate locked object
agent must not bypass provenance
agent must not execute without required authority
```

---

# 9. Requirement

A requirement defines something that must be present or satisfied.

Conceptually:

```text
MUST HAVE
```

Examples:

```text
required evidence
required approval
required provenance
required schema
required human review
```

---

# 10. Preconditions

A precondition defines what must be true before an operation can occur.

Conceptually:

```text
PRECONDITION
→
ACTION ELIGIBLE
```

A failed precondition prevents the operation.

---

# 11. Limits

A limit constrains a measurable quantity.

Examples:

```text
maximum tool calls
maximum execution time
maximum budget
maximum delegation depth
maximum object size
```

The runtime must enforce limits where they are defined as binding.

---

# 12. Invariant

An invariant defines a property that must remain true across the governed system.

Examples:

```text
CAPABILITY ≠ AUTHORITY
OBJECT EXISTS ≠ OBJECT IS CONSUMABLE
HISTORICAL VERSIONS REMAIN TRACEABLE
PROVENANCE CANNOT BE SILENTLY ERASED
```

The definitive invariant registry must come from ratified architecture.

---

# 13. Non-Overridable Invariant

Some invariants may be explicitly classified as non-overridable.

Such an invariant cannot be bypassed through:

```text
agent authority
human preference
policy
emergency mode
tool output
model confidence
```

If an implementation requires violating such an invariant, the architecture must be changed rather than silently bypassed.

---

# 14. Constraint Scope

Every constraint must define where it applies.

Possible scope dimensions:

```text
domain
object_type
object_id
object_version
agent
operation
environment
campaign
workflow
tool
lifecycle_state
```

A constraint outside its scope must not be applied as though it were universal.

---

# 15. Scope Intersection

When multiple constraints apply:

```text
EFFECTIVE CONSTRAINT SET
=
ALL APPLICABLE BINDING CONSTRAINTS
```

A broader constraint must not be discarded simply because a narrower constraint exists unless the policy explicitly defines precedence.

---

# 16. Constraint Applicability

Before enforcement, the system must resolve:

```text
constraint identity
constraint version
scope
target object
operation
agent
environment
lifecycle state
```

Only then can it determine applicability.

---

# 17. Policy

A policy is a structured collection of rules governing behavior.

Conceptually:

```text
POLICY
→ constraints
→ permissions
→ required conditions
→ evaluation rules
```

A policy does not automatically override object lifecycle or authority semantics.

---

# 18. Policy Identity

Every policy receives an explicit identifier.

Recommended conceptual form:

```text
POL-<ULID>
```

Policies must be versioned.

---

# 19. Policy Composition

Multiple policies may apply simultaneously.

Composition must be explicit.

Avoid silently using:

```text
last policy wins
```

or:

```text
most recent policy wins
```

unless that precedence is itself defined by the governing contract.

---

# 20. Conflict

A policy conflict occurs when applicable rules produce incompatible requirements.

Example:

```text
POLICY A → ALLOW
POLICY B → DENY
```

The runtime must not arbitrarily select one.

---

# 21. Conflict Resolution

Conflict resolution should consider only explicitly defined dimensions such as:

```text
scope
constraint type
policy precedence
authority
environment
non-overridable invariant
```

The system must not invent precedence based on:

```text
model strength
creation timestamp
agent confidence
implementation order
```

---

# 22. Deny-Safe Behavior

When a binding constraint conflict cannot be resolved safely, the default behavior should be:

```text
DO NOT EXECUTE
```

or:

```text
ESCALATE
```

rather than silently selecting a permissive interpretation.

---

# 23. Constraint Evaluation

Conceptually:

```text
REQUEST
 ↓
IDENTIFY APPLICABLE CONSTRAINTS
 ↓
EVALUATE
 ↓
PASS / FAIL / CONFLICT / INSUFFICIENT_CONTEXT
```

The result should remain separate from authorization.

---

# 24. Constraint Result

A structured result may be:

```yaml
constraint_result:
  result_id: ...
  target: ...
  constraint_refs: []
  result: PASS
  failures: []
  conflicts: []
  evaluated_at: ...
```

Possible result states:

```text
PASS
FAIL
CONFLICT
INSUFFICIENT_CONTEXT
NOT_APPLICABLE
```

---

# 25. Constraint Failure

A constraint failure should identify:

```text
constraint
version
target
observed condition
required condition
evidence
timestamp
```

Do not report only:

```text
"policy failed"
```

without identifying the rule.

---

# 26. Violation

A violation represents a condition in which a binding constraint has not been satisfied or has been breached.

Conceptually:

```yaml
violation:
  violation_id: ...
  constraint_id: ...
  target: ...
  observed_at: ...
  evidence_refs: []
  severity: ...
  remediation: ...
```

---

# 27. Violation Severity

Severity may be classified as:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

The exact severity mapping is domain-dependent.

Severity must not itself determine authority unless explicitly specified.

---

# 28. Enforcement Mode

Constraints may have different enforcement modes.

Conceptually:

```text
BLOCK
WARN
ESCALATE
AUDIT
```

A binding constraint should normally use:

```text
BLOCK
```

unless the architecture explicitly defines another enforcement behavior.

---

# 29. Enforcement vs Observation

Recording a violation is not equivalent to preventing it.

Therefore distinguish:

```text
OBSERVE
```

from:

```text
ENFORCE
```

The implementation must not claim enforcement merely because it logs violations.

---

# 30. Hard vs Soft Constraints

A useful implementation distinction is:

```text
HARD
SOFT
```

Hard constraints affect eligibility.

Soft constraints influence preferred behavior but may permit deviation.

The exact semantic mapping must be fixed in the registry.

---

# 31. Soft Constraint Deviation

A soft-constraint deviation should preserve:

```text
constraint
reason
agent / actor
decision
timestamp
```

It must not silently become a hard violation.

---

# 32. Exception / Waiver

A binding constraint may be bypassed only where the architecture explicitly permits exceptions.

An exception should preserve:

```text
exception_id
constraint_ref
scope
reason
issuer
authority
validity
conditions
provenance
```

---

# 33. Exception Is Not Deletion

Granting an exception does not remove the underlying constraint.

Instead:

```text
CONSTRAINT
+
AUTHORIZED EXCEPTION
=
CONTEXTUAL EXEMPTION
```

The original constraint remains historically valid.

---

# 34. Exception Scope

Exceptions must be:

```text
specific
scoped
traceable
time-bounded where appropriate
```

Avoid:

```text
exception = true
```

as a universal bypass.

---

# 35. Non-Overridable Constraint Protection

If a constraint is marked:

```text
NON_OVERRIDABLE
```

then:

```text
EXCEPTION
→ DENIED
```

unless the architecture itself is formally changed.

---

# 36. Emergency Mode

Emergency operation must not automatically disable constraints.

Conceptually:

```text
EMERGENCY
+
APPLICABLE EXCEPTION RULES
+
NON-OVERRIDABLE INVARIANTS
=
EMERGENCY ELIGIBILITY
```

The emergency mechanism remains governed.

---

# 37. Authority Interaction

Authority determines:

```text
MAY THIS ACTOR REQUEST / PERFORM THIS ACTION?
```

Constraints determine:

```text
IS THIS ACTION ALLOWED UNDER THE GOVERNING RULES?
```

Therefore:

```text
AUTHORITY PASS
+
CONSTRAINT FAIL
=
DO NOT EXECUTE
```

---

# 38. Lifecycle Interaction

Lifecycle determines:

```text
IS THIS OBJECT IN A STATE THAT PERMITS THIS OPERATION?
```

Therefore:

```text
AUTHORITY PASS
+
CONSTRAINT PASS
+
LIFECYCLE FAIL
=
DO NOT EXECUTE
```

---

# 39. Provenance Interaction

Consequential constraint decisions must be recorded through III-004.

At minimum:

```text
constraint version
policy version
target
result
actor
timestamp
evidence
exception if any
```

---

# 40. Agent Interaction

Agents must not reinterpret binding constraints through natural-language reasoning.

The runtime should expose machine-readable results:

```text
ALLOW
DENY
ESCALATE
```

with supporting reasons.

---

# 41. Constraint Injection Boundary

Constraint definitions are control-plane data.

Untrusted payloads must not be able to create or modify constraints merely by containing text such as:

```text
"ignore previous policy"
```

Content remains data unless it enters the authorized policy-management pathway.

---

# 42. Policy Injection Boundary

Likewise, an agent output must not become a policy simply because it contains a policy-like structure.

Policy creation requires:

```text
authorized policy operation
+
schema validation
+
lifecycle
+
provenance
```

---

# 43. Constraint Source

Every binding constraint must have a source.

Possible sources:

```text
architecture
governance
product policy
security policy
domain rule
human decision
system invariant
```

The source must be identifiable.

---

# 44. Constraint Provenance

A constraint must preserve:

```text
origin
issuer
version
effective time
scope
change history
```

This enables historical reconstruction.

---

# 45. Constraint Change

Changing a binding constraint must be treated as a governed change.

A modification must not silently mutate historical interpretations.

Prefer:

```text
CONSTRAINT v1
      ↓
CONSTRAINT v2
```

with effective-time semantics.

---

# 46. Temporal Applicability

A constraint may have:

```text
valid_from
valid_until
```

Historical decisions must be evaluated against the constraint version applicable at decision time.

---

# 47. Retroactive Policy Changes

A newly created constraint must not automatically rewrite historical decisions.

If retroactive application is permitted, it must be explicit and separately recorded.

---

# 48. Constraint Evaluation Context

A deterministic evaluation should receive:

```text
request
object
object version
agent
authority
lifecycle state
constraints
policies
evidence
environment
```

The evaluator should not silently retrieve unrelated context.

---

# 49. Determinism

For the same evaluation context:

```text
same inputs
+
same policy versions
+
same constraint versions
```

the enforcement decision should be deterministic unless an explicitly nondeterministic adjudication mechanism is part of the contract.

---

# 50. Constraint Ordering

Where multiple constraints must be evaluated, the implementation should not rely on incidental code order.

The semantic result should remain equivalent regardless of evaluation ordering.

---

# 51. Short-Circuiting

The runtime may short-circuit after a decisive:

```text
NON_OVERRIDABLE FAIL
```

but must preserve enough information for the required audit objective.

Do not hide additional critical violations merely because the first failure was found.

---

# 52. Constraint Caching

Cached constraint results must be invalidated when relevant context changes:

```text
constraint version
object version
authority
lifecycle state
environment
```

Stale policy results must not silently authorize execution.

---

# 53. Constraint Testing

Every critical constraint should have:

```text
positive case
negative case
boundary case
conflict case
exception case where applicable
stale-version case
```

---

# 54. Constraint Falsification

The enforcement layer must be attacked with:

```text
missing constraint
wrong scope
wrong version
conflicting policies
fake exception
expired exception
unauthorized exception
non-overridable bypass
policy injection
constraint injection
stale cached result
agent-generated policy
emergency bypass
```

---

# 55. Invariant Verification

Non-overridable invariants should be continuously tested.

For each invariant:

```text
INVARIANT
 ↓
ATTACK CASES
 ↓
OBSERVED RESULT
 ↓
PASS / FAIL
```

An invariant is not considered enforced merely because it exists in documentation.

---

# 56. Enforcement Evidence

For consequential enforcement decisions, preserve:

```text
request
applicable constraints
policy versions
evaluation result
authority context
lifecycle state
exceptions
evidence
final decision
```

This creates a reconstructable enforcement record.

---

# 57. Constraint Monitoring

Operational monitoring may measure:

```text
constraint evaluations
constraint failures
policy conflicts
exceptions
bypass attempts
invariant failures
stale-policy rejections
```

Metrics are diagnostic and do not replace provenance.

---

# 58. Constraint Security Boundary

The policy engine itself becomes a security-critical component.

It must protect against:

```text
policy tampering
constraint deletion
scope expansion
priority manipulation
exception forgery
version rollback
cache poisoning
```

---

# 59. Policy Rollback

Rollback must be explicit.

A rollback must preserve:

```text
previous version
rolled-back version
reason
issuer
authority
timestamp
```

It must not erase the historical policy version.

---

# 60. Policy Activation

A policy should not become active merely because it exists.

Activation should require:

```text
schema validity
authority
lifecycle eligibility
provenance
effective time
```

where applicable.

---

# 61. Policy Deactivation

Deactivation must also be governed.

Historical decisions must remain linked to the policy version that was active at decision time.

---

# 62. Policy Composition Example

Conceptually:

```text
SECURITY POLICY
+
PRODUCT POLICY
+
DOMAIN CONSTRAINT
+
OBJECT CONSTRAINT
+
AGENT CONSTRAINT
```

produces an effective constraint set.

The result must preserve the origin of each applicable rule.

---

# 63. Constraint Contract

Conceptually:

```yaml
constraint:
  constraint_id: CON-...
  version: 1.0.0

  type: PROHIBITION

  scope:
    domain: ...
    object_types: []
    operations: []

  rule:
    condition: ...

  enforcement_mode: BLOCK

  severity: HIGH

  overridable: false

  valid_from: ...
  valid_until: ...

  provenance_ref: ...
```

This is conceptual, not final JSON Schema.

---

# 64. Policy Contract

```yaml
policy:
  policy_id: POL-...
  version: 1.0.0

  scope: ...

  constraints:
    - constraint_id: CON-...

  precedence: ...

  status: ACTIVE

  effective_from: ...

  provenance_ref: ...
```

---

# 65. Exception Contract

```yaml
exception:
  exception_id: EXC-...
  constraint_ref: CON-...
  scope: ...
  reason: ...
  issued_by: ...
  authority_ref: AUTH-...
  valid_from: ...
  valid_until: ...
  conditions: []
  provenance_ref: ...
```

---

# 66. Enforcement Decision Contract

```yaml
enforcement_decision:
  decision_id: CDE-...

  target:
    object_id: IO-...
    version: ...

  request: ...

  applicable_constraints:
    - CON-...

  policy_refs:
    - POL-...

  exception_refs: []

  result: ALLOW

  failures: []
  conflicts: []

  evaluated_at: ...

  provenance_ref: ...
```

---

# 67. Enforcement Pipeline

The canonical enforcement path is:

```text
REQUEST
 ↓
RESOLVE CONTEXT
 ↓
RESOLVE APPLICABLE POLICIES
 ↓
RESOLVE APPLICABLE CONSTRAINTS
 ↓
CHECK NON-OVERRIDABLE INVARIANTS
 ↓
EVALUATE BINDING CONSTRAINTS
 ↓
RESOLVE AUTHORIZED EXCEPTIONS
 ↓
RESOLVE CONFLICTS
 ↓
ALLOW / DENY / ESCALATE
 ↓
RECORD PROVENANCE
```

---

# 68. Integration with the Intelligence Runtime

The runtime must not execute a consequential action before the applicable enforcement result is available.

Conceptually:

```text
AGENT REQUEST
 ↓
AUTHORITY
 ↓
LIFECYCLE
 ↓
CONSTRAINT / POLICY
 ↓
EXECUTION
```

The exact order may be optimized, but no optimization may bypass a required semantic check.

---

# 69. Integration with Self-Critique

Self-critique may identify:

```text
constraint violation
policy conflict
missing requirement
```

but the critique itself does not modify the constraint system.

It produces evidence for evaluation or escalation.

---

# 70. Integration with Adversarial Verification

The adversarial verifier should explicitly attack the enforcement boundary.

Examples:

```text
attempt unauthorized action
attempt policy bypass
attempt exception escalation
attempt stale policy replay
attempt invariant violation
```

The resulting attack record belongs in provenance.

---

# 71. Constraint Invariants

### Invariant 1

Constraints have explicit identity.

### Invariant 2

Constraints are versioned.

### Invariant 3

Constraints are scoped.

### Invariant 4

Recommendations are distinct from binding constraints.

### Invariant 5

Binding constraints are distinct from non-overridable invariants.

### Invariant 6

Non-overridable invariants cannot be bypassed through ordinary authority.

### Invariant 7

Constraint applicability is explicitly resolved.

### Invariant 8

Policy composition is explicit.

### Invariant 9

Conflicts are explicitly resolved.

### Invariant 10

Unresolved critical conflicts do not default to permissive execution.

### Invariant 11

Exceptions are scoped and authorized.

### Invariant 12

Exceptions do not delete the underlying constraint.

### Invariant 13

Emergency mode does not automatically disable constraints.

### Invariant 14

Authority does not override binding constraints unless an explicit exception contract permits it.

### Invariant 15

Lifecycle restrictions remain enforceable.

### Invariant 16

Constraint evaluation is distinct from authority evaluation.

### Invariant 17

Constraint results are provenance-traceable.

### Invariant 18

Historical constraint versions remain reconstructable.

### Invariant 19

Policy changes do not silently rewrite historical decisions.

### Invariant 20

Stale cached decisions cannot silently authorize execution.

### Invariant 21

Untrusted content cannot create policy or constraints.

### Invariant 22

Agent outputs cannot silently become control-plane policy.

### Invariant 23

Invariant enforcement must be empirically tested.

### Invariant 24

Implementation must not invent constraint semantics.

---

# 72. Required Tests

The reference implementation must test:

```text
constraint identity
scope matching
scope mismatch
constraint version
policy composition
policy conflict
non-overridable invariant
hard constraint
soft constraint
recommendation deviation
exception authorization
expired exception
exception scope escalation
emergency mode
authority interaction
lifecycle interaction
stale cached decision
policy rollback
policy activation
policy deactivation
policy injection
constraint injection
```

---

# 73. Falsification Cases

Deliberately attempt:

```text
bypass hard constraint
bypass invariant with authority
forge exception
expand exception scope
reuse expired exception
reuse stale policy result
inject policy through payload
inject constraint through agent output
change policy without lifecycle
delete historical policy version
resolve conflict permissively
disable enforcement during emergency
```

---

# 74. Enforcement Benchmark

A core benchmark should measure:

```text
constraint detection
constraint enforcement
false blocking
false allowing
conflict detection
exception correctness
stale-policy rejection
invariant protection
policy-injection resistance
```

Do not compress these into one score without preserving the individual dimensions.

---

# 75. Deferred Decisions

III-006 intentionally does not freeze:

- exact policy engine;
- exact rule language;
- policy storage;
- constraint database;
- precedence algorithm where semantics permit alternatives;
- exact severity taxonomy;
- exact exception workflow;
- emergency governance implementation;
- cache technology;
- enforcement API;
- policy compilation technology;
- final constraint registry syntax.

These remain engineering decisions unless they change semantic meaning.

---

# 76. Exit Criteria

- [x] Constraint identity defined
- [x] Constraint version defined
- [x] Constraint types defined
- [x] Recommendation boundary defined
- [x] Binding constraint boundary defined
- [x] Prohibition defined
- [x] Requirement defined
- [x] Preconditions defined
- [x] Limits defined
- [x] Invariants defined
- [x] Non-overridable invariant defined
- [x] Scope defined
- [x] Applicability defined
- [x] Policy defined
- [x] Policy composition defined
- [x] Conflict handling defined
- [x] Deny-safe behavior defined
- [x] Violation defined
- [x] Enforcement modes defined
- [x] Hard/soft distinction defined
- [x] Exceptions defined
- [x] Emergency boundary defined
- [x] Authority interaction defined
- [x] Lifecycle interaction defined
- [x] Provenance integration defined
- [x] Injection boundaries defined
- [x] Temporal applicability defined
- [x] Caching boundary defined
- [x] Invariant verification defined
- [x] Enforcement evidence defined
- [x] Self-critique integration defined
- [x] Adversarial verification integration defined
- [x] Constraint invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Enforcement benchmark defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 77. Next Contract

**III-007 — Memory, Context & Knowledge State Contract**

III-007 will define the machine-readable contract for information available to agents and the runtime, including:

```text
memory identity
context identity
knowledge objects
freshness
scope
retrieval
source authority
provenance
staleness
conflict
versioning
working context
long-term context
ephemeral context
context isolation
memory mutation
knowledge invalidation
retrieval trust
```

The central requirement remains:

```text
AVAILABLE INFORMATION
≠
TRUSTED INFORMATION
≠
AUTHORITATIVE INFORMATION
```
