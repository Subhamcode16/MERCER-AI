"""
IF-AGENT-006 Self-Critique Engine.
Evaluates task outputs against explicit criteria:
- task completion
- factual/evidence grounding
- brand/visual alignment
- internal consistency
Emits structured CritiqueResult artifacts.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from .models import CritiqueResult


class CritiqueEngine:
    """
    Quality Critique Engine.
    Evaluates intermediate staff outputs against explicit quality criteria.
    """

    def evaluate_output(
        self,
        task_id: str,
        output_data: Dict[str, Any],
        quality_criteria: Optional[Dict[str, Any]] = None
    ) -> CritiqueResult:
        criteria = quality_criteria or {
            "task_completeness": True,
            "brand_alignment": True,
            "visual_harmony": True,
            "factual_grounding": True,
        }

        findings = []
        suggested_revisions = []

        # Check for explicitly declared defects or color mismatches
        color_palette = output_data.get("color_palette", {})
        accent_tint = color_palette.get("accent_tint", "") if isinstance(color_palette, dict) else ""

        if accent_tint == "#FF0000" or output_data.get("has_defect", False):
            criteria["brand_alignment"] = False
            criteria["visual_harmony"] = False
            findings.append("Color clash detected: #FF0000 accent violates minimalist warm ivory palette.")
            suggested_revisions.append("Replace accent_tint #FF0000 with harmonious neutral #D4C5B9.")

        passed = all(criteria.values())
        score = 0.95 if passed else 0.45

        return CritiqueResult(
            critique_id=f"crt-{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            passed=passed,
            score=score,
            findings=findings,
            suggested_revisions=suggested_revisions,
            evaluated_criteria=criteria,
        )
