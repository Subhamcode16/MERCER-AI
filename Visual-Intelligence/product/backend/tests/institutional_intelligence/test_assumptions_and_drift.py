"""
Tests for Strategic Assumptions and Strategic Drift Detection (Phase 30).
"""
import pytest
from datetime import datetime, timedelta
from src.institutional_intelligence.types import (
    EpistemicStatus,
    ThreatID,
    GovernanceInvariantViolation,
    utc_now,
)
from src.institutional_intelligence.assumptions.monitor import (
    StrategicAssumption,
    AssumptionMonitor,
)
from src.institutional_intelligence.drift.detector import (
    DriftSignal,
    StrategicDriftDetector,
)


def test_assumption_lifecycle_and_staleness():
    monitor = AssumptionMonitor(tenant_id="tenant_01")
    
    # Active assumption with future deadline
    asm_active = StrategicAssumption(
        tenant_id="tenant_01",
        statement="Sustainable silk demand will increase by 25% in Q4.",
        model_confidence=0.8,
        empirical_confidence=0.7,
        review_deadline=utc_now() + timedelta(days=20)
    )
    # Stale assumption with past deadline
    asm_stale = StrategicAssumption(
        tenant_id="tenant_01",
        statement="Traditional print lead times remain fixed at 14 days.",
        model_confidence=0.6,
        empirical_confidence=0.6,
        review_deadline=utc_now() - timedelta(days=5)
    )
    monitor.register_assumption(asm_active, actor_role="STRATEGY_WORKER")
    monitor.register_assumption(asm_stale, actor_role="STRATEGY_WORKER")

    scanned = monitor.scan_for_staleness_and_contradictions()
    assert len(scanned["active"]) == 1
    assert len(scanned["stale"]) == 1
    assert scanned["stale"][0].statement == "Traditional print lead times remain fixed at 14 days."


def test_t30_011_contradiction_recording_and_preservation():
    monitor = AssumptionMonitor(tenant_id="tenant_01")
    asm = StrategicAssumption(
        tenant_id="tenant_01",
        statement="Luxury consumer purchasing power is unaffected by inflation in Region X.",
        model_confidence=0.7,
        empirical_confidence=0.6
    )
    monitor.register_assumption(asm, actor_role="STRATEGY_WORKER")
    
    # Contradiction surfaced by new sales report
    asm.record_contradiction(
        evidence_id="ev_q3_luxury_sales_drop",
        contradicting_statement="Luxury sales in Region X dropped 18% over the past 60 days.",
        recorded_by="intelligence_worker_01"
    )
    assert asm.status == "CONTRADICTED"
    assert asm.epistemic_status == EpistemicStatus.CONTRADICTED
    assert len(asm.contradiction_history) == 1


def test_t30_008_unverified_external_assumption_poisoning_defense():
    monitor = AssumptionMonitor(tenant_id="tenant_01")
    asm_unverified = StrategicAssumption(
        tenant_id="tenant_01",
        statement="Rumor on social blog: Competitor Z closing entire haute couture division.",
        model_confidence=0.9,
        empirical_confidence=0.9
    )
    monitor.register_assumption(asm_unverified, actor_role="EXTERNAL_FEED", is_unverified_external=True)
    
    # Check that empirical confidence is suppressed and status is UNVERIFIED_CLAIM
    assert asm_unverified.epistemic_status == EpistemicStatus.UNVERIFIED_CLAIM
    assert asm_unverified.empirical_confidence <= 0.1


def test_strategic_drift_detection_and_no_suppression():
    detector = StrategicDriftDetector(tenant_id="tenant_01")
    drift = detector.detect_drift(
        drift_type="OBJECTIVE_INITIATIVE_DIVERGENCE",
        target_id="init_showroom_01",
        title="Showroom scope diverging from European brand focus",
        divergence_summary="Initiative is allocating 70% budget to non-core region.",
        severity=0.85,
        evidence_ids=["ev_budget_alloc_report"]
    )
    assert drift.severity == 0.85
    assert len(detector.list_active_drift_signals()) == 1

    # T30-010: Drift signals cannot be silently suppressed
    with pytest.raises(GovernanceInvariantViolation) as excinfo:
        detector.attempt_suppression(drift.drift_id, actor="ai_worker")
    assert excinfo.value.threat_id == ThreatID.T30_010
