"""
Unit tests for Phase 13 Environment Guard (INV-13-005).
"""

import pytest

from src.integration_boundary.environment_guard import EnvironmentGuard
from src.integration_boundary.models import ProviderEnvironment, CredentialReference
from src.integration_boundary.exceptions import EnvironmentMismatchError


def test_environment_guard_mismatch_rejection():
    guard = EnvironmentGuard()
    ref_sandbox = CredentialReference("ref_1", "mock_social", ProviderEnvironment.SANDBOX)

    # 1. Sandbox credential on LIVE operation raises EnvironmentMismatchError
    with pytest.raises(EnvironmentMismatchError):
        guard.validate_environment_boundary(ProviderEnvironment.LIVE, ref_sandbox)

    # 2. Sandbox credential on SANDBOX operation passes
    guard.validate_environment_boundary(ProviderEnvironment.SANDBOX, ref_sandbox)


def test_environment_guard_live_without_explicit_flag():
    guard = EnvironmentGuard()
    ref_live = CredentialReference("ref_live", "mock_social", ProviderEnvironment.LIVE)

    # LIVE credential on LIVE operation without explicit_live_allowed flag raises EnvironmentMismatchError
    with pytest.raises(EnvironmentMismatchError):
        guard.validate_environment_boundary(ProviderEnvironment.LIVE, ref_live, explicit_live_allowed=False)

    guard.validate_environment_boundary(ProviderEnvironment.LIVE, ref_live, explicit_live_allowed=True)
