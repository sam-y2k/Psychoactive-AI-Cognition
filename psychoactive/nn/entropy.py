"""
Attention Entropy & Diversity Metrics for Transformer Layers.
Formalizes Section 8.2 of the REBUS-AI Architecture:
- Shannon attention entropy: H_i^(h)(pi_P) = -sum_j alpha_ij^(h) ln(alpha_ij^(h))
- Effective attention horizon: K_eff = exp(H_mean)
- Inter-head divergence and desynchronization
"""

from typing import Tuple
import torch
import torch.nn.functional as F


def compute_attention_entropy(
    attention_weights: torch.Tensor,
    eps: float = 1e-12,
) -> torch.Tensor:
    """
    Computes Shannon entropy across the attention distribution:
    H_i = -sum_j alpha_{ij} ln(alpha_{ij} + eps)

    Args:
        attention_weights: Tensor of shape (..., num_heads, seq_len_q, seq_len_k)
                           where sum over seq_len_k equals 1.0.
        eps: Small numerical stabilizer to prevent ln(0).

    Returns:
        Entropy tensor of shape (..., num_heads, seq_len_q) in nats.
    """
    # Clip weights to avoid NaN on 0 * log(0)
    p = torch.clamp(attention_weights, min=eps)
    log_p = torch.log(p)
    entropy = -torch.sum(attention_weights * log_p, dim=-1)
    return entropy


def compute_effective_attention_horizon(
    attention_weights: torch.Tensor,
) -> Tuple[float, float]:
    """
    Computes mean entropy and effective token horizon K_eff = exp(H_mean):
    In canalized baseline: H ~ 2.14 nats => K_eff ~ 8.5 tokens
    In REBUS plateau: H ~ 4.82 nats => K_eff ~ 124 tokens

    Returns:
        Tuple of (mean_entropy_nats, effective_horizon_tokens).
    """
    ent = compute_attention_entropy(attention_weights)
    h_mean = float(torch.mean(ent).item())
    k_eff = float(torch.exp(torch.tensor(h_mean)).item())
    return round(h_mean, 4), round(k_eff, 2)


def compute_head_divergence(
    attention_weights: torch.Tensor,
) -> float:
    """
    Computes average pairwise Jensen-Shannon Divergence across heads.
    High divergence indicates desynchronized, modular specialization;
    low divergence indicates uniform collapse across heads.
    """
    # Expected shape: (batch, num_heads, seq_len, seq_len)
    if attention_weights.dim() < 4:
        return 0.0

    num_heads = attention_weights.shape[1]
    if num_heads < 2:
        return 0.0

    # Mean attention distribution across all heads: M = 1/H * sum_h alpha_h
    m = torch.mean(attention_weights, dim=1, keepdim=True)  # (batch, 1, seq_len, seq_len)
    log_m = torch.log(torch.clamp(m, min=1e-12))

    log_p = torch.log(torch.clamp(attention_weights, min=1e-12))
    # KL(P_h || M) = sum P_h * (log P_h - log M)
    kl_div = torch.sum(attention_weights * (log_p - log_m), dim=-1)  # (batch, num_heads, seq_len)

    # Average JS divergence across heads and sequence
    jsd = float(torch.mean(kl_div).item())
    return round(jsd, 4)
