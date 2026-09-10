# PHASE-14-WORKFORCE-ARCHITECTURE.md

## Phase 14 — ILYREN Creative Workforce & Organizational Intelligence Architecture

**Status:** RATIFIED & APPROVED  
**Date:** September 5, 2026  
**Scope:** Organizational Intelligence Boundary, Workforce Taxonomy, Context Scope Isolation, Self-Critique, Independent Review, Trend Intelligence, Visual DNA Synthesis, Institutional Memory, and Evaluation-First Governed Improvement.

---

## 1. Executive Summary

Phase 14 establishes the **organizational intelligence layer** above the existing Phase 1–13 substrate (`src/security_substrate/`, `src/agentic_work/`, `src/execution_control/`, `src/mission_control/`, `src/coordination/`, `src/integration_boundary/`, `src/workflow_gateway/`).

It transitions the system from a collection of isolated AI agents into a governed creative organization:

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$
$$\mathbf{Learning \neq Security\ Policy\ Mutation} \quad \Big| \quad \mathbf{External\ Observation \neq Trusted\ Fact}$$
$$\mathbf{Self\!-\!Improvement \neq Self\!-\!Authorization} \quad \Big| \quad \mathbf{Creative\ Review \neq Execution\ Authorization}$$

---

## 2. Workforce Topology & Package Structure (`src/creative_workforce/`)

The implementation comprises 19 distinct modules:

1. `exceptions.py`: Fail-closed exception hierarchy.
2. `organization_models.py`: Immutable dataclasses (`Department`, `Role`, `AuthorityClass`, `StaffIdentity`, `ContextBinding`, `WorkforceAssignment`, `CritiqueResult`, `ReviewResult`).
3. `staff_registry.py`: `StaffRegistry` containing staff members across Strategy, Creative, Intelligence, Content, and Quality departments.
4. `client_context.py`: `ClientContextManager` establishing hierarchical context (`ClientContext` $\rightarrow$ `BrandContext` $\rightarrow$ `CampaignContext` $\rightarrow$ `MissionContext` $\rightarrow$ `TaskContext`) and enforcing fail-closed cross-client isolation.
5. `delegation.py`: `WorkforceDelegationEngine` decomposing client objectives into role-based assignments with task dependencies and context bindings.
6. `creative_director.py`: `CreativeWorkforceDirector` converting client objectives into organizational work plans.
7. `collaboration.py`: `CreativeCollaborationProtocol` managing structured artifact flow with SHA-256 lineage tracking.
8. `critique.py`: `SelfCritiqueEngine` evaluating artifacts against quality dimensions (brand alignment, visual quality, trend relevance, etc.) to produce non-authoritative revision signals.
9. `independent_review.py`: `IndependentReviewer` conducting double-blind evaluations without execution authorization authority.
10. `revision.py`: `RevisionLoopController` enforcing `MAX_REVISIONS = 3` ceiling and escalating upon threshold breach.
11. `trend_observation.py`: `TrendIntelligenceEngine` collecting external observations, marking them `UNTRUSTED_EXTERNAL_OBSERVATION`, and sanitizing prompt injection attempts.
12. `visual_dna.py`: `VisualDNAManager` extracting and comparing visual dimensions against brand and trend DNA.
13. `creative_direction.py`: `CreativeDirectionSynthesizer` synthesizing brand DNA, visual DNA, trend intelligence, and campaign objectives into inspectable creative direction briefs.
14. `workforce_memory.py`: `InstitutionalMemoryStore` appending organizational history linked to Phase 9 persistent learning.
15. `improvement.py`: `GovernedImprovementEngine` executing evaluation-first controlled experiments for workflow optimization, rejecting degraded strategy candidates and maintaining deterministic rollbacks.
16. `workforce_events.py`: `WorkforceEventStream` emitting secret-free operational events.
17. `workforce_ledger.py`: `WorkforceLedger` maintaining append-only SHA-256 hash-linked audit log in `data/phase14_workforce_ledger/`.
18. `workforce_orchestrator.py`: `CreativeWorkforceOrchestrator` main entry point interfacing between the Workforce Control Plane and Phases 8–13.
19. `__init__.py`: Clean exports.

---

## 3. Core Invariants Verified

- `INV-14-W001`: Capability $\neq$ Authority.
- `INV-14-W002`: Single Authorization Origin (`HumanAuthorizationBoundary`).
- `INV-14-W003`: Hierarchical Context Scope & Strict Client Isolation.
- `INV-14-W004`: Bounded Revision Loop (`MAX_REVISIONS = 3`).
- `INV-14-W005`: Non-authoritative Independent Review.
- `INV-14-W006`: External Observation Untrusted Status (`UNTRUSTED_EXTERNAL_OBSERVATION`).
- `INV-14-W007`: Evaluation-First Governed Improvement with Rollback.
