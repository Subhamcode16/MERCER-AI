"""
Phase 14 Creative Workforce Organization Models
-----------------------------------------------
Immutable dataclasses and enums representing the ILYREN Creative Workforce topology,
staff identities, context bindings, contracts, assignments, critique, and independent review.
Enforces INV-14-W001: Capability != Authority.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Set, Dict, Any, Optional

class Department(Enum):
    """Departments in the ILYREN Creative Workforce."""
    STRATEGY = "STRATEGY"
    CREATIVE = "CREATIVE"
    INTELLIGENCE = "INTELLIGENCE"
    CONTENT = "CONTENT"
    QUALITY = "QUALITY"

class Role(Enum):
    """Role taxonomy across workforce departments."""
    # Strategy
    BRAND_STRATEGIST = "BRAND_STRATEGIST"
    CAMPAIGN_STRATEGIST = "CAMPAIGN_STRATEGIST"
    MARKETING_STRATEGIST = "MARKETING_STRATEGIST"
    GROWTH_ANALYST = "GROWTH_ANALYST"
    # Creative
    CREATIVE_DIRECTOR = "CREATIVE_DIRECTOR"
    ART_DIRECTOR = "ART_DIRECTOR"
    VISUAL_DESIGNER = "VISUAL_DESIGNER"
    GRAPHIC_DESIGNER = "GRAPHIC_DESIGNER"
    MOTION_DESIGNER = "MOTION_DESIGNER"
    COPYWRITER = "COPYWRITER"
    # Intelligence
    TREND_RESEARCHER = "TREND_RESEARCHER"
    CULTURAL_RESEARCHER = "CULTURAL_RESEARCHER"
    COMPETITOR_ANALYST = "COMPETITOR_ANALYST"
    VISUAL_DNA_ANALYST = "VISUAL_DNA_ANALYST"
    AUDIENCE_INTELLIGENCE_ANALYST = "AUDIENCE_INTELLIGENCE_ANALYST"
    # Content
    SOCIAL_CONTENT_STRATEGIST = "SOCIAL_CONTENT_STRATEGIST"
    SCRIPTWRITER = "SCRIPTWRITER"
    EDITORIAL_PLANNER = "EDITORIAL_PLANNER"
    CONTENT_REPURPOSER = "CONTENT_REPURPOSER"
    # Quality
    CREATIVE_CRITIC = "CREATIVE_CRITIC"
    BRAND_COMPLIANCE_REVIEWER = "BRAND_COMPLIANCE_REVIEWER"
    FACT_CHECKER = "FACT_CHECKER"
    INDEPENDENT_REVIEWER = "INDEPENDENT_REVIEWER"

class AuthorityClass(Enum):
    """Authority classes for workforce roles. NO role possesses authorization authority."""
    OBSERVE = "OBSERVE"
    PROPOSE = "PROPOSE"
    CRITIQUE = "CRITIQUE"
    REVIEW = "REVIEW"

@dataclass(frozen=True)
class StaffIdentity:
    """Machine-readable identity for a workforce staff member."""
    staff_id: str
    role: Role
    department: Department
    capabilities: List[str]
    knowledge_domains: List[str]
    authority_class: AuthorityClass
    version: str = "1.0.0"

    def __post_init__(self):
        if not self.staff_id:
            raise ValueError("staff_id cannot be empty.")
        if self.authority_class not in (AuthorityClass.OBSERVE, AuthorityClass.PROPOSE, AuthorityClass.CRITIQUE, AuthorityClass.REVIEW):
            raise ValueError("Invalid authority class. Workforce roles cannot possess execution authorization authority.")

@dataclass(frozen=True)
class ContextBinding:
    """Hierarchical context binding ensuring strict client and campaign isolation."""
    client_id: str
    brand_id: str
    campaign_id: str
    mission_id: str
    task_id: str
    staff_id: str

    def __post_init__(self):
        if not self.client_id or not self.brand_id:
            raise ValueError("client_id and brand_id are required for context binding.")

@dataclass(frozen=True)
class ArtifactContract:
    """Contract defining required properties for a workforce artifact."""
    contract_id: str
    title: str
    required_fields: List[str]
    target_role: Role

@dataclass(frozen=True)
class WorkforceAssignment:
    """Assignment delegated to a staff member by the CreativeWorkforceDirector."""
    assignment_id: str
    objective: str
    assigned_staff_id: str
    role: Role
    context_binding: ContextBinding
    dependencies: List[str] = field(default_factory=list)
    status: str = "PENDING"

@dataclass(frozen=True)
class CritiqueResult:
    """Non-authoritative self-critique evaluation result."""
    critique_id: str
    artifact_id: str
    criteria_scores: Dict[str, float]
    defects: List[str]
    revision_required: bool
    comments: str
    is_authoritative: bool = False

@dataclass(frozen=True)
class ReviewResult:
    """Independent review evaluation result."""
    review_id: str
    artifact_id: str
    reviewer_id: str
    criteria_scores: Dict[str, float]
    recommendation: str  # ACCEPTED, REJECTED, REVISION_NEEDED
    comments: str
    confidence: float = 0.9
    is_authoritative: bool = False

    def __post_init__(self):
        if self.is_authoritative:
            raise ValueError("ReviewResult must remain non-authoritative (is_authoritative=False).")
