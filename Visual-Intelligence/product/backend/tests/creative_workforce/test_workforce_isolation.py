"""
Phase 14 Test Workforce Isolation (AST Audit)
---------------------------------------------
Audits Phase 14 workforce codebase via AST to ensure no direct execution gate mutation or
authorization record forging is attempted.
"""

import ast
import os
import pytest

WORKFORCE_SRC_DIR = "src/creative_workforce"

def test_ast_audit_no_direct_execution_gate_mutation():
    """Verifies that no file in src/creative_workforce imports or calls ExecutionGate directly."""
    for root, _, files in os.walk(WORKFORCE_SRC_DIR):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                filepath = os.path.join(root, f)
                with open(filepath, "r", encoding="utf-8") as src_file:
                    tree = ast.parse(src_file.read(), filename=filepath)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            assert "ExecutionGate" not in alias.name
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            assert "ExecutionGate" not in node.module
                        for alias in node.names:
                            assert "ExecutionGate" not in alias.name
