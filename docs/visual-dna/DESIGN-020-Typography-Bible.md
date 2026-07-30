# DESIGN-020 — Typography Bible
**Layer:** Creative Intelligence (Think)
**Agent:** `design-system-guardian`
**Movement:** I — The Threshold

---

## 1. Typefaces
- **Primary (Display):** *PP Editorial New* (or equivalent high-contrast elegant serif). Used for the core message and titles.
- **Secondary (Utility):** *Inter* (or equivalent geometric sans-serif). Used for small metadata, navigation, and loading states.

## 2. Weight and Sizing
- **H1 (The Core Message):** 4rem - 6rem. Weight: Light (300).
- **Body / Nav:** 0.75rem. Weight: Regular (400). Uppercase, tracking wide (0.1em).

## 3. Color and Opacity
- We never use pure white (`#FFFFFF`). It is too aggressive for the eye.
- **Max Brightness:** `#E6E4E0` (Warm bone white).
- **Fade States:** Text enters at 0% opacity, holds at 10% for a beat, then smoothly glides to 85% opacity.

## 4. The Engraving Principle
- Text must feel like it belongs in the environment. 
- We use `mix-blend-mode: overlay` or `plus-lighter` on large serif titles so the light of the 3D scene beneath interacts with the letterforms.
