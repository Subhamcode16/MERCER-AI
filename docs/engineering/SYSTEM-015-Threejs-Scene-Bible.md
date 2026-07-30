# SYSTEM-015 — Three.js Scene Bible
**Layer:** Engineering Intelligence (Build)
**Agent:** `system-architect`
**Movement:** I — The Threshold

---

## 1. Core Framework
- We utilize **React Three Fiber (R3F)** to bridge declarative React state with the imperative Three.js scene graph.
- The `Canvas` must be positioned as a fixed background layer `(z-index: -1)` spanning `100vw` and `100vh`.

## 2. Scene Graph Hierarchy
```text
Scene
 ├── Lighting Rig (Environment + Directional)
 ├── The Architecture (Limestone Group)
 ├── The Silk (InstancedMesh or highly optimized SkinnedMesh)
 └── The Camera (Driven by GSAP ScrollTrigger)
```

## 3. Rendering & Post-Processing
- **Renderer:** `powerPreference: "high-performance"`, `antialias: false` (we use post-processing AA).
- **Post-Processing Stack:**
  1. **SMAA** (Subpixel Morphological Antialiasing) - Essential for cinematic edges.
  2. **Subtle Bloom** - Threshold 0.9, Intensity 0.2. Only triggers on the Silk's specular highlights.
  3. **Depth of Field (DOF)** - Dynamically controlled by the camera's Z-position to focus the eye.

## 4. Asset Loading
- All heavy assets (HDRI, `.glb` models) must be preloaded via `useGLTF.preload()` before the first frame is rendered. No pop-in is acceptable.
