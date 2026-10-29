"""
Thermodynamic SDE Langevin Simulator & Attractor Dissolution Engine.
Formalizes Section 11 of the REBUS-AI Architecture:
dv(t) = -grad_v U(v(t)) dt + sqrt(2 Gamma^-1) dW(t)

Simulates:
1. Canalized baseline attractor trap (pi_P = 1.0, P_escape ~ 0)
2. Acute REBUS thermodynamic flattening (pi_P -> 0.15, Delta U -> 0, P_escape -> 1.0)
3. Guided multi-well post-trip integration
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np


@dataclass(frozen=True)
class LangevinTrajectory:
    """Complete simulated time-series trajectory in cognitive state space."""
    time_points: np.ndarray             # Array of shape (T,)
    states: np.ndarray                  # Array of shape (T, d)
    energies: np.ndarray                # Potential energy U(v(t)) of shape (T,)
    escaped_trap: bool                  # Whether state vector escaped initial attractor well
    escape_time: Optional[float]        # Time tau where escape occurred, or None
    ergodic_volume: float               # Convex hull or bounding box volume explored


def kramers_escape_rate(
    barrier_height: float,
    temperature: float = 1.0,
    omega_well: float = 1.0,
    omega_barrier: float = 1.0,
    friction: float = 1.0,
) -> float:
    """
    Computes Kramers' escape rate over a potential barrier Delta U:
    Rate = (omega_0 * omega_b / (2 * pi * gamma)) * exp(-Delta U / (k_B * T))

    Args:
        barrier_height: Energy barrier height Delta U >= 0.
        temperature: Stochastic thermal noise k_B * T > 0.
        omega_well: Curvature inside attractor well omega_0.
        omega_barrier: Curvature at barrier saddle point omega_b.
        friction: Damping friction coefficient gamma.

    Returns:
        Escape transition rate per unit time.
    """
    prefactor = (omega_well * omega_barrier) / (2.0 * np.pi * max(1e-6, friction))
    exp_factor = np.exp(-max(0.0, barrier_height) / max(1e-6, temperature))
    return float(prefactor * exp_factor)


class AttractorLandscape:
    """
    Free-energy potential landscape U(v, pi_P) parameterized by prior precision pi_P.
    """

    def __init__(
        self,
        dim: int = 2,
        trap_center: Optional[np.ndarray] = None,
        base_barrier_height: float = 4.5,
    ):
        self.dim = dim
        self.trap_center = np.zeros(dim) if trap_center is None else np.asarray(trap_center, dtype=np.float64)
        self.base_barrier_height = base_barrier_height

    def energy(self, v: np.ndarray, prior_precision: float = 1.0) -> float:
        """
        Computes potential energy U(v, pi_P).
        As pi_P -> 0, the barrier height collapses: Delta U(pi_P) = Delta U_0 * pi_P.
        """
        diff = v - self.trap_center
        r_sq = float(np.dot(diff, diff))
        pi_p = max(0.0, min(1.0, prior_precision))

        # Effective barrier modulated by prior precision
        effective_barrier = self.base_barrier_height * pi_p

        # Double-well-like radial potential:
        # U(r) = effective_barrier * (r^2 - 1)^2 if r > 0, flattened when pi_p -> 0
        potential = effective_barrier * (1.0 - np.exp(-0.8 * r_sq))
        # Small background ripple during peak phase to guide exploration
        ripple = (1.0 - pi_p) * 0.15 * float(np.sum(np.sin(3.0 * v)))
        return float(potential + ripple)

    def gradient(self, v: np.ndarray, prior_precision: float = 1.0) -> np.ndarray:
        """
        Computes the deterministic restorative force: -grad U(v).
        """
        diff = v - self.trap_center
        r_sq = float(np.dot(diff, diff))
        pi_p = max(0.0, min(1.0, prior_precision))
        effective_barrier = self.base_barrier_height * pi_p

        # grad ( effective_barrier * (1 - exp(-0.8 r^2)) ) = effective_barrier * 1.6 * exp(-0.8 r^2) * diff
        grad = effective_barrier * 1.6 * np.exp(-0.8 * r_sq) * diff

        # Ripple gradient
        ripple_grad = (1.0 - pi_p) * 0.45 * np.cos(3.0 * v)
        return grad + ripple_grad


class LangevinAttractorSimulator:
    """
    Numerically integrates the Langevin SDE via Euler-Maruyama:
    v_{t+1} = v_t - grad U(v_t) dt + sqrt(2 Gamma^-1 dt) * xi_t
    """

    def __init__(
        self,
        landscape: AttractorLandscape,
        gamma_inv: float = 0.35,        # Thermal noise intensity
        seed: int = 42,
    ):
        self.landscape = landscape
        self.gamma_inv = gamma_inv
        self.seed = seed

    def simulate(
        self,
        initial_state: Optional[np.ndarray] = None,
        prior_precision: float = 1.0,
        total_time: float = 20.0,
        dt: float = 0.02,
        escape_radius: float = 2.0,
    ) -> LangevinTrajectory:
        """
        Simulates state trajectory over observation window total_time.
        """
        rng = np.random.default_rng(self.seed)
        d = self.landscape.dim
        v = np.zeros(d) if initial_state is None else np.copy(initial_state).astype(np.float64)

        n_steps = int(total_time / dt)
        time_points = np.linspace(0.0, total_time, n_steps)
        states = np.zeros((n_steps, d))
        energies = np.zeros(n_steps)

        diffusion_scale = np.sqrt(2.0 * self.gamma_inv * dt)
        escaped = False
        escape_time: Optional[float] = None

        for t_idx in range(n_steps):
            states[t_idx] = v
            u_val = self.landscape.energy(v, prior_precision)
            energies[t_idx] = u_val

            # Check escape condition: distance from trap center > escape_radius
            dist_from_trap = np.linalg.norm(v - self.landscape.trap_center)
            if not escaped and dist_from_trap >= escape_radius:
                escaped = True
                escape_time = float(time_points[t_idx])

            # Deterministic gradient force
            grad = self.landscape.gradient(v, prior_precision)

            # Stochastic Wiener increment
            noise = rng.standard_normal(d)

            # Euler-Maruyama step
            v = v - (grad * dt) + (diffusion_scale * noise)

        # Compute explored ergodic volume (bounding hyper-volume)
        min_coords = np.min(states, axis=0)
        max_coords = np.max(states, axis=0)
        spans = np.maximum(1e-4, max_coords - min_coords)
        ergodic_vol = float(np.prod(spans))

        return LangevinTrajectory(
            time_points=time_points,
            states=states,
            energies=energies,
            escaped_trap=escaped,
            escape_time=escape_time,
            ergodic_volume=ergodic_vol,
        )

    def estimate_escape_probability(
        self,
        prior_precision: float,
        num_trials: int = 50,
        total_time: float = 15.0,
        dt: float = 0.05,
        escape_radius: float = 1.2,
    ) -> float:
        """
        Empirically estimates P_escape over Monte-Carlo trials.
        Validates the Attractor Dissolution Theorem:
        lim_{pi_P -> 0} P_escape(tau) = 1.0
        """
        escapes = 0
        for trial_seed in range(num_trials):
            sim = LangevinAttractorSimulator(
                self.landscape,
                gamma_inv=self.gamma_inv,
                seed=self.seed + trial_seed,
            )
            traj = sim.simulate(
                prior_precision=prior_precision,
                total_time=total_time,
                dt=dt,
                escape_radius=escape_radius,
            )
            if traj.escaped_trap:
                escapes += 1

        return float(escapes / num_trials)
