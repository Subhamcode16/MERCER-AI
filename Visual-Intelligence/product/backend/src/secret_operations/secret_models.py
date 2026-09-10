"""
Phase 23 Secret Models and Scoped Credential Definitions.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List
import time
import hashlib

class CredentialDomain(str, Enum):
    LLM = "LLM"
    VISION = "VISION"
    MCP = "MCP"
    DATABASE = "DATABASE"
    STORAGE = "STORAGE"
    NOTIFICATION = "NOTIFICATION"
    OBSERVABILITY = "OBSERVABILITY"
    DEPLOYMENT = "DEPLOYMENT"

@dataclass
class SecretMetadata:
    secret_name: str
    domain: CredentialDomain
    version: int
    created_at: float
    last_rotated_at: float
    fingerprint: str
    is_active: bool = True

@dataclass
class SecretLease:
    lease_id: str
    secret_name: str
    domain: CredentialDomain
    consumer_service: str
    created_at: float
    expires_at: float
    is_revoked: bool = False

    def is_valid(self) -> bool:
        return not self.is_revoked and time.time() < self.expires_at

@dataclass
class SecretAuditRecord:
    audit_id: str
    secret_name: str
    domain: CredentialDomain
    action: str  # FETCH, ROTATE, REVOKE, LEASE
    actor: str
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)
