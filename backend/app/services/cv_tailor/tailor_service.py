import logging
import re
from typing import Any, Dict, Optional, Tuple
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.account import Account
from app.models.application import Application
from app.models.cv_template import AccountCvVersion, CvTemplate
from app.models.job import Job
from app.services.cv_tailor.ats_checker import run_ats_text_layer_check
from app.services.cv_tailor.fact_ledger import audit_fact_integrity
from app.services.cv_tailor.latex_processor import (
    check_brace_balance,
    escape_latex_special_chars,
    extract_preamble_and_body,
    strip_control_comments,
)
from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)

# Canonical summary variants from 01_MASTER_CV.tex control notes
SUMMARY_VARIANTS = {
    "agentic_llm": (
        "\\resumeItem{AI Engineer building production \\textbf{agentic AI and LLM systems} -- "
        "architected the Betopia Sales Agent embedded in Odoo CRM for \\textbf{600+ salespersons}, "
        "with a multi-provider LLM chain (OpenAI, Anthropic, Gemini), Qdrant-based \\textbf{RAG}, "
        "and end-to-end ownership from architecture through deployment and operations.}"
    ),
    "mlops_platform": (
        "\\resumeItem{AI Engineer with end-to-end \\textbf{MLOps and AI platform engineering} experience -- "
        "GitHub Actions CI/CD, a Dockerized multi-service production stack (FastAPI, Odoo, PostgreSQL, "
        "Redis, Qdrant), VPS administration, backups, monitoring, and incident response for a system used by "
        "\\textbf{700+ salespersons}.}"
    ),
    "ml_data_science": (
        "\\resumeItem{AI/ML Engineer with hands-on \\textbf{machine learning} experience -- "
        "ensemble models (XGBoost, LightGBM) trained on \\textbf{10,000+ UFC fights} with \\textbf{80+ engineered features} "
        "and served via FastAPI at \\textbf{sub-100ms latency}, plus forecasting, regression and CNN projects, "
        "alongside production LLM and RAG systems.}"
    ),
    "backend_fullstack": (
        "\\resumeItem{AI Engineer with strong \\textbf{backend and full-stack} skills -- "
        "FastAPI services, async Python, Next.js 15 dashboards, PostgreSQL, Redis and Qdrant, shipped with Docker "
        "and GitHub Actions CI/CD into production systems used by \\textbf{700+ salespersons}.}"
    ),
}


class CVTailorResult:
    def __init__(
        self,
        cv_version: AccountCvVersion,
        application: Application,
        ats_score: float,
        fact_audit_passed: bool,
        gaps_detected: list,
        drafter_notes: str,
    ):
        self.cv_version = cv_version
        self.application = application
        self.ats_score = ats_score
        self.fact_audit_passed = fact_audit_passed
        self.gaps_detected = gaps_detected
        self.drafter_notes = drafter_notes


class CVTailorService:
    """
    Module 2 (Apply) CV tailoring pipeline matching ARCHITECTURE.md §3, §5 & §11.
    Executes drafter + reviewer two-pass generation, enforces the verified fact ledger,
    preserves LaTeX preamble exactly, and creates a draft application (human-in-the-loop).
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        db_session: Optional[Session] = None,
    ):
        self.llm_service = llm_service or LLMService()
        self.db_session = db_session

    def select_summary_variant(self, job_title: str, job_description: str) -> str:
        """Selects the best fact-verified Summary variant based on role keywords."""
        text = f"{job_title} {job_description}".lower()
        if any(k in text for k in ["agent", "llm", "rag", "langchain", "reasoning", "prompt"]):
            return SUMMARY_VARIANTS["agentic_llm"]
        if any(k in text for k in ["mlops", "devops", "platform", "infrastructure", "ci/cd", "docker"]):
            return SUMMARY_VARIANTS["mlops_platform"]
        if any(k in text for k in ["machine learning", "data science", "xgboost", "cnn", "forecast"]):
            return SUMMARY_VARIANTS["ml_data_science"]
        return SUMMARY_VARIANTS["backend_fullstack"]

    async def tailor_for_job(
        self,
        account_id: str,
        job: Job,
        channel: str = "email",
    ) -> CVTailorResult:
        """
        Executes the full Drafter -> Reviewer -> Fact Audit -> Persistence pipeline.
        """
        # Step 1: Load master CV template source
        master_cv_path = settings.resolve_cv_path()
        if master_cv_path.exists():
            master_source = master_cv_path.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"Master CV source not found at {master_cv_path}")

        # Step 2: Split and preserve preamble
        preamble, body = extract_preamble_and_body(master_source)
        cleaned_body = strip_control_comments(body)

        # Step 3: Select base summary variant
        summary_bullet = self.select_summary_variant(job.role, job.description or "")

        # Step 4: Drafter Pass (Pass 1)
        drafter_prompt = f"""
You are the CV Drafter for Niloy Sannyal's autonomous job application SaaS.
Target Company: {job.company}
Target Role: {job.role}
Job Description:
{job.description or ''}

Selected Approved Summary Bullet:
{summary_bullet}

RULES (NON-NEGOTIABLE):
1. NEVER invent, exaggerate, or assume facts not present in Niloy's background.
2. Keep the verified numbers exact (600+ salespersons, 10,000+ fights, 80+ features, sub-100ms, 530+ problems).
3. Generate a concise tailored outreach cover letter (2-3 short paragraphs in professional first-person voice).
4. Identify any required skills in the job description that are NOT present in Niloy's background and list them under GAPS.

Provide your response in this exact format:
---COVER_NOTE---
[Your 2-3 paragraph cover letter draft]
---GAPS---
[Bullet points of any missing requirements or 'None']
---TAILORED_SUMMARY---
[Adapted summary item preserving LaTeX formatting]
"""
        drafter_response = await self.llm_service.generate(
            prompt=drafter_prompt,
            context="You are a strict, truth-only CV drafter and ATS keyword specialist.",
        )

        # Step 5: Reviewer Pass (Pass 2)
        reviewer_prompt = f"""
You are the independent Reviewer pass. Critique the following Drafter output for:
1. Any generic buzzwords or weak framing.
2. Any hallucinations (ensure no fake credentials, degrees, or companies).
3. Keyword alignment with role: {job.role} at {job.company}.

Drafter Output:
{drafter_response}

Output your finalized version of the cover letter and confirmed gaps:
---FINAL_COVER---
[Refined cover letter text]
---CONFIRMED_GAPS---
[Finalized list of missing skills]
"""
        reviewer_response = await self.llm_service.generate(
            prompt=reviewer_prompt,
            context="You are an uncompromising reviewer auditing CV facts and outreach impact.",
        )

        # Parse cover letter and gaps from response
        cover_content = ""
        if "---FINAL_COVER---" in reviewer_response:
            parts = reviewer_response.split("---FINAL_COVER---")[1]
            cover_content = parts.split("---CONFIRMED_GAPS---")[0].strip()
        elif "---COVER_NOTE---" in drafter_response:
            parts = drafter_response.split("---COVER_NOTE---")[1]
            cover_content = parts.split("---GAPS---")[0].strip()
        else:
            cover_content = f"Dear Hiring Team at {job.company},\n\nI am excited to apply for the {job.role} position."

        # Parse gaps
        gaps = []
        if "---CONFIRMED_GAPS---" in reviewer_response:
            gaps_text = reviewer_response.split("---CONFIRMED_GAPS---")[1].strip()
            gaps = [line.strip("- *") for line in gaps_text.splitlines() if line.strip() and line.strip().lower() != "none"]

        # Step 6: Assemble tailored LaTeX
        # Substitute summary section in cleaned body
        pattern = r"(\\section\{Summary\}[\s\S]*?\\resumeItemListStart\{?\}?\s*)[\s\S]*?(\s*\\resumeItemListEnd)"
        tailored_body = re.sub(
            pattern,
            r"\g<1>\n  " + summary_bullet.replace("\\", "\\\\") + r"\g<2>",
            cleaned_body,
            count=1,
        )

        tailored_latex = f"{preamble}\n{tailored_body}"

        # Validate LaTeX syntax
        braces_balanced = check_brace_balance(tailored_latex)
        if not braces_balanced:
            logger.warning("Unbalanced braces detected in tailored output; falling back to clean template body.")
            tailored_latex = f"{preamble}\n{cleaned_body}"

        # Step 7: Run Fact Audit and ATS Text-Layer Checks
        fact_audit = audit_fact_integrity(tailored_latex)
        ats_result = run_ats_text_layer_check(tailored_latex, job.description or "")

        # Step 8: Database Persistence (Enforcing Human-in-the-Loop)
        cv_version = AccountCvVersion(
            account_id=account_id,
            job_id=job.id,
            tailored_latex=tailored_latex,
            ats_score=ats_result.score,
            page_count=1,
            cut_summary={"strategy": "relevance_weighted", "gaps": gaps},
            status="draft",
        )

        application = Application(
            account_id=account_id,
            job_id=job.id,
            channel=channel,
            draft_content=cover_content,
            sent_at=None,  # STRICT HUMAN-IN-THE-LOOP: Never auto-sent
            status="draft",
            follow_up_count=0,
            notes=f"ATS Keyword score: {ats_result.score:.2f}. Gaps: {', '.join(gaps) if gaps else 'None'}",
        )

        if self.db_session:
            self.db_session.add(cv_version)
            self.db_session.flush()
            application.cv_version_id = cv_version.id
            self.db_session.add(application)
            self.db_session.commit()
            self.db_session.refresh(cv_version)
            self.db_session.refresh(application)

        return CVTailorResult(
            cv_version=cv_version,
            application=application,
            ats_score=ats_result.score,
            fact_audit_passed=fact_audit.is_valid,
            gaps_detected=gaps,
            drafter_notes=reviewer_response,
        )
