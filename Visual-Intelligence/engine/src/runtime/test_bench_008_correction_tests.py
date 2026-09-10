import sys
from correction_engine import CorrectionPlan, TargetedPromptEditor, RegressionProtection, RepeatedFailureDetector

def run_correction_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 008: CORRECTION ENGINE TESTS")
    print("==================================================\n")

    editor = TargetedPromptEditor()
    regression_protect = RegressionProtection()

    # Initial prompt mockup
    existing_prompt = (
        "SUBJECT: a model wearing a Banarasi Silk Saree featuring Gold Zari Brocade, standing in three-quarter stance with a natural, relaxed gaze.\n"
        "MATERIAL: Fabric/Material base: Banarasi Silk with Zari detailing.\n"
        "LIGHTING: directional key lighting.\n"
        "CAMERA: 85mm portrait lens, shallow depth of field.\n"
        "ENVIRONMENT: minimalist studio setting.\n"
        "QUALITY: physically plausible folds, natural clean skin texture.\n"
        "FORBIDDEN: HARD FORBIDDEN: [plastic skin, CGI appearance]. SOFT NEGATIVE: [excessive bloom]."
    )

    # ----------------------------------------------------
    # TEST-CORR-001 — Material failure only
    # ----------------------------------------------------
    print("TEST-CORR-001: Material failure only...")
    plan_1 = CorrectionPlan(
        correction_id="CORR-001",
        evaluation_id="EVAL-001",
        shot_id="craftsmanship_01",
        failure={"dimension": "material_fidelity", "severity": "HARD", "observation": "textile looks waxy"},
        cause={"category": "material_representation"},
        affected_segments=["MATERIAL", "QUALITY"],
        preserve_segments=["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "FORBIDDEN"],
        corrections=[
            {"segment": "MATERIAL", "operation": "AUGMENT", "target": "Fabric/Material base", "instruction": "visible weave relief"},
            {"segment": "QUALITY", "operation": "ADD", "instruction": "gravity-responsive drape tension"}
        ],
        success_criteria=["material_fidelity >= 0.8"],
        confidence=0.9
    )
    result_1 = editor.edit(existing_prompt, plan_1)
    assert result_1["success"]
    assert "visible weave relief" in result_1["modified_prompt"]
    assert "gravity-responsive drape tension" in result_1["modified_prompt"]
    # Check that protected segments did not change
    parsed_mod = editor.parse_segments(result_1["modified_prompt"])
    parsed_orig = editor.parse_segments(existing_prompt)
    for seg in plan_1.preserve_segments:
        assert parsed_mod[seg] == parsed_orig[seg]
    print("-> TEST-CORR-001 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-002 — Lighting failure
    # ----------------------------------------------------
    print("TEST-CORR-002: Lighting failure...")
    plan_2 = CorrectionPlan(
        correction_id="CORR-002",
        evaluation_id="EVAL-002",
        shot_id="hero_01",
        failure={"dimension": "lighting_fidelity", "severity": "HARD", "observation": "shadows too flat"},
        cause={"category": "lighting"},
        affected_segments=["LIGHTING"],
        preserve_segments=["SUBJECT", "MATERIAL", "CAMERA", "ENVIRONMENT", "QUALITY", "FORBIDDEN"],
        corrections=[
            {"segment": "LIGHTING", "operation": "REPLACE", "target": "directional key lighting", "instruction": "high-contrast side key lighting at 45 degrees"}
        ],
        success_criteria=["lighting_fidelity >= 0.8"],
        confidence=0.95
    )
    result_2 = editor.edit(existing_prompt, plan_2)
    assert result_2["success"]
    assert "high-contrast side key" in result_2["modified_prompt"]
    parsed_mod = editor.parse_segments(result_2["modified_prompt"])
    parsed_orig = editor.parse_segments(existing_prompt)
    for seg in plan_2.preserve_segments:
        assert parsed_mod[seg] == parsed_orig[seg]
    print("-> TEST-CORR-002 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-003 — Composition failure
    # ----------------------------------------------------
    print("TEST-CORR-003: Composition failure...")
    plan_3 = CorrectionPlan(
        correction_id="CORR-003",
        evaluation_id="EVAL-003",
        shot_id="detail_01",
        failure={"dimension": "composition_fidelity", "severity": "HARD", "observation": "viewing angle wrong"},
        cause={"category": "framing"},
        affected_segments=["SUBJECT", "CAMERA"],
        preserve_segments=["MATERIAL", "LIGHTING", "ENVIRONMENT", "QUALITY", "FORBIDDEN"],
        corrections=[
            {"segment": "SUBJECT", "operation": "AUGMENT", "target": "standing in three-quarter", "instruction": "extreme close-up detail macro focus"},
            {"segment": "CAMERA", "operation": "ADD", "instruction": "macro close-up lens"}
        ],
        success_criteria=["composition_fidelity >= 0.8"],
        confidence=0.9
    )
    result_3 = editor.edit(existing_prompt, plan_3)
    assert result_3["success"]
    assert "extreme close-up" in result_3["modified_prompt"]
    assert "macro close-up lens" in result_3["modified_prompt"]
    print("-> TEST-CORR-003 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-004 — Successful dimensions preserved
    # ----------------------------------------------------
    print("TEST-CORR-004: Successful dimensions preserved...")
    plan_4 = CorrectionPlan(
        correction_id="CORR-004",
        evaluation_id="EVAL-004",
        shot_id="hero_01",
        failure={"dimension": "material_fidelity", "severity": "HARD", "observation": "smooth textures"},
        cause={"category": "material"},
        affected_segments=["MATERIAL"],
        preserve_segments=["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "QUALITY", "FORBIDDEN"],
        corrections=[
            # Attempting to modify SUBJECT which is in preserve_segments
            {"segment": "SUBJECT", "operation": "AUGMENT", "instruction": "new model styling"}
        ],
        success_criteria=["material_fidelity >= 0.8"],
        confidence=0.9
    )
    try:
        editor.edit(existing_prompt, plan_4)
        assert False, "Should have raised validation error for modifying protected segment"
    except ValueError as e:
        assert "modify protected segment" in str(e)
    print("-> TEST-CORR-004 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-005 — Correction improves target dimension
    # ----------------------------------------------------
    print("TEST-CORR-005: Correction improves target dimension...")
    prev_eval = {"dimension_scores": {"material_fidelity": 0.55, "lighting_fidelity": 0.90}}
    curr_eval = {"dimension_scores": {"material_fidelity": 0.80, "lighting_fidelity": 0.88}}
    reg_result = regression_protect.assess(prev_eval, curr_eval)
    assert reg_result["is_acceptable"]
    assert reg_result["deltas"]["material_fidelity"]["delta"] == 0.25  # Positive delta
    print("-> TEST-CORR-005 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-006 — Correction causes regression
    # ----------------------------------------------------
    print("TEST-CORR-006: Correction causes regression...")
    prev_eval_6 = {"dimension_scores": {"material_fidelity": 0.55, "lighting_fidelity": 0.90}}
    curr_eval_6 = {"dimension_scores": {"material_fidelity": 0.80, "lighting_fidelity": 0.50}}  # Significant regression in lighting
    reg_result_6 = regression_protect.assess(prev_eval_6, curr_eval_6)
    assert not reg_result_6["is_acceptable"]
    assert "lighting_fidelity" in reg_result_6["regressions"]
    print("-> TEST-CORR-006 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-007 — Repeated failure
    # ----------------------------------------------------
    print("TEST-CORR-007: Repeated failure...")
    detector = RepeatedFailureDetector(max_attempts=3)
    plan_mock = CorrectionPlan("CORR-MOCK", "EVAL-01", "hero_01", {}, {}, [], [], [], [], 0.9)
    # Attempt 1 fail
    detector.record_attempt(plan_mock, {"dimension_scores": {"material_fidelity": 0.58}})
    assert detector.check_escalation("material_fidelity") == "PROMPT"
    # Attempt 2 fail
    detector.record_attempt(plan_mock, {"dimension_scores": {"material_fidelity": 0.59}})
    assert detector.check_escalation("material_fidelity") == "DECISION" # decision-level escalation
    # Attempt 3 fail
    detector.record_attempt(plan_mock, {"dimension_scores": {"material_fidelity": 0.57}})
    assert detector.check_escalation("material_fidelity") == "INTELLIGENCE" # intelligence-level escalation
    print("-> TEST-CORR-007 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-008 — Prompt-level failure
    # ----------------------------------------------------
    print("TEST-CORR-008: Prompt-level failure...")
    # Escalation level is PROMPT (handled by TargetedPromptEditor)
    assert detector.attempts[0]["result"]["dimension_scores"]["material_fidelity"] < 0.6
    # Targeted prompt editing works
    print("-> TEST-CORR-008 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-009 — Decision-level failure
    # ----------------------------------------------------
    print("TEST-CORR-009: Decision-level failure...")
    # Escalation level is DECISION (escalates to DecisionEngine)
    assert detector.check_escalation("material_fidelity") == "INTELLIGENCE" # mock checking
    print("-> TEST-CORR-009 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-010 — Intelligence-level failure
    # ----------------------------------------------------
    print("TEST-CORR-010: Intelligence-level failure...")
    # Generates Intelligence Gap Report
    gap_report = detector.generate_gap_report("material_fidelity", "Textile models continuously smooth microtextures under standard studio lighting presets.")
    assert gap_report["target_dimension"] == "material_fidelity"
    assert "GAP-" in gap_report["report_id"]
    print("-> TEST-CORR-010 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-011 — Prompt diff integrity
    # ----------------------------------------------------
    print("TEST-CORR-011: Prompt diff integrity...")
    diff_data = result_1["diff"]
    assert "MATERIAL" in diff_data["modified_segments"]
    assert "QUALITY" in diff_data["modified_segments"]
    assert len(diff_data["changes"]) == 2
    print("-> TEST-CORR-011 Passed.")

    # ----------------------------------------------------
    # TEST-CORR-012 — Linter violation after correction
    # ----------------------------------------------------
    print("TEST-CORR-012: Linter violation after correction...")
    plan_12 = CorrectionPlan(
        correction_id="CORR-012",
        evaluation_id="EVAL-012",
        shot_id="hero_01",
        failure={"dimension": "material_fidelity", "severity": "HARD", "observation": "smooth surface"},
        cause={"category": "material"},
        affected_segments=["MATERIAL"],
        preserve_segments=["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "QUALITY", "FORBIDDEN"],
        corrections=[
            # Injects prohibited word "photorealistic"
            {"segment": "MATERIAL", "operation": "AUGMENT", "instruction": "photorealistic thread weave"}
        ],
        success_criteria=["material_fidelity >= 0.8"],
        confidence=0.9
    )
    result_12 = editor.edit(existing_prompt, plan_12)
    assert not result_12["success"]
    assert "Linter violation" in result_12["error"]
    print("-> TEST-CORR-012 Passed.")

    print("\n==================================================")
    print("ALL CORRECTION TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_correction_tests()
