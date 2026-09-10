"""
Phase 25 Pydantic API Schemas for Control Plane Endpoints.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class CampaignTransitionRequest(BaseModel):
    target_state: str
    expected_version: int
    reason: Optional[str] = ""

class ApprovalDecisionRequest(BaseModel):
    expected_version: int
    reason: Optional[str] = ""

class CircuitBreakerResetRequest(BaseModel):
    provider_name: str
    reason: str

class OperatorFeedbackRequest(BaseModel):
    deliverable_id: str
    feedback_text: str
    rating: Optional[float] = None
