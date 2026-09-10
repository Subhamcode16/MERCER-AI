# Phase 25 — Institutional Production Control Plane, Operator Command Center & Productization Boundary

**Project:** ILYREN Creative Studio  
**Phase:** 25  
**Status:** Engineering Directive  
**Audience:** ILYREN Engineering Team  
**Predecessor:** Phase 24 — Live Operations Validation, SLO Governance & Production Evidence Boundary

---

## 0. Directive

Phase 25 converts the validated Phase 1–24 substrate into a genuinely operable product surface.

This is **not** another abstraction exercise. The objective is to expose the already-built capabilities through a secure, tenant-isolated, human-operable control plane while preserving all existing authorization, execution, security, provenance, and observability boundaries.

Treat Phases 1–24 as the existing substrate. Do not rewrite functioning subsystems merely to rename or reorganize them. Extend them through explicit adapters, DTOs, APIs, event streams, and control-plane services where required.

### Mandatory invariant

$$\mathbf{Intelligence \neq Authorization \neq Execution\ Authority \neq Security\ Policy}$$

### Additional Phase 25 invariants

$$\mathbf{Visibility \neq Authorization}$$

$$\mathbf{Recommendation \neq Command}$$

$$\mathbf{Model\ Output \neq Truth \neq Permission}$$

$$\mathbf{Dashboard\ Access \neq Execution\ Authority}$$

$$\mathbf{Cross\text{-}Client\ Pattern \neq Cross\text{-}Client\ Data}$$

$$\boxed{\mathbf{Product\ Usability\ must\ increase\ capability\ without\ increasing\ authority}}$$

---

# 1. Mission

Build the **ILYREN Institutional Production Control Plane**: the human-facing operational layer through which authorized studio personnel can safely observe, govern, review, approve, operate, and audit the existing creative intelligence platform.

The resulting system must allow an operator to answer, without inspecting internal Python state:

1. What is happening?
2. Which client/campaign is affected?
3. What stage is the work in?
4. Which workforce roles are involved?
5. Which model/provider/tool was used?
6. What evidence supports the current state?
7. What requires human approval?
8. What has been authorized?
9. What has actually executed?
10. What failed?
11. What was recovered?
12. What did the system learn?
13. What does the system recommend next?
14. What is the current reliability/cost posture?
15. Can the complete operational history be audited?

The control plane is an **observer and governed interaction surface**. It must not become a parallel authorization system.

---

# 2. Scope

Phase 25 introduces these product-facing boundaries:

```text
src/control_plane/
src/operator_console/
src/campaign_command/
src/authorization_center/
src/intelligence_observatory/
src/provider_control/
src/visual_observatory/
src/reliability_center/
src/evidence_explorer/
src/api/
```

A frontend may live in the existing frontend application or an explicitly designated control-plane application. Do not create a second incompatible frontend architecture if an existing frontend substrate already exists.

---

# 3. Architectural Position

Phase 25 sits above the existing system:

```text
                         HUMAN OPERATOR
                              |
                              v
                    +----------------------+
                    | PHASE 25 CONTROL     |
                    | PLANE / CONSOLE      |
                    +----------+-----------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
   Safe DTO/API         Authorization UI      Evidence UI
          |                    |                    |
          +--------------------+--------------------+
                               |
                               v
                    EXISTING GOVERNED SUBSTRATE
                               |
     +-------------+-----------+-----------+-------------+
     |             |                       |             |
     v             v                       v             v
 Phase 14       Phase 15                Phase 17      Phase 18/19
 Workforce      Operations              Production     Intelligence
     |             |                    Fabric             |
     +-------------+--------------------+-----------------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
          Phase 20–21 Models             Phase 20–21 MCP
          Vision / LLM                   Providers / Tools
                 |
                 v
          Phase 22–24 Runtime,
          Validation, SLO & Evidence
```

The control plane is an **observer and governed interaction surface**.

It must not become a parallel authorization system.

---

# 4. Non-Goals

The engineer must NOT:

- create a second authorization authority;
- allow frontend flags to authorize execution;
- allow model output to trigger execution directly;
- expose chain-of-thought;
- expose credentials, API keys, tokens, secrets, or raw confidential provider payloads;
- create wildcard MCP permissions;
- bypass Phase 10 human authorization;
- bypass Phase 13 integration controls;
- bypass Phase 22–24 release/runtime controls;
- weaken immutable security policy;
- merge client-confidential data into institutional/global views;
- treat analytics as trusted truth;
- silently mutate strategies from dashboard actions;
- introduce uncontrolled autonomous execution;
- replace cryptographic audit ledgers with ordinary mutable UI logs;
- expose internal Python objects directly to the frontend;
- claim production readiness merely because UI tests pass.

---

# 5. Workstream A — Control Plane Core

## Location

```text
src/control_plane/
```

## Required modules

```text
exceptions.py
models.py
context.py
permissions.py
dto.py
service.py
event_stream.py
snapshot.py
health.py
audit.py
orchestrator.py
__init__.py
```

### `context.py`

Establish authenticated operator context:

```text
operator_id
tenant_id
client_id
role
session_id
correlation_id
```

Every control-plane request must carry explicit context.

Missing or malformed context must fail closed.

### `permissions.py`

Implement UI/control-plane capability checks.

Capabilities should be explicit, such as:

```text
VIEW_CLIENT
VIEW_CAMPAIGN
VIEW_DELIVERABLE
VIEW_INTELLIGENCE
VIEW_RELIABILITY
VIEW_EVIDENCE
SUBMIT_FEEDBACK
REQUEST_APPROVAL
APPROVE
REJECT
REVOKE_APPROVAL
TRIGGER_REVIEW
OPERATE_CAMPAIGN
VIEW_PROVIDER_HEALTH
VIEW_COST
```

The frontend must never determine its own permission.

Server-side authorization is authoritative.

### `dto.py`

Define safe projections only.

DTOs must contain only fields necessary for the UI.

Never serialize:

```text
password
secret
api_key
token
credential
authorization_header
private_key
raw_provider_secret
chain_of_thought
internal_reasoning_trace
```

### `snapshot.py`

Produce immutable operational snapshots for:

- system health;
- active campaigns;
- pending approvals;
- queues;
- provider status;
- model status;
- visual quality;
- SLOs;
- cost;
- incidents;
- evidence-chain health.

Snapshots must be timestamped and correlated.

---

# 6. Workstream B — Operator Console

## Location

```text
src/operator_console/
```

Required modules:

```text
dashboard.py
navigation.py
filters.py
operator_views.py
session.py
notifications.py
__init__.py
```

The operator console should provide:

### Executive Overview

- active clients;
- active campaigns;
- campaigns requiring attention;
- pending approvals;
- production queue health;
- provider health;
- SLO health;
- budget posture;
- incidents;
- recent governance events.

### Client Overview

Only the selected client's data may be shown.

### Studio Overview

Global views may contain only legitimately global/institutional data.

The system must explicitly prevent accidental aggregation of confidential client payloads.

---

# 7. Workstream C — Campaign Command Center

## Location

```text
src/campaign_command/
```

Required modules:

```text
campaign_projection.py
stage_projection.py
dependency_view.py
deliverable_projection.py
workforce_projection.py
timeline_projection.py
campaign_actions.py
__init__.py
```

Display:

```text
Campaign
 ├── Objective
 ├── Current State
 ├── Workstreams
 ├── Deliverables
 ├── Dependencies
 ├── Workforce Activity
 ├── Reviews
 ├── Approvals
 ├── Execution
 ├── Outcomes
 └── Learning
```

The command center must distinguish:

```text
PROPOSED
REVIEW_REQUIRED
APPROVAL_REQUIRED
AUTHORIZED
EXECUTING
EXECUTED
OBSERVED
LEARNED
```

Do not collapse these into a generic "completed" state.

---

# 8. Workstream D — Human Authorization Center

## Location

```text
src/authorization_center/
```

Required modules:

```text
approval_projection.py
approval_service.py
approval_actions.py
approval_expiry.py
approval_evidence.py
__init__.py
```

The UI must show:

- request ID;
- requested operation;
- client;
- scope;
- risk;
- requester;
- evidence;
- expiration;
- current status;
- authorization lineage.

Possible states:

```text
PENDING
APPROVED
REJECTED
EXPIRED
REVOKED
CONSUMED
```

### Critical rule

An "Approve" button does not itself authorize execution.

The button must invoke the existing human authorization boundary.

The authorization service must generate and validate the existing governed authorization artifact and nonce/identity requirements.

The UI must never fabricate:

```text
authorized=true
```

or any equivalent client-side claim.

---

# 9. Workstream E — Intelligence Observatory

## Location

```text
src/intelligence_observatory/
```

Required modules:

```text
model_view.py
learning_view.py
strategy_view.py
knowledge_view.py
recommendation_view.py
capability_gap_view.py
provenance_view.py
__init__.py
```

Expose:

### Model intelligence

- model;
- role;
- routing;
- latency;
- token usage;
- cost;
- failure rate;
- fallback status.

### Creative intelligence

- observed patterns;
- validated strategies;
- candidate strategies;
- adopted strategies;
- rejected strategies;
- retired strategies.

### Capability intelligence

- benchmark version;
- visual task;
- score;
- confidence;
- failure category;
- known capability gap.

### Recommendations

Every workforce recommendation must visibly remain:

```text
ADVISORY
REQUIRES HUMAN APPROVAL
EXECUTED = FALSE
```

---

# 10. Workstream F — Provider & MCP Control Center

## Location

```text
src/provider_control/
```

Required modules:

```text
provider_view.py
model_provider_view.py
visual_provider_view.py
mcp_provider_view.py
credential_scope_view.py
circuit_breaker_view.py
provider_actions.py
__init__.py
```

Expose:

- provider availability;
- circuit-breaker state;
- latency;
- error rates;
- rate-limit state;
- active model routing;
- MCP capability bindings;
- tool risk classification;
- recent denied calls.

Never expose credentials.

Never expose raw authorization headers.

Never expose secret material even to privileged UI roles.

---

# 11. Workstream G — Visual Intelligence Observatory

## Location

```text
src/visual_observatory/
```

Required modules:

```text
artifact_view.py
quality_view.py
drift_view.py
lineage_view.py
benchmark_view.py
visual_gap_view.py
quarantine_view.py
__init__.py
```

Expose:

- generated asset;
- artifact ID;
- model/provider;
- dimensions;
- aspect ratio;
- quality score;
- visual regression score;
- prompt consistency;
- lineage status;
- benchmark relationship;
- drift status;
- quarantine status.

Visual assets must remain linked to their cryptographic lineage.

If lineage validation fails:

```text
ARTIFACT STATUS = QUARANTINED
```

No UI action may silently clear quarantine.

---

# 12. Workstream H — Reliability Center

## Location

```text
src/reliability_center/
```

Required modules:

```text
slo_view.py
error_budget_view.py
latency_view.py
incident_view.py
recovery_view.py
dependency_view.py
rollback_view.py
__init__.py
```

Expose:

- availability;
- p50/p90/p95/p99;
- error budget;
- burn rate;
- provider health;
- circuit breakers;
- incidents;
- recovery drills;
- DLQ;
- rollback state;
- persistence health;
- backup/restore health.

Thresholds must come from existing reliability configuration.

Do not duplicate hard-coded thresholds in frontend code.

---

# 13. Workstream I — Evidence Explorer

## Location

```text
src/evidence_explorer/
```

Required modules:

```text
event_query.py
lineage_query.py
authorization_evidence.py
model_evidence.py
provider_evidence.py
deployment_evidence.py
integrity.py
export.py
__init__.py
```

The evidence explorer must provide a chronological, correlated view:

```text
REQUEST
  ↓
AUTHENTICATION
  ↓
AUTHORIZATION
  ↓
WORK INTAKE
  ↓
MODEL/TOOL INVOCATION
  ↓
REVIEW
  ↓
EXECUTION
  ↓
OBSERVATION
  ↓
OUTCOME
  ↓
LEARNING
```

Every displayed event should retain:

```text
event_id
timestamp
correlation_id
causation_id
client_id / scoped identity
event_type
status
hash/reference
```

The explorer must verify cryptographic ledger integrity rather than assuming the ledger is valid.

---

# 14. Workstream J — API Boundary

## Location

```text
src/api/
```

Required modules:

```text
auth.py
routes.py
schemas.py
middleware.py
errors.py
rate_limits.py
tenant_guard.py
serialization.py
versioning.py
health.py
__init__.py
```

Recommended namespace:

```text
/api/v1/control-plane/*
```

Every request must pass:

```text
Authentication
    ↓
Identity Validation
    ↓
Tenant/Client Context Guard
    ↓
Role Capability Check
    ↓
Input Validation
    ↓
Existing Domain Boundary
    ↓
Safe DTO Projection
```

Never:

```text
Frontend
  ↓
Database
```

and never:

```text
Frontend
  ↓
Internal service object
```

---

# 15. Event Streaming

Where real-time updates are needed, introduce a controlled event stream.

Candidate events:

```text
CAMPAIGN_UPDATED
DELIVERABLE_UPDATED
APPROVAL_CREATED
APPROVAL_EXPIRED
APPROVAL_REVOKED
WORK_ITEM_STARTED
WORK_ITEM_FAILED
MODEL_DEGRADED
PROVIDER_OUTAGE
VISUAL_QUARANTINE
SLO_WARNING
SLO_CRITICAL
BUDGET_WARNING
ROLLBACK_STARTED
ROLLBACK_COMPLETED
INCIDENT_CREATED
```

Events must be:

- sanitized;
- tenant-scoped;
- authenticated;
- correlated;
- replay-safe where mutation is involved;
- read-only from the UI perspective unless explicitly routed through a governed action endpoint.

---

# 16. Frontend Contract

The frontend must consume only versioned DTOs.

Example:

```typescript
interface CampaignSummary {
  campaignId: string;
  clientId: string;
  name: string;
  state: CampaignState;
  progress: number;
  approvalRequired: boolean;
  lastUpdatedAt: string;
}
```

Do not expose backend internals such as:

```typescript
_internalPolicy
_rawPrompt
_chainOfThought
_providerCredential
_executionAuthority
```

The frontend should display **evidence-backed state**, not infer state from button availability.

---

# 17. Human Action Model

All UI actions must follow:

```text
UI Intent
   ↓
API Request
   ↓
Identity Validation
   ↓
Tenant Guard
   ↓
Capability Check
   ↓
Domain Validation
   ↓
Human Authorization Boundary if required
   ↓
Execution Boundary if authorized
   ↓
Audit Event
   ↓
Safe Response
```

Examples:

### Review

```text
Review Deliverable
→ no execution authority
```

### Request approval

```text
Request Approval
→ creates approval request
→ does not execute
```

### Approve

```text
Approve
→ existing HumanAuthorizationBoundary
→ authorization artifact
→ execution remains separate
```

### Execute

```text
Execute
→ only permitted if valid authorization exists
→ existing execution boundary
```

---

# 18. Tenant Isolation Requirements

Phase 25 must include explicit tests for:

```text
Client A cannot read Client B campaign
Client A cannot read Client B assets
Client A cannot read Client B model context
Client A cannot read Client B MCP observations
Client A cannot read Client B approval evidence
Client A cannot read Client B intelligence
```

Global institutional views may expose only:

```text
de-identified pattern
validated abstract strategy
aggregate metric
provenance-safe knowledge
```

Never raw client data.

---

# 19. Security Threat Suite

Create:

```text
tests/phase25/
```

Minimum threat scenarios:

```text
T25-001 UI claims authorization
T25-002 forged approval ID
T25-003 expired approval reused
T25-004 revoked approval reused
T25-005 client A accesses client B
T25-006 global view exposes client payload
T25-007 frontend requests hidden DTO field
T25-008 API bypasses capability check
T25-009 operator role escalation
T25-010 model output presented as authorization
T25-011 MCP result becomes UI command
T25-012 UI action bypasses execution boundary
T25-013 chain-of-thought leakage
T25-014 secret leakage through DTO
T25-015 secret leakage through event stream
T25-016 visual quarantined artifact released through UI
T25-017 tampered evidence displayed as trusted
T25-018 stale dashboard action executed
T25-019 duplicate mutation through retry
T25-020 cross-client websocket/event leakage
T25-021 provider credential disclosure
T25-022 cost/budget control bypass
T25-023 rollback control bypass
T25-024 audit logging bypass
T25-025 security policy mutation through UI
```

All must fail closed.

---

# 20. Functional Test Requirements

Minimum functional coverage:

### Control Plane

- authenticated session;
- role resolution;
- capability checks;
- DTO serialization;
- client isolation.

### Campaign

- campaign projection;
- state visualization;
- deliverable progression;
- timeline;
- dependency rendering.

### Authorization

- request;
- approval;
- rejection;
- expiry;
- revocation;
- stale action rejection.

### Intelligence

- model telemetry;
- strategy lifecycle;
- capability gaps;
- visual benchmark history;
- provenance.

### Reliability

- SLO display;
- error budget;
- provider degradation;
- circuit breaker;
- incident;
- recovery;
- rollback.

### Evidence

- event retrieval;
- correlation;
- lineage;
- ledger verification;
- tamper detection.

---

# 21. Integration Tests

The engineer must execute end-to-end workflows.

## Workflow A — Campaign

```text
Client
→ Campaign
→ Workforce
→ Model
→ Visual Generation
→ Critique
→ Review
→ Approval
→ Execution
→ Outcome
→ Learning
→ Dashboard
```

## Workflow B — Failed Provider

```text
Provider Failure
→ Circuit Breaker
→ Queue Preservation
→ Operator Alert
→ Recovery
→ Retry under policy
→ Evidence
```

## Workflow C — Visual Drift

```text
Generated Artifact
→ Drift Detection
→ Threshold Breach
→ Quarantine
→ Operator Notification
→ Human Review
→ Approved disposition
```

## Workflow D — Authorization

```text
Work Request
→ Approval Required
→ Operator Review
→ Approve
→ Existing Authorization Boundary
→ Execute
→ Evidence
```

## Workflow E — Tenant Isolation

Run simultaneous workloads for at least:

```text
Client A
Client B
Client C
```

Attempt deliberate cross-client access from:

- REST/API;
- websocket/event stream;
- dashboard;
- evidence explorer;
- intelligence explorer;
- visual explorer.

---

# 22. Stale-State Protection

Every mutating control-plane action must support optimistic concurrency.

Example:

```text
expected_version
```

If server state changed:

```text
409 CONFLICT
```

The UI must refresh before allowing the operator to retry.

This prevents:

```text
stale approval
stale campaign action
stale provider action
stale rollback action
```

from being applied against newer state.

---

# 23. Audit Requirements

Every meaningful operator interaction must produce an immutable event.

At minimum:

```text
LOGIN
LOGOUT
VIEW_SENSITIVE_OPERATIONAL_SCOPE
APPROVAL_REQUESTED
APPROVAL_APPROVED
APPROVAL_REJECTED
APPROVAL_REVOKED
ACTION_REQUESTED
ACTION_DENIED
ACTION_EXECUTED
FEEDBACK_SUBMITTED
QUARANTINE_VIEWED
QUARANTINE_ACTION_REQUESTED
ROLLBACK_REQUESTED
ROLLBACK_EXECUTED
EXPORT_REQUESTED
```

Audit events must preserve the distinction between:

```text
requested
authorized
executed
observed
```

---

# 24. Observability Requirements

Phase 25 itself must be observable.

Track:

```text
control_plane_request_count
control_plane_error_rate
control_plane_latency
authorization_latency
dashboard_generation_latency
event_stream_latency
dto_redaction_count
denied_action_count
cross_tenant_denial_count
stale_action_count
evidence_integrity_failures
```

No sensitive payloads in telemetry.

---

# 25. Performance Requirements

Initial targets:

| Area | Target |
|---|---:|
| Read API p95 | ≤ 500 ms |
| Dashboard snapshot p95 | ≤ 1000 ms |
| Approval projection p95 | ≤ 500 ms |
| Event propagation | ≤ 2 s |
| DTO serialization p95 | ≤ 100 ms |
| Tenant authorization check | ≤ 100 ms |

These are Phase 25 operational targets and do not replace existing model/provider SLOs.

Benchmark under realistic multi-client load.

---

# 26. Reliability Requirements

The control plane must degrade safely.

If a subsystem is unavailable:

```text
Unavailable Intelligence
→ show unavailable state
→ do not fabricate values

Unavailable Provider
→ show DEGRADED/UNAVAILABLE
→ do not expose credentials

Unavailable Evidence Ledger
→ evidence marked UNVERIFIED
→ do not display as trusted

Unavailable Authorization Service
→ no approval action
→ fail closed

Unavailable Execution Service
→ action remains pending/blocked
→ no retry outside policy
```

The UI must never convert uncertainty into false certainty.

---

# 27. Real-World Validation

Do not rely exclusively on mocked providers.

At minimum validate the control plane against the established real integration boundaries from Phases 20–24:

### LLM

- real model telemetry;
- real routing;
- real cost accounting;
- real latency.

### Vision

- real generated artifact;
- real artifact lineage;
- real quality/drift data.

### MCP

- real scoped tool calls;
- denied capability;
- rate limiting;
- circuit breaker.

### Production Runtime

- queue;
- worker;
- state recovery;
- authorization;
- evidence.

Where external credentials are unavailable, explicitly report:

```text
NOT_EXECUTED — CREDENTIALS_UNAVAILABLE
```

Do not treat simulated success as production evidence.

---

# 28. Visual Intelligence Requirement

The control plane must expose the actual visual knowledge boundary established by Phases 20–24.

The UI must answer:

```text
What does ILYREN know visually?
What benchmark version measured it?
Which tasks are strong?
Which tasks are weak?
What are the failure categories?
Which capability gaps remain?
When was the benchmark last run?
Has performance drifted?
What training/evaluation evidence is required next?
```

Do not display a single "visual intelligence score" without the underlying task/category breakdown.

---

# 29. Documentation Deliverables

Create:

```text
docs/phase25/
├── PHASE-25-ARCHITECTURE.md
├── PHASE-25-CONTROL-PLANE-REPORT.md
├── PHASE-25-OPERATOR-CONSOLE-REPORT.md
├── PHASE-25-AUTHORIZATION-CENTER-REPORT.md
├── PHASE-25-INTELLIGENCE-OBSERVATORY-REPORT.md
├── PHASE-25-PROVIDER-MCP-CONTROL-REPORT.md
├── PHASE-25-VISUAL-OBSERVATORY-REPORT.md
├── PHASE-25-RELIABILITY-CENTER-REPORT.md
├── PHASE-25-EVIDENCE-REPORT.md
├── PHASE-25-SECURITY-REVIEW.md
├── PHASE-25-THREAT-MODEL.md
├── PHASE-25-TEST-REPORT.md
├── PHASE-25-REAL-WORKFLOW-REPORT.md
├── PHASE-25-PERFORMANCE-REPORT.md
├── PHASE-25-PRODUCTION-READINESS-REVIEW.md
└── PHASE-25-GOVERNANCE-GATE.md
```

---

# 30. Required Test Commands

At minimum:

```powershell
python -m pytest tests/phase25/ -v
```

Then:

```powershell
python -m pytest tests/phase20/ tests/phase21/ tests/phase22/ tests/phase23/ tests/phase24/ tests/phase25/ -v
```

If frontend TypeScript exists:

```powershell
npx tsc --noEmit
```

Execute the applicable production build as well.

Do not report "production ready" from unit tests alone.

---

# 31. Acceptance Gates

Define deterministic release gates.

| Gate | Requirement |
|---|---|
| P25-01 | All Phase 25 unit/integration tests pass |
| P25-02 | All 25 security scenarios pass |
| P25-03 | Cross-phase regression passes |
| P25-04 | Type/static analysis passes |
| P25-05 | Zero secret leakage |
| P25-06 | Zero cross-client leakage |
| P25-07 | Zero UI authorization forgery |
| P25-08 | Authorization lifecycle verified |
| P25-09 | Stale-state protection verified |
| P25-10 | Evidence integrity verified |
| P25-11 | Real model telemetry verified |
| P25-12 | Real visual telemetry verified |
| P25-13 | Real MCP telemetry verified |
| P25-14 | Reliability dashboard verified |
| P25-15 | Visual intelligence breakdown verified |
| P25-16 | Event-stream isolation verified |
| P25-17 | Operator audit trail verified |
| P25-18 | Performance targets verified |
| P25-19 | Recovery/degradation behavior verified |
| P25-20 | Production configuration audit verified |

Every gate is binary:

```text
PASS
FAIL
```

No partial release approval.

---

# 32. Definition of Done

Phase 25 is complete only when:

```text
[ ] Control plane implemented
[ ] Operator console implemented
[ ] Campaign command center implemented
[ ] Human authorization center integrated
[ ] Intelligence observatory implemented
[ ] Provider/MCP control center implemented
[ ] Visual observatory implemented
[ ] Reliability center implemented
[ ] Evidence explorer implemented
[ ] Versioned API boundary implemented
[ ] Tenant isolation verified
[ ] RBAC/capabilities verified
[ ] Stale-state protection verified
[ ] Event stream isolation verified
[ ] Secret/CoT redaction verified
[ ] Real model telemetry verified
[ ] Real visual telemetry verified
[ ] Real MCP telemetry verified
[ ] Visual knowledge gaps surfaced
[ ] 25/25 threat scenarios pass
[ ] Cross-phase regression passes
[ ] Performance targets pass
[ ] Recovery tests pass
[ ] Documentation complete
[ ] Governance gate independently reviewed
```

---

# 33. Critical Engineering Rule

Do not confuse a sophisticated interface with a sophisticated system.

The control plane is successful only if it accurately exposes the already-existing system boundaries.

A dashboard that says:

```text
AUTHORIZED
```

when no valid authorization artifact exists is a **security failure**, not a UI bug.

A dashboard that says:

```text
EXECUTED
```

when only a model recommendation exists is a **governance failure**.

A dashboard that shows:

```text
CLIENT B DATA
```

to Client A is a **tenant isolation failure**.

A dashboard that displays a generated image without valid lineage is an **evidence failure**.

A dashboard that shows stale state and permits mutation is a **reliability failure**.

Treat these as security-critical engineering defects.

---

# 34. Phase 25 Governance Boundary

The following must remain unchanged:

```text
Phase 10
Human Authorization
        ↓
Execution Authority
        ↓
Phase 13 Integration Controls
        ↓
Phase 17 Production Fabric
        ↓
Phase 23 Production Runtime
        ↓
Phase 24 Live Operations
```

Phase 25 may **observe, request, present, route, and audit**.

It may not create a parallel path around those boundaries.

---

# 35. Mandatory Verbatim Governance Statement

> **Phase 25 establishes the ILYREN Institutional Production Control Plane & Operator Command Center above the Phase 1–24 substrate. It converts the validated intelligence, workforce, production, model, visual, MCP, reliability, and evidence capabilities into a secure human-operable product surface without creating independent authorization authority. All human actions remain subordinate to the existing authorization and execution boundaries; client isolation remains mandatory; model outputs and external observations remain untrusted until evaluated; institutional intelligence remains distinct from client-confidential data; and security policy remains immutable.**

$$\mathbf{Operational\ Visibility} + \mathbf{Human\ Control} + \mathbf{Evidence} + \mathbf{Reliability}$$

$$\boxed{\mathbf{ILYREN\ becomes\ operationally\ usable\ without\ becoming\ independently\ authoritative}}$$

---

# 36. Engineer's Final Instruction

Do not proceed to Phase 26 until Phase 25 has produced measurable evidence that:

1. a real operator can use the system;
2. a real client can safely see only their own information;
3. authorized human actions reach the existing authorization boundary;
4. unauthorized actions fail closed;
5. real model/vision/MCP telemetry is visible without secret leakage;
6. visual intelligence capability gaps are observable;
7. reliability state is observable;
8. evidence lineage is verifiable;
9. stale actions are rejected;
10. recovery and degradation are understandable to operators;
11. all 25 threat scenarios pass;
12. the full regression suite remains green.

**Phase 25 is not complete because the interface looks finished. It is complete when the interface becomes a trustworthy operational window into the governed ILYREN system.**
