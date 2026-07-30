---
VIS-ID: PDB-001
Title: Pose & Motion Database
Version: 1.0.0
Status: Active
Owner: Visual Intelligence Research
Last Updated: 2026-07-20
Depends On:
  - VIO-006 (Domain Fashion Ontology)
  - FDB-001 (Fabric Physics Database)
  - SDB-001 (Studio & Environment Database)
  - EPL-001 (Expert Pattern Library)
Purpose: >
  The authoritative database of subject poses, body orientations, fabric-in-motion
  physics, silhouette architecture, and veil/dupatta as compositional tools.
  The Reasoning Engine queries this database to select a pose that is coherent
  with the garment's physical properties, the campaign's emotional register,
  and the chosen environment. A pose that violates fabric physics will produce
  an AI image that looks physically wrong — this database prevents that.
---

# POSE & MOTION DATABASE (PDB-001)

---

## POSE ARCHITECTURE FRAMEWORK

Every pose is defined across five independent axes. The Prompt Compiler
assembles a pose by specifying each axis independently.

```
AXIS 1: BODY ORIENTATION  → Facing camera, profile, back, overhead
AXIS 2: WEIGHT STANCE     → Which leg bears weight and how that reads
AXIS 3: ARM LANGUAGE      → What arms do and what emotion they communicate
AXIS 4: HEAD POSITION     → Chin angle, face direction, eye direction
AXIS 5: FABRIC RESPONSE   → How garment physically responds to this pose
```

All five axes must be specified. Most AI prompts only describe body orientation.
Atelier specifies all five — this is why Atelier-generated figures feel physically
real and not like mannequins in stated positions.

---
---

## BODY ORIENTATION LIBRARY

---

### ORIENTATION-001: Three-Quarter Front (The Heritage Standard)

**Body Angle:** 30–45° from camera axis, face turns toward camera

#### Axis Breakdown
```yaml
body_orientation: "Body angled 30–45° away from camera — right or left shoulder closer"
weight_stance:
  primary: "Weight on back leg (further from camera)"
  effect: "Hip on weight-bearing side drops slightly — creates natural asymmetry"
  visible: "This hip drop is visible in silhouette — destroys mannequin stiffness"
arm_language:
  primary_arm: "Closer-to-camera arm — relaxed, slightly forward, natural hang"
  secondary_arm: "Further arm — may hold pallu, rest against body, or extend outward"
  rule: "Arms must NOT be perfectly parallel to body or to each other"
head_position:
  face_direction: "Turns back toward camera — 3/4 facial view"
  chin: "Level or slightly lowered — never raised (raising reads as defiant, not elegant)"
  eye_direction: "Toward camera or 10° off camera"
fabric_response:
  saree_banarasi: "Heavy pallu falls diagonally across body — diagonal line reinforces 3/4 angle"
  saree_chiffon: "Light pallu may drift slightly off back shoulder — implies air"
  lehenga: "A-line skirt fans slightly forward-back — asymmetric hem distribution"
```

#### Prompt Language Template
```
"Indian woman standing in three-quarter stance, body angled 45° from camera
with right shoulder closer, weight shifted to back left leg creating natural
hip asymmetry, face turned toward camera showing three-quarter view, chin
level, left arm relaxed at side with slight natural bend at elbow,
right hand lightly holding pallu at mid-chest height"
```

#### Forbidden Combinations
```yaml
forbidden:
  - "Three-quarter body + full frontal face (anatomically inconsistent)"
  - "Three-quarter with both arms perfectly symmetrical"
  - "Three-quarter with weight equally on both feet (static, lifeless)"
```

---

### ORIENTATION-002: Profile (The Sculptural Side)

**Body Angle:** 90° from camera — subject faces completely to the side

**As seen in:** Image 1 (billowing veil profile)

#### Axis Breakdown
```yaml
body_orientation: "Subject faces completely sideways — 90° from camera axis"
weight_stance:
  primary: "Weight on closer leg (toward camera)"
  effect: "Slight forward lean or upright — profile reads as a clean geometric shape"
  rule: "Profile stance must be clean — no arms crossing the body silhouette line"
arm_language:
  front_arm: "Falls naturally forward — visible in front of body silhouette"
  back_arm: "Falls naturally behind — visible behind body silhouette"
  rule: "Neither arm should cross the body's profile line — destroys clean silhouette"
  elevated_option: "One arm may be raised — creates dramatic geometry"
head_position:
  face_direction: "Facing the same direction as body — pure profile"
  chin: "Level or very slightly raised — profile benefits from neck length"
  eye_direction: "Looking in the direction of body facing, or eyes closed"
  eyes_closed_profile: "Extremely powerful — introspective, peaceful, iconic"
fabric_response:
  saree: "Pallu falls forward in front of body OR extends dramatically behind — never neutral"
  gown: "Train extends behind creating an asymmetric ground shadow"
  tulle_veil: "If thrown — extends dramatically behind and above in the direction opposite to facing"
fabric_law: "The profile shot is defined by what happens AROUND the silhouette — not the face"
```

#### The Profile-Specific White-on-White Rule
```yaml
challenge: "Profile of white garment against grey background — values may be too similar"
solution: "MANDATORY rim light on the back edge of the silhouette — creates a bright defining line"
prompt_law: >
  "strong rim/separation light on back edge of figure — creates a bright
  defining line separating white dress from grey background, essential for
  profile silhouette legibility"
```

#### Prompt Language Template
```
"subject facing in pure profile — completely sideways to camera, full
90° profile orientation, weight on closer leg, both arms relaxed and
parallel to body silhouette (not crossing the profile line), eyes closed
with internal peaceful expression, chin level showing clean neck line,
strong rim light on back body edge creating silhouette separation"
```

---

### ORIENTATION-003: Back / Rear View (The Mystery Reveal)

**Body Angle:** Subject faces away from camera — back visible

**As seen in:** Image 2 (water reflection) and Image 3 (cathedral veil)

#### Axis Breakdown
```yaml
body_orientation: "Subject faces completely away — camera sees back of head and body"
weight_stance:
  options:
    neutral_back: "Weight equal — formal, architectural stance"
    three_quarter_back: "Body angled 30° — over-shoulder look possible"
    turned_back: "Body facing away, head turns to look over shoulder — the power look"
arm_language:
  neutral: "Both arms at sides or one at side, one bent at waist — natural rear view"
  raised: "One or both arms raised — creates dramatic geometry against background"
  raised_rule: "Raised arms reveal back of garment construction — ensure back is styled"
  hand_placement_rule: "Hands must be purposeful — not dangling awkwardly"
head_position:
  full_back: "Head facing away — only back of hair/head visible — maximally mysterious"
  over_shoulder: "Head turns to camera — reveals profile or face — more personal"
  chin_angle: "If turning: chin slightly toward lower shoulder — elongates the neck"
fabric_response:
  gown_train: "Train extends behind toward camera — fills lower frame — POWERFUL"
  lehenga: "Gathered skirt spreads around the feet — symmetrical cone viewed from behind"
  saree_pallu: "Pallu falls down the back — architectural cascade from shoulder to floor"
  veil_dupatta: "Draped behind — entire length visible — MUST be the compositional focus"
```

#### The Over-Shoulder Look Specifics
```yaml
pose_name: "The Glance Back"
body: "Fully facing away from camera"
head: "Turned over shoulder — 120–140° rotation from forward position"
expression: "Can be: knowing, questioning, inviting, or cool"
anatomy_rule: "Maximum natural head rotation over shoulder is ~140° — beyond that is forced"
prompt_law: "head turned over left shoulder, 130° rotation — chin toward lower shoulder"
power_of_this_pose: >
  Shows the BACK of the garment (often the most dramatic part — zippers, backs,
  trains, pallu cascade) AND reveals the face — the best of both.
```

#### Arm-Raised Variant (Image 3 Reference)
```yaml
pose_name: "The Cathedral Raise"
description: "Subject facing mostly away, one arm raised straight overhead"
purpose: "Creates extreme vertical composition — extends image height dramatically"
arm_mechanics:
  raised_arm: "Straight vertical — elbow not bent — reaches directly up"
  other_arm: "Holds or touches something (rose, fabric, at waist) — creates counterbalance"
fabric_effect: "Raised arm pulls veil/dupatta into overhead triangle shape — architectural"
anatomy_note: "When arm is raised fully overhead, shoulder rises — visible from back"
prompt_language: >
  "subject facing mostly away from camera, right arm raised straight overhead
  holding cathedral veil apex, arm fully extended — shoulder raised visibly,
  left arm at waist holding a single long-stem rose, veil forms enormous
  triangle from raised hand cascading to floor on both sides"
```

---

### ORIENTATION-004: Overhead / Aerial View

**Body Angle:** Camera positioned directly above — subject seen from top-down

```yaml
use_case: "Garment laid flat, detail shots, abstract fashion"
subject_position: "Lying on floor or surface — face may be visible or obscured"
fabric_response: "Garment spreads around body without gravity distortion — shows full layout"
prompt_language: >
  "aerial overhead view, subject lying on white marble floor, garment spread
  around body showing full textile layout, camera directly above at 90°"
```

---
---

## FABRIC-IN-MOTION PHYSICS LIBRARY

This is the most critical missing section from all existing fashion AI knowledge.
The images you shared are defined by fabric in motion. Motion physics must be
specified precisely — otherwise AI renders motion arbitrarily.

---

### MOTION-001: Tulle / Veil Throw (Billowing Arc)

**As seen in:** Image 1 (the defining element of that entire photograph)

#### What Actually Happens Physically
```yaml
physics: >
  A tulle veil or dupatta thrown into the air follows a parabolic arc.
  The fabric leaves the subject's hands from a low position, travels upward
  and outward, and at the peak of the throw hangs momentarily in an
  expanded shape before falling. The photograph captures the PEAK of the
  throw — maximum expansion, maximum volume.

fabric_behavior_at_peak:
  shape: "Convex upward arc — fabric bends against gravity at peak"
  density: "Fabric has maximum internal space at peak — thin, airy, luminous"
  edge: "Fabric edges are sharp and defined — not limp or drooping"
  translucency: "At peak expansion, tulle is at maximum translucency — nearly air"
  backlight_effect: "If backlit: fabric glows white against darker surroundings"

direction_rule: >
  The throw direction determines where the fabric goes.
  If subject faces left, fabric is thrown to the right and above.
  The fabric arc extends behind and above the subject's back.
  Fabric should NOT cross the subject's face.

gravity_rule: >
  Fabric at peak of throw still responds to gravity at the edges —
  the EDGES begin to droop down while the CENTER is still rising.
  This creates the characteristic wave shape — not a flat sheet.
```

#### Prompt Language — The Throw Peak
```
"white tulle veil captured at peak of throw — fabric billowing in a large
convex arc above and behind the subject, maximum volumetric expansion, fabric
edges beginning to curve downward while center still extends horizontally,
semi-translucent tulle with inner light quality, fabric has visible physical
presence — weight implied despite airborne state, frozen moment of maximum expansion"
```

#### What AI Gets Wrong Without This Knowledge
```yaml
common_failures:
  - "Fabric rendered as flat sheet (no volume, no physics)"
  - "Fabric drooping symmetrically on both sides (wrong arc shape)"
  - "Fabric crossing subject's face (direction error)"
  - "Fabric appearing weightless with no gravity response at edges"
  - "Multiple layers of fabric rendered as a single mass"
forbidden_prompts:
  - "floating fabric" (too generic — no direction or physics)
  - "billowing fabric" alone (no shape specification)
  - "fabric in the air" (no physics, no moment, no direction)
```

---

### MOTION-002: Walking / Stride Motion

#### Physics
```yaml
gait_physics: >
  A walking stride creates multiple simultaneous fabric responses:
  1. The swing leg's hip creates fabric pull in the direction of stride
  2. The supporting leg's fabric column remains relatively still
  3. The pallu/train drags behind with a slight lag
  4. Arms swing slightly — causing fabric at sleeves/blouse to shift

captured_moment: "Mid-stride — front foot forward, back foot pushing off"
fabric_at_this_moment:
  saree: "Pallu begins to swing forward with front-arm momentum"
  lehenga: "Skirt hem leads the stride — curves forward on the stride side"
  train: "Follows behind with full-length lag — still sweeping through last position"
```

#### Prompt Language
```
"subject captured mid-stride, front left leg extended forward, right leg pushing
off behind, fabric responding to directional movement — pallu swinging forward
with natural momentum, train sweeping through the trailing arc of the previous
step position, implied purposeful forward movement, not stiff or posed"
```

---

### MOTION-003: Spinning / Turning (Lehenga Rotation)

#### Physics
```yaml
centrifugal_physics: >
  When a subject spins, gathered skirts (lehenga, full gown) respond to
  centrifugal force — the hem rises and expands outward perpendicular to
  the axis of rotation.

captured_moment_options:
  early_spin: "Skirt just beginning to lift — modest expansion"
  mid_spin: "Skirt at 45–60° from vertical — dramatic flair"
  peak_spin: "Skirt nearly horizontal — maximum drama (requires very fast spin)"

fabric_shape_at_mid_spin: "Cone expanding from waist — smooth curve from waist to expanded hem"
body_position: "Upper body remains relatively vertical — arms may extend for balance"
hair_behavior: "Hair follows rotation — extends outward from head in direction of spin"
face: "Either blurred (motion) or sharp (strobe-frozen) — specify which"
```

#### Prompt Language
```
"subject spinning — lehenga skirt caught mid-rotation expanding into a dramatic
cone shape, hem rising to 50° from vertical, fabric fanning smoothly from fitted
waist to expanded circular hem, upper body slightly tilted in rotation axis,
hair extending outward from centrifugal force, motion-frozen by fast shutter"
```

---

### MOTION-004: Wind Effect / Fan-Driven Motion

#### Physics
```yaml
wind_source: "Studio fan (industrial, directional) — consistent controlled wind"
fabric_response_by_type:
  chiffon_georgette: "Immediate full response — billows dramatically from lightest wind"
  chanderi: "Strong response — translucency becomes visible as fabric lifts"
  organza: "Structured response — maintains some shape while billowing"
  banarasi_silk: "MINIMAL response — heavy structured fabric barely responds to fan wind"
  velvet: "NO visible response — too heavy"
  net_tulle: "Maximum response — each layer separates and billows independently"

direction_law: "Wind must come from ONE consistent direction — fabric moves uniformly"
hair_interaction: "Hair responds to wind before fabric — leads the direction tell"
```

#### Prompt Language
```
"strong directional studio fan wind from camera-right — lightweight chiffon
dupatta billowing dramatically to camera-left, fabric fully extended in the
wind direction, hair also swept left following wind, subject's weight plants
against the wind — slight lean into the source direction"
```

---

### MOTION-005: Seated / Low Position

#### Physics
```yaml
seated_positions:
  floor_seat:
    description: "Subject seated directly on floor — legs to one side or folded"
    fabric_response: "Saree/lehenga fabric pools and spreads around the subject"
    power: "Creates extreme intimacy — subject and fabric become one ground-level composition"
    
  low_platform:
    description: "Seated on a low plinth, step, or cushion 15–30cm high"
    fabric_response: "Fabric cascades over edge — 'spill' effect"
    
  reclining:
    description: "Subject partially reclining — upper body raised, lower extended"
    fabric_response: "Fabric follows body angle — spectacular for saree drape photography"
```

#### Prompt Language
```
"subject seated on ancient marble floor, legs folded to the right side, heavy
Banarasi silk saree pooling and spreading around her on the floor in architectural
folds, fabric cascading outward from seated position, upper body upright and
elegant, hands resting on lap"
```

---
---

## SILHOUETTE ARCHITECTURE LIBRARY

The silhouette is the first thing visible in any fashion photograph. Before
color, texture, or lighting — the silhouette shape communicates the garment's
architectural identity. Atelier must specify this precisely.

---

### SIL-001: The Saree Column

```yaml
description: "The classic standing saree silhouette — vertical column with diagonal pallu line"
shape_geometry: "Narrow vertical — waist to floor, width barely changes from shoulder to hem"
defining_element: "Diagonal pallu line from left shoulder to right hip — the signature"
hem_behavior: "Hem at floor level — a few centimeters of fabric touches floor"
footwear_visibility: "Toes of footwear may be visible below hem (adds human grounding)"
train_option: "Pallu may extend to floor creating a short train behind"
prompt_language: >
  "full-length saree silhouette — vertical column from shoulder to floor, pallu
  falling diagonally from left shoulder across body, hem brushing floor, natural
  vertical proportion"
```

---

### SIL-002: The Lehenga Cone (A-Line)

```yaml
description: "The traditional Lehenga — fitted waist expanding dramatically to floor"
shape_geometry: "Inverted cone — small at waist, maximum width at hem"
hem_diameter: "Varies: modest (80cm) to bridal extreme (3+ meters circumference)"
waist_fit: "Extremely fitted — no ease at waist"
visual_effect: "The waist appears smaller because of the dramatic hem expansion"
prompt_language: >
  "heavy Lehenga with dramatic A-line silhouette — extremely fitted at waist
  expanding to full circular hem at floor, maximum hem circumference,
  waist-to-hem ratio creating strong cone geometry, hem touching floor all around"
```

---

### SIL-003: The Mermaid / Trumpet

```yaml
description: "Fitted through body, flaring only at or below knee"
shape_geometry: "Column from shoulder to knee, dramatic outward flare from knee to floor"
visual_effect: "Emphasizes the body through hips and thighs — curves are visible"
flare_point: "Precisely at knee — above = trumpet, below = mermaid"
movement: "Restricts stride — walking stride is shorter, more deliberate"
prompt_language: >
  "mermaid silhouette — fitted column through body and hips, dramatic outward
  flare beginning at knee, hem spreading to floor in architectural curve,
  body contours clearly defined through fitted bodice and hip section"
```

---

### SIL-004: The Ball Gown Volume

```yaml
description: "Maximum fullness — volume from waist in all directions"
construction: "Requires crinoline/petticoat structure underneath to maintain shape"
shape_geometry: "Dome or sphere below waist"
scale: "Hem circumference: 4–8+ meters — fills significant floor space"
photographing_rule: >
  To show the true scale of a ball gown, the camera MUST be positioned
  to include significant floor space. The hem-to-floor relationship defines
  the silhouette. Cutting off the hem destroys the entire visual identity.
prompt_language: >
  "full ball gown volume — massive dome silhouette from fitted waist, hem
  extending 3 meters in all directions on the floor, crinolined structure
  maintaining perfect dome shape, full floor visible showing scale of hem"
```

---

### SIL-005: The Cathedral Train

```yaml
description: "Extended fabric train trailing behind the subject"
train_length_classifications:
  sweep: "30–45cm trailing behind (subtle)"
  chapel: "1.2m trailing"
  cathedral: "2.1–4m trailing (the most dramatic)"
  royal: "4m+ (ceremonial only)"
photographing_rule: >
  Train must be laid out deliberately before shooting — it does not naturally
  arrange itself. The straight line of the train from body to tip requires
  studio floor space equal to the train length plus camera distance.
prompt_language: >
  "cathedral-length dress train extending 2.5 meters behind subject, fabric
  perfectly laid out in a straight line from the back of the dress to the
  pointed tip, train fabric billowing slightly at sides, full length visible
  from subject to train tip"
```

---
---

## VEIL & DUPATTA AS COMPOSITIONAL TOOL

Veils and dupattas are not accessories — they are compositional elements
that can define the entire visual architecture of a photograph.

---

### VEIL-001: The Cathedral Arch (Raised Overhead)

**As seen in:** Image 3

```yaml
description: "Veil raised above subject's head, held at tip, cascading to floor both sides"
geometry: "Triangle — apex at raised hand, two sides cascading to floor"
required:
  - "Subject facing mostly away from camera (back view)"
  - "One arm raised fully overhead holding veil tip"
  - "Veil of cathedral length (2m+)"
  - "Floor space for veil to cascade on both sides"

fabric_behavior:
  apex: "Held taut at hand — single point of tension"
  cascade: "Falls in natural curtain folds from hand to floor on both sides"
  floor_pool: "Excess fabric pools at floor on both sides of subject"
  translucency: "If backlit — entire triangle glows from interior light"

prompt_language: >
  "cathedral veil raised to apex by right arm extended fully overhead,
  veil forming an enormous triangle from raised hand — two sides cascading
  to floor in natural curtain folds, fabric pooling at floor on both sides
  of the subject, veil translucent and catching light from behind,
  dramatic vertical composition with subject at triangle's geometric center"
```

---

### VEIL-002: The Thrown Arc

**As seen in:** Image 1

```yaml
description: "Veil thrown into the air — captured at peak arc"
geometry: "Convex upward arc — maximum expansion horizontally"
direction: "Always extends behind and above the subject, NEVER across the face"
prompt_language: >
  "floor-length tulle veil thrown into the air and captured at peak expansion —
  billowing in a large convex arc above and behind the subject's right side,
  fabric at maximum airy volume, edges curving downward while center extends
  outward, semi-translucent white tulle glowing against darker background"
```

---

### VEIL-003: The Dupatta Drape (Saree / Lehenga)

```yaml
styles:
  over_head: "Dupatta draped over top of head and over shoulders — traditional"
  one_shoulder: "One end over left shoulder, other end over right arm"
  trailing: "Dupatta trails behind like a short veil"
  held_out: "Both ends held out sideways — creates wing-like composition"

fabric_response_by_material:
  chiffon_dupatta: "Falls in multiple soft vertical folds — maximum drape"
  net_dupatta: "Holds some volume — semi-structured fall"
  silk_dupatta: "Heavier — falls in defined, wider folds"
  
over_head_specifics: "Dupatta edge frames face — creates an oval vignette around face"
prompt_language: >
  "sheer chiffon dupatta draped over head and cascading over both shoulders,
  fabric forming a soft oval frame around the face, excess length falling
  in multiple fine vertical folds on both sides of the body"
```

---

### DUPATTA-004: The Wind-Extended Dupatta

```yaml
description: "Dupatta extended horizontally by wind — horizontal compositional element"
geometry: "Horizontal plane — extends perpendicular to body axis"
direction: "One end attached to subject, other end extends to camera direction or behind"
prompt_language: >
  "dupatta caught by strong directional wind — one end at subject's shoulder,
  fabric extending fully horizontally to the left, completely extended
  parallel to ground at shoulder height, fabric taut and fully unfurled,
  fine chiffon showing translucency against the bright background behind"
```

---
---

## POSE × FABRIC COMPATIBILITY MATRIX

The most important table in this document. Every pose has fabric constraints.

| Pose | Banarasi | Chiffon/Georgette | Lehenga | Velvet | Tulle Veil |
|------|----------|-------------------|---------|--------|-----------|
| **3/4 Front** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Profile** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Back / Rear** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Stride / Walk** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Veil Throw** | ✗ Forbidden | ⭐⭐⭐⭐⭐ | ⭐⭐ | ✗ Forbidden | ⭐⭐⭐⭐⭐ |
| **Spin** | ✗ Forbidden | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✗ Forbidden | ⭐⭐⭐ |
| **Seated Floor** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Cathedral Raise** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Fan Wind** | ✗ Forbidden | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✗ Forbidden | ⭐⭐⭐⭐⭐ |

**Forbidden Combinations (Critical Rules):**
- `Banarasi Silk + Veil Throw` → Heavy silk does NOT throw — it drops. Forbidden.
- `Banarasi Silk + Spin` → Heavy silk does NOT centrifuge. Forbidden.
- `Velvet + Fan Wind` → Velvet pile does not respond visibly to fan. Forbidden.
- `Velvet + Spin` → Velvet weight + spin = collapsed pile direction. Forbidden.

---

## ANATOMICAL REALISM RULES

Rules that prevent AI from generating physically impossible poses.

```yaml
RULE-001: "Maximum over-shoulder head turn is 140° — beyond is anatomically impossible"
RULE-002: "Raised arm above shoulder raises the corresponding shoulder visibly — specify this"
RULE-003: "When weight is on one leg, the opposite hip drops — hip drop must be present"
RULE-004: "Hands hanging at sides ALWAYS have slight bend at fingers — never fully straight"
RULE-005: "Natural standing posture has slight forward lean — never perfectly vertical military"
RULE-006: "Profile view: ear is the outermost point of the head — nose does not protrude beyond"
RULE-007: "Seated on floor: spine curves slightly — never perfectly vertical while seated on floor"
RULE-008: "Walking subjects have at least 30° knee bend on the pushing leg"
RULE-009: "Spinning: centrifugal force tilts upper body away from spin axis — slight lean"
RULE-010: "Arms raised overhead: rib cage elevates — waist appears longer visibly"
```

---

## EXPRESSION LIBRARY

```yaml
EXPRESSION-001_EDITORIAL_NEUTRAL:
  description: "Relaxed jaw, softly parted lips, eyes open and direct — the editorial default"
  eye_quality: "Alert, present, slightly challenging"
  jaw: "Relaxed — no tension"
  prompt: "editorial neutral expression, relaxed jaw, eyes open and direct, softly parted lips"

EXPRESSION-002_EYES_CLOSED:
  description: "Lashes resting on cheek, complete internal peace"
  lash_requirement: "Long lashes create shadow on upper cheek — requires them to be present"
  prompt: "eyes softly closed, long lashes creating shadow on upper cheek, complete peaceful expression"

EXPRESSION-003_OVER_SHOULDER:
  description: "Face turning over shoulder — knowing, inviting, confident"
  jaw_position: "Chin toward lower shoulder — elongates the neck"
  expression: "Knowing awareness — not a full smile, not cold"
  prompt: "face turned over right shoulder, chin slightly toward lower shoulder elongating neck, knowing expression"

EXPRESSION-004_DOWNWARD_GAZE:
  description: "Eyes looking down at about 30–45° below horizontal"
  quality: "Introspective, modest, contemplative"
  prompt: "gaze directed downward at 30°, introspective expression, eyelids slightly lowered"

EXPRESSION-005_PROFILE_CLOSED:
  description: "Profile + eyes closed — the most powerful combination for abstract editorial"
  quality: "Transcendent — the face is a sculptural form, not a personality"
  prompt: "perfect profile, eyes closed, face as pure form — sculptural quality"
```

---

## PHASE 2 ADDITIONS (CAMPAIGN ASSET TESTING)

### ORIENTATION-005: The Editorial Seated (Power & Contemplation)
- **BODY ORIENTATION:** Seated on a contemporary chair, face toward camera.
- **WEIGHT STANCE:** Weight grounded on the seat, leaning forward slightly.
- **ARM LANGUAGE:** One hand resting gracefully on the chin with elbow on knee.
- **HEAD POSITION:** Chin slightly down, intense editorial gaze directly into the lens.
- **FABRIC RESPONSE:** Saree draped across lap with defined folds, rigid tension at the elbow and knee joints.

### ORIENTATION-006: The Balcony Observer (Three-Quarter Profile)
- **BODY ORIENTATION:** Standing by a railing, three-quarter profile away from camera.
- **WEIGHT STANCE:** Weight resting on one leg, leaning gently against the railing.
- **ARM LANGUAGE:** One hand gently resting on the railing, the other lightly touching the collarbone.
- **HEAD POSITION:** Looking thoughtfully into the distance (not at the camera).
- **FABRIC RESPONSE:** Saree falling naturally with gravity, subtle tension where the arm meets the collarbone.

### MOTION-006: The Regal Stride (Mid-Stride Action)
- **BODY ORIENTATION:** Walking slowly towards the camera, mid-stride.
- **WEIGHT STANCE:** Dynamic weight shift, one foot planted, the other lifting.
- **ARM LANGUAGE:** One hand holding the pallu securely to prevent excessive flow.
- **HEAD POSITION:** Regal serious expression, looking straight ahead into the lens.
- **FABRIC RESPONSE:** Fabric catching a slight breeze but maintaining structural integrity, micro-wrinkles at hip and arm showing garment weight and motion.

### MOTION-007: Dynamic Fabric Spin (The Whirlwind)
- **BODY ORIENTATION:** Mid-spin, looking back over the shoulder.
- **WEIGHT STANCE:** Centrifugal lean, weight transitioning between feet.
- **ARM LANGUAGE:** Arms slightly extended to balance and guide the fabric.
- **HEAD POSITION:** Looking back over the shoulder towards the camera.
- **FABRIC RESPONSE:** Dramatic flare of the skirt/lehenga due to centrifugal force.

### VEIL-005: Contemplative Veil Drape (The Ethereal Stillness)
- **BODY ORIENTATION:** Standing still, facing camera or slight 3/4 turn.
- **WEIGHT STANCE:** Evenly distributed, grounded.
- **ARM LANGUAGE:** Hands holding or framed by the sheer dupatta/veil.
- **HEAD POSITION:** Gazing downward contemplatively, eyelids lowered.
- **FABRIC RESPONSE:** Sheer fabric falling straight down or wrapped softly around the head/shoulders.

### EXPRESSION-006: Editorial Close-Up Gaze (The Intensity)
- **BODY ORIENTATION:** Close-up framing, tight on the face and neck.
- **WEIGHT STANCE:** N/A (Close-up).
- **ARM LANGUAGE:** N/A or fingers slightly touching jewelry.
- **HEAD POSITION:** Direct, unflinching stare into the lens.
- **FABRIC RESPONSE:** Focus on heavy jewelry (Nath, choker) and rich brocade textures near the face.

### MOTION-008: Wind-Blown Toss (The Breezy Editorial)
- **BODY ORIENTATION:** Standing, dynamic and free.
- **WEIGHT STANCE:** Weight on one leg, body twisting slightly to follow the fabric.
- **ARM LANGUAGE:** One or both arms raised or extended, actively tossing the pallu into the air.
- **HEAD POSITION:** Looking up or away, enjoying the movement.
- **FABRIC RESPONSE:** CRITICAL RULE: Requires lightweight fabrics (Chiffon/Organza). Fabric billows and flies dramatically in the wind. (Forbidden for heavy silks like Banarasi/Kanjeevaram).

---

*PDB-001 Version 1.2 — Added Wind-Blown Toss motion.*
*Next: Dynamic motion (jumping), partner poses (two-figure compositions)*
