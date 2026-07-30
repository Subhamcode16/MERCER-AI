---
Title: Commercial Semantics Ontology
ID: VIO-008
Status: Draft
---

# VIO-008: Commercial Semantics

This ontology models *why* the image exists—the target audience, the market positioning, and the campaign intent.

## 1. Domain Purpose
To strictly classify the commercial intent of a visual asset, allowing the Pattern Discovery engine to map a "vibe" to specific Visual Craft and Styling patterns.

## 2. Core Hierarchy

```text
Commercial Semantics
├── Campaign Type
│   ├── Editorial (Magazine spread)
│   ├── E-commerce Catalog (White background)
│   ├── Lookbook
│   └── Social Media / UGC
├── Target Demographic
│   ├── Bridal
│   ├── Festive / Occasion Wear
│   ├── Casual / Daily
│   └── Resort Wear
└── Market Position
    ├── Ultra-Luxury (Heritage/Designer)
    ├── Premium (Boutique)
    └── Mass Market (Accessible)
```

## 3. Node Definitions

- **Bridal:** Content targeted at weddings, implying heavy styling, rich colors, and culturally significant presentation.
- **Editorial:** High-fashion storytelling focused on mood, art direction, and brand identity rather than pure product clarity.

## 4. Usage in Runtime (Track A)
When a user requests a "Luxury Bridal" vibe, they are passing a parameter that maps to `Commercial Semantics -> Target Demographic -> Bridal` and `Commercial Semantics -> Market Position -> Ultra-Luxury`. The Decision Engine retrieves the corresponding expert patterns for Visual Craft.
