---
VIS-ID: VAL-001
Title: Textile Campaign Workflow Validation
Version: 1.0.0
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

**1. Event:** User uploads a single image of a saree and types: "I need a campaign for this."
* **Action:** Receive raw multimodal input (text + image).
* **Owner:** `User Intelligence`
* **Knowledge Object:** `Project Memory` (creates new project session)
* **Output:** Raw input registered. Triggers analysis.

**2. Event:** Initial Image Analysis
* **Action:** Extract physical attributes (Fabric: Silk, Style: Banarasi, Color: Royal Blue/Gold Zari, Embroidery: Heavy Brocade).
* **Owner:** `Product Intelligence`
* **Knowledge Object:** `Product DNA` (initial draft created)
* **Output:** Product identity locked with low confidence (needs user verification).

---

# Phase 2: Adaptive Interview (Gap Analysis)

**1. Event:** Gap Analysis for Brand & Audience
* **Action:** The system evaluates current knowledge. It knows the *Product* but knows nothing about the *Brand* or *Business Goal*.
* **Owner:** `Creative Decision Engine` (identifies missing semantics) -> delegates to `Adaptive Interview Engine`
* **Knowledge Object:** `Creative Semantic Model` (identifying missing layers)
* **Output:** Interview triggered.

**2. Event:** The Interview
* **Action:** System asks targeted questions to establish positioning rather than asking for prompts.
    * *System:* "This looks like a premium Banarasi silk. Are we positioning this as a high-end heritage luxury brand, or a modern accessible festive brand?"
    * *User:* "High-end heritage luxury. We want to target brides."
* **Owner:** `Adaptive Interview Engine` (asks) -> `Brand Intelligence` (processes response)
* **Knowledge Object:** `Brand DNA` (created) and `Audience Memory`
* **Output:** Brand positioned as "Luxury/Heritage". Audience positioned as "Bridal".

---

# Phase 3: Product Extraction & Validation

**1. Event:** Product DNA Lock
* **Action:** System asks user to verify the extracted product details to ensure strict consistency across the campaign.
    * *System:* "I've identified this as a Banarasi Silk with heavy gold Zari. I will lock this pattern to ensure it looks identical in all shots. Correct?"
    * *User:* "Yes."
* **Owner:** `Product Intelligence`
* **Knowledge Object:** `Product DNA` (Confidence reaches 100%)
* **Output:** Product constraints locked. Rendering layer is now strictly constrained by this DNA.

---

# Phase 4: Creative Reasoning (Campaign & Scene Planning)

**1. Event:** Campaign Structuring
* **Action:** Transform the user's request ("Instagram, Catalog, Lifestyle, Video, UGC, Banners") into a structured hierarchy of deliverables.
* **Owner:** `Marketing Intelligence`
* **Knowledge Object:** `Campaign Strategy` -> `Storyboard`
* **Output:** Campaign structured into 5 distinct Scenes.

**2. Event:** Scene Semantic Planning (Example: Lifestyle Scene)
* **Action:** Decide the environment, lighting, and composition based on Semantics (Luxury + Heritage + Bridal).
    * *Reasoning:* Luxury Bridal -> requires grand architecture -> Palace Courtyard.
    * *Reasoning:* Heritage -> requires timeless lighting -> Golden Hour.
* **Owner:** `Creative Decision Engine` (orchestrating `Scene Intelligence` and `Lighting Intelligence`)
* **Knowledge Object:** `Creative World Model` -> `Scene DNA`
* **Output:** Scene 1 explicitly defined (Location: Palace Courtyard, Lighting: Golden Hour, Mood: Regal).

---

# Phase 5: Character Planning

**1. Event:** Character Casting
* **Action:** Select a model that fits the Audience (Bridal) and Brand (Heritage Luxury). 
* **Owner:** `Character Intelligence`
* **Knowledge Object:** `Character DNA` (created and locked)
* **Output:** Character established (South Asian, Bridal Makeup, Heavy Antique Gold Jewelry).

---

# Phase 6: Prompt Compilation & Rendering

**1. Event:** Translation to Execution
* **Action:** Compile the structured DNA (Product DNA + Character DNA + Scene DNA + Lighting DNA) into specific syntax required by external renderers.
* **Owner:** `Platform Intelligence` (or `Model Intelligence` / Renderer Router)
* **Knowledge Object:** `Execution Instructions` (Prompts)
* **Output:** Structured prompt generated.

**2. Event:** Model Routing & Generation
* **Action:** Send Lifestyle Image request to Midjourney/Flux. Send Video Ad request to Kling/Veo.
* **Owner:** `Renderer` (External)
* **Knowledge Object:** N/A (Execution layer owns no permanent knowledge)
* **Output:** Raw pixels generated.

---

# Phase 7: Evaluation & Regeneration

**1. Event:** Quality Assurance
* **Action:** Evaluate the raw pixels against the locked DNA.
    * *Check:* Does the border match the `Product DNA`?
    * *Check:* Is the lighting "Golden Hour" as per `Lighting DNA`?
* **Owner:** `Evaluation Intelligence`
* **Knowledge Object:** `Evaluation Memory`
* **Output:** If failure (e.g., Zari pattern hallucinated), send feedback loop to `Model Intelligence` for regeneration. If pass, mark as Approved.

---

# Phase 8: Final Delivery

**1. Event:** Asset Delivery
* **Action:** Present the evaluated, consistent assets to the user across the requested formats.
* **Owner:** `User Intelligence`
* **Knowledge Object:** `Project Memory` (Asset marked as final)
* **Output:** Campaign delivered.

---

# Architectural Verification Results

* **No Ambiguity:** Every step successfully routed to a specific Intelligence Domain.
* **No Missing Owners:** All decisions were owned by a designated intelligence component (e.g., Lighting Intelligence, Product Intelligence).
* **DNA Integrity:** Visual DNA remained the source of truth, heavily utilizing the `Creative Decision Engine` and `Adaptive Interview Engine` to bridge the gap between User Intent and Execution.
* **Conclusion:** The architecture is structurally sound for this use case. We can proceed to formalize the specific DNA abstractions (Character, Product, Brand).
