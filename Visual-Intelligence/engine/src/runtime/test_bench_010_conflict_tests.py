import sys
from conflict_resolver import ConflictResolver, ProductRequirement, MultiProductConflictReport

def run_multi_product_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 010: MULTI-PRODUCT RESOLUTION TESTS")
    print("==================================================\n")

    resolver = ConflictResolver()

    # ----------------------------------------------------
    # TEST-MP-001 — No Conflict
    # ----------------------------------------------------
    print("TEST-MP-001: No Conflict...")
    products = [
        {"product_id": "saree_01", "role": "PRIMARY"},
        {"product_id": "jewelry_01", "role": "SECONDARY"}
    ]
    reqs = [
        ProductRequirement("REQ-01", "saree_01", "apparel", "LIGHTING", "HIGH", "KeyLight", "soft directional light"),
        ProductRequirement("REQ-02", "jewelry_01", "jewelry", "LIGHTING", "MEDIUM", "KeyLight", "soft directional light")
    ]
    solution = resolver.resolve("shot_01", "CRAFTSMANSHIP", products, reqs)
    assert solution.resolved_solution["lighting"]["KeyLight"] == "soft directional light"
    assert solution.resolutions[0]["strategy"] == "ACCOMMODATE"
    print("-> TEST-MP-001 Passed.")

    # ----------------------------------------------------
    # TEST-MP-002 — Partial Conflict
    # ----------------------------------------------------
    print("TEST-MP-002: Partial/Apparent Conflict...")
    reqs_2 = [
        ProductRequirement("REQ-03", "saree_01", "apparel", "LIGHTING", "MANDATORY", "KeyLight", "soft diffused light"),
        ProductRequirement("REQ-04", "jewelry_01", "jewelry", "LIGHTING", "HIGH", "KeyLight", "controlled accent kicker")
    ]
    solution_2 = resolver.resolve("shot_02", "CRAFTSMANSHIP", products, reqs_2)
    assert solution_2.resolutions[0]["strategy"] == "ISOLATE"
    assert solution_2.resolved_solution["lighting"]["global"] == "soft diffused light"
    assert "controlled accent kicker" in solution_2.resolved_solution["lighting"]["accents"]
    print("-> TEST-MP-002 Passed.")

    # ----------------------------------------------------
    # TEST-MP-003 — Direct Conflict
    # ----------------------------------------------------
    print("TEST-MP-003: Direct Conflict...")
    reqs_3 = [
        ProductRequirement("REQ-05", "saree_01", "apparel", "LIGHTING", "HIGH", "KeyLight", "hard side key"),
        ProductRequirement("REQ-06", "jewelry_01", "jewelry", "LIGHTING", "MEDIUM", "KeyLight", "flat front light")
    ]
    solution_3 = resolver.resolve("shot_03", "CRAFTSMANSHIP", products, reqs_3)
    assert solution_3.resolutions[0]["strategy"] == "PRIORITIZE"
    # Saree is primary (role PRIMARY = 4, HIGH = 4 -> score 8) vs Jewelry (role SECONDARY = 3, MEDIUM = 3 -> score 6)
    # Saree wins
    assert solution_3.resolved_solution["lighting"]["KeyLight"] == "hard side key"
    print("-> TEST-MP-003 Passed.")

    # ----------------------------------------------------
    # TEST-MP-004 — Primary Product Priority
    # ----------------------------------------------------
    print("TEST-MP-004: Primary Product Priority...")
    # Verified by TEST-MP-003 priority weights resolving Saree as the winner
    print("-> TEST-MP-004 Passed.")

    # ----------------------------------------------------
    # TEST-MP-005 — Deferred Requirement
    # ----------------------------------------------------
    print("TEST-MP-005: Deferred Requirement...")
    assert len(solution_3.deferred_requirements) == 1
    def_req = solution_3.deferred_requirements[0]
    assert def_req["requirement_id"] == "REQ-06"
    assert def_req["resolution"] == "DEFER"
    assert "reason" in def_req
    assert "impact" in def_req
    print("-> TEST-MP-005 Passed.")

    # ----------------------------------------------------
    # TEST-MP-006 — Shared Lighting Solution
    # ----------------------------------------------------
    print("TEST-MP-006: Shared Lighting Solution...")
    # Verify that in TEST-MP-002 we produce a single global lighting parameter with isolated accent kickers
    # rather than competing global entries
    assert "global" in solution_2.resolved_solution["lighting"]
    assert "accents" in solution_2.resolved_solution["lighting"]
    print("-> TEST-MP-006 Passed.")

    # ----------------------------------------------------
    # TEST-MP-007 — Explainability
    # ----------------------------------------------------
    print("TEST-MP-007: Explainability...")
    res_trace = solution_3.resolutions[0]
    assert "strategy" in res_trace
    assert "description" in res_trace
    assert len(res_trace["preserved_requirements"]) > 0
    assert len(res_trace["reduced_requirements"]) > 0
    print("-> TEST-MP-007 Passed.")

    # ----------------------------------------------------
    # TEST-MP-008 — Prompt Compiler Boundary
    # ----------------------------------------------------
    print("TEST-MP-008: Prompt Compiler Boundary...")
    # Prompt Compiler receives resolved solution (like solution.resolved_solution) rather than competing req list
    assert isinstance(solution.resolved_solution, dict)
    print("-> TEST-MP-008 Passed.")

    # ----------------------------------------------------
    # TEST-MP-009 — Evaluator Boundary
    # ----------------------------------------------------
    print("TEST-MP-009: Evaluator Boundary...")
    # The evaluation payload has access to deferred_requirements so it doesn't fail on deferred items
    assert hasattr(solution, "deferred_requirements")
    print("-> TEST-MP-009 Passed.")

    # ----------------------------------------------------
    # TEST-MP-010 — Mandatory Conflict
    # ----------------------------------------------------
    print("TEST-MP-010: Mandatory Conflict...")
    reqs_10 = [
        ProductRequirement("REQ-10A", "saree_01", "apparel", "LIGHTING", "MANDATORY", "KeyLight", "hard side key"),
        ProductRequirement("REQ-10B", "jewelry_01", "jewelry", "LIGHTING", "MANDATORY", "KeyLight", "flat front light")
    ]
    try:
        resolver.resolve("shot_10", "CRAFTSMANSHIP", products, reqs_10)
        assert False, "Should have escalated mandatory conflict"
    except MultiProductConflictReport as report:
        assert report.conflict["conflict_type"] == "KEY_CONFLICT"
        assert "mandatory" in report.message.lower()
        assert "REP-" in report.report_id
    print("-> TEST-MP-010 Passed.")

    # ----------------------------------------------------
    # TEST-MP-011 — Knowledge Gap
    # ----------------------------------------------------
    print("TEST-MP-011: Knowledge Gap...")
    reqs_11 = [
        ProductRequirement("REQ-11A", "saree_01", "apparel", "LIGHTING", "HIGH", "KeyLight", "soft overall daylight"),
        ProductRequirement("REQ-11B", "jewelry_01", "jewelry", "LIGHTING", "HIGH", "KeyLight", "unknown")
    ]
    try:
        resolver.resolve("shot_11", "CRAFTSMANSHIP", products, reqs_11)
        assert False, "Should have escalated knowledge gap"
    except ValueError as e:
        assert "Knowledge-Layer Escalation" in str(e)
        # Verify structured metadata fields (PATCH-D)
        assert hasattr(e, "product_id")
        assert e.product_id == "jewelry_01"
        assert e.category == "LIGHTING"
        assert e.property_key == "KeyLight"
        assert e.missing_value == "unknown"
    print("-> TEST-MP-011 Passed.")

    # ----------------------------------------------------
    # TEST-MP-012 — Provenance
    # ----------------------------------------------------
    print("TEST-MP-012: Provenance...")
    # Every resolution traces back to contributing requirements
    preserved_req = solution_3.resolutions[0]["preserved_requirements"][0]
    assert preserved_req["requirement_id"] == "REQ-05"
    print("-> TEST-MP-012 Passed.")

    # ----------------------------------------------------
    # TEST-MP-013 — COMPROMISE
    # ----------------------------------------------------
    print("TEST-MP-013: COMPROMISE...")
    reqs_13 = [
        ProductRequirement("REQ-13A", "saree_01", "apparel", "MATERIAL", "HIGH", "texture_visibility", "high"),
        ProductRequirement("REQ-13B", "jewelry_01", "jewelry", "MATERIAL", "HIGH", "specular_response", "moderate")
    ]
    solution_13 = resolver.resolve("shot_13", "CRAFTSMANSHIP", products, reqs_13)
    # Find COMPROMISE strategy resolution
    comp_res = next((res for res in solution_13.resolutions if res["strategy"] == "COMPROMISE"), None)
    assert comp_res is not None
    assert comp_res["strategy"] == "COMPROMISE"
    # Ensure both are represented in final resolved_solution
    assert "moderate-high texture visibility" in solution_13.resolved_solution["material"]["saree_01"]
    assert "moderate-high specular response" in solution_13.resolved_solution["material"]["jewelry_01"]
    print("-> TEST-MP-013 Passed.")

    # ----------------------------------------------------
    # TEST-MP-014 — Cross-Dimension Conflict
    # ----------------------------------------------------
    print("TEST-MP-014: Cross-Dimension Conflict...")
    reqs_14 = [
        ProductRequirement("REQ-14A", "saree_01", "apparel", "LIGHTING", "HIGH", "texture_reveal", "soft directional light"),
        ProductRequirement("REQ-14B", "jewelry_01", "jewelry", "MATERIAL", "HIGH", "highlight_definition", "strong specular response")
    ]
    solution_14 = resolver.resolve("shot_14", "CRAFTSMANSHIP", products, reqs_14)
    # Cross-dimension conflict should be detected
    cross_res = next((res for res in solution_14.resolutions if res["strategy"] == "ISOLATE"), None)
    assert cross_res is not None
    print("-> TEST-MP-014 Passed.")

    # ----------------------------------------------------
    # TEST-MP-015 — Objective-Dependent Resolution
    # ----------------------------------------------------
    print("TEST-MP-015: Objective-Dependent Resolution...")
    # Saree (PRIMARY) KeyLight -> hard side key (HIGH)
    # Jewelry (SECONDARY) KeyLight -> flat front light (MANDATORY)
    reqs_15 = [
        ProductRequirement("REQ-15A", "saree_01", "apparel", "LIGHTING", "HIGH", "KeyLight", "hard side key"),
        ProductRequirement("REQ-15B", "jewelry_01", "jewelry", "LIGHTING", "MANDATORY", "KeyLight", "flat front light")
    ]
    # Under CRAFTSMANSHIP:
    # Saree priority = 4 (PRIMARY) + 4 (HIGH) + 3 (CRAFTSMANSHIP boost because PRIMARY) = 11
    # Jewelry priority = 3 (SECONDARY) + 5 (MANDATORY) + 0 = 8
    # Saree wins
    solution_15_craft = resolver.resolve("shot_15A", "CRAFTSMANSHIP", products, reqs_15)
    assert solution_15_craft.resolved_solution["lighting"]["KeyLight"] == "hard side key"

    # Under LIFESTYLE:
    # Saree priority = 4 (PRIMARY) + 4 (HIGH) + 0 = 8
    # Jewelry priority = 3 (SECONDARY) + 5 (MANDATORY) + 3 (LIFESTYLE boost because LIGHTING/SECONDARY) = 11
    # Jewelry wins
    solution_15_life = resolver.resolve("shot_15B", "LIFESTYLE", products, reqs_15)
    assert solution_15_life.resolved_solution["lighting"]["KeyLight"] == "flat front light"
    
    # Assert they resolved differently under different objectives
    assert solution_15_craft.resolved_solution["lighting"]["KeyLight"] != solution_15_life.resolved_solution["lighting"]["KeyLight"]
    print("-> TEST-MP-015 Passed.")

    print("\n==================================================")
    print("ALL MULTI-PRODUCT TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_multi_product_tests()
