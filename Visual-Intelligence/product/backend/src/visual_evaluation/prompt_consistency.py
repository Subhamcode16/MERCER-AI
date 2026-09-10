"""
Phase 22 Visual Evaluation: Prompt Consistency Evaluator
--------------------------------------------------------
Assesses semantic consistency between input prompt constraints and rendered output tags.
"""

from typing import Dict, Any, List

class PromptConsistencyEvaluator:
    """Evaluates whether key entities and constraints from the prompt manifest in the artifact."""

    def evaluate_consistency(self, required_tokens: List[str], observed_tokens: List[str]) -> Dict[str, Any]:
        if not required_tokens:
            return {"score": 1.0, "missing_tokens": [], "passed": True}

        missing = [tok for tok in required_tokens if tok.lower() not in [o.lower() for o in observed_tokens]]
        matched_count = len(required_tokens) - len(missing)
        score = matched_count / len(required_tokens)

        return {
            "score": round(score, 4),
            "matched_count": matched_count,
            "total_required": len(required_tokens),
            "missing_tokens": missing,
            "passed": score >= 0.8,
        }
