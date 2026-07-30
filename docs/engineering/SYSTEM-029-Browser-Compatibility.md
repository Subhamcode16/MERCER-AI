# SYSTEM-029 — Browser Compatibility
**Layer:** Engineering Intelligence (Build)
**Agent:** `system-architect`
**Movement:** I — The Threshold

---

## 1. WebGL 2.0
- WebGL 2.0 is strictly required for advanced features (e.g., multi-sample render targets, specific shader instructions). 
- If WebGL 2.0 is unsupported, the visitor is served a cinematic 2D video loop instead of the interactive 3D scene.

## 2. Mobile Safari (iOS) Limits
- iOS Safari has aggressive memory limits (often killing tabs that exceed 300MB of RAM).
- We employ aggressive texture downscaling on iOS (limiting `devicePixelRatio` to `Math.min(window.devicePixelRatio, 1.5)`).

## 3. Graceful Degradation
- **Tier 1 (High-End Desktop):** Full shadows, post-processing stack (SMAA, Bloom, DOF), 2K textures.
- **Tier 2 (Mid-Tier / Standard Mobile):** Hard shadows, no DOF, 1K textures.
- **Tier 3 (Low-End Mobile):** No dynamic shadows, baked lighting only, no post-processing.
