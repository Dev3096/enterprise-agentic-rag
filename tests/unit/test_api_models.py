from enterprise_rag.api.models import AskRequest, CitationResponse, AskResponse
from pydantic import ValidationError
import pytest

def test_request_model() -> None:
    request = AskRequest(question= "Why are TOKEN_EXPIRED errors increasing?")
    assert request.question == "Why are TOKEN_EXPIRED errors increasing?"

def test_request_model_no_question_asked_raises_exception() -> None:
    with pytest.raises(ValidationError):
        AskRequest()

def test_request_model_empty_string() -> None:
    with pytest.raises(ValidationError):
        AskRequest(question="")

def test_request_model_empty_string_whitespaces() -> None:
    with pytest.raises(ValidationError):
        AskRequest(question="   ")

@pytest.mark.parametrize(
    "heading", 
    [
        "Root Cause", 
        None,
    ]
)
def test_citation_response(heading: str | None) -> None:
    citation_response = CitationResponse(index=1, title= "INC-482", heading= heading, source= "incidents/INC-482.md", similarity= 0.91)
    assert citation_response.index == 1
    assert citation_response.title == "INC-482"
    assert citation_response.heading == heading

def test_ask_response_one_citation() -> None:
    citation_response = CitationResponse(index=1, title= "INC-482", heading= "Root Cause", source= "incidents/INC-482.md", similarity= 0.91)
    ask_response = AskResponse(answer= "The session cache caused the issue [1].", citations= [citation_response])
    assert ask_response.answer == "The session cache caused the issue [1]."
    assert len(ask_response.citations) == 1
    assert ask_response.citations[0].index == 1

def test_ask_response_multiple_citation() -> None:
    citation_response_1 = CitationResponse(index=1, title= "INC-482", heading= "Root Cause", source= "incidents/INC-482.md", similarity= 0.91)
    citation_response_2 = CitationResponse(index=2, title= "v2.18", heading= "Known Issue", source= "incidents/V2.18.md", similarity= 0.92)
    ask_response = AskResponse(answer= "The session cache caused the issue [1]. This is a known issue [2]", citations= [citation_response_1, citation_response_2])
    assert ask_response.answer == "The session cache caused the issue [1]. This is a known issue [2]"
    assert len(ask_response.citations) == 2
    assert ask_response.citations[0].index == 1
    assert ask_response.citations[1].index == 2





    
