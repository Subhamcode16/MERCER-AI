---
VIS-ID: VAL-001
Title: Textile Campaign Workflow Validation
Version: 1.1.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-30
---

# VAL-001: Textile Campaign Workflow Validation

## Purpose
This document simulates an end-to-end production workflow to stress-test the Visual Intelligence architecture. 
We validate that every action has exactly one owner, relies on explicit knowledge objects, and results in a clear decision.

## Scenario
**Workflow 001:** A Textile Client uploads a single image of a Saree. 
They want a complete campaign: Instagram posts, Catalog Images, Lifestyle Images, Video Ads, UGC, and Website Banners.

---

# Phase 1: User Input & Image Upload

**1. Event:** `User_Uploads_Image`
* **Owner:** `User Intelligence`
* **Reason:** Owns the entry point and session memory initialization.
* **Inputs:** Raw Multimodal Input (Saree Image + Text: "I need a campaign for this.")
* **Action:** Register Asset and initialize project scope.
* **Outputs:** `Project Memory` (Updated)
* **Decision:** Trigger Product Extraction.
* **Next Event:** `Extract_Product_Identity`

---

# Phase 2: Product Extraction (Hypothesis Generation)

**1. Event:** `Extract_Product_Identity`
* **Owner:** `Product Intelligence`
* **Reason:** Owns extraction of persistent product identity from visual assets.
* **Inputs:** Uploaded Image, `Visual Intelligence Ontology`
* **Action:** Analyze visual patterns to form hypotheses about the product.
* **Outputs:** `Candidate Product DNA`
    * Fabric: Silk (Confidence: 91%, Evidence: Lustrous sheen, drape)
    * Style: Banarasi (Confidence: 85%, Evidence: Floral brocade patterns)
    * Color: Royal Blue (Confidence: 96%, Evidence: Hex code match)
    * Embroidery: Gold Zari (Confidence: 74%, Evidence: Metallic thread reflectivity)
* **Decision:** Product identity is below 95% confidence threshold on key anchors. Require User Validation.
* **Next Event:** `Validate_Product_Identity`

---

# Phase 3: Adaptive Interview & Gap Analysis

**1. Event:** `Validate_Product_Identity`
* **Owner:** `Adaptive Interview Engine`
* **Reason:** Responsible for resolving low-confidence hypotheses through human-in-the-loop interaction.
* **Inputs:** `Candidate Product DNA`
* **Action:** Prompt user: "I see a Royal Blue Silk with Gold Zari. Is this a Banarasi Saree?" -> User: "Yes."
* **Outputs:** `Approved Product DNA`
    * Style: Banarasi (Confidence updated to 100%)
    * Embroidery: Gold Zari (Confidence updated to 100%)
* **Decision:** Product DNA locked. Proceed to Brand Gap Analysis.
* **Next Event:** `Identify_Brand_Positioning`

**2. Event:** `Identify_Brand_Positioning`
* **Owner:** `Brand Intelligence`
* **Reason:** Owns the extraction and maintenance of brand identity.
* **Inputs:** `Approved Product DNA`, `Project Memory`
* **Action:** Detect missing semantics. The system knows the *Product* but knows nothing about the *Brand* or *Business Goal*. Triggers `Adaptive Interview Engine` to ask: "Are we positioning this as a high-end heritage luxury brand, or a modern accessible festive brand?" -> User: "High-end heritage luxury. Targeting brides."
* **Outputs:** `Candidate Brand DNA`
    * Positioning: Luxury / Heritage (Confidence: 100%, Evidence: Explicit user input)
    * Audience: Bridal (Confidence: 100%, Evidence: Explicit user input)
* **Decision:** Brand DNA and Audience defined.
* **Next Event:** `Plan_Campaign_Structure`

---

# Phase 4: Creative Reasoning (Campaign & Scene Planning)

**1. Event:** `Plan_Campaign_Structure`
* **Owner:** `Marketing Intelligence`
* **Reason:** Translates business goals ("Instagram, Catalog...") into a structured hierarchy of deliverables.
* **Inputs:** User Request, `Approved Product DNA`, `Candidate Brand DNA`
* **Action:** Generate Storyboard.
* **Outputs:** `Campaign Strategy` -> `Storyboard` (5 distinct Scenes)
* **Decision:** Campaign structured.
* **Next Event:** `Plan_Scene_Semantics`

**2. Event:** `Plan_Scene_Semantics` (Example: Lifestyle Scene)
* **Owner:** `Creative Decision Engine`
* **Reason:** Orchestrates `Scene Intelligence` and `Lighting Intelligence` to resolve creative constraints.
* **Inputs:** `Campaign Strategy`, `Candidate Brand DNA` (Luxury + Heritage + Bridal)
* **Action:** Decide the environment, lighting, and composition based on Semantics.
    * *Hypothesis 1:* Luxury Bridal -> requires grand architecture -> Palace Courtyard.
    * *Hypothesis 2:* Heritage -> requires timeless lighting -> Golden Hour.
* **Outputs:** `Scene DNA`
    * Location: Palace Courtyard
    * Lighting: Golden Hour
    * Mood: Regal
* **Decision:** Scene 1 explicitly defined.
* **Next Event:** `Cast_Character`

---

# Phase 5: Character Planning

**1. Event:** `Cast_Character`
* **Owner:** `Character Intelligence`
* **Reason:** Owns the persistent identity of human models.
* **Inputs:** `Scene DNA`, `Candidate Brand DNA` (Bridal, Heritage)
* **Action:** Select/Generate a character profile matching the constraints.
* **Outputs:** `Character DNA`
    * Traits: South Asian, Bridal Makeup, Heavy Antique Gold Jewelry.
* **Decision:** Character cast and locked for the scene.
* **Next Event:** `Compile_Prompt`

---

# Phase 6: Prompt Compilation & Rendering

**1. Event:** `Compile_Prompt`
* **Owner:** `Platform Intelligence`
* **Reason:** Translates internal DNA objects into syntax specific to external renderers.
* **Inputs:** `Product DNA` + `Character DNA` + `Scene DNA`
* **Action:** Compile structured string/payload.
* **Outputs:** `Execution Instructions` (Midjourney/Flux Prompt)
* **Decision:** Prompt ready for rendering.
* **Next Event:** `Execute_Render`

**2. Event:** `Execute_Render`
* **Owner:** `Renderer` (External API)
* **Reason:** Executes pixel generation. Owns no permanent knowledge.
* **Inputs:** `Execution Instructions`
* **Action:** Call API.
* **Outputs:** Raw Pixels (Candidate Image)
* **Decision:** Image generated.
* **Next Event:** `Evaluate_Quality`

---

# Phase 7: Continuous Evaluation (Quality Assurance)

**1. Event:** `Evaluate_Quality`
* **Owner:** `Evaluation Intelligence`
* **Reason:** Enforces strict adherence to locked DNA constraints.
* **Inputs:** Raw Pixels, `Product DNA`, `Scene DNA`
* **Action:** Evaluate generated image against the anchors.
    * *Check:* Does the border match the `Product DNA`? (Yes)
    * *Check:* Is the lighting "Golden Hour" as per `Scene DNA`? (Yes)
* **Outputs:** Evaluation Report
* **Decision:** Pass. If failure (e.g., Zari pattern hallucinated), decision is to branch back to `Execute_Render`.
* **Next Event:** `Deliver_Assets`

---

# Phase 8: Final Delivery

**1. Event:** `Deliver_Assets`
* **Owner:** `User Intelligence`
* **Reason:** Owns the final handoff and project state finalization.
* **Inputs:** Approved Images
* **Action:** Present assets in requested formats.
* **Outputs:** `Project Memory` (Finalized)
* **Decision:** Workflow Complete.
