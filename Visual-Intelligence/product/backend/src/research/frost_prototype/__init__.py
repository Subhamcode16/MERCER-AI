"""
FROST Research Prototype Package.
Provides isolated, research-only threshold signing and mock hardware custody components.

WARNING:
This implementation is a research prototype and is NOT authorized for production cryptographic,
authorization, hardware-custody, or execution-control use.
"""

from .models import (
    FROSTConfig,
    KeyShare,
    NonceCommitment,
    SigningNoncePair,
    SignatureShare,
    FROSTSignature,
)
from .nonce import (
    SigningNonceTracker,
    NonceException,
    NonceReuseException,
)
from .hardware_custodian import (
    MockHardwareCustodian,
    HardwareCustodianException,
    HardwareLockedException,
    HardwareUnavailableException,
    CorruptedShareException,
    HardwareTimeoutException,
)
from .participants import (
    ParticipantNode,
    compute_lagrange_coefficient,
)
from .signing import (
    FROSTSigningCoordinator,
    generate_test_key_set,
    SigningException,
    InsufficientSignersException,
    InvalidParticipantException,
)
from .verification import (
    FROSTSignatureVerifier,
    VerificationException,
)

__all__ = [
    "FROSTConfig",
    "KeyShare",
    "NonceCommitment",
    "SigningNoncePair",
    "SignatureShare",
    "FROSTSignature",
    "SigningNonceTracker",
    "NonceException",
    "NonceReuseException",
    "MockHardwareCustodian",
    "HardwareCustodianException",
    "HardwareLockedException",
    "HardwareUnavailableException",
    "CorruptedShareException",
    "HardwareTimeoutException",
    "ParticipantNode",
    "compute_lagrange_coefficient",
    "FROSTSigningCoordinator",
    "generate_test_key_set",
    "SigningException",
    "InsufficientSignersException",
    "InvalidParticipantException",
    "FROSTSignatureVerifier",
    "VerificationException",
]
