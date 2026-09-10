"""
Phase 20 - LLM Model Gateway Facade.

Primary entry point for workforce roles to request LLM generations.
Enforces: TASK TYPE -> REQUIRED CAPABILITY -> MODEL POLICY -> APPROVED ADAPTER.
"""

from typing import Dict, Any, Optional
from .models import LLMRequest, LLMResponse
from .provider_registry import ModelProviderRegistry
from .model_policy import ModelPolicyValidator
from .token_budget import TokenBudgetManager
from .structured_output import StructuredOutputValidator
from .redaction import CredentialRedactor
from .model_ledger import ModelLedger
from .exceptions import ModelPolicyViolationError


class ModelGateway:
    """Provider-neutral LLM Gateway facade for the ILYREN workforce."""

    def __init__(self):
        self.registry = ModelProviderRegistry()
        self.policy = ModelPolicyValidator()
        self.budget = TokenBudgetManager()
        self.validator = StructuredOutputValidator()
        self.redactor = CredentialRedactor()
        self.ledger = ModelLedger()

    def generate(
        self,
        request: LLMRequest,
        model_name: Optional[str] = None,
        custom_api_key: Optional[str] = None,
        custom_base_url: Optional[str] = None
    ) -> LLMResponse:
        """Route request through policy validation, provider execution, and audit logging."""
        target_model = model_name or "gemini-2.5-flash"
        provider = self.registry.get_provider(target_model)
        capability = provider.get_capability()

        key = custom_api_key or request.custom_api_key
        base_url = custom_base_url or request.custom_base_url

        # 1. Credential Audit & Redaction on prompt
        request.prompt = self.redactor.sanitize_text(request.prompt)
        self.redactor.audit_for_leakage(request.prompt)

        # 2. Policy & Token Budget Check
        self.policy.validate_request(request, capability)
        self.budget.check_and_reserve(request)

        # 3. Execution
        response = provider.generate(request, custom_api_key=key, custom_base_url=base_url)

        # 4. Structured Output Validation
        self.validator.validate_and_parse(response, request.response_schema)

        # 5. Record Token Usage & Audit Ledger Block
        self.budget.record_usage(request.task_type, response.total_tokens)
        self.ledger.record_interaction(
            request_id=request.request_id,
            provider=response.provenance.provider,
            model=response.provenance.model,
            tokens_used=response.total_tokens
        )

        return response
