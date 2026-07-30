# IMG-002: Physics Ontology

## 1. Core Purpose
The Physics Ontology defines the fundamental ground truth of materials and environments within the Visual Intelligence Platform. It shifts the engine's reasoning from semantic associations ("silk looks shiny") to physical truths ("Banarasi silk has an anisotropic reflectance profile due to metallic woven threads").

By defining the physical realities of the subjects, the Image Formation Solver (IMG-001) can mathematically derive the optimal lighting, camera, and grading parameters needed to accurately capture them.

## 2. The Material Ontology (`material_ontology.json`)
The foundation of the physics engine is the material database. Every textile, metal, and skin type is mapped across multiple physical vectors.

### Key Physical Parameters:
- **Mass / Weight:** Governs drape, gravity response, and structural rigidity (e.g., Chiffon = low mass, Brocade = high mass).
- **Wrinkle Frequency & Amplitude:** How the fabric folds (e.g., Linen = high frequency/sharp amplitude, Neoprene = low frequency/smooth amplitude).
- **Surface Topology:** Micro-structure (e.g., Velvet = dense pile, Satin = smooth planar).
- **Reflectance Profile (BRDF proxy):**
  - Diffuse vs. Specular ratio.
  - Anisotropy (directionality of reflection).
  - Transmission (opacity vs. translucency).
- **Metallic Content:** Presence of conductive threads (Zari) altering highlight behavior.

## 3. Physics-Optics Mapping (`physics_optics_mapping.json`)
This defines how the physical parameters from the Material Ontology dictate optical behavior in the real world. This is the bridge between physics and photography.

### Example Mappings:
- **High Specularity -> Requires Diffusion:** A highly specular surface (like patent leather) requires large, soft light sources (diffusion) to prevent blown-out, clipped highlights.
- **High Anisotropy -> Requires Directionality:** A fabric with anisotropic highlights (like brushed silk) requires hard, directional light to reveal the fabric's structural grain.
- **Low Mass (Translucent) -> Requires Backlighting:** A sheer fabric (like Organza) requires a backlight or rim light to reveal its transmission properties and separate it from the background.
- **High Wrinkle Frequency -> Requires Raking Light:** Fabrics with deep textures (like heavy linen or embroidery) benefit from raking light (light entering at a steep angle) to maximize microcontrast and texture definition.

## 4. Implementation in the Solver
When the Prompt Compiler receives a Product DNA (e.g., "Banarasi Silk Saree"):
1. It queries `material_ontology.json` to retrieve the physical parameters of Banarasi Silk (High Mass, Anisotropic Reflectance, Metallic Content).
2. The solver uses `physics_optics_mapping.json` as the Stage 1 and Stage 2 constraints in the Creative Fitness Function.
3. If the solver evaluates a candidate with "Flat Frontal Lighting", it rejects it because the mapping states that Anisotropic/Metallic materials require Directionality.
