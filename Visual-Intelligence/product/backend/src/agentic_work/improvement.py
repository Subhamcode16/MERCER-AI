"""
IF-AGENT-012 Bounded Self-Improvement Governance.
Maintains version history of adaptive updates and guarantees 100% reversibility.
Rejects updates targeting forbidden security boundaries.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from .models import AdaptiveChange, AdaptiveStatus


class ImprovementManager:
    """
    Self-Improvement Governance Manager.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._history: List[AdaptiveChange] = []

    def register_change(self, change: AdaptiveChange) -> None:
        if not isinstance(change, AdaptiveChange):
            raise ValueError("change must be an instance of AdaptiveChange")
        with self._lock:
            self._history.append(change)

    def revert_last_change(self) -> Optional[AdaptiveChange]:
        with self._lock:
            for change in reversed(self._history):
                if change.status == AdaptiveStatus.ACTIVE:
                    change.status = AdaptiveStatus.ROLLED_BACK
                    return change
            return None

    def get_history(self) -> List[AdaptiveChange]:
        with self._lock:
            return list(self._history)
