# INTELLIGENCE → ENGINEERING PATCH
# ENG-RTC-005-PATCH-001 — Correction Engine Hardening

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** REQUIRED CORRECTIVE PATCH  
**Priority:** HIGH  
**Parent:** ENG-RTC-005 — Correction Plan & Targeted Regeneration Protocol  
**Purpose:** Harden the Correction Engine before ENG-RTC-006

---

# 1. Context

The Intelligence Architect has reviewed:

`ENG-RTC-005-IMPLEMENTATION`

The implementation is accepted in principle, but **ENG-RTC-005 is not yet frozen**.

Three corrective changes are required before we move to:

`ENG-RTC-006 — Multi-Product Intelligence & Conflict Resolution`

This is a focused hardening patch.

Do **not** redesign the Correction Engine.

Do **not** introduce new intelligence domains.

Implement only the corrections defined below, add regression tests, and return the required engineering report.

---

# 2. PATCH-A — Segment Normalizer

## Problem

The current Targeted Prompt Editor can produce mechanically malformed prompt segments.

Observed examples include:

```text
"Banarasi Silk with Zari detailing. with visible weave relief"
```

and:

```text
"natural clean skin texture., gravity-responsive drape tension"
```

These are technically valid strings but demonstrate poor segment composition.

This must be corrected before the output reaches the Generator.

---

# 3. New Pipeline Stage

Add a deterministic:

`Segment Normalizer`

between the Targeted Prompt Editor and Prompt Linter.

Required flow:

```text
CorrectionPlan
      ↓
Targeted Prompt Editor
      ↓
Segment Normalizer
      ↓
Prompt Linter
      ↓
Generator
```

---

# 4. Segment Normalizer Responsibilities

The normalizer may correct only structural/language composition defects introduced during targeted editing.

It may correct:

- duplicate punctuation
- malformed sentence joining
- duplicate spaces
- accidental repeated conjunctions
- `.` followed incorrectly by `with`
- duplicate commas
- empty fragments
- repeated descriptors
- obvious duplicate semantic clauses
- malformed list joining

Examples:

```text
WRONG:
"silk texture. with visible weave relief"

NORMALIZED:
"silk texture with visible weave relief"
```

```text
WRONG:
"natural clean skin texture., gravity-responsive drape tension"

NORMALIZED:
"natural clean skin texture, gravity-responsive drape tension"
```

---

# 5. Critical Boundary

The Segment Normalizer is NOT an intelligence component.

It must NOT:

- invent creative direction
- add new photographic concepts
- introduce new material properties
- change lighting intent
- change camera intent
- change brand positioning
- add unsupported domain claims
- rewrite an entire prompt
- infer missing creative requirements

Its only responsibility is:

> **Make the already-approved targeted modification structurally coherent without changing its semantic intent.**

---

# 6. Normalizer Invariants

For every normalization operation:

```text
semantic intent BEFORE
==
semantic intent AFTER
```

within the scope of structural correction.

The normalizer must not transform:

```text
"soft diffused daylight"
```

into:

```text
"dramatic directional daylight"
```

even if the latter sounds better.

That would be an intelligence decision and is prohibited.

---

# 7. Normalization Scope

The normalizer should operate at the segment level.

For example:

```text
SUBJECT
MATERIAL
LIGHTING
CAMERA
ENVIRONMENT
QUALITY
FORBIDDEN
```

If only:

```text
MATERIAL
QUALITY
```

were modified, only those segments may be normalized.

Protected segments must remain byte-for-byte or semantically unchanged according to the existing architecture.

---

# 8. PATCH-A Tests

Add at minimum:

### TEST-NORM-001
Duplicate punctuation.

Input:

```text
"natural texture., visible weave"
```

Expected:

```text
"natural texture, visible weave"
```

### TEST-NORM-002
Incorrect sentence joining.

Input:

```text
"silk texture. with visible weave relief"
```

Expected:

```text
"silk texture with visible weave relief"
```

### TEST-NORM-003
Duplicate descriptors.

Input:

```text
"visible weave relief, visible weave relief"
```

Expected:

```text
"visible weave relief"
```

### TEST-NORM-004
Semantic preservation.

Input:

```text
"soft diffused daylight. with gentle shadow transitions"
```

Expected:

```text
"soft diffused daylight with gentle shadow transitions"
```

The meaning must remain unchanged.

### TEST-NORM-005
No creative invention.

Provide a malformed segment and verify that the normalizer only repairs composition.

### TEST-NORM-006
Protected segment integrity.

Modify MATERIAL and verify that SUBJECT, LIGHTING, CAMERA, ENVIRONMENT, and other protected segments are unchanged.

---

# 9. PATCH-B — Rename Locality Metric

## Problem

The current implementation defines correction locality approximately as:

```text
changed words / total words
```

This is useful but represents lexical change, not complete semantic change.

Do not remove the existing calculation.

Rename it explicitly to:

`lexical_correction_locality`

---

# 10. Locality Contract

The current metric should be documented as:

> **Lexical Correction Locality:** the proportion of prompt tokens/words altered by a targeted correction.

It is an operational approximation.

It must NOT be described as a complete measure of semantic locality.

---

# 11. Future Semantic Locality

Document, but do not implement yet:

`semantic_correction_locality`

This future metric may evaluate whether the semantic scope of a correction remained localized even when the number of changed words is large.

For this patch:

```text
IMPLEMENT:
lexical_correction_locality

DOCUMENT:
semantic_correction_locality as future enhancement
```

Do not expand scope beyond this.

---

# 12. PATCH-B Tests

### TEST-LOCALITY-001

Verify the existing locality calculation still works after the rename.

### TEST-LOCALITY-002

Verify the result is explicitly labeled:

```text
lexical_correction_locality
```

### TEST-LOCALITY-003

Verify documentation does not claim that lexical locality is equivalent to semantic locality.

---

# 13. PATCH-C — Escalation Semantics

## Problem

The current implementation uses a provisional pattern:

```text
Attempt 1 → Prompt
Attempt 2 → Decision
Attempt 3 → Intelligence
```

This is acceptable as an initial implementation but is too rigid to become the permanent intelligence architecture.

A failed second attempt does not automatically prove that the Decision Engine is wrong.

Likewise, repeated failure can justify escalation earlier than a fixed attempt count when evidence is strong.

---

# 14. Provisional Escalation Rule

For the current implementation:

```text
attempt-based escalation may remain
```

but it must be explicitly marked:

```text
PROVISIONAL
```

It must not be presented as the final escalation intelligence.

---

# 15. Future Escalation Model

Document that the final escalation decision should eventually consider:

```text
failure severity
+
evaluation confidence
+
cause confidence
+
improvement delta
+
failure recurrence
+
correction history
+
protected-dimension regression
```

Conceptually:

```text
Evidence
   ↓
Escalation Assessment
   ↓
Prompt Problem?
Decision Problem?
Intelligence Problem?
Generator Limitation?
Human Review?
```

Do NOT implement this complete adaptive model in this patch.

---

# 16. Important Escalation Principle

Attempt count is a signal.

It is NOT the cause of escalation.

For example:

```text
Attempt 1
+
very high-confidence hard failure
+
same failure already known
+
targeted correction clearly ineffective
```

may justify early escalation.

Conversely:

```text
Attempt 2
+
low evaluator confidence
+
ambiguous failure
```

may justify:

```text
HUMAN_REVIEW
```

rather than automatic Decision Engine escalation.

This logic is for the future architecture, but the current implementation must not prevent it.

---

# 17. PATCH-C Tests

### TEST-ESC-001

Verify provisional attempt-based escalation still functions.

### TEST-ESC-002

Verify escalation metadata identifies the mechanism as:

```text
provisional_attempt_based
```

### TEST-ESC-003

Verify evaluation confidence is preserved in the escalation record.

### TEST-ESC-004

Verify failure severity is preserved.

### TEST-ESC-005

Verify improvement delta is preserved.

The last three fields are required so the future adaptive escalation engine can be introduced without changing the underlying evaluation/correction data model.

---

# 18. No Scope Expansion

This patch must NOT introduce:

- Multi-product reasoning
- New material ontology
- New brand intelligence
- New evaluator dimensions
- New generator models
- Semantic locality implementation
- Adaptive escalation engine
- Autonomous knowledge modification

Those belong to future architectural stages.

---

# 19. Required Regression Suite

After implementing the patch, rerun:

```text
All ENG-RTC-004 evaluator tests
+
All ENG-RTC-005 correction tests
+
All new normalization tests
+
All locality tests
+
All escalation metadata tests
```

No regression is acceptable.

---

# 20. Freeze Criteria

ENG-RTC-005 may be frozen only when:

```text
Segment Normalizer implemented
        AND
Normalization tests pass
        AND
No creative invention by normalizer
        AND
lexical_correction_locality clearly named
        AND
Semantic locality limitation documented
        AND
Provisional escalation explicitly marked
        AND
Severity/confidence/delta preserved
        AND
All regression tests pass
```

---

# 21. Required Engineering Response

Return:

`ENG-RTC-005-PATCH-001-IMPLEMENTATION`

Include:

1. Files changed
2. Segment Normalizer implementation
3. Normalization rules
4. Before/after examples
5. Locality metric rename
6. Locality documentation
7. Escalation metadata changes
8. Provisional escalation implementation
9. New tests
10. Full regression results
11. Confirmation that no new intelligence scope was introduced
12. Remaining known limitations

Do not propose ENG-RTC-006 implementation in this response.

The only objective of this communication is to harden and freeze ENG-RTC-005.

---

# 22. Final Instruction

The goal of this patch is not to make the Correction Engine "smarter."

The goal is to make it:

```text
more deterministic
more auditable
more structurally clean
more semantically bounded
more future-compatible
```

Once this patch passes, the Correction Engine can be frozen and we will move to:

`ENG-RTC-006 — Multi-Product Intelligence & Conflict Resolution`.
