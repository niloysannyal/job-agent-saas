from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session


class ToolCategory(str, Enum):
    SOURCING = "sourcing"
    TAILORING = "tailoring"
    VERIFICATION = "verification"
    LIFECYCLE = "lifecycle"
    COACHING = "coaching"
    INTELLIGENCE = "intelligence"


class ToolExecutionContext(BaseModel):
    account_id: str
    user_email: str = "candidate@jobeazy.internal"
    session_id: Optional[str] = None
    db_session: Optional[Any] = Field(None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GenerativeUIWidget(BaseModel):
    type: str = Field(..., description="JobRadarCarousel, TailorDiffReview, SendApprovalGate, STARStoryMatch, etc.")
    version: str = "1.0"
    props: Dict[str, Any] = Field(default_factory=dict)
    actions: List[Dict[str, Any]] = Field(default_factory=list)


class ToolResult(BaseModel):
    success: bool
    summary: str
    data: Optional[Dict[str, Any]] = None
    ui_widget: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class BaseAgentTool(ABC):
    """
    Standardized Hexagonal Agent Tool Port.
    All external or internal autonomous capabilities implement this interface.
    """
    name: str
    description: str
    category: ToolCategory
    input_schema: Type[BaseModel]
    requires_human_approval: bool = False

    @abstractmethod
    async def execute(self, ctx: ToolExecutionContext, params: BaseModel) -> ToolResult:
        """
        Executes the autonomous tool action and returns structured data
        along with an optional Generative UI contract widget.
        """
        pass
