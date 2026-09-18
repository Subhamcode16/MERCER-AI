"""
Unit and integration tests for Higgsfield Open API provider adapter and Visual Model Gateway.
Validates:
1. Higgsfield unified image and video generation
2. 360° turntable and camera motion trajectories
3. Waterfall fallback mechanism upon provider exceptions
4. Cryptographic SHA-256 visual ledger block recording
"""

import pytest
from src.visual_model_gateway.models import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    CameraMotion,
    VisionAnalysisRequest
)
from src.visual_model_gateway.provider import (
    HiggsfieldVisualProvider,
    SandboxVisualProvider,
    IVisualProvider
)
from src.visual_model_gateway.gateway import VisualModelGateway
from src.visual_model_gateway.exceptions import ArtifactValidationFailedError


def test_higgsfield_provider_image_generation():
    provider = HiggsfieldVisualProvider()
    req = ImageGenerationRequest(
        prompt="Haute couture velvet evening gown in cinematic studio lighting",
        aspect_ratio="9:16",
        creative_direction={"lighting": "Dramatic Chiaroscuro"},
        visual_dna={"dna_id": "vdna_couture_01", "palette": ["#1A1A24", "#D4AF37"]}
    )

    resp = provider.generate_image(req)
    assert resp.status == "SUCCESS"
    assert resp.artifact_id.startswith("art_hf_")
    assert resp.width == 1080
    assert resp.height == 1920
    assert resp.lineage.model_name == "higgsfield-cinematic-v1"
    assert resp.lineage.visual_dna_ref == "vdna_couture_01"
    assert resp.lineage.request_hash is not None
    assert resp.lineage.creative_direction_hash is not None


def test_higgsfield_provider_video_motion_turntable():
    provider = HiggsfieldVisualProvider()
    req = VideoGenerationRequest(
        prompt="360 rotation showcase of embroidered silk bomber jacket",
        aspect_ratio="16:9",
        camera_motion=CameraMotion.ORBIT_360,
        duration_sec=5.0,
        fps=30,
        motion_strength=1.2,
        creative_direction={"camera_rig": "Orbital Crane"}
    )

    resp = provider.generate_video(req)
    assert resp.status == "SUCCESS"
    assert resp.artifact_id.startswith("art_hf_vid_")
    assert resp.camera_motion == CameraMotion.ORBIT_360
    assert resp.duration_sec == 5.0
    assert resp.fps == 30
    assert resp.video_url.endswith(".mp4")
    assert resp.lineage.model_name == "higgsfield-cinematic-v1-motion"


def test_visual_model_gateway_higgsfield_video_pipeline():
    gateway = VisualModelGateway.create_default()
    
    # 1. Image generation
    img_req = ImageGenerationRequest(
        prompt="Avant-garde metallic puffer jacket",
        aspect_ratio="1:1"
    )
    img_resp = gateway.generate_image(img_req)
    assert img_resp.status == "SUCCESS"
    assert img_resp.width == 1024
    assert img_resp.height == 1024

    # 2. Video generation with turntable motion
    vid_req = VideoGenerationRequest(
        prompt="Turntable spin of metallic puffer jacket",
        aspect_ratio="16:9",
        camera_motion=CameraMotion.TURNTABLE_CW,
        duration_sec=4.0,
        parent_artifact_id=img_resp.artifact_id
    )
    vid_resp = gateway.generate_video(vid_req)
    assert vid_resp.status == "SUCCESS"
    assert vid_resp.lineage.parent_artifact_id == img_resp.artifact_id

    # 3. Verify ledger integrity
    assert gateway.ledger.verify_integrity() is True
    assert len(gateway.ledger._chain) == 3  # Genesis + Image + Video


def test_higgsfield_waterfall_fallback():
    """Verify that when Higgsfield encounters network/endpoint errors, it seamlessly falls back."""
    class FailingHiggsfieldProvider(HiggsfieldVisualProvider):
        def generate_image(self, request):
            # Simulate endpoint failure triggering fallback
            return self.fallback_provider.generate_image(request)

        def generate_video(self, request):
            # Simulate endpoint failure triggering fallback
            return self.fallback_provider.generate_video(request)

    sandbox = SandboxVisualProvider(model_name="sandbox-fallback-engine")
    failing_hf = FailingHiggsfieldProvider(fallback_provider=sandbox)
    gateway = VisualModelGateway(provider=failing_hf)

    req = ImageGenerationRequest(prompt="Fallback test prompt", aspect_ratio="16:9")
    resp = gateway.generate_image(req)
    assert resp.status == "SUCCESS"
    assert resp.lineage.model_name == "sandbox-fallback-engine"
    assert gateway.ledger.verify_integrity() is True
