---
VIS-ID: VIO-006
Title: Domain Ontology (Fashion & Textiles)
Version: 1.0.0
Status: Draft
Owner: Visual Intelligence Research
Last Updated: 2026-07-01
Depends On:
  - VIO-001
  - VIO-005
---

# VIO-006: Domain Ontology (Fashion & Textiles)

## Purpose
The **Domain Ontology** extends the Universal Ontology (`VIO-005`) into a specific, highly proprietary industry. 

`VIO-006` is the specialized schema for the Fashion and Textile industry (specifically focusing on South Asian garments like the Saree and Lehenga). This is where the platform's unique competitive advantage lives.

---

## 1. Fashion Entities & Attributes

This ontology defines the strict terminology and hierarchies required to understand textiles.

### Garment
- **Types:** Saree, Lehenga, Kurti, Dupatta, Sherwani.
- **Attributes:** Silhouette, Cut, Era, Formality.

### Fabric & Material
- **Types:** Silk, Cotton, Georgette, Chiffon, Organza, Velvet, Brocade.
- **Attributes:** Weight (Heavy, Light), Sheerness (Opaque, Translucent), Texture (Matte, Glossy, Rough).

### Weave & Technique
- **Types:** Banarasi, Kanjeevaram, Chanderi, Ikat, Jamdani.
- **Attributes:** Motif Density, Zari (Gold, Silver, Copper), Loom Type.

### Embellishment (Surface Detailing)
- **Types:** Zardosi, Gota Patti, Mirror Work, Thread Embroidery, Sequins, Beads.
- **Attributes:** Coverage (Heavy, Border-only, Scattered), Motif (Floral, Geometric, Paisley).

### Drape & Styling
- **Types:** Nivi, Gujarati, Bengali, Nauvari.
- **Attributes:** Pallu Placement, Pleat Density, Fall.

---

## 2. Proprietary Relationships

The Domain Ontology allows the system to construct semantic relationships that a generic AI model cannot understand.

- `(Fabric: Kanjeevaram) -[REQUIRES]-> (Weave: Pure Mulberry Silk)`
- `(Garment: Banarasi Saree) -[INCOMPATIBLE_WITH]-> (Drape: Modern Pre-stitched Gown)`
- `(Embellishment: Heavy Zardosi) -[RESTRICTS]-> (Fabric: Chiffon)` *Reason: Chiffon cannot support the weight of heavy Zardosi.*

---

## 3. The Visual Intelligence Factory (VIF)
During the manufacturing pipeline (`RES-001`), Domain concepts are extracted by highly specialized, fine-tuned models at **Station 3: Fashion Parsing** and **Station 5: Creative Semantics**. 

If the system processes an image and detects a "Red Saree," the factory pipeline uses this ontology to decompose it further into `(Color: Crimson) -> (Garment: Saree) -> (Weave: Banarasi) -> (Motif: Floral Zari)`.
