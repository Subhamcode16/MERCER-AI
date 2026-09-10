"""
Phase 20 Regression & AST Static Import Audit Test Suite.

Verifies:
1. AST Static Isolation: No Phase 20 file imports Phase 3 / Phase 14 authorization/execution mutation logic directly.
2. Orchestrator initialization and cryptographic ledger integrity.
"""

import ast
import os
import glob
import pytest
from src.model_workforce.phase20_orchestrator import Phase20Orchestrator


def test_ast_static_import_isolation():
    """Scan all python files in Phase 20 packages to verify zero illegal authorization or execution imports."""
    packages = [
        "src/model_gateway", "src/visual_model_gateway",
        "src/mcp_gateway", "src/intelligence_evaluation",
        "src/visual_knowledge", "src/model_workforce"
    ]

    base_dir = os.path.join(os.path.dirname(__file__), "../../")
    prohibited_imports = [
        "authorize_execution", "grant_privilege", "mutate_policy",
        "execute_tool", "dispatch_fabric_task", "override_governance"
    ]

    for pkg in packages:
        pkg_dir = os.path.join(base_dir, pkg)
        py_files = glob.glob(os.path.join(pkg_dir, "*.py"))

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


def test_orchestrator_initialization_and_ledger_integrity():
    orch = Phase20Orchestrator()
    assert orch.verify_all_ledgers() is True
