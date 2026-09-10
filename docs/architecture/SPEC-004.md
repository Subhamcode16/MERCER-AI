# SPEC-004
# Collaboration Specification (How do humans and AI decide together?)

**Status:** Canonical  
**Version:** 1.0  
**Associated Law:** [LAW-004 (Laws of Collaboration)](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/System%20Laws/LAW-004.md)

---

## 1. Bento Workspace Canvas
The main campaign planning screen organizes information as a dynamic, interactive grid (Bento Canvas).

### 1.1 Canvas Components
- **Product Preview Card:** Displays the uploaded product image, transparent silhouette, and verified attributes.
- **Brand Context Card:** Displays the active Brand guidelines, logos, and color restrictions.
- **AI Strategy Cards Grid:** Displays the reasoning cards that the user must review and approve before rendering starts.

---

## 2. Interactive AI Strategy Cards
Each card represents a core creative decision.

### 2.1 Card Specifications
- **Audience Card:**
  - Displays target demographic tags.
  - *Interactivity:* User can add/remove audience tags or type custom descriptors.
- **Narrative & Theme Card:**
  - Displays the campaign concept narrative and proposed tagline.
  - *Interactivity:* Editable text field with an "AI Rewrite" utility for quick tone adjustments.
- **Visual Composition Card:**
  - Displays composition (e.g., "Rule of Thirds"), camera focal length, and lighting type.
  - *Interactivity:* Dropdowns for preset visual settings and a custom prompt text box.

---

## 3. The Reasoning Reveal Workflow
To prevent black-box generation, the platform enforces a step-by-step collaborative sequence.

```
┌──────────────────────────────────────────────────────────┐
│                 Step 1: Ingestion                        │
│ User uploads product. Base attributes extracted.         │
└───────────────────────────┬──────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────┐
│                 Step 2: Strategy Reveal                  │
│ AI displays Bento Cards. User edits Strategy & Layout.   │
└───────────────────────────┬──────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────┐
│                 Step 3: Intent Alignment                 │
│ User reviews options and clicks "Approve Strategy".       │
└───────────────────────────┬──────────────────────────────┘
                            ▼
┌──────────────────────────────────────────────────────────┐
│                 Step 4: Safe Execution                   │
│ Rendering layer unlocks. Images generate progressively.    │
└──────────────────────────────────────────────────────────┘
```

- **Enforced Gate:** The "Generate Assets" button remains disabled until the user confirms alignment by clicking the **"Approve Strategy"** button.

---

## 4. Conflict Resolution & Contradiction Alert
When a user edit contradicts established Brand rules or domain laws, the system alerts the user.

### 4.1 Alert Behavior
- **Visual Indicator:** The border of the conflicting card flashes amber, displaying a soft alert icon.
- **Contextual Warning Card:** Explains the conflict clearly (e.g., *"Warning: The selected 'Streetwear Graffiti' theme conflicts with the active brand's 'Quiet Luxury' guidelines"*).
- **Options Provided:**
  1. **Align:** Reset the card to the brand-consistent default.
  2. **Override:** Proceed with the exception (this logs a brand memory exception).
  3. **Refine:** Open the card to adjust settings to find a middle ground.
