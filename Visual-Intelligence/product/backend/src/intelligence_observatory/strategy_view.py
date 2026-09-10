"""
Phase 25 Creative Strategy Lifecycle Registry View.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

@dataclass
class CreativeStrategyItem:
    strategy_id: str
    tenant_id: str
    client_id: str
    theme: str
    pillars: List[str]
    status: str # CANDIDATE, VALIDATED, ADOPTED, REJECTED, RETIRED
    associated_campaigns_count: int = 0
    performance_score: Optional[float] = None
    created_at: float = field(default_factory=time.time)
