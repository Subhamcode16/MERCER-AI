"""
Tests for Phase 23 Secret & Credential Operations.
"""
import pytest
import time
from src.secret_operations.secret_models import CredentialDomain
from src.secret_operations.secret_provider import ProductionSecretProvider
from src.secret_operations.redaction import SecretRedactionEngine
from src.secret_operations.exceptions import (
    UnauthorizedScopeError,
    SecretNotFoundError,
    LeaseExpiredError
)

def test_scoped_secret_acquisition_and_audit():
    provider = ProductionSecretProvider()
    provider.register_secret("gemini_api_key", CredentialDomain.LLM, "sk-gemini-live-secret-key-12345")

    # Valid: llm_gateway requesting LLM domain
    val, lease = provider.acquire_secret_with_lease(
        secret_name="gemini_api_key",
        domain=CredentialDomain.LLM,
        caller_service="llm_gateway",
        ttl_seconds=3600.0
    )
    assert val == "sk-gemini-live-secret-key-12345"
    assert lease.is_valid() is True

    # Invalid scope: mcp_gateway requesting LLM domain
    with pytest.raises(UnauthorizedScopeError):
        provider.acquire_secret_with_lease(
            secret_name="gemini_api_key",
            domain=CredentialDomain.LLM,
            caller_service="mcp_gateway"
        )

def test_secret_rotation_without_restart():
    provider = ProductionSecretProvider()
    provider.register_secret("storage_token", CredentialDomain.STORAGE, "token-v1-initial")

    meta_rotated = provider.rotation_engine.rotate_secret("storage_token", "token-v2-fresh")
    assert meta_rotated.version == 2

    val, _ = provider.acquire_secret_with_lease(
        secret_name="storage_token",
        domain=CredentialDomain.STORAGE,
        caller_service="persistence_engine"
    )
    assert val == "token-v2-fresh"

def test_secret_lease_expiry_and_revocation():
    provider = ProductionSecretProvider()
    provider.register_secret("mcp_key", CredentialDomain.MCP, "mcp-secret-payload-999")

    _, lease = provider.acquire_secret_with_lease(
        secret_name="mcp_key",
        domain=CredentialDomain.MCP,
        caller_service="mcp_gateway",
        ttl_seconds=0.01
    )
    
    # Revoke lease
    provider.lease_manager.revoke_lease(lease.lease_id)
    with pytest.raises(LeaseExpiredError):
        provider.lease_manager.validate_lease(lease.lease_id)

def test_secret_redaction_engine():
    raw_log = "Calling model with api_key: sk-1234567890abcdef1234567890 and Bearer 9876543210fedcba"
    masked = SecretRedactionEngine.redact_text(raw_log)
    assert "sk-1234567890abcdef1234567890" not in masked
    assert "***REDACTED***" in masked

    raw_dict = {
        "tenant_id": "tenant-1",
        "api_key": "super_secret_token",
        "nested": {"client_secret": "my_secret"}
    }
    cleaned = SecretRedactionEngine.redact_dict(raw_dict)
    assert cleaned["api_key"] == "***REDACTED***"
    assert cleaned["nested"]["client_secret"] == "***REDACTED***"
    assert cleaned["tenant_id"] == "tenant-1"
