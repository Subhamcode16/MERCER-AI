"""
Phase 9 — Benchmark Suite Unit Tests
"""

from src.agentic_work.adaptive_strategy import AdaptiveStrategy, StrategyStatus
from src.agentic_work.benchmark_suite import BenchmarkCategory, BenchmarkSuiteRunner


def test_benchmark_suite_scoring():
    runner = BenchmarkSuiteRunner()

    strategy = AdaptiveStrategy(
        strategy_version_id="strat_test_bench",
        parent_version_id="strat_v1_default",
        parameters={
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
                "visual_consistency": 0.3,
                "brand_alignment": 0.3,
                "typography_hierarchy": 0.2,
                "market_relevance": 0.2,
            },
            "research_depth": "DEEP",
            "revision_iteration_cap": 3,
        },
        status=StrategyStatus.APPROVED,
        rationale="Benchmark test strategy",
    )

    result = runner.evaluate_strategy(strategy)

    assert result.passed_all is True
    assert result.overall_score >= 80.0
    assert len(result.category_results) == 5

    assert BenchmarkCategory.VISUAL_IDENTITY_RESEARCH in result.category_results
    assert BenchmarkCategory.BRAND_CAMPAIGN_STRATEGY in result.category_results
    assert BenchmarkCategory.VISUAL_DESIGN_DIRECTION in result.category_results
    assert BenchmarkCategory.SOCIAL_CONTENT_SYSTEM in result.category_results
    assert BenchmarkCategory.REVISION_RECOVERY in result.category_results
