"""
Phase 20 - Visual Model Gateway Schemas & Data Models.

Defines typed Pydantic models for image generation requests, vision analysis,
artifact lineage traces, and visual quality metrics.
"""

import time
import uuid
import hashlib
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class CameraMotion(str, Enum):
    """Camera trajectory motion types supported by Higgsfield unified motion engine."""
    STATIC = "STATIC"
    PAN_LEFT = "PAN_LEFT"
    PAN_RIGHT = "PAN_RIGHT"
    TILT_UP = "TILT_UP"
    TILT_DOWN = "TILT_DOWN"
    ZOOM_IN = "ZOOM_IN"
    ZOOM_OUT = "ZOOM_OUT"
    DOLLY_IN = "DOLLY_IN"
    DOLLY_OUT = "DOLLY_OUT"
    ORBIT_360 = "ORBIT_360"
    TURNTABLE_CW = "TURNTABLE_CW"
    TURNTABLE_CCW = "TURNTABLE_CCW"
    CRANE_UP = "CRANE_UP"
    ROLL = "ROLL"


class VisualLineage(BaseModel):
    """Immutable lineage trace attached to every generated visual artifact."""
    lineage_id: str = Field(default_factory=lambda: f"vlin_{uuid.uuid4().hex[:12]}")
    artifact_id: str
    parent_artifact_id: Optional[str] = None
    model_name: str
    model_version: str
    request_hash: str
    creative_direction_hash: str
    visual_dna_ref: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)
    validation_status: str = "VALIDATED"  # "VALIDATED", "FAILED", "PENDING"


class ImageGenerationRequest(BaseModel):
    """Request structure for visual asset generation."""
    request_id: str = Field(default_factory=lambda: f"vreq_{uuid.uuid4().hex[:12]}")
    prompt: str
    aspect_ratio: str = "1:1"  # "1:1", "9:16", "16:9", "4:5"
    quality_mode: str = "STANDARD"  # "STANDARD", "HIGH", "ULTRA"
    creative_direction: Dict[str, Any] = Field(default_factory=dict)
    visual_dna: Dict[str, Any] = Field(default_factory=dict)
    parent_artifact_id: Optional[str] = None
    client_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    # Higgsfield extended motion / camera controls
    camera_motion: Optional[CameraMotion] = None
    motion_strength: float = 1.0
    seed: Optional[int] = None


class ImageGenerationResponse(BaseModel):
    """Response payload containing generated visual asset and metadata."""
    artifact_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:12]}")
    request_id: str
    image_url_or_bytes: str
    mime_type: str = "image/png"
    aspect_ratio: str
    width: int = 1024
    height: int = 1024
    lineage: VisualLineage
    latency_ms: float = 0.0
    status: str = "SUCCESS"


class VideoGenerationRequest(BaseModel):
    """Request structure for video synthesis and motion physics via Higgsfield."""
    request_id: str = Field(default_factory=lambda: f"vvid_req_{uuid.uuid4().hex[:12]}")
    prompt: str
    source_image_url: Optional[str] = None
    aspect_ratio: str = "16:9"  # "16:9", "9:16", "1:1", "4:5"
    camera_motion: CameraMotion = CameraMotion.STATIC
    duration_sec: float = 4.0
    fps: int = 24
    motion_strength: float = 1.0
    seed: Optional[int] = None
    creative_direction: Dict[str, Any] = Field(default_factory=dict)
    visual_dna: Dict[str, Any] = Field(default_factory=dict)
    parent_artifact_id: Optional[str] = None
    client_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)


class VideoGenerationResponse(BaseModel):
    """Response payload containing generated video asset and motion metadata."""
    artifact_id: str = Field(default_factory=lambda: f"art_vid_{uuid.uuid4().hex[:12]}")
    request_id: str
    video_url: str
    thumbnail_url: Optional[str] = None
    mime_type: str = "video/mp4"
    aspect_ratio: str
    duration_sec: float
    fps: int
    camera_motion: CameraMotion
    lineage: VisualLineage
    latency_ms: float = 0.0
    status: str = "SUCCESS"


class VisionAnalysisRequest(BaseModel):
    """Request for vision model analysis of an image reference."""
    analysis_id: str = Field(default_factory=lambda: f"vanal_{uuid.uuid4().hex[:12]}")
    image_url_or_bytes: str
    task: str  # e.g., "VISUAL_DESCRIPTION", "VISUAL_DNA_EXTRACTION", "CRITIQUE"
    client_id: Optional[str] = None


class VisionAnalysisResponse(BaseModel):
    """Structured observations extracted from visual analysis."""
    analysis_id: str
    task: str
    structured_observations: Dict[str, Any]
    visual_dna: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.90
    latency_ms: float = 0.0

