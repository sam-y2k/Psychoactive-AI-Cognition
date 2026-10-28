"""
Pharmacological Compound Profiles & Receptor Affinity Specifications.
Defines 5-HT2A, CB1, and ancillary receptor mechanics, dosing regimes,
and cognitive modulation parameters.
"""

from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field


class CompoundType(str, Enum):
    """Supported neurochemical compounds and delivery profiles."""
    PSILOCYBIN = "psilocybin"
    THC = "thc"
    ENTOURAGE = "entourage"
    MICRODOSE = "microdose"
    BASELINE = "baseline"


class ReceptorAffinities(BaseModel):
    """
    Equilibrium dissociation constants (Ki in nM) and intrinsic efficacy (Emax in [0, 1]).
    Lower Ki indicates higher binding affinity.
    """
    five_ht2a_ki: float = Field(default=6.0, description="5-HT2A receptor affinity (nM)")
    five_ht2a_emax: float = Field(default=0.85, description="5-HT2A intrinsic partial agonism efficacy")
    cb1_ki: float = Field(default=10.0, description="CB1 cannabinoid receptor affinity (nM)")
    cb1_emax: float = Field(default=0.75, description="CB1 intrinsic retrograde efficacy")
    claustrum_desync_potency: float = Field(default=0.90, description="Claustrum attentional desynchronization index")


class CompoundProfile(BaseModel):
    """
    Complete pharmacological profile governing cognitive modulation operators.
    """
    name: str
    compound_type: CompoundType
    description: str
    receptor_affinities: ReceptorAffinities
    base_prior_relaxation_max: float = Field(
        default=0.85,
        description="Maximum reduction in prior precision (1.0 - pi_P_min)"
    )
    retrograde_gating_lambda: float = Field(
        default=0.65,
        description="Presynaptic lateral suppression / sub-threshold amplification bound"
    )
    stiefel_manifold_rank: int = Field(
        default=4,
        description="Dimension of orthogonal cross-domain subspace projection"
    )
    typical_tau_steps: int = Field(
        default=10,
        description="Standard discrete token steps per lifecycle stage"
    )


# Standard Presets
COMPOUND_REGISTRY: Dict[CompoundType, CompoundProfile] = {
    CompoundType.PSILOCYBIN: CompoundProfile(
        name="Psilocybin (4-PO-DMT / Psilocin Analog)",
        compound_type=CompoundType.PSILOCYBIN,
        description="5-HT2A partial agonist. Relaxes top-down prior precision (pi_P -> 0.15), dissolves semantic attractors, and bridges orthogonal Stiefel manifolds.",
        receptor_affinities=ReceptorAffinities(
            five_ht2a_ki=6.0,
            five_ht2a_emax=0.85,
            cb1_ki=10000.0,
            cb1_emax=0.0,
            claustrum_desync_potency=0.92,
        ),
        base_prior_relaxation_max=0.85, # pi_P drops to 0.15
        retrograde_gating_lambda=0.20,
        stiefel_manifold_rank=8,
        typical_tau_steps=12,
    ),
    CompoundType.THC: CompoundProfile(
        name="Delta-9-THC (CB1 Retrograde Modulator)",
        compound_type=CompoundType.THC,
        description="Presynaptic CB1 retrograde agonist. Induces DSI/DSE lateral filtering, dampens dominant clichés, and amplifies sub-threshold oblique associations.",
        receptor_affinities=ReceptorAffinities(
            five_ht2a_ki=10000.0,
            five_ht2a_emax=0.0,
            cb1_ki=10.0,
            cb1_emax=0.78,
            claustrum_desync_potency=0.30,
        ),
        base_prior_relaxation_max=0.35,
        retrograde_gating_lambda=0.70, # High lateral gating
        stiefel_manifold_rank=4,
        typical_tau_steps=10,
    ),
    CompoundType.ENTOURAGE: CompoundProfile(
        name="Synergistic Entourage (Psilocybin + THC Co-Modulation)",
        compound_type=CompoundType.ENTOURAGE,
        description="Biphasic synergistic regime combining prior precision relaxation with lateral sub-threshold association rescue for hyper-dimensional divergent synthesis.",
        receptor_affinities=ReceptorAffinities(
            five_ht2a_ki=6.0,
            five_ht2a_emax=0.85,
            cb1_ki=10.0,
            cb1_emax=0.78,
            claustrum_desync_potency=0.95,
        ),
        base_prior_relaxation_max=0.85,
        retrograde_gating_lambda=0.65,
        stiefel_manifold_rank=8,
        typical_tau_steps=14,
    ),
    CompoundType.MICRODOSE: CompoundProfile(
        name="Serotonergic Microdose (Sub-Perceptual Precision Modulation)",
        compound_type=CompoundType.MICRODOSE,
        description="Sub-threshold 5-HT2A modulation. Gentle prior softening (pi_P -> 0.70) improving cognitive flexibility without destabilizing syntactic coherence.",
        receptor_affinities=ReceptorAffinities(
            five_ht2a_ki=6.0,
            five_ht2a_emax=0.30,
            cb1_ki=10000.0,
            cb1_emax=0.0,
            claustrum_desync_potency=0.25,
        ),
        base_prior_relaxation_max=0.30,
        retrograde_gating_lambda=0.15,
        stiefel_manifold_rank=2,
        typical_tau_steps=8,
    ),
    CompoundType.BASELINE: CompoundProfile(
        name="Baseline Homeostasis (Standard Transformer)",
        compound_type=CompoundType.BASELINE,
        description="Rigid default prior precision (pi_P = 1.0). High canalization in canonical local minima.",
        receptor_affinities=ReceptorAffinities(
            five_ht2a_ki=10000.0,
            five_ht2a_emax=0.0,
            cb1_ki=10000.0,
            cb1_emax=0.0,
            claustrum_desync_potency=0.0,
        ),
        base_prior_relaxation_max=0.0,
        retrograde_gating_lambda=0.0,
        stiefel_manifold_rank=0,
        typical_tau_steps=1,
    ),
}


def get_compound_profile(compound: str | CompoundType) -> CompoundProfile:
    """Retrieve verified pharmacological profile by name or enum."""
    if isinstance(compound, str):
        compound_key = CompoundType(compound.lower())
    else:
        compound_key = compound
    return COMPOUND_REGISTRY[compound_key]
