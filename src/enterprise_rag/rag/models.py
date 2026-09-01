from dataclasses import dataclass

from enterprise_rag.retrieval.vector_search import SearchResult


@dataclass
class Citation:
    index: int
    title: str
    heading: str | None
    source: str
    similarity: float


@dataclass
class RAGResponse:
    answer: str
    sources: list[SearchResult]
    citations: list[Citation]