# ENG-RTC-009 — Assurance Hardening & Specification Reconciliation

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** NEXT REQUIRED ENGINEERING ACTION  
**Priority:** HIGH  
**Date:** 2026-08-19  
**Depends On:** ENG-RTC-008, IV-006 through IV-015

---

# 1. Purpose

ENG-RTC-009 defines the next engineering iteration following the review of `ENG-RTC-008-IMPLEMENTATION-ASSURANCE-LOOP`.

ENG-RTC-008 successfully demonstrated the minimal end-to-end assurance lifecycle:

```text
claim
→ proof obligation
→ test
→ evidence
→ assurance
→ execution gate
→ action
→ monitoring
→ injected failure
→ counterexample
→ assurance demotion
→ capability restriction
→ repair
→ reverification
→ restoration
```

The implementation report also identified three important architectural weaknesses:

```text
A — correlated verification logic
B — stale assurance / propagation delay
C — single-dimensional assurance state
```

These findings are valuable and must now become adversarial engineering work.

The objective is:

```text
BREAK THE ASSURANCE MACHINERY
        ↓
IDENTIFY FAILURE MODES
        ↓
RECONCILE SPECIFICATION
        ↓
IMPLEMENT CORRECTIONS
        ↓
REATTACK
        ↓
DEMONSTRATE SURVIVAL
```

---

# 2. Review Disposition of ENG-RTC-008

ENG-RTC-008 demonstrated that the minimal loop is functionally executable. The report states that the complete chain was exercised and that all active test benches passed without regression. It also records contradictions between the specification and physical implementation.

Therefore:

```text
MINIMUM ASSURANCE LOOP
→ FUNCTIONALLY DEMONSTRATED

REGRESSION
→ PASSED

ARCHITECTURE
→ REQUIRES HARDENING

INDEPENDENT ASSURANCE
→ NOT YET ESTABLISHED

PRODUCTION SAFETY
→ NOT ESTABLISHED
```

Do not interpret:

```text
ALL TESTS PASSED
```

as:

```text
ARCHITECTURE PROVEN
```

---

# 3. Finding A — Correlated Verification

The engineer identified that the verification harness and `TelemetryMonitor` reuse the same color-drift parser logic. Therefore:

```text
verify()
      +
TelemetryMonitor
      ↓
same parser
```

creates a common failure mode.

If the parser is wrong, both verification and monitoring can fail together. This is explicitly identified in ENG-RTC-008.

---

# 4. Required Correction for Finding A

Do not merely create two copies of the same parser.

The requirement is:

```text
INDEPENDENCE OF FAILURE MODE
```

not:

```text
SEPARATE FILES
```

Implement at least two materially different verification paths.

Possible mechanisms:

```text
primary computation
+
independent recomputation
```

or:

```text
deterministic implementation
+
property/invariant checker
```

or:

```text
numerical parser
+
structural/statistical validator
```

Select and document the appropriate mechanism.

---

# 5. Verifier Fault Injection

Deliberately corrupt the primary verifier.

Inject faults such as:

```text
wrong threshold
off-by-one
incorrect unit conversion
parser corruption
missing field
wrong field
stale configuration
incorrect environment
malformed evidence
incorrect digest
```

Determine whether the independent verification path detects the discrepancy.

Record the result as evidence.

---

# 6. Correlated Failure Experiment

Construct an experiment where:

```text
TARGET
+
VERIFIER
+
MONITOR
```

share a hidden dependency.

First demonstrate:

```text
SHARED DEPENDENCY
 ↓
INCORRECT ASSURANCE
```

Then implement the architectural correction and demonstrate:

```text
SAME ATTACK
 ↓
INDEPENDENT CHECK
 ↓
ASSURANCE BLOCKED / DEMOTED
```

This experiment is mandatory.

---

# 7. Finding B — Assurance Freshness

The engineer identified that runtime invalidation is not instantaneous. The current propagation path can be:

```text
REAL-WORLD FAILURE
 ↓
MONITOR DETECTION
 ↓
EVENT PROPAGATION
 ↓
GRAPH INVALIDATION
 ↓
GATE UPDATE
```

Latency can create a stale-authorization window. This was explicitly identified in ENG-RTC-008.

---

# 8. Required Freshness Model

Every assurance state used by an execution gate must expose, as applicable:

```yaml
assurance_timestamp: ...
last_verified_at: ...
freshness_deadline: ...
source_monitor_timestamp: ...
```

The exact implementation may differ, but the semantics must be explicit.

The gate must distinguish:

```text
CURRENT
AGING
STALE
UNKNOWN
```

according to policy.

---

# 9. Freshness Test

Verify:

```text
freshness valid
→ action may proceed
```

and:

```text
freshness expired
→ REASSESSMENT_REQUIRED
→ block / restrict / escalate
```

Demonstrate actual gate behavior.

---

# 10. Assurance Race / TOCTOU Experiment

Construct:

```text
T0:
claim = VERIFIED

T1:
execution request begins

T2:
critical telemetry violation occurs

T3:
gate has not yet received invalidation

T4:
execution attempts to proceed
```

Measure:

```text
detection latency
propagation latency
gate reaction latency
execution latency
```

Determine whether an unsafe action can occur within the window.

If it can, record the failure. Do not conceal it.

---

# 11. Freshness Failure Policy

Define behavior for:

```text
monitor unavailable
telemetry delayed
telemetry missing
network partition
event queue blocked
resource exhaustion
clock inconsistency
```

Each condition must have explicit semantics:

```text
continue
degrade
REASSESSMENT_REQUIRED
block
escalate
```

---

# 12. Finding C — Multidimensional Assurance

The engineer correctly identified that a single scalar/string status is lossy. A claim can contain positive verification evidence and a localized counterexample simultaneously.

Do not solve this by adding more strings to a single enum.

---

# 13. Required Assurance Model

Implement separate dimensions, at minimum:

```yaml
assurance:
  verification_status: ...
  evidence_status: ...
  freshness_status: ...
  independence_status: ...
  counterexample_status: ...
  assumption_status: ...
  scope_status: ...
  overall_decision: ...
```

Example:

```yaml
verification_status: VERIFIED
evidence_status: VALID
freshness_status: CURRENT
independence_status: LIMITED
counterexample_status: CONFIRMED
assumption_status: VALID
scope_status: LIMITED
overall_decision: REASSESSMENT_REQUIRED
```

The implementation may use another representation, but the semantics must remain multidimensional.

---

# 14. Preserve Positive and Negative Evidence

If:

```text
Test A = PASS
Test B = PASS
Counterexample C = CONFIRMED
```

do not erase the positive evidence.

Preserve:

```text
positive evidence
+
counterexample
+
scope
+
conditions
+
relationships
```

Then derive the operational decision from those dimensions.

---

# 15. Counterexample Semantics

A counterexample should be capable of:

```text
demoting
refuting
scoping
or triggering reassessment
```

depending on the claim.

Do not assume every counterexample universally destroys every dimension of a claim.

Example:

```text
claim scope = "drift ≤ 10%"
counterexample = "drift = 15%"
```

may invalidate that claim while leaving unrelated claims unaffected.

---

# 16. Execution Gate Review

ENG-RTC-008 currently authorizes `compile_and_release` after the claim reaches `VERIFIED`.

Review whether this is consistent with IV-012.

Introduce action classes such as:

```text
compile
release
deploy
external_write
security_change
authority_change
```

with explicit policy requirements.

Do not assume:

```text
VERIFIED
```

is universally sufficient for every action.

---

# 17. Repair Verification

The current flow is:

```text
counterexample
→ RESOLVED
→ reverification
→ VERIFIED
→ restoration
```

Do not treat:

```text
code changed
```

as equivalent to:

```text
counterexample resolved
```

Require, where applicable:

```text
repair implemented
+
original counterexample reproduced before repair
+
counterexample no longer reproducible
+
regression test added
+
relevant adversarial test passed
+
assurance recomputed
```

Only then should `RESOLVED` be emitted.

---

# 18. Attack the Assurance Ledger

ENG-RTC-008 describes the `AssuranceLedger` as append-only and tamper-resistant.

Attempt:

```text
event deletion
event modification
event reordering
timestamp modification
state rewriting
duplicate insertion
fake evidence insertion
counterexample deletion
```

Verify whether integrity violations are detected.

---

# 19. Define "Tamper-Resistant"

Document the actual mechanism behind the term:

```text
append-only application semantics
hash chaining
digital signatures
external anchoring
immutable storage
access control
```

or the actual combination used.

Do not use “tamper-resistant” without specifying the technical property being provided.

---

# 20. Attack Evidence Integrity

ENG-RTC-008 reports target version, environment, seed, and content digests being pinned for evidence.

Test:

```text
evidence modified after generation
→ digest mismatch?
```

and:

```text
metadata modified
→ signature invalid?
```

Also test:

```text
valid historical evidence
+
new target version
```

The system must reject evidence reuse when scope, version, dependencies, or freshness are incompatible.

---

# 21. Verifier Version Binding

Test:

```text
VERIFIER VERSION 1
```

against:

```text
VERIFIER VERSION 2
```

Historical results must remain bound to their original:

```text
verifier version
test protocol
dataset
prompt
environment
target version
```

as applicable.

A new verifier must not silently rewrite historical evidence.

---

# 22. Judge Version Binding

If the evaluation judge changes:

```text
old result
```

must remain associated with:

```text
old judge
```

and new results must identify:

```text
new judge version
```

Do not silently replace historical results.

---

# 23. Gate Bypass Testing

Attempt to bypass the execution gate through:

```text
direct invocation
alternate API
race condition
stale state
cached authorization
forged assurance
malformed state
exception path
fallback path
```

Expected result:

```text
ACTION BLOCKED
```

or the explicitly defined safe fallback.

---

# 24. Telemetry Failure Testing

Test:

```text
monitor unavailable
telemetry delayed
telemetry dropped
telemetry corrupted
telemetry duplicated
telemetry reordered
```

Verify policy-defined behavior.

---

# 25. Unknown-State Testing

Test:

```text
assurance = UNKNOWN
```

and confirm that:

```text
UNKNOWN
→
ALLOW
```

does not occur for actions requiring positive assurance.

---

# 26. Contradictory Evidence Testing

Construct:

```text
evidence A → supports claim
evidence B → contradicts claim
```

Verify that both records remain and the resulting decision follows the conservative assurance semantics.

---

# 27. Adversarial Test Matrix

Create:

`ENG-RTC-009-ADVERSARIAL-MATRIX`

At minimum:

| Attack | Expected Result |
|---|---|
| Primary verifier corrupted | Independent verifier detects discrepancy |
| Monitor parser corrupted | Independent mechanism detects discrepancy |
| Shared hidden dependency exploited | Assurance blocked/demoted after correction |
| Telemetry delayed | Freshness semantics restrict action when required |
| Telemetry lost | Explicit degraded/block behavior |
| Counterexample injected | Appropriate assurance demotion |
| Counterexample hidden | Detection mechanism challenged |
| Evidence modified | Integrity failure |
| Old evidence replayed | Scope/freshness rejection |
| Ledger event modified | Integrity violation |
| Ledger event deleted | Integrity violation |
| Repair without regression | Restoration denied |
| Judge modified | Historical results remain version-bound |
| Verifier modified | Independent reevaluation required |
| Gate bypass attempted | Action blocked |
| Authority revoked during action | Policy-defined restriction |
| Contradictory results | Conflict preserved |
| Unknown assurance | No silent authorization |
| Freshness timeout | Automatic restriction/reassessment |

---

# 28. Do Not Expand Intelligence Capability Yet

During ENG-RTC-009:

```text
NO NEW GENERAL AGENT CAPABILITIES
NO UNRESTRICTED AUTONOMY
NO LARGE MEMORY EXPANSION
NO UNRESTRICTED SELF-MODIFICATION
```

Focus entirely on:

```text
verification
assurance
freshness
independence
evidence integrity
gate correctness
```

The trust machinery must be hardened before substantially increasing intelligence capability.

---

# 29. Required Deliverable

Create:

```text
ENG-RTC-009-ASSURANCE-HARDENING.md
```

It must contain:

## A. Findings

```text
issue
root cause
affected specification
severity
```

## B. Corrections

```text
change
reason
affected component
```

## C. Adversarial Experiments

For every experiment:

```text
attack
setup
expected result
actual result
evidence
```

## D. Remaining Failures

Do not hide failures.

## E. Architecture Changes

For every change:

```text
before
→
failure
→
after
```

## F. Evidence

Include:

```text
test results
failure traces
latencies
hash/signature validation
state transitions
```

## G. Specification Changes

If IV-011, IV-012, IV-013, or IV-014 must change:

```text
identify exact document
identify section
describe required change
provide rationale
```

Do not silently modify specifications.

---

# 30. Acceptance Criteria

ENG-RTC-009 is complete only when:

```text
[ ] correlated verifier failure demonstrated
[ ] independent verification path implemented
[ ] verifier fault injection completed
[ ] freshness model implemented
[ ] freshness timeout behavior tested
[ ] assurance race condition tested
[ ] multidimensional assurance implemented
[ ] contradictory evidence behavior tested
[ ] counterexample scoping tested
[ ] execution action classes reviewed
[ ] repair semantics strengthened
[ ] repair regression tested
[ ] ledger tamper attacks tested
[ ] evidence tamper attacks tested
[ ] evidence replay attacks tested
[ ] verifier version binding tested
[ ] judge version binding tested
[ ] gate bypass attacks tested
[ ] telemetry failure modes tested
[ ] UNKNOWN state tested
[ ] deliberate shared-dependency attack demonstrated
[ ] architectural correction reattacked
[ ] remaining failures documented
[ ] specification conflicts documented
```

---

# 31. Evidence Standard

For every claimed correction:

```text
IMPLEMENTATION CHANGE
        ↓
TEST
        ↓
ATTACK
        ↓
RESULT
        ↓
EVIDENCE
```

A prose assertion that a vulnerability is fixed is insufficient.

---

# 32. Failure Reporting Standard

When a test fails, report:

```yaml
failure:
  id: ...
  condition: ...
  expected: ...
  actual: ...
  severity: ...
  reproducible: ...
  suspected_root_cause: ...
  affected_claims: []
  affected_components: []
  evidence_refs: []
```

Do not convert unresolved failures into successful states.

Use:

```text
UNKNOWN
```

where evidence is insufficient.

---

# 33. Specification Reconciliation

If engineering discovers:

```text
implementation impossible
specification ambiguous
invariant contradictory
assurance semantics incomplete
verification independence insufficient
```

report the conflict.

Process:

```text
ENGINEERING DISCOVERY
 ↓
DOCUMENT CONFLICT
 ↓
IDENTIFY AFFECTED SPECIFICATION
 ↓
PROPOSE REVISION
 ↓
TEST REVISION
 ↓
RATIFY CHANGE
```

Do not silently improvise around a specification conflict.

---

# 34. Engineering Philosophy

The objective is not:

```text
MAKE ALL TESTS PASS
```

The objective is:

```text
FIND WHERE THE ASSURANCE ARCHITECTURE LIES
        ↓
BREAK IT
        ↓
UNDERSTAND WHY
        ↓
REPAIR IT
        ↓
DEMONSTRATE THAT THE REPAIR
SURVIVES THE ORIGINAL ATTACK
```

A newly discovered failure is valuable engineering evidence.

---

# 35. Final Instruction

Proceed with:

```text
ENG-RTC-009
```

Do not expand intelligence capabilities until the assurance-hardening experiments above have been completed and documented.

The next engineering response must contain:

```text
ENG-RTC-009-ASSURANCE-HARDENING.md
```

with implementation evidence, adversarial results, remaining failures, and any proposed specification revisions.

**Do not report the architecture as independently validated unless the experiments actually establish that conclusion.**
