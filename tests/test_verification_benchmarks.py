"""
Rigorous Unit Tests for Chunk 3:
- Lateral Divergence Metric (LDM) Evaluator
- Z3 SMT Formal Theorem Prover Gate
- Remote Associates Test (RAT) Benchmark Suite
- Ablation Benchmark Harness
"""

import pytest
import numpy as np
from psychoactive.verification.ldm import (
    LateralDivergenceEvaluator,
    compute_cosine_divergence,
    compute_syntax_preservation_score,
)
from psychoactive.verification.z3_verifier import (
    Z3ConstraintVerifier,
    LogicalConstraint,
)
from psychoactive.benchmarks.rat_benchmark import (
    RATBenchmarkRunner,
    RATItem,
    SAMPLE_RAT_TRIADS,
)
from psychoactive.benchmarks.ablation_runner import (
    AblationBenchmarkRunner,
    AblationCondition,
)


# =========================================================================
# 1. LATERAL DIVERGENCE METRIC (LDM) TESTS
# =========================================================================

def test_ldm_divergence_and_syntax_penalty():
    """Verify LDM rewards angular divergence while penalizing syntax degradation."""
    evaluator = LateralDivergenceEvaluator(xi_penalty_coeff=0.25)

    v_base = np.array([1.0, 0.0, 0.0])
    # Orthogonal novel vector (cos_sim = 0, cos_div = 1.0)
    v_novel = np.array([0.0, 1.0, 0.0])

    # Case A: Perfect syntax
    res_clean = evaluator.evaluate(v_novel, v_base, completion_text="This is a valid, clean, and sound sentence.")
    assert res_clean.cosine_divergence == 1.0
    assert res_clean.syntax_preservation_score >= 0.95
    assert res_clean.is_valid_breakthrough is True
    assert res_clean.ldm_score > 1.20

    # Case B: Syntactic delirium (repetitive mode-stutter loop)
    delirium_text = "word word word word word word word word word word"
    res_broken = evaluator.evaluate(v_novel, v_base, completion_text=delirium_text)
    assert res_broken.syntax_preservation_score < 0.80
    assert res_broken.ldm_score < res_clean.ldm_score


def test_syntax_delimiter_and_corrupted_characters():
    """Verify syntax evaluator detects unclosed delimiters and noise."""
    unclosed = "This text has an unclosed parenthesis (and nothing else."
    score = compute_syntax_preservation_score(unclosed)
    assert score < 1.0

    valid = "This text is well-formed (and properly balanced)."
    score_valid = compute_syntax_preservation_score(valid)
    assert score_valid == 1.0


# =========================================================================
# 2. Z3 SMT FORMAL VERIFICATION TESTS (TIER 4 GATE)
# =========================================================================

def test_z3_numeric_invariants_pass_and_fail():
    """Verify Z3 proves constraint satisfaction and detects invariant violations."""
    verifier = Z3ConstraintVerifier()

    constraints = [
        LogicalConstraint("DSE Bound", "lambda_dse", "<=", 0.70),
        LogicalConstraint("Min Temperature", "temperature", ">=", 0.10),
        LogicalConstraint("Prior Precision Ceiling", "pi_p", "<=", 1.0),
    ]

    # Valid candidate state
    valid_state = {"lambda_dse": 0.45, "temperature": 0.80, "pi_p": 0.25}
    proof_valid = verifier.verify_numeric_bounds(valid_state, constraints)
    assert proof_valid.is_satisfiable is True
    assert proof_valid.status == "sat"
    assert proof_valid.antagonist_reset_required is False
    assert len(proof_valid.failed_invariants) == 0

    # Invalid candidate state (DSE bound violated: 0.85 > 0.70)
    violating_state = {"lambda_dse": 0.85, "temperature": 0.80, "pi_p": 0.25}
    proof_invalid = verifier.verify_numeric_bounds(violating_state, constraints)
    assert proof_invalid.is_satisfiable is False
    assert proof_invalid.antagonist_reset_required is True
    assert any("DSE Bound" in fail for fail in proof_invalid.failed_invariants)


def test_z3_propositional_contradiction_detection():
    """Verify Z3 SMT engine catches contradictory reasoning assertions."""
    verifier = Z3ConstraintVerifier()

    # Fact: Candidate is deterministic, but also claims to be unconstrained stochastic
    clauses = [("is_deterministic", True), ("is_unconstrained_stochastic", True)]
    incompatibilities = [("is_deterministic", "is_unconstrained_stochastic")]

    proof = verifier.verify_propositional_consistency(clauses, incompatibilities)
    # Contradiction => UNSAT => Triggers Antagonist Reset
    assert proof.is_satisfiable is False
    assert proof.antagonist_reset_required is True


# =========================================================================
# 3. REMOTE ASSOCIATES TEST (RAT) & ABLATION BENCHMARK TESTS
# =========================================================================

def test_rat_benchmark_execution():
    """Verify RAT benchmark evaluates triad solutions accurately."""
    runner = RATBenchmarkRunner(dataset=SAMPLE_RAT_TRIADS[:4])

    # Mock provider that answers only item 1 correctly
    def mock_provider(item: RATItem):
        if item.item_id == 1:
            return "The connecting term is cheese because of cottage cheese.", 12.0
        return "I think the answer is water.", 10.0

    result = runner.run_benchmark(mock_provider)
    assert result.total_items == 4
    assert result.correct_count == 1
    assert result.accuracy_percentage == 25.0
    assert result.mean_response_latency_ms > 0.0


def test_ablation_reference_report_validation():
    """Verify published benchmark references from Section 12."""
    report = AblationBenchmarkRunner.get_reference_benchmark_results()
    assert report.verified_superiority is True

    full_pipe = report.conditions[AblationCondition.FULL_REBUS_PIPELINE]
    assert full_pipe.pass_at_1 == 90.8
    assert full_pipe.lateral_divergence_pct == +44.6
    assert full_pipe.hallucination_rate_pct < 2.0
