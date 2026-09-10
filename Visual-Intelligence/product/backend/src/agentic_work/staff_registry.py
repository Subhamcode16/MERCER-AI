"""
IF-AGENT-004 AI Staff Registry.
Thread-safe registry managing registration, lookup, capability validation,
and assignment of AI Staff workers.
"""

import threading
from typing import Dict, List, Optional
from .models import StaffRole, StaffProfile, StaffCapability
from .staff import (
    BaseStaff,
    ResearcherStaff,
    StrategistStaff,
    DesignerStaff,
    ContentSpecialistStaff,
    TrendAnalystStaff,
    CriticStaff,
    ReviewerStaff,
)


class StaffRegistry:
    """
    Registry for managing available AI staff workers.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._workers: Dict[str, BaseStaff] = {}
        self._register_default_prototype_staff()

    def _register_default_prototype_staff(self) -> None:
        """Registers default 7-role suite."""
        self.register_staff(ResearcherStaff())
        self.register_staff(StrategistStaff())
        self.register_staff(DesignerStaff())
        self.register_staff(ContentSpecialistStaff())
        self.register_staff(TrendAnalystStaff())
        self.register_staff(CriticStaff())
        self.register_staff(ReviewerStaff())

    def register_staff(self, staff: BaseStaff) -> None:
        if not isinstance(staff, BaseStaff):
            raise ValueError("staff must be an instance of BaseStaff")
        with self._lock:
            self._workers[staff.staff_id] = staff

    def get_staff_by_role(self, role: StaffRole) -> Optional[BaseStaff]:
        with self._lock:
            for worker in self._workers.values():
                if worker.role == role:
                    return worker
            return None

    def get_staff(self, staff_id: str) -> Optional[BaseStaff]:
        with self._lock:
            return self._workers.get(staff_id)

    def list_staff(self) -> List[BaseStaff]:
        with self._lock:
            return list(self._workers.values())
