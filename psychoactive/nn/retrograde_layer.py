"""
Endocannabinoid CB1 Retrograde Gating Layer.
Formalizes Module 2 (Section 9.1) of the REBUS-AI Architecture:
g_CB1(h_t) = sigma(W_DSI h_t + b_DSI) * (1 - lambda_DSE * sigma(W_DSE h_t + b_DSE))
h_tilde_t = h_t * (1 + mu * g_CB1(h_t))

Features:
- Preserves the O(1) causal KV-cache invariant
- Biphasic DSI (lateral disinhibition) and DSE (bounded excitatory dampening)
- Strict DSE bounding (lambda_DSE <= 0.70) preventing representational collapse
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass(frozen=True)
class GatingComponents:
    """Internal diagnostics of the biphasic retrograde gating vector."""
    dsi_magnitude: float                # Mean activation of disinhibition channel
    dse_magnitude: float                # Mean activation of excitation dampening channel
    gating_vector_norm: float           # Norm of final g_CB1 modulation vector
    salience_gain_applied: float        # Effective scaling multiplier mu


class CB1RetrogradeLayer(nn.Module):
    """
    Presynaptic CB1 retrograde gating module acting on decoder hidden states.
    """

    def __init__(
        self,
        hidden_dim: int,
        max_lambda_dse: float = 0.70,
        gain_mu: float = 1.0,
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.max_lambda_dse = min(0.70, max(0.0, float(max_lambda_dse)))
        self.gain_mu = gain_mu

        # DSI (Depolarization-Induced Suppression of Inhibition) - Linear Projection
        self.w_dsi = nn.Linear(hidden_dim, hidden_dim, bias=True)

        # DSE (Depolarization-Induced Suppression of Excitation) - Linear Projection
        self.w_dse = nn.Linear(hidden_dim, hidden_dim, bias=True)

        # Layer Normalization for stability
        self.norm = nn.LayerNorm(hidden_dim)

        self._reset_parameters()

    def _reset_parameters(self):
        # Initialize DSI and DSE near neutral identity gates
        nn.init.orthogonal_(self.w_dsi.weight, gain=0.5)
        nn.init.zeros_(self.w_dsi.bias)
        nn.init.orthogonal_(self.w_dse.weight, gain=0.5)
        nn.init.zeros_(self.w_dse.bias)

    def forward(
        self,
        hidden_states: torch.Tensor,
        retrograde_strength: float = 1.0,
        return_diagnostics: bool = False,
    ) -> Tuple[torch.Tensor, Optional[GatingComponents]]:
        """
        Applies retrograde presynaptic filter to candidate token hidden states.

        Args:
            hidden_states: Tensor of shape (..., hidden_dim).
            retrograde_strength: Dynamic scaling factor in [0.0, 1.0].
            return_diagnostics: If True, returns GatingComponents telemetry.

        Returns:
            Tuple of (modulated_hidden_states, optional_diagnostics).
        """
        # When strength is 0 (baseline homeostatic state), pass through unmodified
        if retrograde_strength <= 1e-6:
            diag = GatingComponents(0.0, 0.0, 0.0, 0.0) if return_diagnostics else None
            return hidden_states, diag

        normed = self.norm(hidden_states)

        # 1. DSI Component: sigma(W_DSI h_t + b_DSI)
        dsi = torch.sigmoid(self.w_dsi(normed))

        # 2. DSE Component: (1 - lambda_DSE * sigma(W_DSE h_t + b_DSE))
        # Bounded by strict max_lambda_dse <= 0.70
        effective_lambda = self.max_lambda_dse * min(1.0, retrograde_strength)
        dse = 1.0 - (effective_lambda * torch.sigmoid(self.w_dse(normed)))

        # 3. Composite Retrograde Gating Vector: g_CB1 = DSI * DSE
        g_cb1 = dsi * dse

        # 4. Modulated Forward Hidden State: h_tilde = h * (1 + mu * g_CB1)
        mu = self.gain_mu * retrograde_strength
        modulated = hidden_states * (1.0 + (mu * g_cb1))

        # Diagnostics
        diag = None
        if return_diagnostics:
            diag = GatingComponents(
                dsi_magnitude=float(torch.mean(dsi).item()),
                dse_magnitude=float(torch.mean(dse).item()),
                gating_vector_norm=float(torch.norm(g_cb1).item()),
                salience_gain_applied=float(mu),
            )

        return modulated, diag
