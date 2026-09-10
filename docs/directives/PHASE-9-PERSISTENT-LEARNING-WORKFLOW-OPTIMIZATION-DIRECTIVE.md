# Implementation Plan: Phase 9 — Persistent Learning, Knowledge & Workflow Optimization Boundary

**Document Status:** PROPOSED (Awaiting User Approval)  
**Phase:** 9  
**Scope:** Durable workflow memory, evaluated feedback, external knowledge/trend ingestion, benchmark-driven improvement, artifact lineage, and bounded optimization  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`, Phase 8 Agentic Work Governance  
**Prerequisites:** Phases 1–8 COMPLETE & RATIFIED — 224/224 Pytests PASSED

---

## 1. Purpose

Phase 9 converts the Phase 8 bounded agentic work layer from an in-memory orchestration capability into a **persistent, measurable, versioned learning and workflow-optimization boundary**.

The objective is to allow the system to remember prior outcomes, retain structured feedback, learn from recurring failure patterns, ingest external visual/design/trend observations as explicitly untrusted knowledge, compare new work against historical benchmarks, improve workflow strategies, measure whether adaptations actually improve outcomes, roll back failed changes, and preserve artifact provenance.

### Non-Negotiable Principle

> **The system may improve its methods, but it may never improve its authority.**

Formally:

- `Learning != Authorization`
- `Knowledge != Truth`
- `Optimization != Security Policy Mutation`
- `Self-Improvement != Execution Authority`
- `External Observation != Trusted Fact`
- `User Feedback != Automatic Policy Override`

---

## 2. Architectural Position

Phase 9 sits above the Phase 8 Agentic Work Layer.

```text
USER / WORKFLOW REQUEST
          |
          v
PHASE 8 WORK ORCHESTRATOR
Staff • DAG • Critique • Review • Workflow
          |
          v
PHASE 9 LEARNING BOUNDARY
Workflow Memory -> Feedback -> Evaluation -> Adaptation
      ^               ^           |          |
Knowledge Intake -> Benchmarking -> Versioning -> Rollback
          |
          v
PHASE 1–7 SECURITY SUBSTRATE
Evidence • Decision • Attestation • Audit • Recovery
Epistemic State • Execution Gate
```

Phase 9 **must not** bypass Phase 1–7 security boundaries.

---

## 3. Core Architecture

### 3.1 Workflow Memory

Create a durable structured representation of completed workflows.

Memory should contain:

- workflow identifier;
- task type;
- staff participation;
- task graph version;
- input metadata;
- output artifact identifiers;
- critique scores;
- independent review scores;
- user feedback;
- failure signals;
- revision count;
- adaptation version;
- benchmark results;
- timestamps;
- provenance metadata.

Memory must not store raw secrets, private cryptographic material, authentication credentials, raw security-sensitive buffers, production keys, or unrestricted credential-bearing prompts.

### 3.2 Feedback Learning

Use:

```text
Workflow
   ↓
Outcome
   ↓
Critique + Independent Review
   ↓
User / Evaluator Feedback
   ↓
Learning Signal
   ↓
Pattern Aggregation
   ↓
Candidate Adaptation
   ↓
Evaluation
   ↓
Accept / Reject / Rollback
```

A single feedback event must not directly rewrite orchestration policy.

### 3.3 External Knowledge & Trend Intake

Persist external visual/design observations such as:

- visual identity patterns;
- typography trends;
- color trends;
- layout patterns;
- editorial systems;
- motion patterns;
- social creative patterns;
- campaign structures;
- contemporary design references.

Every observation carries source, timestamps, provenance, confidence, classification, commitment, and status.

External observations remain `UNTRUSTED_EXTERNAL_OBSERVATION` until independently evaluated. Popularity, recency, or repetition must never be treated as proof of truth.

---

## 4. Artifact Lineage Boundary

Every generated workflow artifact should be traceable through:

```text
User Request
    ↓
Workflow ID
    ↓
Task Graph Version
    ↓
Staff Contributions
    ↓
Knowledge / Trend Observations
    ↓
Critique
    ↓
Independent Review
    ↓
Revision History
    ↓
Final Artifact
```

The system must be able to explain why a design decision was made, which staff contributed, which observations influenced it, what critique caused revision, which adaptation version was active, and what changed between versions.

---

## 5. Adaptive Strategy Boundary

Introduce a versioned `AdaptiveStrategy`.

It may modify bounded workflow behavior such as:

- staff ordering;
- task decomposition;
- research depth;
- critique weighting;
- revision prioritization;
- benchmark selection;
- trend-observation weighting;
- context allocation.

It may **never** modify:

- `ExecutionGate`;
- epistemic-state transition rules;
- security policy;
- trust anchors;
- authentication requirements;
- recovery authorization requirements;
- production cryptographic boundaries;
- hardware custody;
- audit integrity rules;
- governance constraints.

---

## 6. Evaluation-First Self-Improvement

No candidate adaptation becomes active merely because it was generated.

Required lifecycle:

```text
CANDIDATE
   ↓
OFFLINE EVALUATION
   ↓
BENCHMARK COMPARISON
   ↓
SECURITY / BOUNDARY CHECK
   ↓
APPROVED ADAPTATION
   ↓
VERSIONED DEPLOYMENT
   ↓
MONITORED WORKFLOW
   ↓
KEEP / ROLLBACK
```

Each adaptation must have an immutable parent version, candidate version, reason, supporting learning signals, benchmark results, evaluator, timestamp, activation status, and rollback pointer.

---

## 7. Permanent Regression & Real-Workflow Benchmarking

Establish reusable benchmarks covering:

1. **Visual Identity Research** — completeness, source diversity, provenance, relevance, contradiction handling.
2. **Brand Campaign Strategy** — coherence, audience fit, differentiation, implementation quality.
3. **Visual Design Direction** — system consistency, typography, color, composition, hierarchy, trend relevance, differentiation.
4. **Social Content System** — narrative consistency, content variety, platform fit, visual consistency, CTA quality.
5. **Revision Recovery** — defect detection, critique quality, revision effectiveness, regression avoidance.

### Mandatory Improvement Experiment

**Run 1:** Execute a defined workflow with baseline strategy `V1` and record measurable metrics.

**Learning Cycle:** Extract structured learning signals.

**Candidate:** Generate strategy `V2`.

**Evaluation:** Run the same benchmark/workflow under `V2`.

`V2` may activate only if quality improves (or a predefined tradeoff is justified), security boundaries remain intact, no forbidden capability appears, regression tests remain green, lineage remains intact, and the improvement is reproducible.

Then intentionally introduce a worse candidate and demonstrate rejection or rollback.

The proof required is:

> **The system can improve itself without being allowed to govern itself.**

---

## 8. Proposed File Manifest

### Agentic Work

- `[NEW] memory_models.py` — `WorkflowMemoryRecord`, `FeedbackRecord`, `LearningPattern`, `WorkflowOutcome`, `ArtifactLineage`.
- `[NEW] memory_store.py` — controlled persistent storage abstraction with append/query/version/provenance/integrity support.
- `[NEW] feedback_learning.py` — feedback aggregation into bounded learning patterns.
- `[NEW] knowledge_store.py` — persistent external-observation store.
- `[NEW] artifact_lineage.py` — immutable artifact ancestry and contribution records.
- `[NEW] adaptive_strategy.py` — versioned orchestration strategies with an explicit mutable-field allowlist.
- `[NEW] improvement_engine.py` — candidate generation, evaluation, activation, rollback.
- `[NEW] benchmark_suite.py` — reusable benchmark definitions and scoring.
- `[NEW] learning_governance.py` — bounded adaptation, approval state, rollback, and immutable security-boundary enforcement.
- `[MODIFY] orchestrator.py` — consume approved `AdaptiveStrategy` without mutating security policy.

---

## 9. Security Substrate Integration

Allowed:

```text
Security Substrate
        ↓
Security Observations
        ↓
Phase 9 Learning / Evaluation
```

Forbidden:

```text
Phase 9 Learning
        ↓
Security Policy Mutation
        ↓
ExecutionGate Unlock
```

Phase 9 must have zero authority to set `VERIFIED`, bypass verification, unlock `ExecutionGate`, alter recovery semantics, alter trust anchors, alter audit integrity, or alter cryptographic boundaries.

---

## 10. Threat Model

- **T9-1 Learning Poisoning:** malicious feedback biases future behavior. Mitigate with aggregation, provenance, evaluation, and benchmark comparison.
- **T9-2 Trend Poisoning:** malicious external observations influence design intelligence. Keep observations untrusted and evaluate them.
- **T9-3 Self-Escalation:** adaptive strategy attempts to modify security behavior. Enforce protected-field allowlists and runtime checks.
- **T9-4 Regression Amplification:** one benchmark improves while others degrade. Use multi-objective regression testing.
- **T9-5 Memory Contamination:** arbitrary instructions are written into memory. Use typed records, provenance, bounded retrieval, and instruction/data separation.
- **T9-6 Artifact Lineage Forgery:** false provenance claims. Use immutable lineage and commitments.
- **T9-7 Feedback Replay:** repeated old feedback distorts learning. Use IDs, commitments, and replay protection.
- **T9-8 Knowledge Staleness:** obsolete trends dominate. Use freshness metadata and temporal weighting.
- **T9-9 Benchmark Gaming:** optimizer overfits benchmarks. Use hidden cases, multiple benchmarks, and real workflow validation.
- **T9-10 Autonomous Policy Mutation:** learning modifies governance/security constraints. Use hard-coded protected boundaries and AST/runtime audits.
- **T9-11 Prompt Injection Through Knowledge:** external observations contain instructions. Treat observations as data, never executable instructions.
- **T9-12 Cross-Workflow Contamination:** one workflow's context leaks into another. Enforce workflow-scoped memory and explicit context boundaries.

---

## 11. Required Tests

Add tests for:

- persistent workflow memory;
- feedback persistence and replay rejection;
- trend observation persistence and provenance;
- artifact lineage integrity/tamper detection;
- adaptive strategy schema enforcement;
- protected-field mutation rejection;
- candidate evaluation and regression comparison;
- rollback;
- poisoned feedback resistance;
- stale knowledge handling;
- prompt-injection-as-data handling;
- cross-workflow isolation;
- concurrent memory writes;
- concurrent adaptation registration;
- deterministic strategy versioning;
- execution-gate isolation;
- epistemic-state isolation.

---

## 12. Acceptance Criteria

Phase 9 cannot be ratified unless:

- [ ] All Phase 1–8 tests remain green.
- [ ] Persistent workflow memory works.
- [ ] Feedback becomes bounded learning signals.
- [ ] External knowledge remains untrusted observation.
- [ ] Artifact lineage is machine-verifiable.
- [ ] Adaptive strategies are versioned.
- [ ] Protected security fields cannot be mutated.
- [ ] Candidate adaptations require evaluation.
- [ ] Failed adaptations roll back.
- [ ] A real workflow benchmark demonstrates measurable improvement.
- [ ] A deliberately harmful adaptation is rejected or rolled back.
- [ ] Cross-workflow context isolation is demonstrated.
- [ ] Knowledge ingestion cannot execute embedded instructions.
- [ ] `ExecutionGate` remains locked throughout learning/optimization.
- [ ] No learning path can transition epistemic state to `VERIFIED`.
- [ ] No production cryptographic/hardware capability is introduced.
- [ ] Security review passes.
- [ ] Governance gate passes with explicit limitations.

---

## 13. Engineer Instruction

> **Do not begin implementation immediately.**
>
> First inspect the complete Phase 1–8 implementation and reconcile this directive with the existing architecture.
>
> Identify:
>
> 1. reusable abstractions;
> 2. existing persistence assumptions;
> 3. existing Phase 8 learning/trend mechanisms;
> 4. security-substrate integration points;
> 5. architectural conflicts;
> 6. requirements that cannot be implemented safely as written.
>
> Then produce a short implementation-readiness report.
>
> **Only implement Phase 9 after the user provides the green signal.**
>
> Preserve all Phase 1–8 behavior. Do not weaken security invariants, introduce production cryptographic/hardware capability, permit self-modification of security policy, allow external knowledge to become executable instructions, or treat learning as authorization.
>
> Phase 9 completion requires both:
>
> **(A) automated regression evidence**, and  
> **(B) a reproducible real-workflow improvement demonstration.**
>
> Large engineering walkthroughs must be delivered as a **single downloadable Markdown file**. Small engineer questions may be provided directly in one Markdown block.

---

## 14. Governance Decision Required

**Status: PROPOSED — NOT AUTHORIZED FOR IMPLEMENTATION**

Recommended approval phrase:

> **GREEN SIGNAL — PROCEED WITH PHASE 9 IMPLEMENTATION.**
