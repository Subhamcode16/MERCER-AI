"""
Phase 25 Visual Rendering Provider Gateway Inspector.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class VisualProviderGatewayView:
    provider: str # Imagen 3, Fal.ai Flux Pro
    active_pipelines: List[str]
    rendering_queue_depth: int
    mean_render_time_seconds: float
    total_images_generated: int
    quarantine_rate_pct: float
