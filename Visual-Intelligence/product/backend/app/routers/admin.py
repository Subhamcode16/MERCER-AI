import logging
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from app.auth.dependencies import AuthenticatedUser, require_admin_user
from app.database import get_db
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", summary="Get administrative dashboard stats")
async def get_admin_stats(
    user: AuthenticatedUser = Depends(require_admin_user),
):
    """
    Returns aggregated CRM dashboard stats for Mercer AI.
    Requires the caller to have the 'admin' role.
    """

    db = get_db()
    settings = get_settings()

    # 1. Total User Count
    total_users = await db.users.count_documents({})

    # 2. Tier Distribution
    tier_counts = {
        "free": 0,
        "starter": 0,
        "pro": 0,
        "studio": 0
    }
    async for doc in db.users.aggregate([{"$group": {"_id": "$tier", "count": {"$sum": 1}}}]):
        tier_counts[doc["_id"]] = doc["count"]

    # 3. Total Credits in Circulation
    total_credits = 0
    async for doc in db.users.aggregate([{"$group": {"_id": None, "total": {"$sum": "$credit_balance"}}}]):
        total_credits = doc.get("total", 0)

    # 4. Marketing Email Opt-in Rate
    opted_in_users = await db.users.count_documents({"receive_marketing": True})
    opt_in_rate = (opted_in_users / total_users * 100) if total_users > 0 else 0.0

    # 5. Recent Credit Transactions (ledger audit log)
    recent_transactions = []
    cursor = db.credit_transactions.find().sort("created_at", -1).limit(20)
    async for tx in cursor:
        # Resolve email if possible from users collection
        user_email = "Unknown"
        user_info = await db.users.find_one({"_id": tx["user_id"]})
        if user_info:
            user_email = user_info["email"]

        recent_transactions.append({
            "id": str(tx["_id"]),
            "user_email": user_email,
            "type": tx["type"],
            "amount": tx["amount"],
            "source": tx.get("source"),
            "created_at": tx["created_at"].isoformat() if tx.get("created_at") else None,
        })

    # 6. List of All Users
    all_users = []
    user_cursor = db.users.find().sort("created_at", -1)
    async for u in user_cursor:
        all_users.append({
            "id": u["_id"],
            "email": u["email"],
            "tier": u["tier"],
            "credit_balance": u["credit_balance"],
            "email_verified": u.get("email_verified", False),
            "role": u.get("role", "user"),
            "receive_marketing": u.get("receive_marketing", False),
            "created_at": u["created_at"].isoformat() if u.get("created_at") else None,
        })

    # 7. Resend Audience Metrics
    resend_stats = {
        "configured": False,
        "contacts_count": 0,
        "audience_name": "None",
        "error": None
    }
    if settings.resend_api_key and settings.resend_audience_id:
        resend_stats["configured"] = True
        url = f"https://api.resend.com/audiences/{settings.resend_audience_id}"
        headers = {"Authorization": f"Bearer {settings.resend_api_key}"}
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(url, headers=headers, timeout=5.0)
                if res.status_code == 200:
                    data = res.json()
                    resend_stats["contacts_count"] = data.get("contacts_count", 0)
                    resend_stats["audience_name"] = data.get("name", "Unknown")
                else:
                    resend_stats["error"] = f"Resend API returned {res.status_code}: {res.text[:100]}"
        except Exception as e:
            resend_stats["error"] = f"Failed to reach Resend: {str(e)}"

    return {
        "status": "ok",
        "total_users": total_users,
        "tier_counts": tier_counts,
        "total_credits": total_credits,
        "opt_in_rate": round(opt_in_rate, 2),
        "recent_transactions": recent_transactions,
        "users": all_users,
        "resend_stats": resend_stats
    }
