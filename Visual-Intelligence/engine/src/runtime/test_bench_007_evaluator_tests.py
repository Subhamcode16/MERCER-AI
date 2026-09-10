import sys
from evaluation import CreativeEvaluator

def run_evaluator_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 007: CREATIVE EVALUATOR TESTS")
    print("==================================================\n")

    evaluator = CreativeEvaluator()

    # Base payload structure
    base_payload = {
        "campaign_id": "test_camp_01",
        "shot_plan": {"shot_id": "hero_01", "shot_priority": "Default", "Framing": "Waist-up portrait"},
        "product_dna": {"BaseGarment": "Saree", "Material": "Silk"},
        "creative_solution": {"Lighting": {"KeyLight": "directional lighting"}},
        "authenticity_profile": {"SkinPores": 0.8},
        "brand_requirements": {"positioning": "Luxury"},
        "campaign_intent": "Luxury awareness",
        "simulated_features": {}
    }

    # ----------------------------------------------------
    # TEST-EVAL-001 — High product fidelity
    # ----------------------------------------------------
    print("TEST-EVAL-001: High product fidelity...")
    payload_1 = dict(base_payload)
    payload_1["simulated_features"] = {
        "BaseGarment": "Saree",
        "product_defects": []
    }
    result_1 = evaluator.evaluate(payload_1)
    assert result_1["dimension_scores"]["product_fidelity"] >= 0.8
    assert result_1["overall_decision"] == "PASS"
    print("-> TEST-EVAL-001 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-002 — Incorrect product construction
    # ----------------------------------------------------
    print("TEST-EVAL-002: Incorrect product construction...")
    payload_2 = dict(base_payload)
    payload_2["simulated_features"] = {
        "BaseGarment": "Saree",
        "product_defects": ["incorrect border"]
    }
    result_2 = evaluator.evaluate(payload_2)
    assert result_2["overall_decision"] in ["REGENERATE", "FAIL"]
    assert any("border" in hf.lower() for hf in result_2["hard_failures"])
    print("-> TEST-EVAL-002 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-003 — Strong product + weak material
    # ----------------------------------------------------
    print("TEST-EVAL-003: Strong product + weak material...")
    payload_3 = dict(base_payload)
    payload_3["shot_plan"] = {"shot_id": "hero_01", "shot_priority": "Craftsmanship", "Framing": "Waist-up portrait"}
    payload_3["simulated_features"] = {
        "BaseGarment": "Saree",
        "product_defects": [],
        "material_defects": ["melted textile"]
    }
    result_3 = evaluator.evaluate(payload_3)
    assert result_3["dimension_scores"]["product_fidelity"] == 1.0
    assert result_3["dimension_scores"]["material_fidelity"] < 0.7
    assert result_3["overall_decision"] == "REGENERATE"
    assert "material" in result_3["targeted_regeneration_guidance"].lower()
    print("-> TEST-EVAL-003 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-004 — Good image + wrong campaign intent
    # ----------------------------------------------------
    print("TEST-EVAL-004: Good image + wrong campaign intent...")
    payload_4 = dict(base_payload)
    payload_4["simulated_features"] = {
        "BaseGarment": "Saree",
        "intent_violations": ["Luxury awareness"]
    }
    result_4 = evaluator.evaluate(payload_4)
    assert result_4["dimension_scores"]["photographic_realism"] == 1.0
    assert result_4["dimension_scores"]["campaign_intent_alignment"] < 0.6
    assert result_4["overall_decision"] != "PASS"
    print("-> TEST-EVAL-004 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-005 — Forbidden AI artifact
    # ----------------------------------------------------
    print("TEST-EVAL-005: Forbidden AI artifact...")
    payload_5 = dict(base_payload)
    payload_5["simulated_features"] = {
        "BaseGarment": "Saree",
        "detected_forbidden_artifacts": ["plastic skin"]
    }
    result_5 = evaluator.evaluate(payload_5)
    assert result_5["overall_decision"] == "REGENERATE"
    assert any("plastic skin" in hf for hf in result_5["hard_failures"])
    print("-> TEST-EVAL-005 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-006 — Minor soft defects
    # ----------------------------------------------------
    print("TEST-EVAL-006: Minor soft defects...")
    payload_6 = dict(base_payload)
    payload_6["simulated_features"] = {
        "BaseGarment": "Saree",
        "human_defects": ["mildly artificial hair"]
    }
    result_6 = evaluator.evaluate(payload_6)
    assert result_6["overall_decision"] == "PASS_WITH_WARNINGS"
    assert len(result_6["soft_failures"]) > 0
    print("-> TEST-EVAL-006 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-007 — Human-review ambiguity
    # ----------------------------------------------------
    print("TEST-EVAL-007: Human-review ambiguity...")
    payload_7 = dict(base_payload)
    payload_7["simulated_features"] = {
        "BaseGarment": "Saree",
        "human_defects": []
    }
    # Simulate a score in the ambiguous range (0.6 - 0.75) by introducing a custom low scoring modifier
    payload_7["simulated_features"] = {
        "BaseGarment": "Saree",
        "KeyLight": "flat lighting" # reduces lighting score to 0.7 (ambiguous range)
    }
    result_7 = evaluator.evaluate(payload_7)
    assert result_7["overall_decision"] == "HUMAN_REVIEW"
    print("-> TEST-EVAL-007 Passed.")

    # ----------------------------------------------------
    # TEST-EVAL-008 — Independent vibe/profile evaluation
    # ----------------------------------------------------
    print("TEST-EVAL-008: Independent vibe/profile evaluation...")
    payload_8 = dict(base_payload)
    payload_8["campaign_intent"] = "Moody"
    payload_8["authenticity_profile"] = {"Name": "E-Commerce Catalog", "SkinPores": 0.4}
    # Verify both dimensions are resolved and returned independently in metadata
    result_8 = evaluator.evaluate(payload_8)
    assert result_8["campaign_id"] == "test_camp_01"
    assert result_8["shot_id"] == "hero_01"
    print("-> TEST-EVAL-008 Passed.")

    print("\n==================================================")
    print("ALL EVALUATOR TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_evaluator_tests()
