"""
Phase 20 - Visual Model Gateway Facade.

Central entry point for workforce roles (e.g., DESIGNER, CRITIC) to perform image generation
and vision analysis with artifact lineage tracking and cryptographic audit logging.
"""

from typing import Dict, Any, Optional
from .models import (
    ImageGenerationRequest, ImageGenerationResponse,
    VisionAnalysisRequest, VisionAnalysisResponse
)
from .provider import IVisualProvider, SandboxVisualProvider
from .artifact_validation import VisualArtifactValidator
from .visual_ledger import VisualLedger


class VisualModelGateway:
    """Facade for image generation and vision model analysis."""

    def __init__(self, provider: Optional[IVisualProvider] = None):
        self.provider = provider or SandboxVisualProvider()
        self.validator = VisualArtifactValidator()
        self.ledger = VisualLedger()

    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate visual asset, validate dimensions/aspect ratio, and record lineage block."""
        response = self.provider.generate_image(request)
        self.validator.validate_artifact(response)
        
        self.ledger.record_action(
            artifact_id=response.artifact_id,
            action_type="IMAGE_GENERATED",
            model_name=response.lineage.model_name
        )

        return response

    def analyze_vision(self, request: VisionAnalysisRequest) -> VisionAnalysisResponse:
        """Perform vision analysis on an image reference."""
        response = self.provider.analyze_vision(request)

        self.ledger.record_action(
            artifact_id=request.analysis_id,
            action_type="VISION_ANALYZED",
            model_name="sandbox-vision"
        )

        return response
