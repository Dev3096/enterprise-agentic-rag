from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    title: str
    source: str
    document_type: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)