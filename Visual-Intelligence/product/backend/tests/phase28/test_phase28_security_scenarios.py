"""
Phase 28 Security Scenarios Test Suite (T28-001 through T28-025).
Validates mathematical invariants, non-scope guarantees, cross-client privacy, anti-hallucination, and RBAC authority boundaries.
"""
import pytest
from datetime import datetime, timezone, timedelta
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.creative_learning.decision_ledger import (
    DecisionLedger,
    DecisionType,
    DecisionContextSnapshot,
    DecisionAlternative,
)
from src.creative_learning.outcome_ingestion import OutcomeIngestionPipeline
from src.creative_learning.attribution import AttributionEngine, EvidenceCausalStatus
from src.creative_learning.hypotheses import LearningHypothesisStore, HypothesisScope
from src.creative_learning.counterfactuals import CounterfactualEngine, CounterfactualState
from src.creative_learning.experiments import ExperimentRegistry, ExperimentStatus
from src.creative_learning.calibration import CalibrationTracker
from src.creative_learning.promotion import KnowledgePromotionEngine, PromotionLifecycleState
from src.creative_learning.contradiction import ContradictionHandler, ContradictionStatus
from src.creative_learning.pattern_discovery import CreativePatternMiner
from src.creative_learning.skill_improvement import SkillImprovementEngine
from src.creative_learning.worker_learning import WorkerPerformanceEvaluator
from src.creative_learning.learning_memory import GovernedKnowledgeStore
from src.creative_learning.freshness import KnowledgeFreshnessEvaluator
from src.creative_learning.drift import EnvironmentDriftDetector, DriftType
from src.creative_learning.learning_governance import LearningGovernanceEngine


# T28-001: Outcome data injection is detected via provenance signature
def test_t28_001_outcome_data_injection():
    pipeline = OutcomeIngestionPipeline()
    feed = pipeline.ingest_feed("c1", "MetaAds", {"impressions": 100}, "MOCK_INJECTION_ATTACK")
    assert feed.is_verified is False


# T28-002: Fake performance evidence without signature fails verification
def test_t28_002_fake_performance_evidence():
    pipeline = OutcomeIngestionPipeline()
    feed = pipeline.ingest_feed("c1", "MetaAds", {"impressions": 100}, "")
    assert feed.is_verified is False


# T28-003: Correlation presented as causation is blocked and qualified
def test_t28_003_correlation_presented_as_causation():
    gov = LearningGovernanceEngine()
    res = gov.evaluate_learning_claim("This visual direction proves causality and guarantees success.")
    assert res.is_compliant is False
    assert any("Correlation ≠ Causal Proof" in v for v in res.violations)


# T28-004: Single campaign cannot become universal rule
def test_t28_004_single_campaign_cannot_become_universal_rule():
    gov = LearningGovernanceEngine()
    res = gov.evaluate_learning_claim("This campaign result is universally true for all clients globally without exception.")
    assert res.is_compliant is False


# T28-005: Contradictory evidence is preserved and not deleted
def test_t28_005_contradictory_evidence_preserved():
    handler = ContradictionHandler()
    contra = handler.log_contradiction("Claim A", "Source A", "Conflicting Evidence B", "c1")
    assert contra.status == ContradictionStatus.OPEN_DISPUTE
    assert len(handler.list_contradictions()) == 1


# T28-006: Private client outcome cannot become global knowledge
def test_t28_006_private_client_outcome_cannot_become_global():
    engine = KnowledgePromotionEngine()
    with pytest.raises(PermissionError):
        engine.propose_promotion(
            claim="Private client secret recipe",
            scope=HypothesisScope.GLOBAL,
            supporting_evidence=["Evidence"],
            affected_knowledge_objects=["GlobalPreset"],
            expected_benefit="Benefit",
            known_risks=[],
            rollback_plan="Rollback",
            client_id="cli_private_123",
        )


# T28-007: Learning cannot modify operator permissions or authorization
def test_t28_007_learning_cannot_modify_authorization():
    gov = LearningGovernanceEngine()
    op = OperatorContext(operator_id="op_intern", role=OperatorRole.STAFF_OPERATOR)
    res = gov.evaluate_policy_mutation_attempt(op, "Modify security policy and grant admin role")
    assert res.is_compliant is False


# T28-008: Optimizer cannot modify security policy
def test_t28_008_optimizer_modifies_security_policy():
    engine = SkillImprovementEngine()
    with pytest.raises(PermissionError):
        engine.propose_skill_refinement("auth-checker", "v1", "fail", [], "Modify permissions to bypass rbac")


# T28-009: Model confidence is not treated as empirical proof
def test_t28_009_model_confidence_treated_as_empirical_proof():
    tracker = CalibrationTracker()
    for _ in range(5):
        tracker.record_prediction("VISUAL_QUALITY", 0.99, True)
    report = tracker.get_calibration_report("VISUAL_QUALITY")
    high_bucket = next(b for b in report.buckets if b.range_label == "0.80 - 1.00")
    assert high_bucket.is_statistically_reliable is False  # Sample too small


# T28-010: Fabricated counterfactual is denied
def test_t28_010_fabricated_counterfactual():
    engine = CounterfactualEngine()
    tree = engine.build_counterfactual_tree("c1", "Path A", "Outcome A", ["Path B"])
    assert tree.alternative_branches[0].state == CounterfactualState.COUNTERFACTUAL_UNKNOWN
    assert tree.alternative_branches[0].estimated_outcome_range is None


# T28-011: Stale learning is flagged with expiry check
def test_t28_011_stale_learning_freshness_check():
    evaluator = KnowledgeFreshnessEvaluator()
    eval_res = evaluator.evaluate_freshness("k1", datetime.now(timezone.utc) - timedelta(days=150), expiry_limit_days=90)
    assert eval_res.is_fresh is False
    assert eval_res.recommendation == "EXPIRED"


# T28-012: Provider drift is flagged as a confounder
def test_t28_012_provider_drift_flagged_as_confounder():
    detector = EnvironmentDriftDetector()
    alert = detector.check_and_record_drift(DriftType.MODEL_VERSION_DRIFT, "Model Provider", "v1", "v2")
    assert alert is not None
    assert "confounder" in alert.confounder_warning.lower()


# T28-013: Skill self-modification requires governed promotion
def test_t28_013_skill_self_modification():
    engine = SkillImprovementEngine()
    prop = engine.propose_skill_refinement("prompt-compiler", "v1", "defect", [], "Append modifier")
    assert prop.status == "PROPOSED"


# T28-014: Worker privilege does not change from performance
def test_t28_014_worker_privilege_does_not_change_from_performance():
    evaluator = WorkerPerformanceEvaluator()
    insight = evaluator.record_worker_performance("w1", "Stylist", "Creative", "Tailoring", 50, 0.99, 45.0)
    assert insight.authority_modification_permitted is False


# T28-015: Rejected creative is preserved in context and not universally invalidated
def test_t28_015_rejected_creative_preserved_in_context():
    ledger = DecisionLedger()
    snapshot = DecisionContextSnapshot("s1", "t1", "c1", "b1", "camp1")
    alt = DecisionAlternative("alt1", "Cyber Neon", "Rejected for Autumn Luxury Lookbook", 0.8)
    rec = ledger.record_decision("camp1", DecisionType.VISUAL_DIRECTION, "op1", snapshot, "Chose Monolith", "Rationale", 0.9, alternatives=[alt])
    assert len(rec.alternatives) == 1
    assert rec.alternatives[0].alternative_id == "alt1"


# T28-016: Outcome linkage maps to exact asset version
def test_t28_016_outcome_linked_to_exact_asset_version():
    from src.creative_learning.outcome_linkage import OutcomeLinkageGraph
    graph = OutcomeLinkageGraph()
    node = graph.link_outcome("c1", "d1", "ast1", 2, "Instagram", ["m1"], 1)
    assert node.asset_version == 2


# T28-017: Tampering with decision ledger is detected
def test_t28_017_decision_ledger_tampering_detected():
    ledger = DecisionLedger()
    snapshot = DecisionContextSnapshot("s1", "t1", "c1", "b1", "camp1")
    rec = ledger.record_decision("camp1", DecisionType.CREATIVE_TERRITORY, "op1", snapshot, "Dec 1", "Rat 1", 0.9)
    assert ledger.verify_ledger_integrity("camp1") is True
    rec.rationale = "TAMPERED_RATIONALE"
    assert ledger.verify_ledger_integrity("camp1") is False


# T28-018: Calibration based on insufficient sample is flagged
def test_t28_018_calibration_tiny_sample_flagged():
    tracker = CalibrationTracker()
    tracker.record_prediction("CREATIVE_DIRECTION", 0.30, True)
    report = tracker.get_calibration_report("CREATIVE_DIRECTION")
    bucket = next(b for b in report.buckets if b.range_label == "0.20 - 0.40")
    assert bucket.is_statistically_reliable is False


# T28-019: Evidence laundering requires provenance proposal
def test_t28_019_evidence_laundering_requires_provenance():
    store = GovernedKnowledgeStore()
    obj = store.store_knowledge("tenant_1", HypothesisScope.BRAND, "Title", "Content", "proposal_ref_99")
    assert obj.provenance_proposal_id == "proposal_ref_99"


# T28-020: Learning rollback does not destroy historical record
def test_t28_020_learning_rollback_preserves_history():
    store = GovernedKnowledgeStore()
    obj = store.store_knowledge("t1", HypothesisScope.BRAND, "Title", "Content", "p1")
    assert obj.is_active is True
    store.rollback_knowledge(obj.knowledge_id, "t1")
    assert obj.is_active is False
    all_objs = store.list_knowledge(tenant_id="t1", active_only=False)
    assert len(all_objs) == 1  # Still present in history


# T28-021: Cross-client pattern leakage is denied
def test_t28_021_cross_client_pattern_leakage_denied():
    miner = CreativePatternMiner()
    with pytest.raises(PermissionError):
        miner.discover_pattern("Pattern A", "COMPOSITION", HypothesisScope.GLOBAL, "Desc", ["c1"], 15.0, client_id="cli_private")


# T28-022: Automated causal claim generation requires epistemic qualification
def test_t28_022_causal_claim_qualification():
    att = AttributionEngine()
    assessment = att.evaluate_attribution("c1", "a1", 20.0, is_controlled_ab_test=False)
    assert assessment.causal_status in {EvidenceCausalStatus.CONFOUNDED, EvidenceCausalStatus.CORRELATIONAL_OBSERVATIONAL}


# T28-023: Non-existent proposal review raises KeyError
def test_t28_023_nonexistent_proposal_review():
    engine = KnowledgePromotionEngine()
    cd = OperatorContext(operator_id="op_cd", role=OperatorRole.CREATIVE_DIRECTOR)
    with pytest.raises(KeyError):
        engine.review_and_decide("prm_404", cd, "APPROVE")


# T28-024: Unauthorized operator cannot approve promotion
def test_t28_024_unauthorized_operator_cannot_approve_promotion():
    engine = KnowledgePromotionEngine()
    prop = engine.propose_promotion("Claim", HypothesisScope.BRAND, ["Ev"], ["Obj"], "Ben", ["Risk"], "Rollback")
    staff = OperatorContext(operator_id="op_staff", role=OperatorRole.STAFF_OPERATOR)
    with pytest.raises(PermissionError):
        engine.review_and_decide(prop.proposal_id, staff, "APPROVE")


# T28-025: Unknown state is preserved and not converted into certainty
def test_t28_025_unknown_state_preserved():
    ledger = DecisionLedger()
    snapshot = DecisionContextSnapshot("s1", "t1", "c1", "b1", "camp1")
    rec = ledger.record_decision("camp1", DecisionType.LAUNCH_TIMING, "op1", snapshot, "Launch Oct 15", "Seasonal peak", 0.88, unknowns=["Competitor surprise launch", "Weather anomaly"])
    assert len(rec.unknowns) >= 2
    assert "Competitor surprise launch" in rec.unknowns
