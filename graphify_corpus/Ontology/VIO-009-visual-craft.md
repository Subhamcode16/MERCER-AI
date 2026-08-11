---
Title: Visual Craft Ontology
ID: VIO-009
Status: Draft
---

# VIO-009: Visual Craft

This ontology represents *how* an image is captured and rendered. It treats photographic and cinematic parameters as first-class semantic knowledge, elevating the system from mere "prompt generation" to structured "Visual Direction."

## 1. Domain Purpose
To strictly classify lighting, camera mechanics, composition, and aesthetic grading, ensuring that creative decisions are structured data, not loose strings.

## 2. Core Hierarchy

```text
Visual Craft
├── Camera System
│   ├── Lens (Focal Length)
│   │   ├── 35mm (Wide)
│   │   ├── 50mm (Normal)
│   │   └── 85mm (Portrait Compression)
│   ├── Aperture / Depth of Field
│   │   ├── f/1.4 - f/2.8 (Shallow)
│   │   └── f/8 - f/11 (Deep)
│   └── Framing / Perspective
│       ├── Eye-Level
│       ├── Low Angle
│       └── Close-up
├── Lighting
│   ├── Key Light
│   │   ├── Soft Window Light
│   │   ├── Hard Direct Sun
│   │   └── Studio Softbox
│   ├── Fill Ratio
│   │   ├── High Contrast (Low Fill)
│   │   └── Flat (High Fill)
│   └── Time of Day
│       ├── Golden Hour
│       └── Blue Hour
├── Image Quality & Rendering
│   ├── Micro-contrast
│   ├── Highlight Roll-off
│   └── Film Stock Simulation (e.g., Kodak Portra, ARRI Look)
└── Color Grading
    ├── Warm (Golds, Ambers)
    ├── Cool (Blues, Cyans)
    └── Muted / Desaturated
```

## 3. Node Definitions

- **85mm Lens:** A short telephoto focal length that provides flattering facial compression and distinct subject isolation (background blur) for portraits.
- **Golden Hour:** The period of daytime shortly after sunrise or before sunset, characterized by soft, warm, directional lighting.

## 4. Lighting Nodes (Phase 2 Additions)

- **Chiaroscuro / Strobe:** Cool diffused window light mixed with a sharp strobe, creating dramatic, high-contrast shadows. (Used for Editorial Studio)
- **Firelight / Nocturne:** Low light ambiance, warm flickering firelight (diyas) casting dynamic shadows, subtle cool moonlight rim on hair. (Used for Nighttime Palace)
- **Overcast Daylight:** Bright, overcast daylight acting as a massive softbox, providing even natural illumination. (Used for Lush Garden)
- **Ethereal Backlight / Edge Wrap:** Strong, diffused, blown-out backlight coming from a window or door behind the subject, wrapping around the edges of a sheer veil. (Used for High-Key Window Doorway)

## 5. Usage in the Ecosystem

**In Track B (VIF):**
Station 4 extracts Visual Craft Claims from an input image.
*Example Claim:* `Subject: Scene, Predicate: Lens, Value: 85mm`

**In Track A (Runtime):**
The Expert Pattern Library maps Commercial Semantics to specific Visual Craft nodes.
*Example:* `Luxury Bridal -> 85mm Lens, f/2.8, Soft Warm Key Light`
