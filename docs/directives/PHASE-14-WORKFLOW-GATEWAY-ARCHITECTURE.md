# Phase 14 Architecture — Production Workflow Gateway & User Control Plane

**Document Status:** RATIFIED / COMPLETE  
**Phase:** 14 — Production Workflow Gateway & User Control Plane  
**Prerequisites:** Phases 1–13 COMPLETE & RATIFIED  

---

## 1. Executive Summary

Phase 14 establishes the **Production Workflow Gateway & User Control Plane** above the existing security substrate (`src/security_substrate/`), agentic work layer (`src/agentic_work/`), execution control plane (`src/execution_control/`), mission control plane (`src/mission_control/`), multi-mission coordination layer (`src/coordination/`), and external tool integration boundary (`src/integration_boundary/`).

The gateway transforms the engineering substrate into a unified, user-facing operating boundary. It enables end-users to specify high-level campaign objectives and brand constraints, review reviewable execution plans, grant explicit Phase 10 execution authorizations, observe live mission progress, pause/resume/cancel work, inspect cryptographic artifact lineage, and submit non-authoritative feedback to persistent learning without bypassing security boundaries.

---

## 2. Core Invariants & Architectural Principles

$$
\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}
$$

$$
\mathbf{User\ Control \neq AI\ Self\!-\!Authorization} \quad \Big| \quad \mathbf{Workflow\ State \neq Security\ State}
$$

- `INV-14-001`: **Single Authorization Origin:** All execution authorization originates from Phase 10 `HumanAuthorizationBoundary`. The gateway CANNOT manufacture authorization records.
- `INV-14-002`: **User Intent Is Not Authorization:** User objectives create workflow goals, NOT execution authority.
- `INV-14-003`: **Plan Before Effect:** Reviewable execution plans are required prior to any external side effect.
- `INV-14-004`: **Authorization Is Action-Bound:** Authorization tokens are capability-, mission-, scope-, nonce-, expiration-, and action-hash-bound.
- `INV-14-005`: **User Controls Mission Lifecycle:** `START`, `PAUSE`, `RESUME`, `CANCEL`, `APPROVE`, `REJECT`, `ESCALATE` controls delegate to existing control planes.
- `INV-14-006`: **Pause Continuation Boundary:** Pausing establishes a safe checkpoint; Resuming invokes Phase 11 revalidation.
- `INV-14-007`: **Terminal Cancellation:** Cancelled missions cannot silently restart.
- `INV-14-008`: **Feedback Is Learning Input:** Feedback is routed to Phase 9 learning, NOT security policy overrides.
- `INV-14-009`: **Epistemic Provenance Visibility:** Untrusted observations are never displayed as verified facts.
- `INV-14-010`: **Artifact Lineage Preservation:** surfaed artifacts include machine-verifiable ancestry and hash integrity commitments.
- `INV-14-011`: **Cross-Mission Isolation:** No cross-mission authorization, resource, or artifact leakage.
- `INV-14-012`: **No Hidden Side Effects:** All plan views, projections, and reviews are strictly side-effect free.
- `INV-14-013`: **External Failure Containment:** Provider failures remain visible operational outcomes.
- `INV-14-014`: **Security State Separation:** Workflow status and security authorization status remain distinct.

---

## 3. Package Architecture & Subservices

```text
Visual-Intelligence/product/backend/src/workflow_gateway/
├── exceptions.py             # Fail-closed exception hierarchy
├── models.py                 # Dataclasses (WorkflowRequest, Plan, Approval, View, Feedback)
├── plan_service.py           # Reviewable execution plan generator (side-effect free)
├── approval_service.py       # Facade over Phase 10 HumanAuthorizationBoundary
├── mission_service.py        # Controlled facade over Phase 11 Autonomous Mission Control
├── coordination_service.py   # Controlled facade over Phase 12 Multi-Mission Coordination
├── artifact_service.py       # Artifact lineage tracker & integrity verifier
├── feedback_service.py       # Ingests user feedback into Phase 9 learning
├── workflow_projection.py    # Secret-sanitized read view builder (WorkflowView)
├── event_stream.py           # System-generated secret-free workflow event bus
├── workflow_audit.py         # Multi-ledger audit correlator (Phase 7, 10, 11, 12, 13)
├── workflow_service.py       # Main facade orchestrating workflow lifecycle
└── __init__.py               # Package exports
```

---

## 4. End-to-End Workflow Lifecycle

```text
USER INTENT --> WORKFLOW SERVICE --> PHASE 11 MISSION CREATION --> PHASE 12 RESOURCE ADMISSION
                                           |
                                           v
USER REVIEW <-- WORKFLOW PROJECTION <-- PLAN SERVICE (Side-Effect Free Plan)
     |
     v
PHASE 10 HUMAN AUTHORIZATION --> AUTHORIZATION RECORD (Token)
                                           |
                                           v
PHASE 13 INTEGRATION CONTROLLER --> EXTERNAL PROVIDER ADAPTER (Sandbox Execution)
                                           |
                                           v
USER CONTROL PLANE <-- ARTIFACT & FEEDBACK SERVICE <-- PHASE 9 PERSISTENT LEARNING
```
