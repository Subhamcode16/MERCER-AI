# ENGINEER-COMMUNICATION-001
# Intelligence ↔ Engineering Message Protocol

**Status:** Active  
**Version:** 1.0  
**Purpose:** Establish the communication protocol between the Intelligence Architect and the Engineering Agent through a human message bridge.

---

# 1. Roles

## Intelligence Architect

Responsible for:

- Creative intelligence architecture
- Domain intelligence
- Knowledge modelling
- Decision logic
- Creative reasoning
- Campaign-generation intelligence
- Evaluation philosophy
- Prompting philosophy
- Agent responsibilities
- Trade-off definitions
- Human/AI interaction principles
- Reviewing generated outputs

The Intelligence Architect determines **what the system should know, reason about, and achieve**.

---

## Engineering Agent

Responsible for:

- Backend implementation
- Agent harness
- Prompting engine
- Runtime architecture
- Knowledge compilation
- Schemas
- APIs
- Orchestration
- Evaluation infrastructure
- Testing
- Logging
- Runtime safety
- Performance
- Integration

The Engineering Agent determines **how the system implements the intelligence architecture**.

---

## Human Message Bridge

The human passes messages between both sides.

The human should not be required to translate technical instructions.

Messages should therefore be:

- self-contained
- implementation-oriented
- versioned
- explicit about decisions
- explicit about required responses

---

# 2. Communication Loop

The operating loop is:

```text
Intelligence Architect
        ↓
Instruction
        ↓
Human Message Bridge
        ↓
Engineering Agent
        ↓
Implementation / Analysis
        ↓
Engineering Report
        ↓
Human Message Bridge
        ↓
Intelligence Architect
        ↓
Review / Correction / Approval
        ↓
Next Instruction
```

This loop continues until the relevant component reaches an accepted state.

---

# 3. Instruction Types

Each message from the Intelligence Architect should belong to one of the following categories.

## BUILD

Create a new component.

Example:

`BUILD: Knowledge Compiler`

---

## MODIFY

Change an existing implementation.

Example:

`MODIFY: Blackboard conflict resolution`

---

## REVIEW

Inspect an implementation or architectural decision.

Example:

`REVIEW: Agent orchestration architecture`

---

## TEST

Create or execute validation scenarios.

Example:

`TEST: Multi-product lighting conflict resolution`

---

## INVESTIGATE

Research or analyse an unresolved engineering question.

Example:

`INVESTIGATE: Runtime representation of weighted constraints`

---

## FREEZE

Lock an architectural decision.

Example:

`FREEZE: Markdown → compiled JSON knowledge pipeline`

---

## REJECT

Explicitly prohibit an approach.

Example:

`REJECT: Agents consuming raw Markdown at runtime`

---

# 4. Instruction Structure

Every substantive instruction should use the following structure:

```text
INSTRUCTION ID:
TITLE:
TYPE:
PRIORITY:

CONTEXT

OBJECTIVE

LOCKED DECISIONS

REQUIRED IMPLEMENTATION

CONSTRAINTS

NON-GOALS

EXPECTED OUTPUT

ACCEPTANCE CRITERIA

QUESTIONS / BLOCKERS
```

Not every field must contain a large amount of text, but the structure should remain consistent.

---

# 5. Locked Decisions

Once a decision has been explicitly frozen, the Engineering Agent must treat it as architectural truth unless a later instruction explicitly reopens it.

Example:

```text
LOCKED DECISION

Markdown is the canonical human-authored knowledge format.

Runtime agents must consume compiled machine-readable artifacts.

Do not introduce runtime Markdown parsing.
```

The engineer may propose improvements, but must not silently change a locked decision.

---

# 6. Engineering Freedom

The Intelligence Architect defines:

- intent
- behaviour
- constraints
- semantics
- expected outcomes

The Engineering Agent retains freedom over:

- programming language
- libraries
- internal abstractions
- implementation patterns
- performance optimisations
- deployment mechanisms

provided they do not violate locked architectural decisions.

---

# 7. Engineering Response Protocol

After receiving an instruction, the Engineering Agent should respond with:

## A. Interpretation

What the engineer believes the instruction means.

## B. Implementation Plan

What will be changed or created.

## C. Architectural Impact

Which existing systems are affected.

## D. Implementation

Code, schemas, files, or architecture as appropriate.

## E. Validation

Tests and results.

## F. Open Questions

Only genuine blockers or architectural ambiguities.

## G. Proposed Next Step

What should happen after the current implementation.

---

# 8. No Silent Assumptions

The Engineering Agent must not silently invent:

- domain rules
- creative rules
- priority systems
- confidence thresholds
- business objectives
- agent responsibilities
- knowledge semantics

when those decisions belong to the Intelligence Layer.

If an implementation requires an intelligence decision, surface it explicitly.

---

# 9. Intelligence vs Implementation Boundary

The following distinction must remain clear.

```text
INTELLIGENCE

What should happen?
Why should it happen?
When should it happen?
What should be prioritised?
What should be rejected?
What should be explained?

        ↓

IMPLEMENTATION

How should it happen?
Where should it execute?
How should it be stored?
How should agents communicate?
How should it be tested?
How should it scale?
```

The Engineering Agent should not redefine intelligence merely because an implementation is convenient.

---

# 10. Evidence Requirement

When the Engineering Agent proposes an architectural change that materially affects intelligence behaviour, it should provide the reasoning behind the proposal.

For significant changes, provide:

- problem
- alternatives considered
- chosen approach
- trade-offs
- expected consequences

---

# 11. Agent Harness Rule

The agent harness must not become the intelligence itself.

The harness is responsible for:

- execution
- context assembly
- tool access
- state management
- message routing
- structured outputs
- validation
- retries
- observability

Domain intelligence must remain externalised into the Intelligence Layer wherever practical.

This prevents the prompting layer from becoming an undocumented source of business logic.

---

# 12. Prompting Engine Rule

Prompts should be treated as **compiled execution instructions**, not the canonical location of domain knowledge.

The preferred architecture is:

```text
Knowledge
   +
Context
   +
Objective
   +
Constraints
   +
Reasoning State
   ↓
Prompt Compiler
   ↓
Agent Prompt
   ↓
Model
   ↓
Structured Output
   ↓
Validator
   ↓
Reasoning / Evaluation
```

Do not bury permanent domain rules inside prompts when those rules belong in the Knowledge Layer.

---

# 13. Knowledge Authority

The Intelligence Layer is the authoritative source for:

- domain facts
- physical properties
- visual craft
- campaign heuristics
- decision rules
- constraints
- evidence
- confidence

The prompting engine should retrieve and compile this information.

It should not independently redefine it.

---

# 14. Creative Evaluation Rule

Generated outputs must be evaluated independently from generation whenever practical.

The generator should not be the sole judge of its own output.

Preferred architecture:

```text
Generate
   ↓
Evaluate
   ↓
Explain
   ↓
Score
   ↓
Correct / Regenerate
```

This separation is especially important for:

- brand consistency
- physical plausibility
- material realism
- photographic realism
- campaign objective alignment
- cross-domain conflicts

---

# 15. Communication Status

Every instruction should ultimately resolve to one of:

```text
PROPOSED
IN PROGRESS
IMPLEMENTED
VALIDATED
FROZEN
BLOCKED
REJECTED
```

A component is not considered complete merely because code exists.

It becomes complete when its acceptance criteria have been validated.

---

# 16. Review Standard

The Intelligence Architect will review implementation according to:

1. Architectural correctness
2. Intelligence fidelity
3. Explainability
4. Extensibility
5. Determinism where required
6. Testability
7. Separation of concerns
8. Alignment with constitutional laws
9. Compatibility with existing Intelligence Modules
10. Ability to support future domains

---

# 17. Current Mission

The immediate engineering mission is:

> Build the concrete backend infrastructure capable of transforming the Intelligence Layer into executable campaign-generation behaviour.

The current focus includes:

- Knowledge compilation
- Knowledge retrieval
- Prompt compilation
- Agent harness
- Blackboard / shared reasoning state
- Constraint resolution
- Creative evaluation
- Multi-product reasoning
- Structured agent outputs
- Decision traces
- Validation

---

# 18. Current Architectural Direction

The system should converge toward:

```text
PRODUCT DNA
      +
BRAND DNA
      +
CREATIVE OBJECTIVE
      +
DOMAIN INTELLIGENCE
      +
VISUAL CRAFT
      +
PHYSICS
      +
CAMPAIGN CONTEXT
      ↓
INTELLIGENCE / REASONING
      ↓
CONSTRAINT SPACE
      ↓
CREATIVE SEARCH
      ↓
CANDIDATE STATES
      ↓
CREATIVE EVALUATION
      ↓
DECISION TRACE
      ↓
PROMPT COMPILATION
      ↓
GENERATION
      ↓
POST-GENERATION CRITIC
      ↓
REFINEMENT
      ↓
FINAL CAMPAIGN
```

This architecture should remain modular so that the same system can eventually support multiple Intelligence Domains.

---

# 19. First Communication Task

Before implementing major new functionality, the Engineering Agent should provide an architectural status report covering:

- Current repository structure
- Existing Intelligence Layer implementation
- Existing knowledge schemas
- Existing Markdown templates
- Existing parser/compiler
- Existing Prompt Compiler
- Existing Agent Harness
- Existing Blackboard
- Existing Brand Critic / Evaluation components
- Existing benchmark infrastructure
- Existing test coverage
- Current gaps
- Technical debt
- Components that should be frozen
- Components that should be redesigned

The report should distinguish clearly between:

```text
IMPLEMENTED
PARTIALLY IMPLEMENTED
PLANNED
MISSING
UNCERTAIN
```

No large architectural rewrite should begin until this status is reviewed.

---

# Final Operating Principle

> **The Intelligence Architect defines the mind. The Engineering Agent builds the nervous system. The human message bridge keeps both aligned.**

Neither side should silently assume the responsibilities of the other.

The objective is not merely to produce working software.

The objective is to produce a system whose implementation faithfully expresses the intelligence architecture.