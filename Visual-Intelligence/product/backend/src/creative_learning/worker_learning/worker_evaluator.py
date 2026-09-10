"""
Phase 28 Worker Performance Learning & Specialization Evaluator.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class WorkerPerformanceInsight:
    insight_id: str
    worker_id: str
    role_name: str
    department: str
    specialization_affinity: str  # e.g. "Architectural Tailoring", "High-Speed Motion Capture"
    evaluated_campaigns_count: int
    review_pass_rate: float
    observed_conversion_lift: float
    authority_modification_permitted: bool = False  # Hard invariant: Learning ≠ Authority


class WorkerPerformanceEvaluator:
    """Evaluates creative worker performance trends without mutating execution privileges."""

    def __init__(self):
        self._insights: Dict[str, WorkerPerformanceInsight] = {}

    def record_worker_performance(
        self,
        worker_id: str,
        role_name: str,
        department: str,
        specialization_affinity: str,
        campaigns_count: int,
        review_pass_rate: float,
        observed_conversion_lift: float,
    ) -> WorkerPerformanceInsight:
        insight = WorkerPerformanceInsight(
            insight_id=f"wpi_{uuid.uuid4().hex[:8]}",
            worker_id=worker_id,
            role_name=role_name,
            department=department,
            specialization_affinity=specialization_affinity,
            evaluated_campaigns_count=campaigns_count,
            review_pass_rate=review_pass_rate,
            observed_conversion_lift=observed_conversion_lift,
            authority_modification_permitted=False,
        )
        self._insights[worker_id] = insight
        return insight

    def get_insight(self, worker_id: str) -> Optional[WorkerPerformanceInsight]:
        return self._insights.get(worker_id)
