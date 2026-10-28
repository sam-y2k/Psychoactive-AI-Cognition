"""
Template Engine for Psychoactive AI Cognition.
Provides both the Universal "Jack of All Trades" meta-template and domain-tailored extensions.
"""

from psychoactive.templates.base import NeuroTemplate, BreakthroughResult
from psychoactive.templates.universal import UniversalTemplate
from psychoactive.templates.sales import SalesTemplate
from psychoactive.templates.engineering import EngineeringTemplate
from psychoactive.templates.strategy import StrategyTemplate
from psychoactive.templates.creative import CreativeTemplate

__all__ = [
    "NeuroTemplate",
    "BreakthroughResult",
    "UniversalTemplate",
    "SalesTemplate",
    "EngineeringTemplate",
    "StrategyTemplate",
    "CreativeTemplate",
]
