# Pharmacological Specifications & Receptor Dynamics

Formal reference for the neurochemical kinetics, equilibrium binding constants, Hill equations, and dosing regimes governing `psychoactive`.

---

### 1. Receptor Equilibrium Dissociation Constants ($K_i$)

| Compound | Target Receptor | $K_i$ Affinity (nM) | Intrinsic Efficacy ($E_{\max}$) | Primary Cognitive Mechanism |
|---|---|:---:|:---:|---|
| **Psilocin (Psilocybin active)** | $5\text{-HT}_{2A}$ | $6.0 \text{ nM}$ | $0.85$ | Apical dendritic depolarization, Layer V pyramidal firing, DMN prior relaxation ($\pi_P \to 0.15$) |
| **Delta-9-THC** | $\text{CB}_1$ | $10.0 \text{ nM}$ | $0.78$ | Presynaptic retrograde lateral suppression, DSE/DSI, sub-threshold association rescue |
| **Microdose** | $5\text{-HT}_{2A}$ | $6.0 \text{ nM}$ | $0.30$ | Sub-perceptual prior loosening ($\pi_P \to 0.70$), high syntactic stability |
| **Baseline Homeostasis** | Control | — | $0.00$ | Standard autoregressive decoding ($\pi_P = 1.0$), canonical corporate attractor |

---

### 2. Receptor Fractional Occupancy (Normalized Hill Equation)

Receptor occupancy $\theta(D)$ as a function of normalized dosage $D \in [0.0, 1.0]$ is governed by the cooperative Hill equation:

$$\theta(D) = \frac{\frac{D^n}{EC_{50}^n + D^n}}{\frac{1^n}{EC_{50}^n + 1^n}}$$

- **Hill Cooperativity Exponent ($n$)**: $1.8$
- **Half-Maximal Effective Concentration ($EC_{50}$)**: $0.50$
- **Boundary Invariants**: $\theta(0.0) = 0.0$ and $\theta(1.0) = 1.0$

---

### 3. Dynamic Sampling Hyperparameter Curves

As the agent advances through the discrete 4-stage lifecycle $t \in [0, 4\tau]$, sampling hyperparameters adapt dynamically:

```
Hyperparameter      Baseline     Ascent           Peak             Return
-----------------------------------------------------------------------------
Prior Precision     1.00         1.00 -> 0.35     0.15 - 0.30      0.35 -> 1.00
Temperature         0.70         0.70 -> 0.95     1.00 - 1.30      0.90 -> 0.20
Presence Penalty    0.00         0.20 -> 0.40     0.60 - 0.85      0.30 -> 0.10
Retrograde Lambda   0.05         0.10 -> 0.50     0.50 - 0.70      0.50 -> 0.05
```
