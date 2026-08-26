import re
from uuid import uuid4

from enterprise_rag.models.document import Document, DocumentChunk


def _split_markdown_sections(
    text: str,
) -> list[tuple[list[str], str]]:
    heading_pattern = re.compile(
        r"^(#{1,6})\s+(.+)$",
        re.MULTILINE,
    )

    matches = list(heading_pattern.finditer(text))

    if not matches:
        return [([], text.strip())]

    sections: list[tuple[list[str], str]] = []

    heading_stack: list[str] = []

    for index, match in enumerate(matches):
        heading_level = len(match.group(1))
        heading_text = match.group(2).strip()

        heading_stack = heading_stack[: heading_level - 1]
        heading_stack.append(heading_text)

        section_start = match.end()

        if index + 1 < len(matches):
            section_end = matches[index + 1].start()
        else:
            section_end = len(text)

        section_content = text[section_start:section_end].strip()

        if section_content:
            sections.append(
                (
                    heading_stack.copy(),
                    section_content,
                )
            )

    return sections


def _split_large_section(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    chunks: list[str] = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def chunk_document(
    document: Document,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[DocumentChunk]:
    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    sections = _split_markdown_sections(
        document.content
    )

    chunks: list[DocumentChunk] = []
    chunk_index = 0

    for heading_path, section_content in sections:
        heading_text = " > ".join(heading_path)

        if heading_text:
            section_text = (
                f"{heading_text}\n\n"
                f"{section_content}"
            )
        else:
            section_text = section_content

        if len(section_text) <= chunk_size:
            section_chunks = [section_text]
        else:
            section_chunks = _split_large_section(
                text=section_text,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

        for section_chunk in section_chunks:
            metadata = document.metadata.copy()

            if heading_path:
                metadata["heading"] = heading_path[-1]
                metadata["heading_path"] = heading_path

            chunks.append(
                DocumentChunk(
                    id=str(uuid4()),
                    document_id=document.id,
                    chunk_index=chunk_index,
                    content=section_chunk,
                    metadata=metadata,
                )
            )

            chunk_index += 1

    return chunks