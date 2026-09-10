"""
Phase 25 External Provider Request and Receipt Evidence Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ProviderReceiptEvidence:
    receipt_id: str
    provider_name: str
    operation: str
    status_code: int
    latency_ms: float
    request_hash: str
    response_hash: str
    cost_usd: float
    circuit_state_at_call: str
