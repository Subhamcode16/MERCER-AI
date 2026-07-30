# DIRECTOR-013 — Camera Blocking Bible
**Layer:** Creative Intelligence (Think)
**Agent:** `cinematic-director`
**Movement:** I — The Threshold

---

## 1. Movement Axis
- The primary camera movement is **Z-axis translation** (pushing in).
- Secondary movement is a slight **Y-axis elevation** (rising up to reveal scale).
- **X-axis** panning is strictly prohibited. The visitor moves *forward* into the institution, not sideways.

## 2. Scroll-Linked Physics
- The camera position is mapped to the scroll progress (0.0 to 1.0).
- **Easing:** Expo.easeOut. The camera must carry inertia. When the user stops scrolling, the camera should drift to a halt over 1.5 seconds. It must never stop instantly.

## 3. LookAt Target
- The camera's `LookAt` vector remains locked to the center mass of the Silk.
- Even as the camera pushes forward, the framing smoothly tracks the organic movement of the fabric.
