# PROD-025 — Development Task Breakdown
**Layer:** Production Intelligence (Translate)
**Agent:** `repository-architect`
**Movement:** I — The Threshold

---

## Sprint 1: The Foundation
- [ ] Initialize Turborepo / Next.js scaffolding.
- [ ] Set up React Three Fiber `Canvas` with global Zustand store.
- [ ] Configure strict ESLint and Prettier rules.
- [ ] Implement asset preloader (fonts, HDRIs, GLB placeholders).

## Sprint 2: Modular World Building (Environment Assets)
- [ ] Generate concept frame & build `<ThresholdHall />` module.
- [ ] Generate concept frame & build `<SilkInstallation />` module.
- [ ] Generate concept frame & build `<StoneWall />` module.
- [ ] Generate concept frame & build `<Skylight />` module.
- [ ] Generate concept frame & build `<BronzeDetail />` module.
- [ ] Generate concept frame & build `<Floor />` module.
- [ ] Generate concept frame & build `<Door />` module.

## Sprint 3: Experience Composition
- [ ] Choreograph the camera path through the modular environment.
- [ ] Map lighting interaction (Spotlight tracking) to the timeline.
- [ ] Connect `gsap.timeline` to native window scroll.
- [ ] Sync GSAP ticker with R3F `useFrame` for physics-based movement.

## Sprint 4: The Interface Layer
- [ ] Build the DOM overlay layer (Z-index: 10).
- [ ] Implement `PP Editorial New` typography components.
- [ ] Map text opacity fades to the final 15% of the scroll timeline.
- [ ] Implement 2-second velocity check to reveal navigation.

## Sprint 5: Polish & Performance
- [ ] Apply Post-Processing stack (SMAA, Bloom, DOF).
- [ ] Run assets through KTX2 / Draco compression pipelines.
- [ ] Audit memory leaks (`dispose()` verification).
- [ ] Test on iOS Safari to verify 300MB memory limit compliance.
