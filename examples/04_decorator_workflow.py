"""
Example 04: The 1-Line Psychoactive Decorator Workflow.
Demonstrates wrapping existing functions or agent tools with @psychoactive.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from psychoactive import psychoactive, CompoundType, MockModelAdapter


# Wrap an existing sales pitch generator with 1 line of code
@psychoactive(compound=CompoundType.THC, dose=0.85, adapter=MockModelAdapter(), verbose=True)
def generate_viral_hook(product_pitch: str) -> str:
    """
    Standard function body is intercepted and automatically driven
    through the 4-stage neurochemical trajectory.
    """
    return product_pitch


def main():
    print("=" * 80)
    print("Example 04: 1-Line Interceptor Decorator (@psychoactive)")
    print("=" * 80)

    prompt = "How can a developer tooling startup market a new SQLite embedding database?"
    
    # Direct execution of the decorated function
    grounded_output = generate_viral_hook(prompt)

    print("\n" + "=" * 80)
    print("DECORATOR EXECUTION OUTPUT:")
    print("=" * 80)
    print(grounded_output)


if __name__ == "__main__":
    main()
