# Knowledge: Sarees

This document collects the verified Knowledge Units (KUs) for the Saree module, structured according to the three levels of the Material Intelligence pipeline.

---

## LEVEL 1: PHYSICAL TRUTH (IMMUTABLE)

```markdown
---
id: "KU-SAREE-001"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "drape", "banarasi"]
---

# Knowledge Unit: Banarasi Silk Drape Weight & Folds

## 1. The Claim
Heavy Banarasi silk (300–700 GSM) forms crisp, structured, architectural folds that hold their shape under gravity without billowing or floating.

## 2. Evidence
- [ER-SAREE-001: Banarasi Silk Material Physics](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L1-L26)

## 3. Creative Implications
Prompts must use architectural and crisp folding language. Billowing or fluid descriptors will cause AI rendering engines to output physically inaccurate georgette/chiffon drapes, ruining Banarasi authenticity.

## 4. Associated Decision Rules
- [DR-SAREE-001: Banarasi Drape Constraints](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

```markdown
---
id: "KU-SAREE-002"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "zari", "banarasi"]
---

# Knowledge Unit: Zari Thread Light Reflectance

## 1. The Claim
Metallic zari threads woven into Banarasi brocade act as individual micro-mirrors, creating intense point catchlights and isotropic metallic reflections under directional light.

## 2. Evidence
- [ER-SAREE-001: Banarasi Silk Material Physics](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L1-L26)

## 3. Creative Implications
To highlight zari embroidery details, the render prompt must explicitly trigger metallic reflections, point catchlights, and micro-contrast.

## 4. Associated Decision Rules
- [DR-SAREE-002: Zari Lighting Requirement](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

```markdown
---
id: "KU-SAREE-003"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["physics", "drape", "kanjeevaram"]
---

# Knowledge Unit: Kanjeevaram Silk Stiffness & Posture

## 1. The Claim
Kanjeevaram silk is an extremely heavy and stiff fabric that holds rigid, thick folds, requiring the wearer's physical posture (hips, shoulders) to visibly adjust to the drape's downward weight.

## 2. Evidence
- [ER-SAREE-002: Kanjeevaram Silk Material Physics](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L28-L53)

## 3. Creative Implications
Pose prompting must carry heavy posture language, and fabric folds must be described as deep, thick, and stiff.

## 4. Associated Decision Rules
- [DR-SAREE-003: Kanjeevaram Posture Rule](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

```markdown
---
id: "KU-SAREE-004"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "translucency", "chanderi"]
---

# Knowledge Unit: Chanderi Semi-Translucency & Light Transmission

## 1. The Claim
Chanderi fabric is lightweight and semi-translucent, transmitting light through the open weave cotton-silk base while silk-woven motifs remain opaque and reflective.

## 2. Evidence
- [ER-SAREE-003: Chanderi Translucency & Optics](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L55-L77)

## 3. Creative Implications
To render Chanderi authentic to its physical properties, backlighting must be used to reveal the light transmitting through the warp and weft.

## 4. Associated Decision Rules
- [DR-SAREE-004: Chanderi Translucency Lighting](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

```markdown
---
id: "KU-SAREE-005"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 1.00
created_at: "2026-07-27"
level: "Level 1: Physical Truth"
tags: ["optics", "reflectance", "velvet"]
---

# Knowledge Unit: Velvet Pile directional Reflectance

## 1. The Claim
Velvet uses a pile-directional reflectance model: compressed pile reflects light (reads lighter) and open pile absorbs light (reads darker), creating a dynamic crushing gradient across folds.

## 2. Evidence
- [ER-SAREE-004: Velvet Pile & Chiaroscuro](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L79-L99)

## 3. Creative Implications
Prompts must specify the pile-direction luminosity gradient to prevent the rendering engine from creating flat, uniform velvet.

## 4. Associated Decision Rules
- [DR-SAREE-005: Velvet Pile Reflectance Rule](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

## LEVEL 2: EXPERT HEURISTICS (PRACTICE)

```markdown
---
id: "KU-SAREE-006"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 0.95
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
tags: ["lighting", "editorial", "zari"]
---

# Knowledge Unit: Angled Lighting for Zari Enrichment

## 1. The Claim
Side/grazing lighting at a 30°–60° angle is required to activate the texture of metallic zari and avoid the flat, dull look caused by front-facing light.

## 2. Evidence
- [ER-SAREE-005: Luxury Bridal Visual Direction](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L101-L126)

## 3. Creative Implications
The rendering pipeline must inject 45-degree angled lighting constraints for any saree containing gold/silver brocade or zari work.

## 4. Associated Decision Rules
- [DR-SAREE-006: Zari Light Angle](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

```markdown
---
id: "KU-SAREE-007"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 0.95
created_at: "2026-07-27"
level: "Level 2: Expert Heuristics"
tags: ["framing", "camera", "kanjeevaram"]
---

# Knowledge Unit: Kanjeevaram Framing Constraints

## 1. The Claim
Kanjeevaram sarees require full-body or three-quarter framing to keep the broad signature interlocked border fully visible in frame.

## 2. Evidence
- [ER-SAREE-005: Luxury Bridal Visual Direction](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L101-L126)

## 3. Creative Implications
The compiler must restrict camera framing to full-body or three-quarter and forbid close-up portrait framing unless specifically overriding for detail macros.

## 4. Associated Decision Rules
- [DR-SAREE-007: Kanjeevaram Framing Rules](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```

---

## LEVEL 3: OBSERVED STATISTICS (PATTERNS)

```markdown
---
id: "KU-SAREE-008"
domain: "Human Expression"
specialization: "Sarees"
status: "Verified"
confidence_score: 0.85
created_at: "2026-07-27"
level: "Level 3: Observed Statistics"
tags: ["statistics", "campaign", "bridal"]
---

# Knowledge Unit: Luxury Bridal Campaign Lighting Statistics

## 1. The Claim
Historical luxury bridal campaigns for Banarasi and Kanjeevaram silks utilize warm golden-hour light (2700K–3200K) in 92% of observed cases to reinforce heritage luxury.

## 2. Evidence
- [ER-SAREE-005: Luxury Bridal Visual Direction](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/evidence.md#L101-L126)
- [FDB-001: Banarasi Statistics](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/knowledge/ontology/FDB-001-fabric-physics-database.md#L115-L120)

## 3. Creative Implications
When lighting is under-specified by the user, the platform should default to golden hour or warm directional lighting to match luxury standards.

## 4. Associated Decision Rules
- [DR-SAREE-008: Default Luxury Lighting](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Intelligence%20Layer/Human%20Expression/Sarees/decision_rules.md)
```
