"""
REBUS Engine (Relaxed Beliefs Under Psychedelics).
Implements the 5-HT2A cortical prior precision relaxation operator:
A_ij(pi_P) = L_ij + pi_P * P_ij
Dismantles canalized narrative loops and dissolves semantic attractor basins.
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
from psychoactive.core.state import NeurochemicalState, LifecycleStage


class REBUSEngine:
    """
    Mathematical and cognitive engine implementing the REBUS principle.
    Operates at both numeric tensor levels (logit decomposition) and prompt-semantic levels.
    """

    def __init__(self, state: NeurochemicalState):
        self.state = state

    def compute_decomposed_logits(
        self,
        likelihood_logits: np.ndarray,
        prior_matrix: Optional[np.ndarray] = None,
        rank: int = 8,
    ) -> np.ndarray:
        """
        Decomposes attention/output logits into Likelihood + Prior:
        A_ij(pi_P) = L_ij + pi_P * P_ij

        Args:
            likelihood_logits: Array of shape (..., V) representing empirical/context evidence.
            prior_matrix: Canonical prior bias matrix P of shape (..., V). If None, generates low-rank UV^T.
            rank: Low-rank parameterization r for inductive prior baseline.

        Returns:
            Modulated logit tensor under instantaneous pi_P precision.
        """
        pi_p = self.state.get_prior_precision()

        if prior_matrix is None:
            # Generate deterministic low-rank inductive prior baseline: P = (U V^T) / sqrt(r)
            v_dim = likelihood_logits.shape[-1]
            rng = np.random.default_rng(seed=42)
            u = rng.standard_normal((v_dim, rank))
            v = rng.standard_normal((v_dim, rank))
            prior_matrix = np.dot(u, v.T) / np.sqrt(rank)

        # A_ij = L_ij + pi_P * P_ij
        modulated = likelihood_logits + (pi_p * prior_matrix)
        return modulated

    def get_sampling_hyperparameters(self) -> Dict[str, float]:
        """
        Translates current REBUS prior precision into standard LLM sampling parameters:
        - Temperature: Inversely scaled with prior precision (re-annealing curve)
        - Top_p: Expands during Peak, tightens during Return
        - Frequency/Presence Penalty: Elevated during Peak to penalize canonical cliché attractors
        """
        pi_p = self.state.get_prior_precision()
        stage = self.state.current_stage

        if stage == LifecycleStage.BASELINE:
            return {
                "temperature": 0.70,
                "top_p": 0.90,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0,
            }

        elif stage == LifecycleStage.ASCENT:
            # Gentle warming of temperature as priors soften
            temp = 0.70 + (0.50 * (1.0 - pi_p))
            return {
                "temperature": round(temp, 2),
                "top_p": 0.95,
                "presence_penalty": 0.30,
                "frequency_penalty": 0.20,
            }

        elif stage == LifecycleStage.PEAK:
            # Maximum entropy exploration
            temp = 0.95 + (0.35 * (1.0 - pi_p))
            return {
                "temperature": round(temp, 2),
                "top_p": 0.98,
                "presence_penalty": 0.75, # Strongly suppress repeating canonical clichés
                "frequency_penalty": 0.60,
            }

        elif stage == LifecycleStage.RETURN:
            # Controlled cooling back to deterministic precision
            temp = 0.85 * pi_p
            return {
                "temperature": max(0.20, round(temp, 2)),
                "top_p": 0.85,
                "presence_penalty": 0.15,
                "frequency_penalty": 0.10,
            }

        return {"temperature": 0.70, "top_p": 0.90}

    def generate_cognitive_directives(self) -> str:
        """
        Generates system-level neuro-cognitive directives matching the active REBUS state.
        Injected into prompt context to dismantle inductive biases across any LLM backend.
        """
        stage = self.state.current_stage
        pi_p = self.state.get_prior_precision()

        if stage == LifecycleStage.BASELINE:
            return (
                "MODE: HOMEOSTATIC BASELINE.\n"
                "Task: Map out the standard, canonical, corporate default assumptions and clichés for this problem. "
                "Expose the local minimum so we know precisely what conventional boundaries must be dismantled."
            )

        elif stage == LifecycleStage.ASCENT:
            return (
                f"MODE: 5-HT2A ASCENT (Prior Precision pi_P = {pi_p:.2f}).\n"
                "Directives:\n"
                "1. Actively suspend the canonical assumptions mapped in the baseline.\n"
                "2. Begin softening domain boundaries; challenge default terminology, industry buzzwords, and linear frameworks.\n"
                "3. Permit lateral, non-obvious hypotheses to enter working memory."
            )

        elif stage == LifecycleStage.PEAK:
            return (
                f"MODE: REBUS PEAK DIVERGENCE (Prior Precision pi_P = {pi_p:.2f} - FLATTENED POTENTIAL WELL).\n"
                "Directives:\n"
                "1. COMPLETE DE-CANALIZATION: You are strictly forbidden from offering conventional, safe, or textbook solutions.\n"
                "2. SYNCHRONOUS CROSS-DOMAIN SYNTHESIS: Force an analogical leap into a completely orthogonal discipline "
                "(e.g., Evolutionary Biology, Fungal Ecology, Hostage Negotiation, Fluid Dynamics, Distributed Cryptography).\n"
                "3. Reframe the core problem through this alien lens to discover previously invisible architectural configurations."
            )

        elif stage == LifecycleStage.RETURN:
            return (
                f"MODE: INTEGRATION & RE-ANNEALING (Prior Precision pi_P = {pi_p:.2f}).\n"
                "Directives:\n"
                "1. DETERMINISTIC CONSOLIDATION: Take the radical breakthroughs generated during the Peak phase and anchor them in reality.\n"
                "2. Translate the orthogonal metaphor into concrete, rigorous, actionable specifications.\n"
                "3. Eliminate fuzziness; produce exact tactics, scripts, schemas, code, or strategic steps that can be deployed immediately."
            )

        return ""
