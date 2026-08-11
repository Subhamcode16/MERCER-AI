---
VIS-ID: SDB-001
Title: Studio & Environment Database
Version: 1.0.0
Status: Active
Owner: Visual Intelligence Research
Last Updated: 2026-07-20
Depends On:
  - VIO-009 (Visual Craft)
  - VIO-010 (Material Intelligence)
  - EPL-001 (Expert Pattern Library)
Purpose: >
  The authoritative database of every shoot environment type — studio and
  location — with full lighting compatibility, backdrop physics, floor
  behavior, and prompt construction rules. The Reasoning Engine queries
  this database alongside FDB-001 to ensure the environment chosen is
  physically and aesthetically coherent with the garment and campaign.
---

# STUDIO & ENVIRONMENT DATABASE (SDB-001)

---

## ARCHITECTURE OF AN ENVIRONMENT

Every shoot environment has three physical layers that interact with the subject and garment:

```
BACKGROUND LAYER    → What is behind the subject (wall, canvas, sky, architecture)
FLOOR LAYER         → What the subject stands on (creates reflections, context, story)
ATMOSPHERE LAYER    → What exists in the air between subject and camera (haze, particles, nothing)
```

All three must be specified. Most AI prompts only describe the background.
Atelier specifies all three — this is the primary reason Atelier-generated images
have environmental depth that generic prompts do not.

---
---

## STUDIO ENVIRONMENTS

---

### ENV-001: Grey Textured Cyclorama (The Sculptural Neutral)

**As seen in:** Image 1 of the reference set (billowing veil portrait)

#### What It Is
A curved seamless studio wall-floor junction painted in a textured mid-grey.
The texture is visible but subtle — concrete-like, plaster-like, or matte
painted canvas. It is NOT a flat digital grey. The texture catches light
differently across the sweep of the wall, creating tonal variation.

#### Background Layer
```yaml
color: "Mid warm grey — approximately HSL(30°, 5%, 55%)"
texture: "Matte plaster or concrete texture — visible micro-roughness"
tonal_variation: "Lighter at top (skylight reflection), darker at sides — NOT uniform"
seamless_curve: "Wall meets floor in a continuous curve — no visible horizon line"
edges: "Slightly darker at extreme left and right — natural light falloff"
depth: "Background appears to recede — gradient from lighter center to darker edges"
prompt_language: >
  "seamless grey textured studio cyclorama, warm matte plaster texture,
  slight tonal variation from lighter center to darker edges, no visible
  horizon line, soft studio atmosphere"
```

#### Floor Layer
```yaml
material: "Same seamless sweep — grey matte"
reflectivity: "Very low — matte floor, minimal subject reflection"
visibility: "Floor visible at bottom of frame but not a visual statement"
prompt_language: "seamless matte grey studio floor, minimal reflection"
```

#### Atmosphere Layer
```yaml
particles: "None — controlled studio"
haze: "None — clean studio air"
quality: "Pure — no atmospheric interference"
```

#### Lighting Compatibility
```yaml
excellent:
  - "Split/Rembrandt — side lighting creates tonal gradient across grey surface"
  - "Soft beauty dish — wraps the subject against the neutral"
  - "High contrast single source — grey absorbs and doesn't compete"
  - "Hair/rim light — separates subject from same-tone background"
good:
  - "Large softbox — even, clean, editorial"
  - "Overhead dramatic — god-ray effect against grey"
poor:
  - "Flat even studio (no separation from background)"
  - "Very warm tungsten (grey turns orange — loses neutrality)"
forbidden:
  - "No light on background — subject and background blend together"

separation_rule: >
  Grey background requires deliberate subject separation.
  Rim light or hair light mandatory when subject's clothing is similar in
  value to the grey background (e.g., white dress against grey — MUST have
  rim to prevent background merge).
```

#### White-on-White Law (Critical)
```yaml
problem: >
  White dress against grey background — the white fabric can blow out
  or lose all texture if not carefully lit. This is the most common AI
  failure mode with this setup.
solution: >
  Background must be UNDEREXPOSED relative to subject dress.
  Fabric texture must be preserved — no blown highlights on dress.
  Correct: "soft wrap light on dress preserving all fabric texture,
  background slightly underexposed for separation"
prompt_law: >
  "fabric texture fully preserved and visible — no blown highlights,
  background intentionally slightly darker than subject for separation,
  rim light creating edge definition against grey"
```

#### Full Environment Prompt Block
```
"seamless warm grey textured studio cyclorama, matte plaster wall surface
with subtle concrete-like micro-texture, tonal gradient from lighter center
to darker edges, no visible horizon line where wall meets floor, matte grey
studio floor with minimal reflection, controlled studio atmosphere — clean
air, no particles, subject illuminated with separation from background via
rim lighting"
```

---

### ENV-002: White High-Key Studio (The Luminous Void)

**As seen in:** Image 2 of the reference set (water reflection silhouette)

#### What It Is
A deliberately overexposed white studio background where the background
becomes a pure light source — a luminous void. The subject is intentionally
darker than the background, creating a silhouette or near-silhouette effect.
The water floor element makes this specific version uniquely powerful.

#### Background Layer
```yaml
color: "Pure white — deliberately overexposed"
technique: "Background lit independently — 2–4 stops brighter than subject"
effect: "Background becomes a glowing light source, not a surface"
horizon: "Invisible — floor and wall merge in light"
prompt_language: >
  "pure white high-key studio background, deliberately overexposed to create
  a luminous void — background acts as a light source, no visible wall or
  floor texture, seamless white infinity"
```

#### Floor Layer — CRITICAL ELEMENT (Water Surface)
```yaml
type: "Standing still water — 3–10cm depth"
surface: "Mirror-perfect reflection when water is completely still"
reflection_quality: "Subject reflected perfectly below — creates vertical symmetry"
color: "Water picks up grey-blue from studio atmosphere — NOT pure white"
edge: "Floor transitions from dry (camera-side) to wet (subject standing point)"
visual_effect: >
  The reflection extends the subject downward — two figures in one.
  The upper subject is in focus, the reflection is in slightly different
  focus plane creating a dreamlike quality.
prompt_language: >
  "subject standing in shallow still water (5cm depth), perfect mirror
  reflection visible below — water surface completely calm, grey-blue
  tonal quality to water surface, soft reflection edges, floor transitions
  from dry studio to shallow water pool"
prompt_law: >
  The water must be STILL. Any ripple destroys the reflection.
  Correct: "perfectly still mirror-surface water"
  Forbidden: "rippling water, moving water, waves"
```

#### Lighting Compatibility
```yaml
defining_technique: "High-key background with subject in relative shadow"
subject_lighting: "Wrap front light — soft, maintains detail despite high-key"
background_lighting: "Independently lit — much brighter than subject"
silhouette_control: >
  The degree of silhouette is controlled by the ratio:
  - Strong silhouette: Background 4+ stops brighter than subject
  - Near-silhouette: Background 2 stops brighter
  - Detail preserved: Background 1 stop brighter
rim_light: "Optional — creates edge definition without breaking high-key mood"
forbidden:
  - "Dark background (defeats entire environmental concept)"
  - "Flat even exposure (destroys high-key dramatic effect)"
```

#### Garment Compatibility
```yaml
excellent:
  - "White/silver/ivory bridal gowns with volume (silhouette reads against light)"
  - "Any heavily embellished garment (embellishment catches background glow)"
  - "Structured silhouette garments — the shape is the story"
poor:
  - "Dark garments (merge with the intended underexposed subject zone)"
  - "Patterned fabrics (pattern lost when subject darkened)"
```

#### Full Environment Prompt Block
```
"pure white high-key studio — background independently lit to luminous
overexposed void acting as a glowing light source, no visible wall or floor
edges, seamless white infinity, subject standing in perfectly still shallow
water (5cm) creating a flawless mirror reflection below, water surface
grey-blue with tonal depth, soft wrap lighting on subject preserving detail
against the luminous white void behind"
```

---

### ENV-003: Painted Canvas / Draped Fabric Backdrop (The Theatrical Stage)

**As seen in:** Image 3 of the reference set (cathedral veil, dark green)

#### What It Is
A large hand-painted canvas or draped fabric (velvet, muslin, or silk)
hung behind the subject as a backdrop. Common in fine art portrait
photography and high fashion editorial. The texture of the canvas or
fabric is visible, painted with tonal variation — greens, blues, greys,
earthy umbers. This is the backdrop of old masters' paintings — it
deliberately references Renaissance and Baroque portraiture.

#### Background Layer
```yaml
type: "Painted artist's canvas OR draped fabric (muslin, velvet)"
texture: "Visible fabric/canvas weave — NOT a smooth wall"
color_variation: "Hand-painted tonal variation — lighter in center, darker at edges"
drape_behavior: "If fabric backdrop: gentle natural folds and drape visible"
reference_aesthetic: "Old Master painting, Baroque portraiture, Art studio"

color_profiles:
  dark_green_hunter:
    base: "HSL(140°, 35%, 20%)"
    variation: "Lighter sage center, deep forest edges"
    mood: "Romantic, classical, botanical"
    prompt: "hand-painted dark hunter green canvas backdrop with lighter sage
             center fading to deep forest edges, visible canvas texture, old
             master painting aesthetic"
  
  warm_umber_brown:
    base: "HSL(30°, 40%, 25%)"
    variation: "Warm amber center, deep tobacco edges"
    mood: "Heritage, classical, Dutch Golden Age"
  
  deep_charcoal_blue:
    base: "HSL(220°, 20%, 20%)"
    variation: "Lighter blue-grey center, near-black edges"
    mood: "Dramatic, cinematic, contemporary editorial"
  
  warm_ivory_cream:
    base: "HSL(45°, 30%, 80%)"
    variation: "Bright warm center, aged parchment edges"
    mood: "Romantic, soft luxury, vintage"
    prompt: "hand-painted warm cream ivory canvas backdrop, soft warm center
             with aged parchment edges, delicate tonal variation"
```

#### The God-Ray / Cathedral Light Effect (Critical for Image 3)
```yaml
what_it_is: >
  A single narrow beam of light entering from above or behind through
  the veil/fabric, creating a visible cone of light in the air.
  This is the defining lighting element of Image 3.
how_it_works: >
  A hard, narrow light source (Fresnel, snoot, or spotlight) aimed
  through the translucent veil fabric. The light scatters through the
  veil material creating a visible atmospheric cone.
requires:
  - "Translucent veil/fabric element in the scene (veil, dupatta, organza)"
  - "Atmospheric particles in air (smoke machine, fine mist) to make beam visible"
  - "Dark background so the beam is visible against depth"
prompt_language: >
  "dramatic single overhead spotlight creating a visible cathedral light
  beam through translucent veil material, atmospheric mist making light
  beam visible in air, cone of light from above illuminating subject from
  within the veil, dark painted canvas background making light beam dramatic"
```

#### Floor Layer
```yaml
type: "Dark studio floor — same dark tone as background"
reflectivity: "Very low — matte"
fabric_contact: "Dress train/hem touches floor — floor must be clean and dark"
prompt_language: "dark matte studio floor, continuous with backdrop tone"
```

#### Lighting Compatibility
```yaml
excellent:
  - "Single dramatic overhead/backlight through veil (god-ray effect)"
  - "Rembrandt — classic portrait lighting referencing old master paintings"
  - "Split lighting — high contrast against the textured dark background"
good:
  - "Large softbox — but loses the theatrical drama"
poor:
  - "High-key flat studio (defeats all texture and drama)"
  - "Cool color temperature (painted canvas reads as warm — cool light fights it)"
```

#### Full Environment Prompt Block (Dark Green / Image 3 Reference)
```
"hand-painted dark hunter green artist's canvas backdrop with visible canvas
texture, lighter sage green center fading to deep forest green edges — tonal
variation referencing old master portrait painting, dramatic single overhead
spotlight beam visible through translucent cathedral veil material, fine
atmospheric mist making the light cone visible in air, dark matte studio floor
continuous with backdrop tone, warm theatrical lighting quality"
```

---

### ENV-004: Minimal Textured Wall (Contemporary Editorial)

**Classification:** Studio > Architectural > Minimal Contemporary

#### Background Layer
```yaml
type: "Concrete, lime plaster, or textured wall surface"
color: "Warm grey, warm white, or warm beige — never cool"
texture: "Micro-texture of real material — concrete pores, plaster irregularity"
prompt_language: >
  "warm raw concrete wall surface with visible material texture, matte
  micro-porous surface, subtle tonal variation across face"
```

#### Compatibility
```yaml
excellent: "Any garment — universal neutral for contemporary editorial"
lighting: "Large softbox or window — texture needs grazing light to be visible"
```

---

### ENV-005: Black Studio / Dark Void

**Classification:** Studio > Dark > Dramatic  

#### Background Layer
```yaml
color: "Near-black — HSL(0°, 0%, 5–10%)"
quality: "Absorbs all light — subject appears to emerge from darkness"
effect: "Subject floats in void — maximum drama"
prompt_language: "pure black studio void, subject emerging from darkness, no background detail"
```

#### Critical Lighting Rule
```yaml
rule: >
  Dark void requires STRONG key light on subject — no ambient fill.
  Subject must be the only source of light information in the frame.
  Any background illumination destroys the void effect.
required: "High contrast key light, no fill, no background light"
```

---
---

## LOCATION ENVIRONMENTS

---

### ENV-006: Heritage Haveli Interior

**Classification:** Location > India > Heritage Residential

#### Environment Description
```yaml
architecture: "2–5 story courtyard mansion, Mughal or Rajput period"
materials: "Red sandstone, limestone, carved marble, wooden latticework (jali)"
characteristic_elements:
  - "Internal open courtyard with central space and tiered balconies"
  - "Carved stone columns (pillars) — fluted or decorated"
  - "Jali screens — geometric or floral pierced stone that casts shadow patterns"
  - "High arched doorways with ornate surrounds"
  - "Stone floor — often marble or lime plaster, with some reflectivity"
light_quality: >
  Interior light comes through jali screens and high windows —
  creating geometric shadow patterns on walls and floors.
  Golden hour: dramatic angled light shafts through jali.
  Blue hour: cool ambient with warm practical lights inside.
```

#### Floor Layer
```yaml
material: "Polished marble or lime plaster"
reflectivity: "Moderate — partial soft reflection of subject"
shadow_patterns: "Jali screen geometry cast on floor — adds visual interest"
prompt_language: >
  "polished marble haveli floor with partial soft subject reflection,
  geometric jali shadow patterns cast across floor surface"
```

#### Atmosphere Layer
```yaml
particles: "Atmospheric dust in shafts of light through jali screens"
quality: "Warm, slightly hazy — feels inhabited and real"
prompt_language: "visible atmospheric dust particles in angled light shafts, warm hazy quality"
```

#### Full Prompt Block
```
"interior of ancient Rajasthani haveli — carved limestone columns,
ornate jali stone screens casting geometric shadow patterns, polished
marble floor with partial soft reflections, warm golden hour light
entering through jali as angled atmospheric beams revealing dust
particles, high arched doorways, tiered stone balconies visible at depth"
```

---

### ENV-007: Palace / Royal Architecture

**Classification:** Location > India > Royal Heritage

```yaml
scale: "Grander than haveli — halls, throne rooms, formal gardens"
materials: "White marble, sandstone, onyx inlay, gold leaf"
characteristic_elements:
  - "Large formal halls with high ceilings (8–15m)"
  - "Pietra dura marble inlay floors"
  - "Monumental doorways with intricate stone carving"
  - "Formal Mughal garden with water channels (chahar bagh)"
  - "Pavilions and jharokha (overhanging balcony windows)"
light_quality: "Formal, directional — light enters through defined architectural openings"
floor_reflectivity: "High — white marble creates strong subject reflections"
prompt_language: >
  "grand Mughal palace interior — white marble with pietra dura inlay floor,
  high carved stone ceiling, monumental arched doorways, polished marble
  creating subject reflection below, formal architectural scale"
```

---

### ENV-008: Temple Corridor (Architectural Use)

**Classification:** Location > India > Sacred Architecture (Non-devotional use)

```yaml
characteristic_elements:
  - "Long colonnade of carved stone pillars — strong repetition"
  - "Dim ambient light between pillars"
  - "Strong directional shaft of light at specific points"
  - "Carved gopuram elements in background at depth"
  - "Dark cool shadow vs warm directional light contrast"
materials: "Black granite (South India), red sandstone (North India), white limestone"
floor: "Stone floor — low reflectivity, rough texture"
atmosphere: "Incense haze (documentary) or clean (editorial)"
prompt_language: >
  "ancient South Indian temple stone corridor — repeated carved black granite
  columns creating strong geometric rhythm, dramatic shaft of directional
  sunlight through column gaps, cool shadow zones alternating with warm lit
  zones, carved stone floor"
```

---

### ENV-009: Outdoor Natural Light — Golden Hour Field / Garden

**Classification:** Location > Outdoor > Natural Light

```yaml
light_source: "Direct low sun — 15–45 minutes before sunset"
color_temperature: "2700K–3400K — extreme warm amber"
quality: "Hard-edged directional — casts long soft shadows"
background_options:
  dry_grass_field: "Warm amber tones — matches golden hour color"
  heritage_garden: "Formal garden, fountain, geometric hedges"
  flowering_trees: "Cherry/gulmohar/bougainvillea — color pop against dress"
  courtyard_steps: "Stone steps of any heritage architecture"

golden_hour_atmosphere:
  haze: "Natural atmospheric haze at depth — feels warm and volumetric"
  dust: "Dust particles in backlight — visible on dark clothing areas"
  bokeh: "Background warm blur — out-of-focus warm golden circles"
  
prompt_language: >
  "outdoor golden hour photography, warm amber directional sunlight at 15°
  from horizon, 2900K color temperature, long soft shadows, warm atmospheric
  haze at background depth, bokeh of warm golden ambient light"
```

---

### ENV-010: Water / Reflective Surface Environments

**Classification:** Environment > Surface Type > Reflective

#### Sub-type A: Shallow Indoor Pool (Studio-controlled)
```yaml
depth: "3–8cm — just enough for reflection, shallow enough for safety"
water_state: "MUST be completely still — any ripple destroys mirror quality"
reflection_quality: "Perfect mirror — subject reflected exactly below"
floor_visibility: "Dark floor visible through water adding depth"
color: "Water takes on ambient light color — slightly darker than ambient"
setup_time: "Water must settle 10+ minutes after disturbance before shooting"
prompt_language: >
  "subject standing in perfectly still shallow studio water (5cm), flawless
  mirror reflection below — water surface absolutely calm, slight grey-blue
  tonal quality to water, dark studio floor visible beneath water at depth"
```

#### Sub-type B: Natural Outdoor Water (Lake / River / Ocean)
```yaml
lake_still_surface:
  best_time: "Dawn or dusk — minimal wind"
  reflection_quality: "Near-perfect in calm conditions"
  color: "Reflects sky color — golden at sunset, blue-grey otherwise"
  atmosphere: "Mist over water at dawn adds magic"
  
ocean_edge:
  type: "Wet sand at wave edge — film of water creates partial reflection"
  reflection_quality: "Distorted, impressionistic — not mirror perfect"
  mood: "More dynamic, less controlled than studio water"

prompt_language_lake: >
  "subject standing at edge of completely still lake at golden hour, perfect
  mirror reflection on water surface, warm amber sky reflected in water,
  gentle mist at water level, mountains or trees reflected at depth"

prompt_language_ocean: >
  "subject at ocean shoreline, standing on reflective wet sand at wave recede,
  partial distorted reflection in thin film of receding water, horizon visible,
  dramatic sky"
```

---
---

## ENVIRONMENT-TO-CAMPAIGN COMPATIBILITY MATRIX

| Environment | Luxury Bridal | Editorial | Festive | E-Commerce | Documentary |
|-------------|--------------|-----------|---------|------------|-------------|
| **Grey Cyclorama** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ |
| **High-Key White** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| **Painted Canvas** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| **Minimal Wall** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Black Void** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ |
| **Haveli Interior** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| **Palace** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Temple Corridor** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Golden Hour Field** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Studio Water** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |
| **Natural Water** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |

---

## STUDIO LIGHTING SETUP LIBRARY

### SETUP-001: Classic Rembrandt / Split (Grey Cyclorama)
```yaml
key_light:
  type: "Beauty dish or medium softbox"
  position: "45° to subject, 45° above eye level"
  distance: "1.5–2m from subject"
  power: "Main exposure reference"
fill_light:
  type: "Large silver reflector"
  position: "Opposite side, same height"
  ratio: "3:1 key to fill"
background_light: "None — background falls to natural grey"
hair_light:
  type: "Small strip softbox or gridded spot"
  position: "Behind and above subject"
  purpose: "Separate subject from background"
result: "Classic luxury editorial — texture, shadow, separation"
```

### SETUP-002: High-Key White (Water/Silhouette)
```yaml
background_lights:
  type: "Two or more large softboxes aimed at white background"
  power: "2–4 stops ABOVE main subject exposure"
  position: "Both sides behind subject, aimed at background"
subject_light:
  type: "Large front softbox or octobox"
  position: "Directly front, large and close"
  power: "Lower — subject intentionally darker than background"
rim_light: "Optional strip softboxes from each side"
result: "High-key luminous void with subject detail preserved"
```

### SETUP-003: God-Ray / Cathedral (Dark Backdrop)
```yaml
key_light:
  type: "Fresnel spot or snoot — hard, narrow beam"
  position: "Directly above or 30° behind subject, aimed down through veil"
  power: "Strong — this is the main story light"
atmosphere:
  type: "Haze machine or fine mist"
  purpose: "Make the light beam itself visible in air"
  density: "Low — enough to see the beam, not enough to cloud the image"
fill_light:
  type: "Very low power — just enough to retain shadow detail"
background_light: "None — background must be dark"
result: "Theatrical dramatic with visible light beam through translucent fabric"
```

### SETUP-004: Profile Separation (Subject on Grey)
```yaml
key_light:
  type: "Large softbox or window light"
  position: "90° side — lighting face in profile"
  power: "Main exposure"
fill_light:
  type: "Low power reflector — opposite side"
  ratio: "4:1 — maintain the profile shadow"
rim_light:
  type: "Strip softbox behind subject"
  purpose: "CRITICAL — separate subject silhouette edge from grey background"
  power: "Match or slightly exceed key — creates hot rim edge"
background_light: "None — background inherits natural grey"
result: "Clean profile with defined silhouette edge, no background merge"
```

---

## PHASE 2 ADDITIONS (CAMPAIGN ASSET TESTING)

### ENV-011: Modern Minimalist Studio (The Editorial Edge)
- **BACKGROUND LAYER:** Textured concrete wall with architectural geometry, negative space.
- **FLOOR LAYER:** Smooth concrete or dark minimalist surface.
- **ATMOSPHERE LAYER:** Clear, high-contrast air, no haze.
- **Lighting Compatibility:** Cool diffused window light mixed with a sharp strobe (chiaroscuro).

### ENV-012: Nighttime Palace Balcony (The Festive Nocturne)
- **BACKGROUND LAYER:** Deep blue night sky, distant bokeh from festive lights.
- **FLOOR LAYER:** Ornate stone railing and carved stone floor.
- **ATMOSPHERE LAYER:** Soft glow from firelight, subtle smoke from diyas.
- **Lighting Compatibility:** Low light ambiance, warm flickering firelight casting dynamic shadows, subtle cool moonlight rim on hair.

### ENV-013: Lush Indian Royal Garden (The Verdant Daylight)
- **BACKGROUND LAYER:** Vibrant green foliage, bougainvillea vines, classic carved stone fountain (soft bokeh).
- **FLOOR LAYER:** Natural garden path, stone pavers.
- **ATMOSPHERE LAYER:** Clear daylight air.
- **Lighting Compatibility:** Bright, overcast daylight acting as a massive softbox, even natural illumination.

### ENV-014: Heritage Fort / Palace Corridor (The Architectural Antique)
- **BACKGROUND LAYER:** Intricately carved stone pillars, ancient Indian fort corridors, sandstone textures.
- **FLOOR LAYER:** Weathered stone slabs or marble.
- **ATMOSPHERE LAYER:** Soft, diffused natural light filtering through arches.
- **Lighting Compatibility:** Soft daylight, subtle rim light to separate subject from stone.

### ENV-015: High-Key Window Doorway (The Ethereal Threshold)
- **BACKGROUND LAYER:** Bright white paneled doors or windows with blown-out backlight.
- **FLOOR LAYER:** Reflective or bright domestic floor surface.
- **ATMOSPHERE LAYER:** Ethereal, glowing air from overexposed window light.
- **Lighting Compatibility:** Strong backlight / high-key window light, soft front fill.

---

*SDB-001 Version 1.1 — 15 environment types, 4 studio lighting setups.*
*Next: Forest / Nature, SETUP-005 (Loop Lighting)*
