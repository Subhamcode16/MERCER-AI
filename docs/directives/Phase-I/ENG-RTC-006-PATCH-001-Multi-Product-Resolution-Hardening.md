# INTELLIGENCE → ENGINEERING CORRECTIVE PATCH
# ENG-RTC-006-PATCH-001 — Multi-Product Resolution Hardening

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Intelligence Architect  
**To:** Engineering Agent  
**Status:** REQUIRED CORRECTIVE PATCH  
**Priority:** HIGH  
**Parent:** ENG-RTC-006 — Multi-Product Intelligence & Conflict Resolution  
**Purpose:** Close architectural gaps before ENG-RTC-006 freeze

---

# 1. Review Decision

The Intelligence Architect has reviewed:

`ENG-RTC-006-IMPLEMENTATION`

The implementation establishes the correct backbone for multi-product intelligence:

- ProductRequirement
- ProductRole
- shot objectives
- conflict detection
- conflict resolution
- provenance
- deferred requirements
- ResolvedShotSolution
- Prompt Compiler boundary
- Evaluator boundary
- escalation
- TEST-MP-001 through TEST-MP-012

The implementation is therefore **accepted in principle but NOT YET FROZEN**.

This is a focused corrective patch.

Do not redesign the resolver.

Do not introduce new product-domain intelligence.

Do not build a physics simulator.

Do not begin ENG-RTC-007.

---

# 2. PATCH-A — Add Explicit COMPROMISE Strategy

## Problem

The ENG-RTC-006 specification required six resolution strategies:

```text
ACCOMMODATE
COMPROMISE
PRIORITIZE
ISOLATE
DEFER
ESCALATE
```

The current implementation contains:

```text
ACCOMMODATE
PRIORITIZE
ISOLATE
DEFER
ESCALATE
```

`COMPROMISE` is missing.

This distinction is architecturally important.

---

# 3. COMPROMISE Definition

Add:

```text
COMPROMISE
```

when multiple requirements can each be partially satisfied through a shared adjustment.

Example:

```text
Saree:
high texture visibility

Jewelry:
high highlight definition
```

A compromise could produce:

```text
Saree:
moderate-high texture visibility

Jewelry:
moderate-high highlight definition
```

This differs from:

```text
PRIORITIZE
```

where one requirement intentionally receives greater treatment and another is reduced.

It also differs from:

```text
ISOLATE
```

where spatial/optical separation allows both requirements to remain substantially intact.

---

# 4. COMPROMISE Contract

The resolution record must identify:

```text
strategy = COMPROMISE
```

and preserve:

```text
requirements involved
original requested values
resolved values
reason
impact
```

No requirement may disappear silently.

---

# 5. PATCH-A TEST

Add:

```text
TEST-MP-013 — COMPROMISE
```

Scenario:

```text
Product A:
high texture visibility

Product B:
moderate specular response
```

Expected:

```text
strategy = COMPROMISE
```

and both requirements must remain represented in the resolved solution.

Verify that the resolver does not incorrectly classify this as:

```text
PRIORITIZE
```

or:

```text
DEFER
```

---

# 6. PATCH-B — Make Shot Objective Operational

## Problem

The current resolver supports:

```text
CRAFTSMANSHIP
LIFESTYLE
CONVERSION
EDITORIAL
```

but the current priority equation is effectively:

```text
Priority Score
=
Role Weight
+
Importance Weight
```

Shot objective currently exists, but it must become an actual resolution input.

---

# 7. Required Principle

The same products and requirements may legitimately produce different resolutions under different shot objectives.

Example:

```text
CRAFTSMANSHIP
→ maximize textile weave + material detail

LIFESTYLE
→ preserve believable interaction + environmental coherence

CONVERSION
→ maximize product readability and commercial clarity

EDITORIAL
→ preserve artistic composition + visual hierarchy
```

Therefore:

```text
same requirements
+
different objective
=
potentially different resolution
```

---

# 8. Implementation Boundary

Introduce shot-objective influence into resolution scoring or strategy selection.

The exact mathematical implementation is engineering territory.

Do NOT create an unnecessarily complex optimization system.

A deterministic objective weighting layer is sufficient for this patch.

The architecture must make it possible to answer:

> "Why did this shot resolve the conflict differently under a different objective?"

---

# 9. Objective-Dependent Provenance

The resolution record should preserve the objective used during resolution.

For example:

```json
{
  "strategy": "PRIORITIZE",
  "objective": "CRAFTSMANSHIP",
  "reason": "Primary textile detail is the shot objective."
}
```

The exact schema may differ.

The semantic information must remain.

---

# 10. PATCH-B TEST

Add:

```text
TEST-MP-015 — Objective-Dependent Resolution
```

Construct the same multi-product requirement set twice:

```text
Shot A:
objective = CRAFTSMANSHIP

Shot B:
objective = LIFESTYLE
```

Verify that the resolver can produce a meaningfully different resolution when the objective warrants it.

The test must demonstrate that the objective is not merely stored as metadata.

---

# 11. PATCH-C — Distinguish Conflict Classes

## Problem

Current conflict detection primarily groups requirements by:

```text
category + key
```

This is a valid first mechanism but not a complete conflict model.

Two requirements can conflict even when they do not share the exact key.

Example:

```text
Saree:
LIGHTING.texture_reveal
→ soft directional light

Jewelry:
MATERIAL.highlight_definition
→ strong specular response
```

These are different keys but can create a lighting/material interaction conflict.

---

# 12. Required Conflict Classification

Preserve the existing direct/key conflict concept and add an explicit distinction:

```text
KEY_CONFLICT
```

versus:

```text
CROSS_DIMENSION_CONFLICT
```

The exact enum names may differ, but the semantic distinction must exist.

---

# 13. Conflict Definitions

### KEY_CONFLICT

Two requirements compete for the same parameter.

Example:

```text
LIGHTING:KeyLight
```

vs:

```text
LIGHTING:KeyLight
```

### CROSS_DIMENSION_CONFLICT

Requirements occupy different semantic dimensions but create a known interaction conflict.

Example:

```text
LIGHTING.texture_reveal
+
MATERIAL.highlight_definition
```

The current patch does NOT require a generalized physics model.

The goal is only to prevent the architecture from assuming:

```text
same key = only possible conflict
```

---

# 14. Spatial / Composition Conflicts

The implementation report correctly identifies future complexity around spatial composition, framing, visibility, and occlusion.

Do not solve geometric boundary-box reasoning in this patch.

However, preserve a future-compatible category:

```text
SPATIAL_COMPOSITION
```

for conflicts involving:

```text
framing
visibility
occlusion
pose
camera distance
product placement
```

This should be classification/provenance only.

No geometry engine is required.

---

# 15. PATCH-C TEST

Add:

```text
TEST-MP-014 — Cross-Dimension Conflict
```

Construct requirements with different keys but an explicit known interaction.

Expected:

```text
conflict detected
conflict_type = CROSS_DIMENSION_CONFLICT
```

Do not require full physical simulation.

---

# 16. PATCH-D — Strengthen Knowledge-Gap Escalation

## Problem

The current implementation correctly detects unknown requirements and escalates.

However, a generic:

```text
ValueError
```

is too weak as the long-term intelligence contract.

Do not redesign the escalation architecture.

Instead, ensure the knowledge-gap escalation preserves structured information.

---

# 17. Required Knowledge-Gap Fields

When knowledge is insufficient, preserve at minimum:

```text
product_id
requirement_id
domain
category
property_key
missing/unknown value
reason
```

The exact object name may remain engineering-specific.

The semantic information is mandatory.

---

# 18. Knowledge-Gap Principle

The resolver must communicate:

> "I cannot safely resolve this because the required intelligence is missing."

It must NOT communicate:

> "I resolved this arbitrarily."

No fallback creative guess is permitted when required knowledge is genuinely unavailable.

---

# 19. Regression Requirement

Existing escalation behavior must remain functional.

The new structured metadata must not break existing callers.

If the current implementation uses compatibility-preserving behavior, retain it.

---

# 20. Required New Test Suite

After the patch, the following tests must exist:

```text
TEST-MP-013 — COMPROMISE
TEST-MP-014 — Cross-Dimension Conflict
TEST-MP-015 — Objective-Dependent Resolution
```

All three must pass.

---

# 21. Existing Tests Must Still Pass

Rerun the complete existing suite:

```text
TEST-MP-001
TEST-MP-002
TEST-MP-003
TEST-MP-004
TEST-MP-005
TEST-MP-006
TEST-MP-007
TEST-MP-008
TEST-MP-009
TEST-MP-010
TEST-MP-011
TEST-MP-012
```

No regression is acceptable.

---

# 22. Required Architectural Invariants

After the patch, these must remain true:

```text
Product requirements
        ↓
Conflict detection
        ↓
Conflict resolution
        ↓
ResolvedShotSolution
        ↓
Prompt Compiler
```

The Prompt Compiler must still NOT resolve product conflicts.

The Evaluator must still evaluate against:

```text
ResolvedShotSolution
+
deferred requirements
```

The system must still preserve:

```text
raw requirement
→ conflict
→ strategy
→ reason
→ final resolution
```

---

# 23. No Scope Expansion

Do NOT implement:

- new material ontology
- new saree knowledge
- new jewelry knowledge
- new footwear knowledge
- new lighting knowledge
- generalized physics simulation
- geometric boundary-box engine
- adaptive evaluator redesign
- semantic locality
- autonomous knowledge-base modification
- ENG-RTC-007

This patch exists only to close the identified ENG-RTC-006 architectural gaps.

---

# 24. Freeze Criteria

ENG-RTC-006 may be frozen only when:

```text
COMPROMISE implemented
        AND
Shot Objective affects resolution
        AND
KEY vs CROSS-DIMENSION conflicts distinguished
        AND
SPATIAL_COMPOSITION remains future-compatible
        AND
Knowledge-gap escalation is structured
        AND
MP-013 passes
        AND
MP-014 passes
        AND
MP-015 passes
        AND
MP-001 through MP-012 still pass
```

---

# 25. Required Engineering Response

Return:

`ENG-RTC-006-PATCH-001-IMPLEMENTATION`

Include:

1. Files changed
2. COMPROMISE implementation
3. Objective influence implementation
4. Conflict-classification changes
5. Knowledge-gap escalation changes
6. New tests MP-013 through MP-015
7. Full regression results MP-001 through MP-015
8. Example COMPROMISE resolution
9. Example CROSS-DIMENSION conflict
10. Example objective-dependent resolution
11. Known limitations
12. Confirmation that no new domain intelligence was introduced
13. Confirmation that Prompt Compiler remains downstream of resolution
14. Confirmation that Evaluator remains downstream of resolved-shot semantics

Do not proceed to the next architectural stage until this patch has been reviewed and frozen.

---

# 26. Final Instruction

The purpose of this patch is **not** to make the Multi-Product Resolver more complicated.

The purpose is to make its decisions:

```text
more semantically correct
more objective-aware
more explicitly classified
more explainable
more provenance-safe
```

Close these gaps cleanly.

Then stop.

We will review the resulting implementation before authorizing the ENG-RTC-006 freeze.
