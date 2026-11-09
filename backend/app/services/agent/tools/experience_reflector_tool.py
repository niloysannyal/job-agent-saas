from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.profile import (
    Certification,
    Education,
    ProfileSkill,
    Project,
    UserProfile,
    WorkExperience,
)
from app.services.agent.base_tool import BaseAgentTool, ToolCategory, ToolExecutionContext, ToolResult


class ExperienceReflectorInput(BaseModel):
    section: str = Field("all", description="'all' | 'skills' | 'projects' | 'experiences' | 'education'")


class ExperienceReflectorTool(BaseAgentTool):
    name: str = "reflect_candidate_profile"
    description: str = "Queries and reflects upon the candidate's canonical career record (skills, projects, work experiences, education, and target roles) without hallucinating unrecorded facts."
    category: ToolCategory = ToolCategory.INTELLIGENCE
    input_schema = ExperienceReflectorInput
    requires_human_approval: bool = False

    async def execute(self, ctx: ToolExecutionContext, params: ExperienceReflectorInput) -> ToolResult:
        session = ctx.db_session
        if not session:
            return ToolResult(
                success=False,
                summary="Database session unavailable",
                error_message="Active database session is required.",
            )

        prof = session.query(UserProfile).filter(UserProfile.account_id == ctx.account_id).first()
        if not prof:
            return ToolResult(
                success=True,
                summary="Candidate profile not yet created.",
                data={"profile": None},
            )

        skills = session.query(ProfileSkill).filter(ProfileSkill.profile_id == prof.id).all()
        projects = session.query(Project).filter(Project.profile_id == prof.id).all()
        experiences = session.query(WorkExperience).filter(WorkExperience.profile_id == prof.id).all()
        educations = session.query(Education).filter(Education.profile_id == prof.id).all()

        skills_list = [s.name for s in skills]
        projects_list = [{"name": p.title, "tech_stack": getattr(p, "technologies", None), "github_url": getattr(p, "github_url", None)} for p in projects]
        exp_list = [{"title": e.title, "company": e.company, "years": f"{e.start_date} - {e.end_date or 'Present'}"} for e in experiences]

        summary = (
            f"Candidate: {prof.full_name or 'Candidate'} ({prof.headline or 'Software Engineer'}). "
            f"{len(skills_list)} Skills ({', '.join(skills_list[:6])}...), "
            f"{len(projects_list)} Projects, {len(exp_list)} Experience entries."
        )

        return ToolResult(
            success=True,
            summary=summary,
            data={
                "name": prof.full_name,
                "headline": prof.headline,
                "skills": skills_list,
                "projects": projects_list,
                "experiences": exp_list,
                "education_count": len(educations),
            },
        )
