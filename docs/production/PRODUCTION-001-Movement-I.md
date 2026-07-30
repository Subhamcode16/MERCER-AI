# PRODUCTION-001 — Movement I: The Threshold

**Version:** 1.0  
**Status:** Production Ready  
**Movement:** I — The Threshold  
**Duration:** 35–45 Seconds (Scroll Driven)  
**Dependencies:**
- DIRECTOR-001 — Movement I
- Motion Grammar
- Design Grammar
- Production Book

---

# Production Goal

The purpose of this document is to translate the creative vision into an executable production script.

Unlike the Director's Bible, this document contains measurable instructions.

Every animation, transition, camera movement, lighting cue and interaction is defined.

There should be **zero interpretation** required from engineering.

---

# Experience Architecture

```text
Movement I

Act I
The Threshold

↓

Act II
Matter Awakens

↓

Act III
Observation

↓

Act IV
Reasoning

↓

Act V
The Institution

↓

Act VI
Invitation
```

---

# Scroll Timeline

| Scroll | Act | Duration |
|---------|-----|----------|
| 0.00–0.15 | Threshold | 5 s |
| 0.15–0.30 | Matter | 7 s |
| 0.30–0.50 | Observation | 8 s |
| 0.50–0.70 | Reasoning | 8 s |
| 0.70–0.90 | Institution | 10 s |
| 0.90–1.00 | Invitation | 5 s |

---

# GLOBAL CAMERA LANGUAGE

Camera behaves like an architectural documentary.

Never cinematic action.

Never handheld.

Never dramatic.

---

## Camera Specification

```text
Lens
35mm

Height
Human eye level

Movement
Slow Dolly

Rotation
None

Shake
0

Acceleration
Extremely Smooth

Speed
0.12–0.18 m/s
```

Camera never rotates unless explicitly stated.

The visitor should never become aware of the camera.

---

# ENVIRONMENT

One continuous environment.

No scene cuts.

No background replacement.

Only progressive architectural revelation.

Environment Components

- Main Hall
- Stone Floor
- Monumental Entrance
- Silk Installation
- Hidden Research Wing
- Monumental Doors
- Atmospheric Fog
- Volumetric Light

---

# LIGHTING SYSTEM

Beginning

```text
Color Temperature

3200K

Intensity

20%
```

Middle

```text
4200K

40%
```

Ending

```text
5200K

65%
```

Gold highlights only appear after Observation begins.

---

# ACT I

# THE THRESHOLD

## Scroll

0.00–0.15

---

## Purpose

Create silence.

Nothing asks for interaction.

---

## Camera

```text
35mm

Slow push forward

Distance

0.6 meters
```

---

## Environment

Almost dark.

Large doorway.

Single human figure.

Silk barely visible.

---

## Motion

Only atmospheric particles.

Almost static.

Silk displacement

0%

---

## Typography

Appears after 800 ms.

Fade only.

No translation.

```text
Opacity

0→100

Duration

1400 ms

Ease

Ease Out Cubic
```

---

## Audio

Room Tone

Large Stone Hall

Wind

-36 dB

No music.

---

# ACT II

# MATTER

## Scroll

0.15–0.30

---

## Trigger

User crosses 15%.

---

## Wind

Starts.

```text
Velocity

0.18 m/s

Direction

Left → Right

Ramp

1.5 seconds
```

---

## Fabric

Displacement

2%

Then

3.5%

Never exceeds

5%

The movement must resemble heavy woven silk.

Never floating cloth.

---

## Lighting

Key Light

+12%

Fill

+6%

Bounce

+4%

---

## Material Projection

Projected directly onto fabric.

Never floating.

Example

```text
Banarasi Silk

Gold Zari

Handwoven

Varanasi
```

Projection brightness

18%

Blend Mode

Soft Light

---

## Audio

Soft fabric movement.

Tiny air displacement.

No digital sounds.

---

# ACT III

# OBSERVATION

## Scroll

0.30–0.50

---

## Camera

Tiny push.

0.2 meters.

---

## Environment

Light slowly reveals architectural texture.

---

## Projection Layer

Three observations appear.

Not simultaneously.

Spacing

2 seconds.

---

Observation One

```text
Material

Confidence

98%
```

---

Observation Two

```text
Reflection Pattern

Detected
```

---

Observation Three

```text
Luxury Editorial

High Similarity
```

---

Animation

Projected.

Not UI.

Fade

400 ms.

No scaling.

---

Audio

Tiny metallic resonance.

Very subtle.

---

# ACT IV

# REASONING

## Scroll

0.50–0.70

---

Purpose

Environment begins thinking.

---

Knowledge Graph

Thin golden lines.

1 px.

Glow

4%

Opacity

18%

---

Relationships

```text
Silk

↓

Indian Heritage

↓

Temple Geometry

↓

Luxury Weddings

↓

Editorial Lighting
```

Connections grow.

Nothing pops.

Everything draws organically.

---

Camera

Stops.

Environment moves.

---

Lighting

Gold accent

22%

---

Audio

Low harmonic resonance.

Almost inaudible.

---

# ACT V

# THE INSTITUTION

## Scroll

0.70–0.90

---

Doors begin opening.

Duration

3.5 seconds.

Massive weight.

Slow acceleration.

---

Behind doors

Research Library.

Books.

Artifacts.

Stone.

Light.

No people.

---

Navigation

Appears only now.

```text
Institute

Library

Research

Journal
```

Animation

Fade

900 ms

Translation

12 px

No scale.

---

Audio

Stone movement.

Heavy.

Architectural.

---

# ACT VI

# INVITATION

## Scroll

0.90–1.00

---

Camera

Stops.

---

Environment

Complete.

---

Single Typography

```text
Would you like to enter?
```

Fade

700 ms.

---

CTA

```text
Enter the Institute
```

Only interactive element.

---

Hover

Glow

4%

Shadow

None.

No bounce.

---

Click

Environment fades.

Studio loads.

---

# REACT COMPONENT TREE

```text
MovementOne

├── VideoPlate
├── AtmosphereLayer
├── VolumetricFog
├── SilkMaterial
├── MaterialProjection
├── ObservationProjection
├── ReasoningProjection
├── ArchitectureDoors
├── NavigationOverlay
├── InvitationOverlay
└── ScrollController
```

---

# GSAP TIMELINE

```text
Timeline

↓

Atmosphere

↓

Typography

↓

Wind

↓

Fabric

↓

Material Projection

↓

Observation

↓

Knowledge Graph

↓

Architecture

↓

Navigation

↓

Invitation
```

Every animation belongs to one master timeline.

Never independent timelines.

---

# PERFORMANCE BUDGET

Video Resolution

4K Master

Runtime Delivery

1080p

---

Frame Rate

30 fps

---

Maximum JS

< 250 KB

---

GPU

One WebGL Scene

---

Simultaneous Animations

Maximum

3

---

# ASSET MANIFEST

## Video

- Master Plate
- Alpha Plate (optional)

---

## 3D

- Silk Mesh
- Door Geometry
- Fog Volume

---

## Audio

- Room Tone
- Wind
- Silk
- Stone Door
- Resonance

---

## Typography

Editorial Serif

UI Sans

---

# ENGINEERING RULES

No animation begins without a cause.

No transition cuts.

No opacity flicker.

No UI panels.

No loading indicators.

No fake AI effects.

Every movement must feel inevitable.

---

# ACCEPTANCE CRITERIA

Movement I is approved when:

- Visitor feels they entered architecture rather than a webpage.
- Silk behaves like real woven material.
- Intelligence emerges from the environment instead of UI widgets.
- Camera movement is imperceptible.
- Scroll feels continuous.
- There are no visible scene cuts.
- The CTA appears only after trust has been established.
- A first-time visitor can describe the experience as "walking into an institution."

---

# Creative Director Approval

**Status:** APPROVED FOR STORYBOARD

The next production artifact is:

**STORYBOARD-001 — Movement I**

Unlike this production script, the storyboard will visualize every shot, every frame transition, every camera composition, every lighting setup, and every UI overlay. It will become the visual blueprint that AI video generation, React implementation, GSAP choreography, and future art direction all reference.