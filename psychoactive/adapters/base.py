"""
Abstract Model Adapter & Deterministic Mock Backend.
Provides zero-lock-in model execution with built-in mock fallback for offline testing.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseModelAdapter(ABC):
    """
    Abstract interface for LLM backends.
    Allows psychoactive templates to steer any LLM without platform lock-in.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        hyperparameters: Optional[Dict[str, float]] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Execute completion with dynamic neurochemical sampling parameters.
        """
        pass


class MockModelAdapter(BaseModelAdapter):
    """
    Deterministic mock adapter for testing, validation, and offline execution without API keys.
    Generates realistic multi-stage responses simulating LLM outputs.
    """

    def __init__(self, responses: Optional[Dict[str, str]] = None):
        self.call_history: List[Dict[str, Any]] = []
        self.responses = responses or {}

    def generate(
        self,
        prompt: str,
        hyperparameters: Optional[Dict[str, float]] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        params = hyperparameters or {}
        self.call_history.append({
            "prompt": prompt,
            "hyperparameters": params,
            "system_instruction": system_instruction,
        })

        # Match custom responses if provided
        for key, resp in self.responses.items():
            if key in prompt:
                return resp

        # Default stage-aware simulated responses
        if "STAGE 1: CANONICAL BASELINE" in prompt:
            return (
                "[CANONICAL BASELINE]\n"
                "The standard approach is to implement a centralized coordination layer with standard "
                "relational tables and conventional rule-based heuristics."
            )
        elif "STAGE 2: ASCENT" in prompt:
            return (
                "[DISMANTLED ASSUMPTIONS]\n"
                "1. Centralized coordination is inherently required for consistency.\n"
                "2. System components must have synchronous state visibility.\n"
                "3. Failure recovery must be deterministic and top-down."
            )
        elif "STAGE 3: PEAK" in prompt:
            return (
                "[PEAK BREAKTHROUGH]\n"
                "Isomorphic synthesis: Map the system onto decentralized fungal hyphae sharing resources "
                "via pulsed local gradients without a global clock or central lock manager."
            )
        elif "STAGE 4: INTEGRATION" in prompt:
            return (
                "[PARADIGM SHIFT]: Replaced centralized mutex locking with localized stigmergic gradient diffusion.\n"
                "[THE MECHANISM]: Nodes broadcast discrete decay pulses to immediate peers; consensus emerges asynchronously.\n"
                "[ACTIONABLE DELIVERABLE]:\n"
                "1. Deploy a ring-buffered lock-free queue with local epoch versioning.\n"
                "2. Replace the master coordinator with an asynchronous gossip-decay protocol.\n"
                "3. Immediate 4x throughput gain with zero deadlock risk."
            )

        return "Simulated execution output."
