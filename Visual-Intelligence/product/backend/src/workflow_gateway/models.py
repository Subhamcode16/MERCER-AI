"""
Phase 14 Workflow Gateway Models
-------------------------------
Immutable domain models governing user workflow lifecycle, objectives, plans,
approvals, projections, outcomes, and feedback.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
import time
import hashlib

from src.workflow_gateway.exceptions import (
    InvalidWorkflowRequestError,
    SecretExposureError,
    CrossMissionLeakageError,
)

class WorkflowStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

@dataclass(frozen=True)
class WorkflowObjective:
    title: str
    target_output: str
    target_platforms: List[str]
    max_budget: float

    def __post_init__(self):
        if not self.title or not isinstance(self.title, str) or not self.title.strip():
            raise InvalidWorkflowRequestError("Objective title cannot be empty.")
        if not self.target_output or not isinstance(self.target_output, str) or not self.target_output.strip():
            raise InvalidWorkflowRequestError("Target output cannot be empty.")
        if self.max_budget < 0.0:
            raise InvalidWorkflowRequestError("Max budget cannot be negative.")
        if not self.target_platforms:
            raise InvalidWorkflowRequestError("At least one target platform must be specified.")

@dataclass(frozen=True)
class WorkflowConstraints:
    max_duration_seconds: int = 3600
    require_human_approval: bool = True
    allowed_capabilities: List[str] = field(default_factory=lambda: ["CREATE_DRAFT", "EDIT_DRAFT", "PUBLISH_CONTENT"])
    brand_guidelines_url: Optional[str] = None

    def __post_init__(self):
        if self.max_duration_seconds <= 0:
            raise InvalidWorkflowRequestError("Max duration seconds must be positive.")
        if not self.allowed_capabilities:
            raise InvalidWorkflowRequestError("Allowed capabilities cannot be empty.")
        for cap in self.allowed_capabilities:
            if cap in ("*", "admin", "all", "ALL"):
                raise InvalidWorkflowRequestError(f"Wildcard or admin capability '{cap}' is strictly prohibited.")

@dataclass(frozen=True)
class WorkflowContext:
    workspace_id: str
    user_id: str
    brand_id: str
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not self.workspace_id or not self.user_id or not self.brand_id:
            raise InvalidWorkflowRequestError("Workspace ID, User ID, and Brand ID are required.")

@dataclass(frozen=True)
class WorkflowRequest:
    workflow_id: str
    objective: WorkflowObjective
    constraints: WorkflowConstraints
    context: WorkflowContext
    created_at: float = field(default_factory=time.time)

    def __post_init__(self):
        if not self.workflow_id or not isinstance(self.workflow_id, str):
            raise InvalidWorkflowRequestError("Workflow ID must be a non-empty string.")

@dataclass(frozen=True)
class WorkflowPlanStep:
    step_id: str
    task_name: str
    assigned_role: str
    capability_required: str
    target_platform: str
    requires_authorization: bool
    status: str = "PROPOSED"
    estimated_cost: float = 0.0

@dataclass(frozen=True)
class WorkflowPlan:
    plan_id: str
    workflow_id: str
    mission_id: str
    steps: List[WorkflowPlanStep]
    created_at: float = field(default_factory=time.time)
    review_notes: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class WorkflowApprovalRequest:
    approval_request_id: str
    workflow_id: str
    mission_id: str
    capability: str
    target_resource: str
    action_hash: str
    requires_explicit_human_signature: bool = True
    status: str = "PENDING"
    created_at: float = field(default_factory=time.time)

@dataclass(frozen=True)
class ArtifactView:
    artifact_id: str
    workflow_id: str
    mission_id: str
    task_id: str
    artifact_type: str
    content_summary: str
    lineage_hash: str
    created_at: float
    integrity_commitment: str

    def verify_integrity(self) -> bool:
        expected = hashlib.sha256(
            f"{self.artifact_id}:{self.mission_id}:{self.lineage_hash}".encode("utf-8")
        ).hexdigest()
        return self.integrity_commitment == expected

@dataclass(frozen=True)
class WorkflowView:
    workflow_id: str
    mission_id: str
    status: WorkflowStatus
    objective_title: str
    plan_step_count: int
    completed_steps: int
    pending_approvals: int
    artifacts_generated: int
    created_at: float
    updated_at: float

    def sanitize_check(self) -> None:
        """Verify no sensitive internal credentials appear in view."""
        for field_val in (self.workflow_id, self.mission_id, self.objective_title):
            if any(secret in str(field_val).lower() for secret in ["secret", "bearer", "private_key", "password"]):
                raise SecretExposureError("Potential secret detected in workflow projection!")

@dataclass(frozen=True)
class WorkflowOutcome:
    workflow_id: str
    mission_id: str
    status: WorkflowStatus
    artifacts: List[ArtifactView]
    execution_summary: str
    total_cost: float
    error_message: Optional[str] = None
    completed_at: float = field(default_factory=time.time)

@dataclass(frozen=True)
class FeedbackSubmission:
    feedback_id: str
    workflow_id: str
    mission_id: str
    task_id: str
    user_observation: str
    feedback_type: str
    submitted_at: float = field(default_factory=time.time)

    def __post_init__(self):
        if not self.feedback_id or not self.workflow_id or not self.mission_id:
            raise InvalidWorkflowRequestError("Feedback ID, Workflow ID, and Mission ID are required.")
        if not self.user_observation or not self.user_observation.strip():
            raise InvalidWorkflowRequestError("User observation cannot be empty.")
