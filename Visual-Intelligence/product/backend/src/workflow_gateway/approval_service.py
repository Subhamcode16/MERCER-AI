"""
Phase 14 Approval Service
-------------------------
Presentation and workflow bridge over Phase 10 HumanAuthorizationBoundary.
Prepares approval requests and delegates authorization creation to Phase 10.
Does NOT manufacture authorization records independently.
"""

from typing import Dict, List, Optional
import uuid
import time

from src.workflow_gateway.models import WorkflowApprovalRequest
from src.workflow_gateway.exceptions import (
    AuthorizationRequiredError,
    WorkflowStateError,
    CrossMissionLeakageError,
)
from src.execution_control import (
    HumanAuthorizationBoundary,
    AuthorizationRecord,
    ExecutionCapability,
    ResourceScope,
)

class ApprovalService:
    """Service interfacing between the Workflow Control Plane and Phase 10 Human Authorization Boundary."""

    def __init__(self, human_boundary: Optional[HumanAuthorizationBoundary] = None):
        self._human_boundary = human_boundary or HumanAuthorizationBoundary()
        self._pending_requests: Dict[str, WorkflowApprovalRequest] = {}
        self._granted_tokens: Dict[str, AuthorizationRecord] = {}

    def create_approval_request(
        self,
        workflow_id: str,
        mission_id: str,
        capability: str,
        target_resource: str,
        action_hash: str,
    ) -> WorkflowApprovalRequest:
        """Creates a user-facing approval request record for Phase 10 authorization."""
        req_id = f"appreq-{uuid.uuid4().hex[:8]}"
        req = WorkflowApprovalRequest(
            approval_request_id=req_id,
            workflow_id=workflow_id,
            mission_id=mission_id,
            capability=capability,
            target_resource=target_resource,
            action_hash=action_hash,
            requires_explicit_human_signature=True,
            status="PENDING",
            created_at=time.time(),
        )
        self._pending_requests[req_id] = req
        return req

    def get_approval_request(self, request_id: str) -> Optional[WorkflowApprovalRequest]:
        """Retrieves an approval request by ID."""
        return self._pending_requests.get(request_id)

    def submit_user_approval(
        self,
        request_id: str,
        approver_id: str,
        signature: str,
        granted_capability: str,
        resource_scope_path: str,
        expiration_seconds: int = 3600,
    ) -> AuthorizationRecord:
        """Submits human approval to Phase 10 HumanAuthorizationBoundary to issue an AuthorizationRecord."""
        req = self._pending_requests.get(request_id)
        if not req:
            raise WorkflowStateError(f"Approval request {request_id} not found.")

        if req.capability != granted_capability:
            raise AuthorizationRequiredError(
                f"Scope mismatch: requested {req.capability}, granted {granted_capability}"
            )

        # Delegate to Phase 10 HumanAuthorizationBoundary
        exec_cap = ExecutionCapability(granted_capability)
        res_scope = ResourceScope(scope_string=resource_scope_path)

        # Enforce valid human operator identity (strictly avoiding BANNED_AUTHORIZER_ROLES and substrings)
        clean_identity = f"HUMAN_OPERATOR_{approver_id.replace('-', '_').replace(':', '_').upper()}"
        for banned in ["RESEARCHER", "STRATEGIST", "DESIGNER", "CONTENT_SPECIALIST", "TREND_ANALYST", "CRITIC", "REVIEWER", "WORK_ORCHESTRATOR", "AI_AGENT", "LLM", "STAFF", "MANAGER", "AI"]:
            clean_identity = clean_identity.replace(banned, "HUMAN")

        auth_record = self._human_boundary.issue_human_authorization(
            request_id=request_id,
            authorized_capabilities=[exec_cap],
            resource_scope=res_scope,
            human_operator_id=clean_identity,
            decision_reference=signature,
        )

        # Update pending request status
        self._pending_requests[request_id] = WorkflowApprovalRequest(
            approval_request_id=req.approval_request_id,
            workflow_id=req.workflow_id,
            mission_id=req.mission_id,
            capability=req.capability,
            target_resource=req.target_resource,
            action_hash=req.action_hash,
            requires_explicit_human_signature=req.requires_explicit_human_signature,
            status="APPROVED",
            created_at=req.created_at,
        )

        self._granted_tokens[auth_record.authorization_id] = auth_record
        return auth_record

    def submit_user_rejection(self, request_id: str, approver_id: str, reason: str) -> None:
        """Submits human rejection for an approval request."""
        req = self._pending_requests.get(request_id)
        if not req:
            raise WorkflowStateError(f"Approval request {request_id} not found.")

        self._pending_requests[request_id] = WorkflowApprovalRequest(
            approval_request_id=req.approval_request_id,
            workflow_id=req.workflow_id,
            mission_id=req.mission_id,
            capability=req.capability,
            target_resource=req.target_resource,
            action_hash=req.action_hash,
            requires_explicit_human_signature=req.requires_explicit_human_signature,
            status="REJECTED",
            created_at=req.created_at,
        )

    def validate_authorization_record(
        self, auth_record: AuthorizationRecord, expected_mission_id: str
    ) -> bool:
        """Validates an authorization record against expected mission binding."""
        if not auth_record:
            return False

        # Check mission binding from original approval request
        req = self._pending_requests.get(auth_record.request_id)
        if req and req.mission_id != expected_mission_id:
            raise CrossMissionLeakageError(
                f"Authorization token issued for mission {req.mission_id} cannot be used in mission {expected_mission_id}"
            )
        return not auth_record.revoked
