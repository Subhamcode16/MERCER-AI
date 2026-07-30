---
Title: Material Intelligence Ontology
ID: VIO-010
Status: Draft
---

# VIO-010: Material Intelligence

This ontology moves the platform beyond naming textiles (e.g., "Banarasi Silk") and into modeling the physical and optical properties of materials. It ensures that the Image Formation Engine has access to the true physical constraints of a garment.

## 1. Domain Purpose

To model the physical behavior, light reflectance, drape, and textural properties of textiles and embellishments, utilizing a rigorous three-layer knowledge pipeline to prevent hallucinations and separate ground truth from stylistic trends.

## 2. The Three-Layer Knowledge Pipeline

The ontology structure strictly segregates material knowledge into three distinct hierarchical layers:

### Level 1: Physical Truth (Immutable)
Ground truth data derived from material science, textile engineering, and empirical measurement. 
*Example:* 
- `Material: Silk`
- `Surface: Semi-Gloss`
- `Light Transmission: Low`
- `Reflectance Model: Anisotropic`
- `Fold Behavior: Heavy/Structured`

### Level 2: Expert Practice (Heuristics)
Domain-specific knowledge provided by fashion designers, textile experts, and luxury photographers on how the material behaves under specific conditions.
*Example:* 
- `Banarasi gold zari looks richer under directional grazing light.`
- `Avoid flat front-lighting on velvet as it destroys micro-contrast.`

### Level 3: Observed Statistics (Patterns)
Data-driven probabilities mined by the Visual Intelligence Factory (VIF) from thousands of real-world campaigns.
*Example:* 
- `92% of high-end Banarasi campaigns utilize warm side lighting.`
- `70% of luxury editorial silk shots use shallow depth of field to emphasize drape.`

## 3. Core Ontology Structure

```yaml
Material Intelligence
├── Optical Properties
│   ├── Surface Finish (Matte, Semi-Gloss, High-Gloss)
│   ├── Reflectance Model (Isotropic, Anisotropic)
│   ├── Light Transmission (Opaque, Translucent, Sheer)
│   └── Specular Width (Narrow, Broad)
├── Structural Physics
│   ├── Drape Physics (Fluid, Structured, Stiff)
│   ├── Fold Behavior (Soft, Heavy, Crisp)
│   └── Edge Stiffness (Low, Medium, High)
└── Micro-Texture
    ├── Thread Density (Low, Medium, High)
    ├── Micro Wrinkle Pattern (Fine, Broad, None)
    └── Embellishment Profile (e.g., Metallic Yarn, Zari)
```

## 4. Usage in the Decision Engine
The Decision Engine retrieves `Level 1` and `Level 2` data as absolute constraints. `Level 3` data is used as a probabilistic guide for generating alternative creative approaches when the Vibe is under-specified.
