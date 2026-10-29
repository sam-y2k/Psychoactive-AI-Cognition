"""
REBUS Multi-Head Attention Layer with Dynamic Logit Decomposition.
Formalizes Module 1 (Section 8) of the REBUS-AI Architecture:
A_ij(pi_P) = L_ij + pi_P * P_ij
P_ij = (U_i V_j^T) / sqrt(r)

Features:
- Exact standard Multi-Head Attention when pi_P = 1.0
- Low-rank inductive prior suppression when pi_P < 1.0 (down to 0.15)
- Causal masking & KV-cache support
- Multi-head attention entropy telemetry (H_mean, K_eff)
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from psychoactive.nn.entropy import compute_attention_entropy, compute_effective_attention_horizon


@dataclass(frozen=True)
class AttentionLogitDecomposition:
    """Telemetry report of internal attention tensors during forward pass."""
    prior_precision: float
    raw_dot_product_norm: float
    likelihood_norm: float
    prior_norm: float
    mean_entropy: float
    effective_horizon: float


class REBUSMultiHeadAttention(nn.Module):
    """
    Drop-in PyTorch Multi-Head Attention module with REBUS 5-HT2A prior relaxation.
    """

    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        dropout: float = 0.0,
        prior_rank: int = 8,
        bias: bool = True,
    ):
        super().__init__()
        if embed_dim % num_heads != 0:
            raise ValueError(f"embed_dim ({embed_dim}) must be divisible by num_heads ({num_heads})")

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.prior_rank = prior_rank
        self.scale = 1.0 / math.sqrt(self.head_dim)

        # Standard Linear Projections
        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)

        # Low-Rank Inductive Prior Generators: P = (U V^T) / sqrt(r)
        # Parameterized as projections from embed_dim to prior_rank
        self.prior_u = nn.Linear(embed_dim, num_heads * prior_rank, bias=False)
        self.prior_v = nn.Linear(embed_dim, num_heads * prior_rank, bias=False)

        self.dropout = nn.Dropout(dropout)

        # Initialize prior weights orthogonally
        nn.init.orthogonal_(self.prior_u.weight)
        nn.init.orthogonal_(self.prior_v.weight)

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        prior_precision: float = 1.0,
        attn_mask: Optional[torch.Tensor] = None,
        is_causal: bool = False,
        return_telemetry: bool = False,
    ) -> Tuple[torch.Tensor, Optional[AttentionLogitDecomposition]]:
        """
        Executes decomposed multi-head attention forward pass.

        Args:
            query: Tensor of shape (batch, seq_len_q, embed_dim)
            key: Tensor of shape (batch, seq_len_k, embed_dim)
            value: Tensor of shape (batch, seq_len_k, embed_dim)
            prior_precision: Scalar pi_P in [0.0, 1.0]. 1.0 = baseline, 0.15 = REBUS peak.
            attn_mask: Optional additive attention mask (batch, seq_len_q, seq_len_k)
            is_causal: If True, applies lower-triangular causal attention mask.
            return_telemetry: If True, returns AttentionLogitDecomposition diagnostics.

        Returns:
            Tuple of (output_tensor, optional_telemetry)
        """
        batch_size, seq_len_q, _ = query.shape
        _, seq_len_k, _ = key.shape

        pi_p = max(0.0, min(1.0, float(prior_precision)))

        # 1. Project Q, K, V -> (batch, num_heads, seq_len, head_dim)
        q = self.q_proj(query).view(batch_size, seq_len_q, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(key).view(batch_size, seq_len_k, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(value).view(batch_size, seq_len_k, self.num_heads, self.head_dim).transpose(1, 2)

        # 2. Scaled Dot-Product: S_ij = (Q K^T) / sqrt(d_k)
        raw_scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale  # (batch, heads, seq_q, seq_k)

        # 3. Compute Low-Rank Prior Matrix P_ij = (U V^T) / sqrt(r)
        # u_proj: (batch, seq_q, num_heads, prior_rank) -> (batch, num_heads, seq_q, prior_rank)
        u_priors = self.prior_u(query).view(batch_size, seq_len_q, self.num_heads, self.prior_rank).transpose(1, 2)
        v_priors = self.prior_v(key).view(batch_size, seq_len_k, self.num_heads, self.prior_rank).transpose(1, 2)
        p_matrix = torch.matmul(u_priors, v_priors.transpose(-2, -1)) / math.sqrt(self.prior_rank)

        # 4. Modulated Logit Decomposition:
        # A_ij(pi_P) = L_ij + pi_P * P_ij where L_ij = S_ij - P_ij
        # => A_ij(pi_P) = S_ij - (1.0 - pi_P) * P_ij
        logits = raw_scores - ((1.0 - pi_p) * p_matrix)

        # 5. Apply Masks (Causal / User-specified)
        if is_causal:
            causal_mask = torch.triu(
                torch.full((seq_len_q, seq_len_k), float("-inf"), device=query.device, dtype=query.dtype),
                diagonal=1,
            )
            logits = logits + causal_mask

        if attn_mask is not None:
            if attn_mask.dim() == 3:
                attn_mask = attn_mask.unsqueeze(1)  # (batch, 1, seq_q, seq_k)
            logits = logits + attn_mask

        # 6. Softmax Attention Distribution
        attn_weights = F.softmax(logits, dim=-1)
        attn_weights = self.dropout(attn_weights)

        # 7. Attention Value Weighted Sum & Output Projection
        context = torch.matmul(attn_weights, v)  # (batch, heads, seq_q, head_dim)
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len_q, self.embed_dim)
        output = self.out_proj(context)

        # 8. Optional Diagnostics & Telemetry
        telemetry: Optional[AttentionLogitDecomposition] = None
        if return_telemetry:
            h_mean, k_eff = compute_effective_attention_horizon(attn_weights)
            telemetry = AttentionLogitDecomposition(
                prior_precision=pi_p,
                raw_dot_product_norm=float(torch.norm(raw_scores).item()),
                likelihood_norm=float(torch.norm(raw_scores - p_matrix).item()),
                prior_norm=float(torch.norm(p_matrix).item()),
                mean_entropy=h_mean,
                effective_horizon=k_eff,
            )

        return output, telemetry
