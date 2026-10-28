"""
Psychoactive: Universal Neurochemical Cognitive Meta-Layer for AI.
A Jack-of-All-Trades cognitive template for escaping LLM mode collapse.
"""

from psychoactive.compounds import (
    CompoundType,
    CompoundProfile,
    COMPOUND_REGISTRY,
    get_compound_profile,
)
from psychoactive.core.state import NeurochemicalState, LifecycleStage
from psychoactive.core.rebus import REBUSEngine
from psychoactive.core.retrograde import RetrogradeFilter
from psychoactive.core.stiefel import StiefelProjector

from psychoactive.templates.base import NeuroTemplate, BreakthroughResult
from psychoactive.templates.universal import UniversalTemplate
from psychoactive.templates.sales import SalesTemplate
from psychoactive.templates.engineering import EngineeringTemplate
from psychoactive.templates.strategy import StrategyTemplate
from psychoactive.templates.creative import CreativeTemplate

from psychoactive.adapters.base import BaseModelAdapter, MockModelAdapter
from psychoactive.adapters.universal_llm import UniversalLLMAdapter
from psychoactive.adapters.decorators import psychoactive

from psychoactive.integration.sitter import TripSitter, CoherenceReport
from psychoactive.integration.grounder import IntegrationGrounder, GroundedArtifact

from psychoactive.session import NeuroSession

__version__ = "0.1.0"

__all__ = [
    # Pharmacological Core
    "CompoundType",
    "CompoundProfile",
    "COMPOUND_REGISTRY",
    "get_compound_profile",
    "NeurochemicalState",
    "LifecycleStage",
    "REBUSEngine",
    "RetrogradeFilter",
    "StiefelProjector",
    # Templates (Jack of All Trades)
    "NeuroTemplate",
    "BreakthroughResult",
    "UniversalTemplate",
    "SalesTemplate",
    "EngineeringTemplate",
    "StrategyTemplate",
    "CreativeTemplate",
    # Adapters & Decorators
    "BaseModelAdapter",
    "MockModelAdapter",
    "UniversalLLMAdapter",
    "psychoactive",
    # Safety & Grounding Gate
    "TripSitter",
    "CoherenceReport",
    "IntegrationGrounder",
    "GroundedArtifact",
    # Session Runner
    "NeuroSession",
]
