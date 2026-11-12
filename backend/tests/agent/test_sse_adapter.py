"""
backend/tests/agent/test_sse_adapter.py

Unit tests for LangGraph to SSE protocol adapter.
Verifies format_sse_frame, event translation, widget wrapping, and stream integrity.
"""

import json
import pytest
from app.services.agent.workflows.sse_adapter import LangGraphSSEAdapter, format_sse_frame
from app.services.agent.workflows.state import ApplicationPackageRef


def parse_sse_event(sse_str: str) -> dict:
    """Helper to parse a single data: {...}\n\n frame."""
    assert sse_str.startswith("data: ")
    assert sse_str.endswith("\n\n")
    return json.loads(sse_str[6:-2])


@pytest.mark.asyncio
async def test_sse_adapter_stream_lifecycle():
    """Verifies that LangGraph node output chunks translate into standard SSE frames."""

    async def mock_graph_stream():
        yield {
            "analyze_fit": {
                "fit_result": {
                    "company": "DeepMind",
                    "role": "Lead AI Engineer",
                    "overall_score": 92,
                    "should_proceed": True,
                }
            }
        }
        yield {
            "detect_method": {
                "channel_info": {
                    "channel_type": "email",
                    "platform_name": "Company Career Portal",
                    "recruiter_email": "jobs@deepmind.com",
                }
            }
        }
        yield {
            "assemble_package": {
                "package_ref": ApplicationPackageRef(
                    application_id="app-1234",
                    job_id="job-5678",
                    company_name="DeepMind",
                    role_title="Lead AI Engineer",
                    channel="email",
                    ats_score=90.0,
                    content_hash="abcde12345",
                ),
                "proposal_id": "prop-5678",
                "downgrade_reason": None,
            }
        }

    frames = []
    async for sse_chunk in LangGraphSSEAdapter.stream_apply_graph(mock_graph_stream(), "conv-101"):
        frames.append(parse_sse_event(sse_chunk))

    # 1. First frame is initial thought
    assert frames[0]["type"] == "thought"
    assert "Initiating" in frames[0]["content"]

    # 2. Contains analyze_fit tool_complete with FitAnalysisCard widget
    fit_frame = next(f for f in frames if f.get("tool") == "analyze_fit")
    assert fit_frame["type"] == "tool_complete"
    assert fit_frame["ui_widget"]["type"] == "FitAnalysisCard"
    assert fit_frame["ui_widget"]["props"]["overall_score"] == 92

    # 3. Contains assemble_package proposal_created with SendApprovalGate widget
    proposal_frame = next(f for f in frames if f["type"] == "proposal_created")
    assert proposal_frame["proposal"]["company"] == "DeepMind"
    assert proposal_frame["ui_widget"]["type"] == "SendApprovalGate"
    assert proposal_frame["ui_widget"]["props"]["content_hash"] == "abcde12345"

    # 4. Final frame is done
    assert frames[-1]["type"] == "done"
    assert frames[-1]["conversation_id"] == "conv-101"

