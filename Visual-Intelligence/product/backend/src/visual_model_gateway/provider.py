"""
Phase 20 - Visual Model Provider Adapters.

Abstract provider interface and implementation for Image Generation & Vision Analysis providers
(Sandbox Visual Provider and Gemini Vision Live Provider).
"""

import time
import json
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    ImageGenerationRequest, ImageGenerationResponse,
    VisionAnalysisRequest, VisionAnalysisResponse, VisualLineage
)


class IVisualProvider(ABC):
    """Abstract interface for image generation and vision analysis providers."""

    @abstractmethod
    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        pass

    @abstractmethod
    def analyze_vision(self, request: VisionAnalysisRequest) -> VisionAnalysisResponse:
        pass


class SandboxVisualProvider(IVisualProvider):
    """Deterministic sandbox provider for local testing and benchmark execution."""

    def __init__(self, model_name: str = "sandbox-imagen-3"):
        self.model_name = model_name

    def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        start_time = time.time()
        artifact_id = f"art_sb_{hashlib.md5(request.prompt.encode()).hexdigest()[:10]}"
        
        # Calculate aspect ratio dimensions
        w, h = 1024, 1024
        if request.aspect_ratio == "9:16":
            w, h = 1080, 1920
        elif request.aspect_ratio == "16:9":
            w, h = 1920, 1080

        req_hash = hashlib.sha256(request.prompt.encode()).hexdigest()
        cd_hash = hashlib.sha256(json.dumps(request.creative_direction).encode()).hexdigest()

        lineage = VisualLineage(
            artifact_id=artifact_id,
            parent_artifact_id=request.parent_artifact_id,
            model_name=self.model_name,
            model_version="1.0.0",
            request_hash=req_hash,
            creative_direction_hash=cd_hash,
            visual_dna_ref=request.visual_dna.get("dna_id", "v-dna-001"),
            validation_status="VALIDATED"
        )

        latency = (time.time() - start_time) * 1000.0

        return ImageGenerationResponse(
            artifact_id=artifact_id,
            request_id=request.request_id,
            image_url_or_bytes=f"https://sandbox.ilyren.internal/assets/{artifact_id}.png",
            mime_type="image/png",
            aspect_ratio=request.aspect_ratio,
            width=w,
            height=h,
            lineage=lineage,
            latency_ms=latency,
            status="SUCCESS"
        )

    def analyze_vision(self, request: VisionAnalysisRequest) -> VisionAnalysisResponse:
        start_time = time.time()

        if request.task == "VISUAL_DNA_EXTRACTION":
            obs = {
                "palette": ["#000000", "#FFFFFF", "#C0C0C0"],
                "typography": {"primary": "Neue Haas Grotesk", "weight": "Bold"},
                "composition": "Minimalist Center Focus 3x3 Grid",
                "lighting": "High-Contrast Studio Strobes"
            }
            v_dna = obs
        elif request.task == "CRITIQUE":
            obs = {
                "defects": ["Minor color bleed on bottom border"],
                "score": 0.91,
                "aspect_ratio_alignment": True
            }
            v_dna = None
        else:
            obs = {"description": "Fashion lookbook model featuring silk trench coat."}
            v_dna = None

        latency = (time.time() - start_time) * 1000.0

        return VisionAnalysisResponse(
            analysis_id=request.analysis_id,
            task=request.task,
            structured_observations=obs,
            visual_dna=v_dna,
            confidence_score=0.92,
            latency_ms=latency
        )
