"""
Phase 10 — Execution Action & Planned Effect Models

Defines immutable data contracts for executable actions and their planned side-effects.
Enforces fail-closed schema validation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, Optional

from src.execution_control.capability_models import ExecutionCapability, validate_capability_string
from src.execution_control.exceptions import ExecutionControlException
from src.execution_control.resource_scope import ResourceScope


@dataclass(frozen=True)
class PlannedEffect:
    """Description of an intended external side-effect."""

    effect_type: str  # e.g., "CREATE_POST_DRAFT", "PUBLISH_SOCIAL_MEDIA"
    target_system: str  # e.g., "SANDBOX_INSTAGRAM_ADAPTER", "SANDBOX_STORAGE_ADAPTER"
    description: str
    reversible: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "effect_type": self.effect_type,
            "target_system": self.target_system,
            "description": self.description,
            "reversible": self.reversible,
        }


@dataclass(frozen=True)
class ExecutionAction:
    """Immutable contract for a capability-scoped executable action."""

    action_id: str
    workflow_id: str
    task_id: str
    capability: ExecutionCapability
    resource_scope: ResourceScope
    input_payload: Dict[str, Any]
    planned_effect: PlannedEffect
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    expires_at: Optional[str] = None
    input_commitment_hash: str = ""

    def __post_init__(self):
        if isinstance(self.action_id, bool) or not isinstance(self.action_id, str) or not self.action_id.strip():
            raise ExecutionControlException("action_id must be a non-empty string.")
        if isinstance(self.workflow_id, bool) or not isinstance(self.workflow_id, str) or not self.workflow_id.strip():
            raise ExecutionControlException("workflow_id must be a non-empty string.")
        if isinstance(self.task_id, bool) or not isinstance(self.task_id, str) or not self.task_id.strip():
            raise ExecutionControlException("task_id must be a non-empty string.")

        # Validate capability
        if isinstance(self.capability, str):
            object.__setattr__(self, "capability", validate_capability_string(self.capability))

        # Compute commitment hash if empty
        if not self.input_commitment_hash:
            raw_bytes = json.dumps(self.input_payload, sort_keys=True).encode("utf-8")
            h = hashlib.sha256(raw_bytes).hexdigest()
            object.__setattr__(self, "input_commitment_hash", h)

    def is_expired(self, current_timestamp: Optional[datetime] = None) -> bool:
        """Checks if the action has expired."""
        if not self.expires_at:
            return False
        now = current_timestamp or datetime.now(timezone.utc)
        exp = datetime.fromisoformat(self.expires_at)
        return now >= exp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id,
            "capability": self.capability.value,
            "resource_scope": self.resource_scope.scope_string,
            "input_payload": self.input_payload,
            "planned_effect": self.planned_effect.to_dict(),
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "input_commitment_hash": self.input_commitment_hash,
        }
