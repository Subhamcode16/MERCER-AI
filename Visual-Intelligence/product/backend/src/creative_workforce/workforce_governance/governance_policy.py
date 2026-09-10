"""
Phase 26 Workforce Governance & Invariant Validation Policy.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from src.creative_workforce.worker_identity.models import WorkerIdentity, WorkerStatus


class GovernanceViolation(Exception):
    pass


class WorkforceGovernance:
    """Enforces non-negotiable architectural invariants and fail-closed governance checks."""

    @staticmethod
    def validate_execution_boundary(
        worker: WorkerIdentity,
        action_name: str,
        is_human_approved: bool,
        requires_human_approval: bool,
    ) -> None:
        # Invariant 4.13: Human Approval Must Remain Explicit
        if requires_human_approval and not is_human_approved:
            raise GovernanceViolation(
                f"Action '{action_name}' requires explicit human approval. Worker '{worker.worker_id}' cannot execute autonomously."
            )

        # Invariant 4.14: Fail Closed if worker is inactive
        if worker.status != WorkerStatus.ACTIVE:
            raise GovernanceViolation(
                f"Governance Fail-Closed: Worker '{worker.worker_id}' is in non-active state '{worker.status.value}'"
            )

    @staticmethod
    def validate_delegation_safety(sender_id: str, recipient_id: str, current_chain: List[str]) -> None:
        # Invariant 4.5: Collaboration != Privilege Transfer
        if recipient_id in current_chain:
            raise GovernanceViolation(f"Delegation loop detected with worker '{recipient_id}'")
