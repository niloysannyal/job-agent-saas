from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.auth import get_current_account, resolve_tenant_id
from app.db.session import get_db
from app.models.account import Account
from app.models.agent import (
    AgentActionProposal,
    AgentActionProposalRead,
    AgentChatRequest,
    AgentConversation,
    AgentConversationRead,
    AgentMessage,
    AgentMessageRead,
    ProposalApprovalRequest,
)
from app.services.agent.engine import AgentEngine

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/chat")
async def chat_with_agent(
    payload: AgentChatRequest,
    account_id: Optional[str] = Query(None, description="Tenant account ID override for superadmin"),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Real-time streaming agent conversation endpoint.
    Emits Server-Sent Events (SSE) containing thoughts, tool starts/completions,
    staged action proposals, and chunked typewriter responses.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    engine = AgentEngine(
        account_id=tenant_id,
        db_session=db,
        user_email=current_account.email,
    )

    async def sse_event_stream():
        async for chunk in engine.chat_stream(
            user_text=payload.message,
            conversation_id=payload.conversation_id,
            context_filters=payload.context_filters,
        ):
            yield chunk

    return StreamingResponse(
        sse_event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/conversations", response_model=List[AgentConversationRead])
def list_conversations(
    account_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """Lists recent agent conversation sessions for the active tenant."""
    tenant_id = resolve_tenant_id(current_account, account_id)
    convos = (
        db.query(AgentConversation)
        .filter(AgentConversation.account_id == tenant_id)
        .order_by(AgentConversation.updated_at.desc())
        .limit(limit)
        .all()
    )
    return convos


@router.get("/conversations/{conversation_id}", response_model=AgentConversationRead)
def get_conversation(
    conversation_id: str,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """Fetches full conversation history and generative UI widgets."""
    tenant_id = resolve_tenant_id(current_account, account_id)
    convo = (
        db.query(AgentConversation)
        .filter(
            AgentConversation.id == conversation_id,
            AgentConversation.account_id == tenant_id
        )
        .first()
    )
    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found.",
        )
    return convo


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: str,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """Deletes an agent conversation session and all its messages."""
    tenant_id = resolve_tenant_id(current_account, account_id)
    convo = (
        db.query(AgentConversation)
        .filter(
            AgentConversation.id == conversation_id,
            AgentConversation.account_id == tenant_id,
        )
        .first()
    )
    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found.",
        )
    db.delete(convo)
    db.commit()
    return None


@router.get("/proposals", response_model=List[AgentActionProposalRead])
def list_action_proposals(
    account_id: Optional[str] = Query(None),
    proposal_status: Optional[str] = Query(None, description="'pending' | 'approved' | 'rejected' | 'executed'"),
    limit: int = Query(50, ge=1, le=100),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Lists staged Human-in-the-Loop action proposals for review.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    query = db.query(AgentActionProposal).filter(AgentActionProposal.account_id == tenant_id)
    if proposal_status:
        query = query.filter(AgentActionProposal.status == proposal_status)
    return query.order_by(AgentActionProposal.created_at.desc()).limit(limit).all()


@router.post("/proposals/{proposal_id}/approve")
async def approve_proposal(
    proposal_id: str,
    payload: Optional[ProposalApprovalRequest] = None,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Human-in-the-Loop Approval Gate:
    Validates candidate authorization, marks proposal approved/executed,
    and triggers downstream dispatch.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    engine = AgentEngine(
        account_id=tenant_id,
        db_session=db,
        user_email=current_account.email,
    )
    try:
        feedback = payload.feedback if payload else None
        result = await engine.approve_proposal(proposal_id=proposal_id, feedback=feedback)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/proposals/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: str,
    payload: Optional[ProposalApprovalRequest] = None,
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Candidate rejection or request for revision of a staged proposal.
    """
    tenant_id = resolve_tenant_id(current_account, account_id)
    engine = AgentEngine(
        account_id=tenant_id,
        db_session=db,
        user_email=current_account.email,
    )
    try:
        feedback = payload.feedback if payload else None
        result = await engine.reject_proposal(proposal_id=proposal_id, feedback=feedback)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
