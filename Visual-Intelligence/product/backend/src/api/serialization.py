"""
Phase 25 API Safe Serializer.
"""
from typing import Any, Dict
from src.control_plane.dto import sanitize_payload

class APISerializer:
    @staticmethod
    def serialize_response(data: Any) -> Any:
        return sanitize_payload(data)
