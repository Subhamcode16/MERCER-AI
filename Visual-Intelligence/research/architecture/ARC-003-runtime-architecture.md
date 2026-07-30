---
VIS-ID: ARC-003
Title: Runtime Architecture
Version: 1.1.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-30
Depends On:
  - ARC-001
  - ARC-002
---

# ARC-003: Runtime Architecture

## Purpose

The **Runtime Architecture** defines the "operating system" of the Visual Intelligence Platform.

While the `Creative Context` (ARC-002) holds the transient state, the Runtime Architecture defines *how that state is mutated*. It is the orchestrator that guarantees work is executed reliably, concurrently, and safely.

We explicitly reject a pure "Event-Driven" architecture. Events signal that something happened, but they do not execute logic. **Tasks execute logic.**

### Runtime Principle
> Events communicate.
> Tasks execute.
> Context stores state.
> The Decision Engine reasons.
> The Runtime orchestrates.

---

## 1. The Execution Model

The Runtime operates on a strict cyclical execution model separating events from execution:

```
Event 
  ↓ 
Router 
  ↓ 
Task 
  ↓ 
Task Result 
  ↓ 
Context Mutation 
  ↓ 
Decision 
  ↓ 
Publisher 
  ↓ 
Event
```

*Note: The Task does not directly mutate the context. It produces a `Task Result`, which the Runtime orchestrates into a safe Context Mutation.*

---

## 2. Core Subsystems

### A. Router
Matches incoming Events to the appropriate Task Definitions.

### B. Execution Engine (formerly Scheduler)
Responsible for the actual orchestration of work. The Execution Engine handles:
- Retries
- Concurrency
- Priorities
- Cancellation
- Timeout
- Orchestration

### C. Context Manager
Handles state synchronization. 
The Runtime SHALL guarantee consistent Context updates regardless of the underlying concurrency mechanism. 

### D. Publisher
Emits new Events (e.g., `ProductExtracted`) to continue the cycle once the Decision Engine has evaluated the new state.

---

## 3. Parallel Execution

The Runtime supports parallel fan-out and fan-in.

Instead of: `Extract Product -> Extract Color -> Extract Border`
The Runtime executes:
```
Image Uploaded
  ↓
  ├── Extract Fabric
  ├── Extract Color
  ├── Extract Border
  ├── OCR
  ├── Metadata
  └── Texture Analysis
```
The Execution Engine manages the parallel execution of these Tasks and merges their Task Results safely back into the Context.

---

## 4. Failure Recovery

We strictly distinguish between two types of failure:

**1. Operational Failure**
- *Examples:* API timeout, Network failure, Rate limit.
- *Owner:* The **Runtime** (specifically the Execution Engine).
- *Action:* Automatic deterministic retries based on the Task Contract.

**2. Reasoning Failure**
- *Examples:* Low confidence, Conflicting evidence, Contradictory semantics.
- *Owner:* The **Decision Engine**.
- *Action:* Evaluates the context and routes to a human or alternative strategy.

---

## 5. Human-in-the-Loop (HitL)

When the Decision Engine detects a Reasoning Failure (e.g., Confidence < 90%), the workflow is not restarted. Instead:

```
Runtime Paused 
  ↓ 
Human Input 
  ↓ 
Resume (from exact state)
```

---

## 6. The Task System

Every intelligence module is simply a collection of Tasks.

### Task Types
Tasks must be explicitly classified to aid the Decision Engine in routing:
- **Inference Task**
- **Extraction Task**
- **Validation Task**
- **Planning Task**
- **Generation Task**
- **Evaluation Task**
- **Persistence Task**

### Task Contract Schema
Every Task must follow a strict, self-describing schema. This allows the Runtime to auto-generate execution plans in the future.

**Example Task Contract:**
```yaml
Name: ExtractFabric
Owner: Product Intelligence
Type: Extraction Task
Consumes: Creative Context
Produces: Task Result (Fabric Identity)
Publishes: FabricExtracted
Reads: Input Registry
Writes: Hypothesis Registry
Failure Events: ExtractionFailed
Timeout: 30s
Retry Policy: 3 attempts
```

---

## 7. Workflow Orchestration

While the Execution Engine manages *how* a specific task runs (concurrency, retries), the overall control flow—deciding *which* task runs next—is governed by the Workflow Orchestration.

**Example Workflow:**
```
Image Uploaded 
  ↓ 
Extract Product 
  ↓ 
Gap Analysis 
  ↓ 
Interview Required? 
  ├── YES -> Pause -> Resume
  └── NO -> Continue
  ↓ 
Planning 
  ↓ 
Rendering
```

The Runtime Orchestrator uses the state of the `Creative Context` and the rules of the `Decision Engine` to chart this high-level path.

---

## 8. Engineering Notes

**Where are the Agents?**
There are no "Agents" in this architecture. There are only the Runtime, Tasks, Decision Engine, Context, and Systems. An "Agent" is merely a deployment strategy for Tasks, not a fundamental building block.

**Context Synchronization Implementations**
While the specification dictates guaranteed consistency, implementations may use Optimistic Locking, MVCC, or CRDTs depending on the database backend.

---

## 9. Acceptance Checklist Validation

1. **Is this a universal concept?** 
   **Yes.** This mirrors mature execution runtimes (Temporal, Airflow, Cadence).
2. **Is it implementation-independent?** 
   **Yes.** It defines the orchestration model, not the code.
3. **Does it have exactly one responsibility?** 
   **Yes.** The Runtime orchestrates work. It does not perform reasoning or store state.
4. **Does it reduce complexity?** 
   **Yes.** It solves parallel execution and state synchronization at the system level.
5. **Can another abstraction replace it?** 
   **No.** Without an Execution Engine and Task System, AI components devolve into chaotic point-to-point scripts.
6. **Has it survived at least one workflow validation?** 
   **Yes.** This emerged directly from tracing the "Why" and "How" in `VAL-001`.
7. **Does it introduce unnecessary coupling?** 
   **No.** Tasks are perfectly decoupled via Context and Task Contracts.
