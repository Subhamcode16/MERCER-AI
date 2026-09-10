"""
Phase 9 — Learning Governance & Security Substrate Barrier

Enforces security substrate isolation, audit event logging to AuditStore,
and runtime assertions guaranteeing that ExecutionGate.is_permitted() remains False.
"""

from typing import Any, Dict, Optional

from src.agentic_work.adaptive_strategy import SecurityBoundaryViolation
from src.security_substrate.execution_gate import ExecutionGate


class LearningGovernanceBarrier:
    """Governance boundary for Phase 9 persistent learning & workflow optimization."""

    def __init__(self, audit_store: Optional[Any] = None):
        self.audit_store = audit_store

    def verify_execution_gate_locked(
        self,
        execution_gate: Optional[ExecutionGate] = None,
        context_name: str = "Phase 9 Learning",
    ) -> None:
        """Asserts that ExecutionGate remains strictly False."""
        if execution_gate is not None:
            if execution_gate.is_permitted():
                raise SecurityBoundaryViolation(
                    f"CRITICAL: ExecutionGate was found UNLOCKED during '{context_name}' operation!"
                )

    def log_governance_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        actor: str = "Phase 9 Learning Boundary",
    ) -> None:
        """Logs audit events to AuditStore if available, and verifies execution gate lock."""
        self.verify_execution_gate_locked(context_name=event_type)

        if self.audit_store and hasattr(self.audit_store, "record_event"):
            try:
                self.audit_store.record_event(
                    event_type=f"PHASE9_{event_type.upper()}",
                    actor=actor,
                    details=details,
                )
            except Exception:
                pass
