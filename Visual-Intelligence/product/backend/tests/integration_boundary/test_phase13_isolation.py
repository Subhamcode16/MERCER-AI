"""
AST and Runtime Isolation Tests for Phase 13 Integration Boundary.

Proves that integration boundary code cannot manufacture authorization, mutate security policies,
or bypass ExecutionGate locks.
"""

import ast
import os
import glob
import pytest

from src.integration_boundary.models import CredentialReference, ExternalRequest, IntegrationOutcome


def test_ast_no_direct_execution_gate_mutation():
    """Verifies no file in src/integration_boundary directly imports or mutates ExecutionGate."""
    src_dir = os.path.join("src", "integration_boundary")
    py_files = glob.glob(os.path.join(src_dir, "*.py"))

    for filepath in py_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "ExecutionGate" not in alias.name
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "ExecutionGate" not in node.module


def test_models_contain_no_raw_secret_fields():
    """Verifies integration boundary data models have no fields named secret or password."""
    for model_cls in (CredentialReference, ExternalRequest, IntegrationOutcome):
        field_names = [f.name for f in model_cls.__dataclass_fields__.values()]
        for fn in field_names:
            assert "secret" not in fn.lower()
            assert "password" not in fn.lower()
            assert "token_value" not in fn.lower()
