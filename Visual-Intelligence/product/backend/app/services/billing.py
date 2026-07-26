"""
Mercer AI — Billing Engine

Implements the two-phase credit deduction system (Reserve -> Commit/Refund)
to safely handle API cost deductions without double-charging or leaking free usage
on network failures.
"""
import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


class InsufficientCreditsError(HTTPException):
    def __init__(self, required: int, current: int = 0):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient credits. Required: {required}, Available: {current}"
        )


async def reserve_credits(db: AsyncIOMotorDatabase, user_id: str, amount: int, job_id: str) -> bool:
    """
    Phase 1: Reserve
    Atomically deducts credits from the user's cached balance using $gte filter.
    Returns True if reservation was successful, raises InsufficientCreditsError otherwise.
    """
    now = datetime.now(timezone.utc)
    
    # Atomic deduction — $gte ensures balance can never go below 0
    reserved = await db.users.find_one_and_update(
        {"_id": user_id, "credit_balance": {"$gte": amount}},
        {"$inc": {"credit_balance": -amount}, "$set": {"updated_at": now}},
    )
    
    if not reserved:
        # We don't know the exact balance here since find_one_and_update failed,
        # but we know it's less than `amount`.
        raise InsufficientCreditsError(required=amount)
        
    # Append to immutable ledger
    await db.credit_transactions.insert_one({
        "user_id": user_id,
        "type": "reserve",
        "amount": -amount,
        "job_id": job_id,
        "created_at": now,
    })
    
    logger.info("Reserved %d credits for user %s, job %s", amount, user_id, job_id)
    return True


async def commit_credits(db: AsyncIOMotorDatabase, user_id: str, job_id: str):
    """
    Phase 2a: Commit
    The generation succeeded. The credits were already deducted in Phase 1,
    so we just write the commit record to finalize the transaction in the ledger.
    """
    await db.credit_transactions.insert_one({
        "user_id": user_id,
        "type": "commit",
        "amount": 0,  # Balance impact already happened at reserve
        "job_id": job_id,
        "created_at": datetime.now(timezone.utc),
    })
    logger.info("Committed credit reservation for job %s", job_id)


async def refund_credits(db: AsyncIOMotorDatabase, user_id: str, amount: int, job_id: str, reason: str = "failed"):
    """
    Phase 2b: Refund
    The generation failed (provider timeout, safety block, etc).
    We add the credits back to the balance and write a refund ledger entry.
    """
    now = datetime.now(timezone.utc)
    
    await db.users.update_one(
        {"_id": user_id},
        {"$inc": {"credit_balance": amount}, "$set": {"updated_at": now}}
    )
    
    await db.credit_transactions.insert_one({
        "user_id": user_id,
        "type": "refund",
        "amount": amount,
        "job_id": job_id,
        "source": "system",
        "reason": reason,
        "created_at": now,
    })
    
    logger.warning("Refunded %d credits for user %s, job %s (Reason: %s)", amount, user_id, job_id, reason)
