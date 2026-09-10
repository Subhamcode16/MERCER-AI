# III-001 — Global Intelligence Object Schema & Identifier Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** II-001 through II-017, II-RAT-001 through II-RAT-003  
**Purpose:** Define the canonical machine-readable identity, envelope, metadata, provenance hooks, lifecycle hooks, and type-discrimination contract for all Intelligence Objects.

---

## 1. Purpose

Phase II established the semantic architecture.

Phase III now begins the translation:

```text
FROZEN SEMANTIC CONTRACT
        ↓
MACHINE-READABLE CONTRACT
        ↓
REFERENCE IMPLEMENTATION
```

III-001 establishes the common contract shared by Intelligence Objects.

It does **not** define every domain-specific object.

Instead, it defines the common structural layer that allows all object types to participate in:

```text
authority
lifecycle
runtime
provenance
validation
evaluation
self-critique
adversarial verification
recovery
```

---

## 2. Core Principle

> **An Intelligence Object must be identifiable, versioned, typed, attributable, lifecycle-aware, provenance-aware, and independently referenceable before it can safely participate in the Intelligence Runtime.**

The canonical identity context is:

```text
OBJECT ID
+
OBJECT TYPE
+
OBJECT VERSION
+
OBJECT STATE
+
AUTHORITY CONTEXT
+
PROVENANCE CONTEXT
```

---

## 3. Object Identity

Every Intelligence Object receives a globally unique identifier.

Recommended format:

```text
IO-<ULID>
```

Example:

```text
IO-01J8X7K9Q3M4A6T2N5R8W1ZC7P
```

The exact identifier-generation library remains an implementation decision.

Mandatory properties:

```text
globally unique
stable
non-semantic
non-reusable
sortable where supported
```

The identifier must not encode business meaning.

Do not create IDs such as:

```text
APPAREL-LINEN-DRESS-001
```

because semantic meaning embedded in identifiers creates coupling.

---

## 4. Identity Immutability

Once assigned:

```text
object_id
```

must never change.

A revised object is represented by a new version or new object according to the lifecycle contract.

Never mutate `object_id` to represent semantic revision.

---

## 5. Object Type

Every object must declare:

```text
object_type
```

Examples may include:

```text
intent
knowledge
evidence
authority
constraint
strategy
narrative
asset
channel_projection
evaluation
critique
attack
recovery_plan
experiment
architectural_claim
```

The definitive registry of types must be compiled from the ratified semantic specifications.

III-001 does not authorize arbitrary new semantic types.

---

## 6. Type Discrimination

An object must be unambiguously distinguishable by:

```text
object_type
```

A consumer must not infer type from arbitrary fields.

Bad:

```text
if object contains "lighting":
    treat as asset strategy
```

Correct:

```text
object_type = "asset_strategy"
```

---

## 7. Object Version

Every object must have a version.

Recommended structure:

```text
version:
  major
  minor
  patch
```

Example:

```text
1.2.0
```

The exact versioning semantics must follow the lifecycle and change-control contracts.

The runtime must distinguish:

```text
object identity
```

from:

```text
object version
```

---

## 8. Schema Version

Every serialized object must identify:

```text
schema_version
```

This distinguishes:

```text
OBJECT VERSION
```

from:

```text
SCHEMA VERSION
```

They must never be conflated.

Example:

```text
object.version = 2.1.0
schema_version = 1.0
```

---

## 9. Common Object Envelope

All Intelligence Objects should share a common envelope.

Conceptually:

```yaml
object:
  object_id: ...
  object_type: ...
  version: ...
  schema_version: ...
  lifecycle_state: ...
  created_at: ...
  updated_at: ...
  created_by: ...
  authority_context: ...
  provenance_context: ...
  payload: ...
```

This is a conceptual contract, not yet a final JSON Schema.

---

## 10. Lifecycle Hook

Every object exposes:

```text
lifecycle_state
```

The field references the canonical lifecycle contract defined by II-014.

III-001 does not redefine the lifecycle graph.

The runtime must validate lifecycle transitions through III-003.

---

## 11. Authority Hook

Every object preserves an explicit reference to its applicable authority context.

Conceptually:

```yaml
authority_context:
  authority_id: ...
  scope: ...
  decision_type: ...
```

The exact authority schema is deferred to:

```text
III-002 — Authority Schema
```

III-001 establishes the reference boundary without redefining authority semantics.

---

## 12. Provenance Hook

Every object preserves a provenance reference.

Conceptually:

```yaml
provenance_context:
  provenance_id: ...
```

The complete provenance event model is deferred to:

```text
III-004 — Provenance Schema
```

No object may silently lose its origin merely because it is transformed.

---

## 13. Timestamps

Objects should preserve:

```text
created_at
updated_at
```

using a canonical timezone-independent representation.

The runtime must distinguish:

```text
creation time
modification time
execution time
evaluation time
```

These timestamps must not be substituted for one another.

---

## 14. Creator / Producer

Every object must identify its producer:

```text
created_by
```

The producer may represent:

```text
human
agent
runtime
external system
import process
```

The identity must be traceable through authority and provenance contracts.

---

## 15. Producer Does Not Imply Authority

The field:

```text
created_by
```

must never be interpreted as:

```text
authorized_by
```

A producer can create a proposed object without possessing authority to approve it.

Therefore:

```text
CREATED_BY
≠
AUTHORIZED_BY
```

---

## 16. Payload

Domain-specific semantic information resides in:

```text
payload
```

The payload schema is determined by:

```text
object_type
+
object-specific contract
```

III-001 must not flatten all domain semantics into the common envelope.

---

## 17. Envelope / Payload Separation

The common envelope handles:

```text
identity
version
state
authority reference
provenance reference
timestamps
producer
schema
```

The payload handles:

```text
domain-specific meaning
```

This prevents runtime infrastructure from becoming coupled to domain-specific semantics.

---

## 18. Object References

Objects may reference other objects through:

```text
object_id
+
version
```

Example:

```yaml
reference:
  object_id: IO-...
  version: 1.2.0
```

A reference should not rely on mutable labels.

---

## 19. Reference Integrity

A reference is valid only if:

```text
object exists
+
referenced version exists
+
reference is permitted
+
referenced object is consumable under lifecycle rules
+
authority permits the relationship
```

The runtime must not assume that an existing ID implies valid consumption.

---

## 20. Reference Relationships

Where semantics require distinction, references may declare relationships such as:

```text
depends_on
derived_from
supports
contradicts
evaluates
critiques
attacks
supersedes
recovers
projects_to
```

The definitive relationship vocabulary must come from the existing semantic specifications.

Do not introduce relationship semantics merely for convenience.

---

## 21. Object Graph vs Execution DAG

Intelligence Objects form a semantic graph:

```text
OBJECT
 ↓
REFERENCES
 ↓
OTHER OBJECTS
```

The graph may contain semantic relationships.

It is distinct from the execution dependency graph.

Therefore:

```text
OBJECT GRAPH
≠
EXECUTION DAG
```

A semantic relationship cycle does not automatically imply an executable cycle.

---

## 22. Object Integrity

A committed object should have an integrity representation.

Conceptually:

```yaml
integrity:
  content_hash: ...
```

The exact hashing mechanism is deferred.

The purpose is to detect unintended modification.

---

## 23. Hash Semantics

The content hash must be derived from a canonical representation.

The implementation must define:

```text
canonical serialization
```

before using hashes for equality or integrity.

Do not hash arbitrary serialization order.

---

## 24. Equality

The system must distinguish:

```text
IDENTITY EQUALITY
SEMANTIC EQUALITY
REPRESENTATIONAL EQUALITY
```

For example:

```text
same object_id
```

does not necessarily mean:

```text
same version
```

and:

```text
same payload
```

does not necessarily mean:

```text
same authority context
```

---

## 25. Status Separation

Do not add a generic:

```text
status
```

field that collapses multiple semantic dimensions.

Where required, preserve distinct concepts such as:

```text
lifecycle_state
evaluation_state
execution_state
```

Thus:

```text
evaluation PASS
```

does not automatically become:

```text
lifecycle APPROVED
```

without an authorized transition.

---

## 26. Locking

If an object enters a lifecycle state that forbids mutation, the runtime must enforce that restriction.

III-001 exposes:

```text
lifecycle_state
```

but III-003 owns the actual mutation rules.

III-001 must not create a second locking mechanism.

---

## 27. Deletion

Deletion semantics must not be inferred from absence.

For auditable objects, prefer explicit lifecycle semantics such as:

```text
RETIRED
ARCHIVED
INVALIDATED
```

rather than silently deleting the record.

Exact deletion policy is deferred to lifecycle and persistence implementation.

---

## 28. Construction

Object construction should follow:

```text
CREATE
 ↓
SCHEMA VALIDATE
 ↓
IDENTITY ASSIGN
 ↓
PROVENANCE RECORD
 ↓
AUTHORITY CONTEXT RESOLVE
 ↓
LIFECYCLE INITIALIZATION
 ↓
COMMIT
```

The exact ordering may vary where technically necessary, but no object should become consumable before required validation and provenance obligations are satisfied.

---

## 29. Mutation

For committed objects:

```text
MUTATION
```

should generally become:

```text
NEW VERSION
```

The implementation must not silently mutate historical state.

---

## 30. Derived Objects

When an object is derived from another object, preserve:

```text
derived_from
```

with the exact source version where deterministic lineage is required.

Example:

```text
Object A v1.0
      ↓
Object B v1.0
```

---

## 31. Supersession

If a new version supersedes an old version, preserve:

```text
NEW
 ↓
supersedes
 ↓
OLD
```

The old object remains historically traceable.

---

## 32. Invalidated Objects

An invalidated object remains identifiable.

Consumers must resolve whether it is still permitted for their intended operation.

Therefore:

```text
OBJECT EXISTS
≠
OBJECT IS CONSUMABLE
```

---

## 33. Archived Objects

Archived objects may remain available for:

```text
historical analysis
provenance
audit
reconstruction
benchmarking
```

but must not automatically remain eligible for active decision-making.

---

## 34. Validation Hooks

Objects may reference validation/evaluation records.

Conceptually:

```yaml
validation:
  evaluation_ids:
    - ...
```

The presence of an evaluation record does not automatically imply approval.

Approval remains a governed lifecycle transition.

---

## 35. Critique Hooks

An object may reference critiques:

```yaml
critique_refs:
  - ...
```

A critique reference does not mutate the object and does not itself establish correctness.

---

## 36. Attack Hooks

An object may reference adversarial verification records:

```yaml
attack_refs:
  - ...
```

Attack records remain separately auditable.

---

## 37. Experiment Hooks

Architectural or benchmark objects may reference experiments:

```yaml
experiment_refs:
  - ...
```

This allows:

```text
claim
→ experiment
→ result
→ evidence
```

to remain traceable.

---

## 38. Error Representation

Object-level errors should be structured rather than stored only as strings.

Conceptually:

```yaml
error:
  code: ...
  severity: ...
  message: ...
  source: ...
  recoverable: ...
```

The definitive error taxonomy remains a Phase III implementation contract.

---

## 39. Uncertainty

Where semantic contracts require uncertainty, it must remain explicit.

Do not encode uncertainty merely through:

```text
null
empty string
missing field
```

unless the specific schema defines that meaning.

Exact uncertainty semantics remain deferred.

---

## 40. Unknown Fields

The implementation must establish a policy for unknown fields.

For critical contracts, strict rejection is preferable during early development because silently accepting unknown semantics can hide version incompatibilities.

The exact compatibility policy remains deferred.

---

## 41. Serialization

III-001 is serialization-neutral.

Possible implementation formats include:

```text
JSON
YAML
database records
event envelopes
```

The canonical representation must eventually be deterministic enough for:

```text
validation
hashing
provenance
replay
```

---

## 42. Canonical Envelope — Conceptual Form

```yaml
object:
  object_id: IO-...
  object_type: ...
  version:
    major: 1
    minor: 0
    patch: 0

  schema_version: 1.0

  lifecycle_state: ...

  created_at: ...
  updated_at: ...

  created_by:
    actor_type: ...
    actor_id: ...

  authority_context:
    authority_id: ...
    scope: ...

  provenance_context:
    provenance_id: ...

  integrity:
    content_hash: ...

  payload: {}

  references: []

  evaluation_refs: []

  critique_refs: []

  attack_refs: []

  experiment_refs: []
```

This is a conceptual contract, not yet a final JSON Schema.

---

## 43. Field Classification

### Required

```text
object_id
object_type
version
schema_version
lifecycle_state
created_at
created_by
payload
```

### Conditionally Required

```text
authority_context
provenance_context
integrity
references
```

depending on object type and lifecycle state.

### Optional

```text
evaluation_refs
critique_refs
attack_refs
experiment_refs
updated_at
```

where applicable.

The exact conditional requirements must be finalized during schema compilation.

---

## 44. Object-Type Registry

Phase III must create a registry:

```text
OBJECT TYPE
→ SCHEMA
→ VERSION
→ LIFECYCLE RULES
→ AUTHORITY RULES
→ PROVENANCE REQUIREMENTS
→ CONSUMPTION RULES
```

This becomes the bridge between generic runtime infrastructure and domain-specific semantics.

---

## 45. Contract Resolution

At runtime:

```text
object_id
 ↓
object_type
 ↓
schema resolution
 ↓
schema validation
 ↓
lifecycle resolution
 ↓
authority resolution
 ↓
provenance resolution
 ↓
consumption decision
```

The runtime must not infer the contract from payload shape.

---

## 46. Schema Evolution

Schema evolution must distinguish:

```text
schema change
```

from:

```text
object semantic revision
```

If a schema change alters semantic meaning, it requires the explicit architecture change process.

---

## 47. Compatibility

Compatibility should not be assumed.

For each schema revision determine:

```text
READ OLD?
WRITE OLD?
MIGRATE OLD?
REJECT OLD?
```

The exact compatibility matrix belongs to implementation.

---

## 48. Migration

Migration must preserve:

```text
object identity
historical versions
provenance
authority history
lifecycle history
```

unless an explicit semantic migration requires otherwise.

---

## 49. Security Boundary

Serialized fields are not inherently trustworthy.

Inputs may be:

```text
agent-generated
user-generated
external
imported
retrieved
adversarial
```

All must pass applicable validation and authority checks.

---

## 50. Prompt Injection Boundary

Payloads may contain arbitrary textual content.

Therefore:

```text
payload content
≠
runtime instruction
```

An object must not become an executable instruction merely because a field contains imperative language.

Execution authority comes from the runtime contract.

---

## 51. Object Consumption

A consumer must resolve:

```text
object identity
object version
schema
lifecycle
authority
provenance
```

before treating an object as valid input.

Conceptually:

```text
LOAD
 ↓
RESOLVE
 ↓
VALIDATE
 ↓
AUTHORIZE
 ↓
CONSUME
```

---

## 52. Consumption Failure

If any mandatory condition fails:

```text
DO NOT CONSUME
```

The system should produce a structured failure or escalation rather than silently degrading into an assumed interpretation.

---

## 53. Audit and Immutability

Historical objects must remain reconstructable.

The implementation should preserve:

```text
previous version
new version
change reason
producer
authority
timestamp
provenance
```

---

## 54. Object Contract Invariants

1. Every object has a globally unique identity.
2. Object identity does not encode semantic meaning.
3. Committed versions are immutable.
4. Object type is explicit.
5. Schema version and object version remain distinct.
6. Lifecycle state is explicit.
7. Authority is referenced explicitly and remains scoped.
8. Producer identity does not imply authority.
9. Provenance is preserved.
10. Object references resolve to explicit versions where deterministic lineage is required.
11. Object existence does not imply consumability.
12. Evaluation status does not silently become lifecycle approval.
13. Critique records do not silently mutate the target.
14. Adversarial records do not silently mutate production state.
15. Semantic object graphs are distinct from execution DAGs.
16. Canonical serialization is required before integrity hashing.
17. Unknown semantic fields cannot be silently trusted.
18. Payload text cannot automatically become runtime instruction.
19. Historical versions remain traceable.
20. Implementation must not invent missing semantic contracts.

---

## 55. Phase III Implementation Contract

The engineer must implement the common object envelope before domain-specific object behavior.

Recommended order:

```text
GLOBAL IDENTIFIER
        ↓
COMMON OBJECT ENVELOPE
        ↓
OBJECT TYPE REGISTRY
        ↓
SCHEMA RESOLUTION
        ↓
LIFECYCLE HOOK
        ↓
AUTHORITY HOOK
        ↓
PROVENANCE HOOK
        ↓
REFERENCE RESOLUTION
        ↓
CONSUMPTION VALIDATION
```

---

## 56. Required Tests

Before downstream agents depend on the object system, test:

```text
duplicate identity
identity mutation
version mutation
type ambiguity
schema mismatch
invalid lifecycle state
unauthorized consumption
missing provenance
invalid reference
stale reference
supersession
invalidated object consumption
unknown field handling
hash instability
payload instruction injection
reference cycle
```

---

## 57. Falsification Cases

Deliberately attack the object contract with:

```text
same ID / different payload
same ID / different version
fake authority reference
fake provenance reference
stale object
invalid state
unknown object type
schema downgrade
payload prompt injection
reference cycle
missing source version
forged evaluation PASS
```

The implementation passes only if these cases are rejected, quarantined, or explicitly escalated according to the applicable contract.

---

## 58. Deferred Decisions

III-001 intentionally does not freeze:

- exact ULID/UUID implementation;
- final serialization format;
- exact JSON Schema syntax;
- schema registry technology;
- database representation;
- content hashing algorithm;
- error-code taxonomy;
- uncertainty representation;
- unknown-field compatibility policy;
- migration tooling;
- persistence implementation;
- exact object-type registry contents beyond ratified semantic types.

These remain engineering decisions unless they alter semantic meaning.

---

## 59. Exit Criteria

- [x] Global object identity defined
- [x] Identity immutability defined
- [x] Object type boundary defined
- [x] Version semantics defined
- [x] Schema version boundary defined
- [x] Common envelope defined
- [x] Lifecycle hook defined
- [x] Authority hook defined
- [x] Provenance hook defined
- [x] Producer boundary defined
- [x] Payload separation defined
- [x] Reference model defined
- [x] Object graph distinction defined
- [x] Integrity boundary defined
- [x] Evaluation/lifecycle separation defined
- [x] Critique/attack hooks defined
- [x] Schema evolution boundary defined
- [x] Consumption validation defined
- [x] Security boundary defined
- [x] Object invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation. Semantic ratification is not required again unless implementation exposes a genuine semantic contradiction.

---

## 60. Next Contract

**III-002 — Authority Schema & Delegation Contract**

III-002 will compile the ratified authority model into a machine-readable representation covering:

```text
authority identity
scope
decision type
delegation
expiration
revocation
conflict
override
human authority
agent authority
cross-domain authority
authority verification
```

The implementation must continue to preserve the central boundary:

```text
CAPABILITY
≠
AUTHORITY
```
