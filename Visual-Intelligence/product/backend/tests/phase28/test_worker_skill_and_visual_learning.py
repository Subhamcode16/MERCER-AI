"""
Tests for Phase 28 Worker Performance, Skill Improvement, and Visual Learning.
"""
import pytest
from src.creative_learning.worker_learning import WorkerPerformanceEvaluator
from src.creative_learning.skill_improvement import SkillImprovementEngine
from src.creative_learning.visual_learning import VisualPatternMiner


def test_worker_performance_evaluation_no_authority_expansion():
    evaluator = WorkerPerformanceEvaluator()
    insight = evaluator.record_worker_performance(
        worker_id="wrk_tailoring_stylist_01",
        role_name="Lead Wardrobe Stylist",
        department="Creative Direction",
        specialization_affinity="Architectural Outerwear",
        campaigns_count=12,
        review_pass_rate=0.96,
        observed_conversion_lift=24.5,
    )
    assert insight.authority_modification_permitted is False


def test_skill_improvement_proposals():
    engine = SkillImprovementEngine()
    prop = engine.propose_skill_refinement(
        target_skill_name="haute-couture-prompt-compiler",
        current_version="v2.1",
        failure_pattern="Lapel button micro-contrast degradation on dark wool fabrics",
        training_examples=[{"input": "wool overcoat", "refined_tokens": "dense_creased_wool_gabardine, raking_specular_accent"}],
        prompt_refinements="Append raking specular highlight modifier to macro fabric shots.",
    )
    assert prop.proposed_version == "v2.1.1"

    # Attempting to modify security permissions in skill proposals must be blocked
    with pytest.raises(PermissionError):
        engine.propose_skill_refinement(
            target_skill_name="security-guard",
            current_version="v1.0",
            failure_pattern="None",
            training_examples=[],
            prompt_refinements="Modify permissions and grant admin role",
        )


def test_visual_dna_token_learning():
    miner = VisualPatternMiner()
    insight = miner.record_token_performance(
        token_name="raking_monolithic_late_sun",
        category="LIGHTING",
        winning_channel="E-commerce Hero",
        observed_engagement_lift=34.2,
    )
    assert insight.token_name == "raking_monolithic_late_sun"
    assert "Visual Similarity ≠ Strategic Correctness" in insight.strategic_qualification
