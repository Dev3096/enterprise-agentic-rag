from pathlib import Path

from enterprise_rag.database.repository import DocumentRepository
from enterprise_rag.embeddings.base import EmbeddingProvider
from enterprise_rag.ingestion.chunking import chunk_document
from enterprise_rag.ingestion.loaders import load_markdown_document


class IngestionPipeline:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        repository: DocumentRepository,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.repository = repository
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def ingest_markdown(
        self,
        file_path: Path,
        document_type: str,
    ) -> int:
        document = load_markdown_document(
            file_path=file_path,
            document_type=document_type,
        )

        chunks = chunk_document(
            document=document,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        texts = [chunk.content for chunk in chunks]

        embeddings = self.embedding_provider.embed_texts(texts)

        self.repository.save_document(document)

        self.repository.save_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return len(chunks)