"""
Phase 25 Operator Console Tests.
"""
import pytest
import time
from src.control_plane.models import OperatorIdentity, OperatorRole
from src.control_plane.context import OperatorContext
from src.control_plane.exceptions import OperatorSessionExpiredError
from src.operator_console.session import OperatorSessionManager
from src.operator_console.navigation import NavigationResolver
from src.operator_console.notifications import NotificationManager, OperatorNotification
from src.operator_console.dashboard import OperatorConsoleDashboard
from src.control_plane.service import ControlPlaneService

def test_operator_session_lifecycle():
    mgr = OperatorSessionManager(default_ttl_seconds=1.0)
    identity = OperatorIdentity(
        operator_id="op-1",
        username="curator_elena",
        roles=[OperatorRole.LEAD_CURATOR],
        tenant_scope="tenant_atelier",
        allowed_clients=["client_alpha"]
    )
    sess_id = mgr.create_session(identity)
    assert sess_id.startswith("sess-")

    sess = mgr.validate_session(sess_id)
    assert sess["operator_id"] == "op-1"

    # Wait for TTL expiry
    time.sleep(1.1)
    with pytest.raises(OperatorSessionExpiredError):
        mgr.validate_session(sess_id)

def test_navigation_menu_resolution():
    curator_menu = NavigationResolver.resolve_navigation_menu([OperatorRole.LEAD_CURATOR])
    curator_ids = [m["id"] for m in curator_menu]
    assert "dashboard" in curator_ids
    assert "approvals" in curator_ids
    assert "campaigns" in curator_ids
    assert "providers" not in curator_ids # SRE only

    sre_menu = NavigationResolver.resolve_navigation_menu([OperatorRole.SRE_ENGINEER])
    sre_ids = [m["id"] for m in sre_menu]
    assert "reliability" in sre_ids
    assert "providers" in sre_ids
    assert "approvals" not in sre_ids

def test_notification_manager():
    mgr = NotificationManager()
    notif = OperatorNotification(
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        title="Approval Required",
        message="Campaign Autumn Equinox requires curator review."
    )
    mgr.dispatch_notification(notif)

    unread = mgr.get_unread_notifications("tenant_atelier", "client_alpha")
    assert len(unread) == 1

    # Cross-tenant unread check
    unread_other = mgr.get_unread_notifications("tenant_other", "client_beta")
    assert len(unread_other) == 0

    mgr.acknowledge_notification(notif.notification_id)
    assert len(mgr.get_unread_notifications("tenant_atelier", "client_alpha")) == 0

def test_operator_console_dashboard_rendering():
    service = ControlPlaneService()
    dashboard = OperatorConsoleDashboard(service=service)
    ctx = OperatorContext(
        operator_id="op-curator-01",
        tenant_id="tenant_atelier",
        client_id="client_alpha",
        roles=[OperatorRole.LEAD_CURATOR]
    )
    exec_view = dashboard.render_executive_dashboard(ctx, "tenant_atelier", "client_alpha")
    assert exec_view["tenant_id"] == "tenant_atelier"
    assert exec_view["system_health"] == "HEALTHY"

    role_view = dashboard.render_role_specific_view(ctx, "tenant_atelier", "client_alpha")
    assert role_view["role"] == "LEAD_CURATOR"
