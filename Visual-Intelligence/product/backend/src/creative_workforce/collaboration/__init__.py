from src.creative_workforce.collaboration.collaboration_hub import (
    CollaborationMessage,
    CollaborationHub,
)

# Export legacy Phase 14 classes for backward compatibility
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import hashlib
import json
import time
import uuid

from src.creative_workforce.organization_models import ContextBinding
from src.creative_workforce.exceptions import ContextScopeViolationError

@dataclass(frozen=True)
class CreativeArtifact:
    """Immutable creative workforce artifact with verifiable lineage commitment."""
    artifact_id: str
    title: str
    content_type: str
    payload: Dict[str, Any]
    context_binding: ContextBinding
    parent_artifact_id: Optional[str] = None
    input_references: List[str] = field(default_factory=list)
    version: int = 1
    created_at: float = field(default_factory=time.time)
    commitment_hash: str = field(default_factory=str)

    def calculate_commitment(self) -> str:
        """Calculates SHA-256 commitment of the artifact payload and lineage."""
        raw = f"{self.artifact_id}:{self.parent_artifact_id}:{self.context_binding.client_id}:{json.dumps(self.payload, sort_keys=True)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

class CreativeCollaborationProtocol:
    """Protocol orchestrating structured artifact flow and verifiable lineage."""

    def __init__(self):
        self._artifacts: Dict[str, CreativeArtifact] = {}

    def create_artifact(
        self,
        title: str,
        content_type: str,
        payload: Dict[str, Any],
        context_binding: ContextBinding,
        parent_artifact_id: Optional[str] = None,
        input_references: Optional[List[str]] = None,
    ) -> CreativeArtifact:
        art_id = f"art-{uuid.uuid4().hex[:8]}"
        raw_content = f"{art_id}:{parent_artifact_id}:{context_binding.client_id}:{json.dumps(payload, sort_keys=True)}"
        commit_hash = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()

        artifact = CreativeArtifact(
            artifact_id=art_id,
            title=title,
            content_type=content_type,
            payload=payload,
            context_binding=context_binding,
            parent_artifact_id=parent_artifact_id,
            input_references=input_references or [],
            commitment_hash=commit_hash,
        )
        self._artifacts[art_id] = artifact
        return artifact

    def get_artifact(self, artifact_id: str) -> Optional[CreativeArtifact]:
        return self._artifacts.get(artifact_id)

__all__ = [
    "CollaborationMessage",
    "CollaborationHub",
    "CreativeArtifact",
    "CreativeCollaborationProtocol",
]
