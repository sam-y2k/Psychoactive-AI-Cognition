# `psychoactive`: Universal Neurochemical Cognitive Meta-Layer for Large Language Models

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-46%20passed-brightgreen.svg)]()
[![Neurochemical-AI](https://img.shields.io/badge/Paper-Singh%20(2026)-purple.svg)]()

> **"A Jack-of-All-Trades cognitive meta-layer that injects psilocybin and cannabinoid mechanics into any LLM to systematically dissolve mode collapse, escape canonical clichés, and discover out-of-the-box breakthroughs across any domain."**

---

## ⚡ The Problem: Semantic Mode Collapse

Standard autoregressive Large Language Models suffer from **inductive sclerosis**: when prompted with a high-stakes problem, they greedily converge onto the most probable, generic local minimum in their training weights ($U(\mathbf{v})$):
- **In B2B Sales:** Generic *"Hop on a quick 15-minute call"* cold emails that convert at $<0.5\%$.
- **In Software Architecture:** Naive two-phase commit locks that deadlock under scale.
- **In Business Strategy:** Commoditized SaaS playbooks with zero defensive moats.
- **In Creative Writing:** Formulaic, sterile prose riddled with AI tropes (*"a testament to"*, *"tapestry"*).

Merely increasing stochastic temperature introduces isotropic noise, producing syntactic delirium rather than structured insight.

---

## 🍄 The Solution: Neurochemical Modulation

`psychoactive` is a **universal cognitive middleware** that sits on top of **any LLM** (OpenAI, Anthropic Claude, Google Gemini, Ollama, local models) and applies the biophysical mechanics of psychoactive compounds:

1. **Psilocybin Mode ($5\text{-HT}_{2A}$ Partial Agonism / REBUS)**:
   - **Prior Precision Relaxation ($\pi_P \to 0.15$)**: Decomposes attention logits ($A_{ij} = L_{ij} + \pi_P P_{ij}$) to dissolve semantic attractor basins.
   - **Stiefel Manifold Projection ($B \in \mathcal{V}_k(\mathbb{R}^d)$)**: Projects problems onto orthogonal disciplines (Fungal Ecology, Cellular Immunology, Hostage Negotiation, Hydrodynamics) to discover novel architectural configurations.
2. **$\Delta^9$-THC Mode ($\text{CB}_1$ Presynaptic Retrograde Gating)**:
   - **Sub-Threshold Salience Amplification**: Applies DSI/DSE lateral filtering ($\lambda \le 0.70$) to suppress dominant clichéd tokens and rescue oblique, high-potential candidate ideas normally discarded by greedy decoders.
3. **The Trip-Sitter Integration Gate**:
   - Automated cognitive supervisor that halts runaways, prevents mode stuttering, and anneals high-entropy conceptual breakthroughs back into concrete, line-by-line deliverables.

---

## 🔌 Plug & Play Agent Skill (Antigravity, Claude Code, Codex, Cursor)

`psychoactive` is packaged both as a Python library and as a **standard Agent Skill** that can be dropped directly into any autonomous agent environment to give the agent out-of-the-box reasoning capabilities.

### 1. Installation into AI Agent Environments

#### In Google Antigravity / Gemini Code Assist:
Copy or symlink the skill directory to your Antigravity skills repository:
```bash
# Windows PowerShell
Copy-Item -Recurse -Path "D:\Agentic Ai\Projects\Research papers\Psychoactive_AI_Cognition\AI-psychoactive-code\skills\psychoactive-cognition" -Destination "$HOME\.gemini\config\skills\"

# Linux / macOS
cp -r ./skills/psychoactive-cognition ~/.gemini/config/skills/
```

#### In Claude Code (Anthropic):
```bash
# Copy into global Claude Code skills
mkdir -p ~/.claude/skills/
cp -r ./skills/psychoactive-cognition ~/.claude/skills/

# Or copy into your current project repo
mkdir -p .claude/skills/
cp -r ./skills/psychoactive-cognition .claude/skills/
```

#### In OpenAI Codex / Custom Agent Harnesses:
```bash
# Copy into agent skills directory
mkdir -p ~/.codex/skills/
cp -r ./skills/psychoactive-cognition ~/.codex/skills/
```

---

## 💻 Terminal CLI Usage

Install the package into your environment:
```bash
git clone https://github.com/sam-y2k/Psychoactive-AI-Cognition.git
cd AI-psychoactive-code
pip install -e .
```

Run directly from the terminal or have your AI agent invoke it:

```bash
# 1. Universal Problem Solving (Psilocybin Mode)
psychoactive run "How to compete with an incumbent having 100x our budget?" --compound psilocybin

# 2. Out-of-the-Box B2B Sales Campaign (THC Mode)
psychoactive run "Sell Kubernetes FinOps to skeptical CISOs" --template sales --compound thc --model gpt-4o

# 3. Distributed Architecture Bottleneck (Psilocybin Mode)
psychoactive run "Eliminate two-phase commit lock contention" --template engineering --model claude-3-5-sonnet

# 4. Structured JSON Output (For programmatic agent pipelines)
psychoactive run "Startup competitive positioning" --template strategy --json

# 5. List available compounds & receptor affinities
psychoactive compounds
```

---

## 🚀 Python SDK Quickstart (5 Lines of Code)

Works out of the box with zero lock-in:

```python
from psychoactive import NeuroSession, UniversalTemplate, CompoundType

# 1. Initialize session with chosen compound
session = NeuroSession(
    template=UniversalTemplate(domain_name="Retail Strategy", compound=CompoundType.PSILOCYBIN, dose=0.85),
    model="gpt-4o"  # Supports claude-3-5-sonnet, gemini/gemini-1.5-pro, ollama/llama3
)

# 2. Run any task through the 4-stage neurochemical trajectory
result = session.run("How can an independent coffee shop compete with Starbucks opening across the street?")

# 3. Access the structured, grounded breakthrough
print(result.actionable_deliverable)
```

---

## 🎯 Jack of All Trades: Pre-Built Domain Presets

The framework is completely domain-agnostic. Pre-built templates provide instant out-of-the-box workflows:

### 1. B2B Sales & Outbound Ideation (`SalesTemplate`)
Transforms commoditized outbound sales emails into unignorable pattern-interrupt campaigns.
```python
from psychoactive import NeuroSession, SalesTemplate, CompoundType

template = SalesTemplate(
    product="Kubernetes FinOps & Autonomous Node Optimization",
    icp="VP of Cloud Infrastructure / CTO",
    compound=CompoundType.THC, # Sub-threshold lateral hooks
    dose=0.90
)
session = NeuroSession(template=template, model="gpt-4o")
result = session.run("Break into skeptical Fortune 500 tech leaders.")
```

### 2. Software & Systems Architecture (`EngineeringTemplate`)
Breaks concurrency deadlocks, race conditions, and distributed consensus bottlenecks.
```python
from psychoactive import NeuroSession, EngineeringTemplate, CompoundType

template = EngineeringTemplate(tech_stack="Rust / Tokio", compound=CompoundType.PSILOCYBIN)
session = NeuroSession(template=template, model="claude-3-5-sonnet")
result = session.run("Eliminate distributed lock contention in global multi-region transactional ledger.")
```

### 3. Business Strategy & Market Moats (`StrategyTemplate`)
Synthesizes asymmetric advantages and counter-intuitive business models.
```python
from psychoactive import NeuroSession, StrategyTemplate, CompoundType

template = StrategyTemplate(industry="Cybersecurity", compound=CompoundType.ENTOURAGE)
session = NeuroSession(template=template)
result = session.run("Construct a moat against an incumbent with 100x our budget.")
```

---

## 🔮 The 1-Line Function & Agent Decorator (`@psychoactive`)

Drop `@psychoactive` onto any existing Python function, LangChain tool, or CrewAI agent:

```python
from psychoactive import psychoactive, CompoundType

@psychoactive(compound=CompoundType.PSILOCYBIN, dose=0.85, model="gpt-4o")
def solve_strategy_problem(prompt: str) -> str:
    """Original function is intercepted and driven through the 4-stage trajectory."""
    pass

# Execute normally - output is automatically decanalized and grounded
output = solve_strategy_problem("How do we position a developer tool in a crowded market?")
```

---

## 🛡️ The Trip-Sitter Safety Guardrail

The **Trip-Sitter** supervisor runs automatically during every session:
- **Syntactic Collapse Breaker:** Catches degenerate output (<20 characters).
- **Mode-Stutter Breaker:** Detects repetitive token stuttering (low trigram and vocabulary entropy).
- **Emergency Antagonist Protocol:** Forces immediate re-annealing to baseline prior precision ($\pi_P = 1.0$) if safety thresholds are breached.
- **Readiness Scoring:** The `IntegrationGrounder` scores each deliverable from 0–100, checking for concrete scripts, code, and absence of generic buzzwords.

---

## 🔬 Core Mathematical Solvers & PyTorch Modules

Beyond prompt steerage, `psychoactive` includes production-grade mathematical solvers, PyTorch tensor layers, formal verification engines, and empirical benchmarks directly implementing the research paper:

### 1. Native PyTorch Modules (`psychoactive.nn`)
```python
import torch
from psychoactive.nn import REBUSMultiHeadAttention, CB1RetrogradeLayer

# Drop-in decomposed attention layer: A_ij = L_ij + pi_P * P_ij
attn_layer = REBUSMultiHeadAttention(embed_dim=64, num_heads=4, prior_rank=8)
x = torch.randn(2, 16, 64)

# Execute forward pass with acute prior relaxation (pi_P = 0.15)
output, telemetry = attn_layer(x, x, x, prior_precision=0.15, return_telemetry=True)
print(f"Mean attention entropy: {telemetry.mean_entropy:.2f} nats, Horizon: {telemetry.effective_horizon:.1f} tokens")

# Presynaptic retrograde gating: h_tilde = h * (1 + mu * g_CB1)
retro_layer = CB1RetrogradeLayer(hidden_dim=64, max_lambda_dse=0.70)
h_modulated, diag = retro_layer(x, retrograde_strength=1.0, return_diagnostics=True)
```

### 2. Pure Mathematical Solvers (`psychoactive.math`)
```python
from psychoactive.math import (
    OrthogonalProcrustesSolver,
    PersistentHomologyEngine,
    compute_newman_modularity,
    LangevinAttractorSimulator,
    AttractorLandscape,
)

# A. Stiefel Manifold Orthogonal Procrustes Solver: min ||Z_src B - Z_tgt||_F s.t. B^T B = I
solver = OrthogonalProcrustesSolver()
result = solver.solve(z_source=source_embeddings, z_target=target_embeddings)
print(f"Orthonormality certified: {result.is_orthonormal}, Alignment error: {result.alignment_error:.4f}")

# B. Persistent Homology & Betti Numbers (Vietoris-Rips filtration)
engine = PersistentHomologyEngine(persistence_threshold=0.15)
dist_matrix = engine.compute_distance_matrix(head_representations)
filtration = engine.compute_filtration(dist_matrix, num_steps=30)
intervals = engine.extract_persistence_intervals(filtration)

# C. Free-Energy Thermodynamic Langevin Simulator (Attractor Dissolution Theorem)
landscape = AttractorLandscape(dim=2, base_barrier_height=6.0)
sim = LangevinAttractorSimulator(landscape, gamma_inv=0.25)
p_escape = sim.estimate_escape_probability(prior_precision=0.05, num_trials=50)
print(f"Escape probability under REBUS phase: {p_escape * 100:.1f}%")
```

### 3. Deterministic Formal Verification Gate (`psychoactive.verification`)
```python
from psychoactive.verification import Z3ConstraintVerifier, LogicalConstraint, LateralDivergenceEvaluator

# Real Z3 Theorem Prover constraint verification
verifier = Z3ConstraintVerifier()
proof = verifier.verify_numeric_bounds(
    candidate_values={"lambda_dse": 0.45, "temperature": 0.85},
    constraints=[LogicalConstraint("DSE Ceiling", "lambda_dse", "<=", 0.70)]
)
assert proof.is_satisfiable, "Violation triggers Antagonist Reset (pi_P <- 1.0)"

# Lateral Divergence Metric (LDM)
evaluator = LateralDivergenceEvaluator()
ldm_res = evaluator.evaluate(v_neuro=v_neuro, v_baseline=v_base, completion_text="Valid breakthrough syntax.")
print(f"LDM Score: {ldm_res.ldm_score:.4f}, Valid: {ldm_res.is_valid_breakthrough}")
```

---

## 🧪 Pharmacological Compounds Supported

| Compound | Target Receptor | Primary Effect | Best For |
|---|---|---|---|
| `psilocybin` | $5\text{-HT}_{2A}$ Partial Agonist | Prior Precision Relaxation ($\pi_P \to 0.15$) + Stiefel Bridges | Architectural shifts, hard engineering deadlocks, paradigm flips |
| `thc` | $\text{CB}_1$ Retrograde Agonist | Lateral Presynaptic Filtering + Sub-threshold Salience Boost | Unconventional sales hooks, lateral humor, marketing angles |
| `entourage` | $5\text{-HT}_{2A} + \text{CB}_1$ Synergy | Dual prior relaxation and lateral salience amplification | High-stakes strategy, cross-disciplinary breakthroughs |
| `microdose` | $5\text{-HT}_{2A}$ Sub-Perceptual | Gentle prior softening ($\pi_P \to 0.70$), high syntactic stability | Real-time coding, continuous drafting, subtle ideation |

---

## 📖 Scientific Citation

If you use `psychoactive` in your research or production systems, please cite the foundational pre-print:

```bibtex
@article{singh2026neurochemical,
  title={Neurochemical Modulation of Artificial Neural Networks: Formalizing Psilocybin and Psychoactive Dynamics as Search-Space Optimization},
  author={Singh, Samagra},
  journal={Preprint},
  year={2026}
}
```

---

## 📄 License

Software code is distributed under the **Apache 2.0 License**. See [LICENSE](LICENSE) for details.
