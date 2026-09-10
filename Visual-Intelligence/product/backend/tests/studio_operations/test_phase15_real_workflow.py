"""
Mandatory Real Workflow Benchmark:
ILYREN Creative Studio — NOCAP 30-Day Operating Cycle (25 Stages).
"""

import pytest
from src.studio_operations.orchestrator import StudioOperationsOrchestrator
from src.studio_operations.studio_models import DeliverableStatus, CampaignStatus, DeliverableType
from src.studio_operations.exceptions import ClientContextViolation
from src.creative_workforce.visual_dna import VisualDNAProfile
from src.creative_workforce.collaboration import CreativeArtifact
from src.creative_workforce.organization_models import ContextBinding

def test_nocap_30day_operating_cycle_benchmark(tmp_path):
    ledger_dir = str(tmp_path / "nocap_30day_ledger")
    orch = StudioOperationsOrchestrator(ledger_dir=ledger_dir)

    # Stage 1: Establish client operating context
    client = orch.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    assert client["client_id"] == "client_nocap"

    # Stage 2: Load NOCAP brand/Visual DNA
    brand = orch.bind_client_brand(
        requesting_client_id="client_nocap",
        brand_id="brand_nocap",
        brand_name="NOCAP",
        visual_dna_summary={"primary_color": "#000000", "aesthetic": "Industrial Streetwear"}
    )
    assert brand["brand_id"] == "brand_nocap"

    # Stage 3: Initialize 30-day campaign
    campaign = orch.launch_campaign(
        requesting_client_id="client_nocap",
        campaign_id="camp_nocap_30day",
        brand_id="brand_nocap",
        title="NOCAP Fall 30-Day Campaign",
        objective="Drive 25% increase in streetwear engagement"
    )
    assert campaign["status"] == "ACTIVE"

    # Stage 4: Generate recurring workstreams
    ws_social = orch.workstream_manager.create_workstream("client_nocap", "ws_social", "camp_nocap_30day", "client_nocap", "Social Content Workstream")
    ws_design = orch.workstream_manager.create_workstream("client_nocap", "ws_design", "camp_nocap_30day", "client_nocap", "Visual Design Workstream")
    assert ws_social.workstream_id == "ws_social"
    assert ws_design.workstream_id == "ws_design"

    # Stage 5: Perform trend intelligence intake
    trend_obs = orch.workforce_orchestrator.trend_engine.collect_observation(
        source_url="https://fashion.example/cyber-streetwear",
        category="fashion_web",
        raw_content="Industrial cyber aesthetics trending in Q3 fashion",
        extracted_patterns=["Cyber Industrial"]
    )
    assert trend_obs.trust_status == "UNTRUSTED_EXTERNAL_OBSERVATION"

    # Stage 6: Create weekly creative direction
    dna_profile = orch.workforce_orchestrator.visual_dna_manager.extract_visual_dna("NOCAP", ["#000000", "#FFFFFF"], ["Sans-Serif Bold"])
    direction = orch.workforce_orchestrator.creative_synthesizer.synthesize_direction(
        campaign_title="NOCAP Fall Drop",
        visual_dna=dna_profile,
        trend_observations=[trend_obs]
    )
    assert direction.brief_id.startswith("cdb-")

    # Stage 7: Generate multiple content concepts
    d1 = orch.deliverable_manager.create_deliverable(
        requesting_client_id="client_nocap",
        deliverable_id="del_nocap_001",
        workstream_id="ws_social",
        campaign_id="camp_nocap_30day",
        client_id="client_nocap",
        title="NOCAP Fall Drop Teaser 1",
        deliverable_type=DeliverableType.SOCIAL_POST,
        content={"caption": "NOCAP Fall 2026. No compromises."}
    )
    assert d1.status == DeliverableStatus.PLANNED

    # Stage 8: Produce campaign assets
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.IN_PROGRESS)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.DRAFT)

    # Stage 9: Run self-critique
    binding = ContextBinding("client_nocap", "brand_nocap", "camp_nocap_30day", "m01", "t01", "staff_creative_lead")
    artifact = CreativeArtifact("art_001", "SOCIAL_POST", "Teaser", d1.content, binding)
    critique = orch.workforce_orchestrator.critique_engine.evaluate_artifact(artifact)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.CRITIQUE)
    assert critique.critique_id.startswith("crit-")

    # Stage 10: Run independent review
    review = orch.workforce_orchestrator.reviewer.review_artifact(artifact)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.REVIEW)
    assert review.is_authoritative is False

    # Stage 11: Execute bounded revisions
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.REVISION)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.CRITIQUE)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.REVIEW)
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.APPROVED)
    assert d1.revision_count == 1

    # Stage 12: Submit approval package
    approval = orch.submit_deliverable_for_human_approval(
        requesting_client_id="client_nocap",
        approval_id="appr_nocap_001",
        campaign_id="camp_nocap_30day",
        workstream_id="ws_social",
        deliverable_id="del_nocap_001",
        proposed_action="Publish Instagram Teaser Post",
        capability="publish_social_post",
        target_platform="instagram"
    )
    assert approval.status == "PENDING"

    # Stage 13: Obtain explicit human authorization
    approved_item = orch.record_human_approval_decision(
        requesting_client_id="client_nocap",
        approval_id="appr_nocap_001",
        approved=True,
        authorizer_id="user_brand_director"
    )
    assert approved_item.status == "APPROVED"
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.READY_FOR_EXECUTION)

    # Stage 14: Execute through Phase 13 sandbox/provider boundary
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.EXECUTED)
    assert d1.status == DeliverableStatus.EXECUTED

    # Stage 15: Collect simulated platform outcomes
    outcome = orch.outcome_engine.record_outcome(
        requesting_client_id="client_nocap",
        outcome_id="out_nocap_001",
        client_id="client_nocap",
        campaign_id="camp_nocap_30day",
        deliverable_id="del_nocap_001",
        platform="instagram",
        metrics={"impressions": 25000, "likes": 3400, "comments": 420},
        raw_feedback="Outstanding brand alignment."
    )
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.OBSERVED)
    assert outcome.observation_tag == "UNTRUSTED_EXTERNAL_OBSERVATION"

    # Stage 16: Evaluate performance
    metrics = orch.performance_engine.calculate_metrics(
        requesting_client_id="client_nocap",
        target_client_id="client_nocap",
        deliverables=[d1],
        approvals=[approved_item]
    )
    assert metrics.total_deliverables == 1
    assert metrics.execution_success_rate == 1.0

    # Stage 17: Generate learning signals
    orch.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_001", DeliverableStatus.LEARNED)
    assert d1.status == DeliverableStatus.LEARNED

    # Stage 18: Run governed improvement experiment
    strat = orch.workforce_orchestrator.improvement_engine.propose_candidate_strategy("1.1.0", {"max_revisions": 3})
    assert strat.version == "1.1.0"

    # Stage 19: Benchmark candidate strategy
    res = orch.workforce_orchestrator.improvement_engine.benchmark_candidate("1.1.0", 0.90)
    assert res.is_adopted is True

    # Stage 20: Prepare next weekly cycle
    cycle = orch.cycle_manager.start_cycle("client_nocap", "cyc_week2", "camp_nocap_30day", "client_nocap", cycle_number=2)
    assert cycle.status == "IN_PROGRESS"

    # Stage 21: Simulate interruption
    continuity_plan = orch.evaluate_continuity("client_nocap", "camp_nocap_30day")
    assert continuity_plan.status == "VALID"

    # Stage 22: Resume from checkpoint
    orch.cycle_manager.complete_cycle("client_nocap", "cyc_week2")
    assert cycle.status == "COMPLETED"

    # Stage 23: Verify client isolation
    with pytest.raises(ClientContextViolation):
        orch.evaluate_continuity(requesting_client_id="client_other", campaign_id="camp_nocap_30day")

    # Stage 24: Verify audit integrity
    assert orch.verify_ledger_integrity() is True

    # Stage 25: Complete 30-day operational report
    health_report = orch.get_studio_health("client_nocap")
    assert health_report.overall_health == "HEALTHY"
