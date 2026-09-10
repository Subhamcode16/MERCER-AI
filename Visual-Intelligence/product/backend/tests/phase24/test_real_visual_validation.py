"""
Tests for Phase 24 Real Visual Generation and Analysis Validation.
"""
import pytest
from src.live_operations.visual_smoke import VisualSmokeProbe
from src.live_operations.live_models import LiveValidationMode, ProbeStatus

@pytest.mark.asyncio
async def test_visual_smoke_probe_execution():
    probe = VisualSmokeProbe(mode=LiveValidationMode.SANDBOX)
    res = await probe.execute_probe({"provider": "imagen_3", "prompt": "Luxury haute couture gown"})
    assert res.status == ProbeStatus.PASS
    assert res.details["quality_score"] >= 0.85
    assert res.details["lineage_valid"] is True

@pytest.mark.asyncio
async def test_visual_smoke_probe_real_missing_creds():
    probe = VisualSmokeProbe(mode=LiveValidationMode.REAL_PROVIDER)
    res = await probe.execute_probe({"provider": "imagen_3", "api_key": None})
    assert res.status == ProbeStatus.NOT_VALIDATED
    assert "CREDENTIAL_UNAVAILABLE" in res.message
