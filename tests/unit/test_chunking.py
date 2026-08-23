from enterprise_rag.ingestion.chunking import chunk_document
from enterprise_rag.models.document import Document


def test_chunk_document_creates_multiple_chunks():
    document = Document(
        id="doc-1",
        title="Test Document",
        source="test.md",
        document_type="test",
        content="A" * 2000,
    )

    chunks = chunk_document(
        document=document,
        chunk_size=800,
        chunk_overlap=150,
    )

    assert len(chunks) > 1

    assert chunks[0].document_id == "doc-1"

    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_chunk_overlap_must_be_smaller_than_chunk_size():
    document = Document(
        id="doc-1",
        title="Test Document",
        source="test.md",
        document_type="test",
        content="Example",
    )

    try:
        chunk_document(
            document=document,
            chunk_size=100,
            chunk_overlap=100,
        )
    except ValueError:
        return

    raise AssertionError("Expected ValueError")