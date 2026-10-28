"""
Business Strategy & Market Moat Template.
Synthesizes asymmetric blue-ocean advantages, counter-intuitive business models, and game-theoretic moats.
"""

from typing import Optional
from psychoactive.compounds import CompoundType
from psychoactive.templates.base import NeuroTemplate


class StrategyTemplate(NeuroTemplate):
    """
    Cognitive template for High-Stakes Business Strategy, Moat Construction & Competitive Positioning.
    Escapes conventional SaaS playbooks and commoditized pricing traps.
    """

    def __init__(
        self,
        industry: str = "Enterprise Technology",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
    ):
        super().__init__(domain_name=f"Strategic Moat & Business Architecture ({industry})", compound=compound, dose=dose)
        self.industry = industry

    def get_domain_grounding_rules(self) -> str:
        return (
            "1. ASYMMETRIC VALUE CAPTURE: Define a revenue or retention mechanism that incumbents cannot copy without destroying their core business.\n"
            "2. COUNTER-INTUITIVE POSITIONING: Invert the primary metric the industry competes on (e.g., speed -> patience, abundance -> scarcity).\n"
            "3. 90-DAY DEPLOYMENT ROADMAP: Provide concrete, phased steps to test and operationalize the strategic moat immediately."
        )
