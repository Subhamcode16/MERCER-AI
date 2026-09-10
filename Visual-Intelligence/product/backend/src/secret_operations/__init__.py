"""
Phase 23 Secret & Credential Operations Package.
"""
from src.secret_operations.exceptions import (
    SecretOperationError,
    SecretNotFoundError,
    SecretRotationError,
    LeaseExpiredError,
    UnauthorizedScopeError,
    SecretLeakageDetected
)
from src.secret_operations.secret_models import (
    CredentialDomain,
    SecretMetadata,
    SecretLease,
    SecretAuditRecord
)
from src.secret_operations.credential_scope import CredentialScopeValidator
from src.secret_operations.redaction import SecretRedactionEngine
from src.secret_operations.lease import SecretLeaseManager
from src.secret_operations.rotation import SecretRotationEngine
from src.secret_operations.audit import SecretAuditLogger
from src.secret_operations.secret_provider import ProductionSecretProvider

__all__ = [
    "SecretOperationError",
    "SecretNotFoundError",
    "SecretRotationError",
    "LeaseExpiredError",
    "UnauthorizedScopeError",
    "SecretLeakageDetected",
    "CredentialDomain",
    "SecretMetadata",
    "SecretLease",
    "SecretAuditRecord",
    "CredentialScopeValidator",
    "SecretRedactionEngine",
    "SecretLeaseManager",
    "SecretRotationEngine",
    "SecretAuditLogger",
    "ProductionSecretProvider"
]
