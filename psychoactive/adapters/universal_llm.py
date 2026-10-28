"""
Universal LLM Adapter via LiteLLM.
Supports 100+ model backends (OpenAI, Claude, Gemini, Ollama, Groq, local vLLM).
"""

from typing import Dict, Any, Optional
import os
from psychoactive.adapters.base import BaseModelAdapter


class UniversalLLMAdapter(BaseModelAdapter):
    """
    Model-agnostic adapter leveraging LiteLLM for zero-lock-in execution.
    Injects dynamic neurochemical sampling hyperparameters (temperature, top_p, penalties).
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        timeout: float = 60.0,
    ):
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.timeout = timeout

    def generate(
        self,
        prompt: str,
        hyperparameters: Optional[Dict[str, float]] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        try:
            import litellm
        except ImportError:
            raise ImportError(
                "litellm is required for UniversalLLMAdapter. "
                "Install it via `pip install litellm`."
            )

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        # Build dynamic sampling parameters
        params = hyperparameters or {}
        call_kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "timeout": self.timeout,
        }

        if self.api_key:
            call_kwargs["api_key"] = self.api_key
        if self.api_base:
            call_kwargs["api_base"] = self.api_base

        # Map neurochemical hyperparameters to standard LLM completion kwargs
        if "temperature" in params:
            call_kwargs["temperature"] = params["temperature"]
        if "top_p" in params:
            call_kwargs["top_p"] = params["top_p"]
        if "presence_penalty" in params:
            call_kwargs["presence_penalty"] = params["presence_penalty"]
        if "frequency_penalty" in params:
            call_kwargs["frequency_penalty"] = params["frequency_penalty"]

        # Merge any user-specified overrides
        call_kwargs.update(kwargs)

        response = litellm.completion(**call_kwargs)
        return response.choices[0].message.content or ""
