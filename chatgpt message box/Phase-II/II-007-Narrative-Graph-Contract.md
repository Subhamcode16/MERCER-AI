# II-007 — Narrative Graph Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Transformation of selected asset requirements and assets into a coherent campaign narrative

---

## 1. Purpose

II-007 defines how the Campaign Intelligence Layer organizes selected assets into a **coherent narrative graph**.

The Narrative Engine answers:

> **In what conceptual and experiential order should campaign information, evidence, emotion, and product meaning be encountered so that the campaign communicates coherently?**

The Narrative Engine does not merely sort images.

It reasons about:

- information progression,
- evidence progression,
- emotional progression,
- product revelation,
- narrative states,
- transitions,
- asset roles,
- audience understanding,
- channel adaptation,
- and narrative coherence.

---

# 2. Core Principle

> **A campaign narrative is a structured progression of meaning, not merely a sequence of assets.**

Therefore:

```text
ASSET ORDER
≠
NARRATIVE
```

and:

```text
NARRATIVE
=
MEANINGFUL PROGRESSION
+
RELATIONSHIPS
+
TRANSITIONS
+
AUDIENCE INTERPRETATION
```

An asset becomes narratively meaningful because of its relationship to the assets and communication states around it.

---

# 3. Canonical Narrative Chain

```text
CAMPAIGN OBJECTIVE
        ↓
COMMUNICATION INTENTS
        ↓
EVIDENCE REQUIREMENTS
        ↓
SELECTED ASSET SET
        ↓
NARRATIVE STATES
        ↓
NARRATIVE EDGES
        ↓
CANONICAL NARRATIVE
        ↓
CHANNEL PROJECTIONS
```

The canonical narrative is established before channel-specific adaptations.

---

# 4. Narrative Graph

The narrative should be represented conceptually as:

```text
NARRATIVE GRAPH
│
├── NODES
│   ├── Narrative State
│   ├── Intent Contribution
│   ├── Evidence Contribution
│   └── Asset References
│
└── EDGES
    ├── PRECEDES
    ├── REVEALS
    ├── DEEPENS
    ├── REINFORCES
    ├── CONTRASTS
    ├── TRANSITIONS_TO
    └── RESOLVES
```

The graph is not required to be a simple linear sequence.

It may contain:

```text
BRANCHES
ALTERNATIVE PATHS
OPTIONAL NODES
CHANNEL-SPECIFIC ENTRY POINTS
```

where strategically justified.

---

# 5. Narrative Node

A Narrative Node represents a meaningful communication state in the campaign.

A node may represent:

- an introduction,
- an identity state,
- a product reveal,
- evidence,
- contextualization,
- emotional development,
- desire,
- resolution,
- or action.

The exact taxonomy remains extensible.

A node should describe **what the audience is expected to understand or experience at that point**, not merely which asset is displayed.

---

# 6. Narrative Node Object

Conceptually:

```text
narrative_node_id
campaign_id
statement
node_type
intent_contributions
evidence_contributions
asset_references
audience_state
information_state
emotional_state
priority
required
provenance
authority
version
status
```

The exact runtime schema is deferred.

---

# 7. Narrative State

A Narrative Node may be evaluated across several dimensions.

## Information State

What does the audience know at this point?

```text
UNKNOWN
AWARE
INTRODUCED
UNDERSTOOD
CONFIRMED
```

## Evidence State

How strongly has the relevant claim been demonstrated?

```text
NOT_PRESENT
REPRESENTED
SUPPORTED
SUFFICIENT
```

## Emotional State

What broad experiential state is the campaign attempting to create?

Examples:

```text
CURIOSITY
TRUST
DESIRE
ADMIRATION
BELONGING
CONFIDENCE
URGENCY
```

These are provisional semantic states rather than a universal psychological model.

---

# 8. Narrative Progression

A coherent narrative should generally produce meaningful progression across one or more dimensions:

```text
INFORMATION
EVIDENCE
EMOTION
PRODUCT REVELATION
CONTEXT
ACTION
```

A sequence in which every asset communicates the same state without progression may be visually strong but narratively weak.

---

# 9. Narrative Entry Point

A campaign may have multiple legitimate entry points.

For example:

```text
MASTER NARRATIVE
       │
       ├── ENTRY A → Product-first
       ├── ENTRY B → Cultural-context-first
       └── ENTRY C → Human-desire-first
```

The existence of multiple entry points does not necessarily mean multiple campaigns.

Channel Projection may select an appropriate entry point while preserving canonical campaign meaning.

---

# 10. Narrative Edge

A Narrative Edge describes why one node relates to another.

Potential relationship types include:

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

Each edge should preserve semantic meaning rather than merely temporal ordering.

---

# 11. Edge Semantics

## PRECEDES

Node A occurs before Node B.

This alone does not imply why.

## REVEALS

Node B exposes information that was not previously available.

## DEEPENS

Node B expands or enriches meaning introduced by Node A.

## REINFORCES

Node B strengthens an already established interpretation.

## CONTRASTS

Node B intentionally changes or challenges the interpretation established by Node A.

## TRANSITIONS_TO

Node A provides a meaningful bridge to Node B.

## RESOLVES

Node B addresses a question, tension, expectation, or unresolved state established earlier.

---

# 12. Narrative Transition

A transition should answer:

> **Why should the audience move from this state to the next?**

A transition may be:

```text
INFORMATIONAL
EMOTIONAL
VISUAL
CONCEPTUAL
CAUSAL
TEMPORAL
PRODUCT-BASED
```

The narrative engine should not rely solely on visual similarity.

---

# 13. Asset-to-Node Mapping

Assets may represent narrative nodes:

```text
ASSET
    ↓ REPRESENTS
NARRATIVE NODE
```

An asset may contribute to more than one node when legitimate.

However, the same asset should not be duplicated across the graph merely to create the appearance of narrative richness.

---

# 14. One Node, Multiple Assets

A single narrative state may require several assets.

Example:

```text
NODE:
Establish craftsmanship

       ↓

ASSET A:
Material detail

ASSET B:
Construction detail

ASSET C:
Human interaction
```

These assets may collectively establish one narrative state.

---

# 15. One Asset, Multiple Nodes

A multi-purpose asset may contribute to several states.

Example:

```text
ASSET A
 ├── PRODUCT REVEAL
 ├── MATERIAL PROOF
 └── DESIRE
```

However, the narrative engine must preserve the distinct contribution rather than assuming that one asset automatically fulfills every narrative function equally.

---

# 16. Narrative and Evidence

The Narrative Engine may use Evidence Requirements as inputs.

It should determine:

```text
WHEN
```

and:

```text
IN WHAT CONTEXT
```

evidence is encountered.

It must not redefine what evidence is required.

Therefore:

```text
Evidence Engine
→ determines WHAT must be demonstrated.

Narrative Engine
→ determines WHEN / HOW meaningfully it is introduced.
```

---

# 17. Narrative and Intent

The Narrative Engine must preserve Communication Intent.

It may determine:

```text
progression
ordering
emphasis
repetition
contrast
resolution
```

but cannot silently redefine the underlying intent.

A narrative conflict with a locked intent must become:

```text
CHALLENGE
```

rather than silent mutation.

---

# 18. Narrative Arc

The campaign may express a broad arc such as:

```text
INTRODUCE
    ↓
REVEAL
    ↓
PROVE
    ↓
DEEPEN
    ↓
DESIRE
    ↓
ACT
```

This is a conceptual pattern, not a universal mandatory sequence.

Some campaigns may begin with:

```text
DESIRE
```

and reveal context later.

Others may begin with:

```text
CULTURAL CONTEXT
```

before product revelation.

The architecture should support multiple valid narrative structures.

---

# 19. Narrative Invariants

A narrative must preserve:

```text
PRODUCT TRUTH
LOCKED INTENTS
HARD BRAND CONSTRAINTS
REQUIRED EVIDENCE
```

Narrative creativity operates within these boundaries.

---

# 20. Narrative Tension

Narrative tension is not necessarily a problem.

A campaign may intentionally create:

```text
EXPECTATION
    ↓
CONTRAST
    ↓
REVELATION
```

The system must distinguish:

```text
INTENTIONAL TENSION
```

from:

```text
UNINTENTIONAL CONTRADICTION
```

This distinction should be recorded explicitly.

---

# 21. Narrative Redundancy

Narrative redundancy occurs when multiple nodes or assets perform substantially the same communication function without meaningful progression.

Example:

```text
Node A → Product admiration
Node B → Product admiration
Node C → Product admiration
```

If no new meaning, evidence, context, or emotional progression occurs, the sequence should be challenged.

This is different from Evidence Saturation.

An asset may be non-redundant at the evidence level but redundant narratively, or vice versa.

---

# 22. Narrative Pacing

Pacing describes the distribution of information and meaning across the sequence.

Potential pacing properties include:

```text
REVEAL_RATE
EVIDENCE_DENSITY
EMOTIONAL_CHANGE
VISUAL_CHANGE
INFORMATION_DENSITY
```

These should remain semantic at this stage.

Exact numerical pacing algorithms are deferred.

---

# 23. Narrative Information Budget

Every campaign has limited audience attention.

The narrative should therefore consider:

```text
WHAT MUST BE INTRODUCED
WHAT MUST BE PROVEN
WHAT CAN BE IMPLIED
WHAT CAN BE OMITTED
```

This connects narrative design to asset-set efficiency.

The system should not repeat information merely because additional repetition is possible.

---

# 24. Narrative Branching

A narrative may branch when different audience or channel contexts require different paths.

Example:

```text
                    INTRO
                      │
              ┌───────┴───────┐
              ↓               ↓
        PRODUCT PATH     CULTURAL PATH
              │               │
              └───────┬───────┘
                      ↓
                   DESIRE
```

Branches should preserve shared campaign invariants.

---

# 25. Narrative Convergence

Different paths may converge on a shared node.

This is useful for channel projection.

```text
PATH A ──┐
         ├──→ SHARED PRODUCT REVEAL
PATH B ──┘
```

The graph must preserve the difference in path history even when the audience reaches the same semantic state.

---

# 26. Canonical Narrative vs Channel Projection

The canonical narrative is the campaign-level semantic structure.

Channel Projection adapts it.

```text
CANONICAL NARRATIVE
        ↓
CHANNEL PROJECTION
        ↓
CHANNEL-SPECIFIC SEQUENCE
```

A channel may:

- omit nodes,
- reorder within permitted boundaries,
- compress transitions,
- select alternative entry points,
- use different asset combinations.

It must not silently change campaign truth or locked strategic meaning.

---

# 27. Narrative Projection Constraints

A channel projection must preserve:

```text
Required Intents
Required Evidence
Hard Constraints
Product Truth
Required Narrative Invariants
```

A projection may challenge feasibility if these cannot coexist with channel constraints.

---

# 28. Narrative Strategy Alternatives

When several narrative structures are valid, the system may preserve alternatives.

Example:

```text
NARRATIVE A
Context → Product → Proof → Desire

NARRATIVE B
Product → Desire → Proof → Context

NARRATIVE C
Human → Product → Cultural Context → Proof
```

The system should not declare a single universal optimum without a declared objective or evaluation basis.

---

# 29. Narrative Selection Criteria

Candidate narratives may be evaluated on:

```text
Intent Coverage
Evidence Progression
Information Progression
Emotional Progression
Product Clarity
Narrative Coherence
Channel Adaptability
Redundancy
Complexity
Audience Attention
```

Exact weighting is deferred.

---

# 30. Narrative Decision Record

Every selected narrative structure should preserve:

```text
narrative_id
selected_structure
reason
supported_intents
evidence_progression
asset_mapping
alternative_structures
rejected_alternatives
constraints
confidence
provenance
```

This enables:

> Why is the campaign structured this way?

to be answered from recorded reasoning.

---

# 31. Narrative Failure States

The engine must distinguish:

```text
NO_VALID_NARRATIVE
```

from:

```text
VALID_BUT_WEAK
```

from:

```text
MULTIPLE_VALID_NARRATIVES
```

from:

```text
BLOCKED_BY_ASSET_GAP
```

from:

```text
BLOCKED_BY_EVIDENCE_CONFLICT
```

from:

```text
BLOCKED_BY_CHANNEL_CONSTRAINT
```

This distinction is important for adaptive replanning.

---

# 32. Self-Critique Requirements

The Self-Critique Agent should inspect:

- weak transitions,
- unexplained ordering,
- repeated meaning,
- missing narrative progression,
- unsupported emotional assumptions,
- evidence appearing too late,
- evidence appearing too early without context,
- asset-to-node mismatch,
- intent drift,
- unnecessary narrative complexity,
- and channel projections that distort the canonical narrative.

The critic should generate a critique record rather than silently rewriting the narrative.

---

# 33. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break the Narrative Contract by:

1. Reordering nodes to destroy causal or informational progression.
2. Removing required evidence nodes.
3. Inserting unsupported emotional states.
4. Creating contradictory narrative transitions.
5. Hiding strategic intent changes inside narrative sequencing.
6. Creating redundant narrative loops.
7. Breaking channel lineage.
8. Creating fake narrative alternatives.
9. Using assets outside their supported roles.
10. Bypassing locked narrative invariants.
11. Creating cycles that cause uncontrolled narrative loops.
12. Turning a channel projection into an undeclared campaign variant.

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

# 34. Validation Invariants

### Invariant 1

Every accepted narrative node traces to one or more campaign intents, evidence requirements, asset roles, or explicitly declared narrative objectives.

### Invariant 2

Every required evidence contribution appears in an appropriate narrative position unless explicitly marked channel-specific or non-narrative.

### Invariant 3

Narrative sequencing cannot silently mutate Communication Intent.

### Invariant 4

Narrative sequencing cannot contradict product truth.

### Invariant 5

Hard constraints cannot be removed for narrative convenience.

### Invariant 6

Every selected narrative edge has an explicit semantic relationship.

### Invariant 7

Narrative redundancy is evaluated independently from evidence redundancy.

### Invariant 8

A channel projection retains lineage to the canonical narrative.

### Invariant 9

A strategic alteration cannot masquerade as a channel projection.

### Invariant 10

Narrative alternatives remain distinguishable from revisions.

### Invariant 11

Intentional narrative tension is distinguishable from unresolved contradiction.

### Invariant 12

Narrative cycles must be explicitly declared and bounded.

---

# 35. Falsifiable Architectural Hypotheses

## Hypothesis A — Graph-based narrative reasoning improves coherence

**Claim:**

Representing narrative as nodes and semantic edges produces more coherent campaigns than simple asset ordering.

**Experiment:**

Compare:

```text
System A:
Asset list + ordering

System B:
Narrative graph
```

Measure:

- human coherence ratings,
- intent progression,
- evidence progression,
- unexplained transitions,
- narrative correction rate.

---

## Hypothesis B — Separating narrative from asset strategy improves adaptability

**Claim:**

Keeping narrative structure independent from asset selection allows the system to substitute or modify assets without unnecessarily rewriting campaign meaning.

**Experiment:**

Replace one asset while preserving its required narrative contribution.

Measure whether:

```text
Narrative meaning preserved?
Unnecessary downstream changes?
```

---

## Hypothesis C — Semantic edges improve transition explainability

**Claim:**

Explicit relationships such as `REVEALS`, `DEEPENS`, and `RESOLVES` provide more reliable explanations than raw sequence positions.

**Experiment:**

Ask evaluators to explain why transitions occur using:

```text
sequence-only representation
vs
semantic-edge representation
```

Measure factual and causal accuracy.

---

## Hypothesis D — Narrative redundancy detection improves attention efficiency

**Claim:**

Detecting repeated narrative meaning reduces unnecessary campaign length without reducing required intent or evidence coverage.

**Experiment:**

Inject semantically repetitive nodes and measure whether the system removes or challenges them while preserving required coverage.

---

## Hypothesis E — Canonical narrative plus channel projection improves cross-channel consistency

**Claim:**

Maintaining one canonical narrative and deriving channel projections reduces strategic drift across channels.

**Experiment:**

Compare:

```text
independently generated channel narratives
vs
canonical narrative → projections
```

Measure intent preservation and product/brand consistency.

---

# 36. Narrative Evaluation Model

The Narrative Engine should eventually expose:

```text
INTENT COVERAGE
        ↓
INFORMATION PROGRESSION
        ↓
EVIDENCE PROGRESSION
        ↓
EMOTIONAL PROGRESSION
        ↓
TRANSITION COHERENCE
        ↓
REDUNDANCY
        ↓
CHANNEL ADAPTABILITY
```

No single scalar score should replace the underlying diagnostic dimensions.

---

# 37. Narrative vs Asset Optimization Boundary

The separation is:

```text
ASSET STRATEGY
→ What assets should exist?

NARRATIVE
→ How do those assets communicate as a coherent progression?
```

The Narrative Engine may identify an asset gap.

It should not silently invent a new asset requirement without passing that requirement back through the appropriate strategy mechanism.

---

# 38. Narrative vs Channel Boundary

The separation is:

```text
CANONICAL NARRATIVE
→ Campaign-level meaning and progression.

CHANNEL PROJECTION
→ Channel-specific adaptation.
```

Channel constraints may trigger a challenge to the canonical narrative, but cannot silently redefine it.

---

# 39. Narrative vs Prompt Compilation Boundary

The Narrative Engine must never produce final generation prompts.

The chain remains:

```text
NARRATIVE ROLE
    ↓
ASSET REQUIREMENT
    ↓
ASSET SPECIFICATION
    ↓
PROMPT COMPILATION
```

Narrative meaning informs execution but does not become execution syntax.

---

# 40. Knowledge Gap Handling

Narrative construction may depend on unknown information.

Example:

```text
Unknown audience response
        ↓
Affects emotional progression
        ↓
Narrative confidence reduced
```

The system should preserve the uncertainty rather than fabricate psychological certainty.

Possible outcomes:

```text
CONDITIONAL NARRATIVE
ALTERNATIVE NARRATIVE
RESEARCH REQUEST
ESCALATION
```

---

# 41. Core Contract

> **The Narrative Engine shall transform selected campaign assets and their associated intent and evidence contributions into a coherent, traceable narrative graph that defines meaningful information, evidence, emotional, and product progression while preserving campaign truth, locked intent, hard constraints, and asset provenance. It shall distinguish semantic narrative relationships from simple ordering, preserve legitimate alternatives and branches, support channel projections without strategic drift, and expose narrative weaknesses through deterministic, self-critical, and adversarial validation.**

---

# 42. Deferred Decisions

II-007 does not freeze:

- final narrative taxonomy,
- psychological emotion model,
- numerical pacing metrics,
- transition scoring,
- graph database representation,
- channel-specific sequence algorithms,
- exact evaluator models,
- optimization weights,
- runtime schema.

These remain subjects for subsequent specifications and validation.

---

# 43. Exit Criteria

II-007 is semantically complete when:

- [x] Narrative graph defined
- [x] Narrative node semantics defined
- [x] Narrative state dimensions defined
- [x] Narrative edge vocabulary established provisionally
- [x] Transition semantics established
- [x] Asset-to-node mapping established
- [x] Intent/evidence boundaries established
- [x] Narrative progression established
- [x] Entry points established
- [x] Branching and convergence established
- [x] Canonical narrative / channel projection boundary established
- [x] Narrative redundancy established
- [x] Narrative alternatives established
- [x] Narrative decision records established
- [x] Failure states established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Asset strategy boundary established
- [x] Prompt compilation boundary established
- [x] Knowledge-gap handling established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-008 — Channel Projection Contract**

This specification will define how the canonical campaign intelligence and narrative are projected into individual channels without allowing channel-specific optimization to silently alter campaign strategy, intent, evidence requirements, or brand/product truth.
