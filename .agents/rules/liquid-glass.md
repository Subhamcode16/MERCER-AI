---
trigger: always_on
---

# Liquid Glass Design System Rule

Whenever "Liquid Glass" or glassmorphism UI design is requested, ALWAYS implement the **authentic iOS 18 Control Center Liquid Glass specification**:

1. **Frosted Translucent Background**: `rgba(255, 255, 255, 0.22)` to `0.28` with heavy blur (`backdrop-blur-[40px] saturate-[190%]`).
2. **Sharp 1px White Specular Rim**: `border: 1px solid rgba(255, 255, 255, 0.65)`.
3. **Dual Inner Bevel Refraction**: `box-shadow: inset 0 1px 1.5px rgba(255, 255, 255, 0.85), inset 0 -1px 1px rgba(255, 255, 255, 0.20), 0 12px 36px rgba(0, 0, 0, 0.14)`.
4. **Circular Sub-Badges**: Icons/buttons inside glass cards must sit within circular frosted sub-capsules (`rounded-full bg-white/28 border-white/75`).
5. **Pure White High-Contrast Typography**: Crisp white text (`#ffffff`) with subtle text drop-shadow (`drop-shadow-sm`).
6. **NEVER use opaque, dark green/grey, or flat glassmorphism**.
