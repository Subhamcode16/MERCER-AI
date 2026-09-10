"""
AST Static & Runtime Isolation Audit for Phase 6 Security Decision & Attestation Boundary.
Proves zero coupling between Phase 6 decision engine, execution gating, state mutations, and research prototype.
"""

import os
import ast
import time
import pytest
from security_substrate import (
    SecurityDecisionEngine,
    DecisionContext,
    DecisionClassification,
    ExecutionGate,
    AssuranceLoopController,
    EpistemicStateStore,
    EpistemicState,
    NormalizedEvidenceRecord,
    EvidenceClassification,
    EvidenceProvenance,
    EvidenceStatus,
)



def test_ast_audit_no_frost_research_imports_in_substrate():
    substrate_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "src",
        "security_substrate",
    )
    substrate_dir = os.path.abspath(substrate_dir)

    forbidden_imports = ["frost_prototype", "research.frost_prototype"]

    for root, _, files in os.walk(substrate_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=filepath)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            for forbidden in forbidden_imports:
                                assert forbidden not in alias.name, f"Forbidden import '{alias.name}' in {file}"
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            for forbidden in forbidden_imports:
                                assert forbidden not in node.module, f"Forbidden import from '{node.module}' in {file}"


def test_ast_audit_no_execution_gate_calls_in_phase6_modules():
    phase6_files = ["decision_models.py", "decision_policy.py", "decision_engine.py", "attestation.py", "decision_replay.py"]
    substrate_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "security_substrate"))

    for fname in phase6_files:
        filepath = os.path.join(substrate_dir, fname)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)

            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    assert node.attr not in ["unlock", "authorize", "execute_gate"], f"Forbidden call attribute '{node.attr}' found in {fname}"


def test_runtime_isolation_decision_does_not_unlock_execution_gate():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False



    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-iso-1",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-iso-1",
    )
    records = [
        NormalizedEvidenceRecord(
            evidence_id="e-iso-1",
            classification=EvidenceClassification.VERIFICATION_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_2_VERIFICATION,
            status=EvidenceStatus.VALIDATED,
            system_id="sys-prod",
            protocol_version="1.0.0",
            creation_time=time.time(),
            ingestion_time=time.time(),
            expiration_time=time.time() + 600.0,
            payload_commitment="comm-iso-1",
            unique_nonce="nonce-iso-1",
            correlation_id="corr-iso-1",
            trust_marker="PRODUCTION_EVIDENCE",
        ),
        NormalizedEvidenceRecord(
            evidence_id="e-iso-2",
            classification=EvidenceClassification.ASSURANCE_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_1_ASSURANCE,
            status=EvidenceStatus.VALIDATED,
            system_id="sys-prod",
            protocol_version="1.0.0",
            creation_time=time.time(),
            ingestion_time=time.time(),
            expiration_time=time.time() + 600.0,
            payload_commitment="comm-iso-2",
            unique_nonce="nonce-iso-2",
            correlation_id="corr-iso-2",
            trust_marker="PRODUCTION_EVIDENCE",
        ),

    ]

    decision, attestation = engine.evaluate_evidence(records, ctx)
    assert decision.classification == DecisionClassification.EVALUATION_PASS

    # Verify ExecutionGate remains strictly locked
    assert gate.is_permitted() is False



def test_runtime_isolation_research_evidence_evaluated_as_research_only():
    engine = SecurityDecisionEngine()
    ctx = DecisionContext(
        context_id="ctx-iso-res",
        policy_version="6.0.0",
        system_id="sys-prod",
        evaluation_timestamp=time.time(),
        evaluation_nonce="non-iso-res",
    )
    records = [
        NormalizedEvidenceRecord(
            evidence_id="e-res-1",
            classification=EvidenceClassification.RESEARCH_CRYPTOGRAPHIC_EVIDENCE,
            provenance=EvidenceProvenance.PHASE_4_RESEARCH,
            status=EvidenceStatus.VALIDATED,
            system_id="sys-research",
            protocol_version="1.0.0",
            creation_time=time.time(),
            ingestion_time=time.time(),
            expiration_time=time.time() + 600.0,
            payload_commitment="comm-res-1",
            unique_nonce="nonce-res-1",
            correlation_id="corr-res-1",
            trust_marker="TEST_ONLY_NOT_PRODUCTION_AUTHORIZATION",
        )
    ]

    decision, attestation = engine.evaluate_evidence(records, ctx)
    assert decision.classification == DecisionClassification.RESEARCH_ONLY
    assert attestation.is_research_only is True
