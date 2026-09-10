from enterprise_rag.generation.service import GenerationService
from enterprise_rag.rag.service import RAGService
from enterprise_rag.retrieval.vector_search import SearchResult
from tests.fake.fake_llm import FakeLLMProvider
import pytest
from enterprise_rag.generation.exceptions import CitationValidationError, MISSING_CITATIONS, INVALID_CITATIONS


class FakeRetrievalService:
    def __init__(self, results: list[SearchResult]) -> None:
        self.results = results

    def retrieve(
        self,
        question: str,
        limit: int = 5,
        candidate_limit: int = 10,
        similarity_threshold: float = 0.50,
    ) -> list[SearchResult]:
        return self.results


def test_rag_service_retrieves_evidence_and_generates_answer() -> None:
    search_results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            title="INC-482",
            source="incidents/INC-482.md",
            document_type="incident",
            heading="Root Cause",
            heading_path=["INC-482", "Root Cause"],
            content=(
                "The distributed session cache incorrectly invalidated "
                "some refresh-token sessions."
            ),
            similarity=0.91,
        )
    ]

    retrieval_service = FakeRetrievalService(
        results=search_results,
    )

    fake_llm = FakeLLMProvider(
        response=(
            "TOKEN_EXPIRED errors were caused by incorrect "
            "session-cache invalidation [1]."
        )
    )

    generation_service = GenerationService(
        llm_provider=fake_llm,
    )

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        generation_service=generation_service,
    )

    response = rag_service.answer(
        question="Why are customers getting TOKEN_EXPIRED errors?"
    )

    assert response.answer == (
        "TOKEN_EXPIRED errors were caused by incorrect "
        "session-cache invalidation [1]."
    )

    assert len(response.sources) == 1
    assert response.sources[0].title == "INC-482"
    assert response.sources[0].heading == "Root Cause"

    assert len(response.citations) == 1

    citation = response.citations[0]

    assert citation.index == 1
    assert citation.title == "INC-482"
    assert citation.heading == "Root Cause"
    assert citation.source == "incidents/INC-482.md"
    assert citation.similarity == 0.91

    assert fake_llm.last_user_prompt is not None
    assert "INC-482 > Root Cause" in fake_llm.last_user_prompt



def test_rag_service_rejects_invalid_citations() -> None:
    search_results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            title="INC-482",
            source="incidents/INC-482.md",
            document_type="incident",
            heading="Root Cause",
            heading_path=["INC-482", "Root Cause"],
            content=(
                "The distributed session cache incorrectly invalidated "
                "some refresh-token sessions."
            ),
            similarity=0.91,
        )
    ]

    retrieval_service = FakeRetrievalService(
        results=search_results,
    )

    fake_llm = FakeLLMProvider(
        response=(
            "The issue was caused by incorrect "
            "session-cache invalidation [7]."
        )
    )

    generation_service = GenerationService(
        llm_provider=fake_llm,
    )

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        generation_service=generation_service,
    )

    
    with pytest.raises(CitationValidationError) as exc_info:
        rag_service.answer(
            question="Why are customers getting TOKEN_EXPIRED errors?"
        )
    assert str(exc_info.value.reason) == INVALID_CITATIONS

def test_rag_service_rejects_no_citations() -> None:
    search_results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            title="INC-482",
            source="incidents/INC-482.md",
            document_type="incident",
            heading="Root Cause",
            heading_path=["INC-482", "Root Cause"],
            content=(
                "The distributed session cache incorrectly invalidated "
                "some refresh-token sessions."
            ),
            similarity=0.91,
        )
    ]

    retrieval_service = FakeRetrievalService(
        results=search_results,
    )

    fake_llm = FakeLLMProvider(
        response=(
            "The issue was caused by incorrect "
            "session-cache invalidation."
        )
    )

    generation_service = GenerationService(
        llm_provider=fake_llm,
    )

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        generation_service=generation_service,
    )

    with pytest.raises(CitationValidationError) as exc_info:
        rag_service.answer(
            question="Why are customers getting TOKEN_EXPIRED errors?"
        )
    assert str(exc_info.value.reason) == MISSING_CITATIONS


def test_rag_service_handles_no_results() -> None:
    retrieval_service = FakeRetrievalService(
        results=[],
    )

    fake_llm = FakeLLMProvider(
        response="I do not have enough information to answer this question.",
    )

    generation_service = GenerationService(
        llm_provider=fake_llm,
    )

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        generation_service=generation_service,
    )

    response = rag_service.answer(
        question="Why are customers getting TOKEN_EXPIRED errors?"
    )

    assert response.answer == "I do not have enough information to answer this question."
    assert len(response.sources) == 0
    assert len(response.citations) == 0
    assert fake_llm.last_system_prompt is None
    assert fake_llm.last_user_prompt is None

def test_rag_service_handles_multiple_citations() -> None:
    search_results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            title="INC-482",
            source="incidents/INC-482.md",
            document_type="incident",
            heading="Root Cause",
            heading_path=["INC-482", "Root Cause"],
            content=(
                "The distributed session cache incorrectly invalidated "
                "some refresh-token sessions."
            ),
            similarity=0.91,
        ), 
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            title="v2.18",
            source="v2.18 / Known Issues",
            document_type="release_notes",
            heading="Known Issues",
            heading_path=["v2.18", "Known Issues"],
            content=(
                "Some customers using long-lived refresh tokens may experience intermittent "
                "TOKEN_EXPIRED errors after upgrading to version 2.18."
            ),
            similarity=0.98,
        )
    ]

    retrieval_service = FakeRetrievalService(
        results = search_results
    )

    fake_llm = FakeLLMProvider(
        response=(
            "The issue was caused by incorrect "
            "session-cache invalidation [1]."
            "Version 2.18 also had a known issue causing intermittent TOKEN_EXPIRED errors [2]."
        )
    )

    generation_service = GenerationService(
        llm_provider=fake_llm,
    )

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        generation_service=generation_service,
    )

    response = rag_service.answer(
        question="Why are customers getting TOKEN_EXPIRED errors?"
    )
    
    assert len(response.citations) == 2
    assert response.citations[0].index == 1
    assert response.citations[0].title == "INC-482"

    assert response.citations[1].index == 2
    assert response.citations[1].title == "v2.18"





