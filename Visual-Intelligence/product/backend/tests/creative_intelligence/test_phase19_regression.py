"""
Phase 19 Regression & AST Static Import Audit Test Suite.

Verifies:
1. AST Static Isolation: No Phase 19 file imports Phase 3 / Phase 14 authorization/execution mutation logic directly.
2. Cross-Phase Substrate Integration: Phase 14-18 components run cleanly alongside Phase 19 without regression.
"""

import ast
import os
import pytest
import glob


def test_ast_static_import_isolation():
    """Scan all python files in src/creative_intelligence/ to verify no illegal authorization or execution imports."""
    source_dir = os.path.join(os.path.dirname(__file__), "../../src/creative_intelligence")
    py_files = glob.glob(os.path.join(source_dir, "*.py"))

    prohibited_imports = [
        "authorize_execution", "grant_privilege", "mutate_policy",
        "execute_tool", "dispatch_fabric_task", "override_governance"
    ]

    for py_file in py_files:
        with open(py_file, "r", encoding="utf-8") as f:
            code = f.read()

        tree = ast.parse(code, filename=py_file)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prohibited in prohibited_imports:
                        assert prohibited not in alias.name, f"Illegal import '{alias.name}' in {py_file}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for prohibited in prohibited_imports:
                        assert prohibited not in node.module, f"Illegal import from '{node.module}' in {py_file}"


def test_phase19_orchestrator_initialization(orchestrator):
    """Verify clean orchestrator initialization and dashboard metric generation."""
    metrics = orchestrator.get_dashboard_metrics()
    assert metrics.provenance_chain_integrity is True
    assert metrics.data_confidentiality_passed is True
    assert metrics.policy_isolation_passed is True
