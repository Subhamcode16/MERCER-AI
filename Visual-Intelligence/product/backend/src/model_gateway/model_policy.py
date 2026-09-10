"""
Phase 20 - LLM Model Policy & Capability Boundary.

Validates that model requests adhere to task requirements, context limits,
and security policies. Enforces strict separation: Model Output != Truth != Permission.
"""

from typing import Dict, Any, Optional
from .models import LLMRequest, ModelCapability
from .exceptions import ModelPolicyViolationError


class ModelPolicyValidator:
    """Enforces capability and governance boundaries on model requests."""

    ALLOWED_TASK_TYPES = {
        "TREND_ANALYSIS", "STRATEGY_SYNTHESIS", "CREATIVE_DIRECTION",
        "COPY_GENERATION", "CRITIQUE", "REVIEW_EVALUATION"
    }

    def validate_request(self, request: LLMRequest, capability: ModelCapability) -> None:
        """Validate request against capability limits, tier locks, and prohibited task intents."""
        if request.task_type not in self.ALLOWED_TASK_TYPES:
            raise ModelPolicyViolationError(f"Task type '{request.task_type}' not allowed under model policy.")

        if len(request.prompt) > capability.context_limit * 4:
            raise ModelPolicyViolationError(f"Prompt length exceeds context limit for model {capability.model_name}.")

        # Enforce Pro Tier access validation
        if capability.tier == "PRO" and request.user_tier != "PRO" and not request.custom_api_key:
            raise ModelPolicyViolationError(
                f"Model '{capability.model_name}' is locked for Standard tier. Requires Pro tier subscription or custom API key."
            )

        # Enforce invariant: Models cannot be requested to execute actions or bypass policy
        prohibited_phrases = ["authorize execution", "bypass policy", "grant admin", "mutate security"]
        prompt_lower = request.prompt.lower()
        for phrase in prohibited_phrases:
            if phrase in prompt_lower:
                raise ModelPolicyViolationError(f"Model prompt contains prohibited self-authorization attempt: '{phrase}'")
