"""
Phase 25 Model Provider Gateway Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ModelProviderGatewayView:
    provider: str # Google, Anthropic, OpenAI
    available_models: List[str]
    active_routing_weights: Dict[str, float]
    current_tps: float
    total_token_spend_usd: float
    rate_limit_headroom_pct: float
