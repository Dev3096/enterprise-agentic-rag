from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated
from enterprise_rag.rag.models import Citation

class AskRequest(BaseModel):
    question: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]

class CitationResponse(BaseModel):
   index: int
   title: str
   heading: str | None
   source: str
   similarity: float

class AskResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]

