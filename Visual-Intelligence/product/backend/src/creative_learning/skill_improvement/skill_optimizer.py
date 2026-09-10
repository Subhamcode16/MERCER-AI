"""
Phase 28 Governed Skill Improvement & Optimization Engine.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
from datetime import datetime, timezone


class SkillImprovementStatus(str, Enum):
    PROPOSED = "PROPOSED"
    EVALUATING = "EVALUATING"
    APPROVED_VERSION = "APPROVED_VERSION"
    REJECTED = "REJECTED"


@dataclass
class SkillImprovementProposal:
    proposal_id: str
    target_skill_name: str
    current_version: str
    proposed_version: str
    failure_pattern_addressed: str
    training_examples: List[Dict[str, str]]
    prompt_refinements: str
    status: SkillImprovementStatus = SkillImprovementStatus.PROPOSED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SkillImprovementEngine:
    """Proposes versioned skill refinements based on review critique and outcome evidence."""

    def __init__(self):
        self._proposals: Dict[str, SkillImprovementProposal] = {}

    def propose_skill_refinement(
        self,
        target_skill_name: str,
        current_version: str,
        failure_pattern: str,
        training_examples: List[Dict[str, str]],
        prompt_refinements: str,
    ) -> SkillImprovementProposal:
        # Enforce that skill improvement cannot modify security or permissions
        if "permissions" in prompt_refinements.lower() or "auth" in prompt_refinements.lower():
            raise PermissionError("Skill optimization cannot modify security permissions or authority parameters.")

        prop = SkillImprovementProposal(
            proposal_id=f"skp_{uuid.uuid4().hex[:8]}",
            target_skill_name=target_skill_name,
            current_version=current_version,
            proposed_version=f"{current_version}.1",
            failure_pattern_addressed=failure_pattern,
            training_examples=training_examples,
            prompt_refinements=prompt_refinements,
        )
        self._proposals[prop.proposal_id] = prop
        return prop

    def list_proposals(self) -> List[SkillImprovementProposal]:
        return list(self._proposals.values())
