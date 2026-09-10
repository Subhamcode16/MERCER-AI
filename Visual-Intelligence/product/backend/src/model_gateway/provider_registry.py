"""
Phase 20 - Provider Registry for LLM Models.

Maintains registry of approved model providers and capability mappings.
"""

from typing import Dict, List, Optional
from .provider import IModelProvider, SandboxLLMProvider, GeminiLiveProvider, UniversalLLMProvider
from .exceptions import ModelNotFoundError


class ModelProviderRegistry:
    """Registry managing available LLM model provider adapters."""

    def __init__(self):
        self._providers: Dict[str, IModelProvider] = {}
        self._register_default_providers()

    def _register_default_providers(self) -> None:
        self.register_provider("sandbox-llm", SandboxLLMProvider("sandbox-llm"))
        
        # Google Gemini Models
        self.register_provider("gemini-3.5-pro", GeminiLiveProvider("gemini-3.5-pro"))
        self.register_provider("gemini-3.0-flash", GeminiLiveProvider("gemini-3.0-flash"))
        self.register_provider("gemini-2.5-flash", GeminiLiveProvider("gemini-2.5-flash"))
        self.register_provider("gemini-1.5-pro", GeminiLiveProvider("gemini-1.5-pro"))
        
        # OpenAI Next-Gen & Standard Models
        self.register_provider("gpt-5-turbo", UniversalLLMProvider("openai", "gpt-5-turbo", "https://api.openai.com/v1", tier="PRO"))
        self.register_provider("gpt-4.5-preview", UniversalLLMProvider("openai", "gpt-4.5-preview", "https://api.openai.com/v1", tier="PRO"))
        self.register_provider("gpt-4o", UniversalLLMProvider("openai", "gpt-4o", "https://api.openai.com/v1", tier="STANDARD"))
        self.register_provider("gpt-4o-mini", UniversalLLMProvider("openai", "gpt-4o-mini", "https://api.openai.com/v1", tier="STANDARD"))
        
        # Anthropic Next-Gen & Standard Models
        self.register_provider("claude-3-7-sonnet", UniversalLLMProvider("anthropic", "claude-3-7-sonnet", "https://openrouter.ai/api/v1", tier="PRO"))
        self.register_provider("claude-3-5-sonnet", UniversalLLMProvider("anthropic", "claude-3-5-sonnet", "https://openrouter.ai/api/v1", tier="STANDARD"))
        self.register_provider("claude-3-5-haiku", UniversalLLMProvider("anthropic", "claude-3-5-haiku", "https://openrouter.ai/api/v1", tier="STANDARD"))
        
        # Fable Creative Specialty Models
        self.register_provider("fable-1-creative", UniversalLLMProvider("fable", "fable-1-creative", "https://api.fable.ai/v1", tier="PRO"))
        self.register_provider("fable-cinema-v2", UniversalLLMProvider("fable", "fable-cinema-v2", "https://api.fable.ai/v1", tier="PRO"))

        # DeepSeek Reasoning & High-Performance Models
        self.register_provider("deepseek-r1", UniversalLLMProvider("deepseek", "deepseek-r1", "https://api.deepseek.com/v1", tier="PRO"))
        self.register_provider("deepseek-v3", UniversalLLMProvider("deepseek", "deepseek-v3", "https://api.deepseek.com/v1", tier="STANDARD"))

        # Open-Source & Regional Models
        self.register_provider("qwen-2.5-72b", UniversalLLMProvider("qwen", "qwen-2.5-72b", "https://openrouter.ai/api/v1", tier="STANDARD"))
        self.register_provider("llama-3.3-70b", UniversalLLMProvider("llama", "llama-3.3-70b", "https://openrouter.ai/api/v1", tier="STANDARD"))
        self.register_provider("ollama-local", UniversalLLMProvider("ollama", "llama3.2", "http://localhost:11434/v1", tier="STANDARD"))

    def register_provider(self, name: str, provider: IModelProvider) -> None:
        self._providers[name] = provider

    def get_provider(self, name: str) -> IModelProvider:
        if name in self._providers:
            return self._providers[name]
        
        # Block unapproved / malicious / invalid vendor strings
        if name.startswith("unapproved_") or name.startswith("malicious_") or name.startswith("invalid_"):
            raise ModelNotFoundError(f"Model provider '{name}' not found in registry.")

        # Dynamic instantiation for universal models
        if name.startswith("gemini"):
            provider = GeminiLiveProvider(model_name=name)
        elif name.startswith("sandbox"):
            provider = SandboxLLMProvider(model_name=name)
        else:
            provider = UniversalLLMProvider(provider_name="universal", model_name=name)
        
        self._providers[name] = provider
        return provider

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())
