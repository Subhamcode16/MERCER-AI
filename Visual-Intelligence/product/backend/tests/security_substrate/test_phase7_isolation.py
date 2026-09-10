"""
AST Static & Runtime Isolation Audit for Phase 7 Security Audit & Integrity Boundary.
Proves zero coupling between Phase 7 audit logging, execution gating, state mutations, and research prototype.
"""

import os
import ast
import time
import pytest
from security_substrate import (
    SecurityAuditBoundary,
    AttestationRecord,
    DecisionClassification,
    ExecutionGate,
    AssuranceLoopController,
)


def test_ast_audit_no_forbidden_phase7_imports():
    phase7_files = ["audit_models.py", "audit_integrity.py", "audit_store.py", "audit_boundary.py"]
    substrate_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "security_substrate"))

    forbidden_modules = ["frost_prototype", "research.frost_prototype", "execution_gate", "assurance_loop", "epistemic_state"]

    for fname in phase7_files:
        filepath = os.path.join(substrate_dir, fname)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for forbidden in forbidden_modules:
                            assert forbidden not in alias.name, f"Forbidden import '{alias.name}' in {fname}"
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for forbidden in forbidden_modules:
                            assert forbidden not in node.module, f"Forbidden import from '{node.module}' in {fname}"


def test_ast_audit_no_execution_methods_in_phase7_modules():
    phase7_files = ["audit_models.py", "audit_integrity.py", "audit_store.py", "audit_boundary.py"]
    substrate_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "security_substrate"))

    forbidden_attrs = ["unlock", "authorize", "grant_access", "execute_gate", "verify_for_execution", "set_verified"]

    for fname in phase7_files:
        filepath = os.path.join(substrate_dir, fname)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)

            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    assert node.attr not in forbidden_attrs, f"Forbidden attribute '{node.attr}' in {fname}"


def test_runtime_isolation_audit_recording_does_not_unlock_execution_gate():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    boundary = SecurityAuditBoundary()
    att = AttestationRecord(
        attestation_id="att-iso-7",
        decision_id="dec-iso-7",
        decision_commitment="comm-iso-7",
        policy_version="6.0.0",
        classification=DecisionClassification.EVALUATION_PASS,
        attestation_timestamp=time.time(),
        attestation_nonce="nonce-iso-7",
        evidence_commitments=["ev-comm-1"],
        is_research_only=False,
    )

    rec = boundary.record_attestation(att)
    assert rec.sequence_number == 1

    # ExecutionGate must remain strictly locked
    assert gate.is_permitted() is False
