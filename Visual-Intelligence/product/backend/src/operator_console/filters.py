"""
Phase 25 Operator Console Scope, Time, and Campaign Filters.
"""
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ConsoleFilter:
    tenant_id: str
    client_id: Optional[str] = None
    campaign_status: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    risk_level: Optional[str] = None
    limit: int = 50
    offset: int = 0
