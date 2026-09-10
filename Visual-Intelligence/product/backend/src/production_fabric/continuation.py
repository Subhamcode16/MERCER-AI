"""
Phase 17 Bounded Continuation Engine.
Determines permissible operational continuation steps under explicit policy rules.
Enforces INV-17-003: Autonomy = Bounded Continuation Under Explicit Policy (Autonomy != Self Authorization).
"""

from typing import Dict, Any, Optional
from src.production_fabric.production_models import ProductionWorkItem, ProductionState
from src.production_fabric.exceptions import ContinuationBoundaryError, FabricPolicyViolation

class BoundedContinuationEngine:
    """Engine validating operational continuation criteria before advancing production steps."""

    def evaluate_continuation(
        self,
        item: ProductionWorkItem,
        autonomy_tier: int,
        requires_approval: bool,
        has_valid_approval: bool,
        studio_orchestrator: Any
    ) -> str:
        """
        Evaluates whether item can proceed to next step.
        Returns next recommended step name or raises ContinuationBoundaryError.
        """
        # Tier 0: Observe only
        if autonomy_tier == 0:
            raise ContinuationBoundaryError("Autonomy Tier 0 restricts system to observation only.")

        # Check client context validity
        client = studio_orchestrator.client_manager.get_client(item.client_id, item.client_id)
        if not client or client.status != "ACTIVE":
            raise ContinuationBoundaryError(f"Client engagement '{item.client_id}' is inactive or invalid.")

        # Check if item is blocked or failed
        if item.state in (ProductionState.BLOCKED, ProductionState.FAILED):
            raise ContinuationBoundaryError(f"Work item '{item.item_id}' is in blocked/failed state '{item.state.value}'.")

        # If operation requires approval and no valid approval is present, request approval unless already ready for execution
        if requires_approval and not has_valid_approval and item.state != ProductionState.READY_FOR_EXECUTION:
            if autonomy_tier < 1:
                raise ContinuationBoundaryError("Approval required but autonomy tier prohibits preparing approval package.")
            return "REQUEST_APPROVAL"

        # State transition determination
        if item.state == ProductionState.ADMITTED:
            return "START_PRODUCTION"
        elif item.state == ProductionState.IN_PRODUCTION:
            return "SUBMIT_CRITIQUE"
        elif item.state == ProductionState.CRITIQUE:
            return "SUBMIT_REVIEW"
        elif item.state == ProductionState.REVIEW:
            return "REQUEST_APPROVAL" if requires_approval else "MARK_APPROVED"
        elif item.state == ProductionState.AWAITING_APPROVAL:
            if not has_valid_approval:
                raise ContinuationBoundaryError("Item is awaiting approval and has not been approved.")
            return "MARK_APPROVED"
        elif item.state == ProductionState.APPROVED:
            return "PREPARE_EXECUTION"
        elif item.state == ProductionState.READY_FOR_EXECUTION:
            if not has_valid_approval:
                raise ContinuationBoundaryError("Ready for execution requires explicit Phase 10 approval token.")
            return "DISPATCH_EXECUTION"
        elif item.state == ProductionState.EXECUTING:
            return "OBSERVE_OUTCOME"
        elif item.state == ProductionState.OBSERVING:
            return "TRIGGER_LEARNING"
        elif item.state == ProductionState.LEARNING:
            return "COMPLETE_RUN"

        return "HALT"
