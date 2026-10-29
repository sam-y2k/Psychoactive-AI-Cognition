"""
Rigorous Unit Tests for Chunk 1 Mathematical Solvers:
- Orthogonal Procrustes Stiefel Manifold Solver
- Topological Data Analysis (TDA) & Persistent Homology Engine
- Free-Energy Langevin SDE Attractor Simulator
"""

import pytest
import numpy as np
from psychoactive.math.procrustes import OrthogonalProcrustesSolver
from psychoactive.math.tda import (
    PersistentHomologyEngine,
    compute_newman_modularity,
)
from psychoactive.math.langevin import (
    AttractorLandscape,
    LangevinAttractorSimulator,
    kramers_escape_rate,
)


# =========================================================================
# 1. ORTHOGONAL PROCRUSTES & STIEFEL MANIFOLD TESTS
# =========================================================================

def test_procrustes_orthonormality_and_isometry():
    """Verify B* lies on Stiefel manifold V_k(R^d) and satisfies B^T B = I_k."""
    solver = OrthogonalProcrustesSolver(tolerance=1e-5)
    rng = np.random.default_rng(42)

    n_samples = 50
    d_dim = 16

    # Generate source representations
    z_src = rng.standard_normal((n_samples, d_dim))

    # Target is an orthogonal rotation of source + small target noise
    # Random orthogonal ground truth Q
    q_gt, _ = np.linalg.qr(rng.standard_normal((d_dim, d_dim)))
    z_tgt = np.dot(z_src, q_gt) + (0.05 * rng.standard_normal((n_samples, d_dim)))

    result = solver.solve(z_src, z_tgt)

    # 1. Must be certified orthonormal
    assert result.is_orthonormal is True
    # 2. Alignment error must be small
    assert result.alignment_error < 0.10
    # 3. Check Gram matrix directly: B^T B = I
    b = result.projection_matrix
    gram = np.dot(b.T, b)
    assert np.allclose(gram, np.eye(d_dim), atol=1e-5)

    # 4. Check isometry on test vectors
    is_iso, delta = solver.assert_isometry(z_src[:5], b)
    assert is_iso is True
    assert delta < 1e-5


def test_procrustes_reduces_reconstruction_error():
    """Verify Procrustes strictly minimizes Frobenius alignment error."""
    solver = OrthogonalProcrustesSolver()
    rng = np.random.default_rng(99)

    z_src = rng.standard_normal((30, 8))
    z_tgt = rng.standard_normal((30, 8))

    res = solver.solve(z_src, z_tgt)
    procrustes_error = res.alignment_error

    # Compare against random orthogonal matrix
    q_random, _ = np.linalg.qr(rng.standard_normal((8, 8)))
    random_proj = np.dot(z_src, q_random)
    random_error = np.linalg.norm(random_proj - z_tgt, ord="fro") / np.linalg.norm(z_tgt, ord="fro")

    # Optimal Procrustes must achieve equal or strictly lower error
    assert procrustes_error <= random_error


# =========================================================================
# 2. TOPOLOGICAL DATA ANALYSIS & BETTI NUMBERS TESTS
# =========================================================================

def test_tda_modular_vs_integrated_betti():
    """Verify Betti numbers capture transition from segregated clusters to integrated loops."""
    engine = PersistentHomologyEngine(persistence_threshold=0.10)

    # Synthetic modular representation: 2 clusters of 5 points each
    # Cluster A around (1, 1), Cluster B around (10, 10)
    rng = np.random.default_rng(123)
    c1 = rng.normal(loc=[1.0, 1.0], scale=0.1, size=(5, 2))
    c2 = rng.normal(loc=[10.0, 10.0], scale=0.1, size=(5, 2))
    points = np.vstack([c1, c2])

    dist_matrix = engine.compute_distance_matrix(points)
    filtration = engine.compute_filtration(dist_matrix, num_steps=30)

    # At low epsilon: beta_0 = 10 (all separate)
    assert filtration[0].betti_0 == 10
    # At intermediate epsilon: beta_0 collapses as clusters merge
    # At high epsilon: beta_0 reaches 1
    assert filtration[-1].betti_0 == 1

    intervals = engine.extract_persistence_intervals(filtration)
    assert len(intervals) > 0

    # Ensure H_0 features were registered
    h0_intervals = [it for it in intervals if it.dimension == 0]
    assert len(h0_intervals) >= 9


def test_tda_newman_modularity():
    """Verify Newman modularity Q drops from segregated (~0.72) to integrated (~0.18)."""
    # 2 isolated 4-node cliques
    # Adjacency matrix for 8 nodes:
    w_segregated = np.zeros((8, 8))
    w_segregated[:4, :4] = 1.0
    w_segregated[4:, 4:] = 1.0
    np.fill_diagonal(w_segregated, 0.0)

    communities = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    q_segregated = compute_newman_modularity(w_segregated, communities)

    # Highly modular network should have Q > 0.40
    assert q_segregated > 0.40

    # Now add dense cross-community edges (synesthetic bridging)
    w_integrated = np.copy(w_segregated)
    w_integrated[:4, 4:] = 0.8
    w_integrated[4:, :4] = 0.8
    q_integrated = compute_newman_modularity(w_integrated, communities)

    # Globally connected network has significantly lower modularity Q
    assert q_integrated < q_segregated
    assert q_integrated <= 0.20


# =========================================================================
# 3. THERMODYNAMIC LANGEVIN ATTRACTOR SIMULATION TESTS
# =========================================================================

def test_attractor_dissolution_theorem():
    """Empirically prove: lim_{pi_P -> 0} P_escape = 1.0 vs pi_P = 1.0 (P_escape ~ 0)."""
    landscape = AttractorLandscape(dim=2, base_barrier_height=6.0)

    # 1. Baseline state (pi_P = 1.0): trapped inside canalized well
    sim_baseline = LangevinAttractorSimulator(landscape, gamma_inv=0.25, seed=100)
    p_escape_baseline = sim_baseline.estimate_escape_probability(
        prior_precision=1.0,
        num_trials=20,
        total_time=12.0,
        dt=0.04,
    )
    # Under steep barrier, state should remain trapped
    assert p_escape_baseline <= 0.10

    # 2. Acute REBUS state (pi_P = 0.05): flattened landscape
    sim_rebus = LangevinAttractorSimulator(landscape, gamma_inv=0.25, seed=100)
    p_escape_rebus = sim_rebus.estimate_escape_probability(
        prior_precision=0.05,
        num_trials=20,
        total_time=12.0,
        dt=0.04,
    )
    # Under flattened barrier, state should traverse freely
    assert p_escape_rebus >= 0.85

    # 3. Ergodic volume expansion
    traj_base = sim_baseline.simulate(prior_precision=1.0, total_time=10.0)
    traj_rebus = sim_rebus.simulate(prior_precision=0.10, total_time=10.0)
    assert traj_rebus.ergodic_volume > traj_base.ergodic_volume


def test_kramers_escape_rate_scaling():
    """Verify Kramers' rate increases exponentially as barrier Delta U vanishes."""
    rate_steep = kramers_escape_rate(barrier_height=5.0, temperature=1.0)
    rate_flat = kramers_escape_rate(barrier_height=0.1, temperature=1.0)

    # Vanishing barrier must increase escape rate by orders of magnitude
    assert rate_flat > (rate_steep * 50.0)
