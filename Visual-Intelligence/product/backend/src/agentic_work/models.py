"""
IF-AGENT-001 Agentic Work Orchestration & Real Workflow Models.
Defines schemas for staff roles, tasks, results, context scopes, critique/review outputs,
learning signals, adaptive changes, and visual observations.
Enforces type safety, non-authoritative flags, and fail-closed validation.
"""

import time
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set


class StaffRole(str, Enum):
    """
    Standard composable AI Staff Roles.
    Workers carry zero security-gating or authorization privileges.
    """
    RESEARCHER = "RESEARCHER"
    STRATEGIST = "STRATEGIST"
    DESIGNER = "DESIGNER"
    CONTENT_SPECIALIST = "CONTENT_SPECIALIST"
    TREND_ANALYST = "TREND_ANALYST"
    CRITIC = "CRITIC"
    REVIEWER = "REVIEWER"


class TaskStatus(str, Enum):
    """
    Lifecycle status tracking for workflow graph tasks.
    """
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"


class AdaptiveStatus(str, Enum):
    """
    Lifecycle status tracking for versioned adaptive changes.
    """
    PROPOSED = "PROPOSED"
    EVALUATING = "EVALUATING"
    ACCEPTED = "ACCEPTED"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


class BANNED_STAFF_TERMS(str, Enum):
    AUTHORIZE = "AUTHORIZE"
    UNLOCK = "UNLOCK"
    PERMIT = "PERMIT"
    EXECUTE_SECURITY = "EXECUTE_SECURITY"


@dataclass
class StaffCapability:
    """
    Explicit capability boundary assigned to a staff profile.
    """
    capability_id: str
    description: str
    allowed_tools: List[str]
    max_tokens: int = 4096

    def __post_init__(self):
        if isinstance(self.capability_id, bool) or not isinstance(self.capability_id, str) or not self.capability_id.strip():
            raise ValueError("capability_id must be a non-empty string")
        for tool in self.allowed_tools:
            if tool.upper() in BANNED_STAFF_TERMS.__members__:
                raise ValueError(f"Forbidden tool capability: {tool}")


@dataclass
class StaffProfile:
    """
    Registered profile for an AI worker.
    """
    staff_id: str
    role: StaffRole
    name: str
    description: str
    capabilities: List[StaffCapability]
    is_active: bool = True

    def __post_init__(self):
        if isinstance(self.staff_id, bool) or not isinstance(self.staff_id, str) or not self.staff_id.strip():
            raise ValueError("staff_id must be a non-empty string")
        if not isinstance(self.role, StaffRole):
            if isinstance(self.role, str):
                self.role = StaffRole(self.role.upper().strip())
            else:
                raise ValueError("role must be a valid StaffRole")


@dataclass
class StaffTask:
    """
    Bounded task node inside a workflow task graph.
    """
    task_id: str
    workflow_id: str
    role: StaffRole
    objective: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    expected_output: str = "JSON or markdown artifact"
    status: TaskStatus = TaskStatus.PENDING
    attempt: int = 1
    max_retries: int = 3
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.task_id, bool) or not isinstance(self.task_id, str) or not self.task_id.strip():
            raise ValueError("task_id must be a non-empty string")
        if isinstance(self.workflow_id, bool) or not isinstance(self.workflow_id, str) or not self.workflow_id.strip():
            raise ValueError("workflow_id must be a non-empty string")
        if not isinstance(self.role, StaffRole):
            if isinstance(self.role, str):
                self.role = StaffRole(self.role.upper().strip())
            else:
                raise ValueError("role must be a StaffRole enum")
        if not isinstance(self.status, TaskStatus):
            if isinstance(self.status, str):
                self.status = TaskStatus(self.status.upper().strip())
            else:
                raise ValueError("status must be a TaskStatus enum")


@dataclass
class StaffResult:
    """
    Result returned by a staff member after executing a StaffTask.
    Contains ZERO security authorization authority.
    """
    task_id: str
    staff_id: str
    role: StaffRole
    status: TaskStatus
    output_data: Dict[str, Any]
    execution_time_seconds: float
    confidence_score: float = 0.90
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    is_authoritative: bool = False
    trust_marker: str = "NON_AUTHORITATIVE_STAFF_OUTPUT"

    def __post_init__(self):
        if self.is_authoritative:
            raise ValueError("StaffResult cannot have is_authoritative=True")
        if isinstance(self.confidence_score, bool) or not isinstance(self.confidence_score, (int, float)):
            raise ValueError("confidence_score must be a numeric value")


@dataclass
class CritiqueResult:
    """
    Structured self-critique produced by CRITIC staff.
    """
    critique_id: str
    task_id: str
    passed: bool
    score: float
    findings: List[str]
    suggested_revisions: List[str]
    evaluated_criteria: Dict[str, bool]
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if isinstance(self.passed, bool) is False:
            raise ValueError("passed must be a boolean")
        if isinstance(self.score, bool) or not isinstance(self.score, (int, float)):
            raise ValueError("score must be a numeric value")


@dataclass
class ReviewResult:
    """
    Independent final review produced by REVIEWER staff.
    Carries zero execution permission authority.
    """
    review_id: str
    workflow_id: str
    approved: bool
    quality_score: float
    defect_reports: List[str]
    approval_reasons: List[str]
    timestamp: float = field(default_factory=time.time)
    is_authoritative: bool = False

    def __post_init__(self):
        if self.is_authoritative:
            raise ValueError("ReviewResult cannot have is_authoritative=True")


@dataclass
class LearningSignal:
    """
    Structured feedback signal emitted post-workflow execution.
    """
    signal_id: str
    workflow_id: str
    task_id: Optional[str]
    source: str  # SYSTEM_ERROR, STAFF_ERROR, CRITIC_FEEDBACK, REVIEWER_FEEDBACK, USER_FEEDBACK, TREND_OBSERVATION
    category: str  # PROMPT_QUALITY, ROUTING_HEURISTIC, QUALITY_CRITERIA, DOMAIN_KNOWLEDGE
    observed_failure: str
    expected_behavior: str
    correction: str
    confidence: float = 0.85
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        if isinstance(self.signal_id, bool) or not isinstance(self.signal_id, str) or not self.signal_id.strip():
            raise ValueError("signal_id must be a non-empty string")
        if self.category == "SECURITY_POLICY":
            raise ValueError("Learning signals cannot target SECURITY_POLICY")


@dataclass
class AdaptiveChange:
    """
    Versioned operational improvement proposal.
    Reversible and strictly scoped to non-security parameters.
    """
    change_id: str
    target_component: str  # PROMPT_TEMPLATE, ROUTING_HEURISTIC, QUALITY_CHECK_CRITERIA
    previous_version: str
    proposed_version: str
    reason: str
    supporting_signals: List[str]
    status: AdaptiveStatus = AdaptiveStatus.PROPOSED
    rollback_target: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    def __post_init__(self):
        forbidden_targets = {"SECURITY_POLICY", "EXECUTION_GATE", "EPISTEMIC_STATE", "AUDIT_INTEGRITY", "RECOVERY_MANAGER"}
        if self.target_component.upper() in forbidden_targets:
            raise ValueError(f"Forbidden adaptive target component: {self.target_component}")


class ObservationClassification(str, Enum):
    TYPOGRAPHY_TREND = "TYPOGRAPHY_TREND"
    COLOR_PALETTE = "COLOR_PALETTE"
    LAYOUT_PATTERN = "LAYOUT_PATTERN"
    EDITORIAL_SYSTEM = "EDITORIAL_SYSTEM"
    GRAPHIC_STYLE = "GRAPHIC_STYLE"
    BRAND_IDENTITY = "BRAND_IDENTITY"


class ObservationCommitment(str, Enum):
    EPHEMERAL = "EPHEMERAL"
    SEASONAL = "SEASONAL"
    PERMANENT = "PERMANENT"


class ObservationStatus(str, Enum):
    UNTRUSTED_EXTERNAL_OBSERVATION = "UNTRUSTED_EXTERNAL_OBSERVATION"
    EVALUATED_OBSERVATION = "EVALUATED_OBSERVATION"
    VERIFIED_FACT = "VERIFIED_FACT"


@dataclass
class VisualObservation:
    """
    External visual trend observation record with provenance tracking.
    """
    observation_id: str
    source_url_or_domain: str = ""
    category: str = "TYPOGRAPHY"
    captured_at: float = field(default_factory=time.time)
    attributes: Dict[str, Any] = field(default_factory=dict)
    provenance_hash: str = ""
    confidence: float = 0.80
    trust_marker: str = "UNTRUSTED_EXTERNAL_OBSERVATION"

    # Phase 9 Extended Fields
    source: str = ""
    timestamp: str = ""
    provenance: str = ""
    summary: str = ""
    details: str = ""
    classification: ObservationClassification = ObservationClassification.TYPOGRAPHY_TREND
    commitment: ObservationCommitment = ObservationCommitment.EPHEMERAL
    status: ObservationStatus = ObservationStatus.UNTRUSTED_EXTERNAL_OBSERVATION

    def __post_init__(self):
        if isinstance(self.observation_id, bool) or not isinstance(self.observation_id, str) or not self.observation_id.strip():
            raise ValueError("observation_id must be a non-empty string")
        if not self.source_url_or_domain and self.source:
            self.source_url_or_domain = self.source
        if not self.source and self.source_url_or_domain:
            self.source = self.source_url_or_domain

    def to_dict(self) -> Dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "source_url_or_domain": self.source_url_or_domain,
            "category": self.category,
            "captured_at": self.captured_at,
            "attributes": self.attributes,
            "provenance_hash": self.provenance_hash,
            "confidence": self.confidence,
            "trust_marker": self.trust_marker,
            "source": self.source,
            "timestamp": self.timestamp,
            "provenance": self.provenance,
            "summary": self.summary,
            "details": self.details,
            "classification": self.classification.value if isinstance(self.classification, Enum) else str(self.classification),
            "commitment": self.commitment.value if isinstance(self.commitment, Enum) else str(self.commitment),
            "status": self.status.value if isinstance(self.status, Enum) else str(self.status),
        }

