# III-004 — Provenance, Lineage & Evidence Trace Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** II-001 through II-017, II-RAT-001 through II-RAT-003, III-001, III-002, III-003  
**Purpose:** Define the machine-readable provenance and lineage contract required to reconstruct the origin, transformation, authority, evidence, evaluation, execution, critique, adversarial verification, and lifecycle history of consequential Intelligence Objects and decisions.

---

# 1. Purpose

III-004 translates the ratified provenance principles into an executable trace model.

The central requirement is:

> **If a consequential decision occurred, the system must be able to reconstruct how it came to exist.**

The provenance layer therefore answers:

```text
WHERE DID THIS COME FROM?
WHAT WAS USED?
WHAT CHANGED?
WHO / WHAT PRODUCED IT?
UNDER WHICH AUTHORITY?
WHICH VERSION WAS CONSUMED?
WHICH EVIDENCE SUPPORTED IT?
WHICH EVALUATIONS OCCURRED?
WHICH CRITIQUES OCCURRED?
WHICH ATTACKS OCCURRED?
WHICH LIFECYCLE TRANSITIONS OCCURRED?
```

---

# 2. Provenance Is Structural

Provenance is not an optional logging feature.

It is part of the semantic integrity of the Intelligence Architecture.

The minimum consequential lineage is:

```text
SOURCE
 ↓
OBJECT
 ↓
DECISION
 ↓
EXECUTION
 ↓
OUTPUT
 ↓
EVALUATION
 ↓
CRITIQUE / ATTACK
 ↓
FINAL STATE
```

The exact path varies by object and workflow, but the ability to reconstruct it must be preserved.

---

# 3. Provenance vs Audit vs Logging

These concepts must remain distinct.

```text
LOGGING
→ records operational events

AUDIT
→ records and reconstructs accountable actions

PROVENANCE
→ establishes origin, transformation, dependency, authority, and lineage
```

A log entry alone is not necessarily sufficient provenance.

A provenance record must be semantically connected to the object, decision, or event it describes.

---

# 4. Provenance Identity

Every provenance context should have a globally unique identifier.

Recommended conceptual form:

```text
PROV-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

---

# 5. Provenance Event

A provenance event represents a meaningful transformation, decision, observation, authorization, evaluation, or lifecycle action affecting an object or process.

Conceptually:

```yaml
provenance_event:
  event_id: PEV-...
  event_type: ...
  timestamp: ...
  actor: ...
  inputs: []
  outputs: []
  authority_refs: []
  evidence_refs: []
  context: ...
```

The exact event taxonomy is compiled from the ratified architecture.

---

# 6. Event Identity

Every provenance event receives a unique identifier:

```text
PEV-<ULID>
```

The event identifier must remain immutable.

---

# 7. Event Types

The initial conceptual vocabulary includes:

```text
CREATED
IMPORTED
RETRIEVED
TRANSFORMED
DERIVED
DECIDED
AUTHORIZED
EVALUATED
CRITIQUED
ATTACKED
EXECUTED
TRANSITIONED
INVALIDATED
SUPERSEDED
ARCHIVED
RESTORED
RECOVERED
```

The definitive registry must be compiled from the ratified specifications.

The engineer must not create new event semantics merely to simplify implementation.

---

# 8. Actor

Every consequential provenance event should identify the actor responsible for producing or initiating it.

An actor may be:

```text
human
agent
runtime
external service
import process
system component
```

Actor identity must resolve to the applicable identity and authority systems.

---

# 9. Actor Does Not Imply Authority

Provenance must preserve:

```text
WHO PERFORMED / INITIATED
```

separately from:

```text
WHO AUTHORIZED
```

Therefore:

```text
ACTOR
≠
AUTHORIZER
```

The event should reference both where required.

---

# 10. Source Identity

When an object originates from an external or internal source, provenance should preserve source identity.

Conceptually:

```yaml
source:
  source_type: ...
  source_id: ...
  source_version: ...
  locator: ...
```

A locator alone is insufficient where the source can change.

---

# 11. Source Snapshot

Where a source is mutable, provenance should preserve a stable snapshot reference where feasible.

This may include:

```text
content hash
snapshot ID
source version
retrieval timestamp
```

The goal is to reconstruct what information was actually available at decision time.

---

# 12. Retrieval Provenance

When retrieved information contributes to a consequential object or decision, record:

```text
source
retrieval time
retrieval mechanism
retrieved version / snapshot
query or retrieval context where appropriate
```

Retrieval does not imply validation or authority.

---

# 13. Transformation Lineage

If:

```text
OBJECT A
```

is transformed into:

```text
OBJECT B
```

the provenance graph must preserve:

```text
A
 ↓
TRANSFORMATION
 ↓
B
```

The transformation record should identify:

```text
transformation type
producer
inputs
outputs
parameters where relevant
timestamp
```

---

# 14. Derived Object Lineage

Derived objects must preserve their exact source versions where deterministic reconstruction requires it.

Example:

```text
A v1.2
  ↓
derive
  ↓
B v1.0
```

The lineage must not collapse this into:

```text
B derived from A
```

without version information.

---

# 15. Decision Lineage

Every consequential decision should preserve:

```text
decision_id
decision_type
decision_maker
authority_refs
inputs
evidence_refs
constraints
object_refs
timestamp
result
```

This connects governance to provenance.

---

# 16. Decision vs Explanation

An explanation generated after a decision is not automatically the provenance of that decision.

The system must distinguish:

```text
DECISION CAUSE / INPUTS
```

from:

```text
POST-HOC EXPLANATION
```

A model-generated explanation may be attached as evidence or commentary, but it must not replace the actual decision lineage.

---

# 17. Authority Lineage

Consequential actions should preserve the authority chain:

```text
REQUEST
 ↓
AUTHORITY
 ↓
DELEGATION
 ↓
AUTHORIZATION DECISION
 ↓
ACTION
```

This connects III-002 to III-004.

---

# 18. Delegation Lineage

When delegated authority is used, provenance must preserve:

```text
source authority
delegation
delegate
scope
decision
```

A historical audit must be able to reconstruct how the delegate acquired the authority used.

---

# 19. Lifecycle Lineage

Every consequential lifecycle transition must be traceable:

```text
PREVIOUS STATE
 ↓
TRANSITION
 ↓
NEW STATE
```

The transition must reference:

```text
object_id
object_version
authority
evidence
actor
timestamp
```

This connects III-003 to III-004.

---

# 20. Runtime Lineage

Runtime execution should preserve:

```text
execution_id
task_id
agent
inputs
outputs
dependencies
runtime state
start time
end time
failure / success
```

Execution lineage must remain distinct from semantic lifecycle state.

---

# 21. Dependency Lineage

When a task or object depends on another object, preserve:

```text
dependency object
dependency version
relationship
resolution time
consumption context
```

This allows stale-input analysis.

---

# 22. Evidence Lineage

Every consequential claim should preserve its evidence references.

Evidence lineage should identify:

```text
evidence_id
source
version / snapshot
retrieval or acquisition event
relevance context
evaluation status
```

Evidence itself may have provenance.

Therefore:

```text
CLAIM
 ↓
EVIDENCE
 ↓
SOURCE
```

must remain reconstructable.

---

# 23. Evidence Does Not Become Authority

Provenance must preserve the distinction:

```text
EVIDENCE
≠
AUTHORITY
```

A source can provide evidence without authorizing a decision.

---

# 24. Evaluation Lineage

Evaluation records should preserve:

```text
evaluation_id
target object / output
evaluator
evaluation contract version
inputs
criteria
result
confidence where applicable
timestamp
```

The provenance layer must preserve which exact object version was evaluated.

---

# 25. Critique Lineage

Self-critique events should preserve:

```text
critique_id
target
critic
target version
inputs
findings
timestamp
```

The critic's findings must remain distinguishable from the original object.

---

# 26. Adversarial Lineage

Adversarial verification should preserve:

```text
attack_id
attack type
target
target version
verifier
attack parameters
execution context
observed result
failure classification
timestamp
```

This enables reproduction and regression.

---

# 27. Attack Evidence

A successful attack should link:

```text
ATTACK
 ↓
OBSERVED FAILURE
 ↓
EVIDENCE
 ↓
REGRESSION CASE
```

A missed attack should also remain recorded where the benchmark requires it.

---

# 28. Experiment Lineage

Architectural experiments must preserve:

```text
experiment_id
claim_id
hypothesis
system version
configuration
inputs
dataset / benchmark version
evaluation protocol
results
conclusion
```

This creates:

```text
ARCHITECTURAL CLAIM
 ↓
EXPERIMENT
 ↓
RESULT
 ↓
EVIDENCE STATUS
```

---

# 29. Claim Lineage

Architectural claims should use the global claim namespace introduced by II-RAT-003.

Recommended form:

```text
ACH-001
ACH-002
...
```

Every claim record should preserve:

```text
claim_id
claim_text
origin_specification
hypothesis
experiment_refs
evidence_refs
current_status
version
```

---

# 30. Claim Status

A claim should not be represented only as:

```text
TRUE / FALSE
```

The architecture requires epistemic distinctions such as:

```text
UNTESTED
SUPPORTED
CONTESTED
FALSIFIED
INCONCLUSIVE
SUPERSEDED
```

The exact registry should be compiled from II-016 and II-017.

---

# 31. Evidence Status vs Claim Status

These are distinct.

```text
EVIDENCE STATUS
```

describes the evidence.

```text
CLAIM STATUS
```

describes the current state of the architectural claim after evaluating evidence.

Do not collapse them.

---

# 32. Provenance Graph

The provenance system forms a directed graph:

```text
SOURCE
 ↓
RETRIEVAL
 ↓
EVIDENCE
 ↓
OBJECT
 ↓
DECISION
 ↓
EXECUTION
 ↓
OUTPUT
 ↓
EVALUATION
 ↓
CRITIQUE / ATTACK
 ↓
LIFECYCLE TRANSITION
```

Additional edges may connect:

```text
AUTHORITY
DELEGATION
CONSTRAINT
RECOVERY
EXPERIMENT
REGRESSION
```

---

# 33. Provenance Graph vs Object Graph

These are distinct structures.

```text
OBJECT GRAPH
→ semantic relationships

PROVENANCE GRAPH
→ historical causality / derivation / accountability
```

An object graph edge such as:

```text
supports
```

does not automatically mean:

```text
caused
```

Provenance must use explicit event semantics.

---

# 34. Provenance Graph vs Execution DAG

Likewise:

```text
PROVENANCE GRAPH
≠
EXECUTION DAG
```

Provenance may contain historical relationships that are not executable dependencies.

---

# 35. Event Ordering

Events should preserve:

```text
timestamp
```

and, where necessary:

```text
sequence number
causal parent
correlation ID
```

Timestamp alone may be insufficient to establish causal order.

---

# 36. Correlation

Related events should support a shared:

```text
correlation_id
```

Example:

```text
request
→ authority check
→ execution
→ evaluation
→ lifecycle transition
```

can be reconstructed as one causal workflow.

---

# 37. Causation

Where one event directly produces another, preserve:

```text
causation_id
```

This distinguishes:

```text
related
```

from:

```text
caused by
```

---

# 38. Idempotency and Duplicate Events

Duplicate event delivery must not create false provenance.

The implementation should support stable event identity and deduplication.

A repeated event must remain distinguishable from a genuinely repeated action.

---

# 39. Event Immutability

Committed provenance events must be immutable.

Correction should use:

```text
corrective event
```

rather than rewriting historical events.

This preserves audit integrity.

---

# 40. Corrections

If an event was recorded incorrectly:

```text
ORIGINAL EVENT
 ↓
CORRECTION EVENT
 ↓
CURRENT INTERPRETATION
```

The original record should remain available unless legally or architecturally required otherwise.

---

# 41. Tamper Detection

The provenance layer should support integrity verification.

Conceptually:

```yaml
integrity:
  content_hash: ...
  previous_event_hash: ...
```

A chained representation may be used where appropriate.

The exact cryptographic mechanism is deferred.

---

# 42. Tamper Evidence vs Tamper Prevention

Provenance can provide:

```text
tamper detection
```

but does not automatically provide:

```text
tamper prevention
```

The architecture must not claim stronger security than the implementation establishes.

---

# 43. Snapshotting

For consequential decisions, provenance should preserve snapshots or immutable references to:

```text
object version
authority version
evidence version
constraint version
evaluation contract version
agent configuration version
```

where required for reconstruction.

---

# 44. Configuration Provenance

A decision may depend on configuration.

Where material, preserve:

```text
agent configuration
prompt / policy version
model identifier
tool configuration
runtime configuration
feature flags
```

The exact sensitivity and retention policy remains implementation-specific.

---

# 45. Prompt Provenance

Where an agent's prompt or instruction materially affects a consequential output, preserve a reference to:

```text
prompt contract version
prompt template version
relevant compiled prompt version
```

Do not assume that storing only the final output is sufficient for reconstruction.

---

# 46. Model Provenance

Where a model contributes materially to a consequential output, preserve:

```text
model identity
model version
provider / runtime identity where relevant
configuration
```

Exact storage of proprietary model internals is not required unless contractually available.

---

# 47. Tool Provenance

Where tools materially affect an output, preserve:

```text
tool identity
tool version
request context
result reference
timestamp
```

This allows downstream evaluation to distinguish:

```text
model-generated information
```

from:

```text
tool-derived information
```

---

# 48. Human Intervention Provenance

Human interventions must remain explicit.

Preserve:

```text
human actor
decision / action
scope
timestamp
authority
reason
object / task affected
```

Do not hide human intervention inside generic runtime logs.

---

# 49. Recovery Lineage

Recovery must preserve:

```text
failure
diagnosis
recovery decision
authority
recovery action
new object/version
re-evaluation
final state
```

This creates:

```text
FAILURE
 ↓
RECOVERY
 ↓
NEW STATE
```

rather than hiding recovery as ordinary mutation.

---

# 50. Strategic Drift Detection

Provenance should allow comparison between:

```text
original intent
```

and:

```text
recovered / revised output
```

to determine whether recovery introduced strategic drift.

The provenance layer records the lineage; the evaluation layer determines whether drift is acceptable.

---

# 51. Cross-Domain Provenance

When multiple domains contribute to a decision, provenance must preserve domain attribution.

Example:

```text
APPAREL EVIDENCE
+
FOOTWEAR EVIDENCE
+
JEWELRY EVIDENCE
        ↓
CROSS-DOMAIN DECISION
```

The final decision must not erase the contributing domains.

---

# 52. Provenance Access

Provenance access must itself be governed.

Not every actor should automatically access:

```text
all source content
all human intervention records
all confidential evidence
```

Therefore:

```text
PROVENANCE
+
AUTHORITY
=
ACCESSIBLE PROVENANCE
```

---

# 53. Privacy / Sensitive Data Boundary

Provenance must not become a justification for indiscriminate retention.

Where sensitive data exists, the implementation must apply applicable:

```text
access controls
retention rules
redaction
minimization
```

The exact policy is deferred to the product's security and compliance requirements.

---

# 54. Provenance Completeness

A provenance record is complete only relative to the reconstruction question.

For a consequential decision, the system should be able to reconstruct at least:

```text
decision
inputs
versions
authority
evidence
constraints
actor
evaluation
result
lifecycle outcome
```

"Complete provenance" must therefore be scoped to a defined audit objective.

---

# 55. Provenance Confidence

Do not represent provenance as simply:

```text
present / absent
```

Where necessary distinguish:

```text
DIRECT
INFERRED
PARTIAL
MISSING
CONFLICTED
UNVERIFIED
```

The exact epistemic taxonomy remains deferred.

---

# 56. Missing Provenance

If mandatory provenance is missing:

```text
DO NOT PRETEND COMPLETE
```

The system should produce:

```text
PROVENANCE_GAP
```

and apply the applicable consumption / evaluation policy.

For consequential operations, missing mandatory provenance should generally block or escalate.

---

# 57. Contradictory Provenance

If two records disagree:

```text
SOURCE A → VERSION 2
SOURCE B → VERSION 3
```

the contradiction must remain visible.

The system must not silently select one merely to create a complete-looking history.

---

# 58. Provenance Reconstruction Query

The system should eventually support questions such as:

```text
What produced object X?

Which sources influenced decision Y?

Which authority allowed action Z?

Which version of evidence was used?

Which model produced this output?

Which evaluation approved it?

Which attack challenged it?

Why was this object invalidated?

Which recovery created this version?
```

These are functional requirements for the provenance layer.

---

# 59. Canonical Provenance Record

Conceptually:

```yaml
provenance_event:
  event_id: PEV-...
  event_type: DERIVED

  timestamp: ...

  actor:
    actor_type: agent
    actor_id: ...

  authorizer_refs:
    - AUTH-...

  correlation_id: ...
  causation_id: ...

  inputs:
    - object_id: IO-...
      version: 1.0.0

  outputs:
    - object_id: IO-...
      version: 1.1.0

  evidence_refs:
    - EVD-...

  authority_refs:
    - AUTH-...

  context:
    model_version: ...
    prompt_version: ...
    tool_versions: []

  integrity:
    content_hash: ...
```

This is conceptual, not final JSON Schema.

---

# 60. Provenance Chain

For an example consequential workflow:

```text
SOURCE S1
   ↓
RETRIEVAL P1
   ↓
EVIDENCE E1
   ↓
OBJECT O1
   ↓
DECISION D1
   ↓
AUTHORIZATION A1
   ↓
EXECUTION X1
   ↓
OUTPUT O2
   ↓
EVALUATION V1
   ↓
CRITIQUE C1
   ↓
ATTACK AT1
   ↓
LIFECYCLE TRANSITION T1
   ↓
FINAL OBJECT O3
```

The system should be able to traverse this chain.

---

# 61. Provenance Invariants

### Invariant 1

Every consequential object has reconstructable origin information.

### Invariant 2

Every consequential decision has traceable inputs.

### Invariant 3

Actor and authorizer remain distinct.

### Invariant 4

Object versions remain explicit.

### Invariant 5

Source versions / snapshots are preserved where required.

### Invariant 6

Transformation lineage is explicit.

### Invariant 7

Decision lineage is explicit.

### Invariant 8

Authority lineage is explicit.

### Invariant 9

Lifecycle lineage is explicit.

### Invariant 10

Runtime lineage remains distinct from semantic lifecycle.

### Invariant 11

Evidence lineage is preserved.

### Invariant 12

Evaluation lineage is preserved.

### Invariant 13

Critique lineage is preserved.

### Invariant 14

Adversarial lineage is preserved.

### Invariant 15

Experiment lineage is preserved.

### Invariant 16

Historical provenance events are immutable.

### Invariant 17

Corrections do not silently rewrite history.

### Invariant 18

Causation is distinct from correlation.

### Invariant 19

Object graphs are distinct from provenance graphs.

### Invariant 20

Provenance graphs are distinct from execution DAGs.

### Invariant 21

Missing mandatory provenance is explicit.

### Invariant 22

Contradictory provenance remains visible.

### Invariant 23

Provenance access is governed.

### Invariant 24

Provenance does not itself establish truth.

### Invariant 25

Provenance does not itself establish authority.

### Invariant 26

Implementation must not invent provenance semantics.

---

# 62. Required Tests

The reference implementation must test:

```text
source lineage
object lineage
version lineage
transformation lineage
decision lineage
authority lineage
delegation lineage
runtime lineage
evidence lineage
evaluation lineage
critique lineage
attack lineage
experiment lineage
recovery lineage
human intervention lineage
missing provenance
contradictory provenance
duplicate events
event correction
causation ordering
tamper detection
stale source reconstruction
cross-domain lineage
```

---

# 63. Falsification Cases

Deliberately attempt:

```text
create object without source
forge actor
forge authorizer
change source version after decision
delete provenance event
rewrite historical event
duplicate event
break causal chain
replace evidence after decision
replace authority after approval
hide human intervention
erase failed attack
erase critique
collapse two object versions
```

The system should detect, reject, quarantine, or explicitly mark these conditions according to the applicable contract.

---

# 64. Audit Reconstruction Test

A core benchmark must ask:

> Given only the persisted object, decision, provenance records, and applicable contract versions, can an independent evaluator reconstruct why the decision occurred?

Measure:

```text
RECONSTRUCTION SUCCESS
RECONSTRUCTION PARTIAL
RECONSTRUCTION FAILURE
```

The benchmark must preserve the exact reconstruction inputs.

---

# 65. Provenance Completeness Metric

A possible diagnostic metric:

```text
Provenance Completeness =
required reconstructable elements present
/
required reconstructable elements
```

This metric is diagnostic only.

A high score does not prove:

```text
truth
correctness
authority
```

---

# 66. Provenance Integrity Metric

A separate diagnostic metric may measure:

```text
integrity-verified events
/
events requiring integrity verification
```

Again, this is not proof of overall system integrity.

---

# 67. Deferred Decisions

III-004 intentionally does not freeze:

- exact provenance database;
- graph database vs relational representation;
- event-bus technology;
- exact event taxonomy beyond ratified semantics;
- cryptographic hash algorithm;
- immutable storage technology;
- retention duration;
- privacy policy;
- redaction strategy;
- exact provenance completeness formula;
- exact sensitive-data classification;
- storage of proprietary model internals;
- final provenance query language.

These remain engineering decisions unless they alter semantic meaning.

---

# 68. Exit Criteria

- [x] Provenance identity defined
- [x] Provenance event defined
- [x] Actor boundary defined
- [x] Authority distinction defined
- [x] Source identity defined
- [x] Source snapshot boundary defined
- [x] Retrieval lineage defined
- [x] Transformation lineage defined
- [x] Decision lineage defined
- [x] Authority lineage defined
- [x] Lifecycle lineage defined
- [x] Runtime lineage defined
- [x] Evidence lineage defined
- [x] Evaluation lineage defined
- [x] Critique lineage defined
- [x] Adversarial lineage defined
- [x] Experiment lineage defined
- [x] Claim lineage defined
- [x] Provenance graph defined
- [x] Graph distinctions defined
- [x] Causation/correlation defined
- [x] Event immutability defined
- [x] Correction model defined
- [x] Tamper boundary defined
- [x] Configuration/model/tool provenance defined
- [x] Human intervention lineage defined
- [x] Recovery lineage defined
- [x] Missing/contradictory provenance defined
- [x] Provenance access boundary defined
- [x] Reconstruction benchmark defined
- [x] Provenance invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 69. Next Contract

**III-005 — Agent Contract, Capability Boundary & Execution Interface**

III-005 will compile the agent model into a machine-readable contract covering:

```text
agent identity
role
capabilities
authority references
inputs
outputs
tools
execution permissions
constraints
handoff
delegation
failure
abstention
timeouts
resource budgets
self-critique interface
adversarial verification interface
provenance obligations
lifecycle interaction
```

The central invariant remains:

```text
AGENT CAPABILITY
≠
AGENT AUTHORITY
```
