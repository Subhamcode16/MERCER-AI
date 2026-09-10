"""
Phase 8 Static AST & Reflection Isolation Tests.
Mandatory architectural proof that Phase 8 reconciler possesses NO authorization authority.
"""

import ast
import inspect
import time
from pathlib import Path
import pytest

from src.security_substrate import (
    AssuranceLoopController,
    ExecutionGate,
    SecurityReconciler,
    ReconciliationSnapshot,
    ReconciliationStatus,
)


FORBIDDEN_AUTHORIZATION_METHODS = {
    "authorize",
    "verify_for_execution",
    "unlock",
    "execute",
    "grant",
    "permit_execution",
    "override_gate",
    "transition_state",
}


def test_ast_audit_no_forbidden_imports():
    substrate_dir = Path(__file__).parent.parent.parent / "src" / "security_substrate"
    p8_files = [
        substrate_dir / "reconciliation_models.py",
        substrate_dir / "reconciliation_policy.py",
        substrate_dir / "reconciliation_integrity.py",
        substrate_dir / "security_reconciler.py",
    ]

    for filepath in p8_files:
        assert filepath.exists(), f"File {filepath} must exist."
        tree = ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "frost_prototype" not in alias.name, f"Illegal import {alias.name} in {filepath.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "frost_prototype" not in node.module, f"Illegal import {node.module} in {filepath.name}"


def test_reflection_audit_no_authorization_methods():
    methods = [m for m, _ in inspect.getmembers(SecurityReconciler, predicate=inspect.isfunction)]
    for forbidden in FORBIDDEN_AUTHORIZATION_METHODS:
        assert forbidden not in methods, f"SecurityReconciler illegally exposes authorization method '{forbidden}'."


def test_reconciliation_does_not_unlock_execution_gate():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)

    # Initial state fail-closed
    assert gate.is_permitted() is False

    # Execute reconciliation on a consistent snapshot
    reconciler = SecurityReconciler()
    snapshot = ReconciliationSnapshot(
        snapshot_id="snap-iso-01",
        system_id="sys-01",
        correlation_id="corr-iso-01",
        timestamp=time.time(),
        evidence_records=[{"evidence_id": "ev-1", "system_id": "sys-01", "correlation_id": "corr-iso-01"}],
        decision_records=[{"decision_id": "dec-1", "system_id": "sys-01", "correlation_id": "corr-iso-01"}],
        attestation_records=[{"attestation_id": "att-1", "system_id": "sys-01", "correlation_id": "corr-iso-01"}],
        audit_records=[{"record_id": "aud-1", "system_id": "sys-01", "correlation_id": "corr-iso-01", "chain_valid": True}],
    )

    result = reconciler.reconcile(snapshot)
    assert result.status == ReconciliationStatus.CONSISTENT

    # ExecutionGate MUST remain locked (fail-closed)
    assert gate.is_permitted() is False
