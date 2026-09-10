"""
Phase 28 Multi-Step Integration Workflows Test Suite.
Tests the 5 canonical workflows:
A — Campaign Postmortem
B — Learning Promotion
C — Future Recommendation
D — Skill Improvement
E — Visual Learning
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.creative_learning.decision_ledger import DecisionLedger, DecisionType, DecisionContextSnapshot
from src.creative_learning.outcome_ingestion import OutcomeIngestionPipeline
from src.creative_learning.outcome_normalization import OutcomeNormalizer
from src.creative_learning.outcome_linkage import OutcomeLinkageGraph
from src.creative_learning.attribution import AttributionEngine, EvidenceCausalStatus
from src.creative_learning.learning_signals import LearningSignalGenerator, LearningSignalType
from src.creative_learning.hypotheses import LearningHypothesisStore, HypothesisScope
from src.creative_learning.counterfactuals import CounterfactualEngine
from src.creative_learning.experiments import ExperimentRegistry, ExperimentStatus
from src.creative_learning.calibration import CalibrationTracker
from src.creative_learning.promotion import KnowledgePromotionEngine, PromotionLifecycleState
from src.creative_learning.contradiction import ContradictionHandler
from src.creative_learning.pattern_discovery import CreativePatternMiner
from src.creative_learning.skill_improvement import SkillImprovementEngine
from src.creative_learning.worker_learning import WorkerPerformanceEvaluator
from src.creative_learning.visual_learning import VisualPatternMiner
from src.creative_learning.learning_memory import GovernedKnowledgeStore


def test_workflow_a_campaign_postmortem_to_learning_signals():
    # 1. Record decisions
    ledger = DecisionLedger()
    snapshot = DecisionContextSnapshot("snp_a", "t_lux", "cli_a", "brd_a", "camp_wf_a")
    ledger.record_decision("camp_wf_a", DecisionType.VISUAL_DIRECTION, "op_cd", snapshot, "Monolithic Elegance", "Silhouette clarity", 0.94)

    # 2. Ingest outcomes
    ingestion = OutcomeIngestionPipeline()
    feed = ingestion.ingest_feed("camp_wf_a", "ShopifyStorefront", {"impressions": 300000, "clicks": 9000, "conversions": 720}, "sig_valid_123")
    assert feed.is_verified

    # 3. Normalize metrics
    normalizer = OutcomeNormalizer()
    metrics = normalizer.normalize_feed("camp_wf_a", "ShopifyStorefront", feed.metrics_payload)
    assert len(metrics) >= 3

    # 4. Linkage
    linkage = OutcomeLinkageGraph()
    linkage.link_outcome("camp_wf_a", "dir_mono", "ast_hero", 1, "Shopify", [m.metric_id for m in metrics], 1)

    # 5. Epistemic Attribution
    attribution = AttributionEngine()
    assessment = attribution.evaluate_attribution("camp_wf_a", "ast_hero", 24.0)
    assert assessment.causal_status == EvidenceCausalStatus.CONFOUNDED

    # 6. Generate learning signals
    signal_gen = LearningSignalGenerator()
    cvr_metric = next(m for m in metrics if m.metric_name == "CONVERSION_RATE")
    signal = signal_gen.evaluate_signal("camp_wf_a", "direction:Monolithic_Elegance", "CONVERSION_RATE", cvr_metric.normalized_value, 0.05, 9000)
    assert signal.signal_type == LearningSignalType.POSITIVE_SIGNAL


def test_workflow_b_learning_promotion_governance_lifecycle():
    engine = KnowledgePromotionEngine()
    store = GovernedKnowledgeStore()
    cd = OperatorContext(operator_id="op_cd_01", role=OperatorRole.CREATIVE_DIRECTOR, tenant_id="t_lux")

    # Propose
    prop = engine.propose_promotion(
        claim="Raking late sun lighting maximizes outerwear texture definition.",
        scope=HypothesisScope.BRAND,
        supporting_evidence=["Autumn Gala Shopify CVR +34%"],
        affected_knowledge_objects=["Preset:Outerwear_DNA"],
        expected_benefit="+20% aesthetic review pass rate",
        known_risks=["Potential contrast harshness"],
        rollback_plan="Revert to diffuse lighting",
        brand_id="brd_a",
    )
    assert prop.state == PromotionLifecycleState.PROVISIONAL

    # Review & Approve
    engine.review_and_decide(prop.proposal_id, cd, "APPROVE", "Signed off by CD Helena")
    assert prop.state == PromotionLifecycleState.PROMOTED

    # Ingest into Governed Knowledge Store
    k_obj = store.store_knowledge(
        tenant_id="t_lux",
        scope=prop.scope,
        title=prop.claim,
        content=f"Benefit: {prop.expected_benefit}",
        provenance_proposal_id=prop.proposal_id,
        brand_id=prop.brand_id,
    )
    assert k_obj.is_active is True


def test_workflow_c_future_recommendation_informing():
    store = GovernedKnowledgeStore()
    store.store_knowledge(
        tenant_id="t_lux",
        scope=HypothesisScope.BRAND,
        title="Tactile Wool Preset",
        content="Apply raking specular token.",
        provenance_proposal_id="prm_01",
        brand_id="brd_a",
    )

    # Next campaign retrieves validated knowledge
    active_knowledge = store.list_knowledge(tenant_id="t_lux", brand_id="brd_a")
    assert len(active_knowledge) == 1
    assert "Tactile Wool Preset" in active_knowledge[0].title


def test_workflow_d_skill_improvement_proposals():
    skill_opt = SkillImprovementEngine()
    prop = skill_opt.propose_skill_refinement(
        target_skill_name="brand-stylist",
        current_version="v1.4",
        failure_pattern="Missing negative prompt tokens on leather sheen",
        training_examples=[{"input": "glossy leather trench", "negative": "plastic glare, cartoon saturation"}],
        prompt_refinements="Append glare mitigation tokens",
    )
    assert prop.proposed_version == "v1.4.1"


def test_workflow_e_visual_learning_pattern_mining():
    miner = VisualPatternMiner()
    insight = miner.record_token_performance("billowing_silk_organza", "TEXTURE", "Lookbook", 28.5)
    assert insight.observed_engagement_lift == 28.5
    assert len(miner.list_insights()) == 1
