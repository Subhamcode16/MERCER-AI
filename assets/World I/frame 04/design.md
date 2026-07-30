# FRAME-004-DESIGN.md
# World 01 — Frame 04
## The Observation

Version: v3.0 (Slider Redesign)
Status: DRAFT

---

# Philosophy

Frame 04 acts as a breathing space. It intentionally breaks the architectural immersion established by Frames 01–03.

Instead of a cinematic, spatial environment, the interface drops into a stark, typographic void. The environment disappears, and a pure, focused editorial layout takes over. The institution itself speaks. 

This creates visual rest and forces the user to focus entirely on the core concepts before the cinematic journey resumes in Frame 05.

---

# Experience Goal

The visitor should feel
"I'm reading the institution's core principles."
A moment of pure, undistracted focus.

---

# Background

Static plain background. Pitch black (or dark ambient tone from the global palette). 
Completely dropping the architectural environment from Frame 03.
No motion in the background.

---

# Layout

The screen is divided into a Header and two main columns.

---------------------------------------------------
HEADER (Top Center)
Headline & Description
---------------------------------------------------
LEFT COLUMN (50%)         RIGHT COLUMN (50%)
Typographic Slider        Image Showcase
---------------------------------------------------

No background elements. Generous negative space must be maintained at all times to preserve the "spacing psychology" of the brand.

---

# Header

Position: Top Center
Alignment: Center
Padding-top: 10vh (to keep it anchored but breathing)

## Headline
Text: Every details becomes knowledge
Size: Large (e.g., 48px or 64px)
Style: Editorial, Warm Ivory, High Contrast

## Description
Text: Observation is the beginning of intelligence. Every material, shadow, texture and form becomes structured knowledge before it becomes creativity.
Size: Small (e.g., 15px)
Style: Warm Ivory, 60% Opacity, Max-width 600px for comfortable reading.
Spacing: Placed comfortably below the headline.

---

# Left Column: Typographic Slider

Position: Left side, spanning the vertical height below the header.
Width: 50%
Padding-left: 8vw

A vertical list of observation concepts.
Scrolling acts as a trigger to slide this list up and down. The global page background does not scroll.

## The 6 Observations
- Material Study
- Botanical Reference
- Light Analysis
- Historical Archive
- Human Perception
- Visual Intelligence

## Typography & States

**Active State:**
- Bright White / Warm Ivory (100% Opacity)
- Bold / Medium weight
- Preceded by an arrow indicator (e.g., `-> Material Study`)
- Positioned in the vertical center of the left column (the active reading zone).

**Inactive State:**
- Dimmed (20-30% Opacity)
- Depth-of-field blur effect applied (mimicking a camera lens focusing solely on the active word).
- No arrow indicator.

---

# Right Column: Image Showcase

Position: Right side, dead center vertically within its column.
Width: 50%
Padding-right: 8vw

Only one image appears at a time, corresponding exactly to the active observation in the left column.

## Image Sizing & Placement
- Large, but strictly NOT full-screen height.
- Must maintain the generous spacing psychology.
- Recommended dimensions: ~400 × 550px (Portrait ratio) or scaled to maintain significant padding on all sides.
- Images stack over one another centrally.
- Use subtle, real reference photography. No illustrations. No icons.

---

# Interaction & Motion

## Scroll Behavior
- The global background remains fixed. 
- The user scrolls to navigate the typographic slider. The words move vertically.

## Image Transitions
- Simple, smooth **Fade In / Fade Out**.
- As a new word enters the "active zone", the previous image fades out, and the new image fades in.
- No sliding, scaling, or bouncing for the images.
- Duration: 500ms
- Ease: Power2.out

---

# Transition to Frame 05

After scrolling past the final observation ("Visual Intelligence"):
The interface slowly fades to black.
The typographic slider and header disappear.
The architectural environment of Frame 05 slowly fades in.
Ambient motion and camera movement resume.