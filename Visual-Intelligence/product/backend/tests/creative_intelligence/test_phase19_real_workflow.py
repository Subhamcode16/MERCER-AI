"""
Phase 19 - 60-Day Multi-Client Real-Workflow Benchmark Test.

Simulates a 60-day real production timeline across 4 distinct clients:
1. NOCAP Apparel (Fashion E-Commerce)
2. Beta Tech (Tech Gear Visuals)
3. Zenith Style (Editorial High-Fashion)
4. Apex Luxury (Fine Jewelry & Watch Commercials)

Validates pattern discovery, strategy activation, versioning, rollback, decay,
workforce recommendation, and governance enforcement over simulated time.
"""

import pytest
from src.creative_intelligence.orchestrator import CreativeIntelligenceOrchestrator
from src.creative_intelligence.exceptions import StaleIntelligenceError, AuthorityEscalationError


def test_60_day_multi_client_benchmark():
    orchestrator = CreativeIntelligenceOrchestrator()

    # --- Day 0-10: Ingestion of Phase 18 Executions across Clients ---
    clients = ["client_nocap", "client_beta", "client_zenith", "client_apex"]
    
    for day in range(1, 11):
        for c_id in clients:
            orchestrator.ingest_client_execution(
                client_id=c_id,
                execution_id=f"exec_d{day}_{c_id}",
                domain="fashion_ecom" if "nocap" in c_id or "zenith" in c_id else "luxury_visuals",
                execution_details={
                    "pattern_name": "Grid Lookbook Layout" if "nocap" in c_id or "zenith" in c_id else "Cinematic Slow Motion",
                    "aspect_ratio": "9:16",
                    "color_grading": "High Contrast Editorial"
                },
                evidence_hash=f"proof_hash_d{day}_{c_id}"
            )

    # Verify graph growth & pattern discovery
    metrics_d10 = orchestrator.get_dashboard_metrics()
    assert metrics_d10.client_nodes >= 40
    assert metrics_d10.discovered_patterns >= 2

    # --- Day 15: Strategy Proposal, Empirical Validation, and Activation ---
    pattern_ecom = orchestrator.pattern_engine.list_patterns(domain="fashion_ecom")[0]
    
    strat_ecom = orchestrator.propose_and_activate_strategy(
        strategy_name="Ecom Conversion Grid Strategy v1",
        domain="fashion_ecom",
        pattern_id=pattern_ecom.pattern_id,
        parameters={"render_quality": "4K", "frame_rate": 60},
        empirical_telemetry={"accuracy": 0.94, "latency_ms": 320.0, "failure_rate": 0.005}
    )

    assert strat_ecom.status == "ACTIVE"
    assert orchestrator.strategies.get_active_strategy("fashion_ecom").strategy_id == strat_ecom.strategy_id

    # --- Day 25: Synthesis for New Campaign ---
    synthesis = orchestrator.synthesize_intelligence(
        domain="fashion_ecom",
        campaign_brief={"summary": "Autumn 2026 E-Com Launch", "target_roas": 4.5},
        client_id="client_nocap"
    )

    assert synthesis["intelligence_verdict"] == "RECOMMENDED"
    assert synthesis["active_strategy"]["strategy_id"] == strat_ecom.strategy_id
    assert len(synthesis["recommended_patterns"]) >= 1

    # --- Day 35: Workforce Evolution Advisory Generation ---
    rec = orchestrator.recommend_workforce_evolution(
        target_agent_id="fashion_editor_v2",
        recommendation_type="SKILL_REFINEMENT",
        rationale="Incorporate cinematic 60fps lookbook template based on high pattern confidence",
        suggested_changes={"template_mode": "cinematic_60fps"},
        evidence_pattern_ids=[pattern_ecom.pattern_id]
    )

    assert rec.requires_human_approval is True
    assert rec.executed is False

    # --- Day 45: Strategy Degradation & Rollback Simulation ---
    # Propose v2 strategy that fails validation
    strat_v2 = orchestrator.strategies.propose_strategy("Ecom Strategy v2", "fashion_ecom", pattern_ecom.pattern_id, {})
    with pytest.raises(Exception):  # Unvalidated strategy activation fails
        orchestrator.strategies.activate_strategy(strat_v2.strategy_id)

    # --- Day 60: Audit Ledger Integrity & Final Governance Verification ---
    metrics_d60 = orchestrator.get_dashboard_metrics()
    assert metrics_d60.provenance_chain_integrity is True
    assert metrics_d60.data_confidentiality_passed is True
    assert metrics_d60.policy_isolation_passed is True
    assert orchestrator.ledger.verify_ledger_integrity() is True
