from enterprise_rag.generation.service import GenerationService
from enterprise_rag.retrieval.base import RetrievalProvider
from enterprise_rag.rag.models import Citation, RAGResponse
from enterprise_rag.generation.citations import (
    find_invalid_citation_indices,
)

class RAGService:
    def __init__(
        self,
        retrieval_service: RetrievalProvider,
        generation_service: GenerationService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service

    def answer(
        self,
        question: str,
        limit: int = 5,
        candidate_limit: int = 10,
        similarity_threshold: float = 0.50,
    ) -> RAGResponse:
        

        results = self.retrieval_service.retrieve(
            question=question,
            limit=limit,
            candidate_limit=candidate_limit,
            similarity_threshold=similarity_threshold,
        )

        citations = [
            Citation(
                index=index,
                title=result.title,
                heading=result.heading,
                source=result.source,
                similarity=result.similarity,
            )
            for index, result in enumerate(results, start=1)
        ]

        answer = self.generation_service.generate_answer(
            question=question,
            results=results,
        )

        valid_indices = set(
            range(1, len(results) + 1)
        )

        invalid_citations = find_invalid_citation_indices(
            answer=answer,
            valid_indices=valid_indices,
        )

        if invalid_citations:
            raise ValueError(
                f"Generated answer contains invalid citations: "
                f"{invalid_citations}"
            )

        return RAGResponse(
            answer=answer,
            sources=results,
            citations=citations,
        )