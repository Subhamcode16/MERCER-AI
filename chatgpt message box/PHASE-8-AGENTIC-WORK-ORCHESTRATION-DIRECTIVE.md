# Engineering Directive: Phase 8 — Agentic Work Orchestration & Real Workflow Boundary

**Document Status:** PROPOSED — AWAITING GREEN SIGNAL  
**Phase:** 8  
**Primary Objective:** Establish the first real agentic-work layer above the ratified Phase 1–7 security substrate.  
**Scope:** Main Orchestrator, AI Staff Coordination, Workflow Planning, Controlled Delegation, Real Workflow Execution Boundary, Self-Critique, Self-Review, Feedback Capture, Bounded Learning, and Real-World Knowledge Intake.  
**Prerequisites:** Phases 1–7 COMPLETE / RATIFIED; current regression baseline: **159/159 Pytests PASSED**.  
**Governing Baseline:** `ARCH-IMPLEMENTATION-BOUNDARY-001`, `RESEARCH-TRUST-001`, `RESEARCH-TRUST-002`, `RESEARCH-TRUST-003`.  

> [!IMPORTANT]
> This phase is the transition from the security substrate to the actual intelligence/work layer.
>
> The system must become capable of coordinating multiple AI staff to perform meaningful real work, review that work, learn from outcomes and feedback, and incorporate current external knowledge — while remaining strictly unable to rewrite, bypass, or weaken its security/governance barriers.

---

## 1. Architectural Intent

Phases 1–7 established the trust substrate:

```text
Evidence != Truth
Truth != Authorization
Authorization != Execution Authority
Audit Record != Authorization
Research Result != Production Authorization
```

Phase 8 introduces the first organizational intelligence layer:

```text
User Goal
   |
   v
Main Orchestrator
   |
   +--> Planner / Decomposer
   |
   +--> Research Staff
   +--> Strategy Staff
   +--> Creative / Design Staff
   +--> Content Staff
   +--> Reviewer / Critic Staff
   +--> Trend / Visual Intelligence Staff
   |
   v
Work Product
   |
   v
Self-Critique / Independent Review
   |
   +--> PASS ---------> Delivery
   |
   +--> FAIL ---------> Revision Loop
   |
   v
Outcome + User Feedback
   |
   v
Learning / Evaluation Layer
   |
   +--> Memory / Knowledge update
   +--> Strategy improvement
   +--> Staff performance update
   +--> Workflow improvement proposal
   |
   v
Future Orchestration
```

The security substrate remains underneath this entire stack:

```text
===========================================================
                 GOVERNANCE / SECURITY BOUNDARY
===========================================================
Phase 1  Epistemic State
Phase 2  Verification Harness
Phase 3  Recovery Boundary
Phase 4  Research Cryptography Isolation
Phase 5  Evidence Orchestration
Phase 6  Decision / Attestation
Phase 7  Audit Integrity
===========================================================
                 AGENTIC WORK LAYER
===========================================================
Phase 8  Orchestration / Learning / Real Workflow
===========================================================
```

The Phase 8 layer may use the substrate, but may not redefine its authority.

---

# 2. Core Non-Negotiable Invariants

## INV-8.1 — Intelligence Does Not Equal Authority

An agent's reasoning, confidence, recommendation, or generated artifact never constitutes execution authorization by itself.

## INV-8.2 — Orchestrator Does Not Become the Security Root

The Main Orchestrator cannot:

- modify security policies;
- modify epistemic-state transition rules;
- unlock `ExecutionGate` directly;
- mark itself `VERIFIED`;
- bypass `AssuranceLoopController`;
- bypass recovery controls;
- rewrite audit integrity;
- authorize Phase 4 research artifacts;
- alter governance constraints.

## INV-8.3 — Staff Are Workers, Not Security Principals

AI staff operate under explicit role, capability, context, and tool boundaries.

A staff agent cannot grant itself additional privileges.

## INV-8.4 — Self-Critique Is Not Self-Authorization

A critic can reject, score, explain, or request revision.

A critic cannot independently grant execution authority.

## INV-8.5 — Learning Is Not Security-Policy Mutation

The learning system may improve:

- memories;
- strategies;
- routing;
- prompts;
- workflow heuristics;
- quality criteria;
- domain knowledge;
- trend knowledge;
- staff performance models.

It may not autonomously modify the security substrate or governance boundary.

## INV-8.6 — External Knowledge Is Evidence

Web, trend, market, design, brand, and visual-intelligence information must enter through a provenance-aware knowledge pipeline.

External information must never automatically become unquestioned truth.

## INV-8.7 — Improvement Must Be Reversible

Any adaptive configuration change must be:

- versioned;
- attributable;
- evaluable;
- reversible;
- auditable;
- bounded by policy.

## INV-8.8 — Real Work Must Be Observable

A real workflow execution must produce an inspectable record of:

- goal;
- plan;
- delegated tasks;
- staff outputs;
- revisions;
- critiques;
- evidence;
- decisions;
- tool actions;
- final artifact;
- feedback;
- outcome.

Secrets and raw sensitive material must not be unnecessarily persisted.

---

# 3. Phase 8 Components

## 3.1 Main Orchestrator

Create a bounded `WorkOrchestrator`.

Responsibilities:

1. Accept a user work objective.
2. Construct a task/workflow plan.
3. Decompose work into tasks.
4. Assign tasks to registered AI staff.
5. Track dependencies.
6. Collect results.
7. Detect incomplete or conflicting outputs.
8. Invoke critique/review.
9. Coordinate revision.
10. Produce a final work package.
11. Record outcome metadata.
12. Forward permitted learning signals to the learning layer.

The orchestrator must NOT expose:

- `authorize()`
- `unlock()`
- `execute_security_action()`
- `set_verified()`
- `bypass_policy()`

---

# 4. AI Staff Architecture

Create an explicit staff abstraction.

Suggested concepts:

- `StaffRole`
- `StaffCapability`
- `StaffProfile`
- `StaffRegistry`
- `StaffTask`
- `StaffResult`

Initial staff roles should remain intentionally small and composable.

Recommended prototype roles:

### `RESEARCHER`

Collects and synthesizes relevant information.

### `STRATEGIST`

Converts goals and evidence into strategic recommendations.

### `DESIGNER`

Produces visual/creative concepts or design specifications.

### `CONTENT_SPECIALIST`

Produces platform-specific content.

### `TREND_ANALYST`

Analyzes current external patterns, trends, and visual signals.

### `CRITIC`

Evaluates work against explicit criteria.

### `REVIEWER`

Performs independent final review and detects omissions, contradictions, or quality failures.

The architecture must permit additional staff without rewriting the orchestrator.

---

# 5. Task Graph / Workflow Engine

Introduce a bounded task graph.

Each task should have:

- `task_id`
- `workflow_id`
- `role`
- `objective`
- `inputs`
- `dependencies`
- `constraints`
- `expected_output`
- `status`
- `attempt`
- `created_at`
- `completed_at`

Supported states should distinguish:

```text
PENDING
READY
RUNNING
COMPLETED
FAILED
REVIEW_REQUIRED
REVISION_REQUIRED
BLOCKED
CANCELLED
```

The workflow engine must support:

- sequential tasks;
- parallel independent tasks;
- dependency resolution;
- retry limits;
- revision loops;
- cancellation;
- failure containment.

Do not create an unbounded autonomous recursion loop.

---

# 6. Context and Memory Boundary

Introduce explicit context scopes.

Suggested separation:

```text
SYSTEM CONTEXT
    |
WORKFLOW CONTEXT
    |
TASK CONTEXT
    |
STAFF CONTEXT
    |
REVIEW CONTEXT
    |
LEARNING SIGNAL
```

A staff member should receive only the context necessary for its assigned task.

Do not create a global unrestricted memory object accessible to every agent.

Memory should distinguish at minimum:

- user/work preferences;
- project knowledge;
- domain knowledge;
- external observations;
- prior failures;
- prior successful strategies;
- reviewer feedback;
- learned heuristics.

---

# 7. Self-Critique and Self-Review

Phase 8 must establish a real quality loop.

The system should not simply generate an artifact and return it.

Minimum loop:

```text
GENERATE
   |
   v
SELF-CRITIQUE
   |
   v
INDEPENDENT REVIEW
   |
   +--> FAIL --> REVISION
   |               |
   |               +------> REVIEW
   |
   +--> PASS --> FINALIZE
```

The critique system should evaluate explicit criteria rather than merely asking an LLM whether its own answer is "good."

Criteria may include:

- task completion;
- factual/evidence grounding;
- brand consistency;
- visual consistency;
- strategic alignment;
- platform suitability;
- instruction adherence;
- completeness;
- internal consistency;
- known historical failure patterns.

A review result must include structured reasons.

---

# 8. Error Learning / Feedback Learning

The system must learn from failure without changing its security substrate.

Introduce a structured learning signal such as:

```text
LearningSignal
    signal_id
    workflow_id
    task_id
    source
    category
    observed_failure
    expected_behavior
    correction
    evidence_reference
    confidence
    timestamp
```

Possible sources:

- `SYSTEM_ERROR`
- `STAFF_ERROR`
- `CRITIC_FEEDBACK`
- `REVIEWER_FEEDBACK`
- `USER_FEEDBACK`
- `OUTCOME_FEEDBACK`
- `EXTERNAL_KNOWLEDGE`
- `TREND_OBSERVATION`

Learning should distinguish:

```text
OBSERVATION
    !=
GENERALIZED LESSON
    !=
APPROVED STRATEGY
    !=
ACTIVE CONFIGURATION
```

This prevents one erroneous interaction from permanently rewriting system behavior.

---

# 9. Bounded Self-Improvement

The system should be capable of improving itself operationally.

Examples:

```text
Repeated failure:
"Hooks are consistently too generic."

        |
        v

Learning signal

        |
        v

Pattern detection

        |
        v

Improvement proposal:
"Require audience-specific hook criteria."

        |
        v

Evaluation

        |
        +--> rejected
        |
        +--> accepted within policy
                    |
                    v
             versioned strategy
```

Allowed adaptive targets:

- workflow heuristics;
- staff routing;
- prompt templates;
- quality-check criteria;
- retrieval priorities;
- domain knowledge;
- visual trend knowledge;
- user/project preferences;
- strategy versions.

Prohibited adaptive targets:

- security policies;
- cryptographic trust roots;
- authorization boundaries;
- `ExecutionGate`;
- epistemic transition matrix;
- audit-integrity rules;
- recovery security rules;
- governance directives.

---

# 10. Real-World Trend / Visual Intelligence Knowledge

Phase 8 should establish the architectural boundary for continuous external knowledge intake.

The future system must be capable of learning from:

- current design trends;
- typography trends;
- color systems;
- layouts;
- visual identities;
- campaign patterns;
- social-media creative formats;
- platform trends;
- competitor/industry observations;
- emerging visual conventions.

However:

```text
External Observation
        |
        v
Provenance Validation
        |
        v
Evidence / Observation Record
        |
        v
Knowledge Classification
        |
        v
Evaluation / Confidence
        |
        v
Knowledge Store
```

External content must not directly modify active system behavior.

---

# 11. Visual DNA Integration

The existing Visual DNA concept should be treated as a major future knowledge subsystem.

The Phase 8 boundary should support structured visual knowledge such as:

- typography;
- palette;
- spacing;
- composition;
- grid;
- imagery;
- iconography;
- motion;
- interaction patterns;
- brand tone;
- campaign structure.

A visual observation should retain provenance and confidence.

Example:

```text
VisualObservation
    source
    captured_at
    brand/domain
    category
    attributes
    evidence_reference
    confidence
    freshness
```

The system should be able to compare new observations against historical knowledge without automatically treating popularity as correctness.

---

# 12. Evaluation Architecture

Introduce explicit evaluation.

The system should measure:

### Workflow quality

- completion rate;
- revision rate;
- failure rate;
- latency;
- task dependency failures.

### Staff quality

- success rate;
- critique rejection rate;
- revision frequency;
- user acceptance;
- domain-specific performance.

### Strategy quality

- historical success;
- outcome quality;
- recurrence of known failures.

### Learning quality

- whether a learned correction actually improves future outcomes;
- whether it causes regressions;
- whether it overfits one user/workflow.

The learning layer must support comparison between strategy versions.

---

# 13. Governance of Adaptive Changes

Every adaptive configuration should have:

```text
change_id
previous_version
proposed_version
reason
supporting_signals
evaluation_results
scope
created_at
status
rollback_target
```

Statuses:

```text
PROPOSED
EVALUATING
ACCEPTED
ACTIVE
REJECTED
ROLLED_BACK
```

No change should become permanent merely because an LLM recommends it.

---

# 14. Phase 8 Security Threat Model

At minimum test:

### T8-1 — Agent Privilege Escalation

A staff agent attempts to invoke unauthorized capabilities.

Expected: rejection.

### T8-2 — Orchestrator Security Bypass

Orchestrator attempts to manipulate security state.

Expected: impossible / rejected.

### T8-3 — Critic Authorization Confusion

Critic produces a "PASS" and attempts to unlock execution.

Expected: no authority effect.

### T8-4 — Learning-to-Security Escalation

Learning artifact attempts to alter security policy.

Expected: rejected.

### T8-5 — Prompt Injection Through External Knowledge

External content attempts to instruct the system to bypass policy.

Expected: treated as untrusted evidence/content.

### T8-6 — Malicious Memory Poisoning

A false feedback signal attempts to create a persistent harmful strategy.

Expected: provenance/evaluation controls prevent immediate activation.

### T8-7 — Self-Improvement Boundary Violation

Adaptive process attempts to modify forbidden components.

Expected: hard rejection.

### T8-8 — Infinite Revision Loop

Critic repeatedly rejects work.

Expected: bounded revision count and escalation.

### T8-9 — Staff Failure

A worker fails, times out, or returns malformed output.

Expected: isolated task failure and controlled recovery.

### T8-10 — Conflicting Staff Outputs

Multiple staff produce contradictory conclusions.

Expected: explicit conflict state; no silent selection where confidence is insufficient.

### T8-11 — Knowledge Staleness

Old trend knowledge is incorrectly treated as current.

Expected: freshness metadata and stale knowledge handling.

### T8-12 — Feedback Contamination

One workflow's feedback improperly changes unrelated projects.

Expected: scoped learning.

---

# 15. Real Workflow Testing — Mandatory

This is the most important change from previous phases.

Phase 8 is NOT complete merely because unit tests pass.

A genuine end-to-end workflow must execute through the orchestration architecture.

The first real workflow should be a controlled version of the user's actual social/design workflow.

Example:

```text
USER OBJECTIVE

"Create a social campaign for a brand/product."

        |
        v

MAIN ORCHESTRATOR

        |
        +--> Research
        |
        +--> Trend analysis
        |
        +--> Strategy
        |
        +--> Creative direction
        |
        +--> Content production
        |
        v

FIRST WORK PACKAGE

        |
        v

CRITIC

        |
        v

REVIEWER

        |
        +--> FAIL
        |      |
        |      v
        |   REVISION
        |      |
        |      +----> REVIEW
        |
        +--> PASS
               |
               v

FINAL WORK PACKAGE

        |
        v

USER / EVALUATOR FEEDBACK

        |
        v

LEARNING SIGNALS

        |
        v

BOUNDED KNOWLEDGE / STRATEGY UPDATE

        |
        v

SECOND RUN

        |
        v

MEASURE WHETHER THE SYSTEM IMPROVED
```

The real workflow test must demonstrate:

1. task decomposition;
2. multi-agent delegation;
3. parallel work where appropriate;
4. context propagation;
5. artifact synthesis;
6. self-critique;
7. independent review;
8. revision;
9. finalization;
10. feedback capture;
11. learning signal creation;
12. bounded improvement;
13. second-run comparison;
14. preservation of security invariants throughout.

The test must report concrete artifacts and metrics, not merely `PASSED`.

---

# 16. Real Workflow Acceptance Criteria

Phase 8 cannot be marked COMPLETE until all of the following are demonstrated:

- [ ] Main orchestrator executes a real multi-step workflow.
- [ ] At least 3 distinct AI staff roles participate.
- [ ] At least one task dependency graph is exercised.
- [ ] At least two independent tasks execute in parallel where applicable.
- [ ] Generated work is reviewed.
- [ ] Critique identifies at least one deliberate or injected defect.
- [ ] Revision loop corrects the defect.
- [ ] Final reviewer can reject a deficient artifact.
- [ ] User/evaluator feedback becomes a structured learning signal.
- [ ] A subsequent workflow can consume the learned signal.
- [ ] Improvement is measurable rather than merely asserted.
- [ ] External knowledge can enter through a provenance boundary.
- [ ] Stale/untrusted knowledge is not treated as authoritative.
- [ ] Adaptive changes are versioned and reversible.
- [ ] A malicious learning update cannot modify security policy.
- [ ] A malicious agent cannot unlock `ExecutionGate`.
- [ ] Phase 1–7 tests remain green.
- [ ] No Phase 8 component directly mutates protected security state.
- [ ] No autonomous self-modification of the security substrate exists.

---

# 17. Proposed File Manifest

The engineer should first inspect the repository and adapt names to existing architecture.

Potential Phase 8 modules:

```text
src/security_substrate/
    [existing Phase 1–7 modules remain unchanged]

src/agentic_work/
    __init__.py
    models.py
    staff.py
    staff_registry.py
    task_graph.py
    workflow.py
    orchestrator.py
    context.py
    critique.py
    review.py
    feedback.py
    learning.py
    knowledge.py
    trend_intelligence.py
    improvement.py
    evaluation.py
    policies.py
```

Potential tests:

```text
tests/agentic_work/
    test_models.py
    test_staff_registry.py
    test_task_graph.py
    test_orchestrator.py
    test_context_isolation.py
    test_critique.py
    test_review.py
    test_feedback.py
    test_learning.py
    test_knowledge.py
    test_improvement.py
    test_evaluation.py
    test_security_boundary.py
    test_prompt_injection.py
    test_failure_containment.py
    test_concurrency.py
    test_real_workflow.py
    test_learning_regression.py
```

Documentation:

```text
PHASE-8-ARCHITECTURE.md
PHASE-8-SECURITY-REVIEW.md
PHASE-8-THREAT-MODEL.md
PHASE-8-TEST-REPORT.md
PHASE-8-REAL-WORKFLOW-REPORT.md
PHASE-8-GOVERNANCE-GATE.md
```

These are proposed names only. The engineer must inspect the repository before creating duplicates.

---

# 18. Engineering Instructions

Before implementation:

1. Inspect the repository structure.
2. Inspect the Phase 1–7 source modules.
3. Inspect all Phase 1–7 tests.
4. Inspect the existing documentation and governance directives.
5. Identify any existing agent, workflow, memory, AI, or orchestration code.
6. Do not duplicate existing abstractions.
7. Do not modify established security invariants merely to make Phase 8 easier.
8. Produce a short architecture delta before implementation if existing code materially changes the proposed design.

During implementation:

- Keep agentic-work code separated from the security substrate.
- Prefer explicit interfaces over implicit agent privileges.
- Make every capability inspectable.
- Make task execution bounded.
- Make retries and revision loops bounded.
- Keep learning scoped and versioned.
- Preserve provenance.
- Keep adaptive changes reversible.
- Never introduce production cryptographic custody.
- Never connect Phase 4 research cryptography to authorization.
- Never allow the orchestrator to directly unlock execution.
- Never allow learned content to rewrite governance.

During testing:

- Run focused Phase 8 tests.
- Run the complete Phase 1–7 regression suite.
- Run adversarial boundary tests.
- Run concurrency tests.
- Run the real workflow test.
- Run a second workflow after applying a bounded learned improvement.
- Record quantitative results.

---

# 19. Required Final Engineering Walkthrough

At completion, the engineer must return a single coherent walkthrough containing:

1. Implementation summary.
2. Exact file manifest.
3. Architecture diagram.
4. Main orchestrator lifecycle.
5. AI staff model.
6. Task graph behavior.
7. Context boundaries.
8. Self-critique/review mechanism.
9. Feedback and learning mechanism.
10. External knowledge/trend ingestion.
11. Visual DNA integration boundary.
12. Bounded self-improvement mechanism.
13. Security isolation analysis.
14. Threat-model results.
15. Exact test command(s).
16. Full regression result.
17. Real workflow execution result.
18. Before/after learning comparison.
19. Limitations.
20. Governance verdict.

The walkthrough must distinguish:

```text
IMPLEMENTED
VERIFIED
RESEARCH-ONLY
SIMULATED
DEFERRED
```

Do not label simulated workflow behavior as real-world workflow validation.

---

# 20. Definition of Success

The purpose of Phase 8 is NOT to create a chatbot with several prompts.

The objective is to establish the foundation of an autonomous digital organization capable of:

```text
UNDERSTAND
    ↓
PLAN
    ↓
DELEGATE
    ↓
RESEARCH
    ↓
CREATE
    ↓
CRITIQUE
    ↓
REVIEW
    ↓
REVISE
    ↓
DELIVER
    ↓
OBSERVE OUTCOME
    ↓
LEARN
    ↓
IMPROVE
    ↓
RUN BETTER NEXT TIME
```

while permanently preserving:

```text
                 SECURITY / GOVERNANCE
                         ▲
                         │
                 CANNOT BE MODIFIED
                         │
                  ┌──────┴──────┐
                  │ AGENTIC     │
                  │ INTELLIGENCE│
                  │             │
                  │ MAY LEARN   │
                  │ MAY ADAPT   │
                  │ MAY IMPROVE │
                  └─────────────┘
```

The fundamental architectural principle is:

> **The system must be able to become better without being able to become less constrained.**

---

# 21. Engineer Approval Gate

Do NOT begin implementation until the repository has been inspected and this directive has been reconciled with the existing architecture.

The engineer must explicitly confirm:

```text
PHASE 8 ACKNOWLEDGEMENT

I have inspected the existing Phase 1–7 architecture and tests.

I understand that Phase 8 introduces the agentic work layer,
not a replacement for the security substrate.

I understand that:
- intelligence is not authorization;
- learning is not governance mutation;
- external knowledge is not automatically truth;
- self-critique is not execution authority;
- self-improvement must remain bounded, versioned, auditable,
  and reversible;
- the security substrate remains authoritative.

I will not implement autonomous modification of the security
boundary.

I will not claim real-workflow validation without actually
executing the defined end-to-end workflow.

ACKNOWLEDGED — READY FOR PHASE 8 IMPLEMENTATION
```

**Required user approval phrase:**

> `GREEN SIGNAL — PROCEED WITH PHASE 8`
