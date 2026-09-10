# II-012 — Provenance, Lineage & Audit Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Immutable provenance, decision lineage, authority traceability, version history, and auditability across the Campaign Intelligence Layer

---

## 1. Purpose

II-012 defines how the intelligence architecture preserves the complete lineage connecting:

```text
KNOWLEDGE
→ AUTHORITY
→ INTENT
→ EVIDENCE
→ ASSET STRATEGY
→ NARRATIVE
→ CHANNEL PROJECTION
→ PROMPT / EXECUTION
→ EVALUATION
→ FAILURE
→ RECOVERY
```

The objective is to make the system capable of answering:

> **Why does this output exist, what information and decisions produced it, who or what authorized those decisions, what evidence supports them, what changed over time, and what happened when the system was challenged?**

The architecture must not depend on reconstructed explanations generated after the fact.

---

# 2. Core Principle

> **Every consequential intelligence-layer decision must have traceable provenance and lineage back to its authoritative inputs, supporting evidence, decision context, and revision history.**

Therefore:

```text
EXPLANATION
≠
PROVENANCE
```

An LLM-generated explanation may describe a decision.

It does not establish that the decision actually originated from the stated reasoning.

---

# 3. Canonical Lineage Chain

```text
SOURCE
   ↓
CLAIM
   ↓
KNOWLEDGE
   ↓
AUTHORITY
   ↓
INTENT
   ↓
EVIDENCE REQUIREMENT
   ↓
ASSET STRATEGY
   ↓
NARRATIVE
   ↓
CHANNEL PROJECTION
   ↓
ASSET SPECIFICATION
   ↓
PROMPT / EXECUTION
   ↓
OUTPUT
   ↓
EVALUATION
   ↓
FAILURE / FINDING
   ↓
RECOVERY
   ↓
NEW VERSION
```

Every applicable stage should preserve its upstream references.

---

# 4. Provenance Definition

Provenance answers:

> **Where did this piece of information or decision come from?**

Potential provenance sources include:

```text
USER INPUT
SOURCE DOCUMENT
RETRIEVED SOURCE
VALIDATED CLAIM
KNOWLEDGE RECORD
SYSTEM RULE
LAW
GLOSSARY
DECISION
AGENT OUTPUT
HUMAN REVIEW
EVALUATION
RECOVERY ACTION
```

The exact provenance taxonomy remains extensible.

---

# 5. Lineage Definition

Lineage answers:

> **How did this object evolve from earlier objects?**

Examples:

```text
Intent v1
   ↓ revised because of evaluation
Intent v2
   ↓ informs
Evidence Requirement v3
```

or:

```text
Asset A
   ↓ selected for
Narrative Node N4
   ↓ projected into
Channel P2
```

Lineage therefore represents relationships across the intelligence graph.

---

# 6. Provenance vs Lineage

These concepts must remain distinct.

## Provenance

```text
Where did this information come from?
```

## Lineage

```text
How did this object connect to other objects and evolve?
```

A system may have provenance without complete lineage, or lineage without sufficient source provenance.

Both are required for full auditability.

---

# 7. Audit Definition

Auditability means:

> **An authorized reviewer can reconstruct the relevant decision path from recorded artifacts without relying on hidden model state or memory.**

The audit system should support:

```text
FORWARD TRACE
```

and:

```text
BACKWARD TRACE
```

---

# 8. Forward Trace

Starting from a source:

```text
SOURCE
 ↓
CLAIM
 ↓
KNOWLEDGE
 ↓
DECISION
 ↓
OUTPUT
```

Question answered:

> Where did this source influence the final campaign?

---

# 9. Backward Trace

Starting from an output:

```text
OUTPUT
 ↓
PROMPT
 ↓
ASSET SPECIFICATION
 ↓
NARRATIVE
 ↓
ASSET STRATEGY
 ↓
EVIDENCE
 ↓
INTENT
 ↓
KNOWLEDGE
 ↓
SOURCE
```

Question answered:

> Why does this output exist?

---

# 10. Decision Lineage

Every consequential decision should preserve:

```text
decision_id
decision_type
input_objects
constraints
authority
reason
alternatives
selected_option
confidence
evidence
parent_version
resulting_version
timestamp
agent / evaluator
provenance
```

The exact runtime schema is deferred.

---

# 11. Decision Authority

Every consequential decision must identify the authority under which it was made.

Potential authority classes:

```text
USER
PRODUCT_OWNER
LOCKED_POLICY
LAW
VALIDATED_KNOWLEDGE
SYSTEM_RULE
AGENT_AUTHORITY
EVALUATION
HUMAN_REVIEW
```

Authority must remain scoped.

---

# 12. Authority Scope

Authority should specify:

```text
OBJECT
DOMAIN
CLAIM TYPE
CONTEXT
TIME
DECISION TYPE
```

Example:

```text
Authority:
Product owner

Scope:
Current product description

Decision:
Product truth

Authority:
HIGH
```

This does not automatically authorize:

```text
historical interpretation
cultural claims
audience psychology
```

---

# 13. Authority Conflict

When two authoritative records conflict:

```text
AUTHORITY A
      ↕
AUTHORITY B
```

the system must create:

```text
AUTHORITY CONFLICT
```

rather than silently selecting one.

Conflict resolution must be governed by the relevant authority hierarchy or escalated when no valid precedence exists.

---

# 14. Immutable Record Principle

Consequential historical records should be append-oriented.

When a decision changes:

```text
OLD RECORD
   ↓
NEW RECORD
```

rather than:

```text
OLD RECORD
   ↓ overwritten
NEW RECORD
```

The original state should remain auditable.

Implementation details such as event sourcing, append-only tables, or versioned documents remain deferred.

---

# 15. Versioning

Every consequential semantic object should have a version.

Conceptually:

```text
OBJECT
├── v1
├── v2
├── v3
└── current
```

Each revision must preserve:

```text
previous_version
change_reason
change_trigger
authority
changed_fields
timestamp
actor
```

---

# 16. Version Semantics

A new version should be created when the object's semantic meaning changes.

Minor metadata changes may follow a different implementation policy.

The system should distinguish:

```text
SEMANTIC CHANGE
```

from:

```text
METADATA CHANGE
```

to prevent unnecessary version fragmentation.

---

# 17. Change Record

Every semantic revision should preserve:

```text
change_id
object_id
from_version
to_version
changed_fields
reason
trigger
authority
evidence
impact
actor
timestamp
```

This enables precise audit.

---

# 18. Decision Alternatives

When a consequential decision involved meaningful alternatives, the lineage should preserve them.

Example:

```text
DECISION
 ├── OPTION A
 ├── OPTION B
 └── OPTION C
       ↓
   SELECTED B
```

The system should record:

```text
why selected
why alternatives rejected
```

when such reasoning is material to the decision.

---

# 19. Rejected Decisions

Rejected alternatives should not be erased when they materially affect auditability.

A rejected option may explain:

```text
why the final strategy looks the way it does
```

or:

```text
why a later recovery revisited an earlier branch
```

---

# 20. Provenance Granularity

Provenance should exist at the smallest practical consequential unit.

Examples:

```text
DOCUMENT
CLAIM
FIELD
DECISION
ASSET
NARRATIVE NODE
EVALUATION FINDING
```

The architecture should avoid attaching one broad citation to an entire object when only a subset of its content is supported.

---

# 21. Evidence Lineage

Every evidence requirement should preserve:

```text
intent_id
claim / requirement
supporting knowledge
supporting sources
evaluation method
status
```

This enables:

> Why was this evidence considered necessary?

to be answered.

---

# 22. Asset Lineage

Every strategic asset should trace to:

```text
asset
 ↓
asset role
 ↓
evidence / narrative contribution
 ↓
intent
 ↓
campaign objective
```

A generated image should therefore not exist as an unexplained visual artifact.

---

# 23. Narrative Lineage

Every narrative node should trace to:

```text
narrative node
 ↓
intent contribution
 ↓
evidence contribution
 ↓
asset references
 ↓
campaign objective
```

Transitions should preserve semantic rationale.

---

# 24. Channel Lineage

Every channel projection should trace to:

```text
channel projection
 ↓
canonical narrative
 ↓
asset strategy
 ↓
evidence
 ↓
intent
 ↓
campaign objective
```

This allows cross-channel strategic drift to be detected.

---

# 25. Prompt Lineage

A prompt should trace to the semantic specification that produced it.

Conceptually:

```text
PROMPT
 ↓
ASSET SPECIFICATION
 ↓
CHANNEL / NARRATIVE ROLE
 ↓
ASSET STRATEGY
 ↓
EVIDENCE
 ↓
INTENT
```

The prompt itself must not become the primary source of strategic meaning.

---

# 26. Output Lineage

Generated outputs should preserve:

```text
output_id
generation_id
prompt_version
asset_specification_version
model
model_version
parameters where relevant
input references
channel context
timestamp
evaluation status
```

This enables reproducibility analysis.

---

# 27. Evaluation Lineage

Every evaluation finding should trace to:

```text
target output
requirement
criterion
observation
evidence
evaluation method
evaluator
result
```

The architecture must preserve whether the finding was:

```text
RULE-BASED
MODEL-BASED
HUMAN
MEASURED
COMPOSITE
```

---

# 28. Recovery Lineage

Every recovery action should trace:

```text
RECOVERY
 ↓
FAILURE
 ↓
EVALUATION / CRITIQUE / ADVERSARIAL FINDING
 ↓
AFFECTED OBJECT
 ↓
ROOT CAUSE
 ↓
NEW VERSION
```

This makes recovery behavior auditable.

---

# 29. Cross-Agent Lineage

When one agent consumes another agent's output, the dependency must be explicit.

Example:

```text
Evidence Agent
       ↓
Asset Strategy Agent
       ↓
Narrative Agent
       ↓
Channel Projection Agent
       ↓
Prompt Compiler
```

The system should preserve:

```text
producer
consumer
input version
output version
timestamp
```

This is necessary to identify cross-agent contamination and stale inputs.

---

# 30. Stale Dependency Detection

An agent may consume an outdated upstream version.

Example:

```text
Evidence v3
        ↓
Asset Strategy generated using Evidence v2
```

The lineage system should detect:

```text
STALE DEPENDENCY
```

and trigger:

```text
RE-EVALUATION
```

or:

```text
REPLAN
```

when material.

---

# 31. Dependency Integrity

A dependency should specify:

```text
source_object
source_version
consumer_object
consumer_version
dependency_type
required
status
```

This allows the system to determine whether downstream objects remain valid after upstream changes.

---

# 32. Provenance Integrity

A provenance record should itself be verifiable.

The system should eventually support checks such as:

```text
Referenced object exists
Referenced version exists
Referenced source is accessible
Claim location is valid
Decision timestamp is valid
Parent-child relation is valid
```

Broken provenance should become a detectable system error.

---

# 33. Audit Trail

The audit trail should preserve events such as:

```text
CREATED
READ
DERIVED
SELECTED
REJECTED
REVISED
EVALUATED
FAILED
CHALLENGED
RECOVERED
ESCALATED
APPROVED
BLOCKED
ARCHIVED
```

Not every event needs identical storage semantics.

The event taxonomy remains extensible.

---

# 34. Audit Query Requirements

The audit system should eventually answer questions such as:

```text
Why was this asset generated?

Which evidence requirement caused it to exist?

Which intent caused that evidence requirement?

Which source supports the underlying claim?

Which agent selected this asset?

Which version of the knowledge did it use?

Was the asset ever challenged?

What evaluation failed?

What recovery changed it?

Why was the final version accepted?
```

These queries are architectural requirements, not merely UI features.

---

# 35. Audit Completeness

A decision should be considered auditable only if its required lineage is present.

Conceptually:

```text
REQUIRED LINEAGE
        ↓
PRESENT?
   ┌────┴────┐
  YES       NO
   ↓         ↓
AUDITABLE   INCOMPLETE
```

Missing lineage must not be silently filled using generated explanations.

---

# 36. Provenance Gaps

Potential states:

```text
COMPLETE
PARTIAL
BROKEN
MISSING
UNCERTAIN
```

The system should identify exactly where the gap occurs.

Example:

```text
Prompt
 ↓
Asset Specification
 ↓
Evidence
 ↓
MISSING INTENT PROVENANCE
```

This is preferable to marking the entire object simply as:

```text
UNKNOWN
```

---

# 37. Audit vs Explanation

A natural-language explanation can be generated from the audit graph.

But:

```text
AUDIT GRAPH
→ source of truth

EXPLANATION
→ presentation layer
```

The explanation must be generated from recorded lineage, not the reverse.

---

# 38. Audit vs Memory

The architecture must not depend on an agent remembering why it made a decision.

Instead:

```text
DECISION
→ recorded lineage
```

The system should remain auditable even if:

```text
agent restarted
model changed
session ended
different evaluator used
```

---

# 39. Lineage Across Model Versions

If a model changes:

```text
Model A
 ↓
Decision v1

Model B
 ↓
Decision v2
```

the system must preserve which model produced which result.

This allows:

```text
MODEL-INDUCED CHANGE
```

to be distinguished from:

```text
KNOWLEDGE CHANGE
```

or:

```text
POLICY CHANGE
```

---

# 40. Lineage Across Knowledge Versions

If knowledge changes:

```text
Knowledge v1
 ↓
Decision v1

Knowledge v2
 ↓
Decision v2
```

the system should identify which downstream decisions require re-evaluation.

---

# 41. Lineage Across Policy / Law Versions

When a law, glossary, policy, or system rule changes:

```text
LAW v1
 ↓
DECISION v4
```

the system should be capable of locating dependent decisions.

This supports:

```text
IMPACT ANALYSIS
+
REGRESSION EVALUATION
+
TARGETED REPLANNING
```

---

# 42. Provenance and Object Authority

Authority claims must preserve:

```text
authority object
 ↓
authority scope
 ↓
supporting evidence
 ↓
conflicts
 ↓
decision dependencies
```

This enables later verification of:

> Why was this object treated as authoritative?

---

# 43. Provenance and Self-Critique

Self-Critique should be able to inspect:

```text
Was the decision based on the claimed source?

Was the correct version used?

Were important alternatives omitted?

Was authority scope exceeded?

Was an inference represented as a fact?

Was stale knowledge consumed?
```

Critique findings should themselves become auditable records.

---

# 44. Provenance and Adversarial Verification

The Adversarial Verification Agent should attempt to break lineage by:

1. Creating orphan decisions.
2. Referencing nonexistent versions.
3. Using stale dependencies.
4. Forging authority relationships.
5. Severing source-to-claim lineage.
6. Creating fake corroboration.
7. Hiding rejected alternatives.
8. Removing failed evaluation records.
9. Mutating old versions.
10. Creating unexplained strategic changes.
11. Producing prompts without upstream specifications.
12. Creating outputs whose model/version provenance is missing.
13. Introducing circular lineage.
14. Creating false parent-child relationships.
15. Using generated explanations as substitute provenance.

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

# 45. Validation Invariants

### Invariant 1

Every consequential decision has traceable provenance.

### Invariant 2

Every semantic revision preserves the previous version.

### Invariant 3

Old versions cannot be silently overwritten.

### Invariant 4

Authority scope is explicit.

### Invariant 5

Source provenance and decision lineage remain distinguishable.

### Invariant 6

Every asset strategy decision traces to its governing evidence / intent context.

### Invariant 7

Every narrative node preserves its upstream semantic lineage.

### Invariant 8

Every channel projection traces to a canonical narrative.

### Invariant 9

Every prompt traces to an asset specification.

### Invariant 10

Every generated output preserves generation provenance.

### Invariant 11

Every evaluation finding traces to a target and criterion.

### Invariant 12

Every recovery traces to the failure that caused it.

### Invariant 13

Stale dependencies are detectable.

### Invariant 14

Broken provenance cannot be silently replaced by generated explanations.

### Invariant 15

Rejected alternatives remain auditable when materially relevant.

### Invariant 16

Audit history is append-oriented for consequential semantic changes.

### Invariant 17

Cross-agent dependencies preserve producer, consumer, and version information.

### Invariant 18

Lineage cannot contain unexplained strategic jumps.

---

# 46. Falsifiable Architectural Hypotheses

## Hypothesis A — Explicit lineage improves decision reconstruction

**Claim:**

A structured lineage graph allows independent reviewers to reconstruct why a decision occurred more accurately than final-state artifacts alone.

**Experiment:**

Compare:

```text
final output only
vs
output + structured lineage
```

Measure reconstruction accuracy.

---

## Hypothesis B — Versioned provenance reduces hidden strategic drift

**Claim:**

Preserving semantic versions makes unintended changes easier to detect than mutable state.

**Experiment:**

Inject controlled changes into upstream knowledge or intent.

Measure whether downstream strategic changes can be correctly attributed.

---

## Hypothesis C — Stale dependency detection reduces invalid downstream decisions

**Claim:**

Detecting outdated upstream versions reduces decisions made against superseded knowledge.

**Experiment:**

Introduce upstream version changes.

Compare:

```text
dependency-unaware system
vs
lineage-aware system
```

Measure stale-decision rate.

---

## Hypothesis D — Provenance completeness improves audit reliability

**Claim:**

Explicit provenance completeness checks reduce unsupported explanations and orphan decisions.

**Experiment:**

Inject missing provenance records.

Measure detection rate before outputs are accepted.

---

## Hypothesis E — Lineage-based adversarial verification detects hidden authority violations

**Claim:**

A verifier with access to the lineage graph can identify authority-scope violations that are difficult to detect from final outputs alone.

**Experiment:**

Inject authority-scope violations.

Measure detection rate:

```text
output-only verification
vs
lineage-aware verification
```

---

## Hypothesis F — Append-oriented semantic history improves failure analysis

**Claim:**

Preserving previous semantic versions enables more accurate diagnosis of why the architecture changed.

**Experiment:**

Provide reviewers with:

```text
current state
vs
complete version history
```

Measure root-cause identification accuracy.

---

# 47. Architecture Proof Through Lineage

The lineage system becomes part of the evidence used to validate the architecture.

A claim such as:

> "The final asset was produced because the product's material evidence requirement demanded it."

should be demonstrable as:

```text
ASSET
 ↓
ASSET ROLE
 ↓
EVIDENCE REQUIREMENT
 ↓
INTENT
 ↓
OBJECTIVE
```

with every edge represented by recorded objects.

This converts an architectural explanation into an inspectable graph.

---

# 48. Provenance Evaluation Dataset

The architecture should eventually maintain tests containing:

```text
VALID LINEAGE
BROKEN LINEAGE
STALE LINEAGE
CONFLICTING AUTHORITY
MISSING SOURCE
MISSING VERSION
ORPHAN DECISION
FAKE CORROBORATION
CIRCULAR DEPENDENCY
UNEXPLAINED STRATEGIC CHANGE
```

Each test should specify:

```text
expected detection
failure severity
required action
```

---

# 49. Audit Performance

Auditability must eventually be evaluated on:

```text
trace completeness
trace correctness
query accuracy
version integrity
stale dependency detection
authority resolution
reconstruction accuracy
```

The audit system itself is not automatically trustworthy merely because it records events.

---

# 50. Audit Security

The exact security implementation is deferred, but consequential provenance should be protected against:

```text
unauthorized mutation
deletion
version rewriting
identity spoofing
timestamp manipulation
lineage forgery
```

The audit system should preserve sufficient integrity for the intended trust model.

---

# 51. Core Contract

> **The Provenance, Lineage & Audit Layer shall preserve an immutable, version-aware, authority-scoped, and queryable record connecting consequential knowledge, claims, decisions, evidence, assets, narratives, channel projections, prompts, outputs, evaluations, failures, and recoveries. It shall support forward and backward tracing, detect stale and broken dependencies, preserve rejected alternatives and semantic revisions where materially relevant, distinguish audit evidence from generated explanations, and provide the structural evidence required to reconstruct and evaluate the behavior of the intelligence architecture itself.**

---

# 52. Deferred Decisions

II-012 does not freeze:

- database implementation,
- event-sourcing architecture,
- graph database selection,
- immutable storage mechanism,
- cryptographic integrity mechanisms,
- audit API,
- retention policy,
- access-control model,
- exact event schema,
- identity architecture,
- timestamp authority.

These remain engineering decisions.

---

# 53. Exit Criteria

II-012 is semantically complete when:

- [x] Provenance defined
- [x] Lineage defined
- [x] Auditability defined
- [x] Forward trace established
- [x] Backward trace established
- [x] Decision lineage established
- [x] Authority scope established
- [x] Authority conflict handling established
- [x] Immutable / append-oriented principle established
- [x] Semantic versioning established
- [x] Change records established
- [x] Alternative / rejection lineage established
- [x] Provenance granularity established
- [x] Evidence lineage established
- [x] Asset lineage established
- [x] Narrative lineage established
- [x] Channel lineage established
- [x] Prompt lineage established
- [x] Output lineage established
- [x] Evaluation lineage established
- [x] Recovery lineage established
- [x] Cross-agent lineage established
- [x] Stale dependency detection established
- [x] Provenance integrity established
- [x] Audit trail established
- [x] Audit query requirements established
- [x] Audit completeness established
- [x] Provenance gap handling established
- [x] Audit / explanation distinction established
- [x] Model and knowledge version lineage established
- [x] Law / policy version impact established
- [x] Authority provenance established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Architecture-proof role established
- [x] Provenance evaluation dataset established
- [x] Audit evaluation principles established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-013 — Multi-Agent Governance & Authority Contract**

This specification will define how the different intelligence agents interact, what each agent is authorized to decide, how conflicts between agents are resolved, how agent outputs become trusted inputs, and how the architecture prevents one capable agent from silently overriding another agent's domain authority.
