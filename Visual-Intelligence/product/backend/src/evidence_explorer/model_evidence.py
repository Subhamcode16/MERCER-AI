"""
Phase 25 Model Invocation Redacted Evidence Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ModelInvocationEvidence:
    trace_id: str
    correlation_id: str
    provider: str
    model: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    input_hash: str
    output_hash: str
    structured_output_valid: bool
    policy_rejected: bool
