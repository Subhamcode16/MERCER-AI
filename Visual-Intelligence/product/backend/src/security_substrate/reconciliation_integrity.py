"""
Reconciliation Integrity & Commitment Helpers for Visual Intelligence Security Substrate (Phase 8).

Provides canonical JSON serialization, SHA-256 snapshot digest generation,
result commitment calculation, and constant-time digest verification.
"""

import hashlib
import hmac
import json
from typing import Any, Dict

from .exceptions import ReconciliationIntegrityException
from .reconciliation_models import ReconciliationResult, ReconciliationSnapshot


def _canonical_json(data: Any) -> str:
    """Serializes data into canonical JSON with sorted keys and compact separators."""
    try:
        return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    except Exception as e:
        raise ReconciliationIntegrityException(f"Canonical serialization failed: {e}") from e


def serialize_reconciliation_snapshot(snapshot: ReconciliationSnapshot) -> str:
    """Returns canonical JSON representation of a ReconciliationSnapshot."""
    if not isinstance(snapshot, ReconciliationSnapshot):
        raise ReconciliationIntegrityException("Object must be a ReconciliationSnapshot instance.")
    return _canonical_json(snapshot.to_dict())


def compute_snapshot_digest(snapshot: ReconciliationSnapshot) -> str:
    """Computes SHA-256 hex digest of a ReconciliationSnapshot's canonical serialization."""
    canonical = serialize_reconciliation_snapshot(snapshot)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_result_commitment(
    result_id: str,
    snapshot_digest: str,
    status_str: str,
    system_id: str,
    correlation_id: str,
    findings_dicts: list,
) -> str:
    """Computes SHA-256 hex commitment for a ReconciliationResult payload."""
    commitment_payload = {
        "result_id": result_id,
        "snapshot_digest": snapshot_digest,
        "status": status_str,
        "system_id": system_id,
        "correlation_id": correlation_id,
        "findings": sorted(findings_dicts, key=lambda f: f.get("finding_id", "")),
        "is_authoritative": False,
        "trust_marker": "NON_AUTHORITATIVE_RECONCILIATION_VIEW",
    }
    canonical = _canonical_json(commitment_payload)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_snapshot_digest(snapshot: ReconciliationSnapshot, expected_digest: str) -> bool:
    """Verifies expected snapshot digest using constant-time comparison."""
    if not isinstance(expected_digest, str) or not expected_digest:
        return False
    actual_digest = compute_snapshot_digest(snapshot)
    return hmac.compare_digest(actual_digest, expected_digest)


def verify_result_commitment(result: ReconciliationResult) -> bool:
    """Verifies that a ReconciliationResult's commitment matches its canonical payload."""
    if not isinstance(result, ReconciliationResult):
        return False
    
    findings_dicts = [f.to_dict() for f in result.findings]
    expected = compute_result_commitment(
        result_id=result.result_id,
        snapshot_digest=result.snapshot_digest,
        status_str=result.status.value,
        system_id=result.system_id,
        correlation_id=result.correlation_id,
        findings_dicts=findings_dicts,
    )
    return hmac.compare_digest(result.result_commitment, expected)
