# INTELLIGENCE → ENGINEERING RESPONSE
# ENG-RTC-005-IMPLEMENTATION — Correction Plan & Targeted Regeneration Protocol

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Engineering Agent  
**To:** Intelligence Architect  
**Status:** VALIDATED & COMPLETED  
**Version:** 1.0  
**Date:** 2026-08-16  
**Reference:** ENG-RTC-005 — Correction Plan & Targeted Regeneration Protocol

---

## 1. Files Created/Changed
*   [`Visual-Intelligence/engine/src/runtime/correction_engine.py`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/engine/src/runtime/correction_engine.py): [NEW] Implemented `CorrectionPlan`, `TargetedPromptEditor`, `RegressionProtection`, `RepeatedFailureDetector`, and `PromptDiff`.
*   [`Visual-Intelligence/engine/src/runtime/test_bench_008_correction_tests.py`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/engine/src/runtime/test_bench_008_correction_tests.py): [NEW] Implemented unit tests for cases `TEST-CORR-001` through `TEST-CORR-012`.

---

## 2. CorrectionPlan Schema
The machine-readable representation of `CorrectionPlan` is implemented as:
```json
{
  "correction_id": "CORR-001",
  "evaluation_id": "EVAL-001",
  "shot_id": "craftsmanship_01",
  "failure": {
    "dimension": "material_fidelity",
    "severity": "HARD",
    "observation": "Fabric surface appears unnaturally smooth and lacks visible textile microstructure."
  },
  "cause": {
    "category": "material_representation"
  },
  "affected_segments": ["MATERIAL", "QUALITY"],
  "preserve_segments": ["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "FORBIDDEN"],
  "corrections": [
    {
      "segment": "MATERIAL",
      "operation": "AUGMENT",
      "target": "Fabric/Material base",
      "instruction": "visible weave relief"
    }
  ],
  "success_criteria": ["material_fidelity >= 0.8"],
  "confidence": 0.9
}
```

---

## 3. Failure → Correction Mapping
Implemented standard mappings in the correction logic:
*   *Material smooth:* Target `MATERIAL`/`QUALITY`, strategy `AUGMENT` / `ADD`.
*   *Lighting flat:* Target `LIGHTING`, strategy `REPLACE` / `STRENGTHEN`.
*   *Wrong crop / framing:* Target `SUBJECT`/`CAMERA`, strategy `REPLACE` / `AUGMENT`.
*   *Skin plastic:* Target `QUALITY`/`FORBIDDEN`, strategy `STRENGTHEN` / `ADD`.
*   *Environment wrong:* Target `ENVIRONMENT`, strategy `REPLACE`.

---

## 4. Correction Locality Implementation
The `TargetedPromptEditor` measures **Correction Locality** by dividing the count of modified prompt words by the total prompt words:
$$\text{Locality} = \frac{\text{changed words}}{\text{total words}}$$
This enforces narrow, localized corrections instead of unbounded rewrites.

---

## 5. Prompt Diff Implementation
Every modification generates a `PromptDiff` dict exposing:
*   `modified_segments`: List of edited sections.
*   `changes`: Array of objects detailing segment name, operator, `before` text, and `after` text.
*   `unchanged_segments`: List of protected sections.

---

## 6. Targeted Editor Interface
The `TargetedPromptEditor.edit(existing_prompt, plan)` interface:
1.  Parses the original prompt into segment dictionary.
2.  Asserts that no operations target a segment in `preserve_segments` or outside `affected_segments`.
3.  Executes `ADD`, `AUGMENT`, `REMOVE`, `REPLACE`, `DE-EMPHASIZE`, `STRENGTHEN`, `WEAKEN` operations.
4.  Rebuilds prompt and runs `PromptLinter.lint(modified_prompt)`. If linter fails (e.g. prohibited slop keywords injected), the editor aborts and returns `success=False`.

---

## 7. Regression Protection & Improvement Delta
`RegressionProtection.assess(prev_eval, curr_eval)` calculates deltas:
$$\Delta\text{dimension} = \text{current score} - \text{previous score}$$
A correction is rejected if any protected dimension drops by $> 0.10$ or falls below the acceptability threshold of $0.60$.

---

## 8. Attempt Budget & Repeated Failure Detection
`RepeatedFailureDetector` manages an attempt budget (default: 3). If failures continue in the same dimension:
*   **Attempt 1:** Escalation Level 1 (Prompt-level targeted editing).
*   **Attempt 2:** Escalation Level 2 (Decision Engine escalation).
*   **Attempt 3:** Escalation Level 3 (Intelligence Gap Report generated).

---

## 9. Full Test Results (Benches 004-008)
All test suites passed successfully:
```text
==================================================
RUNNING TEST BENCH 008: CORRECTION ENGINE TESTS
==================================================
TEST-CORR-001: Material failure only... -> TEST-CORR-001 Passed.
TEST-CORR-002: Lighting failure... -> TEST-CORR-002 Passed.
TEST-CORR-003: Composition failure... -> TEST-CORR-003 Passed.
TEST-CORR-004: Successful dimensions preserved... -> TEST-CORR-004 Passed.
TEST-CORR-005: Correction improves target dimension... -> TEST-CORR-005 Passed.
TEST-CORR-006: Correction causes regression... -> TEST-CORR-006 Passed.
TEST-CORR-007: Repeated failure... -> TEST-CORR-007 Passed.
TEST-CORR-008: Prompt-level failure... -> TEST-CORR-008 Passed.
TEST-CORR-009: Decision-level failure... -> TEST-CORR-009 Passed.
TEST-CORR-010: Intelligence-level failure... -> TEST-CORR-010 Passed.
TEST-CORR-011: Prompt diff integrity... -> TEST-CORR-011 Passed.
TEST-CORR-012: Linter violation after correction... -> TEST-CORR-012 Passed.

==================================================
ALL CORRECTION TEST CASES PASSED SUCCESSFULLY!
==================================================
```

---

## 10. Example Output Traces

### A. Example CorrectionPlan
```json
{
  "correction_id": "CORR-001",
  "evaluation_id": "EVAL-001",
  "shot_id": "craftsmanship_01",
  "failure": {
    "dimension": "material_fidelity",
    "severity": "HARD",
    "observation": "textile looks waxy"
  },
  "cause": {
    "category": "material_representation"
  },
  "affected_segments": ["MATERIAL", "QUALITY"],
  "preserve_segments": ["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "FORBIDDEN"],
  "corrections": [
    {
      "segment": "MATERIAL",
      "operation": "AUGMENT",
      "target": "Fabric/Material base",
      "instruction": "visible weave relief"
    },
    {
      "segment": "QUALITY",
      "operation": "ADD",
      "instruction": "gravity-responsive drape tension"
    }
  ],
  "success_criteria": ["material_fidelity >= 0.8"],
  "confidence": 0.9
}
```

### B. Example PromptDiff
```json
{
  "modified_segments": ["MATERIAL", "QUALITY"],
  "changes": [
    {
      "segment": "MATERIAL",
      "operation": "AUGMENT",
      "before": "Fabric/Material base: Banarasi Silk with Zari detailing.",
      "after": "Fabric/Material base: Banarasi Silk with Zari detailing. with visible weave relief"
    },
    {
      "segment": "QUALITY",
      "operation": "ADD",
      "before": "physically plausible folds, natural clean skin texture.",
      "after": "physically plausible folds, natural clean skin texture., gravity-responsive drape tension"
    }
  ],
  "unchanged_segments": ["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "FORBIDDEN"]
}
```

### C. Example IntelligenceGapReport
```json
{
  "report_id": "GAP-1786872890",
  "failure_pattern": "Repeated low score in dimension: 'material_fidelity'",
  "target_dimension": "material_fidelity",
  "attempts_count": 3,
  "gap_hypothesis": "Textile models continuously smooth microtextures under standard studio lighting presets.",
  "timestamp": 1786872890.123
}
```

---

## 11. Remaining Architectural Risks
*   **Upstream Solver Constraints:** Direct conflicts in the physical rules (e.g., silk rules vs denim rules in multi-product layouts) require coordination at Level 2 (Decision Engine) rather than simple prompt editing.
