"""
Phase 20 - Visual Model Gateway Schemas & Data Models.

Defines typed Pydantic models for image generation requests, vision analysis,
artifact lineage traces, and visual quality metrics.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


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
