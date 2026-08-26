from enterprise_rag.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingProvider,
)
from enterprise_rag.retrieval.service import RetrievalService
from enterprise_rag.retrieval.vector_search import VectorSearchRepository


def main() -> None:
    embedding_provider = SentenceTransformerEmbeddingProvider()
    search_repository = VectorSearchRepository()

    retrieval_service = RetrievalService(
    embedding_provider=embedding_provider,
    search_repository=search_repository,
    )

    question = "Why are customers getting token expired errors after v2.18?"


    # results = retrieval_service.retrieve(
    # question=question,
    # limit=3,
    # document_type="incident",
    # )

    results = retrieval_service.retrieve(
    question=question,
    limit=5,
    similarity_threshold=0.50,
    )

    print(f"\nQuestion: {question}\n")

    for index, result in enumerate(results, start=1):
        print(f"Result #{index}")
        print(f"Similarity: {result.similarity:.4f}")
        print(f"Title: {result.title}")
        print(f"Document Type: {result.document_type}")
        print(f"Source: {result.source}")
        print("Content:")
        print(result.content)
        print("-" * 80)


if __name__ == "__main__":
    main()