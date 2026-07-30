# REACT-016 — React Architecture
**Layer:** Engineering Intelligence (Build)
**Agent:** `react-architect`
**Movement:** I — The Threshold

---

## 1. Component Philosophy
React is used exclusively for state management and layout orchestration. It is not used to render heavy DOM nodes. 
- **The Golden Rule:** The DOM must remain as sparse as possible.

## 2. Server vs. Client Components (Next.js)
- **Server Components:** Used for the outer page wrappers, metadata, and static HTML scaffolding.
- **Client Components:** The WebGL Canvas, GSAP orchestration wrappers, and the dynamic UI layer MUST be Client Components (`"use client"`).

## 3. State Management
- **Local State:** `useState` is forbidden for animation values. It triggers React reconciliations which cause dropped frames.
- **Global State:** We use **Zustand** for transient UI states (e.g., `isScrollLocked`, `currentPhase`).
- **Animation State:** Managed entirely outside React via `useRef` and GSAP.

## 4. Context Isolation
- The WebGL context and the DOM context are bridged using Zustand. Do not pass props deep into the Three.js tree from the DOM; let the components subscribe to the Zustand store directly.
