from sentence_transformers import CrossEncoder

from enterprise_rag.reranking.base import Reranker
from enterprise_rag.retrieval.vector_search import SearchResult


class CrossEncoderReranker(Reranker):

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ) -> None:
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        limit: int,
    ) -> list[SearchResult]:

        if not results:
            return []

        pairs = [
            (query, result.content)
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(results, scores, strict=True),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        return [
            result
            for result, _ in ranked[:limit]
        ]