"""
Phase 10 — Execution Controller Pipeline

Coordinates validated, capability-constrained action execution through registered sandbox adapters.
Enforces human authorization checks, resource boundary validation, idempotency guards, and execution ledger logging.
"""

from datetime import datetime, timezone
import uuid
from typing import Dict, List, Optional

from src.execution_control.action_models import ExecutionAction
from src.execution_control.adapters import AdapterExecutionResult, BaseSandboxAdapter
from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import (
    AdapterNotFoundError,
    CapabilityViolationError,
    PartialExecutionError,
)
from src.execution_control.execution_ledger import ExecutionLedger, ExecutionLedgerRecord
from src.execution_control.execution_policy import ExecutionPolicyEngine
from src.execution_control.idempotency import IdempotencyGuard


class ExecutionController:
    """Bounded operational execution controller."""

    def __init__(
        self,
        policy_engine: Optional[ExecutionPolicyEngine] = None,
        idempotency_guard: Optional[IdempotencyGuard] = None,
        ledger: Optional[ExecutionLedger] = None,
    ):
        self.policy_engine = policy_engine or ExecutionPolicyEngine()
        self.idempotency_guard = idempotency_guard or IdempotencyGuard()
        self.ledger = ledger or ExecutionLedger()
        self._adapters: Dict[ExecutionCapability, BaseSandboxAdapter] = {}

    def register_adapter(self, adapter: BaseSandboxAdapter) -> None:
        """Registers a sandbox integration adapter for its supported capabilities."""
        for cap in adapter.supported_capabilities():
            self._adapters[cap] = adapter

    def execute_action(
        self,
        action: ExecutionAction,
        authorization_record: Optional[AuthorizationRecord] = None,
    ) -> AdapterExecutionResult:
        """Executes a single action after full policy, authorization, scope, and idempotency checks."""
        start_time = datetime.now(timezone.utc).isoformat()

        # 1. Policy & Schema Validation
        self.policy_engine.validate_action_policy(action)

        # 2. Expiry Check
        if action.is_expired():
            raise ValueError(f"Action '{action.action_id}' has expired.")

        # 3. Human Authorization Check (if required by policy)
        if self.policy_engine.requires_human_authorization(action.capability):
            if not authorization_record:
                raise PermissionError(
                    f"Action '{action.action_id}' (Capability: {action.capability.value}) requires explicit human authorization record."
                )

            # Validate active & non-expired & non-revoked
            authorization_record.validate_active()

            # Validate capability match
            if action.capability not in authorization_record.authorized_capabilities:
                raise CapabilityViolationError(
                    f"Authorization '{authorization_record.authorization_id}' does not grant capability '{action.capability.value}'."
                )

            # Validate resource boundary
            authorization_record.resource_scope.validate_boundary(action.resource_scope)

            # Check authorization nonce replay
            self.idempotency_guard.check_and_record_authorization(authorization_record)

        # 4. Action Idempotency Check
        self.idempotency_guard.check_and_record_action(action)

        # 5. Adapter Lookup
        adapter = self._adapters.get(action.capability)
        if not adapter:
            raise AdapterNotFoundError(
                f"No integration adapter registered for capability '{action.capability.value}'."
            )

        # 6. Sandbox Execution
        try:
            result = adapter.execute_action(action)
            end_time = datetime.now(timezone.utc).isoformat()
            status_str = "SUCCESS" if result.success else "FAILED"
            err_msg = result.error_message
            output_data = result.output_data
        except Exception as e:
            end_time = datetime.now(timezone.utc).isoformat()
            status_str = "FAILED"
            err_msg = str(e)
            output_data = {}
            result = AdapterExecutionResult(
                transaction_id=f"tx_err_{uuid.uuid4().hex[:6]}",
                action_id=action.action_id,
                capability=action.capability,
                success=False,
                output_data={},
                error_message=err_msg,
            )

        # 7. Execution Ledger Record
        ledger_rec = ExecutionLedgerRecord(
            execution_id=f"exec_{uuid.uuid4().hex[:8]}",
            action_id=action.action_id,
            workflow_id=action.workflow_id,
            authorization_id=authorization_record.authorization_id if authorization_record else None,
            capability=action.capability,
            resource_scope=action.resource_scope.scope_string,
            decision_reference=authorization_record.decision_reference if authorization_record else "NO_AUTH_REQUIRED",
            start_time=start_time,
            end_time=end_time,
            status=status_str,
            output_summary=output_data,
            error_message=err_msg,
        )
        self.ledger.record_execution(ledger_rec)

        return result

    def execute_batch(
        self,
        actions: List[ExecutionAction],
        authorization_record: Optional[AuthorizationRecord] = None,
    ) -> List[AdapterExecutionResult]:
        """Executes a list of actions sequentially with partial execution halting on failure."""
        results: List[AdapterExecutionResult] = []

        for idx, action in enumerate(actions):
            try:
                res = self.execute_action(action, authorization_record)
                results.append(res)
                if not res.success:
                    raise PartialExecutionError(
                        f"Action {idx + 1}/{len(actions)} ('{action.action_id}') failed: {res.error_message}"
                    )
            except Exception as e:
                if not isinstance(e, PartialExecutionError):
                    raise PartialExecutionError(
                        f"Action {idx + 1}/{len(actions)} ('{action.action_id}') raised exception: {str(e)}"
                    ) from e
                raise

        return results
