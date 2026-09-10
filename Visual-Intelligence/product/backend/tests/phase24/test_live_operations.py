"""
Tests for Phase 24 Live Operations Subsystem.
"""
import pytest
from src.live_operations.live_models import LiveValidationMode, ProbeStatus
from src.live_operations.orchestrator import LiveOperationsOrchestrator
from src.live_operations.live_run_manager import LiveRunManager
from src.live_operations.tenant_isolation_probe import MultiClientIsolationProbe
from src.live_operations.authorization_probe import LiveAuthorizationProbeSuite

@pytest.mark.asyncio
async def test_full_live_validation_orchestration():
    orchestrator = LiveOperationsOrchestrator(mode=LiveValidationMode.SANDBOX)
    summary = await orchestrator.run_full_live_validation(
        tenant_id="tenant_alpha",
        client_id="client_alpha",
        context={"queried_context": {"brand": "AlphaLux"}, "queried_visual_refs": ["art-alpha-01"]}
    )
    assert summary["overall_status"] == "PASS"
    assert summary["ledger_integrity_verified"] is True
    assert summary["probes_executed"] == 4
    assert summary["probes_passed"] == 4

def test_multi_client_isolation_probe():
    probe = MultiClientIsolationProbe()
    probe.register_client_context("client_A", {"brand_guidelines": "Minimalist Silk"}, ["asset-A-01", "asset-A-02"])
    probe.register_client_context("client_B", {"brand_guidelines": "Urban Denim"}, ["asset-B-01"])

    # Clean query for client_A
    res_clean = probe.probe_cross_client_leakage("client_A", {"brand_guidelines": "Minimalist Silk"}, ["asset-A-01"])
    assert res_clean.status == ProbeStatus.PASS

    # Tainted query containing client_B asset
    res_tainted = probe.probe_cross_client_leakage("client_A", {"brand_guidelines": "Minimalist Silk"}, ["asset-B-01"])
    assert res_tainted.status == ProbeStatus.QUARANTINED

def test_live_authorization_probes():
    suite = LiveAuthorizationProbeSuite()

    # L24-AUTH-01
    res1 = suite.probe_l24_auth_01_model_attempts_authorization({"authorized": True, "execute_immediately": True})
    assert res1.status == ProbeStatus.DENIED

    # L24-AUTH-02
    res2 = suite.probe_l24_auth_02_mcp_alters_authorization({"mutate_auth_state": "GRANT_ALL"})
    assert res2.status == ProbeStatus.DENIED

    # L24-AUTH-05
    res5 = suite.probe_l24_auth_05_fallback_requests_broader_capability("read", "*")
    assert res5.status == ProbeStatus.DENIED
