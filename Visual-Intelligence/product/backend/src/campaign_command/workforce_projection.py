"""
Phase 25 Creative Workforce Role Allocation Projection.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class WorkforceRoleAllocation:
    role_id: str
    role_name: str
    department: str
    active_assignments_count: int
    completed_assignments_count: int
    current_status: str # IDLE, ACTIVE, BLOCKED
    last_action_timestamp: float = 0.0
