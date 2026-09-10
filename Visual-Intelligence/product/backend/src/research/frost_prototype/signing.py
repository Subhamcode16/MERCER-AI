"""
FROST Threshold Signing Coordinator Implementation.
Orchestrates polynomial key setup (t-of-n), Round 1 commitment collection, Round 2 signature share collection, and aggregation.
ALL OPERATIONS ARE TEST_ONLY RESEARCH ARTIFACTS.
"""

import secrets
import hashlib
from typing import List, Dict, Tuple, Optional
from .models import (
    FROSTConfig,
    KeyShare,
    NonceCommitment,
    SignatureShare,
    FROSTSignature,
    GROUP_ORDER_Q,
    FIELD_PRIME_P,
    GENERATOR_G
)
from .commitments import compute_group_commitment, compute_challenge
from .participants import ParticipantNode
from .hardware_custodian import MockHardwareCustodian, HardwareCustodianException


class SigningException(Exception):
    """Base exception for FROST signing workflow failures."""
    pass


class InsufficientSignersException(SigningException):
    """Raised when participating signers count is below threshold t."""
    pass


class InvalidParticipantException(SigningException):
    """Raised when duplicate or invalid participants are selected for signing."""
    pass


def generate_test_key_set(total_n: int, threshold_t: int) -> Tuple[int, Dict[int, KeyShare]]:
    """
    Helper function generating synthetic Shamir secret shares for a t-of-n setup.
    f(x) = a_0 + a_1*x + ... + a_{t-1}*x^{t-1} mod Q
    Returns (group_public_key_Y, {participant_id: KeyShare}).
    """
    config = FROSTConfig(total_participants_n=total_n, threshold_t=threshold_t)

    # Master secret a_0 = s in [1, Q-1]
    a_0 = 1 + secrets.randbelow(GROUP_ORDER_Q - 1)
    coeffs = [a_0] + [secrets.randbelow(GROUP_ORDER_Q) for _ in range(threshold_t - 1)]

    group_public_key_Y = pow(GENERATOR_G, a_0, FIELD_PRIME_P)
    shares: Dict[int, KeyShare] = {}

    for i in range(1, total_n + 1):
        # Evaluate polynomial f(i) mod Q
        s_i = 0
        x_pow = 1
        for coeff in coeffs:
            s_i = (s_i + coeff * x_pow) % GROUP_ORDER_Q
            x_pow = (x_pow * i) % GROUP_ORDER_Q

        public_share_Y_i = pow(GENERATOR_G, s_i, FIELD_PRIME_P)
        shares[i] = KeyShare(
            participant_id=i,
            secret_share=s_i,
            public_share=public_share_Y_i,
            group_public_key=group_public_key_Y
        )

    return group_public_key_Y, shares


class FROSTSigningCoordinator:
    """
    Orchestrates t-of-n FROST signing rounds.
    """
    def __init__(self, config: FROSTConfig, group_public_key: int, participant_nodes: Dict[int, ParticipantNode]):
        self.config = config
        self.group_public_key = group_public_key
        self.nodes = participant_nodes

    def execute_threshold_signing(
        self,
        message: bytes,
        signer_ids: List[int],
        pin_map: Optional[Dict[int, str]] = None
    ) -> FROSTSignature:
        """
        Executes complete 2-round FROST threshold signing protocol for the given message.
        """
        pin_map = pin_map or {}

        # 1. Signer Validation
        if len(signer_ids) < self.config.threshold_t:
            raise InsufficientSignersException(
                f"Insufficient signers: got {len(signer_ids)}, required threshold is {self.config.threshold_t}"
            )

        if len(set(signer_ids)) != len(signer_ids):
            raise InvalidParticipantException("Duplicate participant IDs in signing set")

        for p_id in signer_ids:
            if p_id not in self.nodes:
                raise InvalidParticipantException(f"Participant ID {p_id} is not registered in coordinator")

        # 2. Round 1: Collect Nonce Commitments
        commitments: List[NonceCommitment] = []
        nonce_ids: Dict[int, str] = {}

        for p_id in signer_ids:
            nid = f"sig-nonce-{p_id}-{secrets.token_hex(6)}"
            node = self.nodes[p_id]
            comm = node.generate_round1_commitment(nid)
            commitments.append(comm)
            nonce_ids[p_id] = nid

        # 3. Compute Group Commitment R, Binding Factors rho_i, and Challenge c
        aggregate_R, rhos = compute_group_commitment(commitments, message)
        challenge_c = compute_challenge(aggregate_R, self.group_public_key, message)

        # 4. Round 2: Collect Partial Signature Shares z_i
        signature_shares: List[SignatureShare] = []
        comm_map = {c.participant_id: c for c in commitments}

        for p_id in signer_ids:
            node = self.nodes[p_id]
            nid = nonce_ids[p_id]
            comm = comm_map[p_id]
            rho_i = rhos[p_id]
            pin = pin_map.get(p_id, "123456")

            sig_share = node.generate_round2_signature_share(
                nonce_id=nid,
                commitment=comm,
                rho_i=rho_i,
                challenge_c=challenge_c,
                signing_set=signer_ids,
                pin=pin
            )
            signature_shares.append(sig_share)

        # 5. Aggregate Signature Shares S = sum(z_i) mod Q
        aggregate_S = 0
        for share in signature_shares:
            aggregate_S = (aggregate_S + share.partial_sig) % GROUP_ORDER_Q

        msg_hash = hashlib.sha256(message).hexdigest()

        return FROSTSignature(
            group_commitment_R=aggregate_R,
            signature_scalar_S=aggregate_S,
            message_hash=msg_hash,
            participating_ids=sorted(signer_ids)
        )
