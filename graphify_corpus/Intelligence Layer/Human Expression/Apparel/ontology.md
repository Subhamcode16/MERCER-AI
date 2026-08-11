# Ontology: Apparel

This document defines the vocabulary, taxonomy, and core semantic relationships for the general and western Apparel sub-domain under `Human Expression`.

---

## 1. Domain Vocabulary
- **Seams**: The join line where two or more pieces of fabric are sewn together. A critical indicator of physical garment construction in visual renders.
- **Drape**: The way a fabric hangs or falls on a three-dimensional form (fluid, cascading, rigid, boxy).
- **Hems**: The finished edge of the garment (sleeves, skirt bottoms, shirt tails).
- **Wrinkle Propagation**: The organic distribution of creases and wrinkles around joint bending areas (elbows, knees, hips).
- **Silhouette**: The overall outline or shape of a garment (A-line, sheath, tailored, oversized).

---

## 2. Core Taxonomy

### A. Fabric Bases & Material Classes
- **Rigid/Structured Weaves**: Denim, Heavy Wool, Tweed, Heavy Cotton Twill.
- **Drape-Friendly/Fluid Weaves**: Satin, Crepe, Knit jersey, Viscose.
- **Crease-Prone Fibers**: Linen, 100% Cotton.
- **Elastic/Stretch Fabrics**: Spandex, Rib-knit, Compression activewear.

### B. Garment Categories
- **Tops**: T-Shirts, Button-down shirts, Blouses.
- **Bottoms**: Jeans, Chinos, Tailored trousers, Skirts.
- **Outerwear**: Overcoats, Denim jackets, Blazers, Leather jackets.
- **Full-Body**: Contemporary dresses, Jumpsuits, Suits.

### C. Construction & Seam Elements
- **Stitching**: Flatlock stitching (activewear), Double-needle stitching (denim/casual), Blind hems (formal suits).
- **Details**: Collars (ribbed, button-down), Cuffs, Plackets, Pockets (patch, welt).

---

## 3. Relationships & Rules

- `(Fabric: Heavy Denim) -[REQUIRES]-> (Stitching: Double-Needle Seams)`
- `(Fabric: Linen) -[REQUIRES]-> (WrinkleBehavior: High Joint Creasing)`
- `(Fabric: Spandex Activewear) -[INCOMPATIBLE_WITH]-> (WrinkleBehavior: Loose Sagging Folds)`
- `(Garment: Tailored Suit) -[REQUIRES]-> (ShoulderProfile: Padded Structured Seam)`
- `(Garment: Oversized Hoodie) -[REQUIRES]-> (Drape: Sagging Dropped Shoulder)`
