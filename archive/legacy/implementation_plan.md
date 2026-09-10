# Sprint 2: The Physical World

## Primary Visual Artifact: Art Direction Locked
As per our new Studio methodology, the image is now the primary specification, and this markdown is the supporting engineering layer. Our entire goal for this Sprint is to recreate the lighting, depth, and material properties seen below in WebGL.

![Obsidian Silk Threshold](file:///C:/Users/User/.gemini/antigravity-ide/brain/14a1610f-6818-4654-8e16-8db3d7a9de89/obsidian_silk_threshold_1784046264637.png)

## Goal
Establish the environment architecture and the primary subject (Obsidian Silk) within the WebGL scene, ensuring the atmosphere perfectly matches the generated Keyframe artifact.

## User Review Required
> [!WARNING]
> Because we do not yet have the final exported Draco `.glb` mesh from the 3D team, I will use an abstract mathematical geometry (like a highly tessellated sphere or torus knot) to build and calibrate the custom Subsurface Scattering shader and lighting rig. Do you approve of using a placeholder geometry to dial in the look first?

## Proposed Changes

### 1. The Environment & Lighting Rig
#### [NEW] `src/components/canvas/PhysicalWorld.tsx`
We will build the lighting rig that matches the image:
- A strong overhead `SpotLight` with a sharp penumbra for the dramatic spotlight effect.
- A very dim, warm `AmbientLight` to replicate the charcoal limestone bounce.
- A subtle `Fog` matched to the limestone hex color to enforce depth and negative space (the "Void" push).

### 2. The Material (Obsidian Silk)
#### [NEW] `src/components/canvas/ObsidianSilk.tsx`
We will construct the subject. The critical challenge here is the material:
- We will use `MeshPhysicalMaterial` available in Three.js, configuring `transmission`, `thickness`, `roughness`, and `ior` to mimic the subtle translucency at the edges of the silk seen in the image.
- The object will have a slow, breathing, vertical float animation (driven by `useFrame` and `Math.sin`).

### 3. Scene Integration
#### [MODIFY] `src/components/canvas/Scene.tsx`
We will import both `PhysicalWorld` and `ObsidianSilk` into the global `Scene`, removing the temporary placeholder light.

## Verification Plan
1. Start the Next.js dev server.
2. Ensure the visual output in the browser visually aligns with the lighting, contrast, and material feel of the generated image.
