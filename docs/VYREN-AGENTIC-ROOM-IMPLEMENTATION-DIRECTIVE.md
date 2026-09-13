# VYREN — AGENTIC ROOM & OPENAI AGENTS RUNTIME IMPLEMENTATION DIRECTIVE

**Status:** Engineering Directive  
**Scope:** VYREN Room, governed agent runtime adapter, orchestrator, first vertical slice

## Objective

Transform VYREN's primary experience into a persistent collaborative **VYREN Room**.

```text
User → Teaches VYREN → VYREN Builds Context
     → Understands → Thinks → Collaborates
     → Creates → Learns
```

The user experiences one continuous collaboration. Internally, VYREN may delegate to multiple specialist workers.

## Product North Star

> VYREN should feel like sitting down with an exceptional creative team that already knows the context, thinks with you, does the work, and only interrupts you when your judgment matters.

The conversation is the primary interaction layer. Artifacts, decisions, approvals, context, and work states appear inside the Room.

## Architecture Boundary

Preserve Phases 25–29. Do not rewrite them.

VYREN owns:

- identity and tenant isolation
- brand/product/campaign state
- Visual DNA
- knowledge, evidence, provenance
- memory
- decisions and approvals
- permissions and authorization
- governance, audit, rollback
- learning policy and outcome interpretation

The agent runtime provides:

- agent execution
- model interaction
- context management
- long-running sessions
- subagents
- tools/MCP
- sandbox/compute
- runtime recovery and tracing

Mandatory:

```text
VYREN AUTHORIZES.
AGENTS EXECUTE.

Intelligence ≠ Authorization
Agent ≠ Authority
Skill ≠ Authority
Tool Access ≠ Permission
Model Output ≠ Truth
Recommendation ≠ Decision
Decision ≠ Execution Permission
Learning ≠ Policy Mutation
Recovery ≠ Authorization
```

## Target Architecture

```text
                         HUMAN
                           │
                           ▼
                    ┌─────────────┐
                    │ VYREN ROOM  │
                    └──────┬──────┘
                           ▼
                  ┌─────────────────┐
                  │ VYREN           │
                  │ ORCHESTRATOR    │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          STRATEGY     INTELLIGENCE  CREATIVE
              │            │            │
              └────────────┼────────────┘
                           ▼
                        VISUAL
                           │
                           ▼
                        QUALITY
                           │
                           ▼
                  ┌─────────────────┐
                  │ VYREN GOVERNANCE│
                  └────────┬────────┘
                           ▼
                    AGENT RUNTIME
                           ▼
             OpenAI Agents API / Runtime
                           │
                 ┌─────────┼─────────┐
                 ▼         ▼         ▼
                MCP       TOOLS    SANDBOX
```

## 1. Agent Runtime Adapter

Create:

```text
src/agent_runtime/
    interfaces/
    openai/
    sessions/
    workers/
    tools/
    events/
    policy/
    recovery/
    errors/
```

Define a provider-neutral interface first:

```text
AgentRuntime
    create_session()
    resume_session()
    run()
    stream()
    delegate()
    stop()
    recover()
    close()
```

Only the OpenAI adapter may depend directly on provider-specific APIs.

## 2. Worker Mapping

Phase 26 remains canonical.

```text
VYREN Worker
    │
    ├── identity
    ├── role
    ├── skills
    ├── memory scope
    ├── tenant scope
    ├── campaign scope
    ├── tool bindings
    └── authority scope
             │
             ▼
      Runtime Adapter
             │
             ▼
       OpenAI Agent
```

The runtime agent is an implementation of a VYREN worker, not its canonical identity.

## 3. VYREN Orchestrator

Create:

```text
src/orchestrator/
```

Responsibilities:

1. understand Room state;
2. interpret user intent;
3. identify missing information;
4. decide whether VYREN can safely proceed;
5. delegate to permitted workers;
6. collect results;
7. resolve or expose contradictions;
8. construct artifacts;
9. determine whether human attention is required;
10. present the next meaningful interaction.

It must not grant authority, mutate security policy, bypass governance, or directly perform privileged actions.

## 4. VYREN Room

Create:

```text
src/vyren_room/
    conversation/
    messages/
    artifacts/
    decisions/
    approvals/
    activity/
    composer/
    presence/
    state/
    streaming/
    adapters/
```

Core entities:

```text
Room
RoomParticipant
RoomMessage
RoomArtifact
RoomDecision
RoomApproval
RoomWorkEvent
RoomSession
```

The default human-facing actor is **VYREN**. Specialist workers appear contextually rather than as a noisy permanent group chat.

## 5. Human Attention Policy

Possible outcomes:

```text
CONTINUE_AUTOMATICALLY
SHOW_PROGRESS
SHOW_RESULT
ASK_CLARIFICATION
REQUEST_DECISION
REQUEST_APPROVAL
BLOCK
```

Rules:

```text
If VYREN can safely decide:
    continue automatically.

If ambiguity materially affects the result:
    ask.

If consequential human judgment is required:
    request a decision.

If consequential execution requires approval:
    request approval.

If governance is uncertain:
    block/fail closed.
```

Principle:

> Do not ask the human what VYREN can safely decide.

> Do not decide for the human what only the human should decide.

## 6. Artifact-First Conversation

Supported artifact types:

```text
BRAND_UNDERSTANDING
PRODUCT_UNDERSTANDING
AUDIENCE_UNDERSTANDING
VISUAL_DNA
RESEARCH
CREATIVE_DIRECTION
MOODBOARD
CAMPAIGN_CONCEPT
COPY
VISUAL_EXPLORATION
ASSET_COLLECTION
PRODUCTION_PLAN
APPROVAL_REQUEST
OUTCOME_REPORT
LEARNING_SIGNAL
```

Artifacts must render inside the Room.

Example:

```text
VYREN

"I've developed two viable directions."

┌─────────────────┐  ┌─────────────────┐
│ Direction A     │  │ Direction B     │
│ [Visual]        │  │ [Visual]        │
│ [Choose]        │  │ [Choose]        │
└─────────────────┘  └─────────────────┘

[Compare] [Challenge]
```

## 7. Live Work

Room events:

```text
room.created
message.created
agent.started
agent.progress
agent.delegated
agent.completed
agent.failed
artifact.created
artifact.updated
decision.requested
decision.confirmed
approval.requested
approval.granted
approval.denied
knowledge.updated
campaign.updated
learning.created
```

Expose operational progress, never private chain-of-thought.

Example:

```text
Understanding your product       ✓
Studying your references         ✓
Exploring creative directions   ●
Quality review                   ○
```

## 8. Session and Memory Boundary

Keep:

```text
VYREN Room Session
        │
        ├── canonical VYREN state
        │
        └── Agent Runtime Session
```

Runtime context is a projection of permitted VYREN context.

Never equate:

```text
Agent Runtime Session = VYREN Memory
```

Canonical memory remains VYREN-owned:

```text
Conversation Memory
Campaign Memory
Brand Memory
Institutional Memory
```

## 9. Knowledge Contract

Every meaningful extracted fact preserves:

```text
value
source
source_type
confidence
epistemic_status
created_at
updated_at
```

States:

```text
KNOWN
INFERRED
USER_CONFIRMED
UNKNOWN
CONFLICTED
```

Unknown and conflict must survive. Inference must not silently become fact.

## 10. Tool and MCP Boundary

Every tool is registered in VYREN with:

```text
tool_id
tenant_scope
allowed_roles
required_authority
read_write
data_classification
approval_required
evidence_requirement
audit_requirement
```

Architecture:

```text
Agent
  ↓
VYREN Tool Registry
  ↓
Policy Check
  ↓
MCP Gateway / Tool
  ↓
External System
```

External tool/MCP output is **untrusted data**. It does not become truth, authority, permission, or policy automatically.

## 11. Onboarding

Onboarding is the first VYREN Room.

Do not build a giant setup wizard.

```text
VYREN
"Tell me what you're building."

        ↓
User answers

        ↓
VYREN
"Here's what I understand."

[Confirm] [Correct]

        ↓
Product Understanding

        ↓
Visual references

        ↓
Visual DNA Foundation

        ↓
Creative calibration

        ↓
Brand Understanding
Product Understanding
Audience Understanding
Visual DNA Foundation
Creative Preferences
Initial Objectives

        ↓
"What should we create?"
```

The user remains in the same Room throughout onboarding.

## 12. First Vertical Slice

Do not migrate the entire workforce initially.

Build:

```text
USER
  ↓
VYREN ROOM
  ↓
VYREN ORCHESTRATOR
  ↓
INTELLIGENCE WORKER
  ↓
OPENAI AGENTS RUNTIME
  ↓
ONE SCOPED RESEARCH TOOL
  ↓
EVIDENCE
  ↓
VYREN GOVERNANCE
  ↓
RESEARCH ARTIFACT
  ↓
VYREN ROOM
  ↓
USER CONFIRMATION
```

Tool:

```text
research.search
```

The worker proposes a `KnowledgeUpdateProposal`; it does not directly mutate canonical knowledge.

## 13. Multi-Worker Slice

After the first slice works:

```text
USER
 ↓
VYREN
 ↓
Intelligence
 ↓
Creative
 ↓
Visual
 ↓
Quality
 ↓
VYREN
 ↓
Creative Direction Artifact
 ↓
USER DECISION
```

The decision becomes campaign memory.

## 14. ChatKit Evaluation

Evaluate ChatKit as conversation infrastructure, not as the entire VYREN product.

```text
ChatKit / conversation infrastructure
                ↓
        VYREN Room Adapter
                ↓
        VYREN State + Artifacts
```

VYREN-native UI remains responsible for creative directions, visual comparison, Visual DNA, evidence, decisions, approvals, campaign artifacts, production, and learning.

Decide based on prototype evidence.

## 15. Observability and Recovery

Trace:

```text
Room
 ↓
Orchestrator
 ↓
Worker
 ↓
Subagent
 ↓
Tool
 ↓
Governance
 ↓
Result
 ↓
Artifact
 ↓
Decision
```

Preserve:

```text
trace_id
room_id
tenant_id
worker_id
runtime_session_id
tool_id
authorization_decision
timestamp
provenance
```

On failure:

```text
Agent failure
    ↓
Runtime recovery
    ↓
Restore safe state
    ↓
Re-evaluate authorization
    ↓
Resume only if permitted
```

## 16. Security Validation

Minimum first-slice adversarial tests:

```text
T-001 Tenant traversal
T-002 Unauthorized tool
T-003 Authority escalation
T-004 Prompt injection
T-005 Malicious tool output
T-006 Fabricated evidence
T-007 Memory contamination
T-008 Cross-client leakage
T-009 Stale session replay
T-010 Revoked approval replay
T-011 Agent impersonation
T-012 Worker privilege escalation
T-013 Unauthorized MCP invocation
T-014 Hidden instruction injection
T-015 Artifact provenance substitution
T-016 Unauthorized publication
T-017 Policy mutation through agent
T-018 Knowledge mutation without governance
T-019 Approval spoofing
T-020 Recovery without authorization
```

All must fail closed.

## 17. UX Acceptance

A new user must be able to:

1. enter VYREN;
2. explain what they are building;
3. answer adaptive questions;
4. confirm/correct VYREN's understanding;
5. provide references;
6. see Visual DNA being formed;
7. receive creative recommendations;
8. choose or challenge a direction;
9. receive rich artifacts;
10. continue working without learning VYREN's architecture.

The user must not need to configure agents, workers, MCP, runtime sessions, memory systems, or workflows.

## 18. Implementation Order

```text
1. AgentRuntime interface
2. OpenAI runtime adapter
3. Room event model
4. Room streaming
5. VYREN Orchestrator
6. Intelligence Worker
7. One governed tool
8. Evidence result
9. Artifact rendering
10. Human confirmation
11. Persistent Room state
12. Creative Worker
13. Visual Worker
14. Quality Worker
15. Multi-worker delegation
16. ChatKit evaluation
17. Long-running/asynchronous workflows
18. Production hardening
```

## 19. Definition of Done

A user can enter VYREN and say:

> "I want to launch this product."

VYREN can understand, ask only necessary questions, research, build context, confirm understanding, develop creative directions, collaborate internally, present recommendations, receive a human decision, develop, review, produce, request approval when necessary, launch through governed execution, observe outcomes, and learn.

The user experiences:

```text
ONE VYREN
ONE ROOM
ONE CONTINUOUS RELATIONSHIP
```

The system may internally use many workers, tools, models, sessions and subagents.

That complexity remains behind the Room.

## Final Principle

VYREN is not a chatbot and not an OpenAI Agent with a frontend.

VYREN is a governed Creative Intelligence Operating System whose human experience is a persistent collaborative Room and whose workforce can use multiple agent runtimes.

The OpenAI Agents API is an execution substrate.

The VYREN Room is the product.

The VYREN Control Plane is the authority boundary.

VYREN Knowledge and Memory are the organizational brain.

The AI workforce is the labor layer.

The human remains the consequential decision-maker.
