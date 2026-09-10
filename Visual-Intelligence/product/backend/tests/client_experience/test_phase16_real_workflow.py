"""
Mandatory Real Workflow Benchmark:
ILYREN Creative Studio — NOCAP September Campaign: Client-to-Execution Journey (20 Stages).
"""

import pytest
from src.client_experience.command_center import StudioCommandCenter
from src.client_experience.access_models import HumanRole
from src.studio_operations.studio_models import DeliverableStatus, DeliverableType
from src.creative_workforce.visual_dna import VisualDNAProfile
from src.creative_workforce.collaboration import CreativeArtifact
from src.creative_workforce.organization_models import ContextBinding
from src.client_experience.exceptions import ContextGuardViolationError

def test_nocap_september_campaign_client_to_execution_journey(tmp_path):
    audit_dir = str(tmp_path / "nocap_journey_audit")
    center = StudioCommandCenter(audit_dir=audit_dir)

    # Stage 1 — Client Onboarding: Create NOCAP client workspace
    client_res = center.studio_orchestrator.register_client_engagement("client_nocap", "NOCAP Studio", "Fashion")
    assert client_res["client_id"] == "client_nocap"

    user_owner = center.register_user("user_owner_01", "Owner Alice", "alice@nocap.fashion", "client_nocap", HumanRole.CLIENT_OWNER)

    # Stage 2 — Brand Context: Bind NOCAP brand and retrieve safe projections
    brand_res = center.studio_orchestrator.bind_client_brand(
        requesting_client_id="client_nocap",
        brand_id="brand_nocap",
        brand_name="NOCAP",
        visual_dna_summary={"primary_color": "#000000", "aesthetic": "Industrial Streetwear"}
    )
    assert brand_res["brand_id"] == "brand_nocap"

    # Stage 3 — Campaign Request: Client submits September campaign objective
    camp_dto = center.request_campaign(
        user_id="user_owner_01",
        client_id="client_nocap",
        campaign_id="camp_nocap_sept",
        brand_id="brand_nocap",
        title="NOCAP September Fall Drop",
        objective="Drive 30% increase in brand awareness"
    )
    assert camp_dto.campaign_id == "camp_nocap_sept"
    assert camp_dto.status == "ACTIVE"

    # Stage 4 — Workforce Activation: Phase 14 workforce receives objective
    ws_social = center.studio_orchestrator.workstream_manager.create_workstream(
        "client_nocap", "ws_social", "camp_nocap_sept", "client_nocap", "Social Content Workstream"
    )
    assert ws_social.workstream_id == "ws_social"

    # Stage 5 — Production: Creative workforce produces campaign artifact
    d1 = center.studio_orchestrator.deliverable_manager.create_deliverable(
        requesting_client_id="client_nocap",
        deliverable_id="del_nocap_sept_01",
        workstream_id="ws_social",
        campaign_id="camp_nocap_sept",
        client_id="client_nocap",
        title="September Hero Drop Teaser",
        deliverable_type=DeliverableType.SOCIAL_POST,
        content={"caption": "NOCAP September Drop. Zero compromises."}
    )
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.IN_PROGRESS)
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.DRAFT)

    # Stage 6 — Critique: Self-critique generates revision signals
    binding = ContextBinding("client_nocap", "brand_nocap", "camp_nocap_sept", "m01", "t01", "staff_creative_lead")
    artifact = CreativeArtifact("art_sept_01", "SOCIAL_POST", "Teaser", d1.content, binding)
    critique = center.studio_orchestrator.workforce_orchestrator.critique_engine.evaluate_artifact(artifact)
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.CRITIQUE)
    assert critique.critique_id.startswith("crit-")

    # Stage 7 — Revision: Artifact revised within governed limits
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.REVISION)
    assert d1.revision_count == 1

    # Stage 8 — Independent Review: Independent reviewer evaluates candidate
    review = center.studio_orchestrator.workforce_orchestrator.reviewer.review_artifact(artifact)
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.CRITIQUE)
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.REVIEW)
    assert review.is_authoritative is False

    # Stage 9 — Client Review: Client sees safe artifact/review projection
    deliv_dtos = center.list_deliverables("user_owner_01", "client_nocap", "camp_nocap_sept")
    assert len(deliv_dtos) == 1
    assert deliv_dtos[0].status == "REVIEW"

    # Stage 10 — Client Feedback: Client requests structured feedback
    fb_res = center.submit_feedback("user_owner_01", "client_nocap", "fb_sept_01", "del_nocap_sept_01", "PREFERENCE_SIGNAL", "Love the brutalist visual tone.")
    assert fb_res["status"] == "INGESTED"

    # Stage 11 — Final Review: Updated artifact reaches approval readiness
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.APPROVED)
    assert d1.status == DeliverableStatus.APPROVED

    # Stage 12 — Human Approval: Client submits explicit approval via Approval Center
    appr_item = center.studio_orchestrator.submit_deliverable_for_human_approval(
        requesting_client_id="client_nocap",
        approval_id="appr_sept_01",
        campaign_id="camp_nocap_sept",
        workstream_id="ws_social",
        deliverable_id="del_nocap_sept_01",
        proposed_action="Publish Instagram Teaser",
        capability="publish_social_post",
        target_platform="instagram"
    )
    assert appr_item.status == "PENDING"

    # Stage 13 — Authorization: Phase 10 creates the authorization record
    appr_dto = center.submit_approval_decision("user_owner_01", "client_nocap", "appr_sept_01", approved=True)
    assert appr_dto.status == "APPROVED"

    # Stage 14 — Production Readiness: Phase 15 confirms operational readiness
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.READY_FOR_EXECUTION)
    readiness = center.studio_orchestrator.readiness_engine.evaluate_readiness("client_nocap", "client_nocap", "camp_nocap_sept", d1, None, has_approval=True)
    assert readiness.is_ready is True

    # Stage 15 — Controlled Execution: Phase 13 executes draft on provider
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.EXECUTED)
    assert d1.status == DeliverableStatus.EXECUTED

    # Stage 16 — Outcome: External outcome observed
    outcome = center.studio_orchestrator.outcome_engine.record_outcome(
        requesting_client_id="client_nocap",
        outcome_id="out_sept_01",
        client_id="client_nocap",
        campaign_id="camp_nocap_sept",
        deliverable_id="del_nocap_sept_01",
        platform="instagram",
        metrics={"likes": 4200, "impressions": 31000}
    )
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.OBSERVED)
    assert outcome.observation_tag == "UNTRUSTED_EXTERNAL_OBSERVATION"

    # Stage 17 — Client Dashboard: Client sees execution result on dashboard
    dash = center.get_dashboard("user_owner_01", "client_nocap")
    assert dash.client_id == "client_nocap"
    assert dash.overall_health == "HEALTHY"

    # Stage 18 — Learning: Outcome/feedback enters governed learning
    center.studio_orchestrator.deliverable_manager.transition_deliverable("client_nocap", "del_nocap_sept_01", DeliverableStatus.LEARNED)
    assert d1.status == DeliverableStatus.LEARNED

    # Stage 19 — Audit: All interactions and execution events are integrity-verifiable
    assert center.verify_audit_integrity() is True
    assert center.studio_orchestrator.verify_ledger_integrity() is True

    # Stage 20 — Security Assertion: Verify client isolation & zero un-authorized execution
    with pytest.raises(ContextGuardViolationError):
        center.get_dashboard("user_owner_01", "client_other")
