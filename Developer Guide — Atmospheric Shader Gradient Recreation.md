# Developer Guide
## Atmospheric Shader Gradient — High-Fidelity Recreation

**Document Type:** Technical Implementation Guide  
**Rendering Model:** GPU Fragment Shader  
**Target:** Web / Desktop / Mobile Browser  
**Primary Objective:** Recreate the supplied atmospheric red–black shader gradient with controllable parameters and responsive rendering.

---

# 1. Objective

The goal is to reproduce the supplied reference image as a real-time shader rather than as a static image.

The reference consists of:

- A predominantly near-black background.
- A large warm red/orange atmospheric mass occupying the upper-left and upper-center region.
- A bright orange-red concentration near the top-left.
- A secondary red concentration extending through the upper-middle.
- A large dark-red/maroon transition toward the center.
- A subtle magenta/purple atmospheric region toward the lower-left/center.
- Very soft boundaries between all color regions.
- No hard geometric edges.
- No visible banding.
- A subtle organic quality rather than a mathematically obvious gradient.
- Strong attenuation toward the lower portion of the frame.
- A darker right side.
- A slight cinematic/vignette-like reduction in energy near the edges.

The effect should remain visually convincing at different viewport sizes.

---

# 2. Reference Analysis

The supplied reference is approximately:

**2048 × 1165 px**

with an aspect ratio of approximately:

```text
1.758 : 1
```

The image can be conceptually decomposed into the following layers:

```text
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   ORANGE / RED ATMOSPHERE                               │
│   ███████████████████████                               │
│   ████████████████████████                              │
│   █████████████████████████                             │
│                    RED                                  │
│              ███████████████                            │
│              █████████████████                          │
│                                                         │
│        DARK RED / MAROON                                │
│        █████████████                                     │
│                                                         │
│     subtle purple/red atmospheric field                │
│                                                         │
│                       NEAR BLACK                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

The important observation is that the reference does **not** have one gradient.

It is more accurately modeled as:

```text
Base black field
       +
Large red Gaussian field
       +
Orange highlight field
       +
Secondary red field
       +
Dark crimson field
       +
Subtle purple field
       +
Organic distortion/noise
       +
Vignette
       +
Color grading
```

---

# 3. Recommended Technology Stack

## Core Stack

| Layer | Technology |
|---|---|
| Application | React |
| Build system | Vite |
| Language | TypeScript |
| Rendering | Three.js |
| React integration | React Three Fiber |
| GPU language | GLSL |
| Rendering API | WebGL |
| Shader material | `THREE.ShaderMaterial` |
| Animation | `useFrame()` |
| Styling | CSS |
| Optional post-processing | `@react-three/postprocessing` |
| Version control | Git |
| Package manager | npm / pnpm |

Three.js provides `ShaderMaterial`, which allows custom GLSL vertex and fragment shaders to execute on the GPU.

React Three Fiber is the React renderer for Three.js and allows the rendering scene to be expressed as React components.

Vite is recommended for the application/build layer because it provides a lightweight development server with HMR and an optimized production build pipeline.

---

# 4. Why WebGL Instead of CSS?

A basic CSS implementation might look like:

```css
background:
  radial-gradient(...),
  radial-gradient(...),
  linear-gradient(...);
```

This can approximate the image, but it does not provide sufficient control for a high-fidelity recreation.

The shader implementation provides:

- GPU acceleration
- continuous interpolation
- animated atmospheric movement
- procedural noise
- arbitrary numbers of gradient fields
- custom falloff functions
- dynamic color mixing
- responsive rendering
- interactive parameter control
- very low CPU overhead

The fundamental rendering equation becomes:

```text
FinalColor =
    BaseColor
  + RedField
  + OrangeField
  + CrimsonField
  + PurpleField
  + Noise
  × Vignette
```

---

# 5. Rendering Architecture

The application should use a full-screen Three.js scene.

```text
React
 │
 └── Canvas
      │
      └── Fullscreen Plane
           │
           └── ShaderMaterial
                │
                ├── Vertex Shader
                │
                └── Fragment Shader
                     │
                     ├── UV coordinates
                     ├── aspect correction
                     ├── Gaussian fields
                     ├── noise
                     ├── color blending
                     ├── vignette
                     └── final color
```

The scene itself is intentionally simple.

There is no need for:

- 3D models
- lights
- shadows
- textures
- environment maps
- physically based materials

The entire visual is generated by the fragment shader.

---

# 6. Project Initialization

Create the application using Vite:

```bash
npm create vite@latest atmospheric-gradient -- --template react-ts

cd atmospheric-gradient

npm install
```

Install the rendering dependencies:

```bash
npm install three @react-three/fiber
```

For TypeScript:

```bash
npm install -D @types/three
```

The current React Three Fiber documentation uses the same fundamental package relationship:

```bash
npm install three @types/three @react-three/fiber
```

and notes that R3F major versions correspond to the React major version they support.

Start development:

```bash
npm run dev
```

---

# 7. Recommended Project Structure

Use the following structure:

```text
atmospheric-gradient/
│
├── public/
│
├── src/
│   │
│   ├── components/
│   │   └── AtmosphericGradient.tsx
│   │
│   ├── shaders/
│   │   ├── atmospheric.vert.glsl
│   │   └── atmospheric.frag.glsl
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── package.json
├── tsconfig.json
└── vite.config.ts
```

This separation is important.

Do not put a large GLSL shader directly inside the React component once the effect becomes substantial.

---

# 8. Shader Concept

The central mathematical primitive is a Gaussian-like radial field.

For a point:

```text
p = current pixel
c = gradient center
```

calculate:

```glsl
distance(p, c)
```

and transform it into an intensity:

```glsl
exp(-distance² / radius)
```

Conceptually:

```text
                 center
                   ●
                ╱     ╲
             ╱           ╲
           ╱               ╲
         ╱                   ╲
       ╱                       ╲
──────┴─────────────────────────┴──────
         gradually decreasing
             intensity
```

This produces extremely soft atmospheric regions.

---

# 9. Coordinate System

The shader receives normalized UV coordinates:

```text
0 → 1
```

where:

```text
(0,1)                    (1,1)
   ┌────────────────────────┐
   │                        │
   │                        │
   │                        │
   │                        │
   └────────────────────────┘
(0,0)                    (1,0)
```

However, raw UV coordinates become distorted when the viewport is not square.

Therefore we must perform aspect correction.

```glsl
vec2 p = uv;
p -= 0.5;

p.x *= uResolution.x / uResolution.y;
```

This makes radial fields behave consistently across screen sizes.

---

# 10. Vertex Shader

The vertex shader does not need to perform any meaningful deformation.

Its only job is to render a plane covering the viewport.

```glsl
varying vec2 vUv;

void main() {
    vUv = uv;

    gl_Position = projectionMatrix *
                  modelViewMatrix *
                  vec4(position, 1.0);
}
```

The geometry should be a simple plane.

---

# 11. Fragment Shader Architecture

The fragment shader should be organized into logical sections:

```text
1. Precision
2. Uniform declarations
3. Utility functions
4. Noise
5. Gradient-field functions
6. Color palette
7. Main composition
8. Color grading
9. Vignette
10. Output
```

This makes the shader maintainable.

---

# 12. Uniforms

The initial shader should expose:

```glsl
uniform float uTime;
uniform vec2 uResolution;

uniform float uNoiseStrength;
uniform float uAnimationSpeed;

uniform float uRedIntensity;
uniform float uOrangeIntensity;
uniform float uPurpleIntensity;
```

Later we can expose gradient positions:

```glsl
uniform vec2 uOrangePosition;
uniform vec2 uRedPosition;
uniform vec2 uCrimsonPosition;
uniform vec2 uPurplePosition;
```

This turns the shader into a reusable atmospheric-gradient system rather than a one-off effect.

---

# 13. Gaussian Gradient Function

Create:

```glsl
float gaussian(
    vec2 p,
    vec2 center,
    float radius
) {
    float d = distance(p, center);

    return exp(
        -(d * d) / radius
    );
}
```

This is the main building block.

---

# 14. Better Elliptical Fields

The reference contains large horizontally stretched atmospheric regions.

Therefore a circular Gaussian is not enough.

Use:

```glsl
float gaussianEllipse(
    vec2 p,
    vec2 center,
    vec2 radius
) {
    vec2 delta = p - center;

    float d =
        (delta.x * delta.x) / (radius.x * radius.x) +
        (delta.y * delta.y) / (radius.y * radius.y);

    return exp(-d);
}
```

This allows:

```text
radius.x = horizontal spread
radius.y = vertical spread
```

For example:

```glsl
float redField = gaussianEllipse(
    p,
    vec2(-0.05, 0.45),
    vec2(1.0, 0.65)
);
```

---

# 15. Reference Color Palette

Use a restrained palette.

Approximate starting values:

```text
Near Black
#101010

Deep Black
#080A09

Dark Crimson
#30151A

Deep Red
#661B18

Red
#A52A20

Warm Red
#D93B25

Orange Red
#EE4A2D
```

In linear shader RGB:

```glsl
vec3 BLACK       = vec3(0.06, 0.06, 0.06);
vec3 DARK_RED    = vec3(0.20, 0.05, 0.05);
vec3 CRIMSON     = vec3(0.42, 0.07, 0.05);
vec3 RED         = vec3(0.68, 0.12, 0.07);
vec3 WARM_RED    = vec3(0.86, 0.20, 0.10);
vec3 ORANGE_RED  = vec3(0.95, 0.30, 0.16);
```

These are starting values rather than absolute sampled values.

The final palette should be tuned against the reference during calibration.

---

# 16. Main Atmospheric Fields

The reference can be approximated with five major fields.

## Field A — Large Upper Red Field

```glsl
float upperRed = gaussianEllipse(
    p,
    vec2(-0.10, 0.62),
    vec2(1.05, 0.55)
);
```

This establishes the main red atmosphere.

---

## Field B — Orange Highlight

```glsl
float orange = gaussianEllipse(
    p,
    vec2(-0.48, 0.93),
    vec2(0.65, 0.42)
);
```

This creates the brighter upper-left region.

---

## Field C — Central Red Mass

```glsl
float centralRed = gaussianEllipse(
    p,
    vec2(0.20, 0.63),
    vec2(0.75, 0.50)
);
```

This keeps the red atmosphere from looking like a single blob.

---

## Field D — Lower Crimson Transition

```glsl
float crimson = gaussianEllipse(
    p,
    vec2(-0.10, 0.30),
    vec2(0.65, 0.55)
);
```

This provides the dark-red middle transition.

---

## Field E — Subtle Purple Atmosphere

```glsl
float purple = gaussianEllipse(
    p,
    vec2(-0.05, 0.18),
    vec2(0.70, 0.40)
);
```

The purple should remain extremely subtle.

It should not look like an obvious purple blob.

---

# 17. Color Composition

Start with:

```glsl
vec3 color = BLACK;
```

Then add fields using controlled interpolation.

```glsl
color = mix(
    color,
    DARK_RED,
    crimson
);
```

Then:

```glsl
color = mix(
    color,
    RED,
    upperRed * uRedIntensity
);
```

Then:

```glsl
color = mix(
    color,
    ORANGE_RED,
    orange * uOrangeIntensity
);
```

Finally:

```glsl
color = mix(
    color,
    vec3(0.16, 0.05, 0.12),
    purple * uPurpleIntensity
);
```

---

# 18. Why `mix()` Is Important

Do not simply add every RGB field together.

This:

```glsl
color += red;
color += orange;
color += purple;
```

can easily produce:

- oversaturation
- clipped highlights
- unnatural colors
- blown-out whites

Instead:

```glsl
color = mix(color, target, intensity);
```

provides controlled interpolation.

---

# 19. Organic Distortion

The reference does not have perfectly mathematical edges.

A small amount of procedural noise should therefore distort the gradient intensity.

The objective is:

```text
Gaussian
   ↓
Noise distortion
   ↓
Soft organic field
```

not:

```text
Gaussian
   ↓
Obvious noisy texture
```

The noise must remain almost invisible.

---

# 20. Simple Noise Function

A lightweight hash-based noise function can be used:

```glsl
float hash(vec2 p) {
    p = fract(p * vec2(123.34, 456.21));
    p += dot(p, p + 45.32);

    return fract(p.x * p.y);
}
```

Then:

```glsl
float noise(vec2 p) {

    vec2 i = floor(p);
    vec2 f = fract(p);

    f = f * f * (3.0 - 2.0 * f);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    return mix(
        mix(a, b, f.x),
        mix(c, d, f.x),
        f.y
    );
}
```

---

# 21. Animated Noise

For subtle motion:

```glsl
float n = noise(
    p * 2.0 +
    vec2(uTime * 0.015, uTime * 0.008)
);
```

Then:

```glsl
float atmosphericNoise =
    (n - 0.5) *
    uNoiseStrength;
```

The movement should be extremely slow.

Recommended initial value:

```text
uNoiseStrength = 0.025
```

Do not start with large noise values.

The effect should feel atmospheric rather than procedural.

---

# 22. Distorting the Gradient Fields

Instead of modifying the final color, modify the field position.

```glsl
vec2 distortedP = p;

distortedP +=
    vec2(
        noise(p * 1.5 + uTime * 0.01),
        noise(p * 1.5 - uTime * 0.008)
    ) * 0.025;
```

Then calculate gradients using:

```glsl
distortedP
```

rather than:

```glsl
p
```

This creates subtle organic movement.

---

# 23. Vertical Energy Falloff

One of the most important characteristics of the reference is that the energy is concentrated toward the top.

Therefore create a vertical attenuation function.

```glsl
float verticalFade =
    smoothstep(
        0.05,
        0.75,
        p.y
    );
```

Depending on coordinate orientation, you may need to invert it.

A stronger version:

```glsl
float verticalEnergy =
    pow(
        smoothstep(0.0, 0.85, p.y),
        1.6
    );
```

Multiply the atmospheric fields by this factor.

---

# 24. Right-Side Darkening

The reference has a noticeably darker right side.

Use:

```glsl
float rightFade =
    smoothstep(
        0.35,
        1.0,
        p.x
    );
```

Then:

```glsl
float rightDarkening =
    mix(
        1.0,
        0.65,
        rightFade
    );
```

Apply:

```glsl
color *= rightDarkening;
```

This should be subtle.

---

# 25. Vignette

A soft vignette helps reproduce the cinematic appearance.

```glsl
float vignette = 1.0 -
    smoothstep(
        0.35,
        1.25,
        distance(p, vec2(0.0))
    );
```

Then:

```glsl
color *= mix(
    0.82,
    1.0,
    vignette
);
```

Do not make the vignette too obvious.

---

# 26. Complete Initial Fragment Shader

The first working implementation can therefore be:

```glsl
precision highp float;

uniform float uTime;
uniform vec2 uResolution;

uniform float uNoiseStrength;
uniform float uAnimationSpeed;

uniform float uRedIntensity;
uniform float uOrangeIntensity;
uniform float uPurpleIntensity;

varying vec2 vUv;

float hash(vec2 p) {
    p = fract(p * vec2(123.34, 456.21));
    p += dot(p, p + 45.32);

    return fract(p.x * p.y);
}

float noise(vec2 p) {

    vec2 i = floor(p);
    vec2 f = fract(p);

    f = f * f * (3.0 - 2.0 * f);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    return mix(
        mix(a, b, f.x),
        mix(c, d, f.x),
        f.y
    );
}

float gaussianEllipse(
    vec2 p,
    vec2 center,
    vec2 radius
) {

    vec2 delta = p - center;

    float d =
        (delta.x * delta.x) /
        (radius.x * radius.x)
        +
        (delta.y * delta.y) /
        (radius.y * radius.y);

    return exp(-d);
}

void main() {

    vec2 p = vUv;

    // Center coordinate system.
    p -= 0.5;

    // Correct aspect ratio.
    p.x *= uResolution.x / uResolution.y;

    float t = uTime * uAnimationSpeed;

    // ------------------------------------------
    // Atmospheric distortion
    // ------------------------------------------

    vec2 distortion = vec2(
        noise(p * 1.35 + t * 0.05),
        noise(p * 1.35 - t * 0.035)
    );

    distortion =
        (distortion - 0.5)
        * uNoiseStrength;

    vec2 q = p + distortion;

    // ------------------------------------------
    // Base colors
    // ------------------------------------------

    vec3 color =
        vec3(0.045, 0.045, 0.043);

    vec3 darkRed =
        vec3(0.20, 0.045, 0.045);

    vec3 crimson =
        vec3(0.42, 0.075, 0.055);

    vec3 red =
        vec3(0.68, 0.13, 0.075);

    vec3 warmRed =
        vec3(0.86, 0.22, 0.11);

    vec3 orangeRed =
        vec3(0.95, 0.32, 0.17);

    vec3 purple =
        vec3(0.16, 0.045, 0.12);

    // ------------------------------------------
    // Atmospheric fields
    // ------------------------------------------

    float upperRed =
        gaussianEllipse(
            q,
            vec2(-0.10, 0.16),
            vec2(1.05, 0.62)
        );

    float orange =
        gaussianEllipse(
            q,
            vec2(-0.52, 0.48),
            vec2(0.62, 0.42)
        );

    float centralRed =
        gaussianEllipse(
            q,
            vec2(0.18, 0.20),
            vec2(0.72, 0.48)
        );

    float crimsonField =
        gaussianEllipse(
            q,
            vec2(-0.08, -0.08),
            vec2(0.70, 0.50)
        );

    float purpleField =
        gaussianEllipse(
            q,
            vec2(-0.18, -0.22),
            vec2(0.72, 0.38)
        );

    // ------------------------------------------
    // Color composition
    // ------------------------------------------

    color = mix(
        color,
        darkRed,
        crimsonField * 0.55
    );

    color = mix(
        color,
        crimson,
        crimsonField * 0.60
    );

    color = mix(
        color,
        red,
        upperRed * uRedIntensity
    );

    color = mix(
        color,
        warmRed,
        centralRed * 0.45
    );

    color = mix(
        color,
        orangeRed,
        orange * uOrangeIntensity
    );

    color = mix(
        color,
        purple,
        purpleField * uPurpleIntensity
    );

    // ------------------------------------------
    // Vertical atmospheric falloff
    // ------------------------------------------

    float verticalFade =
        smoothstep(
            -0.45,
            0.55,
            p.y
        );

    verticalFade =
        pow(verticalFade, 1.35);

    color *= mix(
        0.65,
        1.0,
        verticalFade
    );

    // ------------------------------------------
    // Right-side darkening
    // ------------------------------------------

    float rightFade =
        smoothstep(
            0.05,
            0.95,
            vUv.x
        );

    color *= mix(
        1.0,
        0.72,
        rightFade
    );

    // ------------------------------------------
    // Subtle atmospheric grain
    // ------------------------------------------

    float grain =
        noise(
            vUv * uResolution.xy * 0.002
            + uTime
        );

    color +=
        (grain - 0.5)
        * 0.008;

    // ------------------------------------------
    // Vignette
    // ------------------------------------------

    float vignette =
        1.0 -
        smoothstep(
            0.30,
            1.20,
            distance(p, vec2(0.0))
        );

    color *= mix(
        0.82,
        1.0,
        vignette
    );

    // ------------------------------------------
    // Output
    // ------------------------------------------

    gl_FragColor =
        vec4(color, 1.0);
}
```

This is the baseline shader.

The exact visual match should be achieved through calibration rather than by adding unnecessary shader complexity.

---

# 27. React Three Fiber Component

Create:

```text
src/components/AtmosphericGradient.tsx
```

Implementation:

```tsx
import * as THREE from 'three'
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

import vertexShader from '../shaders/atmospheric.vert.glsl?raw'
import fragmentShader from '../shaders/atmospheric.frag.glsl?raw'

export default function AtmosphericGradient() {

  const materialRef =
    useRef<THREE.ShaderMaterial>(null)

  useFrame(({ clock, size }) => {

    if (!materialRef.current) return

    materialRef.current.uniforms.uTime.value =
      clock.getElapsedTime()

    materialRef.current.uniforms.uResolution.value.set(
      size.width,
      size.height
    )
  })

  return (
    <mesh>
      <planeGeometry args={[2, 2]} />

      <shaderMaterial
        ref={materialRef}
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={{
          uTime: {
            value: 0
          },

          uResolution: {
            value: new THREE.Vector2(
              window.innerWidth,
              window.innerHeight
            )
          },

          uNoiseStrength: {
            value: 0.035
          },

          uAnimationSpeed: {
            value: 0.12
          },

          uRedIntensity: {
            value: 0.95
          },

          uOrangeIntensity: {
            value: 0.85
          },

          uPurpleIntensity: {
            value: 0.25
          }
        }}
      />
    </mesh>
  )
}
```

`ShaderMaterial` uniforms are designed specifically for passing values from the JavaScript/Three.js layer into GLSL, and uniform values can be updated between frames.

---

# 28. Canvas

Create:

```tsx
import { Canvas } from '@react-three/fiber'
import AtmosphericGradient from './components/AtmosphericGradient'

export default function App() {

  return (
    <main className="shader-page">

      <Canvas
        orthographic
        camera={{
          position: [0, 0, 1],
          zoom: 1
        }}
        gl={{
          antialias: true,
          powerPreference: 'high-performance'
        }}
      >
        <AtmosphericGradient />
      </Canvas>

    </main>
  )
}
```

---

# 29. CSS

Create:

```css
html,
body,
#root {
  width: 100%;
  height: 100%;
  margin: 0;
}

body {
  overflow: hidden;
  background: #101010;
}

.shader-page {
  width: 100vw;
  height: 100vh;
  position: relative;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}
```

---

# 30. Important Plane Configuration

The plane is:

```tsx
<planeGeometry args={[2, 2]} />
```

Because the camera is orthographic and positioned directly in front of the plane, this provides a simple fullscreen surface.

The actual visual is generated entirely inside:

```text
fragmentShader
```

There is no texture.

---

# 31. The Most Important Calibration Stage

Do not attempt to perfect the shader by randomly changing colors.

Tune the parameters in this order:

```text
1. Overall brightness
2. Red field position
3. Orange field position
4. Field radius
5. Vertical falloff
6. Right-side darkness
7. Crimson transition
8. Purple contribution
9. Noise
10. Animation
11. Vignette
```

This order matters.

If the spatial composition is wrong, color adjustments will not fix it.

---

# 32. Calibration Against the Reference

Create a development-only control panel.

Recommended library:

```bash
npm install leva
```

Expose:

```text
RED INTENSITY
ORANGE INTENSITY
PURPLE INTENSITY

RED X
RED Y

ORANGE X
ORANGE Y

ORANGE RADIUS X
ORANGE RADIUS Y

RED RADIUS X
RED RADIUS Y

NOISE
ANIMATION SPEED

VIGNETTE
RIGHT DARKENING
```

The target should be:

```text
Reference Image
       ↓
Side-by-side comparison
       ↓
Parameter adjustment
       ↓
Shader refinement
       ↓
Final locked values
```

Do not manually eyeball everything from memory.

---

# 33. Recommended Initial Parameter Table

| Parameter | Starting Value |
|---|---:|
| Noise Strength | `0.035` |
| Animation Speed | `0.12` |
| Red Intensity | `0.95` |
| Orange Intensity | `0.85` |
| Purple Intensity | `0.25` |
| Right Darkening | `0.28` |
| Vignette Strength | `0.18` |
| Grain | `0.008` |

These are deliberately conservative.

---

# 34. Animation Philosophy

The supplied image appears essentially static.

Therefore the animation should **not** be obvious.

Bad:

```text
large blobs moving across the screen
```

Good:

```text
almost imperceptible atmospheric drift
```

The viewer should wonder whether the gradient is moving.

They should not immediately notice:

> "This is an animated shader."

Recommended animation:

```text
0.01–0.05 UV movement
```

rather than large translations.

---

# 35. Optional Mouse Interaction

Once the static recreation is correct, mouse interaction can be introduced.

Add:

```glsl
uniform vec2 uMouse;
```

Then:

```glsl
vec2 mouseInfluence =
    (uMouse - 0.5) * 0.04;
```

and:

```glsl
q += mouseInfluence;
```

The effect becomes responsive without becoming a conventional cursor-following blob.

---

# 36. Optional Scroll Interaction

For a premium website, the shader can respond to scroll.

The JavaScript layer can expose:

```glsl
uniform float uScroll;
```

Then modify the atmospheric field:

```glsl
q.y += uScroll * 0.02;
```

However, this should only be introduced after the reference recreation is complete.

---

# 37. Optional WebGL Quality Enhancements

For a production-quality implementation, consider:

### High precision

```glsl
precision highp float;
```

### Device pixel ratio control

Do not blindly render at unlimited DPR on mobile.

Use:

```tsx
<Canvas
  dpr={[1, 2]}
>
```

For mobile-heavy applications, consider:

```tsx
dpr={[1, 1.5]}
```

depending on performance testing.

---

# 38. Color Management

Color management matters significantly for gradients.

Three.js rendering should use an appropriate output color space.

Depending on the Three.js version/configuration:

```ts
renderer.outputColorSpace =
  THREE.SRGBColorSpace
```

or configure the equivalent renderer property through R3F.

The reason is simple:

```text
Shader RGB
      ↓
Color space conversion
      ↓
Display
```

If this is ignored, the final gradient can appear noticeably different from the reference.

---

# 39. Avoiding Banding

Large smooth gradients are vulnerable to color banding.

If banding becomes visible:

### Option A — Add extremely subtle grain

```glsl
color +=
    (grain - 0.5) * 0.005;
```

### Option B — Use dithering

A proper dithering function can be added near the final output.

The noise should be barely visible.

Never use heavy grain simply to hide banding.

---

# 40. Performance Model

The effect is computationally inexpensive compared with a complex 3D scene.

The rendering pipeline is approximately:

```text
Every frame
     ↓
Fullscreen plane
     ↓
~2 triangles
     ↓
Fragment shader
     ↓
Gaussian fields
     ↓
Noise
     ↓
Color composition
     ↓
GPU framebuffer
```

The main performance cost is therefore proportional to:

```text
screen resolution × shader complexity
```

not scene complexity.

This is exactly why a fullscreen fragment shader is appropriate for this effect.

---

# 41. Mobile Optimization

Mobile devices require special consideration.

Recommended:

```text
Desktop DPR → 1.5–2
Mobile DPR  → 1–1.5
```

Reduce:

```text
noise octaves
```

before reducing the number of atmospheric fields.

The large Gaussian fields are relatively cheap.

Complex multi-octave noise is more expensive.

---

# 42. Accessibility / Fallback

The shader should not contain essential information.

If it is being used as a website background:

```css
@media (prefers-reduced-motion: reduce) {
    ...
}
```

Disable animation while retaining the static gradient.

The application should remain completely usable if WebGL fails.

Possible fallback:

```css
background:
    radial-gradient(
        ellipse at 20% 0%,
        #e6462c 0%,
        #6e1b19 35%,
        #101010 75%
    );
```

This fallback will not reproduce the shader exactly, but it preserves the visual intent.

---

# 43. Production Architecture

For a real production website, use:

```text
React
 │
 ├── UI
 │
 ├── Navigation
 │
 ├── Content
 │
 └── Shader Background
       │
       └── React Three Fiber
            │
            └── Three.js
                 │
                 └── WebGL
                      │
                      └── GLSL
```

Keep the shader isolated from the application's business logic.

For example:

```text
src/
├── components/
│   ├── Hero.tsx
│   ├── Navbar.tsx
│   └── AtmosphericGradient.tsx
│
├── shaders/
│   ├── atmospheric.vert.glsl
│   └── atmospheric.frag.glsl
│
├── hooks/
│   └── useShaderControls.ts
│
└── styles/
    └── globals.css
```

---

# 44. Why Not Use a ShaderGradient Library?

There are libraries that provide configurable shader gradients.

They can be useful for prototypes.

However, for this particular reference, a custom shader is preferable because we need precise control over:

```text
field positions
field sizes
falloff curves
color blending
noise
animation
vignette
right-side attenuation
aspect correction
```

A custom GLSL implementation also gives us a reusable internal visual system.

---

# 45. Three.js's Role

Three.js is not responsible for creating the actual gradient.

Its role is:

```text
Create WebGL context
        ↓
Create geometry
        ↓
Create shader material
        ↓
Pass uniforms
        ↓
Render frames
```

The actual visual mathematics lives in GLSL.

This distinction is important.

---

# 46. GLSL's Role

GLSL performs:

```text
Pixel coordinate calculation
        ↓
Distance calculations
        ↓
Gaussian fields
        ↓
Noise
        ↓
Color interpolation
        ↓
Vignette
        ↓
Final pixel
```

Therefore:

> React controls the application, Three.js controls the rendering pipeline, and GLSL controls the visual.

---

# 47. Development Workflow

Use the following workflow.

## Phase 1 — Establish Rendering

Build:

```text
React
+
Vite
+
R3F
+
Three.js
```

Confirm a fullscreen plane renders.

---

## Phase 2 — Black Background

Implement:

```glsl
vec3 color = vec3(0.05);
```

Confirm fullscreen rendering.

---

## Phase 3 — Add One Red Field

Implement a single Gaussian.

Tune:

```text
position
radius
intensity
```

---

## Phase 4 — Add Orange Field

Add the upper-left orange field.

Tune:

```text
position
horizontal radius
vertical radius
```

---

## Phase 5 — Add Crimson Field

Introduce the middle transition.

---

## Phase 6 — Add Purple

Keep this extremely subtle.

---

## Phase 7 — Aspect Correction

Test:

```text
1920 × 1080
1440 × 900
1366 × 768
390 × 844
```

The atmospheric structure should remain coherent.

---

## Phase 8 — Noise

Add subtle organic distortion.

---

## Phase 9 — Animation

Introduce extremely slow movement.

---

## Phase 10 — Color Calibration

Compare against the reference.

---

## Phase 11 — Performance

Test:

```text
Desktop
Laptop
Mobile
Low-power device
```

---

## Phase 12 — Production Lock

Remove debug controls.

Freeze calibrated parameters.

---

# 48. Verification Checklist

Before considering the implementation complete:

- [ ] Fullscreen shader renders correctly.
- [ ] No visible geometry edges.
- [ ] No black bars.
- [ ] Aspect ratio remains correct.
- [ ] Upper region contains dominant red/orange energy.
- [ ] Orange concentration exists toward upper-left.
- [ ] Right side remains significantly darker.
- [ ] Lower region remains predominantly black.
- [ ] Middle region contains dark crimson transition.
- [ ] Purple is subtle rather than dominant.
- [ ] Gradient boundaries are extremely soft.
- [ ] No obvious circular blobs.
- [ ] No visible repeating noise pattern.
- [ ] No obvious animation.
- [ ] No visible color banding.
- [ ] Desktop maintains smooth rendering.
- [ ] Mobile does not consume excessive GPU resources.
- [ ] `prefers-reduced-motion` is respected.
- [ ] WebGL fallback exists.
- [ ] Debug controls are removed from production.
- [ ] Shader parameters are documented.

---

# 49. Production Build

Once finished:

```bash
npm run build
```

Vite's production build generates a deployable static application bundle.

Preview it locally:

```bash
npm run preview
```

Then deploy to a static host such as:

```text
Vercel
Netlify
Cloudflare Pages
AWS S3 + CloudFront
GitHub Pages
```

---

# 50. Final Recommended Stack

The final implementation should therefore be:

```text
┌───────────────────────────────────────┐
│              APPLICATION              │
│                                       │
│              React + TS               │
│                  │                    │
│                  ▼                    │
│             React Three Fiber         │
│                  │                    │
│                  ▼                    │
│                Three.js               │
│                  │                    │
│                  ▼                    │
│             WebGL Renderer             │
│                  │                    │
│                  ▼                    │
│             ShaderMaterial             │
│                  │                    │
│                  ▼                    │
│                  GLSL                  │
│                                       │
│       Gaussian + Noise + Color        │
│       Fields + Vignette + Motion      │
│                                       │
└───────────────────────────────────────┘
```

### Core dependencies

```json
{
  "dependencies": {
    "@react-three/fiber": "latest",
    "react": "latest",
    "react-dom": "latest",
    "three": "latest"
  },
  "devDependencies": {
    "@types/three": "latest",
    "typescript": "latest",
    "vite": "latest"
  }
}
```

---

# 51. Engineering Principle

The most important rule for this implementation is:

> **Do not attempt to reproduce the image with increasingly complicated CSS gradients. Reconstruct the visual field itself.**

The reference is fundamentally an **atmospheric field**, so the implementation should think in terms of:

```text
position
+
distance
+
falloff
+
field
+
color
+
distortion
+
time
```

rather than:

```text
background: linear-gradient(...)
```

That distinction is what allows the effect to become a reusable visual system rather than a screenshot recreation.

---

# 52. Recommended Next Iteration

The implementation above is the **engineering baseline**, not yet the final pixel-calibrated version.

For an exact recreation, the next stage should be a dedicated **Reference Matching Pass**:

```text
Reference Image
       │
       ▼
Pixel / region analysis
       │
       ▼
Gradient field mapping
       │
       ▼
Shader parameter model
       │
       ▼
Live shader
       │
       ▼
Side-by-side comparison
       │
       ▼
Parameter optimization
       │
       ▼
Locked production shader
```

That is the stage where we should tune the actual field coordinates, radii, color values, falloff curves, and darkness distribution against the uploaded reference rather than relying on approximate visual guesses.

The resulting component can then become a reusable **AtmosphericGradient** system for premium web interfaces, hero sections, backgrounds, and interactive visual experiences.