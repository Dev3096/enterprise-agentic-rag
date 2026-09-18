from enterprise_rag.api.dependencies import get_rag_service
import pytest
from collections.abc import Generator
import enterprise_rag.api.dependencies as dependencies

@pytest.fixture(autouse=True)
def clear_rag_service_cache() -> Generator[None, None, None]:
    get_rag_service.cache_clear()

    yield

    get_rag_service.cache_clear()

@pytest.fixture
def create_monkey_patch(monkeypatch: pytest.MonkeyPatch) -> Generator[dict[str, object], None, None]:
    fake_embedding_provider = object()
    fake_vector_search = object()
    fake_reranker = object()
    fake_llm_provider = object()
    monkeypatch.setattr(dependencies, "SentenceTransformerEmbeddingProvider", lambda: fake_embedding_provider)
    monkeypatch.setattr(dependencies, "VectorSearchRepository", lambda: fake_vector_search)
    monkeypatch.setattr(dependencies, "CrossEncoderReranker", lambda: fake_reranker)
    monkeypatch.setattr(dependencies, "OpenAILLMProvider", lambda: fake_llm_provider)

    yield {
        "fake_embedding_provider": fake_embedding_provider, 
        "fake_vector_search": fake_vector_search,
        "fake_reranker": fake_reranker,
        "fake_llm_provider": fake_llm_provider
    }


def test_get_rag_service_is_cached(create_monkey_patch: dict[str, object]) -> None:
    first_service = get_rag_service()
    second_service = get_rag_service()
    assert first_service is second_service
    

def test_get_rag_service_wires_dependencies(create_monkey_patch: dict[str, object]) -> None:
    first_service = get_rag_service()
    assert first_service.retrieval_service.embedding_provider is create_monkey_patch["fake_embedding_provider"]
    assert first_service.retrieval_service.search_repository is create_monkey_patch["fake_vector_search"]
    assert first_service.retrieval_service.reranker is create_monkey_patch["fake_reranker"]
    assert first_service.generation_service.llm_provider is create_monkey_patch["fake_llm_provider"]
