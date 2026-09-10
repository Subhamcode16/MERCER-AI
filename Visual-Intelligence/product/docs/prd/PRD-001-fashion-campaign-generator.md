---
PRD-ID: PRD-001
Title: Fashion Campaign Generator MVP
Version: 1.0.0
Status: Draft
Owner: Product (Layer 2)
Last Updated: 2026-07-01
---

# PRD-001: Fashion Campaign Generator MVP

## 1. Product Vision

The Fashion Campaign Generator MVP is the first commercial application built on top of the **Creative Intelligence Infrastructure**. 

It transitions the platform from a theoretical research architecture into a tangible product. By isolating the MVP to a strict vertical slice—Sarees—we will rigorously validate the platform's core thesis: *Can structured visual intelligence generate commercial-grade marketing assets that outperform blind prompting?*

---

## 2. Target Persona: The Brand Owner

For the MVP, the target user is a **Fashion Brand Owner** or **E-Commerce Manager**. 
They are *not* prompt engineers. They do not want to manipulate lighting ratios or configure camera lenses. 

**Their Pain Point:** They have a flat lay or mannequin photo of a new Saree, and they need a high-end luxury campaign for Instagram, but they cannot afford a $10,000 photoshoot.
**Their Desire:** "Take my product, put it on a beautiful model in a luxury setting, and make it look expensive."

---

## 3. The User Journey (The "Magic" Flow)

The application interface must completely hide the complex Runtime and Knowledge Factory architecture. The user experiences a simple, 4-step flow:

1. **Upload:** The user uploads a single image of a Saree (flat lay or simple model shot).
2. **Analysis (Invisible):** 
   - The VIF ingests the image and extracts the `Product DNA` (Banarasi, Gold Zari, Red Silk). 
   - *The user simply sees a loading spinner saying "Analyzing weave and fabric..."*
3. **Select Vibe:** The user is presented with 3 curated campaign aesthetics (e.g., *Luxury Wedding*, *Festive Evening*, *Summer Casual*). The user selects one.
4. **Delivery:** The platform generates and delivers 4 photorealistic campaign images.

---

## 4. Scope Boundaries (Strict Exclusions)

To guarantee quality, the MVP is ruthlessly scoped:

- **Supported Inputs:** ONLY Indian Sarees (specifically Banarasi, Kanjeevaram, and Silk). No western wear, no menswear, no complex multi-garment outfits.
- **Supported Outputs:** ONLY still images (1024x1024 or 1080x1350). No video generation in V1.
- **Customization Limits:** The user cannot write custom text prompts. They must select from predefined Campaign Vibe presets. (This allows us to leverage pre-validated *Knowledge Patterns*).

---

## 5. Success Metrics (Objective Quality)

We reject the vague metric of "99.99% accuracy." The MVP will be evaluated against objective, domain-specific metrics calculated over a test run of 500 campaigns:

1. **Product Fidelity (Target: >90%):** Does the generated saree preserve the exact weave, border, pallu, and embroidery of the uploaded input?
2. **Identity Consistency (Target: >85%):** If generating multiple shots in a single campaign, does the model's face and the product remain consistent?
3. **Creative Consistency (Target: >95%):** Does the generated image strictly adhere to the retrieved *Knowledge Pattern* (e.g., if 'Luxury Wedding' mandates Golden Hour lighting, is it present)?
4. **Human Approval Rate (Target: >75%):** What percentage of generated assets does a human QA tester accept as "commercial-ready" without any revision?

---

## 6. Failure Modes & Fallbacks

- **Unrecognized Product:** If the VIF cannot confidently extract the Saree's Product DNA (Confidence < 0.70), the UI will gracefully inform the user: *"We couldn't perfectly analyze this fabric. Please upload a higher resolution image."* It will *not* attempt to generate a hallucinated garment.
- **Aesthetic Drift:** If the underlying Image Execution model hallucinates an unrelated background element, the `Evaluation Intelligence` (Track C) should flag it internally for review, ensuring the prompt compiler is tweaked in the next deployment.
