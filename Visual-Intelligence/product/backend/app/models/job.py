"""
Mercer AI — Generation Job Data Model

Represents one image generation request in the MongoDB generation_jobs collection.
Tracks the full lifecycle from submission through delivery.
"""
from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    submitted = "submitted"
    queued = "queued"               # Non-urgent: waiting for batch worker
    batched = "batched"             # Grouped into a batch, not yet submitted to provider
    sent_to_provider = "sent_to_provider"   # Batch submitted, provider is processing
    polling = "polling"             # Worker is polling provider for result
    completed = "completed"         # Provider returned success
    failed = "failed"               # Provider returned error or timeout
    credited = "credited"           # Credit committed (success path)
    refunded = "refunded"           # Credit released (failure path)
    delivered = "delivered"         # Result URL surfaced to client


class ModelName(str, Enum):
    nano_banana_2 = "nano_banana_2"         # gemini-3.1-flash-image
    nano_banana_pro = "nano_banana_pro"     # gemini-3-pro-image-preview
    gpt_image_2 = "gpt_image_2"            # gpt-image-2


# Credit cost table — single source of truth
# Key: (ModelName, resolution_or_quality)
CREDIT_COSTS: dict[tuple[str, str], int] = {
    ("nano_banana_2", "1024"): 2,
    ("nano_banana_2", "2048"): 2,
    ("gpt_image_2", "low"):    1,
    ("gpt_image_2", "medium"): 2,
    ("gpt_image_2", "high"):   3,
    ("nano_banana_pro", "1024"): 3,   # Starter preview
    ("nano_banana_pro", "2048"): 4,   # Pro / Studio full res
}


class GenerationJob(BaseModel):
    """
    MongoDB generation_jobs document shape.
    Job lifecycle: submitted → queued → batched → sent_to_provider →
                   polling → completed | failed → credited | refunded → delivered
    """
    user_id: str
    model: ModelName
    prompt: str                               # stored for batch submission; not logged
    resolution: Optional[Literal["1024", "2048"]] = None    # NB2 / NB Pro
    quality: Optional[Literal["low", "medium", "high"]] = None  # GPT Image 2 only
    urgent: bool = False                      # True = skip batch, real-time standard call
    status: JobStatus = JobStatus.submitted
    credit_cost: int                          # set at creation from CREDIT_COSTS
    idempotency_key: Optional[str] = None     # client-generated, prevents double-charge on retry
    provider_batch_id: Optional[str] = None   # set once submitted to provider batch API
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    result_url: Optional[str] = None          # Cloudflare R2 signed URL (set on delivery)
    error: Optional[str] = None              # Human-readable error (never raw provider message)

    class Config:
        populate_by_name = True


class GenerationJobPublic(BaseModel):
    """Safe job shape returned to the client."""
    id: str
    model: ModelName
    status: JobStatus
    credit_cost: int
    urgent: bool
    result_url: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
