"""
Phase 23 Scoped Production Secret Provider.
"""
import os
import logging
from typing import Dict, Any, Optional
from src.secret_operations.secret_models import CredentialDomain, SecretLease
from src.secret_operations.credential_scope import CredentialScopeValidator
from src.secret_operations.rotation import SecretRotationEngine
from src.secret_operations.lease import SecretLeaseManager
from src.secret_operations.audit import SecretAuditLogger
from src.secret_operations.exceptions import SecretNotFoundError

logger = logging.getLogger(__name__)

class ProductionSecretProvider:
    """Provides scoped, audited, and leased secrets to authorized internal subsystems."""

    def __init__(self):
        self.rotation_engine = SecretRotationEngine()
        self.lease_manager = SecretLeaseManager()
        self.audit_logger = SecretAuditLogger()

    def register_secret(self, secret_name: str, domain: CredentialDomain, value: str) -> None:
        self.rotation_engine.set_secret(secret_name, domain, value)
        self.audit_logger.record_access(
            secret_name=secret_name,
            domain=domain,
            action="REGISTER",
            actor="SYSTEM",
            success=True
        )

    def acquire_secret_with_lease(self, secret_name: str, domain: CredentialDomain, caller_service: str, ttl_seconds: float = 3600.0) -> tuple[str, SecretLease]:
        """Validates scope, issues a lease, records audit trail, and returns secret value."""
        # 1. Validate Scope
        CredentialScopeValidator.validate_access(caller_service, domain)

        # 2. Fetch Secret Value
        val = self.rotation_engine.get_secret_value(secret_name)
        if not val:
            self.audit_logger.record_access(
                secret_name=secret_name,
                domain=domain,
                action="FETCH",
                actor=caller_service,
                success=False,
                details={"reason": "NOT_FOUND"}
            )
            raise SecretNotFoundError(f"Secret '{secret_name}' not found for domain '{domain.value}'")

        # 3. Issue Lease
        lease = self.lease_manager.issue_lease(secret_name, domain, caller_service, ttl_seconds)

        # 4. Audit
        self.audit_logger.record_access(
            secret_name=secret_name,
            domain=domain,
            action="FETCH_LEASED",
            actor=caller_service,
            success=True,
            details={"lease_id": lease.lease_id, "ttl": ttl_seconds}
        )

        return val, lease
