# Ontology: Jewelry

This document defines the vocabulary, taxonomy, and core semantic relationships for the Jewelry sub-domain under `Human Expression`.

---

## 1. Domain Vocabulary
- **Refractive Index (RI)**: An optical measurement of how much light bends when entering a gemstone. High RI creates visual brilliant depth.
- **Dispersion (Fire)**: The optical splitting of white light into its spectral rainbow colors when exiting gemstone facets.
- **Reflection Mapping**: The mirror-like reflection of surrounding environment geometries (studio flags, soft boxes) on polished metal surfaces.
- **Facet**: The flat polished surfaces cut onto a gemstone to refract and reflect light.
- **Prong**: The micro-claws holding a gemstone in place.
- **Macro Depth of Field**: A photographic term where background and foreground objects collapse into creamy bokeh, isolating a tiny jewelry piece in sharp focus.

---

## 2. Core Taxonomy

### A. Precious Metals
- **Polished Gold**: High gloss, rose/yellow tint, mirror-like specular reflections.
- **Platinum / White Gold**: Neutral specular reflection tint, high gloss, extreme reflection mapping.
- **Brushed/Satin Metals**: Diffuse reflection, satin sheen, micro-brushed texture.

### B. Gemstone Optics
- **High-Refraction (Diamond)**: Sharp facets, high dispersion (rainbow fire highlights), high transparency.
- **Colored Refractive (Emerald, Ruby, Sapphire)**: Subsurface refraction, light absorption (rich saturated color centers).
- **Lustrous Nacre (Pearl)**: Semi-translucent, soft iridescent surface sheen.

### C. Jewelry Categories
- **Rings**: Solitaires, wedding bands, halo rings.
- **Necklaces**: Pendants, collars, chains.
- **Earrings**: Studs, drop earrings, hoops.
- **Fine Timepieces**: Dial details, bezel geometry, strap/metal bracelet textures.

---

## 3. Relationships & Rules

- `(Gemstone: Diamond) -[REQUIRES]-> (Optics: High Refraction AND Rainbow Dispersion)`
- `(Metal: Polished Gold) -[REQUIRES]-> (Optics: Reflection Mapping)`
- `(Garment: Ring OR Earring) -[REQUIRES]-> (Camera: Macro Lens AND Shallow DOF)`
- `(Lighting: Fresnel Spot) -[REQUIRES]-> (Optics: Gemstone Facet Sparkle)`
- `(Setting: Pavé) -[REQUIRES]-> (Construction: Micro Prong Symmetrical Alignment)`
