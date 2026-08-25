from enterprise_rag.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingProvider,
)
from enterprise_rag.retrieval.vector_search import VectorSearchRepository


def main() -> None:
    embedding_provider = SentenceTransformerEmbeddingProvider()
    search_repository = VectorSearchRepository()

    question = "Why are customers getting token expired errors after v2.18?"

    query_embedding = embedding_provider.embed_text(question)

    results = search_repository.search(
        query_embedding=query_embedding,
        limit=3,
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