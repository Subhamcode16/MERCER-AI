"""
Workflow Integration Models for Visual Intelligence Real Application Pipeline (Phase 8).

Defines data structures for real visual workflow context, asset references, stage tracking,
and non-authoritative workflow outcome summaries.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from src.security_substrate.exceptions import ReconciliationSchemaException

SENSITIVE_KEY_SUBSTRINGS = {
    "private_key",
    "secret",
    "hmac_key",
    "signing_key",
    "seed",
    "passphrase",
    "raw_bytes",
    "raw_asset_data",
}


def _validate_non_empty_str(val: Any, name: str) -> None:
    if isinstance(val, bool) or not isinstance(val, str):
        raise ReconciliationSchemaException(f"Field '{name}' must be a string, got {type(val).__name__}.")
    if not val.strip():
        raise ReconciliationSchemaException(f"Field '{name}' cannot be empty or whitespace-only.")


def _validate_non_negative_number(val: Any, name: str) -> None:
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ReconciliationSchemaException(f"Field '{name}' must be a numeric value, got {type(val).__name__}.")
    if val < 0:
        raise ReconciliationSchemaException(f"Field '{name}' cannot be negative, got {val}.")


def _check_sensitive_keys(data: Any, path: str = "") -> None:
    """Recursively inspect dictionaries for sensitive keys."""
    if isinstance(data, dict):
        for k, v in data.items():
            current_path = f"{path}.{k}" if path else str(k)
            k_lower = str(k).lower()
            for sensitive_term in SENSITIVE_KEY_SUBSTRINGS:
                if sensitive_term in k_lower:
                    raise ReconciliationSchemaException(
                        f"Prohibited sensitive key detected at '{current_path}': '{k}' contains '{sensitive_term}'."
                    )
            _check_sensitive_keys(v, current_path)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            _check_sensitive_keys(item, f"{path}[{idx}]")


class WorkflowStatus(str, Enum):
    """Status of an end-to-end Visual Intelligence workflow execution."""
    INITIALIZED = "INITIALIZED"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    ORCHESTRATED = "ORCHESTRATED"
    DECIDED = "DECIDED"
    AUDITED = "AUDITED"
    RECONCILED = "RECONCILED"
    FAILED = "FAILED"


class WorkflowStage(str, Enum):
    """Stages in the Visual Intelligence application workflow pipeline."""
    OBSERVE = "OBSERVE"
    VERIFY = "VERIFY"
    ORCHESTRATE = "ORCHESTRATE"
    DECIDE = "DECIDE"
    AUDIT = "AUDIT"
    RECONCILE = "RECONCILE"


@dataclass(frozen=True)
class AssetReference:
    """Non-sensitive metadata reference to a visual input asset."""
    asset_id: str
    asset_name: str
    content_type: str
    sha256_hash: str
    size_bytes: int

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.asset_id, "asset_id")
        _validate_non_empty_str(self.asset_name, "asset_name")
        _validate_non_empty_str(self.content_type, "content_type")
        _validate_non_empty_str(self.sha256_hash, "sha256_hash")
        _validate_non_negative_number(self.size_bytes, "size_bytes")
        if len(self.sha256_hash) != 64:
            raise ReconciliationSchemaException("sha256_hash must be a 64-character hex string.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "content_type": self.content_type,
            "sha256_hash": self.sha256_hash,
            "size_bytes": self.size_bytes,
        }


@dataclass(frozen=True)
class WorkflowRunContext:
    """Execution context for a single run of the Visual Intelligence workflow."""
    run_id: str
    system_id: str
    correlation_id: str
    user_id: str
    timestamp: float
    asset_ref: AssetReference
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.run_id, "run_id")
        _validate_non_empty_str(self.system_id, "system_id")
        _validate_non_empty_str(self.correlation_id, "correlation_id")
        _validate_non_empty_str(self.user_id, "user_id")
        _validate_non_negative_number(self.timestamp, "timestamp")
        if not isinstance(self.asset_ref, AssetReference):
            raise ReconciliationSchemaException("asset_ref must be an AssetReference instance.")
        if not isinstance(self.metadata, dict):
            raise ReconciliationSchemaException("metadata must be a dictionary.")
        _check_sensitive_keys(self.metadata, "metadata")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system_id": self.system_id,
            "correlation_id": self.correlation_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "asset_ref": self.asset_ref.to_dict(),
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class WorkflowRunResult:
    """Structured, non-authoritative summary of a completed visual workflow run."""
    run_id: str
    system_id: str
    correlation_id: str
    status: WorkflowStatus
    completed_stages: List[WorkflowStage]
    timestamp: float
    asset_hash: str
    evidence_ids: List[str] = field(default_factory=list)
    decision_id: Optional[str] = None
    attestation_id: Optional[str] = None
    audit_sequence_number: Optional[int] = None
    reconciliation_result_id: Optional[str] = None
    reconciliation_status: Optional[str] = None
    failure_reason: Optional[str] = None
    execution_gate_permitted: bool = field(default=False, init=False)
    trust_marker: str = field(default="WORKFLOW_EXECUTION_NON_AUTHORITATIVE", init=False)

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.run_id, "run_id")
        _validate_non_empty_str(self.system_id, "system_id")
        _validate_non_empty_str(self.correlation_id, "correlation_id")
        if not isinstance(self.status, WorkflowStatus):
            raise ReconciliationSchemaException(f"Invalid status: {self.status}")
        if not isinstance(self.completed_stages, list):
            raise ReconciliationSchemaException("completed_stages must be a list of WorkflowStage values.")
        for idx, stage in enumerate(self.completed_stages):
            if not isinstance(stage, WorkflowStage):
                raise ReconciliationSchemaException(f"completed_stages[{idx}] must be a WorkflowStage instance.")
        _validate_non_negative_number(self.timestamp, "timestamp")
        _validate_non_empty_str(self.asset_hash, "asset_hash")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system_id": self.system_id,
            "correlation_id": self.correlation_id,
            "status": self.status.value,
            "completed_stages": [s.value for s in self.completed_stages],
            "timestamp": self.timestamp,
            "asset_hash": self.asset_hash,
            "evidence_ids": list(sorted(self.evidence_ids)),
            "decision_id": self.decision_id,
            "attestation_id": self.attestation_id,
            "audit_sequence_number": self.audit_sequence_number,
            "reconciliation_result_id": self.reconciliation_result_id,
            "reconciliation_status": self.reconciliation_status,
            "failure_reason": self.failure_reason,
            "execution_gate_permitted": False,
            "trust_marker": "WORKFLOW_EXECUTION_NON_AUTHORITATIVE",
        }
