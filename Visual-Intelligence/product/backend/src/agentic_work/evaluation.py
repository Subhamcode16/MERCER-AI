"""
IF-AGENT-013 Workflow & Staff Evaluation Engine.
Computes quantitative quality metrics across completion rate, revision frequency,
critique scores, and latency.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class WorkflowEvaluationMetrics:
    """
    Quantitative metrics for a workflow execution run.
    """
    workflow_id: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    revision_count: int
    overall_quality_score: float
    total_execution_seconds: float
    passed_review: bool


class EvaluationEngine:
    """
    Quantitative Evaluation Engine.
    """

    def evaluate_workflow_run(
        self,
        workflow_id: str,
        task_results: List[Dict[str, Any]],
        revision_count: int,
        review_passed: bool,
        overall_score: float,
        duration_seconds: float,
    ) -> WorkflowEvaluationMetrics:
        total = len(task_results)
        completed = sum(1 for t in task_results if t.get("status") == "COMPLETED")
        failed = sum(1 for t in task_results if t.get("status") in ("FAILED", "BLOCKED"))

        return WorkflowEvaluationMetrics(
            workflow_id=workflow_id,
            total_tasks=total,
            completed_tasks=completed,
            failed_tasks=failed,
            revision_count=revision_count,
            overall_quality_score=overall_score,
            total_execution_seconds=duration_seconds,
            passed_review=review_passed,
        )
