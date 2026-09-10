"""
Phase 25 Operator Console Session Manager and Token Lifecycle.
"""
import time
import uuid
from typing import Dict, Optional, List, Any
from src.control_plane.models import OperatorIdentity, OperatorRole
from src.control_plane.exceptions import OperatorSessionExpiredError

class OperatorSessionManager:
    """Manages active operator sessions with strict TTL expiration."""

    def __init__(self, default_ttl_seconds: float = 3600.0):
        self.default_ttl = default_ttl_seconds
        self._active_sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, identity: OperatorIdentity) -> str:
        session_id = f"sess-{uuid.uuid4().hex[:16]}"
        now = time.time()
        self._active_sessions[session_id] = {
            "session_id": session_id,
            "operator_id": identity.operator_id,
            "tenant_scope": identity.tenant_scope,
            "allowed_clients": identity.allowed_clients,
            "roles": identity.roles,
            "created_at": now,
            "expires_at": now + self.default_ttl
        }
        return session_id

    def validate_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self._active_sessions:
            raise OperatorSessionExpiredError(f"Session '{session_id}' not found or terminated.")

        sess = self._active_sessions[session_id]
        if time.time() > sess["expires_at"]:
            del self._active_sessions[session_id]
            raise OperatorSessionExpiredError(f"Session '{session_id}' has expired.")

        return sess

    def terminate_session(self, session_id: str) -> None:
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]
