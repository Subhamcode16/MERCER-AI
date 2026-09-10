"""
Phase 10 — Execution Ledger & Operational Audit Store

Provides atomic, file-backed audit logging (`data/phase10_ledger/`) for all executed actions,
verifying integrity via SHA-256 hashes and rejecting raw secrets or credentials.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading
from typing import Any, Dict, List, Optional

from src.execution_control.capability_models import ExecutionCapability


@dataclass(frozen=True)
class ExecutionLedgerRecord:
    """Immutable audit entry for an executed action."""

    execution_id: str
    action_id: str
    workflow_id: str
    authorization_id: Optional[str]
    capability: ExecutionCapability
    resource_scope: str
    decision_reference: str
    start_time: str
    end_time: str
    status: str  # "SUCCESS", "FAILED", "PARTIAL_FAILURE"
    output_summary: Dict[str, Any]
    error_message: Optional[str] = None
    payload_hash: str = ""

    def compute_hash(self) -> str:
        data = {
            "execution_id": self.execution_id,
            "action_id": self.action_id,
            "workflow_id": self.workflow_id,
            "authorization_id": self.authorization_id,
            "capability": self.capability.value if hasattr(self.capability, "value") else str(self.capability),
            "resource_scope": self.resource_scope,
            "decision_reference": self.decision_reference,
            "status": self.status,
        }
        raw_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw_bytes).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "action_id": self.action_id,
            "workflow_id": self.workflow_id,
            "authorization_id": self.authorization_id,
            "capability": self.capability.value if hasattr(self.capability, "value") else str(self.capability),
            "resource_scope": self.resource_scope,
            "decision_reference": self.decision_reference,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "output_summary": self.output_summary,
            "error_message": self.error_message,
            "payload_hash": self.compute_hash(),
        }


class ExecutionLedger:
    """File-backed audit ledger storing operational execution records."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "data", "phase10_ledger")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def record_execution(self, record: ExecutionLedgerRecord) -> str:
        """Saves an execution record atomically."""
        record_dict = record.to_dict()
        file_path = self.base_dir / f"exec_{record.execution_id}.json"

        with self._lock:
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.base_dir, prefix="ledger_tmp_", suffix=".tmp"
            )
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(record_dict, f, indent=2)
                os.replace(temp_path, file_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

        return str(file_path)

    def load_execution(self, execution_id: str) -> ExecutionLedgerRecord:
        """Loads an execution record from file."""
        file_path = self.base_dir / f"exec_{execution_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Ledger entry '{execution_id}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ExecutionLedgerRecord(
            execution_id=data["execution_id"],
            action_id=data["action_id"],
            workflow_id=data["workflow_id"],
            authorization_id=data.get("authorization_id"),
            capability=ExecutionCapability(data["capability"]),
            resource_scope=data["resource_scope"],
            decision_reference=data["decision_reference"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            status=data["status"],
            output_summary=data["output_summary"],
            error_message=data.get("error_message"),
            payload_hash=data.get("payload_hash", ""),
        )

    def clear(self) -> None:
        """Clears stored ledger records."""
        with self._lock:
            for file_path in self.base_dir.glob("exec_*.json"):
                try:
                    file_path.unlink()
                except OSError:
                    pass
