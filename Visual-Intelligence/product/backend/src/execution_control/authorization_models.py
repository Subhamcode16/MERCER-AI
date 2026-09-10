"""
Phase 10 — Authorization Models & Tokens

Defines immutable data contracts for explicit human authorization records.
Enforces nonces, time-bounds, resource scope constraints, and revocation tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional

from src.execution_control.capability_models import ExecutionCapability, validate_capability_string
from src.execution_control.exceptions import (
    AuthorizationExpiredError,
    AuthorizationRevokedError,
    SelfAuthorizationAttemptError,
)
from src.execution_control.resource_scope import ResourceScope


# Forbidden AI Staff Authorizer Identities
BANNED_AUTHORIZER_ROLES = {
    "RESEARCHER",
    "STRATEGIST",
    "DESIGNER",
    "CONTENT_SPECIALIST",
    "TREND_ANALYST",
    "CRITIC",
    "REVIEWER",
    "WORK_ORCHESTRATOR",
    "AI_AGENT",
    "LLM",
}


@dataclass(frozen=True)
class AuthorizationRecord:
    """Immutable contract representing explicit human authorization to execute capabilities."""

    authorization_id: str
    request_id: str
    authorized_capabilities: List[ExecutionCapability]
    resource_scope: ResourceScope
    authorizer_identity: str  # e.g., "HUMAN_OPERATOR_USER_01"
    decision_reference: str
    issued_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    expires_at: Optional[str] = None
    nonce: str = field(default_factory=lambda: str(uuid.uuid4()))
    revoked: bool = False

    def __post_init__(self):
        # Validate that authorizer identity is NOT an AI staff member
        upper_authorizer = self.authorizer_identity.upper().strip()
        if any(banned in upper_authorizer for banned in BANNED_AUTHORIZER_ROLES):
            raise SelfAuthorizationAttemptError(
                f"Self-Authorization Violation: AI staff role '{self.authorizer_identity}' cannot issue execution authorization."
            )

        # Validate capability strings
        validated_caps = []
        for cap in self.authorized_capabilities:
            if isinstance(cap, str):
                validated_caps.append(validate_capability_string(cap))
            else:
                validated_caps.append(cap)
        object.__setattr__(self, "authorized_capabilities", validated_caps)

    def validate_active(self, current_timestamp: Optional[datetime] = None) -> None:
        """Validates that authorization is not revoked and not expired."""
        if self.revoked:
            raise AuthorizationRevokedError(
                f"Authorization '{self.authorization_id}' has been revoked."
            )

        if self.expires_at:
            now = current_timestamp or datetime.now(timezone.utc)
            exp = datetime.fromisoformat(self.expires_at)
            if now >= exp:
                raise AuthorizationExpiredError(
                    f"Authorization '{self.authorization_id}' expired at {self.expires_at}."
                )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authorization_id": self.authorization_id,
            "request_id": self.request_id,
            "authorized_capabilities": [c.value for c in self.authorized_capabilities],
            "resource_scope": self.resource_scope.scope_string,
            "authorizer_identity": self.authorizer_identity,
            "decision_reference": self.decision_reference,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "nonce": self.nonce,
            "revoked": self.revoked,
        }
