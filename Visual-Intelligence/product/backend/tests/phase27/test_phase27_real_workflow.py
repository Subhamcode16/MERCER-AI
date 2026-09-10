"""
Phase 27 Canonical 21-Step Real Workflow Product Demonstration Benchmark.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.campaign_studio.workspace import WorkspaceStore
from src.campaign_studio.campaign_workspace import CampaignWorkspaceManager, StudioCampaignStatus
from src.campaign_studio.discovery import AdaptiveDiscoveryEngine, DiscoveryEpistemicState
from src.campaign_studio.creative_intelligence import CreativeIntelligenceEngine
from src.campaign_studio.direction_management import DirectionManager
from src.campaign_studio.visual_development import VisualDevelopmentPipeline
from src.campaign_studio.asset_lineage import AssetLineageGraph
from src.campaign_studio.review import StudioReviewEngine
from src.campaign_studio.approval import StudioApprovalBridge, StudioApprovalStatus
from src.campaign_studio.launch import LaunchManager, LaunchState
from src.campaign_studio.outcomes import OutcomesManager
from src.campaign_studio.campaign_memory import CampaignMemoryStore
from src.campaign_studio.state_projection import StateProjectionEngine


def test_21_step_canonical_studio_demonstration_benchmark():
    # Step 1: Authenticate Studio Creative Director & Operator Context
    cd_operator = OperatorContext(
        operator_id="op_director_helena",
        role=OperatorRole.CREATIVE_DIRECTOR,
        department="Creative Direction",
    )
    assert cd_operator.role == OperatorRole.CREATIVE_DIRECTOR

    # Step 2: Create Luxury Client ("Aethelgard Holdings") & Brand ("Aethelgard Paris")
    store = WorkspaceStore()
    client = store.create_client("cli_aethelgard", "Aethelgard Holdings", "Haute Couture & Heritage Luxury")
    brand = store.create_brand("brd_aethelgard_paris", client.client_id, "Aethelgard Paris", "Architectural Minimalist Luxury")
    assert brand.brand_id == "brd_aethelgard_paris"

    # Step 3: Register Flagship Product ("Architectural Wool Trench Coat")
    product = store.create_product(
        "prd_monolith_coat",
        brand.brand_id,
        "Architectural Wool Trench Coat",
        "Outerwear / Tailoring",
        ["#1A1A1A", "#E5E0D8", "#8A7D70"],
    )
    assert product.product_id == "prd_monolith_coat"

    # Step 4: Create Campaign Session ("Autumn/Winter 2026 Haute Couture Launch")
    camp_mgr = CampaignWorkspaceManager()
    camp = camp_mgr.create_campaign(
        campaign_id="camp_aw26_couture",
        client_id=client.client_id,
        brand_id=brand.brand_id,
        title="Autumn/Winter 2026 Haute Couture Launch",
        created_by=cd_operator.operator_id,
        description="Flagship seasonal campaign establishing sculptural tailoring identity.",
    )
    assert camp.status == StudioCampaignStatus.INTAKE_DISCOVERY
    assert camp.version == 1

    # Step 5: Intake Incomplete Brief (Trigger Epistemic Missing State)
    disc_eng = AdaptiveDiscoveryEngine()
    items = disc_eng.analyze_intake(camp.campaign_id, {"season": "Autumn/Winter 2026"})
    item_map = {i.dimension: i for i in items}
    assert item_map["season"].state == DiscoveryEpistemicState.KNOWN
    assert item_map["target_audience"].state == DiscoveryEpistemicState.MISSING

    # Step 6: Query Consequential Discovery Questions
    pending_q = disc_eng.get_pending_questions(camp.campaign_id)
    assert len(pending_q) >= 2

    # Step 7: Operator Answers Epistemic Discovery Questions
    for q in pending_q:
        if q.dimension == "target_audience":
            disc_eng.answer_question(camp.campaign_id, q.question_id, "Affluent Minimalists & Design Patrons")
        elif q.dimension == "visual_tone":
            disc_eng.answer_question(camp.campaign_id, q.question_id, "Architectural High-Contrast Editorial")

    # Step 8: Verify Epistemic State Transition to KNOWN
    resolved_items = disc_eng.get_discovery_items(camp.campaign_id)
    for ri in resolved_items:
        if ri.dimension in {"target_audience", "visual_tone"}:
            assert ri.state == DiscoveryEpistemicState.KNOWN

    # Step 9: Transition Campaign Status to CREATIVE_INTELLIGENCE (Version 1 -> 2)
    camp = camp_mgr.transition_status(camp.campaign_id, StudioCampaignStatus.CREATIVE_INTELLIGENCE, cd_operator.operator_id, expected_version=1)
    assert camp.version == 2

    # Step 10: Synthesize Market Signals, Cultural Shifts & Audience Tensions
    intel_eng = CreativeIntelligenceEngine()
    intel = intel_eng.synthesize_intelligence(camp.campaign_id, "Aethelgard Paris", {})
    assert len(intel["market_signals"]) >= 2
    assert len(intel["hypotheses"]) >= 2

    # Step 11: Generate Multi-Candidate Creative Direction Cards
    camp = camp_mgr.transition_status(camp.campaign_id, StudioCampaignStatus.DIRECTION_PROPOSALS, cd_operator.operator_id, expected_version=2)
    dir_mgr = DirectionManager()
    directions = dir_mgr.generate_candidate_directions(camp.campaign_id)
    assert len(directions) == 3

    # Step 12: Operator Refines & Selects Direction ("Monolithic Elegance")
    target_dir = directions[0]
    dir_mgr.refine_direction(camp.campaign_id, target_dir.direction_id, "Deepen raking shadows on concrete textures")
    selected_dir = dir_mgr.select_direction(camp.campaign_id, target_dir.direction_id)
    assert selected_dir.is_selected

    # Step 13: Transition Campaign Status to VISUAL_EXPLORATION (Version 3 -> 4)
    camp = camp_mgr.transition_status(camp.campaign_id, StudioCampaignStatus.VISUAL_EXPLORATION, cd_operator.operator_id, expected_version=3)
    assert camp.version == 4

    # Step 14: Compile Visual DNA Style Locks & Generate Multi-Channel Renders (1:1, 4:5, 9:16, 16:9)
    vis_pip = VisualDevelopmentPipeline()
    dna_tokens = vis_pip.compile_visual_dna(camp.campaign_id, selected_dir.direction_id)
    drafts = vis_pip.generate_asset_drafts(camp.campaign_id, selected_dir.direction_id, count=4)
    assert len(drafts) == 4
    hero_draft = next(d for d in drafts if d.is_hero)
    assert hero_draft.aspect_ratio.value == "16:9"

    # Step 15: Construct 9-Node Cryptographic Lineage Graph
    lineage_graph = AssetLineageGraph()
    lineage_nodes = lineage_graph.build_standard_asset_lineage(
        campaign_id=camp.campaign_id,
        mission_id="mis_aw26_01",
        direction_id=selected_dir.direction_id,
        dna_id="dna_aw26_01",
        prompt_id="prm_aw26_01",
        model_id="mdl_imagen3_01",
        render_id="rnd_aw26_01",
        approval_id="app_aw26_01",
        delivery_id="del_aw26_01",
        asset_id=hero_draft.asset_id,
    )
    assert len(lineage_nodes) == 9

    # Step 16: Verify Tamper-Evident SHA-256 Lineage Chain-of-Custody
    is_valid = lineage_graph.verify_lineage_integrity(hero_draft.asset_id)
    assert is_valid is True

    # Step 17: Execute 5-Dimensional Studio Review & Critique Engine
    camp = camp_mgr.transition_status(camp.campaign_id, StudioCampaignStatus.CRITIQUE_AND_REVIEW, cd_operator.operator_id, expected_version=4)
    rev_eng = StudioReviewEngine()
    critique = rev_eng.evaluate_asset(camp.campaign_id, hero_draft.asset_id)
    assert critique.is_passed is True
    assert critique.overall_score >= 0.85

    # Step 18: Submit Formal Signed Human Approval (CREATIVE_DIRECTOR Sign-off)
    app_bridge = StudioApprovalBridge()
    app_req = app_bridge.create_approval_request(camp.campaign_id, hero_draft.asset_id, cd_operator.operator_id, OperatorRole.CREATIVE_DIRECTOR)
    signed_approval = app_bridge.submit_decision(
        app_req.approval_id,
        cd_operator,
        StudioApprovalStatus.APPROVED,
        "Color calibration, raking lighting, and silhouette verified against brand guidelines.",
    )
    assert signed_approval.status == StudioApprovalStatus.APPROVED

    # Step 19: Stage Multi-Channel Launch Packages & Verify Pre-Launch Checklist
    camp = camp_mgr.transition_status(camp.campaign_id, StudioCampaignStatus.READY_FOR_LAUNCH, cd_operator.operator_id, expected_version=5)
    launch_mgr = LaunchManager()
    manifest = launch_mgr.stage_launch(
        camp.campaign_id,
        {"E-commerce Hero": [hero_draft.asset_id], "Lookbook": [d.asset_id for d in drafts if not d.is_hero]},
        verified_assets=[d.asset_id for d in drafts],
    )
    assert manifest.state == LaunchState.STAGED

    # Step 20: Execute Final Campaign Launch (Version 6 -> 7)
    launched = launch_mgr.execute_launch(camp.campaign_id, cd_operator)
    assert launched.state == LaunchState.LAUNCHED
    camp = camp_mgr.transition_status(camp.campaign_id, StudioCampaignStatus.LAUNCHED, cd_operator.operator_id, expected_version=6)
    assert camp.version == 7
    assert camp.status == StudioCampaignStatus.LAUNCHED

    # Step 21: Record Post-Launch Outcomes & Generate Workforce Advisory Postmortem Insights
    outcomes_mgr = OutcomesManager()
    metrics = outcomes_mgr.record_outcomes(camp.campaign_id, impressions=1250000, click_through_rate=0.068, conversion_lift_percent=31.4)
    assert metrics.impressions == 1250000
    assert "Correlational - Not Causal Proof" in metrics.attribution_model

    postmortems = outcomes_mgr.generate_postmortem(camp.campaign_id)
    assert len(postmortems) >= 1

    # Persist postmortem insight into Brand Memory Store
    mem_store = CampaignMemoryStore()
    mem_store.add_memory(
        client_id=client.client_id,
        brand_id=brand.brand_id,
        category="postmortem_learning",
        title=postmortems[0].key_learning,
        content=postmortems[0].advisory_recommendation,
    )
    brand_memories = mem_store.get_brand_memories(brand.brand_id)
    assert len(brand_memories) == 1

    # Verify State Projection
    proj_eng = StateProjectionEngine()
    overview = proj_eng.project_campaign_overview(
        campaign_id=camp.campaign_id,
        client_name=client.name,
        brand_name=brand.name,
        title=camp.title,
        status=camp.status.value,
        version=camp.version,
        asset_count=len(drafts),
        pending_approvals_count=0,
    )
    assert overview["status"] == "LAUNCHED"
    assert overview["version"] == 7
