---
VIS-ID: VIO-003
Title: Relationship Model
Version: 1.0.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-29
Depends On:
  - VIS-001
  - VIS-002
  - VIO-001
  - VIO-002
Next:
  - VIO-004 Creative Semantic Model
---

# Relationship Model

## Purpose

Entities alone cannot express creative intent.

The Relationship Model defines how entities connect to each other to form a coherent creative world.

Every AI reasoning process, memory lookup, knowledge graph traversal, evaluation, and prompt compilation depends on these relationships.

---

# Philosophy

Entities represent **things**.

Relationships represent **meaning**.

Without relationships the platform becomes a database.

With relationships it becomes intelligence.

---

# Types of Relationships

The Visual Intelligence Platform recognizes seven categories of relationships.

---

## 1. Structural Relationships

Describe hierarchy.

Example

Workspace

contains

Project

Project

contains

Campaign

Campaign

contains

Storyboard

Storyboard

contains

Scene

Scene

contains

Frame

---

## 2. Ownership Relationships

Describe permanent ownership.

Character

owns

Character DNA

Brand

owns

Brand DNA

Product

owns

Product DNA

Ownership is unique.

A DNA object MUST have exactly one owner.

---

## 3. Composition Relationships

Describe objects built from smaller objects.

Example

Scene

contains

Environment

contains

Lighting

contains

Props

contains

Characters

contains

Products

Composition defines what exists together.

---

## 4. Dependency Relationships

Describe decision dependencies.

Example

Audience

influences

Styling

Styling

influences

Photography

Photography

influences

Prompt

Dependencies form the reasoning graph.

---

## 5. Temporal Relationships

Describe sequence.

Examples

Scene A

before

Scene B

Frame 5

after

Frame 4

Campaign

begins

Launch Phase

Temporal reasoning becomes critical for video generation.

---

## 6. Semantic Relationships

Describe meaning.

Examples

Banarasi

is-a

Silk Saree

Wedding Campaign

requires

Traditional Styling

Luxury

associated-with

Warm Lighting

Semantic relationships enable intelligent reasoning.

---

## 7. Reference Relationships

Describe reuse.

Campaign

references

Brand DNA

Scene

references

Character DNA

Prompt

references

Visual DNA

Memory

references

Previous Campaign

Reference relationships eliminate duplication.

---

# Cardinality

Relationships define quantity.

Examples

Project

contains

Many Campaigns

Campaign

contains

Many Storyboards

Storyboard

contains

Many Scenes

Scene

contains

Many Frames

Frame

contains

One Camera Setup

Frame

contains

One Lighting Setup

Frame

contains

Multiple Characters

Frame

contains

Multiple Products

---

# Relationship Rules

Rule 1

Relationships are directional.

Brand

owns

Brand DNA

does not imply

Brand DNA

owns

Brand.

---

Rule 2

Relationships must be explicit.

Nothing is assumed.

---

Rule 3

Relationships may have attributes.

Example

Character

wears

Product

Attributes

Start Frame

End Frame

Visibility

Priority

---

Rule 4

Relationships may evolve.

Example

Character

wears

Saree

Scene 1

Character

wears

Lehenga

Scene 5

The Character remains identical.

Only the relationship changes.

---

Rule 5

Relationships are versioned.

Creative reasoning depends on historical context.

---

# Example Graph

Project

↓

contains

↓

Campaign

↓

contains

↓

Storyboard

↓

contains

↓

Scene

↓

contains

↓

Character

↓

wears

↓

Product

↓

captured-by

↓

Camera

↓

lit-by

↓

Lighting

↓

published-to

↓

Platform

---

# Query Examples

The platform should answer questions such as

Show every Scene containing Character X.

Show every Campaign using Brand DNA Version 2.

Find all Products worn during Wedding scenes.

Retrieve every Frame using Warm Lighting.

List every Campaign targeting Instagram.

Relationships enable these queries.

---

# Future Extensions

Relationships may later include

- Confidence
- Probabilities
- Causal strength
- Evidence
- User feedback
- Performance metrics

---

# Open Questions

Should relationships themselves maintain memory?

Should relationships support inheritance?

How should conflicting relationships be resolved?

---

# Engineering Notes

Relationships are conceptual.

Implementation may use:

- Graph databases
- Relational joins
- Document references
- Hybrid knowledge graphs

The conceptual model remains independent of implementation.