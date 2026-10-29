"""
Formal SMT Verification Engine with Z3 Theorem Prover.
Formalizes Tier 4 of the REBUS-AI Architecture:
- Translates reasoning invariants and safety bounds into formal first-order logic constraints
- Proves satisfiability (SAT) vs logical contradiction (UNSAT)
- Triggers Antagonist Reset (pi_P <- 1.0) if invariant checking fails
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import z3


@dataclass(frozen=True)
class LogicalConstraint:
    """Formal logical proposition or arithmetic inequality."""
    name: str
    variable: str
    operator: str                       # ">=", "<=", "==", "!=", ">", "<"
    threshold: float
    description: str = ""


@dataclass(frozen=True)
class VerificationProof:
    """Certified formal verification output from Z3 SMT solver."""
    is_satisfiable: bool                # True if SAT (consistent), False if UNSAT (contradiction)
    status: str                         # "sat", "unsat", "unknown"
    witness_model: Dict[str, Any]       # Concrete variable assignments satisfying constraints
    failed_invariants: List[str]        # Invariants that triggered contradiction or violation
    antagonist_reset_required: bool     # True if UNSAT triggers emergency pi_P <- 1.0 reset


class Z3ConstraintVerifier:
    """
    Automated SMT Verification Engine acting as the Tier 4 Adversarial Gate.
    """

    def __init__(self, timeout_ms: int = 5000):
        self.timeout_ms = timeout_ms

    def verify_numeric_bounds(
        self,
        candidate_values: Dict[str, float],
        constraints: List[LogicalConstraint],
    ) -> VerificationProof:
        """
        Formulates and solves real arithmetic constraints over candidate reasoning parameters.

        Args:
            candidate_values: Dictionary mapping variable names to candidate floats.
            constraints: List of LogicalConstraint objects to prove.

        Returns:
            VerificationProof with SAT/UNSAT verdict and counter-examples.
        """
        solver = z3.Solver()
        solver.set("timeout", self.timeout_ms)

        z3_vars: Dict[str, z3.ArithRef] = {}
        failed_invariants: List[str] = []

        # 1. Instantiate Z3 Real variables
        for var_name in candidate_values.keys():
            z3_vars[var_name] = z3.Real(var_name)

        # 2. Add Candidate Values as assertions: (var == value)
        for var_name, val in candidate_values.items():
            z3_var = z3_vars[var_name]
            solver.add(z3_var == z3.RealVal(str(val)))

        # 3. Add Safety and Integrity Constraints
        for c in constraints:
            if c.variable not in z3_vars:
                failed_invariants.append(f"Missing variable: {c.variable}")
                continue

            zv = z3_vars[c.variable]
            thresh = z3.RealVal(str(c.threshold))

            if c.operator == ">=":
                expr = zv >= thresh
            elif c.operator == "<=":
                expr = zv <= thresh
            elif c.operator == "==":
                expr = zv == thresh
            elif c.operator == "!=":
                expr = zv != thresh
            elif c.operator == ">":
                expr = zv > thresh
            elif c.operator == "<":
                expr = zv < thresh
            else:
                raise ValueError(f"Unsupported operator: {c.operator}")

            # Check individual constraint validity
            sub_solver = z3.Solver()
            sub_solver.add(solver.assertions())
            sub_solver.add(z3.Not(expr))
            # If sub_solver is SAT, it means the candidate value CAN violate the constraint!
            if sub_solver.check() == z3.sat:
                failed_invariants.append(f"Violated: {c.name} ({c.variable} {c.operator} {c.threshold})")

            solver.add(expr)

        # 4. Global Satisfiability Check
        verdict = solver.check()
        is_sat = (verdict == z3.sat) and (len(failed_invariants) == 0)

        model_dict: Dict[str, Any] = {}
        if verdict == z3.sat:
            m = solver.model()
            for k, zv in z3_vars.items():
                val = m.eval(zv)
                model_dict[k] = str(val)

        return VerificationProof(
            is_satisfiable=is_sat,
            status=str(verdict),
            witness_model=model_dict,
            failed_invariants=failed_invariants,
            antagonist_reset_required=(not is_sat),
        )

    def verify_propositional_consistency(
        self,
        clauses: List[Tuple[str, bool]],
        incompatible_pairs: List[Tuple[str, str]],
    ) -> VerificationProof:
        """
        Proves propositional non-contradiction between asserted reasoning facts.

        Args:
            clauses: List of (proposition_name, truth_value)
            incompatible_pairs: Pairs of propositions that cannot simultaneously be true.

        Returns:
            VerificationProof certifying absence of logical hallucination/contradiction.
        """
        solver = z3.Solver()
        solver.set("timeout", self.timeout_ms)

        prop_vars: Dict[str, z3.BoolRef] = {}
        for name, _ in clauses:
            prop_vars[name] = z3.Bool(name)

        # Assert factual states
        for name, truth in clauses:
            pv = prop_vars[name]
            solver.add(pv if truth else z3.Not(pv))

        # Assert incompatibility exclusions: Not(A and B)
        failed_exclusions = []
        for a, b in incompatible_pairs:
            if a in prop_vars and b in prop_vars:
                solver.add(z3.Not(z3.And(prop_vars[a], prop_vars[b])))

        verdict = solver.check()
        is_sat = (verdict == z3.sat)

        model_dict = {}
        if is_sat:
            m = solver.model()
            for k, pv in prop_vars.items():
                val = m.eval(pv)
                model_dict[k] = bool(val)
        else:
            failed_exclusions.append("Mutual exclusion contradiction detected between active propositions.")

        return VerificationProof(
            is_satisfiable=is_sat,
            status=str(verdict),
            witness_model=model_dict,
            failed_invariants=failed_exclusions,
            antagonist_reset_required=(not is_sat),
        )
