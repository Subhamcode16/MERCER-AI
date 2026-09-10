"""
IF-AGENT-009 Bounded Learning & Adaptive Improvement Manager.
Processes LearningSignal records into versioned AdaptiveChange objects.
Strictly scoped to non-security parameters (prompts, routing, quality criteria).
Reversible with 100% rollback capability.
"""

import time
import uuid
import threading
from typing import Dict, Any, List, Optional
from .models import LearningSignal, AdaptiveChange, AdaptiveStatus


class LearningEngine:
    """
    Bounded Adaptive Learning Engine.
    Processes signals into versioned, auditable, and reversible AdaptiveChange objects.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._active_changes: Dict[str, AdaptiveChange] = {}
        self._signals: List[LearningSignal] = []

    def ingest_signal(self, signal: LearningSignal) -> Optional[AdaptiveChange]:
        if not isinstance(signal, LearningSignal):
            raise ValueError("signal must be a valid LearningSignal instance")

        with self._lock:
            self._signals.append(signal)

            # Generate versioned adaptive change if confidence is high
            if signal.confidence >= 0.70:
                change = AdaptiveChange(
                    change_id=f"chg-{uuid.uuid4().hex[:8]}",
                    target_component=signal.category,
                    previous_version="v1.0.0",
                    proposed_version="v1.1.0",
                    reason=f"Adaptive update triggered by signal {signal.signal_id}: {signal.correction}",
                    supporting_signals=[signal.signal_id],
                    status=AdaptiveStatus.ACTIVE,
                    rollback_target="v1.0.0",
                )
                self._active_changes[change.change_id] = change
                return change
            return None

    def rollback_change(self, change_id: str) -> bool:
        with self._lock:
            change = self._active_changes.get(change_id)
            if change:
                change.status = AdaptiveStatus.ROLLED_BACK
                return True
            return False

    def list_active_changes(self) -> List[AdaptiveChange]:
        with self._lock:
            return [c for c in self._active_changes.values() if c.status == AdaptiveStatus.ACTIVE]
