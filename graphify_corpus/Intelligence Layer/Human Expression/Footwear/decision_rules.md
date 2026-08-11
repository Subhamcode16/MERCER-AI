# Decision Rules: Footwear

This document outlines the executable heuristics used by the Creative Intelligence Platform's reasoning engine when compiling prompts and directing scenes for Footwear campaigns.

---

```markdown
---
id: "DR-FOOT-001"
knowledge_unit: "KU-FOOT-001"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Leather Specular Highlights

## 1. Condition (IF)
IF Product.Material == "Polished Leather" OR Product.Material == "Leather"

## 2. Action (THEN)
THEN PromptCompiler.Inject("polished leather upper with narrow sharp specular highlights along natural curves, anisotropic sheen reflecting ambient light")

## 3. Rationale
Fine polished leather has a narrow specular highlight distribution. Directing the renderer prevents flat matte textures or broad plastic glares.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-FOOT-002"
knowledge_unit: "KU-FOOT-002"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Leather Vamp Crease Enforcement

## 1. Condition (IF)
IF Product.Material == "Leather" OR Product.Material == "Polished Leather"
AND Model.PoseState == "Walking" OR Model.PoseState == "Standing"

## 2. Action (THEN)
THEN PromptCompiler.Inject("subtle organic horizontal flex creases across the toe box vamp, wrinkles interrupting the specular leather sheen")

## 3. Rationale
Worn leather creasing at the vamp is a physical truth of shoe mechanics. Perfectly smooth surfaces read as synthetic plastic in active poses.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-FOOT-003"
knowledge_unit: "KU-FOOT-003"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Suede Pile Reflectance

## 1. Condition (IF)
IF Product.Material == "Suede" OR Product.Material == "Nubuck"

## 2. Action (THEN)
THEN PromptCompiler.Inject("fully diffuse matte suede surface, napped pile texture showing natural light and dark brushed grain variations from fiber direction")
AND PromptCompiler.Forbid(["shiny surface", "high gloss", "specular sheen"])

## 3. Rationale
Suede absorbs light and exhibits pile-directional color shifting. Forbidding sheen prevents rendering errors that look like patent leather.

## 4. Conflicts
Overrides default leather specular rules.
```

---

```markdown
---
id: "DR-FOOT-004"
knowledge_unit: "KU-FOOT-004"
weight: 1.0
priority: "Critical"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Ground Contact Shadows

## 1. Condition (IF)
IF Product.Category == "Footwear" OR Product.Category == "Shoes" OR Product.Category == "Sneakers"
AND Scene.Surface == "Floor" OR Scene.Surface == "Ground"

## 2. Action (THEN)
THEN PromptCompiler.Inject("dense black contact shadow directly under the outsole, strong ambient occlusion at tread-ground interface, rapid shadow diffusion outward")
AND PromptCompiler.Forbid(["hovering shoe", "floating shoe", "missing shadows under sole"])

## 3. Rationale
AI models frequently fail to ground objects. Enforcing ambient occlusion shadows directly under sole treads prevents the shoe from appearing to float.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-FOOT-005"
knowledge_unit: "KU-FOOT-005"
weight: 0.95
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
---

# Decision Rule: Lacing Symmetry Heuristics

## 1. Condition (IF)
IF Product.Closure == "Laces" OR Product.Closure == "Laced"

## 2. Action (THEN)
THEN PromptCompiler.Inject("matching eyelet counts and symmetrical criss-cross lacing pattern on left and right shoes, laces draping naturally downward under gravity casting subtle drop shadows on the shoe tongue, plastic aglets on lace tips")

## 3. Rationale
Shoelace hallucinations are highly common. Enforcing symmetrical lacing patterns, gravity-compliant lace draping, and aglet details maintains shoe integrity.

## 4. Conflicts
Does not apply to slip-ons, boots with zippers, or strap-based closures.
```

---

```markdown
---
id: "DR-FOOT-006"
knowledge_unit: "KU-FOOT-006"
weight: 0.95
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
---

# Decision Rule: Suede Angled Lighting

## 1. Condition (IF)
IF Product.Material == "Suede" OR Product.Material == "Nubuck"
AND Campaign.Intent == "Luxury Editorial" OR Campaign.Intent == "E-Commerce"

## 2. Action (THEN)
THEN LightingPlanner.SetKeyAngle("directional angled side key lighting at 45 degrees")
AND LightingPlanner.Forbid(["flat ring lighting", "direct front-facing flash"])

## 3. Rationale
Suede pile has tiny napped shadows. Angled lighting renders micro-shadows, making suede texture legible. Flat front light washes the texture out.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-FOOT-007"
knowledge_unit: "KU-FOOT-007"
weight: 0.90
priority: "Medium"
status: "Active"
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
---

# Decision Rule: Default Footwear Camera Angle

## 1. Condition (IF)
IF Product.Category == "Footwear" OR Product.Category == "Shoes"
AND Camera.Height == "Under-specified"

## 2. Action (THEN)
THEN CameraPlanner.SetHeight("low-angle camera position placed near the floor level")
AND PromptCompiler.Inject("hero shot from a low perspective, emphasizing shoe profile and sole tread depth")

## 3. Rationale
A low perspective is the standard "hero" angle in 78% of observed premium footwear campaigns, making the product look powerful and emphasizing design volume.

## 4. Conflicts
Always overridable by explicit user framing instructions.
```
