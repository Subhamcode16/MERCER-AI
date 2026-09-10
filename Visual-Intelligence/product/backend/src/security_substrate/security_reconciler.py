"""
Security Reconciler for Visual Intelligence Security Substrate (Phase 8).

Constructs non-authoritative reconciliation views summarizing security record consistency across Phases 1-7.
Operates under thread-safe locking and enforces zero execution gating or state mutation authority.
"""

import threading
import time
from typing import Dict, List, Optional

from .exceptions import (
    ReconciliationReferenceException,
    ReconciliationSchemaException,
)
from .reconciliation_integrity import (
    compute_result_commitment,
    compute_snapshot_digest,
)
from .reconciliation_models import (
    ReconciliationResult,
    ReconciliationSnapshot,
    ReconciliationStatus,
)
from .reconciliation_policy import ReconciliationPolicy


class SecurityReconciler:
    """
    Thread-safe, non-authoritative security record reconciler.
    
    Evaluates pre-fetched security record snapshots and returns deterministic consistency results.
    Guaranteed to possess NO gating or authorization authority methods.
    """

    def __init__(self, policy: Optional[ReconciliationPolicy] = None) -> None:
        self._lock = threading.RLock()
        self._policy = policy or ReconciliationPolicy()
        self._results: Dict[str, ReconciliationResult] = {}
        self._result_seq = 0

    def reconcile(self, snapshot: ReconciliationSnapshot) -> ReconciliationResult:
        """
        Evaluates a ReconciliationSnapshot and returns a signed ReconciliationResult.
        
        This method is strictly non-authoritative. A status of CONSISTENT does not imply VERIFIED or AUTHORIZED.
        """
        if not isinstance(snapshot, ReconciliationSnapshot):
            raise ReconciliationSchemaException("Input must be a ReconciliationSnapshot instance.")

        with self._lock:
            # 1. Compute deterministic snapshot digest
            snap_digest = compute_snapshot_digest(snapshot)

            # 2. Evaluate snapshot using ReconciliationPolicy
            status, findings = self._policy.evaluate(snapshot)

            # 3. Generate result identity
            self._result_seq += 1
            result_id = f"rec-res-{snapshot.system_id}-{self._result_seq:06d}"
            timestamp = time.time()

            # 4. Compute SHA-256 result commitment
            findings_dicts = [f.to_dict() for f in findings]
            commitment = compute_result_commitment(
                result_id=result_id,
                snapshot_digest=snap_digest,
                status_str=status.value,
                system_id=snapshot.system_id,
                correlation_id=snapshot.correlation_id,
                findings_dicts=findings_dicts,
            )

            # 5. Construct ReconciliationResult
            result = ReconciliationResult(
                result_id=result_id,
                snapshot_id=snapshot.snapshot_id,
                system_id=snapshot.system_id,
                correlation_id=snapshot.correlation_id,
                status=status,
                timestamp=timestamp,
                findings=findings,
                snapshot_digest=snap_digest,
                result_commitment=commitment,
            )

            # 6. Cache result locally (append-only in memory)
            self._results[result_id] = result
            return result

    def get_result(self, result_id: str) -> Optional[ReconciliationResult]:
        """Returns a cached ReconciliationResult by result_id, or None if not found."""
        if not isinstance(result_id, str) or not result_id.strip():
            raise ReconciliationReferenceException("result_id must be a non-empty string.")
        with self._lock:
            return self._results.get(result_id)

    def query_results(
        self,
        system_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        status: Optional[ReconciliationStatus] = None,
    ) -> List[ReconciliationResult]:
        """Queries cached reconciliation results filtered by system_id, correlation_id, or status."""
        with self._lock:
            matched = list(self._results.values())
            if system_id:
                matched = [r for r in matched if r.system_id == system_id]
            if correlation_id:
                matched = [r for r in matched if r.correlation_id == correlation_id]
            if status:
                matched = [r for r in matched if r.status == status]
            return sorted(matched, key=lambda r: r.timestamp, reverse=True)
