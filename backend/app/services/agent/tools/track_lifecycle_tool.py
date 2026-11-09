from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.application import Application
from app.models.job import Job
from app.services.agent.base_tool import BaseAgentTool, ToolCategory, ToolExecutionContext, ToolResult


class TrackLifecycleInput(BaseModel):
    action: str = Field("list", description="'list' applications or 'update_status'")
    application_id: Optional[str] = Field(None, description="Application ID when updating status")
    new_status: Optional[str] = Field(None, description="New status: 'draft', 'applied', 'interviewing', 'offer', 'rejected'")
    status_filter: Optional[str] = Field(None, description="Optional status filter when listing")


class TrackApplicationLifecycleTool(BaseAgentTool):
    name: str = "track_application_lifecycle"
    description: str = "Monitors candidate application pipeline, tracks stage progression (Applied, Interviewing, Offer), detects follow-ups due, and renders pipeline analytics."
    category: ToolCategory = ToolCategory.LIFECYCLE
    input_schema = TrackLifecycleInput
    requires_human_approval: bool = False

    async def execute(self, ctx: ToolExecutionContext, params: TrackLifecycleInput) -> ToolResult:
        session = ctx.db_session
        if not session:
            return ToolResult(
                success=False,
                summary="Database session unavailable",
                error_message="Active database session is required.",
            )

        if params.action == "update_status" and params.application_id and params.new_status:
            app = session.query(Application).filter(
                Application.id == params.application_id,
                Application.account_id == ctx.account_id
            ).first()
            if not app:
                return ToolResult(
                    success=False,
                    summary=f"Application {params.application_id} not found",
                    error_message=f"Application {params.application_id} not found.",
                )
            old_status = app.status
            app.status = params.new_status
            session.commit()
            return ToolResult(
                success=True,
                summary=f"Updated application {params.application_id[:8]} status from '{old_status}' to '{params.new_status}'.",
                data={"application_id": app.id, "old_status": old_status, "new_status": app.status},
            )

        # Default: list & summarize pipeline
        query = session.query(Application).filter(Application.account_id == ctx.account_id)
        if params.status_filter:
            query = query.filter(Application.status == params.status_filter)

        apps = query.order_by(Application.created_at.desc()).limit(20).all()

        counts = {"draft": 0, "applied": 0, "interviewing": 0, "offer": 0, "rejected": 0}
        all_apps = session.query(Application).filter(Application.account_id == ctx.account_id).all()
        for a in all_apps:
            s = (a.status or "draft").lower()
            counts[s] = counts.get(s, 0) + 1

        recent_items = []
        for a in apps[:6]:
            job = session.query(Job).filter(Job.id == a.job_id).first()
            recent_items.append({
                "application_id": a.id,
                "job_title": job.role if job else "Role",
                "company": job.company if job else "Company",
                "status": a.status,
                "channel": a.channel,
                "sent_at": a.sent_at.isoformat() if a.sent_at else None,
            })

        ui_widget = {
            "type": "FunnelInsight",
            "version": "1.0",
            "props": {
                "funnel_counts": counts,
                "recent_applications": recent_items,
            },
            "actions": []
        }

        summary = (
            f"Pipeline Summary: {counts.get('draft', 0)} Drafts, {counts.get('applied', 0)} Applied, "
            f"{counts.get('interviewing', 0)} Interviewing, {counts.get('offer', 0)} Offers."
        )

        return ToolResult(
            success=True,
            summary=summary,
            data={"counts": counts, "recent": recent_items},
            ui_widget=ui_widget,
        )
