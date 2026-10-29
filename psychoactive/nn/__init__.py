"""
Native PyTorch Neural Modules for Neurochemical Attention & Gating.
Implements:
- REBUSMultiHeadAttention: Multi-head attention with dynamic logit decomposition (A_ij = L_ij + pi_P P_ij)
- CB1RetrogradeLayer: Presynaptic retrograde hidden-state gating (h_t * (1 + mu * g_CB1))
- Entropy & diversity metrics across attention heads
"""

from psychoactive.nn.dmn_attention import REBUSMultiHeadAttention, AttentionLogitDecomposition
from psychoactive.nn.retrograde_layer import CB1RetrogradeLayer, GatingComponents
from psychoactive.nn.entropy import (
    compute_attention_entropy,
    compute_head_divergence,
    compute_effective_attention_horizon,
)

__all__ = [
    "REBUSMultiHeadAttention",
    "AttentionLogitDecomposition",
    "CB1RetrogradeLayer",
    "GatingComponents",
    "compute_attention_entropy",
    "compute_head_divergence",
    "compute_effective_attention_horizon",
]
