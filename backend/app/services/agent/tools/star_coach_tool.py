from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.interview import StarStory
from app.services.agent.base_tool import BaseAgentTool, ToolCategory, ToolExecutionContext, ToolResult


class StarCoachInput(BaseModel):
    competency: Optional[str] = Field(None, description="Behavioral competency or question theme, e.g. 'leadership', 'debugging under pressure', 'system architecture'")
    job_title: Optional[str] = Field(None, description="Optional target job title for contextual coaching")
    company: Optional[str] = Field(None, description="Optional target company name")


class StarCoachTool(BaseAgentTool):
    name: str = "star_interview_prep"
    description: str = "Retrieves and aligns the candidate's STAR interview stories (Situation, Task, Action, Result) against target competencies or upcoming interviews. Delivers structured coaching cards."
    category: ToolCategory = ToolCategory.COACHING
    input_schema = StarCoachInput
    requires_human_approval: bool = False

    async def execute(self, ctx: ToolExecutionContext, params: StarCoachInput) -> ToolResult:
        session = ctx.db_session
        if not session:
            return ToolResult(
                success=False,
                summary="Database session unavailable",
                error_message="Active database session is required.",
            )

        stories = session.query(StarStory).filter(StarStory.account_id == ctx.account_id).all()

        if not stories:
            return ToolResult(
                success=True,
                summary="No STAR stories recorded yet in the Interview Story Bank.",
                data={"stories": []},
            )

        selected_story = stories[0]
        if params.competency:
            comp_lower = params.competency.lower()
            for s in stories:
                tags = (s.good_for_tags or "").lower()
                title = (s.title or "").lower()
                if comp_lower in tags or comp_lower in title:
                    selected_story = s
                    break

        simulated_q = (
            f"Tell me about a time you handled a critical challenge in {params.competency or 'system scalability'}."
            if params.competency else "Tell me about a project where you demonstrated technical ownership end-to-end."
        )

        ui_widget = {
            "type": "STARStoryMatch",
            "version": "1.0",
            "props": {
                "question": simulated_q,
                "story_title": selected_story.title,
                "good_for_tags": selected_story.good_for_tags or "System Architecture, Production Impact",
                "situation": selected_story.situation,
                "action": selected_story.action,
                "result": selected_story.result,
                "job_title": params.job_title,
                "company": params.company,
            },
            "actions": []
        }

        summary = f"Selected STAR story '{selected_story.title}' to address question: '{simulated_q}'"

        return ToolResult(
            success=True,
            summary=summary,
            data={
                "story_id": selected_story.id,
                "title": selected_story.title,
                "simulated_question": simulated_q,
            },
            ui_widget=ui_widget,
        )
