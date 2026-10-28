"""
The Trip-Sitter: Cognitive Guardrail, Coherence Evaluator & Anti-Psychosis Circuit Breaker.
Ensures divergent conceptual exploration does not degenerate into ungrounded hallucinations,
syntactic delirium, or unrecoverable mode collapse.
"""

from typing import Dict, Any, List, Tuple, Optional
import re
from pydantic import BaseModel, Field

from psychoactive.core.state import NeurochemicalState, LifecycleStage


class CoherenceReport(BaseModel):
    """Diagnostic report evaluating output viability and groundedness."""
    coherence_score: float = Field(description="Score in [0.0, 1.0] measuring semantic grounding")
    divergence_score: float = Field(description="Score in [0.0, 1.0] measuring novelty beyond baseline")
    hallucination_risk: float = Field(description="Estimated risk of unmoored confabulation [0.0, 1.0]")
    circuit_breaker_triggered: bool = Field(default=False, description="Whether emergency antagonist was applied")
    intervention_notes: List[str] = Field(default_factory=list, description="Corrective actions taken by Trip-Sitter")


class TripSitter:
    """
    Automated safety supervisor monitoring the psychoactive reasoning trajectory.
    Applies the Silicon-Serotonergic safety firewalls detailed in Section 16 of the paper:
    1. Unanchored Hallucination Breaker
    2. Syntactic Coherence Guard
    3. Emergency Re-Annealing Antagonist Protocol (5-HT2A inverse agonism analog)
    """

    def __init__(
        self,
        min_coherence_threshold: float = 0.35,
        max_hallucination_threshold: float = 0.75,
    ):
        self.min_coherence_threshold = min_coherence_threshold
        self.max_hallucination_threshold = max_hallucination_threshold

    def evaluate_output(
        self,
        output_text: str,
        stage: LifecycleStage,
        original_task: str,
        baseline_text: Optional[str] = None,
    ) -> CoherenceReport:
        """
        Evaluates a stage's output text for coherence, divergence, and groundedness.
        """
        text = output_text.strip()
        interventions: List[str] = []
        triggered = False

        # 1. Structural emptiness check
        if len(text) < 20:
            interventions.append("Severe syntactic collapse detected: Output too short.")
            return CoherenceReport(
                coherence_score=0.0,
                divergence_score=0.0,
                hallucination_risk=1.0,
                circuit_breaker_triggered=True,
                intervention_notes=interventions,
            )

        # 2. Check for psychotic loop / infinite repetition (Token stuttering)
        words = [w.lower() for w in re.findall(r'\b\w+\b', text)]
        unique_words_count = len(set(words))
        if len(words) >= 10 and unique_words_count <= 3:
            interventions.append("Catastrophic mode-stutter loop detected (low vocabulary entropy).")
            triggered = True
        elif len(words) >= 15:
            trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]
            unique_ratio = len(set(trigrams)) / max(1, len(trigrams))
            if unique_ratio < 0.30:
                interventions.append("Catastrophic mode-stutter loop detected (low n-gram entropy).")
                triggered = True

        # 3. Domain overlap check (Is the analogy anchored to the task?)
        task_keywords = set(re.findall(r'\b[a-zA-Z]{4,}\b', original_task.lower()))
        output_keywords = set(re.findall(r'\b[a-zA-Z]{4,}\b', text.lower()))

        shared_keywords = task_keywords.intersection(output_keywords)
        keyword_overlap = len(shared_keywords) / max(1, len(task_keywords))

        # During Peak, low overlap is expected (high divergence).
        # During Return, high overlap is mandatory (grounded deliverable).
        if stage == LifecycleStage.PEAK:
            divergence_score = min(1.0, 0.70 + (0.30 * (1.0 - keyword_overlap)))
            coherence_score = max(0.40, 0.50 + (0.50 * keyword_overlap))
            hallucination_risk = 0.20 if not triggered else 0.85
        elif stage == LifecycleStage.RETURN:
            divergence_score = 0.50
            coherence_score = min(1.0, 0.60 + (0.40 * keyword_overlap))
            hallucination_risk = 0.10 if keyword_overlap >= 0.20 else 0.45
            if keyword_overlap < 0.10:
                interventions.append("Weak domain anchoring in final return deliverable.")
        else:
            divergence_score = 0.30
            coherence_score = 0.85
            hallucination_risk = 0.05

        if coherence_score < self.min_coherence_threshold or hallucination_risk > self.max_hallucination_threshold:
            triggered = True
            interventions.append("Trip-Sitter Emergency Circuit Breaker: Initiated rapid prior re-tightening.")

        return CoherenceReport(
            coherence_score=round(coherence_score, 3),
            divergence_score=round(divergence_score, 3),
            hallucination_risk=round(hallucination_risk, 3),
            circuit_breaker_triggered=triggered,
            intervention_notes=interventions,
        )

    def apply_emergency_antagonist(self, state: NeurochemicalState) -> str:
        """
        Emergency reset protocol (Silicon Ketanserin / 5-HT2A inverse agonism):
        Forces immediate return to Baseline homeostatic precision (pi_P = 1.0)
        and resets lateral retrograde gating to zero.
        """
        state.transition_to_stage(LifecycleStage.BASELINE)
        return (
            "EMERGENCY TRIP-SITTER PROTOCOL ENGAGED.\n"
            "Pharmacological antagonist administered: Reset prior precision to pi_P = 1.0. "
            "Re-anchoring search to safe, conservative domain bounds."
        )
