import math
from abc import ABC, abstractmethod
from typing import List, Sequence


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
