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
    pass