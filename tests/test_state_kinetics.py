"""
Unit tests for NeurochemicalState and 4-Stage Lifecycle Progression.
"""

import pytest
import math
from psychoactive.compounds import CompoundType, get_compound_profile
from psychoactive.core.state import NeurochemicalState, LifecycleStage


def test_receptor_occupancy_hill_equation():
    """Verify Hill equation response: D=0 => 0, D=1.0 => 1.0, monotonic scaling."""
    state_zero = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.0, ec50=0.5)
    assert state_zero.receptor_occupancy == 0.0

    state_half = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.5, ec50=0.5)
    assert 0.50 <= state_half.receptor_occupancy <= 0.70

    state_full = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=1.0, ec50=0.5)
    assert pytest.approx(state_full.receptor_occupancy, abs=1e-3) == 1.00


def test_four_stage_lifecycle_progression():
    """Verify discrete phase transitions across tau steps."""
    tau = 5
    state = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.85, tau_steps=tau)
    
    assert state.current_stage == LifecycleStage.BASELINE

    # Advance through Baseline [0, tau)
    state.advance_step(tau)
    assert state.current_stage == LifecycleStage.ASCENT

    # Advance through Ascent [tau, 2tau)
    state.advance_step(tau)
    assert state.current_stage == LifecycleStage.PEAK

    # Advance through Peak [2tau, 3tau)
    state.advance_step(tau)
    assert state.current_stage == LifecycleStage.RETURN


def test_prior_precision_kinetics():
    """Verify pi_P(t) drops at Peak and re-anneals at Return."""
    state = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.90, tau_steps=10)

    # Baseline: pi_P = 1.0
    assert state.get_prior_precision() == 1.0

    # Transition to Peak
    state.transition_to_stage(LifecycleStage.PEAK)
    pi_peak = state.get_prior_precision()
    assert 0.10 <= pi_peak <= 0.35

    # Transition to Return
    state.transition_to_stage(LifecycleStage.RETURN)
    # At start of return, it is near peak
    state.advance_step(9) # Near end of return
    pi_return = state.get_prior_precision()
    assert pi_return > pi_peak
    assert pi_return >= 0.85


def test_retrograde_gating_bounds():
    """Verify CB1 retrograde gating lambda adheres to biophysical bound <= 0.70."""
    state_thc = NeurochemicalState(compound=CompoundType.THC, dose=1.0, tau_steps=10)
    state_thc.transition_to_stage(LifecycleStage.PEAK)
    
    lam = state_thc.get_retrograde_gating()
    assert 0.40 <= lam <= 0.70
