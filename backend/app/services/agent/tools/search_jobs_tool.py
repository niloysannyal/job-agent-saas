from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import or_

from app.models.job import Job
from app.services.agent.base_tool import BaseAgentTool, ToolCategory, ToolExecutionContext, ToolResult


class SearchJobsInput(BaseModel):
    query: Optional[str] = Field(None, description="Keywords or job titles to search, e.g. 'Senior Python Engineer' or 'Remote AI'")
    location: Optional[str] = Field(None, description="Location filter such as 'Remote', 'London', 'Germany'")
    min_score: int = Field(50, description="Minimum match score threshold (0-100)")
    limit: int = Field(5, description="Maximum number of job recommendations to return (1-10)")


class SearchAndRankJobsTool(BaseAgentTool):
    name: str = "search_and_rank_jobs"
    description: str = "Searches, filters, and ranks candidate opportunities from the live multi-tenant Job Radar. Returns structured job cards with match scores and a JobRadarCarousel widget."
    category: ToolCategory = ToolCategory.SOURCING
    input_schema = SearchJobsInput
    requires_human_approval: bool = False

    async def execute(self, ctx: ToolExecutionContext, params: SearchJobsInput) -> ToolResult:
        session = ctx.db_session
        if not session:
            return ToolResult(
                success=False,
                summary="Database session unavailable",
                error_message="Active database session is required to search jobs.",
            )

        query = session.query(Job).filter(Job.account_id == ctx.account_id)

        # Apply is_active filter if present
        if hasattr(Job, "is_active"):
            query = query.filter(Job.is_active == True)

        if params.query:
            terms = [t.strip() for t in params.query.split() if len(t.strip()) > 1]
            if terms:
                conds = []
                for term in terms:
                    pattern = f"%{term}%"
                    conds.append(Job.role.ilike(pattern))
                    conds.append(Job.company.ilike(pattern))
                    conds.append(Job.description.ilike(pattern))
                query = query.filter(or_(*conds))

        if params.location:
            loc_pattern = f"%{params.location}%"
            query = query.filter(
                or_(
                    Job.location_type.ilike(loc_pattern),
                    Job.country.ilike(loc_pattern),
                    Job.description.ilike(loc_pattern)
                )
            )

        # Order by match score descending, then created_at
        jobs: List[Job] = query.order_by(Job.match_score.desc().nullslast()).limit(params.limit).all()

        if not jobs:
            # Fallback: return top latest jobs for the user
            jobs = session.query(Job).filter(Job.account_id == ctx.account_id).order_by(Job.created_at.desc()).limit(params.limit).all()

        items = []
        for j in jobs:
            items.append({
                "job_id": j.id,
                "role": j.role,
                "company": j.company,
                "location": j.location_type or j.country or "Flexible",
                "salary": j.salary or "Not disclosed",
                "match_score": int(j.match_score or 75),
                "apply_link": j.apply_link,
                "source": j.source,
            })

        ui_widget = {
            "type": "JobRadarCarousel",
            "version": "1.0",
            "props": {
                "title": f"Top Opportunities Found ({len(items)})",
                "query": params.query or "All Matches",
                "jobs": items,
            },
            "actions": [
                {
                    "id": "tailor_application",
                    "label": "Auto-Tailor CV",
                    "variant": "primary",
                    "payload": {"tool": "autonomous_tailor_cv", "job_id": items[0]["job_id"] if items else None}
                }
            ]
        }

        summary = f"Found {len(items)} matching opportunities. Top match: {items[0]['role']} at {items[0]['company']} ({items[0]['match_score']}% fit)." if items else "No jobs found matching query criteria."

        return ToolResult(
            success=True,
            summary=summary,
            data={"jobs": items, "count": len(items)},
            ui_widget=ui_widget,
        )
