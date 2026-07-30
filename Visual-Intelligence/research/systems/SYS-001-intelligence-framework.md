---
VIS-ID: SYS-001
Title: Intelligence Framework
Version: 1.0.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-30
Depends On:
  - ARC-003
  - MEM-001
---

# SYS-001: Intelligence Framework

## Purpose

The **Intelligence Framework** is the final foundational abstraction of the architecture. It defines the formal structure of an "Intelligence Module" (e.g., `Product Intelligence`, `Character Intelligence`).

Historically, systems vaguely referred to "Agents" as black boxes that magically performed work. Under our 10-year standard, an **Agent does not exist** at the architectural level. An Agent is merely a deployment strategy. 

Instead, we define **Intelligence Modules**—strict, bounded domains of expertise that contain predefined Tasks, interact cleanly with the Runtime (ARC-003), and rely exclusively on the Creative Context (ARC-002) for state.

---

## 1. What is an Intelligence Module?

An Intelligence Module is a **domain-specific collection of Capabilities, bounded by strict Ownership.**

It does not:
- Decide when to run (that is the `Runtime Execution Engine`).
- Decide if its results are acceptable (that is the `Decision Engine`).
- Store its own persistent state (that is the `Memory Framework`).

It strictly:
- Receives Context.
- Executes Domain Tasks.
- Returns Task Results.

---

## 2. Framework Schema

Every Intelligence Module (`SYS-002`, `SYS-003`, etc.) MUST be documented using the following formal structure:

### A. Core Ownership
The absolute bounds of what this Intelligence is legally allowed to decide.
- *Example (Product Intelligence):* Owns fabric extraction, garment taxonomy, and product consistency. It does NOT own lighting or models.

### B. Capabilities (Task Definitions)
A registry of the specific Tasks this module can execute within the Runtime.
- **Inference Tasks:** Deriving semantic meaning from inputs (e.g., `ExtractFabric`).
- **Generation Tasks:** Creating new data (e.g., `GeneratePrompt`).
- **Validation Tasks:** Checking outputs against constraints.
- **Planning Tasks:** Generating structured strategies (e.g., `GenerateScenePlan`).

### C. Input Requirements
What this module requires from the `Creative Context` before its Tasks can execute.
- *Example:* `Character Casting Task` strictly requires `Brand DNA` to be present in the Context.

### D. Output Contracts
The structure of the `Task Results` this module produces.
- *Example:* Must output a `Candidate Product DNA` object with Confidence scores > 0.8.

### E. Memory Interactions
How this module interacts with the `Memory Framework` (MEM-001).
- What DNA does it retrieve?
- What Historical Evidence does it generate?

---

## 3. The Orchestration Cycle

By enforcing this strict schema, the Intelligence Framework seamlessly plugs into the Runtime:

1. **Router:** The Runtime Router matches an Event (e.g., `GarmentUploaded`) to the `Product Intelligence` module because it mathematically owns that domain.
2. **Task Execution:** `Product Intelligence` executes its `ExtractGarment` task, pulling from Context and Outputting a Task Result.
3. **Evaluation:** The `Decision Engine` scores the result.
4. **Memory:** If successful, it is persisted as `DNA` or `Project Memory`.

---

## 4. Acceptance Checklist Validation

As per `research-methodology.md`, this specification has been evaluated against the 10-year standard:

1. **Is this a universal concept?** 
   **Yes.** Any modular intelligence platform requires a framework for defining what a domain expert (module) can and cannot do.
2. **Is it implementation-independent?** 
   **Yes.** An Intelligence Module could be implemented via a single massive LLM prompt, a swarm of small models, or traditional heuristics. The framework remains identical.
3. **Does it have exactly one responsibility?** 
   **Yes.** It defines the *boundaries and contracts* of domain expertise. It leaves orchestration to the Runtime.
4. **Does it reduce complexity?** 
   **Yes.** By defining Intelligence as a collection of Tasks rather than autonomous "Agents", it eliminates chaotic agent-to-agent communication.
5. **Can another abstraction replace it?** 
   **No.** Without this framework, the Runtime wouldn't know what it is orchestrating.
6. **Has it survived at least one workflow validation?** 
   **Yes.** `VAL-001` required multiple distinct "Intelligences" (Product, Scene, Lighting). This framework formalizes how they coexist.
7. **Does it introduce unnecessary coupling?** 
   **No.** Intelligence modules are completely ignorant of each other; they communicate exclusively through the Creative Context.
