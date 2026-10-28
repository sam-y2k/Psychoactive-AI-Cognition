"""
Neurochemical State & 4-Stage Lifecycle Progression.
Formalizes Hill-equation receptor dynamics, transient state kinetics,
and phase transitions across Baseline -> Ascent -> Peak -> Return.
"""

from enum import Enum
from typing import Dict, Any, Optional
import math
from pydantic import BaseModel, Field

from psychoactive.compounds import CompoundProfile, CompoundType, get_compound_profile


class LifecycleStage(str, Enum):
    """The 4-stage cognitive trajectory formalizing the psychedelic lifecycle."""
    BASELINE = "baseline"       # t in [0, tau): Homeostatic framing, mapping canonical attractor
    ASCENT = "ascent"           # t in [tau, 2tau): Progressive prior relaxation & disinhibition
    PEAK = "peak"               # t in [2tau, 3tau): Maximum entropy, unconstrained cross-domain leap
    RETURN = "return"           # t in [3tau, 4tau): Annealing, deterministic grounding & consolidation


class NeurochemicalState:
    """
    State manager tracking continuous pharmacological kinetics and discrete lifecycle phases.
    """

    def __init__(
        self,
        compound: str | CompoundType | CompoundProfile = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
        tau_steps: Optional[int] = None,
        hill_coefficient: float = 1.8,
        ec50: float = 0.50,
    ):
        """
        Initialize the dynamic neurochemical state.

        Args:
            compound: Target compound profile or identifier.
            dose: Normalized dosage D in [0.0, 1.0].
            tau_steps: Number of token/interaction steps per lifecycle stage.
            hill_coefficient: Hill cooperativity exponent n (typically 1.5 - 2.0).
            ec50: Half-maximal effective concentration EC50.
        """
        if isinstance(compound, CompoundProfile):
            self.profile = compound
        else:
            self.profile = get_compound_profile(compound)

        self.dose = max(0.0, min(1.0, float(dose)))
        self.tau_steps = tau_steps or self.profile.typical_tau_steps
        self.hill_coefficient = hill_coefficient
        self.ec50 = ec50

        # Dynamic state variables
        self.current_step = 0
        self.total_lifetime_steps = self.tau_steps * 4
        self.current_stage = LifecycleStage.BASELINE

    @property
    def receptor_occupancy(self) -> float:
        """
        Calculates receptor fractional occupancy via the normalized Hill equation:
        theta = (D^n / (EC50^n + D^n)) / (1^n / (EC50^n + 1^n))
        Ensures D = 1.0 yields full maximal occupancy (1.0).
        """
        if self.dose <= 0.0:
            return 0.0
        d_n = math.pow(self.dose, self.hill_coefficient)
        ec_n = math.pow(self.ec50, self.hill_coefficient)
        raw_theta = d_n / (ec_n + d_n)
        max_theta = 1.0 / (ec_n + 1.0)
        return float(min(1.0, raw_theta / max_theta))

    @property
    def stage_progress(self) -> float:
        """Fractional progress within the active stage [0.0, 1.0]."""
        stage_index = self._get_stage_index(self.current_stage)
        steps_into_stage = self.current_step - (stage_index * self.tau_steps)
        return max(0.0, min(1.0, steps_into_stage / max(1, self.tau_steps)))

    @property
    def overall_progress(self) -> float:
        """Total trajectory progression phi in [0.0, 1.0]."""
        return max(0.0, min(1.0, self.current_step / max(1, self.total_lifetime_steps)))

    def get_prior_precision(self) -> float:
        """
        Calculates instantaneous prior precision pi_P(t) in [pi_min, 1.0].
        At Baseline: pi_P = 1.0.
        At Peak: pi_P = 1.0 - (occupancy * base_prior_relaxation_max).
        At Return: progressively re-anneals back to 1.0.
        """
        max_relax = self.profile.base_prior_relaxation_max * self.receptor_occupancy

        if self.current_stage == LifecycleStage.BASELINE:
            return 1.0

        elif self.current_stage == LifecycleStage.ASCENT:
            # Smooth sigmoid drop from 1.0 down to (1.0 - max_relax)
            p = self.stage_progress
            decay = 0.5 * (1.0 - math.cos(math.pi * p))
            return float(1.0 - (max_relax * decay))

        elif self.current_stage == LifecycleStage.PEAK:
            # Maintained at lowest basin well (maximum entropy)
            return float(max(0.10, 1.0 - max_relax))

        elif self.current_stage == LifecycleStage.RETURN:
            # Re-annealing back to homeostatic reality (1.0)
            p = self.stage_progress
            rebound = 0.5 * (1.0 - math.cos(math.pi * p))
            min_val = 1.0 - max_relax
            return float(min_val + ((1.0 - min_val) * rebound))

        return 1.0

    def get_retrograde_gating(self) -> float:
        """
        Calculates CB1 retrograde lateral transmission filter lambda_DSE(t) in [0.0, 0.70].
        Suppresses high-probability dominant tokens while boosting low-probability tail associations.
        """
        max_gate = min(0.70, self.profile.retrograde_gating_lambda * self.receptor_occupancy)

        if self.current_stage in (LifecycleStage.BASELINE, LifecycleStage.RETURN):
            # Presynaptic suppression is low during baseline and post-integration
            if self.current_stage == LifecycleStage.RETURN:
                p = self.stage_progress
                return float(max_gate * (1.0 - p))
            return 0.05

        elif self.current_stage == LifecycleStage.ASCENT:
            return float(max_gate * self.stage_progress)

        elif self.current_stage == LifecycleStage.PEAK:
            return float(max_gate)

        return 0.0

    def get_stiefel_expansion_factor(self) -> float:
        """
        Orthogonal manifold cross-talk expansion factor in [0.0, 1.0].
        Governs how far the agent jumps into alien conceptual domains.
        """
        if self.profile.stiefel_manifold_rank == 0:
            return 0.0
        
        # Stiefel bridge activates primarily during Peak
        if self.current_stage == LifecycleStage.PEAK:
            return float(self.receptor_occupancy)
        elif self.current_stage == LifecycleStage.ASCENT:
            return float(self.receptor_occupancy * self.stage_progress * 0.5)
        elif self.current_stage == LifecycleStage.RETURN:
            return float(self.receptor_occupancy * (1.0 - self.stage_progress) * 0.3)
        return 0.0

    def advance_step(self, n: int = 1) -> LifecycleStage:
        """
        Advance simulation steps and handle automatic phase transitions.
        """
        self.current_step += n
        new_stage = self._calculate_stage_for_step(self.current_step)
        self.current_stage = new_stage
        return self.current_stage

    def transition_to_stage(self, stage: LifecycleStage):
        """Force transition directly to a designated lifecycle stage."""
        self.current_stage = stage
        stage_idx = self._get_stage_index(stage)
        self.current_step = stage_idx * self.tau_steps

    def _get_stage_index(self, stage: LifecycleStage) -> int:
        mapping = {
            LifecycleStage.BASELINE: 0,
            LifecycleStage.ASCENT: 1,
            LifecycleStage.PEAK: 2,
            LifecycleStage.RETURN: 3,
        }
        return mapping.get(stage, 0)

    def _calculate_stage_for_step(self, step: int) -> LifecycleStage:
        if step < self.tau_steps:
            return LifecycleStage.BASELINE
        elif step < self.tau_steps * 2:
            return LifecycleStage.ASCENT
        elif step < self.tau_steps * 3:
            return LifecycleStage.PEAK
        else:
            return LifecycleStage.RETURN

    def to_dict(self) -> Dict[str, Any]:
        """Export instantaneous pharmacological snapshot."""
        return {
            "compound": self.profile.name,
            "compound_type": self.profile.compound_type.value,
            "dose": self.dose,
            "stage": self.current_stage.value,
            "current_step": self.current_step,
            "stage_progress": round(self.stage_progress, 3),
            "receptor_occupancy": round(self.receptor_occupancy, 3),
            "prior_precision_pi_P": round(self.get_prior_precision(), 3),
            "retrograde_gating_lambda": round(self.get_retrograde_gating(), 3),
            "stiefel_expansion": round(self.get_stiefel_expansion_factor(), 3),
        }
