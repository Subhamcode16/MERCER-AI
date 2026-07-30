# Research Methodology & Governance

## Purpose
This document defines the rigorous standard for introducing, validating, and accepting new architectural specifications within the Visual Intelligence Platform.

Our goal is to build a 10-year reference architecture. We prioritize **restraint over invention**. The strongest architectures are not those with the most concepts, but those where every concept is indispensable.

---

## 1. The Acceptance Checklist

Before any new specification, abstraction, or mental model can be moved from `Draft` to `Review` or `Accepted` status, it **MUST** answer "Yes" to all 7 of the following questions:

1. **Is this a universal concept?** (Does it apply across different brands, products, and campaigns?)
2. **Is it implementation-independent?** (Will this still make sense 10 years from now, even if GPT-10 or a completely new rendering technology exists?)
3. **Does it have exactly one responsibility?** (Does it avoid overlapping with other intelligent systems?)
4. **Does it reduce complexity?** (Does introducing this concept make the overall system easier to reason about?)
5. **Can another abstraction replace it?** (Answer must be **No**. If it can be replaced by an existing concept, we do not need it.)
6. **Has it survived at least one workflow validation?** (Has it been stress-tested in a `VAL` document?)
7. **Does it introduce unnecessary coupling?** (Answer must be **No**. The abstraction should remain modular.)

If a specification fails any of these checks, it must be redesigned or discarded.

---

## 2. Specification Families

Every document in the repository belongs to a specific architectural family, indicated by its prefix. We strictly enforce these families to prevent knowledge fragmentation.

| Prefix | Family | Purpose | Location |
| :--- | :--- | :--- | :--- |
| **VIS** | Vision | Vision & Philosophy | `docs/` |
| **VIO** | Ontology | Knowledge Representation | `ontology/` |
| **ARC** | Architecture | System Behavior & Event Models | `architecture/` |
| **DNA** | Identity | Persistent Identity Schemas | `dna/` |
| **SYS** | Systems | AI Intelligence Modules & Agents | `systems/` |
| **MEM** | Memory | Persistence & Retrieval | `architecture/` |
| **EVL** | Evaluation | Quality & Validation | `architecture/` |
| **VAL** | Validation | Workflow Stress Tests | `research/` |
| **RES** | Research | Research Summaries & Literature | `research/` |
| **EXP** | Experiments | Controlled Experiments | `research/` |
| **ADR** | Decisions | Architecture Decision Records | `docs/` |

---

## 3. Document Lifecycle

Every architectural specification goes through a strict lifecycle, tracked via its frontmatter `Status` field.

1. **Draft:** The initial proposal. Can be edited freely.
2. **Review:** The specification is complete but has not yet survived a Workflow Validation (`VAL`).
3. **Accepted:** The specification has passed the 7-question checklist, survived at least one `VAL` stress test, and an Architecture Decision Record (`ADR`) has been written to officially promote it.

---

## 4. Architecture Decision Records (ADR)

We use ADRs to formally document *why* a significant architectural decision was made.

An ADR must be created when:
- Promoting a specification from `Review` to `Accepted`.
- Introducing a new core Domain Intelligence (e.g., `Lighting Intelligence`).
- Changing a fundamental mechanism (e.g., moving from Pipelines to Event-Driven cycles).

ADRs are stored in `docs/decisions.md` (or as individual `ADR-XXX.md` files) and must include:
- The context and the problem.
- The proposed solution.
- The consequences (positive and negative).
- The evidence from `VAL` workflows that supports the decision.

---

## 5. The Core Pillars

The repository is strictly divided into six core pillars. No new top-level directories may be created. Everything else becomes a subpackage inside one of these:

1. `docs/` - Governance, roadmaps, principles, and decisions.
2. `ontology/` - The semantic foundation and knowledge representation.
3. `architecture/` - How the system behaves, reasons, and plans.
4. `dna/` - How the system defines persistent visual identity.
5. `systems/` - How the system is implemented (expert models, agents).
6. `research/` - Workflow validations, external literature, and experiments.
