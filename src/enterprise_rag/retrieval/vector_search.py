from dataclasses import dataclass

from enterprise_rag.database.connection import get_connection


@dataclass
class SearchResult:
    chunk_id: str
    document_id: str
    title: str
    source: str
    document_type: str
    heading: str | None
    heading_path: list[str]
    content: str
    similarity: float


class VectorSearchRepository:
    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
        document_type: str | None = None,
    ) -> list[SearchResult]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                if document_type is None:
                    cursor.execute(
                        """
                        SELECT
                            c.id,
                            c.document_id,
                            d.title,
                            d.source,
                            d.document_type,
                            c.metadata->>'heading' AS heading,
                            c.metadata->'heading_path' AS heading_path,
                            c.content,
                            1 - (c.embedding <=> %s::vector) AS similarity
                        FROM document_chunks c
                        JOIN documents d
                            ON d.id = c.document_id
                        ORDER BY c.embedding <=> %s::vector
                        LIMIT %s
                        """,
                        (
                            query_embedding,
                            query_embedding,
                            limit,
                        ),
                    )

                else:
                    cursor.execute(
                        """
                        SELECT
                            c.id,
                            c.document_id,
                            d.title,
                            d.source,
                            d.document_type,
                            c.metadata->>'heading' AS heading,
                            c.metadata->'heading_path' AS heading_path,
                            c.content,
                            1 - (c.embedding <=> %s::vector) AS similarity
                        FROM document_chunks c
                        JOIN documents d
                            ON d.id = c.document_id
                        WHERE d.document_type = %s
                        ORDER BY c.embedding <=> %s::vector
                        LIMIT %s
                        """,
                        (
                            query_embedding,
                            document_type,
                            query_embedding,
                            limit,
                        ),
                    )

                rows = cursor.fetchall()

        return [
            SearchResult(
                chunk_id=str(row[0]),
                document_id=str(row[1]),
                title=row[2],
                source=row[3],
                document_type=row[4],
                heading=row[5],
                heading_path=row[6] or [],
                content=row[7],
                similarity=float(row[8]),
            )
            for row in rows
        ]