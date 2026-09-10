"""
Phase 25 Authenticated Operator Context.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import time
import uuid
from src.control_plane.models import OperatorRole
from src.control_plane.exceptions import TenantContextMissingError


@dataclass
class OperatorContext:
    """Carries authenticated operator context across control plane calls."""
    operator_id: str
    tenant_id: str = "tenant_default"
    client_id: str = "cli_default"
    roles: List[OperatorRole] = field(default_factory=list)
    role: Optional[OperatorRole] = None
    department: str = "Creative Direction"
    session_id: str = field(default_factory=lambda: f"sess-{uuid.uuid4().hex[:10]}")
    correlation_id: str = field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:10]}")
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if self.role and not self.roles:
            self.roles = [self.role]
        elif self.roles and not self.role:
            self.role = self.roles[0]

    def validate(self) -> None:
        """Fails closed if essential context fields are missing."""
        if not self.operator_id or not self.operator_id.strip():
            raise TenantContextMissingError("Missing mandatory operator_id in OperatorContext.")
        if not self.tenant_id or not self.tenant_id.strip():
            raise TenantContextMissingError("Missing mandatory tenant_id in OperatorContext.")
        if not self.roles and not self.role:
            raise TenantContextMissingError("Missing mandatory roles in OperatorContext.")
