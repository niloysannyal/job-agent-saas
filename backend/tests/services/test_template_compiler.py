import pytest
from app.services.cv_tailor.template_compiler import CVTemplateCompiler, escape_latex


def test_escape_latex():
    raw = "R&D at Company & Co. (100% growth) with $100k budget #1 _tag_ {val} ~home^peak \\path"
    escaped = escape_latex(raw)
    assert r"\&" in escaped
    assert r"\%" in escaped
    assert r"\$" in escaped
    assert r"\#" in escaped
    assert r"\_" in escaped
    assert r"\{" in escaped
    assert r"\}" in escaped
    assert r"\textasciitilde{}" in escaped
    assert r"\textasciicircum{}" in escaped
    assert r"\textbackslash{}" in escaped


def test_cv_template_compiler_replaces_all_placeholders():
    template = """
\\documentclass{article}
\\begin{document}
{{FULL_NAME}}
{{HEADLINE}}
{{CONTACT_LINE}}
{{SUMMARY_SECTION}}
{{EXPERIENCE_SECTION}}
{{EDUCATION_SECTION}}
{{SKILLS_SECTION}}
{{PROJECTS_SECTION}}
{{CERTIFICATIONS_SECTION}}
\\end{document}
"""
    profile = {
        "full_name": "Jane Doe",
        "headline": "Full-Stack Engineer & Architect",
        "phone": "+1-555-0199",
        "email": "jane@example.com",
        "location_city": "San Francisco",
        "location_country": "USA",
        "linkedin_url": "https://linkedin.com/in/janedoe",
        "github_url": "https://github.com/janedoe",
        "summary": "Full-Stack Engineer with 5+ years building distributed cloud platforms.",
    }
    experiences = [
        {
            "company": "Stripe & Co",
            "title": "Senior Platform Engineer",
            "location": "San Francisco, CA",
            "location_type": "remote",
            "start_date": "2022-01",
            "end_date": None,
            "is_current": True,
            "highlights": [
                "Scaled payments microservices to 10k requests/second.",
                "Reduced p99 latency by 35% using Redis caching.",
            ],
        }
    ]
    educations = [
        {
            "institution": "Stanford University",
            "degree": "B.S.",
            "field_of_study": "Computer Science",
            "start_date": "2016",
            "end_date": "2020",
            "grade": "GPA 3.9/4.0",
        }
    ]
    skills = [
        {"name": "Python", "category": "Languages"},
        {"name": "TypeScript", "category": "Languages"},
        {"name": "FastAPI", "category": "Frameworks"},
        {"name": "AWS", "category": "Cloud & DevOps"},
    ]
    projects = [
        {
            "title": "OpenCloud Mesh",
            "role": "Creator & Lead Maintainer",
            "start_date": "2023",
            "end_date": "Present",
            "technologies": "Go, Docker, Kubernetes",
            "highlights": ["1,500+ GitHub stars with active enterprise adoption."],
        }
    ]
    certifications = [
        {
            "name": "AWS Certified Solutions Architect",
            "issuing_organization": "Amazon Web Services",
            "issue_date": "2023",
        }
    ]

    compiled = CVTemplateCompiler.compile_cv(
        template_source=template,
        profile=profile,
        experiences=experiences,
        educations=educations,
        skills=skills,
        projects=projects,
        certifications=certifications,
    )

    # Verify no template placeholders remain
    assert "{{FULL_NAME}}" not in compiled
    assert "{{HEADLINE}}" not in compiled
    assert "{{CONTACT_LINE}}" not in compiled
    assert "{{SUMMARY_SECTION}}" not in compiled
    assert "{{EXPERIENCE_SECTION}}" not in compiled
    assert "{{EDUCATION_SECTION}}" not in compiled
    assert "{{SKILLS_SECTION}}" not in compiled
    assert "{{PROJECTS_SECTION}}" not in compiled
    assert "{{CERTIFICATIONS_SECTION}}" not in compiled

    # Verify content and escaping
    assert "Jane Doe" in compiled
    assert "Full-Stack Engineer \\& Architect" in compiled
    assert "Stripe \\& Co" in compiled
    assert "Senior Platform Engineer" in compiled
    assert "Stanford University" in compiled
    assert "OpenCloud Mesh" in compiled
    assert "AWS Certified Solutions Architect" in compiled

