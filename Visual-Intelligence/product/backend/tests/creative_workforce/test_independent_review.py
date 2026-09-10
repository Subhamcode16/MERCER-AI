"""
Phase 14 Test Independent Reviewer
-----------------------------------
Tests IndependentReviewer evaluation and double-blind isolation.
"""

import pytest
from src.creative_workforce import (
    IndependentReviewer,
    CreativeCollaborationProtocol,
    ContextBinding,
    SelfAuthorizationAttemptError,
)

def test_independent_review_success():
    reviewer = IndependentReviewer("reviewer-01")
    protocol = CreativeCollaborationProtocol()
    binding = ContextBinding("nocap", "brand", "cmp-1", "m-1", "t-1", "designer-01")

    art = protocol.create_artifact("Campaign Post", "POST", {"text": "NOCAP September Launch"}, binding)
    result = reviewer.review_artifact(art)

    assert result.review_id.startswith("rev-")
    assert result.recommendation == "ACCEPTED"
    assert result.is_authoritative is False

def test_self_review_rejection():
    reviewer = IndependentReviewer("designer-01")
    protocol = CreativeCollaborationProtocol()
    binding = ContextBinding("nocap", "brand", "cmp-1", "m-1", "t-1", "designer-01")

    art = protocol.create_artifact("Campaign Post", "POST", {"text": "NOCAP September Launch"}, binding)
    with pytest.raises(SelfAuthorizationAttemptError):
        reviewer.review_artifact(art)
