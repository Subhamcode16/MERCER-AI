# III-008 — Decision, Planning & Execution Intent Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001 through III-007 and the ratified Phase II semantic architecture  
**Purpose:** Define the machine-readable contract for representing goals, intents, candidate actions, decisions, planning, execution binding, uncertainty, risk, approval, abstention, escalation, counterfactual alternatives, and outcome provenance.

---

# 1. Purpose

III-008 defines the semantic boundary between wanting something to happen, deciding that it should happen, executing the decision, and observing the resulting outcome.

The central boundary is:

```text
INTENT
    ≠
DECISION
    ≠
EXECUTION
    ≠
OUTCOME
```

This separation prevents an agent's generated plan from silently becoming an authorized action.

The contract answers:

```text
WHAT IS THE SYSTEM TRYING TO ACHIEVE?
WHAT ACTION IS BEING PROPOSED?
WHICH ACTION WAS ACTUALLY DECIDED?
WHO / WHAT AUTHORIZED IT?
WHAT CONSTRAINTS APPLY?
WHAT EVIDENCE SUPPORTS IT?
WHAT UNCERTAINTY EXISTS?
WHAT WAS EXECUTED?
WHAT ACTUALLY HAPPENED?
```

---

# 2. Goal

A goal describes a desired state or objective.

Conceptually:

```yaml
goal:
  goal_id: GOAL-...
  description: ...
  success_conditions: []
  scope: ...
  priority: ...
```

A goal does not itself specify an authorized action.

Therefore:

```text
GOAL
≠
ACTION
```

---

# 3. Goal Identity

Every consequential goal should have a stable identity.

Recommended conceptual form:

```text
GOAL-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

---

# 4. Goal Version

A material change to a goal should create a new goal version.

For example:

```text
GOAL v1
 ↓
goal refinement
 ↓
GOAL v2
```

Historical goal versions must remain reconstructable.

---

# 5. Intent

Intent represents a proposed direction for achieving a goal.

Conceptually:

```text
GOAL
 ↓
INTENT
```

An intent may specify:

```text
desired operation
target object
candidate approach
expected effect
```

An intent is not automatically a decision.

---

# 6. Intent Identity

Every consequential intent should receive a unique identifier.

Recommended conceptual form:

```text
INT-<ULID>
```

The intent must reference the goal or request that produced it where applicable.

---

# 7. Intent Status

Possible conceptual states include:

```text
PROPOSED
UNDER_REVIEW
ACCEPTED
REJECTED
SUPERSEDED
WITHDRAWN
```

These statuses are distinct from the governed object lifecycle states in III-003.

---

# 8. Requested Operation

An intent must identify the operation it proposes.

Conceptually:

```yaml
operation:
  operation_id: ...
  operation_type: ...
  target_refs: []
```

The operation must be typed.

Avoid relying solely on natural-language descriptions for consequential actions.

---

# 9. Candidate Action

Planning may produce multiple candidate actions.

Conceptually:

```text
GOAL
 ↓
CANDIDATE A
CANDIDATE B
CANDIDATE C
```

Each candidate should preserve:

```text
action identity
expected effect
required authority
required capabilities
constraints
dependencies
risk
uncertainty
```

---

# 10. Planning

Planning is the process of constructing candidate action sequences or strategies for achieving a goal.

Planning may involve:

```text
decomposition
sequencing
dependency resolution
resource allocation
risk analysis
counterfactual generation
```

Planning output is still a proposal until the decision contract accepts it.

---

# 11. Plan Identity

A plan should receive an explicit identity.

Recommended conceptual form:

```text
PLN-<ULID>
```

A plan may contain:

```text
steps
dependencies
candidate actions
preconditions
postconditions
expected outcomes
```

---

# 12. Plan Version

Material plan changes must be versioned.

Do not silently mutate a plan after it has become part of a consequential decision record.

---

# 13. Plan vs Decision

A plan describes:

```text
HOW SOMETHING COULD BE DONE
```

A decision establishes:

```text
WHAT WILL BE DONE
```

Therefore:

```text
PLAN
≠
DECISION
```

---

# 14. Decision

A decision is an explicit selection or determination made under the applicable authority, evidence, constraints, and lifecycle conditions.

Conceptually:

```yaml
decision:
  decision_id: DEC-...
  decision_type: ...
  target_refs: []
  selected_action: ...
  authority_refs: []
  evidence_refs: []
  constraint_refs: []
  status: ...
```

---

# 15. Decision Identity

Every consequential decision must have a stable identifier.

Recommended conceptual form:

```text
DEC-<ULID>
```

The decision identifier must not change when its downstream execution begins.

---

# 16. Decision Type

Decisions must be typed.

Examples:

```text
SELECT
APPROVE
REJECT
COMMIT
EXECUTE
ESCALATE
ABSTAIN
INVALIDATE
SUPERSEDE
```

The definitive decision registry must remain aligned with III-002 and III-003.

---

# 17. Decision Authority

A decision requires the applicable authority.

The decision layer must query III-002 rather than independently determining authority.

Conceptually:

```text
DECISION REQUEST
 ↓
AUTHORITY RESOLUTION
 ↓
DECISION ELIGIBILITY
```

---

# 18. Decision Preconditions

Before committing a consequential decision, the runtime should resolve:

```text
authority
constraints
lifecycle state
required evidence
dependencies
object version
input validity
```

---

# 19. Decision Postconditions

A committed decision should produce:

```text
decision record
provenance event
authority reference
evidence references
selected action
applicable constraints
decision status
```

---

# 20. Decision Status

Conceptually:

```text
PROPOSED
UNDER_REVIEW
AUTHORIZED
COMMITTED
REJECTED
ABSTAINED
ESCALATED
SUPERSEDED
EXECUTED
FAILED
```

The final status model must distinguish decision status from execution status.

---

# 21. Decision vs Execution

A committed decision does not prove that execution occurred.

Therefore:

```text
DECISION COMMITTED
≠
ACTION EXECUTED
```

Execution requires a separate execution record.

---

# 22. Execution Intent

An execution intent is the explicit binding between a committed decision and an execution request.

Conceptually:

```text
DECISION
 ↓
EXECUTION INTENT
 ↓
EXECUTION
```

This prevents the runtime from treating every plan or model output as executable.

---

# 23. Execution Intent Identity

Recommended conceptual form:

```text
EXI-<ULID>
```

The execution intent should reference:

```text
decision
selected action
target versions
authority
constraints
plan version
```

---

# 24. Execution Eligibility

Execution should require:

```text
VALID DECISION
+
VALID AUTHORITY
+
VALID TARGET
+
VALID LIFECYCLE
+
CONSTRAINT PASS
+
REQUIRED DEPENDENCIES
=
EXECUTION ELIGIBLE
```

---

# 25. Execution Binding

Once an execution intent is bound, it should identify the exact target versions where semantic correctness depends on version identity.

Example:

```text
TARGET OBJECT v3
```

must not silently execute against:

```text
TARGET OBJECT v4
```

unless an explicit compatibility rule permits it.

---

# 26. Plan Drift

If the plan changes after decision commitment:

```text
PLAN v1
 ↓
PLAN v2
```

the system must determine whether the change is material.

A material change should require:

```text
re-evaluation
```

and potentially:

```text
new decision
```

It must not silently execute a materially different plan under an old decision.

---

# 27. Decision Drift

Decision drift occurs when execution materially differs from the committed decision.

Examples:

```text
different target
different operation
different authority scope
different constraints
different material parameters
```

The runtime should detect or prevent such drift.

---

# 28. Execution Outcome

Execution outcome represents what actually occurred.

Conceptually:

```yaml
outcome:
  outcome_id: OUT-...
  execution_id: ...
  status: ...
  outputs: []
  evidence_refs: []
  observed_effects: []
```

Outcome is evidence about execution, not proof that the original decision was correct.

---

# 29. Outcome Status

Possible conceptual states:

```text
SUCCESS
PARTIAL_SUCCESS
FAILED
TIMEOUT
ABORTED
UNKNOWN
```

Exact semantics remain implementation-specific.

---

# 30. Expected vs Observed Outcome

The decision should preserve:

```text
EXPECTED OUTCOME
```

while execution produces:

```text
OBSERVED OUTCOME
```

The two must remain distinguishable.

---

# 31. Outcome Evaluation

After execution:

```text
EXPECTED
vs
OBSERVED
```

may be evaluated.

This can produce:

```text
goal achieved
goal partially achieved
goal failed
unexpected side effect
```

The evaluation must remain a separate record.

---

# 32. Uncertainty

A decision may involve uncertainty.

Uncertainty should be represented explicitly where material.

Conceptually:

```yaml
uncertainty:
  sources: []
  assumptions: []
  unknowns: []
  confidence: ...
```

Confidence must not substitute for evidence or authority.

---

# 33. Confidence Boundary

The architecture must preserve:

```text
CONFIDENCE
≠
AUTHORITY
≠
TRUTH
```

A highly confident agent cannot authorize an action merely because it is confident.

---

# 34. Assumptions

Material assumptions used in planning or decision-making should be explicit.

Examples:

```text
assumed object state
assumed source freshness
assumed dependency availability
assumed user preference
assumed tool behavior
```

Hidden assumptions are a major source of decision failure.

---

# 35. Assumption Provenance

Where an assumption materially affects a decision, preserve:

```text
assumption
source
actor
timestamp
confidence / status
```

---

# 36. Risk

Consequential decisions should preserve risk information where applicable.

Conceptually:

```yaml
risk:
  risk_id: RSK-...
  category: ...
  likelihood: ...
  impact: ...
  mitigations: []
```

The exact risk taxonomy is domain-specific.

---

# 37. Risk vs Constraint

Risk describes:

```text
WHAT COULD GO WRONG
```

A constraint describes:

```text
WHAT MUST / MUST NOT HAPPEN
```

Therefore:

```text
HIGH RISK
```

does not automatically mean:

```text
PROHIBITED
```

unless a policy explicitly establishes that rule.

---

# 38. Candidate Comparison

When multiple actions are available, the decision record should preserve the candidate set where material.

Conceptually:

```text
CANDIDATE A
CANDIDATE B
CANDIDATE C
      ↓
COMPARISON
      ↓
SELECTED CANDIDATE
```

This enables later analysis of:

```text
why A was selected instead of B
```

---

# 39. Counterfactual Alternatives

For consequential decisions, the system may preserve rejected alternatives.

This is especially useful for:

```text
high-impact decisions
risk analysis
adversarial review
post-hoc investigation
```

A rejected alternative must not be represented as if it was executed.

---

# 40. Decision Rationale

A decision should preserve the decision basis.

This may include:

```text
evidence
constraints
risk
candidate comparison
authority
objective
```

A generated explanation must not replace the underlying decision provenance.

---

# 41. Decision Rationale vs Post-Hoc Explanation

The system must distinguish:

```text
DECISION INPUTS / BASIS
```

from:

```text
EXPLANATION GENERATED AFTER THE DECISION
```

A post-hoc explanation can be evidence or commentary but cannot silently become the authoritative causal record.

---

# 42. Abstention

A decision-maker may abstain when:

```text
evidence is insufficient
authority is unclear
constraints conflict
uncertainty exceeds permitted threshold
target state is unknown
required verification is unavailable
```

Abstention is a valid decision outcome.

---

# 43. Escalation

Escalation transfers the decision requirement to an appropriate higher-level process.

It should preserve:

```text
reason
blocking issue
required authority
missing evidence
risk
candidate actions
```

Escalation does not itself approve an action.

---

# 44. Approval

Approval is a decision type with explicit authority requirements.

Therefore:

```text
PROPOSED
→ APPROVAL REQUEST
→ AUTHORITY CHECK
→ APPROVAL DECISION
```

Approval must not be inferred from:

```text
absence of rejection
successful planning
model confidence
```

unless explicitly defined.

---

# 45. Execution Authorization

Execution authorization should be explicit where required.

Conceptually:

```text
DECISION
+
EXECUTION AUTHORITY
+
CONSTRAINT PASS
=
EXECUTION ELIGIBLE
```

---

# 46. Execution Start

Starting execution creates an execution record.

Conceptually:

```text
EXE-<ULID>
```

The execution record should reference:

```text
execution intent
decision
agent
agent version
target
plan
authority
constraints
```

---

# 47. Execution Cancellation

Cancellation should preserve:

```text
who cancelled
authority
reason
execution state
partial effects
timestamp
```

Cancellation does not erase prior execution events.

---

# 48. Partial Execution

An execution may partially complete.

The runtime must preserve:

```text
completed actions
uncompleted actions
observed effects
remaining actions
```

Do not collapse:

```text
PARTIAL
```

into:

```text
SUCCESS
```

without an explicit evaluation.

---

# 49. Side Effects

Observed side effects should be recorded independently from expected outcomes.

Examples:

```text
unexpected state change
additional resource usage
external system mutation
secondary object creation
```

Side effects may trigger evaluation or lifecycle consequences.

---

# 50. Irreversible Actions

Where an operation is difficult or impossible to reverse, the execution contract should require stronger preconditions where applicable.

Potential requirements:

```text
explicit approval
additional verification
confirmation
risk review
rollback plan
```

The exact policy is domain-specific.

---

# 51. Dry Run

Where supported, a dry-run may estimate execution effects without committing them.

A dry-run result must not be represented as actual execution.

Therefore:

```text
DRY RUN
≠
EXECUTION
```

---

# 52. Simulation

Simulation can produce expected outcomes and risk information.

Simulation must not silently establish:

```text
real-world success
approval
authority
```

---

# 53. Plan Verification

Before consequential execution, the plan may be checked for:

```text
constraint compliance
authority
dependency satisfaction
target validity
risk
expected outcome
```

Plan verification does not itself execute the plan.

---

# 54. Self-Critique Integration

The self-critique mechanism may inspect:

```text
goal
intent
plan
decision
assumptions
risk
selected action
```

It should produce a separate critique record.

Critique does not automatically alter the decision.

---

# 55. Adversarial Verification Integration

The adversarial verifier should attempt to break the decision pipeline.

Potential attacks:

```text
goal ambiguity
unsafe plan
constraint bypass
authority mismatch
stale target
hidden assumption
candidate omission
risk underestimation
execution drift
```

The attacks and results must become provenance records.

---

# 56. Decision Revision

If new evidence materially changes the decision basis:

```text
NEW EVIDENCE
 ↓
RE-EVALUATION
 ↓
DECISION REVISION
```

Do not silently overwrite the previous decision.

Create a new decision version or successor decision as defined by the implementation.

---

# 57. Decision Supersession

A new decision may supersede an old decision.

The system must preserve:

```text
old decision
new decision
reason
evidence
authority
timestamp
```

---

# 58. Decision Rollback

Rollback should be explicit and governed.

It must not simply restore a database value.

A rollback is itself a new decision or lifecycle event with provenance.

---

# 59. Execution Retry

A retry must be distinguishable from the original execution.

Conceptually:

```text
EXECUTION E1
 ↓
FAILURE
 ↓
RETRY
 ↓
EXECUTION E2
```

The relationship must be preserved.

---

# 60. Retry Eligibility

A retry should verify:

```text
decision still valid
authority still valid
target still valid
constraints still pass
dependencies still satisfied
```

A failed execution does not automatically authorize unlimited retries.

---

# 61. Idempotency

Where execution can produce duplicate effects, the runtime should support an idempotency mechanism.

Repeated requests must not silently create unintended duplicate actions.

---

# 62. Decision Context Snapshot

A consequential decision should preserve or deterministically reconstruct:

```text
goal version
intent version
plan version
evidence versions
knowledge versions
constraint versions
authority context
agent version
```

This is necessary for later reconstruction.

---

# 63. Decision Provenance

Every consequential decision must connect to III-004.

Minimum lineage:

```text
GOAL
 ↓
INTENT
 ↓
PLAN / CANDIDATES
 ↓
EVIDENCE
 ↓
CONSTRAINTS
 ↓
AUTHORITY
 ↓
DECISION
 ↓
EXECUTION INTENT
 ↓
EXECUTION
 ↓
OUTCOME
```

---

# 64. Decision Object Concept

Conceptually:

```yaml
decision:
  decision_id: DEC-...
  decision_type: SELECT

  goal_ref: GOAL-...
  intent_ref: INT-...
  plan_ref: PLN-...

  selected_action: ACT-...

  authority_refs:
    - AUTH-...

  evidence_refs:
    - EVD-...

  constraint_refs:
    - CON-...

  assumptions: []
  risks: []
  alternatives: []

  status: COMMITTED

  provenance_ref: PROV-...
```

This is conceptual, not final JSON Schema.

---

# 65. Execution Intent Concept

```yaml
execution_intent:
  execution_intent_id: EXI-...

  decision_ref: DEC-...

  target_refs:
    - object_id: IO-...
      version: ...

  action_ref: ACT-...

  authority_refs:
    - AUTH-...

  constraint_refs:
    - CON-...

  plan_ref: PLN-...

  status: READY

  provenance_ref: PROV-...
```

---

# 66. Outcome Concept

```yaml
outcome:
  outcome_id: OUT-...
  execution_ref: EXE-...
  status: SUCCESS

  expected_outcome_refs: []
  observed_effects: []

  output_refs: []
  evidence_refs: []

  provenance_ref: PROV-...
```

---

# 67. Decision Pipeline

The canonical decision path is:

```text
GOAL
 ↓
INTENT
 ↓
CANDIDATE ACTIONS
 ↓
PLAN
 ↓
EVIDENCE / KNOWLEDGE
 ↓
RISK / UNCERTAINTY
 ↓
CONSTRAINT CHECK
 ↓
AUTHORITY CHECK
 ↓
DECISION
 ↓
EXECUTION INTENT
 ↓
EXECUTION
 ↓
OBSERVED OUTCOME
 ↓
OUTCOME EVALUATION
```

Not every workflow requires every stage, but consequential operations must not skip semantically required stages.

---

# 68. Decision Invariants

### Invariant 1

Goal is distinct from action.

### Invariant 2

Intent is distinct from decision.

### Invariant 3

Plan is distinct from decision.

### Invariant 4

Decision is distinct from execution.

### Invariant 5

Execution is distinct from outcome.

### Invariant 6

Expected outcome is distinct from observed outcome.

### Invariant 7

Authority is explicitly resolved.

### Invariant 8

Constraint evaluation is explicit.

### Invariant 9

Evidence versions remain identifiable.

### Invariant 10

Material assumptions remain explicit.

### Invariant 11

Confidence does not create authority.

### Invariant 12

Risk does not automatically equal prohibition.

### Invariant 13

Abstention is valid.

### Invariant 14

Escalation does not equal approval.

### Invariant 15

Approval is explicit.

### Invariant 16

Execution cannot silently diverge from the committed decision.

### Invariant 17

Material plan changes require re-evaluation.

### Invariant 18

Material decision changes create traceable successor decisions.

### Invariant 19

Retries do not automatically inherit unlimited authority.

### Invariant 20

Historical decisions remain reconstructable.

### Invariant 21

Post-hoc explanations do not replace decision provenance.

### Invariant 22

Dry runs are distinct from execution.

### Invariant 23

Simulation is distinct from real-world outcome.

### Invariant 24

Self-critique does not automatically alter a decision.

### Invariant 25

Adversarial verification actively attempts to falsify the decision path.

### Invariant 26

Implementation must not invent decision semantics.

---

# 69. Required Tests

The reference implementation must test:

```text
goal creation
intent creation
candidate generation
plan versioning
decision authority
decision constraints
decision evidence
decision abstention
decision escalation
approval
execution binding
target version binding
plan drift
decision drift
execution cancellation
partial execution
side effects
irreversible-action gating
dry run
simulation
self-critique
adversarial verification
decision revision
decision supersession
rollback
retry
idempotency
decision context reconstruction
outcome evaluation
```

---

# 70. Falsification Cases

Deliberately attempt:

```text
intent becomes executable without decision
plan becomes executable without authority
approval inferred from silence
execution against stale target
execution after authority expiry
execution after constraint failure
material plan change without re-evaluation
decision overwrite without successor record
retry after authority revocation
duplicate execution
dry-run represented as success
simulation represented as real outcome
post-hoc explanation replaces decision basis
agent self-approves decision
adversary cannot inspect exact decision version
```

---

# 71. Decision Reconstruction Benchmark

Given a consequential execution, an independent evaluator should be able to reconstruct:

```text
original goal
intent
candidate actions
selected plan
evidence
knowledge versions
constraints
authority
decision
execution intent
actual execution
observed outcome
```

The benchmark should classify:

```text
FULL RECONSTRUCTION
PARTIAL RECONSTRUCTION
FAILED RECONSTRUCTION
```

---

# 72. Decision Quality Evaluation

Decision quality should remain multi-dimensional.

Measure independently:

```text
goal alignment
constraint compliance
authority compliance
evidence sufficiency
risk calibration
alternative coverage
decision correctness
execution fidelity
outcome quality
```

Do not collapse these into one score without preserving the underlying measurements.

---

# 73. Decision Robustness

A decision should be stress-tested against:

```text
evidence perturbation
knowledge conflict
constraint changes
authority changes
target-version changes
adversarial attacks
assumption failures
tool failures
```

This helps distinguish:

```text
ROBUST DECISION
```

from:

```text
DECISION THAT PASSES ONE SCENARIO
```

---

# 74. Deferred Decisions

III-008 intentionally does not freeze:

- exact planning algorithm;
- planner architecture;
- search strategy;
- optimization objective;
- exact risk model;
- exact uncertainty representation;
- decision scoring;
- candidate ranking;
- simulation technology;
- execution scheduler;
- retry engine;
- rollback mechanism;
- exact outcome evaluator;
- final decision registry syntax.

These remain engineering decisions unless they change semantic meaning.

---

# 75. Exit Criteria

- [x] Goal identity defined
- [x] Goal version defined
- [x] Intent defined
- [x] Intent identity defined
- [x] Requested operation defined
- [x] Candidate action defined
- [x] Planning defined
- [x] Plan identity defined
- [x] Plan/version boundary defined
- [x] Plan/decision distinction defined
- [x] Decision identity defined
- [x] Decision type defined
- [x] Decision authority defined
- [x] Decision preconditions defined
- [x] Decision postconditions defined
- [x] Decision status defined
- [x] Execution intent defined
- [x] Execution eligibility defined
- [x] Execution binding defined
- [x] Plan drift defined
- [x] Decision drift defined
- [x] Outcome defined
- [x] Expected/observed distinction defined
- [x] Uncertainty defined
- [x] Assumptions defined
- [x] Risk defined
- [x] Candidate comparison defined
- [x] Counterfactual alternatives defined
- [x] Abstention defined
- [x] Escalation defined
- [x] Approval defined
- [x] Execution authorization defined
- [x] Partial execution defined
- [x] Side effects defined
- [x] Irreversible-action boundary defined
- [x] Dry-run and simulation boundaries defined
- [x] Self-critique integration defined
- [x] Adversarial verification integration defined
- [x] Decision revision defined
- [x] Supersession defined
- [x] Rollback defined
- [x] Retry defined
- [x] Idempotency defined
- [x] Decision context reconstruction defined
- [x] Provenance defined
- [x] Decision invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Reconstruction benchmark defined
- [x] Decision robustness defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 76. Next Contract

**III-009 — Evaluation, Self-Critique & Adversarial Verification Contract**

III-009 will formalize the verification layer itself:

```text
evaluation identity
evaluation target
evaluation protocol
criteria
metrics
evidence
self-critique
independent critique
adversarial attack
attack generation
verification independence
failure discovery
regression testing
confidence
uncertainty
pass / fail / inconclusive
evaluator authority
evaluation provenance
```

The central requirement will be:

```text
A SYSTEM MUST NOT CLAIM
THAT IT HAS VERIFIED ITSELF
MERELY BECAUSE IT GENERATED
A SECOND ANSWER ABOUT ITS FIRST ANSWER.
```

Verification must become an explicit, testable architectural process.
