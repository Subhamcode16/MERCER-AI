"""
Phase 14 Test Context Scope
---------------------------
Tests hierarchical context scope bindings and client scope creation.
"""

import pytest
from src.creative_workforce import ClientContextManager, ContextScopeViolationError

def test_context_scope_creation():
    mgr = ClientContextManager()
    scope = mgr.register_client("nocap", "NOCAP Apparel", ["nocap-streetwear"])
    assert scope.client_id == "nocap"
    assert "nocap-streetwear" in scope.allowed_brands

def test_unauthorized_brand_rejection():
    mgr = ClientContextManager()
    mgr.register_client("nocap", "NOCAP Apparel", ["nocap-streetwear"])
    with pytest.raises(ContextScopeViolationError):
        mgr.create_context_binding(
            client_id="nocap",
            brand_id="other-brand",
            campaign_id="cmp-1",
            mission_id="m-1",
            task_id="t-1",
            staff_id="designer-01",
        )
