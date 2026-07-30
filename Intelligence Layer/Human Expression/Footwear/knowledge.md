# Knowledge: Footwear

This document collects the verified Knowledge Units (KUs) for the Footwear module, structured according to the three levels of the Material Intelligence pipeline.

---

## LEVEL 1: PHYSICAL TRUTH (IMMUTABLE)

```markdown
---
id: "KU-FOOT-001"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "leather", "specular"]
---

# Knowledge Unit: Polished Leather Reflection

## 1. The Claim
Polished leather possesses a highly smooth, anisotropic surface finish that creates narrow, sharp specular highlights at curvature changes.

## 2. Evidence
- [ER-FOOT-001: Polished Leather Reflection and Creases](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L1-L24)

## 3. Creative Implications
To render leather shoes authentically, the prompt compiler must explicitly call for sharp, narrow specular highlights and clean anisotropic sheen.

## 4. Associated Decision Rules
- [DR-FOOT-001: Leather Specular Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```

---

```markdown
---
id: "KU-FOOT-002"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "wrinkles", "leather"]
---

# Knowledge Unit: Leather Vamp Creasing

## 1. The Claim
During walking or standing flex, leather footwear forms organic horizontal creases across the toe box vamp, which interrupt the polished specular sheen.

## 2. Evidence
- [ER-FOOT-001: Polished Leather Reflection and Creases](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L1-L24)

## 3. Creative Implications
Active or worn leather shoe renders must include subtle horizontal toe box vamp creases. A perfectly smooth toe box reads as synthetic plastic.

## 4. Associated Decision Rules
- [DR-FOOT-002: Vamp Crease Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```

---

```markdown
---
id: "KU-FOOT-003"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "suede", "pile"]
---

# Knowledge Unit: Suede Pile directional Color Shift

## 1. The Claim
Suede has a fully diffuse matte surface with micro-pile fibers that cause color value shifts (light/dark grain) depending on pile brushing direction.

## 2. Evidence
- [ER-FOOT-002: Suede Pile and Light Absorption](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L26-L50)

## 3. Creative Implications
Prompts for suede must demand a matte pile texture with natural light and dark brushed grain variations.

## 4. Associated Decision Rules
- [DR-FOOT-003: Suede Pile Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```

---

```markdown
---
id: "KU-FOOT-004"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "shadows", "grounding"]
---

# Knowledge Unit: Sole Grounding shadow

## 1. The Claim
A shoe in contact with the ground plane casts a dense black contact shadow (ambient occlusion) directly under the outsole where tread blocks touch the floor.

## 2. Evidence
- [ER-FOOT-004: Sole Grounding & Shadows](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L77-L100)

## 3. Creative Implications
The prompt and scene compiler must enforce grounding shadow detail to prevent shoes from appearing to float or hover on the floor.

## 4. Associated Decision Rules
- [DR-FOOT-004: Ground Shadow Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```

---

## LEVEL 2: EXPERT HEURISTICS (PRACTICE)

```markdown
---
id: "KU-FOOT-005"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 0.95
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
tags: ["construction", "lacing"]
---

# Knowledge Unit: Lacing Symmetry Heuristics

## 1. The Claim
Symmetrical eyelet counts, matching criss-cross patterns, and gravity-compliant lace drape are required between left and right shoes.

## 2. Evidence
- [ER-FOOT-003: Lacing Symmetry and Eyelet Integrity](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L52-L75)

## 3. Creative Implications
The prompt compiler must specify symmetrical eyelets, matching lacing, and lace tips capped with plastic or metallic aglets.

## 4. Associated Decision Rules
- [DR-FOOT-005: Symmetrical Lacing Rule](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```

---

```markdown
---
id: "KU-FOOT-006"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 0.95
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
tags: ["lighting", "suede"]
---

# Knowledge Unit: Angled Lighting for Suede Definition

## 1. The Claim
Suede requires angled side lighting to cast micro-shadows across the napped surface, rendering the pile texture readable.

## 2. Evidence
- [ER-FOOT-002: Suede Pile and Light Absorption](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L26-L50)

## 3. Creative Implications
Scene setups for suede shoes must use angled side key lights and avoid flat front light that washes out the texture.

## 4. Associated Decision Rules
- [DR-FOOT-006: Suede Lighting Rule](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```

---

## LEVEL 3: OBSERVED STATISTICS (PATTERNS)

```markdown
---
id: "KU-FOOT-007"
domain: "Human Expression"
specialization: "Footwear"
status: "Verified"
confidence_score: 0.90
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
tags: ["statistics", "framing", "camera"]
---

# Knowledge Unit: Low Camera Angle for Hero Shoes

## 1. The Claim
Historical premium footwear campaigns utilize low-angle camera positions (placed near or slightly above the floor line) in 78% of observed cases to emphasize sole treads and shoe volume.

## 2. Evidence
- [ER-FOOT-004: Sole Grounding & Shadows](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/evidence.md#L77-L100)

## 3. Creative Implications
When shoe campaign framing is under-specified, default the camera height to low-angle or floor-adjacent.

## 4. Associated Decision Rules
- [DR-FOOT-007: Default Footwear Framing](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Footwear/decision_rules.md)
```
