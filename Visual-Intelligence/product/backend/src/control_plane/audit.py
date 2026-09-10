"""
Phase 25 Immutable Operator Audit Trail.
"""
import logging
from typing import List, Optional
from src.control_plane.models import ControlPlaneAuditEvent

logger = logging.getLogger(__name__)

class ControlPlaneAuditLogger:
    """Records operator interactions into an append-only audit log."""

    def __init__(self):
        self._audit_log: List[ControlPlaneAuditEvent] = []

    def record_event(self, event: ControlPlaneAuditEvent) -> None:
        self._audit_log.append(event)
        logger.info(
            f"[AUDIT] Operator={event.operator_id} Tenant={event.tenant_id} Action={event.action} "
            f"Resource={event.target_resource} Status={event.status}"
        )

    def query_audit_events(
        self,
        tenant_id: str,
        client_id: Optional[str] = None,
        limit: int = 100
    ) -> List[ControlPlaneAuditEvent]:
        res = []
        for ev in reversed(self._audit_log):
            if tenant_id == "*" or ev.tenant_id == tenant_id:
                if client_id is None or client_id == "*" or ev.client_id == client_id:
                    res.append(ev)
            if len(res) >= limit:
                break
        return list(reversed(res))
