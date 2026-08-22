from uuid import uuid4

from enterprise_rag.models.document import Document, DocumentChunk


def chunk_document(
    document: Document,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[DocumentChunk]:

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    text = document.content

    chunks: list[DocumentChunk] = []

    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                DocumentChunk(
                    id=str(uuid4()),
                    document_id=document.id,
                    chunk_index=chunk_index,
                    content=chunk_text,
                    metadata=document.metadata.copy(),
                )
            )

            chunk_index += 1

        start += chunk_size - chunk_overlap

    return chunks