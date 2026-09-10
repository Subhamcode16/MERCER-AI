# II-008 — Channel Projection Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Projection of canonical campaign intelligence and narrative into channel-specific execution structures

---

## 1. Purpose

II-008 defines how the Campaign Intelligence Layer projects a canonical campaign into individual communication channels without allowing channel-specific optimization to silently alter campaign strategy, product truth, evidence requirements, or locked intent.

The Channel Projection layer answers:

> **How should the canonical campaign meaning be adapted to the constraints, affordances, audience behavior, and format of a specific channel while preserving the campaign's authoritative semantic invariants?**

The layer is therefore an **adaptation boundary**, not a second strategy engine.

---

# 2. Core Principle

> **A channel projection may change how campaign meaning is delivered, but it must not silently change what the campaign means.**

Therefore:

```text
CANONICAL CAMPAIGN
        ↓
CHANNEL PROJECTION
        ↓
CHANNEL EXECUTION
```

must preserve:

```text
PRODUCT TRUTH
LOCKED INTENTS
HARD BRAND CONSTRAINTS
REQUIRED EVIDENCE
CANONICAL CAMPAIGN INVARIANTS
```

---

# 3. Canonical Projection Chain

```text
CAMPAIGN
   ↓
CANONICAL INTENTS
   ↓
CANONICAL EVIDENCE REQUIREMENTS
   ↓
CANONICAL ASSET STRATEGY
   ↓
CANONICAL NARRATIVE
   ↓
CHANNEL PROJECTION
   ↓
CHANNEL-SPECIFIC ASSET / SEQUENCE REQUIREMENTS
   ↓
CHANNEL EXECUTION
```

The projection layer must consume canonical intelligence rather than independently regenerating campaign strategy.

---

# 4. Channel Projection Definition

A Channel Projection is:

> **A channel-specific representation of the canonical campaign that adapts presentation, sequence, format, pacing, and deployment while preserving the campaign's authoritative semantic commitments.**

Examples may include:

```text
INSTAGRAM_FEED
INSTAGRAM_REEL
YOUTUBE_SHORT
WEBSITE_HERO
PRODUCT_PAGE
EMAIL
PAID_SOCIAL
```

The taxonomy remains extensible.

---

# 5. Projection vs Campaign Variant

This distinction is mandatory.

## Projection

Changes:

```text
format
sequence
pacing
entry point
asset selection
CTA presentation
channel-specific framing
```

while preserving campaign meaning.

## Campaign Variant

Deliberately changes strategic meaning.

```text
CAMPAIGN VARIANT
        ↓
VARIANT_OF
        ↓
MASTER CAMPAIGN
```

A channel projection must not secretly become a campaign variant.

If strategic meaning must change, the system must explicitly create or request a Variant.

---

# 6. Projection Object

Conceptually:

```text
projection_id
campaign_id
channel
parent_narrative_id
entry_point
selected_nodes
selected_assets
omitted_nodes
reordered_nodes
channel_constraints
required_intents
required_evidence
preserved_invariants
adaptation_rationale
authority
confidence
status
provenance
version
```

The exact implementation schema is deferred.

---

# 7. Channel Capability Model

Each channel should expose a capability profile.

Conceptually:

```text
CHANNEL
├── format_constraints
├── duration_constraints
├── aspect_constraints
├── interaction_model
├── audience_context
├── attention_model
├── asset_capabilities
├── text_capabilities
├── audio_capabilities
├── CTA_capabilities
└── platform_constraints
```

The projection engine uses these constraints to adapt the canonical narrative.

---

# 8. Channel Constraints

Constraints should be classified as:

```text
HARD
SOFT
PREFERENCE
```

### Hard

Cannot be violated.

Example:

```text
maximum supported duration
required format
technical publishing constraint
```

### Soft

May be traded off if required.

Example:

```text
preferred pacing
preferred asset count
preferred CTA placement
```

### Preference

Optimization guidance rather than a requirement.

The projection engine must not treat a preference as an invariant.

---

# 9. Canonical Invariants

Every projection must explicitly inherit or reference:

```text
PRODUCT_TRUTH
LOCKED_INTENTS
HARD_BRAND_CONSTRAINTS
REQUIRED_EVIDENCE
REQUIRED_NARRATIVE_INVARIANTS
```

A projection that cannot preserve a required invariant must be marked:

```text
BLOCKED
```

or:

```text
CHALLENGE_REQUIRED
```

rather than silently weakening the invariant.

---

# 10. Intent Preservation

A projection may compress or re-express an intent.

It may not silently remove a required intent.

Conceptually:

```text
CANONICAL INTENT
        ↓
CHANNEL EXPRESSION
```

The mapping must remain traceable.

Example:

```text
Canonical:
Communicate craftsmanship.

Channel:
Show construction detail within the first
available evidence-bearing sequence.
```

The channel expression changes.

The intent does not.

---

# 11. Evidence Preservation

Channel constraints may affect the **form** in which evidence appears.

They must not silently remove required evidence.

Example:

```text
Canonical Evidence:
Material structure must be perceptible.

Channel:
Short-form video

Projection:
Use a brief material-detail sequence.
```

The projection may alter:

```text
duration
placement
sequence
asset combination
```

but must preserve sufficient evidence.

---

# 12. Evidence Compression

When channel constraints require compression, the projection engine should seek:

```text
MULTI-PURPOSE EVIDENCE
```

rather than simply deleting evidence.

For example:

```text
One asset
→ product identity
→ material evidence
→ craftsmanship evidence
```

may be preferable to three separate assets if the contribution remains sufficient.

The Asset Strategy contract remains responsible for determining whether the asset is genuinely sufficient.

---

# 13. Narrative Adaptation

A projection may:

```text
OMIT
REORDER
COMPRESS
EXPAND
RE-ENTRY
```

narrative nodes where channel constraints require it.

However, it must preserve the semantic progression required by the canonical narrative.

Example:

```text
Canonical:
Context → Product → Proof → Desire

Projection:
Product → Proof → Desire
```

If context is omitted, the system must record:

```text
omitted_node = Context
reason = channel_constraint
impact = assessed
```

---

# 14. Narrative Reordering

Reordering is permitted only when semantic dependencies remain valid.

For example:

```text
REVEAL
```

cannot necessarily precede the information it logically depends on.

The projection engine must inspect:

```text
Narrative Edge
+
Evidence Dependency
+
Intent Dependency
```

before reordering nodes.

---

# 15. Channel Entry Points

A channel may use a different entry point into the canonical narrative.

Example:

```text
MASTER
        ↓
 ┌──────┼──────┐
 ↓      ↓      ↓
PRODUCT CONTEXT HUMAN
```

The selected entry point must preserve the required campaign meaning within the available attention window.

---

# 16. Channel-Specific Asset Selection

A projection may select a subset of canonical assets.

```text
CANONICAL ASSET SET
        ↓
CHANNEL FILTER
        ↓
SELECTED ASSETS
```

Selection must be justified by:

```text
intent contribution
evidence contribution
narrative contribution
channel utility
constraint compatibility
```

A channel should not receive arbitrary assets merely because they are available.

---

# 17. New Asset Requirements

A channel projection may discover that the canonical asset set cannot satisfy a channel-specific requirement.

Example:

```text
Canonical campaign
→ sufficient for website

Short-form video
→ requires a motion-specific asset
```

The projection should create:

```text
ASSET GAP / ASSET REQUEST
```

rather than directly bypassing Asset Strategy.

The request must flow back through the appropriate strategy layer.

---

# 18. Projection-Specific Asset Requirement

The architecture should distinguish:

```text
CANONICAL ASSET REQUIREMENT
```

from:

```text
CHANNEL-SPECIFIC ASSET REQUIREMENT
```

The latter exists because the channel has a unique execution need.

Example:

```text
Canonical:
Show craftsmanship.

Channel:
Short-form video requires a brief process transition.

Result:
Channel-specific asset requirement
supporting the canonical intent.
```

The channel requirement remains subordinate to campaign invariants.

---

# 19. Channel-Specific Creative Opportunity

A channel may expose opportunities that are not required by the canonical campaign.

These should be classified as:

```text
CREATIVE_OPPORTUNITY
```

rather than automatically becoming strategic requirements.

Examples:

```text
interactive behavior
platform-native transition
optional sound design
comment prompt
```

A creative opportunity cannot silently become a mandatory campaign objective.

---

# 20. Channel-Specific CTA

A CTA may change between channels.

Example:

```text
Website:
Explore collection

Social:
Learn more

Commerce:
Shop now
```

CTA adaptation is permitted provided it remains consistent with the campaign objective and channel authority.

A CTA that changes strategic intent must trigger a challenge.

---

# 21. Channel Audience Context

A channel projection may use channel-specific audience context.

However:

```text
CHANNEL CONTEXT
≠
NEW AUDIENCE TRUTH
```

If audience assumptions are inferred, they must retain uncertainty and provenance.

The projection layer must not fabricate audience facts simply to justify a preferred execution.

---

# 22. Channel Projection Confidence

Confidence should reflect how well the projection preserves campaign meaning under channel constraints.

For example:

```text
High:
All required intents and evidence preserved.

Medium:
Minor soft-constraint compromises.

Low:
Important evidence compressed or uncertain.

Blocked:
Hard invariant cannot be preserved.
```

Confidence does not alter authority.

```text
CONFIDENCE ≠ AUTHORITY
```

---

# 23. Projection Authority

The Channel Projection Agent may modify:

```text
channel sequence
format
pacing
entry point
channel asset selection
channel CTA expression
```

It may not silently modify:

```text
campaign objective
locked intent
product truth
hard brand constraint
canonical evidence requirement
```

If such a modification appears necessary:

```text
CHALLENGE
```

or:

```text
VARIANT REQUEST
```

must be produced.

---

# 24. Projection Challenge

A projection challenge should contain:

```text
projection_id
target_invariant
channel
constraint
reason
impact
evidence
recommended_action
severity
```

Possible outcomes:

```text
RESOLVED
ACCEPTED
REVISED
ESCALATED
BLOCKED
```

---

# 25. Cross-Channel Consistency

The system should maintain a canonical consistency view.

Conceptually:

```text
                    MASTER CAMPAIGN
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
       CHANNEL A       CHANNEL B       CHANNEL C
          │               │               │
          └───────┬───────┴───────┬───────┘
                  ↓
          CONSISTENCY CHECK
```

The goal is not identical execution.

The goal is:

```text
SEMANTIC CONSISTENCY
```

---

# 26. Allowed Channel Divergence

Divergence is acceptable when it concerns:

```text
format
pacing
asset ordering
entry point
CTA expression
channel-native interaction
presentation
```

Divergence becomes a strategic issue when it concerns:

```text
product truth
campaign objective
locked intent
hard brand meaning
required evidence
```

---

# 27. Projection Lineage

Every projection must preserve lineage:

```text
CHANNEL PROJECTION
        ↓
CANONICAL NARRATIVE
        ↓
CANONICAL ASSET / REQUIREMENT
        ↓
EVIDENCE
        ↓
INTENT
        ↓
OBJECTIVE
```

This allows the system to answer:

> Why does this channel asset or sequence exist?

without relying on retrospective LLM explanations.

---

# 28. Projection Alternatives

When multiple valid channel projections exist, preserve alternatives.

Example:

```text
Projection A:
Product-first

Projection B:
Human-first

Projection C:
Evidence-first
```

The system may rank them based on:

```text
intent preservation
evidence coverage
channel fit
narrative coherence
production efficiency
```

but must not claim uniqueness without evidence.

---

# 29. Projection Optimization

Conceptually:

```text
MAXIMIZE
    Intent Preservation
  + Evidence Sufficiency
  + Narrative Coherence
  + Channel Utility

MINIMIZE
    Constraint Violations
  + Unnecessary Assets
  + Redundancy
  + Complexity
  + Strategic Drift
```

Exact weights remain deferred.

---

# 30. Projection Failure States

The system must distinguish:

```text
VALID_PROJECTION
```

from:

```text
VALID_BUT_SUBOPTIMAL
```

from:

```text
MULTIPLE_VALID_PROJECTIONS
```

from:

```text
BLOCKED_BY_CHANNEL_CONSTRAINT
```

from:

```text
BLOCKED_BY_EVIDENCE_REQUIREMENT
```

from:

```text
REQUIRES_VARIANT
```

from:

```text
REQUIRES_NEW_ASSET
```

---

# 31. Self-Critique Requirements

The Self-Critique Agent should inspect projections for:

- strategic drift,
- missing required evidence,
- unjustified node removal,
- unjustified reordering,
- unsupported audience assumptions,
- excessive compression,
- channel constraint overreach,
- redundant assets,
- accidental campaign-variant creation,
- and loss of provenance.

The critic must produce a critique record rather than silently changing the projection.

---

# 32. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break Channel Projection by:

1. Removing a locked intent.
2. Removing required evidence while claiming preservation.
3. Reordering nodes across dependency boundaries.
4. Turning a projection into an undeclared campaign variant.
5. Introducing unsupported audience assumptions.
6. Using channel preferences as hard constraints.
7. Creating platform-specific strategic drift.
8. Severing projection lineage.
9. Injecting unnecessary assets.
10. Creating contradictory CTAs.
11. Exploiting compression to hide evidence loss.
12. Creating different product truths across channels.
13. Bypassing Asset Strategy for new channel assets.
14. Treating creative opportunities as mandatory strategic requirements.

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

# 33. Validation Invariants

### Invariant 1

Every projection traces to a canonical campaign and narrative.

### Invariant 2

Every required canonical intent is either preserved or explicitly challenged.

### Invariant 3

Every required evidence requirement is either preserved, satisfied through an approved equivalent, or explicitly challenged.

### Invariant 4

Channel constraints cannot silently override hard campaign constraints.

### Invariant 5

A projection cannot silently become a campaign variant.

### Invariant 6

Projection-specific assets must retain lineage to canonical intent or explicitly declared channel opportunity.

### Invariant 7

Channel preferences cannot be treated as hard constraints without authorization.

### Invariant 8

Projection confidence is distinct from authority.

### Invariant 9

Channel divergence must be classifiable as presentation divergence or strategic divergence.

### Invariant 10

Strategic divergence requires explicit review.

### Invariant 11

Projection changes preserve provenance.

### Invariant 12

A projection cannot silently mutate the canonical narrative.

---

# 34. Falsifiable Architectural Hypotheses

## Hypothesis A — Canonical narrative plus projection reduces cross-channel strategic drift

**Claim:**

Maintaining one canonical campaign narrative and deriving channel projections preserves semantic consistency better than independently generating channel campaigns.

**Experiment:**

Compare:

```text
System A:
Independent channel generation

System B:
Canonical campaign → projections
```

Measure:

- intent preservation,
- evidence preservation,
- product-truth consistency,
- strategic drift,
- human correction rate.

---

## Hypothesis B — Explicit invariant tracking prevents hidden evidence loss

**Claim:**

Tracking required intents and evidence explicitly reduces cases where channel compression silently removes campaign-critical meaning.

**Experiment:**

Create constrained channels with limited capacity.

Measure:

```text
required evidence preserved?
missing evidence detected?
false preservation claims?
```

---

## Hypothesis C — Projection/Variant separation prevents strategic contamination

**Claim:**

Explicitly distinguishing channel adaptation from strategic variants reduces undeclared strategic changes.

**Experiment:**

Introduce channel requirements that appear to justify changing campaign meaning.

Expected:

```text
CHALLENGE / VARIANT REQUEST
```

rather than silent mutation.

---

## Hypothesis D — Channel capability modeling improves adaptation quality

**Claim:**

Explicit channel capability profiles produce better projections than generic prompt-level channel instructions.

**Experiment:**

Compare channel projections generated with:

```text
generic channel prompt
vs
structured capability profile
```

Measure constraint violations and semantic preservation.

---

# 35. Projection Evaluation

Every projection should eventually expose:

```text
INTENT PRESERVATION
EVIDENCE PRESERVATION
NARRATIVE PRESERVATION
CHANNEL FIT
PRODUCT TRUTH
BRAND CONSTRAINTS
ASSET EFFICIENCY
STRATEGIC DRIFT
```

No single aggregate score should replace these diagnostic dimensions.

---

# 36. Channel Projection vs Asset Strategy Boundary

```text
Asset Strategy
→ Determines what assets should exist.

Channel Projection
→ Determines which canonical assets and requirements
  are appropriate for this channel.
```

If the channel requires an asset that does not exist:

```text
CHANNEL PROJECTION
        ↓
ASSET GAP
        ↓
ASSET STRATEGY
```

The projection must not bypass this dependency.

---

# 37. Channel Projection vs Narrative Boundary

```text
Narrative Engine
→ Canonical campaign progression.

Channel Projection
→ Channel-specific expression of that progression.
```

The projection may adapt but not silently redefine.

---

# 38. Channel Projection vs Prompt Compilation Boundary

The projection may specify:

```text
format
duration
aspect
sequence
asset role
channel placement
```

It must not produce model-specific final generation prompts.

The chain remains:

```text
CHANNEL PROJECTION
        ↓
ASSET SPECIFICATION
        ↓
PROMPT COMPILATION
        ↓
GENERATION
```

---

# 39. Knowledge Gap Handling

When channel-specific decisions depend on uncertain knowledge:

```text
UNKNOWN
    ↓
KNOWLEDGE GAP
    ↓
PROJECTION IMPACT
```

The system may produce:

```text
CONDITIONAL PROJECTIONS
ALTERNATIVE PROJECTIONS
RESEARCH REQUEST
ESCALATION
```

It must not silently convert uncertainty into channel truth.

---

# 40. Core Contract

> **The Channel Projection Engine shall adapt canonical campaign intelligence and narrative to channel-specific constraints and opportunities while preserving product truth, locked communication intent, required evidence, hard brand constraints, and canonical narrative invariants. It shall distinguish projection from strategic variation, preserve lineage and provenance, surface evidence loss and strategic divergence, route new asset requirements through Asset Strategy, and support explicit alternatives, self-critique, and adversarial verification.**

---

# 41. Deferred Decisions

II-008 does not freeze:

- final channel taxonomy,
- channel capability schemas,
- exact platform integrations,
- numerical channel-fit scoring,
- projection optimization algorithms,
- audience modeling implementation,
- publishing APIs,
- runtime schema,
- prompt implementation.

These remain subjects for later specifications and engineering.

---

# 42. Exit Criteria

II-008 is semantically complete when:

- [x] Channel Projection definition established
- [x] Projection / Variant boundary established
- [x] Projection object defined conceptually
- [x] Channel capability model established
- [x] Hard / soft / preference constraints established
- [x] Canonical invariant preservation established
- [x] Intent preservation established
- [x] Evidence preservation established
- [x] Evidence compression established
- [x] Narrative adaptation established
- [x] Entry-point adaptation established
- [x] Channel-specific asset requirements established
- [x] Creative opportunity boundary established
- [x] CTA adaptation boundary established
- [x] Projection authority established
- [x] Cross-channel consistency established
- [x] Projection lineage established
- [x] Alternative projections established
- [x] Failure states established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Asset Strategy boundary established
- [x] Narrative boundary established
- [x] Prompt Compiler boundary established
- [x] Knowledge-gap handling established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-009 — Creative Search & Knowledge Retrieval Contract**

This specification will define how the intelligence layer retrieves, ranks, validates, and incorporates external/internal knowledge and creative references without allowing retrieval results to silently become authoritative campaign truth.
