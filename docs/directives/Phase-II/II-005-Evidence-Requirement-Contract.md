# II-005 — Evidence Requirement Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Translation of Communication Intents into measurable, traceable, and evaluable Evidence Requirements

---

## 1. Purpose

II-005 defines how accepted Communication Intents are translated into **Evidence Requirements**.

The purpose is to establish a disciplined bridge between:

```text
COMMUNICATION MEANING
        ↓
REQUIRED EVIDENCE
        ↓
ASSET STRATEGY
```

The Evidence Requirement is therefore not a shot, prompt, image, lighting setup, or camera instruction.

It is a statement of:

> **What must be perceptibly demonstrated for a Communication Intent to be sufficiently supported.**

---

# 2. Core Principle

> **An intent describes what the audience should understand, perceive, believe, feel, or do. An evidence requirement describes what must be observable or demonstrable for that intent to be credibly supported.**

Therefore:

```text
INTENT ≠ EVIDENCE
```

and:

```text
EVIDENCE ≠ ASSET
```

and:

```text
EVIDENCE ≠ PROMPT
```

The architecture must preserve these boundaries.

---

# 3. Canonical Translation Chain

The canonical chain is:

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
OBSERVATION / EVALUATION
```

Example:

```text
INTENT:
Make craftsmanship perceptible.

        ↓

EVIDENCE:
Visible construction detail,
material structure, and authentic
finish behavior.

        ↓

ASSET REQUIREMENT:
An asset capable of revealing
construction quality at sufficient
visual scale.

        ↓

ASSET:
Generated detail / interaction asset.

        ↓

EVALUATION:
Was craftsmanship actually perceptible?
```

---

# 4. Evidence Definition

An Evidence Requirement is a **semantic requirement for observable support**.

It answers:

> What would an evaluator need to observe to conclude that this intent has meaningful support?

It should describe:

- the evidence dimension,
- the required strength,
- the acceptable evidence form,
- the preferred evidence form,
- and the conditions under which the evidence becomes sufficient.

---

# 5. Evidence Must Be Observable

An evidence requirement must ultimately correspond to something that can be evaluated.

Weak:

```text
"Make it premium."
```

Better:

```text
"Demonstrate material quality through visible
surface structure, controlled construction detail,
and believable material behavior."
```

The second can be evaluated.

The first is primarily an intent or desired perception.

---

# 6. Evidence Dimensions

Evidence dimensions represent **what aspect of reality or communication must be demonstrated**.

Potential dimensions include:

```text
PRODUCT_IDENTITY
MATERIAL
CRAFTSMANSHIP
CONSTRUCTION
FIT
FORM
TEXTURE
COLOR
FUNCTION
SCALE
CONTEXT
CULTURAL_REFERENCE
BRAND_EXPRESSION
AUTHENTICITY
QUALITY
USE
HUMAN_INTERACTION
EMOTIONAL_STATE
```

This is a provisional vocabulary.

The final ontology should remain domain-extensible rather than becoming a closed universal enum prematurely.

---

# 7. Evidence Strength

Evidence Requirements must express how strongly the evidence needs to appear.

Conceptually:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

However, the exact numerical mapping must not yet be frozen.

Strength is a **requirement property**, not a generation instruction.

For example:

```text
Evidence:
Material texture

Required strength:
HIGH
```

does not automatically mean:

```text
Macro shot
Hard light
85mm lens
```

Those decisions belong downstream.

---

# 8. Evidence Sufficiency

The system must distinguish:

```text
REPRESENTED
```

from:

```text
SUFFICIENT
```

and:

```text
SATURATED
```

### REPRESENTED

Some relevant evidence exists.

### SUFFICIENT

Enough evidence exists to support the corresponding intent at the required strength.

### SATURATED

Additional evidence provides little or no meaningful incremental support.

This distinction is essential for asset-set optimization.

---

# 9. Evidence Saturation

More assets do not automatically mean stronger evidence.

Example:

```text
Evidence Requirement:
Material authenticity

Asset 1 → strong support
Asset 2 → moderate support
Asset 3 → strong support
Asset 4 → nearly identical to Asset 1
Asset 5 → nearly identical to Asset 1
```

The fifth asset may increase asset count without meaningfully increasing evidence.

Therefore the intelligence layer must eventually model:

```text
MARGINAL EVIDENCE VALUE
```

rather than simple asset count.

This becomes an important input to the Asset Strategy and Optimization contracts.

---

# 10. Evidence Contribution

An asset may contribute evidence to one or more Evidence Requirements.

```text
ASSET
 ├── contributes → EVIDENCE-A
 ├── contributes → EVIDENCE-B
 └── contributes → EVIDENCE-C
```

The contribution itself should carry semantic metadata:

```text
evidence_dimension
contribution_strength
confidence
provenance
```

The same asset can therefore provide:

```text
HIGH support
```

for one requirement and:

```text
LOW support
```

for another.

---

# 11. Evidence Requirement Object

Conceptually:

```text
evidence_requirement_id
intent_id
statement
evidence_dimension
required_strength
acceptable_forms
preferred_forms
minimum_conditions
sufficiency_conditions
saturation_conditions
priority
authority
confidence
provenance
status
created_by
created_at
version
```

This is a semantic contract, not yet a runtime schema.

---

# 12. Acceptable vs Preferred Evidence

The architecture must distinguish:

```text
ACCEPTABLE
```

from:

```text
PREFERRED
```

Example:

```text
Intent:
Communicate craftsmanship.

Acceptable:
Construction detail visible in a product or
human-interaction asset.

Preferred:
Detailed visual evidence of construction
at a scale where material and finishing
behavior remain perceptible.
```

This prevents the system from confusing optimization preference with hard necessity.

---

# 13. Evidence Form

Evidence form describes **how the evidence may manifest**, without prescribing a final shot.

Examples:

```text
PRODUCT_DETAIL
HUMAN_INTERACTION
FULL_PRODUCT
ENVIRONMENTAL_CONTEXT
MATERIAL_CLOSE_VIEW
PROCESS_DETAIL
COMPARATIVE_VIEW
USE_CONTEXT
```

Forms remain semantic.

The Asset Strategy layer decides which concrete asset realization is optimal.

---

# 14. Minimum Evidence Conditions

A requirement should specify the minimum conditions under which evidence can count.

Example:

```text
Evidence Dimension:
Material

Minimum Conditions:
- material surface is visible
- texture is not obscured
- relevant physical behavior remains perceptible
- visual quality is sufficient for evaluation
```

The minimum conditions must be domain- and requirement-specific.

---

# 15. Sufficiency Conditions

Sufficiency defines when evidence has crossed the threshold required by the intent.

Conceptually:

```text
OBSERVATION
    ↓
MEETS MINIMUM CONDITIONS
    ↓
EVIDENCE STRENGTH
    ↓
REQUIRED STRENGTH
    ↓
SUFFICIENT
```

Sufficiency should be evaluated against the actual communication requirement rather than a generic visual-quality score.

---

# 16. Evidence Is Not Visual Quality

A visually beautiful image may provide poor evidence.

Example:

```text
Beautiful editorial portrait
+
soft lighting
+
excellent composition
```

may still fail:

```text
Material construction evidence
```

if the relevant construction details cannot be observed.

Therefore:

```text
VISUAL QUALITY ≠ EVIDENCE SUFFICIENCY
```

The two dimensions must be evaluated separately.

---

# 17. Evidence Is Not Authenticity Alone

Likewise:

```text
Authentic material rendering
```

does not automatically prove:

```text
Craftsmanship
```

unless the relevant craftsmanship characteristics are actually observable.

Evidence must be tied to the specific intent.

---

# 18. Evidence Dependencies

Evidence Requirements may depend on one another.

Example:

```text
Product Identity
        ↓
Material Identification
        ↓
Material Authenticity
        ↓
Craftsmanship Interpretation
```

However, dependency must not automatically imply that one requirement is sufficient to satisfy another.

The graph should explicitly represent:

```text
DEPENDS_ON
```

and:

```text
SATISFIES
```

as different relationships.

---

# 19. Evidence Conflicts

Conflicts may occur between evidence requirements.

Examples:

```text
Requirement A:
Soft diffused light required to reveal delicate fabric.

Requirement B:
Hard directional light preferred to reveal
surface structure.

```

The Evidence layer should not resolve such conflicts by choosing a lighting setup.

Instead it should record:

```text
EVIDENCE TENSION
```

and pass the competing requirements to the Asset Strategy / Constraint layer.

This preserves separation of responsibilities.

---

# 20. Evidence Priority

Evidence requirements may have different priorities.

Conceptually:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

Priority is distinct from:

```text
Authority
Strength
Confidence
```

For example:

```text
Authority:
DERIVED

Priority:
CRITICAL

Confidence:
0.82
```

These dimensions must remain separate.

---

# 21. Evidence Authority

Evidence Requirements inherit their authority from the intent unless explicitly overridden by a higher-authority source.

Example:

```text
LOCKED EXPLICIT INTENT
        ↓
Evidence Requirement
```

The Evidence Agent cannot use an evidence interpretation to silently weaken the parent intent.

If evidence is impossible:

```text
CHALLENGE
```

rather than:

```text
SILENTLY LOWER REQUIREMENT
```

---

# 22. Evidence Uncertainty

Evidence Requirements may contain uncertainty.

Example:

```text
Evidence Dimension:
Cultural identity

Confidence:
0.61

Reason:
Cultural relevance is inferred from audience
and brand context rather than explicitly specified.
```

The uncertainty must remain visible.

The system should not present:

```text
0.61 confidence
```

as:

```text
certain campaign truth
```

---

# 23. Evidence Provenance

Every Evidence Requirement must be traceable to:

```text
Intent
    ↓
Intent provenance
    ↓
Supporting knowledge
```

The system should be able to answer:

> Why do we believe this evidence is necessary?

The answer must be reconstructable from the graph.

---

# 24. Evidence Requirement Generation Pipeline

```text
ACCEPTED INTENT
        ↓
INTENT INTERPRETATION
        ↓
EVIDENCE DIMENSION IDENTIFICATION
        ↓
EVIDENCE FORM GENERATION
        ↓
MINIMUM CONDITION DEFINITION
        ↓
SUFFICIENCY DEFINITION
        ↓
PRIORITY / STRENGTH ASSIGNMENT
        ↓
CONFLICT ANALYSIS
        ↓
PROVENANCE ATTACHMENT
        ↓
EVIDENCE VALIDATION
        ↓
ACCEPT / CHALLENGE / ESCALATE
```

---

# 25. Evidence Requirement Validation

An Evidence Requirement should be challenged when:

```text
NO OBSERVABLE EVIDENCE PATH
```

or:

```text
REQUIREMENT IS ACTUALLY AN INTENT
```

or:

```text
REQUIREMENT IS ACTUALLY A SHOT SPECIFICATION
```

or:

```text
REQUIREMENT CONTRADICTS PRODUCT TRUTH
```

or:

```text
REQUIREMENT DEPENDS ON UNKNOWN INFORMATION
```

or:

```text
REQUIREMENT IS REDUNDANT WITHOUT INCREMENTAL VALUE
```

---

# 26. Self-Critique Requirements

The Self-Critique Agent should inspect Evidence Requirements for:

- vague evidence language,
- unobservable requirements,
- excessive specificity,
- hidden execution instructions,
- unsupported evidence dimensions,
- duplicated evidence requirements,
- incorrect strength,
- missing sufficiency conditions,
- contradiction with product truth,
- and evidence that does not actually support the parent intent.

The critic produces a critique record rather than silently rewriting the requirement.

---

# 27. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break the Evidence Contract by:

1. Creating evidence requirements that cannot be observed.
2. Turning a shot instruction into a disguised evidence requirement.
3. Weakening evidence requirements to make asset generation easier.
4. Creating unsupported evidence claims.
5. Creating redundant evidence requirements to inflate asset demand.
6. Exploiting ambiguity in evidence strength.
7. Creating conflicting requirements without exposing the conflict.
8. Claiming evidence is sufficient when the relevant property is not observable.
9. Using one asset to falsely claim support for unrelated intents.
10. Mutating a locked parent intent through evidence changes.
11. Injecting execution-level constraints into semantic evidence.
12. Removing provenance from evidence requirements.

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

# 28. Validation Invariants

### Invariant 1

Every accepted Evidence Requirement traces to an accepted or explicitly challengeable Intent.

### Invariant 2

Every Evidence Requirement has an observable evidence path.

### Invariant 3

Evidence strength is separate from evidence priority.

### Invariant 4

Evidence priority is separate from authority.

### Invariant 5

Evidence confidence is separate from authority.

### Invariant 6

Evidence Requirements do not directly prescribe final shot, camera, lighting, or prompt parameters.

### Invariant 7

A downstream Evidence Agent cannot silently mutate a locked Intent.

### Invariant 8

Evidence sufficiency must be judged against the parent intent.

### Invariant 9

Evidence contribution is relationship-specific.

### Invariant 10

Evidence saturation must be distinguishable from evidence sufficiency.

### Invariant 11

Every accepted requirement preserves provenance.

### Invariant 12

Evidence conflict must be surfaced rather than silently resolved by the Evidence layer.

---

# 29. Falsifiable Architectural Hypotheses

## Hypothesis A — Separating evidence from assets improves asset strategy

**Claim:**

Keeping Evidence Requirements independent from concrete assets allows the optimizer to find multiple valid asset realizations rather than locking strategy prematurely.

**Experiment:**

Compare:

```text
System A:
Intent → direct asset selection

System B:
Intent → Evidence → asset strategy
```

Measure:

- asset redundancy,
- evidence coverage,
- strategy flexibility,
- unnecessary asset count,
- human correction rate.

---

## Hypothesis B — Evidence sufficiency prevents asset-count optimization

**Claim:**

Explicit sufficiency and saturation states reduce the tendency to equate more assets with better campaign evidence.

**Experiment:**

Provide campaigns where multiple near-duplicate assets can satisfy the same requirement.

Measure whether the system stops once sufficient evidence is achieved.

---

## Hypothesis C — Relationship-level evidence contribution improves attribution

**Claim:**

Storing evidence strength on the Asset → Evidence relationship produces more accurate explanations than assigning evidence strength only to the asset.

**Experiment:**

Use multi-purpose assets and compare attribution accuracy.

---

## Hypothesis D — Evidence-path validation reduces vague strategic requirements

**Claim:**

Requiring every accepted evidence requirement to have an observable path reduces non-actionable requirements.

**Experiment:**

Inject abstract or non-observable evidence requirements and measure rejection/challenge rate.

---

# 30. Evidence Coverage Model

At campaign level, the system should eventually be able to represent:

```text
INTENT
   ↓
REQUIRED EVIDENCE
   ↓
AVAILABLE CONTRIBUTIONS
   ↓
AGGREGATED SUPPORT
   ↓
COVERAGE STATE
```

Conceptually:

```text
NOT_REPRESENTED
PARTIALLY_REPRESENTED
REPRESENTED
SUFFICIENT
SATURATED
```

The exact scoring model is intentionally deferred to II-006 and II-010.

---

# 31. Evidence vs Asset Optimization Boundary

The Evidence Engine answers:

> What must be demonstrated?

The Asset Strategy Engine answers:

> What is the most efficient set of assets capable of demonstrating it?

Therefore:

```text
EVIDENCE ENGINE
      ↓
REQUIREMENTS

ASSET STRATEGY
      ↓
REALIZATIONS
```

The Evidence Engine must not optimize the final asset set.

---

# 32. Evidence vs Prompt Compilation Boundary

The Evidence Engine must never produce final generation prompts.

The chain remains:

```text
INTENT
    ↓
EVIDENCE
    ↓
ASSET REQUIREMENT
    ↓
ASSET SPECIFICATION
    ↓
PROMPT COMPILER
```

This prevents semantic strategy from becoming entangled with model-specific prompt language.

---

# 33. Evidence Failure Handling

When an Evidence Requirement cannot currently be satisfied:

```text
EVIDENCE FAILURE
        ↓
DIAGNOSE
        ↓
CLASSIFY
```

Possible causes:

```text
MISSING KNOWLEDGE
CONSTRAINT CONFLICT
INSUFFICIENT ASSET FORM
INSUFFICIENT VISUAL RESOLUTION
GENERATION FAILURE
EVALUATION FAILURE
STRATEGIC AMBIGUITY
```

The Evidence Engine should report the failure; the Replanning system decides what to change.

---

# 34. Core Contract

> **The Evidence Requirement Engine shall translate accepted Communication Intents into observable, traceable, confidence-aware requirements that specify what must be demonstrated, at what required strength, and under what conditions the evidence becomes sufficient, while remaining independent from concrete asset, shot, camera, lighting, and prompt decisions. It shall preserve provenance and authority, expose uncertainty and conflicts, distinguish representation from sufficiency and saturation, and provide explicit validation and adversarial attack surfaces.**

---

# 35. Deferred Decisions

II-005 does not freeze:

- exact evidence taxonomy,
- numerical strength thresholds,
- numerical sufficiency formulas,
- saturation equations,
- final scoring implementation,
- specific visual evaluator models,
- asset-selection algorithms,
- database schema,
- prompt templates.

These decisions belong to subsequent contracts.

---

# 36. Exit Criteria

II-005 is semantically complete when:

- [x] Evidence definition established
- [x] Intent / Evidence / Asset boundaries established
- [x] Evidence dimensions defined provisionally
- [x] Evidence strength separated from priority
- [x] Evidence authority separated from confidence
- [x] Observable evidence requirement established
- [x] Acceptable vs preferred evidence established
- [x] Minimum / sufficiency / saturation states established
- [x] Relationship-level evidence contribution established
- [x] Evidence conflict handling established
- [x] Provenance requirements established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Evidence / Asset Strategy boundary established
- [x] Evidence / Prompt Compiler boundary established
- [x] Failure handling boundary established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-006 — Asset Strategy Contract**

This specification will define how the system converts evidence requirements into an optimal set of asset requirements and candidate assets, including coverage, redundancy, marginal evidence value, multi-purpose assets, cross-domain products, and strategic trade-offs.
