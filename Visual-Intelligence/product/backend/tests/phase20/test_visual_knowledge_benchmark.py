"""
Tests for Visual Knowledge Benchmark Suite and Workforce Model Integration.
"""

import pytest


def test_visual_knowledge_benchmark_250_cases(orchestrator):
    """Run full 250-case benchmark suite and verify metrics and failure taxonomy."""
    results = orchestrator.run_benchmark_suite()

    assert results["total_cases_evaluated"] >= 250
    assert results["status"] == "PASS"
    assert results["metrics"]["visual_observation_accuracy"] >= 0.85
    assert results["metrics"]["visual_dna_accuracy"] >= 0.85
    assert results["metrics"]["reliability_score"] >= 0.95


def test_workforce_model_integration(orchestrator):
    """Verify all 6 workforce roles operate through model gateways."""
    # 1. TREND_ANALYST
    t_res = orchestrator.workforce_bridge.trend_analyst_observe("Cyberpunk", "client_nocap")
    assert t_res["trust_classification"] == "UNTRUSTED_EXTERNAL_OBSERVATION"

    # 2. STRATEGIST
    s_res = orchestrator.workforce_bridge.strategist_synthesize({"theme": "Autumn"}, "client_nocap")
    assert "strategy" in s_res

    # 3. DESIGNER
    d_res = orchestrator.workforce_bridge.designer_generate({"prompt": "Lookbook"}, {}, "client_nocap")
    assert d_res.status == "SUCCESS"

    # 4. CONTENT_SPECIALIST
    c_res = orchestrator.workforce_bridge.content_specialist_write({"brand": "NOCAP"}, "client_nocap")
    assert "copy" in c_res

    # 5. CRITIC
    cr_res = orchestrator.workforce_bridge.critic_evaluate("http://example.png", "client_nocap")
    assert "critique" in cr_res

    # 6. REVIEWER
    r_res = orchestrator.workforce_bridge.reviewer_evaluate({"id": "art_1"}, "client_nocap")
    assert r_res["approved"] is True
