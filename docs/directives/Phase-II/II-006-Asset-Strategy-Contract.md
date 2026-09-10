# II-006 — Asset Strategy Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Translation of Evidence Requirements into an optimal, explainable asset strategy

---

## 1. Purpose

II-006 defines how the Campaign Intelligence Layer converts accepted Evidence Requirements into an **optimal asset strategy**.

The Asset Strategy layer answers:

> **What is the smallest, strongest, strategically coherent set of assets required to satisfy the campaign's evidence and communication objectives?**

It does not merely generate a list of images.

It performs constrained reasoning over:

- evidence coverage,
- asset roles,
- asset capabilities,
- redundancy,
- marginal evidence value,
- narrative contribution,
- channel requirements,
- production constraints,
- cross-domain products,
- and campaign priorities.

---

# 2. Core Principle

> **Asset count is not the optimization target. Evidence coverage and campaign utility are.**

Therefore:

```text
MORE ASSETS
≠
BETTER CAMPAIGN
```

The preferred solution is:

```text
MAXIMUM REQUIRED COVERAGE
+
MINIMUM UNNECESSARY REDUNDANCY
+
STRATEGIC COHERENCE
+
PRODUCTION FEASIBILITY
```

---

# 3. Canonical Strategy Chain

```text
COMMUNICATION INTENTS
        ↓
EVIDENCE REQUIREMENTS
        ↓
CANDIDATE ASSET CAPABILITIES
        ↓
COVERAGE MATRIX
        ↓
CONSTRAINT ANALYSIS
        ↓
REDUNDANCY ANALYSIS
        ↓
MARGINAL VALUE ANALYSIS
        ↓
ASSET SET OPTIMIZATION
        ↓
ASSET REQUIREMENTS
        ↓
NARRATIVE / CHANNEL INTEGRATION
```

The optimizer operates before concrete generation prompts.

---

# 4. Asset Requirement vs Asset

The distinction established in II-002 remains mandatory.

```text
ASSET REQUIREMENT
=
What the campaign needs to exist.

ASSET
=
A concrete realization that satisfies or attempts
to satisfy that requirement.
```

The Asset Strategy Engine primarily creates and optimizes:

```text
ASSET REQUIREMENTS
```

rather than directly generating images.

---

# 5. Asset Role

Every required asset should have one or more semantic roles.

Potential roles include:

```text
PRODUCT_IDENTITY
MATERIAL_PROOF
CRAFTSMANSHIP_PROOF
CONSTRUCTION_PROOF
FUNCTION_PROOF
BRAND_EXPRESSION
DESIRE
TRUST
CONTEXT
CULTURAL_CONTEXT
HUMAN_INTERACTION
CONVERSION
NARRATIVE_TRANSITION
```

This remains a provisional ontology.

Role is distinct from:

```text
SHOT FAMILY
FORMAT
CAMERA
LIGHTING
PROMPT
```

---

# 6. Asset Capability

An asset candidate is described by what evidence it is capable of providing.

Conceptually:

```text
ASSET CANDIDATE
├── roles
├── evidence_dimensions
├── evidence_strengths
├── narrative_capabilities
├── channel_capabilities
├── product_coverage
├── production_cost
├── risk
└── constraints
```

This allows strategy to reason about assets before selecting exact execution parameters.

---

# 7. Coverage Matrix

The optimizer should construct a conceptual matrix:

```text
                    E1   E2   E3   E4
Asset A             H    M    0    0
Asset B             0    H    H    M
Asset C             M    0    H    H
Asset D             H    0    0    L
```

Where:

```text
H = strong contribution
M = moderate contribution
L = low contribution
0 = no meaningful contribution
```

This matrix is conceptual. Numerical scoring is deferred.

The matrix allows the system to reason about:

- coverage,
- overlap,
- gaps,
- and redundancy.

---

# 8. Set-Level Optimization

The optimizer must evaluate the **asset set**, not merely individual asset quality.

An individually excellent asset may be unnecessary if another selected asset already provides equivalent evidence.

Therefore:

```text
ASSET QUALITY
+
SET COVERAGE
+
MARGINAL VALUE
```

must be evaluated together.

---

# 9. Marginal Evidence Value

For each candidate asset:

> **How much additional campaign evidence does this asset provide beyond the assets already selected?**

Conceptually:

```text
Marginal Value(A)
=
Coverage(A ∪ Selected)
-
Coverage(Selected)
```

The exact mathematical formulation is deliberately deferred.

The principle is mandatory.

---

# 10. Redundancy

Redundancy is not automatically bad.

Two assets may overlap while serving different purposes.

Example:

```text
Asset A:
Material detail

Asset B:
Human interaction showing the same material
```

They overlap in material evidence but may differ in:

```text
context
desire
human association
narrative role
```

Therefore redundancy must be evaluated at the **semantic contribution level**, not by visual similarity alone.

---

# 11. Harmful Redundancy

An asset becomes harmful redundancy when:

```text
Incremental Evidence Value ≈ 0
```

and:

```text
Narrative Value ≈ 0
```

and:

```text
Channel Value ≈ 0
```

while still consuming:

```text
production cost
attention
generation budget
or campaign space
```

Such assets should normally be removed.

---

# 12. Multi-Purpose Assets

A single asset may legitimately satisfy multiple requirements.

Example:

```text
Asset A
├── Product Identity
├── Material Proof
├── Craftsmanship Proof
└── Brand Expression
```

Multi-purpose assets are valuable when they provide **genuine independent contributions**.

The optimizer must not inflate their value simply because they are linked to many requirements.

---

# 13. Evidence Saturation Constraint

The optimizer should recognize when additional assets no longer materially improve a requirement.

Conceptually:

```text
Evidence Requirement
        ↓
Asset 1
        ↓
Asset 2
        ↓
Sufficient
        ↓
Asset 3
        ↓
Low Marginal Value
        ↓
Reject unless another strategic role exists
```

This is a core mechanism for controlling asset proliferation.

---

# 14. Asset Necessity

Each selected asset should eventually have a defensible reason for existing.

Possible necessity classes:

```text
REQUIRED
HIGH_VALUE
SUPPORTING
OPTIONAL
EXPLORATORY
```

An asset should not be marked `REQUIRED` merely because it is visually desirable.

It must satisfy a meaningful campaign requirement or locked strategic condition.

---

# 15. Asset Strategy Constraints

The optimizer must consider at least:

```text
Evidence Requirements
Campaign Objectives
Brand Constraints
Product Truth
Production Constraints
Channel Requirements
Narrative Requirements
Asset Diversity
Asset Redundancy
Cross-Domain Conflicts
```

Additional constraints may be introduced by later specifications.

---

# 16. Hard vs Soft Constraints

### Hard constraints

Must not be violated.

Examples:

```text
Product truth
Locked brand constraints
Locked campaign intent
Required evidence
Legal / factual constraints
Explicit production limitations
```

### Soft constraints

May be traded off.

Examples:

```text
Preferred visual variety
Preferred shot family
Optional narrative embellishment
Preferred channel adaptation
Creative exploration
```

The optimizer must distinguish these classes.

---

# 17. Optimization Objective

The conceptual optimization target is:

```text
MAXIMIZE
    Evidence Coverage
  + Strategic Utility
  + Narrative Utility
  + Channel Utility
  + Asset Diversity

MINIMIZE
    Redundancy
  + Production Cost
  + Complexity
  + Risk
  + Unnecessary Asset Count
```

This is a conceptual objective, not yet a frozen mathematical formula.

---

# 18. Lexicographic Priority

When optimization objectives conflict, the system should first protect:

```text
1. Product Truth
2. Hard Constraints
3. Locked Strategic Intent
4. Required Evidence
5. Campaign Coherence
6. Channel Requirements
7. Narrative Optimization
8. Creative Preferences
9. Asset Efficiency
```

The exact ordering may be revised during validation.

The important principle is that creative optimization cannot trade away higher-order invariants silently.

---

# 19. Asset Diversity

Diversity should not mean:

```text
"Make every image look different."
```

It should mean:

> **Provide meaningfully different evidence, narrative, contextual, or channel contributions where those differences improve the campaign.**

Therefore diversity should be evaluated semantically.

Potential diversity dimensions:

```text
evidence dimension
perspective
context
human interaction
product state
narrative role
channel role
visual scale
```

---

# 20. Multi-Product / Cross-Domain Campaigns

A campaign may contain multiple products with competing evidence requirements.

Example:

```text
Apparel:
requires soft, diffused treatment.

Footwear:
benefits from stronger directional definition.

Jewelry:
requires controlled highlight behavior.
```

The Asset Strategy layer must **not automatically force one universal execution treatment** merely because the products coexist in one scene.

Instead it should determine whether:

```text
ONE ASSET
```

can satisfy all requirements sufficiently.

If not:

```text
MULTI-ASSET STRATEGY
```

should be considered.

---

# 21. Cross-Domain Asset Strategy

For a shared scene:

```text
APPAREL
+
FOOTWEAR
+
JEWELRY
```

the optimizer should evaluate:

```text
Shared Evidence
Shared Lighting Compatibility
Shared Composition
Shared Product Visibility
Shared Narrative Role
```

against:

```text
Domain-Specific Evidence
Domain-Specific Constraints
Conflict Severity
```

If a single asset creates unacceptable evidence loss, splitting the requirements is preferable.

---

# 22. Conflict Classification

Cross-domain conflicts should be classified:

```text
COMPATIBLE
TOLERABLE_TENSION
TRADEOFF
INCOMPATIBLE
```

The Asset Strategy layer may resolve:

```text
COMPATIBLE
TOLERABLE_TENSION
```

through optimization.

It should escalate:

```text
INCOMPATIBLE
```

conditions rather than silently sacrificing a hard requirement.

---

# 23. Asset Set Types

The optimizer may conceptually generate:

```text
CORE SET
```

Assets necessary for strategic and evidence sufficiency.

```text
SUPPORTING SET
```

Assets that improve narrative or channel utility.

```text
EXPLORATORY SET
```

Optional assets used for creative exploration.

The final campaign should not accidentally treat exploratory assets as mandatory.

---

# 24. Candidate Generation

Candidate asset requirements may be generated from:

```text
Evidence Requirements
Narrative Needs
Channel Needs
Multi-purpose Opportunities
Known Asset Patterns
Domain Knowledge
Creative Search Results
```

Candidate generation should produce alternatives rather than immediately committing to one.

---

# 25. Candidate Evaluation

Each candidate should conceptually be evaluated on:

```text
Evidence Contribution
Marginal Value
Strategic Utility
Narrative Utility
Channel Utility
Redundancy
Cost
Risk
Constraint Compatibility
Confidence
```

This creates an explicit decision surface.

---

# 26. Asset Strategy Decision Record

Every selected asset requirement should eventually expose:

```text
asset_requirement_id
selected
reason
evidence_supported
marginal_value
strategic_role
narrative_role
channel_roles
constraints
alternatives_considered
rejected_alternatives
confidence
provenance
```

This is essential for explainability.

The system must be able to answer:

> Why did we choose this asset requirement instead of another one?

---

# 27. Alternative Sets

The optimizer should be capable of producing more than one valid strategy when trade-offs are genuine.

For example:

```text
STRATEGY A
6 assets
High evidence coverage
Low narrative diversity

STRATEGY B
7 assets
Similar evidence coverage
Higher narrative utility

STRATEGY C
5 assets
Lower production cost
Slightly lower evidence redundancy
```

The system should not pretend that optimization always produces one objectively unique answer.

A human or higher-level strategy layer may choose among Pareto-valid alternatives.

---

# 28. Pareto Principle

When no strategy dominates another across all relevant dimensions, preserve the alternatives.

Conceptually:

```text
STRATEGY A
better evidence

STRATEGY B
better narrative

STRATEGY C
lower production cost
```

Do not collapse these into a fake single optimum without a declared preference function.

---

# 29. Asset Strategy and Narrative

Asset selection should account for narrative utility, but narrative sequencing belongs to II-007.

Therefore:

```text
Asset Strategy
→ identifies narrative capability

Narrative Engine
→ determines narrative arrangement
```

The Asset Strategy layer must not independently invent the complete narrative.

---

# 30. Asset Strategy and Channels

Likewise:

```text
Asset Strategy
→ identifies potential channel utility

Channel Projection
→ determines channel-specific deployment
```

A candidate asset may be valuable because it can serve multiple channels, but final channel assignment belongs downstream.

---

# 31. Asset Strategy and Prompt Compilation

The Asset Strategy layer must not produce final prompts.

It produces:

```text
ASSET REQUIREMENTS
```

which later become:

```text
ASSET SPECIFICATIONS
```

and eventually:

```text
PROMPT
```

The separation remains:

```text
STRATEGY
→ REQUIREMENT
→ SPECIFICATION
→ PROMPT
→ GENERATION
```

---

# 32. Asset Strategy and Knowledge Gaps

When asset optimization depends on unknown information:

```text
UNKNOWN
    ↓
KNOWLEDGE GAP
    ↓
AFFECTED ASSET STRATEGY
```

The optimizer should not silently assume a value if the assumption could materially change the selected asset set.

Possible outcomes:

```text
REQUEST KNOWLEDGE
DEFER DECISION
GENERATE CONDITIONAL STRATEGIES
ESCALATE
```

---

# 33. Conditional Strategies

When uncertainty materially affects optimization, the system may preserve alternatives.

Example:

```text
IF material = reflective
    → Strategy A

IF material = matte
    → Strategy B
```

This is preferable to silently choosing one assumption.

---

# 34. Self-Critique Requirements

The Self-Critique Agent should review the Asset Strategy for:

- unnecessary assets,
- unsupported asset requirements,
- evidence gaps,
- false multi-purpose claims,
- redundancy,
- hidden hard-constraint violations,
- premature execution decisions,
- unjustified optimization preferences,
- ignored alternatives,
- and unexplained selections.

It should challenge the strategy without silently rewriting it.

---

# 35. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break Asset Strategy by:

1. Injecting redundant assets.
2. Removing critical evidence assets.
3. Claiming zero-marginal-value assets are necessary.
4. Inflating the value of multi-purpose assets.
5. Exploiting evidence overlap.
6. Forcing incompatible product domains into one asset.
7. Bypassing hard constraints for efficiency.
8. Hiding production-cost assumptions.
9. Creating fake Pareto alternatives.
10. Removing provenance from asset decisions.
11. Making a downstream visual preference override strategy.
12. Creating circular asset dependencies.
13. Exploiting uncertain knowledge as if it were known.
14. Producing a large asset set to appear more comprehensive.

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

# 36. Validation Invariants

### Invariant 1

Every required asset requirement traces to at least one strategic, evidence, narrative, or channel need.

### Invariant 2

Every selected asset requirement has an explicit rationale.

### Invariant 3

No asset is required solely because it is visually attractive.

### Invariant 4

Hard constraints cannot be traded away for efficiency without explicit escalation.

### Invariant 5

Marginal evidence value must be considered when evaluating additional assets.

### Invariant 6

Evidence redundancy does not automatically equal strategic redundancy.

### Invariant 7

Multi-purpose assets must demonstrate genuine contribution across their claimed requirements.

### Invariant 8

The optimizer cannot silently resolve incompatible cross-domain requirements.

### Invariant 9

Asset Strategy cannot silently rewrite Communication Intent.

### Invariant 10

Asset Strategy cannot silently become the final narrative.

### Invariant 11

Asset Strategy cannot silently become channel-specific execution.

### Invariant 12

Asset Strategy cannot produce final generation prompts.

### Invariant 13

Unresolved knowledge gaps that materially affect optimization must remain visible.

### Invariant 14

Rejected alternatives and their reasons should remain recoverable for explainability.

---

# 37. Falsifiable Architectural Hypotheses

## Hypothesis A — Evidence-first asset strategy reduces unnecessary asset generation

**Claim:**

Deriving assets from evidence requirements produces smaller and more coherent asset sets than direct shot-list generation.

**Experiment:**

Compare:

```text
System A:
Campaign → Shot List

System B:
Campaign → Intent → Evidence → Asset Strategy
```

Measure:

- evidence coverage,
- asset count,
- redundancy,
- human correction,
- strategic coherence.

---

## Hypothesis B — Marginal-value optimization reduces redundant assets

**Claim:**

Explicit marginal evidence value reduces near-duplicate asset selection without reducing required coverage.

**Experiment:**

Provide candidate pools containing highly redundant assets.

Measure:

```text
coverage maintained?
asset count reduced?
important evidence lost?
```

---

## Hypothesis C — Semantic redundancy is more reliable than visual similarity

**Claim:**

Two visually different assets can be strategically redundant, while visually similar assets can provide distinct campaign value.

**Experiment:**

Create paired examples and compare:

```text
visual similarity
vs
semantic contribution overlap
```

Evaluate whether semantic analysis better predicts true redundancy.

---

## Hypothesis D — Multi-purpose assets improve efficiency only when contribution is genuine

**Claim:**

Allowing multi-purpose assets can reduce asset count without reducing evidence coverage, provided contribution is evaluated per relationship.

**Experiment:**

Compare relationship-aware attribution against naive "supports many requirements" scoring.

---

## Hypothesis E — Preserving Pareto alternatives improves strategic decision quality

**Claim:**

When objectives genuinely conflict, exposing multiple Pareto-valid strategies produces better decisions than forcing a single opaque optimum.

**Experiment:**

Present human evaluators with:

```text
single opaque optimum
vs
explicit Pareto alternatives
```

Measure strategic preference consistency and correction rate.

---

# 38. Asset Strategy Evaluation

At the end of optimization, the system should produce a strategy evaluation:

```text
TOTAL REQUIREMENTS
        ↓
COVERED REQUIREMENTS
        ↓
SUFFICIENT REQUIREMENTS
        ↓
UNRESOLVED REQUIREMENTS
        ↓
SELECTED ASSETS
        ↓
REDUNDANCY
        ↓
MARGINAL VALUE
        ↓
CONSTRAINT STATUS
        ↓
ALTERNATIVE STRATEGIES
```

This creates a measurable decision surface before generation begins.

---

# 39. Asset Strategy Failure States

The system should distinguish:

```text
NO_VALID_STRATEGY
```

from:

```text
VALID_BUT_SUBOPTIMAL
```

and:

```text
VALID_MULTIPLE_STRATEGIES
```

and:

```text
BLOCKED_BY_KNOWLEDGE_GAP
```

and:

```text
BLOCKED_BY_CONSTRAINT_CONFLICT
```

This distinction is important for downstream replanning.

---

# 40. Core Contract

> **The Asset Strategy Engine shall transform validated Evidence Requirements into a minimal, sufficient, strategically coherent, and explainable set of Asset Requirements while maximizing meaningful evidence coverage and campaign utility and minimizing unnecessary redundancy, cost, complexity, and risk. It shall evaluate assets at the set level, account for marginal evidence value and genuine multi-purpose contribution, surface cross-domain conflicts and consequential knowledge gaps, preserve alternative strategies where trade-offs are real, and remain separate from final narrative, channel execution, and prompt compilation.**

---

# 41. Deferred Decisions

II-006 does not freeze:

- exact optimization algorithm,
- numerical scoring function,
- utility weights,
- final asset ontology,
- exact redundancy metric,
- Pareto implementation,
- production-cost model,
- candidate-generation model,
- database schema,
- runtime implementation.

These remain subjects for later specifications and empirical validation.

---

# 42. Exit Criteria

II-006 is semantically complete when:

- [x] Asset Requirement / Asset distinction established
- [x] Asset roles established
- [x] Asset capability model established
- [x] Coverage matrix established
- [x] Set-level optimization established
- [x] Marginal evidence value established
- [x] Redundancy model established
- [x] Multi-purpose asset model established
- [x] Evidence saturation integrated
- [x] Hard / soft constraint model established
- [x] Optimization objective established
- [x] Lexicographic priority established provisionally
- [x] Asset diversity defined semantically
- [x] Cross-domain strategy established
- [x] Conflict classification established
- [x] Core / Supporting / Exploratory sets established
- [x] Pareto alternatives established
- [x] Knowledge-gap handling established
- [x] Conditional strategies established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Narrative boundary established
- [x] Channel boundary established
- [x] Prompt compilation boundary established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-007 — Narrative Graph Contract**

This specification will define how selected assets become a coherent campaign narrative, including narrative states, transitions, sequencing, information progression, emotional progression, asset-to-node mapping, channel projection, and narrative validation.
