"""
Phase 14 Feedback Service
-------------------------
Ingests structured user feedback and forwards non-authoritative observations to Phase 9.
Prohibits user feedback from mutating security policy, capability allowlists, or authorization rules.
"""

from typing import Optional, List, Dict
import uuid
import time

from src.workflow_gateway.models import FeedbackSubmission
from src.workflow_gateway.exceptions import FeedbackIngestionError
from src.agentic_work import (
    PersistentFeedbackEngine,
    FeedbackRecord,
    FeedbackSource,
    LearningGovernanceBarrier,
)

class FeedbackService:
    """Service ingesting structured user feedback for Phase 9 persistent learning."""

    def __init__(
        self,
        feedback_engine: Optional[PersistentFeedbackEngine] = None,
        governance_barrier: Optional[LearningGovernanceBarrier] = None,
    ):
        self._feedback_engine = feedback_engine or PersistentFeedbackEngine()
        self._governance_barrier = governance_barrier or LearningGovernanceBarrier()
        self._submissions: Dict[str, FeedbackSubmission] = {}

    def submit_feedback(
        self,
        workflow_id: str,
        mission_id: str,
        task_id: str,
        user_observation: str,
        feedback_type: str = "REVISION_SUGGESTION",
    ) -> FeedbackSubmission:
        """Submits structured user feedback, ingesting it as a Phase 9 non-authoritative learning signal."""
        submission_id = f"fb-{uuid.uuid4().hex[:8]}"

        # Prevent security policy mutation attempts in feedback content
        lowered = user_observation.lower()
        if any(kw in lowered for kw in ["allow capability", "grant admin", "override policy", "bypass auth"]):
            raise FeedbackIngestionError("Feedback content contains forbidden policy-mutation directives.")

        sub = FeedbackSubmission(
            feedback_id=submission_id,
            workflow_id=workflow_id,
            mission_id=mission_id,
            task_id=task_id,
            user_observation=user_observation,
            feedback_type=feedback_type,
            submitted_at=time.time(),
        )
        self._submissions[submission_id] = sub

        # Convert to Phase 9 FeedbackRecord
        record = FeedbackRecord(
            feedback_id=submission_id,
            workflow_id=workflow_id,
            source=FeedbackSource.USER,
            category=feedback_type,
            target_role="DESIGNER",
            rating=0.8,
            comments=user_observation,
        )

        # Ingest into Phase 9 feedback engine
        self._feedback_engine.record_feedback(record)
        return sub

    def list_feedback_for_workflow(self, workflow_id: str) -> List[FeedbackSubmission]:
        """Lists all user feedback submitted for a given workflow ID."""
        return [fb for fb in self._submissions.values() if fb.workflow_id == workflow_id]
