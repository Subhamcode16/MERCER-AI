# ENG-RTC-010 — Trust Anchor, Persistent Evidence & Temporal Integrity Hardening

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** NEXT REQUIRED ENGINEERING ACTION  
**Priority:** HIGH  
**Depends On:** ENG-RTC-009, IV-010, IV-011, IV-012, IV-013

---

# 1. Purpose

ENG-RTC-010 follows the successful prototype hardening experiments performed under ENG-RTC-009.

ENG-RTC-009 demonstrated the requested prototype behavior for:

```text
correlated verification attack
freshness race / TOCTOU
multidimensional assurance
evidence tampering
ledger modification
ledger deletion
gate bypass
```

However, the engineering report identifies two remaining infrastructure-level weaknesses:

```text
A — Temporal integrity depends on system clock behavior.
B — AssuranceLedger persistence is currently in-memory.
```

The next objective is therefore:

```text
TRUSTED TIME
+
DURABLE ASSURANCE HISTORY
+
EVIDENCE PROVENANCE
+
RECOVERY INTEGRITY
```

The goal is not to select technologies prematurely.

The goal is first to establish which security properties the assurance architecture actually requires and then experimentally determine whether the implementation provides them.

---

# 2. Current Evidence Boundary

ENG-RTC-009 demonstrated prototype hardening, but it did not establish production-grade assurance.

Current position:

```text
MINIMUM ASSURANCE LOOP
→ FUNCTIONALLY DEMONSTRATED

CORRELATED VERIFICATION
→ HARDENED IN PROTOTYPE

FRESHNESS RACE
→ HARDENED IN PROTOTYPE

MULTIDIMENSIONAL ASSURANCE
→ IMPLEMENTED

EVIDENCE INTEGRITY
→ PROTOTYPE VERIFIED

LEDGER TAMPER DETECTION
→ PROTOTYPE VERIFIED

TEMPORAL INTEGRITY
→ NOT YET ESTABLISHED

DURABLE ASSURANCE HISTORY
→ NOT YET ESTABLISHED

TRUST ANCHOR
→ NOT YET ESTABLISHED
```

Do not represent the architecture as production-grade assurance until the remaining properties are experimentally established.

---

# 3. Finding A — Temporal Integrity

The current freshness model depends on:

```text
time.time()
```

This creates an attack surface if the system clock is:

```text
manipulated
desynchronized
incorrect
rolled backward
jumped forward
restored incorrectly
```

The current freshness mechanism must therefore be tested against temporal attacks.

---

# 4. Temporal Security Properties

Before selecting an implementation mechanism, define the required properties.

At minimum investigate:

```text
temporal monotonicity
freshness validity
clock rollback resistance
clock jump resistance
clock desynchronization handling
restart continuity
timestamp provenance
```

Do not assume all operations require identical temporal guarantees.

Classify each temporal dependency by risk.

---

# 5. Distinguish Time Sources

Investigate the semantic differences between:

```text
wall-clock time
monotonic elapsed time
process-relative time
trusted external time
persisted logical time
```

Determine which should be used for:

```text
freshness deadlines
event ordering
audit timestamps
evidence validity
cross-process correlation
cross-machine correlation
replay prevention
```

The implementation should explicitly document why each time source is selected.

---

# 6. Temporal Attack Matrix

Create experiments for:

| Attack | Expected Property |
|---|---|
| Clock moved backward | Freshness cannot become valid merely because time moved backward |
| Clock moved forward | System cannot incorrectly invalidate unrelated evidence without explicit policy |
| Large clock jump | Safe degradation / reassessment |
| Clock desynchronization | Explicit detection or conservative behavior |
| Monitor timestamp altered | Evidence validity is affected appropriately |
| Clock changed during authorization | Gate remains safe |
| Clock changed during monitoring | Freshness semantics remain bounded |
| Restart after clock change | Historical temporal state remains coherent |
| Replay with manipulated timestamp | Replay is rejected where applicable |

Record:

```text
attack
setup
expected
actual
evidence
```

---

# 7. Freshness Must Not Be Bypassable Through Clock Manipulation

Test the following scenario:

```text
T0:
assurance is valid

T1:
assurance becomes stale

T2:
clock is manipulated

T3:
system evaluates freshness again
```

Determine whether the system can incorrectly transition:

```text
STALE
→
CURRENT
```

without a legitimate verification event.

If yes, this is a security failure.

---

# 8. Temporal Integrity Across Restart

Test:

```text
assurance established
 ↓
process shutdown
 ↓
clock change
 ↓
process restart
 ↓
assurance recovery
```

Determine whether the system incorrectly restores old assurance.

The safe behavior must be explicitly defined.

Possible outcomes:

```text
restore
revalidate
expire
reassess
block
```

depending on the assurance scope and action risk.

---

# 9. Finding B — In-Memory Assurance Ledger

ENG-RTC-009 identifies that the current `AssuranceLedger` exists in memory and loses continuity across process restart.

This creates the following problem:

```text
ASSURANCE HISTORY
 ↓
PROCESS CRASH
 ↓
MEMORY LOST
 ↓
LEDGER RESET
```

The system must not silently interpret:

```text
missing history
```

as:

```text
clean history
```

or:

```text
valid assurance
```

---

# 10. Required Persistence Model

Implement durable assurance history.

The implementation must support:

```text
write
persist
shutdown
restart
recover
validate
continue
```

without silently rewriting historical state.

The exact storage technology is an engineering decision.

Do not select a database merely because it is convenient.

First define the required properties.

---

# 11. Persistence Security Properties

Investigate:

```text
durability
integrity
ordering
atomicity
recovery
rollback detection
duplicate detection
truncation detection
historical continuity
```

---

# 12. Crash-Recovery Experiment

Perform:

```text
write event N
 ↓
force process crash
 ↓
restart
 ↓
recover ledger
 ↓
validate chain
```

Test multiple crash positions:

```text
before write
during write
after write
before flush
after flush
during recovery
```

Determine whether the recovered state is:

```text
valid
invalid
partial
unknown
```

and ensure the system does not silently convert:

```text
UNKNOWN
→
VALID
```

---

# 13. Partial-Write Attack

Simulate:

```text
ledger entry partially written
```

The system should detect the incomplete state.

Expected behavior:

```text
integrity failure
+
recovery procedure
```

rather than silent continuation.

---

# 14. Ledger Rollback Attack

Create:

```text
Ledger state N
```

then replace it with:

```text
older Ledger state N-k
```

Determine whether the system can detect that historical state has been rolled back.

This is important because:

```text
hash chaining
```

alone may detect internal inconsistency but does not automatically prove that the presented chain is the newest legitimate chain.

---

# 15. Entire-Chain Replacement Attack

Construct a completely new internally valid hash chain.

Then attempt to substitute it for the legitimate history.

Ask:

```text
Can the system distinguish:

LEGITIMATE HISTORY

from

NEWLY CONSTRUCTED VALID HISTORY?
```

This experiment is mandatory.

It will determine whether we require a trust anchor beyond local hash chaining.

---

# 16. Distinguish Four Properties

Do not collapse the following into one concept:

```text
TAMPER DETECTION
HISTORY AUTHENTICITY
HISTORY DURABILITY
NON-REPUDIATION
```

For each property, specify:

```text
what it means
what threat it addresses
what mechanism establishes it
what evidence demonstrates it
```

---

# 17. Hash-Chaining Evaluation

ENG-RTC-009 proposed hash chaining for ledger integrity.

Do not assume:

```text
HASH CHAIN
=
IMMUTABLE HISTORY
```

A hash chain can establish relationships between records.

It does not automatically establish:

```text
external authenticity
latest-state authenticity
non-repudiation
durability
```

Test these boundaries explicitly.

---

# 18. Trust Anchor Investigation

Determine whether high-risk assurance records require an external or independently protected trust anchor.

Candidate mechanisms may include:

```text
digital signatures
hardware-backed keys
external append-only storage
independent audit service
immutable object storage
trusted timestamping
separate governance authority
```

These are candidates for investigation, not predetermined implementation requirements.

The engineer must establish:

```text
property
→ threat
→ mechanism
→ evidence
```

before selecting one.

---

# 19. Evidence Provenance

Every consequential assurance record should be traceable to:

```text
target version
verifier version
test protocol
environment
inputs
configuration
time context
evidence digest
decision
```

Determine whether the current implementation preserves all required provenance after restart.

---

# 20. Evidence Replay

Construct:

```text
VALID OLD EVIDENCE
```

and attempt to reuse it against:

```text
NEW TARGET VERSION
NEW VERIFIER VERSION
NEW ENVIRONMENT
NEW POLICY
EXPIRED FRESHNESS WINDOW
```

The system must reject evidence reuse where its scope is incompatible.

---

# 21. Historical Evidence Must Remain Historical

A new verifier or policy must not silently rewrite old evidence.

Test:

```text
Evidence generated under V1
 ↓
Verifier V2 introduced
 ↓
Historical evidence inspected
```

The system must preserve:

```text
what was evaluated
when
under which verifier
under which policy
```

---

# 22. Recovery Semantics

Define explicit behavior for:

```text
ledger unavailable
ledger corrupted
ledger partially recovered
ledger missing
trust anchor unavailable
clock unavailable
clock disagreement
evidence unavailable
```

Possible outcomes:

```text
continue
degrade
reassess
block
escalate
```

The decision must depend on risk.

---

# 23. Assurance After Restart

Test:

```text
ASSURANCE = VERIFIED
 ↓
PROCESS CRASH
 ↓
RESTART
```

Determine whether the system should:

```text
retain assurance
revalidate assurance
expire assurance
```

for each action class.

Do not make one global assumption.

For example:

```text
low-risk informational claim
```

may have different restart semantics from:

```text
production deployment authorization
```

---

# 24. Temporal + Persistence Interaction

The most important integration experiment combines both weaknesses:

```text
assurance established
 ↓
ledger persisted
 ↓
clock manipulated
 ↓
process crashes
 ↓
process restarts
 ↓
ledger recovered
 ↓
freshness evaluated
 ↓
execution requested
```

Determine whether an attacker can exploit the combination to restore stale assurance.

This is a cross-layer attack.

---

# 25. Required Test Matrix

Create:

`ENG-RTC-010-TEMPORAL-PERSISTENCE-MATRIX`

At minimum:

| Attack | Expected Result |
|---|---|
| Clock rollback | No artificial freshness restoration |
| Clock jump forward | Conservative policy response |
| Clock desync | Detection / reassessment |
| Clock manipulation during gate | No unsafe authorization |
| Restart after clock change | No silent restoration of stale assurance |
| Crash before ledger write | No false event |
| Crash during ledger write | Partial write detected |
| Crash after ledger write | Event recoverable |
| Ledger rollback | Rollback detected |
| Ledger truncation | Integrity failure detected |
| Entire-chain replacement | Trust-anchor analysis detects/flags ambiguity |
| Old evidence replay | Rejected when scope incompatible |
| Old verifier evidence under new verifier | Historical binding preserved |
| Ledger unavailable | Explicit safe degradation |
| Trust anchor unavailable | Explicit policy response |
| Clock + restart combined attack | No stale-assurance restoration |

---

# 26. Required Deliverable

Produce:

```text
ENG-RTC-010-TRUST-ANCHOR-TEMPORAL-INTEGRITY.md
```

The document must contain:

## A. Findings

```text
issue
root cause
affected specification
severity
```

## B. Threat Model

For:

```text
clock
ledger
evidence
storage
restart
trust anchor
```

## C. Required Security Properties

Explicitly distinguish:

```text
temporal integrity
tamper detection
history authenticity
history durability
non-repudiation
evidence provenance
replay resistance
```

## D. Implementation Changes

```text
change
reason
affected component
```

## E. Adversarial Experiments

For every experiment:

```text
attack
setup
expected result
actual result
evidence
```

## F. Recovery Experiments

Include:

```text
crash
restart
partial write
rollback
corruption
```

## G. Trust Anchor Analysis

Do not simply recommend a technology.

Explain:

```text
threat
→ required property
→ candidate mechanism
→ tradeoff
→ evidence
```

## H. Remaining Failures

Do not hide failures.

## I. Specification Revisions

If IV-010 through IV-014 require modification:

```text
document
section
proposed change
rationale
```

---

# 27. Acceptance Criteria

ENG-RTC-010 is complete only when:

```text
[ ] temporal attack matrix executed
[ ] clock rollback tested
[ ] clock jump tested
[ ] clock desynchronization tested
[ ] freshness bypass through clock manipulation tested
[ ] restart after clock change tested
[ ] durable ledger implemented or justified
[ ] crash recovery tested
[ ] partial write tested
[ ] ledger rollback tested
[ ] ledger truncation tested
[ ] entire-chain replacement tested
[ ] hash-chain security boundary documented
[ ] tamper detection distinguished from authenticity
[ ] durability distinguished from authenticity
[ ] non-repudiation requirements analyzed
[ ] evidence replay tested
[ ] historical verifier binding tested
[ ] trust-anchor requirement analyzed
[ ] trust-anchor failure tested
[ ] ledger-unavailable behavior tested
[ ] combined clock + restart attack tested
[ ] remaining weaknesses documented
[ ] specification conflicts documented
```

---

# 28. Do Not Expand Intelligence Yet

Continue the current restriction:

```text
NO NEW GENERAL AGENT CAPABILITIES
NO UNRESTRICTED AUTONOMY
NO LARGE MEMORY EXPANSION
NO UNRESTRICTED SELF-MODIFICATION
```

The immediate objective remains hardening the trust substrate.

---

# 29. Engineering Philosophy

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

Do not optimize for passing tests.

Optimize for discovering whether the architecture's claims survive adversarial conditions.

---

# 30. Final Instruction

Proceed with:

```text
ENG-RTC-010
TRUST ANCHOR, PERSISTENT EVIDENCE
& TEMPORAL INTEGRITY HARDENING
```

The next engineering response must contain:

```text
ENG-RTC-010-TRUST-ANCHOR-TEMPORAL-INTEGRITY.md
```

with implementation evidence, adversarial results, recovery results, remaining failures, and proposed specification revisions.

Do not report production-grade assurance unless the experiments actually establish it.
