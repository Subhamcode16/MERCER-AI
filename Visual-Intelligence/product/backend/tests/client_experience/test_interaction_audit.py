"""
Unit tests for Phase 16 Interaction Audit Logger.
"""

import pytest
from src.client_experience.interaction_audit import InteractionAuditLogger

def test_interaction_audit_hash_chain(tmp_path):
    audit_dir = str(tmp_path / "audit_ledger")
    logger = InteractionAuditLogger(ledger_dir=audit_dir)

    e1 = logger.record_interaction("client_nocap", "user_a", "LOGIN", {"ip": "127.0.0.1"})
    e2 = logger.record_interaction("client_nocap", "user_a", "APPROVE", {"approval_id": "appr_001", "password_key": "secret"})

    assert e2.previous_hash == e1.current_hash
    assert e2.payload["password_key"] == "[REDACTED]"
    assert logger.verify_integrity() is True
