---
VIS-ID: VIO-002
Title: Entity Model
Version: 1.0.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-29
Depends On:
  - VIS-001
  - VIS-002
  - VIO-001
Next:
  - VIO-003 Relationship Model
---

# Entity Model

## Purpose

This document defines every first-class entity that can exist inside the Visual Intelligence Platform.

Entities are the permanent objects understood by the platform.

Every Visual DNA object, AI Agent, Knowledge Graph node and Memory object references one or more entities.

---

# What is an Entity?

An entity represents something that exists independently inside the creative world.

Examples

Character

Product

Brand

Scene

Camera

Lighting

These are entities.

An entity is NOT

- Prompt
- Response
- Image
- JSON
- API

Those are implementations.

---

# Entity Hierarchy

The ontology is built from nested entities.

```text
Workspace

↓

Project

↓

Campaign

↓

Storyboard

↓

Scene

↓

Frame

↓

Asset
```

This represents creative scope.

---

# Primary Entities

The platform currently defines eighteen primary entities.

## Workspace

Represents the highest organizational boundary.

Contains

Projects

Brands

Users

Knowledge

---

## Project

Represents one creative initiative.

Examples

Wedding Campaign

Summer Collection

Catalog Shoot

Instagram Launch

---

## Campaign

Represents one marketing objective.

Examples

Launch

Festival

Awareness

Conversion

Branding

---

## Storyboard

Represents the sequence of scenes.

Contains

Scene order

Narrative

Transitions

Scene objectives

---

## Scene

Represents one environment and one creative moment.

Examples

Bride entering palace

Product close-up

Walking shot

Lifestyle shot

---

## Frame

Represents one renderable moment.

Image

Video Keyframe

Reference Frame

Thumbnail

---

## Character

Represents a persistent person.

Owns

Character DNA

Recognition Anchors

Appearance

State

---

## Product

Represents the item being promoted.

Examples

Saree

Kurti

Dress

Shoes

Watch

Bag

Jewelry

---

## Brand

Represents brand identity.

Owns

Brand DNA

Positioning

Visual Language

Audience

---

## Environment

Represents physical surroundings.

Examples

Studio

Palace

Temple

Street

Home

Beach

Forest

---

## Camera

Represents image acquisition.

Owns

Lens

Perspective

Composition

Movement

---

## Lighting

Represents illumination.

Owns

Direction

Temperature

Intensity

Mood

Shadows

---

## Color System

Represents visual color language.

Owns

Palette

Contrast

Harmony

Accent

Grading

---

## Motion

Represents movement.

Examples

Walk

Turn

Slow Motion

Tracking

Pan

Zoom

---

## Platform

Represents publishing destination.

Instagram

TikTok

YouTube

Amazon

Shopify

Website

---

## Renderer

Represents execution provider.

GPT Image

Seedance

Higgsfield

Veo

Flux

Kling

Nano Banana

---

## Evaluation

Represents quality analysis.

Owns

Consistency

Scores

Failures

Corrections

---

## Memory

Represents persistent project intelligence.

Owns

Visual DNA

Project History

Knowledge

Previous Decisions

---

# Entity Rules

Rule 1

Entities have identity.

---

Rule 2

Entities own knowledge.

---

Rule 3

Entities may reference other entities.

---

Rule 4

Entities never duplicate ownership.

---

Rule 5

Entities survive generations.

Generated images do not.

---

# Entity Lifecycle

Every entity follows the same lifecycle.

```text
Created

↓

Enriched

↓

Validated

↓

Referenced

↓

Versioned

↓

Archived
```

---

# Ownership

Each entity owns exactly one DNA specification.

Examples

Character

↓

Character DNA

Product

↓

Product DNA

Brand

↓

Brand DNA

Scene

↓

Scene DNA

Camera

↓

Camera DNA

This creates a single source of truth.

---

# Future Extensions

The entity model is intentionally extensible.

Future versions may introduce

Voice

Music

Sound Design

Animation

3D Assets

Locations

Actors

Virtual Influencers

---

# Open Questions

Should Assets become first-class entities?

Should Render Jobs become entities?

Should Experiments become entities?

---

# Engineering Notes

Entities represent business concepts.

Database schemas may differ.

API representations may differ.

The conceptual model remains constant.

Implementation may use graphs, relational databases, document stores, or hybrid systems