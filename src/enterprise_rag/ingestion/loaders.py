from pathlib import Path
from uuid import uuid4

from enterprise_rag.models.document import Document


def load_markdown_document(
    file_path: Path,
    document_type: str,
) -> Document:
    content = file_path.read_text(encoding="utf-8")

    return Document(
        id=str(uuid4()),
        title=file_path.stem,
        source=str(file_path),
        document_type=document_type,
        content=content,
        metadata={
            "file_name": file_path.name,
            "file_extension": file_path.suffix,
        },
    )