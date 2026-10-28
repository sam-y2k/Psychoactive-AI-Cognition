"""
NeuroSession: 4-Stage Cognitive Lifecycle Orchestrator.
Coordinates templates and model adapters across Baseline -> Ascent -> Peak -> Return.
"""

from typing import Optional, Dict, Any, Callable
from psychoactive.compounds import CompoundType
from psychoactive.core.state import LifecycleStage
from psychoactive.templates.base import NeuroTemplate, BreakthroughResult
from psychoactive.templates.universal import UniversalTemplate
from psychoactive.adapters.base import BaseModelAdapter, MockModelAdapter
from psychoactive.adapters.universal_llm import UniversalLLMAdapter
from psychoactive.integration.sitter import TripSitter, CoherenceReport
from psychoactive.integration.grounder import IntegrationGrounder, GroundedArtifact


class NeuroSession:
    """
    High-level execution session that drives a task through the complete 4-stage neurochemical journey.
    Monitored in real time by the Trip-Sitter and consolidated by the Integration Grounder.
    """

    def __init__(
        self,
        template: Optional[NeuroTemplate] = None,
        adapter: Optional[BaseModelAdapter] = None,
        sitter: Optional[TripSitter] = None,
        grounder: Optional[IntegrationGrounder] = None,
        model: str = "gpt-4o",
        compound: str | CompoundType = CompoundType.PSILOCYBIN,
        dose: float = 0.85,
        verbose: bool = False,
    ):
        """
        Initialize the session.

        Args:
            template: The cognitive template (defaults to UniversalTemplate).
            adapter: Model adapter instance. If None, creates UniversalLLMAdapter(model=model).
            sitter: Safety supervisor (defaults to TripSitter).
            grounder: Consolidation parser (defaults to IntegrationGrounder).
            model: Model identifier if adapter is not provided.
            compound: Pharmacological profile.
            dose: Normalized dosage in [0.0, 1.0].
            verbose: If True, prints lifecycle state transitions in real time.
        """
        self.template = template or UniversalTemplate(compound=compound, dose=dose)
        self.adapter = adapter or UniversalLLMAdapter(model=model)
        self.sitter = sitter or TripSitter()
        self.grounder = grounder or IntegrationGrounder()
        self.verbose = verbose

    def run(
        self,
        task: str,
        on_stage_complete: Optional[Callable[[LifecycleStage, str], None]] = None,
    ) -> BreakthroughResult:
        """
        Execute the complete 4-stage neurochemical cognitive trajectory.

        Args:
            task: The core problem, dilemma, or task prompt.
            on_stage_complete: Optional callback invoked after each stage: fn(stage, output_text).

        Returns:
            BreakthroughResult containing the complete structured deliverable and telemetry.
        """
        self._log(f"[*] Initializing {self.template.state.profile.name} Session (Dose: {self.template.state.dose})")
        coherence_audit: Dict[str, Any] = {}

        # STAGE 1: CANONICAL BASELINE
        self.template.state.transition_to_stage(LifecycleStage.BASELINE)
        self._log("\n--- STAGE 1: BASELINE (Mapping Canonical Attractor Basin) ---")
        prompt_1 = self.template.extract_baseline_prompt(task)
        params_1 = self.template.rebus.get_sampling_hyperparameters()
        baseline_output = self.adapter.generate(prompt_1, hyperparameters=params_1)
        if on_stage_complete:
            on_stage_complete(LifecycleStage.BASELINE, baseline_output)
        self._log(f"[Baseline Output]:\n{baseline_output[:300]}...")

        # STAGE 2: ASCENT
        self.template.state.transition_to_stage(LifecycleStage.ASCENT)
        self._log(f"\n--- STAGE 2: ASCENT (Prior Precision pi_P = {self.template.state.get_prior_precision():.2f}) ---")
        prompt_2 = self.template.build_ascent_prompt(task, baseline_output)
        params_2 = self.template.rebus.get_sampling_hyperparameters()
        ascent_output = self.adapter.generate(prompt_2, hyperparameters=params_2)
        if on_stage_complete:
            on_stage_complete(LifecycleStage.ASCENT, ascent_output)
        self._log(f"[Ascent Output]:\n{ascent_output[:300]}...")

        # STAGE 3: PEAK
        self.template.state.transition_to_stage(LifecycleStage.PEAK)
        self._log(f"\n--- STAGE 3: PEAK DIVERGENCE (pi_P = {self.template.state.get_prior_precision():.2f}, Stiefel Projection Active) ---")
        prompt_3 = self.template.build_peak_prompt(task, baseline_output, ascent_output)
        params_3 = self.template.rebus.get_sampling_hyperparameters()
        peak_output = self.adapter.generate(prompt_3, hyperparameters=params_3)
        
        # Trip-Sitter evaluation of Peak divergence
        peak_eval = self.sitter.evaluate_output(peak_output, LifecycleStage.PEAK, task, baseline_output)
        coherence_audit["peak_evaluation"] = peak_eval.model_dump()
        if peak_eval.circuit_breaker_triggered:
            self._log(f"[!] TRIP-SITTER ALERT: Circuit breaker triggered at Peak: {peak_eval.intervention_notes}")
            antagonist_msg = self.sitter.apply_emergency_antagonist(self.template.state)
            self._log(f"[!] {antagonist_msg}")

        if on_stage_complete:
            on_stage_complete(LifecycleStage.PEAK, peak_output)
        self._log(f"[Peak Breakthrough]:\n{peak_output[:300]}...")

        # STAGE 4: RETURN & INTEGRATION
        self.template.state.transition_to_stage(LifecycleStage.RETURN)
        self._log(f"\n--- STAGE 4: RETURN (Re-annealing pi_P = {self.template.state.get_prior_precision():.2f}, Grounding Gate) ---")
        prompt_4 = self.template.build_return_prompt(task, baseline_output, peak_output)
        params_4 = self.template.rebus.get_sampling_hyperparameters()
        return_output = self.adapter.generate(prompt_4, hyperparameters=params_4)
        
        # Trip-Sitter evaluation of Return deliverable
        return_eval = self.sitter.evaluate_output(return_output, LifecycleStage.RETURN, task, baseline_output)
        coherence_audit["return_evaluation"] = return_eval.model_dump()

        if on_stage_complete:
            on_stage_complete(LifecycleStage.RETURN, return_output)
        self._log(f"[Actionable Deliverable]:\n{return_output[:300]}...")

        # Ground deliverable into structured artifact
        grounded_artifact = self.grounder.ground(return_output, peak_output)

        # Construct validated deliverable
        result = self.template.parse_breakthrough(
            task=task,
            baseline=baseline_output,
            peak=peak_output,
            deliverable=return_output,
            orthogonal_domain_name=self.template.stiefel.select_orthogonal_domain(task).name,
        )
        result.metadata["coherence_audit"] = coherence_audit
        result.metadata["grounded_artifact"] = grounded_artifact.model_dump()

        self._log(f"\n[+] Neuro-cognitive trajectory complete. Readiness Score: {grounded_artifact.readiness_score}/100")
        return result

    def _log(self, msg: str):
        if self.verbose:
            print(msg)
