# COMPONENTS.md
# Atelier OS
## Component Design System

Version: 1.0
Status: LOCKED

---

# Philosophy

Components should never become the visual identity.

The experience is defined by architecture, typography, whitespace and materials.

Components simply facilitate interaction.

Every component should disappear behind the user's creativity.

---

# Component Hierarchy

Primary

Workspace

↓

Secondary

Panels

↓

Tertiary

Interactive Components

↓

Utility Components

Never allow utility components to compete with the workspace.

---

# Workspace Canvas

Purpose

Primary creative surface.

Examples

- Material Viewer
- Moodboard
- Campaign
- Canvas
- Image Generation

Rules

- Largest component on screen
- Always central
- Maximum whitespace
- No visible border
- No card styling

The workspace is never treated like a widget.

---

# Navigation

Type

Persistent Sidebar

Contents

- Campaign Studio
- Material Library
- Atlas
- Research
- Knowledge
- Archive
- Settings

Rules

Typography first.

Icons secondary.

No floating navigation.

No glowing active states.

Active item indicated using:

- typography weight
- subtle background
- left indicator

---

# Buttons

## Primary Button

Material

Apple Liquid Glass

Purpose

Primary actions

Examples

- Generate
- Enter Atelier
- Publish
- Create Campaign

Style

- Transparent
- Frosted glass
- Large radius
- Thin white outline
- White typography

Hover

Glass clarity increases.

Arrow shifts slightly.

Lift

2px

Click

Natural compression.

---

## Secondary Button

Text only.

No background.

Minimal interaction.

Used for

- Cancel
- Back
- Skip

---

## Ghost Button

Transparent.

Thin outline.

No fill.

Used sparingly.

---

# Search

Purpose

Universal search.

Style

Apple Liquid Glass.

Large input.

Rounded.

Minimal placeholder.

No borders.

Always accessible.

Supports

- Campaigns
- Materials
- Knowledge
- Research
- Commands

---

# Inputs

Style

Minimal.

Editorial.

Soft glass.

Large touch target.

No heavy outlines.

Labels remain outside.

Never inside placeholders only.

---

# Textarea

Supports

Creative prompting.

Notes.

Reasoning.

Research.

Expandable.

Comfortable reading width.

---

# Dropdown

Glass surface.

Rounded.

Minimal separators.

Large touch targets.

Opens smoothly.

No harsh shadows.

---

# Toggle

Simple capsule.

Subtle animation.

No bright colours.

---

# Checkbox

Minimal square.

Rounded corners.

Soft animation.

---

# Radio

Minimal circular indicator.

Typography remains primary.

---

# Sliders

Thin.

Elegant.

Used only where visual adjustment is required.

Never decorative.

---

# Upload Zone

Purpose

Material upload.

Large.

Editorial.

Minimal outline.

Drag & Drop supported.

States

Empty

Hover

Uploading

Analyzing

Completed

The upload should feel like placing a material onto an architect's table.

---

# Material Viewer

Purpose

Primary visual workspace.

Features

- Zoom
- Pan
- Fullscreen
- Compare
- Annotate

Rules

Image always dominates.

No unnecessary chrome.

Large presentation.

---

# Knowledge Panel

Purpose

Displays institutional knowledge.

Sections

- Evidence
- References
- Related Knowledge
- Material DNA

Never feels like documentation.

Should resemble an editorial notebook.

---

# Reasoning Panel

Purpose

Shows Atelier's thinking.

Contains

- Observation
- Reasoning
- Evidence
- Confidence
- Creative Recommendation

Reasoning streams naturally.

Not instantly.

---

# Conversation Panel

Purpose

Creative collaboration.

Messages

User

↓

Atelier

Supports

Images

Files

Knowledge references

Campaign context

Always contextual.

Never isolated chat.

---

# Moodboard Grid

Purpose

Visual exploration.

Supports

Selection

Comparison

Expansion

Approval

Never use masonry.

Consistent spacing.

Editorial rhythm.

---

# Generation Queue

Purpose

Track generation progress.

Displays

- Status
- Current Task
- ETA
- Result

Never blocks the workspace.

---

# Timeline

Purpose

Campaign history.

Shows

- Uploads
- Decisions
- Reasoning
- Generations
- Refinements

Always chronological.

---

# Notifications

Small.

Bottom corner.

Fade.

Disappear automatically.

Never interrupt.

---

# Toast

Purpose

Quick confirmation.

Duration

3–5 seconds.

Examples

Campaign Saved

Export Ready

Generation Complete

---

# Modal

Purpose

Focused decisions.

Background blur.

Minimal actions.

Large whitespace.

No clutter.

---

# Drawer

Slides from the right.

Used for

Knowledge

References

Research

History

Does not replace the workspace.

---

# Tabs

Simple editorial tabs.

Typography only.

Thin active indicator.

No filled pills.

---

# Accordion

Used for long reasoning.

Opens smoothly.

Maintains reading rhythm.

---

# Breadcrumb

Minimal.

Typography only.

Displays

Workspace

↓

Campaign

↓

Current Context

---

# Progress Indicator

Never percentage only.

Explain progress.

Example

Observing Material

Searching Knowledge

Constructing Reasoning

Generating Concepts

---

# Loading State

Replace spinners.

Show meaningful activity.

Always communicate what Atelier is doing.

---

# Empty State

Simple.

One action.

No illustrations.

Examples

Upload your first material.

Create your first campaign.

---

# Cards

Traditional cards are discouraged.

When required

Use

Editorial Panels

Large spacing.

Soft surfaces.

Minimal borders.

---

# Tooltips

Short.

Helpful.

Never instructional.

Appear instantly.

Disappear naturally.

---

# Avatar

Atelier has no human avatar.

Presence is communicated through typography and reasoning.

Never use robot illustrations.

---

# Cursor

Standard cursor.

Interactive elements subtly respond.

Never create novelty cursors.

---

# Scrollbar

Thin.

Minimal.

Low contrast.

Visible only when needed.

---

# Apple Liquid Glass Components

Glass is reserved only for:

-- Primary Buttons
- Search
- Inputs
- Floating Controls
- Dropdowns
- Command Palette
- Context Menus

Glass should never be used for:

- Cards
- Layout containers
- Panels
- Entire windows
- Decorative backgrounds

Glass communicates interaction.

Never structure.

---

# Dividers

Dividers are subtle.

Prefer whitespace over lines.

If required

Use

1px

Low opacity

Warm grey

Never divide every section.

---

# Status Indicators

Purpose

Communicate state.

States

- Idle
- Thinking
- Processing
- Complete
- Warning
- Error

Avoid saturated colors.

Status should be readable through both typography and iconography.

---

# AI Thinking Indicator

Purpose

Represent Atelier's active reasoning.

Instead of

...

Use

Observing material...

Comparing references...

Searching institutional knowledge...

Building creative direction...

Reasoning should feel transparent.

---

# Evidence Card

Purpose

Display supporting evidence.

Contains

- Source
- Confidence
- Summary
- Related Campaigns

Always collapsible.

Editorial presentation.

Never excessive metadata.

---

# Reference Card

Purpose

Display historical or visual references.

Contains

- Preview
- Title
- Origin
- Category

Supports quick expansion.

---

# Material DNA Card

Purpose

Summarize extracted material intelligence.

Contains

- Material
- Weave
- Texture
- Reflectance
- Surface Behaviour
- Lighting Profile
- Confidence

Should feel like a museum catalogue.

---

# Confidence Indicator

Purpose

Explain AI certainty.

Uses

High

Medium

Low

Never display arbitrary percentages without context.

Confidence should always include reasoning.

---

# Command Palette

Purpose

Universal command interface.

Supports

- Search
- Navigation
- Actions
- AI Commands
- Recent Campaigns

Opens instantly.

Keyboard-first.

Minimal interface.

---

# Context Menu

Purpose

Expose secondary actions.

Appears near interaction point.

Compact.

Typography-first.

Soft glass.

No unnecessary icons.

---

# Image Comparison

Purpose

Compare generated assets.

Modes

- Side by Side
- Overlay
- Slider
- Before / After

Transition should be smooth.

Never disorienting.

---

# Version History

Purpose

Navigate campaign evolution.

Each version contains

- Timestamp
- Creative Direction
- Prompt
- Reasoning
- Generated Assets

Users can restore any version without losing later work.

---

# Export Panel

Purpose

Prepare final delivery.

Contains

- Asset Selection
- Format
- Resolution
- Metadata
- Creative Summary

Export should feel like publishing, not downloading.

---

# Accessibility Components

Every interactive component must support

- Keyboard navigation
- Screen readers
- Focus indicators
- Reduced motion
- High contrast

Accessibility is foundational.

Never optional.

---

# Responsive Behaviour

Components adapt.

They never shrink into unusable sizes.

Priority

1. Workspace

2. Primary Actions

3. Supporting Intelligence

4. Utilities

Creative work always remains visible.

---

# Component Consistency

Every component must share

- Typography
- Corner radius
- Motion language
- Spacing rhythm
- Material language
- Elevation rules

Consistency builds trust.

---

# Component Rules

Every component should answer

Why does this exist?

If the answer is

"because most dashboards have one"

it should be removed.

Every component must directly support creative thinking.

---

# Forbidden Components

Never use

✗ KPI Cards

✗ Analytics Widgets

✗ Colorful Dashboards

✗ Floating FAB Buttons

✗ Neon Badges

✗ Excessive Notifications

✗ Decorative Icons

✗ Empty Widget Boxes

✗ Marketing Banners

✗ Carousels

✗ Gamification

✗ Confetti

✗ AI Robot Mascots

✗ Over-designed Controls

---

# Success Criteria

The component library should feel invisible.

Users should remember the creative work they produced, not the interface they interacted with.

Every component should quietly support Atelier's philosophy:

**Architecture over software.**

**Creativity over complexity.**

**Calmness over clutter.**

**Materials over widgets.**

**Intelligence over automation.**