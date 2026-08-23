from enterprise_rag.database.connection import get_connection
from enterprise_rag.models.document import Document, DocumentChunk
from psycopg.types.json import Jsonb


class DocumentRepository:

    def save_document(self, document: Document) -> None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO documents (
                        id,
                        title,
                        source,
                        document_type,
                        metadata
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        document.id,
                        document.title,
                        document.source,
                        document.document_type,
                        Jsonb(document.metadata),
                    ),
                )

    def save_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding")

        with get_connection() as connection:
            with connection.cursor() as cursor:
                for chunk, embedding in zip(chunks, embeddings, strict=True):
                    cursor.execute(
                        """
                        INSERT INTO document_chunks (
                            id,
                            document_id,
                            chunk_index,
                            content,
                            metadata,
                            embedding
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            chunk.id,
                            chunk.document_id,
                            chunk.chunk_index,
                            chunk.content,
                            Jsonb(chunk.metadata),
                            embedding,
                        ),
                    )