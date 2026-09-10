"""
Phase 20 - LLM Model Provider Adapters.

Supports:
1. GeminiLiveProvider (Google Gemini API)
2. UniversalLLMProvider (OpenAI, Anthropic/OpenRouter, DeepSeek, Qwen, Llama 3, Ollama, Custom OpenAI-Compatible Endpoints)
3. SandboxLLMProvider (Deterministic local testing fallback)
"""

import time
import os
import json
import urllib.request
import urllib.parse
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .models import LLMRequest, LLMResponse, ResponseProvenance, ModelCapability
from .exceptions import ModelProviderError, ModelTimeoutError
from .redaction import CredentialRedactor


class IModelProvider(ABC):
    """Abstract interface for LLM model providers."""

    @abstractmethod
    def get_capability(self) -> ModelCapability:
        pass

    @abstractmethod
    def generate(self, request: LLMRequest, custom_api_key: Optional[str] = None, custom_base_url: Optional[str] = None) -> LLMResponse:
        pass


class SandboxLLMProvider(IModelProvider):
    """Deterministic sandbox provider for local testing and offline fallback."""

    def __init__(self, model_name: str = "sandbox-llm"):
        self.model_name = model_name
        self.redactor = CredentialRedactor()

    def get_capability(self) -> ModelCapability:
        return ModelCapability(
            provider="sandbox",
            model_name=self.model_name,
            version="1.0.0",
            context_limit=128000,
            supports_structured_output=True,
            supports_vision=True,
            supports_tools=True,
            reliability_class="HIGH"
        )

    def generate(self, request: LLMRequest, custom_api_key: Optional[str] = None, custom_base_url: Optional[str] = None) -> LLMResponse:
        start_time = time.time()
        clean_prompt = self.redactor.sanitize_text(request.prompt)

        if request.task_type == "TREND_ANALYSIS":
            content = json.dumps({
                "trend_name": "Y2K Minimalist Cyber",
                "confidence": 0.94,
                "key_elements": ["Chrome accents", "Sheer fabrics", "Low-rise silhouettes"],
                "market_relevance": "HIGH"
            })
        elif request.task_type == "STRATEGY_SYNTHESIS":
            content = json.dumps({
                "strategy_name": "High Conversion Grid Campaign",
                "recommended_focus": "Contrast lighting with bold typography",
                "target_audience": "Gen-Z Luxury E-Com"
            })
        else:
            content = json.dumps({
                "task_type": request.task_type,
                "result": f"Model response for prompt: {clean_prompt[:60]}...",
                "model_used": self.model_name
            })

        latency = (time.time() - start_time) * 1000.0

        prov = ResponseProvenance(
            provider="sandbox",
            model=self.model_name,
            model_version="1.0.0",
            request_id=request.request_id,
            context_scope=request.context_scope,
            structured_output_validated=True
        )

        return LLMResponse(
            request_id=request.request_id,
            content=content,
            structured_data=json.loads(content) if content.startswith("{") else None,
            provenance=prov,
            prompt_tokens=len(clean_prompt) // 4,
            completion_tokens=len(content) // 4,
            total_tokens=(len(clean_prompt) + len(content)) // 4,
            latency_ms=latency,
            status="SUCCESS"
        )


class UniversalLLMProvider(IModelProvider):
    """Universal provider supporting OpenAI, Anthropic, DeepSeek, Qwen, Ollama, and Custom Base URLs."""

    def __init__(self, provider_name: str, model_name: str, default_base_url: Optional[str] = None, tier: str = "STANDARD"):
        self.provider_name = provider_name  # e.g., "openai", "anthropic", "deepseek", "qwen", "fable", "ollama", "custom"
        self.model_name = model_name        # e.g., "gpt-5-turbo", "claude-3-7-sonnet", "deepseek-r1", "fable-1-creative"
        self.default_base_url = default_base_url
        self.tier = tier                    # "STANDARD" or "PRO"
        self.sandbox_fallback = SandboxLLMProvider(model_name=f"sandbox-{model_name}")
        self.redactor = CredentialRedactor()

    def get_capability(self) -> ModelCapability:
        return ModelCapability(
            provider=self.provider_name,
            model_name=self.model_name,
            version="2026.1",
            context_limit=128000,
            supports_structured_output=True,
            supports_vision=True,
            supports_tools=True,
            reliability_class="HIGH",
            tier=self.tier
        )

    def generate(self, request: LLMRequest, custom_api_key: Optional[str] = None, custom_base_url: Optional[str] = None) -> LLMResponse:
        api_key = custom_api_key or os.getenv(f"{self.provider_name.upper()}_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = custom_base_url or self.default_base_url

        # Fallback to sandbox if no custom API key or provider key is present
        if not api_key and self.provider_name != "ollama":
            resp = self.sandbox_fallback.generate(request)
            resp.provenance.provider = f"{self.provider_name}_sandbox_fallback"
            resp.provenance.model = self.model_name
            return resp

        start_time = time.time()
        clean_prompt = self.redactor.sanitize_text(request.prompt)

        # Standard HTTP payload for OpenAI-compatible completions
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": request.system_instruction or "You are an AI creative assistant."},
                {"role": "user", "content": clean_prompt}
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }

        target_url = (base_url or "https://api.openai.com/v1").rstrip("/") + "/chat/completions"

        try:
            req_data = json.dumps(payload).encode("utf-8")
            http_req = urllib.request.Request(target_url, data=req_data, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}" if api_key else ""
            })
            
            with urllib.request.urlopen(http_req, timeout=15) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                content = res_json["choices"][0]["message"]["content"]
                latency = (time.time() - start_time) * 1000.0

                prov = ResponseProvenance(
                    provider=self.provider_name,
                    model=self.model_name,
                    model_version="2026.1",
                    request_id=request.request_id,
                    context_scope=request.context_scope
                )

                return LLMResponse(
                    request_id=request.request_id,
                    content=content,
                    provenance=prov,
                    latency_ms=latency,
                    status="SUCCESS"
                )
        except Exception as e:
            # Fallback to sandbox upon HTTP error or connection failure
            resp = self.sandbox_fallback.generate(request)
            resp.provenance.provider = f"{self.provider_name}_fallback_err:{type(e).__name__}"
            resp.provenance.model = self.model_name
            return resp


class GeminiLiveProvider(IModelProvider):
    """Live Google Gemini Provider adapter."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.sandbox_fallback = SandboxLLMProvider(model_name=f"sandbox-{model_name}")
        self.redactor = CredentialRedactor()

    def get_capability(self) -> ModelCapability:
        is_pro = self.model_name in ["gemini-3.5-pro", "gemini-3.0-flash"]
        return ModelCapability(
            provider="google",
            model_name=self.model_name,
            version="2026.1",
            context_limit=1000000,
            supports_structured_output=True,
            supports_vision=True,
            supports_tools=True,
            reliability_class="HIGH",
            tier="PRO" if is_pro else "STANDARD"
        )

    def generate(self, request: LLMRequest, custom_api_key: Optional[str] = None, custom_base_url: Optional[str] = None) -> LLMResponse:
        key = custom_api_key or self.api_key
        if not key:
            resp = self.sandbox_fallback.generate(request)
            resp.provenance.provider = "google_sandbox_fallback"
            return resp

        start_time = time.time()
        clean_prompt = self.redactor.sanitize_text(request.prompt)

        try:
            from google import genai
            client = genai.Client(api_key=key)
            result = client.models.generate_content(
                model=self.model_name,
                contents=clean_prompt,
            )

            latency = (time.time() - start_time) * 1000.0
            content = result.text or ""

            prov = ResponseProvenance(
                provider="google",
                model=self.model_name,
                model_version="2026.1",
                request_id=request.request_id,
                context_scope=request.context_scope
            )

            return LLMResponse(
                request_id=request.request_id,
                content=content,
                provenance=prov,
                latency_ms=latency,
                status="SUCCESS"
            )
        except Exception as e:
            resp = self.sandbox_fallback.generate(request)
            resp.provenance.provider = f"google_fallback_err:{type(e).__name__}"
            return resp
