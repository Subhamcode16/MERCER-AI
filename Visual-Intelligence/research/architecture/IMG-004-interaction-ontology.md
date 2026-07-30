# IMG-004: Interaction Ontology

## 1. Core Purpose
The Interaction Ontology is the synthesis layer. It defines how independent variables (from the Physics and Visual Craft ontologies) behave when they collide. 

While IMG-002 defines what a material *is*, and IMG-003 defines what a lens *does*, IMG-004 defines what happens when that specific material is shot with that specific lens under a specific Vibe.

## 2. Key Interaction Vectors
The ontology maps several critical collisions:

### Material × Lighting
How specific physical properties react to specific lighting archetypes.
*Example:* `Velvet (dense pile) + Paramount Lighting (frontal)` = **Conflict**. The texture is destroyed. The interaction ontology flags this collision for the solver to resolve or penalize.

### Vibe × Optics
How the brand's aesthetic intent influences camera choices.
*Example:* `Vibe: Luxury Editorial` + `Lens: 35mm` = **Caution**. Luxury traditionally relies on high compression (85mm+) to isolate the subject. Wide angles are usually reserved for streetwear or environmental portraiture.

### Skin Tone × Color Grade
How melanin and undertones react to film emulation.
*Example:* `Skin Tone: Deep Warm` + `Grade: Cyan/Teal Lift` = **Conflict**. Teal shadow lifts can make deep, warm skin tones appear ashen or green. The interaction ontology suggests a `Warm Sandstone` or `Golden Hour` grade instead.

## 3. Conflict Resolution
When an interaction generates a **Conflict**, the solver references the active **Creative Objective (OBJ-001)** to resolve it.

*Example Conflict:* 
- Material dictates `Directional Hard Key` (to show texture).
- Vibe dictates `Soft Ethereal Lighting` (for romantic mood).

*Resolution (via Creative Objective):*
- If Primary Goal = `Preserve Fabric`, the solver chooses `Directional Hard Key`.
- If Primary Goal = `Elicit Emotion/Romance`, the solver chooses `Soft Ethereal Lighting`.

## 4. Candidate Diversity Tuning
To ensure the solver doesn't just output one hyper-optimized but boring result, the interaction ontology defines diversity tolerances. When generating `Solution A`, `Solution B`, and `Solution C`, the solver forces variances along non-critical axes (e.g., changing the background environment or the secondary fill light color) while maintaining the core physical validity.
