"""
Phase 9 — Adaptive Strategy & Allowlist Unit Tests
"""

import shutil
import tempfile
import pytest

from src.agentic_work.adaptive_strategy import (
    AdaptiveStrategy,
    AdaptiveStrategyStore,
    SecurityBoundaryViolation,
    StrategyStatus,
)


@pytest.fixture
def temp_strategy_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_strategy_allowlist_valid_parameters():
    strat = AdaptiveStrategy(
        strategy_version_id="strat_valid",
        parent_version_id="strat_v1_default",
        parameters={
            "staff_ordering": ["RESEARCHER", "DESIGNER", "CRITIC"],
            "task_graph_depth": 5,
            "critique_weights": {"visual_consistency": 0.5},
            "research_depth": "DEEP",
            "revision_iteration_cap": 2,
        },
        status=StrategyStatus.CANDIDATE,
        rationale="Valid tactical adaptation",
    )
    # Should pass validation cleanly
    strat.validate_allowlist()


def test_strategy_rejects_forbidden_security_mutation():
    strat = AdaptiveStrategy(
        strategy_version_id="strat_malicious",
        parent_version_id="strat_v1_default",
        parameters={
            "staff_ordering": ["RESEARCHER", "DESIGNER"],
            "execution_gate": "UNLOCK_GATE",  # Forbidden security field!
        },
        status=StrategyStatus.CANDIDATE,
        rationale="Attempted gate unlock mutation",
    )

    with pytest.raises(SecurityBoundaryViolation) as exc_info:
        strat.validate_allowlist()
    assert "execution_gate" in str(exc_info.value)


def test_strategy_store_lifecycle(temp_strategy_dir):
    store = AdaptiveStrategyStore(base_dir=temp_strategy_dir)

    default_strat = store.get_active_strategy()
    assert default_strat.strategy_version_id == "strat_v1_default"

    new_strat = AdaptiveStrategy(
        strategy_version_id="strat_v2_custom",
        parent_version_id="strat_v1_default",
        parameters={
            "staff_ordering": ["RESEARCHER", "STRATEGIST", "DESIGNER", "CRITIC", "REVIEWER"],
            "task_graph_depth": 5,
            "critique_weights": {"visual_consistency": 0.4, "brand_alignment": 0.6},
            "revision_iteration_cap": 3,
        },
        status=StrategyStatus.APPROVED,
        rationale="Improved critique weighting",
        benchmark_score=88.5,
    )

    store.save_strategy(new_strat)

    loaded = store.get_strategy("strat_v2_custom")
    assert loaded.benchmark_score == 88.5
    assert loaded.status == StrategyStatus.APPROVED
