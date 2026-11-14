import logging
from typing import Any, Dict, Optional
import httpx

from app.core.config import settings
from app.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """
    Anthropic implementation of the LLMProvider interface (Claude 3.5 Sonnet / Haiku).
    Uses httpx.AsyncClient for non-blocking asynchronous calls.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        default_config: Optional[Dict[str, Any]] = None,
    ):
        self.api_key = api_key if api_key is not None else settings.ANTHROPIC_API_KEY
        self.model_name = model_name or getattr(settings, "ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.default_config = default_config or {"max_tokens": 4096}
        self.base_url = "https://api.anthropic.com/v1/messages"

    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        if not self.api_key:
            raise ValueError(
                "Anthropic API key is missing. Set ANTHROPIC_API_KEY in .env or configure in llm_providers table."
            )

        model = kwargs.get("model", self.model_name)
        max_tokens = kwargs.get("max_tokens", self.default_config.get("max_tokens", 4096))
        temperature = kwargs.get("temperature", self.default_config.get("temperature"))

        payload: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if context:
            payload["system"] = context
        if temperature is not None:
            payload["temperature"] = temperature

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        timeout = httpx.Timeout(60.0, connect=10.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content_blocks = data.get("content", [])
                text_parts = [
                    block.get("text", "")
                    for block in content_blocks
                    if block.get("type") == "text"
                ]
                result = "".join(text_parts) if text_parts else ""
                return result.strip()
            except httpx.HTTPStatusError as e:
                logger.error(f"Anthropic API HTTP {e.response.status_code} error: {e.response.text}")
                raise RuntimeError(f"Anthropic generation failed: HTTP {e.response.status_code}") from e
            except Exception as e:
                logger.error(f"Anthropic connection error: {e}")
                raise RuntimeError(f"Anthropic request failed: {e}") from e

