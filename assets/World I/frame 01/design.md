# FRAME-001.md
# World 01 — Frame 01
## The Invitation

Version: v1.0 (Locked)

---

# Objective

Frame 01 is the first visual experience of the website.

It is not a hero banner.
It is not a SaaS landing page.

It is the entrance to a creative institution.

The visitor should immediately feel calm, curious and invited to explore.

The environment is the protagonist.
The interface exists only to support it.

---

# Layout Philosophy

Environment First.

UI Second.

Content Third.

The visitor should first notice the architecture.
Then the atmosphere.
Only then should they begin reading.

Nothing should compete with the environment.

---

# Screen Layout

The entire screen is occupied by the background image.

The UI floats above the image.

No cards.

No glassmorphism.

No floating containers.

No unnecessary borders.

Everything should feel integrated into the architecture.

---

# Content Placement

## Logo

Position:
Top Left

Margin:
8vw from left
6vh from top

Maximum Width:
120px

Behavior:
Static

---

## Navigation

Position:
Top Right

Items:

- Institute
- Research
- Manifesto
- Atlas

Spacing:
40px

Font Size:
15px

Weight:
400

Opacity:
85%

Hover:
Only a gentle opacity transition.

No underline.

No scaling.

---

# Hero Content

Position:

Approximately

18vh from top

8vw from left

Maximum Width:

680px

Everything remains left aligned.

---

## Eyebrow

Text:

CREATIVE INTELLIGENCE INSTITUTE

Font Size:

12px

Letter Spacing:

0.28em

Weight:

500

Opacity:

70%

Color:

Warm Ivory

---

## Headline

Text:

Where Creativity
Becomes Intelligence

Maximum Width:

620px

Font:

Editorial Serif

Weight:

Medium

Desktop Size:

72–88px

Line Height:

0.95

The headline should occupy only two lines.

---

## Description

Maximum Width:

520px

Maximum:

3 lines

Text:

The world's first creative institution where
materials, research and intelligence converge
to shape what has never existed before.

Font Size:

18px

Line Height:

1.7

Opacity:

90%

---

## CTA

Text:

Enter the Institution

Only one primary button.

Height:

52px

Padding:

18px 32px

Corner Radius:

14px

The button should feel premium.

Hover:

Very subtle brightness increase.

No scaling.

---

# Scroll Indicator

Position:

Bottom Center

Text:

Scroll to Enter

Very small.

Only accompanied by a thin vertical line that slowly moves.

---

# Background

Frame 01 occupies the entire viewport.

Use:

object-fit: cover

No zooming.

No rotation.

No image movement while idle.

---

# Image Treatment

## Left Gradient

Apply a soft black gradient from the left.

Purpose:

Improve readability without being visible.

Suggested:

40% black
→ transparent

---

## Bottom Gradient

Apply another soft gradient.

Purpose:

Separate content from lower reflections.

Suggested:

45% black
→ transparent

---

## Vignette

Very soft.

Edges only.

Almost invisible.

Purpose:

Guide visual attention toward the doorway.

---

## Film Grain

Opacity:

2%

Static.

Not animated.

---

# Color

Primary Text:

Warm Ivory

Approximate:

#F5F0E8

Never use pure white.

---

# Empty Space

Content should occupy approximately

40%

of the horizontal space.

The remaining

60%

belongs entirely to the architecture.

Resist filling empty space.

Luxury comes from restraint.

---

# Motion

No entrance animation on page load.

The environment already exists.

Only the typography fades in.

Sequence:

Eyebrow

↓

Headline

↓

Description

↓

CTA

Each delayed by approximately

120ms

Animation:

Opacity

+

20px vertical movement

Duration:

0.8s

Ease:

Power2.out

---

# Idle Environment

The environment must feel alive without drawing attention.

Allowed:

- Soft fabric breathing
- Tiny dust particles
- Gentle water reflections
- Slight leaf movement
- Atmospheric light shimmer

Forbidden:

- Camera shake
- Dramatic cloth motion
- Fast particles
- Lens flares
- Heavy bloom

---

# Scroll Behaviour

The first scroll does not immediately transition to Frame 02.

Instead:

Camera performs a forward push towards the doorway.

Approximately:

10-15% (deeper than the idle state).

Foreground elements exhibit gentle parallax.

As the camera pushes through the doorway, the screen smoothly transitions into a **fade to black**.

Only after the screen is fully black does the transition to Frame 02 begin.

---

# Design Rules

Never use:

- Floating UI cards
- Glassmorphism
- Bright gradients
- Large shadows
- Neon colors
- Over-animated interfaces
- Bouncing elements

Always prioritize:

Silence

Space

Architecture

Material

Light

Calmness

---

# Emotional Goal

The user should feel:

"I've entered somewhere important."

Not

"I've opened a website."

This distinction defines the entire experience.

Frame 01 establishes the visual language for every frame that follows.