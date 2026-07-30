I **approve the direction**, but I **don't approve the implementation as written**.

This solves the symptom (blank canvas), but not the underlying architecture.

As Creative Director, here's my review.

---

# Overall Score

| Category              |   Score |
| --------------------- | ------: |
| Fixes Blank Screen    | ✅ 10/10 |
| Offline Reliability   | ✅ 10/10 |
| Lighting Quality      |    7/10 |
| Architecture          |    8/10 |
| Long-term Scalability |  6.5/10 |

---

# Problem 1

The proposal hardcodes lighting.

```tsx
<spotLight ... />
<pointLight ... />
<pointLight ... />
```

That immediately violates our Creative Constitution.

Remember we defined

> Material Profiles

and

> Experience Tokens

Lighting should not be random JSX.

Lighting should be data.

---

Instead of

```tsx
<spotLight .../>
```

I want

```typescript
LightingProfile

↓

StudioLuxury

↓

Renderer

↓

Three.js Lights
```

---

Example

```typescript
interface LightingProfile {

keyLight

fillLight

rimLight

accentLight

ambient

fog

exposure

temperature

}
```

Then

```typescript
BanarasiSilkProfile

↓

lightingProfile

↓

StudioLuxury
```

---

Now tomorrow

Leather

doesn't need rewritten code.

---

# Problem 2

Environment shouldn't disappear.

I agree

don't use

```tsx
<Environment preset="studio" />
```

because it's network dependent.

But I don't agree

with removing environments entirely.

Instead

Create

```text
Environment Renderer

↓

Offline Environment

↓

Lighting Profile
```

---

Imagine

```text
Studio

Gallery

Luxury Boutique

Temple

Minimal

Editorial
```

Each one

uses local assets.

No internet.

---

# Problem 3

Lighting Philosophy

The proposal

adds

three lights.

That's implementation.

I want philosophy.

---

Lighting DNA

Always

```text
Key

↓

Fill

↓

Rim

↓

Material Accent
```

Never

random point lights.

---

Also

Gold shouldn't illuminate

the whole scene.

Only

zari.

---

Meaning

gold is a material response.

Not

a light color.

Huge difference.

---

Instead

White studio lights

↓

Gold shader reacts

↓

Gold reflects

That's physically believable.

---

# Problem 4

Intensity

```tsx
8.0
```

No.

Magic numbers.

Everything should come

from tokens.

Example

```yaml
Lighting

Key

1.2

Fill

0.6

Rim

0.8

Exposure

1.1

```

---

# Problem 5

Suspense

Approved.

100%.

That should stay.

---

# Problem 6

Verification

Not enough.

I want

Performance Verification.

---

Example

Developer checklist

```text
✓ 60 FPS

✓ No shader compilation warnings

✓ No dropped frames

✓ No unnecessary re-renders

✓ GPU memory stable

✓ Offline rendering

✓ SSR safe

✓ Mobile fallback
```

---

# Biggest Missing Layer

I think this is where we finally introduce

## Render Pipeline

Instead of

```text
Canvas

↓

Lights

↓

Mesh
```

Create

```text
Experience Controller

↓

Material Renderer

↓

Lighting Renderer

↓

Environment Renderer

↓

Post Processing

↓

Canvas
```

Notice

everything

is modular.

---

# My Recommendation

I would rewrite the developer task completely.

---

# EIS-010

## Lighting & Environment Architecture

### Objective

Replace the network-dependent HDR environment with a fully local, data-driven rendering pipeline that supports future material profiles while maintaining Atelier's Lighting DNA.

---

## Phase 1

Create

```typescript
LightingProfile.ts

EnvironmentProfile.ts

MaterialProfile.ts
```

No hardcoded lights.

---

## Phase 2

Implement

LightingRenderer

Responsibilities

* Build Three.js lights
* Read LightingProfile
* Update dynamically
* Support Experience Tokens

---

## Phase 3

Implement

EnvironmentRenderer

Responsibilities

* Local backgrounds
* Fog
* Atmospheric depth
* Color grading
* Offline only

---

## Phase 4

Implement

StudioLuxuryLighting

Current profile

```text
Key

Soft white

↓

Fill

Neutral

↓

Rim

Cool white

↓

Accent

Warm reflection
```

Notice

gold is not emitted.

Gold is reflected.

---

## Phase 5

Performance

Target

```text
Desktop

60 FPS

Laptop

55+

No network assets

No shader stutters

Graceful degradation
```

---

# One Final Addition

This is something I think will make the renderer unique.

---

## Material-Aware Lighting

Instead of

```text
Light

↓

Object
```

Imagine

```text
Material

↓

Lighting Response

↓

Final Appearance
```

Example

```text
Banarasi Silk

↓

Strong anisotropy

↓

Soft reflections

↓

Directional highlights

↓

Warm gold response
```

---

Leather

↓

Low anisotropy

↓

Broad highlights

↓

High roughness

↓

Deep shadows

---

Linen

↓

Diffuse

↓

Almost no reflection

↓

Soft scatter

---

Now the lighting system understands

the material.

Not just the scene.

---

# Final Decision

## ❌ I do not approve this exact implementation.

## ✅ I approve the intent.

### Required changes before implementation

* Replace hardcoded light definitions with **Lighting Profiles**.
* Introduce a **Lighting Renderer** and **Environment Renderer**.
* Make gold a **material response**, not a gold-colored light.
* Replace magic numbers with design tokens.
* Expand verification to include rendering performance and stability.
* Keep the offline-first approach.

---

## Priority Recommendation

One last architectural suggestion before you hand this to the developer AI:

**Don't think of Three.js as "the renderer."**

Think of it as **the final stage** in a rendering pipeline:

```text
Experience Controller
        │
        ▼
Experience Tokens
        │
        ▼
Material Renderer
        │
        ▼
Lighting Renderer
        │
        ▼
Environment Renderer
        │
        ▼
Post-Processing Renderer
        │
        ▼
Three.js Canvas
```

That separation aligns perfectly with the architecture we've been building. It keeps rendering decisions data-driven, makes future materials and environments easy to add, and prevents implementation details from leaking into the creative layer. That's the kind of architecture that will still be maintainable when your platform supports dozens of materials, campaign types, and rendering experiences.
