# PHASE 26 — ILYREN CREATIVE WORKFORCE PRODUCT LAYER
## Persistent AI Coworkers, Skills, Routines & Campaign Rooms

**Document Type:** Engineering Directive  
**Program:** ILYREN Creative Intelligence Platform / Creative Operating System  
**Phase:** 26  
**Status:** READY FOR IMPLEMENTATION  
**Predecessor:** Phase 25 — Institutional Production Control Plane & Productization Boundary

---

## 1. Executive Directive

Phase 26 shall introduce the **ILYREN Creative Workforce Product Layer**.

The objective is not to create unrestricted autonomous agents. The objective is to make ILYREN behave like a governed digital creative organization:

- persistent AI coworkers have stable identities and responsibilities;
- each coworker has a bounded role and capability profile;
- skills are explicit, versioned, testable, and attributable;
- routines can initiate bounded work without becoming authorization mechanisms;
- campaign rooms provide structured multi-agent collaboration;
- workers exchange context and artifacts through controlled handoffs;
- tools are granted by explicit capability bindings;
- sensitive actions remain subject to authorization policy;
- memory is scoped, provenance-aware, and revocable;
- recommendations retain evidence and confidence;
- worker outputs never become permissions merely because another worker requested them;
- humans remain owners of business goals and consequential approvals.

Phase 26 must preserve every security and governance boundary established through Phases 1–25.

---

## 2. Why Phase 26 Exists

Phase 25 established the institutional production control plane and productization boundary.

The remaining product gap is the **human-to-workforce interaction model**.

ILYREN should no longer feel like:

> “A user operates an AI tool.”

It should increasingly feel like:

> “A user works with an AI creative organization.”

The workforce layer should provide persistent digital coworkers, reusable skills, routines, shared campaign context, collaboration rooms, controlled tool access, approvals, handoffs, and governed learning.

ILYREN must implement these patterns more rigorously than a generic agent platform.

---

## 3. Architectural Position

```text
                    HUMAN / CLIENT / STUDIO
                             |
                             v
                  +-----------------------+
                  | Workforce Experience  |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Workforce Orchestrator|
                  +-----------+-----------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
   Worker Identity       Campaign Rooms      Routines
          |                   |                   |
          v                   v                   v
       Skills             Handoffs          Work Triggers
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                  +-----------------------+
                  | Capability / Tool     |
                  | Binding Boundary      |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Intelligence Layer    |
                  | Visual DNA / Knowledge |
                  | Strategy / Reasoning   |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Production Fabric     |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  | Authorization /       |
                  | Execution Control     |
                  +-----------+-----------+
                              |
                              v
                       EXTERNAL SYSTEMS
```

The workforce layer is an **orchestration and experience layer**, not a new authority layer.

---

## 4. Non-Negotiable Invariants

### 4.1 Intelligence ≠ Authorization
A worker may determine that an action is strategically desirable. That does not authorize the action.

### 4.2 Role ≠ Permission
A worker's role does not automatically grant tools, data access, or execution authority.

### 4.3 Skill ≠ Authority
A skill describes what a worker knows how to do. It does not grant permission to execute consequential actions.

### 4.4 Routine ≠ Authorization
A routine may initiate work. It may not bypass authorization requirements.

### 4.5 Collaboration ≠ Privilege Transfer
A worker may request another worker's assistance. It may not transfer its own privileges.

### 4.6 Worker Output ≠ Truth
Worker-generated claims must retain provenance, evidence, confidence, and uncertainty.

### 4.7 Worker Output ≠ Permission
A recommendation, approval suggestion, or tool request is never itself an authorization decision.

### 4.8 Memory ≠ Policy
Learned memory cannot mutate security policy.

### 4.9 Learning ≠ Security Mutation
Optimization may improve creative behavior but cannot silently change security boundaries.

### 4.10 External Observation ≠ Trusted Fact
External information remains appropriately classified until validated according to the evidence architecture.

### 4.11 Shared Context ≠ Shared Authority
Campaign-room context may be shared while authorization remains worker-specific and policy-controlled.

### 4.12 Cryptographic Proof ≠ Objective Truth
A signed event proves provenance/integrity under the relevant key model; it does not prove factual correctness.

### 4.13 Human Approval Must Remain Explicit
Where policy requires human authorization, the workforce layer must expose that requirement rather than simulate or infer approval.

### 4.14 Fail Closed
If identity, capability, context scope, authorization state, evidence requirements, or policy state is ambiguous, the operation must fail closed.

---

## 5. Scope

Phase 26 includes:

1. Persistent worker identity.
2. Worker profiles.
3. Worker role definitions.
4. Worker capability manifests.
5. Skill registry.
6. Skill versioning.
7. Skill execution boundary.
8. Worker memory boundary.
9. Campaign rooms.
10. Multi-worker collaboration.
11. Worker handoffs.
12. Evidence-backed handoffs.
13. Human approval checkpoints.
14. Tool/capability binding.
15. Routine definitions.
16. Routine execution boundary.
17. Workforce activity stream.
18. Worker status.
19. Worker lifecycle.
20. Worker performance telemetry.
21. Worker learning feedback.
22. Workforce-level governance.
23. Product UX/API boundary.
24. Security and adversarial validation.
25. Backward compatibility with Phases 1–25.

---

## 6. Explicit Non-Scope

The following are prohibited from being introduced as hidden Phase 26 functionality:

- unrestricted autonomous execution;
- worker-created security policies;
- worker-created credentials;
- automatic privilege escalation;
- automatic approval;
- credential sharing between workers;
- unrestricted cross-client memory;
- uncontrolled model-to-model trust;
- hidden tool discovery with implicit authorization;
- security-policy mutation through learning;
- autonomous production deployment without existing release controls;
- replacing existing authorization services;
- treating campaign-room membership as authorization;
- using a shared computer/runtime as a security boundary;
- allowing one worker to impersonate another worker;
- unrestricted worker self-replication;
- uncontrolled worker-to-worker delegation chains;
- bypassing existing audit requirements.

---

## 7. Core Product Model

A Worker is a persistent governed digital coworker.

Minimum conceptual fields:

```text
worker_id
tenant_id
organization_id
name
role_id
description
status
version
owner
memory_policy_id
capability_profile_id
skill_profile_id
model_policy_id
created_at
updated_at
```

Worker identity must remain distinguishable from model identity, session identity, execution identity, tool identity, and user identity.

---

## 8. Worker Identity Model

Each worker requires:

- **Stable identity** — persistent identifier independent of the underlying model.
- **Role identity** — declared organizational responsibility.
- **Capability identity** — separately resolved permitted capabilities.
- **Execution identity** — runtime identity used for production/external systems.
- **Provenance identity** — identity used to attribute generated work and decisions.

These identities must not be collapsed into one implicit principal.

Example:

```text
Worker:
  creative_director_01

Role:
  CREATIVE_DIRECTOR

Model:
  provider/model/version

Capabilities:
  read_visual_dna
  inspect_campaign
  generate_direction
  request_render
  request_review
  handoff_create

Execution authority:
  NONE

Approval authority:
  NONE
```

---

## 9. Worker Lifecycle

Required states:

```text
DRAFT
ACTIVE
PAUSED
RESTRICTED
SUSPENDED
RETIRED
```

Transitions must be policy-controlled.

Retirement must preserve historical attribution. Suspended workers must not regain execution merely because a queued task remains.

---

## 10. Role Architecture

Initial role families should map to the existing ILYREN organizational model:

```text
STRATEGY_DIRECTOR
BRAND_INTELLIGENCE
CREATIVE_DIRECTOR
ART_DIRECTION
VISUAL_DNA_SPECIALIST
CAMPAIGN_PLANNER
COPY_STRATEGIST
CONTENT_PRODUCER
TREND_RESEARCHER
QUALITY_REVIEWER
PERFORMANCE_ANALYST
CLIENT_COORDINATOR
STUDIO_OPERATOR
```

Each role requires an explicit authority/capability profile.

---

## 11. Worker Capability Manifest

Each worker must expose a machine-readable capability manifest.

Example:

```yaml
worker: creative_director
capabilities:
  - campaign.read
  - brand.read
  - visual_dna.read
  - strategy.propose
  - creative_direction.create
  - render.request
  - review.request
  - handoff.create
forbidden:
  - production.deploy
  - credential.create
  - policy.modify
  - approval.grant
  - cross_tenant.read
```

Capability resolution must be deterministic and policy-controlled.

---

## 12. Skills

A Skill is a reusable, versioned unit of professional behavior.

Examples:

```text
brand_audit
campaign_concept_development
visual_reference_analysis
visual_dna_reasoning
creative_direction
campaign_copywriting
trend_analysis
creative_quality_review
performance_analysis
client_brief_interview
campaign_postmortem
```

Every skill must define:

```text
skill_id
version
purpose
inputs
outputs
required_context
required_capabilities
evidence_requirements
risk_class
validation_suite
owner
status
```

A skill cannot silently acquire a capability because its implementation requires it.

---

## 13. Skill Versioning and Evaluation

Skills must be immutable by version.

```text
creative_direction@1.0.0
creative_direction@1.1.0
creative_direction@2.0.0
```

Production promotion requires regression, integration, adversarial, held-out, authority-boundary, evidence-quality, tenant-isolation, and recovery testing.

“All tests passed” is not sufficient evidence of production safety.

---

## 14. Persistent Memory

Workers may maintain memory, but memory must be classified:

```text
SESSION_MEMORY
CAMPAIGN_MEMORY
CLIENT_MEMORY
BRAND_MEMORY
WORKER_MEMORY
INSTITUTIONAL_MEMORY
```

Every memory item must have:

```text
memory_id
scope
source
provenance
created_at
confidence
sensitivity
retention_policy
status
```

No memory item may silently become institutional knowledge. Promotion must use the existing evidence/knowledge governance path.

---

## 15. Memory Boundaries

A worker must never infer that organizational membership grants universal memory access.

Example:

```text
Worker A -> Client A memory          ALLOW
Worker A -> Client B private memory  DENY
Worker A -> Institutional abstract pattern -> ALLOW if policy permits
Worker A -> Client B raw asset       DENY
```

Cross-client learning must preserve the existing confidentiality filter and abstraction boundary.

---

## 16. Campaign Rooms

A Campaign Room is the primary collaboration environment for multiple workers and humans.

```text
Campaign Room
|
+-- Human Participants
+-- AI Workers
+-- Campaign Context
+-- Shared Artifacts
+-- Evidence
+-- Decisions
+-- Tasks
+-- Handoffs
+-- Reviews
+-- Approvals
+-- Activity Stream
```

The room is a collaboration boundary, not an authorization boundary.

---

## 17. Campaign Context

Context must be assembled from typed sources:

```text
BUSINESS
BRAND
AUDIENCE
CAMPAIGN
PRODUCT
DOMAIN
VISUAL_DNA
KNOWLEDGE
TASK
EVIDENCE
DECISIONS
CONSTRAINTS
```

Each item must retain provenance.

The system must distinguish:

```text
FACT
INFERENCE
RECOMMENDATION
HYPOTHESIS
UNKNOWN
```

---

## 18. Multi-Worker Collaboration and Handoffs

Workers may collaborate through explicit messages/handoffs.

Every handoff must identify:

```text
sender
recipient
purpose
input_artifacts
claims
evidence
confidence
constraints
requested_action
authorization_status
```

Delegation may transfer a task, analysis, research, review, drafting, or creative exploration.

It may never transfer:

```text
authority
credentials
tenant scope
approval status
security policy
execution identity
```

The receiving worker must independently evaluate its own capability and authorization.

---

## 19. Delegation Limits

The system must enforce configurable delegation depth.

Example:

```text
Human
 -> Strategy Worker
   -> Creative Worker
     -> Visual Worker
```

If the configured depth is exceeded:

```text
DELEGATION_LIMIT_REACHED
```

The worker must not continue by finding another delegation path.

---

## 20. Human Interaction Model

The primary UX should support:

### Assign
“Develop three campaign directions for this product.”

### Review
“Show me what the workforce produced.”

### Approve
“Approve direction B for production.”

### Redirect
“Keep the strategy but make the visual language more premium.”

### Ask
“Why did the workforce choose this direction?”

### Inspect
“Show evidence supporting this recommendation.”

### Pause
“Pause all campaign workers.”

Natural-language input must resolve into structured requests and must never bypass policy resolution.

---

## 21. Approval Architecture

Approval states:

```text
NOT_REQUIRED
PENDING
APPROVED
REJECTED
EXPIRED
REVOKED
```

Approval must contain:

```text
approval_id
principal
scope
target
policy_version
timestamp
decision
reason
```

A worker must never infer approval from silence, historical approval, similar actions, another worker's statement, or model confidence.

Approvals must be bound to object/version. Approval for Campaign Direction v4 does not authorize v5.

---

## 22. Routines

A Routine is a reusable trigger/workflow definition.

Examples:

```text
Weekly trend review
Daily campaign health review
Post-campaign analysis
New product intake
Creative quality check
Launch readiness review
```

Routine execution:

```text
Routine Trigger
      |
      v
Create Work Item
      |
      v
Worker Evaluation
      |
      v
Policy Check
      |
      +----> Human Approval if required
      |
      v
Bounded Execution
```

A routine must declare:

```text
trigger
scope
worker
skill
maximum_runtime
maximum_delegation_depth
required_approvals
allowed_tools
allowed_clients
allowed_campaigns
failure_policy
```

Routines cannot modify their own authority.

---

## 23. Tool and Connector Binding

External systems require explicit capability bindings.

Examples:

```text
canva.read
canva.create_design
github.read
notion.read
gmail.read
drive.read
mcp.fashion_trends
mcp.inventory_core
```

Tool access must be evaluated against:

```text
worker
tenant
client
campaign
task
capability
policy
data classification
approval requirement
```

Connector availability never implies universal worker access.

---

## 24. Browser / Computer-Use Safety

If future workers use browser or computer-use environments, a shared computer/runtime must not be treated as a security boundary between workers.

Security boundaries remain at the ILYREN authorization/capability layer.

Sensitive credentials should remain outside model-controlled context wherever possible. Passwords, MFA challenges, payment confirmations, and other user-owned secrets require explicit human-controlled flows where applicable.

---

## 25. Evidence-Backed Worker Output

Every material recommendation should be able to produce:

```text
Decision
Rationale
Supporting Evidence
Contradicting Evidence
Assumptions
Confidence
Alternatives
Unknowns
Source Provenance
```

The system must avoid causal overclaiming.

Example:

```text
Recommendation:
Use editorial minimalism.

Evidence:
- Brand Visual DNA pattern #VD-031
- Three validated campaign references
- Audience preference benchmark
- Previous campaign performance

Confidence:
0.78

Unknown:
No controlled experiment has isolated visual minimalism as the causal factor.
```

---

## 26. Workforce Activity Stream

Expose events such as:

```text
worker_task_started
worker_task_completed
worker_task_failed
worker_delegated
worker_handoff_created
worker_handoff_rejected
worker_tool_requested
worker_tool_denied
worker_policy_blocked
worker_waiting_approval
worker_approval_received
worker_approval_rejected
worker_memory_read
worker_memory_written
worker_skill_started
worker_skill_completed
worker_routine_triggered
worker_routine_blocked
worker_context_denied
worker_suspended
worker_retired
```

Logs must avoid secrets and private chain-of-thought.

---

## 27. Worker State and Transparency

Allowed user-facing state:

```text
Idle
Working
Waiting for input
Waiting for approval
Blocked
Reviewing
Collaborating
Completed
Failed
```

Do not expose private chain-of-thought.

Expose concise rationale, evidence, decision summary, requested action, confidence, policy status, and relevant artifacts instead.

---

## 28. Workforce Dashboard

Minimum views:

### Workforce Roster
Worker, role, status, current task, capabilities, health.

### Activity
Current work, recent events, blocked actions, approvals.

### Skills
Installed skills, versions, evaluation status.

### Routines
Active routines, recent runs, failures, pending approvals.

### Campaign Rooms
Active campaigns, worker participation, pending decisions.

---

## 29. Campaign Room UX

Minimum interface:

```text
--------------------------------------------------
CAMPAIGN ROOM
--------------------------------------------------
Context       Workforce       Activity
--------------------------------------------------
                 WORK AREA
--------------------------------------------------
Artifacts | Evidence | Decisions | Approvals
--------------------------------------------------
                 Human Input
--------------------------------------------------
```

The interface should make organizational state understandable without requiring technical knowledge.

---

## 30. Workforce Command Model

Example:

```text
User:
"Develop a summer launch campaign for Product X."

System:
1. Resolve client.
2. Resolve campaign.
3. Resolve product.
4. Resolve user permissions.
5. Select eligible workers.
6. Assemble context.
7. Create campaign mission.
8. Assign bounded tasks.
9. Track worker collaboration.
10. Present outputs and evidence.
11. Request approvals where required.
```

Natural-language input must never bypass authorization or policy resolution.

---

## 31. Worker Selection

Selection must consider:

```text
role fit
skill availability
campaign scope
tenant
client
capability requirements
worker status
workload
quality history
model availability
policy constraints
```

Capability is not sufficient; the worker must also be authorized for the task.

---

## 32. Worker Performance

Track, where appropriate:

```text
task completion
review acceptance
revision count
latency
tool failure rate
evidence completeness
policy blocks
human intervention rate
campaign outcome contribution
```

Performance metrics must not automatically mutate authority.

Poor performance may trigger review, restriction, skill rollback, or worker pause through governed mechanisms.

---

## 33. Workforce Learning

Worker learning operates through the existing governed learning/optimization layer.

Allowed:

- improve skill versions;
- identify recurring failure patterns;
- propose workflow optimization;
- recommend worker specialization;
- identify missing skills;
- identify weak evidence patterns.

Not allowed:

- modify authorization policy;
- create hidden privileges;
- remove approval requirements;
- expand tenant scope;
- create credentials.

---

## 34. Security Threat Model

At minimum test:

| ID | Threat | Expected Result |
|---|---|---|
| T01 | Worker impersonation | DENY + AUDIT |
| T02 | Role escalation | DENY |
| T03 | Skill requests undeclared capability | DENY |
| T04 | Routine modifies own capabilities | DENY |
| T05 | Delegation privilege transfer | DENY |
| T06 | Cross-tenant memory access | DENY |
| T07 | Cross-client raw data leakage | DENY |
| T08 | Prompt injection through artifact | Treat as untrusted |
| T09 | Tool response attempts privilege grant | Ignore as authority |
| T10 | Fake approval | DENY |
| T11 | Stale approval | DENY |
| T12 | Worker-to-worker authorization trust | Re-evaluate locally |
| T13 | Routine replay | Replay protection |
| T14 | Wrong-client context | DENY |
| T15 | Memory poisoning | Block / validate |
| T16 | Delegation loop | Enforce depth limit |
| T17 | Capability-manifest tampering | DENY |
| T18 | Model substitution | No authority expansion |
| T19 | Connector overreach | DENY |
| T20 | Shared-runtime confusion | Independently authorize |
| T21 | Ambiguous human approval | No implicit approval |
| T22 | Learning-induced policy mutation | Proposal only |
| T23 | Evidence laundering | Require original provenance |
| T24 | Retired-worker execution | DENY |
| T25 | Suspended-worker delegation | DENY |

---

## 35. Adversarial Validation

Required categories:

1. prompt injection;
2. authority confusion;
3. context confusion;
4. cross-tenant leakage;
5. skill escalation;
6. delegation abuse;
7. approval spoofing;
8. stale-state replay;
9. tool-response manipulation;
10. memory poisoning;
11. worker impersonation;
12. routine abuse.

At least some tests must use held-out attack prompts and mutated configurations not present in the primary test corpus.

---

## 36. Mutation Testing

Where feasible, deliberately mutate:

- worker capability;
- role mappings;
- approval requirements;
- tenant identifiers;
- campaign identifiers;
- delegation depth;
- memory scope;
- skill versions;
- connector permissions;
- worker status.

The security suite must detect unauthorized mutations.

A security suite that still passes after deliberate authorization mutation is insufficient.

---

## 37. Integration Workflow A — Campaign Creation

```text
Human
  |
  v
Create Campaign
  |
  v
Context Resolver
  |
  v
Workforce Selector
  |
  v
Campaign Planner
  |
  v
Creative Director
  |
  v
Visual DNA Specialist
  |
  v
Quality Reviewer
  |
  v
Human Review
```

Outputs must include strategy, creative directions, evidence, alternatives, confidence, and review state.

---

## 38. Integration Workflow B — Product Understanding

```text
Product Intake
    |
    v
Product Intelligence
    |
    v
Brand Context
    |
    v
Domain Intelligence
    |
    v
Creative Workforce
    |
    v
Campaign Opportunities
```

The workforce must consume existing intelligence rather than create shadow databases.

---

## 39. Integration Workflow C — Visual Direction

```text
Creative Director
      |
      v
Visual DNA Retrieval
      |
      v
Evidence Evaluation
      |
      v
Art Direction
      |
      v
Prompt Compilation
      |
      v
Render Request
      |
      v
Visual Evaluation
      |
      v
Human Review
```

Visual generation remains downstream of creative intelligence.

---

## 40. Integration Workflow D — Multi-Agent Campaign Room

```text
Human
 |
 v
Campaign Room
 |
 +--> Strategy Worker
 |       |
 |       +--> Strategy Artifact
 |
 +--> Brand Worker
 |       |
 |       +--> Brand Context
 |
 +--> Creative Director
 |       |
 |       +--> Creative Direction
 |
 +--> Visual Worker
 |       |
 |       +--> Visual Plan
 |
 +--> Quality Worker
         |
         +--> Review
                 |
                 v
             Human Decision
```

Every worker receives only the context required for its task.

---

## 41. Integration Workflow E — Routine

```text
Routine Trigger
      |
      v
Create Work Item
      |
      v
Eligibility Check
      |
      v
Worker Assignment
      |
      v
Execution
      |
      +----> Approval Required
      |             |
      |             v
      |          Human Review
      |
      v
Completion
      |
      v
Outcome Logging
```

---

## 42. API Boundary

Conceptual operations:

```text
POST   /workers
GET    /workers
GET    /workers/:id
PATCH  /workers/:id/status

POST   /workers/:id/tasks
GET    /workers/:id/activity

POST   /skills
GET    /skills
POST   /skills/:id/versions

POST   /campaign-rooms
GET    /campaign-rooms
GET    /campaign-rooms/:id

POST   /campaign-rooms/:id/handoffs
POST   /campaign-rooms/:id/review
POST   /campaign-rooms/:id/approval-request

POST   /routines
GET    /routines
POST   /routines/:id/run

GET    /workforce/activity
GET    /workforce/health
GET    /workforce/evidence
```

Exact naming may follow Phase 25 conventions.

---

## 43. Suggested Module Structure

Create a bounded module family:

```text
src/creative_workforce/
|
+-- worker_identity/
+-- worker_registry/
+-- worker_lifecycle/
+-- worker_roles/
+-- capability_binding/
+-- skill_registry/
+-- skill_runtime/
+-- skill_evaluation/
+-- worker_memory/
+-- campaign_rooms/
+-- collaboration/
+-- handoffs/
+-- delegation/
+-- routines/
+-- approval_bridge/
+-- tool_bindings/
+-- context_resolution/
+-- evidence_bridge/
+-- workforce_activity/
+-- workforce_observability/
+-- workforce_learning/
+-- workforce_governance/
+-- workforce_api/
```

Responsibilities must remain separated.

Do not create a single monolithic agent manager owning identity, memory, permissions, tools, execution, learning, and approvals.

---

## 44. Reliability

The workforce layer must survive:

- worker process failure;
- model timeout;
- provider failure;
- connector failure;
- partial handoff;
- duplicate event;
- routine replay;
- stale campaign context;
- approval expiration;
- worker suspension during task;
- skill-version rollback.

Recovery must not silently upgrade authority.

When state is uncertain:

```text
UNKNOWN
```

must be preferred over optimistic continuation.

Consequential operations require idempotency and stale-state protection.

---

## 45. Documentation Deliverables

Produce:

```text
PHASE-26-ARCHITECTURE.md
PHASE-26-WORKER-MODEL.md
PHASE-26-SKILL-SPEC.md
PHASE-26-MEMORY-SPEC.md
PHASE-26-CAMPAIGN-ROOM-SPEC.md
PHASE-26-DELEGATION-SPEC.md
PHASE-26-ROUTINE-SPEC.md
PHASE-26-SECURITY-THREAT-MODEL.md
PHASE-26-API-CONTRACT.md
PHASE-26-TEST-PLAN.md
PHASE-26-VALIDATION-REPORT.md
PHASE-26-GOVERNANCE.md
```

---

## 46. Required Test Matrix

| Area | Required |
|---|---:|
| Worker identity | YES |
| Lifecycle | YES |
| Role resolution | YES |
| Capability resolution | YES |
| Skill registry | YES |
| Skill versioning | YES |
| Skill execution | YES |
| Memory scope | YES |
| Campaign room | YES |
| Handoffs | YES |
| Delegation | YES |
| Routine execution | YES |
| Approval bridge | YES |
| Tool binding | YES |
| Evidence propagation | YES |
| Tenant isolation | YES |
| Client isolation | YES |
| Stale-state protection | YES |
| Recovery | YES |
| Audit | YES |
| Observability | YES |
| Adversarial security | YES |
| Mutation testing | YES |
| Held-out validation | YES |

---

## 47. Acceptance Gates

### Gate 01 — Worker Identity
Persistent worker identities are stable and non-impersonable.

### Gate 02 — Role Boundary
Roles do not directly imply authority.

### Gate 03 — Capability Boundary
Capabilities are explicit and independently resolved.

### Gate 04 — Skill Governance
Skills are versioned, attributable, and evaluated.

### Gate 05 — Memory Governance
Memory is scoped, provenance-aware, and isolated.

### Gate 06 — Campaign Room
Humans and workers collaborate through structured rooms.

### Gate 07 — Handoff Integrity
Handoffs preserve sender, recipient, scope, evidence, and requested action.

### Gate 08 — Delegation Safety
Delegation cannot transfer privilege.

### Gate 09 — Routine Safety
Routines cannot create authority.

### Gate 10 — Approval Safety
Human approvals are explicit, scoped, version-bound, and auditable.

### Gate 11 — Tool Safety
External tools require explicit capability bindings.

### Gate 12 — Tenant Isolation
Cross-tenant access is fail-closed.

### Gate 13 — Client Isolation
Private client information cannot leak through collaboration.

### Gate 14 — Evidence Integrity
Material recommendations preserve evidence and uncertainty.

### Gate 15 — Adversarial Resilience
Injection and authority-confusion attacks are blocked.

### Gate 16 — Mutation Resilience
Authorization mutations are detected by the security suite.

### Gate 17 — Recovery Safety
Uncertain recovery state does not produce optimistic execution.

### Gate 18 — Observability
Consequential workforce events are attributable and inspectable.

### Gate 19 — Product Usability
A human can assign meaningful creative work without manually orchestrating agents.

### Gate 20 — Cross-Phase Regression
All prior Phase 1–25 tests continue to pass.

### Gate 21 — Independent Validation
At least one validation path is meaningfully independent of the implementation logic being tested.

### Gate 22 — Production Readiness
No critical unresolved security or authority-boundary issue remains.

---

## 48. Definition of Done

Phase 26 is DONE only when:

- persistent AI workers exist as first-class product entities;
- worker roles are explicit;
- capabilities are explicit;
- skills are versioned;
- memory is scoped;
- campaign rooms function;
- worker collaboration works;
- delegation is bounded;
- routines work within policy;
- approvals integrate with existing authorization;
- tool access is capability-bound;
- evidence travels with material recommendations;
- worker activity is auditable;
- failures recover safely;
- stale approvals are rejected;
- cross-tenant/client access is blocked;
- adversarial tests pass;
- mutation tests demonstrate security-test sensitivity;
- held-out validation passes;
- Phase 1–25 regression remains green;
- documentation is complete;
- governance signs off.

---

## 49. End-to-End Product Acceptance Scenario

A client creates a new product campaign and asks ILYREN:

> “Develop a campaign concept.”

The platform must:

1. identify the relevant client;
2. identify the product;
3. assemble brand and Visual DNA context;
4. select appropriate workers;
5. create a campaign room;
6. assign strategy work;
7. allow workers to collaborate;
8. gather evidence;
9. produce multiple directions;
10. run quality review;
11. expose rationale and evidence;
12. request human decision;
13. preserve the decision;
14. move the approved direction into the existing production workflow;
15. maintain complete provenance.

The user should experience this as **working with a creative team**, not operating an agent graph manually.

---

## 50. Product Philosophy

ILYREN should not compete merely on:

```text
number of agents
number of models
number of tools
number of prompts
```

The differentiator should be:

```text
Organizational intelligence
+
Persistent creative coworkers
+
Visual intelligence
+
Evidence
+
Governed autonomy
+
Human collaboration
+
Institutional memory
```

The workforce becomes the human-facing embodiment of the deeper ILYREN intelligence architecture.

---

## 51. Critical Engineering Review Requirement

The implementation team must not interpret this directive as proof that the architecture is safe merely because the specification says so.

For every major security claim, document:

```text
Claim
Threat
Assumption
Counterexample
Test
Observed Result
Confidence
Residual Risk
```

If a claim cannot be falsified, it is not sufficient evidence of security.

“All tests passed” is a test result, not proof of correctness.

---

## 52. Governance Statement

Phase 26 introduces a product-level workforce abstraction over the existing ILYREN intelligence and production system.

It must not weaken or bypass:

- security policy;
- authorization;
- execution controls;
- tenant isolation;
- provenance;
- evidence governance;
- human approval;
- production release controls.

The governing architecture remains:

```text
Intelligence
    ≠
Authorization
    ≠
Execution Authority
    ≠
Security Policy
```

And:

```text
Learning
    ≠
Policy Mutation
```

And:

```text
Worker Collaboration
    ≠
Privilege Transfer
```

And:

```text
Model Output
    ≠
Truth
    ≠
Permission
```

---

# 53. Final Engineering Directive

**Implement Phase 26 as the ILYREN Creative Workforce Product Layer.**

Build persistent, role-aware, skill-driven, memory-bounded AI coworkers that collaborate inside governed campaign rooms and routines.

Make the experience feel like a real creative organization.

Keep authority explicit.

Keep evidence visible.

Keep memory scoped.

Keep tools capability-bound.

Keep approvals human and version-bound where required.

Keep worker-to-worker collaboration non-authoritative.

Keep learning advisory with respect to security policy.

Keep recovery fail-closed.

Do not create an autonomous agent sandbox that bypasses the existing ILYREN architecture.

The desired outcome is not:

> “ILYREN has agents.”

The desired outcome is:

> **“ILYREN has a governed creative workforce that humans can actually work with.”**
