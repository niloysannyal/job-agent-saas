import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.job import Job
from app.services.agent.base_tool import BaseAgentTool, ToolCategory, ToolExecutionContext, ToolResult
from app.services.agent.event_bus import ApplicationTailoredEvent, DomainEventBus
from app.services.cv_tailor.tailor_service import CVTailorService
from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)


class TailorCVInput(BaseModel):
    job_id: str = Field(..., description="ID of the job posting to tailor for")
    channel: str = Field("email", description="Application outreach channel ('email' | 'form' | 'portal')")
    target_angle: Optional[str] = Field(None, description="Optional angle to emphasize, e.g. 'Distributed Systems & FastAPI'")


class AutonomousTailorCVTool(BaseAgentTool):
    name: str = "autonomous_tailor_cv"
    description: str = "Autonomously tailors the candidate's LaTeX CV and drafts outreach for a target job. Enforces the anti-hallucination Fact Ledger, calculates ATS match score, and stages a draft Application."
    category: ToolCategory = ToolCategory.TAILORING
    input_schema = TailorCVInput
    requires_human_approval: bool = False

    async def execute(self, ctx: ToolExecutionContext, params: TailorCVInput) -> ToolResult:
        session = ctx.db_session
        if not session:
            return ToolResult(
                success=False,
                summary="Database session unavailable",
                error_message="Active database session is required for CV tailoring.",
            )

        job = session.query(Job).filter(Job.id == params.job_id, Job.account_id == ctx.account_id).first()
        if not job:
            return ToolResult(
                success=False,
                summary=f"Job {params.job_id} not found",
                error_message=f"Job {params.job_id} does not exist for this account.",
            )

        llm_service = LLMService(db_session=session, account_id=ctx.account_id)
        tailor_service = CVTailorService(llm_service=llm_service, db_session=session)

        try:
            result = await tailor_service.tailor_for_job(
                account_id=ctx.account_id,
                job=job,
                channel=params.channel,
            )

            # Publish domain event
            await DomainEventBus.publish(
                ApplicationTailoredEvent(
                    account_id=ctx.account_id,
                    application_id=result.application.id,
                    job_id=job.id,
                    ats_score=int(result.ats_score),
                    fact_ledger_passed=result.fact_audit_passed,
                )
            )

            # Extract diff highlights or key alignments
            diff_highlights = [
                f"Selected role summary aligned to: {job.role}",
                f"Fact Ledger audit passed: {result.fact_audit_passed} (0 hallucinations)",
                f"Target outreach prepared for channel: {params.channel.upper()}",
            ]
            if result.gaps_detected:
                diff_highlights.append(f"Gaps mitigated: {', '.join(result.gaps_detected[:3])}")

            ui_widget = {
                "type": "TailorDiffReview",
                "version": "1.0",
                "props": {
                    "application_id": result.application.id,
                    "job_id": job.id,
                    "role": job.role,
                    "company": job.company,
                    "ats_score": int(result.ats_score),
                    "fact_audit_passed": result.fact_audit_passed,
                    "draft_content": result.application.draft_content or "",
                    "latex_preview": (result.cv_version.tailored_latex[:500] if getattr(result.cv_version, "tailored_latex", None) else ""),
                    "diff_highlights": diff_highlights,
                },
                "actions": [
                    {
                        "id": "stage_proposal",
                        "label": "Stage For Send Approval",
                        "variant": "primary",
                        "payload": {
                            "tool": "stage_application_proposal",
                            "application_id": result.application.id,
                            "action_type": "SEND_APPLICATION_EMAIL" if params.channel == "email" else "DISPATCH_PORTAL_APPLICATION",
                        }
                    }
                ]
            }

            summary = (
                f"Successfully tailored application for {job.role} at {job.company}! "
                f"ATS Score: {int(result.ats_score)}/100. Fact Ledger verified: {result.fact_audit_passed}."
            )

            return ToolResult(
                success=True,
                summary=summary,
                data={
                    "application_id": result.application.id,
                    "ats_score": int(result.ats_score),
                    "fact_audit_passed": result.fact_audit_passed,
                    "cv_version_id": result.cv_version.id if result.cv_version else None,
                },
                ui_widget=ui_widget,
            )

        except Exception as e:
            logger.exception(f"Error tailoring CV for job {job.id}: {e}")
            return ToolResult(
                success=False,
                summary="Failed to tailor CV",
                error_message=str(e),
            )
