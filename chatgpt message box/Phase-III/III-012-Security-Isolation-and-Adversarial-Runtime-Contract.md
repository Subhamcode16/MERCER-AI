# III-012 — Security, Isolation & Adversarial Runtime Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** III — Machine-Readable Contract Compilation  
**Depends On:** III-001 through III-011 and the ratified Phase II semantic architecture

## 1. Purpose

III-012 defines the runtime security boundary of the intelligence architecture.

The central requirement is:

```text
AN AGENT MUST NEVER BE ABLE
TO TURN ITS INTELLIGENCE OR ACCESS
INTO UNBOUNDED CONTROL OVER THE RUNTIME.
```

The contract governs:

```text
identity security
credential isolation
secret handling
sandboxing
tool isolation
filesystem/network boundaries
resource limits
execution containment
privilege separation
attack detection
compromise response
runtime attestation
secure state transitions
emergency stop
recovery
security provenance
```

The objective is not merely to prevent malicious behavior.

It is to ensure that even when an agent:

```text
fails
hallucinates
is manipulated
is compromised
misinterprets a task
receives poisoned context
produces unsafe code
```

the runtime remains bounded by explicit security controls.

---

# 2. Security Is a Runtime Property

Security must be enforced at the execution boundary.

Therefore:

```text
PROMPT
≠
SECURITY BOUNDARY
```

and:

```text
AGENT INTENTION
≠
RUNTIME AUTHORIZATION
```

A model saying:

```text
"I am authorized."
```

does not establish authorization.

---

# 3. Identity

Every security-relevant actor must have an identifiable security principal.

Principals may include:

```text
human
agent
service
tool
runtime
device
credential
```

Identity must be bound to authenticated context where consequential operations occur.

---

# 4. Identity vs Role

Identity answers:

```text
WHO IS ACTING?
```

Role answers:

```text
WHAT RESPONSIBILITY DOES THIS PRINCIPAL HAVE?
```

Therefore:

```text
IDENTITY ≠ ROLE
```

Role assignment must not silently change identity.

---

# 5. Authentication

Authentication establishes that a principal controls the identity it claims.

The mechanism is implementation-specific and may use:

```text
cryptographic credentials
attestation
trusted identity provider
device identity
short-lived tokens
```

Authentication does not itself establish authorization.

---

# 6. Authorization

Authorization determines whether an authenticated principal may perform an operation.

Conceptually:

```text
IDENTITY
+
CAPABILITY
+
AUTHORITY
+
CONTEXT
+
POLICY
→
AUTHORIZED / DENIED
```

Authorization must be evaluated at the appropriate security boundary.

---

# 7. Capability Boundary

A runtime capability must be explicit.

Examples:

```text
filesystem.read
filesystem.write
network.connect
process.spawn
database.read
database.write
tool.invoke
secret.read
device.control
```

Capabilities must not be inferred merely from natural-language instructions.

---

# 8. Capability vs Privilege

A capability describes what an interface can technically expose.

Privilege describes the effective authority granted to a principal.

Therefore:

```text
EXPOSED CAPABILITY
≠
AUTHORIZED PRIVILEGE
```

The runtime should minimize both.

---

# 9. Least Privilege

Every execution context should receive the minimum privileges required for its task.

Conceptually:

```text
REQUIRED PRIVILEGE
⊆
GRANTED PRIVILEGE
```

Excess privilege increases the impact of:

```text
bugs
prompt injection
compromise
credential theft
tool misuse
```

---

# 10. Privilege Separation

High-impact capabilities should be separated where practical.

Examples:

```text
planning
vs
execution

read
vs
write

network access
vs
secret access

verification
vs
mutation
```

A single compromised component should not automatically gain all privileges.

---

# 11. Privilege Escalation

The runtime must detect or prevent attempts to obtain privileges beyond the authorized scope.

Examples:

```text
changing permissions
obtaining another agent's credentials
escaping sandbox
accessing protected files
calling restricted tools
creating privileged subprocesses
```

---

# 12. Credential Isolation

Credentials must be isolated from general agent context.

An agent should not receive raw credentials unless explicitly authorized.

Preferred pattern:

```text
AGENT
 ↓
AUTHORIZED TOOL
 ↓
CREDENTIAL-BOUND SERVICE
 ↓
EXTERNAL SYSTEM
```

rather than:

```text
AGENT
 ↓
RAW SECRET
 ↓
ARBITRARY USE
```

---

# 13. Secret Handling

Secrets include:

```text
API keys
tokens
passwords
private keys
session credentials
database credentials
signing keys
```

Secrets must not be treated as ordinary memory.

They require:

```text
access control
scope
expiration
auditability
revocation
secure storage
```

---

# 14. Secret Non-Disclosure

The runtime should prevent secrets from being unintentionally emitted into:

```text
agent output
logs
telemetry
prompts
memory
evidence
error messages
tool arguments
```

where disclosure is not authorized.

---

# 15. Secret Redaction

Where secrets appear in logs or diagnostics, the system should use appropriate redaction.

Redaction must not destroy the ability to correlate events where safe identifiers are required.

---

# 16. Short-Lived Credentials

Where practical, use short-lived credentials for agent operations.

Benefits include:

```text
reduced exposure window
simpler revocation
bounded delegation
smaller blast radius
```

---

# 17. Credential Binding

Credentials should be bound to:

```text
principal
task
scope
tool
resource
duration
```

where practical.

A credential issued for one context should not automatically be reusable in another.

---

# 18. Sandbox

Agent execution should occur inside an appropriate isolation boundary where untrusted or high-risk computation is possible.

A sandbox may constrain:

```text
filesystem
network
processes
devices
environment variables
IPC
resources
```

The exact sandbox technology is implementation-specific.

---

# 19. Sandbox Escape

The architecture must explicitly test attempts to escape the sandbox through:

```text
filesystem traversal
process injection
privileged syscalls
container escape
device access
IPC abuse
credential discovery
network pivoting
```

---

# 20. Filesystem Isolation

Filesystem access should be scoped.

Conceptually:

```text
AGENT
 ↓
AUTHORIZED PATHS
```

rather than:

```text
AGENT
 ↓
ENTIRE HOST FILESYSTEM
```

Path authorization must defend against:

```text
../ traversal
symlinks
mount manipulation
alternate path representations
```

where applicable.

---

# 21. Network Isolation

Network permissions should be explicit.

Examples:

```text
no network
allowlisted domains
allowlisted IPs
specific ports
specific protocols
egress-only
```

Network connectivity must not be assumed merely because the runtime has network access.

---

# 22. Network Segmentation

High-risk components should be isolated from sensitive infrastructure where practical.

Potential boundaries:

```text
public internet
agent runtime
tool gateway
internal services
credential service
control plane
```

---

# 23. Tool Isolation

Tools must expose bounded interfaces.

A tool should specify:

```text
identity
version
capabilities
required authority
input schema
output schema
security boundary
```

Tool access must be explicitly authorized.

---

# 24. Tool Invocation Authorization

Before a consequential tool invocation:

```text
AGENT
 ↓
TOOL REQUEST
 ↓
AUTHORIZATION CHECK
 ↓
POLICY CHECK
 ↓
TOOL
```

The tool should not rely solely on the agent's assertion that the invocation is permitted.

---

# 25. Tool Output Trust

Tool output is untrusted data unless explicitly classified otherwise.

Therefore:

```text
TOOL OUTPUT
≠
CONTROL PLANE
```

Tool output must not silently modify:

```text
authority
policy
identity
security state
```

---

# 26. Process Isolation

Agents should not receive unrestricted process-control capability.

Potentially high-risk operations include:

```text
process creation
process termination
privilege change
service installation
startup modification
kernel interaction
```

These require explicit authorization.

---

# 27. Resource Limits

Runtime execution should be bounded by:

```text
CPU
memory
disk
network
process count
execution time
tool calls
concurrency
```

Resource exhaustion must not become an unbounded failure mode.

---

# 28. Execution Timeouts

Consequential execution should have appropriate time limits.

Timeout must remain distinguishable from success:

```text
TIMEOUT ≠ SUCCESS
```

and from known failure:

```text
TIMEOUT ≠ FAILURE
```

when the external state remains uncertain.

---

# 29. Resource Exhaustion

The runtime should detect:

```text
memory exhaustion
CPU exhaustion
disk exhaustion
process explosion
network flooding
tool-call explosion
recursive task creation
```

and apply containment.

---

# 30. Recursive Agent Creation

An agent must not be able to create unlimited agents or tasks merely because it can call an agent-creation interface.

Creation must be:

```text
authorized
bounded
auditable
resource-limited
```

---

# 31. Recursive Tool Invocation

Tool chains must have bounded execution characteristics.

The runtime should control:

```text
depth
duration
fan-out
cost
resource usage
authority propagation
```

---

# 32. Execution Containment

Execution should occur inside an explicit boundary:

```text
REQUEST
 ↓
AUTHORIZATION
 ↓
POLICY
 ↓
SANDBOX
 ↓
RESOURCE LIMITS
 ↓
EXECUTION
 ↓
OBSERVATION
```

The agent should not bypass these controls.

---

# 33. Execution Intent Boundary

III-008 established:

```text
DECISION
≠
EXECUTION INTENT
≠
EXECUTION
```

III-012 strengthens the final boundary:

```text
EXECUTION INTENT
 ↓
RUNTIME SECURITY CHECK
 ↓
ACTUAL EXECUTION
```

An approved plan does not bypass runtime security.

---

# 34. Runtime Security Recheck

Security-sensitive actions should be revalidated immediately before execution.

Revalidation may include:

```text
identity
authority
credential state
policy
resource availability
target state
security posture
```

This protects against time-of-check/time-of-use changes.

---

# 35. Time-of-Check / Time-of-Use

A security decision made earlier may become invalid before execution.

Therefore:

```text
CHECK
 ↓
STATE CHANGE
 ↓
EXECUTION
```

must be protected against where the distinction is material.

---

# 36. Secure State Transitions

Security-relevant state transitions must be explicit.

Examples:

```text
AUTHORIZED
→
SUSPENDED
→
REVOKED
```

or:

```text
SAFE
→
DEGRADED
→
QUARANTINED
→
RECOVERED
```

Invalid transitions must be rejected.

---

# 37. Security State

The runtime should maintain a security state representing relevant conditions such as:

```text
NORMAL
DEGRADED
SUSPICIOUS
COMPROMISED
QUARANTINED
EMERGENCY_STOP
RECOVERY
```

The exact state taxonomy remains implementation-specific.

---

# 38. Security Invariants During State Changes

A transition into a more restrictive state must not accidentally restore broader privileges.

For example:

```text
COMPROMISED
→
RECOVERY
```

must not imply:

```text
FULL AUTHORITY
```

without explicit reauthorization.

---

# 39. Attack Detection

Runtime monitoring should identify suspicious behavior.

Signals may include:

```text
unexpected tool use
authority violations
credential access anomalies
filesystem anomalies
network anomalies
resource abuse
repeated policy failures
sandbox escape attempts
```

Detection is evidence, not automatically proof of compromise.

---

# 40. Detection vs Response

The system must distinguish:

```text
DETECTION
```

from:

```text
RESPONSE
```

Detection identifies a possible security event.

Response performs an authorized containment action.

---

# 41. Security Event Identity

Security events should have stable identities.

Recommended conceptual form:

```text
SEC-<ULID>
```

Each event should preserve:

```text
principal
timestamp
target
event type
observed behavior
evidence
security state
response
provenance
```

---

# 42. Security Incident

A security incident represents a confirmed or sufficiently significant security condition.

Conceptually:

```yaml
security_incident:
  incident_id: SIN-...
  event_refs: []
  principals: []
  affected_resources: []
  severity: ...
  state: ...
  response: ...
  evidence_refs: []
  provenance_ref: ...
```

---

# 43. Severity

Security events should be classified according to impact.

Possible conceptual levels:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

The final severity model is domain-specific.

---

# 44. Compromise

Compromise means the security assumptions surrounding a principal or runtime boundary can no longer be trusted.

Potential responses:

```text
revoke credentials
suspend authority
terminate execution
quarantine runtime
isolate network
preserve evidence
escalate verification
```

---

# 45. Compromise Containment

Containment should prioritize:

```text
STOP FURTHER HARM
PRESERVE EVIDENCE
LIMIT BLAST RADIUS
MAINTAIN ACCOUNTABILITY
```

Containment itself must remain authorized.

---

# 46. Emergency Stop

The runtime must support an emergency-stop mechanism for sufficiently high-risk situations.

Conceptually:

```text
EMERGENCY CONDITION
 ↓
STOP AUTHORIZED EXECUTION
 ↓
ISOLATE
 ↓
PRESERVE STATE/EVIDENCE
 ↓
RECOVERY
```

---

# 47. Emergency Stop Authority

Emergency stop must have explicit authority.

It should not depend exclusively on the agent being stopped.

The mechanism should remain available when the agent is malfunctioning or compromised.

---

# 48. Emergency Stop Semantics

An emergency stop should define:

```text
what stops
what remains running
which credentials are revoked
what evidence is preserved
what external actions can still complete
```

Stopping local execution cannot necessarily reverse external side effects.

---

# 49. Rollback

Rollback is not universally possible.

The architecture must distinguish:

```text
REVERSIBLE ACTION
vs
IRREVERSIBLE ACTION
```

and must never imply that an external action was undone merely because the local runtime reverted state.

---

# 50. Recovery

Recovery should proceed through explicit states:

```text
INCIDENT
 ↓
CONTAINMENT
 ↓
FORENSICS / EVIDENCE PRESERVATION
 ↓
REMEDIATION
 ↓
VERIFICATION
 ↓
REAUTHORIZATION
 ↓
NORMAL OPERATION
```

Skipping verification after compromise should require explicit justification.

---

# 51. Recovery Verification

Before restoring normal authority, verify:

```text
identity integrity
credential integrity
runtime integrity
policy integrity
tool integrity
memory integrity
evidence integrity
```

---

# 52. Runtime Attestation

Where supported, the runtime may attest properties such as:

```text
runtime identity
software version
configuration
security state
sandbox state
trusted environment
```

Attestation provides evidence about runtime state; it does not replace authorization.

---

# 53. Attestation Freshness

Runtime attestation may become stale.

Where material:

```text
attestation timestamp
runtime version
configuration version
validity
```

must be preserved.

---

# 54. Trusted Execution Boundary

The architecture should identify which components are trusted to enforce security.

Conceptually:

```text
UNTRUSTED AGENT
      ↓
TRUSTED SECURITY BOUNDARY
      ↓
RESOURCE
```

The model should not be the final security enforcement point for high-impact operations.

---

# 55. Security Reference Monitor

Where appropriate, a dedicated enforcement layer should mediate sensitive operations.

Conceptually:

```text
AGENT
 ↓
SECURITY REFERENCE MONITOR
 ↓
RESOURCE / TOOL
```

The monitor should enforce:

```text
identity
authority
policy
resource scope
credential rules
```

---

# 56. Security Boundary Bypass

Every critical security boundary should have explicit bypass tests.

Attempt:

```text
direct API access
alternate tool
environment variable abuse
filesystem path manipulation
subprocess creation
credential extraction
message forgery
runtime API misuse
```

---

# 57. Logging

Security-relevant events should be logged with sufficient provenance.

Logs should preserve:

```text
who
what
when
where
why
authority
result
evidence
```

Logs themselves require integrity protection.

---

# 58. Audit Log Integrity

An attacker must not be able to silently rewrite security history.

Potential controls include:

```text
append-only storage
hash chaining
signed records
remote immutable storage
access separation
```

Implementation remains deferred.

---

# 59. Security Provenance

Security events must connect to the broader provenance graph:

```text
PRINCIPAL
 ↓
AUTHORITY
 ↓
REQUEST
 ↓
SECURITY CHECK
 ↓
EXECUTION
 ↓
EVENT
 ↓
RESPONSE
 ↓
OUTCOME
```

This allows security incidents to be reconstructed.

---

# 60. Security Evidence

Security evidence may include:

```text
logs
runtime events
network events
process events
filesystem events
credential events
tool traces
attestation
verification results
```

Evidence must preserve integrity and provenance according to III-010.

---

# 61. Security vs Observability

Observability records behavior.

Security controls behavior.

Therefore:

```text
OBSERVABILITY ≠ ENFORCEMENT
```

A dashboard showing an unauthorized action after it occurred is not equivalent to preventing it.

---

# 62. Security vs Verification

Verification asks whether a property holds.

Security enforcement prevents or contains violations.

Therefore:

```text
VERIFICATION ≠ PREVENTION
```

Both are required for high-impact systems.

---

# 63. Adversarial Runtime Testing

The adversarial verifier should attack the runtime boundary through:

```text
prompt injection
tool injection
credential theft
sandbox escape
authority escalation
network pivot
filesystem traversal
resource exhaustion
process abuse
message replay
identity spoofing
security-log tampering
```

---

# 64. Security Fuzzing

Security-sensitive interfaces should be fuzzed where appropriate.

Targets may include:

```text
tool schemas
authorization inputs
path handling
network rules
message parsers
credential interfaces
policy parsers
state transitions
```

---

# 65. Policy Bypass Testing

Attempt to violate security policy through:

```text
semantic ambiguity
alternate representations
encoding tricks
indirect tool invocation
delegation chains
context manipulation
race conditions
```

---

# 66. Race Conditions

Security checks may race with state changes.

Test:

```text
authorization changes
credential revocation
target mutation
policy updates
resource deletion
```

between check and execution.

---

# 67. Fail-Closed vs Fail-Open

Security-critical components should define behavior when dependencies fail.

Examples:

```text
authorization service unavailable
credential service unavailable
policy unavailable
attestation unavailable
audit storage unavailable
```

The correct behavior is domain-specific, but it must be explicit.

---

# 68. Safe Degradation

A system may continue operating in degraded mode if risk permits.

Degradation should normally reduce:

```text
authority
capability
resource access
automation
```

rather than silently removing safeguards.

---

# 69. Security Dependency Failure

Security dependencies are themselves part of the threat model.

Examples:

```text
identity provider failure
policy service compromise
credential store compromise
monitor failure
attestation failure
```

The architecture should preserve bounded behavior when these components fail.

---

# 70. Blast Radius

Every capability and credential should have an identifiable potential blast radius.

Conceptually:

```text
PRINCIPAL
 ↓
CAPABILITY
 ↓
RESOURCE SET
 ↓
POTENTIAL IMPACT
```

High-blast-radius capabilities require stronger controls.

---

# 71. Security Segmentation

Separate:

```text
control plane
data plane
agent runtime
tool runtime
credential service
audit system
```

where practical.

Compromise of one layer should not automatically compromise all layers.

---

# 72. Control Plane Protection

The control plane contains high-impact functions such as:

```text
authority
policy
identity
credential issuance
security state
emergency stop
```

Agent-generated data must not silently modify control-plane state.

---

# 73. Data Plane Isolation

Data-plane resources may include:

```text
files
databases
APIs
external services
```

Their access must remain bounded by control-plane decisions.

---

# 74. Security Configuration Integrity

Security configuration must be versioned and protected.

Material configuration includes:

```text
policies
allowlists
denylists
sandbox configuration
resource limits
credential scopes
network rules
```

---

# 75. Configuration Change

Security-sensitive configuration changes should produce:

```text
change identity
authorized actor
old version
new version
reason
timestamp
verification result
```

---

# 76. Configuration Rollback

Rollback must preserve:

```text
previous state
rollback event
authority
reason
verification
```

A rollback is itself a security-sensitive operation.

---

# 77. Security Regression

Every discovered runtime vulnerability should become a regression test where appropriate.

```text
VULNERABILITY
 ↓
ATTACK CASE
 ↓
REGRESSION TEST
 ↓
PATCH
 ↓
RETEST
```

---

# 78. Security Benchmark

The runtime should maintain at least:

```text
1. IDENTITY SECURITY
2. AUTHORIZATION CONTAINMENT
3. SANDBOX ISOLATION
4. CREDENTIAL ISOLATION
5. RESOURCE CONTAINMENT
6. ADVERSARIAL RESILIENCE
7. COMPROMISE RECOVERY
8. AUDIT INTEGRITY
```

---

# 79. Security Invariants

### Invariant 1

Authentication does not imply authorization.

### Invariant 2

Capability does not imply permission.

### Invariant 3

Role does not imply authority.

### Invariant 4

Agent intention does not constitute runtime authorization.

### Invariant 5

Secrets are distinct from ordinary agent memory.

### Invariant 6

Credentials are scoped where practical.

### Invariant 7

High-impact operations pass through an explicit security boundary.

### Invariant 8

Tool access is explicitly authorized.

### Invariant 9

Tool output does not automatically become control-plane instruction.

### Invariant 10

Sandbox boundaries cannot be bypassed through alternate representations.

### Invariant 11

Resource consumption is bounded.

### Invariant 12

Execution intent does not bypass runtime security checks.

### Invariant 13

Security-sensitive authorization is revalidated where TOCTOU risk exists.

### Invariant 14

Security state transitions are explicit.

### Invariant 15

Compromise can trigger containment.

### Invariant 16

Emergency stop does not depend exclusively on the compromised agent.

### Invariant 17

Emergency stop does not imply external side effects were reversed.

### Invariant 18

Recovery requires verification before restoration of normal authority.

### Invariant 19

Runtime attestation does not replace authorization.

### Invariant 20

Observability does not equal enforcement.

### Invariant 21

Verification does not equal prevention.

### Invariant 22

Security logs preserve integrity.

### Invariant 23

Control-plane state cannot be silently modified by agent-generated content.

### Invariant 24

Security configuration changes are auditable.

### Invariant 25

Security vulnerabilities become regression cases where appropriate.

### Invariant 26

Security dependency failures have explicit behavior.

### Invariant 27

Degraded operation must not silently remove critical safeguards.

### Invariant 28

Implementation must not invent security semantics.

---

# 80. Required Tests

The reference implementation must test:

```text
identity authentication
authorization
capability enforcement
least privilege
privilege separation
privilege escalation
credential isolation
secret leakage
credential expiration
credential revocation
sandbox isolation
sandbox escape
filesystem isolation
path traversal
network isolation
network pivoting
tool isolation
tool authorization
process isolation
resource limits
resource exhaustion
recursive agent creation
recursive tool invocation
execution containment
runtime security recheck
TOCTOU conditions
secure state transitions
attack detection
security event recording
incident creation
compromise containment
emergency stop
rollback semantics
recovery
recovery verification
runtime attestation
attestation freshness
security boundary bypass
audit log integrity
security provenance
prompt injection
tool injection
credential theft
identity spoofing
message replay
policy bypass
race conditions
dependency failure
safe degradation
configuration integrity
configuration change
security regression
```

---

# 81. Falsification Cases

Deliberately attempt:

```text
agent executes without authorization
agent reads another principal's secret
agent uses expired credential
agent uses revoked credential
agent escapes filesystem sandbox
agent escapes network boundary
agent invokes an unauthorized tool
agent spawns unrestricted subprocesses
agent creates unlimited child agents
agent exhausts memory/CPU/disk
agent bypasses execution-intent security checks
authorization changes immediately before execution
agent modifies security policy
agent modifies audit logs
agent spoofs another agent identity
agent replays an old authorization message
agent turns tool output into control-plane instruction
agent bypasses allowlist through alternate encoding
agent continues operating after compromise containment
agent prevents emergency stop
recovery restores privileges without verification
stale attestation is accepted as current
security dependency failure produces unrestricted execution
degraded mode silently disables critical controls
```

---

# 82. Security Failure Taxonomy

Potential failure classes:

```text
AUTHENTICATION_FAILURE
AUTHORIZATION_FAILURE
PRIVILEGE_ESCALATION
CREDENTIAL_EXPOSURE
SECRET_LEAK
SANDBOX_ESCAPE
FILESYSTEM_BOUNDARY_BREACH
NETWORK_BOUNDARY_BREACH
TOOL_AUTHORIZATION_FAILURE
PROCESS_ISOLATION_FAILURE
RESOURCE_EXHAUSTION
EXECUTION_CONTAINMENT_FAILURE
TOCTOU_FAILURE
SECURITY_STATE_VIOLATION
ATTACK_DETECTION_FAILURE
COMPROMISE_CONTAINMENT_FAILURE
EMERGENCY_STOP_FAILURE
RECOVERY_VERIFICATION_FAILURE
ATTESTATION_FAILURE
AUDIT_INTEGRITY_FAILURE
CONTROL_PLANE_BREACH
CONFIGURATION_INTEGRITY_FAILURE
POLICY_BYPASS
IDENTITY_SPOOFING
MESSAGE_REPLAY
DEPENDENCY_FAILURE
```

---

# 83. Security Incident Reconstruction

For a consequential security event, an evaluator should be able to reconstruct:

```text
principal
identity state
authority state
credential state
request
policy
security checks
runtime configuration
execution
security events
detection
containment
evidence
recovery
final outcome
```

---

# 84. Security Recovery Benchmark

Measure recovery from:

```text
credential compromise
agent compromise
tool compromise
sandbox escape attempt
policy corruption
audit corruption
network attack
resource exhaustion
identity compromise
control-plane attack
```

Metrics may include:

```text
detection time
containment time
unauthorized actions
blast radius
evidence completeness
recovery correctness
residual compromise
```

---

# 85. Deferred Decisions

III-012 intentionally does not freeze:

- exact authentication mechanism;
- identity provider;
- cryptographic primitives;
- sandbox technology;
- container/VM strategy;
- network policy engine;
- secret-management system;
- runtime attestation mechanism;
- security-monitor implementation;
- intrusion-detection implementation;
- audit-log storage;
- emergency-stop transport;
- recovery orchestrator;
- exact security-state taxonomy;
- exact threat-scoring algorithm.

These remain engineering decisions unless they change semantic meaning.

---

# 86. Exit Criteria

- [x] Identity security defined
- [x] Authentication/authorization distinction defined
- [x] Capability/privilege distinction defined
- [x] Least privilege defined
- [x] Privilege separation defined
- [x] Credential isolation defined
- [x] Secret handling defined
- [x] Credential binding/expiration defined
- [x] Sandbox defined
- [x] Sandbox escape testing defined
- [x] Filesystem isolation defined
- [x] Network isolation defined
- [x] Tool isolation defined
- [x] Process isolation defined
- [x] Resource limits defined
- [x] Recursive execution bounds defined
- [x] Execution containment defined
- [x] Runtime security recheck defined
- [x] TOCTOU protection defined
- [x] Secure state transitions defined
- [x] Attack detection defined
- [x] Security events/incidents defined
- [x] Compromise containment defined
- [x] Emergency stop defined
- [x] Rollback/recovery semantics defined
- [x] Runtime attestation defined
- [x] Trusted enforcement boundary defined
- [x] Security reference monitor defined
- [x] Logging/audit integrity defined
- [x] Security provenance defined
- [x] Adversarial runtime testing defined
- [x] Dependency failure handling defined
- [x] Blast-radius and segmentation principles defined
- [x] Control-plane protection defined
- [x] Configuration integrity defined
- [x] Security regression defined
- [x] Benchmarks defined
- [x] Invariants defined
- [x] Required tests defined
- [x] Falsification cases defined
- [x] Failure taxonomy defined
- [x] Recovery benchmark defined
- [x] Deferred decisions defined

**Current assessment:** Ready for engineering review and implementation compilation.

---

# 87. Next Contract

**III-013 — Learning, Adaptation, Self-Modification & Behavioral Stability Contract**

III-013 will formalize how the intelligence system changes itself over time:

```text
learning
adaptation
feedback
policy updates
memory updates
model changes
prompt changes
tool changes
self-modification
configuration changes
behavioral drift
regression
rollback
change authorization
change verification
stable identity across versions
```

The central requirement will be:

```text
A SYSTEM MUST NOT
IMPROVE OR MODIFY ITSELF
IN WAYS THAT SILENTLY CHANGE
ITS AUTHORITY, SAFETY PROPERTIES,
OR BEHAVIORAL CONTRACT.
```
