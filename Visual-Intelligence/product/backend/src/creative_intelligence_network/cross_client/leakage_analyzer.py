"""
Semantic Leakage Analyzer for Cross-Client Abstraction.
"""
import re
from typing import List, Tuple


class SemanticLeakageAnalyzer:
    FORBIDDEN_BRAND_TOKENS = {
        "nike", "adidas", "gucci", "chanel", "zara", "balenciaga",
        "client_alpha", "client_beta", "tenant_secret", "lyren_exclusive",
    }

    @classmethod
    def evaluate_leakage(cls, text: str, client_entities: List[str]) -> Tuple[bool, float, List[str]]:
        """
        Analyzes whether a generalized text contains direct or semantic leakage of private client entities.
        Returns (is_safe, risk_score, violations).
        """
        violations = []
        lower_text = text.lower()

        # 1. Direct Token Match
        for entity in client_entities:
            if entity.lower() in lower_text:
                violations.append(f"DIRECT_CLIENT_TOKEN_LEAK: '{entity}'")

        # 2. Known Brand Tokens
        for token in cls.FORBIDDEN_BRAND_TOKENS:
            if re.search(r'\b' + re.escape(token) + r'\b', lower_text):
                violations.append(f"BRAND_IDENTIFIER_LEAK: '{token}'")

        # 3. Exact Metric Leaks (e.g. "$4,231,000 spend", "exact 4.312% CTR")
        if re.search(r'\$\d+[\d,]*\b', text):
            violations.append("EXACT_CURRENCY_SPEND_LEAK")
        if re.search(r'\b\d+\.\d{3,}%\b', text):
            violations.append("HIGH_PRECISION_METRIC_LEAK")

        risk_score = min(1.0, len(violations) * 0.4)
        is_safe = len(violations) == 0

        return is_safe, risk_score, violations
