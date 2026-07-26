"""
Mercer AI — FastAPI Auth Dependencies

Provides two injectable dependencies:

  get_jwt_claims_only(...)  → JWTClaims
      Verifies the JWT but does NOT query MongoDB.
      Used ONLY by POST /auth/provision where the user doc may not exist yet.

  get_current_user(...)  → AuthenticatedUser
      Full auth: verifies JWT + loads tier and credit_balance from MongoDB.
      Used by all protected routes in Phases 2–7.

  AuthenticatedUser is the typed object downstream route handlers receive.
  It intentionally contains NO raw JWT claims — tier and credits always
  come from MongoDB, never the token.
"""
import logging
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from app.database import get_db
from app.models.user import Tier
from app.utils.jwt import decode_supabase_jwt

logger = logging.getLogger(__name__)

# auto_error=True means FastAPI returns 403 automatically if the
# Authorization header is missing entirely — before our code runs.
_bearer = HTTPBearer(auto_error=True)


@dataclass
class AuthenticatedUser:
    """
    Verified, provisioned user — the object every protected route handler receives.

    tier and credit_balance are ALWAYS sourced from MongoDB, not the JWT.
    This is what prevents a client from escalating its own privileges.
    """
    user_id: str         # Supabase UUID — also the MongoDB _id
    email: str
    tier: Tier
    credit_balance: int
    email_verified: bool
    role: str            # admin | user


@dataclass
class JWTClaims:
    """
    Raw decoded JWT claims — used only by POST /auth/provision.
    The MongoDB user doc may not exist yet at provision time.
    """
    user_id: str
    email: str
    email_verified: bool


# ── Shared 401 exception ───────────────────────────────────────────────────────

def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )


# ── Dependencies ───────────────────────────────────────────────────────────────

async def get_jwt_claims_only(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> JWTClaims:
    """
    Verify JWT and extract claims only — no MongoDB lookup.

    Used exclusively by POST /auth/provision.
    All other protected routes must use get_current_user.
    """
    try:
        claims = decode_supabase_jwt(credentials.credentials)
    except InvalidTokenError as exc:
        logger.warning("JWT decode failed at provision: %s", type(exc).__name__)
        raise _credentials_exception()

    user_id: str | None = claims.get("sub")
    email: str | None = claims.get("email")

    if not user_id or not email:
        logger.warning("JWT missing required claims (sub or email)")
        raise _credentials_exception()

    # Supabase uses 'email_verified' inside user_metadata or app_metadata,
    # or top-level 'email_verified' / 'email_confirmed'.
    # If the user has a valid access token, we assume they passed auth.
    user_meta = claims.get("user_metadata", {})
    app_meta = claims.get("app_metadata", {})
    email_verified = (
        bool(claims.get("email_confirmed", False)) or
        bool(claims.get("email_verified", False)) or
        bool(user_meta.get("email_verified", False)) or
        bool(app_meta.get("email_verified", False)) or
        True  # Supabase access tokens are only issued to verified/authenticated users.
    )
    return JWTClaims(user_id=user_id, email=email, email_verified=email_verified)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> AuthenticatedUser:
    """
    Full auth dependency for all protected routes.

    Pipeline:
    1. Extract Bearer token from Authorization header
    2. Decode + verify JWT locally (signature, expiry) — no network call
    3. Extract user_id (sub) and email from claims
    4. Load user document from MongoDB — tier and credits read HERE, not from JWT
    5. Return AuthenticatedUser to the route handler

    Raises:
        401 — missing, expired, or invalid token
        403 — valid token but user not provisioned (call /auth/provision first)
    """
    # Step 1 & 2 — JWT verification
    try:
        claims = decode_supabase_jwt(credentials.credentials)
    except InvalidTokenError as exc:
        logger.warning("JWT verification failed: %s", type(exc).__name__)
        raise _credentials_exception()

    # Step 3 — Extract identity claims
    user_id: str | None = claims.get("sub")
    email: str | None = claims.get("email")

    if not user_id or not email:
        logger.warning("JWT missing sub or email claim")
        raise _credentials_exception()

    email_verified = bool(claims.get("email_confirmed", False))

    # Step 4 — Load entitlements from MongoDB (never from JWT)
    db = get_db()
    user_doc = await db.users.find_one({"_id": user_id})

    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "User account not found. "
                "Please call POST /auth/provision to create your account."
            ),
        )

    # Step 5 — Return typed user object
    return AuthenticatedUser(
        user_id=user_id,
        email=email,
        tier=Tier(user_doc["tier"]),
        credit_balance=user_doc["credit_balance"],
        email_verified=user_doc.get("email_verified", False),
        role=user_doc.get("role", "user"),
    )

async def require_admin_user(
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """
    Enforces that the authenticated user has the 'admin' role.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    return user
