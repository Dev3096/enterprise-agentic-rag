from enterprise_rag.ingestion.chunking import chunk_document
from enterprise_rag.models.document import Document
from textwrap import dedent


def test_chunk_document_preserves_markdown_hierarchy():
    document = Document(
        id="doc-1",
        title="Authentication Guide",
        source="authentication.md",
        document_type="product_documentation",
        content=dedent(
            """
            # Authentication Service

            ## Access Tokens

            Access tokens remain valid for 60 minutes.

            ## Refresh Tokens

            Refresh tokens remain valid for 30 days.

            ## Authentication Errors

            TOKEN_EXPIRED means the access token has expired.
            """
        ).strip(),
    )

    chunks = chunk_document(
        document=document,
        chunk_size=800,
        chunk_overlap=150,
    )

    assert len(chunks) == 3

    assert chunks[0].metadata["heading"] == "Access Tokens"
    assert chunks[0].metadata["heading_path"] == [
        "Authentication Service",
        "Access Tokens",
    ]

    assert chunks[1].metadata["heading"] == "Refresh Tokens"
    assert chunks[1].metadata["heading_path"] == [
        "Authentication Service",
        "Refresh Tokens",
    ]

    assert chunks[2].metadata["heading"] == "Authentication Errors"
    assert chunks[2].metadata["heading_path"] == [
        "Authentication Service",
        "Authentication Errors",
    ]

    assert (
        "Authentication Service > Access Tokens"
        in chunks[0].content
    )

    assert (
        "Access tokens remain valid for 60 minutes."
        in chunks[0].content
    )


def test_chunk_document_splits_large_markdown_section():
    long_content = "A" * 2000

    document = Document(
        id="doc-1",
        title="Large Document",
        source="large.md",
        document_type="test",
        content=f"""
## Large Section

{long_content}
""".strip(),
    )

    chunks = chunk_document(
        document=document,
        chunk_size=800,
        chunk_overlap=150,
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert chunk.metadata["heading"] == "Large Section"


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