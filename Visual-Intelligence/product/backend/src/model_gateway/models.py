"""
Phase 20 - LLM Model Gateway Schemas & Data Models.

Defines typed Pydantic structures for model capabilities, requests, responses,
provenance metadata, token tracking, and structured output specs.
"""

import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional, Set
from pydantic import BaseModel, Field


class ModelCapability(BaseModel):
    """Declared capability specs of an LLM model."""
    provider: str  # e.g., "google", "openai", "anthropic", "fable", "sandbox"
    model_name: str  # e.g., "gemini-3.5-pro", "gpt-5-turbo", "claude-3-7-sonnet", "sandbox-llm"
    version: str = "1.0.0"
    context_limit: int = 128000
    supports_structured_output: bool = True
    supports_vision: bool = True
    supports_tools: bool = True
    reliability_class: str = "HIGH"  # "HIGH", "STANDARD", "EXPERIMENTAL"
    cost_per_1k_tokens: float = 0.001
    tier: str = "STANDARD"  # "STANDARD" or "PRO"


class LLMRequest(BaseModel):
    """Provider-neutral LLM generation request."""
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:12]}")
    task_type: str  # e.g., "TREND_ANALYSIS", "STRATEGY_SYNTHESIS", "CRITIQUE"
    prompt: str
    system_instruction: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    response_schema: Optional[Dict[str, Any]] = None
    client_id: Optional[str] = None
    context_scope: str = "STUDIO"
    custom_api_key: Optional[str] = None
    custom_base_url: Optional[str] = None
    user_tier: Optional[str] = "STANDARD"  # "STANDARD" or "PRO"
    created_at: float = Field(default_factory=time.time)


class ResponseProvenance(BaseModel):
    """Immutable provenance record attached to every model response."""
    provider: str
    model: str
    model_version: str
    request_id: str
    timestamp: float = Field(default_factory=time.time)
    policy_version: str = "20.0"
    context_scope: str = "STUDIO"
    structured_output_validated: bool = True
    source_references: List[str] = Field(default_factory=list)
    request_hash: str = ""

    def calculate_hash(self) -> str:
        content = f"{self.provider}:{self.model}:{self.request_id}:{self.timestamp}:{self.policy_version}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: Any) -> None:
        if not self.request_hash:
            self.request_hash = self.calculate_hash()


class LLMResponse(BaseModel):
    """Provider-neutral LLM generation response."""
    response_id: str = Field(default_factory=lambda: f"resp_{uuid.uuid4().hex[:12]}")
    request_id: str
    content: str
    structured_data: Optional[Dict[str, Any]] = None
    provenance: ResponseProvenance
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    status: str = "SUCCESS"  # "SUCCESS", "FALLBACK", "FAILED"
