"""
Mercer AI — Users Router

Handles fetching user profile data and billing ledger history.
All routes require get_current_user (full DB validation).
"""
import logging
from typing import List, Dict, Any

from fastapi import APIRouter, Depends

from app.auth import AuthenticatedUser, get_current_user
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", summary="Get current user profile")
async def get_my_profile(
    user: AuthenticatedUser = Depends(get_current_user),
):
    """
    Returns the core profile of the authenticated user.
    Since get_current_user already fetches tier and credits from MongoDB,
    this is essentially a zero-cost endpoint.
    """
    # Simply serialize the dataclass returned by the auth dependency
    return {
        "status": "ok",
        "user_id": user.user_id,
        "email": user.email,
        "tier": user.tier.value,
        "credit_balance": user.credit_balance,
        "email_verified": user.email_verified,
        "role": user.role,
    }


@router.get("/me/transactions", summary="Get recent credit ledger transactions")
async def get_my_transactions(
    user: AuthenticatedUser = Depends(get_current_user),
    limit: int = 50,
):
    """
    Returns the recent transaction history for the user.
    This reads directly from the immutable credit_transactions ledger.
    """
    db = get_db()
    
    # Sort by created_at DESC (newest first)
    cursor = db.credit_transactions.find({"user_id": user.user_id}).sort("created_at", -1).limit(limit)
    
    transactions: List[Dict[str, Any]] = []
    async for tx in cursor:
        transactions.append({
            "id": str(tx["_id"]),
            "type": tx["type"],
            "amount": tx["amount"],
            "source": tx.get("source"),
            "created_at": tx["created_at"].isoformat() if tx.get("created_at") else None,
        })
        
    return {
        "status": "ok",
        "transactions": transactions
    }
