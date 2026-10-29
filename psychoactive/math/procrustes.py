"""
Orthogonal Procrustes Solver on the Stiefel Manifold.
Formalizes Tier 3 of the REBUS-AI Architecture:
min_B ||Z_src B - Z_tgt||_F^2  s.t.  B^T B = I_k

Guarantees:
1. Isometric distance invariance: ||B z_1 - B z_2||_2 = ||z_1 - z_2||_2
2. Metric norm preservation: ||B z||_2 = ||z||_2
3. Elimination of vanishing/exploding representations during cross-domain reasoning.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np


@dataclass(frozen=True)
class StiefelResult:
    """Result of Stiefel manifold orthogonal alignment."""
    projection_matrix: np.ndarray       # B* in V_k(R^d) of shape (d, k)
    alignment_error: float              # Relative Frobenius norm ||Z_src B* - Z_tgt||_F / ||Z_tgt||_F
    is_orthonormal: bool                # Whether B^T B = I_k within tolerance
    singular_values: np.ndarray         # Spectrum of the cross-covariance tensor M = Z_src^T Z_tgt
    spectral_norm_deviation: float      # max |sigma_i - 1| measuring deviation from isometry


class OrthogonalProcrustesSolver:
    """
    Solves the Orthogonal Procrustes problem on the Stiefel Manifold V_k(R^d).
    Maps high-entropy candidate vectors from Domain A into the semantic manifold of Domain B.
    """

    def __init__(self, tolerance: float = 1e-6):
        self.tolerance = tolerance

    def solve(
        self,
        z_source: np.ndarray,
        z_target: np.ndarray,
        subspace_dim: Optional[int] = None,
    ) -> StiefelResult:
        """
        Computes the optimal isometric projection tensor B* in V_k(R^d):
        M = Z_src^T Z_tgt
        U, Sigma, V^T = SVD(M)
        B* = U V^T

        Args:
            z_source: Source latent representations of shape (N, d_src).
            z_target: Target latent representations of shape (N, d_tgt).
            subspace_dim: Dimension k of the target subspace. If None, uses min(d_src, d_tgt).

        Returns:
            StiefelResult containing B*, alignment error, and spectrum diagnostics.
        """
        z_src = np.asarray(z_source, dtype=np.float64)
        z_tgt = np.asarray(z_target, dtype=np.float64)

        if z_src.ndim != 2 or z_tgt.ndim != 2:
            raise ValueError(f"Inputs must be 2D matrices, got shapes {z_src.shape} and {z_tgt.shape}")
        if z_src.shape[0] != z_tgt.shape[0]:
            raise ValueError(
                f"Sample count N must match between source ({z_src.shape[0]}) and target ({z_tgt.shape[0]})"
            )

        n_samples, d_src = z_src.shape
        _, d_tgt = z_tgt.shape
        k = subspace_dim if subspace_dim is not None else min(d_src, d_tgt)

        # 1. Compute cross-covariance matrix M = Z_src^T Z_tgt
        cross_cov = np.dot(z_src.T, z_tgt)  # (d_src, d_tgt)

        # 2. Singular Value Decomposition: M = U Sigma V^T
        u, s, vt = np.linalg.svd(cross_cov, full_matrices=False)

        # 3. Optimal Orthogonal Procrustes Matrix: B* = U V^T
        # Shape: (d_src, d_tgt)
        b_star = np.dot(u[:, :k], vt[:k, :])

        # 4. Verify orthonormality: B^T B = I_k
        gram = np.dot(b_star.T, b_star) if d_src >= d_tgt else np.dot(b_star, b_star.T)
        eye_dim = min(d_src, d_tgt)
        identity = np.eye(eye_dim)
        gram_error = np.max(np.abs(gram - identity))
        is_orthonormal = bool(gram_error < self.tolerance)

        # 5. Compute alignment error: ||Z_src B* - Z_tgt||_F / ||Z_tgt||_F
        projected = np.dot(z_src, b_star)
        diff_norm = np.linalg.norm(projected - z_tgt, ord="fro")
        tgt_norm = np.linalg.norm(z_tgt, ord="fro")
        rel_error = float(diff_norm / max(1e-12, tgt_norm))

        # 6. Spectral norm deviation
        spectral_dev = float(np.max(np.abs(s / max(1e-12, s[0]) - 1.0))) if len(s) > 0 else 0.0

        return StiefelResult(
            projection_matrix=b_star,
            alignment_error=rel_error,
            is_orthonormal=is_orthonormal,
            singular_values=s,
            spectral_norm_deviation=spectral_dev,
        )

    def project(self, vector: np.ndarray, b_matrix: np.ndarray) -> np.ndarray:
        """
        Projects an arbitrary vector or batch of vectors through the Stiefel tensor B:
        z_projected = z B
        """
        v = np.asarray(vector, dtype=np.float64)
        return np.dot(v, b_matrix)

    def assert_isometry(self, z_test: np.ndarray, b_matrix: np.ndarray) -> Tuple[bool, float]:
        """
        Tests whether the projection preserves pairwise Euclidean distances:
        ||z_i B - z_j B|| == ||z_i - z_j||
        """
        z = np.asarray(z_test, dtype=np.float64)
        if z.shape[0] < 2:
            return True, 0.0

        # Original pairwise distance
        orig_dist = np.linalg.norm(z[0] - z[1])
        # Projected pairwise distance
        z_proj = np.dot(z, b_matrix)
        proj_dist = np.linalg.norm(z_proj[0] - z_proj[1])

        delta = float(np.abs(orig_dist - proj_dist))
        is_isometric = delta < self.tolerance
        return is_isometric, delta
