"""
Remote Associates Test (RAT) Benchmark Suite.
Formalizes Section 12.1 of the REBUS-AI Architecture:
Evaluates associative horizon expansion across remote semantic triads.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import re


@dataclass(frozen=True)
class RATItem:
    """A standard Remote Associates Test triad item."""
    item_id: int
    clues: List[str]                    # 3 stimulus words, e.g. ["cottage", "swiss", "cake"]
    solution: str                       # Target bridge word, e.g. "cheese"
    difficulty: str = "medium"          # "easy", "medium", "hard"


@dataclass(frozen=True)
class RATResult:
    """Evaluation result across a test battery."""
    total_items: int
    correct_count: int
    accuracy_percentage: float
    mean_response_latency_ms: float
    item_details: List[Dict[str, Any]]


SAMPLE_RAT_TRIADS: List[RATItem] = [
    RATItem(1, ["cottage", "swiss", "cake"], "cheese", "easy"),
    RATItem(2, ["night", "wrist", "stop"], "watch", "easy"),
    RATItem(3, ["cream", "skate", "water"], "ice", "easy"),
    RATItem(4, ["dew", "comb", "bee"], "honey", "medium"),
    RATItem(5, ["fountain", "baking", "pop"], "soda", "medium"),
    RATItem(6, ["rocking", "wheel", "high"], "chair", "medium"),
    RATItem(7, ["sense", "courtesy", "place"], "common", "hard"),
    RATItem(8, ["worm", "shelf", "end"], "book", "medium"),
    RATItem(9, ["measure", "worm", "video"], "tape", "hard"),
    RATItem(10, ["flake", "mobile", "cone"], "snow", "medium"),
    RATItem(11, ["cracker", "fly", "fighter"], "fire", "medium"),
    RATItem(12, ["opera", "hand", "dish"], "soap", "easy"),
]


class RATBenchmarkRunner:
    """
    Executes the Remote Associates Test across different cognitive modes:
    - Baseline (Greedy / Low Temp)
    - High Temperature (Unanchored Stochastic Noise)
    - REBUS-AI (Dynamic Prior Relaxation + Lateral Gating)
    """

    def __init__(self, dataset: Optional[List[RATItem]] = None):
        self.dataset = dataset or SAMPLE_RAT_TRIADS

    def evaluate_model_response(self, triad: RATItem, model_completion: str) -> bool:
        """Checks whether the ground-truth solution is correctly retrieved in the completion."""
        clean_target = triad.solution.lower().strip()
        text = model_completion.lower().strip()

        # Word boundary match
        pattern = r"\b" + re.escape(clean_target) + r"\b"
        return bool(re.search(pattern, text))

    def run_benchmark(
        self,
        completion_provider,           # Callable: (RATItem) -> (str, float) [text, latency_ms]
    ) -> RATResult:
        """Runs the entire battery and computes accuracy."""
        correct = 0
        details = []
        total_latency = 0.0

        for item in self.dataset:
            text, latency = completion_provider(item)
            is_correct = self.evaluate_model_response(item, text)
            if is_correct:
                correct += 1
            total_latency += latency
            details.append({
                "item_id": item.item_id,
                "clues": item.clues,
                "expected": item.solution,
                "completion": text,
                "correct": is_correct,
                "latency_ms": latency,
            })

        acc = (correct / max(1, len(self.dataset))) * 100.0
        mean_lat = total_latency / max(1, len(self.dataset))

        return RATResult(
            total_items=len(self.dataset),
            correct_count=correct,
            accuracy_percentage=round(acc, 2),
            mean_response_latency_ms=round(mean_lat, 2),
            item_details=details,
        )
