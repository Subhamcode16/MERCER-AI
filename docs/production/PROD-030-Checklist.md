# PROD-030 — Production Checklist
**Layer:** Production Intelligence (Translate)
**Agent:** `production-designer`
**Movement:** I — The Threshold

---

## Pre-Flight Requirements (Must be 100% before launch)

### Assets & Optimization
- [ ] All 3D Geometry is Draco compressed.
- [ ] All Textures are KTX2 compressed.
- [ ] Total WebGL scene polygon count is verified < 300k.
- [ ] Fonts are subsetted and served via WOFF2.
- [ ] Audio files are highly compressed and lazy-loaded.

### Motion & Physics
- [ ] GSAP ScrollTrigger has `scrub: 1.5` enabled.
- [ ] Camera `LookAt` vector never breaks or snaps abruptly.
- [ ] `prefers-reduced-motion` successfully falls back to opacity crossfades.

### Final Creative Sign-Off
- [ ] `creative-director` has reviewed the 60FPS final render.
- [ ] `art-director` has verified the Silk subsurface scattering looks physical, not plastic.
- [ ] `cinematic-director` has verified the 50mm lens distortion and framing.
- [ ] `experience-architect` confirms the "No-UI" rule is intact until the scroll finishes.

---
**Status:** READY FOR ENGINEERING.
