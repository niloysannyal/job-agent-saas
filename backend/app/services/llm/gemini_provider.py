import logging
from typing import Any, Dict, Optional
import httpx

from app.core.config import settings
from app.services.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """
    Google Gemini implementation of the LLMProvider interface (Gemini 2.5 Flash / Pro).
    Uses httpx.AsyncClient for non-blocking asynchronous calls.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        default_config: Optional[Dict[str, Any]] = None,
    ):
        self.api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self.model_name = model_name or getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        self.default_config = default_config or {"max_tokens": 4096}

    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        if not self.api_key:
            raise ValueError(
                "Gemini API key is missing. Set GEMINI_API_KEY in .env or configure in llm_providers table."
            )

        model = kwargs.get("model", self.model_name)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        payload: Dict[str, Any] = {"contents": contents}

        if context:
            payload["systemInstruction"] = {"parts": [{"text": context}]}

        generation_config: Dict[str, Any] = {}
        max_tokens = kwargs.get("max_tokens", self.default_config.get("max_tokens", 4096))
        if max_tokens:
            generation_config["maxOutputTokens"] = max_tokens
        temperature = kwargs.get("temperature", self.default_config.get("temperature"))
        if temperature is not None:
            generation_config["temperature"] = temperature

        if generation_config:
            payload["generationConfig"] = generation_config

        params = {"key": self.api_key}
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, params=params, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    raise RuntimeError("Gemini returned empty candidates list")
                parts = candidates[0].get("content", {}).get("parts", [])
                text_parts = [part.get("text", "") for part in parts if "text" in part]
                result = "".join(text_parts)
                return result.strip()
            except httpx.HTTPStatusError as e:
                logger.error(f"Gemini API HTTP {e.response.status_code} error: {e.response.text}")
                raise RuntimeError(f"Gemini generation failed: HTTP {e.response.status_code}") from e
            except Exception as e:
                logger.error(f"Gemini connection error: {e}")
                raise RuntimeError(f"Gemini request failed: {e}") from e

