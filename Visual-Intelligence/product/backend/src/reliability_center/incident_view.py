"""
Phase 25 Operational Incident Timeline and Status View.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

@dataclass
class IncidentReportView:
    incident_id: str
    severity: str # SEV-1, SEV-2, SEV-3, SEV-4
    title: str
    impacted_services: List[str]
    root_cause: Optional[str]
    mitigation_status: str # INVESTIGATING, MITIGATED, RESOLVED
    opened_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
