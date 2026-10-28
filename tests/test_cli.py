"""
Unit tests for the psychoactive CLI tool.
"""

import pytest
import subprocess
import json
from psychoactive.cli import build_parser, select_template
from psychoactive.templates import SalesTemplate, UniversalTemplate, EngineeringTemplate


def test_cli_parser_defaults():
    """Verify CLI parser sets correct default arguments."""
    parser = build_parser()
    args = parser.parse_args(["run", "Optimize database indexing"])
    assert args.command == "run"
    assert args.task == "Optimize database indexing"
    assert args.compound == "psilocybin"
    assert args.dose == 0.85
    assert args.template == "universal"
    assert args.model == "mock"


def test_cli_template_selection():
    """Verify select_template returns appropriate template classes."""
    t_sales = select_template("sales", "thc", 0.90)
    assert isinstance(t_sales, SalesTemplate)

    t_eng = select_template("engineering", "psilocybin", 0.95)
    assert isinstance(t_eng, EngineeringTemplate)

    t_univ = select_template("universal", "entourage", 0.80)
    assert isinstance(t_univ, UniversalTemplate)


def test_cli_execution_mock():
    """Verify running the CLI module via subprocess produces expected formatted output."""
    cmd = [
        "python", "-m", "psychoactive.cli",
        "run", "Break corporate sales email fatigue",
        "--template", "sales",
        "--compound", "thc",
        "--model", "mock"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "PSYCHOACTIVE BREAKTHROUGH DELIVERABLE" in res.stdout
    assert "Actionable Deliverable" in res.stdout


def test_cli_json_output():
    """Verify --json flag outputs parseable JSON telemetry."""
    cmd = [
        "python", "-m", "psychoactive.cli",
        "run", "Design lock-free queue",
        "--model", "mock",
        "--json"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert "actionable_deliverable" in data
    assert "canonical_cliche" in data
    assert "dosage" in data
