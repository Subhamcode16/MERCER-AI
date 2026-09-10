"""
Phase 25 SRE System Dependency Health View.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ServiceDependencyStatus:
    service_name: str
    service_type: str # DB, QUEUE, AI_PROVIDER, STORAGE
    is_healthy: bool
    latency_ms: float
    error_count_last_hour: int
