# UI-028 — Accessibility Bible
**Layer:** Engineering Intelligence (Build)
**Agent:** `experience-architect`
**Movement:** I — The Threshold

---

## 1. Prefers-Reduced-Motion
- If the OS requests `prefers-reduced-motion`, the heavy Z-axis camera pushes are disabled.
- Instead, the sequence relies on slow, elegant opacity crossfades. The user still scrolls, but the jarring 3D motion is neutralized to prevent motion sickness.

## 2. Screen Readers (ARIA)
- The WebGL `<canvas>` must have `aria-hidden="true"`. It is completely invisible to screen readers.
- A hidden DOM layer exists purely for screen readers, providing a narrative description of the scene as the user scrolls.
- Example: `<div aria-live="polite" class="sr-only">The environment shifts as heavy silk drapes across ancient limestone architecture.</div>`

## 3. Contrast Ratios
- Despite the dark cinematic aesthetic, all primary typography must pass WCAG AA contrast standards (minimum 4.5:1) against the underlying WebGL canvas.
