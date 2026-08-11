---
Title: Styling & Presentation Ontology
ID: VIO-007
Status: Draft
---

# VIO-007: Styling & Presentation

This ontology codifies *how* a garment is worn, accessorized, and presented on a subject.

## 1. Domain Purpose
To strictly classify draping styles, jewelry, makeup, hairstyles, and overall physical presentation of the model/subject.

## 2. Core Hierarchy

```text
Styling & Presentation
├── Draping Style
│   ├── Nivi Drape
│   ├── Bengali Drape
│   ├── Gujarati Drape
│   └── Modern Pre-stitched
├── Jewelry
│   ├── Antique Gold
│   ├── Polki/Kundan
│   ├── Diamond
│   ├── Temple Jewelry
│   └── Minimalist
├── Makeup & Hair
│   ├── Traditional Bridal
│   ├── Editorial/High-Fashion
│   ├── Minimal/Dewy
│   └── Floral Hair Accents (Gajra)
└── Footwear
    ├── Juttis
    ├── Heels
    └── Barefoot
```

## 3. Node Definitions

- **Temple Jewelry:** Intricately crafted chunky gold jewelry originating from South India, often featuring deities.
- **Nivi Drape:** The most common standard style of draping a saree, originating from Andhra Pradesh.
- **South Indian Bridal Drape (Madisaru/Traditional):** Distinctive draping style often used with Kanjeevaram sarees, featuring unique pleating at the back or structured front pleats.
- **Gajra:** A traditional Indian hair garland made of fresh jasmine flowers, typically wrapped around a bun or braid (essential for authentic South Indian bridal styling).

## 4. Usage in VIF
Styling patterns are retrieved during Pattern Discovery based on the target Commerce Semantics. 

*Example Claim (If parsed from image):*
`Subject: Model, Predicate: Jewelry_Style, Value: Temple_Jewelry`
