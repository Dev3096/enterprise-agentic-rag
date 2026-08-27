import json
from pathlib import Path

import pytest

from enterprise_rag.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingProvider,
)
from enterprise_rag.retrieval.service import RetrievalService
from enterprise_rag.retrieval.vector_search import VectorSearchRepository


EVALUATION_FILE = Path(
    "data/evaluation/retrieval_cases.json"
)


def load_retrieval_cases() -> list[dict]:
    return json.loads(
        EVALUATION_FILE.read_text(encoding="utf-8")
    )


@pytest.fixture(scope="session")
def retrieval_service() -> RetrievalService:
    embedding_provider = SentenceTransformerEmbeddingProvider()
    search_repository = VectorSearchRepository()

    return RetrievalService(
        embedding_provider=embedding_provider,
        search_repository=search_repository,
    )
@pytest.mark.parametrize(
    "case",
    load_retrieval_cases(),
    ids=lambda case: case["id"],
)
def test_retrieval_quality(
    case,
    retrieval_service: RetrievalService,
    ):

    results = retrieval_service.retrieve(
        question=case["question"],
        limit=5,
        similarity_threshold=0.50,
    )

    matching_results = [
        result
        for result in results
        if result.title == case["expected_title"]
        and case["expected_heading"] in result.content
    ]

    assert matching_results