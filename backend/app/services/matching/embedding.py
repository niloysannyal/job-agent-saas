import logging
import math
from abc import ABC, abstractmethod
from typing import List, Optional, Sequence

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


def compute_cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """
    Compute cosine similarity between two numeric vectors:
    dot(a, b) / (norm(a) * norm(b))
    Clamped to [0.0, 1.0] for match scoring.
    """
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    sim = dot_product / (norm_a * norm_b)
    # Clamp to [0.0, 1.0]
    return max(0.0, min(1.0, float(sim)))


class EmbeddingClient(ABC):
    """Abstract interface for text embedding generation."""

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embedding vector for a single text string."""
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of text strings."""
        pass


class OpenAIEmbeddingClient(EmbeddingClient):
    """
    Production embedding client backed by OpenAI's Embeddings API (text-embedding-3-small).
    """

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        cleaned = text.strip()
        if not cleaned:
            return [0.0] * 1536

        embeddings = await self.embed_batch([cleaned])
        return embeddings[0] if embeddings else [0.0] * 1536

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings in batches of up to 100 items."""
        if not texts:
            return []

        # Batch inputs to respect API limits
        batch_size = 100
        all_embeddings: List[List[float]] = []

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]
                # Replace empty strings with a single space to avoid OpenAI 400 error
                safe_batch = [t.strip() if t.strip() else " " for t in batch]

                payload = {
                    "input": safe_batch,
                    "model": self.model,
                }

                response = await client.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=payload,
                )

                if response.status_code != 200:
                    err_text = response.text
                    logger.error(f"OpenAI embedding error {response.status_code}: {err_text}")
                    response.raise_for_status()

                data = response.json()
                # Sort by index in case API returns out of order
                items = sorted(data["data"], key=lambda x: x["index"])
                for item in items:
                    all_embeddings.append(item["embedding"])

        return all_embeddings


class MockEmbeddingClient(EmbeddingClient):
    """
    Deterministic mock embedding client for testing without network or GPU.
    Generates normalized 16-dimensional vectors based on word frequencies.
    """

    def __init__(self, dimension: int = 16) -> None:
        self.dimension = dimension

    def _text_to_vector(self, text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * self.dimension

        # Simple deterministic hashing of word tokens across dimension slots
        vec = [0.0] * self.dimension
        words = text.lower().split()
        for w in words:
            slot = abs(hash(w)) % self.dimension
            vec[slot] += 1.0

        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            return [x / norm for x in vec]
        return vec

    async def embed(self, text: str) -> List[float]:
        return self._text_to_vector(text)

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self._text_to_vector(t) for t in texts]


def get_embedding_client(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> EmbeddingClient:
    """
    Factory returning OpenAIEmbeddingClient if API key is provided and valid,
    otherwise MockEmbeddingClient for unit tests and offline environments.
    """
    key = api_key if api_key is not None else settings.OPENAI_API_KEY
    if key and key.strip() and not key.startswith("mock-") and key != "test-key":
        return OpenAIEmbeddingClient(
            api_key=key.strip(),
            model=model or settings.OPENAI_EMBEDDING_MODEL,
        )
    return MockEmbeddingClient()
