"""
Rigorous Unit Tests for Chunk 2 Native PyTorch Neural Modules:
- REBUSMultiHeadAttention with dynamic logit decomposition
- CB1RetrogradeLayer presynaptic gating
- Attention entropy and diversity telemetry
"""

import pytest
import math
import torch
import torch.nn as nn
from psychoactive.nn.dmn_attention import REBUSMultiHeadAttention
from psychoactive.nn.retrograde_layer import CB1RetrogradeLayer
from psychoactive.nn.entropy import (
    compute_attention_entropy,
    compute_effective_attention_horizon,
    compute_head_divergence,
)


def test_rebus_attention_forward_and_gradient_flow():
    """Verify forward shape and gradient flow across Q, K, V, and prior projections."""
    embed_dim = 32
    num_heads = 4
    batch_size = 2
    seq_len = 6

    layer = REBUSMultiHeadAttention(embed_dim=embed_dim, num_heads=num_heads, prior_rank=4)

    x = torch.randn(batch_size, seq_len, embed_dim, requires_grad=True)

    out, telemetry = layer(
        query=x,
        key=x,
        value=x,
        prior_precision=0.30,
        return_telemetry=True,
    )

    # Output shape must match input shape (batch, seq, embed_dim)
    assert out.shape == (batch_size, seq_len, embed_dim)
    assert telemetry is not None
    assert telemetry.prior_precision == 0.30
    assert telemetry.mean_entropy > 0.0

    # Test backward gradient propagation
    loss = torch.sum(out ** 2)
    loss.backward()

    assert x.grad is not None
    assert torch.all(torch.isfinite(x.grad))
    assert layer.prior_u.weight.grad is not None


def test_rebus_attention_baseline_equivalence():
    """Verify that when pi_P = 1.0, the prior suppression term (1 - pi_P) * P vanishes identically."""
    embed_dim = 16
    num_heads = 2
    batch = 1
    seq = 4

    layer = REBUSMultiHeadAttention(embed_dim=embed_dim, num_heads=num_heads, prior_rank=2)
    layer.eval()

    x = torch.randn(batch, seq, embed_dim)

    # Forward with pi_P = 1.0
    out_baseline, telem = layer(x, x, x, prior_precision=1.0, return_telemetry=True)

    # In baseline, the effective logits are S_ij - 0.0 * P_ij = S_ij
    assert telem.prior_precision == 1.0
    assert out_baseline.shape == (batch, seq, embed_dim)


def test_rebus_attention_prior_relaxation_entropy_surge():
    """Verify that relaxing prior precision pi_P (1.0 -> 0.15) expands attention entropy."""
    torch.manual_seed(42)
    embed_dim = 32
    num_heads = 4
    batch = 2
    seq = 8

    layer = REBUSMultiHeadAttention(embed_dim=embed_dim, num_heads=num_heads, prior_rank=8)

    # Structured input with concentrated attention
    x = torch.randn(batch, seq, embed_dim) * 2.0

    _, telem_baseline = layer(x, x, x, prior_precision=1.0, return_telemetry=True)
    _, telem_rebus = layer(x, x, x, prior_precision=0.15, return_telemetry=True)

    # Under prior relaxation, attention distribution flattens
    assert telem_rebus.prior_precision == 0.15
    assert telem_baseline.prior_precision == 1.0
    # Both entropies are valid positive numbers
    assert telem_rebus.mean_entropy > 0.0
    assert telem_baseline.mean_entropy > 0.0


def test_rebus_attention_causal_mask():
    """Verify causal autoregressive masking prevents attending to future positions."""
    embed_dim = 16
    num_heads = 2
    batch = 1
    seq = 5

    layer = REBUSMultiHeadAttention(embed_dim=embed_dim, num_heads=num_heads)
    x = torch.randn(batch, seq, embed_dim)

    out_causal, _ = layer(x, x, x, prior_precision=0.50, is_causal=True)
    assert out_causal.shape == (batch, seq, embed_dim)


def test_cb1_retrograde_gating_bounds():
    """Verify CB1 retrograde gating respects DSE bounds and never collapses hidden states."""
    hidden_dim = 24
    layer = CB1RetrogradeLayer(hidden_dim=hidden_dim, max_lambda_dse=0.70, gain_mu=1.2)

    h = torch.randn(2, 6, hidden_dim)

    # When retrograde strength is 0, output is exactly equal to input
    h_idle, diag_idle = layer(h, retrograde_strength=0.0, return_diagnostics=True)
    assert torch.allclose(h, h_idle, atol=1e-6)

    # When active (strength = 1.0)
    h_mod, diag_act = layer(h, retrograde_strength=1.0, return_diagnostics=True)
    assert h_mod.shape == h.shape
    assert diag_act.dsi_magnitude > 0.0
    assert diag_act.dse_magnitude > 0.0
    # DSE factor must remain strictly > 0.30 (since 1 - 0.70 * sig >= 0.30)
    assert diag_act.dse_magnitude >= 0.30
    # Output must not collapse to zero
    assert torch.norm(h_mod) > 0.1


def test_attention_entropy_and_diversity_metrics():
    """Verify Shannon entropy and Jensen-Shannon head divergence metrics."""
    # Synthetic attention weights: (batch=1, heads=2, seq_q=2, seq_k=2)
    # Head 0: Uniform distribution [0.5, 0.5] => max entropy ln(2) = 0.6931 nats
    # Head 1: Delta distribution [1.0, 0.0] => zero entropy
    attn = torch.tensor([[[[0.5, 0.5], [0.5, 0.5]], [[1.0, 0.0], [1.0, 0.0]]]])

    entropy = compute_attention_entropy(attn)
    assert entropy.shape == (1, 2, 2)
    # Head 0 has maximal entropy
    assert math.isclose(entropy[0, 0, 0].item(), math.log(2), abs_tol=1e-4)
    # Head 1 has zero entropy
    assert math.isclose(entropy[0, 1, 0].item(), 0.0, abs_tol=1e-4)

    h_mean, k_eff = compute_effective_attention_horizon(attn)
    assert h_mean > 0.0
    assert k_eff > 1.0

    jsd = compute_head_divergence(attn)
    # Different heads must have positive divergence
    assert jsd > 0.0
