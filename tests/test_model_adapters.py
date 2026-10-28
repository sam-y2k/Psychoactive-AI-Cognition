"""
Unit tests for BaseModelAdapter, MockModelAdapter, NeuroSession, and @psychoactive decorator.
"""

import pytest
from psychoactive.compounds import CompoundType
from psychoactive.core.state import LifecycleStage
from psychoactive.templates import UniversalTemplate, SalesTemplate, BreakthroughResult
from psychoactive.adapters import MockModelAdapter, UniversalLLMAdapter, psychoactive
from psychoactive.session import NeuroSession


def test_mock_adapter_call_history():
    """Verify MockModelAdapter tracks prompts and dynamic sampling parameters."""
    mock = MockModelAdapter()
    resp = mock.generate("STAGE 1: CANONICAL BASELINE test", hyperparameters={"temperature": 0.70})
    assert len(mock.call_history) == 1
    assert mock.call_history[0]["hyperparameters"]["temperature"] == 0.70
    assert "[CANONICAL BASELINE]" in resp


def test_neuro_session_full_lifecycle_run():
    """Verify NeuroSession coordinates all 4 stages and returns BreakthroughResult."""
    mock = MockModelAdapter()
    template = UniversalTemplate(compound=CompoundType.PSILOCYBIN, dose=0.85)
    session = NeuroSession(template=template, adapter=mock, verbose=False)

    stages_visited = []

    def stage_callback(stage: LifecycleStage, text: str):
        stages_visited.append(stage)

    result = session.run(
        task="Break the deadlock in a multi-region distributed transactional ledger.",
        on_stage_complete=stage_callback,
    )

    # Verify all 4 stages were executed in sequence
    assert stages_visited == [
        LifecycleStage.BASELINE,
        LifecycleStage.ASCENT,
        LifecycleStage.PEAK,
        LifecycleStage.RETURN,
    ]

    # Verify BreakthroughResult structure
    assert isinstance(result, BreakthroughResult)
    assert "deadlock" in result.task_summary
    assert "[CANONICAL BASELINE]" in result.canonical_cliche
    assert "[PEAK BREAKTHROUGH]" in result.peak_breakthrough
    assert "[PARADIGM SHIFT]" in result.actionable_deliverable
    assert result.compound_used == "Psilocybin (4-PO-DMT / Psilocin Analog)"
    assert result.dosage == 0.85


def test_psychoactive_decorator_string_passthrough():
    """Verify @psychoactive decorator intercepts string prompt and returns grounded deliverable."""
    mock = MockModelAdapter()

    @psychoactive(compound=CompoundType.THC, dose=0.90, adapter=mock)
    def my_sales_engine(pitch_request: str) -> str:
        return pitch_request

    deliverable = my_sales_engine("How to sell unsexy B2B compliance software to skeptical CISOs?")
    
    assert isinstance(deliverable, str)
    assert "[ACTIONABLE DELIVERABLE]" in deliverable
    assert len(mock.call_history) == 4  # Ran all 4 stages


def test_psychoactive_decorator_full_result_mode():
    """Verify @psychoactive(return_full_result=True) returns complete telemetry object."""
    mock = MockModelAdapter()

    @psychoactive(compound=CompoundType.PSILOCYBIN, dose=0.85, adapter=mock, return_full_result=True)
    def plan_strategy(challenge: str):
        pass

    result = plan_strategy("SaaS startup facing commoditization from big tech.")
    
    assert isinstance(result, BreakthroughResult)
    assert result.domain == "Universal Problem Solving"
    assert "prior_precision_pi_P" in result.metadata


def test_universal_llm_adapter_parameter_mapping():
    """Verify UniversalLLMAdapter correctly configures parameters."""
    adapter = UniversalLLMAdapter(model="claude-3-5-sonnet", api_key="sk-test-key", timeout=45.0)
    assert adapter.model == "claude-3-5-sonnet"
    assert adapter.api_key == "sk-test-key"
    assert adapter.timeout == 45.0
