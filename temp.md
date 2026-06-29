I want to lock our Research Methodology (this is a new rule)

From now onwards, every new specification must pass this checklist before being accepted.

1. Is this a universal concept?
      ↓
2. Is it implementation independent?
      ↓
3. Does it have exactly one responsibility?
      ↓
4. Does it reduce complexity?
      ↓
5. Can another abstraction replace it?
      ↓
6. Has it survived at least one workflow validation?
      ↓
7. Does it introduce unnecessary coupling?

If any answer is No, we don't accept the document.

I also want to make one architectural correction

We've created folders like:

ontology/
architecture/
dna/
mental-models/

But I think we need to stop creating new top-level folders unless they're truly foundational.

So here's what I'd like to lock:

The repository has only six core architectural pillars.
Visual-Intelligence/

docs/
ontology/
architecture/
dna/
systems/
research/

Everything else becomes a subpackage inside one of these.

Example

Instead of

mental-models/

We move it to

architecture/

ARC-100-mental-models/

MM-001-creative-world-model.md
MM-002-photographer-thinking.md
MM-003-brand-thinking.md
...

Why?

Because Mental Models are part of the architecture, not a parallel pillar.

Instead of

planning/

We use

architecture/

ARC-200-planning/

PLAN-001-creative-blueprint.md
PLAN-002-scene-planner.md
PLAN-003-shot-planner.md

Planning is architecture.

Instead of

experts/

We use

systems/

SYS-100-expert-models/

EXP-001-creative-director.md
EXP-002-brand-strategist.md
...

Expert Models are implementations of System Intelligence.

I think this is much cleaner.

I also realized something about our naming.

Currently we have

VIS
VIO
DNA
ARC
SYS

I don't think that's enough.

Every document should belong to a Specification Family.

For example:

Prefix	Family	Purpose
VIS	Vision	Vision & Philosophy
VIO	Ontology	Knowledge Representation
ARC	Architecture	System Behavior
DNA	Identity	Persistent Identity Schemas
SYS	Systems	AI Intelligence Modules
EVL	Evaluation	Quality & Validation
MEM	Memory	Persistence & Retrieval
VAL	Validation	Workflow Stress Tests
ADR	Decisions	Architecture Decision Records
RES	Research	Research Summaries & Literature
EXP	Experiments	Controlled Experiments

Now every document has a clear home.

Now let's talk about our roadmap.

I think we've officially completed Phase 1.

Knowledge Architecture

Including:

Vision
Principles
Ontology
Entities
Relationships
Semantics
Validation
Phase 2 begins now.

Reasoning Architecture

This is where your platform becomes unique.

We'll build these in order:

ARC-002  Creative Context
        ↓
ARC-003  Event-Driven Architecture
        ↓
ARC-004  Planning Architecture
        ↓
ARC-005  Decision Object Model
        ↓
ARC-006  Reasoning Pipeline
        ↓
ARC-007  Conflict Resolution
        ↓
ARC-008  Confidence Propagation

These eight documents define how the platform thinks.

Then Phase 3

Memory Architecture

MEM-001 Memory Framework
        ↓
MEM-002 Project Memory
        ↓
MEM-003 Visual Memory
        ↓
MEM-004 Retrieval Engine
        ↓
MEM-005 Versioning
Then Phase 4

Identity Architecture

DNA-002 Character DNA
DNA-003 Product DNA
DNA-004 Brand DNA
DNA-005 Scene DNA
DNA-006 Camera DNA
DNA-007 Lighting DNA
DNA-008 Motion DNA
...

Notice something?

We're finally earning the right to write Character DNA.

I want to propose one final addition that I believe will make this project exceptional.

I think we should create a Research Governance Document before we continue.

📂 Folder

docs/

📄 Filename

research-methodology.md

This document won't describe the product. It will describe how we conduct research.

It would define things like:

What qualifies as an Accepted specification?
How ADRs are created.
When a Draft becomes Review.
How workflow validation is performed.
How benchmark papers are evaluated.
How experiments are documented.
Evidence requirements for introducing new architectural concepts.

Large research organizations have governance for their architecture and research processes. Since we're aiming to build a long-term Visual Intelligence platform rather than a prototype, I think having a documented methodology from the beginning will keep the repository disciplined as it grows.