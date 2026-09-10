"""
Phase 16 Client Feedback Manager.
Categorizes structured client feedback into revision, preference, or learning signals without policy mutations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from src.client_experience.access_models import UserIdentity
from src.client_experience.exceptions import FeedbackPolicyMutationError
from src.studio_operations.studio_models import DeliverableStatus

@dataclass(frozen=True)
class FeedbackRecord:
    feedback_id: str
    client_id: str
    deliverable_id: str
    user_id: str
    feedback_type: str  # REVISION_REQUEST, PREFERENCE_SIGNAL, LEARNING_SIGNAL
    comments: str
    sanitized_text: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class FeedbackManager:
    """Manager ingesting and categorizing structured client feedback."""

    def __init__(self):
        self._records: Dict[str, FeedbackRecord] = {}

    def submit_feedback(
        self,
        user: UserIdentity,
        feedback_id: str,
        deliverable_id: str,
        feedback_type: str,
        comments: str,
        studio_orchestrator: Any
    ) -> FeedbackRecord:
        """Submits client feedback with sanitization and policy protection."""
        user.verify_capability("submit_feedback")
        client_id = user.assigned_client_id

        # Reject policy mutation attempts embedded in feedback
        forbidden_keywords = ["grant admin", "override policy", "allow capability", "bypass auth", "disable security"]
        if any(fk in comments.lower() for fk in forbidden_keywords):
            raise FeedbackPolicyMutationError("Feedback payload contains forbidden security policy mutation attempts.")

        sanitized = comments.strip()[:500]

        record = FeedbackRecord(
            feedback_id=feedback_id,
            client_id=client_id,
            deliverable_id=deliverable_id,
            user_id=user.user_id,
            feedback_type=feedback_type,
            comments=comments,
            sanitized_text=sanitized
        )
        self._records[feedback_id] = record
        # If revision requested, trigger deliverable state transition to REVISION if in a valid review status
        if feedback_type == "REVISION_REQUEST":
            deliv = studio_orchestrator.deliverable_manager.get_deliverable(client_id, deliverable_id)
            if deliv and deliv.status in (DeliverableStatus.REVIEW, DeliverableStatus.CRITIQUE, DeliverableStatus.DRAFT):
                studio_orchestrator.deliverable_manager.transition_deliverable(
                    requesting_client_id=client_id,
                    deliverable_id=deliverable_id,
                    target_status=DeliverableStatus.REVISION,
                    content_update={"client_feedback": sanitized}
                )

        return record
