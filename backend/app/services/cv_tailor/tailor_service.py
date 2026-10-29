import html
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


def prune_and_budget_latex(
    latex_body: str,
    job_role: str = "AI Engineer",
    job_description: str = "",
) -> str:
    """
    Budgets and prunes the Master CV body to strictly 1-2 pages matching 01_MASTER_CV.tex trim order:
    1. Cut 'Career Highlights' (overlaps Summary & Experience).
    2. Cut 'Enterprise AI Systems & Initiatives' (duplicates Experience).
    3. Cut 'Technical Leadership & Ownership' (overlaps Experience).
    4. Cut 'Certifications & Courses'.
    5. Cut 'Robotics & Embedded Systems' unless the job explicitly targets robotics/embedded.
    6. Curate Projects to top 2-3 most job-relevant production projects.
    7. Retain full Professional Experience (Betopia Limited + Softvence Agency), Technical Skills,
       Problem Solving, and Education.
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

        # 1. UFC ML Platform (Sub-100ms, FastAPI, MLOps, AWS) - high relevance for AI/ML/Backend
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

        # 2. Company Policy Chatbot or Domain Project
        if any(k in job_text for k in ["llm", "rag", "agent", "chat", "genai", "nlp", "langchain"]):
            selected_projects.append(
                r"""\resumeTrioHeading{Company Policy Chatbot \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://github.com/niloysannyal/Company_Policy_Chatbot}{\uline{GitHub}} \hspace{2pt} \textbar{} \hspace{2pt}
\href{https://company-policy-chatbot.vercel.app/}{\uline{Live Demo}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{RAG-based chatbot answering HR and IT policy questions with context-aware responses, using vector similarity search and persisted conversation memory.}
  \resumeItem{\textbf{Tech Stack:} Python, Streamlit, Gemini API, FAISS, LangChain, HTML, CSS, JavaScript.}
\resumeItemListEnd{}"""
            )
        elif any(k in job_text for k in ["vision", "cv", "cnn", "image", "crop"]):
            selected_projects.append(
                r"""\resumeTrioHeading{Crop Disease Classifier \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://github.com/niloysannyal/Crop_Disease_Classifier}{\uline{GitHub}} \hspace{2pt} \textbar{} \hspace{2pt}
\href{https://cropdiseaseclassifier.streamlit.app/}{\uline{Live Demo}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{CNN-based web app for plant disease detection across corn, potato, wheat, and rice leaves; trained from scratch achieving \textbf{97\% average accuracy} after processing and augmenting thousands of images.}
  \resumeItem{\textbf{Tech Stack:} Python, NumPy, TensorFlow, Keras, Streamlit.}
\resumeItemListEnd{}"""
            )
        else:
            selected_projects.append(
                r"""\resumeTrioHeading{Dhaka Home Rent Prediction \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://github.com/niloysannyal/Data_Science/tree/main/projects/DhakaHomeRentPrediction}{\uline{GitHub}} \hspace{2pt} \textbar{} \hspace{2pt}
\href{https://dhakahomerentprediction.onrender.com/}{\uline{Live Demo}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{ML regression system predicting Dhaka residential rent across \textbf{28,000+ listings}; Random Forest regression achieving \textbf{95\%+ accuracy} after tuning and cross-validation, with extensive feature engineering and outlier handling.}
  \resumeItem{\textbf{Tech Stack:} Python, Pandas, NumPy, Scikit-learn, Flask, Render.}
\resumeItemListEnd{}"""
            )

        # 3. FIFA World Cup 2026 Forecast (Full stack, React, FastAPI, AWS, 32k matches)
        selected_projects.append(
            r"""\resumeTrioHeading{FIFA World Cup 2026 Forecast \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://fifawc2026-simulator.netlify.app/}{\uline{Live Demo}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{Built and deployed a football forecasting platform using \textbf{32,247 international matches (1990--2025)}, featuring custom Elo ratings, probabilistic match prediction, and tournament simulation.}
  \resumeItem{\textbf{Tech Stack:} Python, Scikit-learn, FastAPI, React, Vite, Tailwind CSS, SQLite, AWS, Pandas, NumPy.}
\resumeItemListEnd{}"""
        )

        if needs_robotics:
            selected_projects.append(
                r"""\resumeTrioHeading{Arduino Robo-Car \hspace{2pt} \textbullet \hspace{2pt}
{\normalsize \textnormal{\href{https://github.com/niloysannyal/Robo-Car}{\uline{GitHub}}}}}{}{}
\vspace{-6pt}
\resumeItemListStart{}
  \resumeItem{Multifunctional Bluetooth-controlled robot car with custom Android app, supporting Manual, Line Following, Obstacle Avoidance via IR and ESP32-CAM sensor integration.}
  \resumeItem{\textbf{Tech Stack:} Arduino, C++, MIT App Inventor, Bluetooth HC-05, ESP32-CAM.}
\resumeItemListEnd{}"""
            )

        projects_block = (
            "\\section{Projects}\n\\resumeHeadingListStart{}\n\n"
            + "\n\n".join(selected_projects)
            + "\n\n\\resumeHeadingListEnd{}\n\n"
        )

        body = re.sub(
            r"\\section\{Projects\}[\s\S]*?(?=(\\section\{Problem Solving\}|\\section\{Education\}|\\end\{document\}|$))",
            lambda m: projects_block,
            body,
        )

    body = re.sub(r"\n{3,}", "\n\n", body.strip())
    return body


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
        Executes the full Drafter -> Reviewer -> Fact Audit -> Persistence pipeline
        acting as a Senior Executive Tech Recruiter with 20 years of experience.
        """
        # Step 1: Load master CV template source (from DB profile if available, else disk)
        master_source = None
        candidate_name = "Niloy Sannyal"
        if self.db_session:
            from app.models.profile import UserProfile
            user_prof = self.db_session.query(UserProfile).filter_by(account_id=account_id).first()
            if user_prof and user_prof.full_name and user_prof.full_name.strip():
                candidate_name = user_prof.full_name
            if user_prof and user_prof.master_cv_latex and user_prof.master_cv_latex.strip():
                master_source = user_prof.master_cv_latex

        if not master_source:
            master_cv_path = settings.resolve_cv_path()
            if master_cv_path.exists():
                master_source = master_cv_path.read_text(encoding="utf-8")
            else:
                raise FileNotFoundError(f"Master CV source not found at {master_cv_path}")

        # Step 2: Split and preserve preamble (starts cleanly from \documentclass, no %% comments)
        preamble, body = extract_preamble_and_body(master_source)
        cleaned_body = strip_control_comments(body)

        company_clean = html.unescape(job.company or "")
        role_clean = html.unescape(job.role or "")

        # Step 3: Select base summary variant
        summary_bullet = self.select_summary_variant(role_clean, job.description or "")

        # Step 4: Senior Recruiter Drafter Pass (Pass 1)
        recruiter_context = (
            "You are a Senior Principal Tech Recruiter and Executive Talent Strategist with 20+ years "
            "of experience at Tier-1 tech enterprises. You have up-to-date 2026 hiring knowledge, modern ATS algorithms, "
            "and candidate positioning strategies. You tailor candidate CVs and outreach to maximize interview conversion "
            "without ever inventing false credentials or violating verified facts."
        )

        drafter_prompt = f"""
Act as a Senior Recruiter with 20 years of technical hiring experience.
Tailor {candidate_name}'s Master CV and application outreach for the following target job:

TARGET OPPORTUNITY:
- Company: {company_clean}
- Role: {role_clean}
- Job Description:
{job.description or ''}

CANDIDATE BASE SUMMARY TEMPLATE:
{summary_bullet}

NON-NEGOTIABLE INTEGRITY RULES:
1. STRICT FACT PRESERVATION: NEVER invent or inflate facts.
   Verified numbers must remain exact:
   - 600+ salespersons (Betopia Sales Agent in Odoo CRM)
   - 10,000+ fights, 80+ features, sub-100ms (UFC model)
   - 530+ algorithmic problems (LeetCode/Codeforces)
   - sub-100ms inference latency for production FastAPI APIs
   - 28,000+ listings, 95%+ accuracy
2. RELEVANCE & ATS IMPACT:
   - Craft a high-impact tailored Executive Summary bullet specifically positioning {candidate_name} for {company_clean}'s {role_clean}.
   - Identify skills demanded by the job to highlight.
   - Budget strictly for 1-2 pages maximum.
3. OUTREACH:
   - Write a compelling 2-3 paragraph first-person cover letter.
   - List any explicit missing skill requirements under GAPS.

Provide your response in this exact format:
---TAILORED_SUMMARY---
\\resumeItem{{[Your tailored executive summary highlighting Niloy's verified experience matching {company_clean}'s {role_clean}]}}
---COVER_NOTE---
[Your 2-3 paragraph cover letter draft]
---GAPS---
[Bullet points of any missing requirements or 'None']
"""
        drafter_response = await self.llm_service.generate(
            prompt=drafter_prompt,
            context=recruiter_context,
        )

        # Step 5: Senior Recruiter Reviewer Pass (Pass 2)
        reviewer_prompt = f"""
You are the independent Reviewer pass auditing the output from a Senior Recruiter.
Review the following Drafter output for:
1. Any generic buzzwords, weak framing, or grammatical errors.
2. Any hallucinations (ensure NO fake credentials, degrees, or companies).
3. Keyword alignment with role: {role_clean} at {company_clean}.
4. Strict fact ledger preservation (600+ salespersons, 10,000+ fights, 80+ features, sub-100ms, 530+ problems).

Drafter Output:
{drafter_response}

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

        # Parse tailored summary bullet
        chosen_summary = summary_bullet
        if "---FINAL_SUMMARY---" in reviewer_response:
            s_part = reviewer_response.split("---FINAL_SUMMARY---")[1].split("---FINAL_COVER---")[0].strip()
            if "\\resumeItem" in s_part:
                chosen_summary = s_part
        elif "---TAILORED_SUMMARY---" in drafter_response:
            s_part = drafter_response.split("---TAILORED_SUMMARY---")[1].split("---COVER_NOTE---")[0].strip()
            if "\\resumeItem" in s_part:
                chosen_summary = s_part
        chosen_summary = html.unescape(chosen_summary)

        # Parse cover letter and gaps from response
        cover_content = ""
        if "---FINAL_COVER---" in reviewer_response:
            parts = reviewer_response.split("---FINAL_COVER---")[1]
            cover_content = parts.split("---CONFIRMED_GAPS---")[0].strip()
        elif "---COVER_NOTE---" in drafter_response:
            parts = drafter_response.split("---COVER_NOTE---")[1]
            cover_content = parts.split("---GAPS---")[0].strip()
        else:
            cover_content = f"Dear Hiring Team at {company_clean},\n\nI am excited to apply for the {role_clean} position."
        cover_content = html.unescape(cover_content).strip()

        # Parse gaps
        gaps = []
        if "---CONFIRMED_GAPS---" in reviewer_response:
            gaps_text = reviewer_response.split("---CONFIRMED_GAPS---")[1].strip()
            gaps = [line.strip("- *") for line in gaps_text.splitlines() if line.strip() and line.strip().lower() != "none"]

        # Step 6: Assemble tailored LaTeX budgeted strictly for 1-2 pages
        budgeted_body = prune_and_budget_latex(cleaned_body, job_role=job.role, job_description=job.description or "")
        pattern = r"(\\section\{Summary\}[\s\S]*?\\resumeItemListStart\{?\}?\s*)[\s\S]*?(\s*\\resumeItemListEnd)"
        tailored_body = re.sub(
            pattern,
            r"\g<1>\n  " + chosen_summary.replace("\\", "\\\\") + r"\g<2>",
            budgeted_body,
            count=1,
        )

        tailored_latex = f"{preamble}\n\n{tailored_body}\n\n\\end{{document}}"
        tailored_latex = re.sub(r"(\\end\{document\}\s*)+$", r"\\end{document}", tailored_latex.strip())

        # Validate LaTeX syntax
        braces_balanced = check_brace_balance(tailored_latex)
        if not braces_balanced:
            logger.warning("Unbalanced braces detected in tailored output; falling back to clean template body.")
            tailored_latex = f"{preamble}\n\n{budgeted_body}\n\n\\end{{document}}"

        # Step 7: Run Fact Audit and ATS Text-Layer Checks
        fact_audit = audit_fact_integrity(tailored_latex)
        ats_result = run_ats_text_layer_check(tailored_latex, job.description or "")

        # Dynamic page count calculation
        line_count = len([l for l in tailored_latex.splitlines() if l.strip()])
        computed_page_count = 1 if line_count < 110 else 2

        # Step 8: Database Persistence (Enforcing Human-in-the-Loop)
        cv_version = AccountCvVersion(
            account_id=account_id,
            job_id=job.id,
            tailored_latex=tailored_latex,
            ats_score=ats_result.score,
            page_count=computed_page_count,
            cut_summary={"strategy": "senior_recruiter_2page_budget", "gaps": gaps},
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
