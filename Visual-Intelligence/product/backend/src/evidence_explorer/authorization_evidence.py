"""
Phase 25 Human Authorization Cryptographic Evidence Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class AuthorizationEvidenceRecord:
    authorization_id: str
    campaign_id: str
    tenant_id: str
    client_id: str
    grantee_role: str
    granted_by: str
    valid_until_epoch: float
    signature_sha256: str
    execution_token_id: str
    is_valid: bool
