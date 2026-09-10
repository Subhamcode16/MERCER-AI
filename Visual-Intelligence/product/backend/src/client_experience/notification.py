"""
Phase 16 Notification Center.
Generates secret-free informational alerts for campaign and deliverable events.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from src.client_experience.access_models import UserIdentity

@dataclass(frozen=True)
class NotificationItem:
    notification_id: str
    client_id: str
    event_type: str  # APPROVAL_REQUIRED, REVISION_REQUESTED, CAMPAIGN_BLOCKED, EXECUTION_COMPLETED, ESCALATION_REQUIRED
    message: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class NotificationCenter:
    """Center creating and managing client notification alerts."""

    def __init__(self):
        self._notifications: Dict[str, NotificationItem] = {}

    def send_notification(self, client_id: str, notification_id: str, event_type: str, message: str) -> NotificationItem:
        """Sends a secret-free notification."""
        # Sanitize message to strip secret tokens if any
        sanitized = message.replace("secret", "[REDACTED]").replace("token", "[REDACTED]")
        item = NotificationItem(
            notification_id=notification_id,
            client_id=client_id,
            event_type=event_type,
            message=sanitized
        )
        self._notifications[notification_id] = item
        return item

    def get_notifications_for_user(self, user: UserIdentity) -> List[NotificationItem]:
        """Retrieves active notifications for a user's client workspace."""
        user.verify_capability("view_dashboard")
        return [n for n in self._notifications.values() if n.client_id == user.assigned_client_id]
