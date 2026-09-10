"""
Phase 25 Governed Provider & Circuit Breaker Actions.
"""
from typing import Dict, Any, Optional
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorCapability, ControlPlaneAuditEvent
from src.control_plane.permissions import PermissionGuard
from src.control_plane.audit import ControlPlaneAuditLogger

class ProviderActionHandler:
    """Handles SRE-governed actions on provider circuit breakers and health probes."""

    def __init__(self, audit_logger: Optional[ControlPlaneAuditLogger] = None):
        self.audit_logger = audit_logger or ControlPlaneAuditLogger()

    def reset_circuit_breaker(self, context: OperatorContext, provider_name: str, reason: str) -> Dict[str, Any]:
        PermissionGuard.enforce_capability(context, OperatorCapability.MANAGE_CIRCUIT_BREAKER)

        self.audit_logger.record_event(ControlPlaneAuditEvent(
            operator_id=context.operator_id,
            tenant_id=context.tenant_id,
            client_id=context.client_id,
            action="RESET_CIRCUIT_BREAKER",
            target_resource=provider_name,
            correlation_id=context.correlation_id,
            details={"reason": reason}
        ))

        return {
            "provider": provider_name,
            "status": "RESET_TO_HALF_OPEN",
            "message": f"Circuit breaker for provider '{provider_name}' reset to HALF_OPEN for health probing."
        }
