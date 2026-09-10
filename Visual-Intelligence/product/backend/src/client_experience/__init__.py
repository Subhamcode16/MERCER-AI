"""
Phase 16 ILYREN Client Experience & Studio Command Center Package.
Human interaction boundary providing client workspace, campaign command center, deliverable review, approval center, and performance visibility.
"""

from src.client_experience.exceptions import (
    ClientExperienceError,
    ClientAccessDeniedError,
    InvalidRoleCapabilityError,
    ContextGuardViolationError,
    UIAuthorizationForgeryError,
    FeedbackPolicyMutationError,
    ReasoningLeakageError,
    StaleApprovalError,
)

from src.client_experience.access_models import HumanRole, UserIdentity, ROLE_CAPABILITIES
from src.client_experience.workspace_models import (
    BrandDTO,
    DeliverableDTO,
    ApprovalSummaryDTO,
    CampaignDTO,
    WorkforceActivityDTO,
    TimelineEventDTO,
    PerformanceSummaryDTO,
    ClientWorkspaceDTO,
)

from src.client_experience.context_guard import ClientContextGuard
from src.client_experience.client_access import ClientAccessManager
from src.client_experience.presentation_policy import PresentationPolicyEngine
from src.client_experience.interaction_audit import InteractionAuditLogger, InteractionAuditEntry
from src.client_experience.dashboard import ClientDashboardProjectionEngine
from src.client_experience.campaign_view import CampaignCommandCenterView
from src.client_experience.deliverable_view import DeliverableReviewSurface
from src.client_experience.approval_view import ApprovalCenterView
from src.client_experience.feedback import FeedbackManager, FeedbackRecord
from src.client_experience.workforce_view import WorkforceActivityView
from src.client_experience.timeline import OperationsTimelineEngine
from src.client_experience.performance_view import PerformanceOutcomeView
from src.client_experience.notification import NotificationCenter, NotificationItem
from src.client_experience.api_boundary import ClientExperienceAPIBoundary
from src.client_experience.command_center import StudioCommandCenter

__all__ = [
    # Exceptions
    "ClientExperienceError",
    "ClientAccessDeniedError",
    "InvalidRoleCapabilityError",
    "ContextGuardViolationError",
    "UIAuthorizationForgeryError",
    "FeedbackPolicyMutationError",
    "ReasoningLeakageError",
    "StaleApprovalError",
    # Access Models
    "HumanRole",
    "UserIdentity",
    "ROLE_CAPABILITIES",
    # DTO Models
    "BrandDTO",
    "DeliverableDTO",
    "ApprovalSummaryDTO",
    "CampaignDTO",
    "WorkforceActivityDTO",
    "TimelineEventDTO",
    "PerformanceSummaryDTO",
    "ClientWorkspaceDTO",
    # Security & Guard Engines
    "ClientContextGuard",
    "ClientAccessManager",
    "PresentationPolicyEngine",
    "InteractionAuditLogger",
    "InteractionAuditEntry",
    # View & Surface Engines
    "ClientDashboardProjectionEngine",
    "CampaignCommandCenterView",
    "DeliverableReviewSurface",
    "ApprovalCenterView",
    "FeedbackManager",
    "FeedbackRecord",
    "WorkforceActivityView",
    "OperationsTimelineEngine",
    "PerformanceOutcomeView",
    "NotificationCenter",
    "NotificationItem",
    "ClientExperienceAPIBoundary",
    "StudioCommandCenter",
]
