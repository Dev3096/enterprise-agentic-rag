from typing import Protocol

from enterprise_rag.retrieval.vector_search import SearchResult


class RetrievalProvider(Protocol):
    def retrieve(
        self,
        question: str,
        limit: int = 5,
        candidate_limit: int = 10,
        similarity_threshold: float = 0.50,
    ) -> list[SearchResult]:
        ...