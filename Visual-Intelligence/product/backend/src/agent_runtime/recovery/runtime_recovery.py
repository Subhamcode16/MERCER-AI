"""
Runtime Recovery & Safe State Restoration.
Ensures session failures recover into fail-closed state without unauthorized privilege elevation.
"""

from typing import Dict, Any
from src.agent_runtime.interfaces.agent_runtime import AgentSession
from src.agent_runtime.errors.exceptions import AuthorityEscalationError


class RuntimeRecoveryManager:
    """Safely recovers faulted agent sessions according to invariant #20."""

    @classmethod
    def recover_session(cls, session: AgentSession, safe_state: Dict[str, Any]) -> AgentSession:
        """
        Restores session to safe verified checkpoint.
        Re-verifies that safe_state does not contain unauthorized authority elevations.
        """
        if safe_state.get("authority_escalated") or safe_state.get("is_admin"):
            raise AuthorityEscalationError(
                worker_id=session.worker_id,
                action="Recovery attempted unauthorized authority elevation."
            )

        # Restore sanitized metadata
        restored_metadata = {
            **session.metadata,
            "recovered": True,
            "recovery_checkpoint": safe_state.get("checkpoint_id", "default_safe"),
            "safe_state": {k: v for k, v in safe_state.items() if not k.startswith("auth_")}
        }

        session.metadata = restored_metadata
        session.is_active = True
        return session
