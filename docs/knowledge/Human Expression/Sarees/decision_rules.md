# Decision Rules: Sarees

This document outlines the executable heuristics used by the Creative Intelligence Platform's reasoning engine when compiling prompts and directing scenes for Saree campaigns.

---

```markdown
---
id: "DR-SAREE-001"
knowledge_unit: "KU-SAREE-001"
weight: 1.0
priority: "Critical"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Banarasi Drape Physics Constraints

## 1. Condition (IF)
IF Product.FabricType == "Banarasi Silk" OR Product.FabricType == "Brocade"

## 2. Action (THEN)
THEN PromptCompiler.Inject("heavy structured Banarasi silk brocade with defined crisp architectural folds, large deep pleats holding shape under gravity")
AND PromptCompiler.Forbid(["flowing silk", "billowing fabric", "lightweight drape", "airy folds", "fluttering"])

## 3. Rationale
Banarasi silk brocade is physically heavy (300-700 GSM). Forbid words that describe chiffon/georgette to prevent AI rendering engines from generating thin, synthetic folds.

## 4. Conflicts
Overrides user-specified adjectives such as "billowing" or "lightweight" if they contradict the physical fabric base.
```

---

```markdown
---
id: "DR-SAREE-002"
knowledge_unit: "KU-SAREE-002"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Zari Reflectance Compiler Injection

## 1. Condition (IF)
IF Product.Embellishment == "Zari" OR Product.FabricType == "Banarasi Silk" OR Product.FabricType == "Kanjeevaram Silk"

## 2. Action (THEN)
THEN PromptCompiler.Inject("individual gold and silver zari threads creating distinct sharp point catchlights, metallic reflective thread-work, micro-contrast details")

## 3. Rationale
Zari behaves like microscopic mirrors. Direct prompting forces the renderer to create sharp, specular point catchlights instead of smooth, painted textures.

## 4. Conflicts
None. Applies as an additive rendering modifier.
```

---

```markdown
---
id: "DR-SAREE-003"
knowledge_unit: "KU-SAREE-003"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Kanjeevaram Posture & Drape

## 1. Condition (IF)
IF Product.FabricType == "Kanjeevaram Silk" OR Product.FabricType == "Kanjivaram"

## 2. Action (THEN)
THEN PromptCompiler.Inject("stiff structural drape, deep architectural folds holding shape independently, posture reflecting heavy fabric weight with subtle forward lean or hip shift")
AND PosePlanner.RestrictTo(["standing_heritage", "temple_stance", "seated_royal"])
AND PosePlanner.Forbid(["dynamic_running", "billowing_pose", "jumping", "flying_pallu"])

## 3. Rationale
Kanjeevaram is the heaviest silk family. Poses must reflect this weight, and the fabric folds must remain stiffly architectural rather than flowing.

## 4. Conflicts
None.
```

---

```markdown
---
id: "DR-SAREE-004"
knowledge_unit: "KU-SAREE-004"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Chanderi Translucency Lighting

## 1. Condition (IF)
IF Product.FabricType == "Chanderi" OR Product.FabricType == "Chanderi Silk-Cotton"

## 2. Action (THEN)
THEN LightingPlanner.SetPrimarySource("Backlight or counter-light from window or sun")
AND PromptCompiler.Inject("semi-translucent sheer fabric base glowing under backlight, opaque silk motifs catching specular highlights, dual-surface texture")
AND EnvironmentPlanner.Forbid(["black studio background", "dark interior with no windows"])

## 3. Rationale
Chanderi's identity is defined by its sheer, light-transmitting weave. Backlighting is physically required to make this visible. Dark backgrounds or front-lighting flatten the weave.

## 4. Conflicts
If campaign calls for a "dark studio theme", it must inject a backlight source behind the subject to maintain the translucency glow.
```

---

```markdown
---
id: "DR-SAREE-005"
knowledge_unit: "KU-SAREE-005"
weight: 1.0
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
---

# Decision Rule: Velvet Pile directional Reflectance

## 1. Condition (IF)
IF Product.FabricType == "Velvet"

## 2. Action (THEN)
THEN PromptCompiler.Inject("deep velvet pile direction creating luminosity gradient across surface folds, fabric reads lighter where pile is compressed and darker in open pile shadow zones")
AND LightingPlanner.Forbid(["flat front-facing studio lighting", "ring light key"])

## 3. Rationale
Velvet pile absorbs or reflects light based on pile direction. Side/angled light is required to activate this crushing gradient, which defines velvet luxury.

## 4. Conflicts
Overrides default flat studio catalog lighting setups.
```

---

```markdown
---
id: "DR-SAREE-006"
knowledge_unit: "KU-SAREE-006"
weight: 0.95
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
---

# Decision Rule: Zari Angled Lighting

## 1. Condition (IF)
IF Product.Embellishment == "Zari" OR Product.FabricType == "Banarasi Silk"
AND Campaign.Intent == "Luxury Bridal" OR Campaign.Intent == "Luxury Editorial"

## 2. Action (THEN)
THEN LightingPlanner.SetKeyAngle("30 to 60 degrees side or grazing position")
AND LightingPlanner.Forbid(["strobe flash key", "flat front light"])

## 3. Rationale
Angled lighting captures the three-dimensional relief of woven zari, creating metallic fire. Front lighting makes zari appear dull and uniform.

## 4. Conflicts
Overridable only by explicit user instruction to use flat studio lighting (e.g., for catalog workwear).
```

---

```markdown
---
id: "DR-SAREE-007"
knowledge_unit: "KU-SAREE-007"
weight: 0.95
priority: "High"
status: "Active"
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
---

# Decision Rule: Kanjeevaram Framing Rule

## 1. Condition (IF)
IF Product.FabricType == "Kanjeevaram Silk" OR Product.FabricType == "Kanjivaram"

## 2. Action (THEN)
THEN CameraPlanner.SetFraming(["full body", "three-quarter portrait"])
AND CameraPlanner.Forbid(["tight face close-up", "shoulder crop portrait"])

## 3. Rationale
Kanjeevaram's identity relies heavily on the broad contrast zari border. Tight crops remove the border, making the garment visually unidentifiable as a Kanjeevaram.

## 4. Conflicts
Overridable only if user requests a "Macro Detail close-up" of the fabric pattern.
```

---

```markdown
---
id: "DR-SAREE-008"
knowledge_unit: "KU-SAREE-008"
weight: 0.85
priority: "Medium"
status: "Active"
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
---

# Decision Rule: Default Luxury Bridal Campaign Lighting

## 1. Condition (IF)
IF Campaign.Intent == "Luxury Bridal"
AND Campaign.LightingSetting == "Under-specified"

## 2. Action (THEN)
THEN LightingPlanner.SetLightingProfile("Golden Hour Directional")
AND LightingPlanner.SetColorTemperature("2700K to 3200K warm amber-gold")
AND EnvironmentPlanner.SetBackgroundCategory("Heritage interior or palace courtyard")

## 3. Rationale
Observed statistics show 92% of premium bridal silk campaigns use warm directional golden-hour lighting.

## 4. Conflicts
Always overridable by explicit user creative brief.
```
