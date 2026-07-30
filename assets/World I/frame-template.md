# FRAME-TEMPLATE.md
# World 01 — Frame Template

Version: 1.0

---

# Purpose

This document defines the universal implementation standard for every frame inside World 01.

Every frame inherits this template.

Only the content, background image, subtle motion and transition target change.

Everything else remains identical.

---

# Layout Philosophy

Environment First

Interface Second

Content Third

The environment is always the primary storyteller.

The UI never competes with the environment.

---

# Viewport

Full Screen

Height:
100vh

Width:
100vw

Background:
16:9 Cinematic Image

Object Fit:
cover

---

# Background Treatment

Apply consistently across every frame.

## Left Gradient

Purpose

Increase text readability.

Opacity

40%

Fade

Black → Transparent

---

## Bottom Gradient

Purpose

Separate foreground reflections from typography.

Opacity

45%

Fade

Black → Transparent

---

## Vignette

Soft

Almost invisible.

Purpose

Guide the eye toward the visual subject.

---

## Film Grain

Opacity

2%

Static

---

# Navigation

Position

Top Right

Items

- Institute
- Research
- Manifesto
- Atlas

Never changes.

---

# Logo

Position

Top Left

Never animated.

---

# Hero Content Container

Maximum Width

680px

Position

Left Aligned

Margin Left

8vw

Margin Top

18vh

Never centered.

---

# Eyebrow

Uppercase

12px

Letter Spacing

0.28em

Weight

500

---

# Headline

Editorial Serif

72–88px

Maximum

Two Lines

---

# Description

Maximum Width

520px

Maximum

3 Lines

Font

18px

Line Height

1.7

---

# CTA

Only when required.

Height

52px

Radius

14px

One Primary Action Only.

---

# Motion Rules

Typography

Fade

↓

Slide Up

20px

↓

Fade Complete

Delay

120ms

Sequence

Eyebrow

↓

Headline

↓

Description

↓

CTA

---

# Environment Motion

Always subtle.

Allowed

- Cloth breathing
- Dust particles
- Water reflections
- Leaf movement
- Atmospheric light shimmer

Forbidden

- Camera shake
- Fast motion
- Lens flare
- Heavy bloom
- Random particles
- Animated UI

---

# Camera Rules

Eye Height

1.65m

Lens

35mm

Look

ARRI Alexa 35

Movement

Extremely Slow Forward Dolly

Maximum

3%

Never orbit.

Never rotate.

Never zoom.

---

# Transition

Current Frame

↓

Camera Push (dolly forward)

↓

Foreground Parallax

↓

Fade to Black

↓

Next Frame Fades In

The transition should feel like walking forward through an uninterrupted architectural space, using the darkness as a threshold.

---

# Empty Space

Content

≈40%

Environment

≈60%

Always preserve negative space.

---

# Universal Design Principles

- Minimal
- Quiet
- Architectural
- Material Driven
- Editorial
- Timeless
- Human Scale
- Cinematic

Every new frame should feel like another moment inside the same institution rather than a new webpage.