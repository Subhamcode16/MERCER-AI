"""
Phase 27 Multi-Step Integration Workflows Test Suite.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.campaign_studio.workspace import WorkspaceStore
from src.campaign_studio.campaign_workspace import CampaignWorkspaceManager, StudioCampaignStatus
from src.campaign_studio.discovery import AdaptiveDiscoveryEngine
from src.campaign_studio.creative_intelligence import CreativeIntelligenceEngine
from src.campaign_studio.direction_management import DirectionManager
from src.campaign_studio.visual_development import VisualDevelopmentPipeline
from src.campaign_studio.asset_lineage import AssetLineageGraph
from src.campaign_studio.review import StudioReviewEngine
from src.campaign_studio.approval import StudioApprovalBridge, StudioApprovalStatus
from src.campaign_studio.launch import LaunchManager, LaunchState
from src.campaign_studio.outcomes import OutcomesManager
from src.campaign_studio.conflict_resolution import ConflictResolutionEngine, ConflictDomain, DepartmentPosition


def test_workflow_1_end_to_end_campaign_lifecycle():
    # Setup context
    cd_op = OperatorContext(operator_id="op_cd_01", role=OperatorRole.CREATIVE_DIRECTOR, department="Creative Direction")
    
    # 1. Setup workspace
    store = WorkspaceStore()
    store.create_client("cli_01", "Maison Elegance", "Haute Couture")
    store.create_brand("brd_01", "cli_01", "Elegance Atelier", "Quiet Luxury")
    store.create_product("prd_01", "brd_01", "Silk Evening Cape", "Eveningwear")

    # 2. Create campaign
    camp_mgr = CampaignWorkspaceManager()
    camp = camp_mgr.create_campaign("camp_wf1", "cli_01", "brd_01", "Winter Gala 2026", cd_op.operator_id)
    assert camp.version == 1

    # 3. Discovery
    disc_eng = AdaptiveDiscoveryEngine()
    disc_eng.analyze_intake("camp_wf1", {"season": "Winter 2026"})
    questions = disc_eng.get_pending_questions("camp_wf1")
    for q in questions:
        disc_eng.answer_question("camp_wf1", q.question_id, "Luxury VIP Attendees")
    assert len(disc_eng.get_pending_questions("camp_wf1")) == 0

    camp = camp_mgr.transition_status("camp_wf1", StudioCampaignStatus.CREATIVE_INTELLIGENCE, cd_op.operator_id, expected_version=1)

    # 4. Creative Intelligence
    intel_eng = CreativeIntelligenceEngine()
    intel = intel_eng.synthesize_intelligence("camp_wf1", "Elegance Atelier", {})
    assert len(intel["hypotheses"]) >= 2

    camp = camp_mgr.transition_status("camp_wf1", StudioCampaignStatus.DIRECTION_PROPOSALS, cd_op.operator_id, expected_version=2)

    # 5. Direction Proposal & Selection
    dir_mgr = DirectionManager()
    dirs = dir_mgr.generate_candidate_directions("camp_wf1")
    selected_dir = dir_mgr.select_direction("camp_wf1", dirs[0].direction_id)
    assert selected_dir.is_selected

    camp = camp_mgr.transition_status("camp_wf1", StudioCampaignStatus.VISUAL_EXPLORATION, cd_op.operator_id, expected_version=3)

    # 6. Visual Development & Lineage
    vis_pip = VisualDevelopmentPipeline()
    vis_pip.compile_visual_dna("camp_wf1", selected_dir.direction_id)
    drafts = vis_pip.generate_asset_drafts("camp_wf1", selected_dir.direction_id, count=4)
    hero_asset = drafts[0]

    lineage_graph = AssetLineageGraph()
    lineage_graph.build_standard_asset_lineage(
        campaign_id="camp_wf1",
        mission_id="mis_wf1",
        direction_id=selected_dir.direction_id,
        dna_id="dna_wf1",
        prompt_id="prm_wf1",
        model_id="mdl_wf1",
        render_id="rnd_wf1",
        approval_id="app_wf1",
        delivery_id="del_wf1",
        asset_id=hero_asset.asset_id,
    )
    assert lineage_graph.verify_lineage_integrity(hero_asset.asset_id)

    camp = camp_mgr.transition_status("camp_wf1", StudioCampaignStatus.CRITIQUE_AND_REVIEW, cd_op.operator_id, expected_version=4)

    # 7. Review & Critique
    rev_eng = StudioReviewEngine()
    critique = rev_eng.evaluate_asset("camp_wf1", hero_asset.asset_id)
    assert critique.is_passed

    # 8. Formal Human Approval
    app_bridge = StudioApprovalBridge()
    app_req = app_bridge.create_approval_request("camp_wf1", hero_asset.asset_id, cd_op.operator_id, OperatorRole.CREATIVE_DIRECTOR)
    app_bridge.submit_decision(app_req.approval_id, cd_op, StudioApprovalStatus.APPROVED, "Approved for omni-channel release")

    camp = camp_mgr.transition_status("camp_wf1", StudioCampaignStatus.READY_FOR_LAUNCH, cd_op.operator_id, expected_version=5)

    # 9. Staging & Execution Launch
    launch_mgr = LaunchManager()
    launch_mgr.stage_launch("camp_wf1", {"E-commerce Hero": [hero_asset.asset_id]}, [hero_asset.asset_id])
    launched_manifest = launch_mgr.execute_launch("camp_wf1", cd_op)
    assert launched_manifest.state == LaunchState.LAUNCHED

    camp = camp_mgr.transition_status("camp_wf1", StudioCampaignStatus.LAUNCHED, cd_op.operator_id, expected_version=6)

    # 10. Outcomes & Postmortem
    outcomes_mgr = OutcomesManager()
    outcomes_mgr.record_outcomes("camp_wf1", impressions=500000, click_through_rate=0.062)
    postmortems = outcomes_mgr.generate_postmortem("camp_wf1")
    assert len(postmortems) >= 1


def test_workflow_2_epistemic_discovery_interactive_resolution():
    engine = AdaptiveDiscoveryEngine()
    camp_id = "camp_wf2"
    engine.analyze_intake(camp_id, {})
    questions = engine.get_pending_questions(camp_id)
    assert len(questions) == 2

    # Resolve questions one by one
    for q in questions:
        engine.answer_question(camp_id, q.question_id, "Selected option A")
    
    assert len(engine.get_pending_questions(camp_id)) == 0
    items = engine.get_discovery_items(camp_id)
    assert all(i.state.value == "KNOWN" for i in items if i.dimension in {"target_audience", "visual_tone"})


def test_workflow_3_multi_channel_visual_lineage_verification():
    vis = VisualDevelopmentPipeline()
    graph = AssetLineageGraph()
    camp_id = "camp_wf3"
    dir_id = "dir_wf3"

    drafts = vis.generate_asset_drafts(camp_id, dir_id, count=4)
    for d in drafts:
        graph.build_standard_asset_lineage(
            campaign_id=camp_id,
            mission_id=f"mis_{d.asset_id}",
            direction_id=dir_id,
            dna_id="dna_1",
            prompt_id=f"prm_{d.asset_id}",
            model_id="mdl_1",
            render_id=f"rnd_{d.asset_id}",
            approval_id=f"app_{d.asset_id}",
            delivery_id=f"del_{d.asset_id}",
            asset_id=d.asset_id,
        )
        assert graph.verify_lineage_integrity(d.asset_id) is True


def test_workflow_4_workforce_disagreement_arbitration():
    conf_eng = ConflictResolutionEngine()
    camp_id = "camp_wf4"
    pos_cd = DepartmentPosition("Creative Direction", "CREATIVE_DIRECTOR", "Austere", "Luxury prestige", "Lower virality")
    pos_mkt = DepartmentPosition("Performance", "GROWTH_LEAD", "Vibrant", "Higher CTR", "Brand dilution")

    conflict = conf_eng.register_divergence(
        camp_id, ConflictDomain.AESTHETIC_VS_PERFORMANCE, "Color Palette", [pos_cd, pos_mkt], "Hybrid dual grading"
    )
    assert conflict.resolved is False

    conf_eng.resolve_conflict(camp_id, conflict.conflict_id, "Human Director decided on Hybrid dual grading")
    assert conflict.resolved is True


def test_workflow_5_stale_state_optimistic_locking_recovery():
    mgr = CampaignWorkspaceManager()
    camp = mgr.create_campaign("camp_wf5", "cli_1", "brd_1", "Title", "op_1")
    assert camp.version == 1

    # Update 1
    mgr.transition_status("camp_wf5", StudioCampaignStatus.CREATIVE_INTELLIGENCE, "op_1", expected_version=1)
    camp = mgr.get_campaign("camp_wf5")
    assert camp.version == 2

    # Operator tries update with stale version 1
    with pytest.raises(RuntimeError):
        mgr.transition_status("camp_wf5", StudioCampaignStatus.DIRECTION_PROPOSALS, "op_1", expected_version=1)

    # Operator refreshes and uses current version 2
    mgr.transition_status("camp_wf5", StudioCampaignStatus.DIRECTION_PROPOSALS, "op_1", expected_version=2)
    camp = mgr.get_campaign("camp_wf5")
    assert camp.version == 3
    assert camp.status == StudioCampaignStatus.DIRECTION_PROPOSALS
