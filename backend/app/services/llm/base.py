from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMProvider(ABC):
    """
    Abstract LLM provider interface matching ARCHITECTURE.md §11 & AGENTS.md.
    Every model call goes through one generate(prompt, context) -> str interface.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate text response given a prompt and optional context.
        
        Args:
            prompt: The instruction or query to the model.
            context: Additional background information (e.g. job posting, CV source).
            **kwargs: Provider-specific overrides (temperature, max_tokens, etc.)
        
        Returns:
            The raw text response from the model.
        """
        pass
