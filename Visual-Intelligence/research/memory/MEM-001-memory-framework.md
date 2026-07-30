---
VIS-ID: MEM-001
Title: Memory Framework
Version: 1.1.0
Status: Accepted
Owner: Visual Intelligence Research
Last Updated: 2026-06-30
Depends On:
  - VIO-001
  - ARC-002
---

# MEM-001: Memory Framework

## Purpose

The **Memory Framework** defines the persistent layer of the Visual Intelligence Platform.

Unlike traditional architectures, Memory in this system is **not a database**. It is an abstraction for **Accumulated Experience**. It dictates how the transient Reasoning Architecture (`ARC-002 Creative Context`) solidifies into permanent Knowledge and how it learns over time.

The fundamental lifecycle of data in this platform is:
```
Experience -> Memory -> Knowledge
```

---

## 1. The Memory Law

To prevent the architecture from bloating, the entire system is governed by a single immutable law:

### The Memory Law
> Everything the platform knows must answer one question:
> **"Should this survive the session?"**
>
> If **No** -> It belongs in the `Creative Context`.
> If **Yes** -> It belongs in `Memory`.

If an object does not need to survive the session, it is explicitly dissolved when the Context closes.

---

## 2. Memory Types and Abstractions

Because Memory represents "Accumulated Experience", it must be categorized by how that experience is used in the future.

### A. Experience Memory
Memory does not just store "what" was decided; it stores **whether it worked**.
- **Content:** The Decision, the Result, and the Metric (e.g., Consistency Score, CTR, Human Rating).
- **Example:** "Golden Hour Lighting yielded a 9.4 rating in Bridal Campaigns."
- **Purpose:** Enables the system to organically *learn* what works over time.

### B. DNA (Permanent Identity)
The highest tier of memory. DNA represents immutable (or slowly evolving) core identities.
- **Examples:** Brand DNA, Character DNA.
- **Use Case:** "What are the absolute rules for this subject?"

### C. Project Memory
Data that must survive the session, but only within the scope of a specific campaign or project.
- **Examples:** "We used a red background yesterday, don't use it again today."
- **Use Case:** Continuity, variation, and deduplication across multiple sessions for the same client.

### D. Visual Memory
The repository of explicit image/video data that the system has analyzed or generated, along with their derived VIO graphs.

### E. Historical Evidence
The audit trail of *Why* decisions were made.
- **Use Case:** Explainability, system evaluation, and human auditing.

---

## 3. The Memory Lifecycle (Forgetting)

Real intelligence forgets. Without forgetting, Memory becomes a bloated liability containing deprecated brand rules and failed experiments.

Every memory goes through a lifecycle:
```
Remember -> Strengthen -> Archive -> Forget
```
1. **Remember:** A memory is created and given a baseline strength score.
2. **Strengthen:** Every time a memory is successfully retrieved and used, its strength increases.
3. **Archive:** If a memory is untouched for a threshold period (or yields poor Experience Metrics), it is removed from active RAG (Retrieval-Augmented Generation) search.
4. **Forget:** Archived memories that exceed a storage constraint or decay threshold are permanently purged.

---

## 4. Relevance-Based Retrieval

Memory is useless if it cannot be accurately recalled. Retrieval is not a direct database lookup (`SELECT * FROM DNA`); it is an analytical pipeline.

```
Memory Retrieval 
  ↓ 
Candidate Memories 
  ↓ 
Ranking (based on Semantic Relevance and Experience Metrics)
  ↓ 
Selection 
  ↓ 
Context Injection
```
This guarantees that only the highest-quality, most proven rules are injected into the active `Creative Context`.

---

## 5. Acceptance Checklist Validation

As per `research-methodology.md`, this specification has been evaluated against the 10-year standard:

1. **Is this a universal concept?** 
   **Yes.** Any intelligent system must differentiate between short-term working memory (Context) and long-term experience (Memory).
2. **Is it implementation-independent?** 
   **Yes.** It does not mandate SQL, NoSQL, or Vector databases. It defines semantic categories of memory and a lifecycle.
3. **Does it have exactly one responsibility?** 
   **Yes.** It defines the rules for persistence and retrieval, keeping the Runtime free of state-storage logic.
4. **Does it reduce complexity?** 
   **Yes.** The Memory Law and Forgetting Lifecycle cleanly separate what must be stored from what can be discarded.
5. **Can another abstraction replace it?** 
   **No.** Without Memory, the system has amnesia between sessions.
6. **Has it survived at least one workflow validation?** 
   **Yes.** During `VAL-001`, the system needed to remember Brand rules and prior inputs, necessitating this separation.
7. **Does it introduce unnecessary coupling?** 
   **No.** Modules access Memory exclusively via defined Retrieval Tasks and Persistence Tasks, orchestrated by the Runtime.
