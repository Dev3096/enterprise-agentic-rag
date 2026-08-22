from pathlib import Path

from enterprise_rag.ingestion.loaders import load_markdown_document


def test_load_markdown_document(tmp_path: Path):
    test_file = tmp_path / "example.md"

    test_file.write_text(
        "# Example\n\nThis is a test document.",
        encoding="utf-8",
    )

    document = load_markdown_document(
        file_path=test_file,
        document_type="test_document",
    )

    assert document.title == "example"
    assert document.document_type == "test_document"
    assert "This is a test document." in document.content
    assert document.metadata["file_extension"] == ".md"