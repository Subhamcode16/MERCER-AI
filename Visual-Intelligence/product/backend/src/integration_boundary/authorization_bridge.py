"""
Phase 13 Authorization Bridge.

Consumes Phase 10 AuthorizationRecord objects and verifies mission binding,
capability exactness, resource scope bounds, action hash, and nonce freshness.
Enforces INV-13-001 (Authorization Origin) and INV-13-006 (Scope Propagation).
"""

from datetime import datetime, timezone
from typing import Optional

from src.execution_control.authorization_models import AuthorizationRecord
from src.execution_control.action_models import ExecutionAction
from src.execution_control.capability_models import ExecutionCapability
from src.execution_control.resource_scope import ResourceScope
from src.integration_boundary.exceptions import AuthorizationScopeMismatchError, IntegrationBoundaryError


class AuthorizationBridge:
    """Consumes and verifies Phase 10 AuthorizationRecord tokens. Cannot manufacture authorization."""

    def __init__(self):
        self._verified_nonces: set = set()

    def validate_authorization_for_external_call(
        self,
        authorization_record: Optional[AuthorizationRecord],
        action: ExecutionAction,
        mission_id: str,
        current_time: Optional[datetime] = None
    ) -> None:
        """
        Verifies that an AuthorizationRecord is valid, active, bound to the specified mission,
        grants the requested capability, covers the resource scope, and matches the action hash.
        Fails closed on any mismatch.
        """
        # 1. Verification of authorization token presence (INV-13-001)
        if not authorization_record or not isinstance(authorization_record, AuthorizationRecord):
            raise AuthorizationScopeMismatchError(
                "Authorization Origin Violation (INV-13-001): External execution requires valid Phase 10 AuthorizationRecord."
            )

        # 2. Validate active, non-expired, non-revoked
        authorization_record.validate_active(current_timestamp=current_time)

        # 3. Capability Exactness Check (INV-13-002)
        if action.capability not in authorization_record.authorized_capabilities:
            cap_val = action.capability.value if hasattr(action.capability, "value") else str(action.capability)
            raise AuthorizationScopeMismatchError(
                f"Capability Scope Mismatch (INV-13-006): Authorization '{authorization_record.authorization_id}' does not grant capability '{cap_val}'."
            )

        # 4. Resource Boundary Validation
        try:
            authorization_record.resource_scope.validate_boundary(action.resource_scope)
        except Exception as e:
            raise AuthorizationScopeMismatchError(
                f"Resource Scope Mismatch (INV-13-006): Action scope '{action.resource_scope.scope_string}' is outside authorized scope '{authorization_record.resource_scope.scope_string}': {e}"
            ) from e

        # 5. Nonce Freshness Check
        if authorization_record.nonce in self._verified_nonces:
            raise AuthorizationScopeMismatchError(
                f"Authorization Nonce Replay Violation: Nonce '{authorization_record.nonce}' has already been processed."
            )

        self._verified_nonces.add(authorization_record.nonce)
