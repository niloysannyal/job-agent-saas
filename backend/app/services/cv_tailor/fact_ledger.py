import re
from typing import Dict, List, Set, Tuple


# Canonical verified fact ledger from 01_MASTER_CV.tex control block
VERIFIED_METRICS = {
    "600+ salespersons": r"600\+\s*salespersons?",
    "700+ salespersons": r"700\+\s*salespersons?",
    "530+ problems": r"530\+\s*problems?",
    "350+ LeetCode": r"350\+\s*LeetCode",
    "200+ Codeforces": r"200\+\s*Codeforces",
    "32,247 matches": r"32,?247\s*matches",
    "10,000+ fights": r"10,?000\+\s*fights",
    "80+ features": r"80\+\s*features",
    "sub-100ms": r"sub-?100\s*ms",
    "28,000+ listings": r"28,?000\+\s*listings",
    "95%+ accuracy": r"95%\+\s*accuracy",
    "97% average accuracy": r"97%\s*(average\s*)?accuracy",
    "Apr 2026 -- Present": r"Apr(il)?\s*2026\s*--\s*Present",
    "Nov 2025 -- Mar 2026": r"Nov(ember)?\s*2025\s*--\s*Mar(ch)?\s*2026",
    "Jan 2019 -- Oct 2024": r"Jan(uary)?\s*2019\s*--\s*Oct(ober)?\s*2024",
    "University of Rajshahi": r"University\s+of\s+Rajshahi",
    "B.Sc. ICE": r"B\.?Sc\.?\s*(in\s*)?ICE",
    "Betopia Limited": r"Betopia\s+(Limited|Ltd\.?)",
    "Softvence Agency": r"Softvence\s+(Agency)?",
}

# Suspicious inflated metrics or claims not in master CV
DISALLOWED_PATTERNS = [
    (r"\b(Ph\.?D|Doctorate)\b", "Invented degree (user holds B.Sc. ICE, not Ph.D.)"),
    (r"\b(10\+|15\+|20\+)\s*years\s+of\s+experience\b", "Inflated years of experience"),
    (r"\bGoogle\s+(Brain|DeepMind)\b", "Invented employer claim"),
    (r"\b(Stanford|Harvard|Oxford|Cambridge)\b|\bMIT\s+(degree|alumn|grad|researcher|student)\b", "Invented university claim"),
    (r"\bex-Googler\b", "Invented ex-FAANG claim"),
]


class FactAuditResult:
    def __init__(self, is_valid: bool, flagged_issues: List[str], verified_metrics_found: List[str]):
        self.is_valid = is_valid
        self.flagged_issues = flagged_issues
        self.verified_metrics_found = verified_metrics_found

    def __repr__(self) -> str:
        return f"<FactAuditResult valid={self.is_valid} issues={len(self.flagged_issues)} verified={len(self.verified_metrics_found)}>"


def audit_fact_integrity(tailored_text: str) -> FactAuditResult:
    """
    Audits tailored LaTeX text against the Verified Fact Ledger.
    Ensures no invented degrees, inflated years of experience, or unverified claims.
    """
    flagged_issues = []
    verified_found = []

    # Check for disallowed/invented patterns
    for pattern, reason in DISALLOWED_PATTERNS:
        if re.search(pattern, tailored_text, re.IGNORECASE):
            flagged_issues.append(f"Suspicious invented claim detected: {reason}")

    # Check which canonical metrics are preserved
    for metric_name, regex in VERIFIED_METRICS.items():
        if re.search(regex, tailored_text, re.IGNORECASE):
            verified_found.append(metric_name)

    is_valid = len(flagged_issues) == 0
    return FactAuditResult(
        is_valid=is_valid,
        flagged_issues=flagged_issues,
        verified_metrics_found=verified_found,
    )
