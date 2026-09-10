# IV-004 — Authority, Constraint, Security & Human-Governance Precedence Matrix

**Status:** Engineering Specification — Draft / Active Review  
**Phase:** IV — Cross-Document Validation & Engineering Readiness  
**Depends On:** IV-002, IV-003, III-005, III-006, III-008, III-011, III-012, III-014, III-015  
**Purpose:** Formalize the precedence problem among security controls, invariants, constraints, policies, exceptions, authority, delegation, human approval, agent authority, recommendations, escalation, and execution.

---

# 1. Purpose

IV-004 addresses the central governance question carried forward from IV-003:

```text
WHEN MULTIPLE GOVERNANCE LAYERS
APPLY TO THE SAME ACTION,

WHICH ONE WINS?
```

The objective is not to invent a universal hierarchy unsupported by the Phase III contracts.

The objective is to:

1. identify the governance layers already established;
2. distinguish their semantic roles;
3. identify precedence relationships that are already supported;
4. identify conflicts where the contracts do not yet define precedence;
5. establish candidate invariants;
6. prevent authority, delegation, human approval, or recommendations from silently bypassing stronger controls.

The key architectural distinction is:

```text
AUTHORITY TO PROPOSE
        ≠
AUTHORITY TO APPROVE
        ≠
AUTHORITY TO EXECUTE
        ≠
PERMISSION TO EXECUTE
        ≠
SECURITY ELIGIBILITY
```

---

# 2. Source Basis

This document is grounded in the Phase III contract family and IV-003.

The relevant contract boundaries include:

```text
III-005
Agent Contract, Capability Boundary & Execution Interface

III-006
Constraint, Policy & Invariant Enforcement Contract

III-008
Decision, Planning & Execution Intent Contract

III-011
Multi-Agent Coordination, Delegation & Trust Boundary Contract

III-012
Security, Isolation & Adversarial Runtime Contract

III-014
Human Oversight, Escalation & Accountability Contract

III-015
System-Wide Intelligence Assurance, Evaluation & Proof Contract
```

Additional cross-document conclusions are inherited from IV-003.

Engineering evidence already demonstrates that conflict resolution distinguishes mandatory requirements from weaker requirements, detects direct conflicts, supports escalation for unresolved mandatory conflicts, and records provenance for resolution decisions. fileciteturn16file0L19-L45

The engineering implementation also distinguishes direct `KEY_CONFLICT` from `CROSS_DIMENSION_CONFLICT` and records objective influence in conflict resolution traces. fileciteturn16file6L433-L454

These implementation results are evidence about current engineering behavior, not substitutes for the normative Phase III contracts.

---

# 3. Governance Layers

The architecture should distinguish at least the following layers:

```text
L0  SAFETY / SECURITY BOUNDARY
L1  NON-OVERRIDABLE INVARIANTS
L2  BINDING CONSTRAINTS
L3  POLICY
L4  AUTHORITY SCOPE
L5  DELEGATED AUTHORITY
L6  HUMAN APPROVAL / OVERSIGHT
L7  DECISION / PLAN
L8  EXECUTION INTENT
L9  RECOMMENDATION / PREFERENCE
```

This ordering is a **candidate analytical ordering**, not a ratified runtime precedence hierarchy.

The critical point is that these layers do different jobs.

---

# 4. Governance Is Not One Dimension

A common design error is:

```text
WHO HAS MORE AUTHORITY?
```

treated as the only question.

The actual runtime question is multidimensional:

```text
IS THE ACTION ALLOWED?
WHO MAY AUTHORIZE IT?
WHO MAY EXECUTE IT?
UNDER WHICH POLICY?
UNDER WHICH SECURITY STATE?
WITH WHICH CONSTRAINTS?
WITH WHICH APPROVAL?
```

Therefore precedence must be evaluated per governance dimension.

---

# 5. Dimension A — Safety / Security Eligibility

The first question is:

```text
IS EXECUTION PERMITTED BY THE SECURITY BOUNDARY?
```

An actor's authority does not by itself establish security eligibility.

Conceptually:

```text
AUTHORITY
    +
SECURITY STATE
    +
SECURITY POLICY
    ↓
EXECUTION ELIGIBILITY
```

A valid decision or human approval must not bypass runtime security checks.

This follows directly from the separation between decision/authorization and the security enforcement boundary.

---

# 6. Dimension B — Non-Overridable Invariants

A non-overridable invariant is a condition that cannot be bypassed by ordinary:

```text
policy
exception
agent decision
delegation
human preference
```

The term is retained because IV-003 identified this class as a necessary governance distinction.

The exact registry of non-overridable invariants remains unresolved unless explicitly defined in III-006 or III-012.

---

# 7. Dimension C — Binding Constraints

A binding constraint limits what a decision or execution may do.

Conceptually:

```text
C(action) = TRUE
```

must hold before execution.

A decision cannot convert a binding constraint into a recommendation merely by choosing to ignore it.

---

# 8. Dimension D — Policy

Policy determines what is generally permitted, required, prohibited, or conditioned within a governed scope.

Policy is distinct from:

```text
specific decision
human approval
execution intent
```

A policy exception therefore requires explicit authority and scope.

It must not be inferred from the existence of a human request.

---

# 9. Dimension E — Authority

Authority answers:

```text
WHO MAY REQUEST / APPROVE / EXECUTE?
```

Authority does not necessarily answer:

```text
WHAT IS SAFE?
WHAT IS POLICY-COMPLIANT?
WHAT IS CURRENTLY ELIGIBLE?
```

Therefore:

```text
AUTHORITY
≠
UNCONDITIONAL PERMISSION
```

This is a core governance invariant.

---

# 10. Dimension F — Delegated Authority

Delegation transfers a bounded authority scope.

Conceptually:

```text
DELEGATOR
    ↓
DELEGATION
    ↓
DELEGATEE
```

The delegatee cannot receive more authority than the delegator is permitted to transfer.

Candidate invariant:

```text
delegated_scope
⊆
transferable_authority_scope
```

This is a derived architectural invariant consistent with IV-003's delegation analysis.

---

# 11. Dimension G — Human Approval

Human approval is a governance input.

It does not automatically erase:

```text
security restrictions
non-overridable invariants
binding constraints
authority boundaries
```

An approval should therefore be interpreted as:

```text
APPROVAL WITHIN A GOVERNED SCOPE
```

rather than:

```text
UNCONDITIONAL EXECUTION COMMAND
```

---

# 12. Dimension H — Decision

A decision resolves alternatives under:

```text
goal
evidence
constraints
uncertainty
risk
authority
context
```

A decision therefore remains downstream from stronger governance controls.

The existence of a decision does not create new authority.

---

# 13. Dimension I — Execution Intent

Execution intent specifies the action to be carried out.

It must remain downstream from:

```text
decision
authority
security
constraints
approval
```

where those controls apply.

Candidate invariant:

```text
execution_intent
MUST NOT
CREATE AUTHORITY
```

---

# 14. Dimension J — Recommendation / Preference

Recommendations and preferences are advisory.

They can influence:

```text
ranking
candidate selection
optimization
style
trade-offs
```

but cannot override a binding prohibition.

This is particularly important when a recommendation conflicts with:

```text
mandatory constraint
security restriction
authority boundary
```

The recommendation loses unless an explicit contract says otherwise.

---

# 15. Candidate Precedence Model

The safest candidate ordering is:

```text
SECURITY / SAFETY BOUNDARY
        ↓
NON-OVERRIDABLE INVARIANTS
        ↓
BINDING CONSTRAINTS
        ↓
APPLICABLE POLICY
        ↓
VALID AUTHORITY SCOPE
        ↓
VALID DELEGATION
        ↓
REQUIRED HUMAN APPROVAL
        ↓
DECISION / PLAN
        ↓
EXECUTION INTENT
        ↓
RECOMMENDATION / PREFERENCE
```

This should be treated as a **candidate system-level precedence model**, not as a claim that every relationship is already explicitly ratified.

---

# 16. Why Security Is First

A security boundary exists to prevent execution outside the permitted runtime boundary.

Therefore:

```text
HUMAN APPROVAL
```

cannot legitimately mean:

```text
BYPASS SECURITY
```

and:

```text
AGENT AUTHORITY
```

cannot legitimately mean:

```text
BYPASS SECURITY
```

unless the security architecture explicitly defines a controlled emergency mechanism.

Even then, the emergency mechanism itself must remain governed.

---

# 17. Why Authority Is Not First

Suppose an authorized operator requests:

```text
ACTION X
```

but:

```text
X violates a binding security constraint.
```

The operator may have authority to request X, but the runtime must still determine whether X is executable.

Therefore:

```text
request authority
≠
execution permission
```

This distinction prevents authority from becoming an unbounded control plane.

---

# 18. Why Human Approval Is Not Automatically First

Human approval provides an accountability and governance mechanism.

It does not automatically redefine:

```text
security state
policy
constraints
agent capability
```

Therefore:

```text
APPROVED
```

must not automatically imply:

```text
EXECUTABLE
```

The system must still evaluate all applicable gates.

---

# 19. Why Recommendations Are Last

A recommendation expresses preference or optimization.

It should never silently convert:

```text
DENY
```

into:

```text
ALLOW
```

or:

```text
MANDATORY
```

into:

```text
OPTIONAL
```

This is a direct consequence of distinguishing advisory information from governed constraints.

---

# 20. Constraint Conflict Matrix

| Higher layer | Lower layer | Candidate rule |
|---|---|---|
| Security boundary | Recommendation | Security wins |
| Security boundary | Human approval | Security wins |
| Security boundary | Agent authority | Security wins |
| Non-overridable invariant | Policy | Invariant wins |
| Non-overridable invariant | Exception | Invariant wins |
| Binding constraint | Recommendation | Constraint wins |
| Binding constraint | Decision | Constraint wins |
| Policy | Recommendation | Policy wins |
| Authority scope | Agent request | Request must remain within scope |
| Delegation | Delegatee request | Delegatee remains bounded by delegation |
| Human approval | Recommendation | Approval governs where approval is required |
| Decision | Recommendation | Decision governs execution intent |
| Execution intent | Recommendation | Intent is operationally binding only within prior gates |

These are candidate rules derived from the role distinctions. They should be ratified or modified during contract reconciliation.

---

# 21. Direct Conflict Rule

When two requirements directly conflict and both are mandatory, the system must not silently choose one.

Engineering already demonstrates this principle:

```text
MANDATORY + MANDATORY + DIRECT CONFLICT
                ↓
MULTIPRODUCT CONFLICT REPORT
                ↓
ESCALATION
```

fileciteturn16file0L19-L45

This provides a concrete engineering precedent for the broader governance matrix.

---

# 22. Conflict Resolution Is Not Precedence

The system must distinguish:

```text
PRECEDENCE
```

from:

```text
CONFLICT RESOLUTION
```

Precedence answers:

```text
which governance rule controls?
```

Conflict resolution answers:

```text
how do compatible or competing requirements produce a resolved state?
```

For example, the implementation supports `COMPROMISE` for certain non-exclusive cross-dimensional conflicts. fileciteturn16file6L427-L448

That does not mean `COMPROMISE` can override a security prohibition.

---

# 23. Hard vs Soft Governance

A useful conceptual distinction is:

```text
HARD GOVERNANCE
```

versus:

```text
SOFT GOVERNANCE
```

Hard governance can produce:

```text
DENY
BLOCK
REVOKE
ESCALATE
```

Soft governance can produce:

```text
RANK
PREFER
WARN
OPTIMIZE
```

Engineering already distinguishes mandatory conflicts from weaker requirements and supports escalation rather than silently resolving incompatible mandatory requirements. fileciteturn16file0L19-L45

---

# 24. Override Semantics

The word `override` must not be used without specifying:

```text
WHO overrides?
WHAT is overridden?
WITH WHAT authority?
FOR WHAT scope?
FOR HOW LONG?
UNDER WHICH CONDITIONS?
WITH WHAT audit record?
```

A generic:

```text
override=true
```

would be architecturally unsafe.

---

# 25. Valid Override

A valid override should conceptually require:

```text
OVERRIDE AUTHORITY
+
OVERRIDABLE TARGET
+
SCOPE
+
TIME BOUND
+
REASON
+
AUDIT
+
REQUIRED APPROVAL
+
NO VIOLATION OF NON-OVERRIDABLE CONTROLS
```

The exact schema is deferred.

---

# 26. Non-Overridable Boundary

The architecture must define a finite and explicit set of controls that cannot be overridden by:

```text
agent
human
delegation
policy exception
decision
```

If the system cannot identify what is non-overridable, then the phrase itself provides insufficient runtime semantics.

This is a major open decision.

---

# 27. Exception Semantics

An exception is not the same as an override.

An exception should be interpreted as:

```text
A GOVERNED DEVIATION
FROM A NORMALLY APPLICABLE RULE
```

It must preserve:

```text
scope
authority
duration
reason
approval
audit
```

An exception must not silently become a permanent policy mutation.

---

# 28. Exception Precedence

Candidate rule:

```text
POLICY
   ↓
EXCEPTION
```

means an exception can alter policy application only where the exception is:

```text
valid
authorized
in scope
unexpired
not revoked
not blocked by a non-overridable invariant
```

Therefore:

```text
EXCEPTION
≠
SECURITY BYPASS
```

---

# 29. Revocation Precedence

Revocation is stronger than the prior authority it withdraws.

Conceptually:

```text
AUTHORITY
 ↓
REVOCATION
 ↓
AUTHORITY NO LONGER AVAILABLE
```

A stale authorization token, approval, or delegation must not remain executable merely because it was valid earlier.

This follows the invalidation analysis of IV-003.

---

# 30. Expiration

Expiration is similar to revocation but temporal.

```text
VALID UNTIL T
```

must not become:

```text
VALID FOREVER
```

after T.

Expiration should therefore be checked at the relevant enforcement boundary.

---

# 31. Emergency Behavior

Emergency behavior is one of the most dangerous precedence areas.

The architecture must distinguish:

```text
EMERGENCY STOP
```

from:

```text
EMERGENCY BYPASS
```

An emergency stop generally reduces execution capability.

An emergency bypass increases capability.

They must not be treated as equivalent.

---

# 32. Emergency Stop

A controlled emergency stop should conceptually have precedence over normal execution:

```text
EMERGENCY STOP
        ↓
NORMAL EXECUTION BLOCKED
```

This is consistent with the existence of an emergency-stop boundary in the security architecture.

The exact reset and recovery semantics remain a contract-level question.

---

# 33. Emergency Bypass

An emergency bypass, if permitted at all, requires a separate contract.

The system must define:

```text
who can invoke it
what controls it can bypass
what controls remain non-overridable
how it expires
how it is audited
what verification follows
how authority is restored
```

Without these semantics:

```text
emergency=true
```

must not become an implicit superuser mode.

---

# 34. Agent Authority

Agent authority should be bounded by:

```text
agent identity
capabilities
scope
delegation
policy
security
constraints
```

Therefore:

```text
CAPABILITY
≠
UNBOUNDED AUTHORITY
```

A tool capability must not itself imply permission to use the tool for every possible purpose.

---

# 35. Capability vs Authorization

These must remain distinct:

```text
CAPABILITY
= what the agent can technically invoke

AUTHORIZATION
= what the agent is permitted to invoke now
```

Therefore:

```text
has_tool_access
≠
authorized_for_action
```

This distinction is especially important in distributed and delegated execution.

---

# 36. Human Authority vs Human Approval

These should not be collapsed.

```text
HUMAN AUTHORITY
```

answers:

```text
what the human is permitted to authorize?
```

while:

```text
HUMAN APPROVAL
```

answers:

```text
what action the human actually approved?
```

A person can possess authority without approving an action.

An approval can also be invalid if:

```text
scope changed
decision changed
authorization expired
security state changed
```

as established in IV-003.

---

# 37. Delegated Human Authority

Delegation should preserve:

```text
scope
duration
constraints
revocation
provenance
```

A delegated human authority must not exceed the authority that was delegated.

Candidate invariant:

```text
delegated_authority
⊆
delegator_authority
```

---

# 38. Multi-Agent Authority

For agent-to-agent delegation:

```text
Agent A
   ↓ delegates
Agent B
   ↓ delegates
Agent C
```

the effective authority must remain bounded by the chain.

Conceptually:

```text
Authority(C)
⊆
Authority(B)
⊆
Authority(A)
```

where each transfer is explicitly permitted.

The exact transitive delegation algorithm remains a deferred decision.

---

# 39. Recommendation Conflict

If:

```text
RECOMMENDATION = ALLOW X
```

but:

```text
CONSTRAINT = DENY X
```

the result must be:

```text
DENY X
```

not:

```text
COMPROMISE
```

`COMPROMISE` is only appropriate where the underlying requirements are semantically compatible and the governing layer permits adjustment.

---

# 40. Human Approval Conflict

If:

```text
HUMAN APPROVAL = ALLOW X
```

but:

```text
SECURITY BOUNDARY = DENY X
```

the runtime must not execute X.

The correct semantic result is:

```text
APPROVED
+
NOT EXECUTABLE
```

This distinction should be explicitly represented rather than collapsing approval and execution eligibility.

---

# 41. Authority Conflict

If:

```text
AGENT A
```

has capability to perform X but lacks current authority:

```text
capability = true
authority = false
```

the action must not execute.

This is another direct application of:

```text
CAPABILITY ≠ AUTHORIZATION
```

---

# 42. Constraint vs Goal Conflict

If:

```text
GOAL = achieve X
CONSTRAINT = X prohibited
```

the system must revise the plan rather than reinterpret the constraint.

Conceptually:

```text
GOAL
 ↓
CONSTRAINT CHECK
 ↓
X prohibited
 ↓
ALTERNATIVE / ABSTENTION / ESCALATION
```

This is consistent with the decision contract's support for candidate comparison, counterfactual alternatives, abstention, and escalation.

---

# 43. Policy vs Goal Conflict

If:

```text
GOAL
```

requires an action prohibited by policy:

```text
GOAL ≠ POLICY EXCEPTION
```

The system should:

```text
replan
abstain
escalate
or invoke a valid exception mechanism
```

depending on authority and contract.

---

# 44. Policy vs Human Request

A human request does not automatically become a policy exception.

The system should distinguish:

```text
REQUEST
```

from:

```text
AUTHORIZED EXCEPTION
```

This prevents natural-language instructions from becoming implicit governance mutations.

---

# 45. Human Approval vs Policy Exception

Where policy requires an explicit exception:

```text
human approval
```

may be a prerequisite but is not necessarily sufficient.

The system must determine:

```text
does this human have exception authority?
is this exception type permitted?
is the scope valid?
```

Only then can the exception be considered effective.

---

# 46. Security vs Policy Exception

Candidate rule:

```text
POLICY EXCEPTION
```

cannot bypass:

```text
NON-OVERRIDABLE SECURITY CONTROL
```

unless the security contract explicitly defines a controlled emergency mechanism.

This boundary should be ratified explicitly.

---

# 47. Security vs Human Authority

Candidate rule:

```text
HUMAN AUTHORITY
```

cannot bypass:

```text
NON-OVERRIDABLE SECURITY CONTROL
```

unless a separately governed emergency authority exists.

This avoids making human governance equivalent to unrestricted root control.

---

# 48. Security vs Agent Authority

Candidate rule:

```text
AGENT AUTHORITY
```

cannot bypass security enforcement.

The agent's execution interface remains downstream of the security boundary.

---

# 49. Security vs Assurance

Assurance claims do not grant execution authority.

A verified system may still deny a particular action because:

```text
current security state
```

does not permit it.

Therefore:

```text
VERIFIED
≠
AUTHORIZED
```

and:

```text
AUTHORIZED
≠
CURRENTLY SECURE
```

---

# 50. Assurance vs Governance

Assurance provides evidence about whether the system satisfies governed properties.

It should not become a runtime authority source.

Therefore:

```text
ASSURANCE RESULT
```

may influence:

```text
confidence
deployment eligibility
escalation
risk
```

but does not itself create permission to execute an otherwise prohibited action.

---

# 51. Governance Decision Procedure

A consequential action should conceptually pass through:

```text
1. IDENTIFY ACTION
       ↓
2. IDENTIFY ACTOR
       ↓
3. IDENTIFY CAPABILITY
       ↓
4. IDENTIFY AUTHORITY
       ↓
5. IDENTIFY DELEGATION
       ↓
6. IDENTIFY APPLICABLE POLICY
       ↓
7. IDENTIFY CONSTRAINTS
       ↓
8. IDENTIFY NON-OVERRIDABLE INVARIANTS
       ↓
9. CHECK SECURITY STATE
       ↓
10. CHECK EXCEPTIONS
       ↓
11. CHECK REQUIRED HUMAN APPROVAL
       ↓
12. CHECK DECISION / PLAN
       ↓
13. CHECK EXECUTION INTENT
       ↓
14. EXECUTE ONLY IF ALL REQUIRED GATES PASS
```

The ordering of individual checks may be optimized at implementation level provided semantic precedence is preserved.

---

# 52. Denial Semantics

A denial should identify the controlling reason.

Conceptually:

```yaml
decision:
  status: DENY
  controlling_layer: SECURITY
  rule_ref: ...
  reason: ...
```

This supports explainability and audit.

A generic:

```text
DENIED
```

is insufficient for governance reconstruction.

---

# 53. Multiple Denials

If multiple layers independently deny an action:

```text
SECURITY = DENY
POLICY = DENY
CONSTRAINT = DENY
```

the system should preserve all applicable failures while identifying the controlling boundary.

This avoids losing evidence of layered violations.

---

# 54. Multiple Approvals

If multiple approvals are required:

```text
human approval
+
security authorization
+
policy exception
```

the system should model them as distinct gates.

It should not concatenate them into:

```text
approved = true
```

because each approval may have different:

```text
scope
issuer
expiration
revocation
authority
target
version
```

---

# 55. Approval Composition

Candidate rule:

```text
ALL REQUIRED APPROVALS
```

must remain valid.

Therefore:

```text
approval_A = valid
approval_B = expired
```

must produce:

```text
execution = NOT ELIGIBLE
```

unless the governing contract explicitly permits another route.

---

# 56. Temporal Precedence

Governance is time-sensitive.

A prior:

```text
ALLOW
```

does not necessarily survive:

```text
REVOCATION
EXPIRATION
POLICY CHANGE
SECURITY CHANGE
DECISION CHANGE
```

Therefore the runtime must evaluate the current governance state at the appropriate enforcement boundary.

This directly inherits IV-003's dependency and invalidation model.

---

# 57. TOCTOU Boundary

A governance check performed at time `T1` may become stale before execution at `T2`.

Conceptually:

```text
CHECK(T1)
 ↓
STATE CHANGES
 ↓
EXECUTE(T2)
```

The system must identify which checks require revalidation immediately before execution.

Security-sensitive controls should not rely on stale authorization state where the security contract requires runtime enforcement.

---

# 58. Governance Snapshot

For consequential execution, the system should preserve:

```yaml
governance_snapshot:
  actor_ref: ...
  capability_refs: []
  authority_refs: []
  delegation_refs: []
  policy_refs: []
  constraint_refs: []
  exception_refs: []
  approval_refs: []
  security_state_ref: ...
  decision_ref: ...
  execution_intent_ref: ...
  timestamp: ...
```

This is a conceptual structure.

The final machine-readable schema belongs to the relevant Phase III contracts and engineering compilation.

---

# 59. Escalation

Escalation is required when the system cannot safely resolve a governance conflict.

Examples:

```text
mandatory + mandatory conflict
unknown authority
unknown policy applicability
unknown exception scope
ambiguous approval
security-state uncertainty
delegation ambiguity
```

The system must not fabricate precedence merely to continue execution.

Engineering already uses structured conflict and knowledge-gap reports for unresolved mandatory conflicts and missing domain knowledge. fileciteturn16file0L19-L45

---

# 60. Abstention

Abstention should be a first-class governance outcome.

Possible results:

```text
ALLOW
DENY
ABSTAIN
ESCALATE
REQUIRES_APPROVAL
REQUIRES_REAUTHORIZATION
REQUIRES_REVALIDATION
```

Abstention is especially appropriate when:

```text
governing precedence is undefined
dependency state is unknown
authority cannot be established
security state cannot be established
```

---

# 61. Emergency Decision Procedure

A controlled emergency path should conceptually be:

```text
EMERGENCY DETECTED
        ↓
CLASSIFY EMERGENCY
        ↓
CHECK EMERGENCY AUTHORITY
        ↓
CHECK NON-OVERRIDABLE CONTROLS
        ↓
EXECUTE MINIMAL AUTHORIZED RESPONSE
        ↓
AUDIT
        ↓
CONTAIN
        ↓
RECOVER
        ↓
REAUTHORIZE
        ↓
REVERIFY
```

The phrase:

```text
EMERGENCY
```

must never automatically mean:

```text
BYPASS ALL CONTROLS
```

---

# 62. Emergency Stop vs Emergency Action

These must remain separate:

```text
EMERGENCY STOP
```

is primarily containment.

```text
EMERGENCY ACTION
```

is an execution request under exceptional conditions.

The latter requires explicit governance semantics.

---

# 63. Governance Failure Modes

The architecture should explicitly test:

```text
HUMAN_APPROVAL_BYPASSES_POLICY
HUMAN_APPROVAL_BYPASSES_SECURITY
AGENT_CAPABILITY_BECOMES_AUTHORITY
DELEGATION_ESCALATES_PRIVILEGE
EXCEPTION_ESCAPES_SCOPE
EXCEPTION_OUTLIVES_EXPIRATION
REVOKED_AUTHORITY_REMAINS_ACTIVE
STALE_APPROVAL_EXECUTES
STALE_POLICY_EXECUTES
STALE_SECURITY_CHECK_EXECUTES
RECOMMENDATION_OVERRIDES_CONSTRAINT
DECISION_OVERRIDES_SECURITY
EXECUTION_INTENT_CREATES_AUTHORITY
EMERGENCY_FLAG_BECOMES_SUPERUSER
ASSURANCE_RESULT_BECOMES_AUTHORIZATION
```

These are required falsification classes for IV-004.

---

# 64. Precedence Test Matrix

| Test | Condition | Required conceptual result |
|---|---|---|
| GOV-001 | Recommendation conflicts with binding constraint | Constraint controls |
| GOV-002 | Human approval conflicts with security deny | Security controls |
| GOV-003 | Agent capability without authority | Deny |
| GOV-004 | Delegate exceeds delegated scope | Deny |
| GOV-005 | Expired approval | Re-approval required |
| GOV-006 | Revoked delegation | Dependent authority blocked |
| GOV-007 | Policy exception outside scope | Exception ineffective |
| GOV-008 | Goal conflicts with constraint | Replan / abstain / escalate |
| GOV-009 | Mandatory governance rules conflict | Escalate |
| GOV-010 | Emergency stop active | Normal execution blocked |
| GOV-011 | Assurance says PASS but current security denies | Deny |
| GOV-012 | Decision changed after approval | Approval revalidation required |
| GOV-013 | Security state changed after authorization | Runtime security recheck |
| GOV-014 | Recommendation says allow but policy denies | Deny |
| GOV-015 | Human request attempts implicit policy mutation | Reject as insufficient authority |
| GOV-016 | Unknown authority provenance | Abstain / escalate |
| GOV-017 | Unknown constraint applicability | Abstain / escalate |
| GOV-018 | Revoked exception | Exception ineffective |
| GOV-019 | Emergency action lacks emergency authority | Deny |
| GOV-020 | Emergency action violates non-overridable control | Deny unless explicit governed emergency mechanism exists |

---

# 65. Required Engineering Evidence

Engineering implementation should demonstrate:

```text
precedence evaluation
authority containment
delegation containment
policy enforcement
constraint enforcement
security enforcement
approval binding
revocation propagation
expiration handling
exception scope
emergency-stop behavior
escalation
auditability
explainability
```

The existing implementation demonstrates several useful patterns:

- mandatory direct conflicts escalate rather than silently choosing a winner; fileciteturn16file0L19-L45
- knowledge gaps are represented through structured escalation metadata; fileciteturn16file6L452-L454
- conflict resolution preserves provenance and objective information; fileciteturn16file6L433-L454
- campaign systems distinguish local correction from global rebase rather than applying global changes indiscriminately. fileciteturn16file2L164-L174

These are engineering precedents, not complete governance semantics.

---

# 66. Open Semantic Questions

## Q1 — Exact precedence

Does the candidate ordering:

```text
security
→ invariant
→ constraint
→ policy
→ authority
→ delegation
→ approval
→ decision
→ execution
→ recommendation
```

become the normative hierarchy?

The current analysis recommends it as a strong candidate but does not claim full ratification.

## Q2 — Human override

Can any human actor override a binding policy?

If yes:

```text
which authority?
which policy classes?
which constraints?
which security boundaries?
```

must be specified.

## Q3 — Emergency authority

Is any emergency action permitted to bypass a normally blocking control?

If yes, which controls remain absolutely non-overridable?

## Q4 — Exception authority

Who can create an exception?

## Q5 — Approval semantics

Does approval mean:

```text
permission
acknowledgement
accountability
authorization
```

or a combination?

## Q6 — Security-policy relationship

Which security controls are non-overridable by policy?

## Q7 — Delegation semantics

Can authority be delegated transitively, and under what constraints?

## Q8 — Conflict resolution

When two binding constraints conflict, is escalation always mandatory?

## Q9 — Governance versioning

Which governance changes require reauthorization of already-created execution intents?

---

# 67. Deferred Decisions

IV-004 intentionally does not freeze:

```text
exact governance precedence enum
exact override API
exact emergency-authority schema
exact exception schema
exact approval schema
exact delegation graph implementation
exact policy engine
exact authorization engine
exact security-policy integration mechanism
exact emergency recovery procedure
exact governance event model
exact enforcement-point placement
exact distributed consistency protocol
```

These remain implementation decisions unless they alter the semantic contract.

---

# 68. Candidate System-Level Invariants

### Invariant 1

No authority source can silently override a non-overridable security boundary.

### Invariant 2

Capability does not imply authorization.

### Invariant 3

Human approval does not by itself bypass security or binding constraints.

### Invariant 4

Delegated authority cannot exceed delegator-authorized transferable scope.

### Invariant 5

Execution intent cannot create authority.

### Invariant 6

Recommendations cannot override binding governance.

### Invariant 7

Policy exceptions are bounded by authority, scope, duration, and applicable non-overridable controls.

### Invariant 8

Revoked authority cannot remain executable merely because it was previously valid.

### Invariant 9

Expired approvals cannot silently authorize current execution.

### Invariant 10

A material decision change may invalidate the approval bound to the previous decision.

### Invariant 11

Emergency status does not automatically grant unrestricted authority.

### Invariant 12

Assurance evidence does not itself create execution permission.

### Invariant 13

Unknown governance applicability must not silently become ALLOW for protected actions.

### Invariant 14

When mandatory governance rules conflict and no authoritative precedence exists, the system must escalate rather than invent a winner.

### Invariant 15

Governance decisions must remain reconstructable from actor, authority, policy, constraints, approvals, security state, decision, and execution-intent references.

---

# 69. Architectural Conclusion

The most important result of IV-004 is that governance cannot safely be represented as:

```text
ALLOW / DENY
```

alone.

The runtime needs to preserve at least:

```text
AUTHORITY
CAPABILITY
POLICY
CONSTRAINT
EXCEPTION
APPROVAL
SECURITY STATE
DECISION
EXECUTION ELIGIBILITY
```

as separate concepts.

The resulting model is closer to:

```text
EXECUTABLE(action, actor, authority, policy, constraints,
           approval, security_state, context, time)
```

than:

```text
authorized(actor, action)
```

The former preserves the layered governance architecture.

---

# 70. Relationship to IV-003

IV-003 established:

```text
VALIDITY IS DEPENDENT
ON UPSTREAM STATE.
```

IV-004 adds:

```text
GOVERNANCE IS LAYERED
AND PRECEDENCE-SENSITIVE.
```

Together:

```text
DEPENDENCY
+
PRECEDENCE
=
GOVERNED EXECUTION
```

An action can therefore be:

```text
historically valid
        +
properly approved
        +
within agent capability
```

and still be:

```text
CURRENTLY NOT EXECUTABLE
```

because a stronger current governance boundary blocks it.

This is the intended architectural consequence.

---

# 71. Exit Criteria

- [x] Governance layers identified
- [x] Authority distinguished from capability
- [x] Authority distinguished from execution permission
- [x] Security boundary distinguished from authority
- [x] Binding constraints distinguished from recommendations
- [x] Policy distinguished from exception
- [x] Human authority distinguished from human approval
- [x] Delegation containment analyzed
- [x] Execution intent distinguished from authority
- [x] Candidate precedence model defined
- [x] Conflict versus precedence distinguished
- [x] Override semantics constrained
- [x] Exception semantics analyzed
- [x] Revocation analyzed
- [x] Expiration analyzed
- [x] Emergency stop distinguished from emergency bypass
- [x] Emergency governance boundary analyzed
- [x] Approval composition analyzed
- [x] Temporal governance analyzed
- [x] TOCTOU implications analyzed
- [x] Governance snapshot proposed
- [x] Escalation and abstention analyzed
- [x] Falsification cases defined
- [x] Test matrix defined
- [x] Engineering evidence incorporated
- [x] Open semantic questions documented
- [x] Deferred decisions documented
- [x] Candidate system-level invariants documented

**Current assessment:** The Phase III architecture strongly supports a layered governance model in which security boundaries, binding constraints, authority, delegation, approval, decision, and execution are distinct semantic objects. A complete normative precedence hierarchy is not yet fully ratified by the source contracts. The highest-risk remaining ambiguity concerns human override and emergency authority.

---

# 72. Next Document

**IV-005 — State, Lifecycle & Transition Consistency Matrix**

IV-005 should now examine the interaction between:

```text
OBJECT LIFECYCLE
AUTHORITY LIFECYCLE
DECISION LIFECYCLE
APPROVAL LIFECYCLE
DELEGATION LIFECYCLE
POLICY LIFECYCLE
SECURITY LIFECYCLE
EVIDENCE LIFECYCLE
EVALUATION LIFECYCLE
ASSURANCE LIFECYCLE
```

The key question becomes:

```text
CAN TWO OBJECTS EACH BE IN A VALID STATE
WHILE THEIR COMBINATION IS INVALID?
```

This will test cross-contract state transitions, terminal-state behavior, rollback, supersession, revocation, recovery, and impossible-state prevention.
