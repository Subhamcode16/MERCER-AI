---
VIS-ID: RES-003
Title: Attribute Extraction Framework (Station 3)
Version: 1.0.0
Status: Draft
Owner: Visual Intelligence Research (Track B)
Last Updated: 2026-07-01
Depends On:
  - RES-002
  - VIO-006
---

# RES-003: Attribute Extraction Framework (Station 3)

## Purpose

The **Attribute Extraction Framework (Station 3)** is the first semantic layer of the Visual Intelligence Factory (VIF). 

Once Station 2 isolates the primary foreground subject, Station 3 receives the cropped, normalized image data. Its purpose is to map those raw pixels strictly to the **Domain Ontology (`VIO-006`)**.

Because generalized AI models lack deep domain expertise (e.g., they cannot reliably distinguish a Banarasi weave from a Kanjeevaram weave), this station **does not use a single massive multimodal model**. Instead, it uses an ensemble of highly specialized, fine-tuned micro-models (Classifiers) to guarantee proprietary accuracy.

---

## 1. Station Contract

### A. Inputs
- **Verified Image Asset** (From Station 1).
- **Coordinate Metadata & Subject Masks** (From Station 2). *Allows the station to ignore background pixels and focus purely on the garment/subject.*

### B. Outputs
- **Domain Knowledge Claims (JSON):** A structured payload containing arrays of validated claims (defined in `RES-005`), where every Subject and Predicate corresponds to an entity defined in `VIO-006`.
- **Evidence payload:** Extracted visual or semantic evidence backing each claim.
- **Confidence Matrix:** A confidence score (0.0 - 1.0) calculated for *each* extracted claim.

---

## 2. Core Extraction Tasks (The Ensemble)

Instead of asking one model to "describe the fashion," Station 3 passes the masked subject through parallel, specialized extraction tasks:

### Task A: Garment Classification
- **Model:** Garment Topology Classifier.
- **Goal:** Identify the base structure. (e.g., Saree, Lehenga, Sherwani).
- **Output (Claim):** `Subject: Garment`, `Predicate: IsA`, `Value: Saree`, `Evidence: ["Unstitched drape over shoulder", "Pleats at waist"]`

### Task B: Material & Weave Analysis
- **Model:** Textile Texture Analyzer (Fine-tuned on macro/micro fabric patterns).
- **Goal:** Identify the physical material and specific weaving technique.
- **Output (Claim):** `Subject: Weave`, `Predicate: Technique`, `Value: Banarasi`, `Evidence: ["Heavy gold zari border", "Floral brocade motifs", "Silk texture"]`

### Task C: Embellishment & Detailing Detection
- **Model:** Surface Detailing Detector.
- **Goal:** Identify borders, motifs, and handwork.
- **Output (Claim):** `Subject: Embellishment`, `Predicate: Type`, `Value: Zari Border`, `Evidence: ["Metallic gold thread along hem"]`

### Task D: Drape & Styling Analysis
- **Model:** Drape Topology Classifier.
- **Goal:** Understand how the garment is physically worn (crucial for sarees).
- **Output (Claim):** `Subject: Drape`, `Predicate: Style`, `Value: Nivi`, `Evidence: ["Pallu draped over left shoulder", "Front pleats tucked in center"]`

---

## 3. Confidence & Quality Enforcement

Because Processing Station 3 uses an ensemble approach, confidence is calculated per-claim, not per-image.

**Example Confidence Matrix:**
- `Claim: Garment=Saree`: **0.99** (High Confidence)
- `Claim: Fabric=Silk`: **0.95** (High Confidence)
- `Claim: Weave=Banarasi`: **0.72** (Low Confidence)

### Handling Uncertainty
If a single, massive model fails, the entire image fails. By isolating extraction into micro-tasks, we preserve the successful data.
- The `Saree` and `Silk` claims are locked in as verified.
- Only the `Banarasi` claim is flagged for human review. 

---

## 4. Failure Handling & Human Review (Station 6 Handoff)

1. **Automated Handoff:** The complete array of Knowledge Claims is passed downstream.
2. **Review Routing:** Processing Station 6 (Knowledge Verification) will intercept the payload. Any claim below the `0.90` threshold (e.g., the `0.72` Banarasi claim) will be queued for a human Fashion Expert to manually verify or correct. The expert will see the `Evidence` provided by the model to understand *why* it made that claim.
3. **Continuous Learning:** Once the human expert corrects the `Weave=Banarasi` claim (e.g., providing reason: "Border pattern matches Kanjeevaram"), that structured correction is used as training data to further fine-tune the Textile Texture Analyzer (Task B).

---

## 5. Architectural Boundaries

- **No Universal Concepts:** Processing Station 3 does not care about "Soft Lighting" or "Rule of Thirds." That is strictly the job of Processing Station 4 (Visual Language Analysis) processing the Universal Ontology (`VIO-005`).
- **No Free-text Descriptions:** Processing Station 3 does not output paragraphs of text (e.g., "A beautiful red saree"). It exclusively outputs structured `Knowledge Claims` backed by `Evidence`.
