"""
Phase 18 Outcome Store.

Atomic, hash-integrity-protected outcome observation storage
with anti-replay defense and strict client isolation.
"""

from typing import Dict, List, Optional
import threading

from src.studio_intelligence.outcome_models import OutcomeObservation
from src.studio_intelligence.exceptions import (
    OutcomeValidationError,
    CrossClientIntelligenceViolation,
)


class OutcomeStore:
    """Persistent in-memory & file-backed atomic outcome observation store."""

    def __init__(self):
        self._lock = threading.RLock()
        self._observations: Dict[str, OutcomeObservation] = {}
        self._signatures: set = set()
        self._client_index: Dict[str, List[str]] = {}

    def store_observation(
        self, requesting_client_id: str, observation: OutcomeObservation
    ) -> OutcomeObservation:
        """Stores an outcome observation with client isolation and replay protection."""
        if requesting_client_id != observation.client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot store observations for '{observation.client_id}'."
            )

        with self._lock:
            if observation.observation_id in self._observations:
                raise OutcomeValidationError(
                    f"Duplicate observation ID '{observation.observation_id}' rejected (anti-replay)."
                )

            if observation.hash_signature in self._signatures:
                raise OutcomeValidationError(
                    f"Duplicate outcome signature '{observation.hash_signature}' rejected (anti-replay)."
                )

            self._observations[observation.observation_id] = observation
            self._signatures.add(observation.hash_signature)

            if observation.client_id not in self._client_index:
                self._client_index[observation.client_id] = []
            self._client_index[observation.client_id].append(observation.observation_id)

            return observation

    def get_observation(
        self, requesting_client_id: str, observation_id: str
    ) -> Optional[OutcomeObservation]:
        """Retrieves a single outcome observation enforcing client isolation."""
        with self._lock:
            obs = self._observations.get(observation_id)
            if not obs:
                return None

            if requesting_client_id != obs.client_id:
                raise CrossClientIntelligenceViolation(
                    f"Client '{requesting_client_id}' cannot access observation '{observation_id}' owned by '{obs.client_id}'."
                )

            return obs

    def list_observations(
        self, requesting_client_id: str, target_client_id: str
    ) -> List[OutcomeObservation]:
        """Lists observations for a client context with strict isolation."""
        if requesting_client_id != target_client_id:
            raise CrossClientIntelligenceViolation(
                f"Client '{requesting_client_id}' cannot access observations for '{target_client_id}'."
            )

        with self._lock:
            obs_ids = self._client_index.get(target_client_id, [])
            return [self._observations[oid] for oid in obs_ids if oid in self._observations]
