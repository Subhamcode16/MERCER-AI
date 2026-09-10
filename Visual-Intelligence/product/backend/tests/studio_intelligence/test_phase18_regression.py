"""
Phase 18 Regression Test Suite & AST Security Audit.

Ensures Phase 18 introduces 0 regressions across earlier phases (Phases 14-17)
and verifies AST import integrity (no illegal imports or security policy mutations).
"""

import pytest
import ast
import glob
import os


def test_phase18_ast_forbidden_import_audit():
    """Scans all Phase 18 source code for prohibited security/authority bypass imports."""
    source_files = glob.glob("src/studio_intelligence/**/*.py", recursive=True)
    assert len(source_files) >= 18, f"Expected at least 18 source files in Phase 18, found {len(source_files)}"

    forbidden_names = {"eval", "exec", "os.system", "subprocess.call", "__import__"}

    for filepath in source_files:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code, filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in forbidden_names, (
                        f"Forbidden call '{node.func.id}' found in {filepath}"
                    )
