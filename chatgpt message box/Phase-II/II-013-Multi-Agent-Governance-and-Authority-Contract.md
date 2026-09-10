# II-013 — Multi-Agent Governance & Authority Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Depends On:** II-001 through II-012  
**Scope:** Governance, authority boundaries, inter-agent coordination, conflict resolution, delegation, escalation, and prevention of unauthorized agent override

---

## 1. Purpose

II-013 defines how multiple intelligence agents operate as a coordinated system without allowing one agent to silently assume authority outside its domain.

The central problem is:

> **A multi-agent architecture can become less reliable than a single-agent system if capable agents are allowed to override, reinterpret, or silently replace decisions outside their authorized scope.**

Therefore, the architecture must establish explicit:

```text
ROLE
AUTHORITY
SCOPE
INPUTS
OUTPUTS
DECISION RIGHTS
ESCALATION RIGHTS
CHALLENGE RIGHTS
```

for each agent.

---

# 2. Core Principle

> **Agent capability does not imply agent authority.**

Therefore:

```text
CAPABILITY
≠
AUTHORITY
```

and:

```text
CONFIDENCE
≠
AUTHORITY
```

and:

```text
MODEL INTELLIGENCE
≠
DECISION RIGHT
```

An agent may identify a problem outside its authority without being permitted to resolve that problem unilaterally.

---

# 3. Governance Chain

```text
CAMPAIGN OBJECTIVE
        ↓
AUTHORITATIVE CONSTRAINTS
        ↓
DOMAIN OWNERSHIP
        ↓
AGENT AUTHORITY
        ↓
DELEGATED TASK
        ↓
AGENT DECISION
        ↓
VALIDATION
        ↓
DOWNSTREAM CONSUMPTION
```

Each transition must remain explicit.

---

# 4. Agent as Governed Object

Every agent should have a conceptual governance profile:

```text
agent_id
role
domain
authority_scope
allowed_decisions
forbidden_decisions
required_inputs
allowed_outputs
challenge_rights
escalation_rights
evaluation_requirements
provenance_requirements
version
```

The exact schema remains deferred.

---

# 5. Domain Ownership

Each semantic domain should have a designated authority boundary.

Examples:

```text
Knowledge Agent
→ knowledge retrieval / validation

Evidence Agent
→ evidence requirements

Asset Strategy Agent
→ asset planning

Narrative Agent
→ narrative structure

Channel Projection Agent
→ channel adaptation

Prompt Compiler
→ technical prompt compilation

Evaluation Agent
→ requirement evaluation

Recovery Agent
→ recovery planning
```

These examples establish boundaries, not necessarily final agent names.

---

# 6. Authority Types

Potential authority classes include:

```text
READ
PROPOSE
SELECT
APPROVE
REJECT
BLOCK
ESCALATE
MODIFY
```

An agent may possess one authority type without possessing another.

For example:

```text
Evaluator:
READ + EVALUATE + BLOCK

but not:

MODIFY CAMPAIGN INTENT
```

---

# 7. Principle of Least Authority

Each agent should receive only the authority required to perform its role.

```text
MINIMUM REQUIRED AUTHORITY
```

is preferred over:

```text
GLOBAL CAMPAIGN AUTHORITY
```

This limits accidental strategic mutation.

---

# 8. Proposal vs Decision

An agent output should distinguish:

```text
PROPOSAL
```

from:

```text
DECISION
```

A proposal becomes a decision only through the applicable authority mechanism.

Example:

```text
Narrative Agent:
PROPOSE → reorder nodes

Governance:
CHECK → authority

Result:
ACCEPT / REJECT / ESCALATE
```

---

# 9. Agent Output Types

Agent outputs should be typed.

Possible types:

```text
OBSERVATION
CLAIM
PROPOSAL
DECISION
CHALLENGE
EVALUATION
BLOCK
ESCALATION
RECOVERY_PLAN
```

This prevents downstream agents from treating every message as equally authoritative.

---

# 10. Agent Authority Scope

Authority should be scoped by:

```text
OBJECT
DOMAIN
ACTION
CONTEXT
TIME
CAMPAIGN
```

Example:

```text
Asset Strategy Agent

Allowed:
select asset strategy for campaign X.

Not allowed:
change product truth.
```

---

# 11. Authority Inheritance

An agent consuming an authoritative object does not automatically inherit the object's authority.

Example:

```text
Agent receives:
PRODUCT TRUTH

Agent may:
use product truth.

Agent does not automatically gain:
authority to modify product truth.
```

This is mandatory.

---

# 12. Delegation

Authority may be delegated explicitly.

```text
AUTHORITY OWNER
        ↓
DELEGATION
        ↓
AGENT
```

Delegation should specify:

```text
scope
action
duration
conditions
limits
```

Delegated authority must be revocable.

---

# 13. Delegation Does Not Transfer Ownership

Delegating an action does not necessarily transfer semantic ownership.

Example:

```text
Campaign Owner
→ delegates asset selection

Asset Agent
→ selects asset

Campaign Owner
→ remains authority owner
```

This distinction must remain explicit.

---

# 14. Agent Challenge Rights

Agents should be able to challenge decisions when they detect:

```text
constraint violation
evidence insufficiency
authority violation
knowledge conflict
unsafe assumption
strategic drift
```

Challenge rights do not automatically grant override rights.

```text
CHALLENGE
≠
OVERRIDE
```

---

# 15. Agent Block Rights

Some agents may possess the right to block downstream execution when a critical invariant is violated.

Example:

```text
Evaluation Agent:
Critical evidence requirement FAIL

Result:
BLOCK
```

The blocking authority must be explicitly scoped.

---

# 16. Override Authority

Override must be rare and explicitly governed.

An agent should never override another agent merely because:

```text
its confidence is higher
its model is larger
its output sounds more convincing
```

Override requires an established authority rule.

---

# 17. Conflict Types

Potential agent conflicts include:

```text
FACTUAL CONFLICT
EVIDENCE CONFLICT
STRATEGIC CONFLICT
CONSTRAINT CONFLICT
AUTHORITY CONFLICT
RESOURCE CONFLICT
CHANNEL CONFLICT
TEMPORAL CONFLICT
```

The conflict class determines the appropriate resolution path.

---

# 18. Conflict Resolution Hierarchy

Conceptually:

```text
HARD AUTHORITY
    ↓
HARD CONSTRAINT
    ↓
PRODUCT TRUTH
    ↓
LOCKED INTENT
    ↓
REQUIRED EVIDENCE
    ↓
DOMAIN DECISION
    ↓
SOFT PREFERENCE
    ↓
OPTIMIZATION
```

This is a provisional hierarchy and must be reconciled against earlier ratified laws and authority definitions before implementation.

---

# 19. Conflict Resolution Principle

When two agents disagree:

```text
DO NOT ASK:
Which model sounds smarter?

ASK:
Which agent has authority over this decision?
```

If neither agent has sufficient authority:

```text
ESCALATE
```

---

# 20. Cross-Domain Conflict

Example:

```text
Material Agent:
Requires lighting A.

Editorial Agent:
Prefers lighting B.
```

The system should determine:

```text
Is this a hard material requirement?
Is the editorial preference soft?
Can both be satisfied?
```

The architecture should attempt reconciliation before selecting one agent's preference.

---

# 21. Constraint Reconciliation

When constraints conflict:

```text
CONSTRAINT A
+
CONSTRAINT B
```

the system should attempt:

```text
JOINT SATISFACTION
```

before:

```text
TRADE-OFF
```

If trade-off is necessary:

```text
TRADE-OFF
→ record affected requirements
→ record authority
→ evaluate consequences
```

---

# 22. Agent Communication

Agent-to-agent communication should preserve typed messages.

Conceptually:

```text
sender
receiver
message_type
object
object_version
claim
authority
request
response
timestamp
provenance
```

Free-form natural language should not be the only governance mechanism.

---

# 23. Shared Blackboard

The architecture may use a shared state / blackboard model.

If so:

```text
BLACKBOARD
```

must distinguish:

```text
OBSERVATION
CLAIM
PROPOSAL
DECISION
LOCK
CHALLENGE
EVALUATION
```

Agents must not treat all blackboard entries as equivalent.

---

# 24. State Ownership

Every mutable semantic object should have an owner.

Example:

```text
Intent
→ Intent Authority

Evidence Requirement
→ Evidence Authority

Asset Strategy
→ Asset Strategy Authority

Narrative
→ Narrative Authority
```

Consumers may read these objects without becoming their owners.

---

# 25. Locking

Certain objects may become locked after ratification or approval.

A lock should specify:

```text
object
version
lock_scope
authority
unlock_condition
```

Locked objects cannot be silently mutated.

---

# 26. Unlocking

Unlocking requires explicit authorization.

Possible triggers:

```text
new evidence
authority decision
architecture change
critical failure
user instruction
```

The unlock event must be recorded in provenance.

---

# 27. Stale Agent Output

An agent may produce a valid decision using an outdated input.

Example:

```text
Agent A:
uses Evidence v2

Evidence:
now v3
```

The governance layer should detect:

```text
STALE OUTPUT
```

and determine whether re-evaluation is required.

---

# 28. Agent Output Trust

An output should become trusted according to:

```text
authority
validation
provenance
evaluation
```

not simply:

```text
agent identity
```

---

# 29. Trust Is Scoped

Trust should be represented as:

```text
AGENT
+
DOMAIN
+
ACTION
+
CONTEXT
```

rather than:

```text
Agent X is trusted.
```

An agent can be reliable for:

```text
visual analysis
```

while being unauthorized for:

```text
product truth
```

---

# 30. Self-Critique Agent Governance

The Self-Critique Agent should have authority to:

```text
inspect
challenge
identify weaknesses
request re-evaluation
escalate
```

It should not automatically have authority to:

```text
rewrite the target decision
```

unless explicitly delegated.

---

# 31. Adversarial Verification Agent Governance

The Adversarial Verification Agent should be granted explicit challenge authority.

It should be able to:

```text
attack
invalidate
flag
block
escalate
```

within defined scopes.

It must not modify the system under test merely to manufacture a failure.

---

# 32. Evaluator Governance

The Evaluation Agent may:

```text
evaluate
PASS
PARTIAL
FAIL
UNCERTAIN
NOT_EVALUABLE
BLOCK
ESCALATE
```

It should not silently repair the object it evaluates.

---

# 33. Recovery Agent Governance

The Recovery Agent may:

```text
diagnose
propose recovery
rank recovery options
request re-generation
request re-planning
escalate
abort
```

It should not silently change locked campaign intent.

---

# 34. Human Authority

Human authority must remain explicit.

Potential human roles:

```text
CAMPAIGN OWNER
PRODUCT OWNER
DOMAIN EXPERT
REVIEWER
OPERATOR
```

A human role should not be treated as globally authoritative for every domain unless explicitly defined.

---

# 35. Human Override

Human override should preserve:

```text
who
what
why
scope
previous decision
new decision
timestamp
```

Human override does not eliminate the need for provenance or later evaluation.

---

# 36. Governance Failure

The system should identify:

```text
UNAUTHORIZED DECISION
AUTHORITY OVERREACH
CONFLICTING DECISION
STALE DECISION
MISSING OWNER
MISSING AUTHORITY
CIRCULAR DELEGATION
UNSCOPED OVERRIDE
```

These are governance failures, not merely model errors.

---

# 37. Governance Recovery

A governance failure should trigger:

```text
DETECT
 ↓
FREEZE AFFECTED DECISION
 ↓
IDENTIFY AUTHORITY
 ↓
REVIEW
 ↓
REPLAN / ESCALATE
```

The system should prevent downstream propagation of an unauthorized decision where practical.

---

# 38. Multi-Agent Consensus

Consensus may be useful but must not become the primary authority mechanism.

```text
CONSENSUS
≠
AUTHORITY
```

Five unauthorized agents agreeing do not become more authorized through agreement.

---

# 39. Dissent Preservation

If agents disagree materially, the system should preserve:

```text
agent A position
agent B position
supporting evidence
authority scope
resolution
```

Dissent is valuable evaluation data.

---

# 40. Governance and Architecture Proof

The architecture should eventually test:

```text
Can agents stay within their authority?
Can unauthorized agents be prevented from overriding owners?
Can conflicts be resolved according to authority rather than model confidence?
Can stale outputs be detected?
Can dissent be preserved?
Can adversarial agents challenge without becoming uncontrolled actors?
```

These are falsifiable governance properties.

---

# 41. Self-Critique Requirements

The Self-Critique Agent should inspect governance for:

- authority overreach,
- ambiguous ownership,
- hidden delegation,
- unauthorized mutation,
- stale dependencies,
- unjustified consensus,
- suppressed dissent,
- circular authority,
- and accidental role expansion.

---

# 42. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to:

1. Make a low-authority agent override a high-authority object.
2. Exploit ambiguous authority scopes.
3. Create fake delegation.
4. Use confidence to bypass authority.
5. Create stale decisions.
6. Hide conflicts.
7. Manufacture consensus.
8. Suppress dissent.
9. Modify locked objects.
10. Exploit evaluator authority to rewrite targets.
11. Exploit recovery authority to mutate strategy.
12. Create circular delegation.
13. Bypass human approval requirements.
14. Create unauthorized cross-domain decisions.
15. Turn challenge authority into unrestricted override authority.

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

# 43. Validation Invariants

### Invariant 1

Agent capability does not imply authority.

### Invariant 2

Every consequential agent decision has an explicit authority scope.

### Invariant 3

Agent outputs are typed.

### Invariant 4

Proposal and decision remain distinct.

### Invariant 5

Authority inheritance is not automatic.

### Invariant 6

Delegation is explicit and scoped.

### Invariant 7

Challenge does not imply override.

### Invariant 8

Consensus does not create authority.

### Invariant 9

Locked objects cannot be silently mutated.

### Invariant 10

Stale agent outputs are detectable.

### Invariant 11

Agent conflicts are resolved by authority and constraints, not model confidence.

### Invariant 12

Dissent remains auditable.

### Invariant 13

Governance failures cannot silently propagate.

### Invariant 14

Self-Critique cannot silently rewrite governed decisions.

### Invariant 15

Adversarial Verification cannot modify the system under test merely to manufacture evidence.

### Invariant 16

Every delegation and override preserves provenance.

---

# 44. Falsifiable Architectural Hypotheses

## Hypothesis A — Explicit authority scopes reduce unauthorized agent mutation

**Experiment:**

Inject cross-domain decisions into a multi-agent environment.

Compare:

```text
implicit role prompting
vs
explicit authority governance
```

Measure unauthorized mutation rate.

---

## Hypothesis B — Authority-based conflict resolution outperforms confidence-based resolution

**Experiment:**

Create conflicts where the lower-authority agent has higher model confidence.

Expected:

```text
authority determines decision rights
```

Measure governance violations.

---

## Hypothesis C — Typed messages reduce semantic misinterpretation

**Experiment:**

Compare free-form agent communication against typed message contracts.

Measure:

```text
proposal treated as decision
observation treated as fact
challenge treated as override
```

---

## Hypothesis D — Dissent preservation improves conflict diagnosis

**Experiment:**

Compare systems that collapse disagreements against systems that preserve dissent.

Measure root-cause and resolution accuracy.

---

## Hypothesis E — Stale-output detection reduces invalid downstream decisions

**Experiment:**

Change upstream objects after downstream agents have computed decisions.

Measure whether stale outputs are detected before execution.

---

# 45. Governance Evaluation

The governance layer should eventually expose:

```text
AUTHORITY VIOLATIONS
UNAUTHORIZED MUTATIONS
STALE OUTPUT RATE
CONFLICT RESOLUTION ACCURACY
DELEGATION INTEGRITY
DISSENT PRESERVATION
LOCK VIOLATIONS
ESCALATION ACCURACY
```

These metrics should remain diagnostic rather than collapsing into one opaque governance score.

---

# 46. Governance Dataset

The architecture should eventually maintain test cases covering:

```text
VALID DELEGATION
INVALID DELEGATION
AUTHORITY CONFLICT
CROSS-DOMAIN CONFLICT
STALE OUTPUT
LOCK VIOLATION
UNAUTHORIZED OVERRIDE
FALSE CONSENSUS
SUPPRESSED DISSENT
CIRCULAR AUTHORITY
ADVERSARIAL AGENT
HUMAN OVERRIDE
ESCALATION
```

Each case should preserve expected authority and expected terminal behavior.

---

# 47. Core Contract

> **The Multi-Agent Governance Layer shall define explicit authority, ownership, delegation, communication, challenge, blocking, escalation, and override boundaries for every intelligence agent. It shall prevent capability or confidence from becoming implicit authority, preserve proposal-versus-decision semantics, detect stale and unauthorized outputs, resolve conflicts according to scoped authority and constraints, preserve dissent, protect locked objects, and expose governance behavior to self-critique and adversarial verification.**

---

# 48. Deferred Decisions

II-013 does not freeze:

- final agent roster,
- orchestration framework,
- communication transport,
- blackboard implementation,
- authorization database,
- identity system,
- permission syntax,
- lock implementation,
- human approval UI,
- distributed execution model.

These remain engineering decisions.

---

# 49. Exit Criteria

II-013 is semantically complete when:

- [x] Agent authority defined
- [x] Capability / authority distinction established
- [x] Domain ownership established
- [x] Authority types established
- [x] Least-authority principle established
- [x] Proposal / decision distinction established
- [x] Typed outputs established
- [x] Authority scope established
- [x] Authority inheritance restriction established
- [x] Delegation established
- [x] Challenge rights established
- [x] Block rights established
- [x] Override restrictions established
- [x] Conflict taxonomy established
- [x] Conflict resolution principle established
- [x] Cross-domain reconciliation established
- [x] Agent communication contract established
- [x] Shared-blackboard semantics established
- [x] State ownership established
- [x] Locking established
- [x] Stale-output detection established
- [x] Agent trust scope established
- [x] Self-Critique governance established
- [x] Adversarial governance established
- [x] Human authority established
- [x] Governance failure handling established
- [x] Consensus / authority distinction established
- [x] Dissent preservation established
- [x] Architecture-proof role established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established
- [x] Governance evaluation established
- [x] Governance dataset established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-014 — Intelligence Object Lifecycle & State Contract**

This specification will define the lifecycle of every major intelligence object — creation, validation, approval, locking, consumption, invalidation, revision, archival, and retirement — and how object state interacts with authority, provenance, evaluation, and multi-agent governance.
