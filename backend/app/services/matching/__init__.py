from app.services.matching.service import MatchingService, MatchingResult
from app.services.matching.profile_parser import ProfileParser, ParsedProfile
from app.services.matching.language_gate import LanguageGate
from app.services.matching.embedding import (
    EmbeddingClient,
    MockEmbeddingClient,
    OpenAIEmbeddingClient,
    compute_cosine_similarity,
    get_embedding_client,
)

__all__ = [
    "MatchingService",
    "MatchingResult",
    "ProfileParser",
    "ParsedProfile",
    "LanguageGate",
    "EmbeddingClient",
    "MockEmbeddingClient",
    "OpenAIEmbeddingClient",
    "compute_cosine_similarity",
    "get_embedding_client",
]
