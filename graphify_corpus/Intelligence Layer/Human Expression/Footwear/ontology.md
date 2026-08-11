# Ontology: Footwear

This document defines the vocabulary, taxonomy, and core semantic relationships for the Footwear sub-domain under `Human Expression`.

---

## 1. Domain Vocabulary
- **Vamp**: The front part of the shoe upper, covering the toes and instep. Highly susceptible to folding creases during walking.
- **Sole**: The bottom of the shoe, consisting of the midsole (cushioning) and outsole (tread/grip).
- **Heel**: The back bottom support, dictating the ankle tilt and stance of the model.
- **Aglet**: The metallic or plastic tip of a shoelace.
- **Ground Contact Shadow**: The high-density ambient occlusion shadow cast directly under the sole where it touches the floor.
- **Symmetry**: The structural matching of eyelets, panels, and patterns between the left and right shoes.

---

## 2. Core Taxonomy

### A. Material Classes
- **Polished Leather**: Fine calf leather, patent leather, high-specular gloss, narrow highlights.
- **Suede / Nubuck**: Matte pile texture, directional grain shifting under touch (light/dark variation).
- **Athletic Knit / Mesh**: Highly porous, woven thread micro-texture, diffuse matte finish.
- **Rubber / Synthetics**: Vulcanized rubber, EVA foam soles, flat semi-gloss finish.

### B. Footwear Categories
- **Formal**: Oxford dress shoes, Derby shoes, Chelsea boots, Loafers.
- **Athletic**: Running sneakers, Basketball shoes, Training footwear.
- **Lifestyle / Casual**: Canvas low-tops, sandals, boots.
- **High-Heeled**: stilettos, pumps, wedges.

### C. Construction Parts
- **Upper Elements**: Tongue, Eyelets, Laces, Collar, Heel counter.
- **Sole Elements**: Tread grooves, lugs, sidewall, stitching line (Welting).

---

## 3. Relationships & Rules

- `(Shoe: Oxford Dress Shoe) -[REQUIRES]-> (Material: Polished Leather)`
- `(Shoe: running Sneaker) -[REQUIRES]-> (Material: Athletic Knit OR Nylon)`
- `(Material: Suede) -[REQUIRES]-> (SurfaceReflectance: Matte Pile Grain Shift)`
- `(Material: Polished Leather) -[REQUIRES]-> (SurfaceReflectance: Narrow Specular Highlight)`
- `(State: Sitting OR Walking) -[REQUIRES]-> (GarmentConstraint: Ground Contact Shadow)`
