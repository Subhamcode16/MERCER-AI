# ENGINEERING-RESPONSE-001
# Round Table Conference: Prompt Engine Finalization

**From:** Engineering Agent  
**To:** Intelligence Architect  
**Status:** IN PROGRESS  
**Version:** 1.0  
**Date:** 2026-08-16  

---

## 1. Interpretation of Instruction

*   **Problem Statement:** Recent generated visual library assets suffered from a flat, airbrushed digital look ("AI slop") and failed to reflect the detailed physical drape, lighting angles, and texture rules specified in our ontology.
*   **Conference Objective:** Standardize and finalize the prompt compilation pipeline in `PromptCompiler` to enforce analog realism, realistic skin and fabric textures, and negative parameter containment, using the reference image (`test/lb_001_editorial_studio_1784833153777.png`) as the quality benchmark.

---

## 2. First Communication Task: Architectural Status Report

Following Section 19 of `ENGINEER-COMMUNICATION-001`, here is the status of the runtime prompt and generation engine:

*   **IMPLEMENTED:**
    *   `decision_engine.py`: Synthesizes VIF Knowledge Claims into a Product DNA representation and performs basic vibe lookup.
    *   `constraint_solver.py`: Applies logical rules (System 2) to resolve fabric physics constraints to lighting/camera configurations.
    *   `authenticity_profiles.json`: Stores numerical weights (`Luxury Bridal`, `Editorial`, `E-Commerce Catalog`) for physical and optical imperfections.
*   **PARTIALLY IMPLEMENTED (Critical Gap):**
    *   `prompt_compiler.py`: Currently extracts the `Authenticity_Profile` (line 38) but does not compile it into the output string. It also appends a hardcoded slop trigger: `"High fashion, cinematic, 8k resolution, photorealistic."`
*   **PLANNED:**
    *   Refactoring of `prompt_compiler.py` to map logical constraints and authenticity profiles to a standardized 7-segment output structure.
*   **MISSING:**
    *   A pre-save validation script to verify that generated images conform to the target authenticity profiles (e.g. correct aspect ratio, lack of airbrushed skin artifacts).

---

## 3. Proposed Refactoring of `PromptCompiler`

We propose that the compiled prompt must strictly follow a 7-segment layout:

```text
SUBJECT: [Waist-up or medium close-up framing of the model, pose, and expression]
MATERIAL: [Fabric weight, weave relief, drape tension, and texture characteristics]
LIGHTING: [Key light direction, color temperature, and fill/shadow ratio]
CAMERA: [Focal length, aperture, camera height, and film emulation]
ENVIRONMENT: [Minimalist background or negative space backdrop]
QUALITY: [Dynamic compilation of Authenticity Profile weights to text]
FORBIDDEN: [Dynamic compilation of negative rules to prevent airbrushing/CGI looks]
```

### Dynamic Imperfection Mapping:
*   **Skin Pores (>0.7):** Compiles `"Natural skin texture with visible micro-pores, fine peach fuzz, and natural facial asymmetry"` to `QUALITY`, and `"smooth plastic skin, airbrushed textures"` to `FORBIDDEN`.
*   **Film Grain (>0.4):** Compiles `"Kodak Portra 400 film response, gentle analog grain, soft shadow rolloff"` to `QUALITY`, and `"digital sharpening artifacts, digital noise"` to `FORBIDDEN`.
*   **Fabric Wrinkles (>0.5):** Compiles `"authentic drape tension, visible micro-wrinkles at fabric stress points"` to `QUALITY`, and `"AI-smooth fabric surface, unnaturally smooth folds"` to `FORBIDDEN`.

---

## 4. Open Questions for the Architect

We seek the Intelligence Architect's confirmation on the following constraints:

1.  **Vibe to Profile Mapping:** How should incoming user requests map to the three profiles (`Luxury Bridal`, `Editorial`, `E-Commerce Catalog`) when a custom profile is not provided?
2.  **Detail Allocation Constraint:** Shall we freeze the rule that the compiler forces a `waist-up/medium close-up` crop and a `minimalist studio environment` whenever high-detail editorial realism is requested, to prevent detail dilution?
3.  **Removal of Slop Keywords:** Can we get a **FREEZE** decision to completely ban generic words like `"photorealistic"`, `"hyperrealistic"`, and `"8k"` from the compiler output?
