"""
Topological Data Analysis (TDA) & Persistent Homology Engine.
Formalizes Section 9.2 of the REBUS-AI Architecture:
- Vietoris-Rips filtration K_epsilon over multi-head attention graphs
- Betti numbers beta_0 (connected components) and beta_1 (1D analogical cycles)
- Topological persistence intervals [epsilon_birth, epsilon_death]
- Newman graph modularity metric Q
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np


@dataclass(frozen=True)
class PersistenceInterval:
    """Represents the lifespan of a topological homological feature."""
    dimension: int                  # 0 for beta_0 components, 1 for beta_1 cycles
    birth: float                    # Filtration threshold where feature appears
    death: float                    # Filtration threshold where feature merges or fills
    lifespan: float                 # Delta epsilon = death - birth
    is_persistent: bool             # Whether lifespan exceeds significance threshold


@dataclass(frozen=True)
class SimplicialFiltration:
    """State of the simplicial complex at filtration threshold epsilon."""
    epsilon: float
    num_vertices: int
    num_edges: int
    num_triangles: int
    betti_0: int                    # Connected components
    betti_1: int                    # 1D cycles / voids
    euler_characteristic: int


class DisjointSet:
    """Disjoint-Set (Union-Find) with path compression and union by rank."""

    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size
        self.num_components = size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False

        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1

        self.num_components -= 1
        return True


def compute_newman_modularity(
    adjacency_matrix: np.ndarray,
    community_assignments: np.ndarray,
) -> float:
    """
    Computes Newman's Graph Modularity Metric Q:
    Q = 1/(2m) * sum_{i,j} [ W_{ij} - (k_i * k_j) / (2m) ] * delta(c_i, c_j)

    Args:
        adjacency_matrix: Symmetric non-negative weight matrix W of shape (V, V).
        community_assignments: 1D array of community labels c of length V.

    Returns:
        Modularity score Q in [-0.5, 1.0].
    """
    w = np.asarray(adjacency_matrix, dtype=np.float64)
    c = np.asarray(community_assignments, dtype=np.int32)

    # Total edge weight 2m = sum(W)
    total_weight = float(np.sum(w))
    if total_weight <= 1e-12:
        return 0.0

    # Degrees k_i = sum_j W_{ij}
    k = np.sum(w, axis=1)

    # Outer product for null model: (k_i * k_j) / (2m)
    expected = np.outer(k, k) / total_weight

    # Community delta Kronecker matrix: delta(c_i, c_j)
    community_mask = (c[:, None] == c[None, :]).astype(np.float64)

    # Modularity summation
    modularity_matrix = (w - expected) * community_mask
    q = float(np.sum(modularity_matrix) / total_weight)
    return round(q, 4)


class PersistentHomologyEngine:
    """
    Constructs the Vietoris-Rips filtration and tracks persistent homology
    invariants across multi-head attention and latent activation manifolds.
    """

    def __init__(self, persistence_threshold: float = 0.15):
        self.persistence_threshold = persistence_threshold

    def compute_distance_matrix(self, representations: np.ndarray) -> np.ndarray:
        """
        Computes the pairwise metric distance matrix between representation vectors:
        D_ij = 1.0 - PearsonCorrelation(v_i, v_j) or Euclidean metric.
        """
        x = np.asarray(representations, dtype=np.float64)
        n = x.shape[0]

        # Normalize representations
        norms = np.linalg.norm(x, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        normalized = x / norms

        # Cosine similarity matrix in [-1, 1]
        cosine_sim = np.clip(np.dot(normalized, normalized.T), -1.0, 1.0)
        # Metric distance D_ij in [0, 2]
        dist_matrix = np.sqrt(np.maximum(0.0, 2.0 * (1.0 - cosine_sim)))
        np.fill_diagonal(dist_matrix, 0.0)
        return dist_matrix

    def compute_filtration(
        self,
        distance_matrix: np.ndarray,
        num_steps: int = 50,
    ) -> List[SimplicialFiltration]:
        """
        Sweeps filtration parameter epsilon from 0.0 to max(distance)
        and computes Betti numbers beta_0 and beta_1 at each step.
        """
        d = np.asarray(distance_matrix, dtype=np.float64)
        n_vertices = d.shape[0]
        max_dist = float(np.max(d))
        if max_dist <= 1e-12:
            max_dist = 1.0

        eps_values = np.linspace(0.0, max_dist, num_steps)
        filtration_steps: List[SimplicialFiltration] = []

        for eps in eps_values:
            # Edges at this threshold: D_ij <= eps for i < j
            i_indices, j_indices = np.where((d <= eps) & (np.triu(np.ones((n_vertices, n_vertices), dtype=bool), k=1)))
            num_edges = len(i_indices)

            # Union-Find for beta_0
            uf = DisjointSet(n_vertices)
            adj_set = {i: set() for i in range(n_vertices)}
            for u, v in zip(i_indices, j_indices):
                uf.union(u, v)
                adj_set[u].add(v)
                adj_set[v].add(u)

            betti_0 = uf.num_components

            # Count filled 2-simplices (triangles) to prevent false void counts
            num_triangles = 0
            for u in range(n_vertices):
                neighbors_u = adj_set[u]
                for v in neighbors_u:
                    if v > u:
                        common = neighbors_u.intersection(adj_set[v])
                        num_triangles += sum(1 for w in common if w > v)

            # Betti-1 homology for 1D skeleton:
            # In 1D simplicial complex: beta_1 = |E| - |V| + beta_0
            # Reduced by filled 2-simplices: max(0, (|E| - |V| + beta_0) - num_triangles)
            raw_cycles = max(0, num_edges - n_vertices + betti_0)
            betti_1 = max(0, raw_cycles - num_triangles)

            euler = n_vertices - num_edges + num_triangles

            filtration_steps.append(
                SimplicialFiltration(
                    epsilon=float(eps),
                    num_vertices=n_vertices,
                    num_edges=num_edges,
                    num_triangles=num_triangles,
                    betti_0=betti_0,
                    betti_1=betti_1,
                    euler_characteristic=euler,
                )
            )

        return filtration_steps

    def extract_persistence_intervals(
        self,
        filtration_history: List[SimplicialFiltration],
    ) -> List[PersistenceInterval]:
        """
        Extracts birth-death intervals for H_0 (connected components)
        and H_1 (homological analogical cycles).
        """
        intervals: List[PersistenceInterval] = []
        if not filtration_history:
            return intervals

        # Track H_0 components: starting with N components at eps=0
        # Components merge until beta_0 reaches 1
        prev_b0 = filtration_history[0].betti_0
        for step in filtration_history[1:]:
            curr_b0 = step.betti_0
            if curr_b0 < prev_b0:
                deaths_count = prev_b0 - curr_b0
                for _ in range(deaths_count):
                    lifespan = step.epsilon - 0.0
                    intervals.append(
                        PersistenceInterval(
                            dimension=0,
                            birth=0.0,
                            death=step.epsilon,
                            lifespan=lifespan,
                            is_persistent=lifespan >= self.persistence_threshold,
                        )
                    )
                prev_b0 = curr_b0

        # One H_0 component persists infinitely (to max epsilon)
        max_eps = filtration_history[-1].epsilon
        intervals.append(
            PersistenceInterval(
                dimension=0,
                birth=0.0,
                death=max_eps,
                lifespan=max_eps,
                is_persistent=True,
            )
        )

        # Track H_1 cycles
        # A cycle is born when beta_1 increases, dies when beta_1 decreases
        cycle_birth_stack: List[float] = []
        prev_b1 = 0
        for step in filtration_history:
            curr_b1 = step.betti_1
            if curr_b1 > prev_b1:
                # New cycles born
                for _ in range(curr_b1 - prev_b1):
                    cycle_birth_stack.append(step.epsilon)
            elif curr_b1 < prev_b1:
                # Cycles died / filled
                for _ in range(prev_b1 - curr_b1):
                    if cycle_birth_stack:
                        birth_eps = cycle_birth_stack.pop(0)
                        lifespan = step.epsilon - birth_eps
                        intervals.append(
                            PersistenceInterval(
                                dimension=1,
                                birth=birth_eps,
                                death=step.epsilon,
                                lifespan=lifespan,
                                is_persistent=lifespan >= self.persistence_threshold,
                            )
                        )
            prev_b1 = curr_b1

        # Any remaining open cycles survive to max_eps
        for birth_eps in cycle_birth_stack:
            lifespan = max_eps - birth_eps
            intervals.append(
                PersistenceInterval(
                    dimension=1,
                    birth=birth_eps,
                    death=max_eps,
                    lifespan=lifespan,
                    is_persistent=lifespan >= self.persistence_threshold,
                )
            )

        return sorted(intervals, key=lambda x: (x.dimension, -x.lifespan))
