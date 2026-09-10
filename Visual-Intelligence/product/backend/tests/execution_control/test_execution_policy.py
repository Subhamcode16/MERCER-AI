"""
Phase 10 — Execution Policy Engine Unit Tests
"""

import pytest
from src.execution_control.capability_models import CapabilityRiskLevel, ExecutionCapability
from src.execution_control.execution_policy import ExecutionPolicyEngine


def test_policy_risk_and_authorization_requirements():
    policy = ExecutionPolicyEngine()

    assert policy.get_capability_risk(ExecutionCapability.READ_ANALYTICS) == CapabilityRiskLevel.READ_ONLY
    assert policy.requires_human_authorization(ExecutionCapability.READ_ANALYTICS) is False

    assert policy.requires_human_authorization(ExecutionCapability.PUBLISH_CONTENT) is True
    assert policy.requires_human_authorization(ExecutionCapability.DELETE_CONTENT) is True

    assert policy.requires_dry_run(ExecutionCapability.CREATE_DRAFT) is True
