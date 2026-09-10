import sys
from correction_engine import SegmentNormalizer, CorrectionPlan, TargetedPromptEditor, RepeatedFailureDetector, EscalationMetadata

def run_patch_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 009: CORRECTION ENGINE PATCH TESTS")
    print("==================================================\n")

    # ----------------------------------------------------
    # TEST-NORM-001 — Duplicate punctuation
    # ----------------------------------------------------
    print("TEST-NORM-001: Duplicate punctuation...")
    res_1 = SegmentNormalizer.normalize_segment("natural texture., visible weave")
    assert res_1 == "natural texture, visible weave"
    print("-> TEST-NORM-001 Passed.")

    # ----------------------------------------------------
    # TEST-NORM-002 — Incorrect sentence joining
    # ----------------------------------------------------
    print("TEST-NORM-002: Incorrect sentence joining...")
    res_2 = SegmentNormalizer.normalize_segment("silk texture. with visible weave relief")
    assert res_2 == "silk texture with visible weave relief"
    print("-> TEST-NORM-002 Passed.")

    # ----------------------------------------------------
    # TEST-NORM-003 — Duplicate descriptors
    # ----------------------------------------------------
    print("TEST-NORM-003: Duplicate descriptors...")
    res_3 = SegmentNormalizer.normalize_segment("visible weave relief, visible weave relief")
    assert res_3 == "visible weave relief"
    print("-> TEST-NORM-003 Passed.")

    # ----------------------------------------------------
    # TEST-NORM-004 — Semantic preservation
    # ----------------------------------------------------
    print("TEST-NORM-004: Semantic preservation...")
    res_4 = SegmentNormalizer.normalize_segment("soft diffused daylight. with gentle shadow transitions")
    assert res_4 == "soft diffused daylight with gentle shadow transitions"
    print("-> TEST-NORM-004 Passed.")

    # ----------------------------------------------------
    # TEST-NORM-005 — No creative invention
    # ----------------------------------------------------
    print("TEST-NORM-005: No creative invention...")
    # Normalizer should not add details like color, lighting or camera directions
    raw_segment = "heavy gold zari., thread embroidery"
    res_5 = SegmentNormalizer.normalize_segment(raw_segment)
    assert "luxury" not in res_5.lower()
    assert "cinematic" not in res_5.lower()
    assert res_5 == "heavy gold zari, thread embroidery"
    print("-> TEST-NORM-005 Passed.")

    # ----------------------------------------------------
    # TEST-NORM-006 — Protected segment integrity
    # ----------------------------------------------------
    print("TEST-NORM-006: Protected segment integrity...")
    editor = TargetedPromptEditor()
    existing_prompt = (
        "SUBJECT: a model wearing a Saree.\n"
        "MATERIAL: silk.\n"
        "LIGHTING: soft lighting.\n"
        "CAMERA: 85mm lens.\n"
        "ENVIRONMENT: studio.\n"
        "QUALITY: high detail.\n"
        "FORBIDDEN: none."
    )
    plan = CorrectionPlan(
        correction_id="CORR-NORM-006",
        evaluation_id="EVAL-006",
        shot_id="hero_01",
        failure={"dimension": "material_fidelity", "severity": "HARD"},
        cause={"category": "material"},
        affected_segments=["MATERIAL"],
        preserve_segments=["SUBJECT", "LIGHTING", "CAMERA", "ENVIRONMENT", "QUALITY", "FORBIDDEN"],
        corrections=[
            {"segment": "MATERIAL", "operation": "AUGMENT", "target": "silk", "instruction": "raw silk texture. with weave"}
        ],
        success_criteria=[],
        confidence=0.9
    )
    edit_res = editor.edit(existing_prompt, plan)
    assert edit_res["success"]
    # Check that only MATERIAL is modified
    parsed_mod = editor.parse_segments(edit_res["modified_prompt"])
    parsed_orig = editor.parse_segments(existing_prompt)
    assert "raw silk texture" in parsed_mod["MATERIAL"]
    assert "weave" in parsed_mod["MATERIAL"]
    for seg in plan.preserve_segments:
        assert parsed_mod[seg] == parsed_orig[seg]
    print("-> TEST-NORM-006 Passed.")

    # ----------------------------------------------------
    # TEST-LOCALITY-001 — lexical_correction_locality works
    # ----------------------------------------------------
    print("TEST-LOCALITY-001: lexical_correction_locality works...")
    assert "lexical_correction_locality" in edit_res
    assert edit_res["lexical_correction_locality"] > 0.0
    print("-> TEST-LOCALITY-001 Passed.")

    # ----------------------------------------------------
    # TEST-LOCALITY-002 — Label naming check
    # ----------------------------------------------------
    print("TEST-LOCALITY-002: Label naming check...")
    # Assert result does not contain deprecated "locality" key
    assert "locality" not in edit_res
    print("-> TEST-LOCALITY-002 Passed.")

    # ----------------------------------------------------
    # TEST-LOCALITY-003 — Locality documentation check
    # ----------------------------------------------------
    print("TEST-LOCALITY-003: Locality documentation check...")
    doc = editor.calculate_locality.__doc__
    assert "Lexical Correction Locality" in doc
    assert "does not measure semantic scope" in doc
    assert "semantic_correction_locality" in doc
    print("-> TEST-LOCALITY-003 Passed.")

    # ----------------------------------------------------
    # TEST-ESC-001 — provisional attempt-based escalation still functions
    # ----------------------------------------------------
    print("TEST-ESC-001: Provisional attempt-based escalation still functions...")
    detector = RepeatedFailureDetector(max_attempts=3)
    plan_mock = CorrectionPlan("CORR-MOCK", "EVAL-01", "hero_01", {"severity": "HARD"}, {}, [], [], [], [], 0.9)
    eval_result_1 = {"confidence": 0.85, "dimension_scores": {"material_fidelity": 0.5}}
    detector.record_attempt(plan_mock, eval_result_1)
    
    # Verify escalation check still works
    res_esc = detector.check_escalation("material_fidelity")
    assert res_esc == "PROMPT"
    print("-> TEST-ESC-001 Passed.")

    # ----------------------------------------------------
    # TEST-ESC-002 — Escalation metadata mechanism check
    # ----------------------------------------------------
    print("TEST-ESC-002: Escalation metadata mechanism check...")
    assert res_esc.mechanism == "provisional_attempt_based"
    print("-> TEST-ESC-002 Passed.")

    # ----------------------------------------------------
    # TEST-ESC-003 — Preservation of evaluation confidence
    # ----------------------------------------------------
    print("TEST-ESC-003: Preservation of evaluation confidence...")
    assert res_esc.evaluation_confidence == 0.85
    print("-> TEST-ESC-003 Passed.")

    # ----------------------------------------------------
    # TEST-ESC-004 — Preservation of failure severity
    # ----------------------------------------------------
    print("TEST-ESC-004: Preservation of failure severity...")
    assert res_esc.failure_severity == "HARD"
    print("-> TEST-ESC-004 Passed.")

    # ----------------------------------------------------
    # TEST-ESC-005 — Preservation of improvement delta
    # ----------------------------------------------------
    print("TEST-ESC-005: Preservation of improvement delta...")
    # Record another attempt to check delta
    eval_result_2 = {"confidence": 0.90, "dimension_scores": {"material_fidelity": 0.58}}
    detector.record_attempt(plan_mock, eval_result_2)
    res_esc_2 = detector.check_escalation("material_fidelity")
    # Delta should be eval_result_2 - eval_result_1 = 0.58 - 0.50 = 0.08
    assert abs(res_esc_2.improvement_delta - 0.08) < 0.0001
    print("-> TEST-ESC-005 Passed.")

    print("\n==================================================")
    print("ALL PATCH TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_patch_tests()
