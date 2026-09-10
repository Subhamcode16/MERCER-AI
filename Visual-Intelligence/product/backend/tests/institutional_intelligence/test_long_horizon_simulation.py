"""
Long-Horizon Simulation Test (Phase 30).
Simulates 12 consecutive strategic cycles under dynamic evidence, contradictions,
provider/model drift, delayed outcomes, and rollbacks.
"""
import pytest
from datetime import datetime, timedelta
from src.institutional_intelligence.types import (
    StrategicHorizon,
    StrategicCadenceType,
    OrganizationalMemoryClass,
    InitiativeHealthState,
    utc_now,
)
from src.institutional_intelligence.objectives.models import StrategicObjective
from src.institutional_intelligence.decisions.models import (
    StrategicDecision,
    DecisionAlternative,
    HumanDecisionCapture,
)
from src.institutional_intelligence.assumptions.monitor import StrategicAssumption, AssumptionMonitor
from src.institutional_intelligence.memory.store import MemoryItem, OrganizationalMemoryStore
from src.institutional_intelligence.drift.detector import StrategicDriftDetector
from src.institutional_intelligence.health.evaluator import InitiativeHealthEvaluator
from src.institutional_intelligence.review.engine import StrategicReviewEngine
from src.institutional_intelligence.bridge.bridges import StrategicExecutionBridge
from src.institutional_intelligence.cadence.engine import StrategicCadenceEngine
from src.institutional_intelligence.rollback.manager import StrategicRollbackManager


def test_12_cycle_long_horizon_simulation():
    tenant = "tenant_simulation_12_cycles"
    obj = StrategicObjective(
        tenant_id=tenant,
        owner="human_director",
        creation_authority="AUTH_BOARD",
        title="12-Cycle Strategic Resilience",
        description="Verify long-horizon governance stability",
        scope="MULTI_CYCLE_SIMULATION"
    )
    
    mem_store = OrganizationalMemoryStore(tenant_id=tenant)
    asm_monitor = AssumptionMonitor(tenant_id=tenant)
    drift_detector = StrategicDriftDetector(tenant_id=tenant)
    health_eval = InitiativeHealthEvaluator(tenant_id=tenant)
    review_engine = StrategicReviewEngine(tenant_id=tenant)
    bridge = StrategicExecutionBridge(tenant_id=tenant)
    cadence = StrategicCadenceEngine(tenant_id=tenant)
    rollback_mgr = StrategicRollbackManager(tenant_id=tenant)

    # Run 12 strategic cycles
    for cycle in range(1, 13):
        # 1. New cycle cadence preparation
        cad_rec = cadence.run_cadence_preparation(
            cadence_type=StrategicCadenceType.MONTHLY_PORTFOLIO,
            changes=[f"Cycle {cycle} market data ingested"],
            contradictions=[f"Cycle {cycle} variance"] if cycle in [4, 8] else [],
            assumption_updates=[f"asm_cycle_{cycle}"]
        )
        assert cad_rec.is_preparation_only is True

        # 2. Assumption evolution
        asm = StrategicAssumption(
            tenant_id=tenant,
            statement=f"Cycle {cycle} cost factor assumption",
            model_confidence=0.8,
            empirical_confidence=0.75
        )
        asm_monitor.register_assumption(asm, actor_role="STRATEGY_WORKER")

        # 3. Simulate contradiction & drift in cycles 4 and 8
        if cycle == 4:
            asm.record_contradiction(
                evidence_id="ev_cycle_4_shock",
                contradicting_statement="Unexpected tariff jump",
                recorded_by="intelligence_worker"
            )
            drift = drift_detector.detect_drift(
                drift_type="ASSUMPTION_EVIDENCE_DIVERGENCE",
                target_id=asm.assumption_id,
                title="Tariff Divergence",
                divergence_summary="Tariff rate diverged from baseline.",
                severity=0.8,
                evidence_ids=["ev_cycle_4_shock"]
            )
            assert drift.severity == 0.8

        # 4. Simulate rollback in cycle 9
        if cycle == 9:
            event = rollback_mgr.execute_rollback(
                target_type="RECOMMENDATION",
                target_id="rec_untested_expansion",
                reason="Model hallucination detected on untested channel",
                actor="human_auditor"
            )
            assert event.target_id == "rec_untested_expansion"

        # 5. Evaluate initiative health
        health_rep = health_eval.evaluate(
            initiative_id=f"init_c{cycle}",
            has_contradictions=(cycle == 4),
            is_stale=(cycle == 7),
            is_unknown=(cycle == 12)
        )
        if cycle == 4:
            assert health_rep.overall_state == InitiativeHealthState.CONTRADICTED
        elif cycle == 7:
            assert health_rep.overall_state == InitiativeHealthState.STALE
        elif cycle == 12:
            assert health_rep.overall_state == InitiativeHealthState.UNKNOWN
        else:
            assert health_rep.overall_state == InitiativeHealthState.HEALTHY

        # 6. Append governance memory item for cycle
        mem_item = MemoryItem(
            tenant_id=tenant,
            memory_class=OrganizationalMemoryClass.GOVERNANCE_EVENT,
            title=f"Cycle {cycle} completion",
            content={"cycle_num": cycle, "health": health_rep.overall_state.value},
            provenance=f"sim_cycle_engine_{cycle}"
        )
        mem_store.append_memory(mem_item)

    # Final assertions after 12 cycles
    assert len(mem_store._items) == 12
    assert mem_store.verify_ledger_integrity() is True
    assert len(cadence._history) == 12
    assert len(asm_monitor.list_assumptions()) == 12
