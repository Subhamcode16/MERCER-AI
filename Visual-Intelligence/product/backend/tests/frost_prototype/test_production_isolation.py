"""
Isolation Tests verifying zero coupling between Phase 4 FROST Prototype and Production Security Substrate.
"""

import sys
import ast
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from security_substrate.assurance_loop import AssuranceLoopController
from security_substrate.execution_gate import ExecutionGate
from security_substrate.epistemic_state import EpistemicState

from research.frost_prototype.verification import FROSTSignatureVerifier
from .test_signing import create_test_coordinator


def test_no_security_substrate_imports_in_frost_prototype():
    """AST Audit: Verify no source file under research/frost_prototype imports security_substrate."""
    prototype_dir = Path(__file__).resolve().parent.parent.parent / "src" / "research" / "frost_prototype"
    python_files = list(prototype_dir.glob("*.py"))

    assert len(python_files) > 0

    for py_file in python_files:
        with open(py_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=py_file.name)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "security_substrate" not in alias.name, f"Forbidden import of security_substrate in {py_file.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "security_substrate" not in node.module, f"Forbidden import from security_substrate in {py_file.name}"


def test_frost_prototype_cannot_unlock_execution_gate():
    """Verify evaluating valid FROST prototype signature does NOT unlock ExecutionGate or mutate EpistemicState."""
    assurance_controller = AssuranceLoopController()
    execution_gate = ExecutionGate(assurance_controller)

    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    assert execution_gate.is_permitted() is False

    # Execute valid FROST threshold signing and verification
    coordinator, group_pubkey = create_test_coordinator(total_n=3, threshold_t=2)
    msg = b"Isolation Test Payload"
    sig = coordinator.execute_threshold_signing(msg, [1, 2])
    is_valid = FROSTSignatureVerifier.verify_signature(msg, group_pubkey, sig)

    assert is_valid is True

    # Confirm production security substrate state remains strictly UNKNOWN and ExecutionGate remains LOCKED
    assert assurance_controller.get_current_state() == EpistemicState.UNKNOWN
    assert execution_gate.is_permitted() is False

    exec_res = execution_gate.request_execution("post-frost-action")
    assert exec_res.permitted is False
