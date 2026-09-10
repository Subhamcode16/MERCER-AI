"""
FROST Research Prototype Models & Data Structures.
ALL CRYPTOGRAPHIC MATERIALS ARE TEST_ONLY RESEARCH ARTIFACTS.
NOT FOR PRODUCTION USE.
"""

import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

# Standard 256-bit Schnorr prime subgroup parameters for research prototype field math
GROUP_ORDER_Q = 115792089237316195423570985008687907853269984665640564039457584007913129639747  # 2**256 - 189
FIELD_PRIME_P = 3936931034068750644401413490295388867011179478631779177341557856269046407751399  # 34 * Q + 1
GENERATOR_G = 17179869184  # 2**34 mod P


@dataclass
class FROSTConfig:
    """
    Threshold signing scheme configuration (t-of-n).
    Invariant: 1 <= threshold_t <= total_participants_n
    """
    total_participants_n: int
    threshold_t: int

    def __post_init__(self):
        if self.total_participants_n < 1:
            raise ValueError("total_participants_n must be at least 1")
        if self.threshold_t < 1:
            raise ValueError("threshold_t must be at least 1")
        if self.threshold_t > self.total_participants_n:
            raise ValueError(f"threshold_t ({self.threshold_t}) cannot exceed total_participants_n ({self.total_participants_n})")


@dataclass
class KeyShare:
    """
    Participant synthetic secret share material (TEST_ONLY).
    """
    participant_id: int
    secret_share: int  # TEST_ONLY scalar s_i
    public_share: int  # TEST_ONLY public key point Y_i
    group_public_key: int  # TEST_ONLY group public key Y
    marker: str = "TEST_ONLY_SYNTHETIC_SHARE"

    def __post_init__(self):
        if self.participant_id < 1:
            raise ValueError("participant_id must be a positive integer >= 1")


@dataclass
class NonceCommitment:
    """
    Round 1 Nonce Commitment pair (D_i, E_i) for a participant.
    """
    participant_id: int
    nonce_identifier: str
    commitment_hiding: int   # D_i = d_i * G mod P
    commitment_binding: int  # E_i = e_i * G mod P
    marker: str = "TEST_ONLY_COMMITMENT"


@dataclass
class SigningNoncePair:
    """
    Participant per-signature secret nonces (d_i, e_i) (TEST_ONLY).
    Must never be reused or exposed.
    """
    participant_id: int
    nonce_identifier: str
    hiding_nonce: int   # d_i
    binding_nonce: int  # e_i
    marker: str = "TEST_ONLY_SECRET_NONCE"


@dataclass
class SignatureShare:
    """
    Round 2 Partial signature contribution z_i from participant_id.
    """
    participant_id: int
    partial_sig: int  # z_i = (d_i + rho_i * e_i) + lambda_i * s_i * c mod Q
    marker: str = "TEST_ONLY_SIGNATURE_SHARE"


@dataclass
class FROSTSignature:
    """
    Aggregated FROST Threshold Signature (R, S).
    """
    group_commitment_R: int  # R = sum(R_i) mod P
    signature_scalar_S: int  # S = sum(z_i) mod Q
    message_hash: str
    participating_ids: List[int]
    marker: str = "TEST_ONLY_THRESHOLD_SIGNATURE"
