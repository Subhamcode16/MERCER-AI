# MOTION-001 — Movement I: Motion Timeline

**Version:** 1.0  
**Status:** Production Ready  
**Movement:** I — The Threshold  
**Duration:** 35–45 Seconds  
**Animation Engine:** GSAP + ScrollTrigger + React Three Fiber  
**Purpose:** Define every movement, animation, transition, easing curve, and timing for engineering implementation.

---

# Philosophy

Movement is never decorative.

Movement is communication.

Nothing animates because scrolling occurred.

Everything animates because something in the environment caused it.

The visitor should never perceive animations.

They should perceive the environment evolving naturally.

---

# Motion Hierarchy

Every animated object belongs to one priority level.

```text
Level 01
Environment

↓

Level 02
Atmosphere

↓

Level 03
Materials

↓

Level 04
Light

↓

Level 05
Knowledge

↓

Level 06
Typography

↓

Level 07
Navigation

↓

Level 08
Interaction
```

Lower levels never animate before higher levels.

---

# Master Timeline

```text
0.00 ────────────────────────────── 1.00

Threshold

Matter

Observation

Reasoning

Institution

Invitation
```

One master GSAP timeline.

No independent timelines.

---

# Timeline 01

## Threshold

### Scroll

0.00 → 0.15

---

## Camera

```yaml
position:
  z: -0.8m → -0.2m

duration:
  5s

easing:
  easeInOutCubic

rotation:
  none
```

---

## Fog

Opacity

```yaml
10% → 18%
```

Noise

```yaml
very low
```

Velocity

```yaml
0.02m/s
```

---

## Typography

Delay

```yaml
800ms
```

Opacity

```yaml
0 → 100%
```

Duration

```yaml
1400ms
```

Blur

```yaml
8px → 0px
```

Translation

```yaml
0px
```

Scale

```yaml
100%
```

---

## Audio

Fade

```yaml
0 → -28db

Duration

3s
```

---

# Timeline 02

## Matter Awakens

### Scroll

0.15 → 0.30

---

## Wind

Starts gradually.

```yaml
velocity:
  0 → 0.18m/s

duration:
  1.8s

direction:
  left_to_right
```

---

## Silk

Displacement

```yaml
0%

↓

2%

↓

3.5%
```

Frequency

```yaml
very slow
```

Material response

```yaml
heavy woven silk
```

Never behaves like satin.

Never behaves like lightweight cloth.

---

## Dust Particles

Spawn

```yaml
20

↓

120
```

Opacity

```yaml
8%
```

Randomness

```yaml
very low
```

---

## Light

Intensity

```yaml
20%

↓

34%
```

Temperature

```yaml
3200K

↓

3900K
```

---

# Timeline 03

## Observation

### Scroll

0.30 → 0.50

---

## Camera

Forward

```yaml
0.25m
```

Speed

```yaml
extremely slow
```

---

## Material Projection

Projection One

```yaml
fade:
400ms

hold:
2s

fade_out:
300ms
```

Pause

800ms

Projection Two

Same timing.

Projection Three

Same timing.

---

## Projection Rules

No scaling.

No bouncing.

No floating.

Projection follows cloth deformation.

---

## Surface Tracking

Projection anchors to fabric vertices.

Every fold updates projection coordinates.

---

# Timeline 04

## Reasoning

### Scroll

0.50 → 0.70

---

## Knowledge Graph

Growth

```yaml
draw_speed:
40px/s

opacity:
0 → 18%

line_width:
1px
```

---

## Node Glow

```yaml
0%

↓

6%
```

Never exceeds

8%.

---

## Camera

Stops.

Only environment evolves.

---

## Light

Gold bounce

```yaml
4%

↓

18%
```

---

## Fog

Density

```yaml
18%

↓

12%
```

Knowledge should become clearer.

---

# Timeline 05

## Institution

### Scroll

0.70 → 0.90

---

## Doors

Rotation

```yaml
0°

↓

92°
```

Duration

```yaml
3.8s
```

Weight

Heavy.

Momentum.

No easing bounce.

---

## Library Reveal

Opacity

```yaml
0%

↓

100%
```

Exposure

```yaml
+0.8
```

---

## Navigation

Fade

```yaml
0%

↓

100%
```

Translation

```yaml
12px

↓

0px
```

Duration

```yaml
900ms
```

---

# Timeline 06

## Invitation

### Scroll

0.90 → 1.00

---

## Camera

Stops completely.

No movement.

---

## CTA

Opacity

```yaml
0%

↓

100%
```

Duration

```yaml
700ms
```

Hover

```yaml
glow:
4%

scale:
100%

shadow:
0
```

Click

```yaml
environment fades

↓

transition begins

↓

Movement II loads
```

---

# Universal Motion Rules

## Rule 01

Maximum simultaneous animations

```yaml
3
```

---

## Rule 02

Nothing accelerates instantly.

Everything ramps.

---

## Rule 03

No elastic easing.

Never.

---

## Rule 04

No overshoot.

---

## Rule 05

No bounce.

---

## Rule 06

Motion should feel heavy.

Not digital.

---

# Easing Library

```yaml
Environment:
easeInOutCubic

Typography:
easeOutQuart

Doors:
easeInOutExpo

Camera:
CustomBezier_01

Fabric:
PhysicsSimulation

Knowledge:
Linear
```

These easing presets become global tokens.

---

# ScrollTrigger Map

```text
Movement01

Start

↓

Threshold

↓

Matter

↓

Observation

↓

Reasoning

↓

Institution

↓

Invitation

↓

Complete
```

Every act occupies a fixed percentage of scroll.

No overlap.

---

# Animation Ownership

| Layer | Engine |
|----------|------------|
| Camera | GSAP |
| Typography | GSAP |
| Navigation | GSAP |
| Silk Physics | Three.js |
| Fog | Three.js Shader |
| Dust | GPU Particles |
| Knowledge Graph | SVG + GSAP |
| Lighting | Three.js |
| Video Plate | HTML Video |

---

# React State Machine

```text
Idle

↓

Threshold

↓

Matter

↓

Observation

↓

Reasoning

↓

Institution

↓

Invitation

↓

Complete
```

Each state activates only its own animation layer.

---

# Performance Constraints

Maximum frame time

```yaml
16ms
```

Target FPS

```yaml
60fps
```

Maximum GPU particle count

```yaml
500
```

Maximum simultaneous shaders

```yaml
3
```

Maximum video bitrate

```yaml
12Mbps
```

---

# Acceptance Criteria

Movement is approved when:

- No animation appears decorative.
- Scroll feels like walking.
- Camera movement is almost imperceptible.
- Silk behaves according to physical material properties.
- Knowledge emerges from the environment rather than UI widgets.
- The visitor never perceives a scene cut.
- All transitions are motivated by environmental change.

---

# Next Artifact

## AUDIO-001 — Movement I Sound Bible

The next document defines:

- Spatial audio layout
- Room acoustics
- Material sound signatures
- Wind behavior
- Cloth resonance
- Stone movement
- Dynamic volume curves
- Silence timing
- Audio middleware implementation
- Trigger map
- Mixing specifications

This document will ensure the experience is not only seen but also *felt* through sound.