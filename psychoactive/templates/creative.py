"""
Creative & Narrative Synthesis Template.
Overturns formulaic writing tropes, generic copywriting, and predictable screenwriting beats.
"""

from typing import Optional
from psychoactive.compounds import CompoundType
from psychoactive.templates.base import NeuroTemplate


class CreativeTemplate(NeuroTemplate):
    """
    Cognitive template for Screenwriting, High-Concept Branding, and Novel Narrative Synthesis.
    Overcomes AI writing tropes (sterile tone, predictable three-act structures, trite metaphors).
    """

    def __init__(
        self,
        medium: str = "Narrative Writing / Branding",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
    ):
        super().__init__(domain_name=f"Creative Synthesis ({medium})", compound=compound, dose=dose)
        self.medium = medium

    def get_domain_grounding_rules(self) -> str:
        return (
            "1. ZERO AI STERILITY: Eliminate AI filler words, generic adjectives ('delve', 'testament', 'tapestry'), and safe clichés.\n"
            "2. VISCERAL SENSORY TEXTURE: Ground narrative breakthroughs in specific, tactile, concrete imagery.\n"
            "3. DELIVERABLE ARTIFACT: Deliver the full finished text, logline, treatment, or hook ready for publication."
        )
