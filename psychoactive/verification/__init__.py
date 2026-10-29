"""
Deterministic Adversarial Verification & Metric Engines.
Implements:
- Lateral Divergence Metric (LDM) tensor calculator
- Z3 SMT Theorem Prover integration for formal constraint checking
"""

from psychoactive.verification.ldm import (
    LateralDivergenceEvaluator,
    LDMResult,
    compute_cosine_divergence,
    compute_syntax_preservation_score,
)
from psychoactive.verification.z3_verifier import (
    Z3ConstraintVerifier,
    VerificationProof,
    LogicalConstraint,
)

__all__ = [
    "LateralDivergenceEvaluator",
    "LDMResult",
    "compute_cosine_divergence",
    "compute_syntax_preservation_score",
    "Z3ConstraintVerifier",
    "VerificationProof",
    "LogicalConstraint",
]
