"""
Mercer AI — Email Verification Gate

A FastAPI dependency stacked on top of get_current_user.
Applied to ALL generation routes in Phase 3.

Business rule (from product-about.md):
  - Free tier: credits do not activate until email is verified
  - Paid tiers (Starter, Pro, Studio): not gated — a completed payment
    implies a real, accountable user regardless of email status

Usage in a route:
    from app.auth import require_verified_email, AuthenticatedUser

    @router.post("/generate/{model}")
    async def generate(
        model: str,
        user: AuthenticatedUser = Depends(require_verified_email),
    ):
        # user is fully authenticated AND email-verified (if Free tier)
        ...
"""
from fastapi import Depends, HTTPException, status

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.models.user import Tier


async def require_verified_email(
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """
    Reject Free tier users whose email is not yet verified.
    Passes all paid-tier users through unconditionally.

    Raises:
        403 — Free tier user with unverified email
    """
    if user.tier == Tier.free and not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Please verify your email address to activate your free credits. "
                "Check your inbox for a verification link from Supabase."
            ),
        )
    return user
