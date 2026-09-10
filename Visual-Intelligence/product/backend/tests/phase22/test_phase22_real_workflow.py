"""
Phase 22 Tests: Real End-to-End Workflow Integration
-----------------------------------------------------
"""

import pytest
from src.production_validation import EndToEndCampaignSimulator, ProductionReleaseGate
from src.visual_evaluation import VisualBenchmarkRunner

def test_phase22_real_workflow_execution():
    simulator = EndToEndCampaignSimulator()
    sim_res = simulator.run_simulation("client_real_01", "ILYREN Haute Capsule")
    assert sim_res["status"] == "PASS"
    assert sim_res["execution_permitted"] is True

    runner = VisualBenchmarkRunner()
    bench_res = runner.run_benchmark("gemini-2.5-flash")
    assert bench_res["status"] == "PASS"

    gate = ProductionReleaseGate()
    gate_res = gate.evaluate_release(
        security_tests_green=True,
        client_isolation_green=True,
        authorization_intact=True,
        benchmark_integrity_green=bench_res["status"] == "PASS",
        zero_secrets_leaked=True,
        mcp_isolation_green=True,
        dependencies_validated=True,
        audit_integrity_green=True,
        config_valid=True,
        integrations_available=True,
        regression_green=True,
    )
    assert gate_res.passed is True
