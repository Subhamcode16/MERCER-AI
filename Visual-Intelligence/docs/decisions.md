# decisions.md

# Visual Intelligence Platform

## Architecture Decision Records (ADR)

---

## ADR-001

### Title

Product Scope

### Status

Accepted ✅

### Date

2026-06-29

### Context

The project originally considered building or fine-tuning an image generation model.

This would require massive datasets, GPU infrastructure, diffusion model research, and years of model training.

However, the objective of the product is not to compete with GPT Image, Seedance, Higgsfield, or future rendering models.

The objective is to make these models significantly easier and more reliable to use.

### Decision

The platform will **NOT** build or train its own image or video generation models.

Instead, it will build a **Visual Intelligence Layer** that sits above existing rendering models.

The rendering layer remains replaceable.

### Consequences

Positive

* Model agnostic
* Future proof
* Lower infrastructure cost
* Faster iteration
* Can immediately benefit from improvements in external models

Negative

* Dependent on third-party rendering APIs
* Must continuously evaluate new rendering models

---

## ADR-002

### Title

Core Product Philosophy

### Status

Accepted ✅

### Date

2026-06-29

### Context

Existing AI tools rely heavily on long prompts and repeated manual iterations.

### Decision

The product will transform natural conversation into structured Visual DNA.

Users describe ideas.

The system performs the creative reasoning.

Rendering models perform execution.

### Consequences

The platform owns:

* Creative reasoning
* Visual memory
* Consistency
* Decision making
* Prompt compilation

Rendering models own:

* Image generation
* Video generation

---

## ADR-003

### Title

Knowledge–Decision–Execution Architecture

### Status

Accepted ✅

### Date

2026-06-29

### Context

Large AI systems often mix knowledge, reasoning, and execution together.

This makes maintenance difficult.

### Decision

Every capability in the platform belongs to exactly one layer.

Knowledge

↓

Decision

↓

Execution

The platform owns Knowledge and Decision.

Rendering models own Execution.

### Consequences

Clear separation of responsibilities.

Easy replacement of rendering providers.

---

## ADR-004

### Title

Visual Intelligence Ontology

### Status

Accepted ✅

### Date

2026-06-29

### Context

A structured knowledge taxonomy is required before defining agents or prompts.

### Decision

The platform is organized into 18 top-level Intelligence Domains.

* Brand Intelligence
* Creative Intelligence
* Product Intelligence
* Fashion Intelligence
* Character Intelligence
* Scene Intelligence
* Camera Intelligence
* Lighting Intelligence
* Color Intelligence
* Composition Intelligence
* Motion Intelligence
* Story Intelligence
* Marketing Intelligence
* Platform Intelligence
* Model Intelligence
* Evaluation Intelligence
* Memory Intelligence
* User Intelligence

These domains become the root ontology of the entire platform.

### Consequences

Every paper, reference, benchmark, campaign, image, and research artifact must map to one or more ontology domains.

---

## ADR-005

### Title

Adaptive Interview Engine

### Status

Accepted ✅

### Date

2026-06-29

### Context

Traditional AI assistants ask fixed sequences of questions.

This increases user effort and reduces conversational quality.

### Decision

The platform adopts an Adaptive Interview Engine.

Questions are generated dynamically based on uncertainty rather than predefined forms.

The engine continuously evaluates:

* What is already known?
* What can be inferred?
* What can be retrieved?
* What remains uncertain?

Only missing high-value information is requested from the user.

### Consequences

* Fewer user interactions
* Better user experience
* Higher information quality
* Lower repetition
* Better Visual DNA completeness

---

## ADR-006

### Title

Confidence-Based Reasoning

### Status

Accepted ✅

### Date

2026-06-29

### Context

Not every piece of information has equal certainty.

### Decision

Every field inside Visual DNA stores a confidence score.

Questions are asked only when confidence falls below the required threshold.

### Consequences

The interview engine becomes adaptive rather than rule-based.

---

## ADR-007

### Title

Three-Layer DNA Model

### Status

Accepted ✅

### Date

2026-06-29

### Context

Flat metadata cannot distinguish permanent identity from temporary visual changes.

### Decision

Every DNA object follows a three-layer inheritance model.

Identity Layer

↓

Appearance Layer

↓

State Layer

Identity represents immutable characteristics.

Appearance represents intentional styling.

State represents temporary scene-specific attributes.

### Consequences

Supports consistent identity while allowing creative variation.

This architecture will be reused for:

* Character DNA
* Product DNA
* Brand DNA
* Scene DNA
* Camera DNA
* Environment DNA
* Motion DNA

---

## ADR-008

### Title

Recognition Anchors

### Status

Accepted ✅

### Date

2026-06-29

### Context

Human identity is recognized through a small number of dominant visual characteristics rather than every facial feature equally.

### Decision

Every Character DNA contains Recognition Anchors.

These represent the defining visual traits that must remain stable across generations.

Evaluation engines prioritize preserving Recognition Anchors during validation.

### Consequences

Improved identity consistency.

Reduced unnecessary regeneration.

More human-like identity preservation.

---

# Future ADRs

The following decisions are expected to be documented as the project evolves.

* Product DNA Architecture
* Brand DNA Architecture
* Scene DNA Architecture
* Prompt Compiler Architecture
* Agent Communication Protocol
* Knowledge Graph Design
* Model Routing Strategy
* Evaluation Engine
* Memory Engine
* Creative Decision Engine
* Retrieval Architecture
* Context Management
* Multi-Agent Orchestration
* Failure Recovery Strategy
* Visual Consistency Standard
* Benchmark Methodology
* Experiment Framework

```
```
