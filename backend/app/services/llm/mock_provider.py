from typing import Any, Dict, List, Optional
from app.services.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Deterministic mock provider for unit testing and offline development.
    Can return canned responses or predictable echoes.
    """

    def __init__(self, responses: Optional[List[str]] = None, default_response: str = "Mock generated content"):
        self.responses = list(responses) if responses else []
        self.default_response = default_response
        self.calls: List[Dict[str, Any]] = []

    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        self.calls.append({"prompt": prompt, "context": context, "kwargs": kwargs})
        if self.responses:
            return self.responses.pop(0)
        return self.default_response
