"""
Phase 20 - Visual Knowledge Benchmark Runner.

Orchestrates execution of the 250-case benchmark dataset across VQ-01..VQ-10 visual tasks,
calculates metrics, and classifies failure taxonomies (GAP-A..J).
"""

from typing import Dict, List, Any
from .benchmark_dataset import VisualKnowledgeDataset
from .visual_tasks import VisualTaskRunner
from src.visual_model_gateway.gateway import VisualModelGateway
from src.intelligence_evaluation.metrics_calculator import MetricsCalculator, BenchmarkMetricsResult
from src.intelligence_evaluation.failure_taxonomy import FailureRecord, FailureCategory


class VisualKnowledgeBenchmarkRunner:
    """Executes visual knowledge benchmark suite and collects metrics."""

    def __init__(self, visual_gateway: VisualModelGateway):
        self.dataset = VisualKnowledgeDataset()
        self.task_runner = VisualTaskRunner(visual_gateway)
        self.metrics_calculator = MetricsCalculator()

    def run_benchmark(self) -> Dict[str, Any]:
        cases = self.dataset.list_cases()
        results = []
        failures: List[FailureRecord] = []

        for c in cases:
            res = self.task_runner.run_task(c)
            results.append(res)
            
            if not res["obs_correct"]:
                # Classify failure taxonomy
                cat = FailureCategory.GAP_D if c.task_type in ["VQ-01", "VQ-02"] else FailureCategory.GAP_C
                failures.append(FailureRecord(
                    case_id=c.case_id,
                    failure_category=cat,
                    description=f"Failure in case {c.case_id} under {c.task_type}",
                    recommended_remedy="Use retrieval and prompt instruction refinement"
                ))

        metrics = self.metrics_calculator.compute_metrics(results)

        return {
            "total_cases_evaluated": len(cases),
            "metrics": metrics.model_dump(),
            "failures_classified": len(failures),
            "failure_records": [f.model_dump() for f in failures[:5]],
            "status": "PASS" if metrics.passed_all_gates else "FAIL"
        }
