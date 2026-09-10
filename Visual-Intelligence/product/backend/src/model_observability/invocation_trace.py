"""
Phase 22 Model Observability: Invocation Trace Recorder
-------------------------------------------------------
Records comprehensive invocation telemetry for every LLM and vision model call.
Strict Security Rule: NEVER logs confidential prompts, credentials, auth tokens, or raw chain-of-thought.
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass(frozen=True)
class InvocationTrace:
    trace_id: str
    correlation_id: str
    client_id: str
    provider: str
    model: str
    model_version: Optional[str]
    role: str
    timestamp: float
    latency_ms: float
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    known_cost_usd: Optional[float]
    timeout_occurred: bool
    retry_count: int
    fallback_used: bool
    structured_output_valid: bool
    policy_rejected: bool
    status: str  # SUCCESS, FAILED, TIMEOUT, POLICY_REJECTED
    error_class: Optional[str] = None
    sanitized_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes trace without exposing sensitive prompt contents or secrets."""
        return {
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id,
            "client_id": self.client_id,
            "provider": self.provider,
            "model": self.model,
            "model_version": self.model_version,
            "role": self.role,
            "timestamp": self.timestamp,
            "latency_ms": round(self.latency_ms, 2),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "known_cost_usd": self.known_cost_usd,
            "timeout_occurred": self.timeout_occurred,
            "retry_count": self.retry_count,
            "fallback_used": self.fallback_used,
            "structured_output_valid": self.structured_output_valid,
            "policy_rejected": self.policy_rejected,
            "status": self.status,
            "error_class": self.error_class,
            "metadata": self.sanitized_metadata,
        }

class InvocationTraceRecorder:
    """In-memory telemetry sink and telemetry aggregator."""

    def __init__(self):
        self._traces: List[InvocationTrace] = []

    def record_trace(self, trace: InvocationTrace) -> None:
        self._traces.append(trace)

    def list_traces(self) -> List[InvocationTrace]:
        return list(self._traces)

    def get_traces_by_correlation_id(self, correlation_id: str) -> List[InvocationTrace]:
        return [t for t in self._traces if t.correlation_id == correlation_id]

    def get_traces_by_client(self, client_id: str) -> List[InvocationTrace]:
        return [t for t in self._traces if t.client_id == client_id]

    def clear(self) -> None:
        self._traces.clear()
