"""
backend/app/services/cv_tailor/drafter.py

Decoupled Senior Recruiter Drafter Service (Pass 1).
Pure function service with zero database side-effects:
1. Selects best summary variant based on job role and keywords.
2. Budgets and prunes LaTeX document body to strictly fit 1-2 pages.
3. Invokes Pass 1 LLM prompt to generate tailored executive summary bullet, cover letter draft, and gaps.
4. Assembles draft LaTeX without database mutation.
"""

from dataclasses import dataclass, field
import html
import logging
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.services.cv_tailor.latex_processor import (
    extract_preamble_and_body,
    strip_control_comments,
    escape_latex_special_chars,
)
from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)

# Canonical verified summary variants from 01_MASTER_CV.tex control notes
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


@dataclass
class CandidateCareerContext:
    account_id: str
    candidate_name: str
    headline: str
    master_latex: str
    experiences: List[Dict[str, Any]] = field(default_factory=list)
    educations: List[Dict[str, Any]] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    projects: List[Dict[str, Any]] = field(default_factory=list)
    verified_facts_str: str = ""
    is_niloy: bool = True


class CVDraftInput(BaseModel):
    account_id: str
    job_id: Optional[str] = None
    job_role: str
    job_company: str
    job_description: str
    target_angle: Optional[str] = None
    audit_feedback: Optional[List[str]] = None
    career_context: Optional[CandidateCareerContext] = None


class CVDraftOutput(BaseModel):
    draft_summary_bullet: str
    draft_cover_letter: str
    raw_gaps: List[str] = Field(default_factory=list)
    budgeted_latex_body: str
    preamble: str
    draft_assembled_latex: str
    drafter_raw_response: str


def prune_and_budget_latex(
    latex_body: str,
    job_role: str = "AI Engineer",
    job_description: str = "",
) -> str:
    """
    Budgets and prunes the Master CV body to strictly 1-2 pages matching 01_MASTER_CV.tex trim order.
    """
    def remove_section(b: str, sec_title: str) -> str:
        title_pat = re.escape(sec_title).replace(r"\&", r"(\\&|&)")
        pat = r"\\section\{" + title_pat + r"\}[\s\S]*?(?=(\\section\{|\\end\{document\}|$))"
        return re.sub(pat, "", b)

    body = latex_body
    is_master_template = (
        "Betopia" in latex_body or "Full Send Sports" in latex_body or "Niloy Sannyal" in latex_body
    )
    if is_master_template:
        body = remove_section(body, "Career Highlights")
        body = remove_section(body, "Enterprise AI Systems & Initiatives")
        body = remove_section(body, "Technical Leadership & Ownership")
        body = remove_section(body, "Certifications & Courses")

        job_text = f"{job_role} {job_description}".lower()
        needs_robotics = any(k in job_text for k in ["robot", "embedded", "hardware", "arduino", "drone", "iot", "firmware"])

        # Curate Projects section to 2-3 flagship projects
        selected_projects = []

        # 1. UFC ML Platform (Sub-100ms, FastAPI, MLOps, AWS)
        selected_projects.append(
            r"""\resumeTrioHeading{Full Send Sports AI -- UFC Prediction Platform \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://apps.apple.com/us/app/full-send-sports-ai/id6751740118}{\uline{App Store}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{End-to-end ML pipeline trained on \textbf{10,000+ UFC fights} with \textbf{80+ engineered features}; ensemble models deployed as a FastAPI service with \textbf{sub-100ms latency} for real-time predictions.}
  \resumeItem{Live on the iOS App Store, serving production traffic with high-availability cloud deployment.}
  \resumeItem{\textbf{Tech Stack:} Python, XGBoost, LightGBM, Scikit-learn, FastAPI, AWS.}
\resumeItemListEnd{}"""
        )

        # 2. Intelligent Real Estate Lead Platform
        selected_projects.append(
            r"""\resumeTrioHeading{Intelligent Real Estate Lead Platform \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://github.com/niloysannyal}{\uline{GitHub}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{Full-stack platform tracking and analyzing \textbf{28,000+ real estate listings} with automated lead scoring and recommendation algorithms (\textbf{95\%+ classification accuracy}).}
  \resumeItem{\textbf{Tech Stack:} Next.js 15, FastAPI, PostgreSQL, Redis, Scikit-learn.}
\resumeItemListEnd{}"""
        )

        if needs_robotics:
            selected_projects.append(
                r"""\resumeTrioHeading{Autonomous Rover with Robotic Arm \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://github.com/niloysannyal}{\uline{GitHub}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{Designed and built an autonomous four-wheel rover featuring custom robotic arm with \textbf{5 degrees of freedom}; real-time control with Arduino, ESP32, and custom PCB.}
  \resumeItem{\textbf{Tech Stack:} C++, Arduino, ESP32, Embedded C, Circuit Design.}
\resumeItemListEnd{}"""
            )

        projects_section = (
            "\\section{PROJECTS}\n\\resumeSubHeadingListStart{}\n"
            + "\n".join(selected_projects)
            + "\n\\resumeSubHeadingListEnd{}\n"
        )
        body = remove_section(body, "Projects")
        body = re.sub(r"(\\section\{EDUCATION\}|$)", lambda m: projects_section + m.group(1), body, count=1)

    return body


class CVDrafterService:
    """
    Executes Pass 1 (Senior Recruiter Drafter).
    Outputs tailored summary bullet, cover letter, and pruned LaTeX. Non-mutating.
    """

    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService()

    def select_summary_variant(
        self,
        job_role: str,
        job_description: str,
        headline: str = "",
        top_skills: Optional[List[str]] = None,
        is_niloy: bool = True,
    ) -> str:
        """Selects the canonical summary bullet variant matching target job focus."""
        if not is_niloy and headline:
            return f"\\resumeItem{{{headline}}}"

        text = f"{job_role} {job_description}".lower()

        if any(k in text for k in ["mlops", "platform", "infrastructure", "devops", "ci/cd", "kubernetes", "docker", "pipeline"]):
            return SUMMARY_VARIANTS["mlops_platform"]
        elif any(k in text for k in ["data science", "machine learning", "ml engineer", "model", "scikit", "xgboost", "predict"]):
            return SUMMARY_VARIANTS["ml_data_science"]
        elif any(k in text for k in ["backend", "full stack", "fullstack", "software engineer", "api", "fastapi", "django"]):
            return SUMMARY_VARIANTS["backend_fullstack"]
        else:
            return SUMMARY_VARIANTS["agentic_llm"]

    async def draft_cv(
        self,
        params: CVDraftInput,
        career_context: CandidateCareerContext,
    ) -> CVDraftOutput:
        company_clean = html.unescape(params.job_company or "")
        role_clean = html.unescape(params.job_role or "")

        # 1. Split preamble and body
        preamble, body = extract_preamble_and_body(career_context.master_latex)
        cleaned_body = strip_control_comments(body)

        # 2. Budget and prune LaTeX for 1-2 pages
        budgeted_body = prune_and_budget_latex(
            cleaned_body,
            job_role=role_clean,
            job_description=params.job_description,
        )

        # 3. Select base summary bullet
        summary_bullet = self.select_summary_variant(
            role_clean,
            params.job_description,
            headline=career_context.headline,
            top_skills=career_context.skills,
            is_niloy=career_context.is_niloy,
        )

        # 4. Senior Recruiter Drafter LLM Generation
        recruiter_context = (
            "You are a Senior Principal Tech Recruiter and Executive Talent Strategist with 20+ years "
            "of experience at Tier-1 tech enterprises. You have up-to-date 2026 hiring knowledge, modern ATS algorithms, "
            "and candidate positioning strategies. You tailor candidate CVs and outreach to maximize interview conversion "
            "without ever inventing false credentials or violating verified facts."
        )

        drafter_prompt = f"""
Act as a Senior Recruiter with 20 years of technical hiring experience.
Tailor {career_context.candidate_name}'s Master CV and application outreach for the following target job:

TARGET OPPORTUNITY:
- Company: {company_clean}
- Role: {role_clean}
- Job Description:
{params.job_description or ''}

CANDIDATE BASE SUMMARY TEMPLATE:
{summary_bullet}

NON-NEGOTIABLE INTEGRITY RULES:
1. STRICT FACT PRESERVATION: NEVER invent or inflate facts.
   Verified candidate facts:
{career_context.verified_facts_str}
2. RELEVANCE & ATS IMPACT:
   - Craft a high-impact tailored Executive Summary bullet specifically positioning {career_context.candidate_name} for {company_clean}'s {role_clean}.
   - Identify skills demanded by the job to highlight.
   - Budget strictly for 1-2 pages maximum.
3. OUTREACH:
   - Write a compelling 2-3 paragraph first-person cover letter.
   - List any explicit missing skill requirements under GAPS.

Provide your response in this exact format:
---TAILORED_SUMMARY---
\\resumeItem{{[Your tailored executive summary highlighting {career_context.candidate_name}'s verified experience matching {company_clean}'s {role_clean}]}}
---COVER_NOTE---
[Your 2-3 paragraph cover letter draft]
---GAPS---
[Bullet points of any missing requirements or 'None']
"""
        drafter_response = await self.llm_service.generate(
            prompt=drafter_prompt,
            context=recruiter_context,
        )

        # 5. Parse Drafter Response
        chosen_summary = summary_bullet
        draft_cover = ""
        gaps = []

        if "---TAILORED_SUMMARY---" in drafter_response:
            parts = drafter_response.split("---TAILORED_SUMMARY---")[1]
            if "---COVER_NOTE---" in parts:
                s_part, rest = parts.split("---COVER_NOTE---", 1)
                if "\\resumeItem" in s_part.strip():
                    chosen_summary = s_part.strip()
                if "---GAPS---" in rest:
                    c_part, g_part = rest.split("---GAPS---", 1)
                    draft_cover = c_part.strip()
                    gaps = [g.strip("- ").strip() for g in g_part.strip().split("\n") if g.strip("- ").strip()]
                else:
                    draft_cover = rest.strip()

        # 6. Assemble draft LaTeX
        assembled_body = re.sub(
            r"\\resumeItemListStart\s*\\resumeItem\{.*?\}\s*\\resumeItemListEnd",
            lambda _: f"\\resumeItemListStart\n  {chosen_summary}\n\\resumeItemListEnd",
            budgeted_body,
            count=1,
            flags=re.DOTALL,
        )
        draft_assembled_latex = f"{preamble}\n\\begin{{document}}\n{assembled_body}\n\\end{{document}}"

        return CVDraftOutput(
            draft_summary_bullet=chosen_summary,
            draft_cover_letter=draft_cover,
            raw_gaps=gaps,
            budgeted_latex_body=budgeted_body,
            preamble=preamble,
            draft_assembled_latex=draft_assembled_latex,
            drafter_raw_response=drafter_response,
        )

