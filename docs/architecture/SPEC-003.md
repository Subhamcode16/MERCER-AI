# SPEC-003
# Memory Specification (What have we learned?)

**Status:** Canonical  
**Version:** 1.0  
**Associated Law:** [LAW-003 (Laws of Memory)](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/System%20Laws/LAW-003.md)

---

## 1. Memory Ingestion & Triggers
Memory accumulates automatically through active workspace events.

### 1.1 Ingestion Triggers
- **Trigger 1 — Strategy Adjustment:** Occurs when a user modifies an AI-proposed Strategy Card. The difference between the AI proposal and the user override is logged.
- **Trigger 2 — Asset Finalization:** Triggered when the user exports or publishes a generated asset. This locks the visual styles as a "success" memory.
- **Trigger 3 — Performance Feedback:** Triggered when advertising metrics (e.g., CTR, conversion rate) are uploaded to a campaign.

---

## 2. Memory Organization & Scopes
The platform aggregates experience across four distinct layers to ensure context specificity.

```
┌─────────────────────────────────────────────────────────┐
│                    Workspace Memory                     │
│    (General preferences, pricing behaviors, team settings) │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                      Brand Memory                       │
│    (Style iterations, color trends, approved themes)    │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌───────────────────────────┴─────────────────────────────┐
│    Product Memory                 Campaign Memory       │
│  (Best angles, draping rules)  (Seasonal learnings)     │
└─────────────────────────────────────────────────────────┘
```

- **Brand Memory:** Captures long-term identity evolution. Remembers preferred layouts, color combinations, and audience reactions.
- **Product Memory:** Stores lessons learned from working with a specific product (e.g., "Product A displays best with a 45-degree angle showing its side zipper detail").
- **Campaign Memory:** Preserves short-term contextual findings (e.g., "Holiday campaigns perform better with darker, warm-toned lighting").

---

## 3. Memory-Driven Strategy Initialization
When initiating a new campaign, the system automatically pulls relevant memories to pre-populate strategy options.

### 3.1 Retrieval Protocol
1. New Campaign creation triggers a memory lookup matching the target audience and season.
2. The platform retrieves:
   - **Highly Rated Assets:** Finds previous campaigns for this brand that scored high in performance.
   - **Aesthetic Constraints:** Auto-applies historical overrides (e.g., "User consistently changes gold materials to matte finish").
3. Pre-populated strategy options show a memory badge (e.g., *"Based on your successful Summer launch"*).

---

## 4. Memory Governance & Forgetting UI
Users retain control over what the platform remembers.

### 4.1 Memory Governance Dashboard
- **Brand Memory Map:** Visualizes the brand's style concepts stored by the AI.
- **Memory Operations:**
  - **Pin Memory:** Locks a preference as permanent brand DNA (cannot be decayed).
  - **Prune/Forget:** Instantly deletes a memory node (e.g., clearing outdated seasonal preferences).
  - **Decay Configuration:** Allows brand owners to configure decay rates (e.g., "Let seasonal campaign memories decay after 90 days").
