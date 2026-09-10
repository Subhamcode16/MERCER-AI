"""
Phase 28 Knowledge Freshness & Stale Learning Detection.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
import uuid


@dataclass
class FreshnessEvaluation:
    knowledge_id: str
    is_fresh: bool
    age_days: int
    expiry_limit_days: int
    recommendation: str  # "VALID", "REVALIDATION_REQUIRED", "EXPIRED"


class KnowledgeFreshnessEvaluator:
    """Evaluates the temporal validity of learned knowledge claims."""

    def evaluate_freshness(
        self,
        knowledge_id: str,
        last_validated_at: datetime,
        expiry_limit_days: int = 90,
    ) -> FreshnessEvaluation:
        now = datetime.now(timezone.utc)
        age_days = (now - last_validated_at).days

        if age_days <= expiry_limit_days:
            is_fresh = True
            rec = "VALID"
        elif age_days <= (expiry_limit_days + 30):
            is_fresh = False
            rec = "REVALIDATION_REQUIRED"
        else:
            is_fresh = False
            rec = "EXPIRED"

        return FreshnessEvaluation(
            knowledge_id=knowledge_id,
            is_fresh=is_fresh,
            age_days=age_days,
            expiry_limit_days=expiry_limit_days,
            recommendation=rec,
        )
