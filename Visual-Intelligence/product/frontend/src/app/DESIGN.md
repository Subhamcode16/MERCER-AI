---
name: VYREN Brand Operating System — Daytime Meadow & Liquid Glass Design System
version: 2.0.0
aesthetic: Refractive Liquid Glass & Daylight Architectural Luxury
colors:
  sky-meadow-base: "#87a8b8"
  sky-fog-horizon: "#d8e8ea"
  sun-highlight: "#fff5db"
  grass-sunlit-tip: "#d2da7e"
  grass-deep-root: "#3d5c28"
  text-high-contrast: "#0f172a"
  text-muted-slate: "#334155"
  glass-surface-light: "rgba(255, 255, 255, 0.65)"
  glass-border-light: "rgba(255, 255, 255, 0.75)"
typography:
  editorial-serif:
    family: "var(--font-playfair)"
    weights: [400, 500]
  sans:
    family: "var(--font-inter)"
    weights: [400, 500, 600]
  mono:
    family: "monospace"
    weights: [400, 500]
---

# ❖ VYREN — Design System Specification (`DESIGN.md`)

## 1. Aesthetic Thesis & Anti-Slop Principles (`taste-skill` Review)

* **Refractive Liquid Glass (`liquid-glass-js`)**: Cards sample the underlying WebGL canvas with multi-layered light refraction (`backdrop-filter: blur(24px)`), inner bevel highlights (`inset 0 1.5px 2px rgba(255,255,255,0.95)`), and realistic drop shadows (`0 20px 50px rgba(0,0,0,0.1)`).
* **High-Contrast Editorial Typography**: High-contrast slate text (`#0f172a`) ensures maximum legibility against the daytime Meadow scene.
* **Spatial Breathing Room**: Generous padding, organic rounded corners (`rounded-3xl`), and pill-shaped interactive tabs.

---

## 2. Liquid Glass Card Specification (`liquid-glass-js`)

```css
/* Refractive Glassmorphic Card Token */
.glass-card-liquid {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.75);
  box-shadow: 
    0 20px 50px rgba(0, 0, 0, 0.10),
    inset 0 1.5px 2px rgba(255, 255, 255, 0.95);
  transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1);
}

.glass-card-liquid:hover {
  background: rgba(255, 255, 255, 0.75);
  border-color: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 
    0 25px 60px rgba(0, 0, 0, 0.14),
    inset 0 2px 3px rgba(255, 255, 255, 1);
}
```

---

## 3. Micro-Interactions & Motion Design (`gsap-skills` & `transitions-dev`)

| Trigger Event | Visual Micro-Interaction | Tactile Audio Feedback (`useTactileAudio`) |
|---|---|---|
| **Hover Tab / Button** | Scale `$1.02\times$`, lift `$-1\text{px}$`, smooth border glow | Micro glass tap (1200Hz, 8ms exponential decay) |
| **Prompt Box Focus** | Ring shadow expansion, input container opacity increase to `80%` | Warm soft sine pitch (320Hz → 440Hz ramp, 120ms) |
| **Execute Submission** | Scale active button `$0.95\times \to 1.05\times$`, icon slide right | Harmonic tri-chord swell (440Hz, 554Hz, 659Hz, 880Hz) |
| **Camera Sway** | Smooth ambient breathing sway ($12000\text{ms}$ loop) | Silent background ambiance |

---

## 4. Layout Architecture

* **Top Header Bar**: Fixed top position, glassmorphic backdrop.
  * **Far Left**: Wordmark **V Y R E N** (`font-serif`, `tracking-[0.18em]`).
  * **Far Right**: **Log In** & **Sign Up** auth controls + Tactile Audio toggle.
  * **Middle**: Clean spatial open sky (no distracting nav links).
* **Central Hero & Prompt Container**: Vertically centered max-width container (`max-w-3xl`) over 3D Meadow canvas.
* **Bottom Status Bar**: Fixed bottom overlay with system operational metrics (*AI Workforce*, *Visual DNA*, *Governance*).
