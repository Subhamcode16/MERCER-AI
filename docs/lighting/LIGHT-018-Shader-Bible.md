# LIGHT-018 — Shader Bible
**Layer:** Creative Intelligence (Think)
**Agent:** `lighting-director`
**Movement:** I — The Threshold

---

## 1. The Silk Shader (Custom GLSL)
- **Base:** Physically Based Rendering (PBR).
- **Subsurface Scattering (SSS):** Crucial for the silk. Light must bleed through the fabric when back-lit. 
- **Iridescence:** A micro-layer of iridescence mapped to the Fresnel effect. As the normals face away from the camera, a subtle gold/bronze tint appears.

## 2. The Architecture Shader
- **Base:** Matte rough limestone.
- **Micro-bump:** High-frequency noise texture to break up specular highlights. It must feel dusty and ancient.
- **Specular:** Almost zero. 

## 3. Atmosphere & Volumetrics
- The scene is filled with a distance-based fog.
- **Fog Color:** `#0a0a0a` at the camera, bleeding to `#1a1918` at the far clipping plane.
- **Density:** Exponential squared (`exp2`). 

## 4. Anti-Aliasing
- SMAA (Subpixel Morphological Antialiasing) is required. Jagged geometry edges will immediately ruin the cinematic immersion.
