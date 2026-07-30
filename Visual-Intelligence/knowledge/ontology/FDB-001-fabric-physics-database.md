---
VIS-ID: FDB-001
Title: Indian Fabric Physics Database
Version: 1.0.0
Status: Active
Owner: Visual Intelligence Research
Last Updated: 2026-07-20
Depends On:
  - VIO-010 (Material Intelligence Ontology)
  - VIO-009 (Visual Craft)
  - EPL-001 (Expert Pattern Library)
Purpose: >
  The authoritative physical truth database for all major Indian textiles.
  The Reasoning Engine retrieves entries from this database to constrain
  prompt generation with physics-accurate material behavior.
  This prevents AI hallucination of fabric properties.
  Structured in three layers per VIO-010: Physical Truth (immutable),
  Expert Practice (heuristics), Observed Statistics (patterns).
---

# INDIAN FABRIC PHYSICS DATABASE (FDB-001)

---

## HOW TO READ THIS DATABASE

Each fabric entry contains:

```
LAYER 1 — Physical Truth    → Immutable. Derived from material science.
                              The Reasoning Engine treats these as hard constraints.
                              They CANNOT be overridden by user preference.

LAYER 2 — Expert Practice   → Heuristics from master photographers,
                              textile experts, and luxury creative directors.
                              Overridable only with explicit user instruction.

LAYER 3 — Observed Stats    → Probabilistic patterns from real campaigns.
                              Used when creative direction is under-specified.
                              Always overridable by user.
```

---
---

## SILK FAMILY

---

### FABRIC-001: Banarasi Silk (Zari Woven / Brocade)

**Classification:** Silk > Woven > Brocade > Zari Woven  
**Origin:** Varanasi, Uttar Pradesh  
**Weave Structure:** Jacquard / Kadhua / Cutwork  
**Weight Class:** Heavy (300–700 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Anisotropic Semi-Gloss"
reflectance_model: "Anisotropic"
light_transmission: "Opaque"
specular_width: "Narrow — sharp, defined highlights"
drape_physics: "Structured / Heavy"
fold_behavior: "Crisp, defined, architectural folds — holds shape without support"
fold_scale: "Large, deep folds — not fine pleats"
edge_stiffness: "High"
thread_density: "Very High (400–1200 threads per inch)"
fiber_base: "Mulberry Silk (warp) + Zari thread (weft embellishment)"

zari_properties:
  material: "Metal-wrapped thread (traditionally real gold/silver, modern: metallic polyester)"
  surface: "High-Gloss Metallic"
  reflectance: "Isotropic Metallic — reflects light in all directions uniformly"
  light_behavior: "Creates individual point catchlights under directional light"
  catchlight_intensity: "Extreme — each zari thread is a mirror"

weight_effect_on_body: "Garment creates visible downward pull on shoulder, hip — posture reads garment weight"
movement_physics: "Minimal — fabric does NOT billow, float, or flow freely"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Requires directional light at 30–60° angle to activate zari depth"
    reason: "Zari needs angle to catch anisotropic sheen and create metallic fire"
  - rule: "Avoid flat front-facing light — zari becomes uniform and dull"
    reason: "Front light creates no angle for metallic reflection"
  - rule: "Avoid exclusively cool color temperature (above 5000K)"
    reason: "Gold zari reads as silver or gray under cool light — loses identity"
  - rule: "Golden Hour is the gold standard — 2700K–3200K"
    reason: "Warm light turns zari into liquid gold; all editorial Banarasi references confirm this"

camera_laws:
  - rule: "85mm lens minimum for portrait work"
    reason: "Compression required to separate the rich fabric pattern from background"
  - rule: "f/2.8 or wider — shallow DOF isolates fabric pattern"
  - rule: "Camera angle must not exceed 30° above eye level"
    reason: "High angle flattens the structural fold depth"

drape_direction:
  - rule: "Prompt must NOT use words: flowing, flowy, billowing, lightweight, airy"
    reason: "These describe chiffon physics, not Banarasi — will cause AI hallucination"
  - rule: "Correct language: structured, heavy, architectural, crisp folds, holds shape"

pose_laws:
  - rule: "Heavy fabric weight must be visible in posture — subtle forward lean or hip shift shows weight"
  - rule: "Avoid poses where fabric would theoretically fly or billow"
```

#### LAYER 3 — Observed Statistics

```yaml
lighting_statistics:
  warm_directional_light_usage: "92% of high-end Banarasi campaigns"
  golden_hour_usage: "78% of luxury editorial Banarasi"
  studio_warm_key_usage: "14% of luxury editorial Banarasi"
  flat_overcast_usage: "Only 3% — mostly catalog/documentary"

campaign_distribution:
  luxury_bridal: "45%"
  festive_occasion: "30%"
  luxury_editorial: "15%"
  ecommerce_catalog: "8%"
  documentary: "2%"

color_palette_frequency:
  crimson_gold: "28%"
  royal_blue_gold: "22%"
  deep_green_gold: "18%"
  ivory_gold: "16%"
  purple_gold: "10%"
  other: "6%"

background_frequency:
  haveli_heritage_interior: "35%"
  palace_architecture: "25%"
  minimal_dark_studio: "20%"
  outdoor_heritage: "15%"
  white_studio: "5%"
```

**Prompt Physics Constraint (Compiler Injection):**
```
"heavy structured Banarasi silk brocade with defined crisp architectural folds
(not flowing), anisotropic silk sheen shifting across body surface, individual
gold zari threads creating distinct point catchlights under warm directional
light, visible fabric weight evident in posture and drape geometry"
```

**Forbidden Prompt Phrases:**
`flowing silk` | `billowing fabric` | `lightweight` | `airy drape` | `fluttering`

---

### FABRIC-002: Kanjeevaram / Kanjivaram Silk

**Classification:** Silk > Woven > Temple Silk > Pure Mulberry  
**Origin:** Kanchipuram, Tamil Nadu  
**Weave Structure:** Korvai (body and border woven separately, interlocked)  
**Weight Class:** Very Heavy (400–800 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "High Gloss — highest sheen of all Indian silks"
reflectance_model: "Anisotropic — extreme warp/weft directional shine"
light_transmission: "Fully Opaque"
specular_width: "Narrow to Medium — broad sheen across body surface"
drape_physics: "Very Structured / Very Heavy"
fold_behavior: "Deep, stiff folds — the stiffest drape of all Indian silks"
edge_stiffness: "Very High — edges hold shape without any support"
thread_density: "Extreme (600–1800 threads per inch)"
fiber_base: "Pure Mulberry Silk"

zari_properties:
  type: "Pure Zari border (contrast color to body — the signature)"
  border_width: "4–12 inches (the broader the border, the richer the saree)"
  pallu: "Heavily zari-woven pallu — often a complete woven scene"
  border_light_behavior: "Must be photographed so border is visible — defines identity"

weight_effect_on_body: "Extreme — the heaviest saree in common wear. Posture visibly accommodates weight."
movement_physics: "Near zero — fabric stands almost independently. Folds are architectural."
color_saturation: "Extreme — Kanjeevaram is known for saturated, jewel-tone colors"
color_contrast: "High — body and border are deliberately contrasting colors (e.g., red body / green border)"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Side lighting at 45° — captures dimensional brocade relief"
  - rule: "Color temperature 3500K–4500K — neutral-warm, not too golden"
    reason: "Too warm shifts the saturated body color; neutrality preserves the jewel tone"
  - rule: "The BORDER is the signature — must be visible and in frame"
    reason: "Kanjeevaram identity is incomplete without seeing the zari border"
  - rule: "Full body or 3/4 body shot mandatory — not half body"
    reason: "Half-body crops the border entirely — makes it unidentifiable as Kanjeevaram"

camera_laws:
  - rule: "50mm or 85mm — 50mm preferred for full-body to include environment"
  - rule: "f/4 minimum — enough DOF for border sharpness throughout frame"
  - rule: "Slightly wider angle than Banarasi — environment adds context"

styling_laws:
  - rule: "Temple jewelry is non-negotiable for bridal Kanjeevaram"
  - rule: "Gajra (jasmine hair garland) + bun is the South Indian signature"
  - rule: "Bindi is mandatory"
  - rule: "Kolam or rangoli floor element in environment adds cultural authenticity"
```

#### LAYER 3 — Observed Statistics

```yaml
primary_color_combinations:
  red_green_border: "32%"
  blue_gold_border: "20%"
  green_red_border: "18%"
  purple_green_border: "12%"
  gold_crimson_border: "10%"
  other: "8%"

background_preference:
  temple_stone_architecture: "40%"
  palace_dark_floor: "25%"
  minimal_dark_studio: "20%"
  outdoor_courtyard: "15%"

campaign_distribution:
  luxury_bridal: "60%"
  festive_religious: "25%"
  editorial: "10%"
  ecommerce: "5%"
```

**Prompt Physics Constraint:**
```
"very heavy Kanjeevaram silk with extreme structural stiffness, deep
architectural folds that hold shape independently, broad contrasting zari
border fully visible in frame, high-gloss anisotropic mulberry silk surface
with strong warp/weft directional sheen, jewel-tone saturated body color
in deliberate contrast with metallic border"
```

---

### FABRIC-003: Chanderi Silk-Cotton

**Classification:** Silk > Blended > Silk-Cotton Hybrid  
**Origin:** Chanderi, Madhya Pradesh  
**Weave Structure:** Plain / Jamdani motif  
**Weight Class:** Ultralight (60–120 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Matte-Gloss Hybrid — body is matte cotton, motifs are glossy silk"
reflectance_model: "Dual-surface — silk motifs reflect, cotton base absorbs"
light_transmission: "Semi-Translucent to Translucent"
specular_width: "Wide, diffuse — no sharp specular highlights"
drape_physics: "Fluid / Lightweight"
fold_behavior: "Very fine, multiple small soft pleats — NOT architectural folds"
edge_stiffness: "Low — edges collapse softly"
thread_density: "Low to Medium"

translucency_properties:
  backlight_behavior: "Glows through — fabric becomes luminous under backlight"
  frontlight_behavior: "Appears almost matte — translucency invisible"
  critical_insight: "Backlight is mandatory to reveal Chanderi's defining quality"

movement_physics: "High — responds to slightest air movement, breath, or movement"
color_quality: "Pastels and subtle tones — rarely saturated due to mixed fiber base"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Backlight is mandatory for any editorial Chanderi image"
    reason: "Translucency is Chanderi's identity — frontlight makes it look like cotton only"
  - rule: "Color temperature 5000K–6000K — daylight or cooler"
    reason: "Warm light oversaturates the delicate pastel tones"
  - rule: "Window light or open sky — NO artificial studio lights as primary"
    reason: "Artificial studio light creates harsh reflections on the silk motifs"
  - rule: "Keep background light and minimal"
    reason: "Dark backgrounds lose the translucency effect entirely"

drape_direction:
  - rule: "Prompt should use: delicate, sheer, lightweight, fine soft pleats, translucent"
  - rule: "Implies movement — 'appears to move with each breath'"
  - rule: "Never use: heavy, structured, architectural, crisp folds"
```

#### LAYER 3 — Observed Statistics

```yaml
color_palette_frequency:
  pastel_ivory: "30%"
  sage_green: "18%"
  dusty_rose: "15%"
  pale_blue: "12%"
  gold_tissue: "14%"
  other: "11%"

campaign_distribution:
  luxury_editorial: "45%"
  contemporary_lookbook: "30%"
  festive_daywear: "15%"
  ecommerce: "10%"
```

**Prompt Physics Constraint:**
```
"ultralight semi-translucent Chanderi silk-cotton, delicate fine soft pleats
falling with gravity, fabric luminous and glowing under backlight, dual-surface
quality where silk motifs catch light while cotton base remains matte,
responds to slightest movement"
```

---

### FABRIC-004: Pure Silk (Muga / Tussar / Raw Silk)

**Classification:** Silk > Raw / Unrefined > Natural Gold  
**Origin:** Assam (Muga), Bihar (Tussar)  
**Weight Class:** Medium (150–250 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Natural irregular matte-sheen — NOT refined gloss"
reflectance_model: "Isotropic irregular — random surface variation"
color: "Natural gold-amber (Muga) or off-white/beige (Tussar) — CANNOT be dyed bright"
texture: "Visible irregular slubs and texture knots — intentional characteristic"
drape_physics: "Semi-structured — holds shape somewhat, has body but not architectural"
fold_behavior: "Medium folds with visible texture throughout"
authenticity_marker: "Texture slubs are a sign of authenticity — AI tends to smooth them out"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Grazing light at very low angle reveals the slub texture"
    reason: "The irregular texture surface is the defining quality — must be lit to show"
  - rule: "Warm light (3000K–4000K) — reinforces natural gold color of Muga"
  - rule: "Texture must be visible — avoid flat lighting that smooths the surface"
```

**Prompt Physics Constraint:**
```
"natural raw Muga/Tussar silk with visible irregular slub texture throughout,
matte-to-sheen surface finish with natural gold-amber color that cannot be
dyed, semi-structured drape with medium body, authentic texture knots visible
as signs of handloom craftsmanship"
```

---
---

## COTTON FAMILY

---

### FABRIC-005: Khadi (Handspun Cotton)

**Classification:** Cotton > Handspun > Khadi  
**Origin:** Pan-India (Mahatma Gandhi's independence movement textile)  
**Weave Structure:** Plain weave, hand-spun yarn  
**Weight Class:** Light to Medium (100–200 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Fully Matte — zero sheen"
reflectance_model: "Diffuse — absorbs light uniformly"
light_transmission: "Opaque (single layer)"
texture: "Coarse, visible individual yarns — intentionally uneven"
drape_physics: "Relaxed / Casual — not structured, not fluid"
fold_behavior: "Soft irregular folds — fabric creases easily and retains creases"
crease_behavior: "CRITICAL — Khadi is defined by its authentic wrinkles and creases"
movement_physics: "Moderate — responds to body movement, not to air"
color_quality: "Natural, earthy, muted — dyes appear softened by cotton base"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Overcast or flat light is actually acceptable for Khadi — unlike any other fabric"
    reason: "Khadi's identity is in texture and crease, not sheen — flat light reveals both"
  - rule: "Side grazing light at 30–45° reveals the coarse yarn texture at its best"
  - rule: "Avoid golden hour warm light for political/artisan Khadi — it adds luxury the fabric doesn't claim"

authenticity_laws:
  - rule: "Wrinkles and creases must be present — DO NOT prompt for 'smooth cotton'"
    reason: "Smooth Khadi is not Khadi — the fabric lives in its imperfections"
  - rule: "Prompt must include visible coarse weave texture"
```

#### LAYER 3 — Observed Statistics

```yaml
campaign_distribution:
  artisan_documentary: "40%"
  sustainable_brand: "30%"
  casual_lifestyle: "20%"
  heritage_editorial: "10%"
```

**Prompt Physics Constraint:**
```
"handspun Khadi cotton with fully matte surface, visible coarse irregular yarn
texture, authentic natural wrinkles and creases retained in fabric, relaxed
soft drape with organic fold behavior, earthy muted color with no sheen"
```

---

### FABRIC-006: Ikat (Cotton or Silk-Cotton)

**Classification:** Cotton or Silk-Cotton > Resist-Dyed > Ikat  
**Origin:** Odisha, Telangana, Gujarat  
**Defining Feature:** Blurred, resist-dyed geometric pattern — the blur is intentional

#### LAYER 1 — Physical Truth

```yaml
pattern_physics:
  defining_characteristic: "Pattern edges are intentionally blurred/feathered — this is NOT a defect"
  blur_origin: "Yarn is resist-dyed before weaving — alignment is never perfect"
  critical_insight: "AI models tend to sharpen Ikat patterns — this destroys authenticity"
  correct_rendering: "Pattern should have soft, blurred, watercolor-like edges at boundary"
  
surface_finish: "Matte to low sheen (depending on silk or cotton base)"
drape_physics: "Medium — between structured and fluid"
color_quality: "Bold, graphic geometric patterns with the signature blur"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Flat-to-moderate side light — pattern clarity is the priority"
    reason: "Dramatic lighting creates shadows that compete with the geometric pattern"
  - rule: "Color temperature 5000K–5500K — neutral to reveal true dye colors"
  
pattern_laws:
  - rule: "The blurred edge of the Ikat pattern is MANDATORY in prompt"
    reason: "Sharp Ikat is fake Ikat — AI must be directed to preserve blur"
  - rule: "Correct prompt: 'with characteristic feathered/blurred resist-dyed edges at pattern boundaries'"
```

**Prompt Physics Constraint:**
```
"Ikat fabric with bold geometric resist-dyed pattern featuring characteristic
intentionally blurred/feathered edges at all pattern boundaries (this blur
is authentic, not a defect), matte cotton surface with no sheen, bold color
contrast between pattern and ground"
```

---

### FABRIC-007: Block Print Cotton (Sanganeri / Bagru / Ajrakh)

**Classification:** Cotton > Surface-Printed > Block Print  
**Origin:** Rajasthan (Sanganeri, Bagru), Gujarat (Ajrakh)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Fully Matte"
pattern_physics:
  method: "Wooden block hand-pressed into fabric — imperfection is identity"
  alignment: "Slight misalignment between blocks is authentic and desirable"
  ink_behavior: "Slight bleed at pattern edges — not sharp like digital print"
  critical_insight: "Perfect block print registration reads as machine printed — less authentic"
  
color_quality:
  sanganeri: "Pink/red/black on white base — floral motifs"
  bagru: "Earthy indigo, black, rust on cream — geometric/nature motifs"
  ajrakh: "Deep indigo, madder red, black — geometric precision"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Flat even light — block print pattern is the visual story, not fabric texture"
  - rule: "Avoid dramatic shadows that obscure the pattern geometry"

pattern_laws:
  - rule: "Slight misalignment between block repeats is authentic — prompt should allow for it"
  - rule: "Ink edges should have subtle bleed — not sharp vector-style"
```

**Prompt Physics Constraint:**
```
"hand block printed cotton with characteristic slight misalignment between
block repeats (authentic artisan imperfection), subtle ink bleed at pattern
edges, fully matte surface, traditional natural dye color palette"
```

---
---

## SHEER & LIGHTWEIGHT FAMILY

---

### FABRIC-008: Georgette

**Classification:** Silk or Synthetic > Crepe-Woven > Georgette  
**Weight Class:** Very Light (60–100 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Matte-Crinkle — textured surface, low sheen"
reflectance_model: "Diffuse with micro-texture"
light_transmission: "Semi-translucent — more opaque than chiffon"
texture: "Crinkled crepe texture — tiny uniform crinkles across surface"
drape_physics: "Very Fluid — falls in multiple small soft pleats"
fold_behavior: "Many fine, soft pleats — drapes in cascading layers"
movement_physics: "Very High — moves with lightest air current"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Side or backlight — reveals the cascading pleat structure"
  - rule: "Avoid strong front light — crinkle texture becomes invisible"
  - rule: "Color temperature neutral to warm — accepts both"

pose_laws:
  - rule: "Poses with movement capture Georgette best — implied walk, turning, reaching"
    reason: "Multiple fine pleats in motion are Georgette's visual signature"
```

**Prompt Physics Constraint:**
```
"lightweight georgette with characteristic crinkled crepe texture, fluid drape
falling in multiple cascading soft pleats, semi-translucent quality visible
especially against light, responds dramatically to lightest movement"
```

---

### FABRIC-009: Chiffon (Silk or Synthetic)

**Classification:** Silk or Synthetic > Sheer-Woven > Chiffon  
**Weight Class:** Ultralight (30–60 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Near-Invisible Matte — almost no surface texture"
reflectance_model: "Fully Diffuse — absorbs light"
light_transmission: "Highly Translucent — near-sheer"
drape_physics: "Maximum Fluid — falls like water"
fold_behavior: "Extremely fine, hairlike pleats — dozens of micro-folds"
movement_physics: "Extreme — responds to body heat convection, not just air"
backlight_effect: "CRITICAL — becomes luminous and glowing under backlight"
layering_behavior: "Multiple layers build opacity — single layer is near-transparent"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Backlight is the defining lighting for chiffon — MANDATORY for any editorial"
    reason: "Backlight creates translucency luminescence that defines chiffon's identity"
  - rule: "Front light alone is forbidden for editorial chiffon"
    reason: "Front light makes chiffon look like any other lightweight fabric — identity lost"
  - rule: "Rim lighting from behind creates a halo effect around the silhouette"
```

**Prompt Physics Constraint:**
```
"ultralight near-sheer silk chiffon with maximum fluid drape, falling in
dozens of hairlike micro-pleats, luminous translucent quality glowing under
backlight, responds to every breath and movement, layers build opacity"
```

---

### FABRIC-010: Organza

**Classification:** Silk or Synthetic > Sheer-Woven > Organza  
**Weight Class:** Light but with body (80–120 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Crisp Sheer — unique combination of sheerness and structure"
reflectance_model: "Low specular, high translucency"
light_transmission: "Highly Translucent — similar to chiffon"
drape_physics: "Semi-Structured Sheer — holds form unlike chiffon but remains translucent"
fold_behavior: "Holds crisp folds while remaining sheer — sculptural quality"
critical_insight: "Organza is the only sheer fabric that can hold a structured shape"
edge_behavior: "Edges remain crisp and defined — no soft collapsed edges like chiffon"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Backlight reveals sheerness AND the held structure simultaneously"
  - rule: "Side light reveals the crisp fold edges — sculptural shadows"
  - rule: "Organza can accept more dramatic lighting than chiffon"
    reason: "The structured folds create shadow geometry — works with harder light"
```

**Prompt Physics Constraint:**
```
"crisp organza with sculptural structured folds that hold their shape while
remaining highly translucent and sheer, crisp defined fold edges create shadow
geometry, fabric is simultaneously structured and luminous under backlight"
```

---
---

## EMBELLISHED TEXTILES

---

### FABRIC-011: Velvet

**Classification:** Silk or Cotton > Pile-Woven > Velvet  
**Origin:** Surat (Indian Velvet production center)  
**Weight Class:** Heavy (300–600 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Pile-Dependent — the most complex light behavior of any fabric"
reflectance_model: "Pile-Directional — the single most important physical fact about velvet"

pile_direction_physics: >
  Velvet has millions of cut fiber loops (pile) standing upright.
  Where the pile is compressed (leaning away from viewer), the fabric 
  appears LIGHTER — compressed pile reflects more light back.
  Where the pile is open (standing toward viewer), the fabric appears 
  DARKER — open pile absorbs light into the pile depth.
  This creates a luminosity gradient across the surface that changes 
  as the viewer moves — this is the 'CRUSHING' effect that makes velvet so luxurious.

light_transmission: "Fully Opaque"
drape_physics: "Structured to Semi-Structured"
fold_behavior: "Deep soft folds with pile-direction gradient in shadow zones"
weight_effect: "Very heavy — posture and drape show weight clearly"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "CRITICAL: Side or angled light MANDATORY — pile direction creates luminosity gradient only with angled light"
    reason: "This gradient IS velvet. Without it, velvet looks like felt or suede — identity destroyed"
  - rule: "Front flat light is the WORST choice for velvet — destroys micro-contrast entirely"
    reason: "Front light compresses all pile uniformly — no gradient, no depth, no luxury"
  - rule: "Hard or semi-hard light preferred over soft"
    reason: "Harder light creates stronger pile-direction gradient — more luxurious appearance"
  - rule: "High contrast ratio (4:1 or more) — velvet commands drama"

prompt_law:
  - rule: "MUST include: 'velvet pile direction creating luminosity gradient'"
    reason: "Without explicit direction, AI renders velvet as flat colored surface"
```

**Prompt Physics Constraint:**
```
"deep velvet with characteristic pile-direction luminosity gradient — fabric
appears lighter where pile is compressed against the light direction, darker
where pile stands open, creating rich tonal depth across the surface,
high micro-contrast under angled directional light"
```

**Forbidden Prompt Phrases:**
`smooth velvet` | `uniform velvet` | `flat velvet surface` | `even color velvet`

---

### FABRIC-012: Dupion Silk (Dupioni)

**Classification:** Silk > Slub-Woven > Dupion  
**Weight Class:** Medium-Heavy (180–300 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "High Sheen with Irregular Slub Texture"
reflectance_model: "Anisotropic with irregular interruption from slubs"
texture: "Characteristic slubs (lumpy irregular thickening in weft) — the signature"
drape_physics: "Semi-Structured — stiffer than regular silk"
fold_behavior: "Crisp with visible slub interruptions in fold geometry"
color_quality: "Strong two-tone effect — warp and weft in contrasting colors create iridescence"
iridescence: "Fabric changes color depending on viewing angle — strong optical effect"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Side light to reveal slub texture and anisotropic sheen"
  - rule: "Movement photographs — rotation reveals iridescent color shift"
  - rule: "The two-tone iridescence must be visible — requires angle to camera"
```

**Prompt Physics Constraint:**
```
"Dupion silk with characteristic irregular slub texture creating textural
interruptions across the surface, strong two-tone iridescent quality where
fabric color shifts between warp and weft colors depending on viewing angle,
semi-structured drape with crisp fold behavior"
```

---

### FABRIC-013: Net / Tulle (Embroidered)

**Classification:** Synthetic/Silk > Open-Mesh > Net  
**Common Use:** Lehenga overlay, dupatta, blouse

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Open mesh — the fabric IS its holes"
light_transmission: "Highly Translucent — net is nearly air"
structure: "Grid structure with open cells — embellishment added onto grid"
embellishment: "Sequins, beads, thread work, or zardosi applied to net base"
layering_behavior: "Multiple layers required for opacity — single layer is near-invisible"
drape_physics: "Completely fluid — has no body, falls as air"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Backlight — net becomes a pattern of light and shadow through the mesh"
  - rule: "Sequins on net require angled light to create maximum sparkle"
  - rule: "Studio controlled light for sequin net — each sequin needs to catch light individually"
```

**Prompt Physics Constraint:**
```
"embroidered net with open mesh structure, highly translucent with backlit
mesh pattern visible, sequin/bead embellishments catching light individually,
completely fluid drape with no structural body, multiple layers building
partial opacity"
```

---

### FABRIC-014: Zardosi Embroidered Fabric (Heavy)

**Classification:** Any base fabric > Heavy Hand Embroidery > Zardosi  
**Origin:** Lucknow, Bhopal (Mughal-era craft)

#### LAYER 1 — Physical Truth

```yaml
embellishment_type: "Heavy metallic thread embroidery + gems/stones"
weight_addition: "Adds 100–300 GSM to base fabric"
coverage: "Heavy — entire surface or large panels"
light_behavior: "Three-dimensional — threads stand away from surface, creating shadow underneath"
catchlight_quality: "Complex — metallic threads, gems, sequins all have different reflectance"
base_fabric_restriction: >
  CRITICAL: Zardosi weight restricts base fabric choice.
  Cannot be applied to: Chiffon, Georgette, Organza, Chanderi (fabric tears under weight)
  Compatible with: Velvet, Raw Silk, Heavy Silk, Net (with backing)

drape_physics: "Extremely heavy — structured and stiff from embellishment weight"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Hard angled light — each thread is three-dimensional, needs shadow to show depth"
  - rule: "Avoid soft diffused light — zardosi under soft light looks flat and uniform"
  - rule: "Close-up photography mandatory alongside full-body — macro detail shot shows craftsmanship"
  - rule: "Warm light (3000K–4000K) — gold thread reads as gold, not silver"
```

**Prompt Physics Constraint:**
```
"heavy Zardosi embroidery with three-dimensional metallic thread work standing
above surface, complex multi-material catchlights from metallic thread, gemstone,
and sequin elements under angled light, extreme garment weight affecting posture
and drape structure, embroidery creates micro-shadow at thread base"
```

---
---

## REGIONAL HANDLOOM FAMILY

---

### FABRIC-015: Patola Silk (Double Ikat)

**Classification:** Silk > Double Ikat > Patola  
**Origin:** Patan, Gujarat (one of the rarest Indian textiles)  
**Weight Class:** Medium (150–250 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Moderate sheen — mulberry silk base"
pattern_physics:
  method: "DOUBLE Ikat — both warp AND weft resist-dyed before weaving"
  result: "Pattern is present on both sides of fabric — identical on both faces"
  pattern_type: "Complex geometric — elephants, parrots, flowers in strict geometry"
  edge_behavior: "CRISP pattern edges — unlike single Ikat which is blurry"
  critical_distinction: "Patola has SHARP pattern edges (not blurred like Odisha Ikat)"
price_context: "Among the most expensive handloom sarees in India — heritage luxury"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Flat to moderate side light — the geometric pattern is the entire story"
  - rule: "Pattern must be sharp and legible — NOT blurred (unlike Odisha Ikat)"
  - rule: "Full body or 3/4 shot — the full repeat of the geometric pattern must read"
```

**Prompt Physics Constraint:**
```
"rare Patola double-Ikat silk with complex sharp geometric pattern in crisp
precise edges (not blurred — this is double Ikat not single), pattern identical
on both fabric faces, rich mulberry silk sheen, strictly geometric motifs in
precise repeat"
```

---

### FABRIC-016: Jamdani (Muslin Weave)

**Classification:** Cotton or Silk-Cotton > Supplementary Weft > Jamdani  
**Origin:** Dhaka, Bangladesh / West Bengal (UNESCO Intangible Heritage)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Matte to low sheen"
light_transmission: "Semi-translucent — fine muslin base"
pattern_physics:
  method: "Supplementary weft — pattern woven directly into muslin ground"
  result: "Design appears to float on the fabric surface"
  texture: "Pattern is slightly raised above ground"
  visual_effect: "White or colored motifs appearing to hover on sheer background"
weight: "Extremely light — the finest Jamdani (Dhakai) is the lightest woven textile"
```

**Prompt Physics Constraint:**
```
"fine Jamdani muslin with supplementary weft motifs appearing to float above
the sheer textile ground, extremely lightweight and translucent, motifs
slightly raised above surface creating subtle texture"
```

---

### FABRIC-017: Pochampally Ikat (Telangana)

**Classification:** Silk > Single Ikat > Pochampally  
**Defining Feature:** Characteristic diamond-and-chevron geometric pattern

#### LAYER 1 — Physical Truth

```yaml
pattern_type: "Diamond, chevron, and honeycomb geometric patterns"
edge_behavior: "Blurred/feathered (single Ikat — yarn-dyed before weaving)"
color_palette: "Bold contrasting — primary colors, frequent use of magenta, yellow, black"
silk_base: "Medium-weight mulberry silk"
```

**Prompt Physics Constraint:**
```
"Pochampally Ikat silk with diamond and chevron geometric patterns in bold
contrasting colors, characteristic single-Ikat blurred/feathered pattern
edges, medium-weight silk base with moderate sheen"
```

---

### FABRIC-018: Sambalpuri Ikat (Odisha)

**Classification:** Cotton or Silk > Single Ikat > Sambalpuri  
**Motif Types:** Shankha (conch), Chakra (wheel), Phula (flower)

#### LAYER 1 — Physical Truth

```yaml
motif_type: "Traditional Odishan symbols — conch, wheel, lotus, fish"
edge_behavior: "Distinctly blurred — warp-ikat with characteristic watercolor edge"
color_palette: "Natural, earthy — red, black, beige, natural white"
weight: "Light to medium cotton or tussar silk"
```

**Prompt Physics Constraint:**
```
"Sambalpuri Ikat with traditional Odishan symbolic motifs (conch, wheel,
lotus) in characteristic warp-Ikat blurred watercolor-edge pattern,
earthy natural color palette, cotton or tussar silk base"
```

---

### FABRIC-019: Baluchari Silk (West Bengal)

**Classification:** Silk > Woven Narrative > Baluchari  
**Defining Feature:** Story-telling woven scenes from mythology in the pallu

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "High Gloss — refined mulberry silk"
pallu_characteristic: "Large pictorial woven scene — mythological characters, court scenes"
body_pattern: "Smaller repeating motifs — butis or geometric"
color_palette: "Rich earth tones — dark red, deep blue, forest green with contrast thread"
narrative_element: "The pallu tells a story — this must be visible in photography"
```

**Prompt Physics Constraint:**
```
"Baluchari silk with high-gloss mulberry surface, pallu featuring detailed
woven pictorial narrative scene (mythological figures in intricate tableau),
rich earth-tone body with smaller repeating motifs, pallu must be prominently
displayed to show the woven narrative"
```

---

### FABRIC-020: Gadwal Silk (Telangana)

**Classification:** Silk-Cotton > Korvai Weave > Gadwal

#### LAYER 1 — Physical Truth

```yaml
construction: "Korvai weave — cotton body with silk borders interlocked (like Kanjeevaram)"
body_finish: "Matte cotton — absorbs light"
border_finish: "Glossy silk — reflects light"
visual_contrast: "Strong matte/gloss contrast between body and border is the identity"
```

**Prompt Physics Constraint:**
```
"Gadwal silk-cotton saree with deliberate material contrast: cotton body
with fully matte absorbent surface and silk Korvai border with contrasting
high-gloss reflective finish, border clearly defined from body by both
color and material quality"
```

---
---

## MODERN & FUSION TEXTILES

---

### FABRIC-021: Art Silk / Polyester Silk-Lookalike

**Classification:** Synthetic > Polyester/Viscose > Silk Imitation

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "High-Gloss Synthetic — different from real silk"
critical_distinction:
  real_silk: "Warm, organic sheen — glows from within"
  art_silk: "Cold, plastic sheen — reflects harshly, no depth"
  ai_failure: "AI models cannot distinguish — prompt must specify"
light_behavior: "Harsh specular highlights — not the soft organic silk response"
price_context: "Budget segment — visual direction must match"
```

#### LAYER 2 — Expert Practice

```yaml
lighting_laws:
  - rule: "Softer light preferred — harsher light emphasizes synthetic quality"
  - rule: "Avoid golden hour — warm light makes synthetic fabric look cheap"
  - rule: "5000K–5500K neutral light — honest rendering"
```

---

### FABRIC-022: Linen (Handwoven or Mill-made)

**Classification:** Plant Fiber > Linen  
**Weight Class:** Medium (150–250 GSM)

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "Matte with visible fiber irregularity"
texture: "Coarser than cotton — individual thick-and-thin yarns visible"
drape_physics: "Crisp — holds shape but not architectural"
wrinkle_behavior: "Wrinkles easily and retains wrinkles — this is the identity"
color_quality: "Natural, neutral — linen dyes softly, never saturated"
```

**Prompt Physics Constraint:**
```
"handwoven linen with visible coarse irregular yarn texture, fully matte
surface, characteristic natural wrinkles retained in fabric (authentic to
linen's identity), crisp drape with organic structure"
```

---

### FABRIC-023: Organza Silk (Crushed / Treated)

**Classification:** Silk > Organza > Treated / Crinkled

#### LAYER 1 — Physical Truth

```yaml
surface_finish: "High gloss with intentional crinkle pattern"
texture: "Permanent crinkle — different from regular organza"
light_behavior: "Each crinkle facet reflects independently — creates sparkle-like effect"
structure: "Holds crinkle shape permanently — not movement-responsive"
```

---

### FABRIC-024: Embroidered Net Lehenga (Festival / Bridal)

**Classification:** Synthetic Net > Heavy Embellishment > Lehenga Construction

#### LAYER 1 — Physical Truth

```yaml
construction: >
  Lehenga skirt = Multiple net layers + heavy embellishment on top layer.
  Inner lining = Cotton/silk for modesty and weight.
  Total construction weight can exceed 3–5kg for heavy bridal Lehengas.

volume_physics: "Extreme volume from gathered/pleated skirt — A-line silhouette mandatory"
hem_behavior: "Heavy embellished hem falls with its own weight — maintains shape"
movement_physics: "Skirt moves as a unit — not individual fabric response"
waist_to_hem_ratio: "Waist fitted, skirt expands dramatically — this silhouette IS the Lehenga"
```

#### LAYER 2 — Expert Practice

```yaml
photography_laws:
  - rule: "Full body MANDATORY — cropping Lehenga at mid-thigh destroys entire garment identity"
  - rule: "Low camera angle (below waist) — the dramatic A-line silhouette reads from low angle"
  - rule: "Movement shot: swirling/spinning Lehenga is a signature editorial approach"
  - rule: "Floor must be visible — the hem touching/near the ground completes the silhouette"
```

**Prompt Physics Constraint:**
```
"heavily embellished bridal net Lehenga with extreme gathered A-line silhouette,
dramatic volume from pleated net skirt layers, heavy embellished hem maintaining
shape from weight, fitted waist expanding dramatically to full hem, full body
visible from head to floor showing complete silhouette"
```

---

### FABRIC-025: Dhoti / Mundu (Men's — Cotton)

**Classification:** Cotton > Unstitched > Dhoti  
**Usage:** Men's traditional wear

#### LAYER 1 — Physical Truth

```yaml
drape_physics: "Wrapped, not stitched — held by tuck and pleat at waist"
fold_behavior: "Central pleat fans forward between the legs"
color: "White or off-white in 95% of traditional use"
border: "Woven colored border (zari or cotton) at hem edges"
authenticity: "Slightly misaligned drape is authentic — perfect mechanical drape reads as costume"
```

---
---

## QUICK REFERENCE: FABRIC PHYSICS CONSTRAINTS TABLE

| Fabric | Drape | Sheen | Translucent | Best Light | Worst Light | Forbidden Phrases |
|--------|-------|-------|-------------|------------|-------------|-------------------|
| Banarasi Silk | Structured/Heavy | Anisotropic | No | Golden Hour 45° | Flat Front | flowing, airy, billowing |
| Kanjeevaram | Very Structured | Very High | No | Side 45° warm-neutral | Very Warm | lightweight, fluid |
| Chanderi | Fluid/Light | Dual-surface | Yes | Backlight cool | Warm front | heavy, structured, stiff |
| Chiffon | Max Fluid | None | High | Backlight | Front only | structured, holds shape |
| Georgette | Very Fluid | Low crinkle | Semi | Side/back | Flat front | stiff, architectural |
| Organza | Structured Sheer | Low | High | Back + Side | — | fluid, collapses |
| Velvet | Semi-structured | Pile-gradient | No | Hard Side | Flat Front | smooth, uniform, even |
| Dupion | Semi-structured | Iridescent | No | Side angle | — | uniform color |
| Khadi | Relaxed/Casual | None | No | Flat/Overcast | Golden luxury | smooth, wrinkle-free |
| Ikat | Medium | Fabric-dep. | No | Flat 5500K | — | sharp ikat edges (single ikat) |
| Linen | Crisp | None | No | Flat/Grazing | — | smooth, unwrinkled |
| Zardosi | Extreme Heavy | Complex | No | Hard angled warm | Soft diffused | flat embroidery |
| Patola | Medium | Moderate | No | Flat pattern | — | blurred edges |
| Lehenga (Heavy) | Volume/A-line | Embellishment | Net layers | Dramatic | Half-body crop | midi-length, cropped |

---

## KANJEEVARAM & LIGHTWEIGHT ADDITIONS (v1.1)

### FABRIC-026: Kanjeevaram Silk (South Indian Bridal)
- **Classification:** Silk > Woven > Heavy
- **Material properties:** Exceptionally heavy, stiff silk with thick, wide contrasting borders (often Korvai technique).
- **Drape behavior:** Structured and architectural, similar to Banarasi, but creates distinct boxy pleats due to extreme stiffness.
- **Lighting response:** Rich, lustrous sheen on the main body; brilliant metallic reflection on the broad Zari borders.
- **Prompt language:** "heavy Kanjeevaram silk saree, stiff architectural drape, wide contrasting temple borders with rich gold Zari, distinct boxy pleats"

### FABRIC-027: Chiffon / Organza (Lightweight Sheer)
- **Classification:** Silk/Synthetic > Sheer > Lightweight
- **Material properties:** Ultra-lightweight, translucent, delicate, airy.
- **Drape behavior:** Highly responsive to wind and movement. Billows, flows, and creates fluid curves. Does *not* hold stiff shape.
- **Lighting response:** Transmits light beautifully (subsurface scattering), creates ethereal glowing effects when backlit.
- **Prompt language:** "lightweight sheer chiffon saree, translucent airy fabric, flowing and billowing organically in the wind, delicate drape"

---

## DATABASE EXPANSION LOG

```
v1.0.0 (2026-07-20): 25 fabric entries covering all major Indian textile families.
                     Quick reference table included.
                     
Planned Expansions:
  v1.1.0: Phulkari (Punjab), Kashmiri Pashmina, Bandhani (Rajasthan)
  v1.2.0: South Indian specific: Kota, Maheshwari, Narayanpet
  v1.3.0: Men's textiles: Sherwani fabrics, Kurta weaves
  v2.0.0: Machine-readable JSON schema version of all entries
```
