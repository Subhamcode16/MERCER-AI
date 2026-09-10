# Learning Graph: Composition vs. Rendering

## 1. The Core Fallacy: Polishing the Wrong Thing
**Mistake**: Adding bloom, particles, and complex shaders to a fundamentally flawed composition. 
**Lesson**: Rendering quality cannot fix bad composition. A gray rectangle with bloom is still a rectangle. Focus on spatial hierarchy, perspective, and layout before writing shaders.

## 2. Layout & Focal Hierarchy
**Mistake**: Centering everything linearly (`Plane -> Title -> Subtitle`). This kills depth and tension.
**Lesson**: Editorial luxury requires asymmetry and depth. Distribute elements across different layers and scales. Never center-stack everything.

## 3. The Object & Perspective
**Mistake**: Facing the camera directly at a flat plane.
**Lesson**: Perspective creates luxury. Rotate objects (e.g., 25°), suspend them, make them float. Treat digital objects like museum installations.

## 4. The Environment
**Mistake**: Pitch black backgrounds. They kill depth and atmospheric presence.
**Lesson**: Use deep, rich tones (e.g., deep navy, studio cream) with atmospheric fog, volumetric light, and subtle dust. The environment must feel spatial.

## 5. Typography System
**Mistake**: Relying on a single generic font family for all information.
**Lesson**: Implement a strict three-tier typographic hierarchy:
- **Editorial Serif**: For narrative and storytelling (e.g., "What is this?").
- **Technical Mono**: For raw intelligence and data (e.g., "Reflectivity 98.4%").
- **Modern Sans**: For interaction and UI (e.g., Buttons, labels).

## 6. Narrative Choreography (The Reveal)
**Mistake**: Showing everything at once (Plane + Text + Data).
**Lesson**: Stage the reveal to tell a story. 
1. The Subject (Cloth) 
2. The Action (Scanning Beam) 
3. The Intelligence (Annotations) 
4. The Narrative (Title) 
5. The Depth (Data & Particles).

## 7. Camera & Intimacy
**Mistake**: Camera positioned too far away (20 meters back), creating emotional distance.
**Lesson**: Start close and intimate. Users should feel they are inspecting high-end luxury fabric under a loupe.

## 8. Motion & Physics
**Mistake**: Using generic noise for vertex displacement and calling it "cloth".
**Lesson**: Think in physics, not shaders. Silk has inertia, folds catch light, and corners lag.

## 9. The Golden Rule
> **No visual effect may be introduced unless it supports the narrative.**
Every particle, bloom, and camera move must exist for a semantic reason, not just because it looks "cool".
