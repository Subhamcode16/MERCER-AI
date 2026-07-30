---
VIS-ID: ARC-002
Title: Creative Context
Version: 1.1.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-30
Depends On:
  - VIO-001
  - VIO-002
  - VAL-001
---

# ARC-002: Creative Context

## Purpose

The **Creative Context** is the foundational state object of the Reasoning Architecture. 

While DNA represents permanent, persistent identity, the Creative Context represents the transient "scratchpad" of an active session. It is the data structure that holds raw inputs, evolving hypotheses, collected evidence, and active DNA references during an Event-Driven cycle.

It is a **strictly passive data structure**. It does not execute logic, trigger events, or make decisions. It exists solely to be mutated by Intelligence modules (Owners) and read by the Decision Engine.

### Principle
**The Creative Context SHALL NOT contain duplicated persistent knowledge.**
Persistent knowledge belongs exclusively to DNA or Memory. The Creative Context MAY only reference persistent knowledge.

---

## 1. Context Structure

A Creative Context consists of four main registries:

### A. Inputs (Raw Evidence)
The uninterpreted data provided by external sources (usually the User).
- **Text:** "Make a campaign for this Banarasi saree."
- **Images:** Uploaded multimodal assets.
- **Project Scope:** Delivery requirements (e.g., "Instagram, Catalog").

### B. Hypothesis Registry
The system does not jump to conclusions. Everything extracted by AI begins as a Hypothesis.
A Hypothesis object must contain:
1. **Target:** What is being guessed? (e.g., `Product.Style`)
2. **Value:** The guessed value. (e.g., `Banarasi`)
3. **Confidence:** A mathematical probability score (0.0 to 1.0).
4. **Evidence:** A list of explicit reasons *why* this hypothesis was formed, linking back to Inputs or Ontology. (e.g., "Evidence: Floral brocade patterns in uploaded image").

### C. Validated Facts
Hypotheses that have crossed a strict confidence threshold (e.g., 0.95) or have received explicit Human-In-The-Loop approval are promoted to Facts. 
- Facts are immutable for the duration of the context.
- Facts serve as the absolute constraints for the `Creative Decision Engine` and `Evaluation Intelligence`.

### D. Active DNA References
Pointers to the permanent identity architectures that have been invoked for this session.
- `Brand DNA`: Loaded after Gap Analysis.
- `Product DNA`: Constructed from Validated Facts.
- `Character DNA`: Loaded or generated during Casting.
- `Scene DNA`: Constructed during Creative Reasoning.

---

## 2. Context Lifecycle

The Creative Context follows a strict lifecycle tied directly to the Event-Driven Architecture (`ARC-003`).

1. **Initialization:** Created by `User Intelligence` upon receiving a new Input Event (e.g., `User_Uploads_Image`).
2. **Hypothesis Generation:** Populated by extraction models (e.g., `Product Intelligence`) adding low-to-high confidence guesses and evidence.
3. **Validation Gap:** Analyzed by the `Decision Engine`. If key Hypotheses lack confidence, the Context pauses and an `Adaptive Interview` is triggered.
4. **Promotion:** User responses or strong inference promote Hypotheses to Facts.
5. **DNA Compilation:** Facts are compiled into active DNA References.
6. **Execution:** Context is translated into Rendering Instructions.
7. **Dissolution/Commit:** Once the session ends and outputs are delivered, the transient Context is dissolved. Any newly created or modified DNA is committed to `Long-Term Memory` (`MEM-001`).

---

## 3. Conflict & Uncertainty Modeling

The Creative Context explicitly models uncertainty to prevent AI hallucination and ensure explainability.

**Explainability via Evidence:**
If a user asks, *"Why did you light the scene with Golden Hour?"*
The system traces the Context:
`Fact (Lighting = Golden Hour) <- Hypothesis (Confidence 0.99) <- Evidence (Brand DNA Positioning = Heritage Luxury)`.

**Branching via Confidence:**
The Event-Driven cycle relies on the Context's confidence scores to decide routing. 
- `Confidence < Threshold` -> Route to Interview Engine.
- `Confidence >= Threshold` -> Route to Planning Engine.

---

## 4. Acceptance Checklist Validation

As per `research-methodology.md`, this specification has been evaluated against the 10-year standard:

1. **Is this a universal concept?** 
   **Yes.** Every creative workflow (textile, architecture, character design) requires a transient state to hold intermediate reasoning.
2. **Is it implementation-independent?** 
   **Yes.** This is a mathematical/semantic data structure. It applies whether we are using LLMs, hardcoded heuristics, or future GPT-10 models.
3. **Does it have exactly one responsibility?** 
   **Yes.** It is strictly a passive state container. It does not execute logic.
4. **Does it reduce complexity?** 
   **Yes.** By separating *transient guesses* (Context) from *permanent identity* (DNA), we prevent corrupting permanent knowledge with bad guesses.
5. **Can another abstraction replace it?** 
   **No.** `Memory` is for long-term persistence. `DNA` is for permanent identity. `Context` is the only abstraction for active, short-term reasoning.
6. **Has it survived at least one workflow validation?** 
   **Yes.** It directly solves the "Hypothesis" and "Evidence" gaps discovered in `VAL-001-textile-workflow`.
7. **Does it introduce unnecessary coupling?** 
   **No.** Because it is a passive data structure, intelligence modules only need to know its schema, not each other.
