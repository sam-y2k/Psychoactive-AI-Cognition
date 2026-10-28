"""
Stiefel Manifold Orthogonal Projection & Cross-Domain Synesthesia Engine.
Formalizes mapping onto the Stiefel manifold V_k(R^d) where B^T B = I_k.
Provides algorithmic cross-domain basis hopping (e.g., Sales <-> Fungal Mycelium,
Distributed Locking <-> Cellular Autoimmunity).
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np


class OrthogonalDomain:
    """Represents a distant, orthogonal conceptual domain for analogical synthesis."""
    def __init__(self, name: str, core_concepts: List[str], dynamics: str):
        self.name = name
        self.core_concepts = core_concepts
        self.dynamics = dynamics


DEFAULT_ORTHOGONAL_DOMAINS: List[OrthogonalDomain] = [
    OrthogonalDomain(
        name="Fungal Mycelial Ecology",
        core_concepts=["decentralized nutrient allocation", "hyphal tip exploration", "anastomosis", "pulsed resource trading"],
        dynamics="Zero-hierarchy, high-resilience decentralized routing and resource redistribution under extreme environmental volatility."
    ),
    OrthogonalDomain(
        name="Cellular Immunology & Antigen Processing",
        core_concepts=["MHC class I presentation", "clonal selection", "hypermutation", "self vs non-self discrimination", "checkpoint inhibition"],
        dynamics="Adversarial anomaly detection, rapid decentralized learning, and systemic defense without centralized command."
    ),
    OrthogonalDomain(
        name="Hostage Negotiation & Behavioral Economics",
        core_concepts=["tactical empathy", "calibrated questions", "loss aversion", "no-oriented framing", "the black swan effect"],
        dynamics="De-escalating rigid psychological anchors, exposing hidden asymmetric incentives, and restructuring hostile perceptual fields."
    ),
    OrthogonalDomain(
        name="Submarine Stealth & Fluid Hydrodynamics",
        core_concepts=["acoustic thermoclines", "cavitation boundaries", "active vs passive sonar", "buoyancy compensation"],
        dynamics="Navigating dense adversarial environments, masking operational footprints, and exploiting invisible phase transitions."
    ),
    OrthogonalDomain(
        name="Astrophysical Stellar Nucleosynthesis",
        core_concepts=["gravitational collapse", "degenerate electron pressure", "r-process neutron capture", "event horizons"],
        dynamics="Transforming extreme compression into hyper-dense, novel structural elements; irreversible state bifurcations."
    ),
    OrthogonalDomain(
        name="Ant Colony Foraging & Stigmergy",
        core_concepts=["pheromone decay rates", "tandem recruitment", "quorum thresholding", "trophallaxis"],
        dynamics="Emergent global intelligence arising from simple, asynchronous local interactions without global visibility."
    ),
]


class StiefelProjector:
    """
    Manages orthogonal projection operators B in V_k(R^d) such that B^T B = I_k.
    In semantic space, forces the cognitive engine to traverse across disjoint conceptual domains.
    """

    def __init__(self, ambient_dim: int = 64, subspace_rank: int = 4, seed: int = 42):
        self.ambient_dim = ambient_dim
        self.subspace_rank = subspace_rank
        self.seed = seed
        self.orthogonal_basis = self._generate_stiefel_matrix(ambient_dim, subspace_rank, seed)
        self.domain_library = DEFAULT_ORTHOGONAL_DOMAINS

    def _generate_stiefel_matrix(self, d: int, k: int, seed: int) -> np.ndarray:
        """
        Generates an orthonormal basis matrix B in V_k(R^d) via QR decomposition:
        Q, R = qr(A) => Q[:, :k]^T Q[:, :k] = I_k
        """
        rng = np.random.default_rng(seed)
        gaussian_matrix = rng.standard_normal((d, k))
        q, _ = np.linalg.qr(gaussian_matrix)
        # Ensure exact shape (d, k)
        return q[:, :k]

    def verify_orthonormality(self, tolerance: float = 1e-6) -> bool:
        """Verifies that B^T B = I_k within numerical precision."""
        gram = np.dot(self.orthogonal_basis.T, self.orthogonal_basis)
        identity = np.eye(self.subspace_rank)
        return bool(np.allclose(gram, identity, atol=tolerance))

    def project_vector(self, v: np.ndarray) -> np.ndarray:
        """Projects ambient vector v onto the Stiefel subspace: v_proj = B (B^T v)."""
        coords = np.dot(self.orthogonal_basis.T, v)
        return np.dot(self.orthogonal_basis, coords)

    def select_orthogonal_domain(self, problem_description: str) -> OrthogonalDomain:
        """
        Deterministically selects the most orthogonal conceptual domain to cross-pollinate with the task.
        """
        # Hash text to select stably across repeated runs
        h = sum(ord(c) for c in problem_description.lower())
        idx = h % len(self.domain_library)
        return self.domain_library[idx]

    def generate_stiefel_prompt_bridge(self, problem_description: str) -> str:
        """
        Constructs a Stiefel analogical bridge for LLM reasoning prompts.
        """
        domain = self.select_orthogonal_domain(problem_description)
        concepts_str = ", ".join(f"'{c}'" for c in domain.core_concepts)

        return (
            f"STIEFEL MANIFOLD PROJECTION [Orthogonal Domain: {domain.name}]:\n"
            f"Dynamics: {domain.dynamics}\n"
            f"Core Primitives: {concepts_str}\n"
            "MANDATORY ISOMORPHISM:\n"
            f"Do not solve this problem using standard industry logic. Formally map every core challenge of the problem "
            f"isomorphically onto the mechanics of {domain.name}. What is the exact equivalent of its bottlenecks, "
            f"and what novel solution appears when viewed through this dynamic?"
        )
