"""
Command-Line Interface (CLI) for Psychoactive AI Cognition.
Allows humans and autonomous agents (Antigravity, Claude Code, Codex)
to execute 4-stage neurochemical reasoning from the terminal.
"""

import sys
import argparse
import json
from typing import Optional

from psychoactive.compounds import CompoundType, COMPOUND_REGISTRY
from psychoactive.templates import (
    UniversalTemplate,
    SalesTemplate,
    EngineeringTemplate,
    StrategyTemplate,
    CreativeTemplate,
    NeuroTemplate,
)
from psychoactive.adapters.base import MockModelAdapter
from psychoactive.adapters.universal_llm import UniversalLLMAdapter
from psychoactive.session import NeuroSession


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="psychoactive",
        description="Psychoactive: Universal Neurochemical Cognitive Meta-Layer for LLMs & AI Agents",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Execute 4-stage neurochemical reasoning on a task")
    run_parser.add_argument("task", type=str, help="Problem, prompt, or challenge description")
    run_parser.add_argument(
        "--compound", "-c",
        type=str,
        default="psilocybin",
        choices=["psilocybin", "thc", "entourage", "microdose", "baseline"],
        help="Pharmacological compound profile (default: psilocybin)"
    )
    run_parser.add_argument(
        "--dose", "-d",
        type=float,
        default=0.85,
        help="Normalized dosage in [0.0, 1.0] (default: 0.85)"
    )
    run_parser.add_argument(
        "--template", "-t",
        type=str,
        default="universal",
        choices=["universal", "sales", "engineering", "strategy", "creative"],
        help="Domain template preset (default: universal)"
    )
    run_parser.add_argument(
        "--model", "-m",
        type=str,
        default="mock",
        help="Model identifier (e.g. gpt-4o, claude-3-5-sonnet, gemini/gemini-1.5-pro, ollama/llama3, or 'mock')"
    )
    run_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print real-time stage transitions (Baseline -> Ascent -> Peak -> Return)"
    )
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Output complete result telemetry as JSON"
    )

    # Command: compounds
    subparsers.add_parser("compounds", help="List supported compounds and their cognitive effects")

    # Command: templates
    subparsers.add_parser("templates", help="List available domain templates")

    return parser


def select_template(template_name: str, compound: str, dose: float) -> NeuroTemplate:
    c_type = CompoundType(compound.lower())
    t = template_name.lower()
    if t == "sales":
        return SalesTemplate(compound=c_type, dose=dose)
    elif t == "engineering":
        return EngineeringTemplate(compound=c_type, dose=dose)
    elif t == "strategy":
        return StrategyTemplate(compound=c_type, dose=dose)
    elif t == "creative":
        return CreativeTemplate(compound=c_type, dose=dose)
    return UniversalTemplate(compound=c_type, dose=dose)


def main():
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "compounds":
        print("\nSupported Neurochemical Compounds:")
        print("=" * 70)
        for c_type, profile in COMPOUND_REGISTRY.items():
            print(f"• {c_type.value.upper()}: {profile.name}")
            print(f"  Description: {profile.description}")
            print(f"  Target Receptors: 5-HT2A (Ki={profile.receptor_affinities.five_ht2a_ki}nM), CB1 (Ki={profile.receptor_affinities.cb1_ki}nM)")
            print(f"  Max Prior Relaxation: {profile.base_prior_relaxation_max} | Gating Lambda: {profile.retrograde_gating_lambda}\n")
        return

    elif args.command == "templates":
        print("\nAvailable Domain Presets (Jack of All Trades):")
        print("=" * 70)
        print("• universal:   Universal meta-template for any task, problem, or prompt.")
        print("• sales:       B2B sales cold outreach, positioning, and pattern interrupts.")
        print("• engineering: Software architecture, concurrency deadlocks, and algorithms.")
        print("• strategy:    Asymmetric business moats and counter-intuitive market strategy.")
        print("• creative:    Screenwriting, narrative worldbuilding, and anti-cliché prose.\n")
        return

    elif args.command == "run":
        template = select_template(args.template, args.compound, args.dose)

        if args.model.lower() == "mock":
            adapter = MockModelAdapter()
        else:
            adapter = UniversalLLMAdapter(model=args.model)

        session = NeuroSession(
            template=template,
            adapter=adapter,
            verbose=args.verbose,
        )

        result = session.run(args.task)

        if args.json:
            print(json.dumps(result.model_dump(), indent=2))
        else:
            print("\n" + "=" * 70)
            print("PSYCHOACTIVE BREAKTHROUGH DELIVERABLE")
            print("=" * 70)
            print(f"Domain: {result.domain}")
            print(f"Compound: {result.compound_used} (Dose: {result.dosage})")
            print(f"Orthogonal Analogy: {result.orthogonal_analogy}")
            print(f"Readiness Score: {result.metadata.get('grounded_artifact', {}).get('readiness_score', 'N/A')}/100")
            print("\n[Actionable Deliverable]:\n")
            print(result.actionable_deliverable)
            print("=" * 70)


if __name__ == "__main__":
    main()
