"""
FROST Research Prototype Commitments & Binding Factor Computation.
Calculates per-participant binding factors and aggregated group commitments.
ALL CALCULATIONS ARE TEST_ONLY RESEARCH ARTIFACTS.
"""

import hashlib
from typing import List, Dict, Tuple
from .models import NonceCommitment, GROUP_ORDER_Q, FIELD_PRIME_P, GENERATOR_G


def compute_binding_factor(
    participant_id: int,
    message: bytes,
    commitments: List[NonceCommitment]
) -> int:
    """
    Computes participant binding factor rho_i = H(i, message, B) mod Q
    where B is the canonical serialized string of all participant commitments.
    """
    # Sort commitments by participant_id for canonical ordering
    sorted_comms = sorted(commitments, key=lambda c: c.participant_id)
    b_str = ",".join(f"{c.participant_id}:{c.commitment_hiding}:{c.commitment_binding}" for c in sorted_comms)

    hasher = hashlib.sha256()
    hasher.update(str(participant_id).encode("utf-8"))
    hasher.update(b":")
    hasher.update(message)
    hasher.update(b":")
    hasher.update(b_str.encode("utf-8"))

    digest = hasher.digest()
    rho = int.from_bytes(digest, byteorder="big") % GROUP_ORDER_Q
    return rho if rho != 0 else 1


def compute_participant_commitment(
    comm: NonceCommitment,
    binding_factor_rho: int
) -> int:
    """
    Computes participant effective commitment R_i = (D_i * (E_i ^ rho_i mod P)) mod P
    """
    e_rho = pow(comm.commitment_binding, binding_factor_rho, FIELD_PRIME_P)
    r_i = (comm.commitment_hiding * e_rho) % FIELD_PRIME_P
    return r_i


def compute_group_commitment(
    commitments: List[NonceCommitment],
    message: bytes
) -> Tuple[int, Dict[int, int]]:
    """
    Computes overall group commitment R = prod(R_i) mod P
    and returns (R, {participant_id: rho_i}).
    """
    rhos: Dict[int, int] = {}
    aggregate_R = 1

    for comm in commitments:
        rho_i = compute_binding_factor(comm.participant_id, message, commitments)
        rhos[comm.participant_id] = rho_i
        r_i = compute_participant_commitment(comm, rho_i)
        aggregate_R = (aggregate_R * r_i) % FIELD_PRIME_P

    return aggregate_R, rhos


def compute_challenge(
    group_commitment_R: int,
    group_public_key_Y: int,
    message: bytes
) -> int:
    """
    Computes challenge scalar c = H(R, Y, message) mod Q.
    """
    hasher = hashlib.sha256()
    hasher.update(str(group_commitment_R).encode("utf-8"))
    hasher.update(b":")
    hasher.update(str(group_public_key_Y).encode("utf-8"))
    hasher.update(b":")
    hasher.update(message)

    digest = hasher.digest()
    c = int.from_bytes(digest, byteorder="big") % GROUP_ORDER_Q
    return c if c != 0 else 1
