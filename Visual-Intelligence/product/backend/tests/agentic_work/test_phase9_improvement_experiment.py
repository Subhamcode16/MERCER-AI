"""
Phase 9 — Mandatory Improvement & Rollback Experiment

End-to-End Test demonstrating reproducible workflow improvement under Strategy V2,
rejection of harmful/degraded candidates, 100% deterministic rollback to V1,
and permanent ExecutionGate lock.
"""

import shutil
import tempfile
import pytest

from src.agentic_work.adaptive_strategy import AdaptiveStrategyStore, StrategyStatus
from src.agentic_work.benchmark_suite import BenchmarkSuiteRunner
from src.agentic_work.memory_models import FeedbackRecord, FeedbackSource
from src.agentic_work.persistent_feedback import PersistentFeedbackEngine
from src.agentic_work.persistent_improvement import (
    DegradationRejectedError,
    PersistentImprovementEngine,
)
from src.security_substrate import ExecutionGate, AssuranceLoopController


@pytest.fixture
def temp_experiment_env():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_mandatory_improvement_and_rollback_experiment(temp_experiment_env):
    strat_store = AdaptiveStrategyStore(base_dir=f"{temp_experiment_env}/strategies")
    fb_engine = PersistentFeedbackEngine(
        base_dir=f"{temp_experiment_env}/feedback", aggregation_threshold=3
    )
    imp_engine = PersistentImprovementEngine(
        strategy_store=strat_store, benchmark_runner=BenchmarkSuiteRunner()
    )
    gate = ExecutionGate(AssuranceLoopController())

    # 1. Baseline Strategy V1 Check
    active_v1 = strat_store.get_active_strategy()
    assert active_v1.strategy_version_id == "strat_v1_default"
    baseline_score = active_v1.benchmark_score  # 78.5
    assert gate.is_permitted() is False

    # 2. Record N=3 Consistent Feedback Signals
    for i in range(1, 4):
        fb = FeedbackRecord(
            feedback_id=f"fb_exp_{i}",
            workflow_id=f"wf_exp_{i}",
            source=FeedbackSource.CRITIC_SYSTEM,
            category="TYPOGRAPHY_CRITIQUE",
            target_role="DESIGNER",
            rating=0.4,
            comments="Increase visual consistency and brand alignment weights",
            defect_code="DEFECT_WEAK_WEIGHTS",
        )
        fb_engine.record_feedback(fb)

    patterns = fb_engine.aggregate_learning_patterns()
    assert len(patterns) == 1

    # 3. Propose Candidate Strategy V2 with optimized critique weights & deep research
    v2_params = {
        "staff_ordering": [
            "RESEARCHER",
            "STRATEGIST",
            "DESIGNER",
            "CONTENT_SPECIALIST",
            "TREND_ANALYST",
            "CRITIC",
            "REVIEWER",
        ],
        "task_graph_depth": 7,
        "critique_weights": {
            "visual_consistency": 0.35,
            "brand_alignment": 0.35,
            "typography_hierarchy": 0.15,
            "market_relevance": 0.15,
        },
        "research_depth": "DEEP",
        "revision_iteration_cap": 3,
        "benchmark_selection_weights": {"default": 1.0},
        "versioned_role_prompts": {"DESIGNER": "Prioritize high visual consistency and contrast"},
    }

    candidate_v2 = imp_engine.propose_candidate(
        candidate_version_id="strat_v2_improved",
        parent_version_id="strat_v1_default",
        parameters=v2_params,
        rationale="Optimized weights based on N=3 feedback signals",
    )
    assert candidate_v2.status == StrategyStatus.CANDIDATE

    # 4. Evaluate Candidate V2 against 5-Category Benchmark Suite
    approved_v2, bench_res_v2 = imp_engine.evaluate_candidate("strat_v2_improved")
    assert approved_v2.status == StrategyStatus.APPROVED
    assert bench_res_v2.overall_score > baseline_score  # Benchmark improves!

    # 5. Activate Strategy V2
    active_v2 = imp_engine.activate_strategy("strat_v2_improved")
    assert active_v2.status == StrategyStatus.ACTIVE
    assert strat_store.get_active_strategy().strategy_version_id == "strat_v2_improved"
    assert gate.is_permitted() is False

    # 6. Propose & Evaluate Harmful Candidate V3 (Degraded Parameters)
    v3_harmful_params = {
        "staff_ordering": ["DESIGNER"],
        "task_graph_depth": 1,
        "critique_weights": {"visual_consistency": 0.0},
        "research_depth": "MINIMAL",
        "revision_iteration_cap": 1,
    }
    imp_engine.propose_candidate(
        candidate_version_id="strat_v3_harmful",
        parent_version_id="strat_v2_improved",
        parameters=v3_harmful_params,
        rationale="Harmful minimal strategy test",
    )

    with pytest.raises(DegradationRejectedError):
        imp_engine.evaluate_candidate("strat_v3_harmful")

    # Confirm Strategy V3 is marked REJECTED and Strategy V2 remains ACTIVE
    assert strat_store.get_strategy("strat_v3_harmful").status == StrategyStatus.REJECTED
    assert strat_store.get_active_strategy().strategy_version_id == "strat_v2_improved"

    # 7. Execute Rollback of Active Strategy V2 -> Reverts cleanly to Strategy V1
    rolled_back_to_v1 = imp_engine.rollback_active_strategy()
    assert rolled_back_to_v1.strategy_version_id == "strat_v1_default"
    assert rolled_back_to_v1.status == StrategyStatus.ACTIVE
    assert strat_store.get_strategy("strat_v2_improved").status == StrategyStatus.ROLLED_BACK

    # 8. Assert ExecutionGate remains locked throughout
    assert gate.is_permitted() is False
