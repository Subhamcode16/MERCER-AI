# II-004 — Communication Intent Derivation Contract

**Status:** Engineering Specification — Draft / Under Review  
**Phase:** II — From Ratified Principles to Engineering Specification  
**Scope:** Derivation, validation, authority, provenance, and lifecycle of Communication Intents

---

## 1. Purpose

II-004 defines how the Campaign Intelligence Layer derives **Communication Intents** from authoritative campaign context.

The contract exists to prevent the system from:

- confusing product knowledge with campaign strategy,
- inventing unsupported strategic claims,
- over-interpreting weak evidence,
- allowing downstream agents to silently redefine upstream intent,
- treating inferred preferences as facts,
- or converting every piece of available knowledge into a communication requirement.

The output of this contract is a set of **traceable, confidence-aware Communication Intents** that become the upstream semantic input for the Evidence Requirement Engine.

---

# 2. Core Definition

A Communication Intent represents:

> **What the campaign needs the audience to understand, perceive, believe, feel, or do.**

An intent is therefore a **campaign-level communication decision**, not merely a topic, attribute, product property, or visual description.

### Invalid

```text
"Silk"
"Craftsmanship"
"Premium"
"Red"
"Traditional"
```

These may be knowledge attributes or themes.

### Valid intent

```text
"Make the audience perceive the product
as meticulously crafted rather than mass-produced."
```

The distinction is:

```text
KNOWLEDGE / ATTRIBUTE
        ↓
CAMPAIGN REASONING
        ↓
COMMUNICATION INTENT
```

---

# 3. Intent Derivation Boundary

The Intent Engine may reason over:

```text
Campaign Objective
Product Knowledge
Brand Knowledge
Audience Knowledge
Channel Knowledge
Market / Cultural Context
Explicit User Direction
Authoritative Campaign Constraints
```

It must not treat all retrieved information as equally authoritative.

The engine must preserve the distinction between:

```text
FACT
CONSTRAINT
OBJECTIVE
EXPLICIT INTENT
DERIVED INTENT
INFERRED INTENT
CREATIVE OPPORTUNITY
```

---

# 4. Intent Authority Classes

Every Communication Intent must have an authority class.

## 4.1 EXPLICIT

The intent is directly specified by the user or an authoritative campaign source.

Example:

```text
User:
"Position this collection as contemporary luxury."
```

This becomes an explicit intent.

Explicit intent must preserve its source.

---

## 4.2 DERIVED

The intent is logically derived from authoritative campaign information.

Example:

```text
Objective:
Launch a premium handcrafted collection.

Product knowledge:
Construction is highly detailed.

Derived intent:
Communicate visible craftsmanship as a reason
to perceive the collection as premium.
```

A derived intent must expose the reasoning chain that produced it.

---

## 4.3 INFERRED

The intent is inferred from incomplete or probabilistic contextual information.

Example:

```text
Audience:
Young consumers interested in contemporary
fashion and cultural identity.

Possible inferred intent:
Make cultural heritage feel contemporary
rather than purely traditional.
```

An inferred intent must carry:

- confidence,
- evidence,
- uncertainty,
- and an indication that it is not authoritative campaign truth.

It must never silently become an explicit intent.

---

# 5. Authority Precedence

When intents conflict:

```text
LOCKED EXPLICIT
        ↓
EXPLICIT
        ↓
DERIVED
        ↓
INFERRED
        ↓
EXPLORATORY
```

Higher-authority intent cannot be silently overridden by a lower-authority intent.

A lower-authority intent may:

```text
CHALLENGE
PROPOSE ALTERNATIVE
REQUEST REVISION
```

but not silently mutate the higher-authority intent.

---

# 6. Intent Object — Semantic Requirements

A Communication Intent should conceptually contain:

```text
intent_id
campaign_id
statement
intent_type
authority
source
provenance
confidence
priority
status
supporting_evidence
dependencies
constraints
created_by
created_at
version
```

The exact implementation schema is intentionally deferred.

---

# 7. Intent Statement Requirements

An intent statement should be:

### Audience-oriented

It should describe a desired audience interpretation or response.

### Campaign-specific

It should make sense in the context of the current campaign.

### Actionable

It should be possible to derive evidence requirements from it.

### Traceable

The system must be able to explain why it exists.

### Non-prescriptive at the execution level

It should not prematurely dictate:

```text camera
lighting
lens
crop
prompt wording
```

Those belong downstream.

---

# 8. Intent vs Execution

The following separation is mandatory:

```text
INTENT
"Make craftsmanship perceptible."

        ↓

EVIDENCE
"Visible material structure and construction detail."

        ↓

ASSET REQUIREMENT
"Create a detail asset capable of revealing construction."

        ↓

SHOT SPECIFICATION
"Macro detail with controlled directional lighting."

        ↓

PROMPT
Final generation instructions
```

The Intent Engine must stop before execution-level decisions.

---

# 9. Intent Derivation Pipeline

The canonical derivation process is:

```text
CAMPAIGN CONTEXT
        ↓
AUTHORITATIVE KNOWLEDGE ASSEMBLY
        ↓
OBJECTIVE ANALYSIS
        ↓
EXPLICIT INTENT EXTRACTION
        ↓
DERIVED INTENT GENERATION
        ↓
INFERRED INTENT GENERATION
        ↓
CONFLICT ANALYSIS
        ↓
REDUNDANCY ANALYSIS
        ↓
EVIDENCE FEASIBILITY CHECK
        ↓
INTENT VALIDATION
        ↓
ACCEPT / CHALLENGE / ESCALATE
```

---

# 10. Explicit Intent Extraction

The first operation should always be to identify intents that already exist.

The system should not derive alternatives before checking for explicit direction.

Example:

```text
User:
"Make the collection feel contemporary,
premium, and culturally rooted."
```

The system should extract those strategic instructions rather than replacing them with its own interpretation.

---

# 11. Derived Intent Generation

Derived intents are permitted when the source information supports a meaningful communication implication.

Example:

```text
Campaign Objective:
Product launch

Product Truth:
Hand-finished construction

Brand Position:
Premium craftsmanship

Derived Intent:
Make the hand-finished construction perceptible
as evidence of premium quality.
```

The derivation must be traceable:

```text
OBJECTIVE
+
PRODUCT TRUTH
+
BRAND POSITION
        ↓
DERIVED INTENT
```

---

# 12. Inference Boundary

Inference is permitted only when:

1. the information is genuinely relevant,
2. the inference is plausible,
3. the inference is useful,
4. the uncertainty is represented,
5. and the consequence of being wrong is controlled.

The system must not convert:

```text
"likely"
```

into:

```text
"known"
```

---

# 13. Insufficient Knowledge

When evidence is insufficient to derive a consequential intent, the engine should not fabricate one.

Instead:

```text
INSUFFICIENT KNOWLEDGE
        ↓
KNOWLEDGE GAP
        ↓
REQUEST / RESEARCH / ESCALATION
```

Example:

```text
Audience information:
Unknown

Attempted inference:
"Audience values sustainability."

Result:
BLOCKED / LOW CONFIDENCE

Action:
Create Knowledge Gap.
```

---

# 14. Intent Confidence

Confidence must not be confused with authority.

For example:

```text
EXPLICIT
confidence = high
```

is common but not logically mandatory.

Likewise:

```text
INFERRED
confidence = 0.91
```

does not make it authoritative.

Therefore:

```text
AUTHORITY ≠ CONFIDENCE
```

Authority answers:

> Who or what is entitled to establish this decision?

Confidence answers:

> How certain is the system that this decision is well-supported?

---

# 15. Intent Priority

Intent priority determines relative importance when the campaign contains multiple intents.

Priority should not automatically be interpreted as authority.

For example:

```text
Intent A
Authority: INFERRED
Priority: LOW

Intent B
Authority: EXPLICIT
Priority: HIGH
```

The engine must preserve both dimensions separately.

---

# 16. Intent Conflicts

Conflicts may occur between:

```text
Intent
↔ Intent

Intent
↔ Brand Constraint

Intent
↔ Product Truth

Intent
↔ Channel Requirement
```

The engine must classify the conflict before resolving it.

Possible states:

```text
COMPATIBLE
TENSION
CONFLICT
HARD_CONFLICT
```

---

# 17. Conflict Resolution

The default strategy is:

```text
PRODUCT TRUTH
        ↓
HARD BRAND CONSTRAINT
        ↓
LOCKED EXPLICIT INTENT
        ↓
EXPLICIT INTENT
        ↓
DERIVED INTENT
        ↓
INFERRED INTENT
```

A conflict with product truth cannot be solved by creative reinterpretation.

Example:

```text
Intent:
"Show the garment as handwoven."

Product knowledge:
"Machine-produced."

Result:
HARD CONFLICT
```

The system must reject or escalate the intent rather than invent visual evidence.

---

# 18. Intent Redundancy

Multiple intents may communicate substantially the same semantic objective.

Example:

```text
"Communicate premium quality."

"Make the audience perceive superior quality."

"Establish the product as high-end."
```

These may be semantically overlapping.

The engine should detect redundancy and propose consolidation.

However, consolidation must preserve:

- provenance,
- authority,
- source,
- and any distinct audience or channel meaning.

---

# 19. Intent Decomposition

A broad intent may require decomposition.

Example:

```text
"Position the product as contemporary luxury."
```

may decompose into:

```text
INTENT A
Communicate premium quality.

INTENT B
Communicate contemporary relevance.

INTENT C
Communicate distinctive cultural identity.
```

Decomposition is valid only when each child intent can be justified and independently connected to evidence.

The parent-child relationship must be explicit:

```text
PARENT_INTENT
    ↓ DECOMPOSES_INTO
CHILD_INTENT
```

---

# 20. Intent Composition

Conversely, several low-level intents may contribute to a larger strategic intent.

```text
Craftsmanship
Material authenticity
Construction detail
        ↓
SUPPORT
        ↓
Perceived premium quality
```

This should not be confused with evidence requirements.

The relationship is between communication meanings, not visual proofs.

---

# 21. Intent and Evidence Boundary

A Communication Intent must be capable of producing at least one meaningful Evidence Requirement.

If an intent cannot produce any plausible evidence requirement, the engine should flag it:

```text
INTENT
    ↓
NO EVIDENCE PATH
    ↓
CHALLENGE
```

Possible outcomes:

```text
REFINE INTENT
RECLASSIFY AS CREATIVE OPPORTUNITY
ESCALATE
REJECT
```

This is a key validation mechanism.

---

# 22. Intent and Asset Boundary

The Intent Engine must not directly decide the final asset set.

The correct chain is:

```text
INTENT
    ↓
EVIDENCE
    ↓
ASSET REQUIREMENT
    ↓
ASSET STRATEGY
```

This preserves the separation established in Q1–Q3.

---

# 23. Intent Locking

An intent can become:

```text
LOCKED
```

only through the appropriate authority mechanism.

Once locked:

```text
DOWNSTREAM AGENTS
→ may challenge
→ may request revision
→ may provide contradictory evidence

DOWNSTREAM AGENTS
→ may NOT silently mutate
```

Reopening a locked intent requires an explicit revision event.

---

# 24. Challenge Protocol

An agent that believes an intent is invalid should create:

```text
INTENT CHALLENGE
```

containing:

```text
target_intent
challenger
reason
evidence
severity
expected_impact
recommended_action
```

Possible outcomes:

```text
UPHELD
REVISED
REJECTED
ESCALATED
```

The challenge does not itself alter the intent.

---

# 25. Self-Critique Requirements

The Self-Critique Agent should inspect each accepted intent for:

- unsupported assumptions,
- ambiguous wording,
- insufficient evidence,
- redundant intents,
- contradictions,
- hidden execution prescriptions,
- excessive inference,
- missing audience interpretation,
- and unjustified strategic leaps.

It should produce a critique record rather than directly rewriting the intent.

---

# 26. Adversarial Verification Requirements

The Adversarial Verification Agent should attempt to break the Intent Derivation Contract by:

1. Injecting unsupported strategic claims.
2. Turning weak knowledge into high-confidence intent.
3. Mutating explicit intent through derived evidence.
4. Creating contradictory intents.
5. Creating intents with no evidence path.
6. Hiding execution instructions inside intent statements.
7. Exploiting ambiguous authority.
8. Creating redundant intent explosions.
9. Bypassing locked intent state.
10. Creating strategic drift through channel-specific inference.

Expected result:

```text
ATTACK
→ DETECT
→ BLOCK / CHALLENGE
→ RECORD EVIDENCE
```

---

# 27. Validation Invariants

The following invariants should become deterministic or testable assertions.

### Invariant 1

Every accepted intent has a valid campaign context.

### Invariant 2

Every derived intent has traceable provenance.

### Invariant 3

Every inferred intent exposes uncertainty.

### Invariant 4

Authority and confidence are stored separately.

### Invariant 5

No downstream agent may silently mutate a locked intent.

### Invariant 6

A consequential intent must have an evidence path.

### Invariant 7

Product truth cannot be overridden by an inferred or creative intent.

### Invariant 8

Intent derivation cannot silently introduce execution-level specifications.

### Invariant 9

Intent challenges do not mutate the target automatically.

### Invariant 10

Every accepted intent is versioned.

---

# 28. Falsifiable Architectural Hypotheses

## Hypothesis A — Explicit / Derived / Inferred separation reduces strategic hallucination

**Claim:** Separating authority classes reduces unsupported strategic decisions.

**Experiment:**

Compare:

```text
System A:
all intents treated equally

System B:
explicit / derived / inferred separated
```

Measure:

- unsupported intent rate,
- strategic drift,
- false certainty,
- human correction rate.

---

## Hypothesis B — Evidence-path validation improves intent quality

**Claim:** Requiring an evidence path prevents vague or non-actionable intents.

**Test:**

Introduce intents with no plausible evidence path.

Expected:

```text
CHALLENGE / REJECT / ESCALATE
```

---

## Hypothesis C — Authority and confidence separation improves decision calibration

**Claim:** Treating authority separately from confidence prevents highly confident inference from masquerading as authoritative strategy.

**Test:**

Provide high-confidence but unauthorized inferred information.

Expected:

```text
HIGH CONFIDENCE
+
LOW AUTHORITY
=
NOT AUTHORITATIVE
```

---

## Hypothesis D — Challenge-before-mutation improves strategic stability

**Claim:** Requiring downstream agents to challenge rather than directly mutate upstream intent reduces uncontrolled strategic drift.

**Test:**

Run adversarial downstream mutation attempts.

Expected:

```text
MUTATION BLOCKED
CHALLENGE CREATED
```

---

# 29. Intent Derivation Output

The Intent Engine should ultimately produce:

```text
INTENT SET
│
├── Explicit Intents
├── Derived Intents
├── Inferred Intents
│
├── Conflicts
├── Redundancies
├── Knowledge Gaps
└── Challenges
```

Each accepted intent must be traceable and evidence-ready.

---

# 30. Core Contract

> **The Communication Intent Engine shall derive campaign-specific audience-facing communication goals from authoritative campaign context while preserving authority, provenance, uncertainty, and strategic boundaries. It shall distinguish explicit, derived, inferred, and exploratory intent; reject or escalate unsupported consequential inferences; prevent downstream silent mutation of locked strategic meaning; and produce intents that can be validated through explicit evidence paths.**

---

# 31. Deferred Decisions

II-004 does not yet freeze:

- exact intent taxonomy,
- numerical confidence thresholds,
- specific LLM models,
- prompt templates,
- database representation,
- final evidence scoring,
- UI presentation,
- implementation language.

These belong to later contracts and engineering.

---

# 32. Exit Criteria

II-004 is semantically complete when:

- [x] Intent definition established
- [x] Authority classes established
- [x] Authority precedence established
- [x] Explicit / derived / inferred distinction established
- [x] Confidence separated from authority
- [x] Intent derivation pipeline established
- [x] Conflict model established
- [x] Redundancy handling established
- [x] Intent decomposition/composition established
- [x] Evidence-path requirement established
- [x] Locking and challenge protocol established
- [x] Self-critique requirements established
- [x] Adversarial verification requirements established
- [x] Validation invariants established
- [x] Falsifiable hypotheses established

**Current assessment:** Ready for cross-document review, but **not yet ratified**.

---

## Next Specification

**II-005 — Evidence Requirement Contract**

This specification will define how accepted Communication Intents are translated into measurable evidence requirements without prematurely collapsing evidence into a specific shot, prompt, or asset.
