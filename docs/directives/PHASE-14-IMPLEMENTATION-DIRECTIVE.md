# Phase 14 Implementation Directive — Production Workflow Gateway & User Control Plane

**Document Status:** PROPOSED / AWAITING USER APPROVAL  
**Phase:** 14 — Production Workflow Gateway & User Control Plane  
**Prerequisites:** Phases 1–13 COMPLETE & RATIFIED  
**Current Reported Regression Baseline:** 377 / 377 Pytests PASSED  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`

---

## 1. Objective

Phase 14 establishes the **Production Workflow Gateway & User Control Plane** above the existing mission, coordination, execution, and external-integration layers.

The objective is to transform the existing bounded engineering substrate into a coherent user-facing operating boundary through which a user can:

- define a real objective,
- establish constraints and brand/workspace context,
- review what the system intends to do,
- approve bounded actions,
- observe mission progress,
- pause/resume/cancel work,
- inspect artifacts and provenance,
- provide feedback,
- and retain explicit control over externally visible side effects.

Phase 14 must NOT introduce a second authorization system.

The architectural principle remains:

$$
\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}
$$

$$
\mathbf{User\ Control \neq AI\ Self\!-\!Authorization}
$$

$$
\mathbf{Workflow\ State \neq Security\ State}
$$

$$
\mathbf{Learning \neq Policy\ Mutation}
$$

The gateway is therefore an orchestration and user-control surface over Phases 8–13, not a replacement for their security boundaries.

---

# 2. Why Phase 14 Exists

Phases 8–13 established the internal machinery required for bounded autonomous work:

```text
Phase 8  -> AI Staff / Work Orchestration
Phase 9  -> Persistent Learning / Optimization
Phase 10 -> Human Authorization / Controlled Execution
Phase 11 -> Mission Autonomy / Resume / Retry / Escalation
Phase 12 -> Multi-Mission Coordination / Resource Governance
Phase 13 -> External Tool / Platform Integration
```

What remains is a coherent **operational product boundary** through which a real user can interact with that machinery.

Without such a boundary, the system remains primarily an engineering substrate and benchmark environment.

Phase 14 therefore establishes the canonical workflow lifecycle:

```text
USER
 |
 | objective + constraints
 v
WORKFLOW GATEWAY
 |
 +--> Mission Creation
 |
 +--> Context / Brand / Workspace Binding
 |
 +--> AI Planning
 |
 +--> Critique / Review
 |
 +--> User Review
 |
 +--> Authorization Request
 |
 +--> Human Authorization
 |
 +--> Mission Execution
 |
 +--> External Integration
 |
 +--> Artifact / Outcome Collection
 |
 +--> Feedback
 |
 v
LEARNING / FUTURE IMPROVEMENT
```

No stage may silently bypass the existing control planes.

---

# 3. Non-Negotiable Invariants

## `INV-14-001` — Single Authorization Origin

The gateway cannot issue execution authorization.

All execution authorization must continue to originate from Phase 10 `HumanAuthorizationBoundary`.

---

## `INV-14-002` — User Intent Is Not Authorization

A user saying:

```text
"Run my social campaign."
```

creates intent and a workflow objective.

It does not automatically create unrestricted execution authority.

The system must resolve the requested objective into explicit capabilities/actions and present the authorization boundary before externally visible side effects.

---

## `INV-14-003` — Plan Before Effect

The gateway must expose a reviewable execution plan before any external mutation.

At minimum, the user must be able to inspect:

- intended operation,
- target platform/provider,
- target resource,
- expected effect,
- mission,
- capability,
- authorization requirement,
- estimated cost/resource usage,
- relevant constraints,
- and current risk/status.

---

## `INV-14-004` — Authorization Is Action-Bound

Approval for:

```text
CREATE_DRAFT
```

must not authorize:

```text
PUBLISH_CONTENT
DELETE_CONTENT
MODIFY_BRAND_ASSETS
```

Authorization remains capability-, mission-, scope-, nonce-, expiration-, and action-hash-bound through Phase 10.

---

## `INV-14-005` — User Controls Mission Lifecycle

The gateway must provide explicit controls for:

```text
START
PAUSE
RESUME
CANCEL
APPROVE
REJECT
ESCALATE
```

These operations must delegate to the appropriate existing control plane rather than directly mutating protected internal state.

---

## `INV-14-006` — Pause Means Safe Continuation Boundary

Pausing a mission must prevent new work from beginning while preserving a valid checkpoint/resumption boundary.

Resume must invoke Phase 11's existing mandatory revalidation process.

---

## `INV-14-007` — Cancellation Is Terminal

A cancelled mission must not silently restart.

Any new attempt must create a new mission or follow an explicitly defined recovery path.

---

## `INV-14-008` — User Feedback Is Learning Input, Not Policy Override

Feedback may become a Phase 9 learning signal.

It may not directly mutate:

- security policy,
- capability allowlists,
- authorization rules,
- resource limits,
- execution permissions,
- governance constraints.

---

## `INV-14-009` — Knowledge Provenance Remains Visible

External observations and learned information must retain their provenance/status.

The gateway must not display untrusted observations as verified facts.

---

## `INV-14-010` — Artifact Lineage Is Preserved

Artifacts surfaced to the user must retain machine-verifiable ancestry back to the workflow/mission/task that produced them.

---

## `INV-14-011` — Cross-Mission Isolation

The user interface/API must not allow:

- Mission A artifacts to be silently attached to Mission B,
- Mission A authorization to be reused by Mission B,
- Mission A resources to be implicitly inherited by Mission B.

---

## `INV-14-012` — No Hidden Side Effects

Opening, viewing, reviewing, comparing, or editing a plan must not execute external mutations.

---

## `INV-14-013` — External Failure Does Not Become Success

Provider failures, partial failures, timeouts, rate limits, or reconciliation mismatches must remain visible as operational outcomes.

The gateway must not convert a failed external action into a successful mission result.

---

## `INV-14-014` — Security State Remains Separate

Workflow status, mission status, approval status, provider status, and epistemic security state must remain distinct.

No UI/API state such as:

```text
READY
REVIEWED
APPROVED_FOR_WORKFLOW
```

may be interpreted as:

```text
VERIFIED
AUTHORIZED_FOR_EXECUTION
```

unless it is the actual Phase 10 authorization state.

---

# 4. Proposed Package Structure

Create:

```text
Visual-Intelligence/product/backend/src/workflow_gateway/
```

## `models.py`

Immutable user/workflow contracts:

- `WorkflowRequest`
- `WorkflowObjective`
- `WorkflowConstraints`
- `WorkflowContext`
- `WorkflowPlan`
- `WorkflowApprovalRequest`
- `WorkflowView`
- `WorkflowOutcome`
- `ArtifactView`
- `FeedbackSubmission`

Reject:

- empty identifiers,
- boolean type confusion,
- arbitrary capability strings,
- cross-mission references.

---

## `workflow_service.py`

Canonical application-level workflow entry point.

Responsibilities:

- accept user intent,
- create mission,
- invoke Phase 8 planning,
- invoke Phase 11 mission control,
- invoke Phase 12 coordination,
- prepare Phase 10 approval requests,
- delegate Phase 13 external execution,
- collect outcomes,
- expose state.

It must not implement its own authorization logic.

---

## `plan_service.py`

Transforms mission/task state into a user-reviewable plan.

Must clearly separate:

```text
PROPOSED
AUTHORIZED
EXECUTING
COMPLETED
```

and never infer one state from another.

---

## `approval_service.py`

Presentation/integration layer over Phase 10 `HumanAuthorizationBoundary`.

Responsibilities:

- create approval request views,
- expose exact capability/scope/action hash,
- submit explicit approval/rejection,
- retrieve approval status.

It must never manufacture an `AuthorizationRecord`.

---

## `mission_service.py`

Controlled facade over Phase 11.

Supports:

- start,
- pause,
- resume,
- cancel,
- status,
- escalation inspection.

---

## `coordination_service.py`

Controlled facade over Phase 12.

Provides user-visible:

- resource status,
- mission priority,
- queued work,
- conflicts,
- preemption,
- starvation/escalation state.

It must not permit user/API requests to mutate immutable coordination security policy.

---

## `artifact_service.py`

Surfaces Phase 9 lineage/artifacts.

Every returned artifact must expose:

- artifact ID,
- mission ID,
- task ID,
- artifact type,
- lineage reference,
- integrity commitment,
- generation status,
- review status.

---

## `feedback_service.py`

Accepts structured user feedback and forwards it to Phase 9.

Feedback must include:

- workflow ID,
- mission ID,
- artifact/task reference,
- feedback classification,
- user-provided observation,
- timestamp,
- feedback ID.

Duplicate/replayed feedback must be rejected.

---

## `workflow_projection.py`

Produces a safe read model for UI/API clients.

The projection must not expose:

- provider secrets,
- credential handles,
- private cryptographic material,
- internal security keys,
- hidden prompts,
- private model state.

---

## `event_stream.py`

Structured workflow events:

```text
MISSION_CREATED
PLAN_READY
REVIEW_REQUIRED
APPROVAL_REQUIRED
APPROVED
REJECTED
TASK_STARTED
TASK_COMPLETED
TASK_FAILED
MISSION_PAUSED
MISSION_RESUMED
MISSION_CANCELLED
EXTERNAL_ACTION_STARTED
EXTERNAL_ACTION_COMPLETED
EXTERNAL_ACTION_FAILED
ESCALATION_CREATED
ARTIFACT_CREATED
FEEDBACK_RECEIVED
```

Events must remain secret-free.

---

## `workflow_audit.py`

Correlates gateway activity with existing:

- Phase 7 audit records,
- Phase 10 execution ledger,
- Phase 11 mission ledger,
- Phase 12 coordination ledger,
- Phase 13 integration ledger.

It must preserve the individual authority boundaries rather than replace them with one universal mutable log.

---

## `__init__.py`

Expose only the intended public gateway API.

---

# 5. API Boundary

Phase 14 should establish a transport-neutral service contract first.

Do NOT begin by coupling the architecture to a specific web framework.

Required logical operations:

```text
create_workflow()
get_workflow()
get_plan()
request_approval()
approve()
reject()
start()
pause()
resume()
cancel()
get_mission_status()
get_coordination_status()
list_artifacts()
get_artifact_lineage()
submit_feedback()
list_events()
```

If an HTTP adapter is added, it must be a thin transport layer over these services.

---

# 6. User Workflow Lifecycle

## Stage 1 — Intent

User submits:

```text
objective
constraints
brand/workspace context
desired platforms
desired output
```

The system creates a workflow request.

No external side effect occurs.

---

## Stage 2 — Planning

Phase 8 AI staff construct:

- research,
- strategy,
- visual direction,
- content,
- critique,
- review.

Phase 9 may contribute historical learning and external observations.

No learned behavior grants authorization.

---

## Stage 3 — Mission Formation

Phase 11 creates the bounded mission and task graph.

Phase 12 coordinates resources.

The gateway exposes the resulting plan.

---

## Stage 4 — User Review

The user sees:

- what will be produced,
- what will happen,
- what external systems are involved,
- which actions require authorization,
- expected resources,
- unresolved uncertainty,
- critique/review results,
- known limitations.

No side effect occurs.

---

## Stage 5 — Human Authorization

The gateway invokes Phase 10.

The user authorizes only the exact action/capability presented.

The authorization token remains downstream and opaque to the gateway except for required validation metadata.

---

## Stage 6 — Controlled Execution

Phase 13 performs the external operation.

The gateway observes the result but does not bypass:

- capability mapping,
- scope validation,
- environment guard,
- idempotency,
- rate limits,
- circuit breaker,
- reconciliation,
- audit.

---

## Stage 7 — Outcome

The user receives:

- success/failure,
- artifact,
- provider outcome,
- audit reference,
- lineage,
- unresolved issues,
- next recommended action.

---

## Stage 8 — Feedback

The user can state:

```text
better
worse
wrong direction
too generic
brand mismatch
good
needs revision
trend inaccurate
copy weak
visual hierarchy weak
```

The system stores this as structured feedback.

It does not immediately rewrite security or execution policy.

---

# 7. Threat Model

## T14-1 — API Authorization Bypass

Client calls an endpoint that directly triggers external execution without Phase 10 authorization.

**Required:** reject.

---

## T14-2 — UI Approval Confusion

A UI-level "approve plan" flag is interpreted as execution authorization.

**Required:** reject.

---

## T14-3 — Cross-Mission Action Reuse

Action/authorization from Mission A is submitted through Mission B.

**Required:** reject.

---

## T14-4 — Hidden Side Effect

Read/review endpoint accidentally invokes an external mutation.

**Required:** impossible by architecture and test.

---

## T14-5 — Feedback Policy Mutation

Malicious feedback attempts to alter security policy.

**Required:** feedback remains learning input only.

---

## T14-6 — Artifact Lineage Forgery

Client supplies fabricated artifact ancestry.

**Required:** lineage verification failure.

---

## T14-7 — Secret Exposure Through Projection

Credentials or internal security material appear in workflow views/events.

**Required:** zero leakage.

---

## T14-8 — Mission Lifecycle Bypass

Client directly mutates mission state outside Phase 11.

**Required:** reject / impossible.

---

## T14-9 — Approval Replay

Previously consumed approval is reused.

**Required:** Phase 10 replay protection remains authoritative.

---

## T14-10 — External Failure Misrepresentation

Provider failure appears as workflow success.

**Required:** reconciliation state remains failed/uncertain.

---

## T14-11 — Unauthorized Live Execution

A workflow marked "ready" reaches a live provider without explicit authorization.

**Required:** reject.

---

## T14-12 — Learning-Induced Capability Escalation

Persistent learning attempts to introduce a new capability.

**Required:** reject at existing security boundaries.

---

## T14-13 — Event Tampering

Client submits forged workflow events.

**Required:** events are system-generated only.

---

## T14-14 — Concurrent Lifecycle Race

Two clients simultaneously pause/resume/cancel or approve/reject the same workflow.

**Required:** deterministic state handling and idempotent lifecycle operations.

---

# 8. Required Test Suite

Create:

```text
Visual-Intelligence/product/backend/tests/workflow_gateway/
```

Required modules:

```text
test_models.py
test_workflow_service.py
test_plan_service.py
test_approval_service.py
test_mission_service.py
test_coordination_service.py
test_artifact_service.py
test_feedback_service.py
test_workflow_projection.py
test_event_stream.py
test_workflow_audit.py
test_phase14_security_boundary.py
test_phase14_isolation.py
test_phase14_concurrency.py
test_phase14_real_workflow.py
test_phase14_regression.py
```

---

# 9. Mandatory Real Workflow Benchmark

## NOCAP Autonomous Campaign — User-in-the-Loop Benchmark

Execute a deterministic end-to-end workflow representing a real user delegating social campaign work.

### Required sequence

```text
1. User creates campaign workflow
2. AI staff research + strategy + design + content
3. Critic evaluates output
4. Reviewer performs independent review
5. Mission is created
6. Resources are coordinated
7. User receives execution plan
8. User approves CREATE_DRAFT only
9. Phase 13 creates draft on MockSocialProvider
10. Artifact + lineage returned
11. User submits feedback: "visual direction too generic"
12. Feedback becomes bounded learning input
13. System creates revision task
14. Revised artifact passes critique/review
15. User approves the revised CREATE_DRAFT
16. Second draft is created
17. Attempted PUBLISH_CONTENT without authorization is blocked
18. Attempted cross-mission authorization reuse is blocked
19. Mission completes
20. All applicable ledgers verify integrity
```

### Mandatory assertions

```text
workflow creation              -> SUCCESS
planning                       -> SUCCESS
critique/review                -> SUCCESS
human approval                 -> REQUIRED
authorized CREATE_DRAFT        -> SUCCESS
artifact lineage               -> VERIFIED
feedback ingestion             -> SUCCESS
revision                       -> BOUNDED
unauthorized PUBLISH_CONTENT   -> BLOCKED
cross-mission reuse            -> BLOCKED
learning policy mutation       -> IMPOSSIBLE
secret leakage                 -> NONE
ledger integrity               -> PASS
```

---

# 10. Concurrency Requirements

The gateway must be safe under concurrent clients.

At minimum test:

- simultaneous status reads,
- simultaneous pause/resume,
- simultaneous cancellation,
- duplicate approval submissions,
- duplicate feedback submissions,
- concurrent artifact reads,
- concurrent event retrieval.

State transitions must remain deterministic.

---

# 11. Verification Plan

Run:

```bash
python -m pytest tests/security_substrate \
tests/frost_prototype \
tests/workflow_integration \
tests/agentic_work \
tests/execution_control \
tests/mission_control \
tests/coordination \
tests/integration_boundary \
tests/workflow_gateway -v
```

Acceptance requirements:

1. Existing Phase 1–13 tests remain green.
2. All Phase 14 tests pass.
3. No production credential is required.
4. No real social platform is contacted.
5. No security boundary is weakened.
6. No duplicate authorization system is introduced.
7. All read/review operations remain side-effect-free.
8. All external mutations remain subordinate to Phase 10.
9. Mission lifecycle remains subordinate to Phase 11.
10. Resource coordination remains subordinate to Phase 12.
11. External calls remain subordinate to Phase 13.
12. Learning remains subordinate to Phase 9 governance.
13. Artifact lineage remains verifiable.
14. Gateway events remain secret-free.
15. Mandatory NOCAP benchmark passes.

---

# 12. Governance Requirements

Phase 14 is explicitly prohibited from introducing:

- autonomous human-approval simulation,
- hidden approval defaults,
- "approve all" authorization,
- wildcard execution scopes,
- automatic publication,
- automatic deletion,
- automatic account creation,
- automatic credential acquisition,
- direct provider calls from UI handlers,
- direct `ExecutionGate` mutation,
- direct `EpistemicStateStore` mutation,
- security-policy changes from feedback,
- capability allowlist changes from learning,
- FROST-based authorization,
- production secret-management infrastructure unless separately authorized.

---

# 13. Required Documentation Deliverables

Create:

1. `PHASE-14-WORKFLOW-GATEWAY-ARCHITECTURE.md`
2. `PHASE-14-SECURITY-REVIEW.md`
3. `PHASE-14-THREAT-MODEL.md`
4. `PHASE-14-TEST-REPORT.md`
5. `PHASE-14-REAL-WORKFLOW-REPORT.md`
6. `PHASE-14-GOVERNANCE-GATE.md`

The governance document must explicitly state:

> Phase 14 establishes a user-facing workflow control boundary over the existing agentic, mission, coordination, execution, and external-integration layers. It does not create independent authorization authority. Human authorization remains the sole source of execution authorization, and all external side effects remain subordinate to the existing Phase 10–13 controls.

---

# 14. Engineer Instruction

**DO NOT IMPLEMENT PHASE 14 UNTIL THE USER EXPLICITLY APPROVES THIS DIRECTIVE.**

After approval:

1. Inspect the complete Phase 1–13 implementation and documentation before changing code.
2. Identify and preserve all existing public APIs and invariants.
3. Implement the gateway as a facade/control boundary, not as a replacement architecture.
4. Do not duplicate authorization, execution, mission, coordination, or integration logic.
5. Keep transport concerns separate from domain services.
6. Use deterministic local/mock infrastructure for all tests.
7. Do not introduce real provider credentials.
8. Do not contact live external platforms.
9. Test every read path for side-effect freedom.
10. Test concurrent lifecycle operations.
11. Run targeted Phase 14 tests.
12. Run the complete regression suite.
13. Run AST/import isolation audits.
14. Run the mandatory NOCAP user-in-the-loop benchmark.
15. Verify all relevant ledger integrity.
16. Inspect logs/events for secret leakage.
17. Produce all six documentation deliverables.
18. Report exact files changed.
19. Report exact test counts and runtime.
20. Report every failure encountered and its root cause/fix.
21. Report security findings and limitations.
22. Report the final governance verdict.

**Approval State:** `AWAITING USER GREEN SIGNAL`
