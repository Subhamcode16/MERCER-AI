# Knowledge: Jewelry

This document collects the verified Knowledge Units (KUs) for the Jewelry module, structured according to the three levels of the Material Intelligence pipeline.

---

## LEVEL 1: PHYSICAL TRUTH (IMMUTABLE)

```markdown
---
id: "KU-JEWEL-001"
domain: "Human Expression"
specialization: "Jewelry"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "metal", "reflection"]
---

# Knowledge Unit: Precious Metal Reflection Mapping

## 1. The Claim
Polished precious metals (gold, platinum) act as mirrors, displaying high specular reflectivity (80-95%) with narrow specular width, meaning their visual appearance is defined by the reflections of surrounding environment geometries.

## 2. Evidence
- [ER-JEWEL-001: Precious Metal Specular & Reflection Mapping](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/evidence.md#L1-L24)

## 3. Creative Implications
To render gold/platinum authentically, prompts must specify reflection mapping, reflection shapes, or environment structures to be reflected on the metal shank/band.

## 4. Associated Decision Rules
- [DR-JEWEL-001: Metal Reflection Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/decision_rules.md)
```

---

```markdown
---
id: "KU-JEWEL-002"
domain: "Human Expression"
specialization: "Jewelry"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "gemstone", "dispersion"]
---

# Knowledge Unit: Gemstone Dispersion (Fire)

## 1. The Claim
Cut gemstones (especially diamonds with a refractive index of 2.42 and dispersion of 0.044) refract light through Pavilion facets and split it into rainbow-colored fire highlights when exiting the crown.

## 2. Evidence
- [ER-JEWEL-002: Gemstone Refraction and Dispersion (Fire)](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/evidence.md#L26-L49)

## 3. Creative Implications
Prompts for diamonds and colored gems must explicitly call for internal refraction, sharp facet cuts, and colorful dispersion/fire highlights to avoid looking like flat colored glass.

## 4. Associated Decision Rules
- [DR-JEWEL-002: Gemstone Fire Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/decision_rules.md)
```

---

```markdown
---
id: "KU-JEWEL-003"
domain: "Human Expression"
specialization: "Jewelry"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "camera", "macro"]
---

# Knowledge Unit: Macro Photography Depth of Field

## 1. The Claim
Jewelry macro photography (using 90mm-105mm macro lenses at close distances) creates a razor-thin depth-of-field, leaving only a specific plane of the jewelry piece in sharp focus while the rest rolls off into creamy bokeh.

## 2. Evidence
- [ER-JEWEL-004: Macro Lens & Razor-Thin DOF](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/evidence.md#L77-L100)

## 3. Creative Implications
Close-up jewelry prompts must specify macro lens properties, shallow depth-of-field, and soft background bokeh roll-off to match professional photography standards.

## 4. Associated Decision Rules
- [DR-JEWEL-003: Macro Camera Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/decision_rules.md)
```

---

## LEVEL 2: EXPERT HEURISTICS (PRACTICE)

```markdown
---
id: "KU-JEWEL-004"
domain: "Human Expression"
specialization: "Jewelry"
status: "Verified"
confidence_score: 0.95
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
tags: ["lighting", "gemstone", "metal"]
---

# Knowledge Unit: Dual Studio Lighting for Jewelry

## 1. The Claim
Authentic jewelry rendering requires a dual lighting setup: large diffused panels/softboxes to map clean specular reflection bands on metal surfaces, and hard directional Fresnel spots to trigger gemstone sparkle.

## 2. Evidence
- [ER-JEWEL-003: Fresnel Spot vs Diffused Studio Panels](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/evidence.md#L51-L75)

## 3. Creative Implications
The scene compiler must instruct both soft panel reflections and hard directional highlights to balance metal gloss and gemstone fire without blowing out the highlights.

## 4. Associated Decision Rules
- [DR-JEWEL-004: Dual Lighting Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/decision_rules.md)
```

---

## LEVEL 3: OBSERVED STATISTICS (PATTERNS)

```markdown
---
id: "KU-JEWEL-005"
domain: "Human Expression"
specialization: "Jewelry"
status: "Verified"
confidence_score: 0.90
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
tags: ["statistics", "background", "editorial"]
---

# Knowledge Unit: Luxury Jewelry Editorial Backgrounds

## 1. The Claim
Historical luxury jewelry editorial campaigns utilize dark, textured stone or raw concrete surfaces in 72% of observed cases to contrast and bounce sharp specular light from precious metals and diamonds.

## 2. Evidence
- [ER-JEWEL-003: Fresnel Spot vs Diffused Studio Panels](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/evidence.md#L51-L75)

## 3. Creative Implications
When background surfaces are under-specified for a product close-up, default the backdrop to a dark, textured slate or concrete surface to maximize jewelry contrast.

## 4. Associated Decision Rules
- [DR-JEWEL-005: Default Jewelry Background](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Jewelry/decision_rules.md)
```
