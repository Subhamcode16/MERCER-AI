"""
Phase 22 Tests: Production Validation
--------------------------------------
"""

import pytest
from src.runtime_control import RuntimeConfig
from src.production_validation import (
    EnvironmentValidator,
    IntegrationValidator,
    IntegrationValidatorError,
    EndToEndCampaignSimulator,
    ProductionReleaseGate,
)

def test_environment_validation():
    cfg = RuntimeConfig.from_env("TEST")
    validator = EnvironmentValidator(cfg)
    report = validator.validate_production_readiness()
    assert report["passed"] is True

def test_integration_mcp_validation_wildcard_rejection():
    validator = IntegrationValidator()
    with pytest.raises(IntegrationValidatorError):
        validator.validate_tool_capability("render_mcp", "*", "read")

    with pytest.raises(IntegrationValidatorError):
        validator.validate_tool_capability("render_mcp", "deploy", "admin")

def test_idempotency_replay_rejection():
    validator = IntegrationValidator()
    seen = set()
    assert validator.validate_idempotency("op_001", seen) is True

    with pytest.raises(IntegrationValidatorError):
        validator.validate_idempotency("op_001", seen)

def test_end_to_end_campaign_simulation():
    simulator = EndToEndCampaignSimulator()
    result = simulator.run_simulation("client_omega", "Omega Brand")
    assert result["status"] == "PASS"
    assert result["total_steps"] >= 5
    assert result["authorization_bypassed"] is False
    assert result["execution_permitted"] is True

def test_production_release_gate():
    gate = ProductionReleaseGate()
    pass_res = gate.evaluate_release()
    assert pass_res.passed is True
    assert pass_res.details["verdict"] == "PASS"

    fail_res = gate.evaluate_release(authorization_intact=False)
    assert fail_res.passed is False
    assert fail_res.details["verdict"] == "FAIL"
    assert "G03_authorization_boundary" in fail_res.details["failing_gates"]
