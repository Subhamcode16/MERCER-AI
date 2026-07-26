"""
Mercer AI — Health Check Routes

Two endpoints:
  GET /health     — lightweight liveness probe (no DB)
  GET /health/db  — readiness probe (pings MongoDB)

No auth required — these are infrastructure endpoints.
"""
import logging
import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", summary="Liveness probe")
async def health_check():
    """Returns 200 immediately — confirms the process is alive."""
    return {
        "status": "ok",
        "service": "Mercer AI API",
        "timestamp": int(time.time()),
    }


@router.get("/health/db", summary="Readiness probe")
async def db_health():
    """Pings MongoDB — use for readiness checks before routing traffic."""
    try:
        db = get_db()
        await db.command("ping")
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        logger.error("DB health check failed: %s", type(exc).__name__)
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "unreachable"},
        )
