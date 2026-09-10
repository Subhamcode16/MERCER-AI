# ENG-RTC-007 — Campaign-Level Visual Coherence & Asset System

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** SPECIFICATION — IMPLEMENTATION REQUEST  
**Priority:** CRITICAL  
**Depends On:** ENG-RTC-001 through ENG-RTC-006  
**Architectural Position:** Campaign Intelligence → Shot Family / Asset Coherence

---

# 1. Architectural Transition

ENG-RTC-006 solved the problem of resolving multiple products inside one shot.

The next problem is larger:

> **How do multiple generated shots coexist as one coherent campaign?**

A campaign is not a collection of independently successful images. It is one creative system expressed through many shots, formats, and assets. Campaign-scale generation requires continuity across assets, formats, products, environments, and channels. citeturn0search7turn0search1

Therefore introduce a **Campaign Intelligence** layer above the resolved-shot system.

---

# 2. Core Principle

> **A shot can be locally correct and still be globally wrong for the campaign.**

For example, three individually excellent images can still fail collectively if their lighting language, model identity, color language, camera language, environment, or visual hierarchy drifts.

Therefore:

```text
SHOT QUALITY ≠ CAMPAIGN COHERENCE
```

Both must be evaluated independently.

---

# 3. New Architecture

```text
CAMPAIGN
   ↓
CAMPAIGN CREATIVE SYSTEM
   ↓
SHOT FAMILY
   ↓
SHOT OBJECTIVE
   ↓
PRODUCT REQUIREMENTS
   ↓
MULTI-PRODUCT RESOLUTION
   ↓
RESOLVED SHOT SOLUTION
   ↓
PROMPT COMPILATION
   ↓
GENERATION
   ↓
EVALUATION
```

---

# 4. Campaign Creative System

Before individual shots are generated, establish a campaign-level creative system.

Conceptually:

```json
{
  "campaign_id": "campaign_001",
  "creative_system": {
    "visual_language": {},
    "lighting_language": {},
    "camera_language": {},
    "environment_language": {},
    "color_language": {},
    "material_language": {},
    "human_language": {},
    "composition_language": {}
  }
}
```

Exact schema is engineering territory. The semantic contract is mandatory.

---

# 5. Campaign Invariants

Initially support:

```text
PRODUCT_IDENTITY
MODEL_IDENTITY
COLOR_LANGUAGE
LIGHTING_LANGUAGE
CAMERA_LANGUAGE
ENVIRONMENT_LANGUAGE
MATERIAL_AUTHENTICITY
VISUAL_TONE
BRAND_LANGUAGE
```

Each invariant must be classified as:

```text
LOCKED
GUIDED
VARIABLE
```

### LOCKED
Must remain consistent. Example: product identity or exact product color.

### GUIDED
Should remain coherent but may adapt. Example: lighting direction or focal-length range.

### VARIABLE
Intentionally changes between assets. Example: pose, crop, or shot angle.

This distinction prevents both campaign drift and excessive repetition.

---

# 6. Shot Families

Assets must be grouped into semantic shot families rather than treated as isolated generations.

Initially support:

```text
HERO
PRODUCT_DETAIL
LIFESTYLE
EDITORIAL_PORTRAIT
CONVERSION
SOCIAL_VERTICAL
CATALOG
```

Each family defines an expected range for:

```text
purpose
visual behavior
composition
camera
lighting
product visibility
```

---

# 7. Campaign Asset Matrix

Before generation, create an explicit asset matrix.

Conceptually:

```text
                 HERO  DETAIL  LIFESTYLE  SOCIAL
--------------------------------------------------
PRODUCT A          ✓      ✓        ✓         ✓
PRODUCT B          ✓      ✓        ✓         ✓
PRODUCT C          -      ✓        ✓         ✓
```

Each asset record should include at minimum:

```text
asset_id
shot_family
objective
primary_product
secondary_products
channel
aspect_ratio
priority
```

The matrix is the campaign generation plan.

---

# 8. Campaign Reference Hierarchy

Introduce four reference levels:

```text
MASTER REFERENCE
CAMPAIGN REFERENCE
FAMILY REFERENCE
SHOT REFERENCE
```

### MASTER REFERENCE
Authoritative product/fabric identity.

### CAMPAIGN REFERENCE
Canonical visual direction for the campaign.

### FAMILY REFERENCE
Representative asset defining a shot family's visual behavior.

### SHOT REFERENCE
Specific references needed by an individual generation.

The Prompt Compiler must receive the appropriate reference context without allowing lower-level references to overwrite authoritative product truth.

---

# 9. Product DNA vs Campaign DNA vs Shot DNA

Maintain a strict distinction:

```text
PRODUCT DNA
= what the product is

CAMPAIGN DNA
= how the campaign presents it

SHOT DNA
= how one specific shot executes it
```

Example:

```text
PRODUCT DNA
→ silk weave, border geometry, color, drape

CAMPAIGN DNA
→ warm editorial daylight, restrained palette, premium realism

SHOT DNA
→ 85mm portrait, medium crop, side-lit hero composition
```

Never overwrite Product DNA with Campaign DNA.

---

# 10. Controlled Variation

Campaign coherence does not mean identical images.

The system must explicitly manage:

```text
CONSISTENCY + VARIATION
```

Example:

```text
LOCK:
product identity
campaign color language

GUIDE:
lighting family
camera family

VARY:
pose
camera angle
composition
environment intensity
```

This creates campaign rhythm instead of repetition.

---

# 11. Campaign-Level Conflict

A new failure class now exists:

```text
SHOT VALID + CAMPAIGN INVALID
```

Example:

```text
Shot 01 → warm daylight
Shot 02 → cool daylight
Shot 03 → neutral studio
```

All may individually pass shot evaluation while violating a campaign-level lighting language.

The campaign evaluator must detect this as campaign drift rather than treating each shot independently.

---

# 12. Campaign Coherence Evaluator

Introduce a campaign-level evaluator distinct from the shot evaluator.

Evaluate at minimum:

```text
PRODUCT CONSISTENCY
MODEL CONSISTENCY
LIGHTING CONSISTENCY
COLOR CONSISTENCY
CAMERA CONSISTENCY
ENVIRONMENT CONSISTENCY
MATERIAL CONSISTENCY
VISUAL TONE CONSISTENCY
```

Maintain two separate dimensions:

```text
SHOT QUALITY
CAMPAIGN COHERENCE
```

Do not collapse them into one score.

Example:

```text
Shot Quality:       9.5
Campaign Coherence: 6.8
```

This means the shot is good but does not belong in the campaign without correction.

---

# 13. Campaign Drift

Introduce explicit drift detection for:

```text
REFERENCE_DRIFT
PRODUCT_DRIFT
MODEL_DRIFT
COLOR_DRIFT
LIGHTING_DRIFT
CAMERA_DRIFT
ENVIRONMENT_DRIFT
MATERIAL_DRIFT
```

Each drift event must preserve:

```text
asset
 dimension
expected_state
observed_state
severity
confidence
```

---

# 14. Local vs Global Failure

When campaign coherence fails, determine whether the failure is:

```text
SHOT_LOCAL
```

or:

```text
CAMPAIGN_GLOBAL
```

Example:

```text
One asset has lighting drift
→ local correction

The entire campaign has incompatible camera language
→ campaign-level correction
```

Do not regenerate the entire campaign for a local defect.

---

# 15. Campaign Correction Strategies

Initially support:

```text
RETAIN
CORRECT
REGENERATE
REBASE
ESCALATE
```

### RETAIN
Asset is coherent.

### CORRECT
Targeted correction can restore coherence.

### REGENERATE
The asset cannot be safely corrected.

### REBASE
The campaign baseline itself must be reconsidered.

### ESCALATE
Campaign requirements are contradictory or insufficient.

---

# 16. Campaign Baseline

Do not simply use the first generated image as the canonical baseline.

Baseline selection must derive from:

```text
campaign objective
+ campaign DNA
+ primary product
+ hero-shot requirements
```

The selected baseline becomes the reference against which subsequent assets are evaluated.

---

# 17. Product Identity Across Assets

The original product reference remains authoritative:

```text
PRODUCT REFERENCE
      ↓
GENERATED PRODUCT
      ↓
IDENTITY EVALUATION
```

Campaign styling must not accidentally modify:

```text
product geometry
pattern
color
material identity
distinctive details
```

Campaign styling changes presentation, not product truth.

---

# 18. Multi-Format Coherence

Treat:

```text
4:5
1:1
9:16
16:9
```

as format variants of the same campaign system.

Preserve:

```text
campaign DNA
asset intent
```

while adapting:

```text
composition
crop
negative space
text-safe regions
product placement
```

Do not create a new creative identity for each format unless explicitly requested.

---

# 19. Channel Boundary

Channel adaptation happens after campaign creative direction:

```text
CAMPAIGN DNA
      ↓
SHOT FAMILY
      ↓
ASSET INTENT
      ↓
CHANNEL
      ↓
FORMAT
      ↓
COMPOSITION ADAPTATION
```

A channel or format may adapt composition but must not silently redefine the campaign's core visual identity.

---

# 20. Campaign Graph and State

Represent campaign relationships explicitly:

```text
CAMPAIGN
  │
  ├── Campaign DNA
  ├── Asset Matrix
  ├── Shot Families
  └── Asset Graph
         ├── Asset 01
         ├── Asset 02
         ├── Asset 03
         └── Asset 04
```

Campaign state must retain:

```text
CAMPAIGN BRIEF
CAMPAIGN DNA
ASSET MATRIX
REFERENCE GRAPH
GENERATION STATUS
EVALUATION RESULTS
COHERENCE RESULTS
CORRECTIONS
DRIFT EVENTS
FINAL ASSET SET
```

Every asset must retain reference ancestry.

---

# 21. Required Machine-Readable Objects

Introduce conceptual objects for:

```text
CampaignCreativeSystem
CampaignInvariant
ShotFamily
CampaignAsset
CampaignAssetMatrix
CampaignReference
CampaignDrift
CampaignCoherenceResult
CampaignCorrectionPlan
```

Exact implementation names remain engineering territory.

---

# 22. Required Tests

### TEST-CAMP-001 — Campaign DNA Creation
Campaign DNA is generated from campaign objective + product intelligence.

### TEST-CAMP-002 — Asset Matrix
A campaign produces an explicit asset matrix.

### TEST-CAMP-003 — Shot Family
Assets are assigned to shot families.

### TEST-CAMP-004 — Locked Invariant
Locked product identity cannot be overwritten by shot styling.

### TEST-CAMP-005 — Guided Invariant
Guided lighting language remains within campaign bounds while allowing variation.

### TEST-CAMP-006 — Controlled Variation
Two assets may differ in composition while remaining campaign coherent.

### TEST-CAMP-007 — Campaign Drift
An intentionally inconsistent asset is detected.

### TEST-CAMP-008 — Local vs Global Failure
The system distinguishes shot-local failure from campaign-global failure.

### TEST-CAMP-009 — Campaign Correction
Correctable drift produces targeted correction rather than full campaign regeneration.

### TEST-CAMP-010 — Campaign Rebase
A baseline conflict produces REBASE rather than silently rewriting downstream assets.

### TEST-CAMP-011 — Product Identity
Product geometry, material, color, and distinctive details remain consistent across assets.

### TEST-CAMP-012 — Multi-Format Coherence
4:5, 1:1, 9:16, and 16:9 variants preserve campaign DNA.

### TEST-CAMP-013 — Channel Adaptation
Channel formatting changes composition without changing campaign identity.

### TEST-CAMP-014 — Reference Graph
Asset dependencies and reference ancestry are preserved.

### TEST-CAMP-015 — Campaign Provenance
Every asset traces through:

```text
campaign
→ DNA
→ shot family
→ objective
→ product requirements
→ resolved shot
→ prompt
→ generation
→ evaluation
```

---

# 23. Non-Goals

Do NOT implement in ENG-RTC-007:

- new domain ontologies
- new material physics
- new product identity models
- social trend intelligence
- ad-buy optimization
- performance prediction
- autonomous marketing strategy
- dynamic web trend research
- full video continuity
- semantic image-embedding research
- autonomous campaign re-planning

ENG-RTC-007 is strictly about **visual campaign coherence and asset orchestration**.

---

# 24. Architectural Boundary

The resulting system should be:

```text
CAMPAIGN INTELLIGENCE
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

Campaign intelligence orchestrates. Shot intelligence reasons about an individual shot. Product intelligence defines product truth. These boundaries must remain intact.

---

# 25. Freeze Criteria

ENG-RTC-007 may be frozen only when:

```text
Campaign DNA exists
        AND
Campaign invariants exist
        AND
Shot families exist
        AND
Asset matrix exists
        AND
Reference hierarchy exists
        AND
Controlled variation exists
        AND
Campaign drift is detectable
        AND
Local/global failures are distinguishable
        AND
Campaign correction is targeted
        AND
Multi-format coherence is preserved
        AND
Product identity remains authoritative
        AND
Campaign provenance is complete
        AND
TEST-CAMP-001 through TEST-CAMP-015 pass
```

---

# 26. Required Engineering Response

Return:

`ENG-RTC-007-IMPLEMENTATION`

Include:

1. Files created/changed
2. CampaignCreativeSystem representation
3. Campaign DNA generation
4. Campaign invariant model
5. Locked/guided/variable handling
6. Shot Family model
7. Asset Matrix implementation
8. Reference hierarchy
9. Campaign graph
10. Campaign coherence evaluator
11. Campaign drift detection
12. Local vs global failure classification
13. Campaign correction strategy
14. Multi-format coherence
15. Channel adaptation boundary
16. Campaign state/provenance
17. TEST-CAMP-001 through TEST-CAMP-015 results
18. Example coherent campaign
19. Example campaign drift
20. Example correction
21. Known limitations
22. Architectural risks
23. Confirmation that ENG-RTC-006 remains unchanged

Do not proceed to another architectural layer until ENG-RTC-007 has been reviewed and frozen.

---

# 27. Final Architectural Law

> **A campaign is not a collection of images. It is a coordinated visual system whose individual assets inherit a shared creative identity while retaining controlled variation.**

The system must therefore optimize for:

```text
PRODUCT TRUTH
+
SHOT QUALITY
+
CAMPAIGN COHERENCE
+
CONTROLLED VARIATION
```

—not merely individual image quality.
