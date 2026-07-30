# Ontology: Sarees (Fashion & Textiles)

This document defines the specialized taxonomy, vocabulary, and relationships for the Saree intelligence module under the `Human Expression` domain.

---

## 1. Domain Vocabulary
- **Pallu**: The decorative, loose end of the saree, draped over the shoulder. It is the focal point of design and storytelling.
- **Border**: The woven edge running along the entire length of the saree. Often contrasts in color and design with the body.
- **Body**: The main central panel of the saree.
- **Zari**: Metallic thread (traditionally real gold/silver wrapped around silk, modernly metallic polyester) used to weave intricate patterns.
- **Pleats**: Folds tucked at the waist (typically 5-8 pleats in the Nivi drape) to allow movement.
- **Loom Type**: Handloom (artisanal, contains characteristic irregularities) vs. Powerloom (mass-produced, uniform).

---

## 2. Core Taxonomy

### A. Fabric Bases (Raw Materials)
- **Silk**: Mulberry Silk, Muga Silk, Tussar Silk, Raw Silk.
- **Cotton**: Handspun Khadi, Fine Mulmul, Mercerized Cotton.
- **Lightweight/Sheer**: Georgette, Chiffon, Organza, Tissue.
- **Heavy Pile**: Velvet.

### B. Weaving & Production Techniques
- **Banarasi Brocade**: Heavy silk with metallic zari motifs, originating from Varanasi.
- **Kanjeevaram / Kanjivaram**: Extremely heavy mulberry silk with interlocked borders (Korvai), originating from Tamil Nadu.
- **Chanderi**: Lightweight semi-translucent silk-cotton blend from Madhya Pradesh.
- **Ikat**: Resist-dyed geometric pattern where yarn is dyed before weaving, leaving characteristic feathered edges.
- **Dupion**: Slub-woven silk with irregular thickness in the weft and two-tone iridescent properties.
- **Block Print**: Hand-stamped patterns (e.g., Sanganeri, Ajrakh, Bagru) with organic misalignments.

### C. Embellishments & Surface Detailing
- **Zardosi**: Ornate three-dimensional metallic embroidery using gold/silver threads, sequins, and beads.
- **Gota Patti**: Metallic ribbon applique work, traditionally from Rajasthan.
- **Aari Work**: Fine hook embroidery creating delicate, chain-stitch patterns.

### D. Drapes & Presentation Styles
- **Nivi**: The standard modern drape (pleats tucked in front, pallu over left shoulder).
- **Gujarati / Seedha Pallu**: Pallu draped from back to front over the right shoulder.
- **Bengali**: Pleatless drape wrapped around the body with a heavy key/focal element on the pallu.
- **Nauvari**: Nine-yard trouser-like drape traditional to Maharashtra.

---

## 3. Optical & Material Behavior Taxonomies

### A. Optical Properties
- **Surface Finish**: Anisotropic Semi-Gloss (Silk), Fully Matte (Khadi, Cotton), High Gloss (Kanjeevaram), Iridescent (Dupion), High-Gloss Metallic (Zari).
- **Light Transmission**: Fully Opaque (Velvet, heavy Silk), Semi-Translucent (Chanderi, Georgette), Highly Translucent (Chiffon, Organza, Net).

### B. Structural Physics
- **Drape Stiffness**: Very High (Kanjeevaram), High (Banarasi), Semi-Structured (Raw Silk, Dupion, Organza), Fluid (Chiffon, Georgette, Net), Relaxed (Khadi).
- **Crease Retention**: High Creasing (Khadi, Cotton), Low Creasing (Synthetics, Heavy Silks).

---

## 4. Semantic Relationships & Rules

- `(Fabric: Banarasi Brocade) -[REQUIRES]-> (Weave: Pure Mulberry Silk)`
- `(Fabric: Kanjeevaram) -[REQUIRES]-> (Drape: Structured Stiff Folds)`
- `(Embellishment: Heavy Zardosi) -[INCOMPATIBLE_WITH]-> (Fabric: Chiffon)`  
  *Rule: Weight limits forbid heavy embroidery on sheer bases to prevent tearing.*
- `(Weave: Ikat) -[REQUIRES]-> (Pattern: Blurred/Feathered Edges)`
- `(Fabric: Velvet) -[REQUIRES]-> (Reflectance: Pile-Directional Luminosity Gradient)`
- `(Occasion: Bridal Kanjeevaram) -[REQUIRES]-> (Accessory: Temple Jewelry)`
