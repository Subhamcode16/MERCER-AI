"""
Unit tests for Phase 16 Presentation Policy Engine.
"""

import pytest
from src.client_experience.presentation_policy import PresentationPolicyEngine

def test_presentation_policy_scrubbing():
    engine = PresentationPolicyEngine()
    dirty_dict = {
        "title": "Campaign Brief",
        "secret_token": "abc123secret",
        "private_key": "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC",
        "nested": {"chain_of_thought": "Internal reasoning step...", "public_field": "visible"}
    }

    clean = engine.sanitize_dict(dirty_dict)
    assert "secret_token" not in clean
    assert "private_key" not in clean
    assert "chain_of_thought" not in clean["nested"]
    assert clean["title"] == "Campaign Brief"
    assert clean["nested"]["public_field"] == "visible"
