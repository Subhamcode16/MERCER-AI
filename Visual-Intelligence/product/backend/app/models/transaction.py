"""
Mercer AI — Credit Transaction (Ledger) Data Model

The credit_transactions collection is the SOURCE OF TRUTH for all credit activity.
Entries are IMMUTABLE — never update or delete a row, only insert new offsetting entries.
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


TransactionType = Literal[
    "reserve",   # Credit hold before API call (atomic $gte + $inc)
    "commit",    # Confirms the reserve — generation succeeded
    "release",   # Reverses the reserve — generation failed (no charge)
    "grant",     # Credits added: subscription renewal or top-up
    "refund",    # Credits returned: batch failure / provider error / timeout
    "expire",    # Free-tier credits removed after 14-day expiry window
]

GrantSource = Literal[
    "razorpay",  # Domestic subscription renewal (India)
    "stripe",    # International subscription renewal
    "purchase",  # Manual top-up / pay-as-you-go
    "system",    # Admin grant, promo, or initial free-tier allocation
]


class CreditTransaction(BaseModel):
    """
    MongoDB credit_transactions document shape.
    Append-only — insert only, never mutate.
    """
    user_id: str
    type: TransactionType
    amount: int                              # negative = spend/hold, positive = credit back
    job_id: Optional[str] = None            # links to generation_jobs._id (as string)
    source: Optional[GrantSource] = None    # populated on type="grant" only
    provider_event_id: Optional[str] = None # Razorpay/Stripe event ID — idempotency key
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
