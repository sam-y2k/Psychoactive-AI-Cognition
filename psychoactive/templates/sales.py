"""
Sales & Go-to-Market Ideation Template.
Breaks free from boring, spammy cold outreach templates and commoditized value props.
"""

from typing import Optional
from psychoactive.compounds import CompoundType
from psychoactive.templates.base import NeuroTemplate


class SalesTemplate(NeuroTemplate):
    """
    Cognitive template for Out-of-the-Box B2B Sales, Cold Outreach & Positioning.
    Escapes template fatigue (0.5% response rates) by leveraging lateral hooks and psychological reframing.
    """

    def __init__(
        self,
        product: str = "Enterprise Solution",
        icp: str = "C-Level Executive",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
    ):
        super().__init__(domain_name="B2B Sales & Outbound Ideation", compound=compound, dose=dose)
        self.product = product
        self.icp = icp

    def extract_baseline_prompt(self, task: str) -> str:
        prompt = (
            f"PRODUCT / OFFERING: {self.product}\n"
            f"TARGET ICP: {self.icp}\n"
            f"OBJECTIVE: {task}\n\n"
            "STAGE 1: CANONICAL BASELINE MAPPING.\n"
            "Draft the standard, predictable cold email or sales pitch that 99% of SDRs send today.\n"
            "Include the generic pain points, standard 'hop on a quick 15-min call' CTA, and corporate jargon.\n"
            "Format your answer under: [CANONICAL BASELINE]."
        )
        return prompt

    def get_domain_grounding_rules(self) -> str:
        return (
            "1. COMPLETE COLD OUTREACH ARTIFACT: Deliver a finished, send-ready cold email or sequence.\n"
            "2. UNIGNORABLE PATTERN INTERRUPT: The subject line and opening 2 sentences must break the recipient's autopilot delete reflex.\n"
            "3. ASYMMETRIC VALUE PROPOSITION: Reframe the prospect's pain point using the orthogonal mechanism so they see it from a totally new angle.\n"
            "4. LOW-FRICTION, NON-COMMITTAL CTA: Eliminate 'Can I get 15 mins on your calendar?' Use curiosity-inducing, low-friction ask."
        )
