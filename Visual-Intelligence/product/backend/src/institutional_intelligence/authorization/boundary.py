"""
Human Decision Boundary & Authorization Module (Phase 30).
Enforces explicit, bounded human decision capture and prevents stale approval replay or spoofing.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import uuid
import hashlib
from ..types import ThreatID, GovernanceInvariantViolation, utc_now


class HumanAuthorizationToken(BaseModel):
    token_id: str = Field(default_factory=lambda: f"auth_{uuid.uuid4().hex[:16]}")
    actor_id: str
    tenant_id: str
    decision_id: str
    scope: str
    issued_at: datetime = Field(default_factory=utc_now)
    expires_at: datetime = Field(default_factory=lambda: utc_now() + timedelta(hours=24))
    is_consumed: bool = False
    nonce: str = Field(default_factory=lambda: uuid.uuid4().hex)

    def is_valid(self) -> bool:
        return not self.is_consumed and utc_now() <= self.expires_at


class HumanDecisionBoundaryService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._tokens: Dict[str, HumanAuthorizationToken] = {}

    def issue_authorization(self, actor_id: str, decision_id: str, scope: str, valid_hours: int = 24) -> HumanAuthorizationToken:
        token = HumanAuthorizationToken(
            actor_id=actor_id,
            tenant_id=self.tenant_id,
            decision_id=decision_id,
            scope=scope,
            expires_at=utc_now() + timedelta(hours=valid_hours)
        )
        self._tokens[token.token_id] = token
        return token

    def validate_and_consume(self, token_id: str, requested_scope: str) -> bool:
        token = self._tokens.get(token_id)
        if not token:
            raise GovernanceInvariantViolation(
                ThreatID.T30_021,
                "Authorization token does not exist.",
                {"token_id": token_id}
            )
        
        # T30-022: Stale approval replay prevention
        if token.is_consumed:
            raise GovernanceInvariantViolation(
                ThreatID.T30_022,
                f"Authorization token '{token_id}' has already been consumed and cannot be replayed.",
                {"token_id": token_id}
            )
        
        if utc_now() > token.expires_at:
            raise GovernanceInvariantViolation(
                ThreatID.T30_022,
                f"Authorization token '{token_id}' has expired.",
                {"token_id": token_id, "expired_at": token.expires_at.isoformat()}
            )

        if token.scope != requested_scope and token.scope != "GLOBAL_ADMIN":
            raise GovernanceInvariantViolation(
                ThreatID.T30_003,
                f"Authorization token scope '{token.scope}' does not match requested scope '{requested_scope}'.",
                {"token_id": token_id, "token_scope": token.scope, "requested_scope": requested_scope}
            )

        token.is_consumed = True
        return True
