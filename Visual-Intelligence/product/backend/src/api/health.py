"""
Phase 25 API Health Probe.
"""
from fastapi import APIRouter
from src.control_plane.health import ControlPlaneHealthMonitor

health_router = APIRouter()

@health_router.get("/health")
def get_control_plane_health():
    return ControlPlaneHealthMonitor.evaluate_health()
