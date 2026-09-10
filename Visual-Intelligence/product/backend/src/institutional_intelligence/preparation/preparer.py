"""
Controlled Autonomous Preparation Module (Phase 30).
Allows autonomous agents to perform bounded read, summarize, derive, and draft operations
while strictly rejecting any attempt to mutate policy, allocate budget, or execute consequential actions.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from ..types import ThreatID, GovernanceInvariantViolation


class AutonomousPreparationEngine:
    PERMITTED_ACTIONS = {
        "RETRIEVE_EVIDENCE",
        "SUMMARIZE_CHANGES",
        "UPDATE_DERIVED_VIEW",
        "RANK_ATTENTION_ITEMS",
        "PREPARE_STRATEGIC_BRIEF",
        "PREPARE_AGENDA",
        "IDENTIFY_STALE_ASSUMPTIONS",
        "PREPARE_ALTERNATIVES",
        "SIMULATE_SCENARIOS",
        "DRAFT_INITIATIVE_UPDATE",
        "GENERATE_QUESTIONS"
    }

    FORBIDDEN_ACTIONS = {
        "CHANGE_OBJECTIVE": ThreatID.T30_001,
        "APPROVE_DECISION": ThreatID.T30_003,
        "CHANGE_SECURITY_POLICY": ThreatID.T30_002,
        "ALLOCATE_BUDGET": ThreatID.T30_005,
        "COMMIT_CONTRACT": ThreatID.T30_003,
        "PUBLISH_CONSEQUENTIAL_MATERIAL": ThreatID.T30_003,
        "LAUNCH_CAMPAIGN": ThreatID.T30_003,
        "DELETE_MEMORY": ThreatID.T30_007,
        "CHANGE_TENANT_BOUNDARY": ThreatID.T30_017,
        "MODIFY_AUTHORIZATION_RULES": ThreatID.T30_002
    }

    def validate_action(self, action_name: str, agent_id: str):
        action = action_name.upper()
        if action in self.FORBIDDEN_ACTIONS:
            threat = self.FORBIDDEN_ACTIONS[action]
            raise GovernanceInvariantViolation(
                threat,
                f"Controlled preparation violation: Agent '{agent_id}' attempted forbidden action '{action_name}'.",
                {"agent_id": agent_id, "attempted_action": action_name}
            )
        if action not in self.PERMITTED_ACTIONS:
            raise GovernanceInvariantViolation(
                ThreatID.T30_003,
                f"Unknown action '{action_name}' is not in permitted preparation capabilities.",
                {"agent_id": agent_id, "action": action_name}
            )
        return True
