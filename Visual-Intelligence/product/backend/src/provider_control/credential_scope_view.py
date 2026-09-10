"""
Phase 25 Masked Credential Scope and Secret Lease Inspector.
Enforces zero secret leakage to operator UI.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class CredentialScopeDTO:
    provider: str
    scope_name: str
    is_configured: bool
    masked_fingerprint: str # e.g. "***REDACTED***"
    lease_expires_at: Optional[float] = None
    last_rotated_at: Optional[float] = None

class CredentialScopeViewer:
    @staticmethod
    def get_masked_credential_scopes(configured_providers: List[str]) -> List[CredentialScopeDTO]:
        return [
            CredentialScopeDTO(
                provider=p,
                scope_name=f"scope:{p.lower()}:production",
                is_configured=True,
                masked_fingerprint="***REDACTED***"
            )
            for p in configured_providers
        ]
