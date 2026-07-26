"""
Mercer AI — Generation Models

Data models for the generation API endpoints.
Defines required inputs, credit costs, and standard responses.
"""
from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class GenerationRequest(BaseModel):
    """
    Standard generation request payload from the frontend.
    """
    prompt: str = Field(..., description="The main creative prompt")
    idempotency_key: str = Field(
        ..., 
        description="A unique client-generated UUID for this request to prevent double charging on retries."
    )
    # Future extension: resolution, negative_prompt, aspect_ratio

class GenerationResponse(BaseModel):
    """
    Standard response payload for image generation job submission.
    """
    status: str = "ok"
    job_id: str

class JobResponse(BaseModel):
    """
    Standard response payload for polling a job.
    """
    job_id: str
    status: JobStatus
    image_base64: Optional[str] = None
    error: Optional[str] = None


# Immutable credit cost mapping based on pricing-tier.md
CREDIT_COSTS: Dict[str, int] = {
    "nano_banana_2": 2,
    "gpt_image_2": 2,
    "nano_banana_pro": 4,
}
