---
VIS-ID: EPL-001
Title: Expert Pattern Library
Version: 1.0.0
Status: Active
Owner: Visual Intelligence Research
Last Updated: 2026-07-20
Depends On:
  - VIO-004 (Creative Semantic Model)
  - VIO-008 (Commercial Semantics)
  - VIO-009 (Visual Craft)
  - VIO-010 (Material Intelligence)
  - VIO-011 (Cinematic Imperfections)
Purpose: >
  This is the primary runtime knowledge lookup table for the Reasoning Engine.
  When a material is identified and a campaign context is set, the engine
  queries this library and retrieves a complete, evidence-based Visual Direction.
  The engine does not guess. It retrieves.
---

# EXPERT PATTERN LIBRARY (EPL-001)
## The Runtime Knowledge Lookup Table

---

## How This Library Is Used

The Reasoning Engine calls this library with two keys:

```
query(material_class, campaign_semantic) → VisualDirection
```

Example:
```
query("banarasi_silk_zari", "luxury_bridal") → Pattern: LB-001
```

The returned `VisualDirection` object contains everything the Prompt Compiler
needs to generate a compliant image. Nothing is invented at runtime.

---

## PATTERN INDEX

| Pattern ID | Material Class | Campaign Semantic | Direction Name |
|-----------|----------------|-------------------|----------------|
| LB-001 | Banarasi Silk (Zari) | Luxury Bridal | The Royal Heritage Portrait |
| LB-002 | Kanjeevaram Silk | Luxury Bridal | South Indian Temple Grandeur |
| LB-003 | Georgette / Chiffon | Luxury Bridal | The Ethereal Romantic |
| LE-001 | Banarasi Silk (Zari) | Luxury Editorial | The Institutional Gold |
| LE-002 | Velvet | Luxury Editorial | The Chiaroscuro Drama |
| LE-003 | Chanderi | Luxury Editorial | The Minimal Heritage |
| LE-004 | Raw Silk / Tussar | Luxury Editorial | The Artisan Earth |
| FE-001 | Banarasi Silk | Festive / Occasion | The Diwali Warmth |
| FE-002 | Lehenga (Heavy) | Festive / Occasion | The Celebration Fullness |
| FE-003 | Cotton (Ikat/Block Print) | Festive / Occasion | The Joyful Regional |
| EC-001 | Banarasi Silk | E-Commerce / Catalog | The Clarity Portrait |
| EC-002 | Chiffon / Light Silk | E-Commerce / Catalog | The Clean Lookbook |
| SS-001 | Any Contemporary | Social Media (Instagram) | The Aspirational Moment |
| AD-001 | Any Heritage | Artisan / Documentary | The Craftsman Story |

---

## DETAILED PATTERN ENTRIES

---

### PATTERN: LB-001
**Name:** The Royal Heritage Portrait
**Keys:** `material=banarasi_silk_zari` + `campaign=luxury_bridal`

#### Creative Intent
To make the viewer feel they are witnessing a moment from a royal private
chamber — intimate, grand, and inevitable. The zari should feel like it is
alive under the light. The subject should feel like a woman stepping into
her own history.

#### Lighting Direction
```yaml
profile: Golden Hour Directional
key_light:
  source: "Large window or open courtyard — directional sun"
  angle: "45° to subject, camera-left"
  quality: "Warm, slightly hard-edged (not diffused)"
  color_temperature: "2700K–3200K (amber-gold)"
fill_light:
  source: "Large reflector or white wall bounce, camera-right"
  ratio: "3:1 (key significantly brighter)"
  quality: "Soft, wraps around"
rim_light:
  source: "Ambient skylight or practical background source"
  intensity: "Subtle — only visible on hair and shoulder"
material_response:
  banarasi_zari: "Gold threads will create individual point catchlights — this is the goal"
  silk_body: "Anisotropic sheen — will shift as subject moves"
forbidden:
  - "Flat front-facing studio light"
  - "Cool color temperature (above 5000K)"
  - "Flash or strobe as key light"
  - "Blue hour ambient as primary source"
```

#### Camera Direction
```yaml
lens: "85mm"
aperture: "f/2.0 – f/2.8"
depth_of_field: "Shallow — subject sharp, background creamy bokeh"
camera_angle: "Eye level (1.65m) or very slightly below — never above"
camera_height_rule: "Below the chin creates reverence; above the chin reads as diminishing"
frame_ratio: "4:5 (portrait) for Instagram; 2:3 for print"
framing: "Head to mid-thigh — show enough drape for pallu to read"
negative_space: "Intentional — subject occupies 55–65% of frame"
```

#### Subject & Styling Direction
```yaml
pose_name: "The Standing Heritage"
pose_description: >
  Subject stands with weight shifted to right hip. Left hand holds pallu
  lightly at mid-chest height — arm is not straight, elbow carries natural
  weight. Right arm falls naturally with slight outward rotation showing
  wrist. Three-quarter stance — body at 30–45° to camera, face turns
  toward camera. Chin is level or very slightly down.
expression: "Contemplative confidence — not smiling, not cold. Eyes carry knowing."
eye_direction: "Toward camera, or 10° off to camera-right"
jewelry_required:
  - "Kundan or Polki set — necklace mandatory"
  - "Heavy ear drops or jhumkas"
  - "At least one bangles stack or kada"
  - "Maang tikka if full bridal"
jewelry_forbidden:
  - "Minimalist gold chain only"
  - "Western jewelry (diamond solitaire studs)"
  - "No jewelry"
hair: "Bun or half-up — never loose flowing hair for this pattern (too casual)"
makeup: "Traditional bridal or editorial bridal — full, not minimal"
```

#### Environment Direction
```yaml
location_category: "Heritage Interior"
preferred_locations:
  - "Ancient haveli courtyard with carved stone columns"
  - "Palace room with high ceiling and ornate windows"
  - "Temple corridor (non-devotional — architectural use only)"
  - "Old mansion with wooden latticework (jali) casting shadow patterns"
background_quality: "Rich architectural character — columns, carved stone, ornate detail"
background_sharpness: "Soft bokeh — recognizable shapes but not competing for attention"
foreground_element: "Optional — partial stone column or fabric in extreme foreground adds depth"
forbidden_backgrounds:
  - "Plain white cyclorama"
  - "Modern glass building"
  - "Neutral grey studio background"
  - "Garden with green grass (too casual)"
```

#### Anti-AI Authenticity Profile
```yaml
profile_name: "Luxury Heritage Portrait"
subject_authenticity:
  skin_pores: 0.8
  peach_fuzz: 0.6
  subsurface_scattering: 0.9
  natural_asymmetry: 0.7
  eye_micro_expression: 0.9
hair_authenticity:
  flyaways: 0.5
  strand_definition: 0.7
  weight_physics: 0.9
fabric_authenticity:
  micro_wrinkles_at_stress_points: 0.8
  drape_weight_physics: 1.0
  zari_individual_catchlights: 1.0
optical_authenticity:
  lens_breathing_edges: 0.4
  highlight_rolloff: 0.8
  film_simulation: "Kodak Portra 400 — warm shadows, gentle grain"
  grain_level: 0.3
atmospheric_authenticity:
  dust_particles_in_backlight: 0.6
  depth_haze: 0.5
```

#### Complete Prompt Block (Compiler Output)
```
SUBJECT: Indian woman, late 20s, wearing a deep crimson Banarasi silk
brocade saree with heavy gold zari floral buti pattern, adorned with heavy
traditional Kundan jewelry including a prominent necklace, heavy ear drops
(jhumkas), maang tikka, and a stack of gold bangles, standing in
three-quarter stance with weight shifted to right hip, left hand holding
pallu lightly at mid-chest height, right arm falling naturally with slight
outward wrist rotation, face turned toward camera with contemplative
confidence, eyes carry knowing emotion — not smiling, chin level,

MATERIAL: Heavy structured Banarasi silk drape with defined crisp folds
(not flowing), individual gold zari threads creating distinct point
catchlights under warm directional light, anisotropic silk sheen shifting
across the body, visible micro-wrinkles at fabric stress points at hip and
arm, authentic garment weight evident in posture,

LIGHTING: Warm directional golden hour sun from camera-left at 45°, 2900K
color temperature, 3:1 lighting ratio with soft reflector fill from
camera-right, gold zari threads catching anisotropic point highlights,
subtle rim light on shoulder and hair from ambient skylight,

CAMERA: 85mm lens, f/2.2 aperture, eye-level camera at 1.65m, portrait
4:5 orientation, shallow depth of field with creamy background bokeh,
natural lens breathing at frame edges,

ENVIRONMENT: Interior of ancient haveli courtyard, weathered carved stone
columns partially in foreground, warm afternoon light filtering through
wooden jali screens casting shadow geometry on stone floor, atmospheric
dust particles visible in backlit air, rich architectural depth in
background — soft but legible,

QUALITY: Natural skin texture with visible pores, authentic subsurface
scattering in warm light, fine peach fuzz on skin, natural facial
asymmetry, individual hair strands distinct with natural flyaways at
crown, Kodak Portra 400 film response — warm shadows, gentle grain,
natural highlight rolloff,

FORBIDDEN: smooth plastic skin, uniform solid hair mass, symmetrical pose,
flowing Banarasi fabric, flat studio lighting, white background, cool
color temperature, digital sharpening artifacts, AI-smooth fabric surface,
perfectly symmetrical bilateral composition
```

---

### PATTERN: LB-002
**Name:** South Indian Temple Grandeur
**Keys:** `material=kanjeevaram_silk` + `campaign=luxury_bridal`

#### Creative Intent
Kanjeevaram represents permanence, weight, and divinity. The visual direction
must feel architectural — the saree should feel as solid and timeless as
temple stone. Colors are saturated, contrasting, regal.

#### Lighting Direction
```yaml
profile: "Warm Studio with Architectural Character"
key_light:
  source: "Large studio softbox or open shade — soft but directional"
  angle: "45° side — Rembrandt lighting position"
  color_temperature: "3500K–4000K (warm-neutral)"
  quality: "Slightly softer than LB-001 — silk is heavier, texture needs less drama"
fill_light:
  ratio: "2:1 — less dramatic than Banarasi, fabric speaks through color not zari"
material_response:
  kanjeevaram: "Mulberry silk will create a broad, rich sheen across the body"
  gold_zari_border: "Border should catch light — requires side angle"
  heavy_brocade: "Structural brocade needs light at 45° to reveal relief"
forbidden:
  - "Direct front light (destroys the dimensional brocade)"
  - "Very warm golden hour (oversaturates the silk colors)"
```

#### Camera Direction
```yaml
lens: "85mm or 50mm"
aperture: "f/2.8 – f/4"
rationale: "Slightly deeper DOF than LB-001 — the saree color and border are story, not background"
frame: "Full body or 3/4 body to show complete border of saree"
critical_note: "Kanjeevaram border is a signature design element — MUST be visible"
```

#### Subject & Styling Direction
```yaml
pose_name: "The Temple Stance"
pose_description: >
  Full or near-full body. Subject stands facing slightly toward camera
  with one foot slightly forward. Arms in a classical hand gesture
  (hasta mudra or natural position at sides). The goal is stillness and
  verticality — the saree's architecture demands a quiet pose.
jewelry_required:
  - "Temple jewelry — chunky gold collar necklace mandatory"
  - "Statement ear drops or long jhumkas"
  - "Gold bangles stacked on both wrists"
  - "Vanki (upper arm band) if available"
hair: "Bun with gajra (jasmine flowers) — the South Indian bridal signature"
makeup: "South Indian bridal — darker eye, defined lip, bindi mandatory"
```

#### Environment Direction
```yaml
preferred_locations:
  - "Stone temple corridor (architectural use — columns, carved walls)"
  - "Palace courtyard with granite or black stone floor"
  - "Minimal dark studio with single architectural prop (stone plinth)"
background_rule: "Cool, dark background creates contrast against the saturated Kanjeevaram"
```

#### Anti-AI Authenticity Profile
```yaml
profile_name: "Temple Heritage"
film_simulation: "Fujifilm Pro 400H — slightly cooler, richer shadows"
grain_level: 0.25
fabric_drape_weight: 1.0  # Kanjeevaram is very heavy — posture shows weight
```

---

### PATTERN: LB-003
**Name:** The Ethereal Romantic
**Keys:** `material=georgette_or_chiffon` + `campaign=luxury_bridal`

#### Creative Intent
Where LB-001 is history and LB-002 is architecture, LB-003 is a feeling.
Chiffon and georgette are translucent, fluid, moved by air. The visual
direction must capture impermanence — light through fabric, fabric through
light.

#### Lighting Direction
```yaml
profile: "Backlit Soft Ambient + Warm Practical Fill"
key_light:
  source: "Large window or outdoor open sky — BEHIND subject"
  quality: "Subject is slightly counter-lit — rim glow on body"
  color_temperature: "5000K–5500K (daylight, slightly cool)"
fill_light:
  source: "Warm reflector or interior warm practical light from front"
  ratio: "Very low fill — keep the atmospheric silhouette quality"
material_response:
  chiffon: "CRITICAL — backlight creates translucency glow through fabric"
  georgette: "Multiple small pleats catch light individually — creates shimmer"
  important: "Front key light kills the translucency. Backlight is mandatory."
```

#### Camera Direction
```yaml
lens: "85mm – 135mm"
aperture: "f/1.8 – f/2.0"
depth_of_field: "Razor thin — painterly, dreamy"
exposure: "Slightly lifted shadows — bright and airy overall key"
```

#### Subject & Styling Direction
```yaml
pose_name: "The Movement Pause"
pose_description: >
  Subject appears to have just paused mid-movement — one foot slightly
  forward or lifting, the fabric still moving around the body. One arm
  extended gently outward. The pallu or dupatta is caught in implied
  movement — billowing very slightly. This is not static. It is frozen
  grace.
expression: "Eyes downward or eyes closed — soft, romantic, private"
hair: "Loose or half-up — flowing hair reinforces the ethereal quality"
jewelry: "Light, delicate — pearl drops, antique gold minimalist, no heavy statement"
```

#### Anti-AI Authenticity Profile
```yaml
profile_name: "Ethereal Romance"
fabric_authenticity:
  translucency_rendering: 1.0  # MOST CRITICAL — chiffon must transmit backlight
  micro_pleats_individual: 0.9
  implied_movement: 0.8
optical_authenticity:
  lens_breathing: 0.6
  halation_on_highlights: 0.5  # Slight bloom around backlit edges — beautiful
  film_simulation: "Kodak Ektar 100 — slightly cooler, rich in pastels"
```

---

### PATTERN: LE-001
**Name:** The Institutional Gold
**Keys:** `material=banarasi_silk_zari` + `campaign=luxury_editorial`

#### Creative Intent
The difference between LB-001 (bridal) and LE-001 (editorial) is the
difference between a wedding and a museum. Editorial removes narrative and
amplifies art. The garment becomes the subject. The woman is the vessel.

#### Lighting Direction
```yaml
profile: "High Contrast Warm Studio"
key_light:
  source: "Fresnel or hard light source — beauty dish or direct strobe"
  angle: "45° above, side position"
  quality: "Harder than bridal — editorial wants edge and shadow"
  color_temperature: "3000K–3500K"
fill_light:
  ratio: "4:1 — deep, dramatic shadows"
  source: "Very minimal reflector — shadows must be present"
rim_light:
  source: "Hair/separation light from behind — gold tones on fabric edge"
editorial_principle: "The garment should feel like it is being documented for history"
```

#### Camera Direction
```yaml
lens: "85mm – 135mm"
aperture: "f/2.0"
frame: "Varies — from extreme close-up (fabric texture only) to full-body"
editorial_variety:
  frame_01: "Full body — architecture of the silhouette"
  frame_02: "Mid-body — the drape and pallu relationship"
  frame_03: "Close-up — individual zari buti on the fabric surface (macro)"
  frame_04: "Face + shoulder — expression and jewelry"
```

#### Subject & Styling Direction
```yaml
pose_name: "The Editorial Still"
pose_description: >
  Complete stillness. The editorial body does not perform — it inhabits.
  Pose may be unconventional — facing away from camera, profile only,
  extreme three-quarter, or even fully back-to-camera showing drape.
expression: "Neutral to severe — editorial does not smile. Eyes are statements."
hair: "Structured — bun, chignon, or wet-slicked back. Never soft."
makeup: "High contrast — strong eye, nude lip, or bold lip. No soft bridal makeup."
jewelry: "One statement piece maximum — editorial is about editing, not accumulation"
```

---

### PATTERN: LE-002
**Name:** The Chiaroscuro Drama
**Keys:** `material=velvet` + `campaign=luxury_editorial`

#### Creative Intent
Velvet and drama are the same sentence. The micro-pile of velvet creates
a luminosity gradient unlike any other fabric — lighter where compressed,
darker where the pile opens. The entire visual direction must exploit this.

#### Lighting Direction
```yaml
profile: "Single Source Chiaroscuro"
key_light:
  source: "Single hard light source — dramatic side position"
  angle: "90° to subject — extreme Rembrandt or split lighting"
  quality: "Hard — no diffusion"
  color_temperature: "3200K–3800K"
fill_light:
  ratio: "8:1 or more — half the body in shadow"
  source: "No fill recommended — pure shadow"
velvet_critical_rule: >
  The pile direction of the velvet must be oriented so that the lit side
  shows a lighter shade and the shadow side shows a dramatically darker shade.
  This is the velvet micro-contrast effect. If the pile is oriented wrong,
  the entire effect is lost. Prompt must specify: 'velvet pile direction
  creating luminosity gradient across the body.'
```

---

### PATTERN: LE-003
**Name:** The Minimal Heritage
**Keys:** `material=chanderi` + `campaign=luxury_editorial`

#### Creative Intent
Chanderi is translucent, light, delicate. The visual direction must be
restrained — the opposite of LB-001's richness. White space, negative
space, one figure, one light source, one idea.

#### Lighting Direction
```yaml
profile: "North Light / Overcast Window"
key_light:
  source: "Large north-facing window (indirect daylight)"
  quality: "Completely diffused — no directional shadows"
  color_temperature: "5500K–6000K (pure daylight)"
rationale: >
  Chanderi's translucency is best documented under flat, even light that
  reveals its true color and weave without shadow interference.
  Golden hour would oversaturate the delicate fabric.
```

#### Environment Direction
```yaml
preferred: "Minimal — white or light-toned architectural space"
background: "Near-white or natural linen — fabric color must read clearly"
negative_space: "70% — Chanderi editorial is about restraint"
```

---

### PATTERN: FE-001
**Name:** The Diwali Warmth
**Keys:** `material=banarasi_silk_zari` + `campaign=festive_occasion`

#### Creative Intent
Festive is not editorial. Festive is alive — there are other people nearby,
there is celebration, there is joy. The difference from LB-001 is emotion.
Bridal is solemn. Festive is luminous joy.

#### Lighting Direction
```yaml
profile: "Warm Evening Practical + Diyas / Candles"
key_light:
  source: "Practical warm lights — diyas, string lights, lanterns"
  color_temperature: "1800K–2500K (candlelight warm)"
  quality: "Flickering, multiple small sources"
fill_light:
  source: "Ambient bounce from warm walls"
rationale: "The entire scene should feel like it is lit by fire and festival"
```

#### Subject Direction
```yaml
expression: "Genuine warmth — slight smile is appropriate for festive"
pose: "More dynamic than editorial — reaching toward a diya, looking at another subject, turned in light movement"
jewelry: "Maximalist — this is festive, layering is appropriate"
```

---

### PATTERN: EC-001
**Name:** The Clarity Portrait
**Keys:** `material=banarasi_silk_zari` + `campaign=ecommerce_catalog`

#### Creative Intent
E-commerce has one job: show the product accurately. No mood. No narrative.
The customer must be able to judge the fabric, color, and workmanship from
the image. Nothing should obscure the product.

#### Lighting Direction
```yaml
profile: "Flat Studio Product Lighting"
key_light:
  source: "Large softbox directly front or slightly off-center"
  quality: "Very soft, even — minimal shadows"
  color_temperature: "5500K–6000K (daylight balanced)"
fill_light:
  ratio: "1:1 – nearly flat"
  source: "Second large softbox from opposite side"
ec_rule: "No artistic shadow. Product clarity is mandatory."
forbidden:
  - "Golden hour (color shifts fabric color inaccurately)"
  - "Dramatic shadows (hides fabric detail)"
  - "Bokeh background (distracts from product)"
```

#### Camera Direction
```yaml
lens: "50mm – 85mm"
aperture: "f/5.6 – f/8 — enough depth for entire garment to be sharp"
background: "Pure white or very light grey — no texture"
critical: "Entire garment from shoulder to hem must be sharp and visible"
```

#### Anti-AI Authenticity Profile
```yaml
profile_name: "Luxury E-Commerce"
skin_pores: 0.4        # Some texture but not editorial heavy
fabric_micro_wrinkles: 0.2   # Product must look aspirational, not worn
film_simulation: "None — clean digital render preferred"
grain_level: 0.0
note: "E-commerce authenticity comes from accurate color and material rendering, not photographic character"
```

---

### PATTERN: SS-001
**Name:** The Aspirational Moment
**Keys:** `material=any_contemporary` + `campaign=social_media_instagram`

#### Creative Intent
Instagram is a world of fractions of seconds. The image must communicate
in 0.3 seconds of scroll time. The hook is immediate — warmth, aspiration,
relatability. This is the least editorial of all patterns.

#### Lighting Direction
```yaml
profile: "Golden Hour Outdoor — Natural and Accessible"
key_light:
  source: "Direct golden hour sun or large outdoor reflector"
  quality: "Warm, flattering, universally appealing"
  color_temperature: "3000K–3800K"
rationale: "Golden hour is the universal social media language of aspiration"
```

#### Frame Direction
```yaml
ratio: "4:5 (Instagram portrait optimal)"
composition: "Subject prominent — 70% of frame"
background: "Clean, beautiful, recognizable — garden, street, café, nature"
note: "Unlike editorial (which avoids recognizable backgrounds), social needs relatable context"
```

#### Subject Direction
```yaml
expression: "Approachable warmth — genuine smile or warm neutral"
pose: "Relaxed, casual, caught-in-a-moment — not editorial stiff"
connection: "Subject makes viewer feel they could be there"
```

---

### PATTERN: AD-001
**Name:** The Craftsman Story
**Keys:** `material=any_heritage_handloom` + `campaign=artisan_documentary`

#### Creative Intent
This is not fashion photography. This is documentation of living heritage.
The artisan who made the saree, the hands that wove the zari, the loom that
carried centuries of knowledge. The visual language is documentary — real,
raw, truthful.

#### Lighting Direction
```yaml
profile: "Available Light Documentary"
source: "Only available light — no artificial lighting"
quality: "Whatever exists in the workshop or home — directional through a small window"
color_temperature: "Varies — accept the color of the environment"
principle: "Do not correct. Document."
```

#### Camera Direction
```yaml
lens: "35mm — wide enough to include environment"
aperture: "f/2.8 – f/4 — enough sharpness for context"
camera_style: "Handheld feel — slight imperfection in framing is appropriate"
```

#### Anti-AI Authenticity Profile
```yaml
profile_name: "Heritage Documentary"
film_simulation: "Kodak Tri-X or HP5 — black and white option valid"
grain_level: 0.8     # High grain is appropriate and authentic
skin_pores: 1.0      # Maximum — artisan hands and faces are real and aged
fabric_wrinkles: 1.0 # Working fabric has been handled — it shows
lens_flare: 0.6      # Documentary allows for optical imperfections
```

---

## RETRIEVAL INSTRUCTIONS FOR REASONING ENGINE

When querying this library at runtime:

```python
def retrieve_pattern(material_class: str, campaign_semantic: str) -> dict:
    """
    1. Exact match first: query(material_class, campaign_semantic)
    2. If no exact match: fuzzy match on material_class, then semantic
    3. If still no match: return the Universal Fallback pattern
    4. Merge retrieved pattern with Material DNA from VIO-010
    5. Apply Authenticity Profile from VIO-011
    6. Return complete VisualDirection object to Prompt Compiler
    """
```

### Conflict Resolution Priority
If retrieved pattern conflicts with user-specified preference:
1. **Material Physics Laws (VIO-010, Level 1)** — NEVER override. These are absolute.
2. **Expert Heuristics (VIO-010, Level 2)** — Override only with explicit user instruction.
3. **Statistical Patterns (VIO-010, Level 3)** — User preference always wins.

### Confidence Score Assignment
Each retrieved direction is assigned a confidence score based on match quality:
- **Exact material + exact campaign:** 0.95–1.0
- **Exact material + adjacent campaign:** 0.75–0.85
- **Adjacent material + exact campaign:** 0.65–0.80
- **Fuzzy match on both:** 0.50–0.65 (triggers clarification request)

---

*Library Version 1.0 — Covers 14 core patterns across 6 campaign categories.*
*Next expansion: EC-002, SS-002, LB-004 (Lehenga Bridal), Regional variants.*
