# Template Creation Guide: Building Custom Domain Meta-Layers

The `psychoactive` framework is designed as a **universal Jack-of-All-Trades**. While pre-built templates exist for Sales, Engineering, Strategy, and Creative writing, you can create a custom domain template in fewer than 10 lines of code.

---

### Step-by-Step Custom Template Construction

To create a new template, inherit from `NeuroTemplate` and implement `get_domain_grounding_rules()`:

```python
from psychoactive import NeuroTemplate, CompoundType

class LegalStrategyTemplate(NeuroTemplate):
    """Custom template for high-stakes litigation and antitrust strategy."""

    def __init__(self, jurisdiction: str = "US Federal Circuit", compound: str = CompoundType.PSILOCYBIN, dose: float = 0.85):
        super().__init__(domain_name=f"Litigation Strategy ({jurisdiction})", compound=compound, dose=dose)

    def get_domain_grounding_rules(self) -> str:
        return (
            "1. STATUTORY GROUNDING: Cite concrete statutory provisions, precedent cases, or evidentiary rules.\n"
            "2. UNORTHODOX PROCEDURAL ANGLE: Use the imported mechanism to invert the opponent's burden of proof.\n"
            "3. ACTIONABLE MOTION DRAFT: Provide the exact preliminary motion outline or deposition questioning script."
        )
```

---

### Executing Your Custom Template

```python
from psychoactive import NeuroSession

# Initialize session with your custom template
template = LegalStrategyTemplate(jurisdiction="Antitrust / FTC", dose=0.90)
session = NeuroSession(template=template, model="gpt-4o")

result = session.run("How to defend an open-source AI developer against monopolistic cross-licensing claims?")

print(result.actionable_deliverable)
```

---

### Using the Quick Customization Flag in `UniversalTemplate`

If you don't even want to write a class, you can pass custom grounding criteria directly into `UniversalTemplate`:

```python
from psychoactive import NeuroSession, UniversalTemplate

template = UniversalTemplate(
    domain_name="Biotech Drug Formulation",
    custom_grounding_criteria="Must satisfy Lipinski's Rule of Five and have predicted oral bioavailability > 70%."
)
session = NeuroSession(template=template)
result = session.run("Design an allosteric inhibitor for LRRK2 kinase.")
```
