import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_session_factory
from app.models.llm_provider import LLMProviderConfig
from app.services.llm.base import LLMProvider
from app.services.llm.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class LLMService:
    """
    LLM service router matching ARCHITECTURE.md §11 & AGENTS.md.
    Every model call goes through generate(prompt, context).
    Resolves providers from the llm_providers table and supports automatic failover.
    """

    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        db_session: Optional[Session] = None,
        account_id: Optional[str] = None,
    ):
        self._explicit_provider = provider
        self._db_session = db_session
        self.account_id = account_id

    def _resolve_providers(self) -> List[LLMProvider]:
        """Resolve ordered list of active providers from database or defaults."""
        if self._explicit_provider:
            return [self._explicit_provider]

        session = self._db_session
        close_session = False
        if session is None:
            factory = get_session_factory()
            session = factory()
            close_session = True

        providers: List[LLMProvider] = []
        try:
            # Query tenant-specific overrides and platform defaults
            query = session.query(LLMProviderConfig).filter(
                LLMProviderConfig.is_active == True
            )
            if self.account_id:
                query = query.filter(
                    (LLMProviderConfig.account_id == self.account_id) | (LLMProviderConfig.account_id == None)
                )
            else:
                query = query.filter(LLMProviderConfig.account_id == None)

            configs = query.order_by(LLMProviderConfig.priority.asc()).all()

            for cfg in configs:
                api_key = cfg.encrypted_api_key or settings.OPENAI_API_KEY
                if cfg.provider.lower() == "openai":
                    providers.append(
                        OpenAIProvider(
                            api_key=api_key,
                            model_name=cfg.model_name,
                            default_config=cfg.config or {},
                        )
                    )
                # Additional providers (Anthropic, Gemini) can be registered here as rows in the table
        except Exception as e:
            logger.warning(f"Could not load providers from DB ({e}), falling back to default OpenAI provider.")
        finally:
            if close_session:
                session.close()

        # Fallback Chain Backup ("Last Hope"):
        # If settings.OPENAI_API_KEY is available, ensure a bedrock OpenAI fallback
        # exists at the end of the chain so that if configured models fail,
        # the request automatically falls back to this reliable safety net.
        if settings.OPENAI_API_KEY:
            fallback_model = "gpt-4o-mini"
            if not providers:
                providers.append(
                    OpenAIProvider(
                        api_key=settings.OPENAI_API_KEY,
                        model_name=fallback_model,
                    )
                )
            elif any(getattr(p, "model_name", None) != fallback_model for p in providers):
                providers.append(
                    OpenAIProvider(
                        api_key=settings.OPENAI_API_KEY,
                        model_name=fallback_model,
                    )
                )

        return providers

    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Execute generation across the provider chain with automatic fallback.
        """
        providers = self._resolve_providers()
        last_exception = None

        for idx, provider in enumerate(providers):
            try:
                return await provider.generate(prompt=prompt, context=context, **kwargs)
            except Exception as e:
                logger.warning(
                    f"LLM provider #{idx + 1} ({provider.__class__.__name__}) failed: {e}. Trying fallback if available."
                )
                last_exception = e

        raise RuntimeError(f"All configured LLM providers failed. Last error: {last_exception}")
