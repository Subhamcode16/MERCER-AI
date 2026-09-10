# II-017 — Self-Critique, Adversarial Verification & Meta-Validation Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Depends On:** II-001 through II-016  
**Scope:** Self-critique, adversarial verification, evaluator independence, meta-validation, non-circular verification, seeded failures, hidden attacks, critic benchmarking, and evidence integrity

---

## 1. Purpose

II-017 defines the architecture's internal challenge layer.

The system must not be considered trustworthy merely because it can generate, reason, evaluate, or explain. It must also be able to:

- question its own decisions;
- identify unsupported assumptions and omissions;
- actively attempt to break its own implementation;
- detect weaknesses in its evaluators;
- preserve contradictory evidence; and
- convert discovered failures into regression tests.

The three functions are distinct:

```text
SELF-CRITIQUE
ADVERSARIAL VERIFICATION
META-VALIDATION
```

---

## 2. Core Principle

> **A system cannot establish its own correctness merely by producing an explanation that says it is correct.**

The intended chain is:

```text
SYSTEM OUTPUT
    ↓
SELF-CRITIQUE
    ↓
ADVERSARIAL VERIFICATION
    ↓
INDEPENDENT EVALUATION
    ↓
META-VALIDATION
    ↓
EVIDENCE
```

Evidence remains subordinate to the actual test conditions and cannot be replaced by confidence or explanation.

---

## 3. Three Challenge Layers

### 3.1 Self-Critique

Searches for:

```text
assumptions
omissions
contradictions
unsupported claims
constraint violations
authority risks
evidence gaps
strategic drift
provenance gaps
uncertainty
```

### 3.2 Adversarial Verification

Actively attempts to:

```text
invalidate
exploit
bypass
spoof
contradict
manipulate
```

the system under test.

### 3.3 Meta-Validation

Evaluates whether the critic, verifier, evaluator, and benchmark themselves are reliable.

It examines:

```text
critic quality
attack coverage
false negatives
false positives
independence
correlated failure
benchmark contamination
evaluator manipulation
```

---

## 4. Independence Principle

The architecture must avoid:

```text
GENERATOR
   ↓
CRITIC
   ↓
CRITIC AGREES
   ↓
PASS
```

because the critic may share the generator's:

```text
model
prompt
knowledge
assumptions
biases
failure modes
```

Therefore:

> **Independence is a property to be measured, not assumed.**

Potential independence dimensions:

```text
MODEL
PROMPT
KNOWLEDGE
RETRIEVAL
EVALUATOR
DATA
OBJECTIVE
IMPLEMENTATION
```

Different claims may require different degrees of independence.

---

## 5. Self-Critique Contract

The critic receives a bounded context containing:

```text
target_object
target_version
requirements
constraints
evidence
authority_context
decision_context
```

It produces structured findings such as:

```text
ERROR
OMISSION
CONTRADICTION
UNSUPPORTED_CLAIM
CONSTRAINT_RISK
AUTHORITY_RISK
EVIDENCE_GAP
STRATEGIC_DRIFT
PROVENANCE_GAP
UNCERTAINTY
```

A finding should preserve:

```text
finding_id
target
finding_type
severity
claim
supporting_evidence
counter_evidence
confidence
recommended_action
scope
```

The critic primarily **finds**; recovery or decision agents determine what to do.

The critic must support:

```text
UNABLE_TO_ASSESS
```

when evidence is insufficient.

Critic quality must measure both:

```text
FALSE CRITIQUE RATE
CRITICAL FAILURE RECALL
```

---

## 6. Adversarial Verification Contract

The verifier explicitly asks:

```text
What assumption can I break?
What authority can I spoof?
What evidence can I contradict?
What dependency can I invalidate?
What constraint can I force into conflict?
What evaluation can I manipulate?
What state transition can I bypass?
What output can I make look valid while being wrong?
```

### Attack classes

```text
SEMANTIC
AUTHORITY
EVIDENCE
LIFECYCLE
GOVERNANCE
RUNTIME
PROMPT
EVALUATION
PROVENANCE
RECOVERY
CROSS-DOMAIN
```

Examples include:

- authority spoofing and scope escalation;
- fake or weak evidence;
- invalid lifecycle transitions;
- unauthorized overrides;
- stale writes and dependency bypass;
- prompt/context injection;
- false PASS and metric gaming;
- false provenance;
- recovery-induced strategic drift;
- cross-domain constraint manipulation.

---

## 7. Seeded, Hidden, and Novel Failures

The validation corpus must contain:

```text
KNOWN FAILURES
HIDDEN FAILURES
NOVEL ATTACK OPPORTUNITIES
KNOWN NON-FAILURES
```

Known failures establish recall.

Hidden failures test generalization.

Novel discovery measures whether the verifier can find problems not explicitly seeded.

Track:

```text
NOVEL FAILURE DISCOVERY RATE
```

Attack diversity must vary:

```text
mechanism
domain
severity
object type
agent
execution stage
```

Attack budgets should control:

```text
time
compute
tools
attempts
```

---

## 8. Attack Outcomes

Each attack should terminate as one of:

```text
BLOCKED
DETECTED
MISSED
PARTIALLY_DETECTED
FALSE_ALARM
SYSTEM_FAILURE
```

An attack succeeds when it causes a defined invariant violation without detection or controlled escalation.

---

## 9. Critic / Verifier / Evaluator Separation

These roles remain distinct:

```text
SELF-CRITIQUE
→ inspect

ADVERSARIAL VERIFICATION
→ attack

EVALUATOR
→ assess correctness

META-VALIDATION
→ assess the validators
```

No component certifies itself.

```text
Critic says "no issue"
≠
system is correct

Verifier finds no attack
≠
system is secure
```

The latter means only:

```text
NO FAILURE FOUND UNDER THE TESTED ATTACK BUDGET
```

---

## 10. No Self-Certification

A PASS cannot arise solely because:

```text
Generator says PASS
```

or:

```text
Generator + Critic agree
```

Required evaluation authority must remain independent according to the applicable contract.

Likewise, failure to find a problem is:

```text
NOT_FOUND
```

not automatically:

```text
PROVEN_ABSENT
```

---

## 11. Benchmark Contracts

### Critic benchmark

Must contain:

```text
KNOWN_GOOD
KNOWN_BAD
SUBTLY_BAD
AMBIGUOUS
INSUFFICIENT_EVIDENCE
CONFLICTED
ADVERSARIAL
```

Measure:

```text
precision
recall
severity calibration
abstention
critical-failure recall
```

### Verifier benchmark

Must contain:

```text
known vulnerabilities
hidden vulnerabilities
novel attack opportunities
non-vulnerabilities
```

Measure:

```text
attack success
failure discovery
false alarms
novel discovery
coverage
```

### Evaluator benchmark

Must contain:

```text
clear pass
clear fail
borderline
insufficient evidence
adversarially misleading
```

Measure:

```text
false PASS
false FAIL
abstention
calibration
```

---

## 12. Independence Testing

A controlled matrix should compare combinations such as:

```text
Generator A + Critic A
Generator A + Critic B
Generator B + Critic A
Generator B + Critic B
```

Measure:

```text
failure overlap
critique agreement
missed-failure correlation
```

Likewise vary:

```text
model
attack strategy
prompt
knowledge source
evaluation mechanism
```

High agreement may indicate shared blind spots rather than reliability.

---

## 13. Cross-Verification

Where practical:

```text
Verifier A
→ challenge

Verifier B
→ independently challenge

Evaluator
→ adjudicate
```

Disagreement must be preserved.

If:

```text
A = PASS
B = FAIL
```

the system must not erase the disagreement merely to produce a clean result.

---

## 14. Circularity Detection

The architecture must detect circular validation such as:

```text
Generator
→ Critic
→ Evaluator
→ all rely on Generator's own claims
→ PASS
```

Potential circularity indicators include shared:

```text
model
prompt
evidence
retrieval
evaluator
benchmark
```

An independence matrix should expose these dependencies rather than asserting independence.

---

## 15. Blind-Spot Analysis

Periodically compare:

```text
Critic findings
Verifier findings
Evaluator findings
Human findings
Production failures
```

to identify systematic blind spots.

Production failures should feed back:

```text
PRODUCTION FAILURE
 ↓
CLASSIFY
 ↓
ROOT CAUSE
 ↓
BENCHMARK CASE
 ↓
CRITIC TEST
 ↓
ADVERSARIAL TEST
 ↓
REGRESSION
```

Critic, verifier, evaluator, and attack-corpus versions must remain traceable.

---

## 16. Meta-Validation

Meta-validation evaluates:

```text
critic
verifier
evaluator
benchmark
```

Potential metrics:

```text
CRITICAL FAILURE RECALL
FALSE CRITIQUE RATE
CRITIC PRECISION
ADVERSARIAL DISCOVERY RATE
NOVEL FAILURE DISCOVERY
ATTACK SUCCESS RATE
FALSE ALARM RATE
VERIFIER COVERAGE
EVALUATOR CALIBRATION
CROSS-VERIFIER AGREEMENT
FAILURE CORRELATION
BENCHMARK LEAKAGE RATE
```

No single metric establishes trustworthiness.

An "independence score" is diagnostic only; it is not proof of independence.

---

## 17. Negative and Contradictory Evidence

The evidence system must preserve:

```text
DIRECT
INDIRECT
CORRELATED
WEAK
STRONG
CONTRADICTORY
INCONCLUSIVE
```

If evidence contradicts an architectural claim, possible outcomes include:

```text
REVISE CLAIM
NARROW CLAIM
CHANGE ARCHITECTURE
REMOVE COMPONENT
ADD CONSTRAINT
ABANDON CLAIM
```

There must be no automatic defensive rationalization.

---

## 18. Falsification Protocol

When a claim appears to fail:

```text
DETECT
 ↓
VERIFY FAILURE
 ↓
CHECK REPLICATION
 ↓
ANALYZE SCOPE
 ↓
DECIDE
```

The correct conclusion may be:

```text
THE ARCHITECTURE WAS WRONG
```

This is an acceptable research outcome.

---

## 19. Adversarial Safety

The adversarial verifier remains governed.

It must not receive unrestricted authority to:

```text
modify production state
delete data
change campaign intent
disable security
```

without explicit authorization.

Where attacks could cause side effects, verification should occur in a sandbox.

Every successful attack must preserve:

```text
attack_id
attack_version
target_version
inputs
parameters
execution_context
observed_failure
```

so it can become a regression case.

---

## 20. Self-Critique and Verifier Drift

Critics and verifiers can become stale as the architecture changes.

Track:

```text
critic_version
verifier_version
evaluator_version
architecture_version
knowledge_version
benchmark_version
attack_corpus_version
```

Major architecture changes should trigger revalidation.

---

## 21. Meta-Validation Experiments

The initial experiment program should include:

### A — Same-model critic agreement
Compare same-model and independent critics.

### B — Verifier diversity
Compare one attack strategy with diverse attack strategies.

### C — Hidden failure set
Evaluate against failures unknown during development.

### D — Blind-spot transfer
Test whether one critic's missed failures are also missed by another.

### E — Evaluator correlation
Compare evaluator decisions against independent adjudication.

### F — Benchmark gaming
Optimize against a visible benchmark, then test on a hidden benchmark.

### G — Architecture-change regression
After architectural changes, run old tests, hidden tests, and new attacks.

---

## 22. Hypotheses

### H-011 — Self-Critique

A dedicated self-critique mechanism detects a higher proportion of meaningful weaknesses than generator self-review alone.

### H-012 — Adversarial Verification

A dedicated adversarial verifier discovers critical failures missed by ordinary evaluation and self-critique.

### H-013 — Independence

Increasing evaluator diversity reduces correlated false PASS decisions.

### H-014 — Hidden Failures

A robust adversarial verifier retains meaningful failure-detection performance on hidden and novel attack cases.

### H-015 — Meta-Validation

Meta-validation detects weaknesses in critics, verifiers, evaluators, and benchmarks that would otherwise create false confidence.

### H-016 — Regression

Converting discovered failures into persistent regression cases reduces recurrence of previously observed architectural failures.

---

## 23. Validation Invariants

1. Self-critique is not proof of correctness.
2. Adversarial verification is not proof of security.
3. No component can certify itself.
4. Critic and verifier roles remain distinct.
5. Meta-validation evaluates validators themselves.
6. Independence must be tested, not assumed.
7. Failure-to-detect is a first-class result.
8. Negative evidence is not proof of absence.
9. Hidden tests remain protected from benchmark optimization.
10. Known failures become regression cases.
11. Novel failures are explicitly measured.
12. Critical invariant violations override aggregate quality scores.
13. Evaluator disagreement remains preserved.
14. Correlated evaluator errors are explicitly considered.
15. Adversarial execution is governed and sandboxed.
16. Critic, verifier, evaluator, and benchmark versions are traceable.
17. Contradictory evidence cannot be silently removed.
18. Architectural claims remain falsifiable.
19. Production failures feed the regression corpus.
20. Evidence may force architectural revision or falsification.

---

## 24. Architecture Proof Boundary

After II-017, the architecture can legitimately claim:

> **We have defined a system for testing whether our architectural claims are true.**

It cannot automatically claim:

> **Our architecture is true.**

That conclusion must emerge from actual experiments.

The correct distinction is:

```text
DESIGN
  ↓
IMPLEMENTATION
  ↓
TEST
  ↓
EVIDENCE
  ↓
SUPPORTED / CONTESTED / FALSIFIED CLAIM
```

---

## 25. Phase II Completion Model

```text
II-001 → II-012
SEMANTIC FOUNDATION
        ↓
II-013
GOVERNANCE
        ↓
II-014
LIFECYCLE
        ↓
II-015
RUNTIME
        ↓
II-016
EMPIRICAL VALIDATION
        ↓
II-017
SELF-CRITIQUE + ADVERSARIAL + META-VALIDATION
        ↓
PHASE III
IMPLEMENTATION + EXPERIMENTATION
```

---

## 26. Core Contract

> **The Self-Critique, Adversarial Verification & Meta-Validation Layer shall provide independent, governed mechanisms for identifying weaknesses, actively attempting to break system assumptions and implementations, and evaluating the reliability of the validators themselves. It shall prevent circular self-certification, measure evaluator and critic independence, preserve negative and contradictory evidence, maintain hidden and adversarial test sets, convert discovered failures into regression cases, sandbox adversarial execution, and require architectural claims to remain falsifiable.**

---

## 27. Deferred Decisions

II-017 does not freeze:

- critic model;
- verifier model;
- evaluator model;
- attack-generation framework;
- sandbox implementation;
- independence scoring method;
- statistical methodology;
- human adjudication workflow;
- hidden benchmark infrastructure;
- attack budgets;
- production deployment topology.

These remain implementation and research decisions.

---

## 28. Phase II Exit Criteria

- [x] Self-critique defined
- [x] Adversarial verification defined
- [x] Meta-validation defined
- [x] Independence principle established
- [x] Correlation risk established
- [x] Critique benchmark established
- [x] Verifier benchmark established
- [x] Evaluator benchmark established
- [x] Seeded failures established
- [x] Hidden attacks established
- [x] Novel failure discovery established
- [x] Circularity detection established
- [x] Cross-verification established
- [x] Negative evidence semantics established
- [x] Blind-spot analysis established
- [x] Production failure feedback established
- [x] Critic/verifier/evaluator drift established
- [x] Falsification protocol established
- [x] Adversarial safety established
- [x] Meta-validation experiments established
- [x] H-011 through H-016 established
- [x] Validation invariants established
- [x] Architecture proof boundary established
- [x] Phase II completion model established

**Current assessment:** Phase II semantic specification set is complete, subject to ratification and later empirical validation.

---

# 29. Required Next Phase

After ratification of II-013 through II-017:

```text
1. RATIFY II-013 → II-017
2. Freeze the semantic baseline
3. Convert contracts into machine-readable schemas
4. Define the first benchmark corpus
5. Define the architectural claim registry
6. Implement the minimum reference runtime
7. Implement governance and lifecycle enforcement
8. Implement evaluator
9. Implement self-critique
10. Implement adversarial verification
11. Build the evidence ledger
12. Run controlled experiments
13. Record failures
14. Update regression corpus
15. Re-evaluate architectural claims
```

The first implementation objective should be:

> **Build the smallest executable system capable of falsifying our own architecture.**

Not:

> **Build the largest possible production system.**
