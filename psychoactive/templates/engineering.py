"""
Engineering & Systems Architecture Template.
Escapes textbook design patterns, concurrency deadlocks, and algorithmic bottlenecks.
"""

from typing import Optional
from psychoactive.compounds import CompoundType
from psychoactive.templates.base import NeuroTemplate


class EngineeringTemplate(NeuroTemplate):
    """
    Cognitive template for Software Architecture, Distributed Systems, and Algorithmic Breakthroughs.
    Breaks out of standard textbook patterns (e.g. naive 2PC locks, centralized bottlenecks)
    via biological and physical analogies.
    """

    def __init__(
        self,
        tech_stack: str = "Distributed Systems / Backend",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
    ):
        super().__init__(domain_name=f"Software Engineering ({tech_stack})", compound=compound, dose=dose)
        self.tech_stack = tech_stack

    def get_domain_grounding_rules(self) -> str:
        return (
            "1. FORMAL CORRECTNESS: The proposed architecture must satisfy thread safety, memory boundaries, and race-free execution.\n"
            "2. CONCRETE PSEUDOCODE OR REPO SCAFFOLD: Include exact data structures, algorithmic loop invariants, or type schemas.\n"
            "3. NO MAGIC HAND-WAVING: Clearly state time/space complexity (Big-O) and network synchronization boundaries.\n"
            "4. FAILURE MODE ANALYSIS: Detail the recovery path under network partitions (CAP theorem / split-brain)."
        )
