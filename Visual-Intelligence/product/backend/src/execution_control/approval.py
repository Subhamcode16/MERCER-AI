"""
Phase 10 — Approval Boundary & Human Authorization Interface

Defines the ApprovalState lifecycle and the HumanAuthorizationBoundary interface.
Enforces the fundamental security invariant: AI Review != Human Authorization != Execution.
"""

from enum import Enum
from typing import List, Optional

from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.exceptions import SelfAuthorizationAttemptError
from src.execution_control.resource_scope import ResourceScope


class ApprovalState(str, Enum):
    APPROVED_FOR_REVIEW = "APPROVED_FOR_REVIEW"
    APPROVED_FOR_DRY_RUN = "APPROVED_FOR_DRY_RUN"
    AUTHORIZED_FOR_EXECUTION = "AUTHORIZED_FOR_EXECUTION"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class HumanAuthorizationBoundary:
    """Explicit human-in-the-loop authorization boundary."""

    def __init__(self):
        pass

    def issue_human_authorization(
        self,
        request_id: str,
        authorized_capabilities: List[ExecutionCapability],
        resource_scope: ResourceScope,
        human_operator_id: str,
        decision_reference: str,
        expires_at: Optional[str] = None,
    ) -> AuthorizationRecord:
        """Issues an explicit human authorization record."""
        # Assert that human_operator_id is not an AI worker
        if "AI" in human_operator_id.upper() or "STAFF" in human_operator_id.upper() or "REVIEWER" in human_operator_id.upper():
            raise SelfAuthorizationAttemptError(
                f"Identity '{human_operator_id}' cannot issue human execution authorization."
            )

        auth_record = AuthorizationRecord(
            authorization_id=f"auth_{request_id}",
            request_id=request_id,
            authorized_capabilities=authorized_capabilities,
            resource_scope=resource_scope,
            authorizer_identity=human_operator_id,
            decision_reference=decision_reference,
            expires_at=expires_at,
        )

        return auth_record
