"""
Phase 9 — Workflow Memory Store

Provides controlled file-backed persistent storage for Workflow Memory Records with atomic write semantics,
SHA-256 integrity verification, and search/query capabilities.
"""

from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading
from typing import Any, Dict, List, Optional

from src.agentic_work.memory_models import WorkflowMemoryRecord


class SecretStorageForbiddenError(ValueError):
    """Raised when an attempt is made to store forbidden sensitive data or credentials."""

    pass


class MemoryIntegrityError(RuntimeError):
    """Raised when a stored workflow memory fails SHA-256 integrity verification."""

    pass


FORBIDDEN_KEYS = {
    "secret",
    "password",
    "private_key",
    "token",
    "api_key",
    "credential",
    "session_secret",
}


class WorkflowMemoryStore:
    """File-backed persistent storage engine for workflow memory records."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "data", "phase9_memory")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _sanitize_and_verify_no_secrets(self, data: Any, path: str = "") -> None:
        """Recursively checks that no forbidden secret keys exist in the record."""
        if isinstance(data, dict):
            for k, v in data.items():
                lower_k = str(k).lower()
                if any(forbidden in lower_k for forbidden in FORBIDDEN_KEYS):
                    raise SecretStorageForbiddenError(
                        f"Forbidden secret key '{k}' detected at path '{path}.{k}'"
                    )
                self._sanitize_and_verify_no_secrets(v, f"{path}.{k}")
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                self._sanitize_and_verify_no_secrets(item, f"{path}[{idx}]")

    def save_record(self, record: WorkflowMemoryRecord) -> str:
        """Saves a workflow memory record atomically using a tempfile and rename."""
        record_dict = record.to_dict()
        self._sanitize_and_verify_no_secrets(record_dict)

        file_path = self.base_dir / f"{record.memory_id}.json"

        with self._lock:
            # Write to a temporary file first
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.base_dir, prefix="mem_", suffix=".tmp"
            )
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(record_dict, f, indent=2)
                # Atomic replace
                os.replace(temp_path, file_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

        return str(file_path)

    def load_record(self, memory_id: str) -> WorkflowMemoryRecord:
        """Loads a workflow memory record and verifies its SHA-256 hash integrity."""
        file_path = self.base_dir / f"{memory_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Workflow memory record '{memory_id}' not found.")

        with self._lock:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        stored_hash = data.get("record_hash")
        record = WorkflowMemoryRecord(
            memory_id=data["memory_id"],
            workflow_id=data["workflow_id"],
            task_type=data["task_type"],
            staff_participation=data["staff_participation"],
            task_graph_version=data["task_graph_version"],
            input_metadata=data["input_metadata"],
            output_artifact_ids=data["output_artifact_ids"],
            critique_scores=data["critique_scores"],
            review_scores=data["review_scores"],
            feedback_ids=data["feedback_ids"],
            failure_signals=data["failure_signals"],
            revision_count=data["revision_count"],
            active_strategy_version=data["active_strategy_version"],
            benchmark_scores=data["benchmark_scores"],
            timestamp=data["timestamp"],
        )

        expected_hash = record.compute_hash()
        if stored_hash and stored_hash != expected_hash:
            raise MemoryIntegrityError(
                f"Integrity mismatch for memory '{memory_id}'. Stored: {stored_hash}, Computed: {expected_hash}"
            )

        return record

    def list_records(
        self,
        task_type: Optional[str] = None,
        strategy_version: Optional[str] = None,
    ) -> List[WorkflowMemoryRecord]:
        """Lists records with optional filtering."""
        records: List[WorkflowMemoryRecord] = []
        if not self.base_dir.exists():
            return records

        for file_path in self.base_dir.glob("*.json"):
            try:
                record = self.load_record(file_path.stem)
                if task_type and record.task_type != task_type:
                    continue
                if strategy_version and record.active_strategy_version != strategy_version:
                    continue
                records.append(record)
            except Exception:
                continue

        return records

    def clear(self) -> None:
        """Removes all stored memory records (primarily for testing)."""
        with self._lock:
            for file_path in self.base_dir.glob("*.json"):
                try:
                    file_path.unlink()
                except OSError:
                    pass
