# INTELLIGENCE → ENGINEERING INSTRUCTION
# ENG-RTC-005 — Correction Plan & Targeted Regeneration Protocol

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** APPROVED FOR IMPLEMENTATION  
**Priority:** CRITICAL  
**Depends On:** ENG-RTC-002, ENG-RTC-003, ENG-RTC-004  
**Architectural Position:** Evaluation → Correction → Targeted Regeneration

---

# 1. Purpose

The Evaluation Engine can now determine whether a generated artifact satisfies the intended creative solution.

The next problem is fundamentally different:

> **When an artifact fails, determine exactly what must change while preserving everything that already works.**

The system must therefore NOT use the simplistic loop:

```text
GENERATE
    ↓
FAIL
    ↓
CHANGE EVERYTHING
    ↓
REGENERATE
```

The required loop is:

```text
GENERATE
    ↓
EVALUATE
    ↓
IDENTIFY FAILURE
    ↓
ANALYZE CAUSE
    ↓
CREATE CORRECTION PLAN
    ↓
EDIT ONLY AFFECTED PROMPT SEGMENTS
    ↓
LINT
    ↓
REGENERATE
    ↓
EVALUATE AGAIN
```

This is the architectural transition from **generation** to **controlled visual refinement**.

---

# 2. Core Principle

The system must preserve successful decisions.

Therefore:

> **A correction is a constrained modification, not a new creative generation decision.**

If an artifact has:

```text
Product Fidelity = 0.95
Composition Fidelity = 0.94
Lighting Fidelity = 0.91
Material Fidelity = 0.61
```

the correction process must NOT rewrite:

- product identity
- composition
- lighting
- camera
- environment

unless evidence shows those dimensions contributed to the material failure.

The correction should target:

```text
MATERIAL
+
QUALITY
```

and preserve everything else.

---

# 3. New Architectural Object

Introduce:

# `CorrectionPlan`

The CorrectionPlan sits between evaluation and prompt editing.

Required pipeline:

```text
EVALUATOR
    ↓
FAILURE ANALYZER
    ↓
CORRECTION PLAN
    ↓
TARGETED PROMPT EDITOR
    ↓
PROMPT LINTER
    ↓
GENERATOR
    ↓
EVALUATOR
```

The CorrectionPlan is the only object authorized to define what the regeneration step is permitted to change.

---

# 4. CorrectionPlan Responsibilities

The CorrectionPlan must answer six questions:

```text
1. What failed?
2. How severe is the failure?
3. How confident are we?
4. What caused or contributed to the failure?
5. Which prompt segments may be changed?
6. What must remain unchanged?
```

Optional seventh question:

```text
7. What measurable improvement is required?
```

---

# 5. CorrectionPlan Schema

Implement a machine-readable representation conceptually equivalent to:

```json
{
  "correction_id": "CORR-001",
  "evaluation_id": "EVAL-001",
  "shot_id": "craftsmanship_01",

  "failure": {
    "failure_id": "MAT-STRUCT-001",
    "dimension": "material_fidelity",
    "severity": "HARD",
    "confidence": 0.94,
    "observation": "Fabric surface appears unnaturally smooth and lacks visible textile microstructure."
  },

  "cause": {
    "category": "material_representation",
    "confidence": 0.88,
    "hypothesis": "Insufficient textile microstructure representation in the material and quality instructions."
  },

  "affected_segments": [
    "MATERIAL",
    "QUALITY"
  ],

  "preserve_segments": [
    "SUBJECT",
    "LIGHTING",
    "CAMERA",
    "ENVIRONMENT"
  ],

  "corrections": [
    {
      "segment": "MATERIAL",
      "operation": "augment",
      "target": "textile_microstructure",
      "instruction": "Increase explicit representation of weave relief and natural surface irregularity."
    },
    {
      "segment": "QUALITY",
      "operation": "augment",
      "target": "fabric_authenticity",
      "instruction": "Increase visible microtexture while preserving natural drape."
    }
  ],

  "success_criteria": [
    "material_fidelity >= 0.80",
    "no_new_hard_failures",
    "preserved_composition"
  ],

  "confidence": 0.89
}
```

The exact implementation schema may differ.

The semantics must not.

---

# 6. Failure → Correction Mapping

Do not allow the Targeted Prompt Editor to invent corrections freely.

The system should maintain a structured mapping:

```text
FAILURE
    ↓
CAUSE CATEGORY
    ↓
CORRECTION STRATEGY
    ↓
AFFECTED SEGMENTS
```

Examples:

### Material too smooth

```text
Failure:
synthetic / smooth textile surface

Cause:
insufficient microstructure representation

Correction:
augment MATERIAL + QUALITY
```

### Lighting too flat

```text
Failure:
insufficient dimensionality

Cause:
key/fill relationship does not express intended contrast

Correction:
modify LIGHTING
```

### Wrong crop

```text
Failure:
product detail insufficient

Cause:
framing mismatch

Correction:
modify SUBJECT
possibly CAMERA
```

### Skin too plastic

```text
Failure:
lack of natural skin texture

Cause:
insufficient human-authenticity constraints

Correction:
modify QUALITY
possibly SUBJECT
```

### Environment wrong

```text
Failure:
brand/environment mismatch

Cause:
environment does not satisfy resolved creative solution

Correction:
modify ENVIRONMENT
```

---

# 7. Preserve What Works

The CorrectionPlan must explicitly define immutable segments.

Example:

```json
{
  "affected_segments": ["MATERIAL", "QUALITY"],
  "preserve_segments": [
    "SUBJECT",
    "LIGHTING",
    "CAMERA",
    "ENVIRONMENT"
  ]
}
```

The editor must reject any modification outside:

```text
affected_segments
```

unless the CorrectionPlan is explicitly revised.

---

# 8. Correction Operations

Initially support only a small deterministic set:

```text
ADD
AUGMENT
REMOVE
REPLACE
DE-EMPHASIZE
STRENGTHEN
WEAKEN
```

Do not initially support unrestricted prompt rewriting.

---

# 9. Operation Semantics

## ADD

Introduce a missing descriptor.

Example:

```text
ADD:
visible weave relief
```

## AUGMENT

Increase specificity of an existing concept.

Example:

```text
existing:
natural fabric texture

augment:
visible weave relief, subtle thread variation, physically plausible surface irregularity
```

## REMOVE

Remove a conflicting or harmful instruction.

Example:

```text
remove:
excessive glossy finish
```

## REPLACE

Replace a demonstrably incorrect descriptor.

Example:

```text
soft studio lighting
→
large directional window light
```

Only allowed when the CorrectionPlan identifies the existing instruction as causally related to the failure.

## DE-EMPHASIZE

Reduce prominence without deleting the concept.

## STRENGTHEN

Increase explicitness of an existing requirement.

## WEAKEN

Reduce an overexpressed property.

---

# 10. No Unbounded Prompt Rewriting

The editor must NOT perform:

```text
"Rewrite the prompt to make it better."
```

It must instead receive:

```text
CorrectionPlan
+
Existing Prompt
```

and produce:

```text
Targeted Modified Prompt
```

with a machine-readable diff.

---

# 11. Prompt Diff Is Mandatory

Every correction must produce a diff.

Conceptually:

```json
{
  "modified_segments": ["MATERIAL", "QUALITY"],

  "changes": [
    {
      "segment": "MATERIAL",
      "operation": "AUGMENT",
      "before": "silk texture",
      "after": "silk texture with visible fine weave relief and subtle thread variation"
    }
  ],

  "unchanged_segments": [
    "SUBJECT",
    "LIGHTING",
    "CAMERA",
    "ENVIRONMENT",
    "FORBIDDEN"
  ]
}
```

The system must make corrections auditable.

---

# 12. Correction Locality

Introduce a concept called:

# `Correction Locality`

It measures how much of the original prompt was altered.

Conceptually:

```text
Correction Locality =
changed prompt content
/
total prompt content
```

Lower is generally better.

The system should prefer:

```text
small targeted correction
```

over:

```text
large prompt rewrite
```

unless the evaluation indicates that the creative solution itself is invalid.

---

# 13. Exception — Creative Solution Failure

There is an important exception.

Sometimes the generated artifact fails because the **upstream Creative Solution was wrong**, not because the prompt was poorly compiled.

Example:

```text
Creative Solution:
hard dramatic side light

Artifact:
extreme shadows destroy textile visibility
```

If evaluation determines:

```text
lighting intent conflicts with product visibility
```

then the system must NOT force the Prompt Editor to blindly repair the prompt.

Instead:

```text
EVALUATOR
    ↓
UPSTREAM SOLUTION CONFLICT
    ↓
ESCALATE TO DECISION ENGINE
```

This distinction is critical.

---

# 14. Correction Levels

Introduce three correction levels.

## LEVEL 1 — Prompt-Level Correction

Use when:

```text
creative solution is correct
prompt expression is inadequate
```

Flow:

```text
Evaluator
→ CorrectionPlan
→ Prompt Editor
```

## LEVEL 2 — Decision-Level Correction

Use when:

```text
creative solution itself is inadequate
```

Flow:

```text
Evaluator
→ CorrectionPlan
→ Decision Engine
→ new Creative Solution
→ Prompt Compiler
```

## LEVEL 3 — Intelligence-Level Escalation

Use when:

```text
domain knowledge appears insufficient
```

Example:

```text
Evaluator repeatedly fails to explain
how a specific textile behaves.
```

Flow:

```text
Evaluator
→ Failure Pattern
→ Intelligence Gap
→ Knowledge Layer
→ new/updated claim
→ Decision Engine
```

This creates an important learning loop.

---

# 15. Repeated Failure Detection

The system must detect repeated failures.

Example:

```text
Attempt 1
Material Fidelity = 0.61

Attempt 2
Material Fidelity = 0.63

Attempt 3
Material Fidelity = 0.62
```

If the same failure persists despite targeted corrections:

```text
DO NOT
continue endlessly regenerating.
```

Instead:

```text
Repeated Failure
      ↓
Failure Pattern Detector
      ↓
Determine Layer
      ↓
Prompt Problem?
Decision Problem?
Knowledge Problem?
Generator Limitation?
      ↓
Escalate
```

---

# 16. Regeneration Budget

Introduce a configurable regeneration budget.

Example:

```text
MAX_ATTEMPTS = 3
```

The exact default may be configurable.

After the budget is exhausted:

```text
HUMAN_REVIEW
```

or:

```text
ESCALATE
```

depending on failure type.

Never allow infinite autonomous regeneration.

---

# 17. Preventing Quality Drift

Every regeneration must preserve successful dimensions.

Example:

### Before

```text
Material = 0.61
Lighting = 0.91
Composition = 0.94
```

### After correction

```text
Material = 0.84
Lighting = 0.90
Composition = 0.93
```

This is a successful correction.

But:

```text
Material = 0.84
Lighting = 0.61
Composition = 0.72
```

is not successful.

Therefore the evaluator must compare:

```text
BEFORE
vs
AFTER
```

not only:

```text
AFTER
vs
TARGET
```

---

# 18. Regression Protection

Every correction cycle must maintain a:

```text
previous_evaluation
current_evaluation
```

comparison.

The Correction Engine should reject a correction if it:

- improves one dimension substantially
- while causing unacceptable regression elsewhere

unless the new result is explicitly preferred by campaign priorities.

---

# 19. Improvement Delta

Introduce:

```text
Δdimension = current_score - previous_score
```

Example:

```json
{
  "material_fidelity": {
    "before": 0.61,
    "after": 0.84,
    "delta": 0.23
  },
  "lighting_fidelity": {
    "before": 0.91,
    "after": 0.90,
    "delta": -0.01
  }
}
```

This enables the system to understand whether the correction actually helped.

---

# 20. Correction Success

A correction should be considered successful when:

```text
Targeted Failure Improved
AND
No Critical New Failure
AND
No unacceptable regression in protected dimensions
```

Do not define success merely as:

```text
overall_score increased
```

because a high-weight dimension could mask a critical regression.

---

# 21. Targeted Prompt Editor Contract

The Targeted Prompt Editor receives:

```text
Existing Prompt
+
CorrectionPlan
+
Prompt Provenance
```

It returns:

```text
Modified Prompt
+
Prompt Diff
+
Modified Segments
+
Preserved Segments
+
Editor Confidence
```

The editor must not receive unrestricted authority over the entire campaign intelligence state.

---

# 22. Prompt Linter Integration

The correction flow must remain:

```text
CorrectionPlan
      ↓
Targeted Prompt Editor
      ↓
Prompt Linter
      ↓
Generator
```

The linter must verify:

- required 7 segments still exist
- forbidden keywords remain absent
- no unresolved placeholders
- no duplicate descriptors
- no unsupported claims
- no modification outside allowed segments
- no accidental deletion of protected instructions

---

# 23. Correction Provenance

Every correction must remain traceable.

Example:

```json
{
  "correction_id": "CORR-001",
  "failure_id": "MAT-STRUCT-001",
  "source_claims": [
    "DR-SAREE-001"
  ],
  "affected_segments": [
    "MATERIAL",
    "QUALITY"
  ],
  "editor_operations": [
    "AUGMENT",
    "STRENGTHEN"
  ]
}
```

The system should eventually be able to answer:

> "Why was this part of the prompt changed?"

with a deterministic trace.

---

# 24. Intelligence Gap Detection

Repeated correction failure should eventually produce an intelligence-gap signal.

Example:

```text
Failure:
zari repeatedly appears synthetic.

Attempt 1:
prompt correction failed.

Attempt 2:
prompt correction failed.

Attempt 3:
prompt correction failed.
```

The system should consider:

```text
Possible intelligence gap:
insufficient knowledge describing zari optical behaviour.
```

This must not automatically modify the knowledge base.

Instead produce:

```text
INTELLIGENCE_GAP_REPORT
```

for controlled knowledge-layer review.

---

# 25. Required Machine-Readable Objects

Engineering should introduce at least:

```text
CorrectionPlan
CorrectionOperation
PromptDiff
CorrectionAttempt
CorrectionOutcome
IntelligenceGapReport
```

Exact class/file naming is left to engineering.

---

# 26. Required Test Cases

### TEST-CORR-001
Material failure only.

Expected:

```text
Only MATERIAL + QUALITY modified.
```

### TEST-CORR-002
Lighting failure.

Expected:

```text
Only LIGHTING modified.
```

### TEST-CORR-003
Composition failure.

Expected:

```text
SUBJECT/CAMERA modification permitted.
```

### TEST-CORR-004
Successful dimensions preserved.

Expected:

```text
No unauthorized segment modifications.
```

### TEST-CORR-005
Correction improves target dimension.

Expected:

```text
positive delta
```

### TEST-CORR-006
Correction causes regression.

Expected:

```text
correction rejected or escalated
```

### TEST-CORR-007
Repeated failure.

Expected:

```text
escalation after configured attempt budget
```

### TEST-CORR-008
Prompt-level failure.

Expected:

```text
Targeted Prompt Editor invoked.
```

### TEST-CORR-009
Decision-level failure.

Expected:

```text
Decision Engine escalation.
```

### TEST-CORR-010
Intelligence-level failure.

Expected:

```text
Intelligence Gap Report generated.
```

### TEST-CORR-011
Prompt diff integrity.

Expected:

```text
Every modification auditable.
```

### TEST-CORR-012
Linter violation after correction.

Expected:

```text
Correction rejected before generation.
```

---

# 27. Required Engineering Deliverables

Return:

`ENG-RTC-005-IMPLEMENTATION`

with:

1. Files created/changed
2. CorrectionPlan schema
3. Failure → correction mapping
4. Correction locality implementation
5. Prompt diff implementation
6. Targeted editor interface
7. Regression protection
8. Improvement delta
9. Attempt budget
10. Repeated failure detection
11. Decision-level escalation
12. Intelligence-gap escalation
13. Prompt-linter integration
14. Tests
15. Full test results
16. Example CorrectionPlan
17. Example PromptDiff
18. Example successful correction
19. Example rejected correction
20. Example IntelligenceGapReport
21. Remaining architectural risks

---

# 28. Freeze Conditions

Do not freeze the Correction Engine until:

- targeted modification works
- protected segments cannot be modified accidentally
- prompt diffs are auditable
- regression protection works
- correction locality is measurable
- repeated failures trigger escalation
- prompt/decision/intelligence failure levels are distinguishable
- intelligence gaps are reportable
- all correction tests pass

---

# 29. Final Architectural Rule

The system must now obey:

> **Detect narrowly.**
>
> **Explain causally.**
>
> **Correct locally.**
>
> **Preserve successful decisions.**
>
> **Measure the delta.**
>
> **Reject regressions.**
>
> **Escalate when the problem is above the prompt layer.**

The system should never respond to a failed image with an unrestricted "make it better" operation.

The objective is not endless regeneration.

The objective is:

> **controlled convergence toward the intended creative solution.**
