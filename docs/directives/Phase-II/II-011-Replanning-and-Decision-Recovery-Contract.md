# II-011 — Replanning & Decision Recovery Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Recovery, revision, escalation, and controlled replanning after evaluation failure, critique, adversarial findings, knowledge gaps, or constraint conflicts

---

## 1. Purpose

II-011 defines what the intelligence architecture does when the current plan, decision, asset strategy, narrative, projection, or generated output is found to be insufficient, contradictory, uncertain, or invalid.

The Replanning Layer answers:

> **Given new evidence or a detected failure, what is the smallest justified change required to recover the campaign while preserving authoritative constraints and preventing uncontrolled strategic drift?**

The core principle is:

```text
FAILURE
    ↓
DIAGNOSE
    ↓
LOCALIZE
    ↓
RECOVER
    ↓
RE-EVALUATE
```

Replanning is therefore not synonymous with regeneration.

---

# 2. Core Principle

> **A failure should cause the smallest justified change necessary to restore validity, rather than triggering uncontrolled re-generation of the entire campaign.**

Therefore:

```text
FAILURE
≠
START OVER
```

and:

```text
REPLAN
=
DIAGNOSE
+
LOCALIZE
+
MINIMAL CHANGE
+
REVALIDATION
```

---

# 3. Canonical Recovery Chain

```text
CANDIDATE OUTPUT
        ↓
EVALUATION / CRITIQUE / ADVERSARIAL FINDING
        ↓
FAILURE RECORD
        ↓
FAILURE CLASSIFICATION
        ↓
DEPENDENCY LOCALIZATION
        ↓
RECOVERY OPTIONS
        ↓
IMPACT ANALYSIS
        ↓
REPLAN
        ↓
RE-GENERATE / RE-EVALUATE
        ↓
ACCEPT / ESCALATE / ABORT
```

The recovery process must preserve lineage between the original plan and the revised plan.

---

# 4. Failure Definition

A failure is any condition in which the current state cannot reliably satisfy its governing requirements.

Potential failure sources include:

```text
EVALUATION FAILURE
SELF-CRITIQUE FINDING
ADVERSARIAL FINDING
KNOWLEDGE GAP
AUTHORITY CONFLICT
EVIDENCE INSUFFICIENCY
CONSTRAINT CONFLICT
ASSET GAP
NARRATIVE FAILURE
CHANNEL FAILURE
GENERATION FAILURE
TECHNICAL FAILURE
```

The system must preserve the original source of the failure.

---

# 5. Failure vs Observation

Not every negative observation is a failure.

Example:

```text
Observation:
Lighting is slightly cooler than preferred.

Status:
SOFT DEVIATION
```

versus:

```text
Observation:
Required material evidence is not visible.

Status:
CRITICAL FAILURE
```

The recovery engine must classify severity before deciding what to change.

---

# 6. Failure Severity

Conceptually:

```text
INFO
MINOR
MODERATE
HIGH
CRITICAL
BLOCKING
```

Severity should depend on:

```text
requirement criticality
authority
impact
recoverability
downstream dependency
```

Severity must not be inferred solely from the evaluator's confidence.

---

# 7. Failure Classes

Potential classes include:

```text
REQUIREMENT_FAILURE
EVIDENCE_FAILURE
CONSTRAINT_FAILURE
AUTHORITY_FAILURE
KNOWLEDGE_FAILURE
ASSET_FAILURE
NARRATIVE_FAILURE
CHANNEL_FAILURE
GENERATION_FAILURE
EVALUATION_FAILURE
SYSTEM_FAILURE
```

The taxonomy remains extensible.

---

# 8. Failure Localization

The recovery engine should identify the earliest invalid state in the dependency chain.

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
Generation
```

If the failure is actually:

```text
Incorrect Intent
```

regenerating the image is not a valid recovery.

The system must attempt to localize:

> **Where did the first unjustified or invalid decision enter the chain?**

---

# 9. Root Cause vs Symptom

The system must distinguish:

```text
SYMPTOM
```

from:

```text
ROOT CAUSE
```

Example:

```text
Symptom:
Generated image does not show craftsmanship.

Possible root cause:
Evidence Requirement was underspecified.

Alternative root cause:
Asset Strategy selected an unsuitable asset form.

Alternative root cause:
Prompt Compiler failed to preserve the asset specification.
```

The recovery engine must avoid treating the first visible failure as automatically being the root cause.

---

# 10. Failure Dependency Graph

The system should preserve dependency relationships:

```text
ROOT CAUSE
   ↓
AFFECTED NODE
   ↓
DOWNSTREAM DEPENDENCIES
   ↓
OBSERVED FAILURES
```

This allows recovery scope to be estimated.

---

# 11. Recovery Scope

A recovery may operate at different levels:

```text
LEVEL 0 — Execution Fix
LEVEL 1 — Asset Fix
LEVEL 2 — Narrative Fix
LEVEL 3 — Evidence Fix
LEVEL 4 — Intent Fix
LEVEL 5 — Knowledge Fix
LEVEL 6 — Campaign Replan
```

The system should prefer the lowest level capable of resolving the failure without violating higher-order constraints.

---

# 12. Minimal Recovery Principle

If:

```text
Prompt error
```

is sufficient to explain the failure:

```text
Fix prompt.
```

Do not:

```text
rewrite intent
rewrite evidence
rewrite asset strategy
```

Likewise, if:

```text
Evidence Requirement
```

is invalid, changing only the prompt may hide the underlying failure.

---

# 13. Recovery Options

Possible recovery actions include:

```text
PATCH
REGENERATE
RESELECT
REVISE
REPLAN
RETRIEVE
RE-EVALUATE
ESCALATE
ABORT
```

The selected action must have a recorded rationale.

---

# 14. PATCH

A patch is a localized correction that preserves the semantic structure.

Examples:

```text
Correct a prompt compilation error.

Correct a channel format parameter.

Restore an omitted required field.
```

A patch is preferred when the failure is local and well understood.

---

# 15. Regeneration

Regeneration means producing a new realization while preserving the upstream specification.

Example:

```text
Asset Requirement valid
        ↓
Generated image failed
        ↓
Regenerate asset
```

Regeneration must not silently mutate upstream intent.

---

# 16. Reselection

Reselection means replacing a selected candidate with another valid candidate.

Example:

```text
Asset A
→ insufficient material evidence

Candidate Asset B
→ satisfies evidence requirement
```

The system may replace A with B without rewriting the campaign intent.

---

# 17. Revision

Revision changes an upstream semantic object.

Examples:

```text
Evidence Requirement revised
Narrative node revised
Channel projection revised
```

Revision requires explicit provenance and versioning.

It must not be disguised as regeneration.

---

# 18. Replanning

Replanning changes the strategy because the current strategy cannot satisfy the requirements.

Example:

```text
One asset cannot simultaneously satisfy
three incompatible product evidence requirements.

Current plan:
Single hero asset.

Recovery:
Split into two coordinated assets.
```

This is a strategic asset replanning decision.

---

# 19. Retrieval Recovery

If a decision depends on insufficient knowledge:

```text
KNOWLEDGE GAP
        ↓
RETRIEVAL
        ↓
VALIDATION
        ↓
REPLAN
```

The system should not invent missing knowledge simply to continue execution.

---

# 20. Escalation

Escalation is required when the system cannot safely recover within its authority.

Examples:

```text
Locked intent conflicts with product truth.

Critical evidence cannot be established.

Authoritative sources materially disagree.

Channel constraint conflicts with required evidence.

No valid asset strategy exists.
```

Possible escalation targets:

```text
HUMAN REVIEW
CAMPAIGN OWNER
DOMAIN EXPERT
RESEARCH
SYSTEM OPERATOR
```

The exact routing mechanism is deferred.

---

# 21. Abort

The system should support explicit termination when continuing would require unacceptable assumptions or violations.

Examples:

```text
No valid strategy exists.

Required information cannot be established.

Hard constraint cannot be satisfied.

Evaluation remains critically uncertain after
bounded recovery attempts.
```

Abort is preferable to fabricated success.

---

# 22. Recovery Authority

The Replanning Engine may modify objects only within its authorized scope.

It may:

```text
request regeneration
request asset reselection
propose evidence revision
propose narrative revision
request retrieval
create recovery plans
```

It may not silently override:

```text
locked campaign intent
product truth
hard brand constraints
authoritative user decisions
```

Such changes require challenge or escalation.

---

# 23. Recovery Decision Object

Conceptually:

```text
recovery_id
failure_id
root_cause
affected_nodes
scope
action
rationale
alternatives
expected_impact
constraints
authority
confidence
status
parent_version
new_version
provenance
```

The exact runtime schema remains deferred.

---

# 24. Recovery Impact Analysis

Before executing a recovery, the system should estimate:

```text
UPSTREAM IMPACT
DOWNSTREAM IMPACT
EVIDENCE IMPACT
INTENT IMPACT
ASSET IMPACT
NARRATIVE IMPACT
CHANNEL IMPACT
PRODUCTION IMPACT
```

This prevents local fixes from causing hidden downstream regressions.

---

# 25. Dependency-Aware Recovery

Example:

```text
Evidence Requirement changes
        ↓
Asset Strategy may change
        ↓
Narrative may change
        ↓
Channel Projection may change
        ↓
Prompt may change
```

The system must identify affected descendants.

It should not assume that a revised node can be substituted without re-evaluating dependent nodes.

---

# 26. Versioning

Every semantic revision must create a new version.

Conceptually:

```text
Intent v1
    ↓
Revision
    ↓
Intent v2
```

The system must preserve:

```text
previous version
new version
reason
trigger
authority
```

Old versions remain recoverable for audit and comparison.

---

# 27. Branching Recovery

When uncertainty exists, the system may preserve multiple recovery branches.

Example:

```text
FAILURE
   │
   ├── Recovery A
   ├── Recovery B
   └── Recovery C
```

Each branch should retain:

```text
assumptions
expected benefits
risks
affected requirements
confidence
```

The system should not collapse genuine uncertainty into one arbitrary branch.

---

# 28. Recovery Selection

Candidate recovery plans may be evaluated on:

```text
Requirement Restoration
Constraint Preservation
Evidence Restoration
Strategic Stability
Production Cost
Complexity
Risk
Confidence
Downstream Impact
```

The exact optimization function remains deferred.

---

# 29. Recovery Cost

Recovery cost may include:

```text
generation cost
retrieval cost
human review
time
compute
asset replacement
downstream invalidation
campaign delay
```

Cost should not override critical requirements.

It is an optimization factor after hard constraints are preserved.

---

# 30. Recovery vs Strategic Drift

A recovery becomes strategic drift when it changes the campaign's meaning without explicit authorization.

Example:

```text
Failure:
Craftsmanship evidence insufficient.

Invalid recovery:
Remove craftsmanship intent.

Valid recovery:
Improve evidence path.
```

The system should explicitly detect this pattern.

---

# 31. Recovery Loop

The canonical bounded loop is:

```text
PLAN
 ↓
GENERATE
 ↓
EVALUATE
 ↓
FAIL
 ↓
DIAGNOSE
 ↓
RECOVER
 ↓
GENERATE
 ↓
EVALUATE
```

The loop terminates when:

```text
PASS
```

or:

```text
ESCALATE
```

or:

```text
ABORT
```

---

# 32. Recovery Budget

Every recovery process should have bounded:

```text
MAX_RETRIES
MAX_REPLANS
MAX_GENERATION_ATTEMPTS
MAX_RETRIEVAL_ATTEMPTS
MAX_EVALUATION_ATTEMPTS
TIME_BUDGET
COST_BUDGET
```

Exact values are runtime policy.

The semantic requirement is that infinite recovery is prohibited.

---

# 33. Recovery Stagnation

The system must detect when repeated attempts are not producing meaningful improvement.

Example:

```text
Attempt 1 → failure
Attempt 2 → same failure
Attempt 3 → same failure
Attempt 4 → same failure
```

This should produce:

```text
RECOVERY_STAGNATION
```

rather than continuing indefinitely.

---

# 34. Recovery Regression

A recovery may fix one requirement while breaking another.

Example:

```text
Attempt 1:
Material evidence FAIL
Craftsmanship evidence PASS

Attempt 2:
Material evidence PASS
Craftsmanship evidence FAIL
```

The system must compare evaluation states across attempts.

Improvement in one dimension does not automatically mean overall improvement.

---

# 35. Recovery Delta

Each recovery should record:

```text
WHAT CHANGED
WHAT IMPROVED
WHAT REGRESSED
WHAT REMAINED UNCHANGED
```

This creates measurable recovery evidence.

---

# 36. Recovery Evaluation

After every substantive recovery:

```text
RE-EVALUATE
```

The evaluator must assess affected requirements and any newly affected dependencies.

A system must not declare success based solely on the intended effect of the recovery.

---

# 37. Recovery Rollback

The architecture should support rollback when a recovery produces unacceptable regression.

Conceptually:

```text
v1
 ↓
v2
 ↓
v3
 ↓
REGRESSION
 ↓
ROLLBACK / BRANCH
```

Rollback should preserve the evidence explaining why the recovery was rejected.

---

# 38. Recovery Provenance

Every recovery action must preserve:

```text
trigger
failure
diagnosis
action
decision authority
versions
evaluation results
```

The system should be able to answer:

> Why did the campaign change?

and:

> What caused this change?

without reconstructing history from model conversation logs.

---

# 39. Self-Critique Requirements

The Self-Critique Agent should inspect recovery plans for:

- overreaction,
- underreaction,
- root-cause misidentification,
- unnecessary upstream mutation,
- strategic drift,
- ignored dependencies,
- hidden assumptions,
- repeated failed strategies,
- recovery stagnation,
- regression,
- and unjustified escalation.

The critic should create a critique record rather than silently changing the recovery plan.

---

# 40. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break replanning by:

1. Triggering unnecessary full-campaign rewrites.
2. Hiding a root-cause error behind repeated regeneration.
3. Mutating locked intent during recovery.
4. Removing requirements to make a failure disappear.
5. Creating false recovery improvements.
6. Ignoring downstream dependencies.
7. Exploiting uncertainty to justify arbitrary changes.
8. Creating infinite recovery loops.
9. Hiding regressions.
10. Preventing rollback.
11. Manipulating recovery cost to bypass hard constraints.
12. Creating fake recovery success.
13. Severing version lineage.
14. Converting a recovery into an undeclared strategic variant.

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

# 41. Validation Invariants

### Invariant 1

Every recovery action must trace to a recorded failure, challenge, or knowledge gap.

### Invariant 2

Recovery should prefer the smallest sufficient change.

### Invariant 3

Root cause and symptom must remain distinguishable.

### Invariant 4

Recovery cannot silently mutate locked intent.

### Invariant 5

Recovery cannot silently violate product truth.

### Invariant 6

Recovery cannot silently weaken hard requirements.

### Invariant 7

Substantive recovery requires re-evaluation.

### Invariant 8

Downstream dependencies must be identified after upstream changes.

### Invariant 9

Recovery attempts are versioned.

### Invariant 10

Repeated non-improvement must be detectable.

### Invariant 11

Regression must be evaluated across affected requirements.

### Invariant 12

Recovery loops must be bounded.

### Invariant 13

Rollback must preserve failure and decision history.

### Invariant 14

Escalation is preferable to fabricated certainty.

### Invariant 15

Abort is preferable to violating an authoritative invariant.

### Invariant 16

Recovery decisions preserve provenance.

---

# 42. Falsifiable Architectural Hypotheses

## Hypothesis A — Minimal recovery reduces unintended strategic drift

**Claim:**

Localizing failure and applying the smallest valid recovery produces less downstream strategic change than full regeneration.

**Experiment:**

Compare:

```text
System A:
Full restart after any failure

System B:
Dependency-aware minimal recovery
```

Measure:

- changed upstream decisions,
- strategic drift,
- recovery cost,
- final requirement satisfaction.

---

## Hypothesis B — Root-cause localization reduces repeated failure

**Claim:**

Identifying the earliest invalid decision reduces repeated downstream regeneration of outputs that are structurally doomed to fail.

**Experiment:**

Inject upstream specification errors and compare:

```text
symptom-level regeneration
vs
root-cause-aware recovery
```

Measure repeated failure rate.

---

## Hypothesis C — Recovery delta tracking improves optimization

**Claim:**

Explicitly recording improvement and regression across attempts produces better recovery selection than evaluating only the latest attempt.

**Experiment:**

Compare:

```text
latest-output-only selection
vs
trajectory-aware recovery selection
```

Measure final success and regression rate.

---

## Hypothesis D — Bounded recovery prevents pathological loops

**Claim:**

Explicit retry and stagnation controls prevent infinite or economically irrational recovery cycles.

**Experiment:**

Provide deliberately unsatisfiable requirements.

Expected:

```text
STAGNATION
→ ESCALATE / ABORT
```

rather than unlimited retries.

---

## Hypothesis E — Versioned recovery improves auditability

**Claim:**

Versioned recovery lineage makes strategic changes more accurately explainable than storing only final state.

**Experiment:**

Ask independent reviewers to reconstruct why a campaign changed using:

```text
final state only
vs
versioned recovery history
```

Measure reconstruction accuracy.

---

# 43. Recovery Evaluation Model

Every recovery sequence should eventually expose:

```text
ORIGINAL FAILURE
        ↓
ROOT CAUSE
        ↓
RECOVERY ACTION
        ↓
EXPECTED IMPACT
        ↓
ACTUAL IMPACT
        ↓
REQUIREMENT DELTA
        ↓
REGRESSION CHECK
        ↓
FINAL STATE
```

This creates empirical evidence about whether the recovery mechanism itself works.

---

# 44. Replanning and Architecture Proof

Replanning is also an architectural test surface.

The system can be evaluated on:

```text
Can it identify the correct failure layer?
Can it avoid unnecessary upstream mutation?
Can it preserve locked authority?
Can it recover without hiding failures?
Can it detect stagnation?
Can it recognize regression?
Can it escalate appropriately?
```

These are falsifiable properties of the architecture.

---

# 45. Recovery Dataset

The evaluation corpus should eventually include:

```text
LOCAL EXECUTION FAILURES
EVIDENCE FAILURES
INTENT FAILURES
KNOWLEDGE GAPS
AUTHORITY CONFLICTS
CROSS-DOMAIN CONFLICTS
NARRATIVE FAILURES
CHANNEL FAILURES
GENERATION FAILURES
UNSATISFIABLE CASES
STAGNATION CASES
REGRESSION CASES
```

Each case should specify:

```text
initial state
failure trigger
known root cause
valid recovery
invalid recovery
expected escalation
expected terminal state
```

---

# 46. Core Contract

> **The Replanning Engine shall recover from evaluation failures, self-critique findings, adversarial findings, knowledge gaps, and constraint conflicts through dependency-aware, minimally invasive, versioned, and evidence-driven changes. It shall distinguish symptoms from root causes, preserve authoritative constraints and locked intent, evaluate downstream impact, detect stagnation and regression, support branching and rollback, bound recovery loops, and escalate or abort when safe recovery is not possible.**

---

# 47. Deferred Decisions

II-011 does not freeze:

- exact recovery algorithm,
- dependency graph implementation,
- retry budgets,
- cost functions,
- escalation routing,
- rollback storage,
- branch-pruning algorithm,
- root-cause classifier,
- recovery ranking,
- runtime state machine,
- orchestration framework.

These remain engineering and validation decisions.

---

# 48. Exit Criteria

II-011 is semantically complete when:

- [x] Replanning purpose established
- [x] Failure definition established
- [x] Failure classification established
- [x] Root cause / symptom distinction established
- [x] Dependency-aware localization established
- [x] Recovery scope established
- [x] Minimal recovery principle established
- [x] Patch / regeneration / reselection / revision / replanning distinctions established
- [x] Retrieval recovery established
- [x] Escalation established
- [x] Abort established
- [x] Recovery authority established
- [x] Impact analysis established
- [x] Versioning established
- [x] Branching established
- [x] Recovery selection established
- [x] Recovery cost established
- [x] Strategic drift boundary established
- [x] Recovery loop established
- [x] Budgeting established
- [x] Stagnation detection established
- [x] Regression detection established
- [x] Recovery delta established
- [x] Re-evaluation established
- [x] Rollback established
- [x] Provenance established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Architecture-proof role established
- [x] Recovery dataset requirements established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-012 — Provenance, Lineage & Audit Contract**

This specification will define the immutable lineage connecting knowledge, authority, intents, evidence, asset strategy, narrative, channel projections, evaluations, failures, and recovery decisions so that the complete reasoning history can be reconstructed and audited.
