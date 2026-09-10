"""
Participant Node Implementation for FROST Research Prototype.
Simulates participant signing round operations, Lagrange weighting, and signature share creation.
ALL COMPUTATIONS ARE TEST_ONLY RESEARCH ARTIFACTS.
"""

from typing import List, Dict, Tuple, Optional
from .models import KeyShare, NonceCommitment, SigningNoncePair, SignatureShare, GROUP_ORDER_Q
from .hardware_custodian import MockHardwareCustodian
from .nonce import SigningNonceTracker, NonceReuseException


def compute_lagrange_coefficient(participant_id: int, signing_set: List[int]) -> int:
    """
    Computes Lagrange interpolation coefficient lambda_i for participant_id in signing_set.
    lambda_i = prod(j / (j - i) mod Q) for all j in signing_set, j != i.
    """
    num = 1
    den = 1
    for j in signing_set:
        if j == participant_id:
            continue
        num = (num * j) % GROUP_ORDER_Q
        diff = (j - participant_id) % GROUP_ORDER_Q
        den = (den * diff) % GROUP_ORDER_Q

    den_inv = pow(den, GROUP_ORDER_Q - 2, GROUP_ORDER_Q)
    lambda_i = (num * den_inv) % GROUP_ORDER_Q
    return lambda_i


class ParticipantNode:
    """
    Simulated FROST Participant Node.
    Holds a MockHardwareCustodian, generates nonces, and computes signature shares.
    """
    def __init__(self, participant_id: int, custodian: MockHardwareCustodian, nonce_tracker: Optional[SigningNonceTracker] = None):
        self.participant_id = participant_id
        self.custodian = custodian
        self.nonce_tracker = nonce_tracker or SigningNonceTracker()
        self._active_nonces: Dict[str, SigningNoncePair] = {}

    def generate_round1_commitment(self, nonce_id: Optional[str] = None) -> NonceCommitment:
        """
        Round 1: Generates fresh secret nonce pair (d_i, e_i) and returns public commitment (D_i, E_i).
        """
        secret_pair, commitment = self.nonce_tracker.generate_nonce_pair(self.participant_id, nonce_id)
        self._active_nonces[commitment.nonce_identifier] = secret_pair
        return commitment

    def generate_round2_signature_share(
        self,
        nonce_id: str,
        commitment: NonceCommitment,
        rho_i: int,
        challenge_c: int,
        signing_set: List[int],
        pin: str = "123456"
    ) -> SignatureShare:
        """
        Round 2: Authenticates with custodian, retrieves share s_i, computes Lagrange factor lambda_i,
        computes z_i = (d_i + rho_i * e_i) + lambda_i * s_i * c mod Q,
        and atomically consumes the secret nonce pair to prevent reuse.
        """
        if nonce_id not in self._active_nonces:
            raise NonceReuseException(f"No active secret nonce found for identifier {nonce_id}")

        secret_pair = self._active_nonces[nonce_id]

        # Atomically mark nonce as consumed; raises NonceReuseException if replayed
        self.nonce_tracker.consume_nonce(self.participant_id, nonce_id, commitment)

        # Retrieve share from mock hardware custodian
        key_share = self.custodian.authenticate_and_fetch_share(pin)

        # Compute Lagrange coefficient lambda_i for active threshold set
        lambda_i = compute_lagrange_coefficient(self.participant_id, signing_set)

        # Compute partial signature share z_i = (d_i + rho_i * e_i) + lambda_i * s_i * c mod Q
        nonce_sum = (secret_pair.hiding_nonce + (rho_i * secret_pair.binding_nonce)) % GROUP_ORDER_Q
        share_term = (lambda_i * key_share.secret_share * challenge_c) % GROUP_ORDER_Q
        z_i = (nonce_sum + share_term) % GROUP_ORDER_Q

        # Wipe local secret nonce reference
        del self._active_nonces[nonce_id]

        return SignatureShare(
            participant_id=self.participant_id,
            partial_sig=z_i
        )
