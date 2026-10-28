"""
Universal "Jack of All Trades" Meta-Template.
Operates on ANY prompt, task, or problem across all domains without hardcoded constraints.
"""

from typing import Optional, Dict, Any
from psychoactive.compounds import CompoundType
from psychoactive.templates.base import NeuroTemplate


class UniversalTemplate(NeuroTemplate):
    """
    Jack-of-All-Trades Meta-Template.
    Transforms arbitrary user inputs through the 4-stage neurochemical trajectory,
    dissolving generic corporate clichés and synthesizing grounded breakthroughs.
    """

    def __init__(
        self,
        domain_name: str = "Universal Problem Solving",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
        custom_grounding_criteria: Optional[str] = None,
    ):
        super().__init__(domain_name=domain_name, compound=compound, dose=dose)
        self.custom_grounding_criteria = custom_grounding_criteria

    def get_domain_grounding_rules(self) -> str:
        """
        Universal grounding rubrics that enforce high-utility execution across any field.
        """
        base_rules = (
            "1. NO EMPTY PLATITUDES: Eliminate high-level buzzwords ('leverage synergies', 'optimize workflows').\n"
            "2. SPECIFICITY OVER GENERALITY: Produce concrete, line-by-line deliverables (scripts, formulas, architectures, steps).\n"
            "3. REAL-WORLD VIABILITY: The deliverable must be immediately executable within the user's constraints.\n"
            "4. PRESERVE THE LEAP: Do not revert back to the boring baseline; retain the unfair advantage of the breakthrough."
        )
        if self.custom_grounding_criteria:
            return f"{base_rules}\n5. CUSTOM USER MANDATE: {self.custom_grounding_criteria}"
        return base_rules
