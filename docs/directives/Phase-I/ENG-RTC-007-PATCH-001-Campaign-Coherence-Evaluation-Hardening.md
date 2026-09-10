# INTELLIGENCE → ENGINEERING CORRECTIVE PATCH
# ENG-RTC-007-PATCH-001 — Campaign Coherence Evaluation Hardening

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** REQUIRED CORRECTIVE PATCH  
**Priority:** HIGH  
**Parent:** ENG-RTC-007 — Campaign-Level Visual Coherence & Asset System  
**Depends On:** ENG-RTC-001 through ENG-RTC-007  
**Purpose:** Harden campaign coherence semantics before ENG-RTC-007 freeze

---

# 1. Review Decision

The Intelligence Architect has reviewed:

`ENG-RTC-007-IMPLEMENTATION`

The implementation successfully establishes the campaign orchestration backbone:

- Campaign Creative System
- Campaign DNA
- Campaign invariants
- LOCKED / GUIDED / VARIABLE tiers
- Shot Families
- Campaign Asset Matrix
- Reference hierarchy
- Campaign reference graph
- Campaign coherence result
- Drift detection
- Local/global correction
- Multi-format adaptation
- Channel adaptation
- Campaign provenance
- TEST-CAMP-001 through TEST-CAMP-015

The complete campaign test suite and previous regression suite pass.

However:

> **ENG-RTC-007 MUST NOT BE FROZEN YET.**

The current campaign evaluator is too shallow to serve as the long-term semantic coherence contract.

The engineer explicitly reports that current coherence checking relies on string/exact-color comparison while deeper semantic visual evaluation is deferred.

This patch closes that architectural gap without introducing embeddings, new vision models, or a large redesign.

---

# 2. Core Architectural Problem

The current system can detect:

```text
EXPECTED:
earth tones

OBSERVED:
neon green

→ HARD DRIFT
```

This is useful.

But campaign coherence is not equivalent to string equality.

Example:

```text
CAMPAIGN DNA:
warm natural daylight

ASSET A:
slightly warm natural daylight

ASSET B:
neutral daylight

ASSET C:
cool blue daylight
```

These are not equally distant from the campaign baseline.

Likewise:

```text
CAMPAIGN:
premium restrained editorial realism

ASSET:
matching palette
+
matching camera language
+
plastic CGI-like material rendering
```

The declarative rules may appear correct while the visual result is still campaign-incoherent.

Therefore the architecture must distinguish:

```text
DECLARATIVE COHERENCE
```

from:

```text
PERCEPTUAL COHERENCE
```

---

# 3. PATCH-A — Evaluation Layers

Introduce an explicit two-layer campaign coherence model.

## Layer 1 — Declarative Coherence

Evaluates machine-readable campaign constraints such as:

```text
product identity
locked colors
shot family
aspect ratio
campaign configuration
reference ancestry
invariant tier
declared lighting family
declared camera family
```

This can remain deterministic.

## Layer 2 — Perceptual Coherence

Represents the future evaluation boundary for actual visual similarity/coherence across generated assets.

Examples:

```text
lighting appearance
material rendering
visual tone
camera-language appearance
environmental continuity
human presentation
editorial feel
```

### Critical restriction

Do NOT implement embeddings, CLIP, VLM scoring, or any new perceptual model in this patch.

The requirement is architectural:

```text
DECLARATIVE EVALUATION
        +
PERCEPTUAL EVALUATION
        ↓
CAMPAIGN COHERENCE RESULT
```

The perceptual evaluator may remain a defined interface/stub until the visual evaluation layer provides the required capability.

---

# 4. Evaluation Result Contract

The campaign coherence result must be capable of representing:

```text
declarative_result
perceptual_result
overall_result
```

and must preserve the distinction between:

```text
RULE FAILURE
```

and:

```text
VISUAL COHERENCE FAILURE
```

Do not collapse both into one undifferentiated score.

---

# 5. PATCH-B — Guided Tolerance

The current invariant tiers correctly establish:

```text
LOCKED
GUIDED
VARIABLE
```

However, `GUIDED` must mean:

> **bounded variation**

not:

> unrestricted variation.

A GUIDED invariant must therefore be capable of representing:

```text
target
allowed_variation
tolerance
importance
```

Exact field names are engineering territory.

Example:

```json
{
  "dimension": "LIGHTING",
  "tier": "GUIDED",
  "target": "warm natural daylight",
  "allowed_variation": "moderately warmer/cooler daylight",
  "tolerance": "medium",
  "importance": "high"
}
```

This does NOT require implementing perceptual measurement now.

It only ensures the campaign model has a place to express the intended semantic boundary.

---

# 6. PATCH-C — Variation vs Drift Taxonomy

The campaign system must explicitly distinguish:

```text
VARIABLE
```

from:

```text
GUIDED_VARIATION
```

from:

```text
DRIFT
```

from:

```text
VIOLATION
```

Definitions:

### VARIABLE

Intentional difference permitted by the campaign.

Example:

```text
pose
crop
camera angle
```

### GUIDED_VARIATION

Difference allowed within a GUIDED invariant's tolerance.

Example:

```text
warm daylight
→ slightly warmer daylight
```

### DRIFT

Unintended movement away from the campaign baseline but not necessarily a hard violation.

Example:

```text
warm daylight
→ neutral/cool daylight
```

### VIOLATION

A LOCKED requirement has been broken.

Example:

```text
LOCKED:
earth-tone campaign palette

OBSERVED:
neon green dominant palette
```

The existing HARD/SOFT severity mechanism may remain, but it must not replace this semantic classification.

---

# 7. PATCH-D — Failure Scope

The current implementation maps:

```text
single asset drift
→ CORRECT

multiple assets drift
→ REBASE
```

This is insufficient.

Failure count does not determine failure scope.

Example:

```text
10 assets
8 correct
2 minor lighting drift
```

should not automatically trigger REBASE.

Conversely:

```text
2 assets
2 assets contradict campaign baseline
```

may justify REBASE.

Therefore introduce a semantic failure scope capable of distinguishing:

```text
ASSET_LOCAL
FAMILY_LOCAL
CAMPAIGN_GLOBAL
BASELINE_UNCERTAIN
```

Definitions:

### ASSET_LOCAL

Only one asset is inconsistent and campaign baseline remains trustworthy.

Typical action:

```text
CORRECT
```

### FAMILY_LOCAL

A specific shot family is inconsistent while the campaign remains coherent overall.

Typical action:

```text
CORRECT
```

or:

```text
REGENERATE
```

### CAMPAIGN_GLOBAL

Multiple independent asset families contradict the campaign baseline.

Typical action:

```text
REBASE
```

### BASELINE_UNCERTAIN

Evidence indicates that the selected campaign baseline itself may be unreliable.

Typical action:

```text
REBASE
```

or:

```text
ESCALATE
```

The correction engine must use failure scope rather than raw failure count.

---

# 8. PATCH-E — Campaign Baseline Selection

The campaign baseline must NOT simply become:

```text
first generated image
```

by default.

The baseline selection must explicitly derive from:

```text
CAMPAIGN OBJECTIVE
+
CAMPAIGN DNA
+
PRIMARY PRODUCT
+
HERO REQUIREMENTS
```

The exact selection algorithm is engineering territory.

But the system must record provenance explaining:

```text
why this baseline was selected
```

The selected baseline must be represented as a campaign reference.

---

# 9. Baseline Provenance

Preserve at minimum:

```text
campaign_id
baseline_asset_id
campaign_objective
primary_product
hero_requirement_reference
selection_reason
```

This is necessary because later campaign drift evaluation depends on knowing what the campaign baseline actually represents.

---

# 10. Campaign Coherence Principle

The campaign system must now reason in this order:

```text
CAMPAIGN DNA
        ↓
CAMPAIGN INVARIANTS
        ↓
BASELINE
        ↓
ASSET
        ↓
DECLARATIVE EVALUATION
        ↓
PERCEPTUAL EVALUATION
        ↓
DRIFT CLASSIFICATION
        ↓
FAILURE SCOPE
        ↓
CORRECTION STRATEGY
```

Do not skip directly from:

```text
asset difference
```

to:

```text REBASE
```

---

# 11. Correction Decision Boundary

The correction system must preserve the existing strategies:

```text
RETAIN
CORRECT
REGENERATE
REBASE
ESCALATE
```

But selection must now be informed by:

```text
drift_type
severity
confidence
failure_scope
baseline_trust
```

Example:

```text
ASSET_LOCAL
+
DRIFT
+
high confidence
→ CORRECT
```

Example:

```text
FAMILY_LOCAL
+
VIOLATION
→ REGENERATE
```

Example:

```text
CAMPAIGN_GLOBAL
+
DRIFT
→ REBASE
```

Example:

```text
BASELINE_UNCERTAIN
→ REBASE / ESCALATE
```

The exact scoring model is not required.

---

# 12. Required New Machine-Readable Concepts

Introduce or extend conceptual structures for:

```text
CampaignEvaluationLayer
CampaignTolerance
CampaignDriftType
CampaignFailureScope
CampaignBaselineSelection
```

Exact class names are engineering territory.

The semantic capabilities are mandatory.

---

# 13. Required Tests

Add the following:

## TEST-CAMP-016 — Declarative vs Perceptual Evaluation Boundary

Verify that campaign coherence can distinguish:

```text
declarative evaluation
```

from:

```text
perceptual evaluation
```

without requiring an embedding implementation.

---

## TEST-CAMP-017 — Guided Tolerance Representation

Create a GUIDED invariant containing:

```text
target
allowed variation
tolerance
importance
```

Verify that the representation is preserved.

---

## TEST-CAMP-018 — Variation vs Drift Classification

Verify that the system distinguishes:

```text
VARIABLE
GUIDED_VARIATION
DRIFT
VIOLATION
```

correctly.

---

## TEST-CAMP-019 — Failure Scope Classification

Verify that the system distinguishes:

```text
ASSET_LOCAL
FAMILY_LOCAL
CAMPAIGN_GLOBAL
BASELINE_UNCERTAIN
```

and does not infer scope solely from the number of failed assets.

---

## TEST-CAMP-020 — Baseline Selection Provenance

Verify that the selected baseline records:

```text
campaign objective
primary product
hero requirements
selection reason
```

and is not simply selected because it was the first generated asset.

---

# 14. Regression Requirements

After implementation:

```text
TEST-CAMP-001
through
TEST-CAMP-020
```

must all pass.

Then execute the complete previous regression suite.

No existing ENG-RTC-006 behavior may regress.

---

# 15. Scope Restrictions

Do NOT implement:

- CLIP
- embeddings
- VLM-based scoring
- new computer-vision models
- automatic aesthetic scoring
- new domain ontologies
- new material physics
- marketing-performance prediction
- trend intelligence
- ad-buy optimization
- autonomous campaign strategy
- ENG-RTC-008

This patch is strictly:

> **Campaign coherence semantic hardening.**

---

# 16. Preserve Existing Architecture

Do not modify:

```text
ENG-RTC-006 conflict resolution
Product DNA
ProductRequirement
Prompt Compiler
Shot-level conflict resolver
Existing campaign architecture
```

The intended architecture remains:

```text
PRODUCT KNOWLEDGE
        ↓
CAMPAIGN DNA
        ↓
ASSET MATRIX
        ↓
SHOT FAMILY
        ↓
SHOT OBJECTIVE
        ↓
PRODUCT REQUIREMENTS
        ↓
MULTI-PRODUCT RESOLUTION
        ↓
RESOLVED SHOT
        ↓
PROMPT COMPILER
        ↓
GENERATOR
        ↓
SHOT EVALUATOR
        ↓
CAMPAIGN COHERENCE EVALUATOR
        ↓
CAMPAIGN CORRECTION
```

---

# 17. Freeze Gate

ENG-RTC-007 may be frozen only when:

```text
Evaluation layers exist
        AND
Guided tolerance exists
        AND
Variation/Drift/Violation are distinct
        AND
Failure scope exists
        AND
Baseline selection is explicit
        AND
Baseline provenance exists
        AND
CAMP-016 passes
        AND
CAMP-017 passes
        AND
CAMP-018 passes
        AND
CAMP-019 passes
        AND
CAMP-020 passes
        AND
CAMP-001 through CAMP-015 still pass
        AND
Previous regression suite passes
```

---

# 18. Required Engineering Response

Return:

`ENG-RTC-007-PATCH-001-IMPLEMENTATION`

Include:

1. Files changed
2. Evaluation-layer implementation
3. Guided tolerance implementation
4. Variation/drift/violation classification
5. Failure-scope implementation
6. Baseline-selection implementation
7. Baseline provenance
8. Correction decision changes
9. TEST-CAMP-016 through TEST-CAMP-020
10. Full CAMP-001 through CAMP-020 results
11. Full regression results
12. Example guided variation
13. Example drift
14. Example violation
15. Example family-local failure
16. Example campaign-global failure
17. Example baseline selection
18. Known limitations
19. Confirmation that no perceptual model/embedding was introduced
20. Confirmation that ENG-RTC-006 remains unchanged

---

# 19. Final Instruction

Keep this patch narrow.

We are not asking you to solve perceptual campaign evaluation yet.

We are asking you to make the architecture capable of supporting it correctly later.

The campaign intelligence layer must know the difference between:

```text
intentional variation
allowed variation
unintended drift
hard violation
```

and between:

```text
one bad asset
one bad family
a broken campaign
an unreliable baseline
```

Once those semantics are explicit and the 20 campaign tests pass, stop implementation and return the report for architectural review.

Do not proceed to ENG-RTC-008 until ENG-RTC-007 is reviewed and frozen.
