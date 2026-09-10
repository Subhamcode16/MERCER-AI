"""
Unit tests for Phase 17 Production Observability Stream.
"""

from src.production_fabric.observability import ProductionObservabilityStream

def test_observability_event_emission():
    stream = ProductionObservabilityStream()
    event = stream.emit_event(
        event_id="evt_01",
        event_type="WORK_ADMITTED",
        client_id="client_a",
        campaign_id="c1",
        item_id="w1",
        payload={"title": "Test Title", "secret_key": "sensitive_val"}
    )

    assert event.event_type == "WORK_ADMITTED"
    assert "secret_key" not in event.payload
