"""
Phase 25 Operator Console Package.
"""
from src.operator_console.session import OperatorSessionManager
from src.operator_console.filters import ConsoleFilter
from src.operator_console.navigation import NavigationResolver
from src.operator_console.notifications import OperatorNotification, NotificationManager
from src.operator_console.operator_views import CuratorView, CreativeDirectorView, SREView
from src.operator_console.dashboard import OperatorConsoleDashboard

__all__ = [
    "OperatorSessionManager",
    "ConsoleFilter",
    "NavigationResolver",
    "OperatorNotification",
    "NotificationManager",
    "CuratorView",
    "CreativeDirectorView",
    "SREView",
    "OperatorConsoleDashboard"
]
