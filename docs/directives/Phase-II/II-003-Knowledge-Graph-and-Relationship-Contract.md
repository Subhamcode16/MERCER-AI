# II-003 — Knowledge Graph & Relationship Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Semantic relationships connecting the Campaign Intelligence Layer

## 1. Purpose

II-003 defines the relationship model through which the canonical intelligence objects established in II-002 become a coherent reasoning graph.

The graph must encode semantic dependency, authority boundaries, provenance, evidence flow, narrative relationships, channel inheritance, evaluation impact, and controlled change propagation.

The graph is the **causal and explanatory backbone** of the Campaign Intelligence Layer.

## 2. Core Principle

> An intelligence object is meaningful only in relation to the objects that justify it, depend on it, constrain it, or are affected by it.

Therefore the architecture must preserve both:

`OBJECT + RELATIONSHIP`

rather than treating objects as isolated records.

## 3. Canonical Graph

```text
                         CAMPAIGN
                            │
                     HAS_OBJECTIVE
                            ↓
                      OBJECTIVE
                            │
                  DERIVES / CONSTRAINS
                            ↓
                  COMMUNICATION INTENT
                            │
                     REQUIRES_EVIDENCE
                            ↓
                  EVIDENCE REQUIREMENT
                            │
                    MOTIVATES
                            ↓
                  ASSET REQUIREMENT
                            │
                     REALIZED_AS
                            ↓
                          ASSET
                            │
                ┌───────────┴───────────┐
                ↓                       ↓
          OCCUPIES_NODE          ASSIGNED_TO
                ↓                       ↓
         NARRATIVE NODE          CHANNEL PROJECTION
                │                       │
           RELATES_TO              DERIVED_FROM
                ↓                       ↓
         NARRATIVE NODE        CANONICAL NARRATIVE
```

This is a conceptual graph. Exact implementation representation remains an engineering decision.

## 4. Relationship Categories

### Strategic

```text
CAMPAIGN → HAS_OBJECTIVE → OBJECTIVE
OBJECTIVE → SUPPORTS → COMMUNICATION_INTENT
```

### Evidence

```text
COMMUNICATION_INTENT → REQUIRES_EVIDENCE → EVIDENCE_REQUIREMENT
EVIDENCE_REQUIREMENT → SATISFIED_BY → ASSET
ASSET → CONTRIBUTES_EVIDENCE_TO → EVIDENCE_REQUIREMENT
```

### Planning

```text
EVIDENCE_REQUIREMENT → MOTIVATES → ASSET_REQUIREMENT
ASSET_REQUIREMENT → REALIZED_AS → ASSET
```

### Narrative

Potential semantic relationships:

```text
PRECEDES
FOLLOWS
REVEALS
DEEPENS
REINFORCES
CONTRASTS
TRANSITIONS_TO
RESOLVES
```

### Channel

```text
CHANNEL_PROJECTION → DERIVED_FROM → CANONICAL_NARRATIVE
ASSET → ASSIGNED_TO → CHANNEL_PROJECTION
```

### Evaluation

```text
EVALUATION_RESULT → EVALUATES → TARGET_OBJECT
EVALUATION_RESULT → DIAGNOSES → FAILURE_OR_WEAKNESS
EVALUATION_RESULT → RECOMMENDS → REVISION
```

## 5. Dependency Direction

The default strategic dependency direction is:

```text
CAMPAIGN OBJECTIVE
        ↓
COMMUNICATION INTENT
        ↓
EVIDENCE REQUIREMENT
        ↓
ASSET REQUIREMENT
        ↓
ASSET
        ↓
CHANNEL / NARRATIVE EXECUTION
```

This represents semantic dependency, not a rigid runtime execution sequence.

## 6. Upstream vs Downstream Authority

```text
UPSTREAM
Campaign Objective
      ↓
Intent
      ↓
Evidence
      ↓
Asset Requirement
      ↓
Asset
DOWNSTREAM
```

A downstream agent must not silently redefine an upstream locked decision merely because its own optimization would benefit from doing so.

## 7. Authority Boundary Invariant

> A child object may provide evidence about, challenge, or request revision of its parent decision, but it may not silently mutate the semantic meaning of a locked parent object.

Example:

```text
Evidence Agent
→ may modify Evidence Requirement
→ may flag Intent as insufficient or contradictory
→ may NOT silently modify locked Intent
```

## 8. Challenge vs Mutation

The graph must distinguish:

`CHALLENGE`

from:

`MUTATION`

A downstream agent may challenge a requirement or identify an impossible dependency without automatically changing the underlying decision.

A challenge produces a reviewable event rather than an implicit mutation.

## 9. Provenance Graph

Every derived decision should be traceable:

```text
ASSET
    ↓ REALIZED_AS
ASSET REQUIREMENT
    ↓ MOTIVATED_BY
EVIDENCE REQUIREMENT
    ↓ REQUIRED_BY
COMMUNICATION INTENT
    ↓ SUPPORTED_BY
CAMPAIGN OBJECTIVE
    ↓ BELONGS_TO
CAMPAIGN
```

The system should answer why an asset exists through graph traversal rather than relying on retrospective explanations alone.

## 10. Many-to-Many Evidence Contribution

One asset may support multiple evidence requirements:

```text
ASSET
 ├── CONTRIBUTES_EVIDENCE_TO → EVIDENCE-A
 ├── CONTRIBUTES_EVIDENCE_TO → EVIDENCE-B
 └── CONTRIBUTES_EVIDENCE_TO → EVIDENCE-C
```

One evidence requirement may be supported by multiple assets:

```text
EVIDENCE-A
 ├── SATISFIED_BY → ASSET-1
 ├── SATISFIED_BY → ASSET-2
 └── SATISFIED_BY → ASSET-3
```

This is required for set-level optimization.

## 11. Contribution Strength

Evidence contribution strength should live on the relationship, not solely on the asset.

Conceptually:

```text
ASSET
   │
   └── CONTRIBUTES_EVIDENCE_TO
           │
           ├── evidence_dimension
           ├── contribution_strength
           ├── confidence
           └── provenance
```

The same asset may provide strong evidence for one requirement and weak evidence for another.

## 12. Narrative as a Specialized Subgraph

The narrative graph should not duplicate the entire campaign graph.

```text
CAMPAIGN INTELLIGENCE GRAPH
        │
        ├── Strategic Subgraph
        ├── Evidence Subgraph
        ├── Asset Subgraph
        └── Narrative Subgraph
```

The narrative subgraph references canonical objects where appropriate.

## 13. Narrative Node / Asset Relationship

```text
NARRATIVE NODE
    ↓ REPRESENTED_BY
ASSET
```

An asset may legitimately participate in multiple narrative contexts, including channel-specific contexts, without becoming a duplicate physical asset.

## 14. Canonical Narrative vs Channel Projection

```text
CANONICAL NARRATIVE
        ↓
DERIVED_AS
        ↓
CHANNEL PROJECTION
```

A projection may change sequence, pacing, asset selection, format, entry point, and CTA within its authority.

It must not silently alter product truth, hard brand constraints, locked campaign intent, or locked narrative invariants.

## 15. Campaign Variant

When a channel deliberately changes strategic meaning rather than merely presentation:

```text
CAMPAIGN VARIANT
→ VARIANT_OF
→ MASTER CAMPAIGN
```

A variant inherits master constraints unless explicitly reopened through the appropriate authority mechanism.

## 16. Knowledge Gap Relationships

A knowledge gap points to the decisions it affects:

```text
KNOWLEDGE GAP
→ AFFECTS
→ INTENT / EVIDENCE / ASSET STRATEGY
```

This enables impact-aware escalation and prevents consequential gaps from being silently filled with fabricated certainty.

## 17. Revision and Impact Propagation

```text
REVISION
   ↓
CHANGES
   ↓
OBJECT
   ↓
IMPACTS
   ├── dependent object A
   ├── dependent object B
   └── dependent object C
```

The system should invalidate and reconsider semantically dependent objects rather than recomputing the entire campaign unnecessarily.

## 18. Change Propagation Principle

> A change should propagate only through semantically dependent relationships.

Changing a Shot Family should not automatically modify a Campaign Objective.

Changing a Campaign Objective may propagate through Intent, Evidence, Asset Strategy, Narrative, and Channel Projections.

## 19. Relationship Authority

Authorization applies to:

`OBJECT + OPERATION + RELATIONSHIP`

An agent may be authorized to modify one object type while being forbidden from creating or removing certain relationships.

Conceptually:

```text
CREATE_RELATIONSHIP
REMOVE_RELATIONSHIP
MODIFY_RELATIONSHIP
CHALLENGE_RELATIONSHIP
LOCK_RELATIONSHIP
```

A locked relationship cannot be silently changed. A challenge produces a reviewable event.

## 20. Graph Invariants

### Invariant 1 — No orphaned strategic decisions

Every derived Intent must trace to a Campaign Objective or explicitly declared external authority.

### Invariant 2 — No unsupported evidence requirements

Every Evidence Requirement must trace to one or more Intents unless explicitly marked exploratory.

### Invariant 3 — No unexplained asset requirements

Every Asset Requirement must trace to Evidence Requirements, Intents, or explicitly declared creative objectives.

### Invariant 4 — No unexplained production assets

Every generated campaign Asset must have an Asset Requirement or explicitly declared exploratory status.

### Invariant 5 — Locked upstream state cannot be silently mutated downstream

Authority boundaries must be enforced structurally.

### Invariant 6 — Channel projections retain campaign lineage

A projection must trace to its parent campaign/narrative.

### Invariant 7 — Revisions preserve provenance

No revision may destroy the history required to reconstruct prior state.

### Invariant 8 — Evaluation cannot silently mutate its target

An Evaluation Result may recommend a Revision but cannot silently rewrite the evaluated object.

## 21. Falsifiability & Validation Requirements

### Hypothesis A — Dependency direction protects strategic integrity

**Claim:** Objective → Intent → Evidence → Asset reduces downstream strategic drift.

**Test:** Attempt downstream mutations of upstream objects and measure unauthorized mutation rate, strategic drift, and constraint violations.

### Hypothesis B — Explicit graph relationships improve explainability

**Claim:** A graph-backed provenance chain provides more reliable explanations than free-form retrospective agent reasoning.

**Test:** Compare graph-derived explanations against retrospective agent explanations for factual traceability and unsupported claims.

### Hypothesis C — Localized dependency propagation reduces unnecessary recomputation

**Claim:** Changing a local object should invalidate only semantically dependent objects.

**Test:** Perform controlled mutations and compare expected versus observed invalidation and recomputation sets.

### Hypothesis D — Relationship-level authority is necessary

**Claim:** Object-level permissions alone are insufficient to prevent semantic graph manipulation.

**Test:** Attempt unauthorized relationship creation/removal while keeping object mutation permissions valid.

## 22. Adversarial Attack Surface

The future Adversarial Verification Agent should attempt:

1. Upstream intent mutation
2. Hidden intent creation through evidence
3. Unauthorized relationship creation
4. Relationship deletion
5. Provenance severing
6. Channel projection lineage breaking
7. Variant masquerading as projection
8. Unsupported asset creation
9. Evaluation-result mutation
10. Revision-history destruction
11. Circular dependency injection
12. Contradictory relationship injection

The Verification Harness should record:

```text
ATTACK
→ TARGET
→ EXPECTED INVARIANT
→ OBSERVED RESULT
→ PASS / FAIL
→ EVIDENCE
```

## 23. Circular Dependency Protection

Dependency edges must be distinguished from feedback edges.

For example:

```text
Intent
 ↓
Evidence
 ↓
Asset
 ↓
Evaluation
 ↓
Revision
 ↓
Intent
```

may represent a legitimate closed-loop workflow, but the dependency graph must not permit uncontrolled semantic cycles.

Therefore:

`DEPENDENCY EDGE ≠ FEEDBACK EDGE`

## 24. Proposed Relationship Metadata

Conceptually:

```text
relationship_id
relationship_type
source_id
target_id
authority
provenance
confidence
lifecycle_state
created_by
created_at
locked
```

Evidence relationships may additionally carry:

```text
evidence_dimension
contribution_strength
```

Narrative relationships may additionally carry:

```text
transition_rationale
priority
```

Exact schema details remain an implementation concern.

## 25. Knowledge Graph vs Runtime Blackboard

### Knowledge / Intelligence Graph

Represents:

- semantic truth
- relationships
- provenance
- dependencies
- history

### Runtime Blackboard

Represents:

- current working state
- agent tasks
- candidate decisions
- execution state
- temporary evaluation state

The blackboard may reference the graph but must not become a replacement for it.

## 26. Core Graph Contract

The Campaign Intelligence Graph must provide:

```text
TRACEABILITY
DEPENDENCY
AUTHORITY
PROVENANCE
IMPACT PROPAGATION
NARRATIVE RELATIONSHIPS
CHANNEL LINEAGE
EVALUATION TARGETING
REVISION HISTORY
```

It should allow the system to answer:

- Why does this object exist?
- What does this object depend on?
- What depends on this object?
- Who is allowed to change this relationship?
- What would be affected if this object changed?
- Which evidence supports this decision?
- Which campaign objective ultimately justifies this asset?

## 27. Deferred Decisions

II-003 does not freeze:

- graph database technology,
- relational vs graph storage,
- exact serialization format,
- complete relationship enum,
- indexing strategy,
- traversal implementation,
- caching,
- distributed synchronization.

Those decisions belong to engineering after the semantic contract is ratified.

## 28. Exit Criteria

II-003 is semantically complete when:

- [x] Canonical dependency direction defined
- [x] Relationship categories defined
- [x] Evidence relationships defined
- [x] Narrative relationships separated
- [x] Channel lineage defined
- [x] Variant lineage defined
- [x] Knowledge-gap impact defined
- [x] Revision propagation defined
- [x] Relationship authority defined
- [x] Graph invariants defined
- [x] Falsifiable hypotheses defined
- [x] Adversarial attack surface defined
- [x] Blackboard / graph boundary defined

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-004 — Communication Intent Derivation Contract**

This specification will define how the system derives communication intents from campaign objectives and authoritative knowledge without inventing strategy, over-interpreting weak evidence, or allowing downstream agents to silently redefine campaign meaning.
