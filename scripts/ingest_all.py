from pathlib import Path

from enterprise_rag.database.repository import DocumentRepository
from enterprise_rag.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingProvider,
)
from enterprise_rag.ingestion.pipeline import IngestionPipeline


def main() -> None:
    embedding_provider = SentenceTransformerEmbeddingProvider()
    repository = DocumentRepository()

    pipeline = IngestionPipeline(
        embedding_provider=embedding_provider,
        repository=repository,
    )

    documents = [
        (
            Path("data/synthetic/product_docs/authentication.md"),
            "product_documentation",
        ),
        (
            Path("data/synthetic/release_notes/v2.18.md"),
            "release_note",
        ),
        (
            Path("data/synthetic/incidents/INC-482.md"),
            "incident",
        ),
        (
            Path("data/synthetic/runbooks/login_failures.md"),
            "runbook",
        ),
    ]

    for file_path, document_type in documents:
        chunk_count = pipeline.ingest_markdown(
            file_path=file_path,
            document_type=document_type,
        )

        print(
            f"Successfully ingested {file_path} "
            f"with {chunk_count} chunk(s)"
        )


if __name__ == "__main__":
    main()