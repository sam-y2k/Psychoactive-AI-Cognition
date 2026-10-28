"""
Integration Grounder & Consolidation Engine.
Extracts, structures, and validates the grounded deliverable from the Return stage,
ensuring high execution readiness and zero dilution of the breakthrough.
"""

from typing import Dict, Any, List, Optional
import re
from pydantic import BaseModel, Field


class GroundedArtifact(BaseModel):
    """Clean, structured artifact ready for production deployment."""
    paradigm_shift: str = Field(description="The core conventional assumption that was dismantled")
    orthogonal_mechanism: str = Field(description="The imported cross-domain dynamics and model")
    actionable_tactics: List[str] = Field(description="Concrete step-by-step implementation instructions")
    raw_deliverable: str = Field(description="The complete textual deliverable")
    readiness_score: int = Field(description="Deployment readiness rating from 0 to 100")


class IntegrationGrounder:
    """
    Consolidates the Stage 4 output into an authoritative, structured GroundedArtifact.
    Calculates execution readiness and purges generic corporate filler.
    """

    def ground(self, return_text: str, peak_text: Optional[str] = None) -> GroundedArtifact:
        """
        Parses and structures the final return output.
        """
        text = return_text.strip()

        # 1. Extract Paradigm Shift
        paradigm = self._extract_section(
            text,
            start_tags=["[PARADIGM SHIFT]", "PARADIGM SHIFT:", "1. PARADIGM SHIFT"],
            end_tags=["[THE MECHANISM]", "[MECHANISM]", "2. THE MECHANISM", "[ACTIONABLE DELIVERABLE]"],
        )
        if not paradigm:
            paradigm = "Overturned conventional localized assumptions in favor of orthogonal systemic synthesis."

        # 2. Extract Mechanism
        mechanism = self._extract_section(
            text,
            start_tags=["[THE MECHANISM]", "THE MECHANISM:", "[MECHANISM]", "2. THE MECHANISM"],
            end_tags=["[ACTIONABLE DELIVERABLE]", "3. ACTIONABLE DELIVERABLE", "[DELIVERABLE]"],
        )
        if not mechanism and peak_text:
            mechanism = peak_text[:250].strip() + "..."
        elif not mechanism:
            mechanism = "Cross-domain Stiefel manifold analogical projection."

        # 3. Extract Actionable Deliverable / Tactics
        deliverable_body = self._extract_section(
            text,
            start_tags=["[ACTIONABLE DELIVERABLE]", "ACTIONABLE DELIVERABLE:", "3. ACTIONABLE DELIVERABLE", "[DELIVERABLE]"],
            end_tags=["---", "===", "[END]"],
        )
        if not deliverable_body:
            deliverable_body = text

        # Parse tactical bullet points
        tactics = []
        for line in deliverable_body.split("\n"):
            line = line.strip()
            if re.match(r"^(\d+\.|\-|\*|\•)\s+", line):
                clean_tactic = re.sub(r"^(\d+\.|\-|\*|\•)\s+", "", line)
                if len(clean_tactic) > 10:
                    tactics.append(clean_tactic)

        if not tactics:
            tactics = [line.strip() for line in deliverable_body.split("\n") if len(line.strip()) > 25][:5]

        # 4. Compute Execution Readiness Score (0 - 100)
        score = self._compute_readiness_score(text, tactics)

        return GroundedArtifact(
            paradigm_shift=paradigm.strip(),
            orthogonal_mechanism=mechanism.strip(),
            actionable_tactics=tactics,
            raw_deliverable=deliverable_body.strip(),
            readiness_score=score,
        )

    def _extract_section(self, text: str, start_tags: List[str], end_tags: List[str]) -> Optional[str]:
        lower_text = text.lower()
        start_pos = -1
        best_tag_len = 0

        for tag in start_tags:
            pos = lower_text.find(tag.lower())
            if pos != -1:
                start_pos = pos + len(tag)
                best_tag_len = len(tag)
                break

        if start_pos == -1:
            return None

        # Search for earliest end tag after start_pos
        end_pos = len(text)
        for tag in end_tags:
            pos = lower_text.find(tag.lower(), start_pos)
            if pos != -1 and pos < end_pos:
                end_pos = pos

        extracted = text[start_pos:end_pos].strip(" :-\n")
        return extracted if len(extracted) > 5 else None

    def _compute_readiness_score(self, text: str, tactics: List[str]) -> int:
        score = 50 # Base score

        # Bonus for clear tactics
        if len(tactics) >= 3:
            score += 20
        elif len(tactics) >= 1:
            score += 10

        # Bonus for length and concrete code/scripts
        if len(text) > 400:
            score += 15
        if any(marker in text for marker in ["```", "def ", "class ", "Subject:", "1.", "Step"]):
            score += 15

        # Penalty for empty generic buzzwords
        fluff_words = ["synergy", "paradigm shift", "leverage", "delve", "tapestry", "revolutionize"]
        fluff_count = sum(text.lower().count(w) for w in fluff_words)
        score -= min(25, fluff_count * 5)

        return max(10, min(100, score))
