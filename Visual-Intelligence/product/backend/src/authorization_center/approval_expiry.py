"""
Phase 25 Human Approval Expiration Engine.
"""
import time
from typing import List
from src.authorization_center.approval_projection import HumanApprovalItem

class ApprovalExpiryEvaluator:
    """Evaluates and transitions pending approvals that have exceeded their valid lifetime."""

    @staticmethod
    def evaluate_and_expire(approvals: List[HumanApprovalItem]) -> List[HumanApprovalItem]:
        now = time.time()
        expired = []
        for app in approvals:
            if app.status == "PENDING" and app.expires_at > 0 and now > app.expires_at:
                app.status = "EXPIRED"
                app.version += 1
                expired.append(app)
        return expired

    @staticmethod
    def is_expired(approval: HumanApprovalItem) -> bool:
        if approval.status == "EXPIRED":
            return True
        if approval.status == "PENDING" and approval.expires_at > 0 and time.time() > approval.expires_at:
            return True
        return False
