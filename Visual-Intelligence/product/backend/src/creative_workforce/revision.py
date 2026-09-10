"""
Phase 14 Bounded Revision Loop Controller
-----------------------------------------
Enforces bounded revision loops on workforce artifacts (INV-14-W004).
Default hard ceiling: MAX_REVISIONS = 3.
Prevents infinite autonomous revision loops and escalates when ceiling is breached.
"""

from typing import Dict, Any, Optional
from src.creative_workforce.collaboration import CreativeArtifact, CreativeCollaborationProtocol
from src.creative_workforce.critique import SelfCritiqueEngine, CritiqueResult
from src.creative_workforce.exceptions import RevisionLimitExceededError

MAX_REVISIONS = 3

class RevisionLoopController:
    """Controller enforcing deterministic revision ceilings and managing iterative artifact improvement."""

    def __init__(
        self,
        collaboration_protocol: Optional[CreativeCollaborationProtocol] = None,
        critique_engine: Optional[SelfCritiqueEngine] = None,
        max_revisions: int = MAX_REVISIONS,
    ):
        self.collaboration = collaboration_protocol or CreativeCollaborationProtocol()
        self.critique_engine = critique_engine or SelfCritiqueEngine()
        self.max_revisions = max_revisions
        self._revision_counts: Dict[str, int] = {}

    def _get_root_id(self, artifact: CreativeArtifact) -> str:
        """Traverses parent_artifact_id chain to locate the original root artifact ID."""
        curr = artifact
        while curr.parent_artifact_id and curr.parent_artifact_id in self.collaboration._artifacts:
            curr = self.collaboration._artifacts[curr.parent_artifact_id]
        return curr.artifact_id

    def revise_artifact(
        self,
        original_artifact: CreativeArtifact,
        revised_payload: Dict[str, Any],
        revision_note: str = "Applied revision suggestions",
    ) -> CreativeArtifact:
        """Produces a revised version of an artifact while enforcing MAX_REVISIONS ceiling."""
        root_id = self._get_root_id(original_artifact)
        current_count = self._revision_counts.get(root_id, 0)

        if current_count >= self.max_revisions:
            raise RevisionLimitExceededError(
                f"Artifact '{original_artifact.artifact_id}' reached maximum permitted revisions ({self.max_revisions}). "
                f"Escalation required."
            )

        new_count = current_count + 1
        self._revision_counts[root_id] = new_count

        revised_art = self.collaboration.create_artifact(
            title=f"{original_artifact.title} (v{new_count + 1})",
            content_type=original_artifact.content_type,
            payload=revised_payload,
            context_binding=original_artifact.context_binding,
            parent_artifact_id=original_artifact.artifact_id,
            input_references=[original_artifact.artifact_id],
        )
        self._revision_counts[revised_art.artifact_id] = new_count
        return revised_art

    def get_revision_count(self, artifact_id: str) -> int:
        """Retrieves current revision count for an artifact or artifact tree."""
        art = self.collaboration.get_artifact(artifact_id)
        if art:
            root_id = self._get_root_id(art)
            return self._revision_counts.get(root_id, 0)
        return self._revision_counts.get(artifact_id, 0)
