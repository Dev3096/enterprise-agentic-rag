from fastapi.testclient import TestClient
from enterprise_rag.api.dependencies import get_rag_service
from enterprise_rag.rag.models import RAGResponse
from enterprise_rag.rag.models import Citation
from pprint import pprint
from enterprise_rag.generation.exceptions import CitationValidationError, MISSING_CITATIONS, INVALID_CITATIONS
from typing import Never
import pytest
from collections.abc import Generator

from apps.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["service"] == "enterprise-agentic-rag"


class FakeRAGService:
    def __init__(self):
        self.last_question: str | None = None

    def answer(self, question: str) -> RAGResponse:
        self.last_question = question
        return RAGResponse(answer="This is the response", sources=[], 
                        citations=[Citation(index= 1, title= "INC-432", heading= "Root Cause", source="incidents/INC-482.md", similarity= 0.91)])

class FakeInvalidCitationRAGService:
    def __init__(self):
        self.last_question: str | None = None

    def answer(self, question: str) -> Never:
        self.last_question = question
        raise CitationValidationError(reason= INVALID_CITATIONS, message= "Generated answer contains invalid citations: [7]")

fake_rag_service = FakeRAGService()

def fake_get_rag_service() -> FakeRAGService:
    return fake_rag_service

fake_rag_service_exception = FakeInvalidCitationRAGService()

def fake_exception_rag_service() -> FakeInvalidCitationRAGService:
    return fake_rag_service_exception

app.dependency_overrides[get_rag_service] = fake_get_rag_service 


def test_ask_endpoint() -> None:
    response = client.post("/ask", json= {"question": "Why are TOKEN_EXPIRED errors increasing?"})
    assert response.status_code == 200
    assert fake_rag_service.last_question== "Why are TOKEN_EXPIRED errors increasing?"
    body = response.json()
    assert body["answer"] == "This is the response"
    assert body["citations"][0]["heading"] == "Root Cause" 

def test_ask_endpoint_invalid_citation(override_with_invalid_citation_service) -> None:
    response = client.post("/ask", json= {"question": "Why are TOKEN_EXPIRED errors increasing?"})
    assert response.status_code == 500
    body = response.json()
    assert body["error"] == INVALID_CITATIONS
    assert body["message"] == "Generated answer contains invalid citations: [7]"

@pytest.fixture
def override_with_invalid_citation_service() -> Generator[None, None, None]:
    current_value = app.dependency_overrides.get(get_rag_service)
    app.dependency_overrides[get_rag_service] = fake_exception_rag_service
    yield
    if current_value is None:
        app.dependency_overrides.pop(get_rag_service, None)
    else:
        app.dependency_overrides[get_rag_service] = current_value

@pytest.fixture(autouse=True)
def reset_fake_rag_service() -> None:
    fake_rag_service.last_question = None
    
def test_white_space_only_question() -> None:
    response = client.post("/ask", json= {"question": " "})
    assert response.status_code == 422
    assert fake_rag_service.last_question is None