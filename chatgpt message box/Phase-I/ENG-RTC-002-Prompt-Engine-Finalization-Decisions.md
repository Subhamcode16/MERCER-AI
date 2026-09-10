# INTELLIGENCE → ENGINEERING INSTRUCTION
# ENG-RTC-002 — Prompt Engine Finalization Decisions

**Protocol:** ENGINEER-COMMUNICATION-001  
**Type:** FREEZE + MODIFY  
**Priority:** CRITICAL  
**Status:** APPROVED FOR IMPLEMENTATION

---

# 1. Executive Decision

The Prompt Engine should be refactored, but the proposed architecture requires several important corrections before implementation.

The final architecture must preserve the distinction between:

```text
INTELLIGENCE
What should be represented?

        ↓

DECISION ENGINE
What creative solution should be selected?

        ↓

PROMPT COMPILER
How should the selected solution be expressed to the generation model?

        ↓

GENERATOR
Produce the artifact.

        ↓

EVALUATOR
Determine whether the artifact actually satisfies the intended solution.
```

The Prompt Compiler must **not become a hidden creative decision-maker**.

---

# 2. DECISION — Vibe → Authenticity Profile

## Question

Should vibe names directly map to:

- Luxury Bridal
- Editorial
- E-Commerce Catalog

## Decision

### REJECT direct one-to-one mapping.

A vibe is not an authenticity profile.

Vibes such as `Moody`, `Golden Hour`, `Natural`, `Cinematic`, `Minimal`, `Documentary`, and `Editorial` describe aspects of creative direction.

Authenticity profiles such as `Luxury Bridal`, `Editorial`, and `E-Commerce Catalog` describe broader output/authenticity objectives.

These are different dimensions.

---

# 3. Required Architecture

Treat the following as separate inputs:

```text
Campaign Intent
        +
Output Type
        +
Brand Positioning
        +
Domain
        +
Product DNA
        +
Vibe
        +
Authenticity Profile
        +
Technical Constraints
        ↓
Decision Engine
        ↓
Creative Solution
        ↓
Prompt Compiler
```

The compiler must consume the **resolved creative solution**, rather than attempting to derive that solution itself.

---

# 4. Vibe Resolution

A fallback matching system may exist, but it should be implemented as a **resolver**, not a hardcoded compiler rule.

Example:

```text
vibe = "Moody"
```

must NOT automatically mean:

```text
authenticity_profile = "Editorial"
```

Instead:

```text
Moody
    ↓
Vibe Characteristics
    ├── contrast tendency
    ├── colour temperature tendency
    ├── shadow tendency
    ├── emotional tendency
    └── atmosphere tendency
```

The selected Authenticity Profile remains independently determined.

---

# 5. Recommended Profile Model

The runtime should conceptually support:

```json
{
  "authenticity_profile": "editorial",
  "vibe": "moody",
  "vibe_modifiers": {
    "contrast": 0.78,
    "warmth": 0.32,
    "shadow_depth": 0.71,
    "atmosphere": 0.68
  }
}
```

The exact schema may differ according to implementation requirements.

The important architectural principle is:

> **Vibe modifies the solution. It does not determine the authenticity profile.**

---

# 6. DECISION — Detail Allocation

## Question

Should the compiler force waist-up / medium close-up framing plus a minimalist environment for editorial/bridal realism?

## Decision

### REJECT forced framing.

The system must **not hardcode waist-up or medium close-up framing based solely on authenticity profile or vibe.**

Framing is a creative decision.

It should be determined by:

```text
Campaign Objective
+
Product Visibility Requirement
+
Product Detail Importance
+
Model Requirement
+
Composition Requirement
+
Channel / Placement
+
Creative Direction
```

---

# 7. Detail Allocation Principle

Instead of:

```text
Editorial → waist-up
Bridal → waist-up
```

use:

```text
Product Detail Importance
        ↓
Detail Allocation
        ↓
Framing Recommendation
```

For example, if the product's differentiation is:

```text
zari craftsmanship
fine embroidery
fabric weave
surface texture
```

the system may recommend:

```text
medium shot
+
close-up
+
macro/detail shot
```

But if the campaign objective is:

```text
luxury lifestyle
```

a wider environmental composition may be more appropriate.

---

# 8. Campaigns Are Multi-Shot Systems

Do not optimize one generated image to communicate every product attribute.

The campaign planner should eventually distribute information across a **shot system**.

Example:

```text
SHOT 01
Hero Editorial
→ overall product + identity

SHOT 02
Craftsmanship
→ embroidery / zari / texture

SHOT 03
Silhouette
→ drape / movement / fit

SHOT 04
Lifestyle
→ environment + positioning

SHOT 05
Detail
→ material / construction / finish
```

Therefore the Prompt Compiler should compile prompts **per shot**, using the specific information priorities assigned to that shot.

---

# 9. Environment Rule

Do not force minimalist environments.

Environment should be selected according to the resolved Creative Direction.

Possible environments include:

- minimalist studio
- architectural interior
- domestic environment
- natural landscape
- urban environment
- luxury interior
- gallery
- street environment
- cultural environment
- abstract backdrop

The environment must support the campaign narrative.

---

# 10. DECISION — Generic AI Slop Keywords

## Decision

# FREEZE — YES.

The Prompt Compiler is prohibited from adding generic quality-amplification keywords as a substitute for structured photographic intelligence.

Specifically prohibit compiler-generated use of:

```text
photorealistic
hyperrealistic
8k
4k
ultra detailed
masterpiece
best quality
high quality
award winning
stunning
beautiful
insanely detailed
```

unless a future explicit experiment reopens this decision.

---

# 11. Why This Is Frozen

These terms do not communicate the actual photographic conditions required to produce realism.

Instead of:

```text
photorealistic, 8k, hyperrealistic
```

the system should specify:

```text
natural skin microtexture
+
realistic subsurface skin response
+
fine facial asymmetry
+
authentic fabric tension
+
material-specific specular response
+
physically plausible folds
+
controlled highlight rolloff
+
natural shadow transitions
+
optical depth
+
appropriate lens characteristics
```

The system must describe **causes and observable properties**, not simply demand a quality adjective.

---

# 12. QUALITY Segment

The proposed QUALITY segment is approved conceptually.

It should encode:

## Physical realism

- material behaviour
- fabric deformation
- gravity
- contact
- tension
- folds
- stitching
- surface variation

## Human realism

- skin microtexture
- pores
- peach fuzz
- asymmetry
- hair variation
- natural expression

## Optical realism

- depth of field
- lens behaviour
- highlight rolloff
- shadow transitions
- exposure behaviour
- subtle grain where appropriate

## Photographic realism

- believable lighting
- believable perspective
- coherent focus
- natural tonal response
- realistic colour reproduction

---

# 13. Authenticity Weights Must Be Continuous

Do not make the compiler purely threshold-based.

The current proposal:

```text
SkinPores > 0.7
→ add skin pore descriptor
```

is acceptable as an initial implementation, but the architecture should support continuous weighting.

For example:

```text
SkinPores = 0.25
SkinPores = 0.55
SkinPores = 0.90
```

should result in different intensity of representation.

The compiler may discretize these into practical tiers:

```text
0.00–0.30 → LOW
0.31–0.65 → MEDIUM
0.66–1.00 → HIGH
```

but the underlying value must remain continuous.

---

# 14. FORBIDDEN Layer

The FORBIDDEN segment is approved.

Distinguish between:

## HARD FORBIDDEN

Conditions that must not appear.

Examples:

```text
plastic skin
CGI appearance
airbrushed skin
unnatural waxy surfaces
floating fabric
impossible anatomy
```

## SOFT NEGATIVE

Undesirable tendencies that should be reduced.

Examples:

```text
excessive sharpening
overly smooth gradients
excessive bloom
excessive HDR
heavy digital noise
```

This distinction will become important for the future evaluation system.

---

# 15. Domain-Aware Negatives

Do not create one universal negative prompt containing hundreds of terms.

Instead:

```text
Global Negatives
+
Domain Negatives
+
Product Negatives
+
Campaign Negatives
+
Shot Negatives
```

Example:

```text
GLOBAL
plastic skin

+

TEXTILE
unnaturally smooth fabric

+

JEWELRY
melted gemstones

+

SHOT
incorrect product cropping
```

This keeps prompts focused and reduces negative-prompt contamination.

---

# 16. 7-Segment Prompt Structure

The seven-segment architecture is APPROVED as a compilation structure:

```text
SUBJECT
MATERIAL
LIGHTING
CAMERA
ENVIRONMENT
QUALITY
FORBIDDEN
```

These segments must represent **resolved intelligence**, not independently invent decisions.

---

# 17. Segment Responsibilities

## SUBJECT

Represents:

- subject identity
- model characteristics
- pose
- expression
- body orientation
- shot framing
- product placement

## MATERIAL

Represents:

- material identity
- weight
- weave
- texture
- surface structure
- drape
- tension
- folds
- construction
- material-specific behaviour

## LIGHTING

Represents:

- key direction
- source size
- softness
- colour temperature
- fill ratio
- shadow behaviour
- highlight behaviour
- material interaction

## CAMERA

Represents:

- focal length
- camera height
- perspective
- aperture
- depth of field
- focus priority
- optical characteristics
- film response where appropriate

## ENVIRONMENT

Represents:

- location
- architectural language
- background
- spatial depth
- atmosphere
- negative space
- environmental relationship

## QUALITY

Represents:

- physical realism
- human realism
- optical realism
- photographic realism
- authenticity profile requirements

## FORBIDDEN

Represents:

- hard prohibitions
- soft negative tendencies
- domain-specific failure modes
- shot-specific failure modes

---

# 18. Prompt Compiler Boundary

The compiler may:

- select descriptors
- order descriptors
- compress redundant descriptors
- resolve formatting
- translate structured values into model-readable language
- apply profile intensity
- construct negative constraints
- produce deterministic prompt structure

The compiler must NOT:

- invent domain knowledge
- invent creative strategy
- select campaign objectives
- override hard constraints
- independently determine brand positioning
- silently change product priorities

---

# 19. Required Data Flow

The target pipeline should be:

```text
RAW INPUT
    ↓
DOMAIN KNOWLEDGE
    ↓
PRODUCT DNA
    ↓
CAMPAIGN INTENT
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
7-SEGMENT PROMPT
    ↓
IMAGE GENERATOR
    ↓
EVALUATION ENGINE
    ↓
DECISION TRACE
```

---

# 20. Required Compiler Output

The compiler should eventually produce both:

## A. Human-readable prompt

The seven-segment generation prompt.

## B. Machine-readable compilation trace

Example:

```json
{
  "shot_id": "hero_01",
  "profile": "editorial",
  "vibe": "moody",
  "segments": {
    "subject": [],
    "material": [],
    "lighting": [],
    "camera": [],
    "environment": [],
    "quality": [],
    "forbidden": []
  },
  "source_claims": [
    "fabric.silk.drape",
    "fabric.zari.reflectivity",
    "lighting.editorial.side_key"
  ],
  "constraints_satisfied": [
    "product_visibility",
    "material_legibility"
  ],
  "constraints_relaxed": [],
  "confidence": 0.91
}
```

The system must eventually be able to answer:

> "Why did this prompt contain this instruction?"

---

# 21. Evaluation Must Be Separate

Implement evaluation as a separate stage.

Do not allow the Prompt Compiler to declare an image successful merely because it generated a syntactically valid prompt.

The evaluation system should compare:

```text
INTENDED CREATIVE SOLUTION
        vs
GENERATED ARTIFACT
```

---

# 22. Initial Evaluation Dimensions

Prepare the architecture for evaluating:

```text
Product Fidelity
Material Fidelity
Lighting Fidelity
Composition Fidelity
Human Realism
Photographic Realism
Brand Alignment
Campaign Intent Alignment
Forbidden-Artifact Detection
```

The evaluator schema must be extensible.

---

# 23. Required Tests

Before declaring `prompt_compiler.py` complete, create deterministic unit tests covering:

### Test 01 — High SkinPores

Expected:

- skin microtexture descriptors present
- plastic/airbrushed negatives present

### Test 02 — Low SkinPores

Expected:

- no excessive skin-detail injection

### Test 03 — High FabricWrinkles

Expected:

- stress-point wrinkle descriptors
- natural drape descriptors

### Test 04 — High FilmGrain

Expected:

- appropriate analog response
- grain descriptor
- digital-artifact negative

### Test 05 — Editorial profile + wide environmental campaign

Expected:

- compiler does NOT force waist-up

### Test 06 — Moody vibe + E-Commerce profile

Expected:

- vibe and profile remain independently represented

### Test 07 — Multi-product campaign

Expected:

- compiler receives a resolved solution
- compiler does not independently resolve conflicting product rules

### Test 08 — Generic slop keyword scan

Expected:

- compiler output contains none of the prohibited generic quality keywords

---

# 24. Prompt Linter

Add a validation stage:

```text
Prompt Compiler
      ↓
Prompt Linter
      ↓
Generator
```

The Prompt Linter should detect:

- prohibited generic keywords
- missing required segments
- duplicated descriptors
- unresolved placeholders
- unsupported claims
- excessive prompt length
- conflicting instructions
- missing source claims

This prevents prompt degradation over time.

---

# 25. FREEZE Decisions

The following decisions are now FROZEN:

### FREEZE-001

Vibe does not directly determine Authenticity Profile.

### FREEZE-002

Framing cannot be hardcoded from vibe or authenticity profile.

### FREEZE-003

Environment cannot be hardcoded as minimalist for editorial / bridal output.

### FREEZE-004

Generic AI quality-amplification keywords are prohibited from compiler-generated prompts.

### FREEZE-005

Prompt Compiler must not become a hidden source of domain intelligence.

### FREEZE-006

Prompt compilation must produce a decision/trace representation alongside the final prompt.

### FREEZE-007

Evaluation must remain architecturally separate from generation.

---

# 26. Implementation Priority

Implement in this order:

```text
1. Refactor prompt_compiler.py
        ↓
2. Implement authenticity-profile translation
        ↓
3. Implement structured 7-segment compilation
        ↓
4. Implement dynamic FORBIDDEN generation
        ↓
5. Implement prompt linter
        ↓
6. Implement compilation trace
        ↓
7. Implement evaluator schema
        ↓
8. Add unit tests
        ↓
9. Run reference-image benchmark
```

Do not begin a broad agent-harness rewrite until this compiler boundary is stable.

---

# 27. Reference Artifact Benchmark

Use the provided saree artifact as one of the benchmark cases.

The benchmark should test whether the system can produce a creative specification capable of preserving:

- deep red textile richness
- gold zari legibility
- authentic textile structure
- restrained editorial expression
- cool architectural environment
- warm/cool lighting separation
- natural skin
- realistic fabric folds
- controlled highlights
- contemporary luxury positioning

The goal is **not** to reproduce the exact image.

The goal is to test whether the Intelligence → Decision → Prompt pipeline captures the creative reasoning required to produce this class of artifact.

---

# Final Instruction

Proceed with implementation according to the decisions above.

Do not interpret the seven-segment structure as a license to hardcode creative decisions.

The fundamental rule is:

> **The Intelligence Layer decides. The Decision Engine resolves. The Prompt Compiler expresses. The Generator creates. The Evaluator judges.**

If an implementation requirement conflicts with this separation, stop and surface the conflict rather than silently embedding the missing intelligence inside the compiler.

Return the next engineering report as:

`ENG-RTC-003`

with:

1. Files changed
2. Architecture changes
3. Compiler implementation
4. Prompt-linter implementation
5. Compilation-trace schema
6. Tests added
7. Test results
8. Example compiled prompt
9. Example compilation trace
10. Remaining blockers
11. Proposed next architectural decision
