from uuid import uuid4

from enterprise_rag.database.connection import get_connection
from enterprise_rag.database.repository import DocumentRepository
from enterprise_rag.models.document import Document, DocumentChunk


def test_save_document():
    repository = DocumentRepository()

    document_id = str(uuid4())

    document = Document(
        id=document_id,
        title="Authentication Guide",
        source="data/synthetic/product_docs/authentication.md",
        document_type="product_documentation",
        content="Sample content for repository test.",
        metadata={
            "product": "authentication",
            "version": "2.18",
        },
    )

    repository.save_document(document)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, source, document_type, metadata
                FROM documents
                WHERE id = %s
                """,
                (document_id,),
            )

            result = cursor.fetchone()

    assert result is not None
    assert str(result[0]) == document_id
    assert result[1] == "Authentication Guide"
    assert result[3] == "product_documentation"
    assert result[4]["product"] == "authentication"

def test_save_chunks():
    repository = DocumentRepository()

    document_id = str(uuid4())

    document = Document(
        id=document_id,
        title="Authentication Guide",
        source="data/synthetic/product_docs/authentication.md",
        document_type="product_documentation",
        content="Sample content for chunk persistence test.",
        metadata={
            "product": "authentication",
        },
    )

    repository.save_document(document)

    chunk = DocumentChunk(
        id=str(uuid4()),
        document_id=document_id,
        chunk_index=0,
        content="Access tokens remain valid for 60 minutes.",
        metadata={
            "section": "Access Tokens",
        },
    )

    embedding = [0.01] * 384

    repository.save_chunks(
        chunks=[chunk],
        embeddings=[embedding],
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    document_id,
                    chunk_index,
                    content,
                    metadata,
                    embedding
                FROM document_chunks
                WHERE id = %s
                """,
                (chunk.id,),
            )

            result = cursor.fetchone()

    assert result is not None
    assert str(result[0]) == document_id
    assert result[1] == 0
    assert result[2] == "Access tokens remain valid for 60 minutes."
    assert result[3]["section"] == "Access Tokens"
    assert len(result[4].to_numpy()) == 384