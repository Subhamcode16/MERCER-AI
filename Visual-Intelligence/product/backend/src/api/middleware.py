"""
Phase 25 Request Tracing and Security Middleware.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import uuid
import time
import logging

logger = logging.getLogger(__name__)

class ControlPlaneTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", f"corr-{uuid.uuid4().hex[:10]}")
        start_time = time.time()

        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000.0
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Response-Time-Ms"] = f"{duration_ms:.2f}"

        return response
