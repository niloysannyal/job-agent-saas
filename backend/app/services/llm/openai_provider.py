import logging
from typing import Any, Dict, Optional
import httpx

from app.core.config import settings
from app.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of the LLMProvider interface.
    Uses httpx.AsyncClient for non-blocking asynchronous calls.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        default_config: Optional[Dict[str, Any]] = None,
    ):
        self.api_key = api_key if api_key is not None else settings.OPENAI_API_KEY
        self.model_name = model_name or getattr(settings, "OPENAI_MODEL", "gpt-6-luna")
        self.default_config = default_config or {"max_tokens": 4096}
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is missing. Set OPENAI_API_KEY in .env or configure in llm_providers table."
            )

        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})

        model = kwargs.get("model", self.model_name)

        # Merge defaults with call-specific kwargs
        temperature = kwargs.get("temperature", self.default_config.get("temperature"))
        max_tokens = kwargs.get(
            "max_completion_tokens",
            kwargs.get("max_tokens", self.default_config.get("max_tokens", 4096)),
        )

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
        }

        # Newer OpenAI models (GPT-6 series, o-series reasoning models) require max_completion_tokens
        # rather than max_tokens, and reject non-default temperature values.
        is_reasoning_or_gpt6 = any(
            prefix in model.lower() for prefix in ["gpt-6", "o1", "o3", "o4"]
        )

        if is_reasoning_or_gpt6:
            payload["max_completion_tokens"] = max_tokens
        else:
            payload["max_tokens"] = max_tokens
            if temperature is not None:
                payload["temperature"] = temperature

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return content.strip()
            except httpx.HTTPStatusError as e:
                logger.error(f"OpenAI API HTTP {e.response.status_code} error: {e.response.text}")
                raise RuntimeError(f"OpenAI generation failed: HTTP {e.response.status_code}") from e
            except Exception as e:
                logger.error(f"OpenAI connection error: {e}")
                raise RuntimeError(f"OpenAI request failed: {e}") from e
