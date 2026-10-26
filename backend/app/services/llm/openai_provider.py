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
        model_name: str = "gpt-4o-mini",
        default_config: Optional[Dict[str, Any]] = None,
    ):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model_name = model_name
        self.default_config = default_config or {"temperature": 0.2, "max_tokens": 4096}
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

        # Merge defaults with call-specific kwargs
        temperature = kwargs.get("temperature", self.default_config.get("temperature", 0.2))
        max_tokens = kwargs.get("max_tokens", self.default_config.get("max_tokens", 4096))

        payload = {
            "model": kwargs.get("model", self.model_name),
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

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
