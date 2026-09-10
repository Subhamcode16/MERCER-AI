"""
Phase 25 Master Control Plane Orchestrator.
"""
from typing import Optional
from src.control_plane.service import ControlPlaneService
from src.control_plane.event_stream import ControlPlaneEventStreamBus
from src.control_plane.audit import ControlPlaneAuditLogger

class ControlPlaneOrchestrator:
    """Entry point for initializing and mounting Phase 25 control plane services."""

    def __init__(self):
        self.event_bus = ControlPlaneEventStreamBus()
        self.audit_logger = ControlPlaneAuditLogger()
        self.service = ControlPlaneService(
            event_bus=self.event_bus,
            audit_logger=self.audit_logger
        )
