"""
CB1 Retrograde Presynaptic Filter.
Implements endocannabinoid mechanics: Depolarization-Induced Suppression of
Inhibition (DSI) & Excitation (DSE). Rescues sub-threshold, oblique candidate
associations while penalizing high-probability canonical tropes.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
from psychoactive.core.state import NeurochemicalState, LifecycleStage


class RetrogradeFilter:
    """
    Simulates presynaptic retrograde transmission gating:
    Applies selective lateral inhibition to dominant lexical attractors
    while amplifying weak, sub-threshold remote associations.
    """

    def __init__(self, state: NeurochemicalState):
        self.state = state

    def apply_salience_filtering(
        self,
        token_logits: np.ndarray,
        salience_threshold_quantile: float = 0.20,
    ) -> np.ndarray:
        """
        Applies CB1 retrograde gating to output distribution logits:
        - Down-weights dominant top-k peaks (DSE on overactive excitatory channels)
        - Uplifts the 70th-90th percentile tail (sub-threshold salience rescue)
        - Prunes deep noise (<20th percentile) to prevent degenerate gibberish

        Args:
            token_logits: 1D array of logits across vocabulary or candidate list.
            salience_threshold_quantile: Minimum quantile threshold for association rescue.

        Returns:
            Modulated logit distribution reflecting sub-threshold salience amplification.
        """
        lam = self.state.get_retrograde_gating()
        if lam <= 0.01:
            return token_logits

        logits = np.copy(token_logits)
        # Compute distribution quantiles
        q_low = np.quantile(logits, salience_threshold_quantile)
        q_mid = np.quantile(logits, 0.70)
        q_high = np.quantile(logits, 0.95)

        # 1. Dampen hyper-dominant canonical clichés (DSE)
        dominant_mask = logits >= q_high
        logits[dominant_mask] -= (lam * 2.5)

        # 2. Amplify oblique, sub-threshold candidates (Sub-threshold salience boost)
        sub_threshold_mask = (logits >= q_mid) & (logits < q_high)
        logits[sub_threshold_mask] += (lam * 1.8)

        # 3. Suppress deep ungrounded noise
        noise_mask = logits < q_low
        logits[noise_mask] -= 10.0

        return logits

    def generate_retrograde_directives(self) -> str:
        """
        Generates prompt-level CB1 retrograde instructions for LLM steerage.
        Directs the model to notice subtle, secondary, and lateral implications.
        """
        lam = self.state.get_retrograde_gating()
        stage = self.state.current_stage

        if lam <= 0.05:
            return ""

        return (
            f"SUB-THRESHOLD SALIENCE FILTER (CB1 Retrograde Lambda = {lam:.2f}):\n"
            "1. LATERAL SUPPRESSION: Suppress the primary, most obvious answer that immediately comes to mind.\n"
            "2. TAIL ASSOCIATION RESCUE: Search for secondary, tangential, and oblique connections that are usually "
            "dismissed as 'quirky' or 'too weird'. Pull those low-probability threads to the forefront.\n"
            "3. HYPER-SALIENCE: Connect subtle, unnoticed patterns between disparate elements."
        )
