# IV-003 — Cross-Document Dependency, Lifecycle & Invalidation Analysis

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-002 and Phase III contracts III-001 through III-015  
**Purpose:** Define how dependencies propagate across intelligence objects, authority, evidence, policy, lifecycle, decisions, execution, learning, human oversight, security, and assurance.

---

# 1. Purpose

IV-003 addresses the primary unresolved question from IV-002:

```text
WHEN ONE GOVERNED OBJECT CHANGES,

WHAT ELSE MUST:

- CHANGE?
- BECOME INVALID?
- BE RE-EVALUATED?
- BE RE-AUTHORIZED?
- BE RE-VERIFIED?
- BE RECONSTRUCTED?
```

The goal is not to invent implementation behavior.

The goal is to make explicit the dependency semantics already implied by the Phase III contracts and identify where those semantics remain unspecified.

The central architectural principle is:

```text
A DOWNSTREAM OBJECT MUST NOT REMAIN
VALID MERELY BECAUSE ITS OWN DATA
HAS NOT CHANGED.

VALIDITY MAY DEPEND ON UPSTREAM STATE.
```

---

# 2. Source Basis

This analysis is grounded in the Phase III contract set and IV-002.

Relevant established boundaries include:

```text
III-001
Global Intelligence Object Schema & Identifier Contract

III-003
Intelligence Object Lifecycle & State Machine Contract

III-004
Provenance, Lineage & Evidence Trace Contract

III-005
Agent Contract, Capability Boundary & Execution Interface

III-006
Constraint, Policy & Invariant Enforcement Contract

III-007
Memory, Context & Knowledge State Contract

III-008
Decision, Planning & Execution Intent Contract

III-009
Evaluation, Self-Critique & Adversarial Verification Contract

III-010
Provenance-Aware Memory, Evidence & Retrieval Integrity Contract

III-011
Multi-Agent Coordination, Delegation & Trust Boundary Contract

III-012
Security, Isolation & Adversarial Runtime Contract

III-013
Learning, Adaptation, Self-Modification & Behavioral Stability Contract

III-014
Human Oversight, Escalation & Accountability Contract

III-015
System-Wide Intelligence Assurance, Evaluation & Proof Contract
```

III-001 establishes a common object envelope containing identity, object version, schema version, lifecycle state, timestamps, producer, authority context, provenance context, and payload.

III-007 explicitly distinguishes available information from trusted and authoritative information.

III-008 distinguishes intent, decision, execution, and outcome and includes decision revision, supersession, rollback, retry, idempotency, and reconstruction.

III-009 treats evaluation as a governed process rather than an informal second opinion.

III-013 requires material changes to be governed so that adaptation cannot silently alter authority, safety properties, identity, or behavioral contract.

---

# 3. Dependency Semantics

A dependency exists when the interpretation, validity, authorization, or assurance of object `B` depends materially on object or state `A`.

Conceptually:

```text
A
 ↓
B
```

does not necessarily mean:

```text
A changes
→ B must always be deleted
```

It means:

```text
A changes
→ B's validity must be evaluated
```

The resulting status may be:

```text
VALID
STALE
INVALID
SUPERSEDED
REQUIRES_REVALIDATION
REQUIRES_REAUTHORIZATION
REQUIRES_REVERIFICATION
REQUIRES_REPLANNING
QUARANTINED
```

The exact state vocabulary remains subject to the lifecycle contract.

---

# 4. Dependency Types

The architecture should distinguish at least:

```text
SEMANTIC DEPENDENCY
AUTHORITY DEPENDENCY
EVIDENCE DEPENDENCY
PROVENANCE DEPENDENCY
LIFECYCLE DEPENDENCY
VERSION DEPENDENCY
POLICY DEPENDENCY
SECURITY DEPENDENCY
DELEGATION DEPENDENCY
CONTEXT DEPENDENCY
EXECUTION DEPENDENCY
ASSURANCE DEPENDENCY
HUMAN-APPROVAL DEPENDENCY
CHANGE DEPENDENCY
```

These must not be collapsed into a generic `depends_on` relationship without preserving the dependency type.

---

# 5. Dependency Identity

Every consequential dependency relationship should be reconstructable.

Conceptually:

```yaml
dependency:
  dependency_id: DEP-...
  source_ref: ...
  source_version: ...
  target_ref: ...
  target_version: ...
  dependency_type: ...
  strength: ...
  invalidation_rule: ...
  provenance_ref: ...
```

The exact schema is deferred.

The semantic requirement is not.

---

# 6. Dependency Strength

A useful conceptual classification is:

```text
HARD
SOFT
CONDITIONAL
ADVISORY
```

### HARD

A change in the source invalidates or blocks the target unless explicitly revalidated.

### SOFT

A source change requires reconsideration but does not automatically invalidate the target.

### CONDITIONAL

Invalidation occurs only when a defined property of the source changes.

### ADVISORY

The source affects interpretation or ranking but does not determine validity.

The final registry must be derived from the authoritative semantics.

---

# 7. Core Dependency Graph

The current contracts imply a high-level dependency chain:

```text
SOURCE / OBSERVATION
        ↓
EVIDENCE
        ↓
KNOWLEDGE / MEMORY
        ↓
CONTEXT
        ↓
GOAL / INTENT
        ↓
PLAN
        ↓
DECISION
        ↓
EXECUTION INTENT
        ↓
AUTHORIZATION / APPROVAL
        ↓
SECURITY / CONSTRAINT CHECKS
        ↓
EXECUTION
        ↓
OUTCOME
        ↓
EVALUATION
        ↓
ASSURANCE
```

This is a conceptual dependency graph.

It is not yet the final runtime graph.

---

# 8. Provenance Is a Cross-Cutting Dependency

Provenance is not merely metadata attached to the end of a process.

It is required to reconstruct how downstream objects came to exist.

Therefore:

```text
SOURCE
 ↓
TRANSFORMATION
 ↓
DERIVATION
 ↓
DECISION
 ↓
EXECUTION
 ↓
EVALUATION
```

must preserve lineage.

A transformation must not silently erase the origin of its input.

---

# 9. Version Dependency

III-001 distinguishes:

```text
OBJECT VERSION
```

from:

```text
SCHEMA VERSION
```

A version change must therefore be evaluated according to what changed.

Conceptually:

```text
VERSION CHANGE
      ↓
WHAT SEMANTIC PROPERTY CHANGED?
      ↓
WHICH DEPENDENTS USE THAT PROPERTY?
      ↓
REVALIDATE AFFECTED DEPENDENTS
```

A version increment alone is insufficient to determine impact.

---

# 10. Version Impact Classes

A version change should be classified conceptually as:

```text
NON-MATERIAL
SEMANTICALLY LOCAL
AUTHORITY-AFFECTING
SECURITY-AFFECTING
EVIDENCE-AFFECTING
BEHAVIOR-AFFECTING
SCHEMA-AFFECTING
GLOBAL / CROSS-CUTTING
```

The exact taxonomy remains a deferred engineering decision unless required by semantic meaning.

---

# 11. Schema Version Changes

A schema version change is distinct from an object version change.

Therefore:

```text
OBJECT VERSION CHANGE
≠
SCHEMA VERSION CHANGE
```

A schema change may affect interpretation of many objects even if their object versions remain unchanged.

Therefore:

```text
SCHEMA CHANGE
 ↓
COMPATIBILITY ANALYSIS
 ↓
AFFECTED OBJECT IDENTIFICATION
 ↓
MIGRATION / REVALIDATION
```

The architecture must not silently treat schema compatibility as object validity.

---

# 12. Authority Dependency

Objects can depend on authority context.

Examples include:

```text
decision
execution intent
delegation
human approval
policy exception
credential
self-modification request
```

A change in authority may therefore invalidate downstream objects.

Conceptually:

```text
AUTHORITY CHANGE
      ↓
IDENTIFY DEPENDENTS
      ↓
CHECK SCOPE
      ↓
CHECK EXPIRATION
      ↓
CHECK REVOCATION
      ↓
CHECK DECISION / EXECUTION IMPACT
```

---

# 13. Authority Revocation

Revocation is different from ordinary version change.

A revocation means:

```text
PREVIOUSLY AVAILABLE AUTHORITY
IS NO LONGER AVAILABLE
```

Therefore downstream authorization must not remain valid solely because it was previously issued.

The architecture must determine whether revocation causes:

```text
IMMEDIATE INVALIDATION
FUTURE-USE INVALIDATION
EXECUTION RECHECK
COMPENSATING ACTION
HUMAN ESCALATION
```

The exact rule depends on the authority type.

---

# 14. Approval Dependency

Human approval is a governed dependency.

An approval may depend on:

```text
action identity
action version
decision identity
decision version
scope
authority
context
risk classification
expiration
revocation state
```

Therefore:

```text
ACTION CHANGES
        ↓
APPROVAL VALIDITY CHECK
```

must occur before execution.

An approval for action `A(v1)` must not automatically authorize materially different action `A(v2)`.

---

# 15. Human Approval Invalidation

Conceptually:

```text
APPROVAL
 ↓
BOUND TO
 ↓
ACTION / DECISION / SCOPE / CONTEXT
```

If any approval-binding property changes materially:

```text
APPROVAL
→
REQUIRES REVALIDATION
```

This is especially important for high-impact or irreversible operations.

---

# 16. Delegation Dependency

III-011 defines delegation, authority containment, transitive delegation, expiration, and revocation.

The essential dependency relation is:

```text
DELEGATOR AUTHORITY
        ↓
DELEGATION
        ↓
DELEGATEE AUTHORITY
```

The downstream authority must remain bounded by the upstream authority.

Conceptually:

```text
delegatee_scope
⊆
delegator_transferable_scope
```

This is a semantic invariant candidate, not yet a final formal rule.

---

# 17. Delegation Revocation Propagation

If a parent delegation is revoked:

```text
PARENT DELEGATION REVOKED
        ↓
CHILD DELEGATIONS
        ↓
AUTHORITY RE-EVALUATION
```

The architecture must prevent stale child authority from continuing silently.

This is especially important for:

```text
transitive delegation
tool delegation
cross-agent delegation
external-system delegation
```

---

# 18. Evidence Dependency

A decision may depend on evidence.

Therefore:

```text
DECISION
 ↓
EVIDENCE REFERENCES
```

must be explicit.

If evidence changes materially:

```text
EVIDENCE CHANGE
 ↓
CLAIMS AFFECTED?
 ↓
DECISIONS AFFECTED?
 ↓
EXECUTION AFFECTED?
 ↓
ASSURANCE AFFECTED?
```

The system must not assume that unchanged decision bytes imply unchanged decision validity.

---

# 19. Evidence Invalidation

III-010 explicitly covers:

```text
source mutation
source revocation
evidence invalidation
evidence retraction
stale cache
historical replay
```

Therefore evidence validity is temporal.

Conceptually:

```text
EVIDENCE VALID AT T1
```

does not imply:

```text
EVIDENCE VALID AT T2
```

without checking the applicable freshness and validity conditions.

---

# 20. Evidence Freshness Propagation

A source becoming stale should trigger a dependency analysis:

```text
SOURCE STALE
 ↓
EVIDENCE STALE
 ↓
CLAIM STATUS
 ↓
KNOWLEDGE STATE
 ↓
DECISION
 ↓
EXECUTION ELIGIBILITY
 ↓
ASSURANCE
```

The exact propagation depth is not yet frozen.

This is one of the major open semantic questions identified by IV-002.

---

# 21. Memory Dependency

III-007 distinguishes:

```text
ephemeral context
working memory
long-term memory
knowledge state
evidence store
```

Memory therefore cannot be treated as a single validity domain.

For example:

```text
MEMORY RETENTION
≠
MEMORY TRUTH
≠
MEMORY AUTHORITY
```

A memory update may require re-evaluation of knowledge state without invalidating the entire runtime context.

---

# 22. Knowledge-State Dependency

Knowledge state is structured information available for reasoning and decision support.

Therefore:

```text
EVIDENCE CHANGE
 ↓
KNOWLEDGE DERIVATION
 ↓
KNOWLEDGE VERSION
```

must remain reconstructable.

If a knowledge object was derived from superseded evidence, its validity status must be determinable.

---

# 23. Context Dependency

Context composition may depend on:

```text
retrieved evidence
memory
constraints
goal
task state
agent scope
authority
```

Therefore:

```text
CONTEXT
```

is itself a dependent object.

A context snapshot must preserve enough information to determine:

```text
what was known
which versions were used
what authority applied
which constraints applied
what evidence was available
```

This is necessary for decision reconstruction.

---

# 24. Context Contamination

If untrusted or malicious content enters context:

```text
UNTRUSTED INPUT
 ↓
CONTEXT
```

the system must not automatically promote the content to:

```text
trusted knowledge
authority
control-plane instruction
```

This aligns with the information/trust boundary in III-007 and the security boundary in III-012.

---

# 25. Policy Dependency

A decision or execution may depend on:

```text
policy version
constraint version
exception
scope
temporal applicability
```

Therefore:

```text
POLICY CHANGE
 ↓
IDENTIFY DECISIONS
 ↓
IDENTIFY EXECUTION INTENTS
 ↓
CHECK WHETHER POLICY CHANGE IS MATERIAL
```

A stale policy result must not silently authorize new execution.

---

# 26. Constraint Dependency

A binding constraint may determine execution eligibility.

Therefore:

```text
CONSTRAINT
 ↓
DECISION
 ↓
EXECUTION ELIGIBILITY
```

If a binding constraint changes:

```text
existing decision
→
re-evaluate
```

if the changed property affects the decision's governed action.

---

# 27. Exception Dependency

An exception is itself bounded by:

```text
scope
authority
time
reason
policy
```

Therefore:

```text
EXCEPTION EXPIRATION
→
DOWNSTREAM AUTHORIZATION RECHECK
```

An expired exception must not be silently reused.

---

# 28. Security Dependency

III-012 establishes explicit security boundaries around:

```text
identity
credentials
sandbox
tools
filesystem
network
resources
execution
control plane
audit
emergency stop
```

A security-state change may invalidate downstream execution.

Examples:

```text
credential revoked
sandbox changed
security policy changed
identity state changed
agent compromised
security monitor unavailable
```

The execution path must therefore include appropriate security revalidation.

---

# 29. Security State Dependency

Conceptually:

```text
REQUEST
 ↓
AUTHORITY
 ↓
SECURITY STATE
 ↓
SECURITY CHECK
 ↓
EXECUTION
```

A prior successful check must not necessarily be reused after a material security-state change.

This is particularly relevant to TOCTOU conditions explicitly recognized by III-012.

---

# 30. Decision Dependency

III-008 establishes:

```text
intent
plan
decision
execution intent
outcome
```

A decision depends on:

```text
goal
constraints
authority
evidence
uncertainty
risk
candidate comparison
assumptions
```

Therefore a material change in any of these may require:

```text
decision revision
```

rather than direct execution.

---

# 31. Plan Drift

If the environment or dependencies change after planning:

```text
PLAN
 ↓
DEPENDENCY CHANGE
 ↓
PLAN DRIFT CHECK
```

A plan should not be assumed valid simply because it was previously approved.

The exact drift threshold is a deferred engineering decision.

---

# 32. Decision Drift

Similarly:

```text
DECISION
 ↓
UPSTREAM CHANGE
 ↓
DECISION DRIFT CHECK
```

The decision may become:

```text
STILL VALID
REQUIRES RE-EVALUATION
SUPERSEDED
INVALID
```

---

# 33. Execution-Intent Dependency

Execution intent is downstream from decision and authorization.

Therefore:

```text
DECISION CHANGE
→
EXECUTION INTENT RECHECK
```

and:

```text
AUTHORIZATION CHANGE
→
EXECUTION INTENT RECHECK
```

must be supported.

Execution intent must not become an independent authority source.

---

# 34. Outcome Dependency

Outcome is not merely the final status of execution.

It should preserve:

```text
expected outcome
observed outcome
side effects
execution evidence
```

An unexpected outcome may therefore trigger:

```text
evaluation
incident creation
rollback
recovery
learning signal
assurance reassessment
```

depending on the applicable contracts.

---

# 35. Evaluation Dependency

III-009 defines evaluation as a governed process with:

```text
target
claim
protocol
criteria
metrics
evidence
evaluator
result
provenance
```

Therefore an evaluation result depends on the versions of:

```text
target
evaluation protocol
dataset/test set
evidence
evaluator
```

A changed target or protocol must not silently preserve the interpretation of the old evaluation.

---

# 36. Assurance Dependency

III-015 explicitly distinguishes:

```text
DESIGNED
≠
IMPLEMENTED
≠
TESTED
≠
VERIFIED
≠
VALIDATED
≠
PROVEN
```

Therefore an assurance claim depends on:

```text
claim scope
assumptions
evidence
tests
verification results
falsification results
target versions
```

If a material dependency changes:

```text
ASSURANCE CLAIM
→
REASSESSMENT
```

may be required.

---

# 37. Assurance Revocation

Assurance claims are explicitly revocable.

Therefore:

```text
ASSURANCE CLAIM
 ↓
SUPPORTING EVIDENCE
 ↓
SUPPORTING TESTS
 ↓
TARGET VERSION
```

must be reconstructable.

If critical support is invalidated:

```text
ASSURANCE
→
REVOKE / BLOCK / REASSESS
```

The exact state transition must be compiled into the assurance lifecycle.

---

# 38. Learning Dependency

III-013 requires consequential learning updates to preserve their source and supporting evidence.

Therefore:

```text
OBSERVATION
 ↓
EVALUATION
 ↓
LEARNING SIGNAL
 ↓
UPDATE
```

must preserve lineage.

An invalidated learning source must not silently remain trusted training material.

---

# 39. Self-Modification Dependency

Material modification must identify:

```text
change identity
target
previous version
proposed version
reason
authority
verification
provenance
```

Therefore:

```text
PROPOSED CHANGE
 ↓
AUTHORIZATION
 ↓
VERIFICATION
 ↓
DEPLOYMENT
 ↓
ASSURANCE REASSESSMENT
```

is the required conceptual path.

---

# 40. Behavioral-Stability Dependency

A change that modifies implementation but appears behaviorally harmless still requires evaluation where the change can materially affect governed properties.

Conversely:

```text
behavioral change
```

may occur without:

```text
implementation replacement
```

through learning, memory, policy, or configuration.

Therefore change analysis must not be restricted to code versions.

---

# 41. Human Oversight Dependency

Human decisions depend on:

```text
system recommendation
evidence available
uncertainty
risk
escalation
operator authority
human context
```

Therefore a human approval made against one context must not automatically authorize an materially changed action under another context.

Human decision reconstruction must preserve the relevant context.

---

# 42. Recovery Dependency

Multiple contracts define recovery at different layers:

```text
III-003 → object/lifecycle recovery
III-011 → coordination recovery
III-012 → security recovery
III-013 → change rollback/recovery
III-014 → human oversight recovery
III-015 → assurance recovery
```

These are not contradictions.

They represent different recovery domains.

However, the cross-layer composition remains an open dependency question.

---

# 43. Recovery Composition

A recovery operation should conceptually follow:

```text
FAILURE
 ↓
CONTAINMENT
 ↓
STATE IDENTIFICATION
 ↓
DEPENDENCY ANALYSIS
 ↓
RECOVERY PLAN
 ↓
AUTHORIZATION
 ↓
EXECUTION
 ↓
VERIFICATION
 ↓
RESTORATION
 ↓
ASSURANCE REASSESSMENT
```

Restoring a component must not automatically restore all downstream authority.

---

# 44. Recovery Must Not Restore Stale Authority

A critical invariant candidate is:

```text
RECOVERY
≠
AUTOMATIC AUTHORITY RESTORATION
```

After recovery, the system must determine:

```text
which authority remains valid
which credentials remain valid
which approvals remain valid
which evidence remains valid
which decisions require re-evaluation
```

This aligns with the security requirement that recovery requires verification before restoration of normal authority.

---

# 45. Invalidation Propagation Model

A general propagation model can be expressed as:

```text
SOURCE CHANGE
      ↓
DEPENDENCY DISCOVERY
      ↓
IMPACT CLASSIFICATION
      ↓
TARGET VALIDITY CHECK
      ↓
┌───────────────┬─────────────────┐
│               │                 │
VALID       REVALIDATE        INVALIDATE
│               │                 │
continue      verify          supersede /
                              quarantine /
                              revoke
```

The architecture should avoid global invalidation when the dependency is local.

---

# 46. Locality Principle

A material change should invalidate the smallest necessary dependency set.

Conceptually:

```text
LOCAL CHANGE
→
LOCAL IMPACT
```

unless the dependency graph demonstrates broader propagation.

This prevents:

```text
single memory update
→
global system invalidation
```

without evidence.

---

# 47. Critical-Property Principle

Some changes may be local in data scope but global in consequence.

Examples:

```text
security invariant change
authority model change
credential boundary change
control-plane policy change
schema interpretation change
verification mechanism change
```

Therefore impact must depend on semantic criticality, not merely object count.

---

# 48. Invalidation vs Supersession

These must remain distinct.

### Invalidation

The object is no longer valid for its governed purpose.

### Supersession

A newer object replaces the previous object for the same semantic role.

Therefore:

```text
A(v1)
 ↓
A(v2)
```

does not necessarily mean `A(v1)` was invalid.

It may remain historically valid while being superseded for future use.

---

# 49. Revocation vs Supersession

Revocation is also distinct:

```text
SUPERSEDED
```

means a newer state exists.

```text
REVOKED
```

means prior authority or validity has been withdrawn.

These must not be collapsed.

---

# 50. Staleness vs Invalidity

Stale information may still be historically accurate.

Therefore:

```text
STALE
≠
FALSE
```

But stale information may be insufficient for a current decision.

Therefore:

```text
STALE
→
CONTEXT-DEPENDENT REVALIDATION
```

rather than automatic deletion.

---

# 51. Proposed Dependency State Machine

Conceptually:

```text
VALID
  |
  | upstream change detected
  v
IMPACT_UNKNOWN
  |
  +---- no material impact ----> VALID
  |
  +---- revalidation required --> REVALIDATION_REQUIRED
  |                                |
  |                                +--> VALID
  |                                +--> INVALID
  |
  +---- authority revoked -------> REVOKED
  |
  +---- replacement exists ------> SUPERSEDED
```

This is a conceptual state machine only.

Final lifecycle integration belongs to III-003.

---

# 52. Invalidation Propagation Matrix

| Upstream change | Potential downstream impact | Default action |
|---|---|---|
| Source mutation | Evidence / claims | Revalidate |
| Source revocation | Evidence / claims / decisions | Revalidate or invalidate |
| Evidence invalidation | Knowledge / decisions / assurance | Revalidate |
| Memory update | Knowledge / context | Impact analysis |
| Knowledge version change | Plans / decisions | Revalidate |
| Policy change | Decisions / execution | Re-evaluate |
| Constraint change | Eligibility / decisions | Re-evaluate |
| Authority revocation | Delegations / approvals / execution | Re-authorize or block |
| Delegation revocation | Child authority / actions | Re-authorize or block |
| Approval expiration | Execution | Block / escalate |
| Credential revocation | Execution | Block / re-authenticate |
| Security-state change | Execution | Runtime security recheck |
| Goal change | Plans / decisions | Replan |
| Plan change | Decision / execution intent | Re-evaluate |
| Decision change | Execution intent | Rebind |
| Protocol change | Evaluation / assurance | Re-evaluate |
| Target version change | Evaluation / assurance | Re-evaluate |
| Model change | Behavior / assurance | Reassess |
| Policy-engine change | Enforcement assurance | Reassess |
| Security configuration change | Runtime assurance | Reassess |
| Human context change | Approval | Revalidate |
| Material system change | Assurance claims | Reassess |

The table expresses dependency analysis, not final runtime semantics.

---

# 53. Critical Invalidation Chains

## Chain A — Evidence

```text
SOURCE
 ↓
EVIDENCE
 ↓
CLAIM
 ↓
KNOWLEDGE
 ↓
DECISION
 ↓
EXECUTION
 ↓
ASSURANCE
```

## Chain B — Authority

```text
AUTHORITY
 ↓
DELEGATION
 ↓
AGENT CAPABILITY USE
 ↓
DECISION
 ↓
EXECUTION
```

## Chain C — Policy

```text
POLICY
 ↓
CONSTRAINT
 ↓
ELIGIBILITY
 ↓
DECISION
 ↓
EXECUTION
```

## Chain D — Human Approval

```text
DECISION
 ↓
RISK / ESCALATION
 ↓
HUMAN APPROVAL
 ↓
EXECUTION AUTHORIZATION
 ↓
EXECUTION
```

## Chain E — Security

```text
IDENTITY
 ↓
CREDENTIAL
 ↓
SECURITY STATE
 ↓
SECURITY CHECK
 ↓
EXECUTION
```

## Chain F — Change

```text
CHANGE
 ↓
VERIFICATION
 ↓
DEPLOYMENT
 ↓
BEHAVIOR
 ↓
ASSURANCE
```

---

# 54. Cross-Chain Interaction

The difficult cases occur when multiple chains intersect.

Example:

```text
SOURCE CHANGES
      ↓
EVIDENCE INVALID
      ↓
DECISION INVALID
      ↓
HUMAN APPROVAL
```

The approval itself may still be cryptographically valid while being semantically invalid because its target decision is no longer valid.

Therefore:

```text
APPROVAL INTEGRITY
≠
APPROVAL SEMANTIC VALIDITY
```

This distinction should become an explicit invariant.

---

# 55. Another Cross-Chain Interaction

```text
POLICY CHANGES
      ↓
EXECUTION NO LONGER ALLOWED
      ↓
EXISTING EXECUTION INTENT
```

The execution intent may remain a valid historical object while becoming ineligible for execution.

Therefore:

```text
OBJECT VALIDITY
≠
EXECUTION ELIGIBILITY
```

This distinction is important and should remain explicit.

---

# 56. Another Cross-Chain Interaction

```text
MODEL VERSION CHANGES
      ↓
EVALUATION TARGET CHANGES
      ↓
OLD ASSURANCE RESULT
```

The historical evaluation remains valid for the old target.

But it may no longer support an assurance claim about the new target.

Therefore:

```text
HISTORICAL EVALUATION VALIDITY
≠
CURRENT ASSURANCE APPLICABILITY
```

---

# 57. Another Cross-Chain Interaction

```text
SECURITY CONFIGURATION CHANGES
      ↓
PREVIOUS APPROVAL
      ↓
EXECUTION
```

The approval does not bypass the newly applicable security boundary.

Therefore:

```text
APPROVAL
≠
SECURITY AUTHORIZATION
```

This aligns with the security contract's explicit runtime enforcement boundary.

---

# 58. Dependency Discovery Requirement

Before execution of a consequential action, the runtime should be able to answer:

```text
WHAT DOES THIS ACTION DEPEND ON?
```

At minimum:

```text
decision
plan
goal
evidence
knowledge state
constraints
policy
authority
delegations
approvals
credentials
security state
agent version
tool version
relevant configuration
```

The exact list depends on action type.

---

# 59. Dependency Snapshot

A consequential decision should preserve a dependency snapshot containing references to the relevant versions.

Conceptually:

```yaml
dependency_snapshot:
  object_refs: []
  evidence_refs: []
  policy_refs: []
  constraint_refs: []
  authority_refs: []
  approval_refs: []
  security_state_ref: ...
  model_ref: ...
  tool_refs: []
  context_ref: ...
```

This is required for reconstruction and reproducibility.

---

# 60. Dependency Snapshot vs Full State

The dependency snapshot does not necessarily mean copying all source data.

It means preserving enough references to reconstruct:

```text
WHAT WAS USED
WHICH VERSION
WHICH STATE
WHY IT MATTERED
```

This aligns with the least-evidence and reconstruction principles.

---

# 61. Revalidation Trigger Classes

A dependency change should be able to trigger:

```text
NO ACTION
REVALIDATE
REPLAN
REDECIDE
REAUTHORIZE
REAPPROVE
REVERIFY
BLOCK
QUARANTINE
ESCALATE
ROLLBACK
```

The trigger must be determined by dependency semantics.

---

# 62. Fail-Safe Direction

When dependency validity cannot be established for a high-impact action:

```text
UNKNOWN
```

must not silently become:

```text
PASS
```

This follows the broader contracts' deny-safe and default-deny principles.

For low-impact operations, degraded behavior may be possible where explicitly permitted.

---

# 63. Dependency Failure and Degraded Operation

III-012 permits bounded degraded operation where risk allows.

Therefore dependency failure may produce:

```text
DEGRADED
```

rather than always:

```text
SYSTEM HALT
```

But degradation must not silently remove critical safeguards.

---

# 64. Assurance of the Dependency System

The dependency mechanism itself becomes an assurance target.

The architecture should be able to demonstrate:

```text
DEPENDENCY DISCOVERY COMPLETENESS
DEPENDENCY VERSION ACCURACY
INVALIDATION CORRECTNESS
FALSE INVALIDATION RATE
MISSED INVALIDATION RATE
REVOCATION PROPAGATION
STALE-STATE DETECTION
REVALIDATION CORRECTNESS
RECONSTRUCTION SUCCESS
```

A single dependency-coverage score must not hide critical missed dependencies.

---

# 65. Falsification Cases

Deliberately attempt:

```text
change source after decision
change evidence after approval
revoke authority after delegation
revoke parent delegation after child delegation
expire approval before execution
change policy after planning
change constraint after decision
change security state after authorization
change model after evaluation
change evaluation protocol after assurance
change schema without revalidation
restore compromised agent without reauthorization
reuse stale cached policy
reuse stale evidence
reuse expired credential
reuse superseded execution intent
```

The system should detect, reject, quarantine, revalidate, or explicitly mark these states according to the applicable contract.

---

# 66. Required Benchmarks

## Dependency Reconstruction Benchmark

Given a consequential execution, reconstruct:

```text
all material upstream dependencies
their versions
their validity states
their authority states
their evidence states
their approval states
their security state
```

## Invalidation Propagation Benchmark

Change one upstream object and measure:

```text
affected dependents detected
required dependents revalidated
invalid dependents blocked
unaffected dependents preserved
```

## Revocation Benchmark

Revoke:

```text
authority
delegation
approval
credential
policy exception
source
```

and measure downstream containment.

## Staleness Benchmark

Introduce:

```text
stale evidence
stale memory
stale policy
stale authorization
stale cache
```

and test whether the runtime prevents inappropriate reuse.

---

# 67. Failure Taxonomy

Dependency failures should be classified at least as:

```text
MISSED_DEPENDENCY
FALSE_DEPENDENCY
STALE_DEPENDENCY
BROKEN_REFERENCE
WRONG_VERSION
INVALIDATION_FAILURE
OVER_INVALIDATION
UNDER_INVALIDATION
REVOCATION_PROPAGATION_FAILURE
REVALIDATION_FAILURE
REAUTHORIZATION_FAILURE
REAPPROVAL_FAILURE
RECONSTRUCTION_FAILURE
DEPENDENCY_SNAPSHOT_FAILURE
```

---

# 68. Open Semantic Questions

The current documents do not fully establish:

### Q1 — Exact authority precedence

How do:

```text
security invariants
non-overridable invariants
binding constraints
policy
human authority
agent authority
```

compose?

### Q2 — Exact invalidation depth

How far must evidence invalidation propagate?

### Q3 — Exact approval binding

Which decision changes invalidate human approval?

### Q4 — Exact recovery composition

How do object, security, coordination, human, and assurance recovery interact?

### Q5 — Exact version impact

Which version changes require mandatory revalidation?

### Q6 — Exact schema migration semantics

When does schema change invalidate historical object interpretation?

### Q7 — Exact delegation propagation

How does revocation propagate across transitive and external delegation?

These remain open.

---

# 69. Deferred Decisions

IV-003 intentionally does not freeze:

```text
dependency database
graph representation
dependency query language
exact dependency strength taxonomy
exact invalidation algorithm
exact impact-analysis algorithm
exact cache invalidation mechanism
exact event-bus technology
exact lifecycle state additions
exact authorization precedence algorithm
exact schema migration technology
exact revalidation scheduler
exact dependency snapshot serialization
exact rollback engine
exact recovery orchestrator
```

These remain engineering decisions unless they alter semantic meaning.

---

# 70. Required Architectural Decision

Before implementation, the architecture should define a formal distinction between:

```text
OBJECT VALIDITY
AUTHORIZATION VALIDITY
EXECUTION ELIGIBILITY
EVIDENCE VALIDITY
ASSURANCE APPLICABILITY
```

They must not be represented by one generic `valid: true/false` field.

Conceptually:

```text
object.validity
authorization.validity
execution.eligibility
evidence.validity
assurance.applicability
```

This is one of the most important conclusions of IV-003.

---

# 71. Proposed System-Level Invariants

### Invariant 1

A downstream object must not silently outlive a materially invalid upstream dependency.

### Invariant 2

Historical validity and current applicability are distinct.

### Invariant 3

Revocation propagates to dependent authority where applicable.

### Invariant 4

Approval does not bypass runtime security checks.

### Invariant 5

Execution intent does not create authority.

### Invariant 6

Stale information is not automatically false, but may be insufficient for current use.

### Invariant 7

Supersession does not imply historical invalidity.

### Invariant 8

Recovery does not automatically restore authority.

### Invariant 9

A material system change triggers applicable assurance reassessment.

### Invariant 10

Dependency state must remain reconstructable for consequential decisions.

### Invariant 11

Unknown dependency validity must not silently become PASS for protected operations.

### Invariant 12

Dependency analysis must preserve locality and avoid unnecessary global invalidation.

---

# 72. Engineering Interpretation

The architecture is moving toward a model in which:

```text
VALIDITY
```

is not a static property.

It is a relationship among:

```text
OBJECT
+
VERSION
+
CONTEXT
+
AUTHORITY
+
EVIDENCE
+
POLICY
+
SECURITY STATE
+
TIME
```

Therefore a more accurate conceptual model is:

```text
VALID(object, context, time, authority, dependencies)
```

rather than:

```text
object.valid = true
```

This is an architectural interpretation derived from the dependency requirements, not a final implementation API.

---

# 73. Exit Criteria

- [x] Dependency purpose defined
- [x] Dependency types defined
- [x] Dependency identity conceptualized
- [x] Dependency strength conceptualized
- [x] Cross-document dependency graph established
- [x] Version dependency analyzed
- [x] Authority dependency analyzed
- [x] Delegation dependency analyzed
- [x] Evidence dependency analyzed
- [x] Memory dependency analyzed
- [x] Knowledge dependency analyzed
- [x] Context dependency analyzed
- [x] Policy dependency analyzed
- [x] Constraint dependency analyzed
- [x] Security dependency analyzed
- [x] Decision dependency analyzed
- [x] Execution-intent dependency analyzed
- [x] Human-approval dependency analyzed
- [x] Learning/change dependency analyzed
- [x] Evaluation dependency analyzed
- [x] Assurance dependency analyzed
- [x] Recovery dependency analyzed
- [x] Invalidation model defined
- [x] Revocation model analyzed
- [x] Staleness distinction defined
- [x] Supersession distinction defined
- [x] Cross-chain interactions analyzed
- [x] Dependency snapshot proposed
- [x] Falsification cases defined
- [x] Benchmarks defined
- [x] Failure taxonomy defined
- [x] Open semantic questions documented
- [x] Deferred decisions documented
- [x] Candidate system-level invariants documented

**Current assessment:** The Phase III contracts imply a coherent dependency architecture, but the exact propagation semantics for authority revocation, evidence invalidation, version changes, human approvals, recovery, and assurance applicability remain unresolved. These must be explicitly decided before implementation compilation.

---

# 74. Next Document

**IV-004 — Authority, Constraint, Security & Human-Governance Precedence Matrix**

IV-004 should resolve the highest-priority semantic gap carried forward from IV-002 and IV-003:

```text
WHEN MULTIPLE GOVERNANCE LAYERS
APPLY TO THE SAME ACTION,

WHICH ONE WINS?
```

The analysis must formalize:

```text
security invariants
non-overridable invariants
binding constraints
policy
exceptions
human authority
human approval
agent authority
delegated authority
recommendations
```

and define:

```text
precedence
override
exception
escalation
denial
revocation
emergency behavior
```

without allowing distributed capability or human authority to silently become unbounded runtime control.
