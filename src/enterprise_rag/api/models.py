from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

class AskRequest(BaseModel):
    question: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
