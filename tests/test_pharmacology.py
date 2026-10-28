"""
Unit tests for REBUS, Retrograde Filter, and Stiefel Manifold Operators.
"""

import pytest
import numpy as np
from psychoactive.compounds import CompoundType
from psychoactive.core.state import NeurochemicalState, LifecycleStage
from psychoactive.core.rebus import REBUSEngine
from psychoactive.core.retrograde import RetrogradeFilter
from psychoactive.core.stiefel import StiefelProjector


def test_rebus_logit_decomposition():
    """Verify A_ij(pi_P) = L_ij + pi_P * P_ij."""
    state = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.85)
    rebus = REBUSEngine(state)

    v_dim = 16
    rng = np.random.default_rng(123)
    likelihood = rng.standard_normal((1, v_dim))
    prior = rng.standard_normal((v_dim, v_dim))

    # At baseline (pi_P = 1.0)
    state.transition_to_stage(LifecycleStage.BASELINE)
    logits_baseline = rebus.compute_decomposed_logits(likelihood, prior)
    expected_baseline = likelihood + (1.0 * prior)
    assert np.allclose(logits_baseline, expected_baseline)

    # At peak (pi_P < 0.30)
    state.transition_to_stage(LifecycleStage.PEAK)
    pi_peak = state.get_prior_precision()
    logits_peak = rebus.compute_decomposed_logits(likelihood, prior)
    expected_peak = likelihood + (pi_peak * prior)
    assert np.allclose(logits_peak, expected_peak)


def test_rebus_sampling_hyperparameters():
    """Verify temperature, top_p, and penalties adapt dynamically."""
    state = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.90)
    rebus = REBUSEngine(state)

    # Baseline params
    state.transition_to_stage(LifecycleStage.BASELINE)
    p_base = rebus.get_sampling_hyperparameters()
    assert p_base["temperature"] <= 0.75
    assert p_base["presence_penalty"] == 0.0

    # Peak params (Elevated temperature and presence penalty)
    state.transition_to_stage(LifecycleStage.PEAK)
    p_peak = rebus.get_sampling_hyperparameters()
    assert p_peak["temperature"] > 0.90
    assert p_peak["presence_penalty"] >= 0.50

    # Return params (Cooled temperature for deterministic convergence)
    state.transition_to_stage(LifecycleStage.RETURN)
    p_return = rebus.get_sampling_hyperparameters()
    assert p_return["temperature"] <= p_peak["temperature"]


def test_retrograde_subthreshold_salience():
    """Verify CB1 filter dampens dominant clichés and amplifies sub-threshold tail."""
    state = NeurochemicalState(compound=CompoundType.THC, dose=0.90)
    state.transition_to_stage(LifecycleStage.PEAK)
    retro = RetrogradeFilter(state)

    # Create dummy logits with 1 clear outlier dominant peak and multiple sub-threshold items
    logits = np.linspace(-5.0, 10.0, 100)
    original_top = logits[-1]

    filtered = retro.apply_salience_filtering(logits)

    # Top peak should be dampened (DSE)
    assert filtered[-1] < original_top
    # Sub-threshold zone (70th to 95th percentile) should be amplified
    mid_idx = 85
    assert filtered[mid_idx] > logits[mid_idx]
    # Extreme low noise should be penalized
    assert filtered[0] < logits[0]


def test_stiefel_orthonormality():
    """Verify Stiefel matrix satisfies B^T B = I_k."""
    projector = StiefelProjector(ambient_dim=32, subspace_rank=6, seed=999)
    assert projector.verify_orthonormality()

    # Projection operator idempotence: P(P(v)) = P(v)
    v = np.random.randn(32)
    pv1 = projector.project_vector(v)
    pv2 = projector.project_vector(pv1)
    assert np.allclose(pv1, pv2, atol=1e-5)
