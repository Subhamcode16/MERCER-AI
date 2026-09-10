"""
IF-ASSURE-001 AssuranceLoopController implementation and state management.
Enforces Verification -> Evidence -> Assurance -> Epistemic State separation.
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional, Set

from .epistemic_state import EpistemicState, validate_transition
from .exceptions import (
    MalformedEvidenceException,
    ReplayAttackException,
    StaleTimestampException,
    FailClosedException,
    InvalidStateTransitionException,
)

MAX_FRESHNESS_WINDOW_SECONDS = 900.0  # 15 minutes


@dataclass
class EvidencePayload:
    """
    Evidence Payload output produced by upstream Verification Domain.
    """
    claim_id: str
    asset_hash: str
    signature: str
    timestamp: float
    nonce: str
    status: str  # "PASS" or "FAIL"
    trust_anchor_id: str


class ConsumedNonceCache:
    """
    Thread-safe in-memory cache for consumed nonces (RunID).
    Process restart clears this volatile memory, relying on system state resetting to UNKNOWN on boot.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._nonces: Set[str] = set()

    def has_nonce(self, nonce: str) -> bool:
        with self._lock:
            return nonce in self._nonces

    def add_nonce(self, nonce: str) -> None:
        with self._lock:
            self._nonces.add(nonce)

    def check_and_add(self, nonce: str) -> bool:
        """
        Atomically checks if nonce exists; if not, adds it under a single lock acquisition.
        Returns True if nonce was successfully added (fresh); False if replayed.
        """
        with self._lock:
            if nonce in self._nonces:
                return False
            self._nonces.add(nonce)
            return True

    def clear(self) -> None:
        with self._lock:
            self._nonces.clear()


class EpistemicStateStore:
    """
    Thread-safe storage for the active EpistemicState.
    """
    def __init__(self, initial_state: EpistemicState = EpistemicState.UNKNOWN):
        self._lock = threading.RLock()
        self._state: EpistemicState = initial_state

    def get_state(self) -> EpistemicState:
        with self._lock:
            return self._state

    def transition_to(self, target_state: EpistemicState) -> EpistemicState:
        with self._lock:
            validate_transition(self._state, target_state)
            self._state = target_state
            return self._state

    def force_blocked(self) -> EpistemicState:
        """Emergency fail-closed transition to BLOCKED."""
        with self._lock:
            self._state = EpistemicState.BLOCKED
            return self._state


class AssuranceLoopController:
    """
    IF-ASSURE-001 Assurance Domain Controller.
    Evaluates evidence payloads issued by Verification Domain and manages monotonic epistemic state.
    """
    def __init__(self, store: Optional[EpistemicStateStore] = None):
        self.store = store or EpistemicStateStore()
        self.nonce_cache = ConsumedNonceCache()

    def get_current_state(self) -> EpistemicState:
        return self.store.get_state()

    def ingest_claim_start(self, claim_id: str) -> EpistemicState:
        """
        Transitions state to UNVERIFIED upon receiving a candidate claim for evaluation.
        """
        if not claim_id or not isinstance(claim_id, str):
            self.store.force_blocked()
            raise MalformedEvidenceException("Invalid claim_id provided to ingest_claim_start")

        try:
            current = self.store.get_state()
            if current in (EpistemicState.UNKNOWN, EpistemicState.STALE, EpistemicState.REASSESSMENT_REQUIRED):
                return self.store.transition_to(EpistemicState.UNVERIFIED)
            elif current == EpistemicState.UNVERIFIED:
                return current
            else:
                self.store.force_blocked()
                raise InvalidStateTransitionException(f"Cannot ingest claim start in state {current.value}")
        except InvalidStateTransitionException:
            self.store.force_blocked()
            raise
        except Exception as e:
            self.store.force_blocked()
            raise FailClosedException(f"Unexpected error during ingest_claim_start: {str(e)}") from e

    def update_epistemic_state(self, evidence: EvidencePayload) -> EpistemicState:
        """
        IF-ASSURE-001 Interface Method: Evaluates signed evidence payload and updates epistemic state.
        """
        try:
            # 1. Structural Verification
            if not evidence or not isinstance(evidence, EvidencePayload):
                self.store.force_blocked()
                raise MalformedEvidenceException("Evidence payload must be an instance of EvidencePayload")

            if not evidence.claim_id or not evidence.asset_hash or not evidence.signature or not evidence.nonce:
                self.store.force_blocked()
                raise MalformedEvidenceException("Evidence payload contains empty mandatory fields")

            if not evidence.trust_anchor_id:
                self.store.force_blocked()
                raise MalformedEvidenceException("Evidence payload missing trust_anchor_id")

            # 2. Replay & Freshness Verification (Atomic check-and-add on success)
            if not self.nonce_cache.check_and_add(evidence.nonce):
                self.store.force_blocked()
                raise ReplayAttackException(f"Replayed nonce detected: {evidence.nonce}")

            # 3. Freshness Verification
            current_time = time.time()
            age = current_time - evidence.timestamp
            if age > MAX_FRESHNESS_WINDOW_SECONDS or age < -5.0:  # Allow 5s clock skew
                self.store.force_blocked()
                raise StaleTimestampException(f"Evidence timestamp stale or future-dated: age={age:.2f}s")

            # 4. Status Evaluation
            if evidence.status != "PASS":
                self.store.force_blocked()
                raise MalformedEvidenceException(f"Evidence evaluation status is non-passing: {evidence.status}")

            # 5. Transition to VERIFIED
            return self.store.transition_to(EpistemicState.VERIFIED)

        except (MalformedEvidenceException, ReplayAttackException, StaleTimestampException, InvalidStateTransitionException):
            self.store.force_blocked()
            raise
        except Exception as e:
            self.store.force_blocked()
            raise FailClosedException(f"Unexpected exception during state update: {str(e)}") from e

    def trigger_stale(self) -> EpistemicState:
        """Transitions active state to STALE upon freshness expiration."""
        try:
            return self.store.transition_to(EpistemicState.STALE)
        except Exception:
            return self.store.force_blocked()

    def trigger_reassessment(self) -> EpistemicState:
        """Transitions active state to REASSESSMENT_REQUIRED."""
        try:
            return self.store.transition_to(EpistemicState.REASSESSMENT_REQUIRED)
        except Exception:
            return self.store.force_blocked()

    def trigger_panic(self) -> EpistemicState:
        """Transitions active state to RECOVERY_REQUIRED upon panic lock."""
        try:
            return self.store.transition_to(EpistemicState.RECOVERY_REQUIRED)
        except Exception:
            return self.store.force_blocked()

    def execute_recovery_reset(self, recovery_auth_valid: bool) -> EpistemicState:
        """
        Executes out-of-band administrative recovery reset.
        RECOVERY_REQUIRED -> UNKNOWN (NEVER directly to VERIFIED).
        """
        if self.store.get_state() != EpistemicState.RECOVERY_REQUIRED:
            self.store.force_blocked()
            raise InvalidStateTransitionException("Recovery reset can only be executed from RECOVERY_REQUIRED state.")

        if not recovery_auth_valid:
            self.store.force_blocked()
            raise FailClosedException("Invalid recovery authorization payload.")

        # Wipe nonce cache and reset state strictly to UNKNOWN
        self.nonce_cache.clear()
        return self.store.transition_to(EpistemicState.UNKNOWN)
