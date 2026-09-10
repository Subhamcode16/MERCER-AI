"""
Phase 28 Canonical 21-Step Real Workflow Learning Operating Loop Demonstration Benchmark.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.creative_learning.decision_ledger import DecisionLedger, DecisionType, DecisionContextSnapshot, DecisionAlternative
from src.creative_learning.outcome_ingestion import OutcomeIngestionPipeline
from src.creative_learning.outcome_normalization import OutcomeNormalizer
from src.creative_learning.outcome_linkage import OutcomeLinkageGraph
from src.creative_learning.attribution import AttributionEngine, EvidenceCausalStatus
from src.creative_learning.learning_signals import LearningSignalGenerator, LearningSignalType
from src.creative_learning.hypotheses import LearningHypothesisStore, HypothesisScope
from src.creative_learning.counterfactuals import CounterfactualEngine, CounterfactualState
from src.creative_learning.experiments import ExperimentRegistry, ExperimentStatus
from src.creative_learning.calibration import CalibrationTracker
from src.creative_learning.promotion import KnowledgePromotionEngine, PromotionLifecycleState
from src.creative_learning.contradiction import ContradictionHandler
from src.creative_learning.pattern_discovery import CreativePatternMiner
from src.creative_learning.skill_improvement import SkillImprovementEngine
from src.creative_learning.worker_learning import WorkerPerformanceEvaluator
from src.creative_learning.visual_learning import VisualPatternMiner
from src.creative_learning.learning_memory import GovernedKnowledgeStore
from src.creative_learning.learning_observability import LearningTelemetryEmitter
from src.creative_learning.learning_governance import LearningGovernanceEngine


def test_21_step_canonical_learning_operating_loop_benchmark():
    # Step 1: Authenticate Studio Creative Director & Initialize Operator Context
    cd_operator = OperatorContext(
        operator_id="op_director_helena",
        role=OperatorRole.CREATIVE_DIRECTOR,
        tenant_id="tenant_aethelgard",
        client_id="cli_aethelgard",
        department="Creative Direction",
    )
    assert cd_operator.role == OperatorRole.CREATIVE_DIRECTOR

    # Step 2: Initialize Client & Brand Context Snapshot
    snapshot = DecisionContextSnapshot(
        snapshot_id="snp_aw26_couture",
        tenant_id=cd_operator.tenant_id,
        client_id=cd_operator.client_id,
        brand_id="brd_aethelgard_paris",
        campaign_id="camp_aw26_launch",
        brand_guideline_version="v2.4_monolith",
    )

    # Step 3: Record Material Campaign Decision 1 (Audience Selection)
    ledger = DecisionLedger()
    dec1 = ledger.record_decision(
        campaign_id="camp_aw26_launch",
        decision_type=DecisionType.AUDIENCE_SELECTION,
        actor_id=cd_operator.operator_id,
        context_snapshot=snapshot,
        decision="Target: Affluent Minimalists & Design Patrons",
        rationale="Maximizes resonance for high-tailoring sculptural silhouettes.",
        confidence=0.92,
        expected_impact="+20% engagement quality",
    )
    assert dec1.decision_version == 1

    # Step 4: Record Material Campaign Decision 2 (Visual Direction)
    alt_cyber = DecisionAlternative("alt_cyber", "Cyber Neon Cyberpunk", "Incompatible with brand heritage", 0.8)
    dec2 = ledger.record_decision(
        campaign_id="camp_aw26_launch",
        decision_type=DecisionType.VISUAL_DIRECTION,
        actor_id=cd_operator.operator_id,
        context_snapshot=snapshot,
        decision="Direction: Monolithic Architectural Stillness",
        rationale="Juxtaposes raw limestone against crisp wool overcoat tailoring.",
        confidence=0.95,
        alternatives=[alt_cyber],
    )
    assert dec2.decision_version == 2
    assert dec2.parent_hash == dec1.record_hash

    # Step 5: Record Material Campaign Decision 3 (Token Lock)
    dec3 = ledger.record_decision(
        campaign_id="camp_aw26_launch",
        decision_type=DecisionType.TOKEN_LOCK,
        actor_id=cd_operator.operator_id,
        context_snapshot=snapshot,
        decision="Token Lock: raking_monolithic_late_sun + dense_creased_wool_gabardine",
        rationale="Emphasizes tactile weave and raking micro-contrast shadow.",
        confidence=0.94,
    )
    assert dec3.decision_version == 3

    # Step 6: Verify Immutable Decision Ledger Cryptographic Hash Chain Integrity
    assert ledger.verify_ledger_integrity("camp_aw26_launch") is True

    # Step 7: Simulate Launch Execution (Asset ID: ast_hero_monolith_01)
    launched_asset_id = "ast_hero_monolith_01"

    # Step 8: Ingest Multi-Channel Telemetry Outcome Feeds
    ingestion = OutcomeIngestionPipeline()
    feed_shopify = ingestion.ingest_feed(
        campaign_id="camp_aw26_launch",
        source_platform="ShopifyStorefront",
        metrics_payload={"impressions": 850000, "clicks": 34000, "conversions": 2720, "avg_dwell_sec": 19.4},
        source_signature="sig_rsa_verified_shopify_9921",
    )
    feed_meta = ingestion.ingest_feed(
        campaign_id="camp_aw26_launch",
        source_platform="MetaAds",
        metrics_payload={"impressions": 1200000, "clicks": 42000, "conversions": 2100},
        source_signature="sig_rsa_verified_meta_4482",
    )
    assert feed_shopify.is_verified is True
    assert feed_meta.is_verified is True

    # Step 9: Verify Feed Provenance Signatures & Reject Poisoned Mock Payloads
    feed_bad = ingestion.ingest_feed("camp_aw26_launch", "MockAttack", {"impressions": 99999999}, "MOCK_INJECTION_FAIL")
    assert feed_bad.is_verified is False

    # Step 10: Normalize Metrics Preserving Source Semantics
    normalizer = OutcomeNormalizer()
    norm_metrics = normalizer.normalize_feed("camp_aw26_launch", "ShopifyStorefront", feed_shopify.metrics_payload)
    metric_map = {m.metric_name: m for m in norm_metrics}
    assert metric_map["IMPRESSIONS"].normalized_value == 850000.0
    assert metric_map["CTR"].normalized_value == 0.04
    assert metric_map["CONVERSION_RATE"].normalized_value == 0.08
    assert metric_map["AVG_DWELL_TIME_SEC"].normalized_value == 19.4

    # Step 11: Link Normalized Outcomes to Exact Immutable Launched Asset Versions
    linkage = OutcomeLinkageGraph()
    link_node = linkage.link_outcome(
        campaign_id="camp_aw26_launch",
        direction_id="dir_monolithic_elegance",
        asset_id=launched_asset_id,
        asset_version=1,
        channel="E-commerce Hero",
        metric_ids=[m.metric_id for m in norm_metrics],
        production_release_version=1,
    )
    assert link_node.asset_id == launched_asset_id

    # Step 12: Execute Multi-Factor Epistemic Attribution Engine & Detect Macro Confounders
    attribution_eng = AttributionEngine()
    attr_assessment = attribution_eng.evaluate_attribution(
        campaign_id="camp_aw26_launch",
        asset_id=launched_asset_id,
        raw_lift=32.4,
        is_controlled_ab_test=False,
    )
    assert attr_assessment.causal_status == EvidenceCausalStatus.CONFOUNDED
    assert len(attr_assessment.detected_confounders) >= 1
    assert "Outcome ≠ Causation" in attr_assessment.epistemic_disclaimer

    # Step 13: Build Counterfactual Tree & Explicitly Preserve COUNTERFACTUAL_UNKNOWN
    cf_engine = CounterfactualEngine()
    cf_tree = cf_engine.build_counterfactual_tree(
        campaign_id="camp_aw26_launch",
        chosen_decision="Monolithic Limestone Setting",
        observed_outcome="CVR: 8.0%, Dwell: 19.4s",
        unselected_alternatives=["Cyber Neon", "Studio Flat White"],
    )
    assert len(cf_tree.alternative_branches) == 2
    assert cf_tree.alternative_branches[0].state == CounterfactualState.COUNTERFACTUAL_UNKNOWN

    # Step 14: Generate Classified Learning Signals
    sig_gen = LearningSignalGenerator()
    cvr_signal = sig_gen.evaluate_signal(
        campaign_id="camp_aw26_launch",
        target_entity="token:raking_monolithic_late_sun",
        observed_metric="CONVERSION_RATE",
        actual_value=0.08,
        baseline_value=0.05,
        sample_size=34000,
    )
    assert cvr_signal.signal_type == LearningSignalType.POSITIVE_SIGNAL
    assert cvr_signal.delta_percentage == 60.0

    # Step 15: Formulate Structured Learning Hypothesis with Known Limitations
    hyp_store = LearningHypothesisStore()
    hyp = hyp_store.create_hypothesis(
        statement="Raking late sun lighting significantly enhances tailored outerwear conversion lift.",
        originating_campaigns=["camp_aw26_launch"],
        supporting_evidence=["Shopify 8.0% CVR across 34k visits (+60% over baseline)."],
        scope=HypothesisScope.BRAND,
        confidence=0.89,
        known_limitations=["Tested during Autumn season; outerwear specific."],
        test_recommendation="Conduct multi-channel A/B test on upcoming Spring Trench launch.",
    )
    assert hyp.status == "PROVISIONAL"

    # Step 16: Register Controlled A/B Validation Experiment in Experiment Registry
    exp_reg = ExperimentRegistry()
    exp = exp_reg.register_experiment(
        campaign_id="camp_aw26_launch",
        hypothesis_id=hyp.hypothesis_id,
        title="Raking Monolith vs Studio Soft Lighting A/B Test",
        variants=[
            {"name": "Variant A (Raking Sun)", "allocation": 50.0, "asset_id": "ast_hero_monolith_01"},
            {"name": "Variant B (Studio Diffuse)", "allocation": 50.0, "asset_id": "ast_hero_diffuse_02"},
        ],
        target_metric="CONVERSION_RATE",
    )
    exp_reg.transition_status(exp.experiment_id, ExperimentStatus.RUNNING)

    # Step 17: Record A/B Test Results & Update Confidence-to-Outcome Calibration Radar
    exp_results = exp_reg.record_results(
        experiment_id=exp.experiment_id,
        results={"Variant A (Raking Sun)": 0.081, "Variant B (Studio Diffuse)": 0.052},
        sample_size=12000,
        p_value=0.008,
    )
    assert exp_results.statistical_significance == 0.992

    cal_tracker = CalibrationTracker()
    for _ in range(65):
        cal_tracker.record_prediction("VISUAL_QUALITY", 0.90, True)
    for _ in range(10):
        cal_tracker.record_prediction("VISUAL_QUALITY", 0.90, False)
    cal_report = cal_tracker.get_calibration_report("VISUAL_QUALITY")
    assert cal_report.total_predictions == 75

    # Step 18: Generate Governed Knowledge Promotion Proposal with Rollback Plan
    prom_engine = KnowledgePromotionEngine()
    proposal = prom_engine.propose_promotion(
        claim="Raking monolithic late sun lighting provides superior texture definition and conversion lift for luxury outerwear.",
        scope=HypothesisScope.BRAND,
        supporting_evidence=["Autumn Gala CVR 8.0%", "Controlled A/B test p=0.008"],
        affected_knowledge_objects=["Preset:Outerwear_Tailoring_DNA"],
        expected_benefit="+30% aesthetic engagement lift on e-commerce hero placements",
        known_risks=["Shadow clipping on uncalibrated mobile screens"],
        rollback_plan="Revert Visual DNA preset to balanced studio diffuse baseline.",
        brand_id="brd_aethelgard_paris",
    )
    assert proposal.state == PromotionLifecycleState.PROVISIONAL

    # Step 19: Creative Director Review & Formal Promotion Sign-Off
    promoted_prop = prom_engine.review_and_decide(
        proposal_id=proposal.proposal_id,
        operator=cd_operator,
        decision="APPROVE",
        comments="Approved by Creative Director Helena for Aethelgard Paris tailoring dossier.",
    )
    assert promoted_prop.state == PromotionLifecycleState.PROMOTED

    # Step 20: Persist Promoted Knowledge Object into Governed Knowledge Store with Client Privacy Isolation
    k_store = GovernedKnowledgeStore()
    k_obj = k_store.store_knowledge(
        tenant_id=cd_operator.tenant_id,
        scope=promoted_prop.scope,
        title=promoted_prop.claim,
        content=f"Benefit: {promoted_prop.expected_benefit}",
        provenance_proposal_id=promoted_prop.proposal_id,
        brand_id="brd_aethelgard_paris",
    )
    assert k_obj.is_active is True

    # Step 21: Verify Next-Campaign Recommendation Retrieval & Postmortem Telemetry Emission
    active_brand_knowledge = k_store.list_knowledge(tenant_id=cd_operator.tenant_id, brand_id="brd_aethelgard_paris")
    assert len(active_brand_knowledge) == 1
    assert "Raking monolithic late sun" in active_brand_knowledge[0].title

    telemetry = LearningTelemetryEmitter()
    telemetry.emit("promotion_approved", campaign_id="camp_aw26_launch", operator_id=cd_operator.operator_id, payload={"knowledge_id": k_obj.knowledge_id})
    events = telemetry.list_events(campaign_id="camp_aw26_launch")
    assert len(events) == 1
