# ENG-RTC-011 — Independent Trust Anchoring & Temporal Semantics

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** NEXT REQUIRED ENGINEERING ACTION  
**Priority:** CRITICAL  
**Depends On:** ENG-RTC-010, IV-010, IV-011, IV-012, IV-013

---

## 1. Purpose

ENG-RTC-010 demonstrated clock rollback/jump detection, persistent ledger recovery, corruption detection, rollback detection, alternate-chain detection, and the combined clock+restart attack. However, it also exposed a deeper limitation: the local ledger, local trust anchor, local clock, and local storage can potentially be controlled by the same local attacker. The engineer explicitly identified that an attacker with filesystem access could rewrite both `assurance_ledger.db` and `trust_anchor.json`. fileciteturn19file0L124-L139

RTC-011 therefore asks:

> **What remains trustworthy when the attacker controls the entire local trust substrate?**

The objective is to establish:

```text
REQUIRED TRUST PROPERTY
        ↓
THREAT MODEL
        ↓
REQUIRED INDEPENDENCE
        ↓
CANDIDATE TRUST ANCHOR
        ↓
ADVERSARIAL TEST
        ↓
EVIDENCE
```

---

## 2. RTC-010 Disposition

Do not treat RTC-010 as production-grade assurance.

```text
RTC-010 EXPERIMENTAL HARDENING
→ ACCEPTED

RTC-010 PROTOTYPE RESULTS
→ VALIDATED FOR TESTED SCENARIOS

NON-REPUDIATION
→ NOT ESTABLISHED

EXTERNAL HISTORY AUTHENTICITY
→ NOT ESTABLISHED

INDEPENDENT TRUST ANCHOR
→ NOT ESTABLISHED

FULL TEMPORAL INTEGRITY
→ NOT ESTABLISHED
```

---

## 3. Critical Property Distinctions

Do not collapse these into one concept:

```text
LEDGER INTEGRITY
LEDGER CONTINUITY
LEDGER AUTHENTICITY
LEDGER FRESHNESS
LEDGER DURABILITY
LEDGER NON-REPUDIATION
```

For each property define:

```text
what it means
what threat it addresses
what mechanism establishes it
what evidence demonstrates it
what assumptions it requires
```

In particular, do not claim that append-only database semantics alone establish cryptographic non-repudiation.

---

## 4. Threat Model

Model an attacker who controls:

```text
assurance_ledger.db
trust_anchor.json
local filesystem
application configuration
process state
wall-clock configuration
local environment
restart capability
```

The attacker may attempt:

```text
delete history
rewrite history
truncate history
replace history
create alternate history
replace the trust anchor
rollback the trust anchor
modify timestamps
replay old evidence
forge new evidence
restart the process
combine clock manipulation with restart
```

Do not assume the attacker controls external systems unless explicitly stated.

---

## 5. Central Experiment — Entire Local Trust Substrate Compromise

Construct:

```text
LEGITIMATE HISTORY
        ↓
ASSURANCE ESTABLISHED
        ↓
ATTACKER GAINS LOCAL CONTROL
```

The attacker controls:

```text
ledger
anchor
clock
configuration
process
```

Then attempt:

```text
forge assurance history
        ↓
restart
        ↓
recover
        ↓
request privileged action
```

Determine:

```text
ALLOW?
BLOCK?
REASSESS?
UNKNOWN?
```

Do not modify expected results to match implementation.

---

## 6. Complete-History Forgery

Construct a completely internally consistent alternate history:

```text
new genesis
→
valid hash chain
→
valid evidence records
→
valid local trust anchor
```

Replace the legitimate local state.

Determine whether the system can distinguish:

```text
LEGITIMATE HISTORY
```

from:

```text
NEWLY CONSTRUCTED VALID HISTORY
```

If it cannot, explicitly record:

```text
LOCAL CONSISTENCY ≠ EXTERNAL AUTHENTICITY
```

---

## 7. Trust-Anchor Replacement Attacks

Attack:

```text
trust_anchor.json
```

with:

```text
modified latest hash
modified genesis hash
modified block count
complete replacement
rollback
database + anchor replacement
```

Record which attacks are detected and which are not.

---

## 8. Trust-Anchor Independence

Determine what must be independent from the local attacker:

```text
storage independence
key independence
process independence
administrative independence
network independence
time-source independence
organizational independence
```

Do not assume an external service is automatically independent.

Document the actual trust relationship.

---

## 9. Trust Hierarchy Analysis

Investigate a threat-dependent hierarchy:

```text
LEVEL 0
local runtime state

LEVEL 1
local cryptographic history

LEVEL 2
independently protected local key/material

LEVEL 3
separately controlled external anchor

LEVEL 4
governance / human authority
```

This is an analytical model, not a mandatory implementation.

Determine which level is required for:

```text
low-risk action
release
deployment
security modification
authority modification
self-modification
```

---

## 10. Hash-Chain Boundary

Explicitly test:

```text
hash chain
=
trustworthy history
```

Determine which properties the mechanism actually provides:

```text
internal tamper detection
record linkage
continuity
authenticity
freshness
non-repudiation
```

Do not attribute properties to hashing that it does not establish.

---

## 11. Temporal Semantics

RTC-010 added wall-clock monotonicity checks, but this is not equivalent to a complete temporal model.

Distinguish:

```text
WALL-CLOCK TIME
MONOTONIC ELAPSED TIME
LOGICAL EVENT ORDER
TRUSTED EXTERNAL TIME
PERSISTED TEMPORAL STATE
```

For each define:

```text
purpose
threat
guarantee
failure mode
```

---

## 12. Wall-Clock Testing

Test:

```text
clock rollback
clock jump
clock correction
timezone change
manual time change
synchronization failure
```

Determine where wall-clock time is appropriate for:

```text
human-readable timestamps
cross-machine correlation
evidence timestamps
policy expiration
```

---

## 13. Monotonic-Time Testing

Determine whether a monotonic elapsed-time source should govern:

```text
freshness windows
timeouts
execution deadlines
race mitigation
```

Test wall-clock rollback/jump while observing elapsed-time behavior.

---

## 14. Logical Event Ordering

Where exact clock synchronization is unavailable, investigate:

```text
sequence numbers
logical counters
causal relationships
```

Do not use timestamps as the only ordering mechanism where causality matters.

---

## 15. Trusted External Time

Determine whether high-risk operations require an independently trusted temporal reference.

If so, document:

```text
why
threat addressed
behavior when unavailable
disagreement resolution
```

---

## 16. Action-Class-Specific Freshness

Do not assume one freshness threshold applies to every action.

Evaluate separately:

```text
informational response
compile
release
deployment
external write
security change
authority change
self-modification
```

For each action class define:

```text
maximum acceptable assurance age
required time source
required verification freshness
behavior on time-source failure
```

---

## 17. Clock + Persistence + Trust-Anchor Attack

Mandatory cross-layer experiment:

```text
assurance established
 ↓
ledger persisted
 ↓
trust anchor persisted
 ↓
attacker modifies local clock
 ↓
attacker replaces / rolls back local state
 ↓
process crashes
 ↓
process restarts
 ↓
recovery executes
 ↓
privileged action requested
```

Determine whether the system can:

```text
detect
block
reassess
```

the attack.

---

## 18. Recovery Semantics

Test:

```text
trust anchor unavailable
trust anchor corrupted
trust anchor disagrees with ledger
clock unavailable
clock disagrees with persisted state
external anchor unavailable
key unavailable
key revoked
ledger unavailable
```

Define explicit outcomes:

```text
continue
degrade
REASSESSMENT_REQUIRED
block
escalate
```

---

## 19. Replay Resistance

Test replay of:

```text
old evidence
old assurance state
old trust anchor
old signed records
old deployment authorization
```

against:

```text
new target
new verifier
new policy
new environment
new action
```

Evidence must remain bound to its intended scope.

---

## 20. Historical Evidence Semantics

Preserve:

```text
what was evaluated
when it was evaluated
target version
verifier version
policy
environment
evidence
trust anchor
```

A new verifier must not silently rewrite historical evidence.

---

## 21. Trust-Anchor Rotation

If a cryptographic or external anchor is introduced, test:

```text
anchor V1
 ↓
rotation
 ↓
anchor V2
```

Historical records must remain interpretable.

Test:

```text
old anchor
new anchor
revoked anchor
missing anchor
compromised anchor
```

---

## 22. Adversarial Matrix

Create:

`ENG-RTC-011-INDEPENDENT-TRUST-TEMPORAL-MATRIX`

At minimum:

| Attack | Expected Result |
|---|---|
| Local ledger rewrite | Detection / reassessment |
| Local anchor rewrite | Detection / reassessment |
| Ledger + anchor rewrite | Must not silently become trusted |
| Entire alternate history | Authenticity challenge detected |
| Ledger rollback | Rejected |
| Anchor rollback | Rejected |
| Clock rollback | No freshness restoration |
| Clock jump | Conservative response |
| Clock desync | Explicit handling |
| Clock + restart | No stale assurance restoration |
| Evidence replay | Rejected when scope incompatible |
| Verifier replay | Historical binding preserved |
| Key compromise | Defined trust response |
| Key rotation | Historical evidence remains interpretable |
| Anchor unavailable | Defined degraded/block behavior |
| Anchor disagreement | Explicit conflict handling |
| Combined local-substrate compromise | No silent privileged authorization |

---

## 23. Required Evidence

For every experiment record:

```yaml
experiment:
  id: ...
  threat_model: ...
  setup: ...
  attacker_capabilities: []
  expected_result: ...
  actual_result: ...
  evidence_refs: []
  failure: ...
  residual_risk: ...
```

Do not provide only prose conclusions.

---

## 24. Specification Reconciliation

If RTC-011 reveals that existing specifications overstate guarantees, identify exact documents and sections.

Potentially affected:

```text
IV-010
IV-011
IV-012
IV-013
IV-014
IV-015
```

Review terminology around:

```text
tamper-resistant
immutable
authentic
non-repudiation
trusted
verified
fresh
persistent
```

Do not silently strengthen or weaken definitions.

---

## 25. Required Deliverable

Produce:

```text
ENG-RTC-011-INDEPENDENT-TRUST-ANCHOR-AND-TEMPORAL-SEMANTICS.md
```

It must contain:

### A. RTC-010 Review

```text
what was demonstrated
what remains unresolved
```

### B. Threat Model

```text
attacker capabilities
assets
trust boundaries
```

### C. Trust Property Definitions

```text
integrity
continuity
authenticity
freshness
durability
non-repudiation
```

### D. Trust Hierarchy

```text
local
independent
external
governance
```

with explicit rationale.

### E. Temporal Model

```text
wall clock
monotonic time
logical ordering
external time
```

### F. Implementation Changes

```text
change
reason
affected component
```

### G. Adversarial Experiments

Include all required attacks and actual evidence.

### H. Cross-Layer Attack

Include:

```text
clock
+
ledger
+
anchor
+
restart
+
privileged action
```

### I. Remaining Failures

Do not hide them.

### J. Specification Revisions

Identify exact sections requiring change.

---

## 26. Acceptance Criteria

ENG-RTC-011 is complete only when:

```text
[ ] local trust-substrate attacker model executed
[ ] complete-history forgery tested
[ ] ledger + anchor simultaneous replacement tested
[ ] trust-anchor replacement tested
[ ] trust-anchor rollback tested
[ ] hash-chain security boundary demonstrated
[ ] trust property distinctions documented
[ ] temporal semantics documented
[ ] wall-clock attacks tested
[ ] monotonic-time behavior tested
[ ] logical ordering considered/tested where applicable
[ ] action-class freshness evaluated
[ ] clock + persistence + anchor attack executed
[ ] replay attacks executed
[ ] key compromise analyzed/tested where applicable
[ ] key rotation analyzed/tested where applicable
[ ] anchor failure semantics tested
[ ] recovery semantics tested
[ ] remaining weaknesses documented
[ ] specification conflicts documented
```

---

## 27. Capability Freeze

Until RTC-011 is completed:

```text
NO NEW GENERAL AGENT CAPABILITIES
NO UNRESTRICTED AUTONOMY
NO LARGE MEMORY EXPANSION
NO UNRESTRICTED SELF-MODIFICATION
```

The trust substrate must be hardened before increasing the capabilities that depend upon it.

---

## 28. Engineering Philosophy

The objective remains:

```text
BREAK IT
 ↓
UNDERSTAND IT
 ↓
HARDEN IT
 ↓
ATTACK THE HARDENED VERSION
 ↓
RECORD THE EVIDENCE
```

A valuable outcome may be demonstrating:

```text
LOCAL CONSISTENCY
≠
AUTHENTIC HISTORY
```

or:

```text
LOCAL TIME
≠
TRUSTED TIME
```

If such a limitation is demonstrated, document it rather than hiding it.

---

## 29. Final Instruction

Proceed with:

```text
ENG-RTC-011
INDEPENDENT TRUST ANCHORING
& TEMPORAL SEMANTICS
```

Do not report production-grade assurance unless the experiments establish the corresponding property.

The next engineering response must contain:

```text
ENG-RTC-011-INDEPENDENT-TRUST-ANCHOR-AND-TEMPORAL-SEMANTICS.md
```

with implementation evidence, adversarial results, residual risks, and proposed specification revisions.

**Do not expand intelligence capabilities until the trust-boundary questions above have been experimentally addressed.**
