from enterprise_rag.embeddings.base import EmbeddingProvider
from enterprise_rag.retrieval.vector_search import (
    SearchResult,
    VectorSearchRepository,
)


class RetrievalService:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        search_repository: VectorSearchRepository,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.search_repository = search_repository

    def retrieve(
        self,
        question: str,
        limit: int = 5,
        document_type: str | None = None,
        similarity_threshold: float = 0.50,
    ) -> list[SearchResult]:
        query_embedding = self.embedding_provider.embed_text(question)

        results = self.search_repository.search(
            query_embedding=query_embedding,
            limit=limit,
            document_type=document_type,
        )

        return [
        result
        for result in results
        if result.similarity >= similarity_threshold
    ]