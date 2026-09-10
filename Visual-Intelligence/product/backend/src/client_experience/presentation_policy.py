"""
Phase 16 Presentation Policy Engine.
Enforces INV-16-007: Strips secrets, private keys, credentials, raw prompts, and internal reasoning from DTO projections.
"""

from typing import Dict, Any, List, Optional
from src.client_experience.workspace_models import (
    BrandDTO, DeliverableDTO, ApprovalSummaryDTO, CampaignDTO, WorkforceActivityDTO,
    TimelineEventDTO, PerformanceSummaryDTO, ClientWorkspaceDTO
)
from src.client_experience.exceptions import ReasoningLeakageError

FORBIDDEN_PROJECTION_KEYS = {
    "token", "secret", "password", "key", "private", "chain_of_thought",
    "internal_reasoning", "raw_prompt", "credentials", "auth_nonce_private"
}

class PresentationPolicyEngine:
    """Engine scrubbing sensitive fields and projecting safe client-facing DTOs."""

    def sanitize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Scrubs forbidden keys recursively."""
        clean = {}
        for k, v in data.items():
            if any(fk in k.lower() for fk in FORBIDDEN_PROJECTION_KEYS):
                continue
            if isinstance(v, dict):
                clean[k] = self.sanitize_dict(v)
            elif isinstance(v, list):
                clean[k] = [self.sanitize_dict(item) if isinstance(item, dict) else item for item in v]
            else:
                clean[k] = v
        return clean

    def project_brand(self, brand: Any) -> BrandDTO:
        """Projects StudioBrand into a safe BrandDTO."""
        dna = getattr(brand, "visual_dna_summary", {})
        clean_dna = self.sanitize_dict(dna)
        return BrandDTO(
            brand_id=getattr(brand, "brand_id", ""),
            client_id=getattr(brand, "client_id", ""),
            brand_name=getattr(brand, "brand_name", ""),
            visual_dna_summary=clean_dna,
            tone_of_voice=getattr(brand, "tone_of_voice", "")
        )

    def project_deliverable(self, deliverable: Any) -> DeliverableDTO:
        """Projects Deliverable into a safe DeliverableDTO."""
        content = getattr(deliverable, "content", {})
        clean_content = self.sanitize_dict(content)
        status_val = getattr(deliverable, "status", "")
        if hasattr(status_val, "value"):
            status_val = status_val.value

        return DeliverableDTO(
            deliverable_id=getattr(deliverable, "deliverable_id", ""),
            campaign_id=getattr(deliverable, "campaign_id", ""),
            client_id=getattr(deliverable, "client_id", ""),
            title=getattr(deliverable, "title", ""),
            deliverable_type=str(getattr(deliverable, "deliverable_type", "")),
            status=str(status_val),
            content_summary=clean_content,
            revision_count=getattr(deliverable, "revision_count", 0),
            version=getattr(deliverable, "version", "1.0.0")
        )

    def project_approval(self, approval: Any) -> ApprovalSummaryDTO:
        """Projects ApprovalItem into a safe ApprovalSummaryDTO."""
        appr_id = getattr(approval, "approval_id", "")
        nonce = f"nonce_{appr_id[:8]}"
        status_val = getattr(approval, "status", "")
        if hasattr(status_val, "value"):
            status_val = status_val.value

        return ApprovalSummaryDTO(
            approval_id=appr_id,
            client_id=getattr(approval, "client_id", ""),
            campaign_id=getattr(approval, "campaign_id", ""),
            deliverable_id=getattr(approval, "deliverable_id", ""),
            proposed_action=getattr(approval, "proposed_action", ""),
            target_platform=getattr(approval, "target_platform", ""),
            risk_classification=getattr(approval, "risk_classification", "MEDIUM"),
            status=str(status_val),
            expires_at=getattr(approval, "expires_at", ""),
            nonce=nonce
        )
