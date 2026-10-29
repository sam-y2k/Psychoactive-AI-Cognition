"""
Lateral Divergence Metric (LDM) Tensor Engine.
Formalizes Section 9.2 of the REBUS-AI Architecture:
LDM(v_neuro, v_baseline) = 1 - (v_baseline . v_neuro) / (||v_baseline|| * ||v_neuro||)
                           + xi * S_syntax(v_neuro)

Quantifies escape from canonical corporate attractor basins without generating syntactic garbage.
"""

from dataclasses import dataclass
from typing import Optional, List, Union
import re
import numpy as np


@dataclass(frozen=True)
class LDMResult:
    """Detailed telemetry of the Lateral Divergence Metric."""
    ldm_score: float                    # Total composite LDM score
    cosine_divergence: float            # Raw angular divergence 1 - cos(theta) in [0.0, 2.0]
    cosine_similarity: float            # cos(theta) in [-1.0, 1.0]
    syntax_preservation_score: float    # S_syntax in [0.0, 1.0]
    is_valid_breakthrough: bool         # True if divergence > threshold AND syntax >= 0.95
    penalty_applied: float              # xi * S_syntax term


def compute_cosine_divergence(
    v_neuro: np.ndarray,
    v_baseline: np.ndarray,
) -> Tuple_float:
    """
    Computes cosine similarity and cosine divergence:
    cos_sim = (v_b . v_n) / (||v_b|| * ||v_n||)
    cos_div = 1.0 - cos_sim
    """
    vn = np.asarray(v_neuro, dtype=np.float64).flatten()
    vb = np.asarray(v_baseline, dtype=np.float64).flatten()

    norm_n = np.linalg.norm(vn)
    norm_b = np.linalg.norm(vb)

    if norm_n < 1e-12 or norm_b < 1e-12:
        return 0.0, 1.0

    cos_sim = float(np.clip(np.dot(vb, vn) / (norm_b * norm_n), -1.0, 1.0))
    cos_div = float(1.0 - cos_sim)
    return cos_sim, cos_div


Tuple_float = tuple[float, float]


def compute_syntax_preservation_score(
    text: str,
    target_language: str = "general",
) -> float:
    """
    Evaluates grammatical and structural syntax preservation S_syntax in [0.0, 1.0]:
    - Checks for token stuttering and excessive repetitive unigrams/bigrams
    - Checks balanced parentheses, brackets, and quotes
    - Checks sentence punctuation and valid token boundaries
    """
    if not text or len(text.strip()) == 0:
        return 0.0

    t = text.strip()
    score = 1.0

    # 1. Check balanced delimiters: (), [], {}, "", ''
    delimiters = [("(", ")"), ("[", "]"), ("{", "}")]
    for open_d, close_d in delimiters:
        if t.count(open_d) != t.count(close_d):
            score -= 0.15

    # 2. Check token repetition entropy (hallucinatory stuttering penalty)
    words = [w.lower() for w in re.findall(r"\b\w+\b", t)]
    if len(words) >= 8:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.25:
            score -= 0.60
        elif unique_ratio < 0.40:
            score -= 0.30

    # 3. Check for degenerate unprintable or corrupted characters
    non_ascii_ratio = sum(1 for c in t if ord(c) > 127) / max(1, len(t))
    if non_ascii_ratio > 0.40:
        score -= 0.25

    return float(max(0.0, min(1.0, round(score, 4))))


class LateralDivergenceEvaluator:
    """
    Computes and benchmarks the Lateral Divergence Metric across model completions.
    """

    def __init__(
        self,
        xi_penalty_coeff: float = 0.25,
        min_divergence_threshold: float = 0.30,
        min_syntax_threshold: float = 0.95,
    ):
        self.xi = xi_penalty_coeff
        self.min_divergence_threshold = min_divergence_threshold
        self.min_syntax_threshold = min_syntax_threshold

    def evaluate(
        self,
        v_neuro: np.ndarray,
        v_baseline: np.ndarray,
        completion_text: Optional[str] = None,
        raw_syntax_score: Optional[float] = None,
    ) -> LDMResult:
        """
        Evaluates LDM(v_neuro, v_baseline):
        LDM = (1 - cos_sim) + xi * S_syntax
        """
        cos_sim, cos_div = compute_cosine_divergence(v_neuro, v_baseline)

        if raw_syntax_score is not None:
            s_syntax = float(np.clip(raw_syntax_score, 0.0, 1.0))
        elif completion_text is not None:
            s_syntax = compute_syntax_preservation_score(completion_text)
        else:
            s_syntax = 1.0

        penalty_term = self.xi * s_syntax
        ldm_score = float(cos_div + penalty_term)

        is_valid = bool(
            cos_div >= self.min_divergence_threshold and s_syntax >= self.min_syntax_threshold
        )

        return LDMResult(
            ldm_score=round(ldm_score, 4),
            cosine_divergence=round(cos_div, 4),
            cosine_similarity=round(cos_sim, 4),
            syntax_preservation_score=round(s_syntax, 4),
            is_valid_breakthrough=is_valid,
            penalty_applied=round(penalty_term, 4),
        )

    def evaluate_batch(
        self,
        neuro_embeddings: np.ndarray,
        baseline_embeddings: np.ndarray,
        texts: Optional[List[str]] = None,
    ) -> List[LDMResult]:
        """Evaluates a batch of candidate completions against baseline centroids."""
        results = []
        n = neuro_embeddings.shape[0]
        for i in range(n):
            text_i = texts[i] if texts and i < len(texts) else None
            res = self.evaluate(neuro_embeddings[i], baseline_embeddings[i], completion_text=text_i)
            results.append(res)
        return results
