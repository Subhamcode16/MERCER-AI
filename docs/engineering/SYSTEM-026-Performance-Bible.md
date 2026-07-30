# SYSTEM-026 — Performance Bible
**Layer:** Engineering Intelligence (Build)
**Agent:** `system-architect`
**Movement:** I — The Threshold

---

## 1. The 60FPS Mandate
- The experience MUST run at a locked 60FPS on a standard M1 Mac, and at least 30FPS on mid-tier mobile devices.
- Dropping below 30FPS breaks the cinematic illusion and is considered a critical bug.

## 2. Geometry Budgets
- **Total Scene:** < 300,000 triangles.
- **The Silk:** < 50,000 triangles. Use subdivision only where the camera is close.
- **The Architecture:** heavily decimated, utilizing normal maps for detail rather than raw geometry.

## 3. Texture Compression
- Raw `.png` or `.jpg` textures are forbidden for WebGL.
- All textures MUST be compressed using **KTX2 / Basis Universal**. This reduces GPU memory overhead by 80%.
- Maximum texture resolution: 2K (2048x2048). 4K is forbidden unless it's a critical HDRI environment map.

## 4. Memory Management
- `dispose()` must be called on all Three.js Geometries and Materials when unmounting or transitioning between movements to prevent memory leaks.
