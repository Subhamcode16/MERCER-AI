"""
Mercer AI — Auth Routes

POST /auth/provision
    Called by the frontend immediately after signup and again after email verification.
    Creates the MongoDB user document on first call (upsert) and conditionally grants
    the initial 20 free-tier credits once the user verifies their email.

    This endpoint uses get_jwt_claims_only (not get_current_user) because the
    MongoDB user document may not exist yet at the time this endpoint is called.

Design decisions:
    - Idempotent: safe to call multiple times — subsequent calls update
      email_verified and updated_at only, never overwrite tier or credit_balance.
    - Credit grant guard: checks credit_transactions for an existing system grant
      before issuing credits — prevents double-granting even on repeated calls.
    - Credits are only granted when email_verified=True. If a user provisions
      before verifying, they must call this endpoint again after verification.
"""
import logging
from datetime import datetime, timezone

from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Body, Request

from app.auth.dependencies import JWTClaims, get_jwt_claims_only
from app.database import get_db
from app.models.user import Tier, TIER_CREDIT_ALLOTMENT
from app.services.provider_resend import subscribe_to_resend_marketing
from app.utils.security import limiter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

_FREE_CREDITS = TIER_CREDIT_ALLOTMENT[Tier.free]  # 20 — single source of truth


class ProvisionRequest(BaseModel):
    receive_marketing: bool = False


@router.post("/provision", summary="Provision user account after signup / email verification")
@limiter.limit("10/minute")
async def provision_user(
    request: Request,
    body: Optional[ProvisionRequest] = Body(None),
    claims: JWTClaims = Depends(get_jwt_claims_only),
):
    """
    Upserts a MongoDB user document for the authenticated Supabase user.

    **New user flow:**
    1. Insert user doc (tier=free, credit_balance=0, receive_marketing)
    2. If email_verified=True: grant 20 credits atomically + write ledger entry
    3. If receive_marketing=True: subscribe to Resend marketing list
    4. Return is_new=True, credits_granted=True|False

    **Returning user flow (e.g. called again after email verification):**
    1. Update email_verified + updated_at only
    2. Check ledger — if no system grant exists and email is now verified: grant credits
    3. Return is_new=False, credits_granted=True|False

    Returns:
        {
            "status": "ok",
            "user_id": str,
            "is_new": bool,
            "credits_granted": bool
        }
    """
    db = get_db()
    now = datetime.now(timezone.utc)
    receive_marketing = body.receive_marketing if body else False

    # ── Check if user already exists ──────────────────────────────────────────
    existing = await db.users.find_one({"_id": claims.user_id})
    is_new = existing is None

    if is_new:
        # Auto-promote the first user in the system to 'admin' for easy setup
        user_count = await db.users.count_documents({})
        assigned_role = "admin" if user_count == 0 else "user"

        user_doc = {
            "_id": claims.user_id,
            "email": claims.email,
            "tier": Tier.free.value,
            "credit_balance": 0,
            "email_verified": claims.email_verified,
            "role": assigned_role,
            "receive_marketing": receive_marketing,
            "renewal_date": None,
            "created_at": now,
            "updated_at": now,
        }
        await db.users.insert_one(user_doc)
        logger.info("New user provisioned (role: %s): %s", assigned_role, claims.user_id)
    else:
        # Only update mutable fields — never touch tier or credit_balance here
        await db.users.update_one(
            {"_id": claims.user_id},
            {"$set": {
                "email_verified": claims.email_verified,
                "receive_marketing": receive_marketing or existing.get("receive_marketing", False),
                "updated_at": now,
            }},
        )
        logger.info("Existing user re-provisioned: %s", claims.user_id)

    # ── Resend Marketing Subscription ────────────────────────────────────────
    if receive_marketing:
        await subscribe_to_resend_marketing(claims.email)

    # ── Initial free credit grant ──────────────────────────────────────────────
    # Only grant if: (a) email is verified AND (b) no prior system grant exists.
    # The ledger check is the idempotency guard — not the is_new flag.
    credits_granted = False

    if claims.email_verified:
        prior_grant = await db.credit_transactions.find_one({
            "user_id": claims.user_id,
            "type": "grant",
            "source": "system",
        })

        if prior_grant is None:
            # Grant credits: update cached balance + append ledger entry
            await db.users.update_one(
                {"_id": claims.user_id},
                {"$set": {"credit_balance": _FREE_CREDITS, "updated_at": now}},
            )
            tx_doc = {
                "user_id": claims.user_id,
                "type": "grant",
                "amount": _FREE_CREDITS,
                "source": "system",
                "job_id": None,
                "created_at": now,
            }
            await db.credit_transactions.insert_one(tx_doc)
            credits_granted = True
            logger.info(
                "Granted %d free credits to user: %s",
                _FREE_CREDITS,
                claims.user_id,
            )

    return {
        "status": "ok",
        "user_id": claims.user_id,
        "is_new": is_new,
        "credits_granted": credits_granted,
    }
