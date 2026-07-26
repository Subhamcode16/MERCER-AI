"""
Mercer AI — User & Tier Data Models
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Tier(str, Enum):
    free = "free"
    starter = "starter"
    pro = "pro"
    studio = "studio"


# Credit allotments per tier (used at grant time)
TIER_CREDIT_ALLOTMENT: dict[Tier, int] = {
    Tier.free: 20,
    Tier.starter: 200,
    Tier.pro: 800,
    Tier.studio: 2500,
}

# Free tier credits expire after 14 days (seconds)
FREE_TIER_CREDIT_EXPIRY_SECONDS: int = 14 * 24 * 60 * 60


class UserDoc(BaseModel):
    """
    MongoDB users collection document shape.
    `credit_balance` is a CACHE — the credit_transactions ledger is the source of truth.
    """
    id: str = Field(..., alias="_id")   # Supabase UUID
    email: EmailStr
    tier: Tier = Tier.free
    credit_balance: int = 0             # cached, recomputed from ledger on reconciliation
    email_verified: bool = False        # Free tier credits blocked until True
    role: str = "user"                  # admin | user
    renewal_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class UserPublic(BaseModel):
    """Safe user shape returned to the client — no internal fields."""
    id: str
    email: EmailStr
    tier: Tier
    credit_balance: int
    email_verified: bool
    role: str = "user"
    renewal_date: Optional[datetime] = None
