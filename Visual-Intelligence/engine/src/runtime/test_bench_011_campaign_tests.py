import sys
from campaign_system import (
    CampaignCreativeSystem, CampaignInvariant, ShotFamily, CampaignAsset,
    CampaignAssetMatrix, CampaignReference, CampaignDrift, CampaignCoherenceResult,
    CampaignCorrectionPlan, CampaignOrchestrator, CampaignEvaluationLayer,
    CampaignTolerance, CampaignBaselineSelection
)

def run_campaign_tests():
    print("==================================================")
    print("RUNNING TEST BENCH 011: CAMPAIGN SYSTEM TESTS")
    print("==================================================\n")

    # Common mock creative system and invariants
    creative_system = CampaignCreativeSystem(
        campaign_id="camp_autumn_01",
        visual_language={"style": "editorial realism"},
        lighting_language={"family": "warm daylight", "intensity": "high"},
        camera_language={"sensor": "medium format", "focal_length": "85mm"},
        environment_language={"setting": "stone courtyard"},
        color_language={"palette": "earth tones"},
        material_language={"quality": "authentic weave details"},
        human_language={"model_identity": "Model A"},
        composition_language={"framing": "medium-close"}
    )

    invariants = [
        CampaignInvariant("model_identity", "LOCKED"),
        CampaignInvariant("lighting_family", "GUIDED"),
        CampaignInvariant("color_language", "LOCKED")
    ]

    orchestrator = CampaignOrchestrator("camp_autumn_01", creative_system, invariants)

    # ----------------------------------------------------
    # TEST-CAMP-001 — Campaign DNA Creation
    # ----------------------------------------------------
    print("TEST-CAMP-001: Campaign DNA Creation...")
    dna = creative_system.to_dict()
    assert dna["campaign_id"] == "camp_autumn_01"
    assert dna["human_language"]["model_identity"] == "Model A"
    print("-> TEST-CAMP-001 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-002 — Asset Matrix
    # ----------------------------------------------------
    print("TEST-CAMP-002: Asset Matrix...")
    asset_1 = CampaignAsset("ASSET-01", "HERO", "CRAFTSMANSHIP", "saree_01", ["jewelry_01"], "instagram", "4:5", 10)
    asset_2 = CampaignAsset("ASSET-02", "PRODUCT_DETAIL", "CRAFTSMANSHIP", "saree_01", [], "e-commerce", "1:1", 8)
    orchestrator.add_asset(asset_1)
    orchestrator.add_asset(asset_2)
    matrix = orchestrator.generate_asset_matrix()
    assert len(matrix.assets) == 2
    assert matrix.assets[0].asset_id == "ASSET-01"
    print("-> TEST-CAMP-002 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-003 — Shot Family
    # ----------------------------------------------------
    print("TEST-CAMP-003: Shot Family...")
    family = ShotFamily("HERO", {"focal_length": "85mm"}, {"key_light": "warm"}, {"crop": "waist-up"})
    assert family.name == "HERO"
    assert family.camera_bounds["focal_length"] == "85mm"
    print("-> TEST-CAMP-003 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-004 — Locked Invariant
    # ----------------------------------------------------
    print("TEST-CAMP-004: Locked Invariant...")
    # Change locked model identity -> triggers HARD drift
    observed = {"model_identity": "Model B"}
    drifts = orchestrator.detect_drift(asset_1, observed)
    assert len(drifts) == 1
    assert drifts[0].severity == "HARD"
    assert drifts[0].dimension == "MODEL"
    print("-> TEST-CAMP-004 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-005 — Guided Invariant
    # ----------------------------------------------------
    print("TEST-CAMP-005: Guided Invariant...")
    # Change guided lighting family -> triggers SOFT drift
    observed_guided = {"lighting_family": "cool overcast"}
    drifts_guided = orchestrator.detect_drift(asset_1, observed_guided)
    assert len(drifts_guided) == 1
    assert drifts_guided[0].severity == "SOFT"
    assert drifts_guided[0].dimension == "LIGHTING"
    print("-> TEST-CAMP-005 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-006 — Controlled Variation
    # ----------------------------------------------------
    print("TEST-CAMP-006: Controlled Variation...")
    # Assets may vary in composition/aspect ratio without drifting
    observed_varied = {"model_identity": "Model A", "lighting_family": "warm daylight", "color_palette": "earth tones"}
    drifts_varied = orchestrator.detect_drift(asset_2, observed_varied)
    assert len(drifts_varied) == 0  # No drift on allowed variables
    eval_res = CampaignCoherenceResult(shot_quality=9.2, campaign_coherence=9.8)
    assert eval_res.campaign_coherence > 9.0
    print("-> TEST-CAMP-006 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-007 — Campaign Drift
    # ----------------------------------------------------
    print("TEST-CAMP-007: Campaign Drift...")
    # An inconsistent color triggers drift
    observed_color = {"color_palette": "neon green"}
    drifts_color = orchestrator.detect_drift(asset_1, observed_color)
    assert len(drifts_color) == 1
    assert drifts_color[0].dimension == "COLOR"
    assert drifts_color[0].severity == "HARD"
    print("-> TEST-CAMP-007 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-008 — Local vs Global Failure
    # ----------------------------------------------------
    print("TEST-CAMP-008: Local vs Global Failure...")
    # Single asset drift = local
    drift_local = [CampaignDrift("ASSET-01", "LIGHTING", "warm daylight", "cool overcast", "SOFT", 0.90, "DRIFT")]
    plan_local = orchestrator.determine_correction_strategy(drift_local)
    assert plan_local.strategy == "CORRECT"

    # Multi-asset drift = global
    drift_global = [
        CampaignDrift("ASSET-01", "MODEL", "Model A", "Model B", "HARD", 0.95, "VIOLATION"),
        CampaignDrift("ASSET-02", "MODEL", "Model A", "Model C", "HARD", 0.95, "VIOLATION")
    ]
    plan_global = orchestrator.determine_correction_strategy(drift_global)
    assert plan_global.strategy == "REBASE"
    print("-> TEST-CAMP-008 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-009 — Campaign Correction
    # ----------------------------------------------------
    print("TEST-CAMP-009: Campaign Correction...")
    # Verified by TEST-CAMP-008 showing single-asset soft drift maps to CORRECT
    assert plan_local.strategy == "CORRECT"
    print("-> TEST-CAMP-009 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-010 — Campaign Rebase
    # ----------------------------------------------------
    print("TEST-CAMP-010: Campaign Rebase...")
    # Verified by TEST-CAMP-008 showing multi-asset hard drift maps to REBASE
    assert plan_global.strategy == "REBASE"
    print("-> TEST-CAMP-010 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-011 — Product Identity
    # ----------------------------------------------------
    print("TEST-CAMP-011: Product Identity...")
    resolved_shot = {
        "material": {"saree_01": "Banarasi Muga Silk"},
        "lighting": {"KeyLight": "warm daylight"},
        "camera": {"lens": "85mm"},
        "environment": {"location": "royal garden"}
    }
    compiled_prompt = orchestrator.compile_shot_prompt(asset_1, resolved_shot)
    # Core Product DNA (Muga Silk) must remain authoritative
    assert "Banarasi Muga Silk" in compiled_prompt
    print("-> TEST-CAMP-011 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-012 — Multi-Format Coherence
    # ----------------------------------------------------
    print("TEST-CAMP-012: Multi-Format Coherence...")
    # Prompt is compiled for target format aspect ratio
    assert "aspect ratio 4:5" in compiled_prompt
    print("-> TEST-CAMP-012 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-013 — Channel Adaptation
    # ----------------------------------------------------
    print("TEST-CAMP-013: Channel Adaptation...")
    # Verticals adapt composition without changing core creative DNA
    composition_9_16 = orchestrator.adapt_composition("9:16", "centered waist-up model stance")
    assert "vertical framing" in composition_9_16
    print("-> TEST-CAMP-013 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-014 — Reference Graph
    # ----------------------------------------------------
    print("TEST-CAMP-014: Reference Graph...")
    # Ancestry reference levels are explicitly modelable
    ref_master = CampaignReference("REF-MASTER", "MASTER_REFERENCE", [])
    ref_camp = CampaignReference("REF-CAMP", "CAMPAIGN_REFERENCE", ["REF-MASTER"])
    ref_family = CampaignReference("REF-FAMILY", "FAMILY_REFERENCE", ["REF-CAMP"])
    ref_shot = CampaignReference("REF-SHOT", "SHOT_REFERENCE", ["REF-FAMILY"])
    
    assert ref_shot.ancestry[0] == "REF-FAMILY"
    assert "REF-CAMP" in ref_family.ancestry
    print("-> TEST-CAMP-014 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-015 — Campaign Provenance
    # ----------------------------------------------------
    print("TEST-CAMP-015: Campaign Provenance...")
    # Trace elements must remain present
    provenance = {
        "campaign_id": orchestrator.campaign_id,
        "dna": creative_system.to_dict(),
        "shot_family": asset_1.shot_family,
        "objective": asset_1.objective,
        "primary_product": asset_1.primary_product,
        "resolved_shot": resolved_shot,
        "prompt": compiled_prompt
    }
    assert provenance["campaign_id"] == "camp_autumn_01"
    assert provenance["shot_family"] == "HERO"
    assert provenance["objective"] == "CRAFTSMANSHIP"
    print("-> TEST-CAMP-015 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-016 — Declarative vs Perceptual Evaluation Boundary
    # ----------------------------------------------------
    print("TEST-CAMP-016: Declarative vs Perceptual Evaluation...")
    layer = CampaignEvaluationLayer(declarative_passed=True, perceptual_passed=False, rule_failures=[], visual_failures=["VISUAL_COHERENCE_FAILURE: lighting mismatch"])
    assert layer.declarative_passed
    assert not layer.perceptual_passed
    assert not layer.get_overall_result()
    assert "visual_failures" in layer.to_dict()
    print("-> TEST-CAMP-016 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-017 — Guided Tolerance Representation
    # ----------------------------------------------------
    print("TEST-CAMP-017: Guided Tolerance Representation...")
    tol = CampaignTolerance(target="warm daylight", allowed_variation="slightly warm", tolerance="medium", importance="high")
    invariant_guided = CampaignInvariant("lighting_family", "GUIDED", tol)
    assert invariant_guided.tolerance.target == "warm daylight"
    assert invariant_guided.tolerance.tolerance == "medium"
    print("-> TEST-CAMP-017 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-018 — Variation vs Drift Classification
    # ----------------------------------------------------
    print("TEST-CAMP-018: Variation vs Drift Classification...")
    # Verify Variable classification
    drifts_v = orchestrator.detect_drift(asset_1, {"composition": "close-up"})
    assert len(drifts_v) == 1
    assert drifts_v[0].classification == "VARIABLE"

    # Verify Guided Variation classification
    drifts_gv = orchestrator.detect_drift(asset_1, {"lighting_family": "slightly warm"})
    assert len(drifts_gv) == 1
    assert drifts_gv[0].classification == "GUIDED_VARIATION"

    # Verify Drift classification
    drifts_dr = orchestrator.detect_drift(asset_1, {"lighting_family": "cool overcast"})
    assert len(drifts_dr) == 1
    assert drifts_dr[0].classification == "DRIFT"

    # Verify Violation classification
    drifts_vi = orchestrator.detect_drift(asset_1, {"model_identity": "Model B"})
    assert len(drifts_vi) == 1
    assert drifts_vi[0].classification == "VIOLATION"
    print("-> TEST-CAMP-018 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-019 — Failure Scope Classification
    # ----------------------------------------------------
    print("TEST-CAMP-019: Failure Scope Classification...")
    # Local failure scope
    plan_local_scope = orchestrator.determine_correction_strategy([
        CampaignDrift("ASSET-01", "LIGHTING", "warm", "cool", "SOFT", 0.90, "DRIFT")
    ])
    assert plan_local_scope.failure_scope == "ASSET_LOCAL"
    assert plan_local_scope.strategy == "CORRECT"

    # Family failure scope
    asset_4 = CampaignAsset("ASSET-04", "HERO", "CRAFTSMANSHIP", "saree_01", [], "e-commerce", "1:1", 8)
    orchestrator.add_asset(asset_4)
    plan_family_scope = orchestrator.determine_correction_strategy([
        CampaignDrift("ASSET-01", "LIGHTING", "warm", "cool", "SOFT", 0.90, "DRIFT"),
        CampaignDrift("ASSET-04", "LIGHTING", "warm", "cool", "SOFT", 0.90, "DRIFT")
    ])
    assert plan_family_scope.failure_scope == "FAMILY_LOCAL"

    # Global failure scope
    asset_3 = CampaignAsset("ASSET-03", "LIFESTYLE", "CRAFTSMANSHIP", "saree_01", [], "e-commerce", "1:1", 8)
    orchestrator.add_asset(asset_3)
    plan_global_scope = orchestrator.determine_correction_strategy([
        CampaignDrift("ASSET-01", "LIGHTING", "warm", "cool", "SOFT", 0.90, "DRIFT"),
        CampaignDrift("ASSET-03", "LIGHTING", "warm", "cool", "SOFT", 0.90, "DRIFT")
    ])
    assert plan_global_scope.failure_scope == "CAMPAIGN_GLOBAL"
    assert plan_global_scope.strategy == "REBASE"

    # Baseline uncertain scope
    plan_uncertain_scope = orchestrator.determine_correction_strategy([
        CampaignDrift("ASSET-01", "LIGHTING", "warm", "cool", "SOFT", 0.90, "DRIFT")
    ], baseline_trust=False)
    assert plan_uncertain_scope.failure_scope == "BASELINE_UNCERTAIN"
    assert plan_uncertain_scope.strategy == "REBASE"
    print("-> TEST-CAMP-019 Passed.")

    # ----------------------------------------------------
    # TEST-CAMP-020 — Baseline Selection Provenance
    # ----------------------------------------------------
    print("TEST-CAMP-020: Baseline Selection Provenance...")
    baseline_asset = orchestrator.select_baseline()
    assert orchestrator.baseline_selection is not None
    assert orchestrator.baseline_selection.baseline_asset_id == baseline_asset.asset_id
    assert orchestrator.baseline_selection.campaign_objective == "CRAFTSMANSHIP"
    assert orchestrator.baseline_selection.selection_reason is not None
    print("-> TEST-CAMP-020 Passed.")

    print("\n==================================================")
    print("ALL CAMPAIGN TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    run_campaign_tests()
