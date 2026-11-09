import hashlib
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.agent import AgentActionProposal
from app.models.application import Application
from app.models.cv_template import AccountCvVersion
from app.models.job import Job
from app.services.agent.base_tool import BaseAgentTool, ToolCategory, ToolExecutionContext, ToolResult
from app.services.agent.event_bus import DomainEventBus, ProposalCreatedEvent

logger = logging.getLogger(__name__)


class StageProposalInput(BaseModel):
    application_id: str = Field(..., description="ID of the draft Application to stage for human approval")
    action_type: str = Field("SEND_APPLICATION_EMAIL", description="Type of external action: SEND_APPLICATION_EMAIL, DISPATCH_PORTAL, SEND_FOLLOW_UP")
    recipient: Optional[str] = Field(None, description="Optional recipient email or portal contact")
    notes: Optional[str] = Field(None, description="Optional candidate notes or routing instructions")


class StageApplicationProposalTool(BaseAgentTool):
    name: str = "stage_application_proposal"
    description: str = "Stages an application for mandatory Human-in-the-Loop review before any email or application is dispatched. Freezes materials snapshot and renders the SendApprovalGate UI."
    category: ToolCategory = ToolCategory.VERIFICATION
    input_schema = StageProposalInput
    requires_human_approval: bool = True

    async def execute(self, ctx: ToolExecutionContext, params: StageProposalInput) -> ToolResult:
        session = ctx.db_session
        if not session:
            return ToolResult(
                success=False,
                summary="Database session unavailable",
                error_message="Active database session is required to stage proposal.",
            )

        app = session.query(Application).filter(
            Application.id == params.application_id,
            Application.account_id == ctx.account_id
        ).first()

        if not app:
            return ToolResult(
                success=False,
                summary=f"Application {params.application_id} not found",
                error_message=f"Application {params.application_id} does not exist for this account.",
            )

        job = session.query(Job).filter(Job.id == app.job_id).first()
        cv_ver = None
        if app.cv_version_id:
            cv_ver = session.query(AccountCvVersion).filter(AccountCvVersion.id == app.cv_version_id).first()

        cv_latex = getattr(cv_ver, "tailored_latex", "") if cv_ver else ""
        cv_hash = hashlib.sha256(cv_latex.encode("utf-8")).hexdigest()[:16] if cv_latex else "NONE"

        recipient = params.recipient or "hiring-team@" + (job.company.lower().replace(" ", "") if job else "company") + ".com"

        snapshot = {
            "application_id": app.id,
            "job_id": job.id if job else None,
            "job_role": job.role if job else "Target Role",
            "company": job.company if job else "Target Company",
            "channel": app.channel,
            "recipient": recipient,
            "draft_body": app.draft_content or "",
            "cv_sha256": cv_hash,
            "cv_version_id": app.cv_version_id,
            "ats_score": int(cv_ver.ats_score) if cv_ver and cv_ver.ats_score else 85,
        }

        idempotency_key = f"prop_{app.id}_{cv_hash}_{params.action_type}"

        # Check if an existing pending proposal exists
        existing = session.query(AgentActionProposal).filter(
            AgentActionProposal.account_id == ctx.account_id,
            AgentActionProposal.idempotency_key == idempotency_key,
            AgentActionProposal.status == "pending"
        ).first()

        proposal = existing
        if not proposal:
            proposal = AgentActionProposal(
                account_id=ctx.account_id,
                action_type=params.action_type,
                target_id=app.id,
                title=f"Send Application to {snapshot['company']} ({snapshot['job_role']})",
                description=f"Human-in-the-loop review for {snapshot['job_role']} via {app.channel.upper()}",
                payload_snapshot=snapshot,
                status="pending",
                idempotency_key=idempotency_key,
            )
            session.add(proposal)
            session.commit()
            session.refresh(proposal)

        # Broadcast event
        await DomainEventBus.publish(
            ProposalCreatedEvent(
                account_id=ctx.account_id,
                proposal_id=proposal.id,
                action_type=proposal.action_type,
            )
        )

        ui_widget = {
            "type": "SendApprovalGate",
            "version": "1.0",
            "props": {
                "proposal_id": proposal.id,
                "status": proposal.status,
                "title": proposal.title,
                "company": snapshot["company"],
                "role": snapshot["job_role"],
                "recipient": recipient,
                "draft_body": snapshot["draft_body"],
                "ats_score": snapshot["ats_score"],
                "cv_sha256": cv_hash,
            },
            "actions": [
                {
                    "id": "approve",
                    "label": "Approve & Send",
                    "variant": "primary",
                    "payload": {"proposal_id": proposal.id}
                },
                {
                    "id": "reject",
                    "label": "Reject / Revise",
                    "variant": "danger",
                    "payload": {"proposal_id": proposal.id}
                }
            ]
        }

        summary = f"Staged proposal '{proposal.title}' (ID: {proposal.id[:8]}...). Awaiting human approval before dispatch."

        return ToolResult(
            success=True,
            summary=summary,
            data={"proposal_id": proposal.id, "status": proposal.status, "snapshot": snapshot},
            ui_widget=ui_widget,
        )
