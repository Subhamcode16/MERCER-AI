Viewed SKILL.md:1-164

Here are the primary expansion categories we could add to the **Interaction Ontology (`VIO-012`)** to push the Image Formation Intelligence even closer to a master cinematographer's level.

### 1. Garment × Environment (Contextual Physics)
- **Concept:** How the physical nature of the clothing interacts with the physical world.
- **Example:** `Flowing Chiffon Gown` × `Windy Beach` -> `PRODUCES` Maximum drape dynamism -> `REQUIRES` Fast shutter speed to freeze motion.
- **Example 2:** `Heavy Winter Coat` × `Tropical Set` -> `PRODUCES` Cognitive/Semantic Dissonance -> `AVOID`.

### 2. Vibe (Brand Identity) × Optics (Lens/Camera)
- **Concept:** Lenses carry emotional weight. We can map specific lens compressions and distortions to brand identities.
- **Example:** `Heritage Luxury` × `Camera Lens` -> `REQUIRES` 85mm-105mm (telephoto compression, subject isolation, flattering proportions).
- **Example 2:** `Gen-Z Streetwear` × `Camera Lens` -> `REQUIRES` 24mm-35mm (wide-angle, dynamic distortion, environmental context).

### 3. Subject (Morphology) × Garment (Silhouette)
- **Concept:** How the structure of a garment interacts with the physical structure of the model.
- **Example:** `Stiff Architectural Jacket` × `Dynamic Action Pose` -> `PRODUCES` Unnatural geometric breaking -> `REQUIRES` Static, statuesque posing.

### 4. Material × Camera (Shutter Angle / Motion Blur)
- **Concept:** Connecting the fabric's movement to the camera's shutter speed to capture the essence of the material.
- **Example:** `Liquid Satin` × `Motion` -> `PRODUCES` Smudged specular highlights if shutter is too fast -> `REQUIRES` Shutter drag (1/30s) to show light trails.

### 5. Skin Tone × Color Grade (Subsurface Scattering)
- **Concept:** Preventing color grading from destroying natural skin rendering.
- **Example:** `Deep Melanin Skin` × `Desaturated Teal/Orange Grade` -> `PRODUCES` Ashy/gray skin tones -> `REQUIRES` Preserving warm luminance in the mid-tones.

---

## 🛑 SOCRATIC GATE: Aligning on the Expansion

Before we start mapping these into the `interactions.json` file, I need to understand the strategic direction for this expansion.

### [P0] **ONTOLOGY SCOPE**
**Question:** Should we limit the Interaction Ontology strictly to **physical/optical truths** (e.g., Fabric × Light, Motion × Shutter), or do you want to include **cultural/brand semantics** (e.g., Luxury Vibe × Telephoto Lens)?
**Why This Matters:**
- Mixing physics and culture in the same solver makes the math exponentially harder. If we keep it physical, it's an absolute rule. If we add culture, it becomes subjective and probabilistic.
**Options:**
| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **A: Strictly Physics/Optics** | Bulletproof, unbreakable ground truth rules. | Limits creative auto-generation. | Ensuring the image never looks "fake". |
| **B: Physics + Brand Semantics** | Creates highly opinionated, ready-to-publish creative. | Requires massive subjective data curation. | Building an autonomous Creative Director. |

### [P1] **DATA ACQUISITION**
**Question:** For these new complex interactions, how should we populate the JSON?
**Why This Matters:**
- Writing `Fabric x Shutter Speed` interactions by hand will take months. 
**Options:**
| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **A: Manual Expert Curation (Level 2)** | 100% accurate, curated by us. | Extremely slow to scale. | High-stakes luxury benchmarks (like Banarasi). |
| **B: Algorithmic Mining (Level 3)** | Fast scaling across thousands of fabrics. | Might hallucinate weird combinations. | Expanding to E-commerce fast. |

### [P2] **NEXT IMMEDIATE FOCUS**
**Question:** Which of the 5 expansion categories listed above is the highest priority for our next test bench?
**Options:**
| Option | Focus |
|--------|-------|
| **A** | Garment × Environment |
| **B** | Vibe × Optics |
| **C** | Subject × Garment (Posing) |
| **D** | Material × Camera (Motion) |
| **E** | Skin Tone × Color Grade |

Let me know your thoughts on these options!