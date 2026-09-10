"""
Phase 8 Workflow Integration AST & Reflection Isolation Tests.
Verifies that the workflow integration bridge possesses ZERO execution gating or state mutation authority.
"""

import ast
import inspect
import time
from pathlib import Path
from src.security_substrate import AssuranceLoopController, ExecutionGate
from src.workflow_integration import (
    AssetReference,
    SecurityIntegrationAdapter,
    VisualWorkflowRunner,
    WorkflowRunContext,
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


def test_ast_audit_no_forbidden_workflow_imports():
    wf_dir = Path(__file__).parent.parent.parent / "src" / "workflow_integration"
    wf_files = [
        wf_dir / "workflow_models.py",
        wf_dir / "security_integration_adapter.py",
        wf_dir / "visual_workflow_runner.py",
    ]

    for filepath in wf_files:
        assert filepath.exists(), f"File {filepath} must exist."
        tree = ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "frost_prototype" not in alias.name, f"Illegal import {alias.name} in {filepath.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert "frost_prototype" not in node.module, f"Illegal import {node.module} in {filepath.name}"


def test_reflection_audit_no_workflow_authorization_methods():
    for cls in (VisualWorkflowRunner, SecurityIntegrationAdapter):
        methods = [m for m, _ in inspect.getmembers(cls, predicate=inspect.isfunction)]
        for forbidden in FORBIDDEN_AUTHORIZATION_METHODS:
            assert forbidden not in methods, f"{cls.__name__} illegally exposes authorization method '{forbidden}'."


def test_workflow_runner_never_unlocks_execution_gate():
    controller = AssuranceLoopController()
    gate = ExecutionGate(controller)
    assert gate.is_permitted() is False

    raw_asset = bytearray(b"isolation check bytes")
    asset_ref = AssetReference(
        asset_id="asset-iso-01",
        asset_name="iso.jpg",
        content_type="image/jpeg",
        sha256_hash="f" * 64,
        size_bytes=len(raw_asset),
    )

    context = WorkflowRunContext(
        run_id="run-iso-001",
        system_id="SYSTEM_001",
        correlation_id="corr-iso-001",
        user_id="user-designer-01",
        timestamp=time.time(),
        asset_ref=asset_ref,
    )

    runner = VisualWorkflowRunner(execution_gate=gate)
    res = runner.run_workflow(context=context, asset_bytes=raw_asset)

    assert res.execution_gate_permitted is False
    assert gate.is_permitted() is False
