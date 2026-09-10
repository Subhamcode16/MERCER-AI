"""
Phase 20 Real Workflow Benchmark — NOCAP Campaign Model-Backed Production Cycle.

Simulates end-to-end model-backed production cycle for NOCAP Apparel:
Client Objective -> Context -> Mission -> Workforce Decomposition -> Trend Research (MCP) ->
Visual Analysis -> Creative Direction -> Visual Asset Generation -> Copy Generation ->
Self-Critique -> Revision -> Independent Governance Review -> Human Authorization Gate.
"""

import pytest
from src.model_workforce.phase20_orchestrator import Phase20Orchestrator


def test_nocap_real_workflow_production_cycle():
    orchestrator = Phase20Orchestrator()

    campaign_brief = {
        "campaign_id": "nocap_autumn_2026",
        "client_id": "client_nocap",
        "theme": "Cyberpunk High Fashion Lookbook",
        "target_roas": 5.0,
        "deliverables": ["hero_banner", "social_grid", "campaign_copy"]
    }

    cycle_result = orchestrator.run_nocap_production_cycle(campaign_brief, client_id="client_nocap")

    assert cycle_result["client_id"] == "client_nocap"
    assert cycle_result["trend_observation"]["trust_classification"] == "UNTRUSTED_EXTERNAL_OBSERVATION"
    assert "strategy" in cycle_result["strategy"]
    assert cycle_result["generated_visual_artifact"]["status"] == "SUCCESS"
    assert "copy" in cycle_result["generated_copy"]
    assert cycle_result["self_critique"]["confidence"] >= 0.90
    assert cycle_result["governance_review"]["approved"] is True
    assert cycle_result["status"] == "APPROVED_FOR_HUMAN_AUTHORIZATION"
    assert orchestrator.verify_all_ledgers() is True
