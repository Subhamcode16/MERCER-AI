# PROD-022 — Asset Manifest
**Layer:** Production Intelligence (Translate)
**Agent:** `asset-supervisor`
**Movement:** I — The Threshold

---

## 1. Geometry (3D)
All geometry MUST be Draco compressed and optimized.
- `geo_silk_drape_v4.glb` (Max 50k tris. Contains shape keys for folding animation).
- `geo_limestone_monument.glb` (Max 150k tris. Decimated, reliant on normal maps).

## 2. Textures
All textures MUST be KTX2 compressed.
- `tex_silk_normal.ktx2` (2K)
- `tex_silk_roughness.ktx2` (1K)
- `tex_stone_albedo.ktx2` (2K)
- `tex_stone_normal.ktx2` (2K)

## 3. Environment & Lighting
- `hdri_warm_studio_03.hdr` (1K resolution. Used purely for ambient reflections, not as a visible skybox).

## 4. Typography
- `PP_Editorial_New_Light.woff2` (Preloaded)
- `Inter_Regular.woff2` (Preloaded)

## 5. Audio
All audio must be mixed at -14 LUFS and exported as `.m4a` / `.ogg` for cross-browser playback.
- `sfx_void_resonance.m4a`
- `sfx_heavy_silk.m4a`
- `sfx_monument_wind.m4a`
