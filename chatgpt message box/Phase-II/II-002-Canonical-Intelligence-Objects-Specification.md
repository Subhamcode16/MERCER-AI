# II-002 — Canonical Intelligence Objects Specification

**Status:** Engineering Specification — Established  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Semantic object model for the Campaign Intelligence Runtime

## Purpose

This specification establishes the canonical semantic vocabulary of the Campaign Intelligence Layer before implementation schemas, database structures, or runtime classes are defined.

An intelligence object represents a semantic decision or state, not merely application data.

## Canonical Object Graph

```text
CAMPAIGN
│
├── OBJECTIVE
├── CONTEXT
│   ├── Product Context
│   ├── Brand Context
│   ├── Audience Context
│   └── Channel Context
│
├── COMMUNICATION INTENTS
│   └── EVIDENCE REQUIREMENTS
│
├── ASSET STRATEGY
│   └── ASSET REQUIREMENTS
│       └── ASSETS
│
├── NARRATIVE GRAPH
│   ├── Narrative Nodes
│   └── Narrative Edges
│
├── CHANNEL PROJECTIONS
├── EVALUATION STATE
├── KNOWLEDGE GAPS
└── REVISION HISTORY
```

## Campaign

The root intelligence object containing the complete reasoning context for a campaign.

It references strategic objective, relevant contexts, communication intents, evidence requirements, asset strategy, asset matrix, narrative graph, channel projections, evaluation state, knowledge gaps, and revision history.

Strategic campaign properties should not be silently rewritten by downstream agents.

## Campaign Objective

Represents the intended outcome of the campaign.

The semantic model should distinguish objective type from objective description. The implementation should not prematurely freeze every possible objective as a global enum.

## Campaign Context

A controlled snapshot/reference to relevant knowledge:

- Product
- Brand
- Audience
- Channel
- Market
- Cultural
- Production

The campaign should consume relevant context rather than indiscriminately treating the entire knowledge base as active campaign state.

## Communication Intent

Represents what the campaign needs the audience to understand, perceive, believe, feel, or do.

An intent must distinguish:

- Explicit
- Derived
- Inferred

Derived and inferred intents carry provenance and confidence.

## Evidence Requirement

Represents what must be demonstrated for a communication intent to be sufficiently supported.

It may specify:

- Importance
- Required strength
- Evidence dimensions
- Acceptable forms
- Preferred forms

Evidence status must preserve:

`REPRESENTED ≠ SUFFICIENT ≠ SATURATED`

## Asset Role

Represents why an asset exists within the campaign.

Examples include:

- Product identity
- Material proof
- Craftsmanship proof
- Brand expression
- Desire
- Trust
- Context
- Conversion

`ASSET ROLE ≠ SHOT FAMILY`

## Asset Requirement

Represents the requirement for an executable asset to exist. It connects evidence and communication requirements to an asset role and possible forms.

`ASSET REQUIREMENT → what should exist`

`ASSET → what actually exists`

## Asset

Represents an actual executable visual unit.

Conceptually it may contain:

- Asset identity
- Asset role
- Evidence contributions
- Shot family
- Shot objective
- Narrative position
- Channel assignments
- Generation specification
- Provenance
- Lifecycle state
- Evaluation state

## Narrative Node

Represents a meaningful communication state or event in the campaign narrative. A node is not necessarily a fixed universal sequence position.

## Narrative Edge

Represents the semantic relationship between narrative elements.

Potential relationship types include:

- Precedes
- Follows
- Reveals
- Deepens
- Reinforces
- Contrasts
- Transitions to
- Resolves

The exact canonical relationship vocabulary remains subject to II-003.

## Channel Projection

Represents how the canonical campaign is expressed within a particular distribution environment.

It may contain:

- Channel
- Channel objective
- Selected assets
- Narrative projection
- Format constraints
- Sequence
- Channel-specific requirements

A projection must retain lineage to the master campaign.

## Knowledge Gap

Represents missing or insufficiently authoritative information that prevents a sufficiently reliable intelligence decision.

Examples include unknown product properties, ambiguous audience information, missing channel requirements, and unresolved brand preferences.

A knowledge gap should record severity, affected decisions, resolution requirements, and resolution status. Consequential gaps must be surfaced rather than filled with fabricated certainty.

## Evaluation Result

Represents an observation about the quality or validity of an intelligence or execution result.

It should eventually capture:

- Evaluation scope
- Expected state
- Observed state
- Failure or success condition
- Diagnosis
- Confidence
- Recommended action

Evaluation may occur at asset, asset relationship, asset-set, narrative, channel-projection, or campaign level.

## Revision

Represents a controlled change to intelligence state.

```text
REVISION
├── Source State
├── Changed Object
├── Change
├── Reason
├── Authority
├── Impact
└── Validation
```

Revision history must be preserved rather than overwritten.

## Provisional Authority Matrix

| Object | Primary Creator | Modification Authority | Lock Authority |
|---|---|---|---|
| Campaign | Campaign Orchestrator / User | User / controlled system | User |
| Objective | User / Strategy Agent | User | User |
| Intent | Intent Agent | Intent Agent / User | User |
| Evidence Requirement | Evidence Agent | Evidence Agent / User | User |
| Asset Requirement | Asset Strategy Agent | Asset Strategy Agent | Orchestrator / User |
| Asset | Generation Pipeline | Execution Agents | Orchestrator / Evaluator |
| Narrative | Narrative Agent | Narrative Agent / User | User |
| Channel Projection | Channel Agent | Channel Agent / User | User |
| Evaluation | Evaluator | Evaluator | Evaluator |
| Knowledge Gap | Detecting / Owning Agent | Owning Agent | Resolution process |
| Revision | Orchestrator | Append-only | System |

This matrix is provisional until later agent-harness specifications refine it.

## Universal Object Metadata

Derived intelligence objects should share a common semantic metadata envelope:

```text
id
type
version
lifecycle_state
authority
provenance
confidence
created_by
modified_by
created_at
modified_at
parent_reference
```

The exact implementation schema is intentionally deferred.

## Bidirectional Explainability

### Forward

```text
Campaign Objective
    ↓
Communication Intent
    ↓
Evidence Requirement
    ↓
Asset Requirement
    ↓
Asset
    ↓
Narrative
    ↓
Channel
    ↓
Evaluation
```

### Backward

```text
Asset
    ↓
Asset Requirement
    ↓
Evidence Requirement
    ↓
Communication Intent
    ↓
Campaign Objective
```

The system must be able to answer:

> Why did we generate this asset?

and:

> Which asset supports this campaign requirement?

## Deferred Decisions

II-002 deliberately does not freeze:

- Complete ontology enums
- Numerical thresholds
- Database representation
- Runtime implementation classes
- Graph storage technology

Those decisions follow the semantic relationship contract.
