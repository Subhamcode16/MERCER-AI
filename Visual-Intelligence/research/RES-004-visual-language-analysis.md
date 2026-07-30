---
VIS-ID: RES-004
Title: Visual Language Analysis (Processing Station 4)
Version: 1.0.0
Status: Draft
Owner: Visual Intelligence Research (Track B)
Last Updated: 2026-07-01
Depends On:
  - VIO-005
  - RES-005
---

# RES-004: Visual Language Analysis (Processing Station 4)

## Purpose

**Processing Station 4 (Visual Language Analysis)** is the universal extraction layer of the Visual Intelligence Factory (VIF).

Unlike Processing Station 3—which focuses exclusively on isolated subjects to extract proprietary Fashion data—Station 4 looks at the *entire uncropped image*. Its purpose is to map the raw pixels to the **Universal Ontology (`VIO-005`)**, extracting the foundational rules of visual language (Lighting, Composition, Color). 

This station operates entirely agnostically. It applies the same analytical rigor regardless of whether the image is a photograph, a 3D product render, a magazine layout, or an illustration.

---

## 1. Station Contract

### A. Inputs
- **Asset ID:** Unique identifier.
- **Verified Full Image:** The original, uncropped image (from Station 1).

### B. Outputs
- **Universal Knowledge Claims (JSON):** An array of validated claims conforming to the `RES-005` Knowledge Claim Model.
- **Confidence Matrix:** A confidence score (0.0 - 1.0) calculated for *each* extracted claim.

---

## 2. Core Extraction Tasks (Global Analysis)

For V1 of the platform architecture, Station 4 performs **Global Extraction**—meaning it analyzes the overall visual properties of the entire scene, rather than mapping the specific lighting hitting a single local polygon.

### Task A: Medium Classification
- **Goal:** Determine the physical or digital nature of the asset.
- **Output (Claim):** `Subject: Medium`, `Predicate: Is`, `Value: Photography`, `Evidence: ["Film grain detected", "Photorealistic depth of field"]`

### Task B: Lighting Extraction
- **Goal:** Identify the primary light source direction, quality, and contrast ratio.
- **Output (Claim):** `Subject: Lighting`, `Predicate: Direction`, `Value: Side Lighting`, `Evidence: ["Deep shadows on the right side of frame", "Highlight roll-off on left"]`

### Task C: Composition & Framing
- **Goal:** Map the geometric structure of the image (Rule of Thirds, Symmetry, Perspective).
- **Output (Claim):** `Subject: Composition`, `Predicate: Framing`, `Value: Center Weighted`, `Evidence: ["Primary subject occupies central 40% of grid", "Equal negative space on horizontal axes"]`

### Task D: Color & Mood
- **Goal:** Extract the color palette and intended emotional resonance.
- **Output (Claim):** `Subject: Color`, `Predicate: Palette`, `Value: Monochromatic`, `Evidence: ["90% of pixels fall within Red hue range", "No complementary colors present"]`

---

## 3. The Power of Evidence

Because Station 4 adheres to the `RES-005` Knowledge Claim schema, it cannot simply output `Mood = Somber`. 

If the model claims the mood is Somber, it must provide `Evidence` (e.g., `["Low-key lighting", "Desaturated cool colors"]`). This evidence is what allows the human reviewer at Station 6 to accurately accept or reject the claim. It transforms visual extraction from a "black box guess" into a logical, arguable statement.

---

## 4. Failure Handling & Human Review (Station 6 Handoff)

1. **Automated Handoff:** The array of Universal Knowledge Claims is aggregated and passed downstream.
2. **Review Routing:** Processing Station 6 (Knowledge Verification) intercepts the payload. Any claim below the strict confidence threshold (e.g., `0.95`) is paused and queued for human verification.
3. **Continuous Fine-Tuning:** If the model struggles to accurately classify `Lighting.Quality = Hard` and is repeatedly corrected by human reviewers, those structured corrections serve as the exact training dataset to fine-tune the foundational vision models.

---

## 5. Architectural Boundaries

- **No Semantic Parsing:** Processing Station 4 cannot extract "Banarasi Silk" or "Nivi Drape." Its job is strictly the universal medium.
- **Global Scope (V1):** Station 4 analyzes the entire frame. Localized lighting analysis (e.g., "The left cheek of the subject has a specular highlight") is deferred to V2 architectures to prevent explosive graph complexity.
