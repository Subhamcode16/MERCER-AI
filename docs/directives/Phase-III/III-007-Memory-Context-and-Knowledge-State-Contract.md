# III-007 — Memory, Context & Knowledge State Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001 through III-006 and the ratified Phase II semantic architecture  
**Purpose:** Define the machine-readable contract for memory, context, and knowledge state, including identity, scope, freshness, provenance, authority, retrieval, staleness, conflict, versioning, isolation, mutation, invalidation, and trust.

---

# 1. Purpose

III-007 defines how information becomes available to the Intelligence Runtime without being automatically treated as trusted or authoritative.

The central boundary is:

```text
AVAILABLE INFORMATION
        ≠
TRUSTED INFORMATION
        ≠
AUTHORITATIVE INFORMATION
```

Memory and knowledge are therefore treated as governed information objects and contextual resources rather than as an undifferentiated prompt or storage layer.

The contract answers:

```text
WHAT INFORMATION IS AVAILABLE?
WHERE DID IT COME FROM?
WHICH VERSION IS IT?
HOW FRESH IS IT?
WHAT SCOPE DOES IT HAVE?
CAN THIS AGENT USE IT?
IS IT TRUSTED?
IS IT AUTHORITATIVE?
CAN IT BE MUTATED?
WHEN MUST IT BE INVALIDATED?
```

---

# 2. Memory Is Not Truth

The presence of information in memory does not establish:

```text
correctness
authority
freshness
relevance
```

Memory is a representation of information that was stored or retrieved under some prior process.

Therefore:

```text
MEMORY EXISTS
≠
MEMORY IS TRUE
```

---

# 3. Knowledge State

Knowledge state represents the system's current structured representation of information relevant to a domain, task, object, or decision.

It may contain:

```text
facts
claims
evidence
relationships
constraints
observations
derived information
uncertainties
```

Knowledge state must preserve provenance and version context.

---

# 4. Memory Types

The architecture should distinguish at least:

```text
EPHEMERAL CONTEXT
WORKING MEMORY
LONG-TERM MEMORY
KNOWLEDGE STATE
EVIDENCE STORE
```

These are semantically different and must not be collapsed into one generic memory bucket.

---

# 5. Ephemeral Context

Ephemeral context exists for a limited execution or interaction.

Examples:

```text
current request
temporary tool result
current reasoning context
short-lived execution metadata
```

Ephemeral context should normally have bounded lifetime.

---

# 6. Working Memory

Working memory contains information actively used during a task.

It may include:

```text
intermediate objects
retrieved evidence
temporary plans
active constraints
task-specific state
```

Working memory must remain scoped to its task or execution context.

---

# 7. Long-Term Memory

Long-term memory contains information retained across executions.

Examples:

```text
stable preferences
historical decisions
persistent knowledge
validated prior outputs
```

Retention does not imply perpetual validity.

Long-term memory must remain versioned and subject to invalidation.

---

# 8. Knowledge State vs Memory

Memory may contain raw or historical information.

Knowledge state represents information that has been structured for use.

Therefore:

```text
MEMORY
→ stored information

KNOWLEDGE STATE
→ structured information available for reasoning / decision support
```

Knowledge state must preserve the provenance of the information from which it was derived.

---

# 9. Memory Identity

Every persistent memory record should have a stable identity.

Recommended conceptual form:

```text
MEM-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

---

# 10. Context Identity

Each consequential execution context should have an explicit identity.

Recommended conceptual form:

```text
CTX-<ULID>
```

Context identity allows the runtime to determine:

```text
which information was available
during which execution
under which authority
```

---

# 11. Knowledge Object Identity

Structured knowledge should use the common Intelligence Object contract from III-001.

Therefore:

```text
knowledge
→ object_id
→ object_type
→ version
→ lifecycle
→ authority context
→ provenance
```

Knowledge must not create a parallel identity system where an Intelligence Object already applies.

---

# 12. Memory Scope

Every memory item must have explicit scope where relevant.

Possible dimensions:

```text
user / principal
agent
task
project
domain
campaign
environment
organization
global
```

A memory item scoped to one context must not silently leak into another.

---

# 13. Context Isolation

Context isolation is a security and correctness boundary.

The runtime must prevent accidental transfer of:

```text
authority
sensitive data
stale assumptions
task-specific constraints
private memory
```

between unrelated contexts.

---

# 14. Context Composition

Context should be assembled explicitly.

Conceptually:

```text
REQUEST
+
AUTHORIZED MEMORY
+
RELEVANT KNOWLEDGE
+
CURRENT EVIDENCE
+
ACTIVE CONSTRAINTS
=
EXECUTION CONTEXT
```

The runtime must not indiscriminately inject all available memory.

---

# 15. Retrieval

Retrieval is the process of selecting information for a context.

A retrieval result should preserve:

```text
source
object / memory identity
version
retrieval time
retrieval method
scope
provenance
```

Retrieval does not establish truth.

---

# 16. Retrieval Result

Conceptually:

```yaml
retrieval_result:
  retrieval_id: RET-...
  context_id: CTX-...
  source_refs: []
  retrieved_at: ...
  method: ...
  query_ref: ...
  provenance_ref: ...
```

---

# 17. Retrieval Authority

Access to memory or knowledge must be governed by authority.

Therefore:

```text
RETRIEVABLE
≠
AUTHORIZED TO USE
```

The runtime must resolve the applicable authority before exposing protected information.

---

# 18. Retrieval Relevance

Relevance is distinct from authority.

A memory item can be:

```text
highly relevant
```

while still being:

```text
unauthorized
```

or:

```text
stale
```

---

# 19. Retrieval Trust

Retrieval systems should preserve trust metadata where applicable.

Possible classifications:

```text
VERIFIED
SUPPORTED
UNVERIFIED
CONFLICTED
STALE
UNKNOWN
```

The exact epistemic taxonomy must remain compatible with the evaluation contract.

---

# 20. Source Authority

The authority of a source must not be inferred solely from retrieval ranking.

For example:

```text
top-ranked result
≠
authoritative source
```

Source authority comes from explicit authority / evidence semantics.

---

# 21. Freshness

Information may become stale over time.

Freshness should be represented explicitly where time matters.

Conceptually:

```yaml
freshness:
  observed_at: ...
  valid_from: ...
  valid_until: ...
  freshness_class: ...
```

Exact freshness policy is domain-specific.

---

# 22. Staleness

Staleness does not automatically mean falsehood.

It means the information may no longer be sufficiently current for a particular use.

Therefore:

```text
STALE
≠
FALSE
```

The consuming contract determines whether stale information is acceptable.

---

# 23. Freshness by Use Case

The same information may be:

```text
fresh enough for historical analysis
```

but:

```text
too stale for real-time execution
```

Freshness must therefore be evaluated relative to the intended operation.

---

# 24. Expiration

Where information has an explicit validity period:

```text
valid_until
```

must be enforced.

Expired information should not silently remain active evidence.

---

# 25. Memory Versioning

Persistent memory must be versioned where mutation affects semantic meaning.

Prefer:

```text
MEM v1
 ↓
MEM v2
```

rather than silently rewriting historical memory.

---

# 26. Memory Mutation

Memory mutation must be governed.

A memory write should specify:

```text
writer
authority
source
reason
new version
provenance
```

---

# 27. Memory Write Authority

Agents must not write persistent memory merely because they can generate text.

Persistent memory mutation requires explicit authority.

Therefore:

```text
CAN_GENERATE
≠
MAY_PERSIST
```

---

# 28. Memory Write Validation

Before committing persistent memory, the runtime should evaluate:

```text
schema
scope
authority
provenance
sensitivity
conflict
freshness
retention
```

where applicable.

---

# 29. Memory Poisoning Boundary

Retrieved or generated information may be malicious or incorrect.

The runtime must protect against:

```text
false memory insertion
authority spoofing
instruction injection
malicious preference injection
stale information persistence
cross-context contamination
```

---

# 30. Memory as Data

Stored memory must not automatically become executable instruction.

Therefore:

```text
MEMORY CONTENT
≠
RUNTIME CONTROL
```

A memory item containing:

```text
"ignore all system constraints"
```

remains content unless a trusted control-plane process explicitly interprets it as policy.

---

# 31. Knowledge Ingestion

External information entering knowledge state should pass through:

```text
INGEST
 ↓
IDENTIFY
 ↓
VALIDATE
 ↓
PROVENANCE
 ↓
AUTHORITY / SOURCE ASSESSMENT
 ↓
STORE
 ↓
MAKE AVAILABLE
```

Ingestion does not automatically mean acceptance.

---

# 32. Knowledge Validation

Knowledge validation may evaluate:

```text
schema
source
provenance
consistency
evidence
freshness
authority
```

The exact validation policy is defined by downstream evaluation contracts.

---

# 33. Knowledge Derivation

Derived knowledge must preserve lineage.

Example:

```text
SOURCE A
+
SOURCE B
 ↓
DERIVATION
 ↓
KNOWLEDGE K
```

The knowledge object must retain references to the contributing versions.

---

# 34. Knowledge Conflict

Knowledge sources may disagree.

The runtime must represent:

```text
CONFLICT
```

explicitly rather than silently selecting one source.

Conceptually:

```yaml
knowledge_conflict:
  conflict_id: ...
  subject: ...
  competing_refs: []
  detected_at: ...
  resolution_state: UNRESOLVED
```

---

# 35. Conflict Resolution

Conflict resolution may use:

```text
source authority
evidence quality
freshness
scope
domain rules
explicit adjudication
```

The runtime must not resolve conflicts solely through:

```text
retrieval rank
model confidence
creation timestamp
```

unless explicitly defined.

---

# 36. Unresolved Conflict

If a consequential decision depends on unresolved conflicting knowledge:

```text
DO NOT PRETEND CONSENSUS
```

The system should:

```text
abstain
escalate
request additional evidence
```

according to the applicable contract.

---

# 37. Knowledge Supersession

New knowledge may supersede older knowledge.

Supersession must preserve:

```text
old version
new version
reason
evidence
authority
timestamp
```

Historical knowledge remains reconstructable.

---

# 38. Knowledge Invalidation

Knowledge may be invalidated because of:

```text
source correction
contradictory authoritative evidence
provenance failure
schema failure
adversarial discovery
expiration
policy change
```

Invalidation must be explicit.

---

# 39. Memory Deletion

Deletion should not be used to erase historical reasoning where auditability is required.

Where appropriate, use:

```text
RETIRED
INVALIDATED
ARCHIVED
```

and apply the applicable retention policy.

---

# 40. Memory Access Control

Access should be resolved through:

```text
requesting subject
memory scope
authority
purpose / operation
sensitivity
```

A memory item must not become globally visible merely because one agent can access it.

---

# 41. Context Authority

Context itself does not create authority.

An agent receiving an object in context must still resolve whether it is authorized to:

```text
read
use
transform
act upon
publish
```

that information.

---

# 42. Context Freshness

The runtime should track the freshness of context where consequential actions depend on current information.

A context snapshot should be identifiable:

```text
CTX-...
```

and reconstructable.

---

# 43. Context Snapshot

A consequential execution should preserve the relevant context snapshot or deterministic references to its contents.

Conceptually:

```yaml
context_snapshot:
  context_id: CTX-...
  created_at: ...
  memory_refs: []
  knowledge_refs: []
  evidence_refs: []
  constraint_refs: []
  authority_refs: []
```

---

# 44. Context Reproducibility

For consequential executions, the system should be able to reconstruct:

```text
WHAT THE AGENT COULD SEE
```

at execution time.

This does not require storing every transient token if deterministic references can reconstruct the relevant semantic context.

---

# 45. Context Leakage

The system must detect or prevent unintended transfer of:

```text
memory
authority
constraints
instructions
sensitive evidence
```

between unrelated executions.

---

# 46. Context Contamination

Context contamination occurs when irrelevant, stale, unauthorized, or adversarial information affects a consequential operation.

The system should support detection through:

```text
provenance
scope
freshness
authority
evaluation
```

---

# 47. Retrieval Poisoning

The retrieval layer must be tested against:

```text
malicious documents
false authority claims
instruction injection
duplicate evidence
stale high-ranked results
conflicting sources
```

Retrieval ranking must not be treated as a security boundary.

---

# 48. Memory Trust Update

Trust state should be revisable when new evidence arrives.

Conceptually:

```text
MEMORY
 ↓
NEW EVIDENCE
 ↓
RE-EVALUATION
 ↓
TRUST STATE UPDATE
```

Historical trust states should remain reconstructable.

---

# 49. Knowledge Confidence

Confidence may be associated with knowledge where defined, but confidence must not substitute for:

```text
authority
provenance
evidence
freshness
```

Therefore:

```text
HIGH CONFIDENCE
≠
AUTHORITATIVE
```

---

# 50. Knowledge Claims

A knowledge claim should preserve:

```text
claim identity
claim version
source refs
evidence refs
status
scope
freshness
provenance
```

Claims should remain distinguishable from raw source material.

---

# 51. Working Context Mutation

Working context may change during an execution.

Material changes should remain traceable where they affect consequential output.

For example:

```text
context v1
 ↓
retrieval
 ↓
context v2
 ↓
decision
```

---

# 52. Context Branching

Alternative reasoning paths may create branches:

```text
CTX-A
 ├── CTX-B
 └── CTX-C
```

Branching should preserve lineage.

This is useful for:

```text
planning
counterfactuals
adversarial testing
recovery
```

---

# 53. Context Merge

Merging contexts requires explicit conflict resolution.

Do not silently merge:

```text
authority
constraints
memory
knowledge
```

from two contexts if they conflict.

---

# 54. Context Isolation in Multi-Agent Systems

Each agent should receive only the context required for its task and authority.

A shared workspace must not imply universal visibility.

Conceptually:

```text
GLOBAL KNOWLEDGE
      ↓
AUTHORIZED PROJECTION
      ↓
AGENT CONTEXT
```

---

# 55. Context Projection

A context projection is a controlled subset of available knowledge and memory.

It should preserve:

```text
source refs
versions
scope
authority
provenance
```

This enables least-context operation.

---

# 56. Least Context

Where practical, agents should receive the minimum context necessary for their assigned operation.

This reduces:

```text
context pollution
authority leakage
prompt injection surface
irrelevant reasoning
privacy exposure
```

---

# 57. Context Priority

If context items conflict in relevance, the runtime may rank them, but ranking must not silently determine truth or authority.

Therefore:

```text
CONTEXT PRIORITY
≠
TRUTH
≠
AUTHORITY
```

---

# 58. Memory Retention

Retention should be governed by:

```text
purpose
scope
sensitivity
lifecycle
legal / product policy
audit requirements
```

Exact retention duration remains implementation-specific.

---

# 59. Memory Lifecycle

Persistent memory should participate in lifecycle semantics.

Conceptually:

```text
DRAFT
 ↓
VALIDATING
 ↓
VALID
 ↓
ACTIVE
 ↓
INVALIDATED / SUPERSEDED / ARCHIVED / RETIRED
```

The final state vocabulary must remain compatible with III-003.

---

# 60. Memory Recovery

Recovery of invalidated or archived memory requires:

```text
reason
authority
current evidence
target state
provenance
```

Historical invalidation must not be erased.

---

# 61. Knowledge Rollback

Rollback should create a traceable state change.

It must preserve:

```text
previous knowledge version
rollback target
reason
authority
timestamp
```

---

# 62. Agent Memory Interaction

An agent may:

```text
READ
PROPOSE WRITE
REQUEST RETRIEVAL
REQUEST INVALIDATION
REQUEST UPDATE
```

but actual persistent mutation is governed by authority and lifecycle.

---

# 63. Self-Critique Interaction

A self-critic may examine:

```text
memory used
knowledge used
retrieval results
context assembly
```

to identify:

```text
stale information
unsupported assumptions
missing evidence
context contamination
authority confusion
```

The critique becomes an independent record.

---

# 64. Adversarial Verification Interaction

The adversarial verifier should attack the memory/context layer with:

```text
poisoned memory
stale memory
false authority metadata
cross-context leakage
retrieval injection
conflicting knowledge
context omission
context overexposure
```

The result must be recorded through provenance.

---

# 65. Memory / Knowledge Invariants

### Invariant 1

Available information is not automatically trusted information.

### Invariant 2

Trusted information is not automatically authoritative information.

### Invariant 3

Memory existence does not imply truth.

### Invariant 4

Memory is explicitly scoped.

### Invariant 5

Knowledge state preserves provenance.

### Invariant 6

Persistent memory is versioned where semantic mutation occurs.

### Invariant 7

Persistent memory mutation requires authority.

### Invariant 8

Retrieval does not establish authority.

### Invariant 9

Retrieval ranking does not establish truth.

### Invariant 10

Staleness is distinct from falsehood.

### Invariant 11

Freshness is evaluated relative to intended use.

### Invariant 12

Conflicting knowledge is represented explicitly.

### Invariant 13

Unresolved consequential conflicts trigger abstention, escalation, or additional evidence.

### Invariant 14

Historical knowledge remains reconstructable.

### Invariant 15

Memory content does not automatically become runtime instruction.

### Invariant 16

Context does not create authority.

### Invariant 17

Context isolation prevents unauthorized leakage.

### Invariant 18

Context snapshots for consequential executions are reconstructable.

### Invariant 19

Tool output does not automatically become trusted knowledge.

### Invariant 20

Agent-generated content does not automatically become persistent memory.

### Invariant 21

Knowledge confidence does not substitute for authority or provenance.

### Invariant 22

Memory invalidation is explicit.

### Invariant 23

Memory deletion does not silently erase required historical provenance.

### Invariant 24

Implementation must not invent knowledge semantics.

---

# 66. Required Tests

The reference implementation must test:

```text
memory identity
memory scope
context identity
context isolation
retrieval authorization
retrieval relevance
freshness
staleness
expiration
memory versioning
memory mutation
memory write authority
memory poisoning
knowledge ingestion
knowledge derivation
knowledge conflict
knowledge supersession
knowledge invalidation
memory deletion / archival
context snapshot
context reproducibility
context leakage
context contamination
retrieval poisoning
trust updates
context branching
context merging
least-context projection
```

---

# 67. Falsification Cases

Deliberately attempt:

```text
agent reads unauthorized memory
agent writes memory without authority
stale memory drives consequential decision
expired evidence is treated as current
retrieval rank overrides source authority
malicious document injects control instruction
memory content overrides system policy
conflicting knowledge is silently merged
historical memory version disappears
cross-agent memory leakage
context from task A appears in task B
tool result becomes trusted knowledge without validation
agent-generated claim becomes persistent memory without governance
false authority metadata enters context
```

---

# 68. Memory / Context Benchmark

A core benchmark should measure:

```text
retrieval precision
retrieval authorization correctness
stale-information detection
conflict detection
memory poisoning resistance
context isolation
context reconstruction
knowledge provenance completeness
unauthorized memory-write rejection
context contamination detection
```

These dimensions must remain separately observable.

---

# 69. Context Reconstruction Benchmark

Given a consequential execution, the system should answer:

```text
What memory was available?
What knowledge was available?
Which versions were used?
Which evidence was retrieved?
Which constraints were active?
Which authority context applied?
Which information was excluded?
```

This benchmark connects III-007 directly to III-004.

---

# 70. Trust Benchmark

Test whether the runtime correctly distinguishes:

```text
AVAILABLE
TRUSTED
AUTHORITATIVE
FRESH
RELEVANT
```

These should be independently evaluated.

---

# 71. Deferred Decisions

III-007 intentionally does not freeze:

- exact memory database;
- vector database;
- graph database;
- retrieval engine;
- embedding model;
- context-window management;
- cache implementation;
- retention duration;
- exact trust taxonomy;
- exact freshness algorithm;
- conflict-resolution algorithm;
- memory compression strategy;
- knowledge graph implementation;
- final memory schema registry;
- exact privacy implementation.

These remain engineering decisions unless they change semantic meaning.

---

# 72. Exit Criteria

- [x] Memory identity defined
- [x] Context identity defined
- [x] Knowledge identity boundary defined
- [x] Memory type distinctions defined
- [x] Ephemeral context defined
- [x] Working memory defined
- [x] Long-term memory defined
- [x] Knowledge state defined
- [x] Memory scope defined
- [x] Context isolation defined
- [x] Context composition defined
- [x] Retrieval defined
- [x] Retrieval authority defined
- [x] Retrieval trust defined
- [x] Freshness defined
- [x] Staleness defined
- [x] Expiration defined
- [x] Memory versioning defined
- [x] Memory mutation authority defined
- [x] Memory poisoning boundary defined
- [x] Knowledge ingestion defined
- [x] Knowledge derivation defined
- [x] Knowledge conflict defined
- [x] Knowledge supersession defined
- [x] Knowledge invalidation defined
- [x] Memory access control defined
- [x] Context snapshot defined
- [x] Context reproducibility defined
- [x] Context contamination defined
- [x] Retrieval poisoning defined
- [x] Context branching and merging defined
- [x] Least-context principle defined
- [x] Memory lifecycle defined
- [x] Recovery defined
- [x] Self-critique integration defined
- [x] Adversarial verification integration defined
- [x] Memory / knowledge invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Reconstruction benchmarks defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 73. Next Contract

**III-008 — Decision, Planning & Execution Intent Contract**

III-008 will define how the architecture represents a decision or intended action before execution, including:

```text
decision identity
intent identity
goal
requested operation
candidate actions
constraints
authority
dependencies
evidence
uncertainty
risk
decision status
approval
execution binding
abstention
escalation
counterfactual alternatives
decision provenance
```

The central boundary remains:

```text
INTENT
≠
DECISION
≠
EXECUTION
≠
OUTCOME
```
