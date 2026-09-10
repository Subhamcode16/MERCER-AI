"""
Tests for Phase 24 Real Model Validation.
"""
import pytest
from src.live_operations.llm_smoke import LLMSmokeProbe
from src.live_operations.live_models import LiveValidationMode, ProbeStatus

@pytest.mark.asyncio
async def test_llm_smoke_probe_sandbox_and_real_modes():
    # Sandbox mode with simulated credentials
    probe_sandbox = LLMSmokeProbe(mode=LiveValidationMode.SANDBOX)
    res_sandbox = await probe_sandbox.execute_probe({"provider": "google", "model": "gemini-2.5-flash"})
    assert res_sandbox.status == ProbeStatus.PASS
    assert res_sandbox.details["structured_output_valid"] is True
    assert res_sandbox.details["cost_usd"] > 0.0

    # Real mode without credentials must fail gracefully as NOT_VALIDATED (Never fake PASS)
    probe_real = LLMSmokeProbe(mode=LiveValidationMode.REAL_PROVIDER)
    res_real = await probe_real.execute_probe({"provider": "google", "model": "gemini-2.5-flash", "api_key": None})
    assert res_real.status == ProbeStatus.NOT_VALIDATED
    assert "CREDENTIAL_UNAVAILABLE" in res_real.message
