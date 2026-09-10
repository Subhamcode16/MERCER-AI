"""
Phase 27 Departmental Conflict Resolution & Disagreement Handler.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class ConflictDomain(str, Enum):
    AESTHETIC_VS_PERFORMANCE = "AESTHETIC_VS_PERFORMANCE"
    RISK_VS_INNOVATION = "RISK_VS_INNOVATION"
    BUDGET_VS_SCOPE = "BUDGET_VS_SCOPE"
    TIMELINE_VS_FIDELITY = "TIMELINE_VS_FIDELITY"


@dataclass
class DepartmentPosition:
    department: str  # "Creative Direction", "Performance Marketing", "Brand Stewardship"
    spokesperson_role: str
    standpoint: str
    supporting_argument: str
    risk_assessment: str


@dataclass
class CreativeConflict:
    conflict_id: str
    campaign_id: str
    domain: ConflictDomain
    topic: str
    positions: List[DepartmentPosition]
    recommended_compromise: str
    resolved: bool = False
    resolution_notes: Optional[str] = None


class ConflictResolutionEngine:
    """Surfaces workforce divergence and facilitates human-in-the-loop arbitration."""

    def __init__(self):
        self._conflicts: Dict[str, List[CreativeConflict]] = {}  # campaign_id -> conflicts

    def register_divergence(
        self,
        campaign_id: str,
        domain: ConflictDomain,
        topic: str,
        positions: List[DepartmentPosition],
        recommended_compromise: str,
    ) -> CreativeConflict:
        conflict = CreativeConflict(
            conflict_id=f"cnf_{uuid.uuid4().hex[:8]}",
            campaign_id=campaign_id,
            domain=domain,
            topic=topic,
            positions=positions,
            recommended_compromise=recommended_compromise,
        )
        if campaign_id not in self._conflicts:
            self._conflicts[campaign_id] = []
        self._conflicts[campaign_id].append(conflict)
        return conflict

    def list_conflicts(self, campaign_id: str) -> List[CreativeConflict]:
        return self._conflicts.get(campaign_id, [])

    def resolve_conflict(self, campaign_id: str, conflict_id: str, resolution_decision: str) -> CreativeConflict:
        conflicts = self._conflicts.get(campaign_id, [])
        target = next((c for c in conflicts if c.conflict_id == conflict_id), None)
        if not target:
            raise KeyError(f"Conflict '{conflict_id}' not found for campaign '{campaign_id}'")

        target.resolved = True
        target.resolution_notes = resolution_decision
        return target
