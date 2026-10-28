"""
Example 02: Out-of-the-Box B2B Sales Campaign Transformation.
Demonstrates how an enterprise sales team escapes boring template fatigue (0.5% response rates)
by using the THC / Psilocybin cognitive template.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from psychoactive import (
    NeuroSession,
    SalesTemplate,
    CompoundType,
    MockModelAdapter,
    BreakthroughResult,
)


def run_sales_experiment():
    print("=" * 80)
    print("Example 02: B2B Enterprise Sales Ideation - Escaping the Corporate Cliché")
    print("=" * 80)

    product = "Automated Kubernetes Cost Optimization & Autonomous Cloud FinOps"
    icp = "VP of Cloud Infrastructure / CTO at Fortune 500 Enterprises"
    task = "Break into skeptical tech executives who ignore standard 'Save 30% on AWS' pitch emails."

    # Custom simulated responses highlighting the contrast between Baseline and Grounded Breakthrough
    custom_responses = {
        "STAGE 1: CANONICAL BASELINE": (
            "[CANONICAL BASELINE]\n"
            "Subject: Quick question about your AWS cloud spend\n\n"
            "Hi {First_Name},\n"
            "I noticed you manage infrastructure at {Company}. Cloud costs are rising fast. "
            "Our AI-driven platform helps teams optimize compute waste by up to 30% without downtime.\n"
            "Do you have 15 minutes this Thursday for a quick introductory chat?\n\n"
            "Best,\nJohn (Senior Account Executive)"
        ),
        "STAGE 2: ASCENT": (
            "[DISMANTLED ASSUMPTIONS]\n"
            "1. CTOs care about 'saving 30% on AWS' — in reality, they view cost reduction as unsexy and risk-inducing.\n"
            "2. Asking for a '15-minute call' creates instant cognitive resistance.\n"
            "3. Positioning the product as 'cost optimization' groups us into a commodity bucket with 50 other spam vendors."
        ),
        "STAGE 3: PEAK": (
            "[PEAK BREAKTHROUGH]\n"
            "Isomorphic Mapping onto Submarine Stealth & Acoustic Cavitation:\n"
            "In submarine warfare, cavitation isn't about saving fuel — it's about eliminating acoustic anomalies "
            "that reveal the vessel's coordinates to passive enemy sonar. Cloud waste is not a finance problem; "
            "it is an architectural acoustic anomaly that reveals engineering debt and latent cluster instability.\n"
            "Reframe the campaign from 'Save Money' to 'Eliminating Infrastructure Cavitation Before Q4 Audits'."
        ),
        "STAGE 4: INTEGRATION": (
            "[PARADIGM SHIFT]: Replaced passive cost-savings pitch with infrastructure acoustic stability audit.\n"
            "[THE MECHANISM]: Submarine acoustic cavitation model — treating orphaned cloud compute as hidden operational vulnerabilities.\n"
            "[ACTIONABLE DELIVERABLE]:\n"
            "Subject: Your EKS cluster cavitation index\n\n"
            "{First_Name} — Most infrastructure leads optimize for cloud discounts while ignoring cluster cavitation.\n\n"
            "When orphaned dev nodes spin unchecked across multi-AZ clusters, the threat isn't just a 20% billing bleed. "
            "It's the invisible telemetry noise masking silent latency spikes right before deployment freezes.\n\n"
            "We built a read-only probe that measures your exact cluster cavitation footprint in 3 minutes via CLI.\n\n"
            "Worth sending over the 1-line curl command to run internally, or is this not on your radar right now?\n"
            "— Samagra"
        ),
    }

    # Initialize SalesTemplate with THC (for sub-threshold lateral associations)
    template = SalesTemplate(
        product=product,
        icp=icp,
        compound=CompoundType.THC,
        dose=0.90,
    )

    session = NeuroSession(
        template=template,
        adapter=MockModelAdapter(responses=custom_responses),
        verbose=True,
    )

    result: BreakthroughResult = session.run(task)

    print("\n" + "=" * 80)
    print("SALES CAMPAIGN TRANSFORMATION RESULT:")
    print("=" * 80)
    print(f"Product: {product}")
    print(f"Target ICP: {icp}")
    print(f"Compound Mode: {result.compound_used}")
    print(f"\n[Dismantled Cliché]:\n{result.canonical_cliche}\n")
    print(f"[The Out-of-the-Box Pitch Sequence]:\n{result.actionable_deliverable}\n")
    print(f"Readiness Score: {result.metadata['grounded_artifact']['readiness_score']}/100")


if __name__ == "__main__":
    run_sales_experiment()
