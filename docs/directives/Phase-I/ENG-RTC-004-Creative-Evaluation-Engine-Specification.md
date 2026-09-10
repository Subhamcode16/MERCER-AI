# INTELLIGENCE → ENGINEERING INSTRUCTION
# ENG-RTC-004 — Creative Evaluation Engine Specification

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** APPROVED FOR IMPLEMENTATION  
**Priority:** CRITICAL  
**Supersedes:** Next Architectural Decision from ENG-RTC-003  
**Reference:** ENG-RTC-002 Prompt Engine Finalization Decisions

---

# 1. Purpose

The Prompt Compiler has now reached a stable implementation boundary.

The next architectural layer is the **Creative Evaluation Engine**.

The evaluator must not simply determine whether an image is "good", "realistic", or aesthetically pleasing.

Its primary responsibility is:

> **Determine whether the generated artifact faithfully executes the intended creative solution produced by the Intelligence → Decision pipeline.**

The fundamental comparison is:

```text
INTENDED CREATIVE SOLUTION
            ↓
       GENERATED ARTIFACT
            ↓
        EVALUATION
```

The evaluator therefore judges **execution fidelity**, not generic image quality.

---

# 2. Architectural Principle

The evaluator must remain separate from:

- Intelligence Layer
- Decision Engine
- Constraint Solver
- Prompt Compiler
- Generator

Target architecture:

```text
RAW INPUT
    ↓
INTELLIGENCE
    ↓
DECISION ENGINE
    ↓
CONSTRAINT SOLVER
    ↓
CREATIVE SOLUTION
    ↓
SHOT PLAN
    ↓
PROMPT COMPILER
    ↓
GENERATOR
    ↓
GENERATED ARTIFACT
    ↓
EVALUATION ENGINE
    ↓
EVALUATION RESULT
```

The evaluator must not silently modify the creative solution.

If the artifact fails, it reports the failure.

---

# 3. Core Evaluation Question

Every evaluation must answer:

> **Did the generated artifact satisfy the visual, material, photographic, compositional, and campaign requirements defined by the resolved creative solution?**

Not:

> "Does this image look good?"

And not:

> "Does this image look photorealistic?"

---

# 4. Evaluation Dimensions

The evaluator should initially support the following dimensions:

```text
1. Product Fidelity
2. Material Fidelity
3. Lighting Fidelity
4. Composition Fidelity
5. Human Realism
6. Photographic Realism
7. Brand Alignment
8. Campaign Intent Alignment
9. Forbidden-Artifact Detection
```

These dimensions must remain independently measurable.

Do not collapse them into one score internally.

---

# 5. Product Fidelity

Determine whether the intended product is visually represented correctly.

For a saree example, inspect:

- product identity
- colour
- silhouette
- border
- pallu
- motifs
- zari
- embroidery
- major construction features
- relative placement
- visible product area

The evaluator must distinguish:

```text
Product absent
Product partially represented
Product recognizable but inaccurate
Product substantially faithful
Product highly faithful
```

The exact scoring implementation may use continuous values.

---

# 6. Material Fidelity

Determine whether the generated material behaves like the intended material.

For textile products evaluate:

- weave appearance
- surface structure
- weight
- drape
- gravity response
- fold behaviour
- tension
- sheen
- reflectivity
- microtexture
- material-specific highlights

Example:

A silk saree should not merely be "shiny."

The evaluator should determine whether the artifact demonstrates visual behaviour consistent with the intended silk construction.

---

# 7. Lighting Fidelity

Compare the generated lighting against the resolved lighting solution.

Evaluate:

- key direction
- source softness
- colour temperature
- contrast
- fill level
- shadow direction
- highlight response
- rim light where specified
- material/light interaction

Do not punish an image simply because it differs from the literal prompt wording.

Evaluate against the **resolved lighting intent**.

---

# 8. Composition Fidelity

Evaluate:

- framing
- subject placement
- product visibility
- negative space
- camera relationship
- visual hierarchy
- pose
- environmental relationship
- crop

The evaluator must understand that framing is shot-specific.

For example:

```text
Hero Shot
→ broad visual identity

Craftsmanship Shot
→ product detail priority

Lifestyle Shot
→ environment priority
```

A wide composition must not automatically be treated as a failure simply because another shot uses close framing.

---

# 9. Human Realism

Evaluate:

- anatomy
- hands
- fingers
- facial structure
- skin microtexture
- asymmetry
- hair strands
- eyes
- teeth where visible
- natural expression
- body proportions

The evaluator should identify **observable artifacts**, not simply assign a vague "AI-looking" label.

---

# 10. Photographic Realism

Evaluate:

- optical coherence
- depth of field
- perspective
- focus behaviour
- exposure
- highlight rolloff
- shadow transitions
- lens characteristics
- grain where required
- colour response
- overall photographic plausibility

Do not equate photographic realism with maximum sharpness.

---

# 11. Brand Alignment

Evaluate whether the artifact respects the resolved brand/creative positioning.

Possible factors:

- visual sophistication
- tonal character
- colour discipline
- composition language
- styling
- environment
- emotional positioning
- premium/luxury cues where required

Brand alignment must come from the **resolved brand requirements**, not from the evaluator's personal taste.

---

# 12. Campaign Intent Alignment

Determine whether the image actually performs its intended campaign function.

Examples:

```text
Campaign Intent:
Luxury awareness
→ image should establish aspiration and identity.

Campaign Intent:
Product conversion
→ product clarity and desirability become more important.

Campaign Intent:
Craftsmanship storytelling
→ material and construction details become critical.

Campaign Intent:
Lifestyle positioning
→ product/environment relationship becomes critical.
```

The evaluator must therefore be **intent-aware**.

---

# 13. Forbidden-Artifact Detection

This is a critical evaluator function.

Inspect for:

### Human failures

- plastic skin
- waxy skin
- malformed hands
- impossible anatomy
- unnatural facial structure

### Material failures

- melted textile
- impossible folds
- floating fabric
- texture hallucination
- uniform synthetic surfaces

### Product failures

- missing product details
- malformed borders
- broken motifs
- inconsistent embroidery
- incorrect construction

### Optical failures

- impossible reflections
- inconsistent shadows
- broken perspective
- unnatural depth of field

The evaluator should report specific failure categories.

---

# 14. Hard vs Soft Failures

The evaluation model must distinguish:

## HARD FAILURE

A failure that makes the artifact unacceptable for the intended shot.

Examples:

```text
product identity incorrect
major anatomy failure
missing primary product
severe material hallucination
major composition violation
critical forbidden artifact
```

## SOFT FAILURE

A degradation that reduces quality but does not invalidate the artifact.

Examples:

```text
slightly excessive sharpening
minor texture loss
slightly incorrect shadow softness
mildly artificial hair
minor colour drift
```

---

# 15. Scoring Model

Do not expose only one final number internally.

The evaluator should produce something conceptually similar to:

```json
{
  "product_fidelity": 0.94,
  "material_fidelity": 0.91,
  "lighting_fidelity": 0.87,
  "composition_fidelity": 0.95,
  "human_realism": 0.89,
  "photographic_realism": 0.92,
  "brand_alignment": 0.90,
  "campaign_intent_alignment": 0.93,
  "forbidden_artifact_score": 0.97
}
```

The exact schema may differ.

The important requirement is:

> **Keep the dimensions independently observable.**

---

# 16. Weighted Campaign Score

A weighted aggregate may be calculated for decision-making, but it must be derived from the independent scores.

Example:

```text
Campaign Score =
Product Fidelity × product_weight
+
Material Fidelity × material_weight
+
Lighting Fidelity × lighting_weight
+
...
```

The weights must come from the **shot/campaign priorities**.

Do not use one universal weighting scheme.

For example:

```text
Craftsmanship Shot
→ Material Fidelity receives high weight.

Lifestyle Shot
→ Brand + Campaign Intent + Environment receive higher weight.

Conversion Shot
→ Product Fidelity + Product Visibility receive higher weight.
```

---

# 17. Evaluation Must Be Source-Aware

The evaluator should be able to trace each requirement back to its source.

Example:

```json
{
  "dimension": "material_fidelity",
  "score": 0.91,
  "source_claims": [
    "DR-SAREE-001",
    "DR-SAREE-002"
  ],
  "observations": [
    "structured folds preserved",
    "zari reflectivity present",
    "fabric weight visually plausible"
  ]
}
```

This makes the system explainable.

---

# 18. Evaluation Result Schema

Create a machine-readable evaluation result with at least:

```text
evaluation_id
campaign_id
shot_id
model/generator identifier
evaluation timestamp
dimension scores
hard_failures
soft_failures
observations
source_claims
constraints_checked
overall_decision
confidence
recommended_action
```

---

# 19. Overall Decision

The evaluator should return one of:

```text
PASS
PASS_WITH_WARNINGS
REGENERATE
HUMAN_REVIEW
FAIL
```

Do not make the decision solely from an arbitrary numerical threshold.

Hard failures should be able to force:

```text
REGENERATE
```

or:

```text
FAIL
```

depending on severity.

---

# 20. Recommended Action

The evaluator should identify what should happen next.

Examples:

```text
PASS
→ accept artifact

PASS_WITH_WARNINGS
→ accept but flag issues

REGENERATE
→ regenerate with targeted correction

HUMAN_REVIEW
→ escalate to human decision

FAIL
→ reject artifact
```

Most importantly:

> **Regeneration should be targeted.**

Do not regenerate blindly with the same prompt.

---

# 21. Targeted Regeneration

If the evaluator detects:

```text
material_fidelity = 0.62
```

but:

```text
product_fidelity = 0.95
lighting_fidelity = 0.91
composition_fidelity = 0.94
```

the regeneration system should not rewrite the entire creative solution.

It should identify:

```text
FAILURE DOMAIN
→ MATERIAL
```

and request a targeted correction.

Conceptually:

```text
Existing Creative Solution
        ↓
Failure Analysis
        ↓
Targeted Revision
        ↓
Prompt Compiler
        ↓
Regeneration
```

This prevents quality drift.

---

# 22. Evaluation Observations

The evaluator must produce evidence-like observations.

Bad:

```text
"Looks somewhat AI generated."
```

Preferred:

```text
"Fabric fold transitions become unnaturally uniform across the lower pleats, reducing perceived gravity response."
```

Bad:

```text
"Skin looks fake."
```

Preferred:

```text
"Facial skin lacks expected microtexture and exhibits uniform highlight response across cheek and forehead regions."
```

The system should describe observable properties.

---

# 23. Reference Artifact Benchmark

The previously supplied saree artifact should become an evaluation benchmark.

The benchmark should verify whether the system can distinguish:

### Successful characteristics

- deep red textile richness
- gold zari legibility
- authentic textile structure
- controlled highlights
- natural skin
- realistic folds
- warm/cool lighting relationship
- restrained luxury positioning
- architectural environment

### Failure characteristics

- plastic skin
- synthetic fabric
- melted zari
- excessive smoothing
- impossible folds
- flat lighting
- generic environment
- weak product visibility
- CGI appearance

The benchmark is not a request to reproduce the exact artifact.

It is a test of whether the evaluator understands the **creative requirements represented by the artifact**.

---

# 24. Critical Correction to ENG-RTC-003

The engineering report stated:

> "None. The prompt compilation interface is now fully stable, validated, and conforms to the intelligence rules."

Clarification:

The **compiler interface** may be considered stable for the current implementation.

The **visual intelligence pipeline is not yet fully validated.**

That distinction must be preserved.

The evaluator is required before we can claim end-to-end visual validation.

---

# 25. Additional Compiler Issues to Correct

Before declaring the compiler fully frozen, address the following observations from the ENG-RTC-003 example.

## Issue A — Descriptor duplication

Example:

```text
Banarasi Banarasi Silk Saree
```

The linter must reliably detect and prevent this class of duplication.

Add a regression test.

---

## Issue B — Generic subjective descriptors

Example:

```text
beautiful model
```

The compiler should avoid inserting subjective descriptors unless they are explicitly sourced from the creative solution.

Add a rule for unsourced subjective adjectives.

---

## Issue C — Independent Vibe/Profile Test

The current example uses:

```text
profile = Luxury Bridal
vibe = Luxury Bridal
```

Add a test where:

```text
profile = E-Commerce Catalog
vibe = Moody
```

and verify that the two remain independent.

---

## Issue D — Source provenance

For every major generated descriptor, the trace should make it possible to determine whether it came from:

```text
Intelligence Claim
Decision Engine
Constraint Solver
Authenticity Profile
Vibe Resolver
Shot Plan
Compiler transformation
```

The compiler should not create unexplained creative instructions.

---

# 26. Evaluation Architecture

Implement the evaluator as an independent module.

Conceptually:

```text
evaluation.py
    │
    ├── ProductEvaluator
    ├── MaterialEvaluator
    ├── LightingEvaluator
    ├── CompositionEvaluator
    ├── HumanRealismEvaluator
    ├── PhotographicRealismEvaluator
    ├── BrandAlignmentEvaluator
    ├── CampaignIntentEvaluator
    └── ForbiddenArtifactEvaluator
```

The exact class architecture is left to engineering.

The separation of evaluation dimensions is mandatory.

---

# 27. Evaluation Inputs

The evaluator should receive:

```text
Generated Image
+
Creative Solution
+
Shot Plan
+
Product DNA
+
Relevant Intelligence Claims
+
Active Constraints
+
Authenticity Profile
+
Brand Requirements
+
Campaign Intent
```

Do not evaluate from the image alone.

An image cannot be judged correctly without knowing what it was supposed to achieve.

---

# 28. Evaluation Outputs

The evaluator must return:

```text
Dimension Scores
+
Hard Failures
+
Soft Failures
+
Observations
+
Source Claims
+
Confidence
+
Overall Decision
+
Recommended Action
+
Targeted Regeneration Guidance
```

---

# 29. Implementation Priority

Implement in this order:

```text
1. Define evaluation result schema
        ↓
2. Define evaluator interface
        ↓
3. Implement dimension evaluators
        ↓
4. Implement hard/soft failure classification
        ↓
5. Implement weighted shot-aware scoring
        ↓
6. Implement overall decision logic
        ↓
7. Implement observation/provenance output
        ↓
8. Add reference-artifact benchmark
        ↓
9. Add regression tests
        ↓
10. Integrate evaluator with orchestrator
```

Do not implement automatic regeneration until the evaluation result schema is stable.

---

# 30. Required Test Cases

At minimum create:

### TEST-EVAL-001
High product fidelity.

Expected:

```text
product_fidelity ≥ target
overall → PASS
```

### TEST-EVAL-002
Incorrect product construction.

Expected:

```text
hard product failure
overall → REGENERATE or FAIL
```

### TEST-EVAL-003
Strong product + weak material.

Expected:

```text
product score high
material score low
targeted material regeneration
```

### TEST-EVAL-004
Good image + wrong campaign intent.

Expected:

```text
photographic realism may be high
campaign_intent_alignment low
overall not PASS
```

### TEST-EVAL-005
Forbidden AI artifact.

Expected:

```text
forbidden artifact detected
overall → REGENERATE
```

### TEST-EVAL-006
Minor soft defects.

Expected:

```text
PASS_WITH_WARNINGS
```

### TEST-EVAL-007
Human-review ambiguity.

Expected:

```text
HUMAN_REVIEW
```

### TEST-EVAL-008
Independent vibe/profile evaluation.

Expected:

```text
vibe and authenticity profile remain independent
```

---

# 31. Freeze Conditions

Do NOT freeze the Evaluation Engine until:

- schema is implemented
- dimensions are independently observable
- hard/soft failures work
- source provenance works
- shot-aware weighting works
- reference benchmark runs
- regression tests pass
- targeted regeneration guidance is produced

---

# 32. Final Architectural Rule

The system now follows this principle:

> **Intelligence defines what matters.**
>
> **Decision Engine determines what should be done.**
>
> **Constraint Solver resolves conflicts.**
>
> **Prompt Compiler expresses the solution.**
>
> **Generator creates the artifact.**
>
> **Evaluator determines whether the artifact actually fulfilled the solution.**
>
> **Regeneration corrects only the failed dimensions.**

This separation is mandatory.

---

# 33. Required Engineering Response

Return the next engineering report as:

`ENG-RTC-004-IMPLEMENTATION`

Include:

1. Files created/changed
2. Evaluation architecture
3. Evaluation result schema
4. Dimension evaluator implementation
5. Hard/soft failure implementation
6. Shot-aware weighting implementation
7. Overall decision logic
8. Provenance implementation
9. Reference benchmark
10. Tests added
11. Full test results
12. Example evaluation payload
13. Example failure analysis
14. Example targeted regeneration instruction
15. Remaining architectural gaps
16. Proposed next Intelligence decision

Do not report the system as visually validated until the evaluation benchmark demonstrates that the evaluator can correctly distinguish intended creative solutions from generated artifacts.
