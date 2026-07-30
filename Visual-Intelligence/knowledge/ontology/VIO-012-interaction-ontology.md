---
Title: Interaction Ontology
ID: VIO-012
Status: Draft
---

# VIO-012: Interaction Ontology

This ontology represents the ultimate evolution of the Visual Intelligence architecture. Instead of merely storing static objects and properties, the Interaction Ontology models **cause and effect**. It allows the system to reason like a master cinematographer by understanding how physical entities influence one another within a scene.

## 1. Domain Purpose

To model the relational physics and optical interactions between separate semantic domains (e.g., Material × Lighting, Camera × Environment).

## 2. Core Concept: The Interaction Tuple

Every node in this ontology is defined by an interaction tuple:
`[Entity A] × [Entity B] WHEN [Condition] -> PRODUCES [Effect] -> REQUIRES [Action]`

### Example 1: Material × Lighting
**Entity A:** Banarasi Silk (Material)
**Entity B:** Light Source (Lighting)
**Condition:** Hard Key Light
**Produces:** Specular Clipping and loss of Zari micro-contrast
**Action:** AVOID. Soften key light or use large bounce.

### Example 2: Material × Lighting
**Entity A:** Velvet (Material)
**Entity B:** Light Source (Lighting)
**Condition:** Flat Front-Lighting
**Produces:** Complete loss of texture (appears as a solid color block)
**Action:** AVOID. Require Edge/Rim lighting for separation.

### Example 3: Camera × Environment
**Entity A:** 85mm Lens (Camera)
**Entity B:** Small Studio (Environment)
**Condition:** Distance to subject < 3 meters
**Produces:** Inability to capture full-body drape
**Action:** AVOID full-body composition. Enforce Portrait/Close-up composition.

## 3. The Interaction Matrix

The ontology maps the following core cross-domain relationships:

- `Material × Lighting`: How fabrics reflect, absorb, and scatter specific light qualities.
- `Lighting × Camera`: How exposure, contrast ratios, and lens flares interact.
- `Camera × Lens`: The relationship between sensor size, focal length, and perceived compression.
- `Pose × Garment`: How the physical stiffness/fluidity of a garment dictates valid model poses.
- `Movement × Fabric`: How materials behave in motion (e.g., Chiffon floats, heavy Banarasi structures).
- `Skin × Color Grade`: How specific palettes interact with subsurface skin rendering.

## 4. Usage in the Pipeline (Constraint Solver)
These interaction nodes act as mathematical constraints within the **Image Formation Intelligence** engine (`ARC-001`). When the system attempts to assemble a visual mandate, it checks the Interaction Ontology to ensure that the chosen Lighting does not catastrophically conflict with the chosen Material.
