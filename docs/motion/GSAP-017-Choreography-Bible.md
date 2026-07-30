# GSAP-017 — Choreography Bible
**Layer:** Engineering Intelligence (Build)
**Agent:** `motion-director`
**Movement:** I — The Threshold

---

## 1. The Timeline
- The entire movement is bound to a single master `gsap.timeline({ scrollTrigger: ... })`.
- We do NOT use multiple disconnected ScrollTriggers. Everything is locked to one deterministic timeline.

## 2. Scroll Physics
- `scrub: 1.5` - This provides weight and inertia. When the user stops scrolling, the animation glides to a halt over 1.5 seconds.
- Native scrolling ONLY. We do not use scroll-jacking (e.g., Locomotive Scroll) that hijacks the browser's native wheel event. We use CSS `position: sticky` or fixed containers to keep the user in place while the native scrollbar progresses.

## 3. The Ticker Sync
- GSAP's ticker must be synchronized with Three.js's rendering loop to prevent micro-stutters.
```javascript
gsap.ticker.add((time) => {
  // Update uniforms or manually trigger render if not using R3F auto-render
});
```

## 4. Easing Curves
- `power3.inOut` for intentional, heavy movements.
- Linear easing is strictly used for the master ScrollTrigger progress to map 1:1 with user input.
