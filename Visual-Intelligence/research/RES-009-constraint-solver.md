---
Title: Constraint-Based Image Formation
ID: RES-009
Status: Draft
Owner: Visual Intelligence Research
Last Updated: 2026-07-01
Depends On:
  - ARC-001
  - VIO-012
---

# RES-009: Constraint-Based Image Formation

## Purpose

This document outlines the algorithmic framework for the **Image Formation Intelligence** engine (formerly the Lighting Engine).

The engine abandons static string concatenation (e.g., "Banarasi" + "Golden Hour") in favor of **Constraint Satisfaction**.

## 1. The Core Concept

Lighting, camera perspective, and color grading are no longer owned by the Vibe. Instead, they are *derived* solutions to a set of physical and semantic constraints.

### The Algorithm

```text
1. Collect Hard Constraints (Physics)
   - e.g., Silk requires directional micro-contrast.

2. Collect Soft Constraints (Vibe/Aesthetics)
   - e.g., Luxury Bridal requests soft, warm illumination.

3. Query the Interaction Ontology (VIO-012)
   - Does Soft Illumination destroy Silk micro-contrast?
   - Yes -> Conflict Detected.

4. Resolve Conflict via Constraint Optimization
   - Solution: Use a soft, warm large bounce for the overall scene (satisfies Bridal Vibe), but introduce a hard, directional kicker light specifically grazing the fabric (satisfies Silk Physics).
```

## 2. Deriving the Solution

The Image Formation Intelligence does not generate prompts. It generates a **Lighting Solution**.

A Lighting Solution is an array of mathematically defined light sources (e.g., HDRI environment map + 3 point lights) that satisfy all constraints.

### Constraint Priority Hierarchy

1. **Brand Identity:** (P0) Must never be violated.
2. **Material Physics:** (P1) The product must look physically accurate and luxurious.
3. **Vibe/Aesthetic:** (P2) The emotional tone of the image.
4. **Cinematic Imperfections:** (P3) The Authenticity Profile applied to ground the image in reality.

## 3. Engineering Implementation

For MVP phase, the constraint solver will be implemented as a rule-based inference engine within `ARC-001`. In production, this will evolve into a Graph Neural Network (GNN) that scores lighting permutations against the Interaction Ontology.
