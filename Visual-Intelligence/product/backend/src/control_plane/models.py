"""
Phase 25 Control Plane Core Models, Roles, and Capabilities.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time
import uuid

class OperatorRole(str, Enum):
    LEAD_CURATOR = "LEAD_CURATOR"
    CREATIVE_DIRECTOR = "CREATIVE_DIRECTOR"
    BRAND_STRATEGIST = "BRAND_STRATEGIST"
    SRE_ENGINEER = "SRE_ENGINEER"
    STUDIO_ADMIN = "STUDIO_ADMIN"
    READ_ONLY_VIEWER = "READ_ONLY_VIEWER"
    BRAND_EXECUTIVE = "BRAND_EXECUTIVE"
    STUDIO_LEAD = "STUDIO_LEAD"
    SUPER_ADMIN = "SUPER_ADMIN"
    STAFF_OPERATOR = "STAFF_OPERATOR"
    CLIENT_VIEWER = "CLIENT_VIEWER"

class OperatorCapability(str, Enum):
    VIEW_CLIENT = "VIEW_CLIENT"
    VIEW_CAMPAIGN = "VIEW_CAMPAIGN"
    VIEW_DELIVERABLE = "VIEW_DELIVERABLE"
    VIEW_INTELLIGENCE = "VIEW_INTELLIGENCE"
    VIEW_RELIABILITY = "VIEW_RELIABILITY"
    VIEW_EVIDENCE = "VIEW_EVIDENCE"
    SUBMIT_FEEDBACK = "SUBMIT_FEEDBACK"
    REQUEST_APPROVAL = "REQUEST_APPROVAL"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REVOKE_APPROVAL = "REVOKE_APPROVAL"
    TRIGGER_REVIEW = "TRIGGER_REVIEW"
    OPERATE_CAMPAIGN = "OPERATE_CAMPAIGN"
    VIEW_PROVIDER_HEALTH = "VIEW_PROVIDER_HEALTH"
    VIEW_COST = "VIEW_COST"
    MANAGE_CIRCUIT_BREAKER = "MANAGE_CIRCUIT_BREAKER"
    TRIGGER_RECOVERY_DRILL = "TRIGGER_RECOVERY_DRILL"

@dataclass
class OperatorIdentity:
    operator_id: str
    username: str
    roles: List[OperatorRole]
    tenant_scope: str # e.g. "tenant_atelier", or "*" for system admin
    allowed_clients: List[str]
    email: Optional[str] = None
    created_at: float = field(default_factory=time.time)

@dataclass
class ControlPlaneAuditEvent:
    event_id: str = field(default_factory=lambda: f"aud-{uuid.uuid4().hex[:10]}")
    timestamp: float = field(default_factory=time.time)
    operator_id: str = ""
    tenant_id: str = ""
    client_id: str = ""
    action: str = ""
    target_resource: str = ""
    correlation_id: str = ""
    status: str = "SUCCESS" # SUCCESS, DENIED, ERROR
    details: Dict[str, Any] = field(default_factory=dict)
