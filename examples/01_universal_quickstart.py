"""
Example 01: Universal Quickstart.
Demonstrates running ANY generic task through the 4-stage neurochemical trajectory in 5 lines of code.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from psychoactive import NeuroSession, UniversalTemplate, CompoundType, MockModelAdapter


def main():
    print("=" * 70)
    print("Example 01: Universal Problem Solving with Psilocybin Mode")
    print("=" * 70)

    # 1. Define any arbitrary task across any domain
    task = "How can an independent coffee shop compete with a Starbucks opening across the street?"

    # 2. Initialize NeuroSession (Using MockModelAdapter for zero-cost offline demonstration)
    # For live models: session = NeuroSession(model="gpt-4o", compound=CompoundType.PSILOCYBIN)
    session = NeuroSession(
        template=UniversalTemplate(domain_name="Retail Business Strategy", compound=CompoundType.PSILOCYBIN, dose=0.85),
        adapter=MockModelAdapter(),
        verbose=True,
    )

    # 3. Execute the 4-stage trajectory (Baseline -> Ascent -> Peak -> Return)
    result = session.run(task)

    # 4. Inspect the validated breakthrough deliverable
    print("\n" + "=" * 70)
    print("FINAL GROUNDED BREAKTHROUGH ARTIFACT:")
    print("=" * 70)
    print(f"Domain: {result.domain}")
    print(f"Compound Applied: {result.compound_used} (Dose: {result.dosage})")
    print(f"Orthogonal Analogy: {result.orthogonal_analogy}")
    print("\n[Actionable Deliverable]:\n" + result.actionable_deliverable)
    print("\n[Telemetry]:")
    print(f"Readiness Score: {result.metadata['grounded_artifact']['readiness_score']}/100")
    print(f"Prior Precision at Peak: {result.metadata['prior_precision_pi_P']}")


if __name__ == "__main__":
    main()
