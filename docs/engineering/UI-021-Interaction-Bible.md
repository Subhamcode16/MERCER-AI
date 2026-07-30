# UI-021 — Interaction Bible
**Layer:** Engineering Intelligence (Build)
**Agent:** `experience-architect`
**Movement:** I — The Threshold

---

## 1. Pointer Events
- The Canvas layer has `pointer-events: none` unless a specific 3D mesh requires raycasting (which is rare in Movement I).
- The DOM UI layer sits above and intercepts clicks.

## 2. The Cursor
- We strictly avoid custom "follower" cursors (e.g., a trailing circle). They are a hallmark of generic Awwwards sites and detract from the cinematic gravitas.
- The default OS cursor is maintained. It disappears when the user is scrolling for more than 1 second to maximize immersion.

## 3. Event Throttling
- Window resize events must be heavily debounced (200ms) to prevent WebGL context crashing or stuttering.
- Orientation changes on mobile trigger a graceful crossfade to hide reflows.
