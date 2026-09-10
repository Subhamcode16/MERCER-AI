"""
Unit tests for Phase 17 Studio Production Runtime.
"""

from src.production_fabric.studio_runtime import StudioProductionRuntime

def test_studio_runtime_client_creation():
    studio = StudioProductionRuntime()
    rt_a = studio.get_or_create_client_runtime("client_a")
    rt_b = studio.get_or_create_client_runtime("client_b")

    assert rt_a.client_id == "client_a"
    assert rt_b.client_id == "client_b"
    assert len(studio.list_active_clients()) == 2
