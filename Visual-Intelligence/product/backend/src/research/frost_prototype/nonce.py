"""
FROST Research Prototype Nonce Safety & Consumption Tracker.
Enforces non-reusability, atomic tracking, and duplicate rejection.
ALL NONCES ARE TEST_ONLY RESEARCH ARTIFACTS.
"""

import secrets
import threading
from typing import Dict, Set, Tuple, Optional
from .models import SigningNoncePair, NonceCommitment, GROUP_ORDER_Q, FIELD_PRIME_P, GENERATOR_G


class NonceException(Exception):
    """Base exception for FROST prototype nonce errors."""
    pass


class NonceReuseException(NonceException):
    """Raised when a secret nonce or commitment is reused or replayed."""
    pass


class SigningNonceTracker:
    """
    Thread-safe tracker for participant signing nonces and commitments.
    Ensures per-signature nonces are used strictly ONCE and rejected on reuse.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._consumed_nonces: Set[str] = set()
        self._consumed_commitments: Set[Tuple[int, int]] = set()

    def generate_nonce_pair(self, participant_id: int, nonce_id: Optional[str] = None) -> Tuple[SigningNoncePair, NonceCommitment]:
        """
        Generates a fresh, cryptographically random nonce pair and its public commitments.
        """
        with self._lock:
            nid = nonce_id or f"nonce-{participant_id}-{secrets.token_hex(8)}"
            
            if nid in self._consumed_nonces:
                raise NonceReuseException(f"Duplicate nonce identifier requested: {nid}")

            # Sample random nonces d_i, e_i in [1, Q-1]
            hiding = 1 + secrets.randbelow(GROUP_ORDER_Q - 1)
            binding = 1 + secrets.randbelow(GROUP_ORDER_Q - 1)

            # Compute public commitments D_i = d_i * G mod P, E_i = e_i * G mod P
            comm_d = pow(GENERATOR_G, hiding, FIELD_PRIME_P)
            comm_e = pow(GENERATOR_G, binding, FIELD_PRIME_P)

            comm_tuple = (comm_d, comm_e)
            if comm_tuple in self._consumed_commitments:
                raise NonceReuseException("Generated commitment collision detected")

            secret_pair = SigningNoncePair(
                participant_id=participant_id,
                nonce_identifier=nid,
                hiding_nonce=hiding,
                binding_nonce=binding
            )
            commitment = NonceCommitment(
                participant_id=participant_id,
                nonce_identifier=nid,
                commitment_hiding=comm_d,
                commitment_binding=comm_e
            )

            return secret_pair, commitment

    def consume_nonce(self, participant_id: int, nonce_id: str, commitment: NonceCommitment) -> bool:
        """
        Atomically marks a nonce identifier and commitment pair as consumed.
        Returns True if fresh and consumed; raises NonceReuseException if previously consumed.
        """
        with self._lock:
            if nonce_id in self._consumed_nonces:
                raise NonceReuseException(f"Nonce identifier {nonce_id} has already been consumed for participant {participant_id}")

            comm_tuple = (commitment.commitment_hiding, commitment.commitment_binding)
            if comm_tuple in self._consumed_commitments:
                raise NonceReuseException(f"Commitment pair for nonce {nonce_id} has already been consumed")

            self._consumed_nonces.add(nonce_id)
            self._consumed_commitments.add(comm_tuple)
            return True

    def is_consumed(self, nonce_id: str) -> bool:
        """Checks if a nonce identifier has been consumed."""
        with self._lock:
            return nonce_id in self._consumed_nonces
