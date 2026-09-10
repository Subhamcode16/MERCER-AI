"""
Phase 14 Real Workflow Benchmark
--------------------------------
"ILYREN Creative Studio — NOCAP September Campaign"
Executes a complete 13-stage end-to-end organizational creative campaign benchmark:
Stage 1: Client Objective ("Create September social campaign for NOCAP")
Stage 2: Workforce Director creates campaign mission & delegates assignments across departments
Stage 3: Intelligence gathers external trend observations (UNTRUSTED_EXTERNAL_OBSERVATION) & extracts Visual DNA
Stage 4: Strategy combines Brand DNA, Trend Intelligence, Historical Learning into Strategy Brief
Stage 5: Creative Direction synthesizes CreativeDirectionBrief v1
Stage 6: Production creates initial campaign draft artifact
Stage 7: Self-Critique evaluates artifact quality & issues revision signals
Stage 8: Revision refines artifact within MAX_REVISIONS = 3 ceiling
Stage 9: Independent Review evaluates final proposal candidate (double-blind)
Stage 10: Human Decision & Approval (Phase 10 HumanAuthorizationBoundary)
Stage 11: Controlled Execution (Phase 13 MockSocialProvider)
Stage 12: Post-Work Learning recorded in Institutional Memory
Stage 13: Governed Improvement experiment benchmarked against baseline
"""

import pytest

from src.creative_workforce import CreativeWorkforceOrchestrator
from src.workflow_gateway import WorkflowService
from src.integration_boundary import IntegrationOutcomeClass

def test_ilyren_creative_studio_nocap_september_campaign_benchmark():
    # Initialize Phase 14 Workforce Orchestrator & Phase 14 Workflow Gateway
    workforce_orch = CreativeWorkforceOrchestrator()
    gateway_service = WorkflowService()

    # Stage 1 — Client Objective
    client_id = "nocap_client"
    brand_id = "nocap_apparel"
    campaign_title = "NOCAP September Social Campaign"
    objective = "Create September social campaign featuring Instagram Reel + Carousel Post"

    # Stage 2 — Workforce Director & Delegation
    plan = workforce_orch.director.formulate_workforce_plan(
        client_id=client_id,
        brand_id=brand_id,
        campaign_title=campaign_title,
        objective=objective,
    )
    assert len(plan.assignments) == 7

    # Stage 3 — Intelligence Gathering (Trends + Visual DNA)
    obs = workforce_orch.trend_engine.collect_observation(
        source_url="https://trends.fashion.wiki/september",
        category="streetwear",
        raw_content="Monochrome editorial compositions with kinetic typography",
    )
    assert obs.trust_status == "UNTRUSTED_EXTERNAL_OBSERVATION"

    vdna = workforce_orch.visual_dna_manager.extract_visual_dna(
        brand_or_concept=brand_id,
        primary_colors=["#000000", "#FFFFFF", "#E50914"],
        typography_styles=["Helvetica Neue", "Inter Bold"],
    )

    # Stage 4 & 5 — Strategy & Creative Direction Synthesis
    cdb = workforce_orch.creative_synthesizer.synthesize_direction(
        campaign_title=campaign_title,
        visual_dna=vdna,
        trend_observations=[obs],
    )
    assert cdb.brief_id.startswith("cdb-")

    # Stage 6 — Creative Production (Visual Designer & Copywriter draft)
    designer_asgn = plan.assignments[3]  # Visual Designer
    binding = designer_asgn.context_binding

    art_v1 = workforce_orch.collaboration.create_artifact(
        title="NOCAP September Reel Draft v1",
        content_type="SHORT_FORM_VIDEO",
        payload={
            "text": "NOCAP Autumn Drops - High-Contrast Editorial",
            "brief_id": cdb.brief_id,
            "has_unresolved_defects": True,  # Heuristic defect for testing revision loop
        },
        context_binding=binding,
    )
    assert workforce_orch.collaboration.verify_artifact_lineage(art_v1.artifact_id) is True

    # Stage 7 — Self-Critique
    critique_1 = workforce_orch.critique_engine.evaluate_artifact(art_v1)
    assert critique_1.is_authoritative is False

    # Stage 8 — Revision (Bounded loop)
    revised_payload = {
        "text": "NOCAP Autumn Drops - Refined Minimalist Editorial Composition",
        "brief_id": cdb.brief_id,
        "has_unresolved_defects": False,
    }
    art_v2 = workforce_orch.revision_controller.revise_artifact(art_v1, revised_payload)
    assert workforce_orch.revision_controller.get_revision_count(art_v1.artifact_id) == 1

    # Stage 9 — Independent Review (Double-Blind)
    review = workforce_orch.reviewer.review_artifact(art_v2)
    assert review.recommendation == "ACCEPTED"
    assert review.is_authoritative is False

    # Stage 10 — Human Decision & Authorization via Phase 10 Boundary
    wf_req = gateway_service.create_workflow(
        title=campaign_title,
        target_output="Instagram Reel",
        target_platforms=["mock_social"],
        max_budget=300.0,
    )
    wf_id = wf_req.workflow_id

    task_specs = [{"name": "Create Draft Post", "capability": "CREATE_DRAFT", "platform": "mock_social", "role": "VisualDesigner"}]
    plan_gw = gateway_service.generate_execution_plan(wf_id, task_specs)

    app_req = gateway_service.request_approval_for_step(wf_id, "step-1", action_hash="hash-nocap-v2")
    auth_token = gateway_service.approval_service.submit_user_approval(
        request_id=app_req.approval_request_id,
        approver_id="human_creative_lead",
        signature="sig-nocap-v2",
        granted_capability="CREATE_DRAFT",
        resource_scope_path="/mock_social/drafts",
    )
    assert auth_token.authorization_id is not None

    # Stage 11 — Controlled Execution via Phase 13 Sandbox Integration
    outcome = gateway_service.execute_external_step(
        workflow_id=wf_id,
        step_id="step-1",
        auth_record=auth_token,
        provider_name="mock_social",
        operation_name="create_draft",
        parameters={"text": art_v2.payload["text"]},
        idempotency_key="idemp-nocap-sept-v2",
        environment="SANDBOX",
    )
    assert outcome.outcome_class == IntegrationOutcomeClass.SUCCESS

    # Stage 12 — Post-Work Institutional Memory Recording
    mem_record = workforce_orch.memory_store.record_event(
        record_id="mem-nocap-sept",
        event_type="CAMPAIGN_WORKFLOW_COMPLETED",
        context_binding=binding,
        summary="NOCAP September campaign executed cleanly in sandbox.",
        details={"review_id": review.review_id, "external_outcome_id": outcome.request_id},
    )
    assert mem_record.commitment_hash == mem_record.calculate_hash()

    # Stage 13 — Governed Improvement Experiment
    workforce_orch.improvement_engine.propose_candidate_strategy("v1.1", {"critique_threshold": 0.80})
    exp_res = workforce_orch.improvement_engine.benchmark_candidate("v1.1", 0.92)
    assert exp_res.is_adopted is True

    # Audit Ledger Integrity Verification
    assert workforce_orch.ledger.verify_ledger_integrity() is True
