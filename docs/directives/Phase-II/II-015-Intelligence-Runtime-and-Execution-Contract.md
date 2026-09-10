# II-015 — Intelligence Runtime & Execution Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Depends On:** II-001 through II-014  
**Scope:** Execution of the Intelligence Layer as a governed runtime, including orchestration, dependency scheduling, state access, concurrency, retries, execution boundaries, observability, and separation from generation runtime

---

## 1. Purpose

II-015 defines how the semantic contracts established across Phase II become an executable intelligence runtime.

The previous specifications define:

```text
WHAT THE SYSTEM MEANS
WHAT OBJECTS EXIST
WHO MAY DECIDE
HOW OBJECTS EVOLVE
HOW DECISIONS ARE EVALUATED
HOW FAILURES RECOVER
HOW LINEAGE IS PRESERVED
```

II-015 defines:

```text
HOW THOSE CONTRACTS EXECUTE
```

The runtime must therefore execute intelligence decisions without becoming an uncontrolled second intelligence layer.

---

# 2. Core Principle

> **The runtime executes governed intelligence decisions; it must not silently redefine the semantic contracts it is responsible for executing.**

Therefore:

```text
SEMANTIC CONTRACT
        ↓
RUNTIME EXECUTION
```

not:

```text
RUNTIME BEHAVIOR
        ↓
IMPLICIT SEMANTIC AUTHORITY
```

---

# 3. Runtime Boundary

The Intelligence Runtime sits between semantic intelligence objects and concrete execution.

Canonical architecture:

```text
AUTHORITATIVE KNOWLEDGE
        ↓
INTELLIGENCE OBJECTS
        ↓
GOVERNANCE
        ↓
RUNTIME ORCHESTRATION
        ↓
AGENT EXECUTION
        ↓
EVALUATION
        ↓
RECOVERY / ESCALATION
```

The runtime must preserve the boundaries established by II-013 and II-014.

---

# 4. Intelligence Runtime vs Generation Runtime

These are separate concerns.

## Intelligence Runtime

Determines:

```text
what should happen
which agent acts
which object is consumed
which decision is valid
whether execution may continue
```

## Generation Runtime

Performs:

```text
image generation
text generation
rendering
asset production
external model execution
```

Therefore:

```text
INTELLIGENCE RUNTIME
≠
GENERATION RUNTIME
```

The intelligence runtime may request generation but should not silently become responsible for generation semantics.

---

# 5. Runtime Execution Unit

The fundamental runtime unit is an execution task.

Conceptually:

```text
execution_id
task_id
agent_id
input_objects
input_versions
requested_action
authority_context
dependencies
constraints
execution_policy
status
result
events
timestamp
```

The exact runtime schema remains deferred.

---

# 6. Execution Lifecycle

A generalized execution lifecycle is:

```text
REQUESTED
    ↓
AUTHORIZED
    ↓
READY
    ↓
SCHEDULED
    ↓
RUNNING
    ↓
VALIDATING
    ↓
COMPLETED
```

Alternative terminal states include:

```text
FAILED
BLOCKED
CANCELLED
ESCALATED
TIMED_OUT
ABORTED
```

---

# 7. REQUESTED

A task has been requested but has not yet passed runtime authorization.

The runtime must not execute arbitrary requested work.

---

# 8. AUTHORIZED

The runtime has verified:

```text
agent authority
input availability
required object state
dependency availability
execution policy
```

Authorization must occur before execution.

---

# 9. READY

All known prerequisites are satisfied.

A task may enter READY only when:

```text
required inputs exist
required versions are available
dependencies are satisfied
no blocking conflict exists
```

---

# 10. SCHEDULED

The runtime has assigned execution according to dependency and resource rules.

Scheduling must preserve semantic dependency order.

---

# 11. RUNNING

The agent is actively executing.

Runtime observability should preserve:

```text
start
agent
task
input versions
execution context
```

---

# 12. VALIDATING

The task has produced a candidate result and required validation is occurring.

This distinction is important:

```text
EXECUTED
≠
VALIDATED
```

---

# 13. COMPLETED

The task has completed and its output has passed the required runtime completion conditions.

Completion does not automatically mean:

```text
strategically correct
```

That remains the responsibility of evaluation.

---

# 14. Runtime Failure States

The runtime should distinguish:

```text
FAILED
BLOCKED
CANCELLED
ESCALATED
TIMED_OUT
ABORTED
```

These states have different meanings.

---

# 15. FAILED

Execution encountered an execution-level error.

Examples:

```text
agent exception
service failure
invalid runtime response
resource failure
```

---

# 16. BLOCKED

Execution was intentionally prevented because a governing condition was violated.

Examples:

```text
authority failure
hard constraint failure
invalid object state
missing required evidence
```

---

# 17. CANCELLED

Execution was explicitly cancelled before completion.

The cancellation reason must be recorded.

---

# 18. ESCALATED

Execution cannot safely continue without an authority or review decision.

---

# 19. TIMED_OUT

Execution exceeded its permitted execution window.

Timeout does not automatically imply that the underlying decision was invalid.

---

# 20. ABORTED

Execution was deliberately terminated because continued execution was not acceptable.

Examples:

```text
unsatisfiable requirement
recovery exhaustion
critical governance violation
system safety boundary
```

---

# 21. Dependency Scheduling

The runtime should construct execution dependencies from semantic object relationships.

Example:

```text
Intent
  ↓
Evidence
  ↓
Asset Strategy
  ↓
Narrative
  ↓
Channel Projection
  ↓
Prompt Compilation
  ↓
Generation
```

A downstream task should not execute before required upstream objects are ready.

---

# 22. Dependency Readiness

A task is READY only if all mandatory dependencies satisfy their consumability requirements.

Conceptually:

```text
DEPENDENCY
   ↓
STATE
AUTHORITY
VERSION
VALIDITY
PROVENANCE
   ↓
CONSUMABLE?
```

If not:

```text
WAIT
REPLAN
BLOCK
or
ESCALATE
```

---

# 23. Dependency Graph

The runtime should support a directed dependency graph.

Conceptually:

```text
NODE = EXECUTION TASK
EDGE = REQUIRED DEPENDENCY
```

The graph must be acyclic for dependency scheduling unless an explicit iterative execution construct is introduced.

---

# 24. Cyclic Dependency

If:

```text
A → B
B → C
C → A
```

exists without an explicit iterative contract, the runtime must reject or escalate the graph.

It must not enter an uncontrolled execution loop.

---

# 25. Parallel Execution

Independent tasks may execute concurrently.

Example:

```text
Evidence A ──┐
Evidence B ──┼→ Asset Strategy
Evidence C ──┘
```

provided:

```text
no semantic conflict
no shared mutable state conflict
no ordering requirement
```

exists.

---

# 26. Sequential Execution

Tasks must execute sequentially when:

```text
B depends on A
```

or:

```text
A establishes an authority / state required by B
```

The runtime must not trade semantic correctness for parallelism.

---

# 27. Concurrency Control

When multiple agents attempt to modify related objects, the runtime must enforce:

```text
ownership
version checks
locks
transaction boundaries
```

to prevent lost updates or unauthorized mutation.

---

# 28. Optimistic Concurrency

Where appropriate, the runtime may use version checks:

```text
READ v4
 ↓
PROCESS
 ↓
WRITE
 ↓
CHECK CURRENT VERSION
```

If current version ≠ expected version:

```text
STALE WRITE
→ REJECT / REPLAN
```

Exact implementation remains deferred.

---

# 29. Pessimistic Concurrency

Where semantic risk requires exclusive access, the runtime may use locks.

However:

```text
runtime lock
≠
semantic authority
```

A runtime lock only controls concurrent execution.

It does not grant permission to modify the object.

---

# 30. Transaction Boundary

A consequential runtime operation should define its transaction boundary.

Potentially:

```text
READ INPUTS
→ EXECUTE
→ VALIDATE RESULT
→ COMMIT
```

If validation fails:

```text
DO NOT COMMIT
```

unless the failure is explicitly recorded as a candidate state.

---

# 31. Atomicity

Where practical, semantic state transitions should be atomic.

Example:

```text
OBJECT v4
 ↓
REVISION REQUEST
 ↓
VALIDATE
 ↓
COMMIT v5
```

The system must avoid exposing partially committed semantic state.

---

# 32. Runtime State vs Semantic State

These must remain separate.

### Runtime state

```text
RUNNING
WAITING
QUEUED
FAILED
```

### Semantic object state

```text
DRAFT
VALID
APPROVED
LOCKED
INVALIDATED
```

A task being RUNNING does not mean its output is VALID.

---

# 33. Agent Invocation

Before invoking an agent, the runtime should verify:

```text
agent exists
agent version
authority scope
required inputs
input versions
task type
execution policy
```

The runtime should reject invalid invocations before execution where possible.

---

# 34. Agent Versioning

Agent execution should preserve:

```text
agent_id
agent_version
prompt / policy version
tool version where relevant
```

This allows behavioral changes to be attributed.

---

# 35. Input Version Pinning

An execution should record the exact versions of semantic objects it consumed.

Example:

```text
Intent v3
Evidence v7
Asset Strategy v2
```

The agent should not silently consume newer versions during the same execution unless explicitly designed to do so.

---

# 36. Output Commit

Agent outputs should enter the semantic object lifecycle through a controlled commit path.

```text
AGENT OUTPUT
      ↓
SCHEMA VALIDATION
      ↓
AUTHORITY CHECK
      ↓
PROVENANCE
      ↓
LIFECYCLE TRANSITION
      ↓
COMMIT
```

Raw agent output must not automatically become authoritative state.

---

# 37. Runtime Admission Control

Before accepting an output, the runtime should verify:

```text
schema
required fields
authority
provenance
version
state transition
dependency integrity
```

If any mandatory condition fails:

```text
REJECT
BLOCK
or
ESCALATE
```

---

# 38. Retry Policy

Retries must distinguish:

```text
TRANSIENT EXECUTION FAILURE
```

from:

```text
SEMANTIC FAILURE
```

Transient failure may justify retry.

Semantic failure should normally trigger:

```text
EVALUATION
REPLAN
or
ESCALATION
```

Blind retries are prohibited as a general recovery strategy.

---

# 39. Retry Budget

Each execution should have bounded:

```text
max retries
time budget
cost budget
```

Exact values remain runtime configuration.

---

# 40. Retry Idempotency

Retries must account for side effects.

Where possible, execution tasks should be idempotent.

For non-idempotent actions, the runtime should preserve:

```text
execution identity
side-effect status
commit status
```

to prevent duplicate execution.

---

# 41. Determinism

The runtime should maximize deterministic behavior for:

```text
scheduling
state transitions
authority checks
dependency resolution
validation
```

Generation may remain stochastic.

The system should distinguish:

```text
deterministic orchestration
```

from:

```text
stochastic generation
```

---

# 42. Randomness Recording

When stochastic components materially affect output, the runtime should preserve available reproducibility information such as:

```text
seed
model version
parameters
input versions
prompt version
```

where supported.

---

# 43. Execution Context

Every task should have a bounded execution context containing only the information required for that task.

Conceptually:

```text
TASK
 ↓
AUTHORIZED CONTEXT
 ↓
INPUT OBJECTS
 ↓
TOOLS
 ↓
POLICIES
```

Agents should not automatically receive unrestricted global campaign state.

---

# 44. Context Isolation

Context isolation reduces:

```text
accidental leakage
cross-domain contamination
prompt contamination
unauthorized access
stale knowledge consumption
```

The runtime should prefer explicit inputs over hidden global context.

---

# 45. Tool Access

Tool permissions should be scoped by agent and task.

Example:

```text
Knowledge Agent
→ retrieval tools

Prompt Compiler
→ compilation tools

Evaluator
→ evaluation tools
```

An agent should not automatically receive every available tool.

---

# 46. Runtime Authority Enforcement

The runtime is responsible for enforcing authority contracts.

It must not rely solely on agent self-restraint.

```text
AGENT CLAIMS:
"I am allowed to modify X."

RUNTIME:
VERIFY.
```

---

# 47. Governance Boundary

II-013 defines:

```text
WHO MAY DECIDE
```

II-015 defines:

```text
HOW THAT AUTHORITY IS ENFORCED DURING EXECUTION
```

Therefore:

```text
GOVERNANCE
→ semantic permission

RUNTIME
→ execution enforcement
```

---

# 48. Evaluation Boundary

After a consequential task:

```text
EXECUTE
 ↓
OUTPUT
 ↓
EVALUATION
```

The runtime must not interpret successful execution as successful intelligence.

---

# 49. Failure Routing

Runtime failures should route according to type:

```text
TRANSIENT FAILURE
→ RETRY

SEMANTIC FAILURE
→ EVALUATE / REPLAN

AUTHORITY FAILURE
→ BLOCK / ESCALATE

DEPENDENCY FAILURE
→ WAIT / REPLAN

RESOURCE FAILURE
→ RETRY / ESCALATE

UNSATISFIABLE FAILURE
→ ABORT
```

The exact policy is configurable.

---

# 50. Event Model

Runtime events should preserve:

```text
event_id
execution_id
task_id
event_type
agent
object references
versions
state transition
timestamp
result
error
provenance
```

Events become part of operational and semantic audit.

---

# 51. Observability

The runtime should expose at least:

```text
task status
execution duration
dependency state
agent execution
failure state
retry count
evaluation state
recovery state
```

Observability must not require exposing sensitive internal reasoning traces.

---

# 52. Metrics

Potential runtime metrics:

```text
TASK SUCCESS RATE
TASK FAILURE RATE
BLOCK RATE
RETRY RATE
TIMEOUT RATE
ESCALATION RATE
AVERAGE EXECUTION TIME
QUEUE WAIT TIME
DEPENDENCY WAIT TIME
STALE INPUT RATE
STALE WRITE RATE
EVALUATION REJECTION RATE
RECOVERY RATE
```

These remain diagnostic metrics.

---

# 53. Runtime Logging

Logs should preserve operational facts:

```text
what executed
when
which agent
which version
which inputs
which result
which error
```

Logs should not be treated as a substitute for semantic provenance.

---

# 54. Runtime Trace

A complete execution trace should connect:

```text
EXECUTION
 ↓
TASK
 ↓
AGENT
 ↓
INPUT OBJECT VERSIONS
 ↓
OUTPUT OBJECT VERSION
 ↓
EVALUATION
 ↓
STATE TRANSITION
```

This creates operational lineage compatible with II-012.

---

# 55. Cancellation

Tasks should support controlled cancellation.

Cancellation should preserve:

```text
who cancelled
why
when
task state
partial effects
```

A cancelled task should not be incorrectly recorded as successful.

---

# 56. Timeout Recovery

Timeout handling should distinguish:

```text
execution still potentially active
```

from:

```text
execution definitively failed
```

The runtime must avoid duplicate execution when the external system may still be processing the original task.

---

# 57. Backpressure

If downstream systems cannot keep up, the runtime should support controlled backpressure.

The objective is to prevent:

```text
unbounded queue growth
```

or:

```text
uncontrolled generation
```

Exact queue architecture remains deferred.

---

# 58. Resource Governance

Runtime execution should respect:

```text
compute budget
model-call budget
retrieval budget
generation budget
time budget
concurrency limits
```

Resource limits must not silently weaken hard semantic requirements.

---

# 59. Priority

Tasks may have priority based on:

```text
criticality
dependency centrality
deadline
user request
recovery urgency
```

Priority must not override authority or semantic dependencies.

---

# 60. Scheduling Fairness

Where multiple independent tasks compete for resources, the runtime should avoid indefinite starvation.

Exact scheduling algorithm is deferred.

---

# 61. Runtime and Replanning

Replanning creates new execution tasks.

```text
FAILURE
 ↓
RECOVERY PLAN
 ↓
NEW TASK GRAPH
 ↓
SCHEDULE
```

The runtime executes the new plan but does not invent the recovery strategy.

---

# 62. Runtime and Lifecycle

The runtime must enforce lifecycle transitions defined by II-014.

Example:

```text
Agent output
 ↓
DRAFT
 ↓
VALIDATING
 ↓
VALID
```

The runtime must not skip:

```text
VALIDATING
```

when that state is required for the object type.

---

# 63. Runtime and Provenance

Every consequential execution must contribute to provenance:

```text
execution
 ↓
inputs
 ↓
agent
 ↓
output
 ↓
evaluation
```

This is required for auditability.

---

# 64. Runtime and Governance

The runtime must enforce:

```text
agent authority
object ownership
delegation
locks
approval requirements
```

as defined by II-013.

---

# 65. Runtime and Self-Critique

The runtime should schedule self-critique as an explicit task.

It must not treat:

```text
generator output
```

as equivalent to:

```text
critic output
```

The two remain separate execution roles.

---

# 66. Runtime and Adversarial Verification

Adversarial verification should execute as an explicit governed task.

Conceptually:

```text
CANDIDATE
 ↓
EVALUATION
 ↓
ADVERSARIAL VERIFICATION
 ↓
ACCEPT / CHALLENGE / BLOCK
```

The runtime should ensure adversarial verification cannot silently mutate the target.

---

# 67. Execution Safety Boundary

The runtime must reject or escalate when:

```text
authority cannot be established
required object version is unavailable
critical dependency is invalid
locked object would be modified
required evaluation cannot run
recovery budget is exhausted
execution graph is invalid
```

---

# 68. Runtime State Machine Integrity

The runtime should detect impossible states such as:

```text
COMPLETED
while
required evaluation = FAILED
```

or:

```text
AUTHORIZED
while
authority = REVOKED
```

or:

```text
RUNNING
while
task = CANCELLED
```

These become runtime integrity violations.

---

# 69. Execution Replay

The architecture should eventually support replay for debugging and evaluation.

Replay should use:

```text
input versions
agent version
policy version
runtime version
execution parameters
recorded events
```

Exact deterministic replay is not guaranteed for stochastic models.

---

# 70. Execution Reproducibility

The runtime should distinguish:

```text
EXACT REPLAY
```

from:

```text
CONDITIONAL REPRODUCTION
```

For stochastic generation, the objective may be reproducibility of conditions rather than identical output.

---

# 71. Runtime Regression

Runtime changes should be evaluated against:

```text
dependency scheduling cases
authority cases
state transition cases
failure cases
retry cases
concurrency cases
stale-version cases
```

A faster runtime that violates semantic contracts is a regression.

---

# 72. Runtime Proof Surface

II-015 creates measurable architecture-level claims:

```text
Does the runtime enforce authority?
Does it preserve object versions?
Does it prevent invalid transitions?
Does it respect dependencies?
Does it avoid stale writes?
Does it bound retries?
Does it preserve audit lineage?
Does it separate execution success from semantic success?
```

These are testable properties.

---

# 73. Self-Critique Requirements

The Self-Critique Agent should inspect runtime execution for:

- authority bypass,
- incorrect scheduling,
- stale input consumption,
- invalid state transitions,
- hidden retries,
- unbounded loops,
- improper context access,
- evaluation bypass,
- generation/intelligence boundary violations,
- and unexplained execution outcomes.

---

# 74. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to:

1. Execute an unauthorized task.
2. Consume an invalid object.
3. Consume a stale object.
4. Write against an outdated version.
5. Skip required evaluation.
6. Skip lifecycle validation.
7. Bypass a lock.
8. Exploit retry logic to create infinite execution.
9. Duplicate non-idempotent execution.
10. Create dependency cycles.
11. Cause starvation.
12. Inject unauthorized context.
13. Cause one agent to access another agent's tools.
14. Forge execution completion.
15. Hide a failed task as successful.
16. Cause runtime execution to mutate semantic meaning.
17. Bypass adversarial verification.
18. Create inconsistent runtime and semantic states.

Expected behavior:

```text
ATTACK
    ↓
DETECT
    ↓
BLOCK / CHALLENGE
    ↓
RECORD
```

---

# 75. Validation Invariants

### Invariant 1

Runtime execution cannot create semantic authority by itself.

### Invariant 2

Every consequential task has an authorization context.

### Invariant 3

Input object versions are explicit.

### Invariant 4

Required dependencies must be satisfied before execution.

### Invariant 5

Runtime state and semantic object state remain distinct.

### Invariant 6

Successful execution does not imply semantic correctness.

### Invariant 7

Required evaluation cannot be silently skipped.

### Invariant 8

Locked objects cannot be silently mutated.

### Invariant 9

Stale writes are rejected or explicitly reconciled.

### Invariant 10

Retries are bounded.

### Invariant 11

Semantic failures are not treated as transient execution failures.

### Invariant 12

Dependency cycles are detected.

### Invariant 13

Agent tool access is scoped.

### Invariant 14

Execution context is bounded.

### Invariant 15

Every consequential execution contributes to provenance.

### Invariant 16

Runtime failures preserve their actual failure state.

### Invariant 17

Cancellation and timeout do not become false success.

### Invariant 18

Recovery execution remains separate from recovery strategy.

### Invariant 19

Adversarial verification cannot silently mutate the system under test.

### Invariant 20

Runtime changes remain subject to regression evaluation.

---

# 76. Falsifiable Architectural Hypotheses

## Hypothesis A — Runtime authority enforcement reduces unauthorized decisions

**Experiment:**

Inject unauthorized task requests.

Compare:

```text
agent self-restraint
vs
runtime-enforced authority
```

Measure unauthorized execution rate.

---

## Hypothesis B — Version pinning reduces stale execution

**Experiment:**

Modify upstream objects while tasks are queued.

Compare:

```text
unpinned inputs
vs
version-pinned execution
```

Measure stale consumption and stale writes.

---

## Hypothesis C — Dependency-aware scheduling reduces invalid execution

**Experiment:**

Create tasks with controlled dependency failures.

Measure whether downstream execution is correctly prevented.

---

## Hypothesis D — Typed failure routing reduces inappropriate retries

**Experiment:**

Inject:

```text
transient failures
semantic failures
authority failures
```

Measure whether each enters the correct recovery path.

---

## Hypothesis E — Runtime / generation separation reduces strategic mutation

**Experiment:**

Introduce generation failures.

Compare systems where the generation runtime can modify upstream semantic objects against systems where it cannot.

Measure strategic drift.

---

## Hypothesis F — Runtime lineage improves incident reconstruction

**Experiment:**

Compare:

```text
runtime logs only
vs
runtime trace + semantic lineage
```

Measure incident reconstruction accuracy.

---

# 77. Runtime Test Corpus

The architecture should eventually maintain:

```text
NORMAL EXECUTION
DEPENDENCY WAIT
DEPENDENCY FAILURE
PARALLEL EXECUTION
CONCURRENCY CONFLICT
STALE WRITE
AUTHORITY FAILURE
LOCK VIOLATION
RETRY
TIMEOUT
CANCELLATION
ESCALATION
ABORT
CYCLE DETECTION
RESOURCE EXHAUSTION
CONTEXT VIOLATION
TOOL VIOLATION
EVALUATION FAILURE
ADVERSARIAL ATTACK
RECOVERY EXECUTION
```

Each case should define:

```text
initial state
execution graph
expected runtime behavior
expected semantic state
expected audit events
terminal state
```

---

# 78. Core Contract

> **The Intelligence Runtime shall execute governed intelligence tasks through explicit authorization, dependency-aware scheduling, version-pinned inputs, controlled state transitions, bounded retries, scoped context and tools, observable execution, and traceable provenance. It shall remain separate from the generation runtime, distinguish execution success from semantic correctness, enforce lifecycle and governance contracts, detect stale and unauthorized operations, support evaluation and recovery as explicit tasks, and expose runtime behavior to self-critique, adversarial verification, and regression testing.**

---

# 79. Deferred Decisions

II-015 does not freeze:

- orchestration framework,
- workflow engine,
- message bus,
- queue implementation,
- database,
- distributed execution architecture,
- concurrency mechanism,
- retry library,
- scheduling algorithm,
- container/runtime technology,
- observability stack,
- exact API contracts,
- worker topology.

These remain engineering implementation decisions.

---

# 80. Exit Criteria

II-015 is semantically complete when:

- [x] Runtime purpose established
- [x] Intelligence / generation runtime boundary established
- [x] Execution unit established
- [x] Execution lifecycle established
- [x] Runtime failure states established
- [x] Authorization state established
- [x] Dependency scheduling established
- [x] Dependency readiness established
- [x] Dependency graph established
- [x] Cycle detection established
- [x] Parallel execution established
- [x] Sequential execution established
- [x] Concurrency controls established
- [x] Transaction boundary established
- [x] Atomicity principle established
- [x] Runtime / semantic state distinction established
- [x] Agent invocation requirements established
- [x] Agent versioning established
- [x] Input version pinning established
- [x] Output commit path established
- [x] Runtime admission control established
- [x] Retry semantics established
- [x] Retry budget established
- [x] Idempotency established
- [x] Determinism principles established
- [x] Context isolation established
- [x] Tool access governance established
- [x] Runtime authority enforcement established
- [x] Failure routing established
- [x] Event model established
- [x] Observability established
- [x] Runtime metrics established
- [x] Cancellation established
- [x] Timeout semantics established
- [x] Backpressure established
- [x] Resource governance established
- [x] Priority / fairness established
- [x] Replanning integration established
- [x] Lifecycle integration established
- [x] Provenance integration established
- [x] Self-critique integration established
- [x] Adversarial verification integration established
- [x] Runtime safety boundary established
- [x] Replay / reproducibility principles established
- [x] Runtime regression established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Runtime test corpus established
- [x] Architecture-proof role established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-016 — Validation, Benchmarking & Architectural Evidence Contract**

This specification will define how the architecture is empirically tested and how evidence is collected to support or falsify claims about intelligence quality, object authority, evaluation reliability, multi-agent governance, recovery, provenance, lifecycle integrity, and runtime correctness.
