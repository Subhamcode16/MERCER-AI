# Atelier OS: Brand & Design Guidelines

This living document serves as the absolute source of truth for the visual identity, tone, typography, and motion design of the Atelier Visual Intelligence Operating System. Any future pages, components, or redesigns MUST adhere to these principles to maintain the premium, cinematic experience established in World I.

---

## 1. Core Philosophy
- **Cinematic & Monumental:** The interface should feel like a high-end film or a physical art installation.
- **Silent Authority:** Minimal copy. Extreme negative space. No visual clutter. 
- **Physicality:** UI elements should react like physical glass or light. Motion should follow real-world physics (springs, fluid glares, magnetic pulls).
- **Dark Mode Native:** Deep blacks (`#000000`) dominating the canvas, pierced by warm, cinematic light.

## 2. Typography
Typography is the backbone of the UI. It relies on extreme contrast between massive serif headers and tiny, widely-tracked sans-serif micro-labels.

### Font Stacks
- **Serif (Headings):** `"Playfair Display", ui-serif, Georgia, serif`
- **Sans-Serif (Body & UI):** `ui-sans-serif, system-ui, sans-serif`

### Hierarchy & Usage
- **Micro-Labels (Eyebrows/Tags):** 
  - `text-[12px] tracking-[0.28em] font-medium uppercase opacity-70`
  - Color: `#E1D4C0` (Warm Ivory) or White.
- **Monumental Headings:** 
  - `font-serif font-bold text-[72px] lg:text-[88px] leading-[0.95]`
  - Always use tight leading (`leading-[0.95]`) to make the massive text feel cohesive.
- **Body Text:**
  - `text-[15px] leading-[1.8] opacity-90`
  - Clean, breathable, high line-height.

## 3. Color Palette
The palette is hyper-restricted to let the video/image content shine.
- **Canvas / Background:** `#000000` (Pure Black)
- **Primary Text:** `#FFFFFF` (Pure White) with varying opacities (`opacity-70`, `opacity-90`).
- **Accent / Warmth:** `#E1D4C0` (Warm Ivory) used sparingly for micro-labels or glowing accents.
- **Borders / Separators:** `rgba(255,255,255,0.05)` to `rgba(255,255,255,0.2)` max.

## 4. UI Components (Liquid Glass)
Buttons, cards, and containers should rarely be solid blocks. They must simulate physical glass.
- **Backgrounds:** `bg-white/5`
- **Borders:** Ultra-subtle hairline borders `border border-white/20`.
- **Blur:** High backdrop blurs (`backdrop-blur-xl` or `backdrop-blur-[24px]`).
- **Glows:** Internal and external ambient glows using box-shadows.
  - *Example:* `shadow-[0_0_20px_rgba(255,255,255,0.0),_inset_0_0_10px_rgba(255,255,255,0.1)]`

## 5. Motion & Interaction (GSAP)
No basic CSS hovers. All interactions must be choreographed using GSAP.
- **Theatrical Entrances:** Elements should never instantly snap onto the screen. Use long fades (`1.5s` to `2.5s`) and slight drifts (`y: 20` to `y: 0`).
- **Fluid Hover States:** When interacting with glass, it should distort. Use stretching padding, sweeping light glares, and spring physics (`ease: 'back.out(1.5)'`) for inner icons.
- **Ambient Life:** UI should feel alive even when idle. Use 4-second looping CSS pulses (`animate-pulse`) for ambient glows behind CTAs.
- **Crossfades / Dissolves:** Avoid hard cuts. Use long crossfades (minimum `0.8s`) for transitions.

## 6. Layout & Framing
- **Absolute Centering:** When in doubt, center it.
- **Cinematic Letterboxing:** For monumental video/image reveals, constrain the aspect ratio to `2.76:1` (Ultra Panavision) or `2.35:1` to create thick, dramatic black bars.
- **Negative Space:** Give text massive breathing room. Never cram elements.

---
*Reference these principles before drafting any new sections (e.g., Pricing, Contact, Footer).*
