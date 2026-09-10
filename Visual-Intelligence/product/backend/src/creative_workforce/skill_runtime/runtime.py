"""
Phase 26 Governed Skill Runtime.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import time

from src.creative_workforce.worker_identity.models import WorkerIdentity
from src.creative_workforce.worker_lifecycle.lifecycle_engine import WorkerLifecycleManager
from src.creative_workforce.capability_binding.manifest import CapabilityResolver
from src.creative_workforce.skill_registry.models import SkillDefinition


class SkillRuntimeError(Exception):
    pass


@dataclass
class SkillExecutionResult:
    skill_id: str
    version: str
    worker_id: str
    tenant_id: str
    status: str  # SUCCESS, FAILED, BLOCKED
    outputs: Dict[str, Any] = field(default_factory=dict)
    evidence: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SkillRuntime:
    """Executes versioned skills within strict capability and lifecycle boundaries."""

    def __init__(self, capability_resolver: CapabilityResolver):
        self.capability_resolver = capability_resolver

    def execute_skill(
        self,
        worker: WorkerIdentity,
        skill: SkillDefinition,
        inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> SkillExecutionResult:
        start_time = time.perf_counter()

        # 1. Assert worker executable
        WorkerLifecycleManager.assert_executable(worker)

        # 2. Check skill required capabilities
        for cap in skill.required_capabilities:
            self.capability_resolver.assert_capability(worker.worker_id, cap)

        # 3. Simulate bounded skill execution
        outputs = {
            "result_summary": f"Executed {skill.skill_id}@{skill.version} for worker {worker.worker_id}",
            "processed_inputs": list(inputs.keys()),
            "status": "COMPLETED",
        }
        evidence = {
            "skill_purpose": skill.purpose,
            "risk_class": skill.risk_class.value,
            "required_capabilities": skill.required_capabilities,
        }

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        return SkillExecutionResult(
            skill_id=skill.skill_id,
            version=skill.version,
            worker_id=worker.worker_id,
            tenant_id=worker.tenant_id,
            status="SUCCESS",
            outputs=outputs,
            evidence=evidence,
            confidence=0.92,
            execution_time_ms=duration_ms,
        )
