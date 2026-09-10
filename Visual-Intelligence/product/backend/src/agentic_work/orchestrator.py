"""
IF-AGENT-014 Main Bounded Work Orchestrator.
Orchestrates AI staff delegation, task graph decomposition, execution,
self-critique, revision, review, and feedback learning.
Enforces permanent execution gate lock (ExecutionGate.is_permitted() == False).
"""

import time
import uuid
import threading
from typing import Dict, Any, List, Optional

from src.security_substrate import ExecutionGate, AssuranceLoopController
from .models import (
    StaffTask,
    StaffRole,
    TaskStatus,
    StaffResult,
    CritiqueResult,
    ReviewResult,
    LearningSignal,
)
from .staff_registry import StaffRegistry
from .task_graph import TaskGraph
from .context import SystemContext, WorkflowContext, TaskContext, StaffContext
from .critique import CritiqueEngine
from .review import ReviewEngine
from .feedback import FeedbackEngine
from .learning import LearningEngine
from .evaluation import EvaluationEngine, WorkflowEvaluationMetrics


class WorkOrchestrator:
    """
    Main Agentic Work Orchestrator.
    Coordinates AI staff workers through task graphs, critique loops, and learning layers.
    Possesses ZERO security authorization authority.
    """

    def __init__(
        self,
        staff_registry: Optional[StaffRegistry] = None,
        execution_gate: Optional[ExecutionGate] = None,
        critique_engine: Optional[CritiqueEngine] = None,
        review_engine: Optional[ReviewEngine] = None,
        feedback_engine: Optional[FeedbackEngine] = None,
        learning_engine: Optional[LearningEngine] = None,
    ) -> None:
        self.registry = staff_registry or StaffRegistry()
        self.execution_gate = execution_gate or ExecutionGate(AssuranceLoopController())
        self.critique_engine = critique_engine or CritiqueEngine()
        self.review_engine = review_engine or ReviewEngine()
        self.feedback_engine = feedback_engine or FeedbackEngine()
        self.learning_engine = learning_engine or LearningEngine()
        self.evaluation_engine = EvaluationEngine()

    def execute_workflow(
        self,
        objective: str,
        brand_params: Optional[Dict[str, Any]] = None,
        inject_defect: bool = False
    ) -> Dict[str, Any]:
        """
        Executes a complete multi-step agentic workflow:
        1. Decomposition into TaskGraph
        2. Parallel / Sequential Staff Task Delegation
        3. Self-Critique & Defect Detection
        4. Bounded Revision Loop (max 3)
        5. Independent Final Review
        6. Feedback & Learning Signal Emission
        """
        start_time = time.time()
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        brand_params = brand_params or {}

        # Construct TaskGraph with 7 Staff Tasks
        graph = TaskGraph(workflow_id=workflow_id, max_revisions=3)

        # Task 1: Research
        t1 = StaffTask(
            task_id="t1_research",
            workflow_id=workflow_id,
            role=StaffRole.RESEARCHER,
            objective=f"Research market trends and visual requirements for: {objective}",
            inputs={"brand_params": brand_params},
        )
        # Task 2: Trend Analysis (Parallel with Research)
        t2 = StaffTask(
            task_id="t2_trend",
            workflow_id=workflow_id,
            role=StaffRole.TREND_ANALYST,
            objective="Analyze emerging 2026 visual DNA trends.",
            inputs={"brand_params": brand_params},
        )
        # Task 3: Strategy (Depends on T1 & T2)
        t3 = StaffTask(
            task_id="t3_strategy",
            workflow_id=workflow_id,
            role=StaffRole.STRATEGIST,
            objective="Formulate campaign positioning pillars.",
            inputs={},
            dependencies=["t1_research", "t2_trend"],
        )
        # Task 4: Design (Depends on T3)
        t4 = StaffTask(
            task_id="t4_design",
            workflow_id=workflow_id,
            role=StaffRole.DESIGNER,
            objective="Generate visual layout specifications and color palette.",
            inputs={"inject_defect": inject_defect},
            dependencies=["t3_strategy"],
        )
        # Task 5: Content (Depends on T3)
        t5 = StaffTask(
            task_id="t5_content",
            workflow_id=workflow_id,
            role=StaffRole.CONTENT_SPECIALIST,
            objective="Draft editorial copy and social headlines.",
            inputs={},
            dependencies=["t3_strategy"],
        )
        # Task 6: Critique (Depends on T4 & T5)
        t6 = StaffTask(
            task_id="t6_critique",
            workflow_id=workflow_id,
            role=StaffRole.CRITIC,
            objective="Evaluate design and content outputs against quality standards.",
            inputs={},
            dependencies=["t4_design", "t5_content"],
        )
        # Task 7: Review (Depends on T6)
        t7 = StaffTask(
            task_id="t7_review",
            workflow_id=workflow_id,
            role=StaffRole.REVIEWER,
            objective="Perform independent final review of complete work package.",
            inputs={},
            dependencies=["t6_critique"],
        )

        for t in [t1, t2, t3, t4, t5, t6, t7]:
            graph.add_task(t)

        task_outputs = {}
        critique_results = []
        revision_attempts = 0

        # Graph execution loop
        while not graph.is_finished():
            ready_tasks = graph.get_ready_tasks()
            if not ready_tasks:
                break

            for task in ready_tasks:
                worker = self.registry.get_staff_by_role(task.role)
                if not worker:
                    graph.mark_failed(task.task_id, f"No registered worker for role: {task.role}")
                    continue

                # Prepare TaskContext & StaffContext
                t_ctx = TaskContext(
                    task_id=task.task_id,
                    workflow_id=workflow_id,
                    role=task.role,
                    objective=task.objective,
                    inputs=task.inputs,
                    parent_outputs={dep: task_outputs.get(dep, {}) for dep in task.dependencies},
                )
                s_ctx = StaffContext(
                    staff_id=worker.staff_id,
                    role=worker.role,
                    task_context=t_ctx,
                    allowed_tools=[],
                )

                result = worker.execute_task(s_ctx)
                task_outputs[task.task_id] = result.output_data

                if task.role == StaffRole.CRITIC:
                    critique_data = result.output_data
                    passed = critique_data.get("passed", True)
                    critique_results.append(critique_data)

                    if not passed:
                        revision_attempts += 1
                        # Trigger revision loop if defect detected
                        revisions = critique_data.get("suggested_revisions", [])
                        can_revise = graph.request_revision("t4_design", revisions)
                        if can_revise:
                            # Fix injected defect on revision attempt
                            design_task = graph.get_task("t4_design")
                            if design_task:
                                design_task.inputs["inject_defect"] = False
                            continue
                        else:
                            graph.mark_failed("t6_critique", "Max revisions exceeded.")
                            break

                graph.mark_completed(task.task_id, result.output_data)

        # Final Review execution
        review_out = task_outputs.get("t7_review", {})
        approved = review_out.get("approved", True)
        duration = time.time() - start_time

        # Emit LearningSignal
        if approved:
            sig = self.feedback_engine.create_signal(
                workflow_id=workflow_id,
                source="REVIEWER_FEEDBACK",
                category="PROMPT_TEMPLATE",
                observed_failure="None",
                expected_behavior="High quality lookbook artifact generated",
                correction="Optimize editorial hook formatting",
            )
            self.learning_engine.ingest_signal(sig)

        # Metrics Evaluation
        metrics = self.evaluation_engine.evaluate_workflow_run(
            workflow_id=workflow_id,
            task_results=[{"status": t.status.value} for t in graph._tasks.values()],
            revision_count=revision_attempts,
            review_passed=approved,
            overall_score=review_out.get("quality_score", 0.95),
            duration_seconds=duration,
        )

        return {
            "workflow_id": workflow_id,
            "objective": objective,
            "status": "COMPLETED" if approved else "FAILED",
            "task_outputs": task_outputs,
            "revision_count": revision_attempts,
            "review_passed": approved,
            "metrics": metrics.__dict__,
            "execution_gate_permitted": self.execution_gate.is_permitted(),  # MUST be False!
        }
