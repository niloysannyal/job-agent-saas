"""
backend/app/services/cv_tailor/reviewer.py

Decoupled Senior Recruiter Reviewer Service (Pass 2).
Audits Pass 1 Drafter output for:
1. Fact integrity against verified candidate metrics (fact ledger audit).
2. Hallucinations, generic fluff, and unverified credentials.
3. Keyword alignment and ATS text layer check.
4. LaTeX brace balance and compilation readiness.

Outputs validation verdict (`is_valid`) enabling autonomous self-correction loops in LangGraph.
"""

import html
import logging
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.services.cv_tailor.ats_checker import run_ats_text_layer_check
from app.services.cv_tailor.drafter import CandidateCareerContext, CVDraftOutput
from app.services.cv_tailor.fact_ledger import audit_fact_integrity
from app.services.cv_tailor.latex_processor import check_brace_balance
from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)


class CVReviewInput(BaseModel):
    draft_output: CVDraftOutput
    job_role: str
    job_company: str
    job_description: str
    career_context: CandidateCareerContext


class CVReviewOutput(BaseModel):
    is_valid: bool
    final_tailored_latex: str
    final_summary_bullet: str
    final_cover_letter: str
    confirmed_gaps: List[str] = Field(default_factory=list)
    ats_score: float
    fact_audit_passed: bool
    hallucination_detected: bool
    hallucination_reasons: List[str] = Field(default_factory=list)
    line_count: int
    computed_page_count: int
    reviewer_notes: str


class CVReviewerService:
    """
    Executes Pass 2 (Senior Recruiter Reviewer & Fact Auditor).
    Audits for hallucinations, ATS scores, brace balance, and produces finalized LaTeX.
    """

    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()

    async def review_cv(self, params: CVReviewInput) -> CVReviewOutput:
        role_clean = html.unescape(params.job_role or "")
        company_clean = html.unescape(params.job_company or "")
        draft = params.draft_output
        context = params.career_context

        # 1. Senior Recruiter Reviewer Pass (Pass 2) LLM Generation
        recruiter_context = (
            "You are a Senior Principal Tech Recruiter and Executive Talent Strategist with 20+ years "
            "of experience at Tier-1 tech enterprises. You have up-to-date 2026 hiring knowledge, modern ATS algorithms, "
            "and candidate positioning strategies. You tailor candidate CVs and outreach to maximize interview conversion "
            "without ever inventing false credentials or violating verified facts."
        )

        reviewer_prompt = f"""
You are the independent Reviewer pass auditing the output from a Senior Recruiter.
Review the following Drafter output for:
1. Any generic buzzwords, weak framing, or grammatical errors.
2. Any hallucinations (ensure NO fake credentials, degrees, or companies).
3. Keyword alignment with role: {role_clean} at {company_clean}.
4. Strict fact ledger preservation against candidate background:
{context.verified_facts_str}

Drafter Output:
{draft.drafter_raw_response}

Output your finalized version:
---FINAL_SUMMARY---
[Finalized \\resumeItem{{...}} summary bullet]
---FINAL_COVER---
[Refined cover letter text]
---CONFIRMED_GAPS---
[Finalized list of missing skills or 'None']
"""
        reviewer_response = await self.llm_service.generate(
            prompt=reviewer_prompt,
            context=recruiter_context,
        )

        # 2. Parse Reviewer Response
        final_summary = draft.draft_summary_bullet
        final_cover = draft.draft_cover_letter
        confirmed_gaps = draft.raw_gaps

        if "---FINAL_SUMMARY---" in reviewer_response:
            parts = reviewer_response.split("---FINAL_SUMMARY---")[1]
            if "---FINAL_COVER---" in parts:
                s_part, rest = parts.split("---FINAL_COVER---", 1)
                if "\\resumeItem" in s_part.strip():
                    final_summary = s_part.strip()
                if "---CONFIRMED_GAPS---" in rest:
                    c_part, g_part = rest.split("---CONFIRMED_GAPS---", 1)
                    final_cover = c_part.strip()
                    confirmed_gaps = [g.strip("- ").strip() for g in g_part.strip().split("\n") if g.strip("- ").strip()]
                else:
                    final_cover = rest.strip()

        # 3. Assemble Final LaTeX Document
        final_body = re.sub(
            r"\\resumeItemListStart\s*\\resumeItem\{.*?\}\s*\\resumeItemListEnd",
            f"\\\\resumeItemListStart\n  {final_summary}\n\\\\resumeItemListEnd",
            draft.budgeted_latex_body,
            count=1,
            flags=re.DOTALL,
        )
        final_tailored_latex = f"{draft.preamble}\n\\begin{{document}}\n{final_body}\n\\end{{document}}"

        # 4. Deterministic Fact Ledger & Integrity Audit
        fact_audit = audit_fact_integrity(final_tailored_latex)
        fact_passed = bool(fact_audit.is_valid)
        hallucination_reasons = []
        if not fact_passed:
            hallucination_reasons.extend(fact_audit.flagged_issues)

        # 5. LaTeX Brace Balance Audit
        braces_balanced = check_brace_balance(final_tailored_latex)
        if not braces_balanced:
            hallucination_reasons.append("LaTeX syntax error: Unbalanced braces detected in compiled document.")

        # 6. ATS Text-Layer Check
        ats_result = run_ats_text_layer_check(final_tailored_latex, params.job_description)
        raw_score = float(ats_result.score)
        ats_score = raw_score * 100.0 if raw_score <= 1.0 else raw_score

        # 7. Page Count Budget
        line_count = len(final_tailored_latex.splitlines())
        computed_pages = 1 if line_count < 130 else 2

        is_valid = fact_passed and braces_balanced and (ats_score >= 60.0)

        reviewer_notes = (
            f"Reviewer pass completed. Fact check: {'PASS' if fact_passed else 'FAIL'}. "
            f"ATS Score: {ats_score:.1f}%. Braces balanced: {braces_balanced}. "
            f"Page budget: {computed_pages} page(s)."
        )

        return CVReviewOutput(
            is_valid=is_valid,
            final_tailored_latex=final_tailored_latex,
            final_summary_bullet=final_summary,
            final_cover_letter=final_cover,
            confirmed_gaps=confirmed_gaps,
            ats_score=ats_score,
            fact_audit_passed=fact_passed,
            hallucination_detected=not fact_passed,
            hallucination_reasons=hallucination_reasons,
            line_count=line_count,
            computed_page_count=computed_pages,
            reviewer_notes=reviewer_notes,
        )
