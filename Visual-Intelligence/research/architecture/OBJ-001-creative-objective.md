# OBJ-001: Creative Objective Framework

## 1. Core Purpose
The Image Formation Solver (IMG-001) does not inherently know what "good" is. The **Creative Objective** serves as the master configuration layer that initializes the solver's fitness function weights prior to candidate search. It defines what the solver is attempting to achieve strategically.

## 2. Objective Structure
Every request processed by the Visual Intelligence Platform must include an explicitly defined Creative Objective, consisting of four hierarchical goals:

### Primary Goal (Weight: 0.50)
The non-negotiable intent of the image.
*Examples:* Sell Product, Editorial Storytelling, Brand Identity Establishment.

### Secondary Goal (Weight: 0.30)
The supporting mechanism that enables the Primary Goal.
*Examples:* Preserve Fabric Realism, Elicit Emotion, Show Environmental Context.

### Tertiary Goal (Weight: 0.20)
The aesthetic polishing layer.
*Examples:* Luxury Perception, High Microcontrast, Nostalgic Film Aesthetic.

### Ignore List (Weight: 0.0)
Explicit anti-goals. The solver prunes candidates that prioritize these attributes.
*Examples:* Experimental Composition, Catalog Accuracy, Deep Depth of Field.

## 3. Case Studies: Same DNA, Different Objectives

Given the exact same Product DNA (`Banarasi Silk Saree`), Brand DNA, and Environment, the Creative Objective dictates entirely divergent Creative States:

### Scenario A: Amazon Listing
- **Primary:** Catalog Accuracy (Exact color/texture match).
- **Secondary:** Clean Isolation (No distracting background).
- **Tertiary:** Commercial Lighting.
- **Ignore:** Atmospheric Mood.
- **Resulting Creative State:** Softboard overhead key, 50mm, f/8 for total focal coverage, pure white or neutral gray background, minimal contrast.

### Scenario B: Vogue Editorial
- **Primary:** Editorial Storytelling (Evoke mood and luxury).
- **Secondary:** Cinematic Lighting (Shape and shadow).
- **Tertiary:** Luxury Perception.
- **Ignore:** Catalog Accuracy (It's okay if a shadow obscures the hem).
- **Resulting Creative State:** Hard directional key, negative fill, 85mm, f/2.8 for shallow depth, atmospheric dust, rich film grain.

## 4. Integration with the Solver
The objective function in IMG-001 calculates a score for each candidate state using the weights established by the Creative Objective framework. Trade-offs are evaluated against this specific matrix.
