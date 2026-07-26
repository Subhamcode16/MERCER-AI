"""
Mercer AI — Auth Package

Public interface for the entire auth layer.
All protected routes import exclusively from here — never from submodules directly.

Usage:
    from app.auth import AuthenticatedUser, get_current_user
    from app.auth import require_verified_email   # for generation routes
    from app.auth import get_jwt_claims_only      # for /auth/provision only
"""
from app.auth.dependencies import (
    AuthenticatedUser,
    JWTClaims,
    get_current_user,
    get_jwt_claims_only,
)
from app.auth.email_gate import require_verified_email

__all__ = [
    "AuthenticatedUser",
    "JWTClaims",
    "get_current_user",
    "get_jwt_claims_only",
    "require_verified_email",
]
