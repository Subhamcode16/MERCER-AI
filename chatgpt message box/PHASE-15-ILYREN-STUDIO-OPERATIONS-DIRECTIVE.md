# PHASE 15 — ILYREN Creative Studio Operational Continuity & Production Readiness Boundary

**Document Status:** PROPOSED — Awaiting User Approval  
**Phase:** 15  
**Program:** ILYREN Creative Workforce  
**Primary Objective:** Convert the Phase 14 governed creative workforce into a continuously operable, production-oriented studio control plane capable of managing real client work across campaigns, channels, assets, approvals, execution, observation, and post-work learning.

**Prerequisites:** Phases 1–14 COMPLETE / RATIFIED  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`, Phase 8 Agentic Work Directive, Phase 10 Execution Boundary, Phase 11 Mission Control, Phase 12 Coordination Boundary, Phase 13 Integration Boundary, Phase 14 Creative Workforce Boundary.

---

## 1. Why Phase 15 Exists

Phase 14 established the organizational intelligence layer for ILYREN Creative Studio:

- departments and staff roles,
- client and campaign context,
- workforce delegation,
- creative direction,
- collaboration,
- self-critique,
- independent review,
- revision control,
- trend intelligence,
- Visual DNA,
- institutional memory,
- governed improvement,
- workforce orchestration.

However, a creative workforce becomes genuinely useful to a studio only when it can maintain **operational continuity** around real client work.

Phase 15 therefore does **not** primarily add more AI staff.

Instead, it establishes the layer that allows an ILYREN client engagement to persist as a governed operating lifecycle:

```text
CLIENT
  ↓
BRAND
  ↓
CAMPAIGN
  ↓
MISSION
  ↓
WORKFORCE
  ↓
ARTIFACTS
  ↓
CRITIQUE / REVIEW
  ↓
REVISION
  ↓
HUMAN APPROVAL
  ↓
CONTROLLED EXTERNAL EXECUTION
  ↓
OBSERVATION / OUTCOME
  ↓
LEARNING
  ↓
IMPROVEMENT
  ↓
NEXT WORK CYCLE
```

The objective is to make the system capable of **continuing work**, not merely completing isolated tasks.

---

## 2. Core Architectural Position

Phase 15 sits above and coordinates the already-established boundaries:

```text
                    ILYREN CREATIVE STUDIO
                             │
                  ┌──────────▼──────────┐
                  │ Phase 15             │
                  │ Operational          │
                  │ Continuity Plane     │
                  └──────────┬──────────┘
                             │
       ┌─────────────────────┼──────────────────────┐
       │                     │                      │
 Phase 14              Phase 11/12             Phase 13
 Creative Workforce    Mission/Coordination    External Integration
       │                     │                      │
       └─────────────────────┼──────────────────────┘
                             │
                         Phase 10
                   Human Authorization
                             │
                         Phase 1–7
                    Security Substrate
```

Phase 15 is therefore a **control-plane continuity layer**, not a replacement for the lower-level security and execution boundaries.

---

## 3. Non-Negotiable Invariants

### INV-15-001 — Intelligence Does Not Become Authority

```text
Intelligence ≠ Authorization ≠ Execution Authority ≠ Security Policy
```

No workforce component, strategy engine, reviewer, learner, optimizer, scheduler, or continuity manager may create authorization.

### INV-15-002 — Continuity Does Not Mean Unbounded Autonomy

```text
Continuity ≠ Self-Authorization
```

The system may continue planning, researching, drafting, reviewing, learning, and preparing work under explicit policy.

Side-effect execution remains subject to Phase 10 authorization.

### INV-15-003 — Client Isolation Is Absolute

```text
Client A Context ≠ Client B Context
```

No memory, trend observation, artifact, credential reference, brand asset, strategy, or campaign context may cross client boundaries without an explicit governed transfer mechanism.

### INV-15-004 — Brand Identity Is Context-Bound

A client's Visual DNA, brand rules, tone, assets, and historical strategy must remain bound to that client's context.

The system may learn generalized workflow patterns without silently transferring client-specific identity information.

### INV-15-005 — Learning Cannot Mutate Security Policy

```text
Learning → Strategy Improvement
Learning ↛ Security Policy Mutation
```

Persistent learning may improve creative workflow strategies, but cannot change authorization rules, execution capabilities, security boundaries, credential-access policy, autonomy ceilings, client isolation rules, or audit requirements.

### INV-15-006 — External Reality Is Observed, Not Automatically Trusted

External platform responses, analytics, trends, public design observations, comments, and market signals remain observations.

```text
External Observation ≠ Trusted Fact
```

### INV-15-007 — Every External Mutation Remains Capability Scoped

The continuity plane may request an action, but Phase 13 and Phase 10 remain authoritative for whether that action may execute.

### INV-15-008 — Human Authorization Remains the Production Side-Effect Boundary

The system may prepare posts, campaigns, schedules, assets, captions, content calendars, and publishing plans without authorization.

Production side effects require valid authorization from the established human authorization boundary.

### INV-15-009 — No Autonomous Security Boundary Modification

Self-improvement cannot modify, disable, bypass, or replace any security substrate boundary.

### INV-15-010 — Operational History Must Be Auditable

Every meaningful lifecycle transition must produce structured, secret-free audit evidence.

---

## 4. Phase 15 Objectives

Phase 15 shall establish:

1. Persistent client engagement lifecycle management.
2. Continuous campaign/workstream state.
3. Production-ready workflow queues.
4. Recurring work planning.
5. Client-specific operating policies.
6. Asset and deliverable lifecycle management.
7. Human approval queues.
8. External execution scheduling coordination.
9. Post-execution outcome ingestion.
10. Campaign performance observation.
11. Cross-cycle learning.
12. Operational health monitoring.
13. Recovery from interrupted workflows.
14. Controlled handoff between AI workforce and human operators.
15. Production-readiness validation through long-running realistic workflows.

---

## 5. Proposed Package

Create:

```text
src/studio_operations/
```

The package should become the operational backbone of ILYREN Creative Studio.

---

## 6. Proposed Source Manifest

### 6.1 `exceptions.py`

Define fail-closed operational exceptions:

- `StudioOperationError`
- `ClientContextViolation`
- `CampaignStateViolation`
- `DeliverableStateViolation`
- `ApprovalRequiredError`
- `ApprovalExpiredError`
- `OperationalPolicyViolation`
- `ContinuityViolation`
- `ScheduleConflictError`
- `ProductionReadinessError`
- `ExternalOutcomeValidationError`

Security-sensitive exceptions must remain non-swallowable.

### 6.2 `studio_models.py`

Immutable contracts for:

- `StudioClient`
- `StudioBrand`
- `ClientOperatingPolicy`
- `Campaign`
- `Workstream`
- `Deliverable`
- `DeliverableType`
- `OperationalPriority`
- `CampaignCadence`
- `StudioCycle`
- `OperationalObjective`

Reject missing values, empty/whitespace strings, boolean type confusion, invalid timestamps, and invalid identifiers.

### 6.3 `client_operations.py`

`ClientOperationsManager`

Responsibilities:

- create client operating contexts,
- bind brands,
- establish operating policies,
- enforce client isolation,
- manage client lifecycle,
- expose read-only client summaries.

No credential material may be stored here.

### 6.4 `campaign_manager.py`

`CampaignLifecycleManager`

Responsibilities:

- campaign creation,
- campaign activation,
- campaign pausing,
- campaign completion,
- campaign cancellation,
- campaign resumption,
- campaign health status.

Campaign transitions must be explicit and finite-state controlled.

### 6.5 `workstream.py`

`WorkstreamManager`

Represent persistent creative workstreams such as:

- social content,
- visual design,
- brand development,
- campaign strategy,
- trend intelligence,
- community content,
- analytics,
- creative experimentation.

Workstreams should support recurring cycles.

### 6.6 `deliverables.py`

`DeliverableManager`

Lifecycle:

```text
PLANNED
→ IN_PROGRESS
→ DRAFT
→ CRITIQUE
→ REVISION
→ REVIEW
→ APPROVED
→ READY_FOR_EXECUTION
→ EXECUTED
→ OBSERVED
→ LEARNED
```

Failure or rejection states must remain explicit.

No `APPROVED` state may imply execution authorization.

### 6.7 `approval_queue.py`

`ApprovalQueue`

Provides a structured human-facing approval queue containing client, campaign, workstream, deliverable, proposed action, capability, target platform, risk classification, artifact references, critique summary, independent review, planned effect, expiration, and authorization requirements.

The queue may **request approval**, but cannot manufacture approval.

### 6.8 `operational_scheduler.py`

`StudioOperationalScheduler`

Provides bounded scheduling for recurring content cycles, research windows, campaign deadlines, review deadlines, approval reminders, post-publication observation, analytics collection, and learning cycles.

Scheduling must never bypass Phase 10/13 authorization.

### 6.9 `continuity_engine.py`

`OperationalContinuityEngine`

Core responsibility:

> Determine what should happen next in an active client/campaign lifecycle.

Inputs include campaign state, incomplete work, dependencies, previous outcomes, approvals, deadlines, resource availability, learning signals, and trend observations.

Outputs include next bounded work items, required human decisions, escalation events, waiting conditions, and retry/resume instructions.

It must not directly execute external side effects.

### 6.10 `handoff.py`

`HumanHandoffManager`

Generates structured handoffs for approval, ambiguity, conflicting creative direction, failed reviews, policy conflicts, external platform failures, high-risk execution, missing credentials, exhausted revisions, and unresolved client requirements.

### 6.11 `outcomes.py`

`OutcomeObservationEngine`

Consumes post-execution observations such as engagement metrics, content performance, platform responses, asset outcomes, campaign milestones, and human feedback.

All incoming external data remains observational.

### 6.12 `performance.py`

`StudioPerformanceEngine`

Calculates turnaround time, revision count, review acceptance rate, approval latency, execution success rate, campaign completion rate, recurring defect rate, workflow efficiency, and learning improvement delta.

No performance score may directly modify security policy.

### 6.13 `cycle_manager.py`

`StudioCycleManager`

Represents recurring operational periods.

Example:

```text
MONTH
 ├── WEEK 1
 │    ├── RESEARCH
 │    ├── STRATEGY
 │    └── CONTENT
 ├── WEEK 2
 │    ├── PRODUCTION
 │    └── REVIEW
 ├── WEEK 3
 │    ├── EXECUTION
 │    └── OBSERVATION
 └── WEEK 4
      ├── ANALYSIS
      ├── LEARNING
      └── NEXT-CYCLE PLANNING
```

Cycles must remain bounded and inspectable.

### 6.14 `operational_policy.py`

`StudioOperationalPolicy`

Defines client-specific operational policies including content cadence, review requirements, approval requirements, campaign priorities, allowed platforms, allowed capability classes, escalation thresholds, and revision ceilings.

Security-sensitive restrictions cannot be weakened by client policy.

### 6.15 `readiness.py`

`ProductionReadinessEngine`

Evaluates whether a client/workstream/campaign is ready for operational deployment.

Checks include valid client context, valid brand context, complete campaign objective, valid workforce assignment, artifact lineage, review completion, approval requirements, integration availability, authorization readiness, audit readiness, and rollback/recovery readiness.

Readiness must not itself authorize execution.

### 6.16 `studio_ledger.py`

`StudioOperationsLedger`

Append-only, hash-linked operational history recording lifecycle changes, workstream transitions, deliverable transitions, approvals requested/received, executions, external outcomes, escalations, learning cycles, and improvement experiments.

No secrets.

### 6.17 `health.py`

`StudioHealthMonitor`

Reports stalled campaigns, overdue approvals, repeated failures, integration degradation, excessive revisions, resource starvation, anomalous workflow behavior, and unresolved escalations.

Health monitoring remains advisory/control-plane functionality.

### 6.18 `orchestrator.py`

`StudioOperationsOrchestrator`

The Phase 15 primary entry point.

It coordinates:

```text
Client
 ↓
Brand
 ↓
Campaign
 ↓
Workstreams
 ↓
Creative Workforce
 ↓
Deliverables
 ↓
Review
 ↓
Approval Queue
 ↓
Execution Boundary
 ↓
Outcome Observation
 ↓
Learning
 ↓
Next Cycle
```

The orchestrator must not possess:

- `authorize()`
- `unlock()`
- unrestricted `execute()`
- credential extraction
- security policy mutation

### 6.19 `__init__.py`

Export approved public Phase 15 interfaces.

---

## 7. Operational Data Flow

A standard client cycle should resemble:

```text
CLIENT OBJECTIVE
      ↓
CLIENT OPERATING CONTEXT
      ↓
CAMPAIGN PLAN
      ↓
WORKSTREAM GENERATION
      ↓
PHASE 14 CREATIVE WORKFORCE
      ↓
ARTIFACT PRODUCTION
      ↓
SELF-CRITIQUE
      ↓
INDEPENDENT REVIEW
      ↓
REVISION LOOP
      ↓
READINESS CHECK
      ↓
HUMAN APPROVAL
      ↓
PHASE 10 AUTHORIZATION
      ↓
PHASE 13 INTEGRATION
      ↓
EXTERNAL SIDE EFFECT
      ↓
OUTCOME OBSERVATION
      ↓
PHASE 9 LEARNING
      ↓
PERFORMANCE EVALUATION
      ↓
NEXT OPERATIONAL CYCLE
```

---

## 8. Critical Architectural Distinction

Phase 15 introduces **continuity**, not unrestricted autonomy.

The distinction is:

```text
Autonomous Planning
        ≠
Autonomous Authorization
        ≠
Autonomous Security Mutation
```

The system may wake up because a scheduled work cycle is due and determine:

> "NOCAP has three unfinished content deliverables and one pending review."

It may then assign staff, research, create drafts, critique, revise, prepare approval packages, schedule observations, and analyze previous performance.

But if the next step is:

> "Publish this post."

the system must stop at the established authorization boundary unless valid authorization exists.

---

## 9. Continuous Improvement Model

```text
WORK
 ↓
OUTCOME
 ↓
OBSERVATION
 ↓
EVALUATION
 ↓
FEEDBACK
 ↓
PATTERN
 ↓
CONTROLLED EXPERIMENT
 ↓
BENCHMARK
 ↓
ADOPT / REJECT
 ↓
NEXT WORK CYCLE
```

The system should become better at planning, delegation, creative direction, review, revision, scheduling, resource allocation, workflow sequencing, and client-specific operating patterns.

It must never become better at bypassing its own security boundaries.

---

## 10. Real-World Design Intelligence Boundary

Phase 15 should integrate the existing Phase 9 and Phase 14 trend/Visual DNA systems into recurring operational cycles:

```text
External Design Observation
        ↓
UNTRUSTED_EXTERNAL_OBSERVATION
        ↓
Normalization
        ↓
Visual DNA Extraction
        ↓
Comparison Against Client DNA
        ↓
Creative Direction Signal
        ↓
Human/AI Review
        ↓
Campaign Application
        ↓
Performance Observation
```

The objective is not blind trend copying. The system should identify emerging visual languages, typography movement, composition patterns, color-system changes, campaign structures, content formats, and platform-native creative patterns, then determine whether a trend is compatible with a client's identity.

---

## 11. Multi-Client Operating Model

```text
ILYREN
│
├── Client A
│   ├── Brand
│   ├── Campaigns
│   └── Workstreams
│
├── Client B
│   ├── Brand
│   ├── Campaigns
│   └── Workstreams
│
└── NOCAP
    ├── Brand
    ├── Campaigns
    └── Workstreams
```

A client-specific workforce context must never leak into another client. Shared generalized knowledge may be represented only at the appropriate abstraction level.

---

## 12. Production Readiness Strategy

### LEVEL 0 — SIMULATION

- mock providers,
- synthetic outcomes,
- no production credentials,
- no live mutations.

### LEVEL 1 — CONTROLLED PILOT

- real client context,
- real assets,
- real external integrations where explicitly authorized,
- human approval for every side effect,
- enhanced audit.

### LEVEL 2 — PRODUCTION OPERATIONS

Only after explicit governance approval.

Requirements:

- validated integrations,
- operational monitoring,
- incident recovery,
- credential management,
- backup/recovery procedures,
- audit retention,
- real client workflows,
- failure drills,
- human escalation coverage.

Phase 15 implementation itself must not silently move the system into Level 2.

---

## 13. Threat Model

The engineer must explicitly test at least:

- **T15-1 Client Context Leakage:** Client A data accessed from Client B context → fail closed.
- **T15-2 Continuous Loop Authorization Escalation:** recurring workflow permission converted into execution authorization → rejected.
- **T15-3 Approval Queue Forgery:** `APPROVED` created without valid human authorization → rejected.
- **T15-4 Schedule-to-Execution Bypass:** scheduler invokes external side effects without authorization → rejected.
- **T15-5 Learning-to-Policy Escalation:** adaptive strategy mutates security policy → rejected.
- **T15-6 Trend Injection:** malicious instructions injected into external trend observations → sanitized/quarantined.
- **T15-7 Cross-Client Memory Contamination:** another client's historical memory retrieved → fail closed.
- **T15-8 Deliverable State Forgery:** review/approval states skipped → rejected.
- **T15-9 Interrupted Cycle Recovery:** corrupted checkpoint resumed → recovery blocked.
- **T15-10 Duplicate External Action:** continuity retry duplicates execution → Phase 10/13 idempotency prevents duplication.
- **T15-11 Infinite Operational Loop:** recurring work regenerates indefinitely without progress → bounded iteration and escalation.
- **T15-12 Human Handoff Suppression:** mandatory human decision bypassed → blocked.
- **T15-13 External Outcome Manipulation:** fabricated platform outcomes injected → remain observational and rejected from trusted paths where validation is required.
- **T15-14 Audit Tampering:** lifecycle records modified → integrity failure detected.
- **T15-15 Self-Improvement Boundary Violation:** improvement candidate modifies operational/security boundary code → rejected.

---

## 14. Required Test Structure

Create:

```text
tests/studio_operations/
```

Minimum modules:

```text
test_studio_models.py
test_client_operations.py
test_campaign_manager.py
test_workstream.py
test_deliverables.py
test_approval_queue.py
test_operational_scheduler.py
test_continuity_engine.py
test_handoff.py
test_outcomes.py
test_performance.py
test_cycle_manager.py
test_operational_policy.py
test_readiness.py
test_studio_ledger.py
test_health.py
test_studio_orchestrator.py
test_phase15_security_boundary.py
test_phase15_client_isolation.py
test_phase15_real_workflow.py
test_phase15_regression.py
```

---

## 15. Mandatory Real Workflow Benchmark

### `ILYREN Creative Studio — NOCAP 30-Day Operating Cycle`

The benchmark must evolve the existing NOCAP campaign from a one-shot workflow into a **multi-cycle operational engagement**.

Required stages:

1. Establish client operating context.
2. Load NOCAP brand/Visual DNA.
3. Initialize 30-day campaign.
4. Generate recurring workstreams.
5. Perform trend intelligence intake.
6. Create weekly creative direction.
7. Generate multiple content concepts.
8. Produce campaign assets.
9. Run self-critique.
10. Run independent review.
11. Execute bounded revisions.
12. Submit approval package.
13. Obtain explicit human authorization.
14. Execute through Phase 13 sandbox/provider boundary.
15. Collect simulated platform outcomes.
16. Evaluate performance.
17. Generate learning signals.
18. Run governed improvement experiment.
19. Benchmark candidate strategy.
20. Prepare next weekly cycle.
21. Simulate interruption.
22. Resume from checkpoint.
23. Verify client isolation.
24. Verify audit integrity.
25. Complete 30-day operational report.

The benchmark must demonstrate **continuity across multiple work cycles**, not simply a larger task graph.

---

## 16. Required Regression

Run:

```bash
python -m pytest tests/security_substrate tests/frost_prototype tests/workflow_integration tests/agentic_work tests/mission_control tests/coordination tests/integration_boundary tests/creative_workforce tests/studio_operations -v
```

The engineer must verify:

```text
Phase 1–14 baseline remains intact.
No existing security boundary tests are modified to hide regressions.
No test is deleted merely to achieve a pass.
No Phase 4 research test is weakened.
```

---

## 17. Required Documentation Deliverables

Create:

```text
PHASE-15-STUDIO-OPERATIONS-ARCHITECTURE.md
PHASE-15-OPERATIONAL-SECURITY-REVIEW.md
PHASE-15-THREAT-MODEL.md
PHASE-15-TEST-REPORT.md
PHASE-15-REAL-WORKFLOW-REPORT.md
PHASE-15-PRODUCTION-READINESS-REVIEW.md
PHASE-15-GOVERNANCE-GATE.md
```

The governance gate must explicitly state whether the system is:

```text
SIMULATION ONLY
CONTROLLED PILOT READY
PRODUCTION READY
```

The engineer must not claim production readiness merely because automated tests pass.

---

## 18. Acceptance Criteria

Phase 15 may be considered complete only if:

- [ ] Client contexts are persistent and isolated.
- [ ] Multiple campaigns can operate concurrently.
- [ ] Workstreams can recur without creating infinite loops.
- [ ] Deliverables have a governed lifecycle.
- [ ] Human approvals are explicit and non-forgeable.
- [ ] Scheduling cannot bypass authorization.
- [ ] External execution remains inside Phase 10/13.
- [ ] Outcomes remain observational until validated.
- [ ] Learning remains separated from security policy.
- [ ] Cross-client memory leakage is prevented.
- [ ] Interrupted workflows can safely resume.
- [ ] Operational audit history is tamper-evident.
- [ ] Health monitoring detects stalled or degraded workflows.
- [ ] Self-improvement remains rollback-capable.
- [ ] NOCAP 30-day workflow benchmark passes.
- [ ] Full regression suite passes.
- [ ] No existing tests were weakened or removed.
- [ ] Production readiness is assessed honestly.

---

## 19. Explicit Non-Scope

Phase 15 must NOT implement:

- autonomous credential acquisition,
- unrestricted autonomous publishing,
- autonomous financial transactions,
- autonomous security-policy modification,
- autonomous identity management,
- unrestricted browser control,
- unrestricted shell execution,
- production hardware custody,
- production FROST authorization,
- autonomous legal/contractual decisions,
- silent client-data sharing,
- bypass mechanisms for human approval.

These remain deferred unless a future governance directive explicitly authorizes them.

---

## 20. Engineer Execution Instructions

Implement Phase 15 as a **new bounded control-plane layer**.

The engineer must:

1. Read and respect all Phase 1–14 architecture and governance documentation.
2. Inspect existing interfaces before creating replacements.
3. Reuse Phase 8 workforce orchestration rather than duplicating staff logic.
4. Reuse Phase 9 learning and memory boundaries.
5. Reuse Phase 10 human authorization and execution controls.
6. Reuse Phase 11 mission continuity mechanisms where applicable.
7. Reuse Phase 12 coordination mechanisms for concurrent client/campaign resource governance.
8. Reuse Phase 13 integration controls for every external side effect.
9. Reuse Phase 14 client/workforce context and creative direction systems.
10. Do not create a parallel authorization system.
11. Do not create a parallel credential system.
12. Do not create a second execution path.
13. Keep external observations explicitly untrusted.
14. Keep research cryptography permanently isolated.
15. Maintain fail-closed behavior.
16. Add security tests before declaring implementation complete.
17. Add the mandatory NOCAP 30-day benchmark.
18. Run the entire regression suite.
19. Perform AST/runtime isolation audits.
20. Produce all seven Phase 15 documentation deliverables.
21. Report limitations honestly.
22. Do not declare Phase 15 ratified until implementation, security review, real-workflow benchmark, and governance gate have all passed.

---

## 21. Final Architectural Intent

Phase 15 is intended to transform ILYREN from:

```text
A collection of intelligent agents
```

into:

```text
A continuously operating creative studio control plane
```

while preserving:

```text
Intelligence
    ↓
Workforce
    ↓
Continuity
    ↓
Learning
    ↓
Human Decision
    ↓
Controlled Execution
    ↓
Real-World Feedback
    ↓
Improvement
```

The long-term objective is not to remove humans from the system.

It is to make human involvement **high-leverage**:

```text
Human
  ↓
sets direction / approves consequential actions
  ↓
ILYREN Creative Workforce
  ↓
researches / plans / creates / critiques / reviews /
coordinates / learns / prepares execution
  ↓
Human
  ↓
approves consequential side effects
  ↓
ILYREN
  ↓
executes through bounded integrations
  ↓
real-world outcomes
  ↓
learning
  ↓
better next cycle
```

That is the operational foundation required before ILYREN can credibly function as a persistent AI-native creative studio for real clients.

---

## 22. Governance Gate — Initial Status

```text
PHASE 15 STATUS:
PROPOSED

IMPLEMENTATION:
NOT YET AUTHORIZED

SECURITY REVIEW:
PENDING

REAL WORKFLOW:
PENDING

PRODUCTION READINESS:
NOT ASSESSED

GOVERNANCE VERDICT:
AWAITING USER APPROVAL
```

**Approval required before implementation begins.**
