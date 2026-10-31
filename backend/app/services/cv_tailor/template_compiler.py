"""
CV Template Compiler.
Replaces semantic template placeholders with cleanly formatted, escaped LaTeX
derived from the candidate's structured career entities.
"""
import json
import re
from typing import Any, Dict, List, Optional


LATEX_SPECIAL_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
LATEX_REGEX = re.compile(r"([\\&%$#_{}~^])")


def escape_latex(text: Optional[str]) -> str:
    """Escape special LaTeX characters in a single pass to prevent double-escaping."""
    if not text:
        return ""
    return LATEX_REGEX.sub(lambda m: LATEX_SPECIAL_MAP[m.group(1)], str(text))


class CVTemplateCompiler:
    """Compiles structured profile data into a LaTeX document using curated templates."""

    @classmethod
    def compile_cv(
        cls,
        template_source: str,
        profile: Dict[str, Any],
        experiences: List[Dict[str, Any]],
        educations: List[Dict[str, Any]],
        skills: List[Dict[str, Any]],
        projects: Optional[List[Dict[str, Any]]] = None,
        certifications: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Compile complete CV LaTeX from structured profile data."""
        projects = projects or []
        certifications = certifications or []

        # 1. Contact / Header line
        full_name = escape_latex(profile.get("full_name") or "Candidate")
        headline = escape_latex(profile.get("headline") or profile.get("current_role") or "")

        contact_parts: List[str] = []
        if profile.get("phone"):
            contact_parts.append(escape_latex(profile["phone"]))
        if profile.get("email"):
            email_esc = escape_latex(profile["email"])
            contact_parts.append(f"\\href{{mailto:{profile['email']}}}{{{email_esc}}}")
        city = profile.get("location_city")
        country = profile.get("location_country")
        if city or country:
            loc = ", ".join(filter(None, [city, country]))
            contact_parts.append(escape_latex(loc))
        if profile.get("linkedin_url"):
            contact_parts.append(f"\\href{{{profile['linkedin_url']}}}{{LinkedIn}}")
        if profile.get("github_url"):
            contact_parts.append(f"\\href{{{profile['github_url']}}}{{GitHub}}")
        if profile.get("portfolio_url"):
            contact_parts.append(f"\\href{{{profile['portfolio_url']}}}{{Portfolio}}")

        contact_line = " $\\cdot$ ".join(contact_parts)

        # 2. Summary Section
        summary_text = profile.get("summary") or profile.get("core_narrative") or ""
        summary_section = ""
        if summary_text.strip():
            summary_section = (
                "\\section{Summary}\n"
                "\\resumeItemListStart\n"
                f"  \\resumeItem{{{escape_latex(summary_text.strip())}}}\n"
                "\\resumeItemListEnd\n"
                "\\vspace{-5pt}"
            )

        # 3. Work Experience Section
        exp_lines: List[str] = []
        if experiences:
            exp_lines.append("\\section{Work Experience}")
            exp_lines.append("\\resumeHeadingListStart")
            for exp in experiences:
                comp = escape_latex(exp.get("company", ""))
                title = escape_latex(exp.get("title", ""))
                loc = escape_latex(exp.get("location", ""))
                start = escape_latex(exp.get("start_date", ""))
                end = "Present" if exp.get("is_current") else escape_latex(exp.get("end_date") or "")
                date_str = f"{start} -- {end}" if start and end else (start or end)

                exp_lines.append(f"  \\resumeQuadHeading{{{title}}}{{{date_str}}}{{{comp}}}{{{loc}}}")

                # Bullets / highlights
                bullets = cls._parse_bullets(exp.get("highlights") or exp.get("description"))
                if bullets:
                    exp_lines.append("  \\resumeItemListStart")
                    for b in bullets:
                        exp_lines.append(f"    \\resumeItem{{{escape_latex(b)}}}")
                    exp_lines.append("  \\resumeItemListEnd")

            exp_lines.append("\\resumeHeadingListEnd")
            exp_lines.append("\\vspace{-5pt}")
        experience_section = "\n".join(exp_lines)

        # 4. Education Section
        edu_lines: List[str] = []
        if educations:
            edu_lines.append("\\section{Education}")
            edu_lines.append("\\resumeHeadingListStart")
            for edu in educations:
                inst = escape_latex(edu.get("institution", ""))
                deg = escape_latex(edu.get("degree", ""))
                field = escape_latex(edu.get("field_of_study", ""))
                full_deg = f"{deg} in {field}" if deg and field else (deg or field)
                start = escape_latex(edu.get("start_date", ""))
                end = escape_latex(edu.get("end_date", ""))
                date_str = f"{start} -- {end}" if start and end else (start or end)
                grade = escape_latex(edu.get("grade", ""))

                edu_lines.append(f"  \\resumeQuadHeading{{{full_deg}}}{{{date_str}}}{{{inst}}}{{{grade}}}")
            edu_lines.append("\\resumeHeadingListEnd")
            edu_lines.append("\\vspace{-5pt}")
        education_section = "\n".join(edu_lines)

        # 5. Skills Section
        skills_lines: List[str] = []
        if skills:
            skills_lines.append("\\section{Skills}")
            skills_lines.append("\\resumeHeadingListStart")
            # Group by category
            categories: Dict[str, List[str]] = {}
            for s in skills:
                cat = s.get("category") or "Technical"
                name = s.get("name", "").strip()
                if name:
                    categories.setdefault(cat, []).append(name)

            for cat_name, skill_list in categories.items():
                cat_esc = escape_latex(cat_name)
                skills_joined = ", ".join(escape_latex(name) for name in skill_list)
                skills_lines.append(f"  \\resumeSectionType{{{cat_esc}}}{{:}}{{{skills_joined}}}")

            skills_lines.append("\\resumeHeadingListEnd")
            skills_lines.append("\\vspace{-5pt}")
        skills_section = "\n".join(skills_lines)

        # 6. Projects Section
        proj_lines: List[str] = []
        if projects:
            proj_lines.append("\\section{Projects}")
            proj_lines.append("\\resumeHeadingListStart")
            for p in projects:
                title = escape_latex(p.get("title", ""))
                role = escape_latex(p.get("role", ""))
                tech = escape_latex(p.get("technologies", ""))
                sub = f"{role} $\\cdot$ \\textmd{{{tech}}}" if role and tech else (role or tech)
                start = escape_latex(p.get("start_date", ""))
                end = escape_latex(p.get("end_date", ""))
                date_str = f"{start} -- {end}" if start and end else (start or end)

                proj_lines.append(f"  \\resumeQuadHeading{{{title}}}{{{date_str}}}{{{sub}}}{{}}")

                bullets = cls._parse_bullets(p.get("highlights") or p.get("description"))
                if bullets:
                    proj_lines.append("  \\resumeItemListStart")
                    for b in bullets:
                        proj_lines.append(f"    \\resumeItem{{{escape_latex(b)}}}")
                    proj_lines.append("  \\resumeItemListEnd")

            proj_lines.append("\\resumeHeadingListEnd")
            proj_lines.append("\\vspace{-5pt}")
        projects_section = "\n".join(proj_lines)

        # 7. Certifications Section
        cert_lines: List[str] = []
        if certifications:
            cert_lines.append("\\section{Certifications}")
            cert_lines.append("\\resumeHeadingListStart")
            for c in certifications:
                name = escape_latex(c.get("name", ""))
                org = escape_latex(c.get("issuing_organization", ""))
                date = escape_latex(c.get("issue_date", ""))
                cert_lines.append(f"  \\resumeQuadHeading{{{name}}}{{{date}}}{{{org}}}{{}}")
            cert_lines.append("\\resumeHeadingListEnd")
            cert_lines.append("\\vspace{-5pt}")
        certifications_section = "\n".join(cert_lines)

        # Placeholders replacement
        output = template_source
        output = output.replace("{{FULL_NAME}}", full_name)
        output = output.replace("{{HEADLINE}}", headline)
        output = output.replace("{{CONTACT_LINE}}", contact_line)
        output = output.replace("{{SUMMARY_SECTION}}", summary_section)
        output = output.replace("{{EXPERIENCE_SECTION}}", experience_section)
        output = output.replace("{{EDUCATION_SECTION}}", education_section)
        output = output.replace("{{SKILLS_SECTION}}", skills_section)
        output = output.replace("{{PROJECTS_SECTION}}", projects_section)
        output = output.replace("{{CERTIFICATIONS_SECTION}}", certifications_section)

        return output

    @staticmethod
    def _parse_bullets(raw: Any) -> List[str]:
        """Convert highlights string, JSON array, or newline list into a list of strings."""
        if not raw:
            return []
        if isinstance(raw, list):
            return [str(item).strip() for item in raw if str(item).strip()]
        if isinstance(raw, str):
            trimmed = raw.strip()
            if trimmed.startswith("[") and trimmed.endswith("]"):
                try:
                    parsed = json.loads(trimmed)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except Exception:
                    pass
            # Split by newline
            return [line.lstrip("•-* ").strip() for line in trimmed.split("\n") if line.strip()]
        return []
