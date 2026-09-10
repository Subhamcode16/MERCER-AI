"""
Phase 10 — Capability Models Unit Tests
"""

import pytest
from src.execution_control.capability_models import (
    CAPABILITY_RISK_MAP,
    CapabilityRiskLevel,
    ExecutionCapability,
    validate_capability_string,
)
from src.execution_control.exceptions import CapabilityViolationError


def test_validate_valid_capabilities():
    assert validate_capability_string("CREATE_DRAFT") == ExecutionCapability.CREATE_DRAFT
    assert validate_capability_string("publish_content") == ExecutionCapability.PUBLISH_CONTENT


def test_validate_rejects_forbidden_patterns():
    for forbidden in ["ALLOW_ALL", "ADMIN_EXECUTE", "BYPASS_SECURITY", "UNLOCK_GATE", "ROOT_ACCESS"]:
        with pytest.raises(CapabilityViolationError) as exc:
            validate_capability_string(forbidden)
        assert "Forbidden administrative or bypass capability" in str(exc.value)


def test_validate_rejects_unknown_capability():
    with pytest.raises(CapabilityViolationError):
        validate_capability_string("UNLIMITED_POWER")


def test_capability_risk_mapping():
    assert CAPABILITY_RISK_MAP[ExecutionCapability.READ_ANALYTICS] == CapabilityRiskLevel.READ_ONLY
    assert CAPABILITY_RISK_MAP[ExecutionCapability.PUBLISH_CONTENT] == CapabilityRiskLevel.HIGH_RISK
    assert CAPABILITY_RISK_MAP[ExecutionCapability.DELETE_CONTENT] == CapabilityRiskLevel.CRITICAL
