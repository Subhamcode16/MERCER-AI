"""
Phase 25 Human Approval Projection and Risk Rating Models.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

@dataclass
class HumanApprovalItem:
    approval_id: str
    tenant_id: str
    client_id: str
    campaign_id: str
    requested_operation: str
    scope: str
    risk_rating: str # LOW, MEDIUM, HIGH, CRITICAL
    requester_role: str
    requester_id: str
    evidence_bundle_id: str
    status: str # PENDING, APPROVED, REJECTED, EXPIRED, REVOKED
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    version: int = 1
    decision_reason: Optional[str] = None
    authorized_by: Optional[str] = None
    authorized_at: Optional[float] = None
    execution_token_id: Optional[str] = None
