"""
Tests for Phase 8 SecurityReconciler.
"""

import threading
import time
from src.security_substrate.reconciliation_integrity import verify_result_commitment
from src.security_substrate.reconciliation_models import (
    ReconciliationSnapshot,
    ReconciliationStatus,
)
from src.security_substrate.security_reconciler import SecurityReconciler


def test_security_reconciler_e2e():
    reconciler = SecurityReconciler()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-300",
        system_id="sys-prod-01",
        correlation_id="corr-300",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-1", "system_id": "sys-prod-01", "correlation_id": "corr-300"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-prod-01", "correlation_id": "corr-300"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-prod-01", "correlation_id": "corr-300"}],
        audit_records=[{"record_id": "aud-1", "system_id": "sys-prod-01", "correlation_id": "corr-300", "chain_valid": True}],
    )

    result = reconciler.reconcile(snapshot)
    assert result.status == ReconciliationStatus.CONSISTENT
    assert result.is_authoritative is False
    assert result.trust_marker == "NON_AUTHORITATIVE_RECONCILIATION_VIEW"
    assert verify_result_commitment(result) is True

    cached = reconciler.get_result(result.result_id)
    assert cached is not None
    assert cached.result_id == result.result_id


def test_security_reconciler_concurrency():
    reconciler = SecurityReconciler()
    results = []
    errors = []

    def _worker(idx: int):
        try:
            snapshot = ReconciliationSnapshot(
                snapshot_id=f"snap-conc-{idx}",
                system_id="sys-conc",
                correlation_id=f"corr-conc-{idx}",
                timestamp=time.time(),
                evidence_records=[{"evidence_id": f"ev-{idx}", "system_id": "sys-conc", "correlation_id": f"corr-conc-{idx}"}],
                decision_records=[{"decision_id": f"dec-{idx}", "system_id": "sys-conc", "correlation_id": f"corr-conc-{idx}"}],
                attestation_records=[{"attestation_id": f"att-{idx}", "system_id": "sys-conc", "correlation_id": f"corr-conc-{idx}"}],
            )
            res = reconciler.reconcile(snapshot)
            results.append(res)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=_worker, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == 10
    query_res = reconciler.query_results(system_id="sys-conc")
    assert len(query_res) == 10
