"""
Example 03: Software Architecture Breakthrough.
Demonstrates resolving a distributed locking deadlock in high-throughput microservices
using Psilocybin Mode (REBUS prior precision relaxation + fungal stigmergy).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from psychoactive import (
    NeuroSession,
    EngineeringTemplate,
    CompoundType,
    MockModelAdapter,
)


def main():
    print("=" * 80)
    print("Example 03: Distributed Systems Architecture - Breaking Lock Contention")
    print("=" * 80)

    task = "Eliminate distributed locking deadlocks in a high-frequency financial settlement engine."

    template = EngineeringTemplate(
        tech_stack="Rust / Distributed Raft",
        compound=CompoundType.PSILOCYBIN,
        dose=0.95,
    )

    session = NeuroSession(
        template=template,
        adapter=MockModelAdapter(),
        verbose=True,
    )

    result = session.run(task)

    print("\n" + "=" * 80)
    print("DISTRIBUTED ENGINE ARCHITECTURAL BREAKTHROUGH:")
    print("=" * 80)
    print(f"Tech Stack: {template.tech_stack}")
    print(f"Prior Precision (pi_P at Peak): {result.metadata['prior_precision_pi_P']}")
    print(f"\n[Grounded Architecture Specification]:\n{result.actionable_deliverable}")


if __name__ == "__main__":
    main()
