"""
Unit tests for Phase 17 Production Outcome Loop.
"""

from src.production_fabric.outcome_loop import ProductionOutcomeLoop
from src.studio_operations.orchestrator import StudioOperationsOrchestrator

def test_outcome_loop_ingestion(tmp_path):
    orch = StudioOperationsOrchestrator(ledger_dir=str(tmp_path / "out_ledger"))
    orch.register_client_engagement("client_a", "Alpha", "Tech")

    loop = ProductionOutcomeLoop()
    outcome = loop.ingest_outcome(
        outcome_id="out_01",
        client_id="client_a",
        campaign_id="c1",
        deliverable_id="d1",
        provider="instagram",
        external_post_id="post_999",
        reach=5000,
        engagement_rate=0.085,
        studio_orchestrator=orch
    )

    assert outcome.provenance == "UNTRUSTED_EXTERNAL_OBSERVATION"
    assert outcome.reach == 5000
