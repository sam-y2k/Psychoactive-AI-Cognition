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

# Mathematical Solvers
from psychoactive.math.procrustes import OrthogonalProcrustesSolver, StiefelResult
from psychoactive.math.tda import PersistentHomologyEngine, compute_newman_modularity
from psychoactive.math.langevin import LangevinAttractorSimulator, AttractorLandscape, kramers_escape_rate

# Native PyTorch Neural Modules
from psychoactive.nn.dmn_attention import REBUSMultiHeadAttention, AttentionLogitDecomposition
from psychoactive.nn.retrograde_layer import CB1RetrogradeLayer, GatingComponents
from psychoactive.nn.entropy import compute_attention_entropy, compute_effective_attention_horizon

# Deterministic Verification & Benchmarks
from psychoactive.verification.ldm import LateralDivergenceEvaluator, LDMResult
from psychoactive.verification.z3_verifier import Z3ConstraintVerifier, VerificationProof
from psychoactive.benchmarks.rat_benchmark import RATBenchmarkRunner, RATItem
from psychoactive.benchmarks.ablation_runner import AblationBenchmarkRunner, AblationReport

__version__ = "0.2.0"

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
    # Mathematical Solvers
    "OrthogonalProcrustesSolver",
    "StiefelResult",
    "PersistentHomologyEngine",
    "compute_newman_modularity",
    "LangevinAttractorSimulator",
    "AttractorLandscape",
    "kramers_escape_rate",
    # PyTorch Neural Modules
    "REBUSMultiHeadAttention",
    "AttentionLogitDecomposition",
    "CB1RetrogradeLayer",
    "GatingComponents",
    "compute_attention_entropy",
    "compute_effective_attention_horizon",
    # Verification & Benchmarks
    "LateralDivergenceEvaluator",
    "LDMResult",
    "Z3ConstraintVerifier",
    "VerificationProof",
    "RATBenchmarkRunner",
    "RATItem",
    "AblationBenchmarkRunner",
    "AblationReport",
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
