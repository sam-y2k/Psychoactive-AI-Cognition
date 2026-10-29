"""
Pure Mathematical Solvers for Psychoactive Cognitive Dynamics.
Includes:
- Orthogonal Procrustes Stiefel Manifold Solver
- Topological Data Analysis (TDA) & Persistent Homology Engine
- Free-Energy Thermodynamic SDE Attractor Simulator
"""

from psychoactive.math.procrustes import OrthogonalProcrustesSolver, StiefelResult
from psychoactive.math.tda import (
    PersistentHomologyEngine,
    SimplicialFiltration,
    PersistenceInterval,
    compute_newman_modularity,
)
from psychoactive.math.langevin import (
    LangevinAttractorSimulator,
    AttractorLandscape,
    LangevinTrajectory,
    kramers_escape_rate,
)

__all__ = [
    "OrthogonalProcrustesSolver",
    "StiefelResult",
    "PersistentHomologyEngine",
    "SimplicialFiltration",
    "PersistenceInterval",
    "compute_newman_modularity",
    "LangevinAttractorSimulator",
    "AttractorLandscape",
    "LangevinTrajectory",
    "kramers_escape_rate",
]
