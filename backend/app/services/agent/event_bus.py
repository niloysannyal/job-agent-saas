import asyncio
from datetime import datetime, timezone
import logging
from typing import Any, Callable, Coroutine, Dict, List, Type
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DomainEvent(BaseModel):
    account_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_name: str


class JobIngestedEvent(DomainEvent):
    event_name: str = "job_ingested"
    job_ids: List[str]
    source: str


class ApplicationTailoredEvent(DomainEvent):
    event_name: str = "application_tailored"
    application_id: str
    job_id: str
    ats_score: int
    fact_ledger_passed: bool


class ProposalCreatedEvent(DomainEvent):
    event_name: str = "proposal_created"
    proposal_id: str
    action_type: str


class ProposalApprovedEvent(DomainEvent):
    event_name: str = "proposal_approved"
    proposal_id: str
    action_type: str


EventHandler = Callable[[DomainEvent], Coroutine[Any, Any, None]]


class DomainEventBus:
    """
    Decoupled in-memory asynchronous pub/sub Event Bus for domain events.
    Allows services and tools to broadcast state changes without tight coupling.
    """
    _subscribers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    @classmethod
    def subscribe(cls, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed {handler.__name__} to {event_type.__name__}")

    @classmethod
    async def publish(cls, event: DomainEvent) -> None:
        handlers = cls._subscribers.get(type(event), [])
        if not handlers:
            return

        tasks = []
        for handler in handlers:
            try:
                tasks.append(asyncio.create_task(handler(event)))
            except Exception as e:
                logger.error(f"Error launching handler {handler} for {event.event_name}: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
