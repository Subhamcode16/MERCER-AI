"""
Unit tests for Phase 13 Credential Gateway (INV-13-003 & INV-13-004).
"""

import pytest

from src.integration_boundary.credential_gateway import CredentialGateway
from src.integration_boundary.models import ProviderEnvironment
from src.integration_boundary.exceptions import CredentialAccessViolationError


def test_credential_access_requires_authorization():
    gw = CredentialGateway()
    ref = gw.register_credential_handle(
        provider_id="mock_social",
        environment=ProviderEnvironment.SANDBOX,
        reference_id="ref_social_test",
        secret_handle="SECRET_OPAQUE_KEY_01",
    )

    # 1. Unverified authorization attempt raises CredentialAccessViolationError
    with pytest.raises(CredentialAccessViolationError):
        gw.get_credential_reference("mock_social", ProviderEnvironment.SANDBOX, authorization_verified=False)

    with pytest.raises(CredentialAccessViolationError):
        gw.get_opaque_secret(ref, authorization_verified=False)

    # 2. Verified authorization attempt succeeds
    ref_ok = gw.get_credential_reference("mock_social", ProviderEnvironment.SANDBOX, authorization_verified=True)
    assert ref_ok.reference_id == "ref_social_test"

    secret_ok = gw.get_opaque_secret(ref_ok, authorization_verified=True)
    assert secret_ok == "SECRET_OPAQUE_KEY_01"
