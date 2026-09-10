# Decision Rules: Jewelry

This document outlines the executable heuristics used by the Creative Intelligence Platform's reasoning engine when compiling prompts and directing scenes for Jewelry campaigns.

---

```markdown
---
id: "DR-JEWEL-001"
knowledge_unit: "KU-JEWEL-001"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Metal Reflection Mapping

## 1. Condition (IF)
IF Product.Material == "Polished Gold" OR Product.Material == "Platinum" OR Product.Material == "White Gold" OR Product.Material == "Rose Gold"

## 2. Action (THEN)
THEN PromptCompiler.Inject("polished metal surface reflecting clean white studio lighting panel geometries, sharp mirror-like specular reflections mapping the environment details, no blown-out flat white color patches")

## 3. Rationale
Polished metals reflect their surroundings. Instructing environment reflection mapping avoids rendering gold/platinum as flat painted textures.

## 4. Conflicts
Does not apply to brushed or matte metals.
```

---

```markdown
---
id: "DR-JEWEL-002"
knowledge_unit: "KU-JEWEL-002"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Gemstone Refraction & Fire

## 1. Condition (IF)
IF Product.GemstoneType == "Diamond" OR Product.GemstoneType == "Faceted Stone"

## 2. Action (THEN)
THEN PromptCompiler.Inject("faceted gemstone with high refractive index, sharp geometric pavilion facet cuts, complex internal light reflections, colorful dispersion highlights (fire) splitting light into red and blue spectral sparks")
AND PromptCompiler.Forbid(["colored glass look", "flat transparent surface", "solid color gem"])

## 3. Rationale
Faceted stones rely on high refraction and dispersion to look authentic. Forbidding flat textures forces the AI model to calculate multi-facet internal light bounces.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-JEWEL-003"
knowledge_unit: "KU-JEWEL-003"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Macro Camera & Depth of Field

## 1. Condition (IF)
IF Product.Category == "Jewelry" OR Product.Category == "Ring" OR Product.Category == "Earring"
AND Camera.ShotType == "Close-up" OR Camera.ShotType == "Detail"

## 2. Action (THEN)
THEN CameraPlanner.SetLens("90mm macro lens or 105mm macro lens")
AND CameraPlanner.SetAperture("f/2.8 to f/4 shallow depth-of-field")
AND PromptCompiler.Inject("close-up macro shot with tack-sharp focus plane on front jewelry details, gradual soft focal roll-off into creamy background and foreground bokeh")
AND CameraPlanner.Forbid(["wide depth-of-field", "all elements sharp", "infinite focus"])

## 3. Rationale
Macro photography of small items naturally creates a razor-thin focus depth. Renderings with infinite focus read as flat or amateurish.

## 4. Conflicts
Does not apply to lifestyle fashion shots where jewelry is worn by a model in a wider 3/4 or full-body pose.
```

---

```markdown
---
id: "DR-JEWEL-004"
knowledge_unit: "KU-JEWEL-004"
weight: 0.95
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
---

# Decision Rule: Dual Studio Lighting

## 1. Condition (IF)
IF Product.Category == "Jewelry" OR Product.Category == "Ring" OR Product.Category == "Necklace"
AND Campaign.Setting == "Studio"

## 2. Action (THEN)
THEN LightingPlanner.SetLightingProfile("Dual Studio Layout")
AND PromptCompiler.Inject("soft diffused white light boxes mapping smooth glossy bands along metal shanks, combined with a sharp directional key Fresnel spot light at 45 degrees to activate gemstone facet sparkle")
AND LightingPlanner.Forbid(["harsh direct flash", "soft light boxes only", "single light source"])

## 3. Rationale
Diffused light maps clean specular bands on curved metal; hard spot lights trigger facet refraction. Using one without the other results in flat gems or blown-out metal.

## 4. Conflicts
Overrides default single-source lighting setups.
```

---

```markdown
---
id: "DR-JEWEL-005"
knowledge_unit: "KU-JEWEL-005"
weight: 0.90
priority: "Medium"
status: "Active"
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
---

# Decision Rule: Default Textured Dark Background

## 1. Condition (IF)
IF Product.Category == "Jewelry" OR Product.Category == "Ring" OR Product.Category == "Earring"
AND Scene.Background == "Under-specified"
AND Campaign.Intent == "Luxury Editorial"

## 2. Action (THEN)
THEN EnvironmentPlanner.SetBackgroundSurface("Dark textured slate or raw textured concrete")
AND PromptCompiler.Inject("product placed on a dark textured slate background, creating high-contrast separation and catching sharp specular reflections")

## 3. Rationale
Textured dark surfaces provide excellent contrast for precious metals and gemstones, enhancing light rebounds and highlighting product margins.

## 4. Conflicts
Always overridable by explicit brand guidelines or user-specified backdrops.
```
