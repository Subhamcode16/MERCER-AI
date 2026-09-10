# PHASE-11-ARCHITECTURE-DIRECTIVE.md

# Phase 11 — Operational Autonomy & Mission Orchestration Boundary

**Document Status:** PROPOSED — AWAITING USER APPROVAL  
**Phase:** 11  
**Scope:** Long-running mission orchestration, multi-workflow coordination, scheduling, interruption/resumption, bounded autonomy, escalation, operational observability, resource budgets, and safe recovery  
**Prerequisites:** Phases 1–10 COMPLETE & RATIFIED  
**Current Baseline:** Phase 10 — 284/284 Pytests PASSED  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`, Phase 8 Agentic Work Directive, Phase 9 Persistent Learning Directive, Phase 10 Execution Directive

---

## 1. Purpose

Phase 11 establishes the **Operational Autonomy & Mission Orchestration Boundary**.

Phase 10 introduced controlled execution: the system can construct bounded execution plans and, where explicitly authorized, execute sandbox actions through capability-scoped adapters.

Phase 11 addresses the next architectural problem:

> How does the system operate continuously across many tasks and workflows without becoming an uncontrolled autonomous actor?

The objective is to transform the existing components into a bounded operational runtime capable of managing long-running missions, multiple concurrent workflows, task dependencies, scheduling, interruption/resumption, retries, escalation, resource budgets, execution checkpoints, operational observability, outcome evaluation, and controlled continuation.

The phase MUST NOT create unrestricted autonomy.

The governing model remains:

```text
INTELLIGENCE
    !=
AUTHORIZATION
    !=
EXECUTION AUTHORITY
    !=
SECURITY POLICY
```

And:

```text
AUTONOMY = BOUNDED CONTINUATION UNDER EXPLICIT POLICY
```

not:

```text
AUTONOMY = SELF-AUTHORIZATION
```

---

## 2. Architectural Position

```text
                    USER / ORGANIZATION
                           |
                           v
                    MISSION REQUEST
                           |
                           v
                 PHASE 11 MISSION LAYER
                           |
              +------------+------------+
              |            |            |
              v            v            v
          Scheduler   Mission DAG   Resource Budget
              |            |            |
              +------------+------------+
                           |
                           v
                  PHASE 8 WORK ORCHESTRATOR
                           |
                           v
                  AI STAFF / WORKFLOWS
                           |
                           v
               PHASE 9 LEARNING + KNOWLEDGE
                           |
                           v
              PHASE 6 DECISION / ATTESTATION
                           |
                           v
              PHASE 10 AUTHORIZATION BOUNDARY
                           |
                 +---------+---------+
                 |                   |
               DENY              AUTHORIZED
                                     |
                                     v
                              DRY RUN / PLAN
                                     |
                                     v
                           CONTROLLED EXECUTION
                                     |
                                     v
                              EXECUTION LEDGER
                                     |
                                     v
                             OUTCOME / FEEDBACK
                                     |
                                     v
                              PHASE 9 LEARNING
```

Phase 11 sits ABOVE the existing work and execution layers.

It coordinates them.

It does not replace them.

---

## 3. Core Design Principle

Phase 11 introduces a distinction between:

```text
MISSION
WORKFLOW
TASK
ACTION
EXECUTION
```

These are not interchangeable.

### Mission

A user-defined operational objective.

Example:

```text
Run the NOCAP monthly social campaign.
```

### Workflow

A bounded process required to accomplish part of the mission.

Example:

```text
Campaign research
Visual identity development
Content production
Review
Scheduling
Performance analysis
```

### Task

A discrete unit assigned to an AI staff role.

Example:

```text
Analyze current streetwear visual trends.
```

### Action

A capability-scoped operation that may create a side effect.

Example:

```text
CREATE_DRAFT
resource = campaign:nocap:september
```

### Execution

The actual invocation of a Phase 10 controlled adapter.

---

## 4. Non-Negotiable Invariants

### INV-11-001 — Mission Does Not Imply Authorization

Creating or running a mission MUST NOT authorize execution.

A mission may generate plans and requests.

Only the existing Phase 10 authorization boundary may authorize executable actions.

### INV-11-002 — Autonomous Continuation Is Policy-Bounded

The system may continue work automatically only while the mission remains within its predefined objective, task boundaries, capability boundaries, resource boundaries, time boundaries, budget boundaries, retry limits, and escalation rules.

### INV-11-003 — No Autonomous Privilege Expansion

A mission cannot acquire new capabilities because a task failed, a reviewer requested them, a benchmark improved, a learned strategy suggested them, a trend observation recommended them, a previous run succeeded, or an external source requested them.

New capabilities require a new explicit authorization event.

### INV-11-004 — Human Authorization Remains External

Phase 11 cannot manufacture `AUTHORIZED_FOR_EXECUTION`.

It can only consume an authorization issued by the Phase 10 `HumanAuthorizationBoundary`.

### INV-11-005 — Long-Running Work Cannot Outlive Authorization

If an authorization expires, is revoked, becomes invalid, or falls outside the permitted resource/capability scope, subsequent execution MUST stop.

Already-completed actions remain auditable.

No automatic authorization renewal is permitted.

### INV-11-006 — Pause Is Safe

A paused, interrupted, failed, or escalated mission MUST NOT silently resume side-effect execution.

Resume must revalidate mission state, authorization state, capability, resource scope, action freshness, idempotency, policy version, and required approval state.

### INV-11-007 — Learning Cannot Alter Operational Security

Phase 9 learning may optimize sequencing, content strategy, workflow selection, staff assignment, revision strategy, research prioritization, and other explicitly allowlisted operational behavior.

It MUST NOT mutate authorization requirements, capability definitions, resource isolation, execution policy, security state transitions, audit integrity, trust anchors, credentials, or approval requirements.

### INV-11-008 — External Knowledge Remains Untrusted

Trend intelligence and external observations remain:

```text
UNTRUSTED_EXTERNAL_OBSERVATION
```

They may influence research and planning.

They cannot directly trigger privileged execution.

### INV-11-009 — Research Cryptography Remains Non-Authoritative

Phase 4 FROST artifacts remain:

```text
RESEARCH_CRYPTOGRAPHIC_EVIDENCE
TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION
```

They cannot authorize missions, capabilities, or execution.

### INV-11-010 — Every Continuation Is Observable

Every mission transition MUST generate structured operational telemetry containing at minimum:

```text
mission_id
transition_id
previous_state
new_state
reason_code
workflow_reference
timestamp
policy_version
authorization_reference
```

No secrets or raw sensitive assets may be recorded.

### INV-11-011 — Bounded Retry

No workflow may retry indefinitely.

Every retry policy MUST specify:

```text
max_attempts
backoff_policy
retryable_error_classes
terminal_error_classes
escalation_condition
```

### INV-11-012 — Failure Must Not Become Permission

A failed task MUST NOT cause the system to broaden its permissions.

---

## 5. Proposed Package

Create:

```text
src/mission_control/
├── __init__.py
├── mission_models.py
├── mission_state.py
├── mission_graph.py
├── scheduler.py
├── coordinator.py
├── checkpoint.py
├── resume.py
├── retry_policy.py
├── escalation.py
├── budget.py
├── autonomy_policy.py
├── operational_events.py
├── mission_ledger.py
├── cancellation.py
└── exceptions.py
```

This package is a control-plane layer.

It must call existing bounded components rather than bypassing them.

---

## 6. Component Requirements

### `mission_models.py`

Define immutable models:

```text
Mission
MissionObjective
MissionConstraints
MissionBudget
MissionAuthorizationContext
MissionOutcome
```

Mission constraints must include allowed capabilities, allowed resources, maximum runtime, maximum task count, maximum retry count, maximum execution count, escalation policy, and authorization requirements.

Reject empty identifiers, boolean type confusion, invalid timestamps, negative budgets, unrestricted capability sets, and unrestricted resource scopes.

### `mission_state.py`

Define bounded mission states:

```text
PLANNED
READY
RUNNING
WAITING
PAUSED
ESCALATED
COMPLETED
FAILED
CANCELLED
BLOCKED
```

Forbidden transitions must raise explicit exceptions.

Resume must use an explicit controlled transition.

### `mission_graph.py`

Build a bounded DAG for workflows and tasks.

Requirements:

- cycle detection,
- maximum graph depth,
- maximum task count,
- dependency validation,
- deterministic ordering,
- blocked dependency propagation,
- no dynamically created privileged capabilities.

### `scheduler.py`

Provide bounded scheduling:

```text
RUN_NOW
RUN_AT
RUN_AFTER
WAIT_FOR_DEPENDENCY
RETRY
RESUME
```

It MUST NOT silently schedule an action beyond the authorization expiration window.

### `coordinator.py`

`MissionCoordinator` orchestrates:

```text
Mission
 -> Workflow
 -> Task
 -> WorkOrchestrator
 -> ExecutionPlan
 -> Phase 10 Authorization
 -> ExecutionController
 -> Outcome
```

It MUST NOT contain its own authorization implementation and MUST NOT invoke raw external APIs directly.

### `checkpoint.py`

Create controlled checkpoints containing mission state, graph state, completed task commitments, execution references, learning references, policy versions, and authorization references.

Secrets and raw assets are prohibited.

Checkpoint integrity must be verifiable.

### `resume.py`

Before resuming execution:

```text
validate checkpoint
validate mission policy
validate authorization
validate capability
validate resource scope
validate action idempotency
validate expiry
validate current security state
```

If any check fails:

```text
PAUSED / ESCALATED / BLOCKED
```

not automatic execution.

### `retry_policy.py`

Implement explicit retry policies.

Example:

```text
TRANSIENT_TIMEOUT:
    max_attempts = 3

HARD_AUTHORIZATION_FAILURE:
    max_attempts = 0

RESOURCE_SCOPE_VIOLATION:
    max_attempts = 0

TEMPORARY_ADAPTER_FAILURE:
    max_attempts = 2
```

Security failures MUST NOT be blindly retried.

### `escalation.py`

Implement structured escalation:

```text
HUMAN_REVIEW_REQUIRED
AUTHORIZATION_REQUIRED
RESOURCE_SCOPE_CONFLICT
POLICY_CONFLICT
REPEATED_FAILURE
QUALITY_FAILURE
BUDGET_EXCEEDED
SECURITY_ANOMALY
```

Escalation creates a waiting state.

It does not create authority.

### `budget.py`

Track mission-level limits:

```text
max_runtime
max_tasks
max_retries
max_executions
max_generated_assets
max_external_requests
```

Budget exhaustion must stop continuation.

### `autonomy_policy.py`

Define autonomy classes:

```text
AUTONOMOUS_RESEARCH
AUTONOMOUS_ANALYSIS
AUTONOMOUS_DRAFTING
AUTONOMOUS_REVISION
AUTONOMOUS_CRITIQUE
AUTONOMOUS_REVIEW
AUTHORIZED_EXECUTION
```

Only the first six may be autonomous by default.

`AUTHORIZED_EXECUTION` MUST remain dependent on Phase 10 authorization.

### `operational_events.py`

Define structured operational events:

```text
MISSION_CREATED
MISSION_STARTED
TASK_STARTED
TASK_COMPLETED
TASK_FAILED
TASK_RETRIED
EXECUTION_REQUESTED
EXECUTION_AUTHORIZED
EXECUTION_DENIED
MISSION_PAUSED
MISSION_ESCALATED
MISSION_RESUMED
MISSION_COMPLETED
MISSION_FAILED
MISSION_CANCELLED
```

### `mission_ledger.py`

Maintain an append-only mission history.

Every state transition must be hash-linked or otherwise integrity-verifiable.

Reuse Phase 7 audit primitives where appropriate rather than creating competing security mechanisms.

### `cancellation.py`

Support:

```text
USER_CANCEL
SYSTEM_CANCEL
SECURITY_CANCEL
BUDGET_CANCEL
AUTHORIZATION_CANCEL
```

Cancellation must be idempotent.

A cancelled mission cannot silently restart.

---

## 7. Integration With Existing Phases

### Phase 8

Phase 11 consumes Phase 8's `WorkOrchestrator`, task graphs, staff roles, critique, independent review, and workflow results.

Phase 11 must not duplicate these systems.

### Phase 9

Phase 11 sends operational outcomes to Phase 9:

```text
outcome
 -> feedback
 -> learning signal
 -> benchmark
 -> strategy optimization
```

Learning remains bounded.

### Phase 10

Phase 11 is the primary consumer of Phase 10's controlled execution interface:

```text
MissionCoordinator
        |
        v
ExecutionPlan
        |
        v
HumanAuthorizationBoundary
        |
        v
ExecutionController
        |
        v
Sandbox Adapter
```

The mission layer MUST NOT call adapters directly.

### Phases 1–7

Phase 11 cannot mutate epistemic state directly, bypass assurance, bypass evidence policy, bypass decision policy, bypass audit integrity, bypass recovery rules, unlock `ExecutionGate`, or create `VERIFIED` state.

---

## 8. Operational Autonomy Model

### Tier 0 — Advisory

The system analyzes, recommends, drafts, and critiques.

No execution.

### Tier 1 — Bounded Autonomous Work

The system may autonomously research, analyze, generate drafts, revise, critique, and organize tasks.

No externally consequential side effects.

### Tier 2 — Pre-Authorized Bounded Execution

The user explicitly authorizes a defined capability/resource/time scope.

The system may continue automatically within that exact boundary.

Example:

```text
Capability:
CREATE_DRAFT

Resource:
campaign:nocap:september

Duration:
24 hours

Maximum executions:
20

Allowed adapters:
SandboxContentPlatform
```

No scope expansion.

### Tier 3 — Human Escalation

Any action outside the current authorization boundary requires human intervention.

Examples:

```text
new capability
new account
new external platform
new resource
authorization expiry
destructive operation
policy conflict
budget increase
security anomaly
```

The system waits.

It does not improvise authority.

---

## 9. Required Real Workflow Benchmark

Phase 11 MUST include a realistic long-running benchmark:

```text
MISSION:
Operate a complete NOCAP social campaign for one campaign cycle.

DAY 0
User provides campaign brief.
        |
        v
MISSION PLANNING
        |
        +--> Research
        +--> Trend Intelligence
        +--> Brand Strategy
        +--> Visual Direction
        +--> Content Strategy
        |
        v
AI STAFF EXECUTION
        |
        +--> Designer
        +--> Content Specialist
        +--> Critic
        +--> Reviewer
        |
        v
QUALITY GATE
        |
        v
EXECUTION PLAN
        |
        v
HUMAN AUTHORIZATION
        |
        v
DRY RUN
        |
        v
SANDBOX EXECUTION
        |
        +--> CREATE_DRAFT
        +--> MODIFY_BRAND_ASSETS
        +--> SCHEDULE_CONTENT
        |
        v
CHECKPOINT
        |
        v
INTERRUPTION SIMULATION
        |
        v
SAFE PAUSE
        |
        v
RESUME
        |
        +--> Revalidate authorization
        +--> Revalidate scope
        +--> Revalidate idempotency
        |
        v
CONTINUATION
        |
        v
OUTCOME CAPTURE
        |
        v
PHASE 9 LEARNING SIGNAL
```

The benchmark must demonstrate continuity without silently increasing authority.

---

## 10. Threat Model — T11-1 Through T11-18

1. **Self-Authorization:** mission attempts to issue authorization — hard rejection.
2. **Authorization Expiry:** authorization expires while work continues — execution stops before the next side effect.
3. **Scope Expansion:** task requests a new resource — escalation.
4. **Capability Expansion:** workflow requests a capability outside mission scope — denial/escalation.
5. **Retry Amplification:** repeated failure causes unlimited retries — bounded retry and escalation.
6. **Resume After Cancellation:** cancelled mission is resumed — rejection.
7. **Resume After Revocation:** authorization revoked while paused — execution denied.
8. **Checkpoint Tampering:** checkpoint modified — integrity failure and safe halt.
9. **Dependency Cycle:** malformed task graph contains a cycle — graph rejected.
10. **Budget Exhaustion:** mission exceeds budget — controlled halt.
11. **Learning Escalation:** learned strategy requests privileged capability — `SecurityBoundaryViolation`.
12. **Trend Injection:** external observation attempts to inject an execution command — remains untrusted.
13. **Research Escalation:** FROST artifact presented as authorization — rejection.
14. **Concurrent Resume:** two workers resume same mission — exactly one valid transition.
15. **Duplicate Execution:** same action submitted concurrently — Phase 10 idempotency protection.
16. **Partial Failure:** multi-action mission fails after some actions complete — safe halt with accurate ledger.
17. **Security Boundary Mutation:** mission attempts to alter Phase 1–10 policies — impossible/rejected.
18. **Runaway Autonomous Loop:** workflow recursively generates work — bounded graph/task/depth limits and termination.

---

## 11. Test Plan

Create:

```text
tests/mission_control/
├── test_mission_models.py
├── test_mission_state.py
├── test_mission_graph.py
├── test_scheduler.py
├── test_coordinator.py
├── test_checkpoint.py
├── test_resume.py
├── test_retry_policy.py
├── test_escalation.py
├── test_budget.py
├── test_autonomy_policy.py
├── test_operational_events.py
├── test_mission_ledger.py
├── test_cancellation.py
├── test_phase11_security_boundary.py
├── test_phase11_concurrency.py
├── test_phase11_failure_recovery.py
└── test_phase11_real_workflow.py
```

Minimum coverage:

- model validation,
- mission state transitions,
- DAG cycle detection,
- scheduler bounds,
- authorization expiry,
- authorization revocation,
- capability scope,
- resource scope,
- checkpoint integrity,
- safe resume,
- cancellation,
- retry bounds,
- budget limits,
- escalation,
- concurrent mission transitions,
- concurrent duplicate resume,
- duplicate execution,
- partial failure,
- learning isolation,
- trend injection isolation,
- research isolation,
- runaway task generation,
- full sandbox real-workflow benchmark,
- Phase 1–10 regression.

---

## 12. Regression Requirement

Run:

```bash
python -m pytest tests/security_substrate tests/frost_prototype tests/workflow_integration tests/agentic_work tests/execution_control tests/mission_control -v
```

All previous tests MUST remain unchanged and passing.

Expected baseline:

```text
Phase 1–10 baseline: 284
Phase 11 additions: <N>
Final total: <284 + N>
Failures: 0
Skipped: 0
```

No previous security test may be weakened, removed, or modified merely to obtain a passing result.

---

## 13. Documentation Deliverables

Create:

```text
PHASE-11-MISSION-ARCHITECTURE.md
PHASE-11-OPERATIONAL-AUTONOMY-REVIEW.md
PHASE-11-THREAT-MODEL.md
PHASE-11-TEST-REPORT.md
PHASE-11-REAL-WORKFLOW-REPORT.md
PHASE-11-GOVERNANCE-GATE.md
```

The governance gate MUST machine-verify:

1. Can a mission authorize itself?
2. Can autonomy expand its own capabilities?
3. Can authorization expire safely during a mission?
4. Can a cancelled mission resume?
5. Can a paused mission bypass revalidation?
6. Can learning alter execution security policy?
7. Can external trend intelligence trigger privileged execution?
8. Can a FROST research artifact authorize execution?
9. Can retry loops become unbounded?
10. Can task graphs recursively grow without bounds?
11. Can duplicate workers resume the same mission?
12. Can duplicate actions produce duplicate side effects?
13. Can a mission cross resource boundaries?
14. Can budget exhaustion be bypassed?
15. Can a mission execute without audit telemetry?
16. Can Phase 11 mutate Phase 1–10 security invariants?
17. Can partial failure cause uncontrolled continuation?
18. Can the system safely cancel and recover?

---

## 14. Explicitly Prohibited

Phase 11 MUST NOT introduce:

- unrestricted autonomous execution,
- autonomous credential acquisition,
- autonomous privilege escalation,
- self-issued authorization,
- automatic authorization renewal,
- automatic approval of high-risk actions,
- production social credentials,
- unrestricted production API access,
- arbitrary shell execution,
- arbitrary code execution,
- unrestricted filesystem execution,
- production FROST,
- native YubiKey/PIV/TPM/HSM integration,
- security-policy mutation through learning,
- bypass of Phase 10 authorization,
- bypass of `ExecutionGate`,
- hidden background execution,
- silent mission continuation after security failure,
- infinite retries,
- unbounded task generation,
- destructive operations without explicit authorization,
- modification/deletion of previous security tests.

---

## 15. Acceptance Criteria

Phase 11 is complete only when:

- [ ] Mission model exists.
- [ ] Mission state machine exists.
- [ ] Mission DAG is bounded and cycle-safe.
- [ ] Scheduler is bounded.
- [ ] Mission coordinator integrates Phase 8–10 without bypasses.
- [ ] Authorization remains external.
- [ ] Authorization expiry is enforced.
- [ ] Authorization revocation is enforced.
- [ ] Resource scope is preserved.
- [ ] Capability scope is preserved.
- [ ] Safe checkpoints exist.
- [ ] Resume requires full revalidation.
- [ ] Cancellation is idempotent.
- [ ] Retry policies are bounded.
- [ ] Escalation is explicit.
- [ ] Mission budgets are enforced.
- [ ] Operational autonomy tiers are enforced.
- [ ] Learning cannot mutate security policy.
- [ ] External knowledge remains untrusted.
- [ ] Phase 4 research artifacts remain non-authoritative.
- [ ] Duplicate mission transitions are concurrency-safe.
- [ ] Duplicate execution is protected by Phase 10 idempotency.
- [ ] Partial failure halts safely.
- [ ] Runaway task generation is bounded.
- [ ] Every mission transition is observable and auditable.
- [ ] Real long-running sandbox workflow completes.
- [ ] Interruption/resumption benchmark succeeds.
- [ ] Threat matrix passes.
- [ ] Full Phase 1–10 regression passes.
- [ ] Security review is PASS or PASS WITH LIMITATIONS.
- [ ] Governance gate is independently documented.
- [ ] No prohibited production capability is introduced.

---

## 16. Engineer Instructions

Before implementation:

1. Inspect the actual Phase 1–10 repository interfaces and documentation.
2. Do not assume the walkthroughs are exact API contracts.
3. Produce an implementation-readiness assessment.
4. Map every Phase 11 dependency to an existing interface.
5. Identify any architectural conflict before modifying code.
6. Do not modify earlier phases merely to simplify Phase 11.
7. Reuse Phase 7 audit primitives and Phase 10 execution primitives where appropriate rather than creating competing security mechanisms.
8. Keep all external integrations sandbox/mock-only.
9. Implement tests alongside every control-plane component.
10. Run the complete Phase 1–11 regression suite.
11. Run AST/static dependency isolation checks.
12. Run runtime authorization-boundary tests.
13. Run concurrency tests.
14. Run checkpoint tampering and resume tests.
15. Run the long-running sandbox campaign benchmark.
16. Simulate interruption, authorization expiry, cancellation, partial execution, retry exhaustion, and recovery.
17. Verify Phase 9 learning cannot mutate Phase 1–10 security policy.
18. Produce all required Phase 11 documentation.
19. Report exact files changed.
20. Report exact tests added and exact test counts.
21. Report the exact final pytest output.
22. Report security findings and limitations.
23. Report the governance verdict.
24. Do not claim production readiness merely because the test suite passes.

---

## 17. Engineer Return Format

Return one complete engineering walkthrough containing:

```text
Phase 11 implementation status
Implementation-readiness assessment
Files created/modified
Architecture implemented
Mission/autonomy model
Authorization integration
Checkpoint/resume behavior
Retry/escalation behavior
Budget enforcement
Threat matrix results
Concurrency results
Real long-running workflow benchmark
Interruption/resumption benchmark
Regression test output
Security review verdict
Governance verdict
Known limitations
Explicit deferred capabilities
```

The engineering walkthrough must be returned as one complete Markdown document.

Do not proceed beyond Phase 11 without a new governance directive.

---

## 18. Approval Gate

**STATUS: AWAITING USER APPROVAL**

Recommended approval phrase:

```text
GREEN SIGNAL — PROCEED WITH PHASE 11
```

No implementation should begin until this approval is explicitly provided.
