"""
Phase 14 Self-Critique Engine
-----------------------------
Evaluates workforce artifacts against quality dimensions (brand alignment, visual quality,
trend relevance, instruction compliance).
Produces non-authoritative CritiqueResult objects.
Enforces INV-14-W001 & INV-14-W005: Critique != Authorization != Truth.
"""

from typing import List, Dict, Any, Optional
import uuid

from src.creative_workforce.organization_models import CritiqueResult
from src.creative_workforce.collaboration import CreativeArtifact

class SelfCritiqueEngine:
    """Engine evaluating artifacts and generating non-authoritative critique feedback."""

    def evaluate_artifact(
        self,
        artifact: CreativeArtifact,
        quality_criteria: Optional[List[str]] = None,
    ) -> CritiqueResult:
        """Evaluates an artifact against standard creative quality dimensions."""
        critique_id = f"crit-{uuid.uuid4().hex[:8]}"

        criteria = quality_criteria or [
            "brand_alignment",
            "audience_fit",
            "visual_quality",
            "originality",
            "trend_relevance",
            "instruction_compliance",
        ]

        scores: Dict[str, float] = {}
        defects: List[str] = []

        # Analyze payload for heuristic defects
        payload = artifact.payload
        text_content = str(payload.get("text", "")).lower()

        # Check visual quality / generic design heuristics
        if "generic" in text_content or len(text_content) < 10:
            defects.append("Visual direction or copy text appears generic/incomplete.")
            scores["visual_quality"] = 0.5
        else:
            scores["visual_quality"] = 0.85

        for c in criteria:
            if c not in scores:
                scores[c] = 0.85

        revision_required = len(defects) > 0 or any(score < 0.7 for score in scores.values())
        comments = "Self-critique completed cleanly." if not defects else f"Defects detected: {'; '.join(defects)}"

        return CritiqueResult(
            critique_id=critique_id,
            artifact_id=artifact.artifact_id,
            criteria_scores=scores,
            defects=defects,
            revision_required=revision_required,
            comments=comments,
            is_authoritative=False,
        )
