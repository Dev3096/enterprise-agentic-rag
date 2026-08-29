from abc import ABC, abstractmethod

from enterprise_rag.retrieval.vector_search import SearchResult


class Reranker(ABC):

    @abstractmethod
    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        limit: int,
    ) -> list[SearchResult]:
        pass