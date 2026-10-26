import re
from typing import Dict, List, Optional, Set, Tuple


# Default fallback trim priority (lower number = cut first when overflowing)
TRIM_PRIORITIES = {
    "robotics_embedded": 1,
    "certifications": 2,
    "career_highlights": 3,
    "leadership": 4,
    "enterprise_ai_systems": 5,
    "personal_projects": 6,
    "work_experience": 10,
    "education": 10,
    "skills": 10,
    "summary": 10,
}


def score_bullet_relevance(
    bullet_text: str,
    job_tokens: Set[str],
    section_category: str = "general",
) -> float:
    """
    Computes a relevance-weighted score for a single LaTeX bullet:
    score = keyword_overlap + section_base_priority.
    """
    clean_text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^\}]*\})?", " ", bullet_text)
    clean_text = re.sub(r"[^a-zA-Z0-9\s]", " ", clean_text).lower()
    bullet_words = set(clean_text.split())

    # Keyword intersection
    overlap = len(bullet_words.intersection(job_tokens))
    base_priority = TRIM_PRIORITIES.get(section_category, 5)

    # Relevance score
    score = (overlap * 2.5) + base_priority
    return score


def extract_keywords_from_job(job_description: str) -> Set[str]:
    """Extracts non-stopword tokens from a job posting for relevance scoring."""
    stopwords = {
        "the", "and", "to", "of", "in", "for", "a", "with", "as", "on", "at", "by", "from",
        "an", "be", "this", "which", "or", "you", "we", "our", "are", "is", "will", "your",
        "that", "have", "experience", "role", "team", "looking", "working", "work", "join",
    }
    words = re.findall(r"\b[a-zA-Z0-9_\-\+\#]{2,}\b", job_description.lower())
    return {w for w in words if w not in stopwords}


def plan_relevance_cuts(
    sections: Dict[str, List[str]],
    job_description: str,
    target_bullets_count: int = 14,
) -> Tuple[Dict[str, List[str]], Dict[str, any]]:
    """
    Applies relevance-weighted line scoring to trim bullets to fit within
    the target 1-page budget.
    """
    job_tokens = extract_keywords_from_job(job_description)
    cut_log = []
    retained_sections = {}

    total_bullets = sum(len(bullets) for bullets in sections.values() if isinstance(bullets, list))

    for sec_name, bullets in sections.items():
        if not isinstance(bullets, list) or len(bullets) == 0:
            retained_sections[sec_name] = bullets
            continue

        # Score each bullet in section
        scored = []
        for bullet in bullets:
            score = score_bullet_relevance(bullet, job_tokens, section_category=sec_name)
            scored.append((score, bullet))

        # Sort by score descending (highest relevance first)
        scored.sort(key=lambda x: x[0], reverse=True)

        # Decide retention quota
        if sec_name in ["robotics_embedded", "certifications"] and "robotics" not in job_description.lower():
            # Drop lowest priority sections when over budget
            retained = [b for s, b in scored[:1]]  # Keep at most 1
            for s, b in scored[1:]:
                cut_log.append({"section": sec_name, "score": s, "preview": b[:60]})
        elif sec_name == "career_highlights" and total_bullets > target_bullets_count:
            # Overlaps Summary and Experience; keep top 2
            retained = [b for s, b in scored[:2]]
            for s, b in scored[2:]:
                cut_log.append({"section": sec_name, "score": s, "preview": b[:60]})
        else:
            retained = [b for s, b in scored]

        retained_sections[sec_name] = retained

    summary = {
        "cut_count": len(cut_log),
        "cut_items": cut_log,
        "strategy": "relevance_weighted_scoring",
    }
    return retained_sections, summary
