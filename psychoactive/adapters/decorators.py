"""
Decorator API for Psychoactive Cognitive Steerage.
Allows wrapping existing Python functions, tools, and agent workflows with a single line.
"""

from functools import wraps
from typing import Callable, Any, Optional
from psychoactive.compounds import CompoundType
from psychoactive.templates.base import NeuroTemplate, BreakthroughResult
from psychoactive.templates.universal import UniversalTemplate
from psychoactive.adapters.base import BaseModelAdapter
from psychoactive.session import NeuroSession


def psychoactive(
    compound: str | CompoundType = CompoundType.PSILOCYBIN,
    dose: float = 0.85,
    model: str = "gpt-4o",
    template: Optional[NeuroTemplate] = None,
    adapter: Optional[BaseModelAdapter] = None,
    return_full_result: bool = False,
    verbose: bool = False,
):
    """
    Decorator that intercepts a function call and routes its first string argument
    through the 4-stage psychoactive cognitive journey.

    Example:
        @psychoactive(compound="thc", dose=0.80)
        def generate_campaign(product_description: str) -> str:
            pass  # Intercepted and replaced with grounded psychoactive output
    """
    def decorator(fn: Callable[..., Any]):
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract task string from args or kwargs
            task_str = ""
            if args and isinstance(args[0], str):
                task_str = args[0]
            elif "task" in kwargs:
                task_str = str(kwargs["task"])
            elif "prompt" in kwargs:
                task_str = str(kwargs["prompt"])
            else:
                # If function returns a string prompt, use its return value as task
                candidate = fn(*args, **kwargs)
                if isinstance(candidate, str):
                    task_str = candidate
                else:
                    task_str = str(args)

            session = NeuroSession(
                template=template or UniversalTemplate(compound=compound, dose=dose),
                adapter=adapter,
                model=model,
                compound=compound,
                dose=dose,
                verbose=verbose,
            )

            result: BreakthroughResult = session.run(task_str)

            if return_full_result:
                return result
            return result.actionable_deliverable

        return wrapper
    return decorator
