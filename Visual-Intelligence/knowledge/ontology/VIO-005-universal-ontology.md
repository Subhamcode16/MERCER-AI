---
VIS-ID: VIO-005
Title: Universal Ontology
Version: 1.0.0
Status: Draft
Owner: Visual Intelligence Research
Last Updated: 2026-07-01
Depends On:
  - VIO-001
---

# VIO-005: Universal Ontology

## Purpose
The **Universal Ontology** defines the foundational layer of visual intelligence. It captures the concepts that exist in *every* visual medium, regardless of the industry or subject matter. 

Whether the system is analyzing a fashion editorial, an architectural rendering, or a food photography shoot, the concepts in this ontology remain constant.

---

## 1. Universal Entities

The Universal Ontology dictates the following core Entities:

### Lighting
- **Attributes:** Intensity, Direction (Front, Back, Side, Top), Quality (Hard, Soft), Color Temperature, Contrast Ratio.
- **Constraints:** A single light source cannot be simultaneously Hard and Soft.

### Composition
- **Attributes:** Rule of Thirds, Symmetry, Leading Lines, Framing, Negative Space, Balance.
- **Relationships:** Subject -[POSITIONED_AT]-> Intersection.

### Camera (Lens & Perspective)
- **Attributes:** Focal Length (e.g., 35mm, 85mm), Aperture (Depth of Field), Angle (Low, High, Eye-Level), Aspect Ratio.

### Color & Mood
- **Attributes:** Palette (Monochromatic, Analogous, Complementary), Saturation, Brightness, Emotion (e.g., Melancholic, Energetic, Regal).

### Environment (Space)
- **Attributes:** Indoor, Outdoor, Studio, Natural, Urban, Abstract.

---

## 2. Interaction with Domain Ontologies

The Universal Ontology cannot exist in isolation. It provides the **canvas** upon which a Domain Ontology (e.g., `VIO-006 Fashion`) places its specific subjects.

**Example of Merged Intelligence:**
- *Universal Concept:* Soft side-lighting with a shallow depth of field (85mm).
- *Domain Concept (Fashion):* Banarasi Silk Saree with Zari embroidery.
- *Merged Result:* The soft lighting highlights the metallic texture of the Zari weaving while the shallow depth of field isolates the drape from the background.

---

## 3. The Visual Intelligence Factory (VIF)
During the manufacturing pipeline (`RES-001`), Universal concepts are typically extracted by foundational vision and photography models (e.g., CLIP, Depth Anything) at **Station 4: Photography Analysis**, entirely independent of the fashion-parsing models running at Station 3.
