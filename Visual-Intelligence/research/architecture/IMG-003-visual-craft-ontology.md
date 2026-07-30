# IMG-003: Visual Craft Ontology

## 1. Core Purpose
The Visual Craft Ontology is the single most valuable layer of permanent knowledge in the platform. While fashion trends and AI renderers change, the fundamental principles of optics, lighting, and color science remain constant. 

This ontology defines how the camera and the light interact with the scene, allowing the Image Formation Solver to construct deeply physical and highly aesthetic Creative States.

## 2. Lens Language
Lenses do more than define a field of view; they define psychological proximity and spatial compression.
- **Wide Angle (e.g., 24mm, 35mm):** High spatial distortion, deep depth of field, places the viewer *inside* the environment. Used for environmental storytelling.
- **Standard (e.g., 50mm):** Human-eye equivalent, neutral spatial compression.
- **Telephoto (e.g., 85mm, 135mm):** High spatial compression (flattens background), isolates the subject, shallow depth of field. Used for premium portraiture and luxury isolation.

## 3. Lighting Archetypes
Lighting defines form and mood.
- **Paramount / Butterfly:** Frontal, slightly above. High glamour, fills wrinkles, defines cheekbones.
- **Split:** 90 degrees to the side. High drama, textural emphasis, halves the subject.
- **Rembrandt:** 45 degrees side/high. Classic, natural, creates the signature cheek triangle.
- **Broad / Short:** Defines whether the broad side of the face (facing camera) or short side (turned away) is illuminated. Short lighting slims the subject and adds mystery.

## 4. Color Science
Color grading establishes the emotional baseline.
- **Highlight Roll-off:** How smoothly bright areas transition to pure white (e.g., Arri Alexa smooth roll-off vs. harsh digital clipping).
- **Halation:** The red glow around bright specular highlights, characteristic of physical film.
- **Palettes:** Warm Sandstone, Cool Cyan/Teal, Desaturated Luxury.

## 5. Renderer Capability Profiles
Because the Visual Craft Ontology is renderer-agnostic, the **Prompt Compiler** must filter the Creative State through a Renderer Capability Profile (e.g., `renderer_profiles.json`).

If the solver outputs a Creative State demanding `1/50th shutter speed for motion blur` and the target is `GPT Image` (which does not understand explicit shutter speed), the Prompt Compiler translates this into `heavy motion blur, dynamic movement`. If the target is a highly technical 3D renderer or an advanced model that *does* understand shutter speed, it passes the parameter exactly as is.
