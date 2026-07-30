# IMG-001: Image Formation Solver Specification

## 1. Core Purpose
The Image Formation Solver is the mathematical engine of the Visual Intelligence Platform. It does not assemble strings; it solves a constrained optimization problem to produce a renderer-agnostic **Creative State**. 

It transitions the architecture from a rigid lookup table to a dynamic **Creative Search** algorithm.

## 2. The Creative Fitness Function (4-Stage Hierarchy)
Candidate states are evaluated through a 4-stage hierarchical objective function (the Creative Fitness Function).

### Stage 1: Validity (Hard Constraints)
*Objective: Reject impossible or physically breaking solutions.*
- The solver analyzes the candidate state against the Physics Ontology (IMG-002).
- If a candidate violates a hard physical constraint (e.g., `Material = Velvet` + `Lighting = Hard Backlight without Rim`), it is assigned a score of `0` and immediately rejected from the search space.

### Stage 2: Physical Correctness
*Objective: Rank remaining candidates by optical and material realism.*
- The solver evaluates how well the Lighting and Camera states complement the Material's physical properties.
- Graded against canonical physical benchmarks.

### Stage 3: Creative Quality
*Objective: Optimize for the Creative Objective (OBJ-001).*
- The solver weighs the candidate against the active Creative Objective (e.g., Luxury Editorial vs. E-Commerce).
- Mood, brand fidelity, and storytelling are scored here.

### Stage 4: Platform Optimization
*Objective: Maximize renderer compatibility and efficiency.*
- Evaluates the candidate against Renderer Capability Profiles.
- If the target renderer is Seedance (video), candidates with strong motion/camera path definitions score higher.
- If the target renderer is Flux, candidates relying heavily on unsupported granular shutter speed parameters are penalized.

## 3. The Creative Search Algorithm
The solver explores the constrained search space using the following pipeline:
1. **Generate (N=50)**: Create 50 potential Creative State candidates by mutating Lighting, Camera, and Grading parameters.
2. **Reject (N=40)**: Stage 1 Validity removes 40 physically or semantically impossible candidates.
3. **Rank (N=10)**: Stage 2 ranks the remaining 10 based on Physical Correctness.
4. **Optimize (N=3)**: Stage 3 & 4 select the top 3 candidates (Solution A, Solution B, Solution C) maximizing Creative Quality and Platform Optimization.
5. **Evaluate & Select (N=1)**: The highest-scoring candidate is selected (or presented to the user for choice).

## 4. Explainability: The Creative Decision Trace
Every generated Creative State must output a trace explaining its configuration. This ensures the solver remains transparent and debuggable.

**Trace Schema:**
```yaml
Decision:
  Component: [Lighting/Camera/Grade]
  Value: [Selected Value]

Why:
  [Human readable physical or creative rationale]

Evidence:
  - [Ontology Document ID]
  - [Rule ID]
  - [Brand Pattern ID]

Confidence:
  [0.0 - 1.0 based on fitness score]

Trade-offs:
  Pros:
    - [What this decision achieves]
  Cons:
    - [What this decision sacrifices]

Alternatives Considered:
  - [Alternative 1] (Rejected: [Reason])
  - [Alternative 2] (Rejected: [Reason])
```

## 5. Output: The Creative State
The solver outputs a structured payload detailing the physics of the scene. It does *not* output a prompt.

**Example Payload:**
```yaml
Lighting:
  Key:
    Direction: Left 35°
    Softness: Hard
    Temperature: 5600K
    Purpose: [Metallic Separation]
Camera:
  Lens: 85mm
  Aperture: f/5.6
Color:
  Grade: Warm Sandstone
```
The **Prompt Compiler** handles translating this state into the specific syntax (JSON, Natural Language, ComfyUI Nodes) required by the target renderer.
