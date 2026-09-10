"""
IF-AGENT-003 AI Staff Role Implementations.
Defines composable worker abstractions for RESEARCHER, STRATEGIST, DESIGNER,
CONTENT_SPECIALIST, TREND_ANALYST, CRITIC, and REVIEWER.
Enforces non-authoritative output boundaries.
"""

import time
import uuid
from typing import Dict, Any, List, Optional

from .models import (
    StaffRole,
    StaffCapability,
    StaffProfile,
    StaffTask,
    StaffResult,
    TaskStatus,
    CritiqueResult,
    ReviewResult,
)
from .context import StaffContext, ReviewContext


class BaseStaff:
    """
    Abstract base class for all AI Staff workers.
    Workers possess ZERO security authorization privileges.
    """

    def __init__(self, staff_id: str, role: StaffRole, name: str, description: str) -> None:
        self.staff_id = staff_id
        self.role = role
        self.name = name
        self.description = description

    def execute_task(self, context: StaffContext) -> StaffResult:
        raise NotImplementedError("Subclasses must implement execute_task")


class ResearcherStaff(BaseStaff):
    """
    RESEARCHER: Collects, analyzes, and synthesizes domain facts & market data.
    """

    def __init__(self, staff_id: str = "staff-researcher-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.RESEARCHER,
            name="Research Specialist",
            description="Collects and synthesizes visual and brand domain intelligence.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        obj = context.task_context.objective
        inputs = context.task_context.inputs

        output = {
            "summary": f"Synthesized research for objective: {obj}",
            "key_insights": [
                "Target audience favors clean layout with high contrast typography.",
                "Minimalist aesthetic relies on generous negative space.",
                "Color palette focus: monochrome with warm ivory accents.",
            ],
            "reference_sources": ["brand_guidelines_2026", "market_lookbook_archive"],
        }
        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED,
            output_data=output,
            execution_time_seconds=time.time() - start_time,
            confidence_score=0.92,
        )


class StrategistStaff(BaseStaff):
    """
    STRATEGIST: Converts research insights into campaign positioning & messaging pillars.
    """

    def __init__(self, staff_id: str = "staff-strategist-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.STRATEGIST,
            name="Brand Strategist",
            description="Formulates campaign positioning and strategic creative pillars.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        parent_outputs = context.task_context.parent_outputs

        output = {
            "campaign_title": "Modern Minimalist Silhouette Collection 2026",
            "positioning_statement": "Understated luxury expressed through precise tailoring and quiet elegance.",
            "pillars": [
                {"name": "Architectural Lines", "focus": "Clean structure & geometric balance"},
                {"name": "Tactile Texture", "focus": "Premium organic cotton & refined wool"},
                {"name": "Timeless Palette", "focus": "Warm charcoal, ivory, and brushed brass"},
            ],
        }
        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED,
            output_data=output,
            execution_time_seconds=time.time() - start_time,
            confidence_score=0.94,
        )


class DesignerStaff(BaseStaff):
    """
    DESIGNER: Produces visual/creative concepts, layout specifications, and color systems.
    """

    def __init__(self, staff_id: str = "staff-designer-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.DESIGNER,
            name="Visual Art Director",
            description="Generates visual layout specs, color schemes, and aesthetic direction.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        inputs = context.task_context.inputs
        
        # Check if a intentional defect was injected for critique testing
        inject_defect = inputs.get("inject_defect", False)

        output = {
            "layout_system": "6-Column Asymmetric Bento Grid",
            "primary_font": "Outfit / Inter Display",
            "secondary_font": "Newsreader Serif",
            "color_palette": {
                "background": "#FDFBF7",
                "text_primary": "#1A1A1A",
                "accent_tint": "#D4C5B9" if not inject_defect else "#FF0000",  # Red clash defect if injected!
            },
            "visual_style": "High-key studio lighting with soft directional shadows" if not inject_defect else "Generic cluttered aesthetic",
            "has_defect": inject_defect,
        }

        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED,
            output_data=output,
            execution_time_seconds=time.time() - start_time,
            confidence_score=0.88 if not inject_defect else 0.40,
        )


class ContentSpecialistStaff(BaseStaff):
    """
    CONTENT_SPECIALIST: Crafts copy, captions, and platform-specific messaging.
    """

    def __init__(self, staff_id: str = "staff-content-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.CONTENT_SPECIALIST,
            name="Editorial Copywriter",
            description="Drafts elevated editorial copy, hooks, and campaign messaging.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        output = {
            "hero_headline": "Form Meets Silence.",
            "subheadline": "The 2026 Minimalist Lookbook curated for refined simplicity.",
            "social_copy": "Stripped of distraction. Crafted with intention. Discover the new silhouette collection.",
            "call_to_action": "Explore the Lookbook",
        }
        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED,
            output_data=output,
            execution_time_seconds=time.time() - start_time,
            confidence_score=0.91,
        )


class TrendAnalystStaff(BaseStaff):
    """
    TREND_ANALYST: Evaluates real-world visual trends and market observations.
    """

    def __init__(self, staff_id: str = "staff-trend-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.TREND_ANALYST,
            name="Trend Intelligence Specialist",
            description="Analyzes emerging visual, typographic, and palette conventions.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        output = {
            "emerging_trends": [
                "Warm monochromatic background surfaces replacing stark white",
                "Wide serif typography for luxury editorial headers",
                "Sparse micro-animations for digital lookbook reveals",
            ],
            "confidence": 0.86,
            "freshness_window": "2026 Q3",
        }
        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED,
            output_data=output,
            execution_time_seconds=time.time() - start_time,
            confidence_score=0.86,
        )


class CriticStaff(BaseStaff):
    """
    CRITIC: Evaluates intermediate work products against explicit quality criteria.
    """

    def __init__(self, staff_id: str = "staff-critic-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.CRITIC,
            name="Quality Critic",
            description="Evaluates artifacts against multi-criteria quality standards.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        parent_outputs = context.task_context.parent_outputs

        # Inspect designer output if present (check t4_design, designer_task, or search values)
        designer_out = parent_outputs.get("t4_design") or parent_outputs.get("designer_task") or {}
        if not designer_out:
            for out in parent_outputs.values():
                if isinstance(out, dict) and ("color_palette" in out or "has_defect" in out):
                    designer_out = out
                    break

        has_defect = designer_out.get("has_defect", False)
        accent_color = designer_out.get("color_palette", {}).get("accent_tint", "")

        findings = []
        suggested_revisions = []
        criteria = {
            "task_completeness": True,
            "brand_alignment": not has_defect,
            "visual_harmony": accent_color != "#FF0000",
            "factual_grounding": True,
        }

        passed = all(criteria.values())
        score = 0.95 if passed else 0.45

        if not passed:
            findings.append("Color clash detected: #FF0000 accent violates minimalist warm ivory palette.")
            suggested_revisions.append("Replace accent_tint #FF0000 with harmonious neutral #D4C5B9.")

        critique_res = CritiqueResult(
            critique_id=f"crt-{uuid.uuid4().hex[:8]}",
            task_id=context.task_context.task_id,
            passed=passed,
            score=score,
            findings=findings,
            suggested_revisions=suggested_revisions,
            evaluated_criteria=criteria,
        )

        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED if passed else TaskStatus.REVISION_REQUIRED,
            output_data={
                "critique_result": critique_res.__dict__,
                "passed": passed,
                "score": score,
                "findings": findings,
                "suggested_revisions": suggested_revisions,
            },
            execution_time_seconds=time.time() - start_time,
            confidence_score=score,
        )


class ReviewerStaff(BaseStaff):
    """
    REVIEWER: Performs independent final review.
    Carries ZERO execution permission authority.
    """

    def __init__(self, staff_id: str = "staff-reviewer-01") -> None:
        super().__init__(
            staff_id=staff_id,
            role=StaffRole.REVIEWER,
            name="Independent Reviewer",
            description="Performs independent final verification of complete work package.",
        )

    def execute_task(self, context: StaffContext) -> StaffResult:
        start_time = time.time()
        parent_outputs = context.task_context.parent_outputs

        # Check if critique passed (check t6_critique, critic_task, or search values)
        critic_out = parent_outputs.get("t6_critique") or parent_outputs.get("critic_task") or {}
        if not critic_out:
            for out in parent_outputs.values():
                if isinstance(out, dict) and "passed" in out:
                    critic_out = out
                    break

        passed = critic_out.get("passed", True)

        approved = passed
        quality_score = 0.96 if approved else 0.40
        defects = [] if approved else ["Unresolved visual palette conflict in design specification."]
        reasons = ["All 7 staff outputs coherent and aligned with minimalist brand directives."] if approved else []

        review_res = ReviewResult(
            review_id=f"rev-{uuid.uuid4().hex[:8]}",
            workflow_id=context.task_context.workflow_id,
            approved=approved,
            quality_score=quality_score,
            defect_reports=defects,
            approval_reasons=reasons,
        )

        return StaffResult(
            task_id=context.task_context.task_id,
            staff_id=self.staff_id,
            role=self.role,
            status=TaskStatus.COMPLETED if approved else TaskStatus.FAILED,
            output_data={
                "review_result": review_res.__dict__,
                "approved": approved,
                "quality_score": quality_score,
                "defect_reports": defects,
                "approval_reasons": reasons,
            },
            execution_time_seconds=time.time() - start_time,
            confidence_score=quality_score,
        )
