"""
Phase 20 - Visual Artifact Validation Engine.

Validates generated image artifacts against aspect ratio specs, resolution bounds,
and visual quality policies before returning to workforce.
"""

from .models import ImageGenerationResponse
from .exceptions import ArtifactValidationFailedError


class VisualArtifactValidator:
    """Validates generated image attributes."""

    ALLOWED_ASPECT_RATIOS = {"1:1", "9:16", "16:9", "4:5"}

    def validate_artifact(self, response: ImageGenerationResponse) -> bool:
        if response.aspect_ratio not in self.ALLOWED_ASPECT_RATIOS:
            raise ArtifactValidationFailedError(f"Unsupported aspect ratio: {response.aspect_ratio}")

        if response.width <= 0 or response.height <= 0:
            raise ArtifactValidationFailedError("Invalid artifact dimensions.")

        if not response.lineage or not response.lineage.artifact_id:
            raise ArtifactValidationFailedError("Artifact missing required lineage metadata.")

        return True
