# Decision Rules: Apparel

This document outlines the executable heuristics used by the Creative Intelligence Platform's reasoning engine when compiling prompts and directing scenes for Apparel campaigns.

---

```markdown
---
id: "DR-APP-001"
knowledge_unit: "KU-APP-001"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Denim Drape & Stitching Constraints

## 1. Condition (IF)
IF Product.FabricType == "Denim" OR Product.FabricType == "Raw Denim"

## 2. Action (THEN)
THEN PromptCompiler.Inject("stiff raw denim with wide rigid folds holding structured shape under gravity, double-needle contrast stitching along flat seams and cuffs, twill weave micro-texture")
AND PromptCompiler.Forbid(["billowing", "flowing drape", "soft pleats", "slinky"])

## 3. Rationale
Denim twill has low drape compliance. Forbid fluid movement descriptors to prevent rendering engine hallucinations. Contrast stitching is an essential visual identifier of authentic denim.

## 4. Conflicts
Overrides user-specified fluid adjectives if applied to a denim product.
```

---

```markdown
---
id: "DR-APP-002"
knowledge_unit: "KU-APP-002"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Linen Crease Enforcement

## 1. Condition (IF)
IF Product.FabricType == "Linen" OR Product.FabricType == "Flax Linen"

## 2. Action (THEN)
THEN PromptCompiler.Inject("fully matte linen texture with zero sheen, organic high-contrast crease lines and wrinkles locked at elbow and knee joints and waistline")

## 3. Rationale
Linen lacks luster and creases deeply due to flax fibers. Forcing wrinkle injection prevents the AI from rendering linen with polyester-smooth textures.

## 4. Conflicts
None. Applies as an additive modifier.
```

---

```markdown
---
id: "DR-APP-003"
knowledge_unit: "KU-APP-003"
weight: 1.0
priority: "Critical"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Spandex Activewear Contour wrapping

## 1. Condition (IF)
IF Product.FabricType == "Spandex" OR Product.FabricType == "Activewear" OR Product.FabricType == "Compression Fabric"

## 2. Action (THEN)
THEN PromptCompiler.Inject("compression activewear wrapping body contours tightly under elastic tension, completely smooth wrinkle-free surfaces at joints, flatlock stitching running flush along panels")
AND PromptCompiler.Forbid(["loose sagging folds", "draping waistline", "baggy pleats"])

## 3. Rationale
Elastane-based compression fabrics eliminate loose folds and use flatlock seams to avoid chafing. Renders must reflect this elastic tension.

## 4. Conflicts
Overrides any default soft drape or wrinkle rules.
```

---

```markdown
---
id: "DR-APP-004"
knowledge_unit: "KU-APP-004"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Tailored Blazer Structure

## 1. Condition (IF)
IF Product.Category == "Blazer" OR Product.Category == "Tailored Suit" OR Product.Category == "Formal Coat"

## 2. Action (THEN)
THEN PromptCompiler.Inject("structured tailored blazer with straight sharp shoulder lines supported by internal canvas padding, crisp roll lapels forming a distinct V-shape")
AND PosePlanner.Forbid(["slouchy shoulder pose", "hunched posture"])

## 3. Rationale
Formal outerwear has internal padding that defines the structure. Posture and drape must reflect this straight silhouette.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-APP-005"
knowledge_unit: "KU-APP-005"
weight: 0.95
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
---

# Decision Rule: Blazer Lapel Lighting

## 1. Condition (IF)
IF Product.Category == "Blazer" OR Product.Category == "Formal Coat"
AND Campaign.Intent == "Luxury Editorial" OR Campaign.Intent == "E-Commerce"

## 2. Action (THEN)
THEN LightingPlanner.SetKeyAngle("directional side key lighting at 45 degrees")
AND PromptCompiler.Inject("lapel edge casting a subtle drop shadow on the chest, defining tailoring depth and structural overlap")

## 3. Rationale
Lapels overlap the blazer chest. Flat front light washes out the lapel shadow, making the chest area appear flat and lacking dimensional tailoring depth.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-APP-006"
knowledge_unit: "KU-APP-006"
weight: 0.90
priority: "Medium"
status: "Active"
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
---

# Decision Rule: Default Linen Lighting

## 1. Condition (IF)
IF Product.FabricType == "Linen"
AND Campaign.LightingSetting == "Under-specified"

## 2. Action (THEN)
THEN LightingPlanner.SetLightingProfile("Soft diffused natural daylight or north light")
AND PromptCompiler.Inject("soft lighting emphasizing coarse linen weave micro-texture without casting harsh dark shadows")

## 3. Rationale
Diffused natural light preserves the subtle, low-contrast coarse weave of linen. Hard lighting creates shadow lines that compete with the organic wrinkle patterns.

## 4. Conflicts
Always overridable by explicit user creative direction.
```
