"""
Phase 9 — Artifact Lineage Tracker

Provides machine-verifiable artifact ancestry and provenance tracking, linking outputs to
Workflow ID, Task Graph Version, Staff Contributions, Knowledge Observations, and Active Strategy Version.
"""

import json
import os
from pathlib import Path
import tempfile
import threading
from typing import Dict, List, Optional

from src.agentic_work.memory_models import ArtifactLineageRecord


class LineageTamperError(RuntimeError):
    """Raised when an artifact lineage record fails SHA-256 cryptographic hash verification."""

    pass


class ArtifactLineageTracker:
    """File-backed persistent storage engine for machine-verifiable artifact lineage."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "data", "phase9_lineage")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def record_lineage(self, record: ArtifactLineageRecord) -> str:
        """Records artifact lineage atomically."""
        lineage_dict = record.to_dict()
        file_path = self.base_dir / f"lineage_{record.artifact_id}.json"

        with self._lock:
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.base_dir, prefix="lin_tmp_", suffix=".tmp"
            )
            try:
                with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                    json.dump(lineage_dict, f, indent=2)
                os.replace(temp_path, file_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

        return str(file_path)

    def get_lineage(self, artifact_id: str) -> ArtifactLineageRecord:
        """Retrieves and verifies artifact lineage integrity."""
        file_path = self.base_dir / f"lineage_{artifact_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Lineage record for artifact '{artifact_id}' not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        stored_lineage_hash = data.get("lineage_hash")
        record = ArtifactLineageRecord(
            artifact_id=data["artifact_id"],
            workflow_id=data["workflow_id"],
            task_id=data["task_id"],
            task_graph_version=data["task_graph_version"],
            staff_contributions=data["staff_contributions"],
            knowledge_observation_ids=data["knowledge_observation_ids"],
            critique_scores=data["critique_scores"],
            review_scores=data["review_scores"],
            revision_count=data["revision_count"],
            active_strategy_version=data["active_strategy_version"],
            payload_hash=data["payload_hash"],
            timestamp=data["timestamp"],
        )

        expected_hash = record.compute_hash()
        if stored_lineage_hash and stored_lineage_hash != expected_hash:
            raise LineageTamperError(
                f"Lineage hash mismatch for artifact '{artifact_id}'. Stored: {stored_lineage_hash}, Computed: {expected_hash}"
            )

        return record

    def clear(self) -> None:
        """Removes all stored lineage records."""
        with self._lock:
            for file_path in self.base_dir.glob("lineage_*.json"):
                try:
                    file_path.unlink()
                except OSError:
                    pass
