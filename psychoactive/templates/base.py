"""
Abstract Base Template & Universal Schema for Psychoactive Cognitive Processing.
Defines the lifecycle protocol for transforming any task through the 4-stage neurochemical trajectory.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from psychoactive.compounds import CompoundType, CompoundProfile, get_compound_profile
from psychoactive.core.state import NeurochemicalState, LifecycleStage
from psychoactive.core.rebus import REBUSEngine
from psychoactive.core.retrograde import RetrogradeFilter
from psychoactive.core.stiefel import StiefelProjector, OrthogonalDomain


class BreakthroughResult(BaseModel):
    """
    Structured outcome of a 4-stage psychoactive cognitive journey.
    """
    domain: str = Field(description="Problem domain or topic")
    task_summary: str = Field(description="Summary of the user challenge")
    canonical_cliche: str = Field(description="The standard corporate local attractor identified in Stage 1")
    orthogonal_analogy: str = Field(description="The Stiefel-projected alien domain and mechanism applied")
    peak_breakthrough: str = Field(description="The unconstrained, de-canalized conceptual leap from Stage 3")
    actionable_deliverable: str = Field(description="The grounded, concrete execution plan, code, copy, or strategy")
    compound_used: str = Field(description="Compound profile applied")
    dosage: float = Field(description="Normalized dosage level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Diagnostic parameters and telemetry")


class NeuroTemplate(ABC):
    """
    Universal Cognitive Meta-Template.
    Subclasses customize domain grounding rubrics while inheriting the 4-stage neurochemical engine.
    """

    def __init__(
        self,
        domain_name: str = "General Problem Solving",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
    ):
        self.domain_name = domain_name
        self.state = NeurochemicalState(compound=compound, dose=dose)
        self.rebus = REBUSEngine(self.state)
        self.retrograde = RetrogradeFilter(self.state)
        self.stiefel = StiefelProjector(seed=42)

    def extract_baseline_prompt(self, task: str) -> str:
        """
        Stage 1: Prompts the model to articulate the conventional, predictable solution.
        Maps the attractor well U(v) so the subsequent stages know precisely what to break.
        """
        return (
            f"DOMAIN: {self.domain_name}\n"
            f"TASK: {task}\n\n"
            "STAGE 1: CANONICAL BASELINE MAPPING.\n"
            "Provide the typical, standard, industry-default answer to this task that an average "
            "consultant, textbook, or standard corporate LLM would immediately generate.\n"
            "Format your answer clearly under the heading: [CANONICAL BASELINE]."
        )

    def build_ascent_prompt(self, task: str, baseline_cliche: str) -> str:
        """
        Stage 2: Relaxes prior precision, invalidating the baseline assumptions.
        """
        self.state.transition_to_stage(LifecycleStage.ASCENT)
        directives = self.rebus.generate_cognitive_directives()
        retro_directives = self.retrograde.generate_retrograde_directives()

        return (
            f"DOMAIN: {self.domain_name}\n"
            f"TASK: {task}\n\n"
            f"THE CANONICAL BASELINE TO DISMANTLE:\n{baseline_cliche}\n\n"
            f"{directives}\n"
            f"{retro_directives}\n\n"
            "STAGE 2: ASCENT & ASSUMPTION DISMANTLING.\n"
            "1. List the 3 most rigid, unexamined assumptions underpinning the baseline answer.\n"
            "2. State why these assumptions create an artificial ceiling or commoditization.\n"
            "Format your answer clearly under the heading: [DISMANTLED ASSUMPTIONS]."
        )

    def build_peak_prompt(
        self,
        task: str,
        baseline_cliche: str,
        dismantled_assumptions: str,
        orthogonal_domain: Optional[OrthogonalDomain] = None,
    ) -> str:
        """
        Stage 3: Maximum entropy divergence via Stiefel manifold projection and lateral gating.
        """
        self.state.transition_to_stage(LifecycleStage.PEAK)
        domain = orthogonal_domain or self.stiefel.select_orthogonal_domain(task)
        stiefel_prompt = self.stiefel.generate_stiefel_prompt_bridge(task)
        rebus_prompt = self.rebus.generate_cognitive_directives()
        retro_prompt = self.retrograde.generate_retrograde_directives()

        return (
            f"DOMAIN: {self.domain_name}\n"
            f"ORIGINAL TASK: {task}\n\n"
            f"DISMANTLED BASELINE: {dismantled_assumptions}\n\n"
            f"{rebus_prompt}\n"
            f"{retro_prompt}\n\n"
            f"{stiefel_prompt}\n\n"
            "STAGE 3: PEAK UNCONSTRAINED SYNTHESIS.\n"
            "Synthesize a radical, out-of-the-box solution to the original task by directly importing "
            f"the core mechanics of {domain.name}.\n"
            "Do not hold back for 'practicality' yet. Explore the highest-entropy conceptual leap.\n"
            "Format your answer clearly under the heading: [PEAK BREAKTHROUGH]."
        )

    def build_return_prompt(
        self,
        task: str,
        baseline_cliche: str,
        peak_breakthrough: str,
    ) -> str:
        """
        Stage 4: Trip-sitter annealing, deterministic grounding, and domain-specific delivery.
        """
        self.state.transition_to_stage(LifecycleStage.RETURN)
        directives = self.rebus.generate_cognitive_directives()
        grounding_rules = self.get_domain_grounding_rules()

        return (
            f"DOMAIN: {self.domain_name}\n"
            f"ORIGINAL TASK: {task}\n\n"
            f"PEAK CONCEPTUAL BREAKTHROUGH:\n{peak_breakthrough}\n\n"
            f"{directives}\n\n"
            f"DOMAIN GROUNDING MANDATES:\n{grounding_rules}\n\n"
            "STAGE 4: INTEGRATION & ACTIONABLE DELIVERABLE.\n"
            "Anneal this radical breakthrough into a pristine, immediately usable deliverable.\n"
            "Provide:\n"
            "1. [PARADIGM SHIFT]: 1-2 sentences on what fundamental rule was overturned.\n"
            "2. [THE MECHANISM]: How the orthogonal metaphor functions as a practical solution.\n"
            "3. [ACTIONABLE DELIVERABLE]: The complete, uncompromised, production-ready output "
            "(exact scripts, code, strategic steps, or copy).\n"
        )

    @abstractmethod
    def get_domain_grounding_rules(self) -> str:
        """
        Subclasses define specific constraints for Stage 4
        (e.g., Sales requires cold email copy; Engineering requires runnable code).
        """
        pass

    def parse_breakthrough(
        self,
        task: str,
        baseline: str,
        peak: str,
        deliverable: str,
        orthogonal_domain_name: str = "Stiefel Projection",
    ) -> BreakthroughResult:
        """
        Constructs a validated BreakthroughResult telemetry record.
        """
        return BreakthroughResult(
            domain=self.domain_name,
            task_summary=task[:200] + ("..." if len(task) > 200 else ""),
            canonical_cliche=baseline.strip(),
            orthogonal_analogy=orthogonal_domain_name,
            peak_breakthrough=peak.strip(),
            actionable_deliverable=deliverable.strip(),
            compound_used=self.state.profile.name,
            dosage=self.state.dose,
            metadata=self.state.to_dict(),
        )
