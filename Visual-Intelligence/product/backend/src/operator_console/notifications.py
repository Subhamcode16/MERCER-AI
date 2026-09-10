"""
Phase 25 Operator Console Notification Dispatcher.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time
import uuid

@dataclass
class OperatorNotification:
    notification_id: str = field(default_factory=lambda: f"notif-{uuid.uuid4().hex[:10]}")
    tenant_id: str = ""
    client_id: str = ""
    recipient_role: Optional[str] = None
    title: str = ""
    message: str = ""
    severity: str = "INFO" # INFO, WARNING, CRITICAL, ACTION_REQUIRED
    acknowledged: bool = False
    timestamp: float = field(default_factory=time.time)
    action_link: Optional[str] = None

class NotificationManager:
    """Manages active operator notifications and acknowledgments."""

    def __init__(self):
        self._notifications: List[OperatorNotification] = []

    def dispatch_notification(self, notification: OperatorNotification) -> None:
        self._notifications.append(notification)

    def get_unread_notifications(self, tenant_id: str, client_id: str) -> List[OperatorNotification]:
        return [
            n for n in self._notifications
            if not n.acknowledged and (tenant_id == "*" or n.tenant_id == tenant_id)
            and (client_id == "*" or n.client_id == client_id)
        ]

    def acknowledge_notification(self, notification_id: str) -> bool:
        for n in self._notifications:
            if n.notification_id == notification_id:
                n.acknowledged = True
                return True
        return False
