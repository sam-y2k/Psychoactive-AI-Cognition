"""
Unit tests for TripSitter Safety Guardrail & IntegrationGrounder.
"""

import pytest
from psychoactive.compounds import CompoundType
from psychoactive.core.state import NeurochemicalState, LifecycleStage
from psychoactive.integration.sitter import TripSitter, CoherenceReport
from psychoactive.integration.grounder import IntegrationGrounder, GroundedArtifact
from psychoactive.templates.universal import UniversalTemplate
from psychoactive.adapters.base import MockModelAdapter
from psychoactive.session import NeuroSession


def test_trip_sitter_coherent_evaluation():
    """Verify TripSitter approves coherent grounded text without triggering breaker."""
    sitter = TripSitter()
    task = "Design a low-latency database replication mechanism across multi-cloud regions."
    sample_peak = (
        "We map the replication mechanism onto decentralized fungal hyphae sharing resources. "
        "Each database replica functions as an autonomous mycelial tip exchanging pulsed state updates "
        "along localized latency gradients without a central cluster leader."
    )

    report = sitter.evaluate_output(sample_peak, LifecycleStage.PEAK, task)
    assert isinstance(report, CoherenceReport)
    assert report.coherence_score >= 0.40
    assert report.circuit_breaker_triggered is False
    assert report.hallucination_risk < 0.50


def test_trip_sitter_syntactic_collapse_breaker():
    """Verify TripSitter catches degenerate gibberish and triggers emergency breaker."""
    sitter = TripSitter()
    task = "Optimize an enterprise supply chain."
    gibberish = "word word word" # Under 20 chars, few unique tokens

    report = sitter.evaluate_output(gibberish, LifecycleStage.PEAK, task)
    assert report.circuit_breaker_triggered is True
    assert report.coherence_score == 0.0
    assert "Severe syntactic collapse" in report.intervention_notes[0]


def test_trip_sitter_repetitive_stutter_loop():
    """Verify TripSitter catches repetitive mode-collapse token stuttering."""
    sitter = TripSitter()
    task = "Solve customer churn."
    stutter = "repeat loop repeat loop repeat loop repeat loop repeat loop repeat loop repeat loop repeat loop repeat loop repeat loop"

    report = sitter.evaluate_output(stutter, LifecycleStage.PEAK, task)
    assert report.circuit_breaker_triggered is True
    assert any("Catastrophic mode-stutter loop" in note for note in report.intervention_notes)


def test_emergency_antagonist_protocol():
    """Verify applying emergency antagonist immediately restores baseline homeostasis."""
    state = NeurochemicalState(compound=CompoundType.PSILOCYBIN, dose=0.90)
    state.transition_to_stage(LifecycleStage.PEAK)
    assert state.current_stage == LifecycleStage.PEAK
    assert state.get_prior_precision() < 0.35

    sitter = TripSitter()
    msg = sitter.apply_emergency_antagonist(state)

    assert state.current_stage == LifecycleStage.BASELINE
    assert state.get_prior_precision() == 1.0
    assert "EMERGENCY TRIP-SITTER PROTOCOL ENGAGED" in msg


def test_integration_grounder_parsing():
    """Verify IntegrationGrounder accurately extracts sections, tactics, and readiness score."""
    grounder = IntegrationGrounder()
    return_text = (
        "[PARADIGM SHIFT]: Abandon synchronous two-phase commits in favor of asynchronous fungal stigmergy.\n"
        "[THE MECHANISM]: Nodes broadcast discrete decay pulses; local consensus emerges without global locking.\n"
        "[ACTIONABLE DELIVERABLE]:\n"
        "1. Deploy a ring-buffered lock-free queue with localized version timestamps.\n"
        "2. Replace master coordinator with asynchronous peer gossip-decay protocol.\n"
        "3. Run automated deterministic TLA+ model checker to verify race-free execution."
    )

    artifact = grounder.ground(return_text)
    assert isinstance(artifact, GroundedArtifact)
    assert "two-phase commits" in artifact.paradigm_shift
    assert "decay pulses" in artifact.orthogonal_mechanism
    assert len(artifact.actionable_tactics) == 3
    assert "ring-buffered" in artifact.actionable_tactics[0]
    assert artifact.readiness_score >= 80


def test_neuro_session_coherence_telemetry_integration():
    """Verify NeuroSession logs TripSitter coherence audit and GroundedArtifact in metadata."""
    mock = MockModelAdapter()
    session = NeuroSession(adapter=mock)
    result = session.run("Transform enterprise B2B sales outreach.")

    assert "coherence_audit" in result.metadata
    assert "grounded_artifact" in result.metadata
    assert "peak_evaluation" in result.metadata["coherence_audit"]
    assert "return_evaluation" in result.metadata["coherence_audit"]
    assert result.metadata["grounded_artifact"]["readiness_score"] > 50
