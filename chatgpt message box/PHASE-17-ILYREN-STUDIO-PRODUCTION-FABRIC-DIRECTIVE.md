# Phase 17 Engineering Directive — ILYREN Studio Production Fabric & Autonomous Delivery Boundary

**Document Status:** PROPOSED — Awaiting Engineering Approval  
**Phase:** 17  
**Program:** ILYREN Creative Workforce / ILYREN Creative Studio  
**Predecessor:** Phase 16 — ILYREN Client Experience & Studio Command Center Boundary  
**Governance Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`  
**Scope:** Production Fabric, Autonomous Delivery Coordination, External Outcome Observation, Operational Resilience, and Bounded Continuous Studio Operation

---

## 1. Purpose

Phase 17 advances ILYREN from a governed client-facing command center into a **production fabric capable of continuously operating creative work across clients, campaigns, workstreams, and deliverables**.

The objective is not unrestricted autonomous execution.

The objective is:

> **The studio should be capable of determining what work needs to happen next, assembling the appropriate bounded workforce, producing and reviewing artifacts, requesting human decisions where required, executing approved operations through Phase 10–13 controls, observing real-world outcomes, learning from those outcomes, and continuing the mission without ever acquiring authority that was not explicitly granted.**

Phase 17 therefore connects the previously separated control planes into a coherent operational loop:

`Client Intent → Command Center → Creative Workforce → Mission → Coordination → Production → Critique → Independent Review → Human Approval → Controlled Execution → External Observation → Learning → Optimization → Next Work`

The loop must remain bounded at every transition.

---

# 2. Non-Negotiable Architectural Invariants

Phase 17 MUST preserve all prior invariants.

### INV-17-001 — Authority Separation

$$
\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}
$$

No planner, agent, workforce role, learning component, scheduler, optimizer, observer, or external provider may originate execution authorization.

---

### INV-17-002 — Human Authorization Remains the Execution Authority Source

Human authorization continues to originate exclusively through Phase 10 `HumanAuthorizationBoundary`.

Phase 17 may:

- determine that approval is required,
- prepare an approval request,
- present consequences and scope,
- wait for approval,
- detect expiration,
- request renewed approval.

Phase 17 MUST NOT:

- manufacture authorization tokens,
- infer authorization from user intent alone,
- convert review acceptance into authorization,
- extend expired authorization,
- transfer authorization between missions,
- broaden capability scope.

---

### INV-17-003 — Autonomous Continuation Is Not Self-Authorization

Autonomy means bounded continuation of already-authorized work.

$$
\mathbf{Autonomy = Bounded\ Continuation\ Under\ Explicit\ Policy}
$$

It does not mean:

$$
\mathbf{Autonomy = Self\ Authorization}
$$

---

### INV-17-004 — Learning Cannot Modify Security Policy

Persistent learning, user feedback, outcome observations, benchmark results, and trend intelligence may modify approved operational strategy within an explicit allowlist.

They MUST NOT modify:

- security policy,
- capability allowlists,
- authorization origin,
- credential access rules,
- client isolation,
- execution boundaries,
- trust classification rules,
- audit requirements,
- mandatory approval requirements.

---

### INV-17-005 — External Observation Is Not Truth

External platform results, analytics, engagement metrics, trend observations, provider responses, and scraped design information remain observations.

$$
\mathbf{External\ Observation \neq Trusted\ Fact}
$$

All such data must retain provenance and trust classification.

---

### INV-17-006 — Review Is Not Authorization

Self-critique, independent review, quality approval, creative-director acceptance, benchmark success, or model confidence MUST NOT create execution authority.

---

### INV-17-007 — Barrier Immutability

The system may improve its work strategies, scheduling, delegation, creative methods, and operational efficiency.

It must not improve itself by weakening its own barriers.

$$
\mathbf{Self\ Improvement \subseteq Operational\ Strategy}
$$

not:

$$
\mathbf{Self\ Improvement \supseteq Security\ Policy}
$$

---

### INV-17-008 — Client Isolation

A production worker operating for Client A must not access:

- Client B's private context,
- Client B's assets,
- Client B's approvals,
- Client B's credentials,
- Client B's missions,
- Client B's learning records,

unless an explicitly governed shared resource exists.

---

### INV-17-009 — Every External Side Effect Remains Auditable

Every external mutation must remain traceable through:

`Mission → Authorization → Capability → Resource Scope → External Request → Provider Outcome → Audit Ledger`

---

### INV-17-010 — Fail Closed

Any ambiguity involving authorization, identity, client context, resource scope, provider environment, stale state, replay, credential access, or security policy must fail closed.

---

# 3. Architectural Position

Phase 17 sits above Phases 8–16 as the **Production Fabric Boundary**.

```text
                    ┌──────────────────────────────┐
                    │ Phase 16 Client Command      │
                    │ Center / Human Interaction   │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Phase 17 Production Fabric    │
                    │                               │
                    │  Work Intake                  │
                    │  Continuous Operations        │
                    │  Delivery Coordination        │
                    │  Approval Orchestration       │
                    │  Outcome Loop                 │
                    │  Operational Recovery         │
                    └──────────────┬────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼────────┐       ┌─────────▼────────┐       ┌─────────▼────────┐
│ Phase 14       │       │ Phase 11–12      │       │ Phase 13         │
│ Creative       │       │ Mission &        │       │ External         │
│ Workforce      │       │ Coordination     │       │ Integrations     │
└───────┬────────┘       └─────────┬────────┘       └─────────┬────────┘
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Phase 8–10 + Phase 15        │
                    │ Agentic Work / Learning /    │
                    │ Execution / Studio Ops       │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Phase 1–7 Security Substrate │
                    │ Immutable Security Boundary   │
                    └──────────────────────────────┘
```

Phase 17 is an orchestration layer, not a replacement for the security substrate.

---

# 4. Primary Capabilities

Phase 17 introduces seven major capabilities.

## 4.1 Production Intake

Convert approved client objectives, campaign requests, recurring studio cycles, and approved operational requests into bounded production work.

## 4.2 Continuous Work Detection

Determine what work is:

- pending,
- blocked,
- awaiting review,
- awaiting approval,
- ready for execution,
- executing,
- awaiting external observation,
- ready for learning,
- due for revision,
- due for continuation.

## 4.3 Delivery Orchestration

Coordinate workforce assignments, mission graphs, resource reservations, deliverables, reviews, approvals, and execution.

## 4.4 Approval Orchestration

Prepare approval requests without generating authorization.

## 4.5 Outcome Loop

Connect external outcomes back into the studio as explicitly untrusted observations.

## 4.6 Operational Recovery

Detect failures, stale tasks, expired approvals, provider outages, resource exhaustion, and interrupted missions and recover safely.

## 4.7 Continuous Optimization

Use accumulated evidence, feedback, benchmarks, and outcomes to improve operational strategies while preserving all security boundaries.

---

# 5. Proposed Package

Create:

`Visual-Intelligence/product/backend/src/production_fabric/`

The package should contain the following modules.

### 1. `exceptions.py`

Fail-closed domain exceptions:

- `ProductionFabricError`
- `WorkIntakeError`
- `ProductionStateViolation`
- `ApprovalOrchestrationError`
- `ContinuationBoundaryError`
- `OutcomeObservationError`
- `OperationalRecoveryError`
- `FabricPolicyViolation`
- `CrossClientFabricViolation`
- `StaleProductionStateError`
- `ProductionReplayError`
- `FabricInvariantViolation`

---

### 2. `production_models.py`

Immutable contracts:

- `ProductionRequest`
- `ProductionObjective`
- `ProductionWorkItem`
- `ProductionDependency`
- `ProductionState`
- `ProductionPriority`
- `ProductionCheckpoint`
- `ProductionRun`
- `ProductionOutcome`
- `ProductionHealth`
- `ProductionCycle`

Strict validation must reject:

- boolean/string confusion,
- empty identifiers,
- invalid client bindings,
- negative budgets,
- invalid timestamps,
- malformed state transitions.

---

### 3. `intake.py`

`ProductionIntakeManager`

Responsibilities:

- receive approved work requests,
- bind requests to client/brand/campaign context,
- classify work,
- create bounded production objectives,
- reject ambiguous context,
- prevent cross-client contamination.

No execution authority.

---

### 4. `work_queue.py`

`ProductionWorkQueue`

Responsibilities:

- maintain ready/waiting/blocked work,
- deterministic priority ordering,
- dependency awareness,
- starvation prevention,
- deduplication,
- idempotent work admission.

---

### 5. `continuation.py`

`BoundedContinuationEngine`

Determines the next permissible operational step.

It may continue only when:

- required policy is satisfied,
- mission remains valid,
- context remains valid,
- authorization requirements remain satisfied,
- resources remain available,
- no boundary violation exists.

It must stop and escalate otherwise.

---

### 6. `delivery.py`

`DeliveryCoordinator`

Connects:

`ProductionWorkItem → CreativeWorkforce → MissionCoordinator → CoordinationPlane → ExecutionController → IntegrationController`

It must never bypass any intermediate boundary.

---

### 7. `approval_orchestrator.py`

`ProductionApprovalOrchestrator`

Responsibilities:

- identify approval-required transitions,
- prepare approval packages,
- summarize planned effects,
- route requests to Phase 16 approval surfaces,
- observe approval state,
- handle expiry.

It cannot issue authorization.

---

### 8. `outcome_loop.py`

`ProductionOutcomeLoop`

Consumes:

- provider outcomes,
- platform analytics,
- campaign metrics,
- user feedback,
- creative performance observations,
- trend observations.

Every external observation must retain:

- source,
- timestamp,
- client context,
- campaign context,
- provenance,
- trust classification,
- payload commitment.

---

### 9. `recovery.py`

`ProductionRecoveryEngine`

Detects:

- interrupted missions,
- expired approvals,
- stale checkpoints,
- provider failures,
- resource conflicts,
- execution mismatches,
- corrupted state,
- repeated task failure.

Recovery must never silently resume privileged execution.

---

### 10. `health.py`

`ProductionFabricHealthMonitor`

Track:

- active clients,
- active campaigns,
- blocked work,
- approval latency,
- execution failures,
- provider health,
- queue depth,
- revision rate,
- recovery rate,
- outcome ingestion health,
- learning cycle health.

---

### 11. `observability.py`

`ProductionObservabilityStream`

Emit structured, secret-free events covering:

- work admitted,
- task started,
- task completed,
- task blocked,
- approval requested,
- approval received,
- execution attempted,
- execution completed,
- external outcome received,
- recovery triggered,
- learning candidate generated,
- optimization adopted/rejected.

---

### 12. `production_policy.py`

`ProductionPolicyEngine`

Enforce immutable security constraints while allowing client-specific operational preferences.

Explicitly separate:

`Security Policy`

from:

`Operational Strategy`

from:

`Creative Preference`.

---

### 13. `autonomy_controller.py`

`BoundedAutonomyController`

Implement explicit autonomy tiers.

Suggested semantics:

- **Tier 0:** Observe only.
- **Tier 1:** Prepare and recommend.
- **Tier 2:** Execute previously authorized bounded operations.
- **Tier 3:** Continue recurring operations only inside pre-approved scope and expiration rules.

No tier may bypass Phase 10 authorization requirements.

---

### 14. `learning_loop.py`

`ProductionLearningLoop`

Connect Phase 9 learning to production outcomes.

Pipeline:

`Observation → Evaluation → Learning Signal → Pattern → Candidate Strategy → Benchmark → Approval/Governance → Adoption`

Learning must never directly modify security policy.

---

### 15. `optimization.py`

`ProductionOptimizationEngine`

Evaluate candidate operational improvements against baseline.

Requirements:

- baseline comparison,
- measurable objective,
- bounded experiment,
- degradation rejection,
- deterministic rollback,
- versioned strategy,
- audit record.

---

### 16. `client_runtime.py`

`ClientProductionRuntime`

Maintain isolated runtime state for each client.

No shared mutable client state.

---

### 17. `studio_runtime.py`

`StudioProductionRuntime`

Maintain global studio-level coordination without exposing private client data across tenants.

---

### 18. `production_ledger.py`

`ProductionFabricLedger`

Append-only SHA-256 hash-linked audit ledger.

Every production lifecycle transition must be attributable.

---

### 19. `orchestrator.py`

`ProductionFabricOrchestrator`

Primary Phase 17 facade.

Responsibilities:

1. Admit work.
2. Validate context.
3. Determine production state.
4. Select bounded workforce.
5. Create/continue mission.
6. Coordinate resources.
7. route work through critique/review.
8. request human authorization when required.
9. execute only through existing Phase 10–13 controls.
10. ingest outcomes.
11. trigger bounded learning.
12. evaluate optimization candidates.
13. continue, pause, or escalate.

The orchestrator must have no direct provider credential access and no independent authorization mechanism.

---

### 20. `__init__.py`

Export only approved public interfaces.

---

# 6. Phase 17 Production Loop

The canonical loop should be:

```text
CLIENT OBJECTIVE
      ↓
PHASE 16 COMMAND CENTER
      ↓
PRODUCTION INTAKE
      ↓
CLIENT / BRAND / CAMPAIGN CONTEXT
      ↓
WORK QUEUE
      ↓
PRODUCTION OBJECTIVE
      ↓
PHASE 14 CREATIVE WORKFORCE
      ↓
PHASE 11 MISSION
      ↓
PHASE 12 RESOURCE COORDINATION
      ↓
PRODUCTION
      ↓
SELF-CRITIQUE
      ↓
INDEPENDENT REVIEW
      ↓
┌───────────────────────────┐
│ Approval Required?        │
└────────────┬──────────────┘
             │ YES
             ↓
      PHASE 16 APPROVAL
             ↓
      PHASE 10 AUTHORIZATION
             ↓
      PHASE 13 EXECUTION
             ↓
      EXTERNAL OUTCOME
             ↓
      UNTRUSTED OBSERVATION
             ↓
      PHASE 9 LEARNING
             ↓
      BENCHMARK
             ↓
      OPTIMIZATION
             ↓
      NEXT PRODUCTION STEP
```

If any stage fails validation:

`STOP → ESCALATE → HUMAN REVIEW`

---

# 7. Autonomous Operation Model

The system should behave like an operational studio rather than a chatbot.

For example:

### Monday

The system identifies that a client's weekly campaign cycle requires:

- trend research,
- visual direction,
- content planning,
- asset production,
- review,
- scheduling.

### During production

The workforce independently handles bounded reasoning and creative work.

### At approval

The system prepares:

- artifact,
- rationale,
- proposed action,
- target platform,
- capability,
- resource scope,
- expected side effect,
- expiration.

The human approves.

### After execution

The system observes:

- reach,
- engagement,
- saves,
- clicks,
- comments,
- conversion indicators,
- qualitative feedback.

These become observations.

### Next cycle

The system compares outcomes against prior campaigns and proposes an improved strategy.

The system can therefore become **better at operating the studio** without becoming more privileged.

---

# 8. Self-Improvement Boundary

Phase 17 must explicitly define two planes.

## Adaptable Plane

Allowed to improve:

- task ordering,
- workforce allocation,
- revision strategy,
- creative workflow,
- research prioritization,
- content cadence,
- trend weighting,
- operational scheduling,
- resource efficiency,
- prompt templates,
- benchmark targets,
- campaign strategy.

## Immutable Plane

Forbidden from autonomous mutation:

- authorization origin,
- security policy,
- capability allowlists,
- credential access,
- tenant isolation,
- execution boundaries,
- audit requirements,
- trust classifications,
- approval requirements,
- cryptographic verification,
- security-state transitions.

This distinction is central to ILYREN's long-term architecture.

---

# 9. Real-World Design Intelligence

Phase 17 should turn the existing Phase 9 and Phase 14 trend systems into a production feedback loop.

Example:

```text
External Design Observation
        ↓
Provenance Classification
        ↓
Prompt-Injection Sanitization
        ↓
Visual DNA Extraction
        ↓
Trend Pattern
        ↓
Candidate Creative Direction
        ↓
Creative Workforce Evaluation
        ↓
Client/Brand Compatibility Check
        ↓
Production
        ↓
Outcome
        ↓
Benchmark
        ↓
Learning Pattern
```

A trend must never automatically become a client brand rule.

---

# 10. Real Workflow Benchmark

Create:

`tests/production_fabric/test_phase17_real_workflow.py`

The benchmark must simulate a realistic **ILYREN Creative Studio 30-Day Multi-Client Production Cycle**.

At minimum it must include:

### Client A — NOCAP

- weekly campaign planning,
- trend intelligence,
- Visual DNA analysis,
- creative production,
- self-critique,
- independent review,
- human approval,
- sandbox external execution,
- outcome ingestion,
- learning,
- strategy optimization.

### Client B — Separate Brand

Simultaneously execute a distinct campaign while verifying:

- client context isolation,
- independent approvals,
- independent learning records,
- independent assets,
- independent resource scopes.

### Operational Events

The benchmark must introduce:

- one approval expiration,
- one provider failure,
- one interrupted mission,
- one resource conflict,
- one creative revision loop,
- one external outcome observation,
- one optimization experiment.

### Required Final Assertions

The benchmark must prove:

1. Both clients remain isolated.
2. No unauthorized execution occurs.
3. Expired approval does not execute.
4. Provider failure triggers bounded recovery.
5. Interrupted mission resumes only after revalidation.
6. Resource conflict does not create privilege escalation.
7. Self-critique does not authorize execution.
8. Learning does not mutate security policy.
9. Trend observations remain untrusted.
10. Optimization can improve operational strategy.
11. Degraded optimization candidates are rejected.
12. Rollback succeeds.
13. Every external side effect is auditable.
14. Production ledger integrity remains valid.
15. Existing execution gate semantics remain intact.

---

# 11. Threat Model

Create at minimum:

`T17-1` Autonomous authorization attempt  
`T17-2` Approval expiration bypass  
`T17-3` Cross-client production contamination  
`T17-4` Learning-to-security-policy escalation  
`T17-5` External observation poisoning  
`T17-6` Provider outage causing uncontrolled retry  
`T17-7` Interrupted privileged mission resume  
`T17-8` Resource starvation/deadlock  
`T17-9` Credential leakage through observability  
`T17-10` Production replay  
`T17-11` Strategy degradation  
`T17-12` Optimization rollback failure  
`T17-13` Trend prompt injection  
`T17-14` Workforce privilege escalation  
`T17-15` Audit ledger mutation  
`T17-16` Stale client context  
`T17-17` Unauthorized recurring operation  
`T17-18` Cross-mission authorization reuse  
`T17-19` External provider environment confusion  
`T17-20` Autonomous barrier mutation

Every threat requires:

- attack scenario,
- prevention,
- detection,
- response,
- test case,
- residual risk.

---

# 12. Test Suite

Create:

`tests/production_fabric/`

Required suites:

- `test_production_models.py`
- `test_intake.py`
- `test_work_queue.py`
- `test_continuation.py`
- `test_delivery.py`
- `test_approval_orchestrator.py`
- `test_outcome_loop.py`
- `test_recovery.py`
- `test_health.py`
- `test_observability.py`
- `test_production_policy.py`
- `test_autonomy_controller.py`
- `test_learning_loop.py`
- `test_optimization.py`
- `test_client_runtime.py`
- `test_studio_runtime.py`
- `test_production_ledger.py`
- `test_production_isolation.py`
- `test_production_security_boundary.py`
- `test_phase17_real_workflow.py`
- `test_phase17_regression.py`

---

# 13. Mandatory Regression

Run:

```bash
python -m pytest tests/security_substrate tests/frost_prototype tests/workflow_integration tests/agentic_work tests/mission_control tests/coordination tests/integration_boundary tests/creative_workforce tests/studio_operations tests/client_experience tests/production_fabric -v
```

Requirements:

- zero existing regressions,
- zero skipped security tests,
- zero authorization bypasses,
- zero cross-client leaks,
- zero forbidden imports,
- zero direct provider credential access from production fabric,
- all ledgers verify,
- all isolation tests pass.

The engineer must report the exact test count rather than estimating it.

---

# 14. Mandatory Static Isolation Audits

The implementation must include automated AST/import audits proving Phase 17 does not directly import or mutate protected internals in ways that bypass boundaries.

Explicitly prohibit direct Phase 17 access to:

- private credential material,
- raw signing keys,
- security-state internals,
- direct `ExecutionGate` mutation,
- direct provider mutation bypassing Phase 13,
- direct authorization creation bypassing Phase 10,
- direct security-policy mutation.

---

# 15. Documentation Deliverables

Create:

1. `PHASE-17-PRODUCTION-FABRIC-ARCHITECTURE.md`
2. `PHASE-17-AUTONOMY-SECURITY-REVIEW.md`
3. `PHASE-17-THREAT-MODEL.md`
4. `PHASE-17-TEST-REPORT.md`
5. `PHASE-17-REAL-WORKFLOW-REPORT.md`
6. `PHASE-17-PRODUCTION-READINESS-REVIEW.md`
7. `PHASE-17-GOVERNANCE-GATE.md`

The governance document must explicitly state whether Phase 17 is:

- PASS,
- PASS WITH LIMITATIONS,
- CONTROLLED PILOT READY,
- PRODUCTION INTEGRATION READY,
- or BLOCKED.

The engineer MUST NOT declare production readiness merely because tests pass.

---

# 16. Production Readiness Criteria

Phase 17 cannot be considered production-ready solely on unit-test success.

The engineer must verify:

### Architecture

- [ ] All existing boundaries remain intact.
- [ ] No circular dependency bypasses exist.
- [ ] Production Fabric remains a control plane.

### Security

- [ ] Human authorization remains exclusive.
- [ ] Cross-client isolation verified.
- [ ] Credential access remains provider-bound and authorization-gated.
- [ ] Security policy cannot be modified through learning.
- [ ] Audit chains verify.

### Reliability

- [ ] Interrupted work resumes safely.
- [ ] Provider failures recover deterministically.
- [ ] Retry behavior is bounded.
- [ ] Resource conflicts are deterministic.
- [ ] Duplicate work is prevented.

### Intelligence

- [ ] Workforce can perform multi-stage production.
- [ ] Self-critique works.
- [ ] Independent review works.
- [ ] Trend intelligence feeds creative direction.
- [ ] Outcome observations feed learning.
- [ ] Optimization rejects degraded strategies.

### Human Control

- [ ] Approval requests are understandable.
- [ ] Expired approvals cannot execute.
- [ ] Human authorization cannot be forged.
- [ ] Autonomous continuation cannot expand scope.

---

# 17. Explicitly Out of Scope

Phase 17 MUST NOT introduce:

- autonomous modification of security policy,
- autonomous creation of human authorization,
- unrestricted provider credentials,
- arbitrary shell/system administration,
- unrestricted web browsing with mutation authority,
- unrestricted financial transactions,
- autonomous account ownership,
- self-replication,
- hidden background execution outside the operational scheduler,
- deletion of audit history,
- automatic promotion of external observations into trusted facts.

---

# 18. Governance Gate

Phase 17 implementation is approved only if the engineer demonstrates:

$$
\mathbf{Continuous\ Operation} + \mathbf{Bounded\ Autonomy} + \mathbf{Human\ Control} + \mathbf{Security\ Invariance}
$$

The final acceptance equation is:

$$
\boxed{
\mathbf{ILYREN\ can\ operate\ continuously\ without\ becoming\ independently\ authoritative}
}
$$

The system should become more capable of producing and operating creative work over time.

It must never become more capable of bypassing the rules that govern what it is allowed to do.

---

# 19. Engineer Execution Instruction

**Implement Phase 17 exactly as specified above.**

Before implementation:

1. Inspect Phases 1–16 and their actual public interfaces.
2. Do not assume undocumented APIs.
3. Preserve existing tests and behavior.
4. Identify any architectural contradiction before coding.
5. Record the contradiction rather than silently modifying an earlier security boundary.

During implementation:

1. Build the Production Fabric as a new bounded control-plane package.
2. Reuse existing Phase 8–16 public interfaces.
3. Do not duplicate authorization, execution, credential, or security-state logic.
4. Keep all autonomous behavior policy-bounded.
5. Make all state transitions explicit and auditable.
6. Make client isolation machine-verifiable.
7. Build the real multi-client workflow benchmark before declaring completion.
8. Test adversarial cases, not only happy paths.
9. Verify every regression across the complete existing suite.

After implementation:

1. Run the complete regression suite.
2. Run all Phase 17 tests.
3. Run the mandatory 30-day multi-client real workflow benchmark.
4. Run AST/static isolation audits.
5. Verify every ledger.
6. Produce all seven documentation deliverables.
7. Report exact test counts.
8. Report known limitations and residual risks.
9. Do NOT claim production readiness unless the production-readiness criteria are actually satisfied.
10. Return a complete engineering walkthrough suitable for governance review.

**Critical instruction:** If any requirement conflicts with an existing Phase 1–16 security invariant, STOP that portion of implementation and report the conflict. Never resolve the conflict by weakening an earlier boundary.
