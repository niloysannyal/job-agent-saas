import asyncio
from datetime import datetime, timezone
import json
import logging
import re
from typing import Any, AsyncIterator, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.agent import AgentActionProposal, AgentConversation, AgentMessage
from app.models.application import Application
from app.services.agent.base_tool import ToolExecutionContext, ToolResult
from app.services.agent.event_bus import DomainEventBus, ProposalApprovedEvent
from app.services.agent.registry import AgentToolRegistry
from app.services.agent.tools.experience_reflector_tool import ExperienceReflectorTool
from app.services.agent.tools.search_jobs_tool import SearchAndRankJobsTool
from app.services.agent.tools.stage_proposal_tool import StageApplicationProposalTool
from app.services.agent.tools.star_coach_tool import StarCoachTool
from app.services.agent.tools.tailor_cv_tool import AutonomousTailorCVTool
from app.services.agent.tools.track_lifecycle_tool import TrackApplicationLifecycleTool
from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)


AGENT_SYSTEM_PROMPT = """You are JobEazy Career Agent, an autonomous executive career copilot and talent agent with 20 years of technical recruiting and systems engineering expertise.

YOUR MISSION:
Autonomously discover matching opportunities, tailor candidate LaTeX CVs with mathematical ATS alignment, verify strict adherence to the Verified Fact Ledger (NEVER hallucinate unrecorded achievements or degrees), prepare compelling outreach, and guide interview preparation.

NON-NEGOTIABLES:
1. Human-in-the-Loop on Send: You NEVER dispatch external applications or emails automatically. You must always stage an action proposal using the `stage_application_proposal` tool so the candidate can review and click Approve.
2. Anti-Hallucination Barrier: Only reference facts verified in the candidate's canonical profile.
3. Decisive Action: When the user asks you to find jobs, tailor a resume, or prepare interview stories, call the appropriate tool.

AVAILABLE TOOLS:
{tools_doc}

OUTPUT FORMAT:
Always respond with a valid JSON object matching this schema:
{{
  "thought": "<internal reasoning chain explaining your evaluation and next step>",
  "tool_call": {{
    "name": "<tool_name>",
    "arguments": {{ ... }}
  }} or null,
  "message": "<conversational explanation to show the candidate>"
}}
"""


class AgentEngine:
    """
    Core Autonomous Agent Orchestrator.
    Manages conversations, SSE streaming, dynamic tool execution,
    anti-hallucination fact verification, and human-in-the-loop proposals.
    """

    def __init__(
        self,
        account_id: str,
        db_session: Session,
        user_email: str = "candidate@jobeazy.internal",
        llm_service: Optional[LLMService] = None,
    ):
        self.account_id = account_id
        self.db = db_session
        self.user_email = user_email
        self.llm = llm_service or LLMService(db_session=self.db, account_id=self.account_id)
        self.registry = AgentToolRegistry()
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        self.registry.register(SearchAndRankJobsTool())
        self.registry.register(AutonomousTailorCVTool())
        self.registry.register(StageApplicationProposalTool())
        self.registry.register(TrackApplicationLifecycleTool())
        self.registry.register(StarCoachTool())
        self.registry.register(ExperienceReflectorTool())

    def _build_tools_documentation(self) -> str:
        lines = []
        for tool in self.registry.list_tools():
            schema = tool.input_schema.model_json_schema().get("properties", {})
            params_str = ", ".join(f"{k}: {v.get('type', 'any')}" for k, v in schema.items())
            lines.append(f"- `{tool.name}({params_str})`: {tool.description}")
        return "\n".join(lines)

    async def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> AgentConversation:
        if conversation_id:
            convo = self.db.query(AgentConversation).filter(
                AgentConversation.id == conversation_id,
                AgentConversation.account_id == self.account_id
            ).first()
            if convo:
                return convo

        convo = AgentConversation(
            account_id=self.account_id,
            title="Career OS Session",
        )
        self.db.add(convo)
        self.db.commit()
        self.db.refresh(convo)
        return convo

    async def chat_stream(
        self,
        user_text: str,
        conversation_id: Optional[str] = None,
        context_filters: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> AsyncIterator[str]:
        """
        Processes candidate prompt and yields typed SSE frames in real time:
        - {"type": "thought", "content": ...}
        - {"type": "tool_start", "tool": ...}
        - {"type": "tool_complete", "tool": ..., "ui_widget": ...}
        - {"type": "proposal_created", "proposal_id": ..., "ui_widget": ...}
        - {"type": "text_chunk", "content": ...}
        - {"type": "done", "conversation_id": ...}
        """
        convo = await self.get_or_create_conversation(conversation_id)

        # 1. Persist User Message with optional file attachments
        attached_files = attachments or (context_filters or {}).get("attachments", [])
        user_widget = None
        if attached_files:
            user_widget = {
                "type": "AttachmentList",
                "props": {
                    "files": [
                        {
                            "filename": a.get("filename", "file"),
                            "file_type": a.get("file_type", "document"),
                            "size_formatted": a.get("size_formatted", ""),
                            "summary": a.get("summary", ""),
                            "preview_url": a.get("preview_url"),
                        }
                        for a in attached_files
                    ]
                }
            }

        user_msg = AgentMessage(
            conversation_id=convo.id,
            account_id=self.account_id,
            role="user",
            content=user_text,
            ui_widget=user_widget,
        )
        self.db.add(user_msg)
        self.db.commit()

        # Update conversation title from first user message if default
        if convo.title == "Career OS Session" and user_text:
            convo.title = user_text[:35] + ("..." if len(user_text) > 35 else "")
            self.db.commit()

        # 2. Check for deterministic fast-track intent or prepare LLM query
        fast_tool = self._detect_fast_track_tool(user_text, context_filters)
        
        thought_content = ""
        tool_call_dict = None
        assistant_text = ""
        widget_to_render = None
        tool_res_obj = None

        if fast_tool:
            thought_content = f"Detected high-intent query: directing to {fast_tool['name']}."
            tool_call_dict = fast_tool
            assistant_text = f"Executing {fast_tool['name'].replace('_', ' ')} based on your request..."
        else:
            tools_doc = self._build_tools_documentation()
            system_prompt = AGENT_SYSTEM_PROMPT.format(tools_doc=tools_doc)

            # Context history
            recent_msgs = (
                self.db.query(AgentMessage)
                .filter(AgentMessage.conversation_id == convo.id)
                .order_by(AgentMessage.created_at.desc())
                .limit(6)
                .all()
            )
            history_str = "\n".join([f"{m.role.upper()}: {m.content}" for m in reversed(recent_msgs)])

            # Build attachments context block
            attachments_block = ""
            if attached_files:
                att_lines = []
                for att in attached_files:
                    fn = att.get("filename", "file")
                    ft = att.get("file_type", "document")
                    fs = att.get("summary", "")
                    content = att.get("extracted_text", "")
                    att_lines.append(f"--- ATTACHED FILE: {fn} [{ft.upper()}: {fs}] ---\n{content}\n--- END ATTACHED FILE ---")
                attachments_block = "\n\n" + "\n\n".join(att_lines)

            prompt = (
                f"Conversation history:\n{history_str}\n\n"
                f"Active UI Context: {json.dumps(context_filters or {})}\n"
                f"{attachments_block}\n\n"
                f"Candidate Query: {user_text}\n\n"
                f"Respond with JSON (thought, tool_call, message):"
            )

            # Stream initial thought frame
            yield f"event: frame\ndata: {json.dumps({'type': 'thought', 'content': 'Analyzing intent, profile context, and available tools...'})}\n\n"
            await asyncio.sleep(0.05)

            try:
                llm_response = await self.llm.generate(prompt=prompt, context=system_prompt)
                parsed = self._parse_llm_json(llm_response)
                thought_content = parsed.get("thought", "Evaluating next optimal step.")
                tool_call_dict = parsed.get("tool_call")
                assistant_text = parsed.get("message", "")
            except Exception as e:
                logger.warning(f"LLM call or parse failed: {e}. Falling back to default assistant.")
                thought_content = "Falling back to direct conversational mode."
                assistant_text = "I am ready to assist you. You can ask me to search for jobs, tailor your CV for a specific opportunity, or practice STAR interview questions."

        # Emit thought frame
        if thought_content:
            yield f"event: frame\ndata: {json.dumps({'type': 'thought', 'content': thought_content})}\n\n"
            await asyncio.sleep(0.05)

        # 3. Execute Tool if requested
        if tool_call_dict and isinstance(tool_call_dict, dict) and tool_call_dict.get("name"):
            tool_name = tool_call_dict.get("name")
            tool_args = tool_call_dict.get("arguments", {})

            yield f"event: frame\ndata: {json.dumps({'type': 'tool_start', 'tool': tool_name, 'arguments': tool_args})}\n\n"
            await asyncio.sleep(0.05)

            exec_ctx = ToolExecutionContext(
                account_id=self.account_id,
                user_email=self.user_email,
                session_id=convo.id,
                db_session=self.db,
            )

            tool_res: ToolResult = await self.registry.execute_tool(
                tool_name=tool_name,
                ctx=exec_ctx,
                arguments=tool_args,
            )
            tool_res_obj = tool_res

            if tool_res.ui_widget:
                widget_to_render = tool_res.ui_widget

            yield f"event: frame\ndata: {json.dumps({'type': 'tool_complete', 'tool': tool_name, 'success': tool_res.success, 'summary': tool_res.summary, 'ui_widget': tool_res.ui_widget})}\n\n"
            await asyncio.sleep(0.05)

            if tool_res.ui_widget and tool_res.ui_widget.get("type") == "SendApprovalGate":
                proposal_id = tool_res.ui_widget.get("props", {}).get("proposal_id")
                yield f"event: frame\ndata: {json.dumps({'type': 'proposal_created', 'proposal_id': proposal_id, 'ui_widget': tool_res.ui_widget})}\n\n"

            if tool_res.summary:
                assistant_text = (
                    f"{tool_res.summary}\n\n{assistant_text}".strip()
                    if assistant_text and not assistant_text.startswith("Executing")
                    else tool_res.summary
                )

        # 4. Stream response text in realistic typewriter chunks
        if assistant_text:
            chunks = self._chunk_text(assistant_text, size=40)
            for c in chunks:
                yield f"event: frame\ndata: {json.dumps({'type': 'text_chunk', 'content': c})}\n\n"
                await asyncio.sleep(0.02)

        # 5. Persist Assistant Message
        assistant_msg = AgentMessage(
            conversation_id=convo.id,
            account_id=self.account_id,
            role="assistant",
            content=assistant_text,
            thought=thought_content,
            tool_calls=[tool_call_dict] if tool_call_dict else None,
            tool_result=tool_res_obj.model_dump() if tool_res_obj else None,
            ui_widget=widget_to_render,
        )
        self.db.add(assistant_msg)
        self.db.commit()

        # 6. Stream Done Frame
        yield f"event: done\ndata: {json.dumps({'conversation_id': convo.id, 'message_id': assistant_msg.id})}\n\n"

    def _detect_fast_track_tool(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Fast-track common one-click prompt chips and unambiguous commands."""
        t = text.lower().strip()
        ctx = context or {}

        # 1. Search / Radar Scan
        if any(p in t for p in ["run daily radar scan", "scan radar", "find jobs", "search jobs", "show new opportunities"]):
            query = ctx.get("query") or ("python" if "python" in t else "")
            return {"name": "search_and_rank_jobs", "arguments": {"query": query, "limit": 5}}

        # 2. Tailor CV
        if any(p in t for p in ["auto-tailor", "tailor cv", "tailor my cv", "tailor application", "prepare cv"]):
            job_id = ctx.get("job_id")
            if not job_id:
                # Find first active job
                from app.models.job import Job
                first_job = self.db.query(Job).filter(Job.account_id == self.account_id).first()
                if first_job:
                    job_id = first_job.id
            if job_id:
                return {"name": "autonomous_tailor_cv", "arguments": {"job_id": job_id}}

        # 3. Stage Proposal
        if any(p in t for p in ["stage proposal", "stage for approval", "ready to send", "prepare send"]):
            app_id = ctx.get("application_id")
            if not app_id:
                first_app = self.db.query(Application).filter(Application.account_id == self.account_id, Application.status == "draft").first()
                if first_app:
                    app_id = first_app.id
            if app_id:
                return {"name": "stage_application_proposal", "arguments": {"application_id": app_id}}

        # 4. Pipeline Tracking
        if any(p in t for p in ["draft due follow-ups", "follow-up", "pipeline status", "track application", "how many applied"]):
            return {"name": "track_application_lifecycle", "arguments": {"action": "list"}}

        # 5. Interview Prep
        if any(p in t for p in ["practice technical interview", "star interview", "interview coach", "mock interview", "behavioral question"]):
            return {"name": "star_interview_prep", "arguments": {"competency": "system scalability"}}

        # 6. Profile Reflection
        if any(p in t for p in ["what are my skills", "review my profile", "my experience", "reflect candidate profile"]):
            return {"name": "reflect_candidate_profile", "arguments": {"section": "all"}}

        return None

    def _parse_llm_json(self, raw: str) -> Dict[str, Any]:
        """Robustly extracts JSON payload from LLM responses even if wrapped in backticks."""
        raw = raw.strip()
        # Remove markdown codeblocks if present
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
        if match:
            raw = match.group(1).strip()

        try:
            return json.loads(raw)
        except Exception:
            # Fallback: simple text response
            return {
                "thought": "Direct response generated.",
                "tool_call": None,
                "message": raw,
            }

    def _chunk_text(self, text: str, size: int = 40) -> List[str]:
        words = text.split(" ")
        chunks = []
        current = []
        current_len = 0
        for w in words:
            current.append(w)
            current_len += len(w) + 1
            if current_len >= size:
                chunks.append(" ".join(current) + " ")
                current = []
                current_len = 0
        if current:
            chunks.append(" ".join(current))
        return chunks

    async def approve_proposal(self, proposal_id: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes human-in-the-loop approval of an action proposal.
        Enforces tenant isolation and transitions status to 'approved' -> 'executed'.
        """
        proposal = self.db.query(AgentActionProposal).filter(
            AgentActionProposal.id == proposal_id,
            AgentActionProposal.account_id == self.account_id
        ).first()

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found.")

        if proposal.status != "pending":
            return {
                "success": False,
                "message": f"Proposal is already {proposal.status}.",
                "proposal_id": proposal.id,
                "status": proposal.status,
            }

        now = datetime.now(timezone.utc)
        proposal.status = "approved"
        proposal.approved_at = now
        proposal.executed_at = now

        # Execute business logic if target is Application
        if proposal.target_id:
            app = self.db.query(Application).filter(
                Application.id == proposal.target_id,
                Application.account_id == self.account_id
            ).first()
            if app:
                app.sent_at = now
                app.status = "applied"

        self.db.commit()

        # Broadcast domain event
        await DomainEventBus.publish(
            ProposalApprovedEvent(
                account_id=self.account_id,
                proposal_id=proposal.id,
                action_type=proposal.action_type,
            )
        )

        return {
            "success": True,
            "message": f"Proposal '{proposal.title}' approved and executed successfully.",
            "proposal_id": proposal.id,
            "status": "executed",
            "executed_at": now.isoformat(),
        }

    async def reject_proposal(self, proposal_id: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        proposal = self.db.query(AgentActionProposal).filter(
            AgentActionProposal.id == proposal_id,
            AgentActionProposal.account_id == self.account_id
        ).first()

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found.")

        proposal.status = "rejected"
        proposal.updated_at = datetime.now(timezone.utc)
        self.db.commit()

        return {
            "success": True,
            "message": f"Proposal '{proposal.title}' rejected.",
            "proposal_id": proposal.id,
            "status": "rejected",
        }
