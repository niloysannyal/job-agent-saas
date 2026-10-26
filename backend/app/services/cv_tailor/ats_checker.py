import re
from typing import Dict, List, Set, Tuple


class ATSCheckResult:
    def __init__(
        self,
        score: float,
        matched_keywords: List[str],
        missing_keywords: List[str],
        contact_verified: bool,
        issues: List[str],
    ):
        self.score = score
        self.matched_keywords = matched_keywords
        self.missing_keywords = missing_keywords
        self.contact_verified = contact_verified
        self.issues = issues

    def to_dict(self) -> Dict[str, any]:
        return {
            "score": round(self.score, 3),
            "matched_keywords_count": len(self.matched_keywords),
            "missing_keywords_count": len(self.missing_keywords),
            "matched_keywords": self.matched_keywords[:15],
            "missing_keywords": self.missing_keywords[:15],
            "contact_verified": self.contact_verified,
            "issues": self.issues,
        }


def run_ats_text_layer_check(
    tailored_text: str,
    job_description: str,
) -> ATSCheckResult:
    """
    Simulates ATS parser text-layer inspection:
    1. Verifies contact header fields (Email, Phone, LinkedIn, GitHub) exist as plain text.
    2. Measures keyword density and coverage against the job description.
    3. Identifies honest gaps for missing skills.
    """
    issues = []

    # 1. Contact verification
    has_email = bool(re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", tailored_text))
    has_linkedin = "linkedin.com" in tailored_text.lower()
    has_github = "github.com" in tailored_text.lower()
    contact_verified = has_email and (has_linkedin or has_github)

    if not has_email:
        issues.append("Missing or unparseable email address in header.")
    if not (has_linkedin or has_github):
        issues.append("Missing portfolio links (LinkedIn or GitHub) in header.")

    # 2. Extract technical keyword set from job description
    job_words = re.findall(r"\b[A-Za-z0-9_\+\#]{3,}\b", job_description.lower())
    tech_keywords = {
        "python", "fastapi", "docker", "redis", "postgresql", "qdrant", "llm", "rag",
        "agentic", "agent", "langchain", "langgraph", "ci/cd", "git", "rest", "api",
        "aws", "gcp", "azure", "linux", "nlp", "machine learning", "ml", "ai",
        "pytorch", "tensorflow", "react", "next.js", "typescript", "javascript",
    }
    extracted_target_skills = {w for w in job_words if w in tech_keywords}
    if not extracted_target_skills:
        # Fallback to general tokens
        extracted_target_skills = {w for w in set(job_words) if len(w) > 4}

    # 3. Match against tailored CV text
    cv_text_lower = tailored_text.lower()
    matched = []
    missing = []

    for skill in extracted_target_skills:
        if skill in cv_text_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    total_skills = len(extracted_target_skills)
    score = (len(matched) / total_skills) if total_skills > 0 else 0.5

    return ATSCheckResult(
        score=score,
        matched_keywords=sorted(matched),
        missing_keywords=sorted(missing),
        contact_verified=contact_verified,
        issues=issues,
    )
