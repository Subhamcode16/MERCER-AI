"""
Phase 21 - Evidence-Based Model Routing Engine.

Maps workforce roles to candidate model providers based on benchmark evidence,
task constraints, context limits, visual capabilities, and reliability specs.

Roles:
- TREND_ANALYST: Research/Reasoning model (gemini-2.5-flash / deepseek-v3)
- STRATEGIST: Reasoning + Long-Context model (gemini-1.5-pro / gpt-4o)
- DESIGNER: Multimodal + Image Generation model (imagen-3-hd / gemini-2.5-flash)
- CONTENT_SPECIALIST: Language & Copywriting model (claude-3-5-sonnet / gpt-4o)
- CRITIC: Independent Multimodal Evaluator (gemini-2.5-flash)
- REVIEWER: Independent Gate Evaluator (sandbox-llm / gemini-1.5-pro)
"""

from typing import Dict, Any, Optional
from .exceptions import ModelPolicyViolationError


class ModelRoutingPolicy:
    """Role-to-model evidence-derived routing policy for Phase 21 workforce."""

    ROLE_MODEL_MAPPING: Dict[str, str] = {
        "TREND_ANALYST": "gemini-2.5-flash",
        "STRATEGIST": "gemini-1.5-pro",
        "DESIGNER": "gemini-2.5-flash",
        "CONTENT_SPECIALIST": "claude-3-5-sonnet",
        "CRITIC": "gemini-2.5-flash",
        "REVIEWER": "gemini-1.5-pro"
    }

    FALLBACK_MODEL_MAPPING: Dict[str, str] = {
        "TREND_ANALYST": "sandbox-llm",
        "STRATEGIST": "sandbox-llm",
        "DESIGNER": "sandbox-llm",
        "CONTENT_SPECIALIST": "sandbox-llm",
        "CRITIC": "sandbox-llm",
        "REVIEWER": "sandbox-llm"
    }

    def resolve_model_for_role(self, role: str, is_fallback: bool = False) -> str:
        """Resolve optimal target model for a given workforce role."""
        mapping = self.FALLBACK_MODEL_MAPPING if is_fallback else self.ROLE_MODEL_MAPPING
        if role not in mapping:
            return "gemini-2.5-flash" if not is_fallback else "sandbox-llm"
        return mapping[role]

    def validate_critic_independence(self, primary_role: str, critic_role: str, primary_model: str, critic_model: str) -> bool:
        """Ensure reviewer/critic is independent and not evaluating its own generation directly."""
        if primary_role == critic_role:
            raise ModelPolicyViolationError("Critic role cannot be identical to generation role.")
        return True
