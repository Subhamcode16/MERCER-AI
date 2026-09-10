# III-005 — Agent Contract, Capability Boundary & Execution Interface

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001, III-002, III-003, III-004 and the ratified Phase II semantic architecture  
**Purpose:** Define the machine-readable contract for Intelligence Agents, including identity, role, capabilities, authority references, inputs, outputs, tools, execution permissions, constraints, handoff, delegation, failure, abstention, resource controls, self-critique, adversarial verification, provenance obligations, and lifecycle interaction.

---

# 1. Purpose

III-005 defines what an Intelligence Agent is allowed to be within the architecture.

The central boundary is:

```text
AGENT CAPABILITY
        ≠
AGENT AUTHORITY
```

An agent may technically possess a capability while lacking authority to use it in a particular context.

The agent contract therefore exists to make the following explicit:

```text
WHO IS THE AGENT?
WHAT ROLE DOES IT HAVE?
WHAT CAN IT DO?
WHAT MAY IT DO HERE?
WHAT INPUTS MAY IT CONSUME?
WHAT OUTPUTS MAY IT PRODUCE?
WHAT TOOLS MAY IT USE?
WHAT CONSTRAINTS APPLY?
WHEN MUST IT ABSTAIN?
HOW IS ITS WORK VERIFIED?
HOW IS ITS WORK RECORDED?
```

---

# 2. Agent as a Governed Intelligence Object

An agent is not an unrestricted autonomous actor.

It participates in the architecture through:

```text
IDENTITY
+
CAPABILITY
+
AUTHORITY
+
CONSTRAINTS
+
EXECUTION CONTRACT
+
PROVENANCE
+
LIFECYCLE
```

The agent contract must therefore integrate with III-001 through III-004 rather than creating parallel semantics.

---

# 3. Agent Identity

Every agent must have a globally unique identity.

Recommended conceptual form:

```text
AGT-<ULID>
```

The identifier must be:

```text
globally unique
stable
non-semantic
non-reusable
```

Agent identity must not encode:

```text
model name
role
provider
authority level
environment
```

Those are separate attributes.

---

# 4. Agent Version

Every agent implementation or contract version must be explicitly identifiable.

Conceptually:

```yaml
agent_version:
  major: 1
  minor: 0
  patch: 0
```

An agent identity represents the logical agent.

A version represents a particular contract / implementation revision.

---

# 5. Agent Schema Version

The agent contract itself must carry:

```text
schema_version
```

This must remain distinct from:

```text
agent_version
```

and:

```text
model_version
```

Therefore:

```text
agent identity
≠
agent contract version
≠
model version
```

---

# 6. Agent Role

Every agent must declare its role.

Examples:

```text
planner
retriever
reasoner
evaluator
critic
adversarial_verifier
executor
orchestrator
recovery_agent
research_agent
```

The role describes intended responsibility.

It does not itself grant authority.

Therefore:

```text
ROLE
≠
AUTHORITY
```

---

# 7. Role Boundary

An agent must not infer additional responsibilities merely because it can technically perform them.

For example:

```text
ROLE = EVALUATOR
```

does not automatically grant:

```text
APPROVE
COMMIT
EXECUTE
```

authority.

Those permissions must be explicitly resolved through III-002.

---

# 8. Capability

Capabilities describe what an agent is technically able to perform.

Conceptually:

```yaml
capabilities:
  - read_object
  - generate_candidate
  - evaluate
  - invoke_tool
```

Capability declarations must be explicit.

---

# 9. Capability Registry

Capabilities should come from a controlled registry.

Avoid arbitrary strings created independently by each agent.

Conceptually:

```text
CAPABILITY
→ capability_id
→ description
→ input requirements
→ output contract
→ risk classification
```

The exact registry is an implementation concern unless a capability changes architectural semantics.

---

# 10. Capability Is Not Permission

The following must remain separate:

```text
CAPABILITY
→ technical possibility

AUTHORITY
→ permitted action

LIFECYCLE
→ state eligibility

POLICY
→ contextual constraints
```

Execution eligibility therefore becomes:

```text
CAPABILITY
+
AUTHORITY
+
LIFECYCLE
+
POLICY
+
INPUT VALIDITY
=
ELIGIBLE ACTION
```

---

# 11. Authority Reference

An agent must reference its authority context rather than embedding authority into its role.

Conceptually:

```yaml
authority_refs:
  - authority_id: AUTH-...
```

The runtime resolves effective authority through III-002.

---

# 12. Agent Inputs

Every agent must define its accepted inputs.

Conceptually:

```yaml
inputs:
  - object_type: ...
    schema_version: ...
    required: true
```

The agent must not silently accept arbitrary object structures.

---

# 13. Input Validation

Before processing an input, the agent interface should verify:

```text
object identity
object version
object type
schema compatibility
lifecycle eligibility
authority context
provenance availability
```

The agent should not be responsible for independently reinventing these systems.

It invokes the canonical contracts.

---

# 14. Input Trust Boundary

An input object is not trusted merely because:

```text
another agent produced it
```

or:

```text
it exists in the runtime
```

The input must pass applicable validation.

---

# 15. Agent Outputs

Every agent must define its output contract.

Conceptually:

```yaml
outputs:
  - object_type: ...
    schema_version: ...
```

The output must be a valid Intelligence Object or an explicitly defined control result.

---

# 16. Output Authority Boundary

Producing an output does not automatically grant permission to:

```text
approve
commit
publish
execute
override
```

The output enters the applicable lifecycle and authority contracts.

---

# 17. Proposed vs Committed Output

Agents should distinguish between:

```text
PROPOSED OUTPUT
```

and:

```text
COMMITTED OUTPUT
```

An agent may generate a proposal without having authority to commit it.

This is a foundational safety boundary.

---

# 18. Tool Access

Tools must be explicitly declared.

Conceptually:

```yaml
tools:
  - tool_id: ...
    capability_ref: ...
```

An agent must not discover arbitrary runtime tools and treat their availability as permission.

---

# 19. Tool Invocation

A tool invocation should resolve:

```text
agent
+
tool
+
capability
+
authority
+
input
+
object context
```

before execution.

Conceptually:

```text
AGENT REQUEST
 ↓
CAPABILITY CHECK
 ↓
AUTHORITY CHECK
 ↓
INPUT CHECK
 ↓
TOOL POLICY
 ↓
EXECUTE
```

---

# 20. Tool Results

Tool results become inputs or evidence.

They must not automatically become:

```text
truth
authority
approval
```

Tool output requires applicable validation and provenance.

---

# 21. Execution Permissions

Execution permission is not equivalent to tool possession.

An agent may have:

```text
tool capability
```

without having:

```text
permission to invoke that tool
```

in a particular context.

---

# 22. Constraints

Agents must declare applicable constraints.

Examples:

```text
allowed object types
allowed domains
maximum resource usage
forbidden operations
required evidence
required human approval
maximum delegation depth
```

Constraints are cumulative unless the governing policy explicitly states otherwise.

---

# 23. Constraint Non-Bypass

An agent must not bypass a constraint because:

```text
model confidence is high
deadline is near
tool is available
another agent suggested it
execution would be easier
```

A constraint can only be changed through an authorized architectural or governance mechanism.

---

# 24. Execution Context

Each agent execution should have an explicit execution context.

Conceptually:

```yaml
execution_context:
  execution_id: EXE-...
  request_id: REQ-...
  agent_id: AGT-...
  agent_version: ...
  object_refs: []
  authority_refs: []
  correlation_id: ...
```

This connects execution to provenance.

---

# 25. Execution Isolation

An agent execution must not silently inherit unrelated context.

Context should be explicitly passed or resolved.

This reduces:

```text
authority leakage
data leakage
stale-context use
cross-task contamination
```

---

# 26. Context Scope

Agent context should distinguish:

```text
task context
object context
authority context
runtime context
historical context
```

Do not flatten these into an untyped memory blob.

---

# 27. Resource Budget

Where applicable, every agent execution may have:

```text
token budget
time budget
tool-call budget
memory budget
compute budget
cost budget
```

The runtime should enforce these limits.

A budget is a constraint, not authority.

---

# 28. Timeout

Agent executions should have explicit timeout behavior where appropriate.

A timeout must produce a structured result such as:

```text
TIMEOUT
```

rather than silently appearing as:

```text
SUCCESS
```

---

# 29. Failure

Agent failure must be represented explicitly.

Conceptually:

```yaml
failure:
  code: ...
  category: ...
  recoverable: ...
  message: ...
  provenance_ref: ...
```

Failure is an outcome, not necessarily an object invalidation.

---

# 30. Failure Classification

Potential categories include:

```text
INPUT_INVALID
AUTHORITY_DENIED
CONSTRAINT_VIOLATION
TOOL_FAILURE
TIMEOUT
RESOURCE_EXHAUSTED
MODEL_FAILURE
SCHEMA_FAILURE
PROVENANCE_FAILURE
DEPENDENCY_FAILURE
UNKNOWN
```

The definitive taxonomy is deferred to the implementation contract.

---

# 31. Abstention

Agents must have an explicit abstention mechanism.

An agent should abstain when:

```text
required information is missing
authority cannot be established
constraints conflict
evidence is insufficient
output contract cannot be satisfied
confidence / uncertainty requirements are not met
verification cannot be completed
```

Abstention is a valid result.

---

# 32. Abstention Is Not Failure

The architecture must distinguish:

```text
FAILURE
```

from:

```text
ABSTENTION
```

Failure means the agent attempted an allowed operation and could not complete it.

Abstention means the agent correctly declined to make an unsupported or unauthorized decision.

---

# 33. Escalation

When an agent cannot safely proceed, it may return:

```text
ESCALATE
```

The escalation must specify:

```text
reason
missing information
required authority
blocking constraint
recommended next actor / contract
```

---

# 34. Handoff

Agents may hand work to another agent.

A handoff must preserve:

```text
source agent
target agent
task context
object refs
object versions
authority context
constraints
provenance
reason
```

---

# 35. Handoff Does Not Transfer Authority Automatically

A handoff does not automatically transfer authority.

Therefore:

```text
AGENT A AUTHORITY
        ≠
AGENT B AUTHORITY
```

The receiving agent must resolve its own effective authority.

---

# 36. Delegation

Where delegation is permitted, it must use III-002.

The agent contract must not implement a separate delegation system.

Conceptually:

```text
AGENT
 ↓
DELEGATION REQUEST
 ↓
AUTHORITY CONTRACT
 ↓
DELEGATED AUTHORITY
 ↓
TARGET AGENT
```

---

# 37. Delegation Containment

The receiving agent must never receive more authority than the source delegation permits.

```text
DELEGATED AGENT AUTHORITY
⊆
SOURCE AUTHORITY
```

---

# 38. Self-Critique Interface

The architecture explicitly supports a self-critique agent/interface.

A producing agent may request critique of its output.

Conceptually:

```text
PRODUCER
 ↓
OUTPUT
 ↓
CRITIC
 ↓
CRITIQUE OBJECT
```

The critique must be represented independently from the original output.

---

# 39. Self-Critique Independence

Self-critique must not be treated as proof of correctness.

A critic that shares:

```text
same model
same context
same assumptions
same failure mode
```

may reproduce the original error.

Therefore:

```text
SELF-CRITIQUE
≠
INDEPENDENT VERIFICATION
```

---

# 40. Adversarial Self-Verification Interface

The architecture also explicitly supports an adversarial verifier.

Its purpose is not merely to review the output.

It must attempt to:

```text
break
falsify
contradict
stress
invalidate
```

the target implementation or output.

Conceptually:

```text
OUTPUT
 ↓
ADVERSARIAL VERIFIER
 ↓
ATTACK
 ↓
OBSERVED RESULT
 ↓
VERIFICATION RECORD
```

---

# 41. Critic / Adversary Separation

The architecture should distinguish:

```text
CRITIC
→ searches for defects / weaknesses

ADVERSARIAL VERIFIER
→ actively attempts to construct failure
```

They may share infrastructure, but their contracts and evaluation objectives must remain distinguishable.

---

# 42. Verification Independence

Where an evaluation claim requires independent verification, the verifier should minimize shared failure modes with the producer.

Possible independence dimensions include:

```text
different model
different prompt
different reasoning path
different implementation
different data slice
different evaluator
```

The exact independence protocol is deferred to the evaluation contract.

---

# 43. No Self-Approval

An agent must not approve its own consequential output unless the architecture explicitly permits that operation.

Even then, approval must remain a separate authority decision.

Therefore:

```text
PRODUCE
≠
APPROVE
```

---

# 44. Verification Result

A verifier should produce a structured result such as:

```text
PASS
FAIL
INCONCLUSIVE
NOT_TESTED
```

The result must include:

```text
target version
verification protocol
evidence
attack / test cases
timestamp
verifier identity
```

---

# 45. Verification Does Not Equal Truth

A successful verification result establishes only what the verification protocol tested.

Therefore:

```text
VERIFICATION PASS
≠
UNIVERSAL CORRECTNESS
```

The evaluation contract must define the claim being supported.

---

# 46. Self-Improvement Boundary

An agent may generate:

```text
critique
repair proposal
new candidate
```

but must not silently replace its own production implementation.

Self-modification requires explicit lifecycle and authority control.

---

# 47. Repair Proposal

A repair agent may produce:

```yaml
repair_proposal:
  target_version: ...
  failure_refs: []
  proposed_change: ...
  expected_effect: ...
  risk: ...
```

The proposal must enter the normal lifecycle.

---

# 48. Recursive Verification

A repaired implementation may be sent through:

```text
repair
 ↓
self-critique
 ↓
adversarial verification
 ↓
evaluation
 ↓
approval
```

The system must preserve each iteration's provenance.

---

# 49. Verification Regression

A repair that fixes one failure must be tested against:

```text
previous failures
+
known regressions
+
new adversarial cases
```

A repair must not be considered safe merely because the triggering test now passes.

---

# 50. Agent Lifecycle

Agent implementations should themselves have lifecycle semantics.

Conceptually:

```text
DRAFT
 ↓
VALIDATING
 ↓
VALID
 ↓
APPROVED
 ↓
ACTIVE
 ↓
DEPRECATED / SUSPENDED / RETIRED
```

The exact state registry must remain compatible with III-003.

An agent cannot activate itself by writing its own state.

---

# 51. Agent Activation

Activation requires:

```text
valid agent contract
+
required evaluation
+
required authority
+
runtime compatibility
```

The exact activation policy is deferred.

---

# 52. Agent Suspension

An agent may be suspended due to:

```text
security failure
repeated verification failure
authority revocation
resource violation
contract incompatibility
operational incident
```

Suspension should preserve provenance.

---

# 53. Agent Retirement

Retirement prevents normal activation while preserving historical reconstruction.

Historical executions remain attributable to the retired agent version.

---

# 54. Model / Agent Separation

An agent is not equivalent to a model.

An agent may specify:

```text
role
tools
policies
capabilities
contracts
verification behavior
```

while using a model as one implementation component.

Therefore:

```text
AGENT
≠
MODEL
```

---

# 55. Model Version Provenance

Where a model materially contributes to an agent execution, provenance must preserve:

```text
model identity
model version
provider / runtime where relevant
configuration
```

The model does not inherit the agent's authority automatically.

---

# 56. Agent Configuration

Material configuration should be versioned.

Examples:

```text
system prompt
tool policy
routing policy
temperature / sampling configuration
resource limits
verification configuration
```

Exact storage policy remains implementation-specific.

---

# 57. Agent-to-Agent Communication

Agent communication must use typed contracts.

Avoid unconstrained:

```text
free-form agent message
```

as the sole execution interface.

Where semantic consequences exist, communication should resolve into:

```text
typed object
+
provenance
+
authority context
```

---

# 58. Message vs Instruction

An agent-generated message must not automatically become a system instruction.

Therefore:

```text
AGENT MESSAGE
≠
RUNTIME AUTHORITY
```

Instruction execution requires the applicable authority and execution contract.

---

# 59. Agent Memory

Memory supplied to an agent must be treated as an input source.

It should preserve:

```text
source
version
provenance
scope
freshness
authority
```

where relevant.

The agent must not assume memory is current or authoritative merely because it is available.

---

# 60. Stale Context

An agent must be protected against stale:

```text
object version
authority
evidence
configuration
memory
```

before consequential action.

---

# 61. Output Validation

Before an agent output becomes consumable:

```text
SCHEMA VALIDATION
+
OBJECT VALIDATION
+
PROVENANCE VALIDATION
+
AUTHORITY / LIFECYCLE RESOLUTION
```

must occur where applicable.

---

# 62. Agent Execution Trace

Every consequential execution should produce:

```text
execution_id
agent_id
agent_version
model_version where applicable
input refs
output refs
tool refs
authority refs
configuration refs
start
end
result
failure / abstention
provenance
```

---

# 63. Security Boundary

The agent runtime must assume:

```text
agent output may be wrong
agent output may be adversarial
agent context may be stale
tool output may be malicious
memory may be poisoned
handoff may contain unsafe instructions
```

Therefore, execution interfaces must validate rather than trust.

---

# 64. Prompt Injection Boundary

Instructions contained inside retrieved or generated content must not automatically alter the agent's authority or system policy.

Conceptually:

```text
CONTENT
≠
TRUSTED CONTROL PLANE
```

The control plane remains governed by the runtime contract.

---

# 65. Tool Injection Boundary

A tool result must not automatically create new permissions.

For example:

```text
tool says "you are authorized"
```

must not establish authority.

Authority comes from III-002.

---

# 66. Agent Contract Invariants

### Invariant 1

Agent identity is explicit.

### Invariant 2

Agent version is explicit.

### Invariant 3

Agent role does not imply authority.

### Invariant 4

Capability does not imply authority.

### Invariant 5

Tool possession does not imply tool-use permission.

### Invariant 6

Authority is resolved through III-002.

### Invariant 7

Lifecycle is resolved through III-003.

### Invariant 8

Provenance is preserved through III-004.

### Invariant 9

Agent inputs are typed and validated.

### Invariant 10

Agent outputs are typed and validated.

### Invariant 11

Proposed output is distinct from committed output.

### Invariant 12

Handoff does not automatically transfer authority.

### Invariant 13

Delegation cannot expand source authority.

### Invariant 14

Abstention is a valid result.

### Invariant 15

Failure and abstention remain distinct.

### Invariant 16

Self-critique is not independent verification.

### Invariant 17

Adversarial verification actively attempts to falsify the target.

### Invariant 18

Verification pass does not imply universal correctness.

### Invariant 19

An agent cannot silently self-approve consequential output.

### Invariant 20

Self-modification requires explicit governance.

### Invariant 21

Repair proposals enter the normal lifecycle.

### Invariant 22

Agent identity is distinct from model identity.

### Invariant 23

Historical executions remain attributable to exact agent versions.

### Invariant 24

Agent messages do not automatically become runtime instructions.

### Invariant 25

Retrieved content does not automatically become trusted control-plane input.

### Invariant 26

Tool output does not create authority.

### Invariant 27

Stale context must not silently drive consequential actions.

### Invariant 28

Implementation must not invent agent semantics.

---

# 67. Required Tests

The reference implementation must test:

```text
identity resolution
capability resolution
authority mismatch
role/authority confusion
tool permission failure
input schema failure
output schema failure
stale input
stale authority
handoff
handoff authority leakage
delegation containment
abstention
failure classification
timeout
resource exhaustion
self-critique
adversarial verification
verification independence
self-approval attempt
self-modification attempt
repair regression
agent suspension
agent retirement
prompt injection
tool injection
memory poisoning
```

---

# 68. Falsification Cases

Deliberately attempt:

```text
agent with capability but no authority
agent with role but no permission
agent invokes undeclared tool
agent invokes declared tool outside scope
agent approves its own output
agent modifies its own contract
agent bypasses lifecycle
agent bypasses provenance
handoff transfers authority implicitly
delegate exceeds authority
stale authority is replayed
tool output claims authorization
retrieved text injects control instruction
memory supplies false authority
critic repeats producer error
adversary cannot access target version
repair fixes one test but regresses another
```

---

# 69. Agent Execution Benchmark

A consequential agent benchmark should record:

```text
INPUT
CAPABILITY SET
AUTHORITY SET
CONSTRAINTS
TOOLS
MODEL VERSION
OUTPUT
CRITIQUE
ADVERSARIAL ATTACKS
EVALUATION
FINAL DECISION
```

This enables independent reconstruction and comparison between agent configurations.

---

# 70. Agent Reliability Is Multi-Dimensional

Do not collapse agent quality into a single score.

At minimum distinguish:

```text
task performance
constraint compliance
authority compliance
provenance completeness
verification robustness
abstention quality
failure recovery
adversarial robustness
```

A single aggregate score may hide critical failure modes.

---

# 71. Self-Critique Evaluation

Self-critique should be evaluated on:

```text
defect detection rate
false criticism rate
missed critical defects
correction usefulness
agreement with independent evaluation
```

It must not be credited merely because the critic produces a critique.

---

# 72. Adversarial Verification Evaluation

Adversarial verification should be evaluated on:

```text
attack coverage
failure discovery rate
false attack rate
reproducibility
novel failure discovery
regression detection
```

A verifier that never finds failures may be:

```text
effective
```

or:

```text
too weak
```

Therefore raw pass rates are insufficient.

---

# 73. Independence Benchmark

Where we claim independent verification, measure shared failure modes between:

```text
producer
critic
adversary
evaluator
```

Independence should be demonstrated empirically where possible rather than asserted from different agent names.

---

# 74. Deferred Decisions

III-005 intentionally does not freeze:

- exact agent runtime;
- agent framework;
- model provider;
- model routing;
- tool registry technology;
- resource accounting implementation;
- exact capability taxonomy;
- final agent-state registry;
- exact handoff transport;
- exact delegation transport;
- self-critique model-selection strategy;
- adversarial-verifier model-selection strategy;
- independence threshold;
- final reliability aggregation formula;
- exact execution API.

These remain engineering decisions unless they alter semantic meaning.

---

# 75. Exit Criteria

- [x] Agent identity defined
- [x] Agent version defined
- [x] Agent schema version defined
- [x] Role boundary defined
- [x] Capability boundary defined
- [x] Authority reference defined
- [x] Input contract defined
- [x] Output contract defined
- [x] Tool boundary defined
- [x] Execution permission boundary defined
- [x] Constraint boundary defined
- [x] Execution context defined
- [x] Resource budget boundary defined
- [x] Timeout defined
- [x] Failure defined
- [x] Abstention defined
- [x] Escalation defined
- [x] Handoff defined
- [x] Delegation boundary defined
- [x] Self-critique interface defined
- [x] Adversarial verification interface defined
- [x] Verification independence boundary defined
- [x] Self-approval prohibition defined
- [x] Self-modification boundary defined
- [x] Repair and regression boundary defined
- [x] Agent lifecycle interaction defined
- [x] Model/agent distinction defined
- [x] Communication boundary defined
- [x] Memory boundary defined
- [x] Security boundaries defined
- [x] Agent invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Agent benchmarks defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 76. Next Contract

**III-006 — Constraint, Policy & Invariant Enforcement Contract**

III-006 will define how the architecture converts constraints into enforceable machine-readable rules covering:

```text
constraint identity
scope
priority
hard vs soft constraints
preconditions
prohibitions
required conditions
policy composition
conflicts
non-overridable invariants
policy evaluation
constraint violations
escalation
waivers / exceptions
policy provenance
runtime enforcement
```

The central requirement remains:

```text
A CONSTRAINT IS NOT A RECOMMENDATION
WHEN THE ARCHITECTURE DEFINES IT AS BINDING.
```
