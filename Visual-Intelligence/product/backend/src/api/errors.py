"""
Phase 25 Standardized API Error Formatter.
"""
from typing import Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.control_plane.exceptions import (
    ControlPlaneError,
    TenantContextMissingError,
    UnauthorizedOperatorActionError,
    StaleActionConflictError,
    DTOSerializationError,
    TenantAccessDeniedError
)

def format_error_response(status_code: int, error_type: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error_type": error_type,
            "message": message
        }
    )

async def control_plane_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, StaleActionConflictError):
        return format_error_response(409, "STALE_ACTION_CONFLICT", str(exc))
    elif isinstance(exc, (UnauthorizedOperatorActionError, TenantAccessDeniedError)):
        return format_error_response(403, "FORBIDDEN_OPERATOR_ACTION", str(exc))
    elif isinstance(exc, TenantContextMissingError):
        return format_error_response(400, "MISSING_TENANT_CONTEXT", str(exc))
    elif isinstance(exc, DTOSerializationError):
        return format_error_response(500, "DTO_PROJECTION_SECURITY_ERROR", "Prohibited sensitive field sanitized.")
    elif isinstance(exc, HTTPException):
        return format_error_response(exc.status_code, "HTTP_EXCEPTION", str(exc.detail))
    return format_error_response(500, "INTERNAL_CONTROL_PLANE_ERROR", str(exc))
