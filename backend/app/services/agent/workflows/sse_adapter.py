"""
backend/app/services/agent/workflows/sse_adapter.py

LangGraph to Server-Sent Events (SSE) Protocol Adapter.
Transforms async generator stream chunks from LangGraph workflows (`ApplyGraph`, `CopilotGraph`)
into deterministic JSON event frames expected by `frontend/src/context/AgentContext.jsx`:
- `thought`
- `tool_start`
- `tool_complete`
- `proposal_created`
- `text_chunk`
- `done`
"""

import json
import logging
from typing import Any, AsyncGenerator, Dict, Optional

logger = logging.getLogger(__name__)


def format_sse_frame(data: Dict[str, Any]) -> str:
    """Formats a Python dictionary as a standard SSE data line."""
    return f"data: {json.dumps(data)}\n\n"


def dump_model(obj: Any) -> Any:
    """Serializes Pydantic models cleanly using model_dump() or dict()."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return obj


def get_field(obj: Any, key: str, default: Any = None) -> Any:
    """Safely extracts field from either Pydantic model or dict."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class LangGraphSSEAdapter:
    """
    Translates LangGraph stream chunks into SSE events.
    """

    @staticmethod
    async def stream_apply_graph(
        graph_stream: AsyncGenerator[Dict[str, Any], None],
        conversation_id: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Consumes updates from `apply_graph.astream(..., stream_mode='updates')`
        and yields SSE frames.
        """
        # Yield initial thinking frame
        yield format_sse_frame({
            "type": "thought",
            "content": "Initiating autonomous job application workflow...",
        })

        last_status = "working"

        async for chunk in graph_stream:
            if not isinstance(chunk, dict):
                continue

            for node_name, node_output in chunk.items():
                if not isinstance(node_output, dict):
                    continue

                if node_name == "analyze_fit":
                    fit = node_output.get("fit_result")
                    score = get_field(fit, "overall_score", 0)
                    company = get_field(fit, "company", "Target Company")
                    role = get_field(fit, "role", "Target Role")
                    should_proceed = get_field(fit, "should_proceed", True)

                    yield format_sse_frame({
                        "type": "thought",
                        "content": f"Evaluated 4D career alignment for {company} ({role}): Score {score}/100.",
                    })
                    yield format_sse_frame({
                        "type": "tool_complete",
                        "tool": "analyze_fit",
                        "output": dump_model(fit),
                        "ui_widget": {
                            "type": "FitAnalysisCard",
                            "props": {
                                "company": company,
                                "role": role,
                                "overall_score": score,
                                "should_proceed": should_proceed,
                            },
                        },
                    })

                elif node_name == "detect_method":
                    info = node_output.get("channel_info", {})
                    channel = get_field(info, "channel_type", "generic_web")
                    platform = get_field(info, "platform_name", "Web Portal")
                    recruiter = get_field(info, "recruiter_email")

                    yield format_sse_frame({
                        "type": "thought",
                        "content": f"Channel detected: {channel.replace('_', ' ').title()} on {platform}."
                                   + (f" Contact: {recruiter}" if recruiter else ""),
                    })
                    yield format_sse_frame({
                        "type": "tool_complete",
                        "tool": "detect_method",
                        "output": info,
                        "ui_widget": {
                            "type": "ChannelDetectionCard",
                            "props": info,
                        },
                    })

                elif node_name == "draft_cv":
                    draft = node_output.get("cv_draft")
                    yield format_sse_frame({
                        "type": "thought",
                        "content": "Senior Recruiter AI drafted tailored LaTeX CV within 1-2 page budget.",
                    })
                    yield format_sse_frame({
                        "type": "tool_complete",
                        "tool": "draft_cv",
                        "output": dump_model(draft),
                    })

                elif node_name == "review_cv":
                    review = node_output.get("cv_review")
                    fact_passed = get_field(review, "fact_audit_passed", True)
                    ats_score = get_field(review, "ats_score", 0.0)
                    pages = get_field(review, "computed_page_count", 1)

                    yield format_sse_frame({
                        "type": "thought",
                        "content": f"Senior Recruiter review pass completed. Fact Audit: {'PASS' if fact_passed else 'FLAG'}. ATS Score: {ats_score:.1f}%. Pages: {pages}.",
                    })
                    yield format_sse_frame({
                        "type": "tool_complete",
                        "tool": "review_cv",
                        "output": dump_model(review),
                        "ui_widget": {
                            "type": "TailoredResumeCard",
                            "props": {
                                "fact_passed": fact_passed,
                                "ats_score": ats_score,
                                "pages": pages,
                            },
                        },
                    })

                elif node_name == "draft_outreach":
                    outreach = node_output.get("outreach")
                    subject = get_field(outreach, "subject_line")
                    yield format_sse_frame({
                        "type": "thought",
                        "content": f"Tailored outreach generated: {subject or 'Direct Application'}.",
                    })
                    yield format_sse_frame({
                        "type": "tool_complete",
                        "tool": "draft_outreach",
                        "output": dump_model(outreach),
                    })

                elif node_name == "assemble_package":
                    package = node_output.get("package_ref")
                    proposal_id = node_output.get("proposal_id")
                    downgrade = node_output.get("downgrade_reason")

                    company = get_field(package, "company_name", "Company")
                    role = get_field(package, "role_title", "Role")
                    content_hash = get_field(package, "content_hash")

                    yield format_sse_frame({
                        "type": "thought",
                        "content": "Canonical package assembled and verified against Fact Ledger.",
                    })
                    yield format_sse_frame({
                        "type": "proposal_created",
                        "proposal": {
                            "proposal_id": proposal_id,
                            "company": company,
                            "role": role,
                            "downgrade_reason": downgrade,
                            "content_hash": content_hash,
                        },
                        "ui_widget": {
                            "type": "SendApprovalGate",
                            "props": {
                                "proposal_id": proposal_id,
                                "company": company,
                                "role": role,
                                "downgrade_reason": downgrade,
                                "content_hash": content_hash,
                            },
                        },
                    })

                elif node_name == "needs_edit":
                    last_status = "needs_edit"
                    yield format_sse_frame({
                        "type": "thought",
                        "content": "Fact audit verification flagged unverified statements after self-correction retry. Halting workflow for human review.",
                    })
                    yield format_sse_frame({
                        "type": "error",
                        "error": "CV tailoring failed fact audit: unverified claims detected after self-correction retry.",
                    })

                elif node_name == "hitl_gate":
                    yield format_sse_frame({
                        "type": "thought",
                        "content": "Execution paused at Human-in-the-Loop Send Approval Gate.",
                    })

                elif node_name == "dispatch":
                    last_status = "queued_in_hold"
                    yield format_sse_frame({
                        "type": "thought",
                        "content": "Application authorized. Successfully enqueued into Outbox hold queue.",
                    })

        # Final termination frame
        yield format_sse_frame({
            "type": "done",
            "conversation_id": conversation_id or "apply-thread",
            "status": last_status,
        })
