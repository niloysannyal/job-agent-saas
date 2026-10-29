import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ApplyChannelType(str, Enum):
    GOOGLE_FORM = "google_form"
    TYPEFORM = "typeform"
    DIRECT_EMAIL = "direct_email"
    ATS_PORTAL = "ats_portal"
    DIRECT_MESSAGE = "direct_message"
    GENERIC_WEB = "generic_web"


@dataclass
class FormFieldQuestion:
    """Represents a specific question field extracted from an application form or posting."""
    id: str
    prompt: str
    field_type: str = "paragraph"  # "short_text" | "paragraph" | "url" | "number" | "choice"
    char_limit: Optional[int] = None
    is_required: bool = True
    suggested_focus: Optional[str] = None


@dataclass
class FormInspectionResult:
    """Comprehensive discovery analysis of how to apply for a target job."""
    channel_type: ApplyChannelType
    apply_url: str
    platform_name: str
    recruiter_email: Optional[str] = None
    target_handle: Optional[str] = None
    questions: List[FormFieldQuestion] = field(default_factory=list)
    detection_confidence: float = 1.0
    action_summary: str = ""


# Common email exclusions (generic support or marketing emails that are not hiring contacts)
GENERIC_EMAIL_IGNORE = {
    "support@adzuna.com",
    "info@adzuna.com",
    "contact@remotive.com",
    "hi@remoteok.com",
    "legal@remoteok.com",
    "privacy@adzuna.com",
}


class FormDetectiveService:
    """
    Autonomous Apply Channel and Form Detective.
    Analyzes destination apply links and posting descriptions to:
      1. Classify the exact application channel (Google Form, Direct Email, ATS Portal, DM).
      2. Extract recruiter contact info or target social handles.
      3. Discover or infer structured form questions that must be answered.
    """

    @classmethod
    def detect_channel(
        cls,
        apply_url: Optional[str] = None,
        posting_text: Optional[str] = None,
        company_name: Optional[str] = None,
        role_title: Optional[str] = None,
    ) -> FormInspectionResult:
        url = (apply_url or "").strip()
        text = posting_text or ""
        company = company_name or "Target Company"
        role = role_title or "Target Role"

        parsed_url = urlparse(url)
        netloc = parsed_url.netloc.lower()
        path = parsed_url.path.lower()

        # -------------------------------------------------------------
        # 1. Google Form Discovery
        # -------------------------------------------------------------
        if "forms.gle" in netloc or "docs.google.com/forms" in (netloc + path):
            questions = cls.extract_form_questions(text, company, role)
            return FormInspectionResult(
                channel_type=ApplyChannelType.GOOGLE_FORM,
                apply_url=url,
                platform_name="Google Forms",
                questions=questions,
                detection_confidence=0.98,
                action_summary=f"Direct Google Form detected. {len(questions)} tailored questions ready for auto-drafting.",
            )

        # Check if text contains an explicit Google Form link
        gform_match = re.search(r"https?://(forms\.gle/[a-zA-Z0-9_\-]+|docs\.google\.com/forms/[^\s\"']+)", text)
        if gform_match:
            gform_url = gform_match.group(0)
            questions = cls.extract_form_questions(text, company, role)
            return FormInspectionResult(
                channel_type=ApplyChannelType.GOOGLE_FORM,
                apply_url=gform_url,
                platform_name="Google Forms",
                questions=questions,
                detection_confidence=0.95,
                action_summary=f"Google Form link discovered in posting body. {len(questions)} tailored answers ready.",
            )

        # -------------------------------------------------------------
        # 2. Typeform / Tally / Airtable Discovery
        # -------------------------------------------------------------
        if "typeform.com" in netloc or "tally.so" in netloc or "airtable.com" in netloc:
            platform = "Typeform" if "typeform" in netloc else ("Tally" if "tally" in netloc else "Airtable Form")
            questions = cls.extract_form_questions(text, company, role)
            return FormInspectionResult(
                channel_type=ApplyChannelType.TYPEFORM,
                apply_url=url,
                platform_name=platform,
                questions=questions,
                detection_confidence=0.95,
                action_summary=f"{platform} application form detected with {len(questions)} question fields.",
            )

        # -------------------------------------------------------------
        # 3. Direct Email Discovery
        # -------------------------------------------------------------
        email = cls._extract_recruiter_email(url, text)
        if email:
            questions = [
                FormFieldQuestion(
                    id="email_subject",
                    prompt=f"Outreach Subject Line for {role} at {company}",
                    field_type="short_text",
                    char_limit=120,
                    is_required=True,
                    suggested_focus="High-converting, concise email subject",
                ),
                FormFieldQuestion(
                    id="email_cover_body",
                    prompt=f"Personalized Executive Outreach Email to {email}",
                    field_type="paragraph",
                    char_limit=2500,
                    is_required=True,
                    suggested_focus="Value proposition, key metrics, and call to action",
                ),
            ]
            return FormInspectionResult(
                channel_type=ApplyChannelType.DIRECT_EMAIL,
                apply_url=f"mailto:{email}",
                platform_name="Direct Recruiter Email",
                recruiter_email=email,
                questions=questions,
                detection_confidence=0.92,
                action_summary=f"Direct recruiter contact ({email}) discovered. Ready for 1-click Gmail draft creation.",
            )

        # -------------------------------------------------------------
        # 4. ATS Portal Discovery (Greenhouse, Lever, Workday, Ashby)
        # -------------------------------------------------------------
        ats_name = cls._identify_ats(netloc, path, text)
        if ats_name:
            questions = cls.extract_form_questions(text, company, role)
            return FormInspectionResult(
                channel_type=ApplyChannelType.ATS_PORTAL,
                apply_url=url,
                platform_name=ats_name,
                questions=questions,
                detection_confidence=0.90,
                action_summary=f"{ats_name} application portal identified. Tailored CV and portal answers prepared.",
            )

        # -------------------------------------------------------------
        # 5. Direct Message / Social Discovery (LinkedIn / X / Discord)
        # -------------------------------------------------------------
        dm_match = re.search(r"https?://(www\.)?(linkedin\.com/in/[a-zA-Z0-9_\-]+|twitter\.com/[a-zA-Z0-9_]+|x\.com/[a-zA-Z0-9_]+)", text)
        if dm_match:
            dm_url = dm_match.group(0)
            handle = dm_url.rstrip("/").split("/")[-1]
            platform = "LinkedIn" if "linkedin" in dm_url else "Twitter / X"
            questions = [
                FormFieldQuestion(
                    id="dm_connection_note",
                    prompt=f"Direct outreach note to {handle} on {platform} (under 300 chars)",
                    field_type="short_text",
                    char_limit=300,
                    is_required=True,
                    suggested_focus="Ultra-concise connection request mentioning role and mutual alignment",
                ),
                FormFieldQuestion(
                    id="dm_full_pitch",
                    prompt=f"Full direct message pitch to {handle}",
                    field_type="paragraph",
                    char_limit=1000,
                    is_required=False,
                    suggested_focus="InMail / direct message highlighting key production systems built",
                ),
            ]
            return FormInspectionResult(
                channel_type=ApplyChannelType.DIRECT_MESSAGE,
                apply_url=dm_url,
                platform_name=platform,
                target_handle=handle,
                questions=questions,
                detection_confidence=0.88,
                action_summary=f"Hiring contact ({handle} on {platform}) detected. Direct outreach notes prepared.",
            )

        # -------------------------------------------------------------
        # 6. Generic Web Fallback
        # -------------------------------------------------------------
        questions = cls.extract_form_questions(text, company, role)
        return FormInspectionResult(
            channel_type=ApplyChannelType.GENERIC_WEB,
            apply_url=url,
            platform_name="Company Careers Portal",
            questions=questions,
            detection_confidence=0.75,
            action_summary="Generic career portal link. Standard application materials and form answers drafted.",
        )

    @classmethod
    def _extract_recruiter_email(cls, url: str, text: str) -> Optional[str]:
        """Extract valid recruiter or hiring email from apply URL or posting text."""
        # 1. Check mailto in URL
        if url.startswith("mailto:"):
            email = url.replace("mailto:", "").split("?")[0].strip()
            if email and "@" in email and email.lower() not in GENERIC_EMAIL_IGNORE:
                return email

        # 2. Check posting text for hiring emails
        # Look for phrases like "send your resume to...", "email us at...", "apply to..."
        hiring_patterns = [
            r"(?:email|send|forward|reach out to|apply directly to|contact)[^.\n\r]{1,40}?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
            r"\b([a-zA-Z0-9_.+-]+@(?:jobs|careers|talent|hiring|recruiting)\.[a-zA-Z0-9-.]+)\b",
            r"\b(jobs|careers|hiring|talent)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b",
        ]

        for pat in hiring_patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                candidate_email = match.group(1) if "@" in match.group(1) else f"{match.group(1)}@{match.group(2)}"
                candidate_email = candidate_email.strip().lower()
                if candidate_email not in GENERIC_EMAIL_IGNORE:
                    return candidate_email

        # 3. Check for any standard email in text as fallback
        all_emails = re.findall(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b", text)
        for e in all_emails:
            e_lower = e.lower().strip()
            if e_lower not in GENERIC_EMAIL_IGNORE and not e_lower.endswith((".png", ".jpg", ".gif", ".webp")):
                return e_lower

        return None

    @classmethod
    def _identify_ats(cls, netloc: str, path: str, text: str) -> Optional[str]:
        """Identify ATS platform name from hostname or path."""
        ats_map = {
            "greenhouse.io": "Greenhouse ATS",
            "boards.greenhouse.io": "Greenhouse ATS",
            "lever.co": "Lever ATS",
            "jobs.lever.co": "Lever ATS",
            "ashbyhq.com": "Ashby ATS",
            "myworkdayjobs.com": "Workday ATS",
            "smartrecruiters.com": "SmartRecruiters",
            "bamboohr.com": "BambooHR",
            "workable.com": "Workable ATS",
            "breezy.hr": "Breezy HR",
            "recruitee.com": "Recruitee",
        }
        for domain, name in ats_map.items():
            if domain in netloc:
                return name

        # Check text for ATS badges
        if "greenhouse" in text.lower():
            return "Greenhouse ATS"
        if "lever" in text.lower():
            return "Lever ATS"
        if "workday" in text.lower():
            return "Workday ATS"

        return None

    @classmethod
    def extract_form_questions(
        cls,
        posting_text: str,
        company_name: str,
        role_title: str,
    ) -> List[FormFieldQuestion]:
        """
        Extract explicit form questions found in the posting text,
        or synthesize the standard high-impact application questionnaire for the role.
        """
        questions: List[FormFieldQuestion] = []
        seen_prompts = set()

        # Look for explicit questions in posting text
        question_patterns = [
            r"(?:^|[.:\n\r•\-\*\?])[ \t]*([A-Z][^.\n\r]{10,250}\?)",
            r"(?:^|[.:\n\r])[ \t]*(Why (?:do you want|are you interested)[^.\n\r]{5,200}[:?])",
            r"(?:^|[.:\n\r])[ \t]*(Please (?:describe|share|tell us)[^.\n\r]{5,200}[:?])",
            r"(?:^|[.:\n\r])[ \t]*(Describe (?:a time|a difficult|your experience)[^.\n\r]{5,200}[:?])",
        ]

        idx = 1
        for pat in question_patterns:
            matches = re.finditer(pat, posting_text, re.MULTILINE | re.IGNORECASE)
            for m in matches:
                prompt = m.group(1).strip()
                if len(prompt) >= 15 and prompt.lower() not in seen_prompts:
                    seen_prompts.add(prompt.lower())
                    questions.append(
                        FormFieldQuestion(
                            id=f"q_{idx}",
                            prompt=prompt,
                            field_type="paragraph",
                            char_limit=1500,
                            is_required=True,
                            suggested_focus="Concrete metrics, STAR alignment, and factual achievements",
                        )
                    )
                    idx += 1
                if len(questions) >= 5:
                    break

        # If no explicit form questions were in the text, provide the canonical
        # 4 application questions every top-tier engineering / AI / tech form requires
        if not questions:
            questions = [
                FormFieldQuestion(
                    id="why_company",
                    prompt=f"Why are you interested in joining {company_name} as {role_title}?",
                    field_type="paragraph",
                    char_limit=1500,
                    is_required=True,
                    suggested_focus=f"Alignment with {company_name}'s mission, technical challenges, and immediate contribution",
                ),
                FormFieldQuestion(
                    id="technical_challenge",
                    prompt="Describe a complex production system or difficult technical challenge you owned and resolved.",
                    field_type="paragraph",
                    char_limit=2000,
                    is_required=True,
                    suggested_focus="STAR methodology: situation, architecture, technical decision, and measurable outcome",
                ),
                FormFieldQuestion(
                    id="portfolio_links",
                    prompt="Link to your GitHub, portfolio, or a production project you built.",
                    field_type="url",
                    char_limit=500,
                    is_required=False,
                    suggested_focus="Verified production URLs and GitHub repositories",
                ),
                FormFieldQuestion(
                    id="compensation_availability",
                    prompt="What is your desired compensation expectation and notice period / availability?",
                    field_type="short_text",
                    char_limit=300,
                    is_required=True,
                    suggested_focus="Clear, market-aligned compensation and notice period matching profile",
                ),
            ]

        return questions
