# MOTION.md
# Atelier OS
## Motion Design System

Version: 1.0
Status: LOCKED

---

# Philosophy

Motion is not decoration.

Motion communicates intention.

Every animation should explain what is happening, where attention should move, and how the interface is responding.

If an animation cannot justify its existence, it should not exist.

The user should never notice the animation itself.

They should only notice that the experience feels natural.

---

# Motion Principles

Always

✓ Calm

✓ Intentional

✓ Architectural

✓ Physical

✓ Continuous

✓ Predictable

✓ Elegant

✓ Subtle

✓ Functional

Never

✗ Playful

✗ Bouncy

✗ Flashy

✗ Gamified

✗ Over-animated

✗ Distracting

✗ Decorative

✗ Loud

---

# Motion Language

The Atelier interface behaves like architecture.

Walls do not slide.

Concrete does not bounce.

Light does not snap.

Everything transitions naturally.

Movement should feel like:

- walking through a museum
- sunlight moving across concrete
- linen responding to soft air
- turning pages in an editorial book

---

# Motion Hierarchy

Primary Motion

Workspace transitions

↓

Secondary Motion

Panel transitions

↓

Tertiary Motion

Micro interactions

↓

Ambient Motion

Light

Particles

Glass

---

# Timing

Micro Interaction

120–180ms

Hover

200–300ms

Panel Transition

350–500ms

Workspace Transition

600–900ms

Scene Transition

1000–1500ms

Never animate slower than necessary.

Never animate faster than comfortable reading.

---

# Easing

Default

ease-out

Entrance

ease-out

Exit

ease-in

Continuous Motion

linear

Avoid exaggerated easing curves.

Motion should feel physically believable.

---

# Workspace Transitions

Changing workspaces should feel like moving deeper into the institution.

Never feel like changing pages.

The camera remains mentally continuous.

No flashes.

No route jumps.

No full-screen reloads.

---

# Navigation Motion

Navigation does not slide aggressively.

Active sections gently fade.

Typography changes weight.

Glass indicators glide softly.

The interface should never shake.

---

# Panel Behaviour

Panels fade.

Panels never pop.

Opacity

↓

Small vertical movement

↓

Settle

Maximum movement

16–24px

---

# Sidebar

Opening

Soft horizontal reveal.

Closing

Soft fade.

No snapping.

No scaling.

---

# Modal Behaviour

Modals feel like architectural overlays.

Background softly blurs.

Opacity increases.

Modal gently rises.

Never bounce.

Never zoom dramatically.

---

# Hover Behaviour

Hover communicates possibility.

Glass becomes slightly clearer.

Border brightness increases subtly.

Scale

1.02 maximum

Elevation

2px maximum

Arrow icons may shift slightly.

Nothing else moves.

---

# Click Behaviour

Buttons compress naturally.

Scale

0.98

Duration

120ms

Release immediately.

Never use exaggerated click animations.

---

# Loading Behaviour

Loading is communication.

Never show empty spinners.

Instead reveal:

Observing...

Reasoning...

Searching Knowledge...

Building Direction...

Generating...

The interface should feel alive.

---

# AI Behaviour

AI responses appear progressively.

Reasoning arrives first.

Evidence follows.

Knowledge expands naturally.

The interface should feel like thinking.

Not rendering.

---

# Typography Motion

Typography fades.

Never slides dramatically.

Never rotates.

Never scales excessively.

Opacity

↓

Translate Y

↓

Settle

Maximum movement

12px

---

# Image Behaviour

Images fade into place.

Never zoom.

Never rotate.

Never bounce.

When replaced

Crossfade.

Maintain composition.

---

# Material Viewer

Uploaded materials remain stable.

Zooming feels physical.

Panning remains smooth.

Lighting previews fade naturally.

The material always remains the hero.

---

# Glass Behaviour

Glass does not animate continuously.

Only interaction changes it.

Hover

Slightly clearer.

Focus

Slight refraction.

Click

Natural compression.

Glass should always feel solid.

---

# Scroll Behaviour

Scrolling is cinematic.

The interface should feel like travelling.

No snapping.

No parallax overload.

No excessive sticky behaviour.

Motion should guide attention.

Not compete for it.

---

# Ambient Motion

The interface always feels alive.

Examples

Subtle light movement.

Very soft gradient evolution.

Tiny glass reflections.

Gentle cursor reactions.

Nothing should loop noticeably.

---

# Notifications

Fade in.

Remain.

Fade out.

No bouncing.

No sliding across the screen.

Notifications should feel polite.

---

# Success States

Success should feel calm.

Small checkmark.

Soft fade.

Muted green.

No celebration.

---

# Error States

Errors appear gently.

Muted brick red.

Helpful explanation.

No shaking.

No flashing.

No alarming behaviour.

---

# Focus States

Keyboard focus should be obvious.

Soft glow.

Thin outline.

Never overpower the interface.

Accessibility remains first.

---

# Workspace Evolution

As the user works,

the interface evolves.

Panels appear.

Reasoning expands.

Knowledge grows.

Nothing suddenly replaces existing content.

The workspace should feel like ideas accumulating on an architect's desk.

---

# AI Conversation

Messages appear naturally.

Streaming text.

Thoughtful pauses.

Evidence unfolds progressively.

The AI should feel like it is genuinely thinking.

---

# Full Screen Transitions

Transitions between major experiences should preserve continuity.

Landing Page

↓

Enter Atelier

↓

Workspace

Should feel like one uninterrupted camera journey.

Never like loading a different application.

---

# Performance

Target

60 FPS

Avoid layout shifts.

GPU-accelerated transforms.

Opacity and transform animations preferred.

Avoid animating width, height or expensive layout properties.

---

# Motion Accessibility

Support reduced motion.

When enabled:

Remove ambient animations.

Reduce transition durations.

Disable non-essential movement.

Preserve hierarchy through opacity only.

---

# Motion Rules

Every animation must answer:

What changed?

Why did it change?

Where should the user look next?

If those questions cannot be answered,

the animation should not exist.

---

# Success Criteria

Users should never remember the animations.

They should remember how calm, effortless and natural Atelier felt.

Motion should become invisible.

The interface should behave less like software and more like a thoughtfully designed architectural space where creativity unfolds naturally.