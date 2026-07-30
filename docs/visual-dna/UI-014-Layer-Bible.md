# UI-014 — UI Layer Bible
**Layer:** Creative Intelligence (Think)
**Agent:** `experience-architect`
**Movement:** I — The Threshold

---

## 1. The Glass Plane
- The UI exists on an invisible 2D plane resting above the 3D environment.
- It must never feel like standard web components (no hard boxes, no drop shadows).

## 2. Transparency and Blending
- **Backgrounds:** UI containers have 0% background opacity. We do not use cards.
- **Text Readability:** Achieved through subtle CSS background blurs (`backdrop-filter: blur(4px)`) masked purely behind the text bounding box, or through lighting attenuation in the 3D scene behind the text.

## 3. Interaction Design
- **Hover States:** No color changes on hover. Hover states trigger a slow tracking expansion (letter-spacing increases by 0.02em) and a subtle increase in opacity (0.6 to 1.0).
- **Click States:** A soft, ripple-less scale down (0.98) over 400ms.

## 4. The "No-UI" Rule
- Navigation elements are hidden until the scroll velocity hits 0 for more than 2 seconds, OR the user moves their cursor to the extreme edges of the screen.
- The environment is the interface.
