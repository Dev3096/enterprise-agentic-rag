from enterprise_rag.generation.service import GenerationService
from enterprise_rag.retrieval.vector_search import SearchResult
from tests.fake.fake_llm import FakeLLMProvider


def test_generation_service_builds_grounded_prompt() -> None:
    fake_llm = FakeLLMProvider(
        response="The issue was caused by incorrect session-cache invalidation."
    )

    service = GenerationService(
        llm_provider=fake_llm,
    )

    results = [
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

    answer = service.generate_answer(
        question="Why are customers getting TOKEN_EXPIRED errors?",
        results=results,
    )

    assert answer == (
        "The issue was caused by incorrect session-cache invalidation."
    )

    assert fake_llm.last_system_prompt is not None
    assert fake_llm.last_user_prompt is not None

    assert "Answer only using the provided evidence" in (
        fake_llm.last_system_prompt
    )

    assert "Why are customers getting TOKEN_EXPIRED errors?" in (
        fake_llm.last_user_prompt
    )

    assert "INC-482 > Root Cause" in fake_llm.last_user_prompt

    assert (
        "The distributed session cache incorrectly invalidated"
        in fake_llm.last_user_prompt
    )


def test_generation_service_returns_fallback_when_no_evidence() -> None:
    fake_llm = FakeLLMProvider(
        response="This response should never be used."
    )

    service = GenerationService(
        llm_provider=fake_llm,
    )

    answer = service.generate_answer(
        question="What caused the authentication issue?",
        results=[],
    )

    assert answer == (
        "I do not have enough information to answer this question."
    )

    assert fake_llm.last_system_prompt is None
    assert fake_llm.last_user_prompt is None