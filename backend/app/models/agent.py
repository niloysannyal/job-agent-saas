import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.account import Account


class AgentActionProposal(Base):
    """
    First-Class Action Proposal entity enforcing Human-in-the-Loop on Send.
    Every automated action requiring external interaction or candidate sign-off
    is first staged here before execution.
    """
    __tablename__ = "agent_action_proposals"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    # Multi-tenant isolation
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="e.g. SEND_APPLICATION_EMAIL, STAGE_APPLICATION, SCHEDULE_FOLLOW_UP",
    )
    target_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        nullable=True,
        doc="Target entity ID such as application_id or job_id",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Proposed Agent Action",
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    payload_snapshot: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
        doc="Frozen snapshot of email subject, body, recipient, CV SHA256 hash, etc.",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        doc="'pending' | 'approved' | 'rejected' | 'executed' | 'expired'",
    )
    idempotency_key: Mapped[Optional[str]] = mapped_column(
        String(128),
        index=True,
        nullable=True,
        doc="Deduplication key to avoid multiple dispatches",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    executed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    account: Mapped["Account"] = relationship(
        "Account",
        backref="action_proposals",
        foreign_keys=[account_id],
    )


class AgentConversation(Base):
    """
    Conversation session between user and Career OS Agent.
    """
    __tablename__ = "agent_conversations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Agent Session",
    )
    is_pinned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    account: Mapped["Account"] = relationship(
        "Account",
        backref="agent_conversations",
        foreign_keys=[account_id],
    )
    messages: Mapped[List["AgentMessage"]] = relationship(
        "AgentMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="AgentMessage.created_at",
    )


class AgentMessage(Base):
    """
    Individual turn within an agent conversation, preserving thought traces,
    tool executions, and generative UI descriptors.
    """
    __tablename__ = "agent_messages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    conversation_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("agent_conversations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="'user' | 'assistant' | 'system' | 'tool'",
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )
    thought: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Inner chain-of-thought and reasoning traces",
    )
    tool_calls: Mapped[Optional[Any]] = mapped_column(
        JSON,
        nullable=True,
        doc="Array of tool invocation requests",
    )
    tool_result: Mapped[Optional[Any]] = mapped_column(
        JSON,
        nullable=True,
        doc="Execution result returned by tool adapter",
    )
    ui_widget: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        doc="Generative UI contract payload for rich card rendering",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    conversation: Mapped["AgentConversation"] = relationship(
        "AgentConversation",
        back_populates="messages",
    )


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class AgentActionProposalBase(BaseModel):
    action_type: str
    target_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    payload_snapshot: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    idempotency_key: Optional[str] = None


class AgentActionProposalRead(AgentActionProposalBase):
    id: str
    account_id: str
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class AgentMessageRead(BaseModel):
    id: str
    conversation_id: str
    account_id: str
    role: str
    content: str
    thought: Optional[str] = None
    tool_calls: Optional[Any] = None
    tool_result: Optional[Any] = None
    ui_widget: Optional[Dict[str, Any]] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AgentConversationRead(BaseModel):
    id: str
    account_id: str
    title: str
    is_pinned: bool = False
    created_at: datetime
    updated_at: datetime
    messages: List[AgentMessageRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class AgentConversationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    is_pinned: Optional[bool] = None


class AgentChatRequest(BaseModel):
    message: str = Field(..., description="User query or command for the agent")
    conversation_id: Optional[str] = Field(None, description="Optional existing session ID")
    context_filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Active UI context such as selected job_id or screen")
    attachments: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Uploaded file payloads/extracted content")


class ProposalApprovalRequest(BaseModel):
    feedback: Optional[str] = Field(None, description="Optional instruction or adjustments from user")
