# PHASE 27 — ILYREN CREATIVE CAMPAIGN STUDIO
## Human Experience, Campaign Operating System & Product Surface

**Document Type:** Engineering Directive  
**Program:** ILYREN Creative Intelligence Platform / Creative Operating System  
**Phase:** 27  
**Predecessor:** Phase 26 — ILYREN Creative Workforce Product Layer  
**Status:** READY FOR IMPLEMENTATION

---

# 1. Executive Directive

Phase 27 shall transform the capabilities established through Phases 1–26 into the first coherent **ILYREN Creative Campaign Studio product experience**.

Phase 26 established persistent AI coworkers, skills, routines, campaign rooms, bounded delegation, scoped memory, capability bindings, approvals, evidence, and workforce observability.

Phase 27 must make those capabilities operate as a unified product workflow centered on the user's actual creative work.

The canonical flow is:

```text
Business Objective
      ↓
Product Understanding
      ↓
Brand Understanding
      ↓
Adaptive Discovery
      ↓
Creative Intelligence
      ↓
Creative Direction
      ↓
Visual Intelligence
      ↓
Campaign Development
      ↓
Review / Revision
      ↓
Production
      ↓
Launch
      ↓
Outcome
      ↓
Learning
```

The objective is not to expose the underlying agent architecture. The objective is to make the intelligence architecture feel like a coherent creative organization.

---

# 2. Critical Review of Phase 26

The Phase 26 walkthrough reports:

```text
56 / 56 dedicated tests
301 / 301 cross-phase tests
25 / 25 security scenarios
5 / 5 workflows
20-step productization benchmark
```

and declares:

> PASS — CREATIVE WORKFORCE PRODUCT LAYER VALIDATED

These results establish strong implementation evidence for the reported test corpus. They do **not**, by themselves, prove that the workforce architecture is universally secure, correct, or production-complete.

Phase 27 must preserve the validation discipline established earlier:

- test coverage must not be confused with architectural proof;
- passing integration workflows must not imply real-world UX validation;
- worker rationale must not be treated as hidden reasoning transparency;
- simulated external actions must not be represented as live-world success;
- benchmark success must remain bounded by benchmark scope;
- model/provider behavior must remain observable and attributable;
- natural-language intent must never become authorization merely because it was expressed naturally.

Phase 27 therefore adds **product-level validation**, not merely another feature layer.

---

# 3. Strategic Product Transition

```text
PHASE 1–4
Security substrate / verification research

PHASE 5–13
Governed runtime and execution architecture

PHASE 14–19
Creative workforce + institutional intelligence

PHASE 20–24
Real intelligence integrations + production operations

PHASE 25
Institutional production control plane

PHASE 26
Persistent creative workforce

PHASE 27
Creative Campaign Studio
```

Phase 27 is the transition from **capability platform** to **coherent product experience**.

---

# 4. Product Thesis

ILYREN should not present itself as:

- an agent builder;
- a prompt interface;
- an image generator;
- a workflow automation tool;
- a collection of AI models.

The product should present itself as:

> **A Creative Intelligence Studio where humans work with a governed AI creative workforce to understand products, develop campaigns, create visual directions, produce assets, and learn from outcomes.**

---

# 5. Core Product Objects

```text
Organization
    |
    +-- Client
          |
          +-- Brand
                |
                +-- Product
                      |
                      +-- Campaign
                            |
                            +-- Creative Room
                                  |
                                  +-- Mission
                                        |
                                        +-- Tasks
                                        +-- Workers
                                        +-- Decisions
                                        +-- Evidence
                                        +-- Assets
                                        +-- Approvals
                                        +-- Outcomes
```

Reuse Phase 25 and Phase 26 domain models. Do not create shadow campaign, client, worker, or approval models.

---

# 6. Primary User Journey

```text
WELCOME
   ↓
WORKSPACE
   ↓
CLIENT / BRAND
   ↓
PRODUCT
   ↓
CAMPAIGN
   ↓
DISCOVERY
   ↓
CREATIVE INTELLIGENCE
   ↓
CREATIVE DIRECTIONS
   ↓
VISUAL DEVELOPMENT
   ↓
CAMPAIGN ASSETS
   ↓
REVIEW
   ↓
APPROVAL
   ↓
PRODUCTION
   ↓
LAUNCH
   ↓
OUTCOMES
```

The system should preserve continuity between stages so users do not reconstruct context manually.

---

# 7. Product Experience Modes

```text
OBSERVE
UNDERSTAND
COLLABORATE
EXECUTE
```

**OBSERVE:** gather and present relevant information.

**UNDERSTAND:** construct product, brand, audience, domain, and visual intelligence.

**COLLABORATE:** human and workforce develop strategy and creative direction together.

**EXECUTE:** approved work enters governed production.

Execution remains downstream of authorization.

---

# 8. Human / AI Responsibility Model

Human owns:

```text
Business objective
Audience
Positioning
Strategic intent
Consequential decisions
Final approvals
```

Shared:

```text
Campaign strategy
Creative direction
Prioritization
Iteration
Review
```

AI workforce owns within bounded authority:

```text
Research
Synthesis
Creative exploration
Visual analysis
Campaign development
Asset planning
Quality review
Performance analysis
Workflow coordination
```

The interface must communicate this division clearly.

---

# 9. Workspace

The Workspace is the user's persistent home.

Minimum areas:

```text
Overview
Clients
Brands
Products
Campaigns
Creative Workforce
Knowledge
Visual DNA
Production
Outcomes
Activity
```

Surface active work rather than requiring users to navigate the architecture manually.

---

# 10. Campaign Command Center

Every campaign requires a unified command center:

```text
Campaign Overview
Objective
Product
Audience
Strategy
Creative Directions
Visual System
Workforce
Assets
Reviews
Approvals
Production
Launch
Performance
Evidence
Activity
```

The command center is the primary campaign-facing source of truth, while authoritative state remains in existing domain services.

---

# 11. Adaptive Discovery

Support an adaptive business interview based on:

```text
product
brand
campaign objective
audience
market
existing knowledge
uncertainty
missing evidence
```

Ask fewer, more consequential questions rather than forcing a static questionnaire.

Track discovery state as:

```text
KNOWN
INFERRED
MISSING
CONFLICTING
UNKNOWN
```

Inferred information must not silently become fact.

---

# 12. Creative Intelligence Surface

Before generating assets, expose:

```text
Business Opportunity
Audience Insight
Brand Tension
Creative Opportunity
Narrative
Creative Territory
Visual Direction
Risks
Unknowns
Evidence
```

This preserves the strategic layer above rendering.

---

# 13. Creative Direction Cards

Each direction must be a structured object:

```text
Direction
Core Idea
Audience Tension
Narrative
Visual Language
Composition
Color
Typography
Motion
Evidence
Confidence
Risks
Alternative
```

Users must be able to compare directions rather than receive one opaque answer.

---

# 14. Visual DNA Integration

For each relevant recommendation show:

```text
Relevant Visual DNA
Why It Matters
Supporting References
Contradicting References
Confidence
Application
```

Visual DNA remains evidence-backed. Similarity must not be presented as strategic correctness.

---

# 15. Visual Development

```text
Creative Direction
      ↓
Art Direction
      ↓
Scene Planning
      ↓
Composition
      ↓
Prompt Compilation
      ↓
Rendering
      ↓
Visual Evaluation
      ↓
Revision
```

Preserve lineage between final assets and originating creative direction.

---

# 16. Asset Lineage

Every production asset should be traceable to:

```text
Campaign
Mission
Creative Direction
Visual Direction
Prompt / Compilation Version
Model
Provider
Generation Event
Evaluation
Review
Approval
Final Asset
```

This is required for reproducibility and post-campaign learning.

---

# 17. Human Review and Revision

Review must support:

```text
Approve
Reject
Request Revision
Comment
Compare
Annotate
Escalate
```

Natural-language review must not automatically equal approval.

Every revision preserves:

```text
previous_version
new_version
reason
requester
worker
evidence
timestamp
```

Historical versions must remain inspectable.

---

# 18. Approval Integration

Reuse existing Phase 25/26 approval mechanisms.

Approval remains:

```text
explicit
scoped
version-bound
auditable
revocable
```

The UI must distinguish:

```text
Recommended
Ready for Review
Awaiting Approval
Approved
Rejected
Production Authorized
```

These states are not interchangeable.

---

# 19. Production Transition

```text
Campaign Studio
      |
      v
Approval
      |
      v
Production Request
      |
      v
Production Fabric
      |
      v
Provider / Tool Execution
      |
      v
Delivery
```

Phase 27 must not create an alternative production execution path.

---

# 20. Launch and Outcome Workspace

Launch workspace:

```text
Approved Assets
Channels
Formats
Scheduling State
Launch Checklist
Approval State
Provider State
Delivery State
Exceptions
```

Clearly distinguish planning state from actual external-world state.

Post-launch:

```text
Outcome Collection
      ↓
Performance Evaluation
      ↓
Attribution Analysis
      ↓
Creative Feedback
      ↓
Campaign Postmortem
      ↓
Institutional Learning
```

Do not represent correlation or attribution evidence as causal proof.

---

# 21. Campaign Memory

Preserve:

```text
Brief
Discovery
Decisions
Creative Directions
Rejected Directions
Approved Direction
Assets
Reviews
Approvals
Outcome
Postmortem
```

Rejected directions are valuable memory but must not silently become current strategy.

---

# 22. Workforce Presence

Workers should appear as organizational participants:

```text
Campaign Planner
    Working on audience opportunity

Creative Director
    Developing campaign territories

Visual DNA Specialist
    Reviewing visual references

Quality Reviewer
    Waiting for directions

Human
    Decision required
```

Communicate responsibility and state without exposing private chain-of-thought.

---

# 23. Command Interface

Support commands such as:

```text
"Build a campaign for..."
"Compare these directions."
"Ask the visual specialist to review this."
"Show evidence."
"Create three alternatives."
"Prepare this for review."
"Pause the campaign."
```

Every command must resolve into structured intent and pass normal authorization/policy evaluation.

---

# 24. Explainability UX

For material recommendations provide:

```text
WHAT
WHY
EVIDENCE
CONFIDENCE
ALTERNATIVES
UNKNOWN
NEXT ACTION
```

Do not expose private chain-of-thought.

---

# 25. Conflict, Error, and Stale-State UX

If workers disagree, preserve disagreement:

```text
Worker A:
Recommendation

Worker B:
Contradicting recommendation

Evidence:
...

Unresolved question:
...

Human decision:
Required
```

If a stale artifact is approved:

```text
This version is no longer current.

Approved:
Direction v4

Current:
Direction v5

Review required.
```

Failure UI should show what failed, where, why it was blocked, what remains valid, available action, and whether human input is required.

UNKNOWN backend state must never be represented as successful external execution.

---

# 26. Operational vs Creative Views

Maintain separate experiences:

### Creative / Client View
Decisions, creative work, evidence, review, approvals, outcomes.

### Studio / Operator View
Worker health, queues, providers, failures, execution, recovery.

### Governance View
Authorization, audit, policy, evidence, risk, compliance.

Shared data is acceptable; responsibilities must not collapse.

---

# 27. API Boundary

Conceptual product-oriented operations:

```text
POST /studio/campaigns
GET  /studio/campaigns/:id
GET  /studio/campaigns/:id/state

POST /studio/campaigns/:id/discovery
POST /studio/campaigns/:id/intelligence
POST /studio/campaigns/:id/directions

POST /studio/campaigns/:id/directions/:direction_id/review
POST /studio/campaigns/:id/directions/:direction_id/approve

POST /studio/campaigns/:id/assets
POST /studio/campaigns/:id/assets/:asset_id/revise

GET  /studio/campaigns/:id/evidence
GET  /studio/campaigns/:id/lineage
GET  /studio/campaigns/:id/activity

POST /studio/campaigns/:id/production
GET  /studio/campaigns/:id/outcomes
POST /studio/campaigns/:id/postmortem
```

Exact naming must conform to existing API conventions.

---

# 28. Suggested Module Structure

```text
src/campaign_studio/
|
+-- workspace/
+-- campaign_workspace/
+-- discovery/
+-- creative_intelligence/
+-- direction_management/
+-- visual_development/
+-- asset_lineage/
+-- review/
+-- approval/
+-- launch/
+-- outcomes/
+-- campaign_memory/
+-- command_interface/
+-- evidence_explorer/
+-- conflict_resolution/
+-- state_projection/
+-- studio_api/
+-- studio_governance/
```

Do not duplicate existing workforce, production, authorization, or intelligence engines.

---

# 29. State Projection

Product read models may be created for performance, but:

> **projection ≠ source of authority**

Authoritative state remains in established domain services. UI optimistic state must never mutate authoritative state or bypass consistency checks.

---

# 30. Security Threat Model

Minimum scenarios:

| ID | Threat | Expected Result |
|---|---|---|
| T27-001 | Unauthorized campaign access | DENY |
| T27-002 | Cross-client campaign access | DENY |
| T27-003 | UI hides approval requirement | Server-side enforcement remains |
| T27-004 | Stale UI approval | DENY |
| T27-005 | Natural-language command bypass | Structured authorization required |
| T27-006 | Hidden worker privilege escalation | DENY |
| T27-007 | Cross-client evidence leakage | DENY |
| T27-008 | Rejected direction treated as approved | DENY |
| T27-009 | Asset lineage tampering | DETECT / DENY |
| T27-010 | Historical version mutation | DENY |
| T27-011 | Worker claims human approval | DENY |
| T27-012 | UI/backend state conflict | Backend authoritative |
| T27-013 | Room membership implies authority | DENY |
| T27-014 | Evidence source substitution | DETECT |
| T27-015 | Prompt injection via artifact | Treat as untrusted |
| T27-016 | Hidden tool invocation | DENY / AUDIT |
| T27-017 | Unauthorized launch | DENY |
| T27-018 | Outcome data scope violation | DENY |
| T27-019 | Worker retirement loses provenance | Preserve attribution |
| T27-020 | Private CoT exposed | Prevent |
| T27-021 | Worker disagreement hidden | Preserve disagreement |
| T27-022 | Unsupported causal claim | Flag uncertainty |
| T27-023 | Production path bypass | DENY |
| T27-024 | Stale private UI cache | Invalidate / reauthorize |
| T27-025 | Broad unintended command | Require explicit structured scope |

---

# 31. Product-Level Adversarial Testing

Test the complete path:

```text
User Input
 -> Command Resolver
 -> Context
 -> Workforce
 -> Intelligence
 -> Approval
 -> Production
```

Include prompt injection, malicious campaign content, misleading filenames, conflicting instructions, stale browser state, unauthorized deep links, manipulated client identifiers, approval replay, fabricated worker messages, manipulated evidence, cross-client navigation, and hidden action requests.

---

# 32. End-to-End Validation

Validate at minimum:

- New Campaign
- Existing Brand
- Multiple Directions
- Revision
- Approval
- Production
- Launch
- Outcome
- Postmortem
- Recovery

Each must preserve context, evidence, authorization, lineage, and accurate state.

---

# 33. Product Usability Validation

Do not rely exclusively on automated tests.

Conduct controlled human evaluation measuring:

```text
time to first meaningful decision
time to understand campaign state
number of manual orchestration actions
approval comprehension
evidence comprehension
error recovery
task completion
user confusion
worker trust calibration
```

The objective is to determine whether the product actually reduces orchestration complexity.

---

# 34. Productization Benchmark

Create a controlled benchmark covering:

```text
Create client
Create brand
Add product
Create campaign
Complete discovery
Generate intelligence
Generate directions
Compare directions
Request revision
Review evidence
Approve direction
Create asset
Review asset
Approve asset
Send to production
Inspect production state
Inspect lineage
Review outcome
Complete postmortem
```

Record both system correctness and human usability.

---

# 35. Performance and Reliability

Measure:

```text
workspace load
campaign load
worker-state refresh
evidence retrieval
direction comparison
asset lineage retrieval
approval transition
activity stream latency
```

The product must remain coherent under worker/provider failure, API timeout, stale browser state, partial production, approval expiration, concurrent edits, campaign version changes, recovery, and service restart.

Do not optimize by weakening authorization or consistency.

---

# 36. Auditability

Every consequential product action must be attributable to:

```text
human
worker
system
routine
external provider
```

Record:

```text
actor
action
object
object_version
scope
timestamp
result
authorization_state
correlation_id
```

---

# 37. Accessibility and Internationalization

Support:

- keyboard navigation;
- accessible controls;
- semantic labels;
- readable evidence presentation;
- responsive layouts;
- localization-ready strings.

Do not defer foundational accessibility decisions until after the product model becomes difficult to change.

---

# 38. Documentation Deliverables

Produce:

```text
PHASE-27-PRODUCT-ARCHITECTURE.md
PHASE-27-UX-ARCHITECTURE.md
PHASE-27-CAMPAIGN-STATE-MODEL.md
PHASE-27-DISCOVERY-SPEC.md
PHASE-27-CREATIVE-INTELLIGENCE-UX.md
PHASE-27-VISUAL-DEVELOPMENT-SPEC.md
PHASE-27-ASSET-LINEAGE.md
PHASE-27-APPROVAL-UX.md
PHASE-27-OUTCOME-SPEC.md
PHASE-27-API-CONTRACT.md
PHASE-27-SECURITY-THREAT-MODEL.md
PHASE-27-TEST-PLAN.md
PHASE-27-USABILITY-VALIDATION.md
PHASE-27-VALIDATION-REPORT.md
PHASE-27-GOVERNANCE.md
```

---

# 39. Acceptance Gates

1. **Unified Campaign Journey** — end-to-end workflow works without manual context reconstruction.
2. **Product Understanding** — product intelligence is visible before creative generation.
3. **Adaptive Discovery** — missing information is identified rather than forcing a static questionnaire.
4. **Creative Intelligence** — decisions are represented above rendering.
5. **Multiple Directions** — alternatives are comparable with evidence and uncertainty.
6. **Visual DNA** — visual intelligence is integrated and traceable.
7. **Asset Lineage** — assets retain creative and production lineage.
8. **Review** — human review is explicit and version-aware.
9. **Approval** — approval is scoped, explicit, version-bound, and auditable.
10. **Production Integration** — no alternate production path exists.
11. **Outcome Continuity** — campaigns connect production to outcomes and postmortem.
12. **Memory Continuity** — campaign memory preserves decisions, alternatives, assets, and outcomes.
13. **Worker Presence** — workers appear as bounded organizational participants.
14. **Evidence Transparency** — material decisions expose evidence, confidence, alternatives, and unknowns.
15. **Security** — all 25 Phase 27 threat scenarios pass.
16. **Cross-Phase Regression** — Phases 1–26 remain green.
17. **End-to-End Validation** — canonical campaign scenarios pass.
18. **Human Usability** — controlled evaluation demonstrates reduced orchestration burden.
19. **Failure UX** — failure and UNKNOWN states are communicated accurately.
20. **No Hidden Authority** — no UI, worker, routine, or command path creates authority outside existing governance.
21. **Independent Validation** — at least one meaningful product/security validation path is independent of implementation logic.
22. **Production Readiness** — no critical unresolved product, security, authorization, data-isolation, or provenance issue remains.

---

# 40. Definition of Done

Phase 27 is complete only when:

- ILYREN has a coherent campaign-centered product experience;
- users can create and manage campaigns without understanding internal agent graphs;
- product understanding precedes creative generation;
- adaptive discovery works;
- creative intelligence is visible;
- multiple creative directions can be compared;
- Visual DNA is integrated;
- visual development is traceable;
- assets retain lineage;
- review and approval are explicit;
- approved work enters the existing production fabric;
- launch state reflects real backend state;
- outcomes connect back to campaigns;
- campaign memory preserves the lifecycle;
- workforce participation is understandable;
- evidence is inspectable;
- stale state is handled safely;
- cross-client isolation is preserved;
- adversarial product tests pass;
- human usability evaluation passes;
- Phase 1–26 regression remains green;
- documentation is complete;
- governance signs off.

---

# 41. Canonical Product Demonstration

```text
1. Open ILYREN.
2. Select a client.
3. Select a brand.
4. Select a product.
5. Create a campaign.
6. ILYREN identifies missing information.
7. Human answers only consequential questions.
8. Workforce develops campaign intelligence.
9. ILYREN presents multiple creative territories.
10. Evidence is inspectable.
11. Human selects a direction.
12. Visual workforce develops the visual system.
13. Assets are generated through governed production.
14. Human reviews a versioned asset.
15. Human approves the exact version.
16. Production Fabric executes.
17. Launch state is shown.
18. Outcome data is collected.
19. Workforce evaluates performance.
20. Campaign postmortem is created.
21. Governed learning is proposed.
```

The demonstration should feel like one continuous organization, not twenty disconnected AI features.

---

# 42. Architectural Rule

Phase 27 must remain a **product surface over the existing intelligence architecture**.

Do not create parallel:

```text
UI Intelligence
UI Memory
UI Authorization
UI Production
UI Worker Engine
```

Instead:

```text
Product Experience
       ↓
Existing Domain Services
       ↓
Existing Intelligence / Workforce / Production / Authorization
       ↓
External Systems
```

---

# 43. Final Engineering Directive

**Implement Phase 27 as the ILYREN Creative Campaign Studio.**

Turn the existing architecture into a coherent human-facing campaign operating system.

The user should be able to enter with a business objective and leave with:

```text
understanding
+
strategy
+
creative direction
+
visual system
+
approved assets
+
production
+
outcomes
+
learning
```

The workforce should feel persistent.

The intelligence should feel contextual.

The evidence should remain inspectable.

The visual intelligence should influence decisions before rendering.

The campaign should retain memory across its lifecycle.

The user should remain the owner of consequential decisions.

The existing authorization and production systems remain authoritative.

The product must never make autonomy appear broader than it actually is.

The desired outcome is not:

> “ILYREN has a beautiful dashboard.”

The desired outcome is:

> **“ILYREN is a place where a human can actually run a creative campaign with an intelligent, governed AI creative organization.”**
