"""
Phase 14 Staff Registry
-----------------------
Maintains the canonical workforce taxonomy of specialized staff members across all 5 departments:
Strategy, Creative, Intelligence, Content, and Quality.
Supports lookups and role queries while enforcing capability/authority boundaries.
"""

from typing import Dict, List, Optional
from src.creative_workforce.organization_models import (
    Department,
    Role,
    AuthorityClass,
    StaffIdentity,
)
from src.creative_workforce.exceptions import StaffNotFoundError
from src.creative_workforce.dossiers.dossier_models import StaffDossier
from src.creative_workforce.dossiers.dossier_registry import (
    get_dossier as registry_get_dossier,
    list_dossiers as registry_list_dossiers,
    list_dossiers_by_department as registry_list_dossiers_by_department,
)

class StaffRegistry:
    """Registry maintaining active workforce staff identities across departments."""

    def __init__(self):
        self._staff: Dict[str, StaffIdentity] = {}
        self._bootstrap_default_workforce()

    def _bootstrap_default_workforce(self):
        """Populates the canonical 5-department staff taxonomy."""
        defaults = [
            # Strategy
            StaffIdentity("brand_strategist_01", Role.BRAND_STRATEGIST, Department.STRATEGY, ["brand_positioning", "audience_archetypes"], ["fashion", "streetwear"], AuthorityClass.PROPOSE),
            StaffIdentity("campaign_strategist_01", Role.CAMPAIGN_STRATEGIST, Department.STRATEGY, ["campaign_planning", "channel_strategy"], ["marketing", "social"], AuthorityClass.PROPOSE),
            StaffIdentity("growth_analyst_01", Role.GROWTH_ANALYST, Department.STRATEGY, ["performance_analytics", "funnel_optimization"], ["growth", "data"], AuthorityClass.OBSERVE),
            # Creative
            StaffIdentity("creative_director_01", Role.CREATIVE_DIRECTOR, Department.CREATIVE, ["executive_vision", "creative_synthesis"], ["creative_direction", "branding"], AuthorityClass.PROPOSE),
            StaffIdentity("art_director_01", Role.ART_DIRECTOR, Department.CREATIVE, ["visual_direction", "composition", "moodboards"], ["fashion", "editorial"], AuthorityClass.PROPOSE),
            StaffIdentity("visual_designer_01", Role.VISUAL_DESIGNER, Department.CREATIVE, ["graphic_design", "layout", "typography"], ["visual_arts", "ui"], AuthorityClass.PROPOSE),
            StaffIdentity("copywriter_01", Role.COPYWRITER, Department.CREATIVE, ["brand_voice", "scriptwriting", "hooks"], ["copywriting", "editorial"], AuthorityClass.PROPOSE),
            # Intelligence
            StaffIdentity("trend_researcher_01", Role.TREND_RESEARCHER, Department.INTELLIGENCE, ["trend_collection", "cultural_signals"], ["fashion_trends", "culture"], AuthorityClass.OBSERVE),
            StaffIdentity("visual_dna_analyst_01", Role.VISUAL_DNA_ANALYST, Department.INTELLIGENCE, ["color_palette_extraction", "aesthetic_clustering"], ["visual_dna", "style"], AuthorityClass.OBSERVE),
            # Content
            StaffIdentity("content_strategist_01", Role.SOCIAL_CONTENT_STRATEGIST, Department.CONTENT, ["content_buckets", "editorial_calendar"], ["social_media", "reels"], AuthorityClass.PROPOSE),
            StaffIdentity("scriptwriter_01", Role.SCRIPTWRITER, Department.CONTENT, ["shortform_video_scripts", "dialogue"], ["content", "video"], AuthorityClass.PROPOSE),
            # Quality
            StaffIdentity("creative_critic_01", Role.CREATIVE_CRITIC, Department.QUALITY, ["defect_detection", "alignment_critique"], ["quality_assurance", "critique"], AuthorityClass.CRITIQUE),
            StaffIdentity("independent_reviewer_01", Role.INDEPENDENT_REVIEWER, Department.QUALITY, ["blind_review", "final_candidate_scoring"], ["review", "compliance"], AuthorityClass.REVIEW),
        ]
        for s in defaults:
            self._staff[s.staff_id] = s

    def register_staff(self, staff: StaffIdentity) -> None:
        """Registers a new staff identity."""
        self._staff[staff.staff_id] = staff

    def get_staff(self, staff_id: str) -> StaffIdentity:
        """Retrieves a staff identity by ID or raises StaffNotFoundError."""
        if staff_id not in self._staff:
            raise StaffNotFoundError(f"Staff member '{staff_id}' not found in registry.")
        return self._staff[staff_id]

    def list_by_department(self, department: Department) -> List[StaffIdentity]:
        """Lists all staff members belonging to a department."""
        return [s for s in self._staff.values() if s.department == department]

    def list_by_role(self, role: Role) -> List[StaffIdentity]:
        """Lists all staff members assigned to a specific role."""
        return [s for s in self._staff.values() if s.role == role]

    def list_all(self) -> List[StaffIdentity]:
        """Lists all registered workforce staff members."""
        return list(self._staff.values())

    def get_dossier(self, staff_id: str) -> Optional[StaffDossier]:
        """Retrieves the full staff dossier for a staff member."""
        return registry_get_dossier(staff_id)

    def list_dossiers(self) -> List[StaffDossier]:
        """Lists all registered workforce staff dossiers."""
        return registry_list_dossiers()

    def list_dossiers_by_department(self, department: Department) -> List[StaffDossier]:
        """Lists all staff dossiers belonging to a department."""
        return registry_list_dossiers_by_department(department)

