"""
Phase 25 Reliability Center Tests.
"""
from src.reliability_center.slo_view import SLOComplianceView
from src.reliability_center.error_budget_view import ErrorBudgetBurnView
from src.reliability_center.latency_view import LatencyPercentileDistributionView
from src.reliability_center.recovery_view import DisasterRecoveryDrillSummary
from src.reliability_center.rollback_view import CanaryRollbackStatusView

def test_slo_compliance_view():
    slo = SLOComplianceView(
        slo_name="99.9% Production Availability",
        target_value=99.9,
        observed_value=100.0,
        unit="%",
        is_compliant=True
    )
    assert slo.is_compliant is True

def test_error_budget_burn_view():
    eb = ErrorBudgetBurnView(
        total_budget_percentage=0.10,
        consumed_percentage=0.02,
        burn_rate_ratio=0.20,
        alert_status="HEALTHY"
    )
    assert eb.alert_status == "HEALTHY"
    assert eb.circuit_breaker_tripped is False

def test_canary_rollback_view():
    canary = CanaryRollbackStatusView(
        active_release_version="v24.1.0",
        canary_traffic_split_pct=10.0,
        canary_error_rate_pct=0.0,
        baseline_error_rate_pct=0.0,
        sla_breach_detected=False,
        automated_rollback_triggered=False
    )
    assert canary.automated_rollback_triggered is False
