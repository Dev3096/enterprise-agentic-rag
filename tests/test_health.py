from fastapi.testclient import TestClient
from enterprise_rag.api.dependencies import get_rag_service
from enterprise_rag.rag.models import RAGResponse

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
        return RAGResponse(answer="This is the response", sources=[], citations=[])

fake_rag_service = FakeRAGService()

def fake_get_rag_service() -> FakeRAGService:
    return fake_rag_service

app.dependency_overrides[get_rag_service] = fake_get_rag_service 


def test_ask_endpoint() -> None:
    response = client.post("/ask", json= {"question": "Why are TOKEN_EXPIRED errors increasing?"})
    assert response.status_code == 200
    assert fake_rag_service.last_question== "Why are TOKEN_EXPIRED errors increasing?"
    body = response.json()
    assert body["answer"] == "This is the response"
    assert body["citations"] == []

