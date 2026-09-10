"""
Phase 14 Test Client Isolation
------------------------------
Tests fail-closed prevention of cross-client data leakage (INV-14-W003).
"""

import pytest
from src.creative_workforce import (
    ClientContextManager,
    ContextBinding,
    CrossClientLeakageError,
)

def test_cross_client_access_rejection():
    mgr = ClientContextManager()
    mgr.register_client("client_a", "Client A", ["brand_a"])
    mgr.register_client("client_b", "Client B", ["brand_b"])

    binding_a = mgr.create_context_binding("client_a", "brand_a", "cmp-a", "m-a", "t-1", "staff-1")

    with pytest.raises(CrossClientLeakageError):
        mgr.validate_cross_client_access(binding_a, target_client_id="client_b")

def test_same_client_access_permitted():
    mgr = ClientContextManager()
    mgr.register_client("client_a", "Client A", ["brand_a"])
    binding_a = mgr.create_context_binding("client_a", "brand_a", "cmp-a", "m-a", "t-1", "staff-1")
    mgr.validate_cross_client_access(binding_a, target_client_id="client_a")
