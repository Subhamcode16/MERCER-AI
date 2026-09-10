"""
Unit tests for Phase 11 Escalation Manager.
"""

import pytest

from src.mission_control.escalation import EscalationManager, EscalationReason


def test_escalation_ticket_lifecycle():
    mgr = EscalationManager()

    ticket = mgr.escalate(
        mission_id="m1",
        reason=EscalationReason.HUMAN_REVIEW_REQUIRED,
        message="Review needed for visual assets",
        task_id="t_design",
    )

    assert ticket.ticket_id.startswith("esc_m1_")
    assert ticket.resolved is False

    pending = mgr.get_pending_tickets("m1")
    assert len(pending) == 1

    mgr.resolve_ticket(ticket.ticket_id, "Approved by brand manager.")
    assert ticket.resolved is True
    assert len(mgr.get_pending_tickets("m1")) == 0
