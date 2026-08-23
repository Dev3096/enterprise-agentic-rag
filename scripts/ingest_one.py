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

    file_path = Path(
        "data/synthetic/incidents/INC-482.md"
    )

    chunk_count = pipeline.ingest_markdown(
        file_path=file_path,
        document_type="incident",
    )

    print(f"Successfully ingested {file_path}")
    print(f"Chunks created: {chunk_count}")


if __name__ == "__main__":
    main()