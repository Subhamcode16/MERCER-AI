# INTELLIGENCE → ENGINEERING RESPONSE
# ENG-RTC-006-IMPLEMENTATION — Multi-Product Intelligence & Conflict Resolution

**Protocol:** ENGINEER-COMMUNICATION-001  
**From:** Engineering Agent  
**To:** Intelligence Architect  
**Status:** VALIDATED & COMPLETED  
**Version:** 1.0  
**Date:** 2026-08-16  
**Depends On:** ENG-RTC-001 through ENG-RTC-005  
**Architectural Position:** Intelligence Resolution → Shot-Level Creative Solution

---

## 1. Files Created/Changed
*   [`Visual-Intelligence/engine/src/runtime/conflict_resolver.py`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/engine/src/runtime/conflict_resolver.py): [NEW] Implemented the Multi-Product Conflict Resolution engine, including `ProductRequirement`, `Conflict`, `ConflictResolution`, `ResolvedShotSolution`, `MultiProductConflictReport`, and the `ConflictResolver` coordinator.
*   [`Visual-Intelligence/engine/src/runtime/test_bench_010_conflict_tests.py`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/engine/src/runtime/test_bench_010_conflict_tests.py): [NEW] Implemented verification tests for cases `TEST-MP-001` through `TEST-MP-012`.

---

## 2. Product Requirement & Role Representation
*   **ProductRequirement:** Encapsulates visual, material, lighting, and camera requirements at the individual product level. Stores `requirement_id`, `product_id`, `domain`, `category`, `importance` (MANDATORY, HIGH, MEDIUM, LOW), `property_key`, and `value`.
*   **ProductRole:** Defines the product's priority inside the shot (`PRIMARY`, `SECONDARY`, `SUPPORTING`, `BACKGROUND`). Assigned weights directly map to conflict negotiation priority:
    *   `PRIMARY` = 4
    *   `SECONDARY` = 3
    *   `SUPPORTING` = 2
    *   `BACKGROUND` = 1

---

## 3. Shot Objective & Conflict Detection
*   **Shot Objective:** Supports `CRAFTSMANSHIP`, `LIFESTYLE`, `CONVERSION`, and `EDITORIAL` objectives.
*   **Conflict Detection:** Groups requirements by category and key. If multiple requirements from different products compete for the same key (e.g. `LIGHTING:KeyLight` or `CAMERA:Framing`), a conflict is explicitly detected and classified.
*   **Conflict Classification:**
    *   `Direct`: Mutually exclusive global parameters (e.g. `hard side key` vs `flat front light`).
    *   `Apparent` / `Partial`: Requirements can be accommodated or isolated simultaneously via advanced local setups (e.g. soft overall light + controlled accent kicker for jewelry highlight).

---

## 4. Resolution Strategies & Priority Score
The resolver computes a priority score for each competing requirement:
$$\text{Priority Score} = \text{Role Weight} + \text{Importance Weight}$$
*   **ACCOMMODATE:** Satisfies both requirements if they are compatible.
*   **PRIORITIZE:** Selects the requirement with the highest priority score for the global parameter, while deferring others.
*   **ISOLATE:** Satisfies both by dividing lighting setups into a `GLOBAL` component and `LOCAL ACCENTS`.
*   **DEFER:** Reduces or drops a low-priority requirement, recording the reason and impact to ensure no requirement vanishes silently.
*   **ESCALATE:** Triggers when mandatory constraints collide or domain knowledge is missing.

---

## 5. Provenance & Resolved Shot Solution representation
The output of the resolver is a structured `ResolvedShotSolution` exposing:
*   `shot_id` and `objective`.
*   `primary_product` and the active role dictionary.
*   `resolved_solution`: Final parameters parsed for `lighting`, `camera`, `material`, and `environment`.
*   `resolutions`: Explicit explainability logs detailing strategies, reasons, preserved, and reduced requirements.
*   `deferred_requirements`: Explicit tracking of deferred constraints.

---

## 6. Prompt Compiler & Evaluator Integration
*   **Prompt Compiler Boundary:** The compiler is isolated from creative decision-making. It receives the `ResolvedShotSolution` (which resolves conflicts upstream) rather than competing requirements.
*   **Evaluator Boundary:** The evaluator receives the `ResolvedShotSolution` and `deferred_requirements`. This ensures the evaluator evaluates only against resolved choices and does not punish an image for intentionally deferred constraints.

---

## 7. Escalation Handling
*   **MultiProductConflictReport:** Raised when two or more `MANDATORY` requirements are in a `Direct` conflict (cannot coexist).
*   **Knowledge-Layer Escalation:** Raised (`ValueError`) if a requirement contains `"unknown"` values, signaling that the resolver lacks sufficient domain knowledge.

---

## 8. Verification Results (TEST-MP-001 through TEST-MP-012)
All tests passed successfully:
```text
==================================================
RUNNING TEST BENCH 010: MULTI-PRODUCT RESOLUTION TESTS
==================================================
TEST-MP-001: No Conflict... -> TEST-MP-001 Passed.
TEST-MP-002: Partial/Apparent Conflict... -> TEST-MP-002 Passed.
TEST-MP-003: Direct Conflict... -> TEST-MP-003 Passed.
TEST-MP-004: Primary Product Priority... -> TEST-MP-004 Passed.
TEST-MP-005: Deferred Requirement... -> TEST-MP-005 Passed.
TEST-MP-006: Shared Lighting Solution... -> TEST-MP-006 Passed.
TEST-MP-007: Explainability... -> TEST-MP-007 Passed.
TEST-MP-008: Prompt Compiler Boundary... -> TEST-MP-008 Passed.
TEST-MP-009: Evaluator Boundary... -> TEST-MP-009 Passed.
TEST-MP-010: Mandatory Conflict... -> TEST-MP-010 Passed.
TEST-MP-011: Knowledge Gap... -> TEST-MP-011 Passed.
TEST-MP-012: Provenance... -> TEST-MP-012 Passed.

==================================================
ALL MULTI-PRODUCT TEST CASES PASSED SUCCESSFULLY!
==================================================
```

---

## 9. Examples

### A. Example Multi-Product Resolution (TEST-MP-002)
*   **Input:** Saree requires `soft diffused light` (MANDATORY); Jewelry requires `controlled accent kicker` (HIGH).
*   **Resolution:** `ISOLATE` strategy.
*   **Output Solution:**
    ```json
    {
      "lighting": {
        "global": "soft diffused light",
        "accents": ["controlled accent kicker"]
      }
    }
    ```

### B. Example Unresolved Conflict (TEST-MP-010)
*   **Input:** Saree requires `hard side key` (MANDATORY); Jewelry requires `flat front light` (MANDATORY).
*   **Resolution:** Triggers `MultiProductConflictReport` escalation due to Direct conflict of Mandatory properties.
    ```json
    {
      "report_id": "REP-1786872890",
      "conflict": {
        "conflict_id": "CONF-1",
        "conflict_type": "Direct",
        "category": "LIGHTING",
        "description": "Competing requirements on LIGHTING:KeyLight: saree_01(hard side key), jewelry_01(flat front light)"
      },
      "message": "Multi-Product Conflict: mutate/direct collision of mandatory requirements on LIGHTING:KeyLight"
    }
    ```

---

## 10. Compliance & Limitations
*   **No Scope Expansion:** Confirmed that no new material or domain ontology has been introduced, only conflict resolution logic for existing categories.
*   **Architectural Risks:** Complex spatial composition conflicts (e.g., shoe and neck jewelry visibility in the same framing window) will require geometric boundary box calculations in subsequent versions.
