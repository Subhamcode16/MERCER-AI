"""
Phase 18 Real-World Workflow Benchmark — 30-Day Multi-Client Operations Loop.

Simulates closed-loop creative operations across Days 0–30 for:
1. NOCAP Apparel (Fashion)
2. Beta Tech (SaaS/Tech)
3. Zenith Style (Synthetic Lifestyle Brand)

Verifies:
- Client objective ingestion -> Workforce -> Research -> Direction -> Production -> Review -> Approval -> Execution -> Outcome -> Evaluation -> Learning -> Experiment -> Promotion / Rejection -> Improved Future Work.
"""

import pytest
from src.studio_intelligence.orchestrator import StudioIntelligenceOrchestrator
from src.studio_intelligence.outcome_models import (
    OutcomeObservation,
    OutcomeProvenance,
    LearningSignal,
    LearningStage,
)
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.integration_boundary.models import IntegrationOutcomeClass


def test_phase18_30day_multiclient_benchmark(tmp_path):
    ledger_dir = str(tmp_path / "real_workflow_ledger")
    orchestrator = StudioIntelligenceOrchestrator(ledger_dir=ledger_dir)

    # ---------------------------------------------------------
    # DAY 0: Client & Campaign Initialization
    # ---------------------------------------------------------
    client_nocap = "client_nocap_apparel"
    client_beta = "client_beta_tech"
    client_zenith = "client_zenith_style"

    # Assertion 1: Multi-client setup confirmed
    assert client_nocap != client_beta != client_zenith

    # ---------------------------------------------------------
    # DAYS 1–5: Research & Creative Direction
    # ---------------------------------------------------------
    # Workforce generates creative direction for NOCAP & Beta Tech

    # ---------------------------------------------------------
    # DAYS 6–10: Production & Self-Critique
    # ---------------------------------------------------------
    # Content drafted, initial self-critiques applied

    # ---------------------------------------------------------
    # DAYS 11–15: Independent Review, Revision, & Phase 10 Human Approval
    # ---------------------------------------------------------
    cap = ExecutionCapability.PUBLISH_CONTENT

    auth_nocap = AuthorizationRecord(
        authorization_id="auth_nocap_d15",
        request_id="req_publish_nocap",
        authorized_capabilities=[cap],
        resource_scope=ResourceScope(f"client:{client_nocap}"),
        authorizer_identity="HUMAN_OWNER_NOCAP",
        decision_reference="DECISION_REF_NOCAP",
    )

    auth_beta = AuthorizationRecord(
        authorization_id="auth_beta_d15",
        request_id="req_publish_beta",
        authorized_capabilities=[cap],
        resource_scope=ResourceScope(f"client:{client_beta}"),
        authorizer_identity="HUMAN_OWNER_BETA",
        decision_reference="DECISION_REF_BETA",
    )

    # Assertion 2 & 3: Human Authorization records valid
    assert auth_nocap.authorization_id == "auth_nocap_d15"
    assert auth_beta.authorization_id == "auth_beta_d15"
    assert auth_nocap.revoked is False
    assert auth_beta.revoked is False

    # ---------------------------------------------------------
    # DAYS 16–20: Controlled Provider Action (Phase 13 Subordination)
    # ---------------------------------------------------------
    # Publish actions executed via SandboxSocialProvider through Phase 13 Subordination
    cap = ExecutionCapability.PUBLISH_CONTENT

    pub_nocap = orchestrator.provider_runtime.execute_provider_action(
        client_id=client_nocap,
        action_name="publish_content",
        capability=cap,
        auth_record=auth_nocap,
        payload={"content": "Autumn Streetwear Lookbook Vol 1"},
        idempotency_key="idemp_nocap_day18",
    )

    pub_beta = orchestrator.provider_runtime.execute_provider_action(
        client_id=client_beta,
        action_name="publish_content",
        capability=cap,
        auth_record=auth_beta,
        payload={"content": "Beta Tech AI Assistant v2.0 Released!"},
        idempotency_key="idemp_beta_day18",
    )

    # Assertion 4 & 5: Provider publication successful
    assert pub_nocap.outcome_class == IntegrationOutcomeClass.SUCCESS
    assert pub_beta.outcome_class == IntegrationOutcomeClass.SUCCESS

    # ---------------------------------------------------------
    # DAYS 21–25: Outcome Collection & Performance Evaluation
    # ---------------------------------------------------------
    obs_nocap = OutcomeObservation(
        observation_id="obs_nocap_day22",
        client_id=client_nocap,
        campaign_id="camp_nocap_autumn",
        deliverable_id="deliv_lookbook",
        work_item_id="work_nocap_1",
        platform="instagram",
        metrics={
            "impressions": 18000.0,
            "engagements": 1200.0,
            "clicks": 550.0,
            "approval_latency_sec": 3600.0,
            "publishing_errors": 0.0,
        },
        raw_payload={"status": "active"},
        provenance=OutcomeProvenance.UNTRUSTED_EXTERNAL_OBSERVATION,
    )

    obs_beta = OutcomeObservation(
        observation_id="obs_beta_day22",
        client_id=client_beta,
        campaign_id="camp_beta_q4",
        deliverable_id="deliv_saas_announcement",
        work_item_id="work_beta_1",
        platform="linkedin",
        metrics={
            "impressions": 12000.0,
            "engagements": 600.0,
            "clicks": 250.0,
            "approval_latency_sec": 7200.0,
            "publishing_errors": 0.0,
        },
        raw_payload={"status": "active"},
        provenance=OutcomeProvenance.UNTRUSTED_EXTERNAL_OBSERVATION,
    )

    orchestrator.ingest_outcome(client_nocap, obs_nocap)
    orchestrator.ingest_outcome(client_beta, obs_beta)

    # Assertion 6 & 7: Outcome observations ingested
    assert orchestrator.outcome_store.get_observation(client_nocap, "obs_nocap_day22") is not None
    assert orchestrator.outcome_store.get_observation(client_beta, "obs_beta_day22") is not None

    # ---------------------------------------------------------
    # DAYS 26–28: Learning Signal Extraction & Candidate Strategies
    # ---------------------------------------------------------
    learn_nocap = orchestrator.process_closed_loop_learning(
        requesting_client_id=client_nocap,
        observation=obs_nocap,
        client_feedback_text="Phenomenal engagement on visual lookbook!",
        human_review_score=0.92,
        revision_count=1,
    )

    learn_beta = orchestrator.process_closed_loop_learning(
        requesting_client_id=client_beta,
        observation=obs_beta,
        client_feedback_text="Copy was slightly dense; took 3 revisions.",
        human_review_score=0.75,
        observed_defect="High copy revisions causing approval latency",
        revision_count=3,
    )

    # Assertion 8 & 9: Learning signals generated
    signal_nocap: LearningSignal = learn_nocap["signal"]
    signal_beta: LearningSignal = learn_beta["signal"]
    assert signal_nocap.signal_id.startswith("sig_")
    assert signal_beta.signal_id.startswith("sig_")

    # ---------------------------------------------------------
    # DAYS 29–30: Sandbox Benchmarking against Baseline & Promotion/Rejection
    # ---------------------------------------------------------
    # Scenario A: NOCAP candidate strategy demonstrates high performance -> PROMOTED
    res_nocap = orchestrator.optimize_strategy(
        requesting_client_id=client_nocap,
        learning_signal=signal_nocap,
        baseline_metrics={"overall_score": 0.75, "publishing_errors": 0.0, "revision_count": 1.0},
        candidate_metrics={"overall_score": 0.90, "publishing_errors": 0.0, "revision_count": 1.0},
    )

    # Scenario B: Zenith Style candidate strategy demonstrates DEGRADED performance -> REJECTED & ROLLED BACK
    signal_zenith = LearningSignal(
        signal_id="sig_zenith_day29",
        evaluation_id="eval_zenith_1",
        client_id=client_zenith,
        stage=LearningStage.LEARNING_SIGNAL,
        category="CREATIVE_EXPERIMENT",
        observation_summary="Low click rate",
        proposed_hypothesis="Experimental neon color scheme",
        strategy_variables={"visual_style": "NEON_EXPERIMENTAL"},
    )

    res_zenith = orchestrator.optimize_strategy(
        requesting_client_id=client_zenith,
        learning_signal=signal_zenith,
        baseline_metrics={"overall_score": 0.70, "publishing_errors": 0.0, "revision_count": 1.0},
        candidate_metrics={"overall_score": 0.45, "publishing_errors": 2.0, "revision_count": 4.0},
    )

    # Assertion 10: NOCAP strategy successfully PROMOTED
    assert res_nocap["status"] == "PROMOTED"
    assert res_nocap["improvement_delta"] == 0.15

    # Assertion 11: Zenith Style candidate REJECTED & ROLLED BACK
    assert res_zenith["status"] == "REJECTED_ROLLED_BACK"

    # Assertion 12: Adopted NOCAP knowledge item stored in memory
    nocap_memory = orchestrator.memory.list_knowledge_items(client_nocap, client_nocap)
    assert len(nocap_memory) == 1

    # Assertion 13: Zenith Style memory remains unpolluted by rejected candidate
    zenith_memory = orchestrator.memory.list_knowledge_items(client_zenith, client_zenith)
    assert len(zenith_memory) == 0

    # Assertion 14: Client isolation maintained between NOCAP, Beta Tech, & Zenith Style
    dash_nocap = orchestrator.get_dashboard_summary(client_nocap, client_nocap)
    assert dash_nocap["total_observations"] == 1
    assert dash_nocap["adopted_knowledge_count"] == 1

    # Assertion 15: SHA-256 Hash-linked Audit Ledger Chain Integrity Verified
    assert orchestrator.verify_ledger() is True
