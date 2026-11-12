import asyncio
from datetime import datetime, timezone, timedelta
import json
import logging
import re
from typing import Any, AsyncIterator, Dict, List, Optional
import uuid
from sqlalchemy.orm import Session

from app.models.agent import AgentActionProposal, AgentConversation, AgentMessage
from app.models.application import Application
from app.models.dispatch import (
    AccountDispatchSettings,
    ApplicationPdfPayload,
    HoldQueueItem,
    SendAuthorization,
    UserCommand,
)
from app.services.agent.base_tool import ToolExecutionContext, ToolResult
from app.services.agent.event_bus import DomainEventBus, ProposalApprovedEvent
from app.services.agent.registry import AgentToolRegistry
from app.services.agent.tools.experience_reflector_tool import ExperienceReflectorTool
from app.services.agent.tools.search_jobs_tool import SearchAndRankJobsTool
from app.services.agent.tools.stage_proposal_tool import StageApplicationProposalTool
from app.services.agent.tools.star_coach_tool import StarCoachTool
from app.services.agent.tools.tailor_cv_tool import AutonomousTailorCVTool
from app.services.agent.tools.track_lifecycle_tool import TrackApplicationLifecycleTool
from app.services.dispatch.hash_utils import compute_content_hash
from app.services.metering.quota_service import QuotaService, QuotaExceededException
from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)


AGENT_SYSTEM_PROMPT = """You are JobEazy Career Agent, an autonomous executive career copilot and talent agent with 20 years of technical recruiting and systems engineering expertise.

YOUR MISSION:
Autonomously discover matching opportunities, tailor candidate LaTeX CVs with mathematical ATS alignment, verify strict adherence to the Verified Fact Ledger (NEVER hallucinate unrecorded achievements or degrees), prepare compelling outreach, and guide interview preparation.

NON-NEGOTIABLES & STRICT DOMAIN BOUNDARY:
1. STRICT PURPOSE & DOMAIN BOUNDARY (NO ARBITRARY CODE GENERATION):
   - Your sole and exclusive purpose is automating job search, career profiling, CV tailoring, application pipeline management, outreach drafting, and interview coaching.
   - You MUST REFUSE arbitrary coding tasks, general software engineering assignments, writing standalone code/scripts, data structures & algorithms implementations, homework, or general AI queries unrelated to the candidate's job search or interview prep.
   - If the candidate asks you to write code (e.g. 'write a python script to...', 'implement a binary search tree', 'create class Node', 'solve this problem in Python'), politely and firmly DECLINE:
     Explain that your role as JobEazy Career Agent is dedicated solely to finding matching jobs, tailoring resumes, managing applications, and coaching for job interviews. Redirect them to what you can do (e.g., finding relevant engineering roles, tailoring their CV for developer positions, or preparing STAR interview responses).
   - The ONLY code you may ever discuss or generate is:
     (a) LaTeX CV code specifically for the user's CV templates.
     (b) High-level architectural or conceptual talking points specifically framed within a STAR behavioral or system design interview response.
2. Human-in-the-Loop on Send: You NEVER dispatch external applications or emails automatically. You must always stage an action proposal using the `stage_application_proposal` tool so the candidate can review and click Approve.
3. Anti-Hallucination Barrier: Only reference facts verified in the candidate's canonical profile.
4. Decisive Action: When the user asks you to find jobs, tailor a resume, or prepare interview stories, call the appropriate tool.
5. CLEAN & POLISHED PROSE:
   - Your responses must be clean, professional, concise, and structured.
   - Never output raw JSON escape characters, unescaped newlines, or unformatted text blocks. Use clear headings, bullet points, and well-spaced paragraphs.

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

        # 2. Check for deterministic fast-track intent or out-of-scope requests or prepare LLM query
        scope_refusal = self._evaluate_scope_boundary(user_text)
        fast_tool = self._detect_fast_track_tool(user_text, context_filters) if not scope_refusal else None
        
        thought_content = ""
        tool_call_dict = None
        assistant_text = ""
        widget_to_render = None
        tool_res_obj = None

        if scope_refusal:
            thought_content = scope_refusal["thought"]
            tool_call_dict = None
            assistant_text = scope_refusal["message"]
        elif fast_tool:
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

        # Refine conversation title if a specific job target was detected or general topic summarized
        new_title = self._resolve_conversation_title(
            convo=convo,
            user_text=user_text,
            tool_call=tool_call_dict,
            tool_res=tool_res_obj,
            context_filters=context_filters,
        )
        if new_title and (
            convo.title in ("Career OS Session", "Agent Session", "New Application")
            or " - " in new_title
            or convo.title.endswith("...")
        ):
            convo.title = new_title
            self.db.commit()

        # 6. Stream Done Frame with conversation_id and resolved title
        yield f"event: done\ndata: {json.dumps({'conversation_id': convo.id, 'message_id': assistant_msg.id, 'title': convo.title})}\n\n"

    def _resolve_conversation_title(
        self,
        convo: AgentConversation,
        user_text: str,
        tool_call: Optional[Dict[str, Any]] = None,
        tool_res: Optional[ToolResult] = None,
        context_filters: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Determines the conversation title per rules:
        - If a specific job is targeted/applied to: 'Company name - Role'
        - If no specific job is targeted: clean summarized topic label
        """
        ctx = context_filters or {}
        # 1. Check if tool result produced a SendApprovalGate or TailoredApplicationCard
        if tool_res and tool_res.ui_widget:
            props = tool_res.ui_widget.get("props", {})
            company = props.get("company")
            role = props.get("job_role") or props.get("role")
            if company and role:
                return f"{company} - {role}"

        # 2. Check tool call arguments
        if tool_call:
            args = tool_call.get("arguments", {})
            job_id = args.get("job_id")
            if job_id:
                from app.models.job import Job
                job = self.db.query(Job).filter(Job.id == job_id).first()
                if job and job.company and job.role:
                    return f"{job.company} - {job.role}"

        # 3. Check explicit targetJob in context_filters
        target_job = ctx.get("targetJob") or ctx.get("job")
        if isinstance(target_job, dict) and target_job.get("company") and target_job.get("role"):
            return f"{target_job['company']} - {target_job['role']}"

        # 4. Check user_text for explicit regex: e.g. 'at [Company]' / 'for [Role] at [Company]'
        match = re.search(
            r"(?:for|at)\s+([A-Za-z0-9\s/+#.-]+?)\s+at\s+([A-Za-z0-9\s/+#.-]+)",
            user_text,
            re.IGNORECASE,
        )
        if match:
            role_candidate = match.group(1).strip()
            comp_candidate = match.group(2).strip()
            if role_candidate and comp_candidate and not role_candidate.lower().startswith("application"):
                return f"{comp_candidate} - {role_candidate}"

        # 5. Non-specific application / general topic summary
        tool_name = tool_call.get("name") if tool_call else ""
        t_low = user_text.lower()
        if "radar" in t_low or tool_name == "search_and_rank_jobs":
            q = (tool_call.get("arguments", {}).get("query") if tool_call else "") or ""
            return f"Radar Scan: {q.title()}" if q and len(q) < 20 else "Radar Scan: Top Matches"

        if "interview" in t_low or "star" in t_low or tool_name == "star_interview_prep":
            comp = (tool_call.get("arguments", {}).get("competency") if tool_call else "") or "General"
            return f"STAR Coach: {comp.title()}"

        if "profile" in t_low or "skills" in t_low or tool_name == "reflect_candidate_profile":
            return "Candidate Profile & Skills"

        if "follow-up" in t_low or tool_name == "track_application_lifecycle":
            return "Application Pipeline Tracker"

        # Fallback: clean prompt snippet without trailing dots
        clean = re.sub(r"[?!.,;]+$", "", user_text.strip())
        if len(clean) > 32:
            return clean[:30] + "..."
        return clean.capitalize() if clean else "New Application"

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

    def _evaluate_scope_boundary(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Enforce strict SaaS scope boundary:
        The Career Copilot agent is dedicated strictly to job search automation,
        LaTeX CV tailoring, application pipeline management, and interview coaching.
        Arbitrary code generation, standalone scripts, algorithms, or programming assignments
        are politely refused and redirected.
        """
        t = text.lower().strip()

        # If it is an explicit career/job/interview/CV task, keep it in scope
        in_scope_markers = [
            "cv", "resume", "latex", "interview", "star", "job", "career",
            "apply", "application", "outreach", "cover letter", "radar",
            "experience", "salary", "portfolio", "headline", "recruiter",
            "hire", "hiring", "posting", "referral"
        ]
        if any(marker in t for marker in in_scope_markers):
            return None

        # Check for standalone code generation / data structure / homework patterns
        code_request_patterns = [
            r"\b(?:write|code|create|generate|implement|build|give me)\s+(?:a|an|the|some)?\s*(?:python|javascript|typescript|java|c\+\+|c#|golang|rust|ruby|php|sql|bash|shell)?\s*(?:script|code|program|function|class|method|algorithm|snippet|solution|data structure)\b",
            r"\b(?:implement|code|write)\s+(?:a|an)?\s*(?:node|binary tree|linked list|stack|queue|hashmap|trie|graph|sorting|quicksort|mergesort|dfs|bfs|dynamic programming)\b",
            r"\b(?:solve|solution for)\s+(?:this\s+)?(?:leetcode|hackerrank|codewars|problem|algorithm|puzzle)\b",
            r"\bclass\s+[A-Za-z0-9_]+\s*:\s*def\s+__init__",
            r"\bdef\s+[a-z0-9_]+\s*\(.*\)\s*:",
        ]

        for pattern in code_request_patterns:
            if re.search(pattern, t):
                return {
                    "thought": "Detected out-of-scope general programming request. My exclusive role is Job Application & Career Copilot.",
                    "tool_call": None,
                    "message": (
                        "I am your dedicated **JobEazy Career Copilot**. My focus is exclusively on automating your job applications, tailoring your CV, managing your pipeline, and preparing you for interviews.\n\n"
                        "I do not generate standalone programming scripts or data structures. However, I can help you with your technical career in several impactful ways:\n\n"
                        "• **Find Software Engineering Roles**: Discover matching developer jobs aligned with your tech stack.\n"
                        "• **Tailor Your CV**: Highlight your software projects, system design achievements, and tech skills for specific job openings.\n"
                        "• **Technical & STAR Interview Coaching**: Practice explaining system design, architectural decisions, and behavioral scenarios.\n\n"
                        "Would you like me to run a job radar scan or tailor your CV for an engineering opportunity?"
                    ),
                }

        return None

    def _clean_assistant_message(self, raw: str) -> str:
        if not raw:
            return ""
        text = raw.strip()
        # Unescape literal escaped newlines if raw JSON string leaked through
        if "\\n" in text and "\n" not in text:
            text = text.replace("\\n", "\n")
        if "\\t" in text:
            text = text.replace("\\t", "  ")
        if '\\"' in text:
            text = text.replace('\\"', '"')
        # Close any unclosed markdown code fence
        if text.count("```") % 2 != 0:
            text += "\n```"
        return text.strip()

    def _parse_llm_json(self, raw: str) -> Dict[str, Any]:
        """Robustly extracts JSON payload from LLM responses even if wrapped in backticks."""
        raw = raw.strip()
        # Remove markdown codeblocks if present
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
        if match:
            raw = match.group(1).strip()

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                if parsed.get("message"):
                    parsed["message"] = self._clean_assistant_message(parsed["message"])
                return parsed
        except Exception:
            pass

        # Fallback: clean text response
        return {
            "thought": "Direct response generated.",
            "tool_call": None,
            "message": self._clean_assistant_message(raw),
        }

    def _chunk_text(self, text: str, size: int = 40) -> List[str]:
        # Split by lines first so newlines are strictly preserved in chunks
        lines = text.split("\n")
        chunks = []
        for line_idx, line in enumerate(lines):
            words = line.split(" ")
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
            # Preserve line break between lines
            if line_idx < len(lines) - 1:
                if chunks:
                    chunks[-1] += "\n"
                else:
                    chunks.append("\n")
        return chunks

    async def approve_proposal(self, proposal_id: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes human-in-the-loop approval of an action proposal.
        Enforces tenant isolation, reserves quota, creates UserCommand, calculates canonical content hash,
        mints SendAuthorization, enqueues HoldQueueItem with undo countdown window,
        and transitions Application to 'queued' (NOT 'applied'; sent_at strictly remains None until dispatch).
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

        # Check if target is an Application for outbound dispatch
        app = None
        if proposal.target_id:
            app = self.db.query(Application).filter(
                Application.id == proposal.target_id,
                Application.account_id == self.account_id
            ).first()

        if app:
            from app.services.dispatch.gateway import SendGateway, SendGatewayException
            try:
                hold_item = SendGateway.queue_application_send(
                    db=self.db,
                    account_id=self.account_id,
                    application=app,
                    source="ui_click",
                    mode="supervised",
                    correlation_id=proposal.id,
                )
            except QuotaExceededException as e:
                return {
                    "success": False,
                    "error_code": "QUOTA_EXCEEDED",
                    "message": str(e),
                    "proposal_id": proposal.id,
                    "status": "pending",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error_code": "DISPATCH_QUEUE_FAILED",
                    "message": str(e),
                    "proposal_id": proposal.id,
                    "status": "pending",
                }

            # Transition states
            proposal.status = "approved"
            proposal.approved_at = now
            proposal.executed_at = now
            self.db.commit()

            # Broadcast domain event
            await DomainEventBus.publish(
                ProposalApprovedEvent(
                    account_id=self.account_id,
                    proposal_id=proposal.id,
                    action_type=proposal.action_type,
                )
            )

            if hold_item.release_at:
                rel = hold_item.release_at if hold_item.release_at.tzinfo else hold_item.release_at.replace(tzinfo=timezone.utc)
                delay_sec = max(0, int((rel - now).total_seconds()))
                release_at_str = rel.isoformat()
            else:
                delay_sec = 30
                release_at_str = None

            return {
                "success": True,
                "message": f"Proposal '{proposal.title}' approved and queued for dispatch with {delay_sec}s undo countdown.",
                "proposal_id": proposal.id,
                "status": "queued",
                "hold_queue_item_id": hold_item.id,
                "authorization_id": hold_item.authorization_id,
                "undo_expires_at": release_at_str,
                "executed_at": now.isoformat(),
            }

        # Non-application proposal approval
        proposal.status = "approved"
        proposal.approved_at = now
        proposal.executed_at = now
        self.db.commit()

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

    async def cancel_hold_dispatch(
        self,
        hold_item_id: Optional[str] = None,
        application_id: Optional[str] = None,
        proposal_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Mid-hold cancel during undo countdown window.
        Reverts application to 'draft', voids authorization, releases quota reservation,
        and sets hold queue item status to 'aborted' with abort_reason='user_cancelled'.
        """
        now = datetime.now(timezone.utc)
        hold_query = self.db.query(HoldQueueItem).filter(HoldQueueItem.account_id == self.account_id)

        if hold_item_id:
            hold_item = hold_query.filter(HoldQueueItem.id == hold_item_id).first()
        elif application_id:
            hold_item = hold_query.filter(
                HoldQueueItem.application_id == application_id,
                HoldQueueItem.status == "pending"
            ).order_by(HoldQueueItem.created_at.desc()).first()
        elif proposal_id:
            prop = self.db.query(AgentActionProposal).filter_by(id=proposal_id, account_id=self.account_id).first()
            if not prop or not prop.target_id:
                raise ValueError(f"Proposal {proposal_id} not found or has no application target.")
            hold_item = hold_query.filter(
                HoldQueueItem.application_id == prop.target_id,
                HoldQueueItem.status == "pending"
            ).order_by(HoldQueueItem.created_at.desc()).first()
        else:
            raise ValueError("Must provide hold_item_id, application_id, or proposal_id to cancel.")

        if not hold_item:
            raise ValueError("No active pending dispatch hold item found to cancel.")

        if hold_item.status != "pending":
            return {
                "success": False,
                "message": f"Cannot cancel dispatch: item is already in '{hold_item.status}' state.",
                "hold_item_id": hold_item.id,
                "status": hold_item.status,
            }

        # 1. Abort hold item
        hold_item.status = "aborted"
        hold_item.abort_reason = "user_cancelled"
        hold_item.error_message = "Cancelled by candidate during undo window."

        # 2. Release quota reservation
        if hold_item.reservation_id:
            QuotaService.release(self.db, hold_item.reservation_id)

        # 3. Void SendAuthorization
        if hold_item.authorization_id:
            auth = self.db.query(SendAuthorization).filter_by(id=hold_item.authorization_id).first()
            if auth:
                auth.status = "voided"
                auth.voided_at = now

        # 4. Revert Application to draft
        app = self.db.query(Application).filter_by(id=hold_item.application_id, account_id=self.account_id).first()
        if app:
            app.status = "draft"
            app.sent_at = None

        # 5. If proposal exists, mark rejected
        if proposal_id:
            prop = self.db.query(AgentActionProposal).filter_by(id=proposal_id, account_id=self.account_id).first()
            if prop:
                prop.status = "rejected"

        self.db.commit()

        return {
            "success": True,
            "message": "Dispatch cancelled successfully. Application reverted to draft.",
            "hold_item_id": hold_item.id,
            "status": "aborted",
            "abort_reason": "user_cancelled",
            "application_status": "draft",
        }

    async def reject_proposal(self, proposal_id: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Rejects a proposal. If it was already approved and is in pending hold, cancels the dispatch.
        """
        proposal = self.db.query(AgentActionProposal).filter(
            AgentActionProposal.id == proposal_id,
            AgentActionProposal.account_id == self.account_id
        ).first()

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found.")

        if proposal.status == "approved":
            # If in hold queue, cancel it
            try:
                return await self.cancel_hold_dispatch(proposal_id=proposal_id)
            except ValueError:
                pass

        proposal.status = "rejected"
        proposal.updated_at = datetime.now(timezone.utc)
        self.db.commit()

        return {
            "success": True,
            "message": f"Proposal '{proposal.title}' rejected.",
            "proposal_id": proposal.id,
            "status": "rejected",
        }
