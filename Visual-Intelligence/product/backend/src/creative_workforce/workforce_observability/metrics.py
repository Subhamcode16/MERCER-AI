"""
Phase 26 Workforce Observability & Performance Tracking.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


@dataclass
class WorkerTelemetryMetrics:
    worker_id: str
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    total_reviews_accepted: int = 0
    total_reviews_rejected: int = 0
    total_policy_blocks: int = 0
    avg_latency_ms: float = 0.0
    evidence_completeness_score: float = 1.0


class WorkforceObservability:
    """Aggregates performance metrics across workers and campaign rooms."""

    def __init__(self):
        self._metrics: Dict[str, WorkerTelemetryMetrics] = {}

    def get_or_create_metrics(self, worker_id: str) -> WorkerTelemetryMetrics:
        if worker_id not in self._metrics:
            self._metrics[worker_id] = WorkerTelemetryMetrics(worker_id=worker_id)
        return self._metrics[worker_id]

    def record_task_completed(self, worker_id: str, latency_ms: float) -> None:
        m = self.get_or_create_metrics(worker_id)
        prev_total = m.total_tasks_completed
        m.total_tasks_completed += 1
        m.avg_latency_ms = ((m.avg_latency_ms * prev_total) + latency_ms) / m.total_tasks_completed

    def record_policy_block(self, worker_id: str) -> None:
        m = self.get_or_create_metrics(worker_id)
        m.total_policy_blocks += 1

    def record_review_result(self, worker_id: str, accepted: bool) -> None:
        m = self.get_or_create_metrics(worker_id)
        if accepted:
            m.total_reviews_accepted += 1
        else:
            m.total_reviews_rejected += 1
