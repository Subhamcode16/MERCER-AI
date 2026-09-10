"""
Cryptographic utility functions for Option H Verification Harness.
Implements salted asset commitments, HMAC signatures, and nonce generation.
"""

import hmac
import hashlib
import secrets
from typing import Dict, Any


def compute_salted_commitment(asset_bytes: bytearray, salt_bytes: bytes) -> str:
    """
    Computes a salted SHA-256 hash commitment over transient raw asset bytes.
    Commitment = SHA-256(asset_bytes || salt_bytes)
    """
    if not isinstance(asset_bytes, (bytearray, bytes)):
        raise TypeError("asset_bytes must be a bytearray or bytes object")
    if not isinstance(salt_bytes, bytes) or len(salt_bytes) < 32:
        raise ValueError("salt_bytes must be a bytes object of at least 32 bytes to ensure 256-bit entropy")

    hasher = hashlib.sha256()
    hasher.update(asset_bytes)
    hasher.update(salt_bytes)
    return hasher.hexdigest()


def generate_salt(length: int = 32) -> bytes:
    """Generates a cryptographically secure random salt."""
    return secrets.token_bytes(length)


def generate_nonce(length: int = 16) -> str:
    """Generates a 256-bit random hex nonce (RunID)."""
    return secrets.token_hex(length)


def sign_evidence_payload(payload_fields: Dict[str, Any], secret_key: bytes) -> str:
    """
    Computes HMAC-SHA256 signature over evidence payload fields.
    """
    if not secret_key or not isinstance(secret_key, bytes):
        raise ValueError("secret_key must be a non-empty bytes object")

    # Canonical string representation of signature fields
    msg = f"{payload_fields.get('claim_id')}:{payload_fields.get('asset_hash')}:{payload_fields.get('timestamp')}:{payload_fields.get('nonce')}:{payload_fields.get('status')}:{payload_fields.get('trust_anchor_id')}"
    return hmac.new(secret_key, msg.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_evidence_signature(payload_fields: Dict[str, Any], signature: str, secret_key: bytes) -> bool:
    """
    Verifies HMAC-SHA256 signature over evidence payload fields using constant-time comparison.
    """
    if not signature or not isinstance(signature, str):
        return False
    expected_sig = sign_evidence_payload(payload_fields, secret_key)
    return hmac.compare_digest(expected_sig, signature)
