"""
Unit tests for the Universal Template Engine & Domain Presets.
"""

import pytest
from psychoactive.compounds import CompoundType
from psychoactive.core.state import LifecycleStage
from psychoactive.templates import (
    UniversalTemplate,
    SalesTemplate,
    EngineeringTemplate,
    StrategyTemplate,
    CreativeTemplate,
    BreakthroughResult,
)


def test_universal_template_four_stage_prompts():
    """Verify UniversalTemplate generates valid prompts across all 4 stages for any generic task."""
    task = "Optimize an enterprise supply chain experiencing unpredictable bottleneck delays."
    template = UniversalTemplate(domain_name="Global Operations", compound=CompoundType.PSILOCYBIN, dose=0.85)

    # Stage 1: Baseline Mapping
    p1 = template.extract_baseline_prompt(task)
    assert "STAGE 1: CANONICAL BASELINE MAPPING" in p1
    assert "Global Operations" in p1
    assert task in p1

    # Stage 2: Ascent
    baseline_fake = "Use standard buffer inventory and lean JIT tracking."
    p2 = template.build_ascent_prompt(task, baseline_fake)
    assert "STAGE 2: ASCENT & ASSUMPTION DISMANTLING" in p2
    assert "5-HT2A ASCENT" in p2
    assert template.state.current_stage == LifecycleStage.ASCENT

    # Stage 3: Peak
    assumptions_fake = "Assumption 1: Centralized tracking is required."
    p3 = template.build_peak_prompt(task, baseline_fake, assumptions_fake)
    assert "STAGE 3: PEAK UNCONSTRAINED SYNTHESIS" in p3
    assert "STIEFEL MANIFOLD PROJECTION" in p3
    assert template.state.current_stage == LifecycleStage.PEAK

    # Stage 4: Return
    peak_fake = "Model supply chain as fungal hyphae sharing phosphorus."
    p4 = template.build_return_prompt(task, baseline_fake, peak_fake)
    assert "STAGE 4: INTEGRATION & ACTIONABLE DELIVERABLE" in p4
    assert "[ACTIONABLE DELIVERABLE]" in p4
    assert template.state.current_stage == LifecycleStage.RETURN


def test_sales_template_grounding_and_icp():
    """Verify SalesTemplate properly binds ICP, product, and outreach rubrics."""
    sales = SalesTemplate(
        product="Agentic Cyber Defense Platform",
        icp="Chief Information Security Officer (CISO)",
        compound=CompoundType.THC,
        dose=0.90,
    )
    task = "Break into Fortune 500 banks where SDR emails get 0% reply rates."

    p1 = sales.extract_baseline_prompt(task)
    assert "Agentic Cyber Defense Platform" in p1
    assert "Chief Information Security Officer (CISO)" in p1

    rules = sales.get_domain_grounding_rules()
    assert "COMPLETE COLD OUTREACH ARTIFACT" in rules
    assert "UNIGNORABLE PATTERN INTERRUPT" in rules


def test_engineering_template_formal_rubrics():
    """Verify EngineeringTemplate enforces concurrency and thread-safety constraints."""
    eng = EngineeringTemplate(tech_stack="Rust / Tokio", compound=CompoundType.PSILOCYBIN, dose=0.90)
    rules = eng.get_domain_grounding_rules()
    assert "FORMAL CORRECTNESS" in rules
    assert "CONCRETE PSEUDOCODE" in rules
    assert "FAILURE MODE ANALYSIS" in rules


def test_compound_directive_switching_thc_vs_psilocybin():
    """Verify switching from Psilocybin to THC switches the cognitive operator."""
    task = "Generate viral positioning for a developer productivity tool."

    # Psilocybin template
    psilo_template = UniversalTemplate(compound=CompoundType.PSILOCYBIN, dose=0.85)
    p3_psilo = psilo_template.build_peak_prompt(task, "Baseline", "Assumptions")
    assert "REBUS PEAK DIVERGENCE" in p3_psilo

    # THC template
    thc_template = UniversalTemplate(compound=CompoundType.THC, dose=0.85)
    p3_thc = thc_template.build_peak_prompt(task, "Baseline", "Assumptions")
    assert "SUB-THRESHOLD SALIENCE FILTER" in p3_thc
    assert "LATERAL SUPPRESSION" in p3_thc


def test_breakthrough_result_schema_validation():
    """Verify BreakthroughResult parses and stores complete audit telemetry."""
    template = UniversalTemplate(domain_name="Biotech Discovery", compound=CompoundType.PSILOCYBIN, dose=0.85)
    
    result = template.parse_breakthrough(
        task="Discover an allosteric inhibitor for LRRK2 kinase.",
        baseline="Screen conventional ATP-competitive benzene scaffolds.",
        peak="Project onto marine sponge macrolide polycyclic dynamics.",
        deliverable="1. Paradigm Shift: Ditch aromatic planar rings. 2. Synthesis: 3 spirocyclic non-planar scaffolds.",
        orthogonal_domain_name="Marine Polycycles"
    )

    assert isinstance(result, BreakthroughResult)
    assert result.domain == "Biotech Discovery"
    assert "LRRK2" in result.task_summary
    assert "benzene" in result.canonical_cliche
    assert result.compound_used == "Psilocybin (4-PO-DMT / Psilocin Analog)"
    assert result.dosage == 0.85
    assert "prior_precision_pi_P" in result.metadata
