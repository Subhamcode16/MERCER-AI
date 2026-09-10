"""
IF-AGENT-010 Knowledge Intake & Provenance Boundary Engine.
Manages continuous external observation intake with explicit provenance tracking.
External information remains untrusted evidence until evaluated.
"""

import time
import hashlib
import threading
from typing import Dict, Any, List, Optional
from .models import VisualObservation


class KnowledgeStore:
    """
    Provenance-aware Knowledge & Observation Store.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._observations: Dict[str, VisualObservation] = {}

    def ingest_observation(self, observation: VisualObservation) -> None:
        if not isinstance(observation, VisualObservation):
            raise ValueError("observation must be a VisualObservation instance")
        with self._lock:
            self._observations[observation.observation_id] = observation

    def get_observation(self, observation_id: str) -> Optional[VisualObservation]:
        with self._lock:
            return self._observations.get(observation_id)

    def query_by_category(self, category: str) -> List[VisualObservation]:
        with self._lock:
            return [obs for obs in self._observations.values() if obs.category.upper() == category.upper()]
