import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class ParsedProfile:
    """Structured representation of parsed user profile and CV."""
    target_roles_text: str
    dealbreakers_text: str
    declared_languages: List[str] = field(default_factory=lambda: ["english"])
    cv_clean_text: str = ""
    combined_embedding_text: str = ""


class ProfileParser:
    """
    Parses cv_templates/01_MASTER_CV.tex and docs/USER_PROFILE.md.

    KNOWN FORMAT LIMITATIONS IN docs/USER_PROFILE.md (flagged per instructions):
    ----------------------------------------------------------------------------
    1. Spoken Languages:
       USER_PROFILE.md currently contains NO explicit declared spoken languages
       section (it lists technical programming languages in the CV and notes an
       English writing preference in Tone & Style).
       Behavior: We search for an explicit '- Languages:' / '## Languages' entry;
       if not found, we default to ['english'] and flag this as an unconfigured field.
    2. Dealbreakers:
       The dealbreaker in USER_PROFILE.md is currently free-text prose:
         '- Dealbreakers: generic/low-substance roles that don't involve real production systems'
       Free-text prose without structured boolean criteria (e.g., minimum salary,
       mandatory remote, specific prohibited technologies, or visa requirement)
       cannot be evaluated deterministically by regex.
    """

    @staticmethod
    def extract_clean_cv_text(latex_content: str) -> str:
        """
        Extract readable text from LaTeX CV, stripping comments and common markup.
        """
        lines: List[str] = []
        for line in latex_content.splitlines():
            stripped = line.strip()
            # Ignore control comments
            if stripped.startswith("%"):
                continue
            # Strip inline comments (% not preceded by backslash)
            clean_line = re.sub(r"(?<!\\)%.*$", "", line)
            # Remove common LaTeX formatting commands while keeping inner text
            clean_line = re.sub(r"\\textbf\{([^}]*)\}", r"\1", clean_line)
            clean_line = re.sub(r"\\textit\{([^}]*)\}", r"\1", clean_line)
            clean_line = re.sub(r"\\uline\{([^}]*)\}", r"\1", clean_line)
            clean_line = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", clean_line)
            clean_line = re.sub(r"\\resumeItem\{([^}]*)\}", r"\1", clean_line)
            clean_line = re.sub(r"\\section\{([^}]*)\}", r"\n=== \1 ===\n", clean_line)
            # Strip remaining backslash commands
            clean_line = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{([^}]*)\})?", r"\3", clean_line)
            clean_line = clean_line.replace("{", "").replace("}", "").replace("\\", "")
            if clean_line.strip():
                lines.append(clean_line.strip())

        return "\n".join(lines)

    @classmethod
    def parse(
        cls,
        cv_path: Optional[Path] = None,
        profile_path: Optional[Path] = None,
    ) -> ParsedProfile:
        cv_file = cv_path or settings.resolve_cv_path()
        profile_file = profile_path or settings.resolve_profile_path()

        cv_clean_text = ""
        if cv_file.exists():
            raw_cv = cv_file.read_text(encoding="utf-8")
            cv_clean_text = cls.extract_clean_cv_text(raw_cv)
        else:
            logger.warning(f"Master CV not found at {cv_file}")

        target_roles_text = ""
        dealbreakers_text = ""
        declared_languages = ["english"]

        if profile_file.exists():
            raw_profile = profile_file.read_text(encoding="utf-8")

            # Extract Target roles
            roles_match = re.search(
                r"^[ \t]*-[ \t]*Target roles:[ \t]*(.+?)(?=^[ \t]*-|\Z)",
                raw_profile,
                re.MULTILINE | re.DOTALL,
            )
            if roles_match:
                target_roles_text = " ".join(roles_match.group(1).split())

            # Extract Dealbreakers
            deal_match = re.search(
                r"^[ \t]*-[ \t]*Dealbreakers:[ \t]*(.+?)(?=^[ \t]*-|\Z)",
                raw_profile,
                re.MULTILINE | re.DOTALL,
            )
            if deal_match:
                dealbreakers_text = " ".join(deal_match.group(1).split())

            # Extract Languages if declared
            lang_match = re.search(
                r"^[ \t]*-[ \t]*Languages?:[ \t]*(.+?)(?=^[ \t]*-|\Z)",
                raw_profile,
                re.MULTILINE | re.DOTALL,
            )
            if lang_match:
                raw_langs = lang_match.group(1).lower()
                # Split by commas / slashes and clean up proficiency qualifiers
                langs: List[str] = []
                for part in re.split(r"[,/;\n]", raw_langs):
                    cleaned = re.sub(r"\(.*?\)", "", part).strip().lower()
                    if cleaned:
                        langs.append(cleaned)
                if langs:
                    declared_languages = langs
            else:
                logger.info(
                    "No explicit 'Languages:' declared in USER_PROFILE.md. Defaulting to ['english']."
                )
        else:
            logger.warning(f"USER_PROFILE.md not found at {profile_file}")

        # Combined representation for vector embedding:
        # Target Roles front-loaded + full CV text
        combined = f"TARGET ROLES:\n{target_roles_text}\n\nEXPERIENCE AND SKILLS:\n{cv_clean_text}"

        return ParsedProfile(
            target_roles_text=target_roles_text,
            dealbreakers_text=dealbreakers_text,
            declared_languages=declared_languages,
            cv_clean_text=cv_clean_text,
            combined_embedding_text=combined.strip(),
        )

    @classmethod
    def parse_from_db(
        cls,
        db: Any,
        account_id: str,
        cv_path: Optional[Path] = None,
        profile_path: Optional[Path] = None,
    ) -> ParsedProfile:
        """
        Dynamically extracts candidate profile and CV data from database models:
        (UserProfile, TargetDesignation, SpokenLanguage, ProfileSkill, WorkExperience,
        Project, Education, Certification, and UserResume).
        Grounded 100% in the user's structured database profile, with default resume context.
        """
        from app.models.profile import UserProfile, UserResume
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        profile = None
        default_resume = None
        if db is not None:
            try:
                stmt = (
                    select(UserProfile)
                    .where(UserProfile.account_id == account_id)
                    .options(
                        selectinload(UserProfile.target_designations),
                        selectinload(UserProfile.spoken_languages),
                        selectinload(UserProfile.skills),
                        selectinload(UserProfile.work_experiences),
                        selectinload(UserProfile.projects),
                        selectinload(UserProfile.educations),
                        selectinload(UserProfile.certifications),
                    )
                )
                profile = db.scalars(stmt).first()

                resume_stmt = (
                    select(UserResume)
                    .where(UserResume.account_id == account_id)
                    .order_by(UserResume.is_default.desc(), UserResume.created_at.desc())
                )
                default_resume = db.scalars(resume_stmt).first()
            except Exception as e:
                logger.warning(f"Failed to query UserProfile/UserResume from DB for {account_id}: {e}")

        if profile:
            # 1. Target roles from TargetDesignation rows or current_role
            roles = [td.title for td in (profile.target_designations or []) if td.title]
            if not roles and profile.current_role:
                roles = [profile.current_role]
            target_roles_text = ", ".join(roles)

            # 2. Dealbreakers
            dealbreakers_text = profile.dealbreakers or ""

            # 3. Spoken languages
            langs = [sl.language.lower().strip() for sl in (profile.spoken_languages or []) if sl.language]
            declared_languages = langs if langs else ["english"]

            # 4. Synthesize structured profile experience and skills
            sections: List[str] = []

            # Profile summary / headline / positioning
            summary_parts = []
            if profile.headline:
                summary_parts.append(f"Headline: {profile.headline}")
            if profile.summary:
                summary_parts.append(f"Summary: {profile.summary}")
            if profile.current_role or profile.current_company:
                curr = f"Current Role: {profile.current_role or ''}"
                if profile.current_company:
                    curr += f" at {profile.current_company}"
                summary_parts.append(curr)
            if profile.core_narrative:
                summary_parts.append(f"Core Narrative: {profile.core_narrative}")
            if profile.primary_identity:
                summary_parts.append(f"Primary Identity: {profile.primary_identity}")
            if summary_parts:
                sections.append("\n".join(summary_parts))

            # Skills
            if profile.skills:
                skills_by_cat: Dict[str, List[str]] = {}
                for s in profile.skills:
                    cat = s.category or "General"
                    entry = f"{s.name} ({s.proficiency})" if s.proficiency else s.name
                    skills_by_cat.setdefault(cat, []).append(entry)
                skill_lines = [f"Skills ({cat}): {', '.join(items)}" for cat, items in skills_by_cat.items()]
                sections.append("\n".join(skill_lines))

            # Work Experience
            if profile.work_experiences:
                exp_lines = ["Experience:"]
                for we in profile.work_experiences:
                    period = f"{we.start_date} - {we.end_date or ('Present' if we.is_current else '')}"
                    line = f"- {we.title} at {we.company} ({period})"
                    if we.description:
                        line += f": {we.description}"
                    if we.highlights:
                        line += f" | Key achievements: {we.highlights}"
                    exp_lines.append(line)
                sections.append("\n".join(exp_lines))

            # Projects
            if profile.projects:
                proj_lines = ["Projects:"]
                for p in profile.projects:
                    line = f"- {p.title}"
                    if p.technologies:
                        line += f" (Tech: {p.technologies})"
                    if p.highlights:
                        line += f": {p.highlights}"
                    proj_lines.append(line)
                sections.append("\n".join(proj_lines))

            # Education & Credentials
            edu_parts = []
            if profile.educations:
                for ed in profile.educations:
                    edu_parts.append(f"- {ed.degree} from {ed.institution} ({ed.field_of_study or ''})")
            if profile.certifications:
                for c in profile.certifications:
                    edu_parts.append(f"- Certification: {c.name} by {c.issuing_organization}")
            if edu_parts:
                sections.append("Education & Credentials:\n" + "\n".join(edu_parts))

            # Default Resume / Uploaded context
            resume_text = ""
            if default_resume and default_resume.extracted_text:
                resume_text = default_resume.extracted_text.strip()
            elif profile.master_cv_latex:
                resume_text = cls.extract_clean_cv_text(profile.master_cv_latex)

            if resume_text:
                sections.append(f"Resume Content ({default_resume.name if default_resume else 'Profile CV'}):\n{resume_text}")

            cv_clean_text = "\n\n".join(sections)
            combined = f"TARGET ROLES:\n{target_roles_text}\n\nEXPERIENCE AND SKILLS:\n{cv_clean_text}"
            return ParsedProfile(
                target_roles_text=target_roles_text,
                dealbreakers_text=dealbreakers_text,
                declared_languages=declared_languages,
                cv_clean_text=cv_clean_text,
                combined_embedding_text=combined.strip(),
            )

        # Clean fallback to disk files
        return cls.parse(cv_path=cv_path, profile_path=profile_path)

