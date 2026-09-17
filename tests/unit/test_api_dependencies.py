from enterprise_rag.api.dependencies import get_rag_service
import pytest
from collections.abc import Generator
import enterprise_rag.api.dependencies as dependencies

@pytest.fixture(autouse=True)
def clear_rag_service_cache() -> Generator[None, None, None]:
    get_rag_service.cache_clear()

    yield

    get_rag_service.cache_clear()

def test_get_rag_service_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_embedding_provider = object()
    fake_vector_search = object()
    fake_reranker = object()
    fake_llm_provider = object()
    monkeypatch.setattr(dependencies, "SentenceTransformerEmbeddingProvider", lambda: fake_embedding_provider)
    monkeypatch.setattr(dependencies, "VectorSearchRepository", lambda: fake_vector_search)
    monkeypatch.setattr(dependencies, "CrossEncoderReranker", lambda: fake_reranker)
    monkeypatch.setattr(dependencies, "OpenAILLMProvider", lambda: fake_llm_provider)
    first_service = get_rag_service()
    second_service = get_rag_service()
    assert first_service is second_service