import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

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
