# Knowledge: Apparel

This document collects the verified Knowledge Units (KUs) for the Apparel module, structured according to the three levels of the Material Intelligence pipeline.

---

## LEVEL 1: PHYSICAL TRUTH (IMMUTABLE)

```markdown
---
id: "KU-APP-001"
domain: "Human Expression"
specialization: "Apparel"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "drape", "denim"]
---

# Knowledge Unit: Denim Drape Stiffness

## 1. The Claim
Heavy denim (12-15 oz) has low drape compliance, holding wide, rigid folds and structured shapes under gravity rather than soft, cascading pleats.

## 2. Evidence
- [ER-APP-001: Heavy Denim Physics and Seams](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/evidence.md#L1-L26)

## 3. Creative Implications
Prompts for raw/heavy denim must explicitly specify rigid folds and structured drapes. Words describing soft fluid drape will cause rendering anomalies.

## 4. Associated Decision Rules
- [DR-APP-001: Denim Drape Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/decision_rules.md)
```

---

```markdown
---
id: "KU-APP-002"
domain: "Human Expression"
specialization: "Apparel"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "wrinkles", "linen"]
---

# Knowledge Unit: Linen Creasing and Wrinkle Retention

## 1. The Claim
Linen immediately forms and permanently retains sharp, high-contrast, organic crease lines at joint bending areas (elbows, knees, waist) during movement.

## 2. Evidence
- [ER-APP-002: Linen Creasing and Surface Matte](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/evidence.md#L28-L53)

## 3. Creative Implications
Prompts for worn linen must demand organic wrinkles at joint stress areas. Disallowing wrinkles on linen generates synthetic-looking renders.

## 4. Associated Decision Rules
- [DR-APP-002: Linen Crease Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/decision_rules.md)
```

---

```markdown
---
id: "KU-APP-003"
domain: "Human Expression"
specialization: "Apparel"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "stretch", "activewear"]
---

# Knowledge Unit: Activewear Stretch & recovery

## 1. The Claim
Spandex-blend activewear wraps body contours tightly under elastic recovery, resulting in smooth, wrinkle-free fabric surfaces even around joints under tension.

## 2. Evidence
- [ER-APP-003: Spandex activewear Contour Wrapping](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/evidence.md#L55-L79)

## 3. Creative Implications
Activewear prompts must emphasize smooth skin-tight wrapping and forbid loose sagging folds at elbows or knees.

## 4. Associated Decision Rules
- [DR-APP-003: Activewear Contour Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/decision_rules.md)
```

---

```markdown
---
id: "KU-APP-004"
domain: "Human Expression"
specialization: "Apparel"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "tailoring", "outerwear"]
---

# Knowledge Unit: Structured Outerwear Shoulder Profile

## 1. The Claim
Tailored formal outerwear features straight, structured shoulder lines reinforced by internal canvas padding, maintaining shape independent of the natural shoulder slope.

## 2. Evidence
- [ER-APP-004: Tailored Blazer Structure & Padding](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/evidence.md#L81-L105)

## 3. Creative Implications
Formal blazers and coats must be prompted with structured padded shoulders, avoiding dropped or slouchy silhouettes.

## 4. Associated Decision Rules
- [DR-APP-004: Blazer Structure Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/decision_rules.md)
```

---

## LEVEL 2: EXPERT HEURISTICS (PRACTICE)

```markdown
---
id: "KU-APP-005"
domain: "Human Expression"
specialization: "Apparel"
status: "Verified"
confidence_score: 0.95
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
tags: ["lighting", "tailoring"]
---

# Knowledge Unit: Directional Light for Blazer Depth

## 1. The Claim
Tailored blazers require directional side lighting to cast a subtle drop shadow under the lapel edge, defining the garment's three-dimensional silhouette.

## 2. Evidence
- [ER-APP-004: Tailored Blazer Structure & Padding](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/evidence.md#L81-L105)

## 3. Creative Implications
The scene planner must set directional side-lighting setups for formal outerwear to avoid a flat chest render.

## 4. Associated Decision Rules
- [DR-APP-005: Blazer Lapel Lighting](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/decision_rules.md)
```

---

## LEVEL 3: OBSERVED STATISTICS (PATTERNS)

```markdown
---
id: "KU-APP-006"
domain: "Human Expression"
specialization: "Apparel"
status: "Verified"
confidence_score: 0.90
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
tags: ["optics", "statistics", "linen"]
---

# Knowledge Unit: Linen Campaign Lighting Defaults

## 1. The Claim
Historical premium linen campaigns utilize soft, diffused daylight (north light or open sky) in 85% of observed cases to avoid harsh shadow competition with the linen's natural weave texture.

## 2. Evidence
- [ER-APP-002: Linen Creasing and Surface Matte](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/evidence.md#L28-L53)

## 3. Creative Implications
When linen lighting is under-specified, default to soft daylight/north light to maximize weave texture readability.

## 4. Associated Decision Rules
- [DR-APP-006: Default Linen Lighting](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Apparel/decision_rules.md)
```
