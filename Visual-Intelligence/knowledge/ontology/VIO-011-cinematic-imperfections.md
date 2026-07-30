---
Title: Cinematic Imperfections Ontology
ID: VIO-011
Status: Draft
---

# VIO-011: Cinematic Imperfections (Authenticity Profiles)

This ontology codifies the principle that "Luxury comes from imperfections." Perfect optics, perfect skin, and perfect textures read as artificially generated (AI). This ontology formalizes the deliberate introduction of optical and physical imperfections as a core semantic dimension of visual style.

## 1. Domain Purpose

To map physical, atmospheric, and optical imperfections to specific commercial aesthetics (Authenticity Profiles) rather than treating them as a universal "anti-AI" layer.

## 2. Authenticity Profiles

An Authenticity Profile is a weighted vector of imperfections assigned to a specific target aesthetic. Different mediums and campaigns require vastly different imperfection signatures.

### Example Profiles

**1. High Fashion Editorial**
Requires hyper-realism but pristine optics.
- `Skin Pores`: 0.8
- `Hair Flyaways`: 0.6
- `Fabric Wrinkles`: 0.7
- `Lens Imperfections`: 0.1
- `Film Grain`: 0.0

**2. Vintage / Heritage Documentary**
Requires atmospheric and optical character.
- `Film Grain`: 0.9 (e.g., Kodak Portra emulation)
- `Lens Flare & Halation`: 0.7
- `Atmospheric Dust`: 0.6
- `Skin Pores`: 0.8
- `Sensor Noise / Gate Weave`: 0.5

**3. Luxury E-Commerce / Product Catalog**
Requires maximum product clarity with only subtle organic grounding.
- `Skin Pores`: 0.5
- `Fabric Wrinkles`: 0.2
- `Lens Imperfections`: 0.0
- `Film Grain`: 0.0
- `Dust`: 0.0

## 3. Core Ontology Structure

```yaml
Cinematic Imperfections
├── Subject Imperfections
│   ├── Skin (Pores, Peach Fuzz, Natural Oil, Subsurface Scattering)
│   ├── Hair (Flyaways, Stray Strands)
│   └── Styling (Fabric Micro-wrinkles, Uneven Drapes)
├── Material Imperfections
│   ├── Metal (Micro-scratches, Oxidation, Imperfect Polish)
│   └── Architecture (Weathered Stone, Chipped Carvings)
├── Atmospheric Imperfections
│   ├── Dust Particles
│   ├── Natural Haze / Fog
│   └── Bloom
└── Optical Imperfections
    ├── Film Grain
    ├── Lens Flare / Halation
    ├── Chromatic Aberration
    └── Lens Breathing / Soft Edges
```

## 4. Usage in the Pipeline
The `Image Formation Intelligence` (Decision Engine) retrieves the designated Authenticity Profile for the requested Vibe and passes these specific, weighted imperfections as absolute directives to the Prompt Compiler.
