"""
Unit tests for Phase 16 Notification Center.
"""

import pytest
from src.client_experience.notification import NotificationCenter
from src.client_experience.access_models import UserIdentity, HumanRole

def test_notification_center_flow():
    center = NotificationCenter()
    center.send_notification("client_nocap", "notif_001", "APPROVAL_REQUIRED", "Human approval required for post del_001. token_abc123")

    user = UserIdentity("user_owner", "Alice", "alice@nocap.com", "client_nocap", HumanRole.CLIENT_OWNER)
    notifications = center.get_notifications_for_user(user)

    assert len(notifications) == 1
    assert "token_abc123" not in notifications[0].message
    assert "[REDACTED]" in notifications[0].message
