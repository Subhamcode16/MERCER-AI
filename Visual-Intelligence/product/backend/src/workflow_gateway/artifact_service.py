"""
Phase 14 Artifact Service
-------------------------
Surfaces generated artifacts and Phase 9 lineage information to the user control plane.
Preserves machine-verifiable ancestry and hash integrity commitments.
"""

from typing import List, Dict, Optional
import hashlib
import time

from src.workflow_gateway.models import ArtifactView
from src.workflow_gateway.exceptions import (
    ArtifactLineageError,
    CrossMissionLeakageError,
)

class ArtifactService:
    """Service managing artifact exposure, lineage, and cryptographic verification."""

    def __init__(self):
        self._artifacts: Dict[str, ArtifactView] = {}

    def register_artifact(
        self,
        artifact_id: str,
        workflow_id: str,
        mission_id: str,
        task_id: str,
        artifact_type: str,
        content_summary: str,
        lineage_hash: str,
    ) -> ArtifactView:
        """Registers a new artifact view with cryptographic integrity commitment."""
        now = time.time()
        commitment = hashlib.sha256(
            f"{artifact_id}:{mission_id}:{lineage_hash}".encode("utf-8")
        ).hexdigest()

        view = ArtifactView(
            artifact_id=artifact_id,
            workflow_id=workflow_id,
            mission_id=mission_id,
            task_id=task_id,
            artifact_type=artifact_type,
            content_summary=content_summary,
            lineage_hash=lineage_hash,
            created_at=now,
            integrity_commitment=commitment,
        )
        self._artifacts[artifact_id] = view
        return view

    def get_artifact(self, artifact_id: str, expected_mission_id: Optional[str] = None) -> Optional[ArtifactView]:
        """Retrieves an artifact by ID, optionally validating mission boundaries."""
        art = self._artifacts.get(artifact_id)
        if art and expected_mission_id and art.mission_id != expected_mission_id:
            raise CrossMissionLeakageError(
                f"Artifact {artifact_id} belongs to mission {art.mission_id}, not {expected_mission_id}"
            )
        return art

    def list_workflow_artifacts(self, workflow_id: str) -> List[ArtifactView]:
        """Lists all artifacts generated for a given workflow ID."""
        return [art for art in self._artifacts.values() if art.workflow_id == workflow_id]

    def verify_artifact_lineage(self, artifact_id: str) -> bool:
        """Verifies the machine-verifiable integrity commitment of an artifact."""
        art = self._artifacts.get(artifact_id)
        if not art:
            raise ArtifactLineageError(f"Artifact {artifact_id} not found.")
        if not art.verify_integrity():
            raise ArtifactLineageError(f"Cryptographic integrity verification failed for artifact {artifact_id}")
        return True
