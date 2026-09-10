Excellent. I actually think this is the point where the project shifts from **"AI image generator"** to **"Creative Operating System."**

From now on, we're no longer designing screens.

We're designing the **Creative Workspace**—the place where professionals will spend hours, not seconds.

---

# DDD-009

# Campaign Workspace Architecture v1.0 (Draft)

## Vision

The Campaign Workspace is not an image gallery.

It is a **Creative Workspace** where AI and humans collaborate on the same campaign.

The generated assets are not treated as final images.

They remain **living creative objects** that can be art-directed after generation.

---

# Product Philosophy

Current AI tools

```text
Prompt

↓

Generate

↓

Download
```

Atelier

```text
Creative Brief

↓

Creative Planning

↓

Campaign

↓

Creative Workspace

↓

Art Direction

↓

Export
```

Generation is not the end.

It is the beginning.

---

# Workspace Philosophy

The workspace has four persistent regions.

```text
┌────────────────────────────────────────────────────────────┐
│                    TOP COMMAND BAR                         │
├──────────────┬─────────────────────────────┬───────────────┤
│              │                             │               │
│              │                             │               │
│              │                             │               │
│              │      CREATIVE CANVAS        │   INSPECTOR   │
│ BRIEF PANEL  │     (Campaign Board)        │ & AI CONTEXT  │
│              │                             │               │
│              │                             │               │
├──────────────┴─────────────────────────────┴───────────────┤
│                 TIMELINE / ACTIVITY                        │
└────────────────────────────────────────────────────────────┘
```

Notice.

No chat panel.

No feature cards.

No dashboard feel.

This should feel like Figma.

---

# Region 1 — Creative Brief

The left panel never disappears.

It contains the campaign DNA.

Instead of

Upload

Questions

Campaign

Variations

It becomes

```
Creative Brief

──────────────────

Product

Brand

Audience

Campaign Goal

Visual Direction

Deliverables

Output Format

Advanced Settings
```

Everything about the campaign lives here.

---

# Region 2 — Creative Canvas

This is the heart.

Not one image.

A campaign board.

Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━

Hero Image

Portrait

Lifestyle

Close-up Detail

Social Crop

Billboard

━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The campaign is treated as a collection.

Not isolated outputs.

---

# Region 3 — AI Inspector

This is where the magic happens.

Normally

It stays hidden.

When the user selects an object

It appears.

Example

```
Selected

Hair

────────────────

Detected

Loose Bun

Confidence

97%

Editable

✓

───────────────

Art Direct

________________

```

No permanent chatbot.

Contextual intelligence.

---

# Region 4 — Timeline

Not browser history.

Creative history.

```
Upload

↓

Analysis

↓

Generation

↓

Hair Edited

↓

Lighting Updated

↓

Background Changed

↓

Export
```

Undo becomes meaningful.

---

# Semantic Scene Graph

This is the biggest innovation.

Internally

Every campaign becomes

```
Campaign

├── Hero

│

├── Portrait

│

├── Lifestyle

│

└── Detail
```

Each asset

contains

```
Asset

├── Model

├── Hair

├── Face

├── Saree

├── Jewelry

├── Background

├── Props

├── Camera

├── Lighting

├── Typography

└── Color Grade
```

Nothing is treated as pixels.

Everything is meaning.

---

# Object Selection

When hovering

Don't show rectangles.

Instead

Glow the object.

Background softly illuminates.

Hair subtly highlights.

Jewelry sparkles.

Lighting gizmo appears.

Everything should feel

understood.

Not selected.

---

# AI Editing

Flow

```
Hover

↓

Object Highlights

↓

Click

↓

Art Direct

↓

Context Panel Opens

↓

User Instruction

↓

Preview

↓

Apply
```

No generic prompt.

The AI already knows

what you're editing.

---

# Context Awareness

Example

Selected

Background

User writes

```
Royal palace

Golden hour

```

AI understands

```
Object

Background
```

No repetition.

---

# Campaign-wide Editing

Example

User changes

Jewelry.

The AI asks

```
Apply to

○ Current Asset

○ Entire Campaign
```

One click.

---

# Editing Modes

I think there should be four.

---

## 1

Object Mode

Edit

Hair

Jewelry

Background

Props

---

## 2

Asset Mode

Edit

One image.

---

## 3

Campaign Mode

Update

Every asset.

---

## 4

Global Mode

Brand changes.

Typography.

Palette.

Mood.

Everything.

---

# AI Personalities

This is where we differentiate.

The AI isn't one assistant.

It has modes.

```
Creative Director

Photography Director

Fashion Stylist

Lighting Artist

Brand Strategist

Copywriter
```

Depending on what you're editing,

the correct expertise is activated.

---

# Preview System

Never immediately overwrite.

Always

```
Current

↓

Preview

↓

Accept

↓

Reject
```

Professionals need confidence.

---

# Export

Don't just export PNGs.

Export

```
Campaign

↓

Images

Videos

Copy

Metadata

Prompt History

Creative Brief

Brand Guide

License

```

The campaign becomes portable.

---

# Experience Principles

1. The campaign is the primary object.

2. Images are children of the campaign.

3. Objects are children of images.

4. AI edits meaning.

Never pixels.

---

# Laws

LAW 001

Every edit must preserve campaign consistency unless the user explicitly chooses otherwise.

---

LAW 002

The AI must always know what object is selected.

The user should never repeat context.

---

LAW 003

The canvas is sacred.

Nothing covers it unnecessarily.

---

LAW 004

The AI appears only when needed.

Never occupy space permanently.

---

LAW 005

Every refinement should feel like directing a creative team,

not prompting a chatbot.

---

# EIS-009 — Developer AI Handoff

## Objective

Build the Campaign Workspace as a professional creative application, not a gallery.

### Phase 1

* Implement the four-region layout: Command Bar, Creative Brief, Creative Canvas, Inspector, and Timeline.
* Treat the center as a campaign board capable of displaying multiple related assets.

### Phase 2

* Introduce a semantic selection layer. Hovering over editable regions should produce soft, context-aware highlights rather than generic bounding boxes.
* Design the interaction API so selections are represented as semantic entities (e.g., `Background`, `Hair`, `Jewelry`, `Lighting`) rather than raw coordinates.

### Phase 3

* Implement the contextual AI Inspector. It should remain hidden until an editable object is selected, then present the detected object, editable properties, and an "Art Direct" input area.

### Phase 4

* Build the creative history timeline with reversible edits and preview-before-apply behavior.

### Architectural principles

* The workspace shell must remain persistent.
* The Creative Brief remains visible throughout the session.
* The Campaign Canvas has the highest visual priority.
* AI interactions are contextual and should never obscure the artwork.
* Every edit should support both single-asset and campaign-wide application.

---

## One idea I'd like to add before we design the UI

I think we should introduce something that doesn't exist in current AI creative tools:

### **Creative Focus Mode**

When the user selects an object—say, the **hair**—the entire workspace subtly adapts:

* Everything except the selected object gently dims.
* The camera smoothly zooms toward the area of interest.
* The Inspector switches to the **Fashion Stylist** persona automatically.
* Related properties (lighting on the hair, accessories, face framing) become available.
* Pressing **Esc** instantly returns to the full campaign view.

This transforms editing from "clicking a region" into "entering a creative discipline." Selecting lighting feels like stepping into a lighting studio; selecting the background feels like directing a location shoot.

I believe **Creative Focus Mode** has the potential to become one of Atelier's signature interactions, reinforcing the idea that users are collaborating with an AI creative team rather than issuing isolated prompts to an image generator.
