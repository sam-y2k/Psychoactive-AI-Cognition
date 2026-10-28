# Psychoactive AI Cookbook: Multi-Domain Recipes

Practical recipes demonstrating how `psychoactive` solves real-world bottlenecks across disparate industries.

---

### Recipe 1: Outbound B2B Sales Campaign Breaker

**The Bottleneck:** Standard cold emails suffer from severe template fatigue (0.5% open-to-reply rate). C-level executives delete "hop on a quick 15-min call" pitches on autopilot.

```python
from psychoactive import NeuroSession, SalesTemplate, CompoundType

# Step 1: Initialize SalesTemplate with THC Mode for lateral pattern interrupts
sales_template = SalesTemplate(
    product="Autonomous Cloud FinOps & Kubernetes Cost Optimization",
    icp="VP of Engineering / Head of Infrastructure",
    compound=CompoundType.THC,
    dose=0.90
)

# Step 2: Run through NeuroSession
session = NeuroSession(template=sales_template, model="gpt-4o")
result = session.run("Generate a 3-touch outbound cold sequence for skeptical tech leaders.")

print("Dismantled Cliché:\n", result.canonical_cliche)
print("Unignorable Campaign Deliverable:\n", result.actionable_deliverable)
```

---

### Recipe 2: Breaking Software Architecture Concurrency Deadlocks

**The Bottleneck:** Distributed systems teams stall when trying to coordinate multi-region transactional state without paying extreme latency penalties on centralized locks.

```python
from psychoactive import NeuroSession, EngineeringTemplate, CompoundType

# Step 1: Initialize EngineeringTemplate with Psilocybin Mode (prior relaxation)
eng_template = EngineeringTemplate(
    tech_stack="Rust / Distributed Raft",
    compound=CompoundType.PSILOCYBIN,
    dose=0.95
)

session = NeuroSession(template=eng_template, model="claude-3-5-sonnet")
result = session.run("Eliminate two-phase commit lock contention across 5 global regions.")

print(result.actionable_deliverable)
```

---

### Recipe 3: Constructing an Asymmetric Business Moat

**The Bottleneck:** Startups default to building feature parity with incumbents, competing on the same dimension where the incumbent has 100x more capital.

```python
from psychoactive import NeuroSession, StrategyTemplate, CompoundType

strategy_template = StrategyTemplate(
    industry="Enterprise Compliance Software",
    compound=CompoundType.ENTOURAGE,
    dose=0.85
)

session = NeuroSession(template=strategy_template, model="gpt-4o")
result = session.run("How do we build an asymmetric moat against incumbents with 90% market share?")

print(result.actionable_deliverable)
```

---

### Recipe 4: Overcoming AI Writing Tropes in Creative Fiction

**The Bottleneck:** Standard LLMs write sterile, formulaic prose stuffed with clichés ("tapestry", "shivers down spine", "a testament to").

```python
from psychoactive import NeuroSession, CreativeTemplate, CompoundType

creative_template = CreativeTemplate(
    medium="Cyberpunk Noir Screenplay",
    compound=CompoundType.PSILOCYBIN,
    dose=0.80
)

session = NeuroSession(template=creative_template, model="claude-3-5-sonnet")
result = session.run("Write the opening scene introducing an underground neural-lace surgeon.")

print(result.actionable_deliverable)
```
