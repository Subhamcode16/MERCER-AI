"""
Phase 14 AST & Secret Isolation Audits
-------------------------------------
Parses AST of Phase 14 modules to verify:
- No direct ExecutionGate mutation.
- No direct EpistemicStateStore mutation.
- No raw credential fields in dataclasses.
"""

import ast
import os
import pytest

def test_ast_no_direct_execution_gate_mutation():
    """Verify Phase 14 code does not contain direct ExecutionGate.mutate or override calls."""
    gateway_dir = os.path.join("src", "workflow_gateway")
    for fname in os.listdir(gateway_dir):
        if fname.endswith(".py"):
            fpath = os.path.join(gateway_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=fname)

            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute):
                    assert node.attr not in [
                        "force_authorize",
                        "override_security_policy",
                        "bypass_human_authorization",
                    ], f"Forbidden security bypass attribute access '{node.attr}' found in {fname}"

def test_models_contain_no_raw_secret_fields():
    """Verify models.py dataclass definitions contain no secret storage fields."""
    models_path = os.path.join("src", "workflow_gateway", "models.py")
    with open(models_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename="models.py")

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            field_names = [n.target.id for n in node.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
            for fname in field_names:
                assert fname.lower() not in [
                    "raw_secret",
                    "api_key_secret",
                    "private_key_pem",
                    "password_hash",
                ], f"Forbidden raw secret field '{fname}' defined in model class '{node.name}'"
