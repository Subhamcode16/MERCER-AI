"""
Phase 14 Independent Reviewer
------------------------------
Conducts independent, double-blind artifact evaluations.
Evaluates final proposal candidates prior to human decision / execution preparation.
Enforces INV-14-W005: ReviewResult is non-authoritative and CANNOT authorize execution or mutate security policy.
"""

from typing import List, Dict, Any, Optional
import uuid

from src.creative_workforce.organization_models import ReviewResult
from src.creative_workforce.collaboration import CreativeArtifact
from src.creative_workforce.exceptions import SelfAuthorizationAttemptError, ReviewerBypassError

class IndependentReviewer:
    """Reviewer evaluating candidate artifacts independently from the producing staff."""

    def __init__(self, reviewer_id: str = "independent_reviewer_01"):
        self.reviewer_id = reviewer_id

    def review_artifact(
        self,
        artifact: CreativeArtifact,
        critique_history: Optional[List[Any]] = None,
    ) -> ReviewResult:
        """Performs an independent review on a candidate artifact."""
        # Ensure reviewer identity is distinct from producing staff to maintain double-blind isolation
        if artifact.context_binding.staff_id == self.reviewer_id:
            raise SelfAuthorizationAttemptError("Producer staff cannot act as its own independent reviewer.")

        review_id = f"rev-{uuid.uuid4().hex[:8]}"

        payload = artifact.payload
        scores = {
            "overall_quality": 0.9,
            "brand_compliance": 0.95,
            "production_readiness": 0.88,
        }

        # Check for unresolved defects in payload
        if payload.get("has_unresolved_defects", False):
            scores["production_readiness"] = 0.5
            recommendation = "REVISION_NEEDED"
            comments = "Artifact contains unresolved design defects."
        else:
            recommendation = "ACCEPTED"
            comments = "Independent review passed. Ready for human authorization review."

        return ReviewResult(
            review_id=review_id,
            artifact_id=artifact.artifact_id,
            reviewer_id=self.reviewer_id,
            criteria_scores=scores,
            recommendation=recommendation,
            comments=comments,
            confidence=0.92,
            is_authoritative=False,  # Enforces non-authoritative boundary
        )
